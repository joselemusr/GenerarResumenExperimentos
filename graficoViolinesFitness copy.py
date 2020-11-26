# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:39:13 2020

@author: felip
"""


import os
import numpy as np
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import requests

import zlib
import pickle

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats # importando scipy.stats
from matplotlib import pyplot as plt 
import pandas

def generarDataGraficos(experimentos,engine,metadata,orden,directory,nombre_algoritmo,repair,Init,MH):
    
    sql = """ select re.fitness, de.nombre_algoritmo from resultado_ejecucion as re
	inner join datos_ejecucion as de on re.id_ejecucion = de.id 
		where de.parametros ilike :instancia
			and de.nombre_algoritmo = :nomalg
	order by de.nombre_algoritmo asc 
							limit 31;"""
    with engine.connect() as connection:
        for instancia in orden:
            instanciaStr = f"%{instancia}%"
            #print(instanciaStr)
            newDirectory = directory + instancia.replace(".txt","") + "/" + repair + "/dg" 
            try:
                os.makedirs(str(newDirectory))
            except OSError:
                print("Ya existe el directorio %s " % newDirectory)
            else:
                print("Se ha creado el directorio: %s " % newDirectory)
            resultado = open(newDirectory + "/dg-" + Init + "-" + MH + "-SCP-CPU-" + repair + instancia.replace(".txt","")+'.csv', 'w')
            resultado.write("fitness,archivo\n")
            for algoritmo in experimentos:
                param = {"instancia":instanciaStr,"nomalg":algoritmo} 
                arrResult = connection.execute(text(sql),**param)
            
                for result in arrResult:
                    resultado.write(str(result[0])+','+result[1].split("_")[2]+'\n')
            resultado.close()
            
            
def generarGraficoViolin(directory,nombre_algoritmo,orden,tipo):

    for instancia in orden:
        
        filename = directory+'/Data Violin_'+instancia.replace(".txt","")+'.csv'
        data = pandas.read_csv(filename,header=0)
        
        fig, ax = plt.subplots()
        sns.set(style="whitegrid")
        if tipo == "violin":
            ax = sns.violinplot(x="archivo",y="fitness",data=data)
        if tipo == "boxplot":
            ax = sns.boxplot(x="archivo",y="fitness",data=data)
        ax.set_title("Fitness Distribution Obtained "+nombre_algoritmo)
        plt.xlabel("instance "+instancia.replace(".txt",""))
        plt.ylabel("fitness")
        fig.savefig(f'{directory}/Grafico_{tipo}_{instancia.replace(".txt","")}_{nombre_algoritmo}.pdf', format='pdf')
        print(f'Se ha generado el gráfico de {tipo} para {nombre_algoritmo} en la instacia {instancia.replace(".txt","")}')
        plt.close() 
        
        
def generarGraficoBoxPlot(directory,nombre_algoritmo,orden,tipo):

    for instancia in orden:
        
        filename = directory+'/Data Violin_'+instancia.replace(".txt","")+'.csv'
        data = pandas.read_csv(filename,header=0)
        
        fig, ax = plt.subplots()
        sns.set(style="whitegrid")
        if tipo == "violin":
            ax = sns.violinplot(x="archivo",y="fitness",data=data)
        if tipo == "boxplot":
            ax = sns.boxplot(x="archivo",y="fitness",data=data)
        ax.set_title("Fitness Distribution Obtained "+nombre_algoritmo)
        plt.xlabel("instance "+instancia.replace(".txt",""))
        plt.ylabel("fitness")
        fig.savefig(f'{directory}/Grafico_{tipo}_{instancia.replace(".txt","")}_{nombre_algoritmo}.pdf', format='pdf')
        print(f'Se ha generado el gráfico de {tipo} para {nombre_algoritmo} en la instacia {instancia.replace(".txt","")}')
        plt.close() 
        
        
        
        
        