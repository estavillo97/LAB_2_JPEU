# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:27:53 2020

@author: Estavillo
"""
# -- ------------------------------------------------------------------------------------ -- #
# -- Proyecto: laboratorio 2 de trading.                               -- #
# -- Codigo: lab2 - elaborar herramientas de análisis                           -- #
# -- Repositorio: https://github.com/estavillo97/LAB_2_JPEU/funciones.py      --#                                                    -- #
# -- Autor: Juan Pablo Estavillo Urrea                                                                -- #
# -- ------------------------------------------------------------------------------------ -- #
import datetime                                            #para uso de fechas
from oandapyV20 import API                                 # conexion con broker OANDA
import numpy as np                                      # funciones numericas
import pandas as pd                                       # dataframes y utilidades
from datetime import timedelta                            # diferencia entre datos tipo tiempo          
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos

# -- --------------------------------------------------------- FUNCION: Descargar precios -- #
# -- Descargar precios historicos con OANDA
# añadi estas librerias de Francisco por si se llegaran a ocupar
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
    param_archivo : xlsx that will be read.
    
    ---------
    description
    put the location of the xlsx 
    get a data frame from the selected xlsx 
    """
    archivo=pd.read_excel(param_archivo,skiprows=4)
    archivo=archivo.iloc[:18]
    
    #fill with 0
    archivo['Close Time']=archivo['Close Time'].fillna(0)
    
    #eliminar los balance para mantener solo buy y sell
    archivo=archivo[archivo.Type != 'balance']
    return archivo

