import subprocess
import os
import sys

# Ruta absoluta al directorio del proyecto
ruta_base = r"G:\CURSO PYTHON\Pruebas -Ejercicio Python Datos\Prueba Analisis de Datos SAP\Informe Miercoles 191125\dashboard"

os.chdir(ruta_base)

print("\n========= AUTO ACTUALIZADOR SAP DASHBOARD =========\n")
print(f"- Carpeta base: {ruta_base}\n")

# 1. Procesar datos SAP
try:
    print("🔄 Procesando y limpiando datos SAP...")
    subprocess.run([sys.executable, "procesamiento_inventario_sap.py"], check=True)
    print("✅ Limpieza completada.")
except Exception as e:
    print("❌ Error en el procesamiento de datos:", e)
    sys.exit(1)

# 2. Lanzar dashboard de Streamlit
try:
    print("\n🚀 Iniciando dashboard interactivo...\n")
    subprocess.run(["streamlit", "run", "0_Panel_de_Control.py"])
except Exception as e:
    print("❌ Error al iniciar el dashboard:", e)
    sys.exit(1)
