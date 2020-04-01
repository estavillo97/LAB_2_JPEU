# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:27:53 2020

@author: Estavillo
"""

# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: Describir brevemente el proyecto en general                                -- #
# -- Codigo: lab2 - describir brevemente el codigo                             -- #
# -- Repositorio: https://github.com/estavillo97/LAB_2_JPEU/funciones.py      --#                                                    -- #
# -- Autor: Juan Pablo Estavillo Urrea                                                                -- #
# -- ------------------------------------------------------------------------------------ -- #

# import numpy as np                                      # funciones numericas
import pandas as pd                                       # dataframes y utilidades
from datetime import timedelta                            # diferencia entre datos tipo tiempo
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos


# -- --------------------------------------------------------- FUNCION: Descargar precios -- #
# -- Descargar precios historicos con OANDA

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Parameters
    ----------
    p0_fini
    p1_ffin
    p2_gran
    p3_inst
    p4_oatk
    p5_ginc
    Returns
    -------
    dc_precios
    Debugging
    ---------
    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """
        Parameters
        ----------
        p0_start
        p1_end
        p2_inc
        p3_delta
        Returns
        -------
        ls_resultado
        Debugging
        ---------
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4999:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final
    
############################# funciones nuevas 

def f_leer_archivo(param_archivo):
    
    """
    Parameters
    ----------
    param_archivo
    
    ---------
    descripción
    Al ingresar la localización y/o nombre de tu archivo, 
    debes de obtener de regreso el dataframe con toda la información.
    """
    archivo=pd.read_excel(param_archivo,skiprows=4)
    archivo=archivo.iloc[:18]
    archivo['Close Time']=archivo['Close Time'].fillna(0)
    
    return archivo

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


#%%


def f_columnas_tiempos(param_data):
    """
    Parameters
    ----------
    param_data : pd.DataFrame : df con información de transacciones ejecutadas
    
    Returns
    -------
    param_data : pd.DataFrame : df con columna agregada 'tiempo'
    
    Debugging
    ---------
    param_data = f_leer_archivo("trade3.xlsx)
    """
    
    # convert into datetie 
    param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
    param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])
    
    # time transcurred 
    #param_data['time']=
    param_data['time'] = [(param_data.loc[i, 'Close Time'] -
                             param_data.loc[i, 'Open Time']).delta / 1e9
                            for i in range(0, len(param_data['Close Time']))]


    # return param_data['time ']
    return param_data

#%%
# Nuevas columnas pips para saber el tamaño en pips de las transacciones ejecutadas 

def f_columnas_pips(datos):
    """
    Parameters
    ----------
    datos : pd.DataFrame : dataframe con las transacciones ejecutadas ya con la columna 'tiempos'
    Returns
    -------
    param_data : pd.DataFrame : dataframe anterior pero con columnas 'pips' y 'pips acumulados'
    
    Debugging
    ---------
    datos =  f_leer_archivo("archivo_tradeview_1.xlsx")
    
    """
#    param_data['pips'] = [param_data.loc[i,'closeprice'] * f_pip_size(param_ins=param_data.loc[i,'symbol']) for i in range\
#               (0, len(param_data.rows)) 
#                  if param_data['type'] == 'buy' else\
#                  param_data.loc[i,'openprice'] \
#                  * f_pip_size(param_ins=param_data.loc[i,'symbol'])]
#    return param_data['pips']
    
    datos['pips'] = [(datos.closeprice[i] - datos.openprice[i])*f_pip_size(datos.symbol[i]) for i in range(len(datos))]
    datos['pips'][datos.type == 'sell'] *= -1
    datos['pips_acm'] = datos.pips.cumsum()
    datos['profit_acm'] = datos['profit'].cumsum()
    
    return datos.copy()

#%%  Estadísticas básicas

