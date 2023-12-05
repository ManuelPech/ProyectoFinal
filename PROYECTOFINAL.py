import pandas as pd
import streamlit as st
import requirements
with st.spinner('Instalando dependencias...'):
    requirements_file = 'requirements.txt'
    st.requirements(RequirementsFile(requirements_file))
from dash.dependencies import Input, Output
import plotly.express as px
# Cargar los datos
archivo_excel = "datos/registrosventas.xlsx"
datos_ventas = pd.read_excel(archivo_excel)

datos_ventas['Fecha pedido'] = pd.to_datetime(datos_ventas['Fecha pedido'])

# Título
st.title("Bienvenido, este es el Dashboard del Análisis de Ventas")

# Páginas dispoibles
paginas = ["Resumen Ejecutivo", "Distribución de Ventas", "Tendencias Temporales", "Mapa de Ventas", "Comparación de Variables", "Productos Más Vendidos"]

# Seleccionar la página
pagina_seleccionada = st.sidebar.selectbox("Selecciona una página", paginas)

# Filtrar datos según las fechas seleccionadas
fecha_minima = datos_ventas['Fecha pedido'].min().date()
fecha_maxima = datos_ventas['Fecha pedido'].max().date()
fecha_inicio = st.sidebar.date_input("Selecciona la fecha de inicio:",
                                     min_value=fecha_minima,
                                     max_value=fecha_maxima,
                                     value=fecha_minima)
fecha_fin = st.sidebar.date_input("Selecciona la fecha de fin:",
                                   min_value=fecha_inicio,
                                   max_value=fecha_maxima,
                                   value=fecha_maxima)
datos_filtrados = datos_ventas[(datos_ventas['Fecha pedido'] >= pd.to_datetime(fecha_inicio)) &
                               (datos_ventas['Fecha pedido'] <= pd.to_datetime(fecha_fin))]

# menuuuuu
if pagina_seleccionada == "Resumen Ejecutivo":
    st.subheader("Resumen Ejecutivo")

    totali = datos_filtrados['Importe venta total'].sum()
    totalc = datos_filtrados['Importe Coste total'].sum()
    margen_beneficio_promedio = ((totali - totalc) / totali) * 100
    utilidad = totali - totalc

    resumen_data = {
        'Nombre': ['Ingresos Totales', 'Costos Totales', 'Utilidad Neta', 'Margen de Beneficio Promedio'],
        'Valor': [f"${totali:,.2f}", f"${totalc:,.2f}", f"${utilidad:,.2f}",
                  f"{margen_beneficio_promedio:.2f}%"]
    }
    resumen_df = pd.DataFrame(resumen_data)
    st.table(resumen_df)

elif pagina_seleccionada == "Distribución de Ventas":
    st.subheader("Distribución de Ventas")
    fig_ventas_por_pais = px.bar(datos_filtrados, x='País', y='Importe venta total',
                                 title='Ventas por País', labels={'Importe venta total': 'Ventas'})
    st.plotly_chart(fig_ventas_por_pais)

elif pagina_seleccionada == "Tendencias Temporales":
    # tendencia
    st.title('Gráfica de Tendencias')

    if 'Fecha pedido' in datos_filtrados.columns and 'Importe venta total' in datos_filtrados.columns:
        st.line_chart(datos_filtrados.set_index('Fecha pedido')[['Importe venta total']])

    else:
        st.warning('El DataFrame no tiene las columnas necesarias para la visualización.')

elif pagina_seleccionada == "Mapa de Ventas":
    paises = datos_filtrados['País'].unique()
    paisseleccionado = st.sidebar.selectbox("Selecciona un país:", paises)

    # Filtrar d país seleccionado
    datos_pais = datos_filtrados[datos_filtrados['País'] == paisseleccionado]

    # Crear choropleth map
    fig = px.choropleth(datos_pais,
                        locations='País',
                        color='Importe venta total',
                        hover_name='País',
                        title=f"Mapa de Ventas para {paisseleccionado}",
                        locationmode='country names',
                        fitbounds="locations")
    fitbounds = "locations"
    st.plotly_chart(fig)
#tabla
    st.write(f"Información para {paisseleccionado}:")
    st.write(datos_pais)

elif pagina_seleccionada == "Comparación de Variables":
    st.subheader("Comparación de Variables")
    fig_comparacion = px.scatter(datos_filtrados, x='Importe venta total', y='Importe Coste total',
                                 color='País', size='Unidades',
                                 title='Comparación de Ventas vs. Costos por País')
    st.plotly_chart(fig_comparacion)

elif pagina_seleccionada == "Productos Más Vendidos":
    st.subheader("Productos Más Vendidos")
    # Productos Más Vendidos
    productos_mas_vendidos = datos_filtrados.groupby('Tipo de producto')['Unidades'].sum().reset_index()
    fig_pie_productos_mas_vendidos = px.pie(productos_mas_vendidos, values='Unidades', names='Tipo de producto',
                                            title='Productos Más Vendidos', labels={'Unidades': 'Cantidad Vendida'})
    st.plotly_chart(fig_pie_productos_mas_vendidos)
