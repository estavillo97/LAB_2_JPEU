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

import funciones as fn
import pandas as pd

#%%
# no esta completo

def f_leer_archivo(n_archivo):
    data = pd.read_excel(n_archivo)
    return data


data=f_leer_archivo('trade3.xlsx')


def f_pip_size(param_ins):
    """
    Parameters
    ----------
    param_ins : str : instrument name
    
    Returns
    -------
    pip_inst : func :number of pips of the selected financial asset
    
    Debugging
    ---------
    
    """

    #transfom to lower
    inst = param_ins.lower()

    # list
    pip_inst = {'usdjpy': 100, 'gbpjpy': 100, 'eurjpy': 100, 'cadjpy': 100,
                'chfjpy': 100,
                'eurusd': 10000, 'gbpusd': 10000, 'usdcad': 10000, 'usdmxn': 10000,
                'audusd': 10000, 'nzdusd': 10000, 'usdchf': 10000, 'eurgbp': 10000,
                'eurchf': 10000, 'eurnzd': 10000, 'euraud': 10000, 'gbpnzd': 10000,
                'gbpchf': 10000, 'gbpaud': 10000, 'audnzd': 10000, 'nzdcad': 10000,
                'audcad': 10000, 'xauusd': 10, 'xagusd': 10, 'btcusd': 1}

    return pip_inst[inst]

data = fn.f_columnas_tiempos(data)

data = fn.f_columnas_pips(data)


data = fn.f_capital_acm(data)


estadisticas = fn.f_basic_stats(data)

profit_d = fn.f_profit_diario(data)
desempeno = fn.f_stats_mad(data)
#%%
#las conclusiones irán aqui 