def f_basic_stats(datos):
    """
    Parameters
    ----------
      datos : pd.DataFrame : dataframe con las transacciones ejecutadas, después de 'tiempos'
    
    Returns
    -------
    Dos dataframes:
    df_1_tabla : pd.DataFrame : dataframe con estadísticas básicas del comportamiento del trader
    df_2_ranking : pd.DataFrame : dataframe con un ranking entre el 0 y el 1 en donde se califica con cuales divisas se obtuvieron operaciones precisas realizadas
        
    Debugging
    ---------
    datos = f_leer_archivo("archivo_tradeview_1.xlsx")
    """
    # print('------------')
    # print(datos.head(3))
    # print('------------')
    
    # Ejemplo: df[(df['col1'] >= 1) & (df['col1'] <=1 )]
    
    df_1_tabla = pd.DataFrame({'Ops totales': [len(datos['order']), 'Operaciones totales'],
                                'Ops ganadoras': [len(datos[datos['profit'] >= 0]), 'Operaciones ganadoras'],
                                'Ops ganadoras_b': [len(datos[(datos['type'] == 'buy') & (datos['profit'] >= 0)]), 'Operaciones ganadoras en compra'],
                                'Ops ganadoras_s': [len(datos[(datos['type'] == 'sell') & (datos['profit'] >= 0)]), 'Operaciones ganadoras en venta'],
                                'Ops perdedoras': [len(datos[datos['profit'] < 0]), 'Operaciones perdedoras'],
                                'Ops perdedoras_b': [len(datos[(datos['type'] == 'buy') & (datos['profit'] < 0)]), 'Operaciones perdedoras en compra'],
                                'Ops perdedoras_s' : [len(datos[(datos['type'] == 'sell') & (datos['profit'] < 0)]), 'Operaciones perdedoras en venta'],
                                'Profit media': [datos['profit'].median(), 'Mediana de profit de operaciones'],
                                'Pips media': [datos['pips'].median(), 'Mediana de pips de operaciones'],
                                'r_efectividad': [len(datos[datos['profit'] >= 0])/len(datos['order']), 'Ganadoras Totales/Operaciones Totales'],
                                'r_proporcion': [len(datos[datos['profit'] >= 0]) / len(datos[datos['profit'] < 0]), 'Perdedoras Totales/Ganadoras Totales'],
                                'r_efectividad_b': [len(datos[(datos['type'] == 'buy') & (datos['profit'] >= 0)]) / len(datos['order']), 'Operaciones ganadoras de compra/Operaciones Totales'],
                                'r_efectividad_s': [len(datos[(datos['type'] == 'sell') & (datos['profit'] >= 0)]) / len(datos['order']), 'Operaciones ganadoras de venta/Operaciones Totales'],
                                }, index = ['Valor', 'Descripción']).transpose()
    
    tb1 = pd.DataFrame({i: len(datos[datos.profit >0][datos.symbol == i])/len(datos[datos.symbol == i])
                        for i in datos.symbol.unique()}, index = ['rank']).transpose()
    
    df_1_ranking = (tb1*100).sort_values(by = 'rank', ascending = False).T.transpose()
    
    return {'df_1_tabla' : df_1_tabla.copy(), 'df_1_ranking' : df_1_ranking.copy()}

#%% Parte 3: Medidas de atribución al desempeño
#%% 
# Cálculo del capital acumulado
def f_capital_acm(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : dataframe con transacciones ejecutadas después de haber corrido 'tiempos' y 'pips'
    Returns
    -------
    datos : pandas.DataFrame : se le agrega una columna al dataframe
    
    Debugging
    ---------
    datos = f_leer_archivo("archivo_tradeview_1.csv")
    """
    
    # Se forma una nueva columna inicializada en $5,000 donde se le suma/resta el profit acumulado en cada renglón
    datos['capital_acm'] = 5000 + datos.profit_acm 
    return datos.copy()

#%% 
# Cálculo del profit diario
    
def f_profit_diario(datos):
     """
     Parameters
     ----------
     datos : pandas.DataFrame : dataframe de fechas históricas solo usando columnas timestamp y profit
  
     Returns
     -------
     datos : pandas.DataFrame : dataframe con las columnas timestamp, profit diario y el acumulado
  
     Debugging
     ---------
     datos = f_leer_archivo("archivo_tradeview_1.xlsx")
     """
     pass
  

#%%
    
# Terminar el profit acumulado diario antes de terminar stats mad
    
def f_stats_mad(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : dataframe con transacciones ejecutadas después de tiempos y pips
    
    Returns
    -------
    datos : pandas.DataFrame : dataframe con rendimientos logarítmicos. Tomando en cuenta que se inicializa con una cuenta de $5,000
    Debugging
    ---------
    datos = 'f_leer_archivo("archivo_tradeview_1.csv")
    
    """
    rend_log = np.log(datos.capital_acm[1:].values/datos.capital_acm[:-1].values)
    # benchmark = 
    # rend_log_bench = np.log(datos_benchmark...)
    # tracking_error = rend_log - rend_log_bench
    
    # https://towardsdatascience.com/python-for-finance-stock-portfolio-analyses-6da4c3e61054
    # https://www.investopedia.com/terms/i/informationratio.asp    
    rf = 0.08
    
    #%%
    #TIP DEL PROFE
    #df_data.groupby('fechas_dias')['profit'].sum()
    #%%
    # Cambiar a semanal los datos
    # Agregar un benchmark SP500
    MAD = pd.DataFrame({
        'sharpe': (rend_log.mean()*30 - rf) / rend_log.std()*(30**0.5),
        'sortino_b': (rend_log.mean()*30 - rf) / rend_log[rend_log >= 0].std()*(30**0.5),
        'sortino_s': (rend_log.mean()*30 - rf) / rend_log[rend_log < 0].std()*(30**0.5),
        # Que de donde se inicia, no hayan valores mayores al punto de inicio y sea solo tendencia bajista
        # 'drawdown_cap': 
        # Que de donde se inicia, no hayan valores menores al punto de inicio y que sea solo tendencia alcista
        # 'drawup_cap': 
        #'drawdown_pips': datos.pips_acm...,
        #'drawup_pips': datos.pips_acm.. #,
        # 'information_ratio': (rend_log.mean()*7 - rend_log_bench.mean()*7) / tracking_error.std()*7**0.5
        }, index = ['Valor']).transpose()

    return MAD

#%% Parte 4: Sesgos cognitivos del trader

# def f_sesgos_cognitivos():
#     """
#     Parameters
#     ----------
    
#     Returns
#     -------
    
#     Debugging
#     ---------
    
#     """
    
#     pass
    
# Disposission effect

