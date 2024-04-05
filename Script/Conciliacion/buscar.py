import datetime
import csv

# Configuraciones iniciales
hoy = datetime.datetime.now().date().strftime('%Y%m%d')
nombre_archivo_limpio = 'Conciliado.csv'
control = r'C:\ProduccionRpa\Mendel\Control'
conciliacion_hoy = fr'{control}\Conciliacion\{hoy}'

# Cargar folios de Mendel en un conjunto
folios_mendel = set()
try:
    with open('mendel.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Salta el encabezado
        for row in reader:
            folio = row[0][:8].lower()  # Solo primeros 8 caracteres, en minúsculas
            folios_mendel.add(folio)
except Exception as e:
    print(f"Error al leer el archivo mendel.csv: {e}")
    exit()

# Cargar folios de Conciliado en otro conjunto
folios_conciliado = set()
try:
    with open(f'{conciliacion_hoy}/{nombre_archivo_limpio}', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            folio = row[0][:8].lower()  # Solo primeros 8 caracteres, en minúsculas
            folios_conciliado.add(folio)
except Exception as e:
    print(f"Error al leer el archivo de conciliados: {e}")
    exit()

# Verificar si cada folio de Conciliado existe en Mendel
folios_no_encontrados_en_mendel = [folio for folio in folios_conciliado if folio not in folios_mendel]

# Verificar si cada folio de Mendel existe en Conciliado
folios_no_encontrados_en_conciliado = [folio for folio in folios_mendel if folio not in folios_conciliado]

# Imprimir resultados
if folios_no_encontrados_en_mendel:
    print("Folios de Conciliado no encontrados en Mendel:")
    for folio in folios_no_encontrados_en_mendel:
        print(folio)
else:
    print("Todos los folios de Conciliado fueron encontrados en Mendel.")

if folios_no_encontrados_en_conciliado:
    print("\nFolios de Mendel no encontrados en Conciliado:")
    for folio in folios_no_encontrados_en_conciliado:
        print(folio)
else:
    print("\nTodos los folios de Mendel fueron encontrados en Conciliado.")
