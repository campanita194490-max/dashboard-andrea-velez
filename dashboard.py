"""
Proyecto: Dashboard de Comercio Electrónico
Autora: Andrea Vélez Perdomo
Año: 2026

Descripción:
Dashboard interactivo desarrollado con Python y Streamlit
para el análisis de productos y ventas en ecommerce.

© 2026 Andrea Vélez Perdomo
Uso académico. Todos los derechos reservados.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# CONFIGURACIÓN DE LA PÁGINA (DEBE IR PRIMERO)
st.set_page_config(
    page_title="Dashboard Ecommerce",
    layout="wide"
)

# TITULO EN MOVIMIENTO REBOTANDO
st.markdown(
"""
<style>
@keyframes rebote {
0% { transform: translateX(-50px); }
50% { transform: translateX(50px); }
100% { transform: translateX(-50px); }
}

.titulo-movimiento {
font-size:40px;
font-weight:bold;
color:#1f77b4;
text-align:center;
animation: rebote 4s infinite;
}

.subtitulo-movimiento {
font-size:26px;
font-weight:bold;
color:#1f77b4;
text-align:center;
animation: rebote 4s infinite;
}
</style>

<div class="titulo-movimiento">
🛒 Dashboard de Comercio Electrónico | Análisis de Datos
</div>
""",
unsafe_allow_html=True
)

# LOGO
st.image("logo.png", width=200)

# INTRODUCCIÓN
st.header("Introducción")

st.write("""
En la actualidad, el análisis de datos se ha convertido en una herramienta fundamental para comprender el comportamiento de los mercados y apoyar la toma de decisiones.

En el ámbito del comercio electrónico, el análisis de información permite identificar tendencias, evaluar el desempeño de los productos y comprender las preferencias de los usuarios.

Este dashboard interactivo fue desarrollado utilizando Python y Streamlit con el objetivo de analizar datos de productos de comercio electrónico mediante visualizaciones, indicadores y filtros interactivos.
""")

# OBJETIVOS
st.subheader("Objetivos del Dashboard")

st.write("""
• Analizar el comportamiento de los productos en comercio electrónico.

• Identificar tendencias en precios, ventas y calificaciones de los productos.

• Explorar la relación entre variables importantes como precio, rating y volumen de ventas.

• Facilitar la toma de decisiones mediante visualizaciones interactivas y análisis de datos.

• Proporcionar una herramienta que permita explorar la información de manera clara, dinámica y comprensible.
""")

st.divider()

# CARGAR DATOS
df = pd.read_csv("ecommerce_data_5000 (1).csv")

# LIMPIAR NOMBRES
df.columns = df.columns.str.strip().str.lower()

# CREAR COLUMNA DE TIEMPO
df["año"] = np.random.randint(2019, 2024, size=len(df))

# DETECTAR COLUMNAS
texto_cols = df.select_dtypes(include="object").columns
num_cols = df.select_dtypes(include=["int64","float64"]).columns

col_producto = texto_cols[0]
col_categoria = texto_cols[1]

col_precio = num_cols[0]
col_rating = num_cols[1]
col_ventas = num_cols[2]

st.markdown(
"""
<div class="subtitulo-movimiento">
 Análisis interactivo de productos y ventas en ecommerce
