
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

def generarResumenPorcentaje(nombreAlgoritmo,engine,metadata,orden,file):

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

    print(nombreAlgoritmo.replace("SCP","").replace("U_C","U-Complex-Rand").replace("U_S","U-Simple-Rand").replace("__","_").replace("_","-")+" Exploration-Exploitation Average")
    #Parte superior de la tabla
    file.write("\\begin{table}[H]")
    file.write("\\begin{center}")
    file.write(f'\\caption{{{nombreAlgoritmo.replace("SCP","").replace("U_C","U-Complex-Rand").replace("U_S","U-Simple-Rand")+" Exploration-Exploitation Average"}}}')
    file.write("\\resizebox{\\textwidth}{!}{")
    file.write("\\begin{tabular}{c|cc|cc|cc|cc|cc|cc|}")
    file.write("\\toprule")
    file.write("\\multicolumn{1}{c}{}")

    #for
    for k in range(len(medidasDiversidad)):
        file.write(f'& \\multicolumn{{2}}{{c}}{{{medidasDiversidad[k]}}}')

    file.write("\\\\")
    file.write("\\multicolumn{1}{c}{Inst.}")

    #for
    for k in range(len(medidasDiversidad)):
        file.write(" & \\multicolumn{1}{c}{XPL\%}  & \\multicolumn{1}{c}{XPLT\%}")


    file.write("\\\\")
    file.write("\\midrule")
    file.write(os.linesep)

    with engine.connect() as connection:
        for instancia in orden:
            estado = []
            facEvol = []
            linea = []
            
            instanciaStr = f"%{instancia}%"
            param = {"instancia":instanciaStr,"nomalg":nombreAlgoritmo}
            #print(instanciaStr)
            
            arrResult = connection.execute(text(sql),**param)
            i = 0
            maxDiversidades = None
            porcXpl = []
            porcXpt = []
            for result in arrResult:
                fila = json.loads(result[0])
                # print(f"fila['PorcentajeExplor']: {fila['PorcentajeExplor']}")
                # print(f"fila['PorcentajeExplor']: {list(fila['PorcentajeExplor'].replace('[','').replace(']','').split(' '))}")
                PorcExplor = list(fila['PorcentajeExplor'].replace("[","").replace("]","").split(" ")) #[0, , , ,1,2,3,4,5]
                PorcExplor = np.array([float(item) for item in PorcExplor if item != ""])                
                porcXpl.append(PorcExplor)
                porcXpt.append(100 - PorcExplor)
                
            porcXpl = np.array(porcXpl)
            porcXpt = np.array(porcXpt)

            # print(f'porcXpl: {porcXpl.shape}')
            # print(f'porcXpt: {porcXpt.shape}')


            linea.append(instancia.replace(".txt","").replace("scp","").replace("nr",""))
            linea.append(str(np.around(np.mean(porcXpl[:,0]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpt[:,0]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpl[:,1]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpt[:,1]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpl[:,2]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpt[:,2]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpl[:,3]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpt[:,3]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpl[:,4]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpt[:,4]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpl[:,5]),decimals=2)))
            linea.append(str(np.around(np.mean(porcXpt[:,5]),decimals=2)))
   
            file.write("&".join([str(item) for item in linea])+"\\\\")
    
    #Parte inferior de la tabla
    file.write(os.linesep)
    file.write("\\bottomrule")
    file.write("\\end{tabular}}")
    file.write("\\end{center}")
    file.write("\\end{table}")
    file.write(os.linesep)        