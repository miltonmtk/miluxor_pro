import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

# Configuración de página
st.set_page_config(page_title="MILUXOR", layout="wide")
st.title("🚀 MILUXOR - Pipeline de Ingeniería")

# Captura de datos optimizada pR (Resistente a espacios)
col1, col2 = st.columns(2)
with col1:
    h_input = st.text_input("Humedades (%) [Separe por comas]:", "10.5,12.2,14.8,16.5,18.2,20.1")
with col2:
    d_input = st.text_input("Densidades (kg/m³) [Separe por comas]:", "1.72,1.85,1.94,1.96,1.91,1.82")

if st.button("EJECUTAR AUDITORÍA Y GENERAR REPORTE"):
    try:
        # Conversión con limpieza de espacios accidentales
        h = np.array([float(x.strip()) for x in h_input.split(',')])
        d = np.array([float(x.strip()) for x in d_input.split(',')])
        
        if len(h) != len(d):
            st.error("Error: La cantidad de Humedades y Densidades debe ser igual.")
            st.stop()

        # Ajuste Polinomial de segundo grado
        p = np.polyfit(h, d, 2)
        h_opt = -p[1] / (2 * p[0])
        d_max = np.polyval(p, h_opt)

        # Renderizado veloz de gráfico (DPI optimizado para web)
        fig, ax = plt.subplots()
        ax.plot(h, d, 'ro', label='Datos Laboratorio')
        x_range = np.linspace(min(h), max(h), 100)
        ax.plot(x_range, np.polyval(p, x_range), 'b-', label='Ajuste Polinomial pR')
        ax.set_xlabel('Humedad (%)')
        ax.set_ylabel('Densidad (kg/m³)')
        ax.legend()
        ax.grid(True, linestyle='--')
        
        # Guardado optimizado para PDF
        plot_path = 'temp_plot.png'
        plt.savefig(plot_path, dpi=75, bbox_inches='tight')
        plt.close(fig) # Liberación de memoria inmediata

        st.success(f"Análisis Completado: Humedad Óptima {h_opt:.2f}% | Densidad Máxima {d_max:.2f} kg/m³")
        st.image(plot_path)

        # Generación de PDF compatible y rápida
        # Nota: Se usa 'Helvetica' por ser fuente estándar de PDF (evita errores de fpdf)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(190, 10, "CERTIFICADO DE AUDITORÍA MILUXOR", 1, 1, 'C')
        pdf.ln(10)
        
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(100, 10, f"Humedad Optima Calculada: {h_opt:.2f}%", 0, 1)
        pdf.cell(100, 10, f"Densidad Seca Maxima: {d_max:.2f} kg/cm3", 0, 1)
        pdf.ln(5)
        
        # Inserción de gráfico optimizado
        pdf.image(plot_path, x=15, y=None, w=180)
        
        # Salida de PDF como buffer para evitar latencia de escritura en disco
        pdf_output = pdf.output(dest='S').encode('latin-1')
        
        st.download_button(
            label="📥 DESCARGAR CERTIFICADO PDF",
            data=pdf_output,
            file_name="Certificado_Miluxor.pdf",
            mime="application/pdf"
        )
        
        # Limpieza de archivo temporal
        if os.path.exists(plot_path):
            os.remove(plot_path)

    except Exception as e:
        st.error(f"Falla en el Pipeline: {e}")

st.markdown("---")
st.caption("2026 MILUXOR - Especialista en Pedagogía y Digitalización de Procesos Técnicos")
