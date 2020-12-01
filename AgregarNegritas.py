import numpy as np
import pandas as pd
import os
ArchivoNegritas = "archivoTablaResumen_WOA_Negritas.txt"
df = pd.read_csv(r"C:\Users\José Lemus Romani\Google Drive\2.- Universidad\2.- Doctorado\7mo Semestre\0.- Git\GenerarResumenExperimentos\archivoTablaResumen_WOA.csv")
csvMatrix = df.to_numpy()
cols = csvMatrix.shape[1]
filas = csvMatrix.shape[0]

resultados = csvMatrix[:,2:cols]
colsResultados = resultados.shape[1]
filasResultados = resultados.shape[0]
resultadosAux = resultados

columAEliminar = int((colsResultados/3) * 2)
colsDelete = 0
for i in range(columAEliminar):
    if (i%2 == 0):
        colsDelete = colsDelete + 1
    resultadosAux = np.delete(resultadosAux, colsDelete, axis=1)

argmin = np.argmin(resultadosAux, axis=1)

salida = open(ArchivoNegritas, "w",encoding="utf=8")
salida.write("\\\\\\midrule")

for i in range(filas):
    linea = []
    for j in range(cols):
        if (j == (2+ argmin[i]*3)):
            linea.append("\textbf{" + str(csvMatrix[i][j]) + "}" + "&")
        else:
            linea.append(str(csvMatrix[i][j]) + "&")
    #print(linea)
    if i == filas-1:
        salida.write( " \\hline" + str(linea).replace("[","").replace("]","").replace("'","").replace(",","").replace("nan","") + "\\\\")
    else:
        salida.write(str(linea).replace("[","").replace("]","").replace("'","").replace(",","").replace("nan","") + "\\\\")
salida.close()
#filepy = open("C:/Users/José Lemus Romani/Desktop/configure2.py","w", encoding="utf=8")
#filepy.write("# Utils" + os.linesep)
