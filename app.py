import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="PadelYa - Reservas", page_icon="🎾", layout="wide")

# Estilo Visual PadelYa
st.markdown("""
    <style>
    .stApp { background-color: #0b1e1e; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #0b1e1e; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1a2e2e;
        border-radius: 10px 10px 0px 0px;
        color: white;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #2ecc71 !important; 
        color: black !important;
    }
    .stButton>button {
        background-color: #f1c40f !important;
        color: black !important;
        font-weight: bold;
        border-radius: 15px;
    }
    /* Estilo para los eventos libres en el calendario */
    .fc-event-main { color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Base de datos simulada de horarios DISPONIBLES
if 'horarios_libres' not in st.session_state:
    st.session_state.horarios_libres = [
        {"title": "LIBRE", "start": "2026-01-02T16:00:00", "end": "2026-01-02T18:00:00", "backgroundColor": "#2ecc71"},
        {"title": "LIBRE", "start": "2026-01-02T18:00:00", "end": "2026-01-02T20:00:00", "backgroundColor": "#2ecc71"},
        {"title": "LIBRE", "start": "2026-01-02T20:00:00", "end": "2026-01-02T22:00:00", "backgroundColor": "#2ecc71"},
    ]

st.title("🎾 PadelYa")

tab_jugador, tab_dueno = st.tabs(["🎾 BUSCAR CANCHA", "🔐 PANEL DUEÑO"])

# --- VISTA JUGADOR ---
with tab_jugador:
    st.header("Canchas Libres en Posadas")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("1. Filtros")
        complejo = st.selectbox("Elegí el Complejo:", ["World Padel Center", "La Terraza", "Padel Pro"])
        st.info("Solo se muestran los turnos de 120 min disponibles.")
        
        st.subheader("2. Tu Reserva")
        nombre = st.text_input("Nombre del Capitán:")
        horario_elegido = st.selectbox("Elegí un horario libre del calendario:", 
                                      [f"{h['start'][11:16]} a {h['end'][11:16]}" for h in st.session_state.horarios_libres])
        
        if st.button("RESERVAR AHORA"):
            if nombre:
                st.success(f"¡Pedido enviado! Pagá la seña para confirmar tu turno en {complejo}.")
                st.link_button("💳 PAGAR SEÑA ($3.600)", "https://www.mercadopago.com.ar")
            else:
                st.error("Ingresá tu nombre para reservar.")

    with col_b:
        st.subheader("Disponibilidad Horaria")
        opciones_cal = {
            "initialView": "timeGridDay",
            "locale": "es",
            "slotMinTime": "08:00:00",
            "slotMaxTime": "23:59:00",
            "allDaySlot": False,
            "headerToolbar": {"left": "prev,next", "center": "title", "right": ""},
        }
        calendar(events=st.session_state.horarios_libres, options=opciones_cal, key="cal_jugador")

# --- VISTA DUEÑO ---
with tab_dueno:
    st.subheader("Administración de Cancha")
    clave = st.text_input("Clave:", type="password")
