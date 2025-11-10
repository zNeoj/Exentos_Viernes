import math
import pandas as pd
from data import df

# Variable global para usar en tabla_Hist
intervalos = None


def intervalos(var):
    global intervalos
    """
    Calcula los intervalos óptimos para un histograma usando la regla de Sturges.

    Args:
        var: Array o lista de valores numéricos

    Returns:
        tuple: (x_min, x_max, amplitud) - valores mínimo, máximo y amplitud de intervalos
    """
    n = len(var)
    x_max = var.max()
    x_min = var.min()
    recorrido = x_max - x_min
    intervalos = round(1 + (3.3 * (math.log10(n))))
    amplitud = (recorrido / intervalos)

    return x_min, x_max, amplitud


def tablaFrecuencia(tabla, col, nomCol):
    """
    Calcula una tabla de frecuencias con frecuencias absolutas, relativas y acumuladas.

    Args:
        tabla: DataFrame de pandas
        col: Columna sobre la cual calcular las frecuencias
        nomCol: Nombre para la columna de frecuencias absolutas

    Returns:
        DataFrame: Tabla con frecuencias absolutas, relativas y acumuladas
    """
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
def tabla_Hist(varCol, nomCol):
    global intervalos
    # Paso1: Determinar el tamaño de la muestra
    print('Variable: ' + nomCol, '\n')
    n = len(varCol)
    print('Paso1: Tamaño de la muestra: ', n, '\n')

    # Paso2: Determinar el máximo y el mínimo
    x_max = varCol.max()
    x_min = varCol.min()
    print('Paso2: Máximo y mínimo: ')
    print('Máximo: ', x_max)
    print('Mínimo: ', x_min, '\n')

    # Paso3: Calcular el recorrido
    recorrido = x_max - x_min
    print('Paso3: Recorrido: ', recorrido, '\n')

    # Paso4: Calcular intervalos (clases)
    # Fórmula de Sturges (1 + 3.3 log n)
    intervalos = round(1 + (3.3 * (math.log10(n))))
    print('Paso4: Intervalos: ', intervalos, '\n')

    # Paso5: Calcular la amplitud de cada intervalo
    amplitud = recorrido / intervalos
    print('Paso5: Amplitud: ', '%0.2f' % amplitud, '\n')


# Función para actualizar el layout de las graficas
def actualiza_layout(grafica, x_title, y_title):
    grafica.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_pad_l=20,
        title_font_family='verdana',
        title_font_color='black',
        title_font_size=16,
        font_size=13,
        height=400
    )
