import os



def generarTex(file,NombresAlgoritmo,instancias,escaleColumnWidth,path):
    #For de NombreAlgoritmo: "GWO-Repair-Complex-Init-Zeros", "SCA-Repair-Simple-Init-Rand" #Tam 16 Implementaciones
    for NombreAlgoritmo in NombresAlgoritmo:
        MH = NombreAlgoritmo.split('-')[0] 
        repair = NombreAlgoritmo.split('-')[2]
        Init = NombreAlgoritmo.split('-')[4]
        file.write(f"\\section{{{NombreAlgoritmo}}}")
        file.write(os.linesep)  

        #for por InstanciaText: "41", 51, 61, a1 #Tam 7
        for instancia in instancias:
            file.write(f"\\subsection{{Intance {instancia}}}")
            #file.write(os.linesep)  

            file.write("\\subsection{Convergence graphics}")
            file.write(os.linesep)  
            #for por archivo que empiecen con gc en el directorio, "gc-Zeros-GWO-SCP-BCL1-CPU-C-scp41", "gc-Zeros-GWO-SCP-MIR2-CPU-C-scp41" #Tam 7
            
            rutagc = path + MH + '/' + Init  + '/' + 'scp' + instancia.replace('.','') + '/' + repair + '/' + 'gc'
            gcResultadoTotal = os.listdir(rutagc)

            for gcResultado in gcResultadoTotal:
                if gcResultado != "desktop.ini":
                    file.write(os.linesep)  
                    file.write("\\begin{figure}[H]")
                    file.write("\\centering ")
                    file.write(f"\\includegraphics[width={escaleColumnWidth}\\columnwidth]{{{rutagc.replace(path,'') + '/' + gcResultado}}}")
                    #file.write(f"\\caption{{{gcResultado.replace('.pdf','')}}} \\label{{{gcResultado.replace('.pdf','')}}}")
                    file.write(f"\\caption{{{gcResultado.replace('.pdf','')}}} ")
                    file.write("\\end{figure}")

                


            #file.write(os.linesep)  
            file.write("\\subsection{Diversity Graphics}")
            file.write(os.linesep)  
            
            rutagd = path + MH + '/' + Init  + '/' + 'scp' + instancia.replace('.','') + '/' + repair + '/' + 'gd'
            gdResultadoTotal = os.listdir(rutagd)
            #for por Experimento #Tam 7 BLC1, MIR2, QL1, QL2, QL3, QL4, QL5
            for gdResultado in gdResultadoTotal:
                if gdResultado != "desktop.ini":
                    file.write(os.linesep)  
                    file.write("\\begin{figure}[H]")
                    file.write("\\centering ")
                    file.write(f"\\includegraphics[width={escaleColumnWidth}\\columnwidth]{{{rutagd.replace(path,'') + '/' + gdResultado}}}")
                    #file.write(f"\\caption{{{gdResultado.replace('.pdf','')}}} \\label{{{gdResultado.replace('.pdf','')}}}")
                    file.write(f"\\caption{{{gdResultado.replace('.pdf','')}}}")
                    file.write("\\end{figure}")



            #file.write(os.linesep)  
            file.write("\\subsection{Exploration and Exploitation Graphics}")
            file.write(os.linesep)  
            rutagee = path + MH + '/' + Init  + '/' + 'scp' + instancia.replace('.','') + '/' + repair + '/' + 'gee'
            geeResultadoTotal = os.listdir(rutagee)
            #for por Experimento #Tam 7 BLC1, MIR2, QL1, QL2, QL3
            for geeResultado in geeResultadoTotal:
                if geeResultado != "desktop.ini":
                    file.write(os.linesep)  
                    file.write("\\begin{figure}[H]")
                    file.write("\\centering ")
                    file.write(f"\\includegraphics[width={escaleColumnWidth}\\columnwidth]{{{rutagee.replace(path,'') + '/' + geeResultado}}}")
                    #file.write(f"\\caption{{{geeResultado.replace('.pdf','')}}} \\label{{{geeResultado.replace('.pdf','')}}}")
                    file.write(f"\\caption{{{geeResultado.replace('.pdf','')}}} ")
                    file.write("\\end{figure}")
