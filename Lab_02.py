# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - layout general del proyecto
# -- mantiene: juanpabloestavillo
# -- repositorio: https://github.com/
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import pandas as pd

#%%
#datos = fn.f_leer_archivo('archivo_tradeview_1.xlsx')

import funciones as fn

# no esta completo


def f_leer_archivo(param_archivo):
    data = pd.read_excel(n_archivo)
    
    return data
   

data=f_leer_archivo('trade3.xlsx')

def f_pip_size(param_inst):
    if 'jpy' in param_inst:
        a=10000
    else:
        a=100
    return a
a=f_pip_size('eurusd')
def f_columnas_tiempos(param_data):

def f_columnas_pips(param_data:):
    
def f_estadisticas_ba(param_data):
    
def f_estadisticas_av(param_data):
    


    #inst=inst.lower()
    #pips_inst={'usdjpy':100,
       #     'gbpjpy':100}
    
    return  1


