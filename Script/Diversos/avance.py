import csv

acumulador1 = acumulador2 = acumulador3 = 0
with open(r'C:\ProduccionRpa\Mendel\Control\Tabla\20240523\tabla2-test.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    data = []
    for row in reader:
        folio = row[0]
        uuid = row[22]
        data.append([folio, uuid])
        acumulador1 += 1
        
with open(r'C:\ProduccionRpa\Mendel\Control\Aplicados\folio_gastos_aplicados.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    datos = []
    next(reader)
    for row in reader:
        acumulador2 += 1
        folio = row[0]
        datos.append(folio)

for row in data:
    if row[0] in datos:
        acumulador3 += 1

print(f'Folios Autorizados: {acumulador1}\nFolios aplicados: {acumulador2}\nPorcentaje de avance de folios aplicados: {round((acumulador2/acumulador1)*100)}%')