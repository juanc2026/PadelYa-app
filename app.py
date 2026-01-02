import streamlit as st
import pandas as pd
from streamlit_calendar import calendar
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="PadelYa - Reservas", page_icon="🎾", layout="wide")

# --- 1. CONEXIÓN CON TU GOOGLE SHEETS ---
# Este es el link que me pasaste transformado para que la app pueda leerlo
SHEET_URL = "https://docs.google.com/spreadsheets/d/1BCC74IuRiJ9OomWQId26h5oGnEtAGnc9UvZOADMmNoA/export?format=csv"

def cargar_datos():
    try:
        # Leemos el Excel online
        df = pd.read_csv(SHEET_URL)
        # Limpiamos espacios en blanco de los nombres de columnas
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error al conectar con la planilla: {e}")
        return pd.DataFrame()

df_turnos = cargar_datos()

# Convertimos los datos del Excel al formato del calendario
eventos_calendario = []
if not df_turnos.empty:
    for _, fila in df_turnos.iterrows():
        # Solo mostramos los que están "libre"
        if str(fila['Estado']).lower() == 'libre':
            # El formato debe ser YYYY-MM-DDTHH:MM:SS
            # Asumimos que en el Excel la fecha está como DD/MM/YYYY
            fecha_partes = str(fila['Dia']).split('/')
            fecha_iso = f"{fecha_partes[2]}-{fecha_partes[1]}-{fecha_partes[0]}"
            
            eventos_calendario.append({
                "title": f"LIBRE - {fila['Complejo']}",
                "start": f"{fecha_iso}T{fila['inicio']}",
                "end": f"{fecha_iso}T{fila['Fin']}",
                "backgroundColor": "#2ecc71"
            })

# --- 2. ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1e1e; color: white; }
    .stButton>button {
        background-color: #f1c40f !important;
        color: black !important;
        font-weight: bold;
        border-radius: 15px;
        width: 100%;
    }
    .fc-event-main { color: black !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎾 PadelYa")

tab_jugador, tab_dueno = st.tabs(["🎾 BUSCAR CANCHA", "🔐 PANEL DUEÑO"])

# --- VISTA JUGADOR ---
with tab_jugador:
    st.header("Canchas Libres en Posadas")
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("📍 Filtros")
        complejo_sel = st.selectbox("Seleccioná el Complejo:", df_turnos['Complejo'].unique() if not df_turnos.empty else ["Cargando..."])
        
        st.divider()
        st.subheader("📝 Tu Reserva")
        nombre = st.text_input("Nombre del Capitán:")
        
        # Horarios disponibles filtrados por complejo
        if not df_turnos.empty:
            turnos_filtrados = df_turnos[(df_turnos['Complejo'] == complejo_sel) & (df_turnos['Estado'].str.lower() == 'libre')]
            horarios_lista = [f"{r['inicio'][:5]} a {r['Fin'][:5]}" for _, r in turnos_filtrados.iterrows()]
            
            if horarios_lista:
                horario_elegido = st.selectbox("Elegí un horario:", horarios_lista)
                if st.button("RESERVAR AHORA"):
                    if nombre:
                        st.success(f"¡Pedido enviado! Avisale al dueño por WhatsApp.")
                        mensaje_wa = f"Hola! Soy {nombre}, quiero reservar el turno de {horario_elegido} en {complejo_sel}."
                        st.link_button("📱 AVISAR POR WHATSAPP", f"https://wa.me/543764000000?text={mensaje_wa.replace(' ', '%20')}")
                    else:
                        st.error("Ingresá tu nombre.")
            else:
                st.warning("No hay turnos libres para este complejo.")

    with col_b:
        calendar(events=eventos_calendario, options={
            "initialView": "timeGridDay",
            "locale": "es",
            "slotMinTime": "08:00:00",
            "slotMaxTime": "24:00:00",
            "headerToolbar": {"left": "prev,next", "center": "title", "right": ""},
        }, key="cal_jug")

# --- VISTA DUEÑO ---
with tab_dueno:
    st.info("Para gestionar los turnos, editá directamente tu planilla de Google Sheets.")
    st.link_button("📂 ABRIR MI EXCEL", "https://docs.google.com/spreadsheets/d/1BCC74IuRiJ9OomWQId26h5oGnEtAGnc9UvZOADMmNoA/")
    if st.button("🔄 ACTUALIZAR APP"):
        st.rerun()
