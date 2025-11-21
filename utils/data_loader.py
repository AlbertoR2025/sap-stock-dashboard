import pandas as pd
import os
from .columnas import estandarizar_columnas

def cargar_datos():
    ruta = os.path.join("data", "inventario_procesado_final.csv")

    df = pd.read_csv(ruta, encoding="utf-8")

    df = estandarizar_columnas(df)

    return df
