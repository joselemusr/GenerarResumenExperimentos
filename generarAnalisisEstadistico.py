# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 18:04:53 2020

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
import json
import requests

import zlib
import pickle
import time
import scipy


def generarAnalisisEstadistico(directory,orden,instancia,experimento):
    
    
    Path = "Data/"
    nombre_archivo = "dg-Rand-"+experimento+"-SCP-CPU-Complex-"
    documento = []
    for algoritmo in instancia:
        documento.append(Path+directory+experimento+"-"+algoritmo+".txt")

    
    archivoBCL1 = open(documento[0],'w')
#    archivoMIR2 = open(documento[1],'w')
    archivoQL1 = open(documento[2],'w')
    archivoQL2 = open(documento[3],'w')
    archivoQL3 = open(documento[4],'w')
    archivoQL4 = open(documento[5],'w')
    archivoQL5 = open(documento[6],'w')
    
    archivoBCL1.write("\\begin{tabular}{c|ccccccc}")
    archivoBCL1.write("\\toprule")
    archivoBCL1.write(" & \\multicolumn{5}{c|}{"+experimento+"-BCL1 p-value}\\\\\n")
    archivoBCL1.write("Inst. & QL1 & QL2 & QL3 & QL4 & QL5 \\\\\\hline\\midrule\n")
    
    # archivoMIR2.write("\\begin{tabular}{c|ccccccc}")
    # archivoMIR2.write("\\toprule")
    # archivoMIR2.write(" & \\multicolumn{6}{c|}{"+experimento+"-MIR2 p-value}\\\\\n")
    # archivoMIR2.write("Inst. & BCL1 & QL1 & QL2 & QL3 & QL4 & QL5 \\\\\\hline\\midrule\n")
    
    archivoQL1.write("\\begin{tabular}{c|ccccccc}")
    archivoQL1.write("\\toprule")
    archivoQL1.write(" & \\multicolumn{5}{c|}{"+experimento+"-QL1 p-value}\\\\\n")
    archivoQL1.write("Inst. & BL1 & QL2 & QL3 & QL4 & QL5 \\\\\\hline\\midrule\n")
    
    archivoQL2.write("\\begin{tabular}{c|ccccccc}")
    archivoQL2.write("\\toprule")
    archivoQL2.write(" & \\multicolumn{5}{c|}{"+experimento+"-QL2 p-value}\\\\\n")
    archivoQL2.write("Inst. & BCL1 & QL1 & QL3 & QL4 & QL5 \\\\\\hline\\midrule\n")
    
    archivoQL3.write("\\begin{tabular}{c|ccccccc}")
    archivoQL3.write("\\toprule")
    archivoQL3.write(" & \\multicolumn{5}{c|}{"+experimento+"-QL3 p-value}\\\\\n")
    archivoQL3.write("Inst. & BCL1 & QL1 & QL2 & QL4 & QL5 \\\\\\hline\\midrule\n")
    
    archivoQL4.write("\\begin{tabular}{c|ccccccc}")
    archivoQL4.write("\\toprule")
    archivoQL4.write(" & \\multicolumn{5}{c|}{"+experimento+"-QL4 p-value}\\\\\n")
    archivoQL4.write("Inst. & BCL1 & QL1 & QL2 & QL3 & QL5 \\\\\\hline\\midrule\n")
    
    archivoQL5.write("\\begin{tabular}{c|ccccccc}")
    archivoQL5.write("\\toprule")
    archivoQL5.write(" & \\multicolumn{5}{c|}{"+experimento+"-QL5 p-value}\\\\\n")
    archivoQL5.write("Inst. & BCL1 & QL1 & QL2 & QL3 & QL4 \\\\\\hline\\midrule\n")
    
    
    
    for instance in orden:
        BCL1 = []
        # MIR2 = []
        QL1 = []
        QL2 = []
        QL3 = []
        QL4 = []
        QL5 = []
        dataBCL1 = []
        outlierBCL1 = []
        # dataMIR2 = []
        # outlierMIR2 = []
        dataQL1 = []
        outlierQL1 = []
        dataQL2 = []
        outlierQL2 = []
        dataQL3 = []
        outlierQL3 = []
        dataQL4 = []
        outlierQL4 = []
        dataQL5 = []
        outlierQL5 = []
        
        file_name = Path + nombre_archivo + instance.split(".")[0]+".csv"
        
        fo = open(file_name ,'r')
        for line in fo.readlines():
            if line.split(",")[1] == "BCL1\n":
                BCL1.append(float(line.split(",")[0])) #obtengo la data de BCL1 para la instancia "instance"
            # if line.split(",")[1] == "MIR2\n":
            #     MIR2.append(float(line.split(",")[0])) #obtengo la data de MIR2 para la instancia "instance"
            if line.split(",")[1] == "QL1\n":
                QL1.append(float(line.split(",")[0])) #obtengo la data de QL1 para la instancia "instance"
            if line.split(",")[1] == "QL2\n":
                QL2.append(float(line.split(",")[0])) #obtengo la data de QL2 para la instancia "instance"
            if line.split(",")[1] == "QL3\n":
                QL3.append(float(line.split(",")[0])) #obtengo la data de QL3 para la instancia "instance"
            if line.split(",")[1] == "QL4\n":
                QL4.append(float(line.split(",")[0])) #obtengo la data de QL4 para la instancia "instance"
            if line.split(",")[1] == "QL5\n":
                QL5.append(float(line.split(",")[0])) #obtengo la data de QL5 para la instancia "instance"
        fo.close()
        
        
        
        if BCL1:
            dataBCL1 , outlierBCL1 = isOutlier(BCL1) # limpiamos los datos sacando los outlier
        # if MIR2:
        #     dataMIR2 , outlierMIR2 = isOutlier(MIR2) # limpiamos los datos sacando los outlier
        if QL1:
            dataQL1 , outlierQL1 = isOutlier(QL1) # limpiamos los datos sacando los outlier
        if QL2:
            dataQL2 , outlierQL2 = isOutlier(QL2) # limpiamos los datos sacando los outlier
        if QL3:
            dataQL3 , outlierQL3 = isOutlier(QL3) # limpiamos los datos sacando los outlier
        if QL4:
            dataQL4 , outlierQL4 = isOutlier(QL4) # limpiamos los datos sacando los outlier
        if QL5:
            dataQL5 , outlierQL5 = isOutlier(QL5) # limpiamos los datos sacando los outlier
        
                
        #print("analisis estadistico para la instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        cantidad_minima = tamanioMinimo(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5)
        #print(cantidad_minima)


        # analisis estadistico de BCL1 contra los demas 
        analisisEstadisticoBCL1 = analisisEstadisticoBCL1conOtros(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5, cantidad_minima)
        archivoBCL1.write(instance.replace(".txt","").replace("scp","").replace("nr","")+"&")
        archivoBCL1.write("&".join([str(item) for item in analisisEstadisticoBCL1])+"\\\\\n")
        if len(analisisEstadisticoBCL1) < 5:
            print("FALTAN p-values para BCL1 instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        
        # # analisis estadistico de MIR2 contra los demas
        # analisisEstadisticoMIR2 = analisisEstadisticoMIR2conOtros(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5, cantidad_minima)
        # archivoMIR2.write(instance.replace(".txt","").replace("scp","").replace("nr","")+"&")
        # archivoMIR2.write("&".join([str(item) for item in analisisEstadisticoMIR2])+"\\\\\n")
        # if len(analisisEstadisticoMIR2) < 5:
        #     print("FALTAN p-values para MIR2 instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        
        # analisis estadistico de QL1 contra los demas
        analisisEstadisticoQL1 = analisisEstadisticoQL1conOtros(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5, cantidad_minima)
        archivoQL1.write(instance.replace(".txt","").replace("scp","").replace("nr","")+"&")
        archivoQL1.write("&".join([str(item) for item in analisisEstadisticoQL1])+"\\\\\n")
        if len(analisisEstadisticoQL1) < 5:
            print(analisisEstadisticoQL1)
            print("FALTAN p-values para QL1 instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        
        # analisis estadistico de QL2 contra los demas
        analisisEstadisticoQL2 = analisisEstadisticoQL2conOtros(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5, cantidad_minima)
        archivoQL2.write(instance.replace(".txt","").replace("scp","").replace("nr","")+"&")
        archivoQL2.write("&".join([str(item) for item in analisisEstadisticoQL2])+"\\\\\n")
        if len(analisisEstadisticoQL2) < 5:
            print("FALTAN p-values para QL2 instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        
        # analisis estadistico de QL3 contra los demas
        analisisEstadisticoQL3 = analisisEstadisticoQL3conOtros(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5, cantidad_minima)
        archivoQL3.write(instance.replace(".txt","").replace("scp","").replace("nr","")+"&")
        archivoQL3.write("&".join([str(item) for item in analisisEstadisticoQL3])+"\\\\\n")
        if len(analisisEstadisticoQL3) < 5:
            print("FALTAN p-values para QL3 instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        
        # analisis estadistico de QL4 contra los demas
        analisisEstadisticoQL4 = analisisEstadisticoQL4conOtros(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5, cantidad_minima)
        archivoQL4.write(instance.replace(".txt","").replace("scp","").replace("nr","")+"&")
        archivoQL4.write("&".join([str(item) for item in analisisEstadisticoQL4])+"\\\\\n")
        if len(analisisEstadisticoQL4) < 5:
            print("FALTAN p-values para QL4 instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        
        # analisis estadistico de QL5 contra los demas
        analisisEstadisticoQL5 = analisisEstadisticoQL5conOtros(dataBCL1,  dataQL1, dataQL2, dataQL3, dataQL4, dataQL5, cantidad_minima)
        archivoQL5.write(instance.replace(".txt","").replace("scp","").replace("nr","")+"&")
        archivoQL5.write("&".join([str(item) for item in analisisEstadisticoQL5])+"\\\\\n")
        if len(analisisEstadisticoQL4) < 5:
            print("FALTAN p-values para QL5 instancia "+instance.replace(".txt","").replace("scp","").replace("nr","") + " experimento "+experimento)
        
        
    archivoBCL1.write("\\bottomrule\n")   
    archivoBCL1.write("\\caption{p-value of "+experimento+"-BCL1 compared to others algorithm} \\label{tabla:p-value "+experimento+"-BCL1}\n")
    archivoBCL1.write("\\end{tabular}\n")
    
    # archivoMIR2.write("\\bottomrule\n")   
    # archivoMIR2.write("\\caption{p-value of "+experimento+"-MIR2 compared to others algorithm} \\label{tabla:p-value "+experimento+"-MIR2}\n")
    # archivoMIR2.write("\\end{tabular}\n")
    
    archivoQL1.write("\\bottomrule\n")   
    archivoQL1.write("\\caption{p-value of "+experimento+"-QL1 compared to others algorithm} \\label{tabla:p-value "+experimento+"-QL1}\n")
    archivoQL1.write("\\end{tabular}\n")
    
    archivoQL2.write("\\bottomrule\n")   
    archivoQL2.write("\\caption{p-value of "+experimento+"-QL2 compared to others algorithm} \\label{tabla:p-value "+experimento+"-QL2}\n")
    archivoQL2.write("\\end{tabular}\n")
    
    archivoQL3.write("\\bottomrule\n")   
    archivoQL3.write("\\caption{p-value of "+experimento+"-QL3 compared to others algorithm} \\label{tabla:p-value "+experimento+"-QL3}\n")
    archivoQL3.write("\\end{tabular}\n")
    
    archivoQL4.write("\\bottomrule\n")   
    archivoQL4.write("\\caption{p-value of "+experimento+"-QL4 compared to others algorithm} \\label{tabla:p-value "+experimento+"-QL4}\n")
    archivoQL4.write("\\end{tabular}\n")
    
    archivoQL5.write("\\bottomrule\n")   
    archivoQL5.write("\\caption{p-value of "+experimento+"-QL5 compared to others algorithm} \\label{tabla:p-value "+experimento+"-QL5}\n")
    archivoQL5.write("\\end{tabular}\n")
    
    archivoBCL1.close()
    # archivoMIR2.close()
    archivoQL1.close()
    archivoQL2.close()
    archivoQL3.close()
    archivoQL4.close()
    archivoQL5.close()
    
    

def analisisEstadisticoBCL1conOtros(dataBCL1,dataQL1,dataQL2,dataQL3,dataQL4,dataQL5,cantidad_minima):
    analisisEstadisticoBCL1 = []
    # if len(dataMIR2) != 0 and len(dataBCL1) != 0:
    #     try:
    #         analisisEstadisticoBCL1.append(scipy.stats.mannwhitneyu(dataBCL1[0:cantidad_minima],dataMIR2[0:cantidad_minima],alternative='less')[1])
    #     except:
    #         pass
        
    # else:
    #     analisisEstadisticoBCL1.append("-")
    if len(dataQL1) != 0 and len(dataBCL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataBCL1[0:cantidad_minima],dataQL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoBCL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoBCL1.append("0.000")
                else:
                    analisisEstadisticoBCL1.append(valorTest.round(3))
        except:
            analisisEstadisticoBCL1.append("-")
            pass
    else:
        analisisEstadisticoBCL1.append("-")
    if len(dataQL2) != 0 and len(dataBCL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataBCL1[0:cantidad_minima],dataQL2[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoBCL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoBCL1.append("0.000")
                else:
                    analisisEstadisticoBCL1.append(valorTest.round(3))
        except:
            analisisEstadisticoBCL1.append("-")
            pass
    else:
        analisisEstadisticoBCL1.append("-")
    if len(dataQL3) != 0 and len(dataBCL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataBCL1[0:cantidad_minima],dataQL3[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoBCL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoBCL1.append("0.000")
                else:
                    analisisEstadisticoBCL1.append(valorTest.round(3))
        except:
            analisisEstadisticoBCL1.append("-")
            pass
    else:
        analisisEstadisticoBCL1.append("-")
    if len(dataQL4) != 0 and len(dataBCL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataBCL1[0:cantidad_minima],dataQL4[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoBCL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoBCL1.append("0.000")
                else:
                    analisisEstadisticoBCL1.append(valorTest.round(3))
        except:
            analisisEstadisticoBCL1.append("-")
            pass
    else:
        analisisEstadisticoBCL1.append("-")
    if len(dataQL5) != 0 and len(dataBCL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataBCL1[0:cantidad_minima],dataQL5[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoBCL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoBCL1.append("0.000")
                else:
                    analisisEstadisticoBCL1.append(valorTest.round(3))
        except:
            analisisEstadisticoBCL1.append("-")
            pass
    else:
        analisisEstadisticoBCL1.append("-")
        
    return(analisisEstadisticoBCL1)

# def analisisEstadisticoMIR2conOtros(dataBCL1,dataQL1,dataQL2,dataQL3,dataQL4,dataQL5,cantidad_minima):
#     analisisEstadisticoMIR2 = []
#     if len(dataBCL1) != 0 and len(dataMIR2) != 0:
#         try:
#             analisisEstadisticoMIR2.append(scipy.stats.mannwhitneyu(dataMIR2[0:cantidad_minima],dataBCL1[0:cantidad_minima],alternative='less')[1])
#         except:
#             pass
#     else:
#         analisisEstadisticoMIR2.append("-")
#     if len(dataQL1) != 0 and len(dataMIR2) != 0:
#         try:
#             analisisEstadisticoMIR2.append(scipy.stats.mannwhitneyu(dataMIR2[0:cantidad_minima],dataQL1[0:cantidad_minima],alternative='less')[1])
#         except:
#             pass
#     else:
#         analisisEstadisticoMIR2.append("-")
#     if len(dataQL2) != 0 and len(dataMIR2) != 0:
#         try:
#             analisisEstadisticoMIR2.append(scipy.stats.mannwhitneyu(dataMIR2[0:cantidad_minima],dataQL2[0:cantidad_minima],alternative='less')[1])
#         except:
#             pass
#     else:
#         analisisEstadisticoMIR2.append("-")
#     if len(dataQL3) != 0 and len(dataMIR2) != 0:
#         try:
#             analisisEstadisticoMIR2.append(scipy.stats.mannwhitneyu(dataMIR2[0:cantidad_minima],dataQL3[0:cantidad_minima],alternative='less')[1])
#         except:
#             pass 
#     else:
#         analisisEstadisticoMIR2.append("-")
#     if len(dataQL4) != 0 and len(dataMIR2) != 0:
#         try:
#             analisisEstadisticoMIR2.append(scipy.stats.mannwhitneyu(dataMIR2[0:cantidad_minima],dataQL4[0:cantidad_minima],alternative='less')[1])
#         except:
#             pass
#     else:
#         analisisEstadisticoMIR2.append("-")
#     if len(dataQL5) != 0 and len(dataMIR2) != 0:
#         try:
#             analisisEstadisticoMIR2.append(scipy.stats.mannwhitneyu(dataMIR2[0:cantidad_minima],dataQL5[0:cantidad_minima],alternative='less')[1])
#         except:
#             pass
#     else:
#         analisisEstadisticoMIR2.append("-")
        
#     return(analisisEstadisticoMIR2)

def analisisEstadisticoQL1conOtros(dataBCL1,dataQL1,dataQL2,dataQL3,dataQL4,dataQL5,cantidad_minima):
    analisisEstadisticoQL1 = []
    if len(dataBCL1) != 0 and len(dataQL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL1[0:cantidad_minima],dataBCL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL1.append("0.000")
                else:
                    analisisEstadisticoQL1.append(valorTest.round(3))
        except:
            analisisEstadisticoQL1.append("-")
            pass

    else:
        analisisEstadisticoQL1.append("-")
    # if len(dataMIR2) != 0 and len(dataQL1) != 0:
    #     try:
    #         analisisEstadisticoQL1.append(scipy.stats.mannwhitneyu(dataQL1[0:cantidad_minima],dataMIR2[0:cantidad_minima],alternative='less')[1])
    #     except:
    #         pass
    # else:
    #     analisisEstadisticoQL1.append("-")
    if len(dataQL2) != 0 and len(dataQL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL1[0:cantidad_minima],dataQL2[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL1.append("0.000")
                else:
                    analisisEstadisticoQL1.append(valorTest.round(3))
        except:
            analisisEstadisticoQL1.append("-")
            pass
    else:
        analisisEstadisticoQL1.append("-")
    if len(dataQL3) != 0 and len(dataQL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL1[0:cantidad_minima],dataQL3[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL1.append("0.000")
                else:
                    analisisEstadisticoQL1.append(valorTest.round(3))
        except:
            analisisEstadisticoQL1.append("-")
            pass
    else:
        analisisEstadisticoQL1.append("-")
    if len(dataQL4) != 0 and len(dataQL1) != 0:
        try:
            analisisEstadisticoQL1.append(scipy.stats.mannwhitneyu(dataQL1[0:cantidad_minima],dataQL4[0:cantidad_minima],alternative='less')[1])
        except:
            analisisEstadisticoQL1.append("-")
            pass

    else:
        analisisEstadisticoQL1.append("-")
    if len(dataQL5) != 0 and len(dataQL1) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL1[0:cantidad_minima],dataQL5[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL1.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL1.append("0.000")
                else:
                    analisisEstadisticoQL1.append(valorTest.round(3))
        except:
            analisisEstadisticoQL1.append("-")
            pass
    else:
        analisisEstadisticoQL1.append("-")
        
    return(analisisEstadisticoQL1)

def analisisEstadisticoQL2conOtros(dataBCL1,dataQL1,dataQL2,dataQL3,dataQL4,dataQL5,cantidad_minima):
    analisisEstadisticoQL2 = []
    if len(dataBCL1) != 0 and len(dataQL2) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL2[0:cantidad_minima],dataBCL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL2.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL2.append("0.000")
                else:
                    analisisEstadisticoQL2.append(valorTest.round(3))
        except:
            analisisEstadisticoQL2.append("-")
            pass
    else:
        analisisEstadisticoQL2.append("-")
    # if len(dataMIR2) != 0 and len(dataQL2) != 0:
    #     try:
    #         analisisEstadisticoQL2.append(scipy.stats.mannwhitneyu(dataQL2[0:cantidad_minima],dataMIR2[0:cantidad_minima],alternative='less')[1])
    #     except:
    #         pass
    # else:
    #     analisisEstadisticoQL2.append("-")
    if len(dataQL1) != 0 and len(dataQL2) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL2[0:cantidad_minima],dataQL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL2.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL2.append("0.000")
                else:
                    analisisEstadisticoQL2.append(valorTest.round(3))
        except:
            analisisEstadisticoQL2.append("-")
            pass
    else:
        analisisEstadisticoQL2.append("-")
    if len(dataQL3) != 0 and len(dataQL2) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL2[0:cantidad_minima],dataQL3[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL2.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL2.append("0.000")
                else:
                    analisisEstadisticoQL2.append(valorTest.round(3))
        except:
            analisisEstadisticoQL2.append("-")
            pass
    else:
        analisisEstadisticoQL2.append("-")
    if len(dataQL4) != 0 and len(dataQL2) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL2[0:cantidad_minima],dataQL4[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL2.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL2.append("0.000")
                else:
                    analisisEstadisticoQL2.append(valorTest.round(3))
        except:
            analisisEstadisticoQL2.append("-")
            pass
    else:
        analisisEstadisticoQL2.append("-")
    if len(dataQL5) != 0 and len(dataQL2) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL2[0:cantidad_minima],dataQL5[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL2.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL2.append("0.000")
                else:
                    analisisEstadisticoQL2.append(valorTest.round(3))
        except:
            analisisEstadisticoQL2.append("-")
            pass
    else:
        analisisEstadisticoQL2.append("-")
        
    return(analisisEstadisticoQL2)

def analisisEstadisticoQL3conOtros(dataBCL1,dataQL1,dataQL2,dataQL3,dataQL4,dataQL5,cantidad_minima):
    analisisEstadisticoQL3 = []
    if len(dataBCL1) != 0 and len(dataQL3) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL3[0:cantidad_minima],dataBCL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL3.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL3.append("0.000")
                else:
                    analisisEstadisticoQL3.append(valorTest.round(3))
        except:
            analisisEstadisticoQL3.append("-")
            pass
    else:
        analisisEstadisticoQL3.append("-")
    # if len(dataMIR2) != 0 and len(dataQL3) != 0:
    #     try:
    #         analisisEstadisticoQL3.append(scipy.stats.mannwhitneyu(dataQL3[0:cantidad_minima],dataMIR2[0:cantidad_minima],alternative='less')[1])
    #     except:
    #         pass
    # else:
    #     analisisEstadisticoQL3.append("-")
    if len(dataQL1) != 0 and len(dataQL3) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL3[0:cantidad_minima],dataQL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL3.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL3.append("0.000")
                else:
                    analisisEstadisticoQL3.append(valorTest.round(3))
        except:
            analisisEstadisticoQL3.append("-")
            pass
    else:
        analisisEstadisticoQL3.append("-")
    if len(dataQL2) != 0 and len(dataQL3) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL3[0:cantidad_minima],dataQL2[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL3.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL3.append("0.000")
                else:
                    analisisEstadisticoQL3.append(valorTest.round(3))
        except:
            analisisEstadisticoQL3.append("-")
            pass
    else:
        analisisEstadisticoQL3.append("-")
    if len(dataQL4) != 0 and len(dataQL3) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL3[0:cantidad_minima],dataQL4[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL3.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL3.append("0.000")
                else:
                    analisisEstadisticoQL3.append(valorTest.round(3))
        except:
            analisisEstadisticoQL3.append("-")
            pass
    else:
        analisisEstadisticoQL3.append("-")
    if len(dataQL5) != 0 and len(dataQL3) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL3[0:cantidad_minima],dataQL5[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL3.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL3.append("0.000")
                else:
                    analisisEstadisticoQL3.append(valorTest.round(3))
        except:
            analisisEstadisticoQL3.append("-")
            pass
    else:
        analisisEstadisticoQL3.append("-")
        
    return(analisisEstadisticoQL3)

def analisisEstadisticoQL4conOtros(dataBCL1,dataQL1,dataQL2,dataQL3,dataQL4,dataQL5,cantidad_minima):
    analisisEstadisticoQL4 = []
    if len(dataBCL1) != 0 and len(dataQL4) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL4[0:cantidad_minima],dataBCL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL4.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL4.append("0.000")
                else:
                    analisisEstadisticoQL4.append(valorTest.round(3))
        except:
            analisisEstadisticoQL4.append("-")
            pass
    else:
        analisisEstadisticoQL4.append("-")
    # if len(dataMIR2) != 0  and len(dataQL4) != 0:
    #     try:
    #         analisisEstadisticoQL4.append(scipy.stats.mannwhitneyu(dataQL4[0:cantidad_minima],dataMIR2[0:cantidad_minima],alternative='less')[1])
    #     except:
    #         pass
    # else:
    #     analisisEstadisticoQL4.append("-")
    if len(dataQL1) != 0 and len(dataQL4) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL4[0:cantidad_minima],dataQL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL4.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL4.append("0.000")
                else:
                    analisisEstadisticoQL4.append(valorTest.round(3))
        except:
            analisisEstadisticoQL4.append("-")
            pass
    else:
        analisisEstadisticoQL4.append("-")
    if len(dataQL2) != 0 and len(dataQL4) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL4[0:cantidad_minima],dataQL2[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL4.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL4.append("0.000")
                else:
                    analisisEstadisticoQL4.append(valorTest.round(3))
        except:
            analisisEstadisticoQL4.append("-")
            pass
    else:
        analisisEstadisticoQL4.append("-")
    if len(dataQL3) != 0 and len(dataQL4) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL4[0:cantidad_minima],dataQL3[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL4.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL4.append("0.000")
                else:
                    analisisEstadisticoQL4.append(valorTest.round(3))
        except:
            analisisEstadisticoQL4.append("-")
            pass
    else:
        analisisEstadisticoQL4.append("-")
    if len(dataQL5) != 0 and len(dataQL4) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL4[0:cantidad_minima],dataQL5[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL4.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL4.append("0.000")
                else:
                    analisisEstadisticoQL4.append(valorTest.round(3))
        except:
            analisisEstadisticoQL4.append("-")
            pass
    else:
        analisisEstadisticoQL4.append("-")
        
    return(analisisEstadisticoQL4)

def analisisEstadisticoQL5conOtros(dataBCL1,dataQL1,dataQL2,dataQL3,dataQL4,dataQL5,cantidad_minima):
    analisisEstadisticoQL5 = []
    if len(dataBCL1) != 0 and len(dataQL5) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL5[0:cantidad_minima],dataBCL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL5.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL5.append("0.000")
                else:
                    analisisEstadisticoQL5.append(valorTest.round(3))
        except:
            analisisEstadisticoQL5.append("-")
            pass
    else:
        analisisEstadisticoQL5.append("-")
    # if len(dataMIR2) != 0 and len(dataQL5) != 0:
    #     try:
    #         analisisEstadisticoQL5.append(scipy.stats.mannwhitneyu(dataQL5[0:cantidad_minima],dataMIR2[0:cantidad_minima],alternative='less')[1])
    #     except:
    #         pass
    # else:
    #     analisisEstadisticoQL5.append("-")
    if len(dataQL1) != 0 and len(dataQL5) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL5[0:cantidad_minima],dataQL1[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL5.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL5.append("0.000")
                else:
                    analisisEstadisticoQL5.append(valorTest.round(3))
        except:
            analisisEstadisticoQL5.append("-")
            pass
    else:
        analisisEstadisticoQL5.append("-")
    if len(dataQL2) != 0 and len(dataQL5) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL5[0:cantidad_minima],dataQL2[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL5.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL5.append("0.000")
                else:
                    analisisEstadisticoQL5.append(valorTest.round(3))
        except:
            analisisEstadisticoQL5.append("-")
            pass
    else:
        analisisEstadisticoQL5.append("-")
    if len(dataQL3) != 0 and len(dataQL5) != 0:
        try:
            valorTest = scipy.stats.mannwhitneyu(dataQL5[0:cantidad_minima],dataQL3[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL5.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL5.append("0.000")
                else:
                    analisisEstadisticoQL5.append(valorTest.round(3))
        except:
            analisisEstadisticoQL5.append("-")
            pass
    else:
        analisisEstadisticoQL5.append("-")
    if len(dataQL4) != 0 and len(dataQL5) != 0:
        try:

            valorTest = scipy.stats.mannwhitneyu(dataQL5[0:cantidad_minima],dataQL4[0:cantidad_minima],alternative='less')[1]
            if valorTest >= 0.05:
                analisisEstadisticoQL5.append("-")
            else:
                if valorTest < 0.0009:
                    analisisEstadisticoQL5.append("0.000")
                else:
                    analisisEstadisticoQL5.append(valorTest.round(3))
        except:
            analisisEstadisticoQL5.append("-")
            pass
    else:
        analisisEstadisticoQL5.append("-")
        
    return(analisisEstadisticoQL5)

def isOutlier(data):
    
    data = np.sort(data)
    Q1 = np.percentile(data, 25, interpolation = 'midpoint')  
    Q3 = np.percentile(data, 75, interpolation = 'midpoint')  
    IQR = (Q3-Q1)
    low = Q1 - 1.5 * IQR 
    upper = Q3 + 1.5 * IQR 
    
    dataNew =[]
    outlier = []
    for x in data: 
        if ~((x> upper) or (x<low)): 
             dataNew.append(x)
        else:
            outlier.append(x)
    return dataNew, outlier


def tamanioMinimo(BCL1,QL1,QL2,QL3,QL4,QL5):
    minimos = []
    if len(BCL1) != 0:
        minimos.append(len(BCL1))
    # if len(MIR2) != 0:
    #     minimos.append(len(MIR2))
    if len(QL1) != 0:
        minimos.append(len(QL1))
    if len(QL2) != 0:
        minimos.append(len(QL2))
    if len(QL3) != 0:
        minimos.append(len(QL3))
    if len(QL4) != 0:
        minimos.append(len(QL4))
    if len(QL5) != 0:
        minimos.append(len(QL5))
    
    return min(minimos)
    
    
    
    
    
    
    
    
    
    
