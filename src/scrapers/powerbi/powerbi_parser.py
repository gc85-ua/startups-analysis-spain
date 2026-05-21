import pandas as pd
import csv
import json
def pbi_json_to_df(data:dict) -> pd.DataFrame:

    # 1. Extraer Metadatos y nombres de columnas del descriptor
    result_data = data["results"][0]["result"]["data"]
    descriptor_select = result_data["descriptor"]["Select"]

    col_order = [item["Value"] for item in descriptor_select]
    col_names = []
    for item in descriptor_select:
        # Extraemos el nombre legible de la propiedad (ej: 'razon_social')
        full_name = item.get("Name", item["Value"])
        display_name = full_name.split(".")[-1] if "." in full_name else full_name
        col_names.append(display_name)

    # 2. Acceder a los datos y diccionarios
    ds = result_data["dsr"]["DS"][0]
    value_dicts = ds.get("ValueDicts", {})
    dm0 = ds["PH"][0]["DM0"]

    rows = []
    current_schema = []
    previous_row = [None] * len(col_order)

    # 3. Iterar sobre los registros (DM0)
    for entry in dm0:
        # Actualizar el esquema si el registro lo incluye
        if "S" in entry:
            current_schema = entry["S"]

        bitmask_null = entry.get("Ø", 0)  # Nulos
        bitmask_repeat = entry.get("R", 0)  # Repetidos de la fila anterior
        raw_values = entry.get("C", [])  # Valores presentes

        num_cols = len(current_schema)
        current_row_vals = [None] * num_cols
        val_ptr = 0

        for i in range(num_cols):
            col_info = current_schema[i]

            # Caso 1: El valor es Nulo
            if bitmask_null & (1 << i):
                current_row_vals[i] = None
            # Caso 2: El valor se repite de la fila anterior
            elif bitmask_repeat & (1 << i):
                current_row_vals[i] = previous_row[i]
            # Caso 3: El valor está presente en la lista 'C'
            else:
                if val_ptr < len(raw_values):
                    val = raw_values[val_ptr]
                    val_ptr += 1

                    # Si la columna usa diccionario, traducimos el índice
                    if "DN" in col_info and isinstance(val, int):
                        dict_name = col_info["DN"]
                        if dict_name in value_dicts:
                            val = value_dicts[dict_name][val]

                    # Conversión de fechas (Power BI usa milisegundos Unix)
                    col_id = col_info["N"]
                    idx_in_names = col_order.index(col_id)
                    if "fecha" in col_names[idx_in_names].lower() and isinstance(
                        val, (int, float)
                    ):
                        val = pd.to_datetime(val, unit="ms")

                    current_row_vals[i] = val

        # Mapear a un diccionario con nombres finales
        row_dict = {
            col_names[col_order.index(current_schema[i]["N"])]: current_row_vals[i]
            for i in range(num_cols)
        }
        rows.append(row_dict)
        previous_row = current_row_vals

    return pd.DataFrame(rows)[col_names]

# Converts the JSON output of a PowerBI query to a CSV file
def extract(input_file, output_file):
    input_json = read_json(input_file)
    data = input_json["results"][0]["result"]["data"]
    dm0 = data["dsr"]["DS"][0]["PH"][0]["DM0"]
    columns_types = dm0[0]["S"]
    columns = map(lambda item: item["GroupKeys"][0]["Source"]["Property"] if item["Kind"] == 1 else item["Value"], data["descriptor"]["Select"])
    value_dicts = data["dsr"]["DS"][0].get("ValueDicts", {})

    reconstruct_arrays(columns_types, dm0)
    expand_values(columns_types, dm0, value_dicts)

    replace_newlines_with(dm0, "")
    write_csv(output_file, columns, dm0)

def read_json(file_name):
    with open(file_name) as json_config_file:
        return json.load(json_config_file)

def write_csv(output_file, columns, dm0):
    with open(output_file, "w") as csvfile:
        wrt = csv.writer(csvfile)
        wrt.writerow(columns)
        for item in dm0:
            wrt.writerow(item["C"])

def reconstruct_arrays(columns_types, dm0):
    # fixes array index by applying
    # "R" bitset to copy previous values
    # "Ø" bitset to set null values
    lenght = len(columns_types)
    prevItem = None
    for item in dm0:
        currentItem = item["C"]
        if "R" in item or "Ø" in item:
            copyBitset = item.get("R", 0)
            deleteBitSet = item.get("Ø", 0)
            for i in range(lenght):
                if is_bit_set_for_index(i, copyBitset):
                    currentItem.insert(i, prevItem[i])
                elif is_bit_set_for_index(i, deleteBitSet):
                    currentItem.insert(i, None)
        prevItem = currentItem

def is_bit_set_for_index(index, bitset):
    return (bitset >> index) & 1 == 1

# substitute indexes with actual values
def expand_values(columns_types, dm0, value_dicts):
    for (idx, col) in enumerate(columns_types):
        if "DN" in col:
            for item in dm0:
                dataItem = item["C"]
                if isinstance(dataItem[idx], int):
                    valDict = value_dicts[col["DN"]]
                    dataItem[idx] = valDict[dataItem[idx]]

def replace_newlines_with(dm0, replacement):
    for item in dm0:
        elem = item["C"]
        for i in range(len(elem)):
            if isinstance(elem[i], str):
                elem[i] = elem[i].replace("\n", replacement)

