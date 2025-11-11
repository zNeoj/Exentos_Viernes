import streamlit as st
import pandas as pd
import numpy as np
import io
import math
import plotly.express as px
import plotly.figure_factory as ff


# Cargar datos educativos
df = pd.read_csv('Datos/StudentPerformanceFactors.csv')

# Obtener las métricas generales
# Promedio de horas estudiadas por nivel de motivación
alta_motivacion = df[df['Motivation_Level'] == 'High']
alta_motivacion_media = alta_motivacion['Hours_Studied'].mean()

baja_motivacion = df[df['Motivation_Level'] == 'Low']
baja_motivacion_media = baja_motivacion['Hours_Studied'].mean()

# Cantidad por nivel de motivación
motivacion_counts = df['Motivation_Level'].value_counts()
alta_motivacion_count = motivacion_counts.get('High', 0)
media_motivacion_count = motivacion_counts.get('Medium', 0)
baja_motivacion_count = motivacion_counts.get('Low', 0)


# Función para calcular intervalos
def intervalos(var):
    n = len(var)
    x_max = var.max()
    x_min = var.min()
    recorrido = x_max - x_min
    intervalos = round(1 + (3.3 * (math.log10(n))))
    amplitud = (recorrido / intervalos)
    return x_min, x_max, amplitud


# Función para tabla de frecuencias no agrupados
def tablaFrecuencia(tabla, col, nomCol):
    tabla1 = pd.DataFrame(tabla)
    lista = []
    for reg in tabla:
        cont = 0
        for i in col:
            if reg == i:
                cont = cont + 1
        lista.append(cont)

    tabla2 = pd.DataFrame(lista)
    total = tabla2.sum()
    tabla3 = pd.concat([tabla1, tabla2], axis=1)
    tabla3.columns = [nomCol, 'frecAbs']

    def calcula(frecAbs):
        fRel = frecAbs / total
        return fRel

    tabla3['frecRel'] = tabla3['frecAbs'].apply(calcula)
    tabla3['frecAcum'] = tabla3['frecRel'].cumsum()

    return tabla3


# Función para tabla de frecuencias agrupados
def tabla_Hist(varCol, nomCol, var_min=None):
    # Paso1: Determinar el tamaño de la muestra
    n = len(varCol)

    # Paso2: Determinar el máximo y el mínimo
    x_max = varCol.max()
    x_min = varCol.min()

    # Paso3: Calcular el recorrido
    recorrido = x_max - x_min

    # Paso4: Calcular intervalos (clases)
    intervalos = round(1 + (3.3 * (math.log10(n))))

    # Paso5: Calcular la amplitud de cada intervalo
    amplitud = recorrido / intervalos

    # Paso6: Construir la tabla de frecuencias
    df_tf = pd.DataFrame()
    df_tf['Clase'] = list(range(1, intervalos + 1))
    df_tf['limInf'] = np.full(shape=intervalos, fill_value=np.nan)

    for i in range(intervalos):
        df_tf.loc[i, 'limInf'] = round(x_min + (i * amplitud), 3)

    df_tf['limSup'] = round(df_tf['limInf'] + amplitud, 3)
    df_tf['x'] = (df_tf['limSup'] + df_tf['limInf']) / 2
    df_tf['f'] = np.full(shape=intervalos, fill_value=np.nan)

    for i in range(intervalos):
        k = 0
        if i == 0:
            for j in range(n):
                if varCol.iloc[j] <= df_tf['limSup'].iloc[i]:
                    k = k + 1
            df_tf.loc[i, 'f'] = k
        else:
            for j in range(n):
                if (varCol.iloc[j] > df_tf['limInf'].iloc[i]) and (varCol.iloc[j] <= df_tf['limSup'].iloc[i]):
                    k = k + 1
            df_tf.loc[i, 'f'] = k

    df_tf['Fa'] = df_tf['f'].cumsum()
    df_tf['fr'] = round(df_tf['f'] / n, 4)
    df_tf['Fra'] = df_tf['fr'].cumsum()

    return df_tf


# Función para actualizar el layout de las gráficas
def actualiza_layout(grafica, x_title, y_title):
    grafica.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_pad_t=20,
        title_font_family='verdana',
        title_font_color='black',
        title_font_size=16,
        font_size=15,
        height=400
    )


