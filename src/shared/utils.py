import unicodedata
import random
import json
import time
import re
import os
from rapidfuzz import process, fuzz
from typing import Any, Dict, List, Optional
import pandas as pd

def normalize(text: str) -> str:
    """
    Remove accents from a given text.

    :param text: Input string potentially containing accented characters.
    :type text: str
    :return: String with accents removed.
    :rtype: str
    """
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def slugify(text: str) -> str:
    """
    Convert a string into a slug format: lowercase, with non-alphanumeric characters replaced by underscores.
    Conserves uppercase letters.

    :param text: Input string to be slugified.
    :type text: str
    :return: Slugified string.
    :rtype: str
    """
    return "".join(c if c.isalnum() else "_" for c in text)


def random_delay(min_delay=1, max_delay=2):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)


def save_as_json(data: dict | list[dict] | None, filename: str, directory: str = "../data/processed/json/") -> None:
    """
    Docstring for save_as_json

    :param data: data to be saved as JSON
    :type data: dict | list[dict] | None
    :param filename: file's name, with extension .json
    :type filename: str
    :param directory: directory to save the file
    :type directory: str
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)

    if data is None:
        data = {}
    if not isinstance(data, (dict, list)):
        raise ValueError(
            "Data must be a dictionary or a list of dictionaries to be saved as JSON.")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def extract_domain(url: str) -> str:
    """
    Extract the domain from a given URL.

    :param url: The URL string.
    :type url: str
    :return: The extracted domain.
    :rtype: str
    """
    # Remove protocol (http, https, ftp, etc.)
    url = re.sub(r'^\w+://', '', url)
    # Remove 'www.' prefix if present
    url = re.sub(r'^www\.', '', url)
    # Extract domain up to the first '/' or end of string
    domain = re.split(r'[/?#]', url)[0]
    return domain

def normalize_address(address: str) -> str:
    """
    Normaliza una dirección en español:
    - Expande abreviaturas comunes (c/, av., avda., pl., pza., etc.) a la palabra completa.
    - Elimina prefijos de número como 'nº', 'n°', 'num.', 'núm.', 'numero', 'número'.
    - Quita la coma que precede directamente a un número de portal ("Calle X, 12" -> "Calle X 12").

    :param address: Dirección a normalizar.
    :return: Dirección normalizada.
    """
    if not address:
        return address

    s = address.strip()

    # Expandir abreviaturas comunes en una sola pasada para evitar solapamientos
    abbr_map = {
        'c/': 'Calle', 'c.': 'Calle', 'c': 'Calle',
        'avda': 'Avenida', 'av.': 'Avenida', 'av': 'Avenida', 'avenida': 'Avenida',
        'plz': 'Plaza', 'plz.': 'Plaza', 'pza': 'Plaza', 'pza.': 'Plaza', 'plaza': 'Plaza',
        'paseo': 'Paseo', 'pº': 'Paseo', 'p.º': 'Paseo'
    }

    # Primero manejar 'C/' y 'C.' (forma muy común) para evitar solapamientos
    s = re.sub(r"(?i)\bC[\/\.]\s*", "Calle ", s)

    # Patrón que captura la abreviatura (sin 'c' porque ya se manejó) y sin solapamientos problemáticos
    abbr_pattern = re.compile(
        r"(?i)\b(?:avda|av\.?|avenida|plz\.?|pza\.?|plaza|paseo|pº|p\.º)\b\.?\s*")

    def _expand(m: re.Match) -> str:
        tok = m.group(0)
        # normalizar token a una forma clave: eliminar espacios y puntos, mantener º y /
        key = re.sub(r"[\s\.]", "", tok).lower()
        key = key.replace('\\', '')
        key = key.strip()
        val = abbr_map.get(key, None)
        return (val + ' ') if val else m.group(0)

    s = abbr_pattern.sub(_expand, s)

    # Eliminar prefijos de número (num., nº, n°, núm., numero, número, etc.)
    s = re.sub(
        r"(?i)\b(?:num(?:ero)?|n(?:º|°)|núm(?:\.)?|número)\.?\s*[:\-]?\s*", "", s)

    # Eliminar variantes de 's/n' o 'S/N' (sin número)
    s = re.sub(r"(?i)\bS\s*\/?\s*N\b\.?", "", s)

    # Quitar coma cuando precede directamente a un número (p.ej. 'Calle X, 12' -> 'Calle X 12')
    # No tocar comas que estén dentro de números (p.ej. '38,500') porque quedan entre dígitos.
    s = re.sub(r",\s+(?=\d)", " ", s)

    # Eliminar comas redundantes que no estén entre dígitos (p.ej. ",,", ", Isla...", etc.)
    s = re.sub(r"(?<!\d),(?!\d)", "", s)

    # Truncar texto tras el número final (mantener hasta el último token numérico si existe)
    # Patrón para un token numérico: dígitos, opcional decimal o rango con guión
    num_pat = re.compile(r"\d+(?:[.,]\d+)?(?:[-–—]\d+(?:[.,]\d+)?)?")
    matches = list(num_pat.finditer(s))
    if matches:
        last = matches[-1]
        s = s[: last.end()]

    # Normalizar espacios y limpiar separadores sobrantes
    s = re.sub(r"[\s\-]{2,}", " ", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = s.strip()

    # Quitar coma final o guion final si los hay
    s = re.sub(r"[\-,\.\s]+$", "", s)

    return s


def fuzzy_match_dict(key: str, candidates: Dict[str, Any], key_modifiers: Optional[List[str]] = None, threshold: float = 80.0) -> Optional[str]:
    """
    Función para hacer un match inteligente de una clave contra un diccionario de candidatos usando RapidFuzz.
    Se generan varias queries a partir de la clave original usando los modificadores, y se busca la mejor coincidencia entre todas las queries y los candidatos.
    Args:
        key (str): La clave a buscar.
        candidates (dict[str, str]): Un diccionario donde las claves son los posibles matches y los valores son lo que se retornará si hay un match.
        key_modifiers (list[str]): Lista de prefijos a agregar a la clave original para generar queries adicionales (ej. "Universidad ", "Universitat ", etc.).
        threshold (float): El puntaje mínimo de similitud para considerar un match válido (0-100).
    Returns:
        str | None: El valor del candidato que mejor coincide si el puntaje supera el umbral. De lo contrario, None.
    """
    # early return para casos obvios
    if pd.isna(key) or not isinstance(key, str):
        return None

    # 1. Generar todas las posibles "queries" (fuerza bruta acotada al input, no al dataset)
    modifiers = key_modifiers or []
    queries = [key] + [f"{mod}{key}" for mod in modifiers]

    best_overall_score = 0
    best_candidate_key = None

    # 2. Usar process.extractOne que está altamente optimizado en C++
    # Esto busca la mejor query contra TODAS las keys de candidatos mucho más rápido
    # que un bucle for en Python.
    # Cachear esto fuera si es posible
    candidate_keys = list(candidates.keys())

    for query in queries:
        # extractOne devuelve (match, score, index)
        result = process.extractOne(
            query,
            candidate_keys,
            scorer=fuzz.ratio,
            score_cutoff=threshold
        )

        if result:
            match_key, score, _ = result
            if score > best_overall_score:
                best_overall_score = score
                best_candidate_key = match_key

    # Retornar el valor normalizado si hubo match
    return candidates[best_candidate_key] if best_candidate_key else None