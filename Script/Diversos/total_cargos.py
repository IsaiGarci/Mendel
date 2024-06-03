import csv
import datetime
import os

# Función para leer el archivo de tabla2-test.csv y almacenar los datos en una lista
def leer_tabla(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            folio = row[0]
            nombre = row[2]
            total = float(row[4])  # Aseguramos que el total sea un número
            data.append([folio, nombre, total])
    return data

# Función para leer el archivo de folio_gastos_aplicados.csv y almacenar los folios autorizados en una lista
def leer_folios_autorizados(file_path):
    folios_autorizados = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            folios_autorizados.append(row[0])
    return folios_autorizados

# Función para guardar los totales acumulados en un archivo CSV
def guardar_totales(file_path, totales):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Nombre', 'Total Acumulado'])
        for nombre, total in totales.items():
            writer.writerow([nombre, round(total,2)])

# Ruta de los archivos CSV
reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')
tabla2_test_path = fr'{reportes}\{hoy}'
for file in os.listdir(tabla2_test_path):
    if file.startswith('Reporte-'):
        tabla2_test_path = fr'{tabla2_test_path}\{file}'
        break
folios_aplicados_path = r'C:\ProduccionRpa\Mendel\Control\polizas_aplicadas.csv'
totales_path = r'total_cargos.csv'

# Leer los archivos
data = leer_tabla(tabla2_test_path)
folios_autorizados = leer_folios_autorizados(folios_aplicados_path)

# Inicializar variables para acumulación
totales_acumulados = {}

# Recorrer los datos y acumular los totales si los folios están autorizados
for folio, nombre, total in data:
    if folio in folios_autorizados:
        if nombre in totales_acumulados:
            totales_acumulados[nombre] += total
        else:
            totales_acumulados[nombre] = total

# Guardar los totales acumulados en el archivo CSV
guardar_totales(totales_path, totales_acumulados)

# Imprimir los resultados
for nombre, total in totales_acumulados.items():
    print(f'Empleado: {nombre} - Total acumulado: {total}')
