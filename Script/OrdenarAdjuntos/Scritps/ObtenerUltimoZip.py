import os
from datetime import datetime, timedelta


directorio_descargas = 'C:\\Users\\E-EC1-3752\\Downloads'
tiempo_actual = datetime.now()
limite_tiempo = tiempo_actual - timedelta(minutes=5)


for archivo in os.listdir(directorio_descargas): 
    ruta_completa = os.path.join(directorio_descargas, archivo)
    if os.path.isfile(ruta_completa) and archivo.endswith('.zip'):
        print(f'Analizando archivo: {archivo}')
        
        tiempo_modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
        if tiempo_modificacion > limite_tiempo:
            print(f'Archivo encontrado: {archivo}, modificado en: {tiempo_modificacion}')
            with open('../Data/UbicacionUltimoZip.txt', 'w', encoding='utf-8') as file:
                file.write(ruta_completa)