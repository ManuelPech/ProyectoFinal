import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
archivo_excel = "datos/registrosventas.xlsx"
datos_ventas = pd.read_excel(archivo_excel)

# Convertir la columna 'Fecha pedido' a formato de fecha
datos_ventas['Fecha pedido'] = pd.to_datetime(datos_ventas['Fecha pedido'])

# Páginas disponibles
paginas = ["👋 Bienvenida", "📊 Resumen Ejecutivo", "📈 Tendencias Temporales", "🗺️ Mapa de Ventas", "🔄 Comparación de Variables", "🛍️ Productos Más Vendidos"]

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

# Página de Bienvenida
if pagina_seleccionada == "👋 Bienvenida":
    st.title("¡Hola, esta es la página de bienvenida!")
    st.subheader(" ")
    st.subheader("👨‍💻 Nuestros integrantes")
    st.write("Conoce a nuestro talentoso equipo detrás de este proyecto:")

    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)

    # Imagen 1 en la primera columna
    col1.image("datos/MANU.png", caption="Manuel Alfonso Pech Ek", use_column_width=True)

    # Imagen 2 en la segunda columna
    col2.image("datos/PERFILDAMIAN.jpg", caption="Damian Emmanuel Dzul Gamboa", use_column_width=True)

    # Información destacada
    st.write("""
           ¡Hola! Te damos la bienvenida a nuestro completo Dashboard diseñado para proporcionarte una visión detallada y perspicaz de las ventas. Este análisis se centra en los registros de ventas, permitiéndote explorar tendencias temporales, visualizar el rendimiento geográfico a través de un mapa de ventas, comparar variables clave y descubrir los productos más vendidos.
        """)

    # Elementos interactivos
    st.markdown("### ¿Cómo empezar?")
    st.write("1. Utiliza el menú lateral para seleccionar la sección que deseas explorar.")
    st.write("2. Ajusta las fechas para obtener información específica sobre el periodo de interés.")
    st.write("3. ¡Explora y descubre insights valiosos en tus datos de ventas!")

    # Gráfico de barras
    categorias = ["Les gusta nuestro trabajo", "La opcion 1, pero no lo aceptan"]
    porcentajes = [81, 19]
    fig_barras = px.bar(x=categorias, y=porcentajes, text=porcentajes,
                        labels={'x': 'Opciones', 'y': 'Porcentaje'},
                        title='Opiniones de los compañeros',
                        color_discrete_sequence=['rgba(255, 182, 193, 0.7)', 'rgba(255, 105, 180, 0.7)'])

    fig_barras.update_traces(texttemplate='%{text:.2s}%', textposition='outside')
    st.plotly_chart(fig_barras)

# Página de Resumen Ejecutivo
elif pagina_seleccionada == "📊 Resumen Ejecutivo":
    # Título
    st.title("Resumen Ejecutivo")
    st.subheader(" ")
    st.write("Aquí encontrarás un resumen clave de las métricas ejecutivas relacionadas con las ventas. Este resumen te ofrece una visión rápida y clara del rendimiento financiero general durante el periodo seleccionado.")
    st.subheader(" ")

    # Calcular métricas clave
    totali = datos_filtrados['Importe venta total'].sum()
    totalc = datos_filtrados['Importe Coste total'].sum()
    margen_beneficio_promedio = ((totali - totalc) / totali) * 100
    utilidad = totali - totalc

    # Crear un DataFrame con el resumen
    resumen_data = {
        'Nombre': ['Ingresos Totales', 'Costos Totales', 'Utilidad Neta', 'Margen de Beneficio Promedio'],
        'Valor': [f"${totali:,.2f}", f"${totalc:,.2f}", f"${utilidad:,.2f}",
                  f"{margen_beneficio_promedio:.2f}%"]
    }
    resumen_df = pd.DataFrame(resumen_data)

    # Mostrar la tabla de resumen
    st.table(resumen_df)

