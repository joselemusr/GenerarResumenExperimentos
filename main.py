import os
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import time

import generarResumen as gr
import graficoConvergencia as gc
import generarTex as gt
import graficosDiversidad as gd
import graficosExplorVsExplot as gee
import generarResumenPorcentajeExplorExplot as gtee
#import generarGraficoAcciones as ga
import graficoViolinesFitness as gvf

#Credenciales
config = configparser.ConfigParser()
config.read('db_config.ini')
host = config['postgres']['host']
db_name = config['postgres']['db_name']
port = config['postgres']['port']
user = config['postgres']['user']
pwd = config['postgres']['pass']

#Conección
engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
metadata = db.MetaData()

# orden = {
#                 'scp41.txt':[0,429]
#                 ,'scp51.txt':[1,253]
#                 ,'scp61.txt':[2,138]
#                 ,'scpa1.txt':[3,253]
#                 ,'scpb1.txt':[0,69]
#                 ,'scpc1.txt':[1,227]
#                 ,'scpd1.txt':[2,60]
#                 }
orden = {
        'scp41.txt':[0,429]
        ,'scp42.txt':[1,512]
        ,'scp43.txt':[2,516]
        ,'scp44.txt':[3,494]
        ,'scp45.txt':[0,512]
        ,'scp46.txt':[1,560]
        ,'scp47.txt':[2,430]
        ,'scp48.txt':[3,492]
        ,'scp49.txt':[0,641]
        ,'scp410.txt':[1,514]
        ,'scp51.txt':[2,253]
        ,'scp52.txt':[3,302]
        ,'scp53.txt':[0,226]
        ,'scp54.txt':[1,242]
        ,'scp55.txt':[2,211]
        ,'scp56.txt':[3,213]
        ,'scp57.txt':[0,293]
        ,'scp58.txt':[1,288]
        ,'scp59.txt':[2,279]
        ,'scp510.txt':[3,265]
        ,'scp61.txt':[0,138]
        ,'scp62.txt':[1,146]
        ,'scp63.txt':[2,145]
        ,'scp64.txt':[3,131]
        ,'scp65.txt':[0,161]
        ,'scpa1.txt':[1,253]
        ,'scpa2.txt':[2,252]
        ,'scpa3.txt':[3,232]
        ,'scpa4.txt':[0,234]
        ,'scpa5.txt':[1,236]
        ,'scpb1.txt':[2,69]
        ,'scpb2.txt':[3,76]
        ,'scpb3.txt':[0,80]
        ,'scpb4.txt':[1,79]
        ,'scpb5.txt':[2,72]
        ,'scpc1.txt':[3,227]
        ,'scpc2.txt':[0,219]
        ,'scpc3.txt':[1,243]
        ,'scpc4.txt':[2,219]
        ,'scpc5.txt':[3,215]
        ,'scpd1.txt':[0,60]
        ,'scpd2.txt':[1,66]
        ,'scpd3.txt':[2,72]
        ,'scpd4.txt':[3,62]
        ,'scpd5.txt':[0,61]
        }

# instancias = ["mscp41.txt"
#                 ,"mscp51.txt"
#                 ,"mscp61.txt"
#                 ,"mscpa1.txt"
#                 ,"mscpb1.txt"
#                 ,"mscpc1.txt"
#                 ,"mscpd1.txt"
#                 ]
instancias = [
			"mscp41.txt"
			,"mscp42.txt"
			,"mscp43.txt"
			,"mscp44.txt"
			,"mscp45.txt"
			,"mscp46.txt"
			,"mscp47.txt"
			,"mscp48.txt"
			,"mscp49.txt"
			,"mscp410.txt"
			,"mscp51.txt"
			,"mscp52.txt"
			,"mscp53.txt"
			,"mscp54.txt"
			,"mscp55.txt"
			,"mscp56.txt"
			,"mscp57.txt"
			,"mscp58.txt"
			,"mscp59.txt"
			,"mscp510.txt"
			,"mscp61.txt"
			,"mscp62.txt"
			,"mscp63.txt"
			,"mscp64.txt"
			,"mscp65.txt"
			,"mscpa1.txt"
			,"mscpa2.txt"
			,"mscpa3.txt"
			,"mscpa4.txt"
			,"mscpa5.txt"
			,"mscpb1.txt"
			,"mscpb2.txt"
			,"mscpb3.txt"
			,"mscpb4.txt"
			,"mscpb5.txt"
			,"mscpc1.txt"
			,"mscpc2.txt"
			,"mscpc3.txt"
			,"mscpc4.txt"
			,"mscpc5.txt"
			,"mscpd1.txt"
			,"mscpd2.txt"
			,"mscpd3.txt"
			,"mscpd4.txt"
			,"mscpd5.txt"
                ]



