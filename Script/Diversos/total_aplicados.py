import csv
import datetime
import os

def leer_tabla(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            data.append(row)
    return headers, data

def leer_folios_aplicados(file_path):
    folios_autorizados = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            folios_autorizados.append(row[0])
    return folios_autorizados

# Ruta de los archivos CSV
reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')
tabla_dir = fr'{reportes}\{hoy}'

# Encontrar el archivo de reporte correspondiente
tabla = ''
for file in os.listdir(tabla_dir):
    if file.startswith('Reporte-'):
        tabla = fr'{tabla_dir}\{file}'
        break

folios_aplicados_path = r'C:\ProduccionRpa\Mendel\Control\Aplicados\folio_gastos_aplicados.csv'
cargos_path = 'Cargos aplicados.csv'

# Leer los folios aplicados
folios_aplicados = leer_folios_aplicados(folios_aplicados_path)

# Leer la tabla de reporte
headers, datos_reporte = leer_tabla(tabla)

# Filtrar y guardar las filas correspondientes en Cargos aplicados
cargos_aplicados = []

for row in datos_reporte:
    folio = row[0]  # Asumiendo que el folio está en la primera columna
    if folio in folios_aplicados:
        cargos_aplicados.append(row)

# Ordenar las filas por el nombre (columna 2)
cargos_aplicados.sort(key=lambda x: x[2])

# Escribir las filas en el archivo Cargos aplicados
with open(cargos_path, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(headers)  # Escribir el encabezado
    writer.writerows(cargos_aplicados)  # Escribir las filas filtradas y ordenadas
