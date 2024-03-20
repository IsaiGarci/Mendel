import csv
import os

try:
    with open(f'910a2cbf-34b6-435a-9cee-43a4bde1d7b6.csv', 'r') as f:
        print('Procesando archivo')
        reader = csv.reader(f)
        data = [row for row in reader]
        ##Ordenamos los datos por fecha de la columna 1
        try:
            data.sort(key=lambda x: x[1])
        except:
            pass
    with open(f'910a2cbf-34b6-435a-9cee-43a4bde1d7b6.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        print('Reporte creado con éxito')
except:
    pass