import csv

# Ruta del archivo de entrada
input_file_path = r'C:\ProduccionRpa\Mendel\Reportes\20240531\Reporte-6ad4d20240531.csv'
# Ruta del archivo de salida
output_file_path = 'Empleados_Mendel.csv'

# Abre el archivo de entrada en modo lectura
with open(input_file_path, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = 'Usuario', 'Empleado'
    next(reader)  # Lee la primera fila como encabezado
    datos = []
    nombres_vistos = set()
    
    # Itera sobre las filas del archivo CSV
    for row in reader:
        # Verifica que la fila tenga suficientes columnas
        Nombre = row[2]
        Empleado = row[42]
        if Nombre not in nombres_vistos:
            datos.append([Nombre, Empleado])
            nombres_vistos.add(Nombre)

# Ordena los datos por el número de empleado (asumiendo que Empleado es una cadena que representa un número)
datos.sort(key=lambda x: int(x[1]))

# Abre el archivo de salida en modo escritura
with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    # Escribe los encabezados y luego los datos ordenados en el archivo de salida
    writer.writerow(header)
    writer.writerows(datos)
