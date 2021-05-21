import os
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import time

from utils.dicts import getDictOrden

from utils.generarGraficos import generarGraficosDiversidad as plotDiversidad


#Credenciales
env = configparser.ConfigParser()
env.read('env.ini')
host = env['postgres']['host']
db_name = env['postgres']['db_name']
port = env['postgres']['port']
user = env['postgres']['user']
pwd = env['postgres']['pass']

#Conección
print("-"*100,f"Conectando a DB: {host}:{port}/{db_name}","-"*100)
try:
    engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}', connect_args={'connect_timeout': 10})
    engine.connect()
    metadata = db.MetaData()
    print('Conexion ok!')
except:
    print('No se conectó a la db')
    print("-"*100,"Falló todo :( ","-"*100)
    exit()
experimentos = ['WOA_SCP_SAR_C']

root = env['reports']['ROOT']
formatoGraficos = env['plots']['FORMATO']
init = env['reports']['INIT']

orden = getDictOrden()
generarGraficosDiversidad = True

path = root+env['reports']['LATEX']
#Generar gráficos de Diversidad
if generarGraficosDiversidad == True:
    inicio = time.time()
    for experimento in experimentos:
        
        exp = experimento.split('_')
        mh = '_'.join(exp[0:3])
        repair = exp[3]
        repair = repair.replace('C', 'Complex').replace('S', 'Simple')
        directory = path + mh

        # Crear directorio
        directory = f'{path}{mh}_{init}'
        try:
            os.makedirs(str(directory))
        except OSError:
            print("Ya existe el directorio %s " % directory)
        else:
            print("Se ha creado el directorio: %s " % directory)

        print(mh)
        print(repair)
        print(directory)

        plotDiversidad([mh],engine,metadata,orden,directory,formatoGraficos,init,repair)
    print(f"Se han generado de gráficos de Diversidad en: {time.time()-inicio}")
