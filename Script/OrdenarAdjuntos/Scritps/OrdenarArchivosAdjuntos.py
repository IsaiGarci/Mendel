## IMPORTACIONES DEL CÓDIGO.
from datetime import datetime
import pandas as pd
import glob


## VARIABLES GENERALES DEL CÓDIGO.
TodaysDate = datetime.now().strftime("%Y%m%d")
TodaysReport = f'../../../Reportes/{TodaysDate}/Reporte-*.csv'
FinishedFile = f'../Data/TermineArchivosAdjuntos.txt'


## FUNCIONES DEL CÓDIGO.
def CleanAuditFile():
    with open('../Data/ArchivosAdjuntosPorPersona.csv', 'w', encoding='utf-8') as file:
        file.write('')

def CreateFinishingFile(FilesByUser):
    with open(FinishedFile, 'w', encoding='utf-8') as file:
        file.write('')

def GetFilesByUser(TodaysReport):
    #CleanAuditFile()
    
    ReportFiles = glob.glob(TodaysReport)
    FilesByUser = {}
    
    for TodaysReport in ReportFiles:
        Df = pd.read_csv(TodaysReport)
        Grouped = Df.groupby('Usuario')

        for name, group in Grouped:
            PdfFiles = group['Nombre PDF'].dropna().tolist()
            XmlFiles = group['Nombre XML'].dropna().tolist()

            if name not in FilesByUser:
                FilesByUser[name] = {'PDFs': PdfFiles, 'XMLs': XmlFiles}
            else:
                FilesByUser[name]['PDFs'].extend(PdfFiles)
                FilesByUser[name]['XMLs'].extend(XmlFiles)
    count = 0
    with open('../Data/ArchivosAdjuntosPorPersona.csv', 'a', encoding='utf-8') as file:
        for user, files in FilesByUser.items():
            max_pairs = max(len(files['PDFs']), len(files['XMLs']))
            for i in range(max_pairs):
                pdf = files['PDFs'][i] if i < len(files['PDFs']) else "PDF faltante"
                xml = files['XMLs'][i] if i < len(files['XMLs']) else "XML faltante"
                # Ignorar la línea si faltan ambos archivos
                if pdf == "PDF faltante" and xml == "XML faltante":
                    count += 1
                    continue
                file.write(f'{user};{pdf};{xml}\n')
    
    
<<<<<<< HEAD
    with open(f'../Data/TermineArchivosAdjuntos.txt', 'a', encoding='utf-8') as file:
=======
    with open(f'../Data/TerminéArchivosAdjuntos.txt', 'a', encoding='utf-8') as file:
>>>>>>> c1d0193436b12cbc8fb8e8ff454c527477627512
        file.write('Terminé de ordenar los archivos adjuntos\n')
    
    return FilesByUser   



## MAIN DEL CODE.
if __name__ == "__main__":
    GetFilesByUser(TodaysReport)