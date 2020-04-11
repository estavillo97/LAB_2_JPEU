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
import pandas_datareader.data as web
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
     #use 2 tipos de fechas para formar el dataframe 
     fechas = pd.DataFrame({ 'timestamp' :   (pd.date_range(datos['Close Time'].min(), datos['Close Time'].max(), normalize = True))})
     # cantidad de operaciones cerradas ese dia
     datos['operations'] = [i.date() for i in datos['Close Time']] 
     #variable que usa todas las fechas usadas para hacer trading 
     diario = pd.date_range(datos.operations.min(),datos.operations.max()).date
     # convertir a dataframe las fechas diarias
     fechas2 = pd.DataFrame({'timestamp' : diario})
     #agrupar las operaciones 
     groups = datos.groupby('operations')
     #sumar los profits 
     profit = groups['Profit'].sum()
     # convertir los profits diarios a dataframe
     prd = pd.DataFrame({'profit_d' : [profit[i] if i in profit.index else 0 for i in diario]})
     profit_acm = np.cumsum(prd) + 5000
     # juntar en un solo dataframe los dos dataframes anteriores fechas y profits diarios
     merge1 =pd.merge(fechas, prd, left_index = True, right_index = True)
     # juntar el dataframe anterior de los dos df con los profits acumulados
     df_profit_diario1 = pd.merge(merge1, profit_acm, left_index = True, right_index = True)
     # renombrar las columnas del nuevo dataframe
     df_profit_diario = df_profit_diario1.rename(columns = {"profit_d_x" : "profit_d", "profit_d_y" : "profit_acm_d"})
     #combinamos data frames
     df=pd.merge(df_profit_diario,fechas2,left_index=True,right_index=True)
     #eliminamos los sabados 
     df = df[df.timestamp_x.dt.weekday != 5]
     #usamos la columna de timestamp como index
     df=df.set_index('timestamp_y')
     #borramos el timestamp que ya no vamos a usar 
     df=df.drop('timestamp_x',axis=1)
     return df

     

