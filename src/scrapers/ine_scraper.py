from bs4 import BeautifulSoup
import requests
import csv
from src.shared.utils import slugify, normalize


def scrape_INE_ccaa_provinces(
    url: str = "https://www.ine.es/daco/daco42/codmun/cod_ccaa_provincia.htm",
    out_file_path: str = "../data/processed/ine_ccaa_y_provincias.csv",
    verbose: bool = True,
):
    response = None
    try:
        verbose and print("[+] Fetching and parsing the webpage...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except Exception as e:
        print(f"Error fetching or parsing the webpage: {e}")

    try:
        verbose and print("[+] Parsing HTML content...")
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")
        verbose and print("[+] Extracting data from the table...")
        data = []
        # csv columns must be in snake_case without accents
        headers = [slugify(normalize(header.text.strip())).lower() for header in table.find_all("th")]
        data.append(headers)
        for row in table.find_all("tr")[1:]:  # Skip header row
            cols = row.find_all("td")
            if len(cols) < len(headers):
                continue  # Skip rows that don't have enough columns
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])  # Get rid of empty values
    except Exception as e:
        print(f"Error processing the HTML content: {e}")

        if verbose:
            print("[+] Extracted data:")
            for entry in data:
                print(entry)

        verbose and print(f"[+] storing data to '{out_file_path}'...")

    try:
        with open(out_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")  # there are names with commas
            writer.writerows(data)
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
