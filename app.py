import streamlit as st
import pandas as pd

# 1. Configuración de la página (Responsive y moderna)
st.set_page_config(page_title="Programa del Evento", page_icon="📅", layout="centered")

# 2. Diseño del Encabezado (Logo y Título)
# Guarda tu logo en la misma carpeta como 'logo.png'
try:
    st.image("logo.png", use_column_width=True) 
except:
    pass # Si no hay logo, simplemente no lo muestra

st.title("📅 Programa del Evento")
st.markdown("Consulta las actividades, horarios y conferencistas.")

# 3. Conexión a Google Sheets (Lectura en tiempo real)
# REEMPLAZA ESTA URL CON EL ENLACE CSV QUE COPIASTE EN EL PASO 1
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlHklmNiJDAhEYYVWVB05YVUdS-DfOhhTmzJX_AE7VZHikEH4fzAsV6A_-tZe7qQ/pub?gid=2138557096&single=true&output=csv"

# El decorador cache_data hace que se actualice cada 60 segundos
@st.cache_data(ttl=60) 
def load_data():
    # Leemos directamente el CSV público
    return pd.read_csv(SHEET_CSV_URL)

try:
    df = load_data()
    
    # 4. Filtro por Día (Diseño tipo Pestañas o Selector)
    st.subheader("Filtra por fecha")
    dias = df["Fecha"].unique()
    dia_seleccionado = st.selectbox("Selecciona el día del evento:", dias)
    
    # Filtramos el dataframe
    df_filtrado = df[df["Fecha"] == dia_seleccionado]
    
    st.write("---")
    
    # 5. Renderizado Moderno en "Tarjetas" (Ideal para Celulares)
    for index, row in df_filtrado.iterrows():
        with st.container():
            # Usamos columnas para darle un look de aplicación
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"### ⏰ {row['Hora']}")
                
            with col2:
                st.markdown(f"**📍 {row['Lugar']}**")
                st.markdown(f"#### {row['Actividad']}")
                if pd.notna(row['Moderador/Conferencista']):
                    st.markdown(f"**🗣️ Speaker:** {row['Moderador/Conferencista']}")
                if pd.notna(row['Tema']):
                    st.markdown(f"**📝 Tema:** {row['Tema']}")
            
            st.divider() # Línea divisoria elegante entre actividades
            
except Exception as e:
    st.error("Error al cargar los datos. Verifica que la URL de Google Sheets sea correcta y esté en formato CSV.")
    st.write(e)