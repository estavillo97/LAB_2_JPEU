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
import plotly.offline as py       # hasta arriba
#py.offline.init_notebook_mode(connected=False)    # hasta arriba
#py.iplot(tu_grafica)                                                     # en el mismo renglon
import funciones as fn           #aqui están todas las funciones 
import pandas as pd              #pandas  aunque no se use 

#%%
#leer archivo 
data=fn.f_leer_archivo('trade3.xlsx')

#agregar columna de tiempo 
data=fn.f_columnas_tiempos(data)

#agregar columna de pip
data = fn.f_columnas_pips(data)

#diccionario con estadísticas de operaciones 
estadisticas = fn.f_estadisticas_ba(data)

#crear dataframe con los profits de cada dia 
profit_d = fn.f_profit_diario(data)

desempeno = fn.f_stats_mad(data)
#%%
#parte 4
