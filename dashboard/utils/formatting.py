import pandas as pd

def formato_num(df, columnas):
    """Convierte columnas especificadas a formato numérico"""
    for col in columnas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(float)
    return df
