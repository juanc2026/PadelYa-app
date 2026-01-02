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
        width: 100%;
    }
    .fc-event-main { color: black !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Base de datos simulada de horarios DISPONIBLES
if 'horarios_libres' not in st.session_state:
    st.session_state.horarios_libres = [
        {"title": "LIBRE", "start": "2026-01-02T18:00:00", "end": "2026-01-02T20:00:00", "backgroundColor": "#2ecc71"},
        {"title": "LIBRE", "start": "2026-01-02T20:00:00", "end": "2026-01-02T22:00:00", "backgroundColor": "#2ecc71"},
        {"title": "LIBRE", "start": "2026-01-02T22:00:00", "end": "2026-01-02T23:59:59", "backgroundColor": "#2ecc71"},
    ]

st.title("🎾 PadelYa")

tab_jugador, tab_dueno = st.tabs(["🎾 BUSCAR CANCHA", "🔐 PANEL DUEÑO"])

# --- VISTA JUGADOR ---
with tab_jugador:
    st.header("Canchas Libres en Posadas")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        st.subheader("📍 Canchas")
        complejo = st.selectbox("Seleccioná el Complejo:", ["World Padel Center", "La Terraza", "Padel Pro"])
        
        st.divider()
        
        st.subheader("📝 Tu Reserva")
        nombre = st.text_input("Nombre del Capitán:")
        
        # Formateo de horarios para el selector
        horarios_visibles = [f"{h['start'][11:16]} a {h['end'][11:16]}" for h in st.session_state.horarios_libres]
        
        if horarios_visibles:
            horario_elegido = st.selectbox("Elegí un horario libre:", horarios_visibles)
        else:
            st.warning("No hay turnos libres cargados.")
        
        if st.button("RESERVAR AHORA"):
            if nombre:
                st.success(f"¡Pedido enviado! Pagá la seña para confirmar en {complejo}.")
                st.link_button("💳 PAGAR SEÑA ($3.600)", "https://www.mercadopago.com.ar")
            else:
                st.error("Por favor, ingresá tu nombre.")

    with col_b:
        st.subheader("Disponibilidad (Hasta las 24 hs)")
        opciones_cal = {
            "initialView": "timeGridDay",
            "locale": "es",
            "slotMinTime": "08:00:00",
            "slotMaxTime": "24:00:00", # Extendido hasta medianoche
            "allDaySlot": False,
            "headerToolbar": {"left": "prev,next", "center": "title", "right": ""},
            "buttonText": {"today": "Hoy"},
        }
        calendar(events=st.session_state.horarios_libres, options=opciones_cal, key="cal_jugador")

# --- VISTA DUEÑO ---
with tab_dueno:
    st.subheader("Administración de Cancha")
    clave = st.text_input("Contraseña:", type="password")
    
    if clave == "padel123":
        st.write("### Cargar Disponibilidad Nocturna")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fecha = st.date_input("Día:")
            h_inicio = st.time_input("Hora Inicio:")
        with col_c2:
            h_fin = st.time_input("Hora Fin:")
        
        if st.button("HABILITAR TURNO LIBRE"):
            # Ajuste para el formato ISO de medianoche
            fin_str = f"{fecha}T{h_fin}"
            if h_fin.hour == 0 and h_fin.minute == 0:
                fin_str = f"{fecha}T23:59:59"
                
            nuevo_turno = {
                "title": "LIBRE",
                "start": f"{fecha}T{h_inicio}",
                "end": fin_str,
                "backgroundColor": "#2ecc71"
            }
            st.session_state.horarios_libres.append(nuevo_turno)
            st.success("Turno cargado hasta tarde.")
            st.rerun()
            
        st.divider()
        if st.button("LIMPIAR AGENDA"):
            st.session_state.horarios_libres = []
            st.rerun()
