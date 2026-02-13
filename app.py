import streamlit as st
import pandas as pd
import urllib.parse

# ==========================================
# ⚙️ CONFIGURACIÓN GENERAL
# ==========================================
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRMqf84LupPoxeTv6HUpl-jlKcNggzROPpfE_wLpKdwzhnNEpHANPQwW9GIRf_DhCAHxDSO6kHcM1Yc/pub?output=csv"

WHATSAPP_NUMERO = "5493496527659" 

st.set_page_config(
    page_title="Backdoor - Hardware & Tecnologia",
    page_icon="💻",
    layout="wide"
)

# ==========================================
# 🎨 ESTILOS CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');

    .stApp { background-color: #000000 !important; }
    
    /* Ocultamos la sidebar por completo por si acaso */
    section[data-testid="stSidebar"] { display: none !important; }

    html, body, [class*="css"] {
        font-family: 'Lexend', sans-serif !important;
        color: #e0e0e0 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important; 
        font-weight: 600 !important;
    }

    .info-header {
        font-size: 1rem;
        margin-bottom: 20px;
        color: #cccccc;
    }
    .info-header a {
        color: #4da6ff;
        text-decoration: none;
        font-weight: 500;
    }
    .service-list {
        margin-top: 15px;
        line-height: 1.8;
        font-weight: 300;
        color: #ffffff;
    }

    /* Estilo para los filtros integrados */
    .filter-container {
        background-color: #111111;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        border: 1px solid #222222;
    }

    div[data-baseweb="select"] > div, input[type="text"] {
        background-color: #222222 !important;
        color: white !important;
        border-color: #444444 !important;
    }

    div[data-testid="stImage"] img {
        height: 200px !important;
        object-fit: contain !important;
        width: 100% !important;
        margin-bottom: 15px;
        background-color: #ffffff;
        border-radius: 5px;
        padding: 5px;
    }

    .precio-grande { font-size: 1.6rem; font-weight: 700; color: #ffffff; margin-bottom: 0px; }
    .metodo-pago { font-size: 0.8rem; color: #9e9e9e; margin-top: -5px; margin-bottom: 15px; display: block; font-weight: 300; }
    
    div.stButton > button:first-child {
        background-color: #ffffff; color: #000000; border: 1px solid #ffffff; 
        border-radius: 6px; font-weight: 600; transition: all 0.3s ease;
    }

    /* Limpieza de interfaz */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stActionButtonIcon"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 BACKEND (Sin cambios)
# ==========================================
def limpiar_precio(precio):
    if pd.isna(precio): return 0.0
    p_str = str(precio).replace('$', '').replace(' ', '').replace('.', '').replace(',', '.')
    try: return float(p_str)
    except ValueError: return 0.0

@st.cache_data(ttl=60)
def cargar_inventario():
    try:
        df = pd.read_csv(URL_CSV)
        df.columns = df.columns.str.strip().str.upper()
        df['PRECIO_FINAL'] = df['PV CONTADO'].apply(limpiar_precio)
        if 'DESCRIPCIÓN' in df.columns:
            df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].fillna("")
        mask_disponible = df['STOCK'].astype(str).str.upper().str.contains("EN STOCK", na=False)
        return df[mask_disponible].copy()
    except Exception as e:
        return pd.DataFrame()

def generar_link_whatsapp(producto, precio):
    mensaje = f"Hola Backdoor! Me interesa: {producto} - Precio: ${precio:,.0f}"
    return f"https://wa.me/{WHATSAPP_NUMERO}?text={urllib.parse.quote(mensaje)}"

# ==========================================
# 🖥️ FRONTEND
# ==========================================
def main():
    st.title("Backdoor - Hardware & Tecnologia")
    
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
    
    df = cargar_inventario()
    if df.empty:
        st.info("⏳ Cargando catálogo...")
        return

    # --- SECCIÓN DE FILTROS INTEGRADA ---
    st.markdown("### 🔍 Filtrar Productos")
    
    # Usamos st.columns para que los filtros queden uno al lado del otro
    col_cat, col_sub, col_ord, col_bus = st.columns([2, 2, 2, 3])
    
    with col_cat:
        lista_cat = ["Todas"] + sorted(df['CATEGORÍA'].astype(str).unique().tolist())
        cat_sel = st.selectbox("Categoría", lista_cat)

    df_filtrado = df.copy()
    if cat_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['CATEGORÍA'] == cat_sel]

    with col_sub:
        if 'SUBCATEGORÍA' in df.columns and cat_sel != "Todas":
            subs = df_filtrado['SUBCATEGORÍA'].dropna().unique().tolist()
            sub_sel = st.selectbox("Subcategoría", ["Todas"] + sorted([str(x) for x in subs]))
            if sub_sel != "Todas":
                df_filtrado = df_filtrado[df_filtrado['SUBCATEGORÍA'] == sub_sel]
        else:
            st.selectbox("Subcategoría", ["-"], disabled=True)

    with col_ord:
        orden = st.selectbox("Ordenar por", ["Destacados", "Menor Precio", "Mayor Precio"])
        if orden == "Menor Precio":
            df_filtrado = df_filtrado.sort_values("PRECIO_FINAL", ascending=True)
        elif orden == "Mayor Precio":
            df_filtrado = df_filtrado.sort_values("PRECIO_FINAL", ascending=False)

    with col_bus:
        busqueda = st.text_input("Buscar por nombre...")
        if busqueda:
            mask = df_filtrado['NOMBRE'].str.contains(busqueda, case=False) | df_filtrado['DESCRIPCIÓN'].str.contains(busqueda, case=False)
            df_filtrado = df_filtrado[mask]

    st.markdown("---")
    st.write(f"Mostrando {len(df_filtrado)} productos")

    # --- GRILLA DE PRODUCTOS ---
    cols = st.columns(3)
    for i, (index, row) in enumerate(df_filtrado.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                img = row['IMAGEN'] if 'IMAGEN' in df.columns else None
                st.image(img if pd.notna(img) and str(img).startswith('http') else "https://via.placeholder.com/400", use_container_width=True)
                
                nombre_limpio = row['NOMBRE'].replace('*', '').strip()
                st.markdown(f"**{nombre_limpio}**")
                
                if pd.notna(row['DESCRIPCIÓN']):
                    st.caption(str(row['DESCRIPCIÓN']).strip())
                
                st.markdown(f'<div class="precio-grande">$ {row["PRECIO_FINAL"]:,.0f}</div><span class="metodo-pago">Efectivo / Transferencia</span>', unsafe_allow_html=True)
                
                link = generar_link_whatsapp(nombre_limpio, row['PRECIO_FINAL'])
                st.link_button("Consultar", link, type="secondary", use_container_width=True)

if __name__ == "__main__":
    main()