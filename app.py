import streamlit as st

# CONFIGURACIÓN DE IMAGEN Y DISEÑO
st.set_page_config(page_title="PadelYa", page_icon="🎾", layout="centered")

# CSS para que se vea como el diseño de la imagen
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #0b1e1e;
    }
    
    /* Títulos y textos */
    h1, h2, h3, p, span {
        color: white !important;
        font-family: 'sans-serif';
    }

    /* Tarjetas de complejos */
    .cancha-card {
        background-color: #1a2e2e;
        padding: 15px;
        border-radius: 15px;
        border-left: 5px solid #2ecc71;
        margin-bottom: 20px;
    }

    /* Botón principal estilo PadelYa (Amarillo) */
    .stButton>button {
        background-color: #f1c40f !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        border: none !important;
        height: 3em !important;
        text-transform: uppercase;
    }

    /* Estilo de los inputs */
    .stSelectbox, .stTextInput {
        background-color: #1a2e2e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ENCABEZADO
st.title("🎾 PadelYa")
st.write("Reserva tu turno de 120 min en Posadas")

# MENÚ LATERAL
menu = st.sidebar.radio("Navegación", ["Explorar Canchas", "Mis Reservas", "Panel Dueño"])

if 'reservas' not in st.session_state:
    st.session_state.reservas = []

# --- PANTALLA 1: EXPLORAR (EL DISEÑO QUE VISTE) ---
if menu == "Explorar Canchas":
    st.subheader("Complejos en Posadas")
    
    # Simulación de las tarjetas de la imagen
    with st.container():
        st.markdown("""
        <div class="cancha-card">
            <h4>World Padel Center</h4>
            <p>⭐ 4.8 | Costanera, Posadas</p>
            <p><b>Precio 120 min: $12.000</b></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("RESERVAR EN WORLD PADEL"):
            st.session_state.paso = "horario"
            st.session_state.complejo_sel = "World Padel Center"

    with st.container():
        st.markdown("""
        <div class="cancha-card">
            <h4>La Terraza</h4>
            <p>⭐ 4.5 | Av. Uruguay, Posadas</p>
            <p><b>Precio 120 min: $11.500</b></p>
        </div>
        """, unsafe_allow_html=True)
        st.button("RESERVAR EN LA TERRAZA")

# --- PANTALLA 2: SELECCIÓN DE HORARIO ---
if menu == "Explorar Canchas" and 'complejo_sel' in st.session_state:
    st.divider()
    st.subheader(f"Horarios para {st.session_state.complejo_sel}")
    hora = st.select_slider("Seleccioná tu bloque de 2 horas:", 
                           options=["18:00 a 20:00", "20:00 a 22:00", "22:00 a 00:00"])
    
    nombre = st.text_input("Tu nombre para la reserva:")
    
    if st.button("SOLICITAR AHORA"):
        st.session_state.reservas.append({
            "jugador": nombre,
            "horario": hora,
            "estado": "Pendiente",
            "complejo": st.session_state.complejo_sel
        })
        st.balloons()
        st.success("¡Solicitud enviada! El dueño te confirmará en breve.")

# --- PANTALLA 3: PANEL DUEÑO ---
if menu == "Panel Dueño":
    st.subheader("Gestión de Turnos")
    if not st.session_state.reservas:
        st.write("No hay solicitudes hoy.")
    else:
        for i, res in enumerate(st.session_state.reservas):
            st.markdown(f"""
            <div style="background-color:#2c3e50; padding:10px; border-radius:10px; margin-bottom:10px">
                <p>Jugador: {res['jugador']}<br>Horario: {res['horario']}<br>Estado: {res['estado']}</p>
            </div>
            """, unsafe_allow_html=True)
            if res['estado'] == "Pendiente":
                if st.button(f"ACEPTAR TURNO DE {res['jugador']}", key=i):
                    res['estado'] = "Aprobado - Esperando Seña"
                    st.rerun()
