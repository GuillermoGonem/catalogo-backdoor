import streamlit as st
import pandas as pd
import urllib.parse

# ==========================================
# ⚙️ CONFIGURACIÓN GENERAL
# ==========================================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRMqf84LupPoxeTv6HUpl-jlKcNggzROPpfE_wLpKdwzhnNEpHANPQwW9GIRf_DhCAHxDSO6kHcM1Yc/pub?output=csv"

# ¡NÚMERO ACTUALIZADO!
WHATSAPP_NUMERO = "5493496527659" 

st.set_page_config(
    page_title="Backdoor - Hardware & Tecnologia",
    page_icon="💻", # <--- Icono de Notebook
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🎨 ESTILOS CSS (THEME: BLACK & WHITE ENTERPRISE)
# ==========================================
st.markdown("""
    <style>
    /* 1. Importar Lexend */
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');

    /* 2. FORZAR FONDO NEGRO */
    .stApp { background-color: #000000 !important; }
    section[data-testid="stSidebar"] { background-color: #111111 !important; }

    /* 3. Tipografía Global */
    html, body, [class*="css"] {
        font-family: 'Lexend', sans-serif !important;
        color: #e0e0e0 !important;
    }

    /* 4. Títulos (Blancos) */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important; 
        font-weight: 600 !important;
    }

    /* 5. Estilo para la Info de Cabecera (Instagram/Servicios) */
    .info-header {
        font-size: 1rem;
        margin-bottom: 20px;
        color: #cccccc;
    }
    .info-header a {
        color: #4da6ff; /* Azulito tipo link moderno */
        text-decoration: none;
        font-weight: 500;
    }
    .service-list {
        margin-top: 15px;
        line-height: 1.8;
        font-weight: 300;
        color: #ffffff;
    }

    /* 6. Inputs y Selectores */
    div[data-baseweb="select"] > div, input[type="text"] {
        background-color: #222222 !important;
        color: white !important;
        border-color: #444444 !important;
    }
    label { color: #cccccc !important; }

    /* 7. Imágenes de Productos */
    div[data-testid="stImage"] img {
        height: 200px !important;
        object-fit: contain !important;
        width: 100% !important;
        margin-bottom: 15px;
        background-color: #ffffff;
        border-radius: 5px;
        padding: 5px;
    }

    /* 8. Precios y Botones */
    .precio-grande { font-size: 1.6rem; font-weight: 700; color: #ffffff; margin-bottom: 0px; }
    .metodo-pago { font-size: 0.8rem; color: #9e9e9e; margin-top: -5px; margin-bottom: 15px; display: block; font-weight: 300; }
    
    div.stButton > button:first-child {
        background-color: #ffffff; color: #000000; border: 1px solid #ffffff; 
        border-radius: 6px; font-weight: 600; transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #000000; color: #ffffff; border-color: #ffffff; transform: scale(1.02);
    }

    /* 9. Limpieza */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 BACKEND
# ==========================================
def limpiar_precio(precio):
    if pd.isna(precio): return 0.0
    p_str = str(precio).replace('$', '').replace(' ', '').replace('.', '').replace(',', '.')
    try:
        return float(p_str)
    except ValueError:
        return 0.0

@st.cache_data(ttl=60)
def cargar_inventario():
    try:
        df = pd.read_csv(URL_CSV)
        df.columns = df.columns.str.strip().str.upper()
        
        if 'STOCK' not in df.columns or 'PV CONTADO' not in df.columns:
            st.error("Error: Revisar columnas del Excel.")
            return pd.DataFrame()

        df['PRECIO_FINAL'] = df['PV CONTADO'].apply(limpiar_precio)
        if 'DESCRIPCIÓN' in df.columns:
            df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].fillna("")

        mask_disponible = df['STOCK'].astype(str).str.upper().str.contains("EN STOCK", na=False)
        return df[mask_disponible].copy()
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

def generar_link_whatsapp(producto, precio):
    mensaje = f"Hola Backdoor! Me interesa: {producto} - Precio: ${precio:,.0f} (Efectivo/Transf)"
    mensaje_encoded = urllib.parse.quote(mensaje)
    telefono = WHATSAPP_NUMERO.replace("+", "").replace(" ", "").strip()
    return f"https://wa.me/{telefono}?text={mensaje_encoded}"

# ==========================================
# 🖥️ FRONTEND
# ==========================================
def main():
    # --- TÍTULO Y CABECERA ---
    st.title("Backdoor - Hardware & Tecnologia")
    
    # Bloque de Info de Contacto y Servicios
    st.markdown("""
        <div class="info-header">
            📸 Instagram: <a href="https://www.instagram.com/backdoor_tecnologia/" target="_blank">@backdoor_tecnologia</a> <br>
            💬 WhatsApp: <a href="https://wa.me/5493496527659" target="_blank">+54 9 3496 52-7659</a>
            <div class="service-list">
                💻 | PCs, notebooks y periféricos.<br>
                🛠️ | Soporte técnico.<br>
                🚀 | Hacé tu pedido, envíos a todo el país.<br>
                💳 | Efectivo, transferencia y tarjetas de crédito.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    df = cargar_inventario()
    
    if df.empty:
        st.info("⏳ Cargando catálogo...")
        return

    # --- FILTROS ---
    st.sidebar.header("Filtros")
    lista_cat = ["Todas"] + sorted(df['CATEGORÍA'].astype(str).unique().tolist())
    cat_sel = st.sidebar.selectbox("Categoría", lista_cat)
    
    df_filtrado = df.copy()
    if cat_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['CATEGORÍA'] == cat_sel]
        if 'SUBCATEGORÍA' in df.columns:
            subs = df_filtrado['SUBCATEGORÍA'].dropna().unique().tolist()
            if subs:
                lista_sub = ["Todas"] + sorted([str(x) for x in subs])
                sub_sel = st.sidebar.selectbox("Subcategoría", lista_sub)
                if sub_sel != "Todas":
                    df_filtrado = df_filtrado[df_filtrado['SUBCATEGORÍA'] == sub_sel]

    orden = st.sidebar.selectbox("Ordenar por:", ["Destacados", "Menor Precio", "Mayor Precio"])
    if orden == "Menor Precio":
        df_filtrado = df_filtrado.sort_values("PRECIO_FINAL", ascending=True)
    elif orden == "Mayor Precio":
        df_filtrado = df_filtrado.sort_values("PRECIO_FINAL", ascending=False)

    busqueda = st.sidebar.text_input("Buscar producto")
    if busqueda:
        mask_nombre = df_filtrado['NOMBRE'].astype(str).str.contains(busqueda, case=False, na=False)
        mask_desc = df_filtrado['DESCRIPCIÓN'].astype(str).str.contains(busqueda, case=False, na=False)
        df_filtrado = df_filtrado[mask_nombre | mask_desc]

    # --- GRILLA ---
    st.write(f"Mostrando {len(df_filtrado)} productos")
    cols = st.columns(3)
    
    for i, (index, row) in enumerate(df_filtrado.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                # Imagen
                img = row['IMAGEN'] if 'IMAGEN' in df.columns else None
                if pd.isna(img) or not str(img).startswith('http'):
                    st.image("https://via.placeholder.com/400x400/222222/555555?text=Backdoor", use_container_width=True)
                else:
                    st.image(img, use_container_width=True)

                # Nombre
                nombre_limpio = row['NOMBRE'].replace('*', '').strip()
                st.markdown(f"**{nombre_limpio}**")
                
                # Descripción
                desc = row['DESCRIPCIÓN'] if 'DESCRIPCIÓN' in df.columns else None
                if pd.notna(desc) and str(desc).strip() != "":
                    st.caption(str(desc).strip())
                
                # Precio
                precio_fmt = f"{row['PRECIO_FINAL']:,.0f}"
                st.markdown(f"""
                    <div class="precio-grande">$ {precio_fmt}</div>
                    <span class="metodo-pago">Efectivo / Transferencia</span>
                """, unsafe_allow_html=True)
                
                # Botón
                link = generar_link_whatsapp(nombre_limpio, row['PRECIO_FINAL'])
                st.link_button("Consultar", link, type="secondary", use_container_width=True)

if __name__ == "__main__":
    main()