import pandas as pd

df = pd.read_csv("data/inventario_procesado_final.csv", encoding="utf-8-sig")

print("="*80)
print("REPORTE COMPLETO DEL INVENTARIO")
print("="*80)

# Información general
print(f"\nTOTAL DE REGISTROS: {len(df):,}")

# Mostrar las unidades presentes (columna 'un')
unidades_unicas = df['un'].unique()
print(f"\nUnidades distintas encontradas en el inventario: {len(unidades_unicas)}")
print("Lista de unidades:", ', '.join(str(u) for u in unidades_unicas))

# KPIs principales
print("\n" + "="*80)
print("KPIs PRINCIPALES")
print("="*80)

print(f"Stock Total: {df['stock'].sum():,.0f} unidades")
print(f"Cajas Totales: {df['cajas'].sum():,.0f} cajas")
print(f"Pallets Totales: {df['pallets'].sum():,.0f} pallets")
print(f"Camiones Totales: {df['camiones'].sum():,.0f} camiones")

# Top 11 materiales por cajas
print("\n" + "="*80)
print("TOP 11 MATERIALES POR CANTIDAD DE CAJAS")
print("="*80)

top_11_cajas = df.groupby(['material', 'descripcion'])['cajas'].sum().nlargest(11)

for i, (idx, val) in enumerate(top_11_cajas.items(), 1):
    material, descripcion = idx
    stock_total = df[df['material'] == material]['stock'].sum()
    print(f"{i:2d}. Material {material}")
    print(f"    {descripcion}")
    print(f"    Stock total: {stock_total:,.0f} unidades")
    print(f"    {val:,.0f} cajas ({val/1000:.1f} miles)\n")

# Resumen por almacén
print("="*80)
print("RESUMEN POR ALMACÉN")
print("="*80)

almacenes = df.groupby('almacen').agg({
    'stock': 'sum',
    'cajas': 'sum',
    'pallets': 'sum'
}).round(0)

print(almacenes)

print("\n" + "="*80)
print("VERIFICACIÓN COMPLETADA")
print("="*80)
