import pandas as pd

df = pd.read_csv("data/inventario_procesado_final.csv", encoding="utf-8-sig")
print("Columnas encontradas en el archivo limpio:")
for col in df.columns:
    print(f"- [{repr(col)}]")
