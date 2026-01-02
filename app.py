import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="PadelYa - Posadas", page_icon="🎾", layout="wide")

# URL de tu planilla (formateada para lectura directa)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BCC74IuRiJ9OomWQId26h5oGnEtAGnc9UvZOADMmNoA/gviz/tq?tqx=out:csv"

# Función para cargar datos desde Google Sheets
def cargar_datos():
    try:
        df = pd.read_csv(SHEET_URL)
        return df
    except:
        return pd.DataFrame(columns=['complejo', 'dia', 'inicio', 'fin', 'estado'])

# Estilo PadelYa
st.markdown("""
    <style>
    .stApp { background-color: #0b1e1e; color: white; }
    .stButton>button { background-color: #f1c40f !important; color: black !important; border-radius: 15px; width: 100%; }
    .fc-event-main { color: black !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

df_turnos = cargar_datos()

st.title("🎾 PadelYa")
tab_jugador, tab_dueno = st.tabs(["🎾 RESERVAR", "🔐 PANEL"])

with tab_jugador:
    st.header("Canchas Libres en Posadas")
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        complejo = st.selectbox("Seleccioná el Complejo:", ["World Padel Center", "La Terraza", "Padel Pro"])
        nombre = st.text_input("Tu Nombre:")
        
        # Filtramos los turnos LIBRES de la planilla para el complejo elegido
        libres = df_turnos[(df_turnos['complejo'] == complejo) & (df_turnos['estado'].str.lower() == 'libre')]
        
        opciones = [f"{row['inicio']} a {row['fin']}" for index, row in libres.iterrows()]
        
        if opciones:
            horario_sel = st.selectbox("Horarios disponibles:", opciones)
            if st.button("RESERVAR AHORA"):
                st.success(f"¡Pedido enviado! Avisale al dueño por WhatsApp.")
                st.link_button("💬 AVISAR POR WHATSAPP", "https://wa.me/543764000000")
        else:
            st.warning("No hay turnos libres cargados en la planilla para este complejo.")

    with col_b:
        # Transformar datos de la planilla al formato del calendario
        eventos_cal = []
        for _, row in libres.iterrows():
            eventos_cal.append({
                "title": "LIBRE",
                "start": f"{row['dia']}T{row['inicio']}",
                "end": f"{row['dia']}T{row['fin']}",
                "backgroundColor": "#2ecc71"
            })
            
        calendar(events=eventos_cal, options={"initialView": "timeGridDay", "locale": "es", "slotMinTime": "08:00:00", "slotMaxTime": "24:00:00"}, key="cal")

with tab_dueno:
    st.info(f"Para gestionar los turnos, editá directamente tu planilla de Google: [Abrir Planilla](https://docs.google.com/spreadsheets/d/1BCC74IuRiJ9OomWQId26h5oGnEtAGnc9UvZOADMmNoA/edit)")