# tablasResumen = [
# ,['GWO_SCP_BCL1','GWO_SCP_MIR2','GWO_SCP_QL1','GWO_SCP_QL2','GWO_SCP_QL3']
# ,['SCA_SCP_BCL1','SCA_SCP_MIR2','SCA_SCP_QL1','SCA_SCP_QL2','SCA_SCP_QL3']
# ,['HHO_SCP_BCL1','HHO_SCP_MIR2','HHO_SCP_QL1','HHO_SCP_QL2','HHO_SCP_QL3']
# ,['WOA_SCP_BCL1','WOA_SCP_MIR2','WOA_SCP_QL1','WOA_SCP_QL2','WOA_SCP_QL3']
# ]
experimentos = [
#['GWO_SCP_BCL1_CPU_S','GWO_SCP_MIR2_CPU_S','GWO_SCP_QL1_CPU_S','GWO_SCP_QL2_CPU_S','GWO_SCP_QL3_CPU_S','GWO_SCP_QL4_CPU_S','GWO_SCP_QL5_CPU_S']
['GWO_SCP_BCL1_CPU_C','GWO_SCP_MIR2_CPU_C','GWO_SCP_QL1_CPU_C','GWO_SCP_QL2_CPU_C','GWO_SCP_QL3_CPU_C','GWO_SCP_QL4_CPU_C','GWO_SCP_QL5_CPU_C']
#,['SCA_SCP_BCL1_CPU_S','SCA_SCP_MIR2_CPU_S','SCA_SCP_QL1_CPU_S','SCA_SCP_QL2_CPU_S','SCA_SCP_QL3_CPU_S','SCA_SCP_QL4_CPU_S','SCA_SCP_QL5_CPU_S'] 
,['SCA_SCP_BCL1_CPU_C','SCA_SCP_MIR2_CPU_C','SCA_SCP_QL1_CPU_C','SCA_SCP_QL2_CPU_C','SCA_SCP_QL3_CPU_C','SCA_SCP_QL4_CPU_C','SCA_SCP_QL5_CPU_C']
#,['HHO_SCP_BCL1_CPU_S','HHO_SCP_MIR2_CPU_S','HHO_SCP_QL1_CPU_S','HHO_SCP_QL2_CPU_S','HHO_SCP_QL3_CPU_S','HHO_SCP_QL4_CPU_S','HHO_SCP_QL5_CPU_S'] 
,['HHO_SCP_BCL1_CPU_C','HHO_SCP_MIR2_CPU_C','HHO_SCP_QL1_CPU_C','HHO_SCP_QL2_CPU_C','HHO_SCP_QL3_CPU_C','HHO_SCP_QL4_CPU_C','HHO_SCP_QL5_CPU_C']
#,['WOA_SCP_BCL1_CPU_S','WOA_SCP_MIR2_CPU_S','WOA_SCP_QL1_CPU_S','WOA_SCP_QL2_CPU_S','WOA_SCP_QL3_CPU_S','WOA_SCP_QL4_CPU_S','WOA_SCP_QL5_CPU_S']
,['WOA_SCP_BCL1_CPU_C','WOA_SCP_MIR2_CPU_C','WOA_SCP_QL1_CPU_C','WOA_SCP_QL2_CPU_C','WOA_SCP_QL3_CPU_C','WOA_SCP_QL4_CPU_C','WOA_SCP_QL5_CPU_C']
]

