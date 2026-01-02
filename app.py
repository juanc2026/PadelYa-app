import streamlit as st

# Configuración de página
st.set_page_config(page_title="PadelYa Posadas", page_icon="🎾", layout="centered")

# --- 1. ESTILO CSS (DISEÑO MODERNO) ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 0px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        overflow: hidden;
        border: 1px solid #eee;
    }
    .card-content { padding: 15px; }
    .stButton>button {
        border-radius: 12px;
        font-weight: bold;
    }
    /* Botón de Pago Amarillo */
    .pago-btn button {
        background-color: #f1c40f !important;
        color: black !important;
        height: 55px !important;
        font-size: 18px !important;
    }
    /* Botón WhatsApp Flotante */
    .whatsapp-float {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #25d366;
        color: white;
        border-radius: 50px;
        padding: 15px 20px;
        z-index: 100;
        text-decoration: none;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENCIA DE DATOS (BASE DE DATOS TEMPORAL) ---
if 'horarios' not in st.session_state:
    st.session_state.horarios = {
        "World Padel Center": ["18:00", "20:00", "22:00"],
        "La Terraza": ["19:00", "21:00"],
        "Padel Pro": ["17:00", "19:00", "21:00"]
    }

# --- BOTÓN FLOTANTE WHATSAPP ---
st.markdown('<a href="https://wa.me/543764000000" class="whatsapp-float">💬 Ayuda WhatsApp</a>', unsafe_allow_html=True)

# Lógica de Navegación
if 'paso' not in st.session_state: st.session_state.paso = "inicio"

# --- PANTALLA 1: EXPLORAR CANCHAS ---
if st.session_state.paso == "inicio":
    st.markdown("<h2 style='text-align: center; color: #1a2e2e;'>Canchas en Posadas</h2>", unsafe_allow_html=True)
    
    # Datos de los complejos (Punto 1: Fotos reales)
    complejos = [
        {"nombre": "World Padel Center", "img": "https://images.unsplash.com/photo-1626224484214-40d5d9c3c844?w=500", "ubi": "Costanera, Posadas"},
        {"nombre": "La Terraza", "img": "https://images.unsplash.com/photo-1592910129881-892b68e4210c?w=500", "ubi": "Av. Uruguay, Posadas"},
        {"nombre": "Padel Pro", "img": "https://images.unsplash.com/photo-1554068865-24bccd4e34b8?w=500", "ubi": "Itaembé Guazú, Posadas"}
    ]

    for comp in complejos:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <img src="{comp['img']}" style="width:100%; height:150px; object-fit:cover;">
                <div class="card-content">
                    <h3 style='margin:0; color: #1a2e2e;'>{comp['nombre']}</h3>
                    <p style='color:gray; margin:0;'>📍 {comp['ubi']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Ver Horarios en {comp['nombre']}", key=comp['nombre']):
                st.session_state.seleccionado = comp['nombre']
                st.session_state.paso = "horarios"
                st.rerun()

# --- PANTALLA 2: SELECCIONAR HORARIO ---
elif st.session_state.paso == "horarios":
    st.button("⬅️ Volver", on_click=lambda: setattr(st.session_state, 'paso', 'inicio'))
    st.title(st.session_state.seleccionado)
    st.subheader("Seleccioná tu Horario")
    
    disponibles = st.session_state.horarios[st.session_state.seleccionado]
    
    col1, col2 = st.columns(2)
    for i, h in enumerate(disponibles):
        col = col1 if i % 2 == 0 else col2
        if col.button(f"🟢 {h} hs", key=h):
            st.session_state.horario_final = h
            st.session_state.paso = "pago"
            st.rerun()

# --- PANTALLA 3: CONFIRMACIÓN Y PAGO ---
elif st.session_state.paso == "pago":
    st.button("⬅️ Cambiar Horario", on_click=lambda: setattr(st.session_state, 'paso', 'horarios'))
    st.markdown("<h2 style='text-align: center;'>Confirmar Reserva</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.write(f"**Complejo:** {st.session_state.seleccionado}")
        st.write(f"**Turno:** {st.session_state.horario_final} hs (120 min)")
        st.divider()
        st.write("💰 **Total:** $12.000")
        st.write("💳 **Seña requerida:** $3.600")
        
        nombre = st.text_input("Ingresá tu nombre completo:")
        
        st.markdown('<div class="pago-btn">', unsafe_allow_html=True)
        if st.button(f"PAGAR SEÑA ($3.600) 🔒"):
            if nombre:
                st.balloons()
                st.success(f"¡Reserva confirmada para {nombre}!")
                # Aquí podrías poner el link real de Mercado Pago
            else:
                st.error("Por favor, escribí tu nombre.")
        st.markdown('</div>', unsafe_allow_html=True)