def f_pip_size(param_ins):
    """
    Parameters
    ----------
    param_ins : string with the name of the pair currency you are trading
    
    Returns
    -------
    pip_inst : func :number of pipss of the currency. 
    
    Debugging
    ---------
    """

    #transfom to lower
    inst = param_ins.lower()
    # dictionary with pips per trading currency
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
    param_data : pd.DataFrame : df con columna agregada 'time'
    
    Debugging
    ---------
    param_data = f_leer_archivo("trade3.xlsx)
    """
    #here i define the index of the clean data 
    a=[1,2,3,4,6,7,8,11,13,14,17]

    # convert into datetie 
    param_data['Close Time'] = pd.to_datetime(param_data['Close Time'])
    param_data['Open Time'] = pd.to_datetime(param_data['Open Time'])
    
   #create time column
    param_data['tiempo'] = [(param_data.loc[i, 'Close Time'] -param_data.loc[i, 'Open Time']).delta / 1e9 for i in a]
        #param_data['tiempo']=
        #param_data['tiempo'][i]=param_data['Close Time'][i]-param_data['Open Time'][i]
    # return param_data['time']
    return param_data

#%%
# Nuevas columnas pips para saber el tamaño en pips de las transacciones ejecutadas 

def f_columnas_pips(data):
    """
    Parameters
    ----------
    datos : pd.DataFrame : dataframe con las transacciones ejecutadas ya con la columna 'tiempos'
    Returns
    -------
    param_data : pd.DataFrame : dataframe anterior pero con columnas 'pips' y 'pips acumulados'
    
    Debugging
    ---------
    datos =  f_leer_archivo("trade3.xlsx")
    
    """

    
    a=[1,2,3,4,6,7,8,11,13,14,17]
    for i in a:
        currency=data['Item'][i]
        data['Item'][i]=currency.split('-')[0]
    
    data['pips'] = [(data['Price.1'][i] - data['Price'][i])*f_pip_size(data['Item'][i]) for i in a]
    data['pips'][data['Type'] == 'sell'] *= -1
    data['pips_acm'] = data.pips.cumsum()
    data['profit_acm'] = data['Profit'].cumsum()
    data['capital_acm'] = 5000 + data.profit_acm 
    
    return data

#%%  Estadísticas básicas

def f_estadisticas_ba(datos):
    """
    Parameters
    ----------
      datos : pd.DataFrame : DataFrame con transacciones después de correr las funciones anteriores
    
    Returns
    -------
    Dos dataframes:
    df_1_tabla : pd.DataFrame :  DataFrame  el cual muestre el ratio de efectividad de las operaciones realizadas con cada instrumento operado
    df_2_ranking : pd.DataFrame : dataframe con un ranking entre el 0 y el 1 en donde se califica con cuales divisas se obtuvieron operaciones precisas realizadas
        
    Debugging
    ---------
    datos = f_leer_archivo("trade3.xlsx")
    """
    
    df_1_tabla = pd.DataFrame({'Ops totales': [len(datos), 'Operaciones totales'],
                                'Ops ganadoras': [len(datos[datos['Profit'] >= 0]), 'Operaciones ganadoras'],
                                'Ops ganadoras_b': [len(datos[(datos['Type'] == 'buy') & (datos['Profit'] >= 0)]), 'Operaciones ganadoras en compra'],
                                'Ops ganadoras_s': [len(datos[(datos['Type'] == 'sell') & (datos['Profit'] >= 0)]), 'Operaciones ganadoras en venta'],
                                'Ops perdedoras': [len(datos[datos['Profit'] < 0]), 'Operaciones perdedoras'],
                                'Ops perdedoras_b': [len(datos[(datos['Type'] == 'buy') & (datos['Profit'] < 0)]), 'Operaciones perdedoras en compra'],
                                'Ops perdedoras_s' : [len(datos[(datos['Type'] == 'sell') & (datos['Profit'] < 0)]), 'Operaciones perdedoras en venta'],
                                'Profit media': [datos['Profit'].median(), 'Mediana de profit de operaciones'],
                                'Pips media': [datos['pips'].median(), 'Mediana de pips de operaciones'],
                                'r_efectividad': [len(datos[datos['Profit'] >= 0])/len(datos), 'Ganadoras Totales/Operaciones Totales'],
                                'r_proporcion': [len(datos[datos['Profit'] >= 0]) / len(datos[datos['Profit'] < 0]), 'Perdedoras Totales/Ganadoras Totales'],
                                'r_efectividad_b': [len(datos[(datos['Type'] == 'buy') & (datos['Profit'] >= 0)]) / len(datos), 'Operaciones ganadoras de compra/Operaciones Totales'],
                                'r_efectividad_s': [len(datos[(datos['Type'] == 'sell') & (datos['Profit'] >= 0)]) / len(datos), 'Operaciones ganadoras de venta/Operaciones Totales'],
                                }, index = ['Valor', 'Descripción']).transpose()
    
    tb1 = pd.DataFrame({i: len(datos[datos.Profit >0][datos.Item == i])/len(datos[datos.Item == i])
                        for i in datos.Item.unique()}, index = ['rank']).transpose()
    
    df_2_ranking = (tb1*100).sort_values(by = 'rank', ascending = False).T.transpose()
    
    return {'df_1_tabla' : df_1_tabla, 'df_2_ranking' : df_2_ranking}

#%% Parte 3
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
     datos = f_leer_archivo("trade3.xlsx")
     """
     # cantidad de operaciones cerradas ese dia
     datos['ops'] = [i.date() for i in datos['Close Time']] 
     diario = pd.date_range(datos.ops.min(),datos.ops.max()).date
     # convertir a dataframe las fechas diarias
     fechas = pd.DataFrame({'timestamp' : diario})
     
     groups = datos.groupby('ops')
     profit = groups['Profit'].sum()
     # convertir los profits diarios a dataframe
     profit_diario = pd.DataFrame({'profit_d' : ['Profit'[i] if i in profit.index else 0 for i in diario]})
     profit_acm = np.cumsum(profit_diario) + 5000
     # juntar en un solo dataframe los dos dataframes anteriores fechas y profits diarios
     f_p1 =pd.merge(fechas, profit_diario, left_index = True, right_index = True)
     # juntar el dataframe anterior de los dos df con los profits acumulados
     df_profit_diario1 = pd.merge(f_p1, profit_acm, left_index = True, right_index = True)
     # renombrar las columnas del nuevo dataframe
     df_profit_diario = df_profit_diario1.rename(columns = {"profit_d_x" : "profit_d", "profit_d_y" : "profit_acm_d"})
     
     return df_profit_diario
def f2_profit_diario(datos):
     #dia inicial
     inicio=datos['Open Time'].min()
     #dia ultimo
     final=datos['Close Time'].max()
     #que dia se hizo la operacion
     datos['date'] = [i.date() for i in datos['Close Time']] 
     #diario = pd.date_range(datos.ops.min(),datos.ops.max()).date
     # convertir a dataframe las fechas diarias
     
     
     #groups = datos.groupby('ops')
     #fechas para que se conviertan en indice 
     fechas=[]
     profit_diario=[]
     #añadir todas las fechas 
     fechas.append(inicio)
     i=inicio
     #ciclo para obtener todos los dias 
     while i<final:
         
         i=i+datetime.timedelta(days=1)
         #quitar sábados 
         if datetime.date.weekday(i)!=5:
             fechas.append(i.date)
               

     
     df=pd.DataFrame(columns=['profit_d','pofit_acm_d'],index=fechas)
     #usarlo como lista para meter el profit usando el date  
     dates=datos['date'].tolist
     #usar listas para meter el profit 
     pr=datos['Profit'].tolist

                 
                          
     return df
     

#%%
# Terminar el profit acumulado diario antes de terminar stats mad
def f_estadisticas_mad(datos):
    """
    Parameters
    ----------
    datos : DataFrame con transacciones actualizadas
    
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

#%%  Parte 4 