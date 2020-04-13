# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 07:20:19 2020

@author: Estavillo
"""

# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - layout general del proyecto
# -- mantiene: Juan Pablo Estavillo
# -- repositorio: https://github.com/
# -- ------------------------------------------------------------------------------------ -- #
import plotly.offline as py       # hasta arriba                                                  # en el mismo renglon
import funciones as fn           #aqui están todas las funciones 
import pandas as pd              #pandas  aunque no se use 
import plotly.graph_objects as go  #para graficar
#%%
#leer archivo 
data=fn.f_leer_archivo('trade3.xlsx')

#agregar columna de tiempo 
data=fn.f_columnas_tiempos(data)

#agregar columna de pip
data = fn.f_columnas_pips(data)

#diccionario con estadísticas de operaciones 
estadistica_operaciones = fn.f_estadisticas_ba(data)

#crear dataframe con los profits de cada dia 
profit_d = fn.f_profit_diario(data)

#aqui se hacen las medidas de atribucion al riesgo 
Medidas_atribucion_riesgo = fn.f_stats_mad(data)
#%%
#parte 4 
sesgos=fn.f_be_de(data)
#%%
#parte 5       (esta grafica solo tiene el usdjpy mayor a 0 ya que fue con el unico par que llego a take profit )
#Gráfica 1: Ranking
#tomamos el dataframe 
grafica1=estadistica_operaciones['df_2_ranking']
#las unicas operaciones que tuve en ganadas fueron en usdjpy por lo que la grafica quedara muy mal
#etiquetas 
labels = grafica1.index
#valores para pie chart 
valores=grafica1.reset_index()['rank'].values
values = valores

# pull is given as a fraction of the pie radius
fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[.2, 0, 0, 0,0,0,0])])
fig.update_layout(title_text="ranking of currency")
fig.show()


#Gráfica 2: DrawDown y DrawUp
#crear grafica 
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data['operations'],
    y=data.capital_acm,
    mode="lines" ,
    line=dict(color=("black"))
    
))
# ponerle titulo
fig.update_layout(title_text="DrawDown y DrawUp")
#mostrar 
fig.show()
####
import plotly.graph_objects as go
fig = go.Figure(data=go.Bar(y=[2, 3, 1],x=['status_quo', 'aversion_perdida', 'sensibilidad_decreciente']))
fig.show()