experimentos = [
['SCA_SCP_BCL1_CPU_C','SCA_SCP_MIR2_CPU_C','SCA_SCP_QL1_CPU_C','SCA_SCP_QL2_CPU_C','SCA_SCP_QL3_CPU_C','SCA_SCP_QL4_CPU_C','SCA_SCP_QL5_CPU_C']
#,['WOA_SCP_BCL1_CPU_S','WOA_SCP_MIR2_CPU_S','WOA_SCP_QL1_CPU_S','WOA_SCP_QL2_CPU_S','WOA_SCP_QL3_CPU_S','WOA_SCP_QL4_CPU_S','WOA_SCP_QL5_CPU_S']
,['GWO_SCP_BCL1_CPU_C','GWO_SCP_MIR2_CPU_C','GWO_SCP_QL1_CPU_C','GWO_SCP_QL2_CPU_C','GWO_SCP_QL3_CPU_C','GWO_SCP_QL4_CPU_C','GWO_SCP_QL5_CPU_C']
]

experimentos3 = [
['GWO_SCP_BCL1_CPU_S','GWO_SCP_MIR2_CPU_S','GWO_SCP_QL1_CPU_S']
,['GWO_SCP_BCL1_CPU_C','GWO_SCP_MIR2_CPU_C','GWO_SCP_QL1_CPU_C']
,['SCA_SCP_BCL1_CPU_S','SCA_SCP_MIR2_CPU_S','SCA_SCP_QL1_CPU_S'] 
,['SCA_SCP_BCL1_CPU_C','SCA_SCP_MIR2_CPU_C','SCA_SCP_QL1_CPU_C']
,['HHO_SCP_BCL1_CPU_S','HHO_SCP_MIR2_CPU_S','HHO_SCP_QL1_CPU_S']
,['HHO_SCP_BCL1_CPU_C','HHO_SCP_MIR2_CPU_C','HHO_SCP_QL1_CPU_C']
,['WOA_SCP_BCL1_CPU_S','WOA_SCP_MIR2_CPU_S','WOA_SCP_QL1_CPU_S']
,['WOA_SCP_BCL1_CPU_C','WOA_SCP_MIR2_CPU_C','WOA_SCP_QL1_CPU_C']
]

#experimentos =[['WOA_SCP_BCL1_CPU_C','WOA_SCP_MIR2_CPU_C','WOA_SCP_QL1_CPU_C','WOA_SCP_QL2_CPU_C','WOA_SCP_QL3_CPU_C','WOA_SCP_QL4_CPU_C','WOA_SCP_QL5_CPU_C']]
#experimentos =[['WOA_SCP_BCL1_CPU_C','WOA_SCP_QL1_CPU_C']]

#Condicionales Generales
path = "Latex/"
Init = "Rand" #"Zeros"


#Para Generar Tablas resumen
generarTablasResumen = False
directoryTablasResumen = "archivoTablaResumen.txt"
CompararConOtros = False

#Para Generar Gráficos de Convergencia
generarGraficosConvergencia = False
formatoGraficos = "pdf"

#Para generar Tex con gráficos de Convergencia
generarTex = False
directoryTex = "archivoGeneradoTex.txt"
escaleColumnWidth = 0.45
NombresAlgoritmo = ["HHO-Repair-Complex-Init-Zeros","SCA-Repair-Complex-Init-Zeros","WOA-Repair-Complex-Init-Zeros","GWO-Repair-Complex-Init-Zeros","SCA-Repair-Complex-Init-Rand","HHO-Repair-Complex-Init-Rand","WOA-Repair-Complex-Init-Rand","GWO-Repair-Complex-Init-Rand","HHO-Repair-Simple-Init-Zeros","SCA-Repair-Simple-Init-Zeros","WOA-Repair-Simple-Init-Zeros","GWO-Repair-Simple-Init-Zeros","SCA-Repair-Simple-Init-Rand","HHO-Repair-Simple-Init-Rand","WOA-Repair-Simple-Init-Rand","GWO-Repair-Simple-Init-Rand"]
#NombresAlgoritmo = ["GWO-Repair-Simple-Init-Zeros"]
instancias = ['4.1','5.1','6.1','a.1','b.1','c.1','d.1']
#instancias = ['4.1','5.1']

