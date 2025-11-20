import pandas as pd

def estandarizar_columnas(df):

    mapping = {
        "centro": "Centro",
        "almacen": "Almacén",
        "material": "Material",
        "descripcion": "Descripción",
        "lote": "Lote",
        "f_prod": "F_Prod",
        "stock": "Stock",
        "un": "Un",
        "un_pallet": "Un_Pallet",
        "f_caja": "F_Caja",
        "cajas": "Cajas",
        "pallets": "Pallets",
        "camiones": "Camiones",
        "bloqueado": "Bloqueado",
        "control_calidad": "Control_Calidad"
    }

    # Renombrar solo las columnas que existan
    df = df.rename(columns=mapping)

    return df
