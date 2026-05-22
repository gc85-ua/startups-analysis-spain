import pandas as pd
from typing import Dict, Optional
from src.shared.utils import slugify, normalize


def process_cobertura_excel(
        input_path:str="../data/bronze/avance.digital.gob.es/Cobertura_BA_España_2021-2024_MUN_PROV_CCAA_Nacional_datosgob.xlsx",
        output_path:str="../data/silver/cobertura_banda_ancha_municipios_2021_2024.csv",
        sheet_name:str="Municipio_%viviendas",
        dtype:Optional[Dict[str, type]]=None
) -> pd.DataFrame:
    """
    Procesa el archivo Excel de cobertura de banda ancha en España, limpiando y normalizando los datos para su análisis posterior.
    
    :param input_path: Ruta al archivo Excel de entrada con los datos de cobertura.
    :type input_path: str
    :param output_path: Ruta donde se guardará el archivo CSV procesado.
    :type output_path: str
    :param sheet_name: Nombre de la hoja del Excel que contiene los datos a procesar.
    :type sheet_name: str
    :param dtype: Diccionario de tipos de datos para las columnas del DataFrame. Si es None, se inferirán automáticamente.
    :type dtype: Optional[Dict[str, type]]
    :return: DataFrame procesado con los datos de cobertura.
    :rtype: DataFrame
    """
    data_df = pd.read_excel(
        input_path,
        sheet_name=sheet_name,
        dtype=dtype
    )

    # remplazar del nombre de las columnas: saltos de línea, ':', '.', espacios dobles y parentesis
    # convertir las columnas a snake_case
    data_df.columns = [slugify(normalize(col.lower().strip().replace("\n", " ").replace(':', '').replace('.', '').replace(
        "  ", " ").replace("(", "").replace(")", ""))) for col in data_df.columns]
    targets = [
        'pais',
        'comunidad',
        'provincia',
        'cmun',
        'municipio',
        'habitantes',
        'viviendas',
        'ftth',
        '1gbps',
        '5g'
    ]
    useful_columns = [
        col for col in data_df.columns if any(target in col.lower() for target in targets)
    ]
    cobertura_df = data_df[useful_columns].copy()

    def clean_column_names(col):
        # 1. Mapeo de meses a números
        meses = {'enero': '01', 'junio': '06'}

        # 2. Simplificar prefijos largos (1gbps y 5g banda)
        col = col.replace(
            'cob_1gbps_descarga_condiciones_maxima_demanda_', '1gbps_')
        col = col.replace('5g_banda_3_5ghz_', '5g_3_5ghz_')
        # Se mantiene similar pero por estructura
        col = col.replace('viviendas_catastro_', 'viviendas_catastro_')

        # 3. Reemplazar "mes_año" por "mm_año"
        for mes_nombre, mes_num in meses.items():
            if mes_nombre in col:
                col = col.replace(mes_nombre, mes_num)

        return col

    # Aplicar de una sola vez
    cobertura_df.rename(columns=clean_column_names, inplace=True)

    # imputamos columnas faltantes con 0, asumiendo que si no se reporta cobertura es porque es 0
    if '5g_3_5ghz_06_2021' not in cobertura_df.columns:
        cobertura_df['5g_3_5ghz_06_2021'] = 0
    if '5g_3_5ghz_06_2022' not in cobertura_df.columns:
        cobertura_df['5g_3_5ghz_06_2022'] = 0
    if '1gbps_06_2021' not in cobertura_df.columns:
        cobertura_df['1gbps_06_2021'] = 0

    # 1. Columnas estructurales (estáticas)
    targets_base = ['pais', 'comunidad_autonoma', 'provincia',
                    'cmun', 'municipio', 'habitantes', 'viviendas']

    cols_base = [col for col in cobertura_df.columns if any(
        target in col.lower() for target in targets_base)]

    # 2. Generación dinámica de series temporales (2021 a 2024)
    years = range(2021, 2025)

    # Generamos las listas de tecnología en una sola línea por cada una
    cols_ftth = [f'ftth_06_{y}' for y in years]
    cols_1gbps = [f'1gbps_06_{y}' for y in years]

    # Para el 5G, unimos la básica y la de banda 3.5GHz
    cols_5g = [f'5g_06_{y}' for y in years] + \
        [f'5g_3_5ghz_06_{y}' for y in years]

    # 3. Reordenar el DataFrame
    cobertura_df = cobertura_df[cols_base + cols_ftth + cols_1gbps + cols_5g]

    cobertura_df.to_csv(
        output_path, sep=";", index=False)

    return cobertura_df
