import streamlit as st
from datetime import datetime

# Configuración de página estilo Mobile
st.set_page_config(page_title="PadelYa", page_icon="🎾", layout="centered")

# CSS para replicar el diseño de la imagen (Colores y formas)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #333; }
    
    /* Tarjetas de Complejos */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 0px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    .card-img {
        width: 100%; height: 120px;
        background-color: #2ecc71;
        background-image: linear-gradient(to bottom right, #2ecc71, #27ae60);
    }
    .card-content { padding: 15px; }
    
    /* Grilla de Horarios (Botones Verdes) */
    .stButton>button {
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        border: none;
    }
    
    /* Botón de Pago Amarillo */
    div[data-testid="stForm"] .stButton>button {
        background-color: #f1c40f !important;
        color: black !important;
        font-size: 18px !important;
        margin-top: 20px;
    }
    
    /* Tabs personalizadas */
    .stTabs [data-baseweb="tab-list"] { background-color: white; padding: 5px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Lógica de navegación simple
if 'pantalla' not in st.session_state:
    st.session_state.pantalla = "inicio"
if 'complejo_sel' not in st.session_state:
    st.session_state.complejo_sel = None

# --- PANTALLA 1: COMPLEJOS EN POSADAS ---
if st.session_state.pantalla == "inicio":
    st.markdown("<h2 style='text-align: center; color: #1a2e2e;'>Complejos en Posadas</h2>", unsafe_allow_html=True)
    
    canchas = [
        {"nombre": "World Padel Center", "ubi": "Costanera", "rating": "4.8"},
        {"nombre": "La Terraza", "ubi": "Av. Uruguay", "rating": "4.5"},
        {"nombre": "Padel Pro", "ubi": "Itaembé Guazú", "rating": "4.7"}
    ]
    
    for c in canchas:
        with st.container():
            st.markdown(f"""
            <div class="card">
                <div class="card-img"></div>
                <div class="card-content">
                    <h3 style='margin:0;'>{c['nombre']}</h3>
                    <p style='color:gray; margin:0;'>⭐ {c['rating']} | {c['ubi']}, Posadas</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Seleccionar {c['nombre']}", key=c['nombre']):
                st.session_state.complejo_sel = c['nombre']
                st.session_state.pantalla = "horarios"
                st.rerun()

# --- PANTALLA 2: SELECCIONAR HORARIO ---
elif st.session_state.pantalla == "horarios":
    if st.button("⬅️ Volver"):
        st.session_state.pantalla = "inicio"
        st.rerun()
        
    st.title(st.session_state.complejo_sel)
    st.subheader("Seleccionar Horario")
    
    # Días (como en la imagen)
    st.write("📅 **Enero 2026**")
    st.write("Hoy, Vie 02 | Sáb 03 | Dom 04 | Lun 05")
    
    st.markdown("---")
    st.write("🍀 **Césped Sintético**")
    
    # Grilla de horarios
    col1, col2 = st.columns(2)
    horarios = ["16:00", "17:30", "19:00", "20:30", "22:00", "23:30"]
    
    for i, h in enumerate(horarios):
        col = col1 if i % 2 == 0 else col2
        if col.button(h, key=f"h_{h}"):
            st.session_state.horario_sel = h
            st.session_state.pantalla = "pago"
            st.rerun()

# --- PANTALLA 3: CONFIRMAR Y PAGAR ---
elif st.session_state.pantalla == "pago":
    if st.button("⬅️ Cambiar Horario"):
        st.session_state.pantalla = "horarios"
        st.rerun()
        
    st.markdown("<h2 style='text-align: center;'>Confirmar Reserva</h2>", unsafe_allow_html=True)
    
    with st.form("pago_form"):
        st.write(f"**Complejo:** {st.session_state.complejo_sel}")
        st.write(f"**Horario:** {st.session_state.horario_sel} hs")
        st.write(f"**Duración:** 120 min")
        st.divider()
        st.write("💰 **Precio Total:** $12.000")
        st.write("💳 **Seña requerida (30%):** $3.600")
        
        nombre = st.text_input("Nombre completo")
        
        # El botón amarillo de la imagen
        enviar = st.form_submit_button(f"Pagar Seña ($3.600) 🔒")
        
        if enviar:
            if nombre:
                st.success(f"¡Reserva pre-confirmada para {nombre}!")
                st.info("Redirigiendo a Mercado Pago...")
                # Aquí iría el link real: st.link_button("Ir a MP", "URL")
            else:
                st.error("Por favor ingresá tu nombre")

# --- BOTÓN DE ADMINISTRACIÓN (FLOTANTE ABAJO) ---
st.sidebar.markdown("---")
if st.sidebar.button("🔐 Acceso Dueño"):
    st.session_state.pantalla = "inicio"
    st.sidebar.write("Clave: admin123")
