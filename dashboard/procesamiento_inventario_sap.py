# =============================================================
# procesamiento_inventario_sap.py — VERSIÓN ROBUSTA AUTOMÁTICA
# =============================================================

import pandas as pd
import glob
import unicodedata
import os

# Diagnóstico: imprime contexto de ejecución
print("=== DEPURACIÓN ===")
print("Directorio actual de ejecución:", os.getcwd())
print("Contenido de la carpeta actual:", os.listdir())
print("Contenido de ./data:", os.listdir("data") if os.path.exists("data") else "NO EXISTE")
print("===================")

print("INICIANDO PROCESAMIENTO DE INVENTARIO SAP")
print("===========================================================\n")

# 1) BUSCAR ARCHIVO SAP EN /data
def encontrar_archivo_sap():
    archivos = glob.glob(os.path.join("data","*.xlsx")) + glob.glob(os.path.join("data","*.XLSX"))
    if not archivos:
        print("ERROR: No se encontró archivo SAP en /data")
        exit(1)
    archivo = archivos[0]
    print(f"Archivo SAP detectado: {archivo}\n")
    return archivo

archivo_sap = encontrar_archivo_sap()

# 2) CARGAR ARCHIVO
df = pd.read_excel(archivo_sap)
print(f"Registros cargados: {len(df):,}")
print(f"Columnas originales: {list(df.columns)}\n")

# 3) NORMALIZAR NOMBRES DE COLUMNAS
def normalizar(nombre):
    nombre = ''.join(c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn')
    return nombre.lower().strip().replace("  ", " ")

df.columns = [normalizar(c) for c in df.columns]
df = df.rename(columns={
    "texto breve de material": "descripcion",
    "descripcion del material": "descripcion",
    "libre utilizacion": "stock",
    "unidad medida base": "un",
    "inspecc.de calidad": "control_calidad",
    "en control calidad": "control_calidad",
    "stock bloqueado": "bloqueado"
})
print("Columnas normalizadas:")
print(df.columns.tolist(), "\n")

# 4) FILTRAR MATERIALES
materiales_validos = [
    "930101926","930101927","930101928",
    "920100665","920100666","920100667","920100668",
    "920100669","920100670","920100511","920100514",
    "920100046","920100057","920100512","920100513"
]

df["material"] = df["material"].astype(str).str.replace(r"\.0$", "", regex=True)
df = df[df["material"].isin(materiales_validos)].copy()
print(f"Materiales filtrados: {df['material'].nunique()}\n")
if df.empty:
    print("ERROR: Ninguno de los materiales válidos está presente.")
    exit(1)

# 5) LIMPIAR STOCK
df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)

# 6) FECHA DESDE LOTE
mes_map = {
    "A": "01","B":"02","C":"03","D":"04","E":"05","F":"06",
    "G":"07","H":"08","I":"09","J":"10","K":"11","L":"12"
}
def extraer_fecha(lote):
    lote = str(lote).strip()
    if len(lote) < 5:
        return ""
    try:
        aa = lote[:2]
        letra = lote[2].upper()
        dia = lote[3:5]
        mes = mes_map.get(letra, "00")
        return f"{dia}.{mes}.20{aa}"
    except:
        return ""
df["f_prod"] = df["lote"].apply(extraer_fecha)

# 7) FACTORES POR MATERIAL
info = {
    "930101926":{"un_pallet":3900,"f_caja":48},
    "930101927":{"un_pallet":3900,"f_caja":48},
    "930101928":{"un_pallet":3900,"f_caja":48},
    "920100665":{"un_pallet":4180,"f_caja":10},
    "920100666":{"un_pallet":4180,"f_caja":10},
    "920100667":{"un_pallet":4180,"f_caja":10},
    "920100668":{"un_pallet":4180,"f_caja":10},
    "920100669":{"un_pallet":4180,"f_caja":10},
    "920100670":{"un_pallet":4180,"f_caja":10},
    "920100046":{"un_pallet":2700,"f_caja":24},
    "920100057":{"un_pallet":2700,"f_caja":24},
    "920100511":{"un_pallet":3900,"f_caja":48},
    "920100514":{"un_pallet":3900,"f_caja":48},
    "920100512":{"un_pallet":3900,"f_caja":48},
    "920100513":{"un_pallet":3900,"f_caja":48}
}
df["un_pallet"] = df["material"].map(lambda x: info[x]["un_pallet"])
df["f_caja"] = df["material"].map(lambda x: info[x]["f_caja"])

# 8) CÁLCULOS
df["cajas"] = (df["stock"] / df["f_caja"]).round(0).astype(int)
df["pallets"] = (df["stock"] / df["un_pallet"]).round(2)
df["camiones"] = (df["pallets"] / 20).round(2)

# 9) ORDEN FINAL DE COLUMNAS
df = df[[
    "centro","almacen","material","descripcion","lote","f_prod",
    "stock","un","un_pallet","f_caja",
    "cajas","pallets","camiones",
    "bloqueado","control_calidad"
]]
df = df.sort_values("stock", ascending=False)

# 10) RESUMEN FINAL
print("==================== RESUMEN FINAL ====================\n")
print(f"Total registros procesados: {len(df):,}")
print(f"Stock total: {df['stock'].sum():,}")
print(f"Cajas totales: {df['cajas'].sum():,}")
print(f"Pallets totales: {df['pallets'].sum():.1f}")
print(f"Camiones: {df['camiones'].sum():.2f}")
print("========================================================\n")

# 11) GUARDAR ARCHIVO FINAL
df.to_csv(os.path.join("data", "inventario_procesado_final.csv"), index=False, encoding="utf-8-sig")
print("Guardado en data/inventario_procesado_final.csv")
print("PROCESO COMPLETADO\n")
