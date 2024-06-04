import os
import datetime
import csv

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')
tabla2_test_path = fr'{reportes}\{hoy}'

for file in os.listdir(tabla2_test_path):
    if file.startswith('Reporte-'):
        tabla2_test_path = fr'{tabla2_test_path}\{file}'
        break

def leer_tabla(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            empleado = row[42]
            nombre = row[2]
            data[empleado] = nombre
    return data

def leer_datos(file_path, tabla_data):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            empleado = row[0]
            cargo = row[1]
            if empleado in tabla_data:
                data.append([tabla_data[empleado], cargo])
    return data

def main():
    datos_tabla = leer_tabla(tabla2_test_path)
    datos_combinados = leer_datos('Descuentos SEM 20 .csv', datos_tabla)
    
    # Ordenar los datos por el nombre (primer elemento de cada fila)
    datos_combinados.sort(key=lambda x: x[0])
    
    with open('Descuentos.csv', 'w',newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Nombre', 'Cargo'])
        for row in datos_combinados:
            writer.writerow(row)

if __name__ == '__main__':
    main()
