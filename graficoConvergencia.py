import os
import numpy as np
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt

import zlib
import pickle

def generarGraficosConvergencia(nombreAlgoritmo,engine,metadata,instancias,orden,directory,formatoGraficos,repair,Init):

    # #credenciales
    # config = configparser.ConfigParser()
    # config.read('db_config.ini')
    # host = config['postgres']['host']
    # db_name = config['postgres']['db_name']
    # port = config['postgres']['port']
    # user = config['postgres']['user']
    # pwd = config['postgres']['pass']

    # #Conexión
    # engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
    # metadata = db.MetaData()

    sql = """select 
            fitness_mejor, fitness_mejor_iteracion, fitness_promedio
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


    with engine.connect() as connection:
        for instancia in orden:
            fitmejor = []
            fitmejorIt = []
            fitProm = []
            instanciaStr = f"%{instancia}%"
            param = {"instancia":instanciaStr,"nomalg":nombreAlgoritmo}
            arrResult = connection.execute(text(sql),**param)
            
            #Crear directorio de instancia
            directorygc = directory + "/" + instancia.replace('.txt','') + "/" + repair + "/" + "gc"
            try:
                os.makedirs(str(directorygc))
            except OSError:
                print("Ya existe el directorio %s " % directorygc)
            else:
                print("Se ha creado el directorio: %s " % directorygc)

            if arrResult is not None:

                for result in arrResult:
                    fitmejor.append(result[0])
                    fitmejorIt.append(result[1])
                    fitProm.append(result[2])

                indices = np.arange(1,len(fitmejor)+1)
                fig, ax = plt.subplots()
                fig.suptitle(f"{nombreAlgoritmo.replace('_','-')} Instance {instancia.replace('scp','').replace('nr','').replace('.txt','')}", fontsize=16)
                plt.plot(indices, np.array(fitmejor), label = "Best Fitness")
                #Opcionales
                # plt.plot(indices, np.array(fitmejorIt), label = "Best Fitness at iteration")
                # plt.plot(indices, np.array(fitProm), label = "Average Fitness")
                plt.xlabel('Iteration')
                # Set the y axis label of the current axis.
                plt.ylabel('Fitness')
                ax.autoscale_view()
                filename = f"gc-{Init}-{nombreAlgoritmo.replace('_','-')}-{instancia.replace('.txt','')}"
                if formatoGraficos == "png":
                    fig.savefig(f'{directorygc}/{filename}.png', format='png')
                elif formatoGraficos == "eps":
                    fig.savefig(f'{directorygc}/{filename}.eps', format='eps')
                elif formatoGraficos == "pdf":
                    fig.savefig(f'{directorygc}/{filename}.pdf', format='pdf')
                #print(f'Se ha generado el gráfico de Convergencia del experimento: {nombreAlgoritmo} en la instacia {instancia.replace(".txt","")}')
                plt.close()
