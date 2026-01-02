import streamlit as st
from datetime import time

# Configuración de estilo "App Mobile"
st.set_page_config(page_title="PadelYa Posadas", page_icon="🎾", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; font-weight: bold; }
    .stSelectbox { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎾 PadelYa")
st.caption("Reserva tu turno de 120 min en Posadas")

# Simulamos base de datos en la sesión
if 'reservas' not in st.session_state:
    st.session_state.reservas = []

menu = st.sidebar.selectbox("Menú", ["Reservar Turno", "Soy Dueño (Panel)"])

# --- VISTA JUGADOR ---
if menu == "Reservar Turno":
    st.subheader("📍 Elegí tu Cancha")
    complejo = st.selectbox("Complejo:", ["World Padel Center", "La Terraza", "Padel Pro"])
    
    precio_total = 12000
    monto_seña = precio_total * 0.30
    
    st.info(f"Precio: ${precio_total} | Seña: ${monto_seña:.0f}")
    
    horario = st.select_slider("Horario (2 horas):", 
                               options=["16:00 a 18:00", "18:00 a 20:00", "20:00 a 22:00", "22:00 a 00:00"])
    
    nombre = st.text_input("Tu Nombre:")
    
    if st.button("SOLICITAR TURNO"):
        if nombre:
            nueva_reserva = {
                "jugador": nombre,
                "complejo": complejo,
                "horario": horario,
                "estado": "Pendiente",
                "seña": monto_seña
            }
            st.session_state.reservas.append(nueva_reserva)
            st.success("📩 Solicitud enviada. Avisale al dueño para que la apruebe.")
        else:
            st.error("Por favor, poné tu nombre.")

# --- PANEL DEL DUEÑO ---
else:
    st.subheader("📋 Gestión de Turnos")
    
    if not st.session_state.reservas:
        st.write("No hay pedidos pendientes.")
    else:
        for i, res in enumerate(st.session_state.reservas):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**{res['jugador']}** - {res['horario']}")
                st.caption(f"Estado: {res['estado']}")
            
            with col2:
                if res["estado"] == "Pendiente":
                    if st.button("✅ APROBAR", key=f"ok_{i}"):
                        res["estado"] = "Aprobado (Pagar Seña)"
                        st.rerun()
                
                # BOTÓN DE MERCADO PAGO REAL (Aparece cuando el dueño aprueba)
                if res["estado"] == "Aprobado (Pagar Seña)":
                    # AQUÍ PEGAS TU LINK DE MERCADO PAGO
                    link_mp = "https://www.mercadopago.com.ar" 
                    st.link_button("💳 PAGAR SEÑA", link_mp, type="primary")

    if st.button("Limpiar historial (Prueba)"):
        st.session_state.reservas = []
        st.rerun()
