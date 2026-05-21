import logging
import os
import re
import json
from typing import Dict
import requests
import functools
from src.shared.utils import random_delay, save_as_json

def disk_cache(dir_attr, key_regex=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(cls, *args, **kwargs):
            # 1. Extraer la llave del caché
            # Si hay regex, buscamos en el primer argumento (address). 
            # Si no, asumimos que el primer argumento es el postal_code.
            raw_key = args[0] if args else kwargs.get("postal_code") or kwargs.get("address")
            
            if key_regex:
                match = re.match(key_regex, str(raw_key))
                cache_key = match[0] if match else None
            else:
                cache_key = raw_key

            cache_dir = getattr(cls, dir_attr)
            cache_filepath = os.path.join(cache_dir, f"{cache_key}.json") if cache_key else None

            # 2. Lógica de Hit
            if cache_filepath and os.path.isfile(cache_filepath):
                cls._logger.info(f"Cache HIT: {cache_key}")
                with open(cache_filepath, "r", encoding="utf-8") as f:
                    return json.load(f)

            # 3. Ejecución de la función original
            result = func(cls, *args, **kwargs)

            # 4. Lógica de Save (Persistencia)
            # Solo guardamos si hay una llave válida y el flag de cache es True
            should_cache = kwargs.get("cache_response_as_json", True)
            if should_cache and cache_key and result:
                save_as_json(result, filename=f"{cache_key}.json", directory=cache_dir)
                cls._logger.info(f"Cache SAVED: {cache_key}")

            return result
        return wrapper
    return decorator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)