# Gráfica de Scatter
def sct(varX, varY, co, cocs, x_titulo, y_titulo, tam, titulo, marg_x=None, marg_y=None, facetCol=None):
    grafica_sc = px.scatter(df, x=varX, y=varY, color=co, color_continuous_scale=cocs,
                            size=tam, marginal_x=marg_x, marginal_y=marg_y,
                            facet_col=facetCol, title=titulo)
    actualiza_layout(grafica_sc, x_titulo, y_titulo)
    return grafica_sc


# Gráfica de Histograma
def histograma(var, tit, subtit, col, cods, textoA, x_titulo, y_titulo, agrupados,
               x_min=0, x_max=0, amplitud=0, varY=None, pshape=None):
    if agrupados == True:
        grafica_hist = px.histogram(df, x=var, title=tit)
        grafica_hist.update_traces(marker_line_width=1,
                                   xbins=dict(start=x_min, end=x_max, size=amplitud))
    else:
        grafica_hist = px.histogram(df, x=var, y=varY, pattern_shape=pshape, title=tit,
                                    color=col, color_discrete_sequence=cods, text_auto=textoA)

    actualiza_layout(grafica_hist, x_titulo, y_titulo)
    return grafica_hist


# Gráfica de Histograma con función de densidad
def grafica_densidad(var, etiqueta, color):
    x_min, x_max, amplitudA = intervalos(var)
    amplitud = amplitudA
    graf_dens = ff.create_distplot([var], [etiqueta], show_hist=True, show_curve=True,
                                   curve_type='kde', show_rug=False, bin_size=amplitud,
                                   colors=[color])
    graf_dens.update_traces(marker_line_width=1)
    graf_dens.update_layout(
        title='Gráfica de densidad: ' + etiqueta,
        xaxis_title='Rango de ' + etiqueta,
        yaxis_title='Frecuencia - Densidad',
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_pad_t=20,
        title_font_family='verdana',
        title_font_color='black',
        title_font_size=16,
        font_size=15,
        height=400
    )
    return graf_dens


# Gráfica BoxPlot
def boxpltl(yvar, cds, titulo, x_titulo, y_titulo, col=None, xvar=None, puntos=None):
    grafica_box = px.box(df, x=xvar, y=yvar, points=puntos, color=col,
                         color_discrete_sequence=cds, title=titulo)
    actualiza_layout(grafica_box, x_titulo, y_titulo)
    return grafica_box


# Gráfica Sunburst
grafica_sunb = px.sunburst(df, path=['School_Type', 'Motivation_Level', 'Internet_Access'],
                           values='Hours_Studied', color='Exam_Score',
                           color_continuous_scale=px.colors.cyclical.IceFire)
grafica_sunb.update_traces(marker=dict(line=dict(color='purple', width=1)))
grafica_sunb.update_layout(
    title='Horas de estudio por tipo de escuela y nivel de motivación',
    font=dict(family='Courier New, monospace', size=14, color='purple'),
    paper_bgcolor='white',
    height=400
)

