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
#st.sidebar.image('Imagenes/imagenIco.ico') # luego le ponemos un png pq me truena
st.sidebar.markdown('---')
st.sidebar.header('Análisis exploratorio de DataSet')
op = st.sidebar.radio('Selecciona: ', ['Estadisitca', 'Visualización'])

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
                    yvar = 'Asistencia'
                    cds = ['Olive']
                    titulo = 'Porcentaje de asistencia'
                    x_titulo = ('Variable asistencia')
                    y_titulo = 'Porcentaje asistencia'
                    box_asistencia = func.boxplt1(yvar, cds, titulo, x_titulo, y_titulo)

                    st.plotly_chart(box_asistencia, use_container_width = True)




        elif opcionUni == 'Tipo de Escuela':
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
        opcionBi = st.sidebar.multiselect('Selecciona dos variables', ['Puntaje de examen', 'Horas estudiadas', 'Horas de sueño'])

        lista1 = ['Puntaje de examen', 'Horas estudiadas']
        lista2 = ['Horas estudiadas', 'Horas de sueño']
        if set(opcionBi) == set(lista1):
            varX = df['Exam_Score']
            varY = df['Hours_Studied']
            col1, col2 = st.columns(2)
            with col1:
                col = 'Exam_Score'
                cocs = 'delta'
                x_title = 'Puntaje de examen'
                y_title = 'Horas estudiadas'
                tamano = 'Exam_Score'
                titulo = 'Puntaje de examen - Horas estudiadas'
                sct_EC_1 = graficas.sct(varX, varY, col, cocs, x_title, y_title, tamano, titulo)

                st.plotly_chart(graficas.sct_EC_1, use_container_width = True)