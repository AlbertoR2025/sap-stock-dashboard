def filtrar_materiales(df, lista_materiales):
    """Filtra el DataFrame por una lista de materiales"""
    df = df.copy()
    df["Material"] = df["Material"].astype(str).str.replace(".0", "", regex=False)
    return df[df["Material"].isin(lista_materiales)]
