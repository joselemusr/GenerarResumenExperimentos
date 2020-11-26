import os
import shutil
path = "Latex/"
MHs = os.listdir(path) 
RutaDestino = "PDF/"

for mh in MHs:
    print(mh)
    directorioMH = path + mh
    Inits = os.listdir(directorioMH) 
    for init in Inits:
        print(init)
        directorioInit = directorioMH + "/" + init
        repairs = os.listdir(directorioInit) 
        for repair in repairs:
            print(repair)
            directorioRepair = directorioInit + "/" + repair
            dgs = os.listdir(directorioRepair)     
            for dg in dgs:
                print(dg)
                directorioDg = directorioRepair + "/" + dg + "/dg/"
                ArchivosEnElDirectorio = os.listdir(directorioDg)
                for archivo in ArchivosEnElDirectorio:
                    extension = archivo.split('.')[1]
                    if extension =="pdf":
                        shutil.copy(directorioDg + archivo, RutaDestino + archivo)
             
