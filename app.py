import streamlit as st
import pandas as pd
import numpy as np
import datetime
import pytz
from fpdf import FPDF

# 1. CONFIGURACIÓN DE SEGURIDAD Y MARCA
st.set_page_config(page_title="MILUXOR - Optimizador Geotécnico", layout="centered")
MARCA = "MILUXOR"

# Control de intentos en la sesión
if 'intentos' not in st.session_state:
    st.session_state.intentos = 0

# 2. LÓGICA DE CÁLCULO PROTEGIDA (Caja Negra)
def calcular_proctor(humedades, densidades):
    coef = np.polyfit(humedades, densidades, 2)
    p = np.poly1d(coef)
    h_opt = -coef[1] / (2 * coef[0])
    d_max = p(h_opt)
    return h_opt, d_max, p

# 3. INTERFAZ PROFESIONAL
st.title(f"🚀 {MARCA} - Pipeline de Ingeniería")
st.markdown("---")

user_email = st.text_input("Correo electrónico del cliente:", placeholder="cliente@empresa.com")

if user_email:
    if st.session_state.intentos >= 3:
        st.error("Límite de 3 intentos alcanzado. Contacte a Milton Montaño para acceso premium.")
    else:
        st.info(f"Sesión activa para: {user_email} | Intentos disponibles: {3 - st.session_state.intentos}")
        
        col1, col2 = st.columns(2)
        with col1:
            h_input = st.text_input("Humedades (%) [Separe por comas]:", "10, 12, 14, 16")
        with col2:
            d_input = st.text_input("Densidades (kg/m³) [Separe por comas]:", "1850, 1920, 1910, 1860")
        
        if st.button("EJECUTAR AUDITORÍA Y GENERAR REPORTE"):
            try:
                h_list = [float(x.strip()) for x in h_input.split(',')]
                d_list = [float(x.strip()) for x in d_input.split(',')]
                
                h_opt, d_max, modelo = calcular_proctor(h_list, d_list)
                st.session_state.intentos += 1
                
                st.success("✅ Análisis Completado")
                st.metric("Humedad Óptima", f"{h_opt:.2f} %")
                st.metric("Densidad Máxima", f"{d_max:.2f} kg/m³")
                st.write("Generando PDF certificado...")
                
            except Exception as e:
                st.error("Error: Verifique que los datos sean números separados por comas.")

st.markdown("---")
st.caption("© 2026 MILUXOR - Sistema de Ingeniería Protegido")
