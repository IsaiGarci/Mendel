## IMPORTACIONES DEL CÓDIGO.
import os, shutil


## VARIABLES GENERALES DEL CÓDIGO.
Attachments = '../Data/Adjuntos'
UsersFolderPath = '../../../Empleados'
FilesPath = '../Data/ArchivosAdjuntosPorPersona.csv'


## FUNCIONES DEL CÓDIGO.
def CreateFinishingFile():
    with open('../Data/TerminéMoverAdjuntos.txt', 'w') as file:
        file.write('Terminé de mover los archivos adjuntos\n')

def MoveFiles():     
    with open(FilesPath, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    for linea in lineas:
        partes = linea.strip().split(';')
        nombre_persona = partes[0]
        archivos = partes[1:]
        ruta_carpeta_persona = os.path.join(UsersFolderPath, f'{nombre_persona}/Adjuntos')

        for archivo in archivos:
            if archivo != "XML faltante" or archivo != "PDF faltante":
                ruta_archivo_original = os.path.join(Attachments, archivo)
                ruta_archivo_destino = os.path.join(ruta_carpeta_persona, archivo)
                if os.path.exists(ruta_archivo_original):
                    shutil.move(ruta_archivo_original, ruta_archivo_destino)
                    print(f"El archivo {archivo} fue movido a la carpeta de {nombre_persona}.")
    
    CreateFinishingFile()    

## MAIN DEL CÓDIGO.
if __name__ == '__main__':
    MoveFiles()