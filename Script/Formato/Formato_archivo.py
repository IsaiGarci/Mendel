import os, csv, datetime

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')

#Cambiamos el formato de los archivo a UTF-8
def formatear():
    try:
        for file in os.listdir(f'{reportes}\{hoy}'):
            with open(f'{reportes}\{hoy}\{file}', 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                data = [row for row in reader]
                data.sort(key=lambda x: x[1])
            with open(f'{reportes}\{hoy}\{file}', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)
                print('Reporte creado con éxito')
    except Exception as e:
        print(f'Error al formatear el archivo: {e}')
        pass

#Creamos archivo nuevo sin External Card
def limpiar_reporte():
    for archivo in os.listdir(f'{reportes}/{hoy}'):
        if archivo.endswith('.csv'):
            datos_limpios = []
            print(f'{reportes}/{hoy}/{archivo}')
            with open(f'{reportes}/{hoy}/{archivo}', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                encabezado = next(reader)  # Guarda el encabezado
                for row in reader:
                    if row[11] != 'EXTERNAL_CARD':
                        datos_limpios.append(row)

            nombre_archivo_limpio = f'Limpio_{archivo}'
            with open(f'{reportes}/{hoy}/{nombre_archivo_limpio}', 'w', newline='', encoding='utf-8') as f_limpio:
                print(f'Creando archivo {nombre_archivo_limpio}')
                writer = csv.writer(f_limpio)
                writer.writerow(encabezado)  # Escribe el encabezado original
                writer.writerows(datos_limpios)

def Formato_archivo():
    formatear()
    limpiar_reporte()

