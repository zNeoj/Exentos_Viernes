import plotly.express as px
from func import actualiza_layout
from data import df


# Gráfica de Scatter:
def sct(varX, varY, co, cocs, x_titulo, y_titulo, tam, titulo,
        marg_x=None, marg_y=None, facetCol=None):

    grafica_sc = px.scatter(df, x=varX, y=varY,
                            color=co,
                            color_continuous_scale=cocs,
                            size=tam,
                            marginal_x=marg_x,
                            marginal_y=marg_y,
                            facet_col=facetCol,
                            title=titulo
                            )

    actualiza_layout(grafica_sc, x_titulo, y_titulo)

    return grafica_sc
