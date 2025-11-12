import streamlit as st
import pandas as pd
import numpy as np
import io
import math
import plotly.express as px
import func
import graficas
from data import df
from graficas import sct

aprobados = df[df['Exam_Score'] >= 70]
aprobados_media = aprobados['Hours_Studied'].mean()

reprobados = df[df['Exam_Score'] < 70]
reprobados_media = reprobados['Hours_Studied'].mean()

estudiantes = df['Exam_Score'].value_counts()

general_aprobados = (df['Exam_Score'] >= 70).value_counts()
no_aprobo = general_aprobados[0]
si_aprobo = general_aprobados[1]


grafica_sunb = px.sunburst(df, path = ['School_Type', 'Motivation_Level'],
                           values = 'Hours_Studied', color = 'Hours_Studied',
                           color_continuous_scale = px.colors.cyclical.IceFire)

grafica_sunb.update_traces(marker = dict(line = dict(color = 'purple', width = 1)))
grafica_sunb.update_layout(
    title = 'Horas de estudio de los estudiantes por tipo de escuela',
    font = dict(family = 'Courier New, monospace',
                size = 14,
                color = 'purple'),
    paper_bgcolor = 'white', #'hsl(50, 20%, 50%)',
    height = 400
    )

st.set_page_config(page_title = 'EPtablero de EPcontrol',
                   layout = 'wide', page_icon = 'Imagenes/imagenIco.ico')

st.markdown(
    """
        <style>
            .block-container{
                padding-top:1rem;
                padding-bottom:0rem;
                padding-left:5rem;
                padding-right:5rem;
                }
        </style>
        """, unsafe_allow_html=True
    )

st.title('EPtablero de EPvisualizacion de EPvariables')
st.text('Indicadores generales para el Dataset Estudiantes')

# Metricas generales
colm1, colm2, colm3, colm4 = st.columns(4, vertical_alignment="center",
                                        border = True)

with colm1:
    aprobados_mediana = df['Hours_Studied'].median()
    st.metric('Horas de estudio promedio para aprobados',
              '%0.2f' %aprobados_media,
              delta = f'{aprobados_mediana} mediana',
              delta_color = 'inverse')

with colm2:
    reprobados_mediana = df['Hours_Studied'].median()
    st.metric('Horas de estudio promedio para reprobados',
              '%0.2f' %reprobados_media,
              delta = f'{reprobados_mediana} mediana')

with colm3:
    porcentajeSi = ('%0.0f' % ((si_aprobo / (si_aprobo + no_aprobo))* 100))
    st.metric('Numero de aprobados',
              si_aprobo,
              delta = f'{porcentajeSi} %',
              delta_color = 'inverse')

with colm4:
    porcentajeNo = ('%0.0f' % ((no_aprobo / (si_aprobo + no_aprobo))* 100))
    st.metric('Numero de reprobados',
              no_aprobo,
              delta = f'{porcentajeNo} %')

st.markdown('---')


# SIDEBAR
st.sidebar.header('Logo empresa')
st.sidebar.image('Imagenes/Logo.png') # luego le ponemos un png pq me truena
st.sidebar.markdown('---')
st.sidebar.header('Análisis exploratorio de DataSet')
op = st.sidebar.radio('Selecciona: ', ['Estadistica', 'Visualización'])

