# =============================================================================
# DASHBOARD COMPLETO SAP - SCRIPT INTEGRADO
# Procesamiento + Verificación + Visualización
# =============================================================================

import pandas as pd
import glob
import unicodedata
import os
import sys

print("\n" + "="*80)
print("🚀 SISTEMA INTEGRADO DE ANÁLISIS SAP")
print("="*80 + "\n")

# =============================================================================
# PASO 1: PROCESAMIENTO DE DATOS SAP
# =============================================================================
print("📊 PASO 1: PROCESAMIENTO DE DATOS\n")

def encontrar_archivo_sap():
    archivos = glob.glob("data/*.xlsx") + glob.glob("data/*.XLSX")
    if not archivos:
        print("❌ No se encontró archivo SAP en /data")
        sys.exit(1)
    archivo = archivos[0]
    print(f"📁 Archivo SAP detectado: {archivo}\n")
    return archivo

archivo_sap = encontrar_archivo_sap()
df = pd.read_excel(archivo_sap)
print(f"📄 Registros cargados: {len(df):,}")

# Normalizar columnas
def normalizar(nombre):
    nombre = ''.join(c for c in unicodedata.normalize('NFD', nombre)
                     if unicodedata.category(c) != 'Mn')
    return nombre.lower().strip().replace(" ", "_")

df.columns = [normalizar(c) for c in df.columns]
df = df.rename(columns={
    "texto_breve_de_material": "descripcion",
    "descripcion_del_material": "descripcion",
    "libre_utilizacion": "stock",
    "unidad_medida_base": "un",
    "inspecc.de_calidad": "control_calidad",
    "en_control_calidad": "control_calidad",
    "stock_bloqueado": "bloqueado"
})

# Filtrar materiales válidos
materiales_validos = [
    "930101926","930101927","930101928",
    "920100665","920100666","920100667","920100668",
    "920100669","920100670","920100511","920100514",
    "920100046","920100057","920100512","920100513"
]

df["material"] = df["material"].astype(str).str.replace(r"\.0$", "", regex=True)
df = df[df["material"].isin(materiales_validos)].copy()
print(f"🎯 Materiales filtrados: {df['material'].nunique()}")

if df.empty:
    print("❌ ERROR: Ninguno de los materiales válidos está presente.")
    sys.exit(1)

# Limpiar stock
df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)

# Extraer fecha desde lote
mes_map = {
    "A":"01","B":"02","C":"03","D":"04","E":"05","F":"06",
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

# Factores por material
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

# Cálculos
df["cajas"] = (df["stock"] / df["f_caja"]).round(0).astype(int)
df["pallets"] = (df["stock"] / df["un_pallet"]).round(2)
df["camiones"] = (df["pallets"] / 20).round(2)

# Orden final de columnas
df = df[[
    "centro","almacen","material","descripcion","lote","f_prod",
    "stock","un","un_pallet","f_caja",
    "cajas","pallets","camiones",
    "bloqueado","control_calidad"
]]
df = df.sort_values("stock", ascending=False)

# Guardar archivo procesado
df.to_csv("data/inventario_procesado_final.csv", index=False, encoding="utf-8-sig")
print("💾 Guardado en data/inventario_procesado_final.csv")
print("✅ Procesamiento completado\n")

# =============================================================================
# PASO 2: VERIFICACIÓN Y REPORTE
# =============================================================================
print("="*80)
print("📋 PASO 2: VERIFICACIÓN Y REPORTE")
print("="*80 + "\n")

print(f"📊 Total registros procesados: {len(df):,}")
print(f"📦 Stock total: {df['stock'].sum():,} unidades")
print(f"📦 Cajas totales: {df['cajas'].sum():,}")
print(f"🚛 Pallets totales: {df['pallets'].sum():.1f}")
print(f"🚚 Camiones: {df['camiones'].sum():.2f}\n")

# Top 5 materiales por cajas
print("TOP 5 MATERIALES POR CANTIDAD DE CAJAS:")
print("-" * 60)
top_5_cajas = df.groupby(['material', 'descripcion'])['cajas'].sum().nlargest(5)
for i, (idx, val) in enumerate(top_5_cajas.items(), 1):
    material, descripcion = idx
    stock_total = df[df['material'] == material]['stock'].sum()
    print(f"{i}. Material {material}")
    print(f"   {descripcion}")
    print(f"   Stock: {stock_total:,.0f} unidades | Cajas: {val:,.0f}\n")

print("="*80)
print("✅ VERIFICACIÓN COMPLETADA")
print("="*80 + "\n")

# =============================================================================
# PASO 3: LANZAR DASHBOARD INTERACTIVO
# =============================================================================
print("="*80)
print("🚀 PASO 3: INICIANDO DASHBOARD INTERACTIVO")
print("="*80 + "\n")
print("El dashboard se abrirá en tu navegador...")
print("Presiona Ctrl+C en la terminal para detenerlo.\n")

import subprocess
try:
    subprocess.run(["streamlit", "run", "0_Panel_de_Control.py"])
except KeyboardInterrupt:
    print("\n\n🛑 Dashboard detenido por el usuario.")
except Exception as e:
    print(f"❌ Error al iniciar dashboard: {e}")
    sys.exit(1)
