#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script Maestro: Automatización del Inventario SAP
- Procesa datos descargados de SAP
- Verifica integridad
- Muestra verificación visual en consola
- Sube archivos actualizados a GitHub
- Envía notificación por email
"""

import subprocess
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pandas as pd  # Agregamos el import aquí arriba

# ======================== CONFIGURACIÓN ========================
PROYECTO_ROOT = r"G:\CURSO PYTHON\Pruebas -Ejercicio Python Datos\Prueba Analisis de Datos SAP\Informe Viernes 21 Nov"
DATA_FOLDER = os.path.join(PROYECTO_ROOT, "dashboard", "data")
ARCHIVOS_ACTUALIZAR = [
    "dashboard/data/inventario_procesado_final.csv",
]

# Git
GITHUB_REMOTE = "origin"
GITHUB_BRANCH = "main"
GITHUB_REPO_URL = "https://github.com/AlbertoR2025/sap-stock-dashboard"

# Email config (asegúrate de usar tu App Password de Gmail y correo remitente)
EMAIL_REMITENTE = "btoreyes@gmail.com"
EMAIL_PASSWORD = "oxyf vwgt cqjj njnn"
EMAIL_DESTINATARIO = "luis.reyesv@nutrisco.com"
EMAIL_ASUNTO_EXITO = "✅ Actualización Inventario SAP - Exitosa"
EMAIL_ASUNTO_ERROR = "❌ Error en Actualización Inventario SAP"

# ======================== FUNCIONES ========================

def enviar_email(asunto, mensaje, es_html=False):
    """Envía email de notificación"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_REMITENTE
        msg['To'] = EMAIL_DESTINATARIO
        msg['Subject'] = asunto

        tipo = 'html' if es_html else 'plain'
        msg.attach(MIMEText(mensaje, tipo, 'utf-8'))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✉️ Email enviado exitosamente a {EMAIL_DESTINATARIO}")
    except Exception as e:
        print(f"⚠️ Error al enviar email: {str(e)}")

def run_python_script(script_name):
    """Ejecuta un script Python ubicado en la subcarpeta dashboard y captura resultado"""
    print(f"\n{'='*60}")
    print(f"▶️  Ejecutando: {script_name}")
    print(f"{'='*60}")

    # Construye la ruta al script dentro de la carpeta dashboard
    script_path = os.path.join(PROYECTO_ROOT, "dashboard", script_name)
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        cwd=os.path.join(PROYECTO_ROOT, "dashboard")
    )

    print(result.stdout)

    if result.returncode != 0:
        error_msg = f"❌ ERROR en {script_name}:\n{result.stderr}"
        print(error_msg)
        enviar_email(
            EMAIL_ASUNTO_ERROR,
            f"Falló la ejecución de: {script_name}\n\nError:\n{result.stderr}\n\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        sys.exit(result.returncode)

    return result

def run_git_command(cmd):
    """Ejecuta comando Git"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=PROYECTO_ROOT
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ Git warning/error:\n{result.stderr}")
    return result

def mostrar_verificacion(archivo_csv):
    print("\n=== Verificación de Datos Procesados ===")
    resultado_preview = ""
    try:
        df = pd.read_csv(archivo_csv)

        # Muestra primeras 5 filas
        print("\nPrimeras 5 filas del procesado:")
        print(df.head(5).to_string(index=False))

        resultado_preview += "<pre>" + df.head(5).to_string(index=False) + "</pre>"

        # KPIs rápidos
        total_unidades = df["STOCK"].sum() if "STOCK" in df.columns else None
        materiales_unicos = df["Material"].nunique() if "Material" in df.columns else None

        print("\nKPIs principales:")
        if total_unidades is not None:
            print(f"Total unidades de stock: {total_unidades:,}")
            resultado_preview += f"\n<b>Total unidades de stock:</b> {total_unidades:,}"
        if materiales_unicos is not None:
            print(f"Materiales únicos: {materiales_unicos}")
            resultado_preview += f"\n<b>Materiales únicos:</b> {materiales_unicos}"
    except Exception as e:
        print("⚠️ No se pudo mostrar verificación:", str(e))
        resultado_preview += f"\nError: {str(e)}"
    return resultado_preview

# ======================== FLUJO PRINCIPAL ========================
def main():
    print("\n" + "="*60)
    print("🚀 SCRIPT MAESTRO - ACTUALIZACIÓN INVENTARIO SAP")
    print("="*60)
    print(f"📅 Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Proyecto: {PROYECTO_ROOT}")
    print(f"📊 Datos: {DATA_FOLDER}")
    print("="*60 + "\n")

    try:
        # 1. Procesar Inventario SAP
        run_python_script("procesamiento_inventario_sap.py")

        # 2. Verificar Datos
        run_python_script("verificar_completo.py")

        # 3. Mostrar verificación visual y KPIs en consola (incluye resumen para email)
        resumen_verificacion = mostrar_verificacion(
            os.path.join(PROYECTO_ROOT, "dashboard/data/inventario_procesado_final.csv")
        )

        # 4. Actualizar GitHub
        print("\n" + "="*60)
        print("📤 Actualizando repositorio en GitHub")
        print("="*60)
        run_git_command(f"git pull {GITHUB_REMOTE} {GITHUB_BRANCH}")

        print("\n➕ Agregando archivos actualizados...")
        for archivo in ARCHIVOS_ACTUALIZAR:
            archivo_path = os.path.join(PROYECTO_ROOT, archivo)
            if os.path.exists(archivo_path):
                run_git_command(f'git add "{archivo}"')
                print(f"   ✓ {archivo}")
            else:
                print(f"   ⚠️ Archivo no encontrado: {archivo}")

        commit_msg = f'auto: actualización inventario SAP {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        print(f"\n💾 Creando commit...")
        run_git_command(f'git commit -m "{commit_msg}"')

        print(f"\n🚀 Subiendo cambios a GitHub...")
        run_git_command(f"git push {GITHUB_REMOTE} {GITHUB_BRANCH}")

        print("\n" + "="*60)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("="*60)

        mensaje_exito = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #28a745;">✅ Actualización Exitosa - Inventario SAP</h2>
            <p><strong>Fecha/Hora:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Repositorio:</strong> <a href="{GITHUB_REPO_URL}">{GITHUB_REPO_URL}</a></p>
            <p><strong>Dashboard:</strong> <a href="https://sap-stock-dashboard.streamlit.app/">Ver Dashboard</a></p>
            <h3>Preview de Datos Procesados:</h3>
            {resumen_verificacion}
            <h3>Pasos Completados:</h3>
            <ul>
                <li>✓ Procesamiento de datos SAP</li>
                <li>✓ Verificación de integridad</li>
                <li>✓ Sincronización con GitHub</li>
            </ul>
            <p style="color: #666; font-size: 12px; margin-top: 30px;">
                Este mensaje fue generado automáticamente por el Script Maestro de Actualización.
            </p>
        </body>
        </html>
        """
        enviar_email(EMAIL_ASUNTO_EXITO, mensaje_exito, es_html=True)
        print(f"\n📧 Notificación enviada a: {EMAIL_DESTINATARIO}")
        print(f"🌐 Dashboard actualizado: https://sap-stock-dashboard.streamlit.app/")

    except Exception as e:
        error_detalle = f"Error inesperado: {str(e)}"
        print(f"\n❌ {error_detalle}")
        enviar_email(
            EMAIL_ASUNTO_ERROR,
            f"Error crítico en Script Maestro:\n\n{error_detalle}\n\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
