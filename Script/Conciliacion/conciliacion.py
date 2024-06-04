
import datetime, os, csv

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')

def reporte_conciliacion():
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion_hoy = fr'{control}\Conciliacion\{hoy}'
    fecha_inicio =  datetime.datetime(2024, 5, 1, 0, 0)
    fecha_fin = datetime.datetime(2024, 5, 31, 23, 59)

    #Abrimos reporte de hoy
    for archivo in os.listdir(f'{reportes}/{hoy}'):
        if archivo.endswith('.csv') and archivo.startswith('Reporte'):
            datos_limpios = []
            print(f'{reportes}/{hoy}/{archivo}')
            with open(f'{reportes}/{hoy}/{archivo}', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                encabezado = next(reader)  # Guarda el encabezado
                for row in reader:
                    fecha = row[1]
                    tipo_pago = row[13]
                    if fecha >= fecha_inicio.strftime('%Y/%m/%d %H:%M') and fecha <= fecha_fin.strftime('%Y/%m/%d %H:%M') and row[15] != '':
                        if '\n' in row[21]:
                            row[21] = row[21].replace('\n', ' ')
                        if tipo_pago != 'DECLINED_PAYMENT' and tipo_pago != 'DECLINED_WITHDRAWAL':
                            datos_limpios.append(row)
                        #datos_limpios.append(row)
            
            nombre_archivo_limpio = f'Conciliado.csv'


            with open(f'{conciliacion_hoy}/{nombre_archivo_limpio}', 'w', newline='', encoding='utf-8') as f_limpio:
                print(f'Creando archivo {nombre_archivo_limpio}')
                writer = csv.writer(f_limpio)
                writer.writerow(encabezado)  # Escribe el encabezado original
                writer.writerows(datos_limpios)

def carpetas_control():
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion = fr'{control}\Conciliacion'
    conciliacion_hoy = fr'{control}\Conciliacion\{hoy}'

    if not os.path.exists(conciliacion):
        os.makedirs(conciliacion)

    if not os.path.exists(conciliacion_hoy):
        os.makedirs(conciliacion_hoy)

def reporte():
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion_hoy = fr'{control}\Conciliacion\{hoy}'
    total_factura = 0

    with open(f'{conciliacion_hoy}/Conciliado.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        encabezado = next(reader)  # Guarda el encabezado
        for row in reader:
            if row[4] != None or row[4] != '':
                #Sumamos los valores de la columna 5
                total_factura += float(row[4])
                total_factura = int(round(total_factura, 2))
                #Formateamos el valor a moneda mexicana
                
    with open(f'{conciliacion_hoy}/Reporte.csv', 'w', newline='', encoding='utf-8') as f:
        header = ['Total importes', 'Total mendel','Diferencia']
        total_mendel = 1331654.99
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow([total_factura, total_mendel, round((total_factura - total_mendel), 2)])

def agregar_folios_noencontrados():
    #Agregamos folios de mendel que no se encontraron en conciliado
    ''

def main():
    carpetas_control()
    reporte_conciliacion()
    reporte()

if __name__ == '__main__':
    main()