#Para generar Gráficos de Explor vs Explot
generarGraficosExplorVsExplot = False

#Para generar Gráficos de Diversidad
generarGraficosDiversidad = False

#Para generar tabla Explor vs Explot
generarTablaExplorExplot = False
directoryTablasExplorExplot = "archivoTablaExplorExplot.txt"

#Para generar Grafico de acciones seleccionadas tanto en exploracion con en explotacion
generarGraficoAcciones = False
promedioacciones = False

# graficos de violines, posee dos etapas: generacion de data con un archivo csv, generacion de grafico violin a partir de dicha data csv
generarDataGraficos = True
generarGraficosViolin = True
generarGraficosBoxPlot = True


# Generar Tablas resumen
if generarTablasResumen == True:
    inicio = time.time()
    file = open(directoryTablasResumen, "w")
    for i in range(len(experimentos)):
        gr.generarResumen(experimentos[i],CompararConOtros,engine,metadata,orden,file)
    file.close()
    print(f"Se han generado las tablas de Resumen en: {time.time()-inicio}")

#Generar gráficos de Convergencia
if generarGraficosConvergencia == True:
    inicio = time.time()
    for i in range(len(experimentos)):
        MH = experimentos[i][0].replace('_SCP_BCL1_CPU_C','').replace('_SCP_BCL1_CPU_S','')
        repair = experimentos[i][0].replace('GWO_SCP_BCL1_CPU_','').replace('SCA_SCP_BCL1_CPU_','').replace('HHO_SCP_BCL1_CPU_','').replace('WOA_SCP_BCL1_CPU_','')
        repair = repair.replace('C', 'Complex').replace('S', 'Simple')
        for j in range(len(experimentos[i])):
            #Crear directorio
            directory = path + MH + "/" + Init
            try:
                os.makedirs(str(directory))
            except OSError:
                print("Ya existe el directorio %s " % directory)
            else:
                print("Se ha creado el directorio: %s " % directory)
            gc.generarGraficosConvergencia(experimentos[i][j],engine,metadata,instancias,orden,directory,formatoGraficos,repair,Init)
    print(f"Se han generado los gráficos de Convergencia en: {time.time()-inicio}")

#Generar gráficos de exploración y explotación
if generarGraficosExplorVsExplot == True:
    inicio = time.time()
    for i in range(len(experimentos)):
        MH = experimentos[i][0].replace('_SCP_BCL1_CPU_C','').replace('_SCP_BCL1_CPU_S','')
        repair = experimentos[i][0].replace('GWO_SCP_BCL1_CPU_','').replace('SCA_SCP_BCL1_CPU_','').replace('HHO_SCP_BCL1_CPU_','').replace('WOA_SCP_BCL1_CPU_','')
        repair = repair.replace('C', 'Complex').replace('S', 'Simple')
        for j in range(len(experimentos[i])):
            #Crear directorio
            directory = path + MH + "/" + Init
            try:
                os.makedirs(str(directory))
            except OSError:
                print("Ya existe el directorio %s " % directory)
            else:
                print("Se ha creado el directorio: %s " % directory)

            gee.generarGraficosEve(experimentos[i][j],engine,metadata,orden,directory,formatoGraficos,Init,repair)
    print(f"Se han generado de gráficos de exploración y explotación en: {time.time()-inicio}")

