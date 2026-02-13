import streamlit as st
import pandas as pd
import urllib.parse

# ==========================================
# ⚙️ CONFIGURACIÓN GENERAL
# ==========================================
# Link directo a tu CSV publicado
URL_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRMqf84LupPoxeTv6HUpl-jlKcNggzROPpfE_wLpKdwzhnNEpHANPQwW9GIRf_DhCAHxDSO6kHcM1Yc/pub?output=csv"

# TU NÚMERO DE WHATSAPP (Sin espacios ni símbolos)
WHATSAPP_NUMERO = "5493496527659" 

st.set_page_config(
    page_title="Backdoor - Hardware & Tecnologia",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🎨 ESTILOS CSS (THEME: BLACK & WHITE ENTERPRISE)
# ==========================================
st.markdown("""
    <style>
    /* 1. Importar fuente Lexend */
    @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@300;400;500;600;700&display=swap');

    /* 2. FORZAR FONDO NEGRO (Blindaje contra Modo Claro) */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* Barra lateral un poco más clara para diferenciar */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
    }

    /* 3. Tipografía Global */
    html, body, [class*="css"] {
        font-family: 'Lexend', sans-serif !important;
        color: #e0e0e0 !important; /* Gris claro para lectura */
    }

    /* 4. Títulos (Blancos puros) */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important; 
        font-weight: 600 !important;
    }

    /* 5. Inputs y Selectores (Adaptados al tema oscuro) */
    div[data-baseweb="select"] > div {
        background-color: #222222 !important;
        color: white !important;
        border-color: #444444 !important;
    }
    input[type="text"] {
        background-color: #222222 !important;
        color: white !important;
        border-color: #444444 !important;
    }
    label {
        color: #cccccc !important;
    }

    /* 6. IMÁGENES DE PRODUCTOS */
    div[data-testid="stImage"] img {
        height: 200px !important;
        object-fit: contain !important;
        width: 100% !important;
        margin-bottom: 15px;
        background-color: #ffffff; /* Fondo blanco detrás de la foto para PNGs transparentes */
        border-radius: 5px;
        padding: 5px; /* Pequeño marco blanco */
    }

    /* 7. PRECIOS Y PAGOS */
    .precio-grande {
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff; 
        margin-bottom: 0px;
    }
    .metodo-pago {
        font-size: 0.8rem;
        color: #9e9e9e; /* Gris medio */
        margin-top: -5px;
        margin-bottom: 15px;
        display: block;
        font-weight: 300;
    }

    /* 8. BOTÓN (Estilo Backdoor Minimalista) */
    div.stButton > button:first-child {
        background-color: #ffffff; /* Botón Blanco */
        color: #000000; /* Texto Negro */
        border: 1px solid #ffffff; 
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #000000; /* Al pasar el mouse: Fondo Negro */
        color: #ffffff; /* Texto Blanco */
        border-color: #ffffff;
        transform: scale(1.02); /* Efecto Zoom sutil */
    }

    /* 9. Limpieza de interfaz (Ocultar menú de Streamlit) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 BACKEND (LÓGICA DE DATOS)
# ==========================================
def limpiar_precio(precio):
    """Convierte texto sucio ($ 1.200,00) a número float (1200.0)"""
    if pd.isna(precio): return 0.0
    p_str = str(precio).replace('$', '').replace(' ', '').replace('.', '').replace(',', '.')
    try:
        return float(p_str)
    except ValueError:
        return 0.0

@st.cache_data(ttl=60) # Actualiza cada 60 segundos
def cargar_inventario():
    try:
        df = pd.read_csv(URL_CSV)
        
        # Normalizar nombres de columnas
        df.columns = df.columns.str.strip().str.upper()
        
        # Validar columnas críticas
        if 'STOCK' not in df.columns or 'PV CONTADO' not in df.columns:
            st.error("Error crítico: No encuentro las columnas STOCK o PV CONTADO en el Excel.")
            return pd.DataFrame()

        # Limpieza de datos
        df['PRECIO_FINAL'] = df['PV CONTADO'].apply(limpiar_precio)
        
        # Rellenar descripciones vacías para evitar errores
        if 'DESCRIPCIÓN' in df.columns:
            df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].fillna("")

        # FILTRO PRINCIPAL: Solo mostrar lo que dice "EN STOCK"
        mask_disponible = df['STOCK'].astype(str).str.upper().str.contains("EN STOCK", na=False)
        return df[mask_disponible].copy()
        
    except Exception as e:
        st.error(f"Error cargando el catálogo: {e}")
        return pd.DataFrame()

def generar_link_whatsapp(producto, precio):
    """Genera un link seguro para todos los dispositivos"""
    mensaje = f"Hola Backdoor! Me interesa: {producto} - Precio: ${precio:,.0f} (Efectivo/Transf)"
    mensaje_encoded = urllib.parse.quote(mensaje)
    telefono = WHATSAPP_NUMERO.replace("+", "").replace(" ", "").strip()
    return f"https://wa.me/{telefono}?text={mensaje_encoded}"

# ==========================================
# 🖥️ FRONTEND (INTERFAZ)
# ==========================================
def main():
    # --- TÍTULO PRINCIPAL ---
    st.title("Backdoor - Hardware & Tecnologia")
    st.markdown("---")
    
    df = cargar_inventario()
    
    if df.empty:
        st.info("⏳ Cargando catálogo o sin stock disponible...")
        return

    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.header("Filtros")
    
    # 1. Categoría
    lista_cat = ["Todas"] + sorted(df['CATEGORÍA'].astype(str).unique().tolist())
    cat_sel = st.sidebar.selectbox("Categoría", lista_cat)
    
    df_filtrado = df.copy()
    if cat_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['CATEGORÍA'] == cat_sel]
        
        # 2. Subcategoría (Cascada)
        if 'SUBCATEGORÍA' in df.columns:
            subs = df_filtrado['SUBCATEGORÍA'].dropna().unique().tolist()
            if subs:
                lista_sub = ["Todas"] + sorted([str(x) for x in subs])
                sub_sel = st.sidebar.selectbox("Subcategoría", lista_sub)
                if sub_sel != "Todas":
                    df_filtrado = df_filtrado[df_filtrado['SUBCATEGORÍA'] == sub_sel]

    # 3. Ordenar
    # "Destacados" = Orden original del Excel (Fila 1, Fila 2, etc.)
    orden = st.sidebar.selectbox("Ordenar por:", ["Destacados", "Menor Precio", "Mayor Precio"])
    
    if orden == "Menor Precio":
        df_filtrado = df_filtrado.sort_values("PRECIO_FINAL", ascending=True)
    elif orden == "Mayor Precio":
        df_filtrado = df_filtrado.sort_values("PRECIO_FINAL", ascending=False)

    # 4. Buscador Inteligente
    busqueda = st.sidebar.text_input("Buscar producto")
    if busqueda:
        # Busca tanto en el Nombre como en la Descripción
        mask_nombre = df_filtrado['NOMBRE'].astype(str).str.contains(busqueda, case=False, na=False)
        mask_desc = df_filtrado['DESCRIPCIÓN'].astype(str).str.contains(busqueda, case=False, na=False)
        df_filtrado = df_filtrado[mask_nombre | mask_desc]

    # --- GRILLA DE PRODUCTOS ---
    st.write(f"Mostrando {len(df_filtrado)} productos")
    
    # Grid de 3 columnas
    cols = st.columns(3)
    
    for i, (index, row) in enumerate(df_filtrado.iterrows()):
        with cols[i % 3]:
            # Contenedor estilo Tarjeta
            with st.container(border=True):
                
                # A. IMAGEN
                img = row['IMAGEN'] if 'IMAGEN' in df.columns else None
                if pd.isna(img) or not str(img).startswith('http'):
                    # Placeholder oscuro si no hay foto
                    st.image("https://via.placeholder.com/400x400/222222/555555?text=Backdoor", use_container_width=True)
                else:
                    st.image(img, use_container_width=True)

                # B. NOMBRE DEL PRODUCTO
                # Quitamos asteriscos o espacios extra
                nombre_limpio = row['NOMBRE'].replace('*', '').strip()
                st.markdown(f"**{nombre_limpio}**")
                
                # C. DESCRIPCIÓN (¡Agregado!)
                # Solo se muestra si existe y no está vacía
                desc = row['DESCRIPCIÓN'] if 'DESCRIPCIÓN' in df.columns else None
                if pd.notna(desc) and str(desc).strip() != "":
                    st.caption(str(desc).strip())
                
                # D. PRECIO Y METODO DE PAGO
                precio_fmt = f"{row['PRECIO_FINAL']:,.0f}"
                st.markdown(f"""
                    <div class="precio-grande">$ {precio_fmt}</div>
                    <span class="metodo-pago">Efectivo / Transferencia</span>
                """, unsafe_allow_html=True)
                
                # E. BOTÓN DE CONSULTA
                link = generar_link_whatsapp(nombre_limpio, row['PRECIO_FINAL'])
                st.link_button("Consultar", link, type="secondary", use_container_width=True)

if __name__ == "__main__":
    main()