import streamlit as st
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Cargar los datos
archivo_excel = "datos/registrosventas.xlsx"
datos_ventas = pd.read_excel(archivo_excel)

datos_ventas['Fecha pedido'] = pd.to_datetime(datos_ventas['Fecha pedido'])

# Título
st.title("Bienvenido, este es el Dashboard del Análisis de Ventas")

# Páginas dispoibles
paginas = ["Bienvenida", "Resumen Ejecutivo", "Tendencias Temporales", "Mapa de Ventas", "Comparación de Variables", "Productos Más Vendidos"]

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
if pagina_seleccionada == "Bienvenida":
    st.subheader("¡Bienvenido al Dashboard de Análisis de Ventas!")

    # Información destacada
    st.write("""
            Esta aplicación proporciona información detallada sobre las ventas, 
            tendencias temporales, mapas de ventas, comparación de variables y productos más vendidos. 
            Utiliza el menú lateral para navegar entre las diferentes secciones y ajusta las fechas para 
            obtener información específica. ¡Explora y descubre insights valiosos!
        """)

    # Elementos interactivos
    st.markdown("### ¿Cómo empezar?")
    st.write("1. Utiliza el menú lateral para seleccionar la sección que deseas explorar.")
    st.write("2. Ajusta las fechas para obtener información específica sobre el periodo de interés.")
    st.write("3. ¡Explora y descubre insights valiosos en tus datos de ventas!")

    # Ejemplo de Insight
    st.markdown("### Ejemplo de Insight")
    st.write("Descubre cómo han evolucionado las ventas a lo largo del tiempo y realiza comparaciones detalladas.")

    # Enlace rápido a la sección de Tendencias Temporales
    st.markdown("[Ir a Tendencias Temporales](#)")

    # Elemento adicional
    st.markdown("### Prueba esta característica")
    if st.button("Haz clic aquí"):
        st.success("¡Bien hecho! Has descubierto una característica oculta. Sigue explorando.")

    # Testimonio ficticio
    st.markdown("""
            > "Esta aplicación ha cambiado la forma en que entendemos nuestras ventas. 
            > Es fácil de usar y proporciona insights valiosos de manera rápida."
        """)

# menuuuuu
elif pagina_seleccionada == "Resumen Ejecutivo":
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


elif pagina_seleccionada == "Tendencias Temporales":
    # tendencia
    st.title('Gráfica de Tendencias')

    if 'Fecha pedido' in datos_filtrados.columns and 'Importe venta total' in datos_filtrados.columns:
        st.line_chart(datos_filtrados.set_index('Fecha pedido')[['Importe venta total']])

    else:
        st.warning('El DataFrame no tiene las columnas necesarias para la visualización.')

elif pagina_seleccionada == "Mapa de Ventas":
    # Crear choropleth map con color basado en el importe de venta total
    fig = px.choropleth(datos_filtrados,
                        locations='País',
                        color='Importe venta total',
                        hover_name='País',
                        title="Mapa de Ventas",
                        locationmode='country names',
                        color_continuous_scale='viridis',  # Puedes cambiar 'viridis' por otra escala de color
                        range_color=(datos_filtrados['Importe venta total'].min(),
                                     datos_filtrados['Importe venta total'].max()),
                        labels={'Importe venta total': 'Importe de Venta Total'},
                        )
    st.plotly_chart(fig)

    st.subheader("Distribución de Ventas")
    fig_ventas_por_pais = px.bar(datos_filtrados, x='País', y='Importe venta total',
                                 title='Ventas por País', labels={'Importe venta total': 'Ventas'})
    st.plotly_chart(fig_ventas_por_pais)

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