#Generar gráficos de Diversidad
if generarGraficosDiversidad == True:
    inicio = time.time()
    for i in range(len(experimentos)):
        MH = experimentos[i][0].replace('_SCP_BCL1_CPU_C','').replace('_SCP_BCL1_CPU_S','')
        repair = experimentos[i][0].replace('GWO_SCP_BCL1_CPU_','').replace('SCA_SCP_BCL1_CPU_','').replace('HHO_SCP_BCL1_CPU_','').replace('WOA_SCP_BCL1_CPU_','')
        repair = repair.replace('C', 'Complex').replace('S', 'Simple')
        directory = path + experimentos[i][0].replace('_BCL1_CPU_C','-Diversidad').replace('_BCL1_CPU_S','-Diversidad').replace('_','-')

        #Crear directorio
        directory = path + MH + "/" + Init
        try:
            os.makedirs(str(directory))
        except OSError:
            print("Ya existe el directorio %s " % directory)
        else:
            print("Se ha creado el directorio: %s " % directory)


        gd.generarGraficosDiversidad(experimentos[i],engine,metadata,orden,directory,formatoGraficos,Init,repair)
    print(f"Se han generado de gráficos de Diversidad en: {time.time()-inicio}")

#Generar tex
if generarTex == True:
    inicio = time.time()
    file = open(directoryTex, "w")
    gt.generarTex(file,NombresAlgoritmo,instancias,escaleColumnWidth,path)
    file.close()
    print(f".txt generado en: {time.time()-inicio}")

#GenerarTablaExplorExplot
if generarTablaExplorExplot == True:
    inicio = time.time()
    file = open(directoryTablasExplorExplot, "w")
    for i in range(len(experimentos)):
        for j in range(len(experimentos[i])):
            gtee.generarResumenPorcentaje(experimentos[i][j],engine,metadata,orden,file)
    file.close()

# if generarGraficoAcciones == True:
#     for i in range(len(experimentos)):
#         for j in range(len(experimentos[i])):
#             directory = path + MH + "/" + Init
#             directory = experimentos[i][j].replace('_','-')
#             try:
#                 os.mkdir(str(directory))
#             except OSError:
#                 print("Ya existe el directorio %s " % directory)
#             else:
#                 print("Se ha creado el directorio: %s " % directory)
#             ga.generarGraficoAcciones(experimentos[i][j],engine,metadata,orden,directory,promedioacciones)
            
if generarDataGraficos == True:
    for i in range(len(experimentos)):
        MH = experimentos[i][0].split("_")[0]
        repair = experimentos[i][0].split("_")[4].replace('C','Complex').replace('S','Simple')
        binaryType = experimentos[i][0].split("_")[2]
        directory = path + MH + "/" + Init + "/"
        
        try:
            os.makedirs(str(directory))
        except OSError:
            print("Ya existe el directorio %s " % directory)
        else:
            print("Se ha creado el directorio: %s " % directory)

        gvf.generarDataGraficos(experimentos[i],engine,metadata,orden,directory,MH,repair,Init)
        
if generarGraficosViolin == True:
    for i in range(len(experimentos)):

        MH = experimentos[i][0].split("_")[0]
        repair = experimentos[i][0].split("_")[4].replace('C','Complex').replace('S','Simple')
        binaryType = experimentos[i][0].split("_")[2]
        directory = path + MH + "/" + Init + "/"
        
        gvf.generarGraficoViolin(directory,MH,orden,repair,Init)
        
# if generarGraficosBoxPlot == True:
#     for i in range(len(experimentos)):
#         MH = experimentos[i][0].replace('_SCP_BCL1_CPU_C','').replace('_SCP_BCL1_CPU_S','')
#         directory = path + MH + "/" + Init
#         directory = "Graficos_Violin"+"/"+experimentos[i][0].split("_")[0]+"-"+experimentos[i][0].split("_")[4]
        
#         tipo="boxplot"
#         gvf.generarGraficoBoxPlot(directory,experimentos[i][0].split("_")[0],orden,tipo)
        

