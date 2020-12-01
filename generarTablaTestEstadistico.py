import sqlalchemy as db
import configparser
from sqlalchemy.sql import text
import pandas as pd
import numpy as np
import json
from scipy.stats import ranksums, mannwhitneyu
import csv
import math


def generarTablaTestEstadistico(nombreAlgoritmo,instancias,engine,metadata,orden,file):

    df = pd.read_csv('dataExperimentos.csv')
    instancias = df['instancia'].unique()
    parametros = df['parametro'].unique()
    #parametros = [" ".join(sorted(param.split(" "))) for param in parametros]
    #parametros.sort()
    #print(parametros)
    #exit()

    #print(instancias)
    #print(parametros)

    """

    42

    p1,p2,p3
    p1
    p2
    p3

    """

    dataDict = {}
    dataDict['instancia'] = []
    dataDict['param1'] = []
    dataDict['param2'] = []
    dataDict['pvalue'] = []

    print(parametros)

    paramData = []
    paramDatanumber = []


    parametro1 = 'alpha: 1 recompensa: 2'
    print (f'parametro1 = {parametro1}')
    param1Data = []
    param1number = []

    for parametro2 in parametros:
        instanciaData = []
        for instancia in instancias:
            print(instancia)
            datosInstancia = df.where(df['instancia'] == instancia).dropna()
            
            #print(datosInstancia)
            #exit()
            
            #if parametro1 == parametro2:
            #    continue
            dataParametros1 = np.array(json.loads( datosInstancia.where(datosInstancia['parametro'] == parametro1).dropna()['valores'].values[0] ))
            dataParametros2 = np.array(json.loads( datosInstancia.where(datosInstancia['parametro'] == parametro2).dropna()['valores'].values[0] ))
            #print(np.array(json.loads(dataParametros1)))
            #exit()
            #print(df.where(df['instancia'] == instancia and df['parametro'] == parametro1))
            #pValue = aplicarTest()
            try:
                if parametro1 != parametro2 and (dataParametros1!=dataParametros2).all():
                    pValue = mannwhitneyu(dataParametros1, dataParametros2, alternative='less')[1]
                    instanciaData.append(pValue)
                #pValue = ranksums(dataParametros1, dataParametros2).pvalue
                
            except Exception as error:
                print(f"error con parametros {parametro1}; {parametro2}; instancia {instancia}")
                print(f"valores {dataParametros1} ***\n {dataParametros2}")
                raise error
            #print(f"instancia {instancia} param1 {parametro1}, param2 {parametro2}, pvalue {pValue}")
            #dataDict['instancia'].append(instancia)

            
            
            #dataDict[parametro2] = pvalue
            #dataDict['param1'].append(parametro1)
            #dataDict['param2'].append(parametro2)
            #dataDict['pvalue'].append(pValue)
        print(instanciaData)
        promedio = np.average(np.array(instanciaData))
        if math.isnan(promedio):
            param1number.append(0)
        else:
            param1number.append(promedio)
        if promedio < 0.05:
            param1Data.append("\\textbf{" + "{:.3f}".format(promedio) + "}")
        else:
            param1Data.append("{:.3f}".format(promedio))
        #paramData.append(np.average(np.array(instanciaData)))
    paramData.append(param1Data)
    paramDatanumber.append(param1number)

    df1 = pd.DataFrame(np.array(paramData))
    df1.index = df1.index+1
    df1.to_csv(f'testEstadistico-promedio.csv', sep='&', line_terminator='\\\\\n',  quoting=csv.QUOTE_NONE, escapechar=" ")
    #print(paramDatanumber)
    print(np.sum(np.array(paramDatanumber), axis=1))
    print(np.argmin(np.sum(np.array(paramDatanumber), axis=1)))