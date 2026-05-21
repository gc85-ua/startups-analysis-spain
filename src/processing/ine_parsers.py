import pandas as pd
import urllib.request
import re
import os

def parse_cnae_2025_txt(
    text_file_path: str = "../data/bronze/INE/cnae_2025.txt",
) -> pd.DataFrame:
    def is_seccion(line) -> tuple[bool, str, str]:
        if "SECCIÓN" in line:
            return True, line[0], line.split(":")[1].strip()
        return False, "", ""

    def is_grupo(line) -> tuple[bool, str, str]:
        if len(line.split(" ")[0]) == 2:
            grupo = line.split(" ")[0]
            descripcion = " ".join(line.split(" ")[1:]).strip()
            return True, grupo, descripcion
        return False, "", ""

    def is_subgrupo(line) -> tuple[bool, str, str]:
        if len(line.split(" ")[0]) == 4 and "." in line.split(" ")[0]:
            subgrupo = line.split(" ")[0].replace(".", "")
            descripcion = " ".join(line.split(" ")[1:]).strip()
            return True, subgrupo, descripcion
        return False, "", ""

    def is_codigo(line) -> tuple[bool, str, str]:
        if len(line.split(" ")[0]) == 5 and "." in line.split(" ")[0]:
            codigo = line.split(" ")[0].replace(".", "")
            descripcion = " ".join(line.split(" ")[1:]).strip()
            return True, codigo, descripcion
        return False, "", ""

    def es_dummy(line) -> bool:
        return len(line) < 5

    with open(text_file_path, "r") as file:
        data = []
        codigo = ""
        descripcion = ""
        subgrupo = ""
        descripcion_subgrupo = ""
        grupo = ""
        descripcion_grupo = ""
        seccion = ""
        descripcion_seccion = ""

        for line in file:
            if es_dummy(line):
                continue
            is_seccion, seccion_tmp, descripcion_seccion_tmp = is_seccion(line)
            if is_seccion:
                seccion = seccion_tmp
                descripcion_seccion = descripcion_seccion_tmp
                continue
            is_grupo, grupo_tmp, descripcion_grupo_tmp = is_grupo(line)
            if is_grupo:
                grupo = grupo_tmp
                descripcion_grupo = descripcion_grupo_tmp
                continue

            is_subgrupo, subgrupo_tmp, descripcion_subgrupo_tmp = is_subgrupo(line)
            if is_subgrupo:
                subgrupo = subgrupo_tmp
                descripcion_subgrupo = descripcion_subgrupo_tmp
                continue

            is_codigo, codigo_tmp, descripcion_codigo_tmp = is_codigo(line)
            if is_codigo:
                codigo = codigo_tmp
                descripcion = descripcion_codigo_tmp
                data.append(
                    {
                        "codigo": codigo,
                        "descripcion": descripcion,
                        "subgrupo": subgrupo,
                        "descripcion_subgrupo": descripcion_subgrupo,
                        "grupo": grupo,
                        "descripcion_grupo": descripcion_grupo,
                        "seccion": seccion,
                        "descripcion_seccion": descripcion_seccion,
                    }
                )
            else:
                print(f"Error parsing line: {line}")
        return pd.DataFrame(data)


