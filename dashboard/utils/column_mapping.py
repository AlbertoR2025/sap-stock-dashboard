def estandarizar_columnas(df):

    mapping = {
        "centro": "Centro",
        "almacen": "Almacen",
        "material": "Material",
        "descripcion": "Descripcion",
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

    # normalizar primero
    df.columns = [col.strip().lower() for col in df.columns]

    # mapear después
    df = df.rename(columns=mapping)

    return df
