
import os
import numpy as np
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import json
import requests

import zlib
import pickle

def generarGraficosDiversidad(nombresAlgoritmos,engine,metadata,orden,directory,formatoGraficos,Init,repair):

    sql = """select 
            parametros_iteracion
            from
            datos_iteracion
            where id_ejecucion = (
            select datos_ejecucion.id from datos_ejecucion 
            inner join resultado_ejecucion on datos_ejecucion.id = resultado_ejecucion.id_ejecucion
            where datos_ejecucion.parametros ILIKE :instancia
            and nombre_algoritmo = :nomalg
            order by resultado_ejecucion.fitness asc
            limit 1
            ) order by datos_iteracion.id asc"""
            
    res = []
    i=0
    medidasDiversidad = []
    medidasDiversidad.append('DimensionalHussain') #0
    medidasDiversidad.append('PesosDeInercia') #1
    medidasDiversidad.append('LeungGaoXu') #2
    medidasDiversidad.append('Entropica') #3
    medidasDiversidad.append('Hamming') #4
    medidasDiversidad.append('MomentoDeInercia') #5

    with engine.connect() as connection:
        for instancia in orden:

            #Crear directorio de instancia
            directorygd = directory + "/" + instancia.replace('.txt','') + "/" + repair + "/" + "gd"
            try:
                os.makedirs(str(directorygd))
            except OSError:
                print("Ya existe el directorio %s " % directorygd)
            else:
                print("Se ha creado el directorio: %s " % directorygd)

            for medidaDiv in medidasDiversidad:
                fig, ax = plt.subplots()
                idx = 0
                for nombreAlgoritmo in nombresAlgoritmos:
                    estado = []
                    facEvol = []
                    
                    instanciaStr = f"%{instancia}%"
                    param = {"instancia":instanciaStr,"nomalg":nombreAlgoritmo}
                    #print(instanciaStr)
                    
                    arrResult = connection.execute(text(sql),**param)
                    i = 0
                    maxDiversidades = None
                    diversidad = []
                    for result in arrResult:
                        fila = json.loads(result[0])
                        # print(f"fila['PorcentajeExplor']: {fila['PorcentajeExplor']}")
                        # print(f"fila['PorcentajeExplor']: {list(fila['PorcentajeExplor'].replace('[','').replace(']','').split(' '))}")
                        diversidadBD = list(fila['Diversidades'].replace("[","").replace("]","").split(" ")) #[0, , , ,1,2,3,4,5]
                        diversidadBD = np.array([float(item) for item in diversidadBD if item != ""])                
                        diversidad.append(diversidadBD)
                        
                    diversidadGrafico = np.array(diversidad)
                
                    plt.plot(np.arange(diversidadGrafico.shape[0]),diversidadGrafico[:,idx])
                idx = idx + 1
                
                fig.suptitle(f"{nombreAlgoritmo.replace('_','-')}{medidaDiv} % Diversity {instancia.replace('scp','').replace('nr','').replace('.txt','')}", fontsize=16) #Mover despues, no es necesario hacer esta linea en cada for
                plt.legend(nombresAlgoritmos, loc='upper left')
                versiones = str(nombresAlgoritmos).replace('WOA','').replace('GWO','').replace('SCA','').replace('HHO','').replace('_SCP','').replace('_CPU_C','').replace('_CPU_S','').replace('_','-').replace('[','-').replace(']','-').replace(' ','').replace(',','').replace("'","").replace('--','-')
                algoritmo = nombresAlgoritmos[0].replace('_SCP_BCL1_CPU_S','-S').replace('_SCP_BCL1_CPU_S','-S').replace('_SCP_BCL1_CPU_S','-S').replace('_SCP_BCL1_CPU_S','-S').replace('_SCP_BCL1_CPU_C','-C').replace('_SCP_BCL1_CPU_C','-C').replace('_SCP_BCL1_CPU_C','-C').replace('_SCP_BCL1_CPU_C','-C')
                filename = f"gd-{Init}-{medidaDiv}-{algoritmo}{versiones}{instancia.replace('.txt','')}"
                if formatoGraficos == "png":
                    fig.savefig(f'{directorygd}/{filename}.png', format='png')
                elif formatoGraficos == "eps":
                    fig.savefig(f'{directorygd}/{filename}.eps', format='eps')
                elif formatoGraficos == "pdf":
                    fig.savefig(f'{directorygd}/{filename}.pdf', format='pdf')
                plt.close()