class CorreosApi:
    _logger = logging.getLogger("CorreosApi")
    _logger.setLevel(logging.INFO)
    _suggestions_cache_directory = "../data/cache/correos_api/suggestions/"
    _polygon_cache_directory = "../data/cache/correos_api/polygons/"
    _details_cache_directory = "../data/cache/correos_api/details/"
    # delay interval in seconds for random delay between requests
    _delay_interval = (1, 3)
    _suggestions_url = (
        "https://api1.correos.es/digital-services/searchengines/api/v1/suggestions"
    )
    _postal_code_detail_url = (
        "https://api1.correos.es/digital-services/searchengines/api/v1/postalcodes"
    )
    _polygon_detail_url = "https://api1.correos.es/digital-services/searchengines/api/v1/postalcodes/polygon"
    _headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es",
        "Origin": "https://www.correos.es",
        "Priority": "u=1,i",
        "Referer": "https://www.correos.es/",
        "Sec-Ch-Ua": '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-Gpc": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }

    @classmethod
    def set_config(cls, suggestions_cache_directory=None, polygon_cache_directory=None, details_cache_directory=None, delay_interval=None, log_level=None):
        if suggestions_cache_directory is not None:
            cls._suggestions_cache_directory = suggestions_cache_directory
        if polygon_cache_directory is not None:
            cls._polygon_cache_directory = polygon_cache_directory
        if details_cache_directory is not None:
            cls._details_cache_directory = details_cache_directory
        if delay_interval is not None:
            cls._delay_interval = delay_interval
        if log_level is not None:
            cls._logger.setLevel(log_level)

    @classmethod
    def try_get(cls, url, headers, params):
        try:
            random_delay(*cls._delay_interval)
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            response_json = response.json()
            cls._logger.debug(
                f"Successful GET request to {url} with params {params}")
            cls._logger.debug(f"Response status code: {response.status_code}")
            cls._logger.info(f"Response content: {response_json}")
            return response_json
        except requests.RequestException as e:
            cls._logger.error(f"Error fetching data from {url}: {e}")
            return {"error": str(e)}

    @classmethod
    def _check_cache(cls, postal_code: str, cache_directory: str) -> dict | None:
        cache_filepath = os.path.join(cache_directory, f"{postal_code}.json")
        if os.path.isfile(cache_filepath):
            cls._logger.info(f"Cache hit for postal code: {postal_code}")
            with open(cache_filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        cls._logger.info(f"No cache found for postal code: {postal_code}")
        return None

    @classmethod
    @disk_cache("_suggestions_cache_directory")
    def get_postal_code_suggestion(cls, postal_code: str, cache_response_as_json=True) -> Dict:
        
        URL = cls._suggestions_url
        HEADERS = cls._headers
        PARAMS = {"text": postal_code}
        response = cls.try_get(URL, HEADERS, PARAMS)
        code_404 = response.get(
            "code", None
        )  # even though the api returns 200, if the response json contains code 404 it means no suggestions was found
        if code_404 == 404 or not response.get("suggestions", []):
            cls._logger.info(
                f"No suggestions found for postal code: {postal_code}")
            return {}
        
        return response

    @classmethod
    @disk_cache("_details_cache_directory",key_regex='^\d{5}')
    def get_postal_code_detail(
        cls, address: str, latitude: float, longitude: float, cache_response_as_json=True
    ) -> Dict:
        URL = cls._postal_code_detail_url
        PARAMS = {
            # address format must be like suggestions[0].text attribute
            "address": address,
            # latitude should be the suggestions[0].latitude attribute
            "latitude": latitude,
            # longitude should be the suggestions[0].longitude attribute
            "longitude": longitude,
        }
        HEADERS = cls._headers
        return cls.try_get(URL, HEADERS, PARAMS)
        

    @classmethod
    @disk_cache("_polygon_cache_directory")
    def get_postal_code_polygon(cls, postal_code: str, distance: int = 0, cache_response_as_json=True) -> dict:
       
        URL = cls._polygon_detail_url
        PARAMS = {"postalcode": postal_code, "distance": distance}
        HEADERS = cls._headers
        return cls.try_get(URL, HEADERS, PARAMS)

    @classmethod
    def get_coords_from_postal_code(cls, postal_code: str, save_geojson: bool = False, geojson_directory: str = "../data/silver/geojson/") -> tuple[float, float] | tuple[None, None]:
        suggestions = cls.get_postal_code_suggestion(postal_code).get("suggestions", None)
        suggestion = suggestions[0] if suggestions else None
        if not suggestion:
            return None, None
        latitude = suggestion.get("latitude", None)
        longitude = suggestion.get("longitude", None)
        if latitude is None or longitude is None:
            cls._logger.info(
                f"Coordinates not found in suggestion for postal code: {postal_code}")
            return None, None

        if save_geojson:
            geojson_filename = f"{postal_code}_polygon.geojson"
            if not os.path.isfile(f"{geojson_directory}{geojson_filename}"):
                arcgis_json = cls.get_postal_code_polygon(postal_code)
                geojson = arcgis_json_to_geojson(arcgis_json)
                save_as_json(geojson, directory=geojson_directory,
                             filename=geojson_filename)
                cls._logger.info(
                    f"GeoJSON polygon data saved to {geojson_filename}")
            else:
                cls._logger.info(
                    f"GeoJSON polygon data already exists at {geojson_filename}")

        return latitude, longitude

    @classmethod
    def get_municipality_code_from_postal_code(cls, postal_code: str) -> str | None:
        suggestions = cls.get_postal_code_suggestion(postal_code).get("suggestions", None)
        suggestion = suggestions[0] if suggestions else None
        if not suggestion:
            return None
        address = suggestion.get("text", "")
        latitude = suggestion.get("latitude", None)
        longitude = suggestion.get("longitude", None)

        response = cls.get_postal_code_detail(address, latitude, longitude)
        municipality_code = None
        for item in response.get("postalCodes", []):
            if item.get("postalCode") == postal_code:
                municipality_code = item.get("municipalityCode")
                break
        if municipality_code is None:
            cls._logger.info(
                f"Municipality code not found for postal code: {postal_code}")
        return municipality_code

    @classmethod
    def get_municipality_name_from_postal_code(cls, postal_code: str) -> str | None:
        suggestions = cls.get_postal_code_suggestion(postal_code).get("suggestions", None)
        suggestion = suggestions[0] if suggestions else None
        if not suggestion:
            return None
        address = suggestion.get("text", "")
        municipality = address.split(
            ",")[1].strip() if "," in address else None
        return municipality
    @classmethod
    def get_province_name_from_postal_code(cls, postal_code: str) -> str | None:
        suggestions = cls.get_postal_code_suggestion(postal_code).get("suggestions", None)
        suggestion = suggestions[0] if suggestions else None
        if not suggestion:
            return None
        address = suggestion.get("text", "")
        province = address.split(
            ",")[2].strip() if "," in address else None
        return province
    @classmethod
    def get_ccaa_name_from_postal_code(cls, postal_code: str) -> str | None:
        suggestions = cls.get_postal_code_suggestion(postal_code).get("suggestions", None)
        suggestion = suggestions[0] if suggestions else None
        if not suggestion:
            return None
        address = suggestion.get("text", "")
        ccaa = address.split(
            ",")[3].strip() if "," in address else None
        return ccaa


def is_clockwise(ring: list) -> bool:
    """
    Determines if a polygon ring is wound clockwise using the Shoelace formula.
    Returns True if clockwise, False if counter-clockwise.
    """
    area = 0
    # Iterate through each vertex
    for i in range(len(ring)):
        p1 = ring[i]
        # Wrap around to the first vertex for the last calculation
        p2 = ring[(i + 1) % len(ring)] 
        
        # (x2 - x1) * (y2 + y1)
        area += (p2[0] - p1[0]) * (p2[1] + p1[1])
        
    # If the signed area is positive, the ring is clockwise
    return area > 0

def enforce_right_hand_rule(rings: list) -> list:
    """
    Ensures rings follow the GeoJSON Right-Hand Rule (RFC 7946):
    - Exterior ring (index 0): Counter-Clockwise
    - Interior rings/holes (index > 0): Clockwise
    """
    corrected_rings = []
    
    for i, ring in enumerate(rings):
        is_cw = is_clockwise(ring)
        
        if i == 0:
            # Exterior ring: Must be Counter-Clockwise
            if is_cw:
                # Reverse the list of coordinates
                corrected_rings.append(ring[::-1]) 
            else:
                corrected_rings.append(ring)
        else:
            # Interior rings (holes): Must be Clockwise
            if not is_cw:
                corrected_rings.append(ring[::-1])
            else:
                corrected_rings.append(ring)
                
    return corrected_rings

def arcgis_json_to_geojson(arcgis_json: dict) -> dict:
    """
    Converts ArcGIS JSON format to GeoJSON format, strictly adhering 
    to the RFC 7946 Right-Hand Rule for Polygon winding.

    :param arcgis_json: The ArcGIS JSON data.
    :type arcgis_json: dict
    :return: The converted GeoJSON data.
    :rtype: dict
    """
    geojson = {"type": "FeatureCollection", "features": []}

    for feature in arcgis_json.get("features", []):
        geometry = feature.get("geometry", {})
        attributes = feature.get("attributes", {})

        geojson_feature = {
            "type": "Feature",
            "geometry": {}, 
            "properties": attributes
        }

        if "x" in geometry and "y" in geometry:
            geojson_feature["geometry"] = {
                "type": "Point",
                "coordinates": [geometry["x"], geometry["y"]],
            }
        elif "rings" in geometry:
            geojson_feature["geometry"] = {
                "type": "Polygon",
                "coordinates": enforce_right_hand_rule(geometry["rings"]),
            }
        # Add more geometry types as needed (e.g., Polyline -> LineString)

        geojson["features"].append(geojson_feature)

    return geojson
