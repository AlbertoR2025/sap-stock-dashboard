def calcular_kpis(df):
    """Calcula los KPIs principales del inventario"""
    try:
        total_stock = df["stock"].sum() if "stock" in df.columns else 0
        total_cajas = df["cajas"].sum() if "cajas" in df.columns else 0
        total_pallets = df["pallets"].sum() if "pallets" in df.columns else 0
        total_camiones = df["camiones"].sum() if "camiones" in df.columns else 0
        
        return total_stock, total_cajas, total_pallets, total_camiones
    except Exception as e:
        print(f"Error calculando KPIs: {e}")
        return 0, 0, 0, 0
