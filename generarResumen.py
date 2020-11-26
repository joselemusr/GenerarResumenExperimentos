#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 23:38:08 2019

@author: mauri
"""

import os
import numpy as np
import datetime as dt
import configparser
import sqlalchemy as db
from sqlalchemy.sql import text
import pandas as pd
def generarResumen(nombreAlgoritmoAComparar,CompararConOtros,engine,metadata,orden,file):
        directory = './'
        res = []
        instancias = []

        optimos = []
        diferencias = []
        mejores = []
        peores = []
        promedios = []
        std = []
        indices=[]
        ejecuciones = []

        #Nombre de Experimentos a comparar
        # nombreAlgoritmoAComparar = ['GWO_SCP_BCL1','SCA_SCP_BCL1','HHO_SCP_BCL1','WOA_SCP_BCL1',
        #     'GWO_SCP_MIR2','SCA_SCP_MIR2','HHO_SCP_MIR2','WOA_SCP_MIR2',
        #     'GWO_SCP_QL1','SCA_SCP_QL1','HHO_SCP_QL1','WOA_SCP_QL1',
        #     'GWO_SCP_QL2','SCA_SCP_QL2','HHO_SCP_QL2','WOA_SCP_QL2',
        #     'GWO_SCP_QL3','SCA_SCP_QL3','HHO_SCP_QL3','WOA_SCP_QL3']

        #nombreAlgoritmoAComparar = ['GWO_SCP_BCL1','GWO_SCP_MIR2','GWO_SCP_QL1','GWO_SCP_QL2','GWO_SCP_QL3']

        #nombreAlgoritmoAComparar = ['SCA_SCP_BCL1','SCA_SCP_MIR2','SCA_SCP_QL1','SCA_SCP_QL2','SCA_SCP_QL3']

        #nombreAlgoritmoAComparar = ['HHO_SCP_BCL1','HHO_SCP_MIR2','HHO_SCP_QL1','HHO_SCP_QL2','HHO_SCP_QL3']

        #nombreAlgoritmoAComparar = ['WOA_SCP_BCL1','WOA_SCP_MIR2','WOA_SCP_QL1','WOA_SCP_QL2','WOA_SCP_QL3']

        #CompararConOtros = False #Si es False no devuelve los resultados de la literatura

        # #Credenciales
        # config = configparser.ConfigParser()
        # config.read('db_config.ini')
        # host = config['postgres']['host']
        # db_name = config['postgres']['db_name']
        # port = config['postgres']['port']
        # user = config['postgres']['user']
        # pwd = config['postgres']['pass']

        # #Conección
        # engine = db.create_engine(f'postgresql://{user}:{pwd}@{host}:{port}/{db_name}')
        # metadata = db.MetaData()

        #Óptimo Instancias
        # orden = {
        #         'scp41.txt':[0,429]
        #         ,'scp51.txt':[1,253]
        #         ,'scp61.txt':[2,138]
        #         ,'scpa1.txt':[3,253]
        #         ,'scpb1.txt':[0,69]
        #         ,'scpc1.txt':[1,227]
        #         ,'scpd1.txt':[2,60]
        #         }
        # orden = {
        #         'scp41.txt':[0,429]
        #         ,'scp42.txt':[1,512]
        #         ,'scp43.txt':[2,516]
        #         ,'scp44.txt':[3,494]
        #         ,'scp45.txt':[0,512]
        #         ,'scp46.txt':[1,560]
        #         ,'scp47.txt':[2,430]
        #         ,'scp48.txt':[3,492]
        #         ,'scp49.txt':[0,641]
        #         ,'scp410.txt':[1,514]
        #         ,'scp51.txt':[2,253]
        #         ,'scp52.txt':[3,302]
        #         ,'scp53.txt':[0,226]
        #         ,'scp54.txt':[1,242]
        #         ,'scp55.txt':[2,211]
        #         ,'scp56.txt':[3,213]
        #         ,'scp57.txt':[0,293]
        #         ,'scp58.txt':[1,288]
        #         ,'scp59.txt':[2,279]
        #         ,'scp510.txt':[3,265]
        #         ,'scp61.txt':[0,138]
        #         ,'scp62.txt':[1,146]
        #         ,'scp63.txt':[2,145]
        #         ,'scp64.txt':[3,131]
        #         ,'scp65.txt':[0,161]
        #         ,'scpa1.txt':[1,253]
        #         ,'scpa2.txt':[2,252]
        #         ,'scpa3.txt':[3,232]
        #         ,'scpa4.txt':[0,234]
        #         ,'scpa5.txt':[1,236]
        #         ,'scpb1.txt':[2,69]
        #         ,'scpb2.txt':[3,76]
        #         ,'scpb3.txt':[0,80]
        #         ,'scpb4.txt':[1,79]
        #         ,'scpb5.txt':[2,72]
        #         ,'scpc1.txt':[3,227]
        #         ,'scpc2.txt':[0,219]
        #         ,'scpc3.txt':[1,243]
        #         ,'scpc4.txt':[2,219]
        #         ,'scpc5.txt':[3,215]
        #         ,'scpd1.txt':[0,60]
        #         ,'scpd2.txt':[1,66]
        #         ,'scpd3.txt':[2,72]
        #         ,'scpd4.txt':[3,62]
        #         ,'scpd5.txt':[0,61]
        #         ,'scpnre1.txt':[1,29]
        #         ,'scpnre2.txt':[2,30]
        #         ,'scpnre3.txt':[3,27]
        #         ,'scpnre4.txt':[0,28]
        #         ,'scpnre5.txt':[1,28]
        #         ,'scpnrf1.txt':[2,14]
        #         ,'scpnrf2.txt':[3,15]
        #         ,'scpnrf3.txt':[0,14]
        #         ,'scpnrf4.txt':[1,14]
        #         ,'scpnrf5.txt':[2,13]
        #         ,'scpnrg1.txt':[3,176]
        #         ,'scpnrg2.txt':[0,154]
        #         ,'scpnrg3.txt':[1,166]
        #         ,'scpnrg4.txt':[2,168]
        #         ,'scpnrg5.txt':[3,168]
        #         ,'scpnrh1.txt':[0,63]
        #         ,'scpnrh2.txt':[1,63]
        #         ,'scpnrh3.txt':[2,59]
        #         ,'scpnrh4.txt':[3,58]
        #         ,'scpnrh5.txt':[0,55]

        #         }

        #Resultados de la literatura
        babc = [
                [430,430.5],
                [512,512],
                [516,516],
                [494,494],
                [512,512],
                [561,561.7],
                [430,430],
                [493,494],
                [643,645.5],
                [514,514],
                [254,255],
                [309,310.2],
                [228,228.5],
                [242,242],
                [211,211],
                [213,213],
                [296,296],
                [288,288],
                [280,280],
                [266,267],
                [140,140.5],
                [146,146],
                [145,145],
                [131,131],
                [161,161],
                [254,254],
                [254,254],
                [234,234],
                [234,234],
                [237,238.6],
                [69,69],
                [76,76],
                [80,80],
                [79,79],
                [72,72],
                [230,231],
                [219,219],
                [244,244.5],
                [220,224],
                [215,215],
                [60,60],
                [67,67],
                [73,73],
                [63,63],
                [62,62],
                [29,29],
                [30,30],
                [27,27],
                [28,28],
                [28,28],
                [14,14],
                [15,15],
                [14,14],
                [14,14],
                [13,13],
                [176,176],
                [154,154],
                [166,166],
                [168,168],
                [168,168],
                [63,63],
                [63,63],
                [59,59],
                [58,58],
                [55,55]
        ]        

        bcso = [
                [459,479.6],
                [570,594.2],
                [590,606.8],
                [547,578.3],
                [545,554.2],
                [637,649.9],
                [462,467.4],
                [546,566.9],
                [711,725.0],
                [537,552.1],
                [279,281.6],
                [339,339.9],
                [247,250.5],
                [251,253.2],
                [230,230.4],
                [232,242.7],
                [332,338.0],
                [320,329.9],
                [295,298.6],
                [285,286.9],
                [151,159.9],
                [152,157.4],
                [160,164.3],
                [138,141.7],
                [169,172.8],
                [286,286.9],
                [274,276.3],
                [257,263.1],
                [248,251.3],
                [244,244],
                [79,79],
                [86,88.5],
                [85,85.4],
                [89,89],
                [73,73],
                [242,242.4],
                [240,240.8],
                [277,278],
                [250,250],
                [243,244.3],
                [65,65.7],
                [70,70.1],
                [79,80.8],
                [64,66.6],
                [65,65.6],
                [29,44103],
                [34,34.2],
                [31,43982],
                [32,32.9],
                [30,43920],
                [17,43847],
                [18,43879],
                [17,43878],
                [17,43847],
                [15,44089],
                [190,192.7],
                [165,166],
                [187,187.7],
                [179,183.2],
                [181,184.3],
                [70,71.2],
                [67,67],
                [68,69.6],
                [66,66.6],
                [61,61.5]
        ]

        bfo = [
                [481,481.03],
                [580,580.00],
                [619,619.03],
                [537,537.00],
                [609,609.00],
                [653,653.00],
                [491,491.07],
                [565,565.00],
                [749,749.03],
                [550,550.00],
                [296,296.03],
                [372,372.00],
                [250,250.00],
                [277,277.07],
                [253,253.00],
                [264,264.03],
                [337,337.00],
                [326,326.00],
                [350,350.00],
                [321,321.00],
                [173,173.03],
                [180,180.07],
                [160,160.00],
                [161,161.00],
                [186,186.00],
                [285,285.00],
                [285,285.07],
                [272,272.00],
                [297,297.00],
                [262,262.00],
                [80,80.03],
                [92,92.00],
                [93,93.00],
                [98,98.03],
                [87,87.00],
                [279,279.00],
                [272,272.00],
                [288,288.00],
                [262,262.00],
                [262,262.07],
                [71,71.00],
                [75,75.00],
                [88,88.00],
                [71,71.00],
                [71,71.00],
                [32,32.03],
                [36,36.00],
                [35,35.00],
                [34,34.00],
                [34,34.00],
                [17,43907],
                [17,17.00],
                [21,21.00],
                [19,19.00],
                [16,16.00],
                [230,230.03],
                [191,191.00],
                [198,198.00],
                [214,214.00],
                [223,223.00],
                [85,85.07],
                [81,81.03],
                [76,76.00],
                [75,75.00],
                [68,68.00]
        ]

        bfla = [
                [430,430],
                [516,518],
                [520,520],
                [501,504],
                [514,514],
                [563,563],
                [431,432],
                [497,499],
                [656,656],
                [518,519],
                [254,255],
                [307,307],
                [228,230],
                [242,242],
                [211,213],
                [213,214],
                [297,299],
                [291,293],
                [281,283],
                [265,266],
                [140,141],
                [147,147],
                [147,148],
                [131,133],
                [166,169],
                [255,258],
                [260,260],
                [237,239],
                [235,238],
                [236,239],
                [70,70],
                [76,77],
                [80,80],
                [79,80],
                [72,73],
                [229,231],
                [223,225],
                [253,253],
                [227,228],
                [217,218],
                [60,62],
                [67,68],
                [75,77],
                [63,65],
                [63,66],
                [29,29],
                [31,32],
                [28,28],
                [29,30],
                [28,31],
                [15,15],
                [15,15],
                [16,17],
                [15,16],
                [15,17],
                [182,183],
                [161,161],
                [173,174],
                [173,177],
                [174,174],
                [68,69],
                [66,66],
                [62,63],
                [63,64],
                [59,61]
        ]

        bela = [
                [447,448],
                [559,568],
                [537,543],
                [527,528],
                [527,530],
                [607,607],
                [448,448],
                [509,509],
                [682,684],
                [571,573],
                [280,281],
                [318,319],
                [242,242],
                [251,251],
                [225,225],
                [247,248],
                [316,316],
                [315,316],
                [314,315],
                [280,282],
                [152,152],
                [160,160],
                [160,160],
                [140,140],
                [184,184],
                [261,262],
                [279,279],
                [252,253],
                [250,251],
                [241,241],
                [86,87],
                [88,89],
                [85,85],
                [84,85],
                [78,79],
                [237,237],
                [237,237],
                [271,272],
                [246,247],
                [224,224],
                [62,63],
                [73,74],
                [79,80],
                [67,67],
                [66,66],
                [30,31],
                [35,35],
                [34,34],
                [33,34],
                [30,31],
                [17,17],
                [18,19],
                [17,18],
                [17,17],
                [16,16],
                [194,194],
                [176,176],
                [184,185],
                [196,196],
                [198,198],
                [70,70],
                [71,71],
                [68,69],
                [70,71],
                [69,70]
        ]


        #Consulta SQL
        sql = """select 
                min(resultado_ejecucion.fitness ),
                avg(resultado_ejecucion.fitness )
                from
                resultado_ejecucion
                inner join datos_ejecucion on datos_ejecucion.id = resultado_ejecucion.id_ejecucion
                where datos_ejecucion.parametros ILIKE :instancia
                and nombre_algoritmo = :nomalg
                group by datos_ejecucion.parametros"""

        #Solicitar datos desde la Base de Datos
        res = []
        i=0
        Sumatorias = []












        #Parte superior de la tabla
        file.write("\\begin{table}[]")
        file.write(os.linesep)
        file.write(f'\\centering \\caption{{{nombreAlgoritmoAComparar[0].replace("_SCP_BCL1_CPU_S","-repair-Simple").replace("_SCP_BCL1_CPU_C","-repair-Complex")}}}')
        file.write("\\resizebox{\\textwidth}{!}{")
        file.write("\\begin{tabular}{@{}ll|lll|lll|lll|lll|lll|lll|lll@{}}")
        file.write("\\toprule")
        file.write("\\multicolumn{1}{c}{}  & \\multicolumn{1}{c}{}")
        file.write(os.linesep)

        #for
        for j in range(len(nombreAlgoritmoAComparar)):
            file.write(f'& \\multicolumn{{3}}{{c}}{{{nombreAlgoritmoAComparar[j].replace("GWO_SCP_","").replace("SCA_SCP_","").replace("HHO_SCP_","").replace("WOA_SCP_","").replace("_","-")}}}')

        file.write("\\\\")
        file.write("\\multicolumn{1}{c}{Inst.}  & \\multicolumn{1}{c}{Opt.}")

        #for
        for j in range(len(nombreAlgoritmoAComparar)):
            file.write("& \\multicolumn{1}{c}{Best}  & \\multicolumn{1}{c}{Avg}  & \\multicolumn{1}{c}{RPD}")

        file.write(os.linesep)
        file.write("\\\\")
        file.write("\\midrule")

        with engine.connect() as connection:
                for instancia in orden:
                        CandDatos = 0
                        linea = []
                        linea.append(instancia.replace(".txt","").replace("scp","").replace("nr",""))
                        linea.append(orden[instancia][1])
                        instanciaStr = f"%{instancia}%"
                        
                        for nombreAlgoritmo in nombreAlgoritmoAComparar:
                                param = {"instancia":instanciaStr,"nomalg":nombreAlgoritmo}
                                arrResult = connection.execute(text(sql),**param)
                                
                                for result in arrResult:
                                        if int(result[0]) is None:
                                                linea.append(0.0) #Best
                                                linea.append(0.0) #avg
                                                linea.append(0.0) #RPD
                                        else:
                                                linea.append(int(result[0])) #Best
                                                linea.append(round(result[1],2)) #avg
                                                linea.append(round((result[0]-orden[instancia][1])*100/orden[instancia][1],2)) #RPD
                        

                                                
                                        #***Condición para completar con Blancos si no hay
                                        CandDatos = CandDatos +3
                        if CompararConOtros == True:
                                #BCSO
                                linea.append(bcso[i][0]) #Best
                                linea.append(bcso[i][1]) #avg
                                linea.append(round((bcso[i][0]-orden[instancia][1])*100/orden[instancia][1],2)) #RPD
                                CandDatos = CandDatos +3
                                #BFO
                                linea.append(bfo[i][0]) #Best
                                linea.append(bfo[i][1]) #avg
                                linea.append(round((bfo[i][0]-orden[instancia][1])*100/orden[instancia][1],2)) #RPD
                                CandDatos = CandDatos +3
                                #BFLA
                                linea.append(bfla[i][0]) #Best
                                linea.append(bfla[i][1]) #avg
                                linea.append(round((bfla[i][0]-orden[instancia][1])*100/orden[instancia][1],2)) #RPD
                                CandDatos = CandDatos +3
                                #BELA
                                linea.append(bela[i][0]) #Best
                                linea.append(bela[i][1]) #avg
                                linea.append(round((bela[i][0]-orden[instancia][1])*100/orden[instancia][1],2)) #RPD
                                CandDatos = CandDatos +3
                                #BABC
                                linea.append(babc[i][0]) #Best
                                linea.append(babc[i][1]) #avg
                                linea.append(round((babc[i][0]-orden[instancia][1])*100/orden[instancia][1],2)) #RPD
                                CandDatos = CandDatos +3

                        #Condición para guardar solamente las instancias con resultados
                        #if (CandDatos != 15) or (CandDatos != 0):
                        Sumatorias.append(linea)
                        file.write("&".join([str(item) for item in linea])+"\\\\")
                        res.append(linea) 
                        i+=1
                for i in range(len(Sumatorias)):
                        aux = Sumatorias[i]
                        aux[0] = 0
                        aux[1] = 0
                        Sumatorias[i] = aux
                Sumatorias = np.array(Sumatorias)
                lineaSum = []
                lineaSum.append(np.round(np.mean(Sumatorias,axis=0),decimals=2))
                lineaAux = lineaSum[0].tolist()
                
                aux2 = "&".join([str(item) for item in lineaAux])+"\\\\"
                file.write("\\hline")
                file.write(aux2.replace('0.0', ''))

        #Parte inferior de la tabla
        file.write(os.linesep)
        file.write("\\bottomrule")
        file.write("\\end{tabular}  }")
        file.write("\\end{table}")

        file.write(os.linesep)
        file.write(os.linesep)        
