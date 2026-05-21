import googlemaps
import os
from geopy.extra.rate_limiter import RateLimiter
from src.shared.utils import save_as_json
import re
from src.geocoders.CorreosApi import CorreosApi
import logging

class GoogleMaps:
    _client = None
    _rate_limiter = None
    _logger = logging.getLogger(__name__)

    @classmethod
    def _initialize(cls):
        if cls._client is None:
            api_key = os.getenv("GOOGLE_MAPS_API_KEY")
            cls._client = googlemaps.Client(key=api_key)

    @classmethod
    def set_rate_limiter(cls, min_delay_seconds: float = 1.0):
        cls._initialize()
        cls._rate_limiter = RateLimiter(
            cls._client.geocode, min_delay_seconds=min_delay_seconds
        )

    @classmethod
    def geocode(cls, term: str, save_json: bool = False, filename: str = None, rate_limiter: bool = True, acceptable_types=['ROOFTOP']) -> tuple[float, float, str] | tuple[None, None, None]:
        """
        Class method to obtain coordinates (latitude and longitude) for a given postal code using Google Maps API.

        :param cls: The class itself.
        :param term: The term to geocode.
        :type term: str
        :return: A tuple containing latitude and longitude, or (None, None) if not found.
        :rtype: tuple[float, float] | tuple[None, None]
        """
        cls._initialize()
        rate_limiter and cls.set_rate_limiter()
        try:
            components = {
                "country": "ES",
            }
            
            cp_match = re.match(r'\b\d{5}\b', term)
            if cp_match:
                cls._logger.info(f"Postal code {cp_match.group(0)} detected in term '{term}'")
                components["postal_code"] = cp_match.group(0)
            if components.get("postal_code"):
                cp = components.get("postal_code")
                components["administrative_area"] = CorreosApi.get_province_name_from_postal_code(cp)
                #components["locality"] = CorreosApi.get_municipality_name_from_postal_code(cp)
            cls._logger.info(f"Components for geocoding: {components}")
            geocode_result = cls._rate_limiter(f"{term}") if rate_limiter else cls._client.geocode(f"{term}",components=components)
            if geocode_result:
                cls._logger.info(f"Geocode result for '{term}': {geocode_result}")
                if save_json:
                    filename = f"{term.replace(' ', '_')}_geocoded.json" if filename is None else filename
                    save_as_json(geocode_result, filename,
                                 directory="../data/cache/json/")
                location = geocode_result[0]["geometry"]["location"]
                formatted_address = geocode_result[0]["formatted_address"]
                return location["lat"], location["lng"], formatted_address

            raise ValueError(f"Term not found: {term}")

        except Exception as e:
            cls._logger.error(f"Error: {e}")
            return None, None, None