def parse_cnae_2025_excel(
    excel_file_path: str = "../data/bronze/INE/cnae_2025.xlsx",
    sheet_name="Estructura_CNAE2025",
    usecols="A:B",
) -> pd.DataFrame:
    cnae_df = pd.read_excel(
        excel_file_path,
        sheet_name=sheet_name,
        usecols=usecols,
        dtype=str,
    )

    def is_seccion(row: pd.Series) -> tuple[bool, str, str]:
        letter = row.iloc[0].strip()
        if len(letter) == 1 and letter.isalpha():
            return True, letter, row.iloc[1].strip()
        return False, "", ""

    def is_grupo(row: pd.Series) -> tuple[bool, str, str]:
        code = row.iloc[0].strip()
        if len(code) == 2 and code.isdigit():
            return True, code.replace(".", ""), row.iloc[1].strip()
        return False, "", ""

    def is_subgrupo(row: pd.Series) -> tuple[bool, str, str]:
        code = row.iloc[0].strip()
        if (
            len(code) == 4
            and "." in code
            and all(part.isdigit() for part in code.split("."))
        ):
            return True, code.replace(".", ""), row.iloc[1].strip()
        return False, "", ""

    def is_codigo(row: pd.Series) -> tuple[bool, str, str]:
        code = row.iloc[0].strip()
        if (
            len(code) == 5
            and "." in code
            and all(part.isdigit() for part in code.split("."))
        ):
            return True, code.replace(".", ""), row.iloc[1].strip()
        return False, "", ""

    data = []
    codigo = ""
    descripcion = ""
    subgrupo = ""
    descripcion_subgrupo = ""
    grupo = ""
    descripcion_grupo = ""
    seccion = ""
    descripcion_seccion = ""

    for _, row in cnae_df.iterrows():
        is_seccion, seccion_tmp, descripcion_seccion_tmp = is_seccion(row)
        if is_seccion:
            seccion = seccion_tmp
            descripcion_seccion = descripcion_seccion_tmp
            continue

        is_grupo, grupo_tmp, descripcion_grupo_tmp = is_grupo(row)
        if is_grupo:
            grupo = grupo_tmp
            descripcion_grupo = descripcion_grupo_tmp
            continue

        is_subgrupo, subgrupo_tmp, descripcion_subgrupo_tmp = is_subgrupo(row)
        if is_subgrupo:
            subgrupo = subgrupo_tmp
            descripcion_subgrupo = descripcion_subgrupo_tmp
            continue

        is_codigo, codigo_tmp, descripcion_codigo_tmp = is_codigo(row)
        if is_codigo:
            codigo = codigo_tmp
            descripcion = descripcion_codigo_tmp
            data.append(
                {
                    "codigo": codigo,
                    "descripcion": descripcion,
                    "subgrupo": subgrupo,
                    "descripcion_subgrupo": descripcion_subgrupo,
                    "grupo": grupo,
                    "descripcion_grupo": descripcion_grupo,
                    "seccion": seccion,
                    "descripcion_seccion": descripcion_seccion,
                }
            )
        else:
            print(f"Error parsing line: {row.tolist()}")

    return pd.DataFrame(data)


def download_callejero(month: int, year: int, download_directory:str="../data/bronze/INE/") -> str:
    url = "https://www.ine.es/prodyser/callejero/caj_esp/caj_esp_0{month}{year}.zip"
    output_path = f"{download_directory}caj_esp_0{month}{year}.zip"
    check_dir = os.path.dirname(output_path)
    
    if not os.path.exists(check_dir):
        os.makedirs(check_dir)
    if os.path.isfile(output_path):
        print(f"File already exists: {output_path}")
        return output_path
    
    urllib.request.urlretrieve(url.format(month=month, year=year), output_path)
    return output_path


def parse_tram_file_text(text: str) -> pd.DataFrame:
    codigo_regex = re.compile(
        r"^(0[1-9]|[1-4][0-9]|5[0-2])[0-9]{3}$"
    )  # the pattern is the same for codigo_postal and codigo_municipio
    data = []
    for line in text.splitlines():
        if not line.strip():
            continue

        codigo_postal = line[42:47].strip() if len(line) > 47 else ""
        codigo_municipio = line[0:5].strip() if len(line) > 5 else ""

        if not codigo_regex.match(codigo_postal) or not codigo_regex.match(
            codigo_municipio
        ):
            print(f"Skipping invalid line: {line[0:25]}...")
            continue

        data.append(
            {"codigo_postal": codigo_postal, "codigo_municipio": codigo_municipio}
        )

    return (
        pd.DataFrame(data)
        .sort_values(by=["codigo_postal", "codigo_municipio"])
        .drop_duplicates()
        .reset_index(drop=True)
    )


def process_callejero_zip(file_path) -> pd.DataFrame:
    import zipfile

    with zipfile.ZipFile(file_path, "r") as zip_file:
        tram_file_name, tram_file_found = None, False
        for filename in zip_file.namelist():
            if "TRAM" in filename.upper():
                tram_file_found = True
                tram_file_name = filename
                break

        if not tram_file_found:
            raise ValueError("No TRAM file found in the ZIP archive.")

        content = zip_file.read(tram_file_name)
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1")

        return parse_tram_file_text(text)


def parse_callejero_censal(month: int, year: int) -> pd.DataFrame:
    if month != 1 and month != 7:
        raise ValueError("Callejero Censal is only available for January and July.")
    if year < 2021:
        print("WARNING: data before 2021 may not be parsed correctly.")
    return process_callejero_zip(download_callejero(month, year))
