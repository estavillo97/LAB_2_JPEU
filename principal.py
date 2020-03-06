# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: principal.py - layout general del proyecto
# -- mantiene: Juan Pablo Estavillo
# -- repositorio: https://github.com/
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import pandas as pd

#%%
datos = fn.f_leer_archivo('archivo_tradeview_1.xlsx')

import funciones as fn

# no esta completo


def importar_precios(n_archivo):
    data = pd.read_csv(n_archivo)
    return data


importar_precios('trade3.XLS')

def f_pip_size(param_inst):



    #inst=inst.lower()
    #pips_inst={'usdjpy':100,
       #     'gbpjpy':100}
    
    return  1