#%%
def f_stats_mad(datos):
    """
    Parameters
    ----------
    datos : pandas.DataFrame : dataframe de datos después de ser usado en las funciones de parte 2
    
    Returns
    -------
    datos : pandas.DataFrame : rendimientos logarítmicos. 
            Se va a utilizar como referencia una cuenta con 5000 USD
    Debugging
    ---------
    datos = 'f_leer_archivo("trade3.xlsx")
    
    """
    profit_d = f_profit_diario(datos)
    
    # Sharpe ratio
    rend_log = np.log(profit_d.profit_acm_d[1:].values/profit_d.profit_acm_d[:-1].values)
    rf = 0.08/300
    mar = 0.3/300
    
        
    # Sortino compra
    # Numerador
    s_buy = (f_profit_diario(datos[datos['type'] == 'buy']))
    rend_log_b = np.log(s_buy.profit_acm_d[1:].values / s_buy.profit_acm_d[:-1].values)
    # Denominador
    tdd_sb = rend_log_b - mar
    tdd_sb[tdd_sb > 0] = 0
    # Final
    sortino_b = (rend_log_b.mean() - mar) / (((tdd_sb*2).mean())*0.5)
    

    # Sortino venta
    # Numerador
    s_sell = (f_profit_diario(datos[datos['type'] == 'sell']))
    rend_log_s = np.log(s_sell.profit_acm_d[1:].values / s_sell.profit_acm_d[:-1].values)
    # Denominador
    tdd_ss = rend_log_s - mar
    tdd_ss[tdd_ss > 0] = 0
    # Final
    sortino_s = (rend_log_s.mean() - mar) / ((tdd_ss*2).mean())*0.5
    
    
    
    # DD y DU
    where_row = profit_d.loc[profit_d['profit_acm_d'] == profit_d.profit_acm_d.min()]
    where_position = where_row.index.tolist()
    
    # Drawdown
    prev_where = profit_d.loc[0:where_position[0]]
    where_max_prev = profit_d.loc[profit_d['profit_acm_d'] == prev_where.profit_acm_d.max()]
    where_min_prev = profit_d.loc[profit_d['profit_acm_d'] == prev_where.profit_acm_d.min()]
    max_dd = where_max_prev.iloc[0]['profit_acm_d']
    min_dd = where_min_prev.iloc[0]['profit_acm_d']
    dd = max_dd - min_dd
    fecha_i_dd = where_max_prev.iloc[0]['timestamp']
    fecha_f_dd = where_min_prev.iloc[0]['timestamp']
    drawdown =  "{}, {}, ${:.2f}" .format(fecha_i_dd, fecha_f_dd, dd)
     
    # Drawup
    foll_where = profit_d.loc[where_position[0]:]
    where_max_foll = profit_d.loc[profit_d['profit_acm_d'] == foll_where.profit_acm_d.max()]
    where_min_foll = profit_d.loc[profit_d['profit_acm_d'] == foll_where.profit_acm_d.min()]
    max_du = where_max_foll.iloc[0]['profit_acm_d']
    min_du = where_min_foll.iloc[0]['profit_acm_d']
    du = max_du - min_du
    fecha_f_du = where_max_foll.iloc[0]['timestamp']
    fecha_i_du = where_min_foll.iloc[0]['timestamp']
    drawup =  "{}, {}, ${:.2f}" .format(fecha_i_du, fecha_f_du, du)        

    
    # Information Ratio
    benchmark_original = pd.DataFrame(web.YahooDailyReader('^GSPC', profit_d['timestamp'].min(), profit_d['timestamp'].max(), interval='d').read()['Adj Close'])
    # Ajustar fechas como columna en el dataframe
    benchmark = benchmark_original.reset_index()
    # Agregar columna de los rendimientos logarítmicos de los precios de Cierre Ajustado del SP500
    benchmark['rend_log'] = pd.DataFrame(np.log(benchmark['Adj Close'][1:].values / benchmark['Adj Close'][:-1].values))
    # Juntar el dataframe de profits con el benchmark en uno solo
    bench_merge = profit_d.merge(benchmark,  left_on = 'timestamp', right_on = 'Date')
    # Recorrer los valores de los rendimientos logarítmicos una posición abajo y llenar con 0
    bench_merge['rend_log'] = bench_merge['rend_log'].shift(1, fill_value = 0)
    
    # Cálculo de rendimientos logarítmicos de los profit_acm_d
    rend_log_profit = pd.DataFrame(np.log(bench_merge.profit_acm_d[1:].values/bench_merge.profit_acm_d[:-1].values))
    # rend_log_profit = rend_log_profit.shift(1, fill_value = 0)
    
    # Agregar la columna de rendimientos de profit_acm_d 
    bench_merge.insert(3, column = 'rend_log_profit', value = rend_log_profit)
    # Recorrer una fila hacia abajo los rendimientos en el dataframe
    bench_merge['rend_log_profit'] = bench_merge['rend_log_profit'].shift(1, fill_value = 0)
    
    # Numerador Information Ratio
    # Promedio de rendimientos del profit_acm_d
    profit_prom = bench_merge['rend_log_profit'].mean()
    # Promedio de rendimientos del SP500
    bench_prom = bench_merge['rend_log'].mean()
    # Numerador del information ratio = diferencia de los dos anteriores
    num_ir = profit_prom - bench_prom
    
    # Denominador Information Ratio
    # Diferencia por rows de los rendimientos del profit_acm_d y del SP500
    dif_denom = bench_merge['rend_log_profit'] - bench_merge['rend_log']
    # Desviación estándar de la diferencia
    denom_ir = dif_denom.std()
    
    # Cálculo del ratio
    info_ratio = num_ir/denom_ir
    
    
    # Métricas
    metrica = pd.DataFrame({'métricas': ['sharpe', 'sortino_b', 'sortino_s', 'drawdown_cap_b', 'drawdown_cap_s', 'information_r']})
    valor = pd.DataFrame({'valor' : [((rend_log.mean() - rf)/ rend_log.std()), 
                                     (sortino_b),
                                     (sortino_s),
                                     (drawdown),
                                     (drawup),
                                     (info_ratio)
                                     ]})
    
    df_mad1 = pd.merge(metrica, valor, left_index = True, right_index = True)
    descripcion = pd.DataFrame({'descripción': ['Sharpe Ratio', 'Sortino Ratio para Posiciones de Compra', 'Sortino Ratio para Posiciones de Venta', 'DrawDown de Capital', 'DrawUp de Capital', 'Information Ratio']})
    df_MAD = pd.merge(df_mad1, descripcion, left_index = True, right_index= True)
    # convert_dict = {'valor': float} 
    # df_MAD = df_MAD.astype(convert_dict) 
    
    return df_MAD
 ####
def f2_stats_mad(datos):
    #necesitamos los datos de profit diario
    prd=f_profit_diario(datos)
    #descargamos los precios diarios del benchmark que en este caso es el sp500 diario
    sp500d = pd.DataFrame(web.YahooDailyReader('^GSPC', prd.index.min(), prd.index.max(), interval='d').read()['Adj Close']).reset_index()
    #risk free rate 
    rfr=.08/300
    #mar rate 
    mar=.3/300
    
    #