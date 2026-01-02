import streamlit as st
from streamlit_calendar import calendar # Requiere instalarse, ver nota abajo

st.set_page_config(page_title="PadelYa - Agenda", page_icon="🎾", layout="wide")

# Estilo PadelYa Nocturno
st.markdown("""
    <style>
    .stApp { background-color: #0b1e1e; color: white; }
    .fc-v-event { background-color: #2ecc71 !important; border: none !important; } /* Color de turnos ocupados */
    .stButton>button { background-color: #f1c40f !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎾 Agenda de Turnos PadelYa")

# 1. Base de datos de turnos (Simulada)
if 'events' not in st.session_state:
    st.session_state.events = [
        {"title": "RESERVADO - Juan", "start": "2026-01-02T18:00:00", "end": "2026-01-02T20:00:00"},
        {"title": "RESERVADO - Fer", "start": "2026-01-02T20:00:00", "end": "2026-01-02T22:00:00"},
    ]

col1, col2 = st.columns([3, 1])

with col1:
    # CONFIGURACIÓN DEL CALENDARIO
    calendar_options = {
        "initialView": "timeGridDay", # Vista de día con horas
        "slotMinTime": "08:00:00",
        "slotMaxTime": "23:59:00",
        "allDaySlot": False,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "timeGridDay,timeGridWeek",
        },
        "slotDuration": "01:00:00", # Bloques de 1 hora (mostraremos 2 para el turno)
    }
    
    state = calendar(events=st.session_state.events, options=calendar_options)
    st.write("👆 *Toca un espacio vacío para solicitar o un turno para ver detalles*")

with col2:
    st.subheader("Nuevas Reservas")
    with st.form("nueva_reserva"):
        nombre = st.text_input("Nombre del Jugador")
        fecha = st.date_input("Fecha")
        hora_inicio = st.time_input("Hora de inicio")
        
        if st.form_submit_button("AGENDAR TURNO 120 MIN"):
            # Lógica para crear el evento de 2 horas
            start_dt = f"{fecha}T{hora_inicio}"
            # Agregamos a la lista
            st.session_state.events.append({
                "title": f"OCUPADO - {nombre}",
                "start": start_dt,
                "end": start_dt # Aquí podrías sumar 2 horas con datetime
            })
            st.rerun()

    if st.button("Limpiar Agenda"):
        st.session_state.events = []
        st.rerun()
