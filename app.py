import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Control de Gastos Hormiga", layout="wide")
st.title("📊 Mi Gestor de Gastos Personales")

# --- ANALYTICAL CHALLENGE / PERSPECTIVA CRÍTICA ---
# ¿Por qué categorizar tan al detalle? En economía conductual, separar "comida" de "comida extra"
# rompe el sesgo de autoengaño. Nos ayuda a ver el costo de oportunidad real.

# Inicializar el estado de la aplicación para guardar datos en memoria
if 'categorias' not in st.session_state:
    st.session_state.categorias = ["Comida extra", "Refrescos", "Dulces o snacks", "Cuidado personal", "Gasto social", "Gasolina extra"]

if 'historial_gastos' not in st.session_state:
    st.session_state.historial_gastos = pd.DataFrame(columns=["Fecha", "Categoría", "Monto", "Descripción"])

# --- SECCIÓN 1: GESTIÓN DE CATEGORÍAS ---
st.sidebar.header("⚙️ Configuración")
nueva_categoria = st.sidebar.text_input("Añadir nueva categoría:")
if st.sidebar.button("Agregar Categoría") and nueva_categoria:
    if nueva_categoria not in st.session_state.categorias:
        st.session_state.categorias.append(nueva_categoria)
        st.sidebar.success(f"'{nueva_categoria}' añadida.")
    else:
        st.sidebar.warning("La categoría ya existe.")

# --- SECCIÓN 2: REGISTRO DE GASTOS ---
st.header("📝 Registrar Nuevo Gasto")
col1, col2, col3 = st.columns(3)

with col1:
    categoria_seleccionada = st.selectbox("Selecciona la categoría:", st.session_state.categorias)
with col2:
    monto = st.number_input("Monto ($):", min_value=0.0, step=1.0, format="%.2f")
with col3:
    descripcion = st.text_input("Descripción (opcional):", placeholder="Ej. Coca-Cola con amigos")

if st.button("Guardar Gasto", use_container_width=True):
    if monto > 0:
        nuevo_gasto = {
            "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Categoría": categoria_seleccionada,
            "Monto": monto,
            "Descripción": descripcion
        }
        # Añadir al DataFrame
        st.session_state.historial_gastos = pd.concat([st.session_state.historial_gastos, pd.DataFrame([nuevo_gasto])], ignore_index=True)
        st.success("¡Gasto registrado con éxito!")
    else:
        st.error("Por favor, introduce un monto mayor a 0.")

---

# --- SECCIÓN 3: VISUALIZACIÓN Y GRÁFICOS ---
st.header("📉 Análisis de tus Gastos")

if not st.session_state.historial_gastos.empty:
    df = st.session_state.historial_gastos
    
    # Métricas clave
    total_gastado = df["Monto"].sum()
    st.metric(label="Total Gastado hasta ahora", value=f"${total_gastado:,.2f}")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Distribución por Categoría")
        # Agrupar datos para el gráfico de pastel
        df_grouped = df.groupby("Categoría")["Monto"].sum().reset_index()
        fig_pie = px.pie(df_grouped, values="Monto", names="Categoría", hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_graf2:
        st.subheader("Historial Reciente")
        st.dataframe(df.sort_values(by="Fecha", ascending=False), use_container_width=True)
else:
    st.info("Aún no has registrado ningún gasto. ¡Empieza llenando el formulario de arriba!")