if op == 'Visualización':
    st.sidebar.markdown('---')

    st.sidebar.header('Visualización exploratoria')
    opcion = st.sidebar.radio('Selecciona:', ['Una variable', 'Dos variables'])

    if opcion == 'Una variable':
        opcionUni = st.sidebar.selectbox('Selecciona una variable', ['Horas estudiadas', 'Horas de sueño','Puntaje de examen', 'Asistencia', 'Acceso a Internet'])

        col1, col2 = st.columns([0.98, 0.02])
        if opcionUni == 'Horas estudiadas':
            with col1:
                var = 'Hours_Studied'
                tit = 'Frecuencia de horas estudiadas'
                subtit = 'por estudiante'
                col = 'Hours_Studied'
                cods = [['Red'], ['Olive'], ['Yellow'], ['Purple'], ['Blue'], ['Green']]
                textoA = True
                x_titulo = 'Número de horas'
                y_titulo = 'Frecuencia'
                agrupados = False
                hist_horas = func.histograma(var, tit, subtit, col, cods, textoA, x_titulo, y_titulo, agrupados)

                st.plotly_chart(hist_horas, use_container_width = True)

        elif opcionUni == 'Horas de sueño':
            with col1:
                col1_1, col1_2 = st.columns(2)
            with col1_1:
                var = 'Sleep_Hours'
                tit = 'Frecuencia de horas de sueño'
                subtit = 'Horas por estudiante'
                col = 'Sleep_Hours'
                cods = [['Red'], ['Olive'], ['Yellow'], ['Purple'], ['Blue'], ['Green']]
                textoA = True
                x_titulo = 'Número de horas'
                y_titulo = 'Frecuencia'
                agrupados = False
                hist_horasSleep = func.histograma(var, tit, subtit, col, cods, textoA,
                                  x_titulo, y_titulo, agrupados)
                st.plotly_chart(hist_horasSleep, use_container_width = True)
            with col1_2:
                st.plotly_chart(grafica_sunb, use_container_width = True)


        elif opcionUni == 'Puntaje de examen':
            with col1:
                col1_1, col1_2 = st.columns(2)
                col_examen = df['Exam_Score']
                with col1_1:
                    x_min, x_max, amplitudA = func.get_intervalos(col_examen)
                    amplitud = '%0.2f' %amplitudA
                    var = 'Exam_Score'
                    tit = 'Frecuencia de variable Puntaje de Examen'
                    subtit = 'Puntaje de examen'
                    col = 'Exam_Score'
                    cods = ['Olive']
                    textoA = True
                    x_titulo = 'Rango de Puntaje de Examen'
                    y_titulo = 'Frecuencia'
                    agrupados = False
                    hist_examen = func.histograma(var, tit, subtit, col, cods, textoA, x_titulo, y_titulo, agrupados, x_min, x_max, amplitud)

                    st.plotly_chart(hist_examen, use_container_width = True)

                with col1_2:
                    etiq = 'Puntaje de examen'
                    color = 'red'
                    densidad_examen = func.grafica_densidad(col_examen, etiq, color)
                    st.plotly_chart(densidad_examen, use_container_width = True)



        elif opcionUni == 'Asistencia':
            with col1:
                col1_1, col1_2, col1_3 = st.columns(3)
                col_asistencia = df['Attendance']
                with col1_1:
                    x_min, x_max, amplitudA = func.get_intervalos(col_asistencia)
                    amplitud = '%0.2f' %amplitudA
                    var = 'Attendance'
                    tit = 'Frecuencia de variable Asistencia'
                    subtit = 'Asistencia'
                    col = 'Attendance'
                    cods = ['Olive']
                    textoA = True
                    x_titulo = 'Rango de porcentaje de asistencia'
                    y_titulo = 'Frecuencia'
                    agrupados = True
                    hist_asistencia = func.histograma(var, tit, subtit, col, cods, textoA, x_titulo, y_titulo, agrupados, x_min, x_max, amplitud)

                    st.plotly_chart(hist_asistencia, use_container_width = True)

                with col1_2:
                    etiq = 'Asistencia'
                    color = 'red'
                    densidad_asistencia = func.grafica_densidad(col_asistencia, etiq, color)
                    st.plotly_chart(densidad_asistencia, use_container_width = True)

                with col1_3:
                    yvar = 'Attendance'
                    cds = ['Olive']
                    titulo = 'Porcentaje de asistencia'
                    x_titulo = ('Variable asistencia')
                    y_titulo = 'Porcentaje asistencia'
                    box_asistencia = func.boxplt1(yvar, cds, titulo, x_titulo, y_titulo)

                    st.plotly_chart(box_asistencia, use_container_width = True)




        elif opcionUni == 'Acceso a Internet':
            with col1:
                col1_1, col1_2 = st.columns(2)
                with col1_1:
                    var = 'Internet_Access'
                    tit = 'Frecuencia de alumnos con Acceso a Internet'
                    subtit = 'Clasificado por alumno con y sin Acceso a Internet'
                    col= 'Internet_Access'
                    cods = [['Magenta'],['Olive']]
                    textoA = True
                    x_titulo = "Acceso a Internet"
                    y_titulo = 'Cantidad'
                    agrupados = False
                    hist_acceso_internet = func.histograma(var, tit, subtit, col, cods, textoA, x_titulo, y_titulo, agrupados)
                    st.plotly_chart(hist_acceso_internet, use_container_width = True)
                with col1_2:
                    var = 'Internet_Access'
                    tit = 'Frecuencia de alumnos con Acceso a Internet'
                    subtit = 'Clasificado por fumador y no fumador por Tipo de Escuela'
                    col = 'School_Type'
                    cods = ['Magenta', 'Magenta'],['Olive', 'Olive']
                    textoA = True
                    x_titulo = 'Acceso a Internet'
                    y_titulo = 'Cantidad'
                    agrupados = False
                    hist_acceso_internet2 = func.histograma(var, tit, subtit, col, cods, textoA, x_titulo, y_titulo,
                                                           agrupados)
                    st.plotly_chart(hist_acceso_internet2, use_container_width=True)



    elif opcion == 'Dos variables':

        opcionBi = st.sidebar.multiselect('Selecciona dos variables',

                                          ['Hours_Studied', 'Attendance', 'Exam_Score', 'Previous_Scores'])

        # Definir 3 combinaciones predefinidas

        lista1 = ['Hours_Studied', 'Exam_Score']

        lista2 = ['Attendance', 'Exam_Score']

        lista3 = ['Previous_Scores', 'Exam_Score']

        if len(opcionBi) == 2:

            if set(opcionBi) == set(lista1):

                # COMBINACIÓN 1: Horas Estudio vs Puntaje Examen - 4 GRÁFICAS

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

                    # Gráfica 2: Scatter por género

                    col = 'Gender'

                    cocs = 'viridis'

                    titulo = 'Horas-Puntaje por Género'

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

                    # Gráfica 4: Boxplot por motivación

                    yvar = 'Exam_Score'

                    cds = ['red', 'blue', 'green']

                    titulo = 'Puntaje por Nivel de Motivación'

                    x_titulo = 'Nivel de Motivación'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'Motivation_Level'

                    xvar = 'Motivation_Level'

                    box_1 = func.boxplt1(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar)

                    st.plotly_chart(box_1, use_container_width=True)


            elif set(opcionBi) == set(lista2):

                # COMBINACIÓN 2: Asistencia vs Puntaje Examen - 4 GRÁFICAS DIFERENTES

                st.subheader("Análisis: Asistencia vs Puntaje de Examen")

                col1, col2 = st.columns(2)

                with col1:

                    # Gráfica 5: Scatter por tipo de escuela

                    varX = df['Attendance']

                    varY = df['Exam_Score']

                    col = 'School_Type'

                    cocs = 'plasma'

                    x_titulo = 'Asistencia (%)'

                    y_titulo = 'Puntaje de Examen'

                    tamano = 'Attendance'

                    titulo = 'Asistencia-Puntaje por Tipo de Escuela'

                    sct_1 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_1, use_container_width=True)

                with col2:

                    # Gráfica 6: Scatter con faceta por internet

                    col = 'Internet_Access'

                    cocs = 'thermal'

                    titulo = 'Asistencia-Puntaje por Acceso a Internet'

                    facetCol = 'Internet_Access'

                    sct_2 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo, facetCol=facetCol)

                    st.plotly_chart(sct_2, use_container_width=True)

                col3, col4 = st.columns(2)

                with col3:

                    # Gráfica 7: Scatter con violin marginal

                    marg_x = 'histogram'

                    marg_y = 'violin'

                    titulo = 'Asistencia-Puntaje con Violines'

                    sct_3 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo, marg_x, marg_y)

                    st.plotly_chart(sct_3, use_container_width=True)

                with col4:

                    # Gráfica 8: Histograma comparativo

                    var = 'Exam_Score'

                    tit = 'Distribución de Puntajes por Asistencia'

                    subtit = 'Comparación de rendimiento'

                    col_hist = 'Attendance'

                    cods = ['red', 'orange', 'yellow']

                    textoA = True

                    x_titulo = 'Puntaje de Examen'

                    y_titulo = 'Frecuencia'

                    agrupados = False

                    hist_1 = func.histograma(var, tit, subtit, col_hist, cods, textoA, x_titulo, y_titulo, agrupados)

                    st.plotly_chart(hist_1, use_container_width=True)


            elif set(opcionBi) == set(lista3):

                # COMBINACIÓN 3: Calificaciones Previas vs Puntaje Examen - 3 GRÁFICAS DIFERENTES

                st.subheader("Análisis: Calificaciones Previas vs Puntaje de Examen")

                col1, col2 = st.columns(2)

                with col1:

                    # Gráfica 9: Scatter por calidad docente

                    varX = df['Previous_Scores']

                    varY = df['Exam_Score']

                    col = 'Teacher_Quality'

                    cocs = 'rainbow'

                    x_titulo = 'Calificaciones Previas'

                    y_titulo = 'Puntaje de Examen'

                    tamano = 'Previous_Scores'

                    titulo = 'Calificaciones-Puntaje por Calidad Docente'

                    sct_1 = sct(varX, varY, col, cocs, x_titulo, y_titulo, tamano, titulo)

                    st.plotly_chart(sct_1, use_container_width=True)

                with col2:

                    # Gráfica 10: Boxplot con puntos outliers

                    yvar = 'Exam_Score'

                    cds = ['purple', 'blue', 'cyan', 'green']

                    titulo = 'Puntaje por Calidad Docente (outliers)'

                    x_titulo = 'Calidad del Profesor'

                    y_titulo = 'Puntaje Examen'

                    col_box = 'Teacher_Quality'

                    xvar = 'Teacher_Quality'

                    puntos = 'outliers'

                    box_1 = func.boxplt1(yvar, cds, titulo, x_titulo, y_titulo, col_box, xvar, puntos)

                    st.plotly_chart(box_1, use_container_width=True)

                # Gráfica 11: Densidad para calificaciones previas

                col3, col4 = st.columns(2)

                with col3:

                    col_prev_scores = df['Previous_Scores']

                    etiq = 'Calificaciones_Previas'

                    color = 'blue'

                    densidad_prev = func.grafica_densidad(col_prev_scores, etiq, color)

                    st.plotly_chart(densidad_prev, use_container_width=True)


            else:

                st.warning("Selecciona una de las combinaciones predefinidas para ver el análisis completo.")

                st.info(
                    "Combinaciones disponibles: Horas Estudio-Examen, Asistencia-Examen, Calificaciones Previas-Examen")


        elif len(opcionBi) > 2:

            st.warning("Por favor selecciona solo 2 variables para el análisis bivariado.")

        else:

            st.info("Selecciona 2 variables para comenzar el análisis.")


elif op == 'Estadistica':
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
            t_f = func.tablaFrecuencia(tablaF, colF, nomColF)
            st.write(t_f)

    elif opcion_explora == 'T Frecuencias Agrupados':
        col1, col2, col3 = st.columns([0.2, 0.6, 0.2], border=False)
        with col1:
            opcion_col = st.selectbox('Selecciona la variable (Tabla Frecuencias): ',
                                      ['Hours_Studied', 'Attendance', 'Previous_Scores', 'Exam_Score'])

        with col2:
            nomCol = opcion_col
            var_col = df[opcion_col]
            t_fA = func.tabla_Hist(var_col, nomCol)
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
st.sidebar.info('Dashboard diseñado con fines académicos para la materia Lenguajes y Autómatas y Sistemas Programables con la profesora Verónica Quintero Rosas')