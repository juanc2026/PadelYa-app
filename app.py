import streamlit as st
import pandas as pd
from datetime import time

# Configuración de la App
st.set_page_config(page_title="PadelYa Posadas", page_icon="🎾")

st.title("🎾 PadelYa - Prototipo Funcional")
st.sidebar.header("Menú de Navegación")
modo = st.sidebar.radio("Ir a:", ["Vista Jugador", "Panel del Dueño (Confirmación)"])

# Base de datos simulada (En una app real esto sería Firebase)
if 'reservas' not in st.session_state:
    st.session_state.reservas = []

# --- VISTA JUGADOR ---
if modo == "Vista Jugador":
    st.subheader("📍 Complejos en Posadas")
    complejo = st.selectbox("Elegí tu complejo:", ["World Padel Center", "La Terraza", "Padel Pro"])
    
    st.info("Turnos de 120 minutos (2 horas)")
    precio_total = 12000
    horario = st.select_slider("Elegí tu horario:", 
                               options=[time(16,0), time(18,0), time(20,0), time(22,0)])
    
    if st.button("Solicitar Reserva"):
        nueva_reserva = {
            "jugador": "Usuario de Prueba",
            "complejo": complejo,
            "horario": horario.strftime("%H:%M"),
            "estado": "Pendiente",
            "total": precio_total,
            "seña": precio_total * 0.30
        }
        st.session_state.reservas.append(nueva_reserva)
        st.warning("✅ Solicitud enviada. Esperando que el dueño confirme...")

# --- PANEL DEL DUEÑO ---
else:
    st.subheader("📋 Solicitudes Pendientes")
    if not st.session_state.reservas:
        st.write("No hay solicitudes nuevas.")
    else:
        for i, res in enumerate(st.session_state.reservas):
            if res["estado"] == "Pendiente":
                with st.expander(f"Reserva de {res['jugador']} - {res['horario']} hs"):
                    st.write(f"**Complejo:** {res['complejo']}")
                    st.write(f"**Seña a cobrar (30%):** ${res['seña']}")
                    col1, col2 = st.columns(2)
                    if col1.button("ACEPTAR", key=f"acp_{i}"):
                        res["estado"] = "Aprobada - Esperando Pago"
                        st.success("Aprobado. El jugador recibió el link de Mercado Pago.")
                    if col2.button("RECHAZAR", key=f"rej_{i}"):
                        st.session_state.reservas.pop(i)
                        st.error("Reserva rechazada.")

    st.divider()
    st.subheader("✅ Turnos Confirmados")
    for res in st.session_state.reservas:
        if res["estado"] == "Aprobada - Esperando Pago":
            st.write(f"✔️ {res['horario']} - {res['jugador']} (Saldo pendiente en cancha: ${res['total'] - res['seña']})")
