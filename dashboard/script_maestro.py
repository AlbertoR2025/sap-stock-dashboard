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
import pandas as pd

# ======================== CONFIGURACIÓN ========================
PROYECTO_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(PROYECTO_ROOT, "data")
DASHBOARD_FOLDER = PROYECTO_ROOT  # <--- DIRECTO, NO AGREGAR "dashboard"
ARCHIVOS_ACTUALIZAR = [
    os.path.join("data", "inventario_procesado_final.csv"),
]
# Git
GITHUB_REMOTE = "origin"
GITHUB_BRANCH = "main"
GITHUB_REPO_URL = "https://github.com/AlbertoR2025/sap-stock-dashboard"
# Email config
EMAIL_REMITENTE = "btoreyes@gmail.com"
EMAIL_PASSWORD = "oxyf vwgt cqjj njnn"
EMAIL_DESTINATARIO = "luis.reyesv@nutrisco.com"
EMAIL_ASUNTO_EXITO = "✅ Actualización Inventario SAP - Exitosa"
EMAIL_ASUNTO_ERROR = "❌ Error en Actualización Inventario SAP"

# ======================== FUNCIONES ========================

def enviar_email(asunto, mensaje, es_html=False):
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
    """Ejecuta un script Python en el mismo directorio y captura resultado"""
    print(f"\n{'='*60}")
    print(f"▶️ Ejecutando: {script_name}")
    print(f"{'='*60}")
    script_path = os.path.join(DASHBOARD_FOLDER, script_name)
    print("DEBUG script_path:", script_path)
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True
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
        cmd, shell=True, capture_output=True, text=True,
        cwd=PROYECTO_ROOT
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ Git warning/error:\n{result.stderr}")
    return result

def mostrar_verificacion(archivo_csv):
    print("\n=== Verificación de Datos Procesados ===")
    try:
        df = pd.read_csv(archivo_csv)
        print("\nPrimeras 5 filas del procesado:")
        print(df.head(5).to_string(index=False))
        # KPIs
        total_unidades = df["stock"].sum() if "stock" in df.columns else None
        materiales_unicos = df["material"].nunique() if "material" in df.columns else None
        print("\nKPIs principales:")
        if total_unidades is not None:
            print(f"Total unidades de stock: {total_unidades:,}")
        if materiales_unicos is not None:
            print(f"Materiales únicos procesados: {materiales_unicos:,}")
    except Exception as e:
        error_detalle = f"Error inesperado: {str(e)}"
        print(f"\n❌ {error_detalle}")
        enviar_email(
            EMAIL_ASUNTO_ERROR,
            f"Error crítico en Script Maestro:\n\n{error_detalle}\n\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        sys.exit(1)

# ======================== MAIN ========================

def main():
    try:
        # 1. Procesamiento SAP
        run_python_script("procesamiento_inventario_sap.py")
        # 2. Verificación visual y KPIs
        mostrar_verificacion(os.path.join(DATA_FOLDER, "inventario_procesado_final.csv"))
        # 3. Subir a GitHub
        cmd = "git add ."
        run_git_command(cmd)
        commit_msg = f"auto: inventario actualizado {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        run_git_command(f'git commit -m "{commit_msg}"')
        run_git_command(f"git push {GITHUB_REMOTE} {GITHUB_BRANCH}")
        # 4. Notificación de éxito
        mensaje_exito = (
            f"<b>Actualización exitosa del inventario SAP.</b><br>"
            f"<br><b>Fecha/Hora:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            f"<br><b>Repositorio:</b> {GITHUB_REPO_URL}"
            f"<br><b>Dashboard:</b> Ver Dashboard"
            "<br><br>Este mensaje fue generado automáticamente por el Script Maestro.<br>"
        )
        enviar_email(EMAIL_ASUNTO_EXITO, mensaje_exito, es_html=True)
        print(f"\n📧 Notificación enviada a: {EMAIL_DESTINATARIO}")
        print(f"🌐 Dashboard actualizado: https://sap-stock-dashboard.streamlit.app/")
    except Exception as e:
        error_detalle = f"Error inesperado (main): {str(e)}"
        print(f"\n❌ {error_detalle}")
        enviar_email(
            EMAIL_ASUNTO_ERROR,
            f"Error crítico en Script Maestro (main):\n\n{error_detalle}\n\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