# Configuración de la página Streamlit
st.set_page_config(page_title='Tablero de Control Educativo', layout='wide', page_icon='📚')

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 5rem;
    padding-right: 5rem;
}
</style>
""", unsafe_allow_html=True)

# Título principal
st.title('Tablero de visualización de variables educativas')
st.text('Indicadores generales para el DataSet de Factores de Rendimiento Estudiantil')

# Mostrar métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric('Horas promedio (alta motivación)', f'{alta_motivacion_media:.2f}')
with col2:
    st.metric('Horas promedio (baja motivación)', f'{baja_motivacion_media:.2f}')
with col3:
    st.metric('Estudiantes alta motivación', alta_motivacion_count)
with col4:
    st.metric('Estudiantes baja motivación', baja_motivacion_count)

# Sección Logo de la empresa
st.sidebar.header('Institución Educativa')
# st.sidebar.image('Imagenes/imagenG.png')

# Selector de variables
st.sidebar.markdown('---')
st.sidebar.header('Análisis exploratorio de DataSet')
op = st.sidebar.radio('Selecciona:', ['Estadística', 'Visualizacion'])

if op == 'Visualizacion':
    st.sidebar.markdown('---')
    st.sidebar.header('Visualización exploratoria')
    opcion = st.sidebar.radio('Selecciona:', ['Una variable', 'Dos variables'])

    if opcion == 'Una variable':
        opcionUni = st.sidebar.selectbox('Selecciona una variable',
                                         ['Hours_Studied', 'Attendance', 'Motivation_Level', 'Previous_Scores',
                                          'Exam_Score'])
        col1, col2 = st.columns([0.98, 0.02])

        if opcionUni == 'Hours_Studied':
            with col1:
                var = 'Hours_Studied'
                tit = 'Distribución de horas de estudio'
                subtit = 'por estudiante'
                col = 'Hours_Studied'
                cods = ['Red']
                textoA = True
                x_titulo = 'Horas de estudio'
                y_titulo = 'Frecuencia'
                agrupados = False
                hist_horas = histograma(var, tit, subtit, col, cods, textoA,
                                        x_titulo, y_titulo, agrupados)
                st.plotly_chart(hist_horas, use_container_width=True)

        elif opcionUni == 'Attendance':
            with col1:
                col1_1, col1_2 = st.columns(2)
                with col1_1:
                    var = 'Attendance'
                    tit = 'Distribución de asistencia'
                    subtit = 'Porcentaje de asistencia'
                    col = 'Attendance'
                    cods = ['Red', 'Olive', 'Yellow']
                    textoA = True
                    x_titulo = 'Asistencia (%)'
                    y_titulo = 'Frecuencia'
                    agrupados = False
                    hist_asistencia = histograma(var, tit, subtit, col, cods, textoA,
                                                 x_titulo, y_titulo, agrupados)
                    st.plotly_chart(hist_asistencia, use_container_width=True)

                with col1_2:
                    st.plotly_chart(grafica_sunb, use_container_width=True)

        elif opcionUni == 'Motivation_Level':
            with col1:
                var = 'Motivation_Level'
                tit = 'Distribución de nivel de motivación'
                subtit = 'Nivel de motivación de estudiantes'
                col = 'Motivation_Level'
                cods = ['Magenta', 'Olive', 'Blue']
                textoA = True
                x_titulo = 'Nivel de motivación'
                y_titulo = 'Cantidad'
                agrupados = False
                hist_motivacion = histograma(var, tit, subtit, col, cods, textoA,
                                             x_titulo, y_titulo, agrupados)
                st.plotly_chart(hist_motivacion, use_container_width=True)

        elif opcionUni == 'Previous_Scores':
            with col1:
                col1_1, col1_2 = st.columns(2)
                col_prev_scores = df['Previous_Scores']
                with col1_1:
                    x_min, x_max, amplitudA = intervalos(col_prev_scores)
                    amplitud = '%0.2f' % amplitudA
                    var = 'Previous_Scores'
                    tit = 'Distribución de calificaciones previas'
                    subtit = 'Puntajes anteriores'
                    col = 'Previous_Scores'
                    cods = ['Olive']
                    textoA = True
                    x_titulo = 'Calificaciones previas'
                    y_titulo = 'Frecuencia'
                    agrupados = True
                    hist_prev_scores = histograma(var, tit, subtit, col, cods,
                                                  textoA, x_titulo, y_titulo,
                                                  agrupados, x_min, x_max, amplitud)
                    st.plotly_chart(hist_prev_scores, use_container_width=True)

                with col1_2:
                    etiq = 'Previous_Scores'
                    color = 'blue'
                    densidad_prev_scores = grafica_densidad(col_prev_scores, etiq, color)
                    st.plotly_chart(densidad_prev_scores, use_container_width=True)

        elif opcionUni == 'Exam_Score':
            with col1:
                col1_1, col1_2, col1_3 = st.columns(3)
                col_exam_score = df['Exam_Score']
                with col1_1:
                    x_min, x_max, amplitud = intervalos(col_exam_score)
                    amplitud = '%0.2f' % amplitud
                    var = 'Exam_Score'
                    tit = 'Distribución de puntajes de examen'
                    subtit = 'Puntajes finales'
                    col = 'Exam_Score'
                    cods = ['Olive']
                    textoA = True
                    x_titulo = 'Puntaje de examen'
                    y_titulo = 'Frecuencia'
                    agrupados = True
                    hist_exam = histograma(var, tit, subtit, col, cods,
                                           textoA, x_titulo, y_titulo,
                                           agrupados, x_min, x_max, amplitud)
                    st.plotly_chart(hist_exam, use_container_width=True)

                with col1_2:
                    etiq = 'Exam_Score'
                    color = 'red'
                    densidad_exam = grafica_densidad(col_exam_score, etiq, color)
                    st.plotly_chart(densidad_exam, use_container_width=True)

                with col1_3:
                    yvar = 'Exam_Score'
                    cds = ['Olive']
                    titulo = 'Puntajes de examen'
                    x_titulo = 'Variable puntaje'
                    y_titulo = 'Puntaje examen'
                    box_exam = boxpltl(yvar, cds, titulo, x_titulo, y_titulo)
                    st.plotly_chart(box_exam, use_container_width=True)




    elif opcion == 'Dos variables':

        opcionBi = st.sidebar.multiselect('Selecciona dos variables',

                                          ['Hours_Studied', 'Attendance', 'Exam_Score', 'Previous_Scores',
                                           'Motivation_Level', 'Sleep_Hours'])

        # Definir 5 combinaciones predefinidas

        lista1 = ['Hours_Studied', 'Exam_Score']

        lista2 = ['Attendance', 'Exam_Score']

        lista3 = ['Previous_Scores', 'Exam_Score']

        lista4 = ['Motivation_Level', 'Exam_Score']

        lista5 = ['Sleep_Hours', 'Exam_Score']

        if len(opcionBi) == 2:

            if set(opcionBi) == set(lista1):

                # COMBINACIÓN 1: Horas Estudio vs Puntaje Examen

                st.subheader("Análisis: Horas de Estudio vs Puntaje de Examen")

                col1, col2 = st.columns(2)

                with col1:

                    # Gráfica 1: Scatter básico

                    varX = df['Hours_Studied']

                    varY = df['Exam_Score']

                    col = 'Hours_Studied'

                    cocs = 'delta'

                    x_titulo = 'Horas de Estudio'

                    y_titulo = 'Puntaje de Examen'

                    tamano = 'Hours_Studied'

                    titulo = 'Relación Horas Estudio - Puntaje Examen'

                    sct_1 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_1, use_container_width=True)

                with col2:

                    # Gráfica 2: Scatter por motivación

                    col = 'Motivation_Level'

                    cocs = 'viridis'

                    titulo = 'Horas-Puntaje por Motivación'

                    sct_2 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_2, use_container_width=True)

                col3, col4 = st.columns(2)

                with col3:

                    # Gráfica 3: Scatter con marginales

                    marg_x = 'histogram'

                    marg_y = 'box'

                    titulo = 'Horas-Puntaje con Distribuciones'

                    sct_3 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo, marg_x, marg_y)

                    st.plotly_chart(sct_3, use_container_width=True)

                with col4:

                    # Gráfica 4: Boxplot

                    yvar = 'Exam_Score'

                    cds = ['red', 'blue', 'green']

                    titulo = 'Puntaje por Motivación'

                    x_titulo = 'Nivel de Motivación'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'Motivation_Level'

                    xvar = 'Motivation_Level'

                    box_1 = boxpltl(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar)

                    st.plotly_chart(box_1, use_container_width=True)


            elif set(opcionBi) == set(lista2):

                # COMBINACIÓN 2: Asistencia vs Puntaje Examen

                st.subheader("Análisis: Asistencia vs Puntaje de Examen")

                col1, col2 = st.columns(2)

                with col1:

                    varX = df['Attendance']

                    varY = df['Exam_Score']

                    col = 'Attendance'

                    cocs = 'plasma'

                    x_titulo = 'Asistencia (%)'

                    y_titulo = 'Puntaje de Examen'

                    tamano = 'Attendance'

                    titulo = 'Relación Asistencia - Puntaje Examen'

                    sct_1 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_1, use_container_width=True)

                with col2:

                    col = 'School_Type'

                    cocs = 'thermal'

                    titulo = 'Asistencia-Puntaje por Tipo Escuela'

                    sct_2 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_2, use_container_width=True)

                col3, col4 = st.columns(2)

                with col3:

                    marg_x = 'histogram'

                    marg_y = 'violin'

                    titulo = 'Asistencia-Puntaje con Distribuciones'

                    sct_3 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo, marg_x, marg_y)

                    st.plotly_chart(sct_3, use_container_width=True)

                with col4:

                    yvar = 'Exam_Score'

                    cds = ['orange', 'purple']

                    titulo = 'Puntaje por Tipo de Escuela'

                    x_titulo = 'Tipo de Escuela'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'School_Type'

                    xvar = 'School_Type'

                    box_1 = boxpltl(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar)

                    st.plotly_chart(box_1, use_container_width=True)


            elif set(opcionBi) == set(lista3):

                # COMBINACIÓN 3: Calificaciones Previas vs Puntaje Examen

                st.subheader("Análisis: Calificaciones Previas vs Puntaje de Examen")

                col1, col2 = st.columns(2)

                with col1:

                    varX = df['Previous_Scores']

                    varY = df['Exam_Score']

                    col = 'Previous_Scores'

                    cocs = 'electric'

                    x_titulo = 'Calificaciones Previas'

                    y_titulo = 'Puntaje de Examen'

                    tamano = 'Previous_Scores'

                    titulo = 'Relación Calificaciones Previas - Puntaje Examen'

                    sct_1 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_1, use_container_width=True)

                with col2:

                    col = 'Teacher_Quality'

                    cocs = 'rainbow'

                    titulo = 'Calificaciones-Puntaje por Calidad Docente'

                    sct_2 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_2, use_container_width=True)

                col3, col4 = st.columns(2)

                with col3:

                    marg_x = 'histogram'

                    marg_y = 'box'

                    titulo = 'Calificaciones-Puntaje con Distribuciones'

                    sct_3 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo, marg_x, marg_y)

                    st.plotly_chart(sct_3, use_container_width=True)

                with col4:

                    yvar = 'Exam_Score'

                    cds = ['red', 'blue', 'yellow', 'green']

                    titulo = 'Puntaje por Calidad Docente'

                    x_titulo = 'Calidad del Profesor'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'Teacher_Quality'

                    xvar = 'Teacher_Quality'

                    box_1 = boxpltl(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar)

                    st.plotly_chart(box_1, use_container_width=True)


            elif set(opcionBi) == set(lista4):

                # COMBINACIÓN 4: Motivación vs Puntaje Examen

                st.subheader("Análisis: Nivel de Motivación vs Puntaje de Examen")

                col1, col2 = st.columns(2)

                with col1:

                    # Para variables categóricas como Motivation_Level, usamos boxplot

                    yvar = 'Exam_Score'

                    cds = ['red', 'blue', 'green']

                    titulo = 'Puntaje por Nivel de Motivación'

                    x_titulo = 'Nivel de Motivación'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'Motivation_Level'

                    xvar = 'Motivation_Level'

                    box_1 = boxpltl(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar)

                    st.plotly_chart(box_1, use_container_width=True)

                with col2:

                    # Violin plot para distribución

                    yvar = 'Exam_Score'

                    cds = ['red', 'blue', 'green']

                    titulo = 'Distribución de Puntajes por Motivación'

                    x_titulo = 'Nivel de Motivación'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'Motivation_Level'

                    xvar = 'Motivation_Level'

                    puntos = 'all'  # Mostrar todos los puntos

                    box_2 = boxpltl(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar, puntos)

                    st.plotly_chart(box_2, use_container_width=True)

                col3, col4 = st.columns(2)

                with col3:

                    # Scatter de horas vs puntaje coloreado por motivación

                    varX = df['Hours_Studied']

                    varY = df['Exam_Score']

                    col = 'Motivation_Level'

                    cocs = 'viridis'

                    x_titulo = 'Horas de Estudio'

                    y_titulo = 'Puntaje de Examen'

                    tamano = 'Hours_Studied'

                    titulo = 'Horas-Puntaje por Motivación'

                    sct_1 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_1, use_container_width=True)

                with col4:

                    # Histograma de puntajes por motivación

                    var = 'Exam_Score'

                    tit = 'Distribución de Puntajes por Motivación'

                    subtit = 'Comparación por nivel de motivación'

                    col_hist = 'Motivation_Level'

                    cods = ['red', 'blue', 'green']

                    textoA = True

                    x_titulo = 'Puntaje de Examen'

                    y_titulo = 'Frecuencia'

                    agrupados = False

                    hist_1 = histograma(var, tit, subtit, col_hist, cods, textoA, x_titulo, y_titulo, agrupados)

                    st.plotly_chart(hist_1, use_container_width=True)


            elif set(opcionBi) == set(lista5):

                # COMBINACIÓN 5: Horas Sueño vs Puntaje Examen

                st.subheader("Análisis: Horas de Sueño vs Puntaje de Examen")

                col1, col2 = st.columns(2)

                with col1:

                    varX = df['Sleep_Hours']

                    varY = df['Exam_Score']

                    col = 'Sleep_Hours'

                    cocs = 'blues'

                    x_titulo = 'Horas de Sueño'

                    y_titulo = 'Puntaje de Examen'

                    tamano = 'Sleep_Hours'

                    titulo = 'Relación Horas Sueño - Puntaje Examen'

                    sct_1 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_1, use_container_width=True)

                with col2:

                    col = 'Physical_Activity'

                    cocs = 'greens'

                    titulo = 'Sueño-Puntaje por Actividad Física'

                    sct_2 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_2, use_container_width=True)

                col3, col4 = st.columns(2)

                with col3:

                    marg_x = 'histogram'

                    marg_y = 'violin'

                    titulo = 'Sueño-Puntaje con Distribuciones'

                    sct_3 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo, marg_x, marg_y)

                    st.plotly_chart(sct_3, use_container_width=True)

                with col4:

                    yvar = 'Exam_Score'

                    cds = ['orange', 'purple', 'brown']

                    titulo = 'Puntaje por Actividad Física'

                    x_titulo = 'Actividad Física'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'Physical_Activity'

                    xvar = 'Physical_Activity'

                    box_1 = boxpltl(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar)

                    st.plotly_chart(box_1, use_container_width=True)


            else:

                st.warning("Selecciona una de las combinaciones predefinidas para ver el análisis completo.")

                st.info(
                    "Combinaciones disponibles: Horas Estudio-Examen, Asistencia-Examen, Calificaciones Previas-Examen, Motivación-Examen, Sueño-Examen")


        elif len(opcionBi) > 2:

            st.warning("Por favor selecciona solo 2 variables para el análisis bivariado.")

        else:

            st.info("Selecciona 2 variables para comenzar el análisis.")

elif op == 'Estadística':
    # Segunda sección de interacción
    st.sidebar.markdown('---')
    st.sidebar.header('Análisis exploratorio')
    opcion_explora = st.sidebar.selectbox('Selecciona:',
                                          ['Visualizar DataFrame', 'Descripcion por Variable',
                                           'Cuartiles', 'T Frecuencias No Agrupados',
                                           'T Frecuencias Agrupados', 'Medidas Centrales',
                                           'Medidas de Dispersion']
                                          )

    if opcion_explora == 'Visualizar DataFrame':
        with st.expander('Data Set: Factores de Rendimiento Estudiantil', expanded=False):
            st.markdown('''
            El Data Set contiene información sobre factores que afectan el rendimiento estudiantil:
            * **Hours_Studied**: Horas de estudio semanales
            * **Attendance**: Porcentaje de asistencia
            * **Parental_Involvement**: Nivel de involucramiento parental
            * **Access_to_Resources**: Acceso a recursos educativos
            * **Extracurricular_Activities**: Participación en actividades extracurriculares
            * **Sleep_Hours**: Horas de sueño por noche
            * **Previous_Scores**: Calificaciones anteriores
            * **Motivation_Level**: Nivel de motivación del estudiante
            * **Internet_Access**: Acceso a internet
            * **Tutoring_Sessions**: Sesiones de tutoría
            * **Family_Income**: Nivel de ingreso familiar
            * **Teacher_Quality**: Calidad del profesorado
            * **School_Type**: Tipo de escuela (Pública/Privada)
            * **Peer_Influence**: Influencia de compañeros
            * **Physical_Activity**: Actividad física
            * **Learning_Disabilities**: Presencia de discapacidades de aprendizaje
            * **Parental_Education_Level**: Nivel educativo de los padres
            * **Distance_from_Home**: Distancia desde casa a la escuela
            * **Gender**: Género del estudiante
            * **Exam_Score**: Puntaje del examen final
            ''')

        st.dataframe(df, use_container_width=True)
        col1, col2, col3 = st.columns(3, border=True)
        with col1:
            st.text('Tipos de datos')
            tipos_df = df.dtypes
            st.write(tipos_df)
        with col2:
            info = io.StringIO()
            df.info(buf=info)
            info_df = info.getvalue()
            st.text('Información general')
            st.text(info_df)
        with col3:
            st.text('Describe df')
            describ = df.describe()
            st.write(describ)

    elif opcion_explora == 'Descripcion por Variable':
        col1, col2, col3 = st.columns([0.3, 0.2, 0.5], border=False)
        with col1:
            var_col = list(df.columns)
            opcion_col = st.selectbox('Selecciona la variable (describe()): ', var_col)

        with col2:
            describe_col = df[opcion_col].describe()
            st.write(describe_col)

    elif opcion_explora == 'Cuartiles':
        col1, col2, col3 = st.columns([0.3, 0.2, 0.5], border=False)
        with col1:
            opcion_col = st.selectbox('Selecciona la variable (cuartiles): ',
                                      ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Exam_Score'])

        with col2:
            cuartiles = df[opcion_col].quantile([0.25, 0.50, 0.75])
            st.write(cuartiles)

    elif opcion_explora == 'T Frecuencias No Agrupados':
        col1, col2, col3 = st.columns([0.2, 0.6, 0.2], border=False)
        with col1:
            opcion_col = st.selectbox('Selecciona la variable (Tabla Frecuencias): ',
                                      ['School_Type', 'Internet_Access', 'Motivation_Level', 'Gender'])

        with col2:
            tablaF = sorted(df[opcion_col].unique())
            colF = df[opcion_col]
            nomColF = opcion_col
            t_f = tablaFrecuencia(tablaF, colF, nomColF)
            st.write(t_f)

    elif opcion_explora == 'T Frecuencias Agrupados':
        col1, col2, col3 = st.columns([0.2, 0.6, 0.2], border=False)
        with col1:
            opcion_col = st.selectbox('Selecciona la variable (Tabla Frecuencias): ',
                                      ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Exam_Score'])

        with col2:
            nomCol = opcion_col
            var_col = df[opcion_col]
            t_fA = tabla_Hist(var_col, nomCol)
            st.write(t_fA)

    elif opcion_explora == 'Medidas Centrales':
        col1, col2, col3, col4 = st.columns(4, border=False)
        with col1:
            opcion_col = st.selectbox('Selecciona la variable (Medidas Centrales): ',
                                      ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Exam_Score'])

        with col2:
            media_v = df[opcion_col].mean()
            st.metric('Media', '%0.2f' % media_v)
        with col3:
            mediana_v = df[opcion_col].median()
            st.metric('Mediana', '%0.2f' % mediana_v)
        with col4:
            moda_v = df[opcion_col].mode().iloc[0] if not df[opcion_col].mode().empty else 0
            st.metric('Moda', '%0.2f' % moda_v)

    elif opcion_explora == 'Medidas de Dispersion':
        col1, col2, col3, col4, col5, col6 = st.columns(6, border=False)
        with col1:
            opcion_col = st.selectbox('Selecciona la variable (Medidas Dispersión): ',
                                      ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Exam_Score'])

        with col2:
            rango_v = df[opcion_col].max() - df[opcion_col].min()
            st.metric('Rango', '%0.2f' % rango_v)
        with col3:
            varianza_v = df[opcion_col].var()
            st.metric('Varianza', '%0.2f' % varianza_v)
        with col4:
            std_v = df[opcion_col].std()
            st.metric('Desviación estándar', '%0.2f' % std_v)
        with col5:
            asimetria_v = df[opcion_col].skew()
            st.metric('Asimetría', '%0.3f' % asimetria_v)
        with col6:
            curtosis_v = df[opcion_col].kurt()
            st.metric('Curtosis', '%0.3f' % curtosis_v)

st.sidebar.markdown('---')
st.sidebar.header('Acerca de')
st.sidebar.info('Dashboard diseñado con fines académicos para análisis de factores educativos')