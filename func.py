import math
import pandas as pd


def intervalos(var):
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
