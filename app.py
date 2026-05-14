import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import pytz
import os
import uuid

# Protocolo pR: Configuración de Entorno
st.set_page_config(page_title="MILUXOR - Auditoría", layout="wide")
st.title("🚀 MILUXOR - Pipeline de Ingeniería y Auditoría")

# --- CONTROL DE INTENTOS (Límite: 3) ---
if 'intentos' not in st.session_state:
    st.session_state.intentos = 0

# --- SECCIÓN 1: DATOS DE AUDITORÍA Y SEGUIMIENTO ---
st.sidebar.header("📋 Datos de Seguimiento")
user_email = st.sidebar.text_input("Correo electrónico del interesado:")
user_id = st.sidebar.text_input("Número de Identificación (C.C./NIT):")

# --- SECCIÓN 2: ENTRADA DE DATOS TÉCNICOS ---
col1, col2 = st.columns(2)
with col1:
    h_input = st.text_input("Humedades (%) [Separe por comas]:", "10.5,12.2,14.8,16.5,18.2,20.1")
with col2:
    d_input = st.text_input("Densidades (kg/m³) [Separe por comas]:", "1.72,1.85,1.94,1.96,1.91,1.82")

if st.button("EJECUTAR AUDITORÍA Y GENERAR REPORTE"):
    # 1. Validación de Límite de Oportunidades
    if st.session_state.intentos >= 3:
        st.error("⛔ Límite de 3 oportunidades agotado para esta sesión.")
        st.stop()

    # 2. Validación de Prospecto
    if not user_email or not user_id:
        st.error("⚠️ Error: Debe ingresar Correo e Identificación para fines de auditoría.")
        st.stop()

    try:
        # Procesamiento de Datos
        h = np.array([float(x.strip()) for x in h_input.split(',')])
        d = np.array([float(x.strip()) for x in d_input.split(',')])
        
        # Ajuste Polinomial
        p = np.polyfit(h, d, 2)
        h_opt = -p[1] / (2 * p[0])
        d_max = np.polyval(p, h_opt)

        # Renderizado de Gráfico (DPI 75 para cumplimiento de tiempo 15-20s)
        fig, ax = plt.subplots()
        ax.plot(h, d, 'ro', label='Datos Laboratorio')
        x_range = np.linspace(min(h), max(h), 100)
        ax.plot(x_range, np.polyval(p, x_range), 'b-', label='Ajuste Polinomial pR')
        ax.set_xlabel('Humedad (%)')
        ax.set_ylabel('Densidad (kg/m³)')
        ax.legend()
        ax.grid(True, linestyle='--')
        
        plot_path = 'temp_plot.png'
        plt.savefig(plot_path, dpi=75, bbox_inches='tight')
        plt.close(fig)

        # Auditoría de Seguimiento: Tiempo y ID Único
        bog_tz = pytz.timezone('America/Bogota')
        now = datetime.now(bog_tz)
        fecha_str = now.strftime("%d/%m/%Y")
        hora_str = now.strftime("%H:%M:%S")
        num_pdf = str(uuid.uuid4())[:8].upper() # Número de PDF único por ejecución

        st.success(f"Análisis Completado para: {user_email}")
        st.image(plot_path)

        # --- GENERACIÓN DE PDF PROFESIONAL ---
        pdf = FPDF()
        pdf.add_page()
        
        # Encabezado con ID de PDF Único
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(190, 10, f"CERTIFICADO DE AUDITORÍA MILUXOR #{num_pdf}", 1, 1, 'C')
        pdf.ln(5)

        # Bloque de Auditoría Separado
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(95, 7, f"IDENTIFICACIÓN: {user_id}", 0, 0)
        pdf.cell(95, 7, f"FECHA: {fecha_str}", 0, 1, 'R')
        pdf.cell(95, 7, f"CORREO: {user_email}", 0, 0)
        pdf.cell(95, 7, f"HORA: {hora_str}", 0, 1, 'R')
        pdf.ln(10)

        # Resultados Técnicos
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(190, 8, "RESULTADOS DEL ANÁLISIS:", 0, 1)
        pdf.set_font("Helvetica", '', 11)
        pdf.cell(190, 7, f"- Humedad Optima: {h_opt:.2f}%", 0, 1)
        pdf.cell(190, 7, f"- Densidad Seca Maxima: {d_max:.2f} kg/m3", 0, 1)
        pdf.ln(5)

        # Gráfico
        pdf.image(plot_path, x=15, y=None, w=180)
        
        pdf_output = pdf.output(dest='S').encode('latin-1')
        
        # Contador de intentos exitosos
        st.session_state.intentos += 1
        st.info(f"Oportunidades utilizadas: {st.session_state.intentos} de 3")

        st.download_button(
            label="📥 DESCARGAR CERTIFICADO AUDITADO",
            data=pdf_output,
            file_name=f"Auditoria_{num_pdf}_{user_id}.pdf",
            mime="application/pdf"
        )
        
        if os.path.exists(plot_path): os.remove(plot_path)

    except Exception as e:
        st.error(f"Falla en el Pipeline: {e}")

st.markdown("---")
st.caption("2026 MILUXOR - Especialista en Pedagogía y Digitalización de Procesos Técnicos")
