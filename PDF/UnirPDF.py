from PyPDF2 import PdfFileMerger
import os

pdfs2 = os.listdir()
pdfs = []
for pdf in pdfs2:
    extension = pdf.split('.')[1]
    if extension == "pdf":
        pdfs.append(pdf)

print(pdfs)
nombre_archivo_salida = "Violines_GWO_HHO_SCA_WOA.pdf"
fusionador = PdfFileMerger()

for pdf in pdfs:
    fusionador.append(open(pdf, 'rb'))

with open(nombre_archivo_salida, 'wb') as salida:
    fusionador.write(salida)