# Página de Tendencias Temporales
elif pagina_seleccionada == "📈 Tendencias Temporales":
    # Título
    st.title("Gráfica de tendencias")
    st.subheader(" ")
    st.write("Visualiza la tendencia temporal de las ventas a lo largo del tiempo. Este gráfico te permite identificar patrones, picos y valles en el rendimiento de las ventas.")
    st.subheader(" ")

    # Verificar si las columnas necesarias están presentes en los datos filtrados
    if 'Fecha pedido' in datos_filtrados.columns and 'Importe venta total' in datos_filtrados.columns:
        # Mostrar el gráfico de líneas
        st.line_chart(datos_filtrados.set_index('Fecha pedido')[['Importe venta total']])
    else:
        # Mostrar un mensaje de advertencia si las columnas no están presentes
        st.warning('El DataFrame no tiene las columnas necesarias para la visualización.')

# Página de Mapa de Ventas
elif pagina_seleccionada == "🗺️ Mapa de Ventas":
    # Título
    st.title("Mapa de ventas")
    st.subheader(" ")
    st.write("Explora la distribución geográfica de las ventas mediante un mapa interactivo. Este mapa te proporciona una visión global del rendimiento de las ventas en diferentes regiones y países.")
    st.subheader(" ")

    # Crear choropleth map con color basado en el importe de venta total
    fig = px.choropleth(datos_filtrados,
                        locations='País',
                        color='Importe venta total',
                        hover_name='País',
                        title="Mapa de Ventas",
                        locationmode='country names',
                        color_continuous_scale='viridis',
                        range_color=(datos_filtrados['Importe venta total'].min(),
                                     datos_filtrados['Importe venta total'].max()),
                        labels={'Importe venta total': 'Importe de Venta Total'},
                        )

    # Mostrar el mapa de ventas
    st.plotly_chart(fig)

    # Subtítulo y gráfico de barras de distribución de ventas por país
    st.subheader("Distribución de Ventas")
    fig_ventas_por_pais = px.bar(datos_filtrados, x='País', y='Importe venta total',
                                 title='Ventas por País', labels={'Importe venta total': 'Ventas'})
    st.plotly_chart(fig_ventas_por_pais)

# Página de Comparación de Variables
elif pagina_seleccionada == "🔄 Comparación de Variables":
   # Título
    st.title("Comparación de Variables")
    st.subheader(" ")
    st.write(
        "Compara las variables clave, como las ventas y los costos, para cada país. Este análisis te permite identificar relaciones y patrones entre diferentes métricas de rendimiento.")
    st.subheader(" ")

    # Agrupar por país y sumar las ventas y costos
    datos_agrupados = datos_filtrados.groupby('País').agg(
        {'Importe venta total': 'sum', 'Importe Coste total': 'sum', 'Unidades': 'sum'}).reset_index()

    # Crear un gráfico de dispersión para comparar ventas y costos por país
    fig_comparacion = px.scatter(datos_agrupados, x='Importe venta total', y='Importe Coste total',
                                 color='País', size='Unidades',
                                 title='Comparación de Ventas vs. Costos por País')

    # Mostrar el gráfico de comparación
    st.plotly_chart(fig_comparacion)

# Página de Productos Más Vendidos
elif pagina_seleccionada == "🛍️ Productos Más Vendidos":
    # Título
    st.title("Productos más Vendidos")
    st.subheader(" ")
    st.write("Descubre los productos más vendidos y su contribución al total de unidades vendidas. Este análisis te permite identificar qué productos son los más populares y contribuyen significativamente al éxito general de las ventas.")
    st.subheader(" ")

    # Calcular las cantidades vendidas por tipo de producto
    productos_mas_vendidos = datos_filtrados.groupby('Tipo de producto')['Unidades'].sum().reset_index()

    # Crear un gráfico de pastel para mostrar los productos más vendidos
    fig_pie_productos_mas_vendidos = px.pie(productos_mas_vendidos, values='Unidades', names='Tipo de producto',
                                            title='Productos Más Vendidos', labels={'Unidades': 'Cantidad Vendida'})

    # Mostrar el gráfico de pastel
    st.plotly_chart(fig_pie_productos_mas_vendidos)