</div>
""",
unsafe_allow_html=True
)

# FILTROS
st.sidebar.header("Filtros")

df_filtrado = df.copy()

# FILTRO AÑO
año = st.sidebar.selectbox(
    "Seleccionar año",
    sorted(df["año"].unique())
)

df_filtrado = df_filtrado[df_filtrado["año"] == año]

# FILTRO CATEGORÍA
categorias = st.sidebar.multiselect(
    "Categoría",
    options=df[col_categoria].unique(),
    default=df[col_categoria].unique()
)

df_filtrado = df_filtrado[df_filtrado[col_categoria].isin(categorias)]

# FILTRO PRECIO
precio_min = float(df[col_precio].min())
precio_max = float(df[col_precio].max())

rango_precio = st.sidebar.slider(
    "Rango de precio",
    precio_min,
    precio_max,
    (precio_min, precio_max)
)

df_filtrado = df_filtrado[
    (df_filtrado[col_precio] >= rango_precio[0]) &
    (df_filtrado[col_precio] <= rango_precio[1])
]

# FILTRO RATING
rating_min = st.sidebar.slider(
    "Rating mínimo",
    float(df[col_rating].min()),
    float(df[col_rating].max()),
    float(df[col_rating].min())
)

df_filtrado = df_filtrado[df_filtrado[col_rating] >= rating_min]

# FILTRO VENTAS
ventas_min = st.sidebar.slider(
    "Ventas mínimas",
    int(df[col_ventas].min()),
    int(df[col_ventas].max()),
    int(df[col_ventas].min())
)

df_filtrado = df_filtrado[df_filtrado[col_ventas] >= ventas_min]

# BUSCAR PRODUCTO
buscar = st.sidebar.text_input("Buscar producto")

if buscar:
    df_filtrado = df_filtrado[
        df_filtrado[col_producto].str.contains(buscar, case=False)
    ]

# ORDENAR PRODUCTOS
orden = st.sidebar.selectbox(
    "Ordenar productos por",
    [col_precio, col_rating, col_ventas]
)

df_filtrado = df_filtrado.sort_values(by=orden, ascending=False)

# KPIs
st.subheader("Indicadores principales")

k1,k2,k3,k4 = st.columns(4)

k1.metric("Productos", len(df_filtrado))
k2.metric("Ventas totales", int(df_filtrado[col_ventas].sum()))
k3.metric("Precio promedio", round(df_filtrado[col_precio].mean(),2))
k4.metric("Rating promedio", round(df_filtrado[col_rating].mean(),2))

st.divider()

# DESCARGAR DATOS
st.subheader("Descargar datos filtrados")

st.download_button(
    label="Descargar CSV",
    data=df_filtrado.to_csv(index=False).encode("utf-8"),
    file_name="datos_filtrados.csv",
    mime="text/csv"
)

st.divider()

# TABLA
st.subheader("Datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)

st.divider()

# GRÁFICOS
st.subheader("Visualización de datos")

fig1 = px.histogram(df_filtrado, x=col_precio, nbins=30, title="Distribución de precios")
st.plotly_chart(fig1, use_container_width=True)

cat_counts = df_filtrado[col_categoria].value_counts().reset_index()
cat_counts.columns = ["Categoria","Cantidad"]

fig2 = px.bar(cat_counts, x="Categoria", y="Cantidad", title="Productos por categoría")
st.plotly_chart(fig2, use_container_width=True)

ventas_cat = df_filtrado.groupby(col_categoria)[col_ventas].sum().reset_index()

fig3 = px.bar(ventas_cat, x=col_categoria, y=col_ventas, color=col_categoria, title="Ventas por categoría")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter(df_filtrado, x=col_precio, y=col_rating, color=col_categoria, title="Relación entre precio y rating")
st.plotly_chart(fig4, use_container_width=True)

# EVOLUCIÓN
st.subheader("Evolución de ventas por año")

ventas_año = df.groupby("año")[col_ventas].sum().reset_index()

fig6 = px.line(ventas_año, x="año", y=col_ventas, markers=True, title="Ventas por año")
st.plotly_chart(fig6, use_container_width=True)

# TOP PRODUCTOS
st.subheader("Top 10 productos más vendidos")

top = (
    df_filtrado
    .groupby(col_producto)[col_ventas]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig5 = px.bar(top, x=col_ventas, y=col_producto, orientation="h", title="Top productos")
st.plotly_chart(fig5, use_container_width=True)

# RANKING
st.subheader("Ranking de productos")

ranking = df_filtrado.sort_values(by=col_ventas, ascending=False)[[col_producto,col_categoria,col_ventas]]
st.dataframe(ranking.head(20))

st.divider()

# CONCLUSIONES
st.subheader("Conclusiones")

st.write("• Algunas categorías concentran mayor número de productos.")
st.write("• Los productos con mayor rating no siempre tienen el precio más alto.")
st.write("• Las categorías con más ventas muestran mayor demanda del mercado.")
st.write("• El análisis con dashboards facilita la toma de decisiones.")

# RECOMENDACIONES
st.subheader("Recomendaciones")

st.write("""
1. Analizar con mayor profundidad las categorías que presentan mayores ventas.

2. Evaluar las estrategias de precios de los productos.

3. Monitorear continuamente el comportamiento del mercado mediante dashboards interactivos.

4. Utilizar herramientas de análisis de datos como Python y Streamlit para apoyar la toma de decisiones.
""")

st.divider()

st.markdown(
"""
---
### Créditos del Proyecto

**Autora:** Andrea Vélez Perdomo  
**Proyecto:** Dashboard de Comercio Electrónico  
**Herramientas utilizadas:** Python, Streamlit, Pandas, Plotly  
**Año:** 2026
"""
)
