import csv, os, datetime
# Función para leer el archivo de tabla2-test.csv y almacenar los datos en una lista
def leer_tabla(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            folio = row[0]
            nombre = row[2]
            total = float(row[4])   # Aseguramos que el total sea un número
            data.append([folio, nombre, total])
            data.sort(key=lambda x: x[1])   # Ordenamos los datos por nombre
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
            writer.writerow([nombre, total])

# Ruta de los archivos CSV
reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')
tabla2_test_path = fr'{reportes}\{hoy}'
for file in os.listdir(tabla2_test_path):
    if file.startswith('Reporte-'):
        tabla2_test_path = fr'{tabla2_test_path}\{file}'
        break
folios_aplicados_path = r'C:\ProduccionRpa\Mendel\Control\Aplicados\folio_gastos_aplicados.csv'
totales_path = r'total_abonos.csv'

# Leer los archivos
data = leer_tabla(tabla2_test_path)
folios_autorizados = leer_folios_autorizados(folios_aplicados_path)

# Inicializar variables para acumulación
totales_acumulados = {}
nombre_anterior = None
total_acumulado = 0

# Recorrer los datos y acumular los totales si los folios están autorizados
for folio, nombre, total in data:
    if folio in folios_autorizados:
        if nombre == nombre_anterior:
            total_acumulado += total
        else:
            if nombre_anterior is not None:
                totales_acumulados[nombre_anterior] = total_acumulado
                print(f'Empleado: {nombre_anterior} - Total acumulado: {total_acumulado}')
            total_acumulado = total
        nombre_anterior = nombre

# Asegurarse de guardar el último total acumulado
if nombre_anterior is not None:
    totales_acumulados[nombre_anterior] = total_acumulado
    print(f'Empleado: {nombre_anterior} - Total acumulado: {total_acumulado}')

# Guardar los totales acumulados en el archivo CSV
guardar_totales(totales_path, totales_acumulados)