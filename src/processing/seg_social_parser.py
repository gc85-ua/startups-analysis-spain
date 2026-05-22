import pandas as pd
from typing import Dict, List
from src.shared.utils import normalize, slugify


def process_ss_afiliation_excel(file_path: str, municipios_dict: Dict[str, str], 
                                regimenes_incluidos: List[str] = ['111', '521'], 
                                export_to_csv: bool = False, 
                                export_directorio: str = "../data/silver/") -> pd.DataFrame:
    """
    Procesa un archivo de afiliación de la Seguridad Social en formato Excel y devuelve un DataFrame con la información relevante.
    
    :param file_path: Ruta al archivo Excel a procesar.
    :type file_path: str
    :param municipios_dict: Diccionario que mapea códigos de municipio a nombres de municipio.
    :type municipios_dict: Dict[str, str]
    :param regimenes_incluidos: Lista de códigos de régimen que se deben incluir en el resultado. Por defecto incluye '111' (régimen por cuenta ajena) y '521' (régimen por cuenta propia).
    :type regimenes_incluidos: List[str]
    :param export_to_csv: Si es True, se exportará el DataFrame procesado a un archivo CSV.
    :type export_to_csv: bool
    :param export_directorio: Ruta donde se guardará el archivo CSV procesado.
    :type export_directorio: str
    :return: DataFrame procesado con la información relevante.
    :rtype: DataFrame
    """
    # Cargar el archivo Excel
    data_df = pd.read_excel(file_path, dtype=str)

    # Normalizar los nombres de las columnas
    data_df.columns = [slugify(normalize(col.lower()))
                       for col in data_df.columns]

    # Asegurar que el código de municipio tenga 5 dígitos, si no llegan a 5 se debe al 0 a la izquierda
    data_df['cod_municipio'] = data_df['cod_municipio'].astype(str).str.zfill(5)

    # filtrar por regimenes incluidos y municipios incluidos
    mask_regimen = data_df['cod_regimen'].isin(regimenes_incluidos)
    mask_municipio = data_df['cod_municipio'].isin(municipios_dict.keys())
    afiliacion_df = data_df[mask_regimen & mask_municipio].copy().reset_index(drop=True)

    # Filtrar por sexo conocido
    afiliacion_df = afiliacion_df.dropna(subset=['cod_sexo', 'cod_cnae']).reset_index(drop=True)

    # Mapear código de municipio a nombre de municipio
    afiliacion_df['municipio'] = afiliacion_df['cod_municipio'].map(
        municipios_dict)

    # Filtrar por CNAE conocido
    afiliacion_df = afiliacion_df[~afiliacion_df['cod_cnae'].isna()].copy(
    ).reset_index(drop=True)

    # Convertir fecha al último día del mes correspondiente
    fecha = afiliacion_df['fecha'].drop_duplicates().tolist()
    fecha = pd.to_datetime(fecha[0], format='%Y%m') + pd.offsets.MonthEnd(1)
    afiliacion_df['fecha'] = fecha
    mask_less_eq = afiliacion_df['afiliados'].str.contains('<') | afiliacion_df['afiliados'].str.contains('<=')
    afiliacion_df.loc[mask_less_eq, 'afiliados'] = afiliacion_df.loc[mask_less_eq, 'afiliados'].str.replace('<', '').str.replace('=', '').str.strip()
    afiliacion_df['afiliados'] = afiliacion_df['afiliados'].astype(int)
    afiliacion_df.loc[mask_less_eq, 'afiliados'] = afiliacion_df.loc[mask_less_eq, 'afiliados'] // 2

    if export_to_csv:
        afiliacion_df.to_csv(
            f"{export_directorio}/{file_path.split('/')[-1].split('.')[0]}.csv", sep=";", index=False
        )

    return afiliacion_df