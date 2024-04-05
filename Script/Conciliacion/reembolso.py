import datetime, os, csv

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')

def reporte_conciliacion():
    control = r'C:\ProduccionRpa\Mendel\Control'
    datos_limpios = []

    # Abrimos reporte de hoy
    for archivo in os.listdir(f'{reportes}/{hoy}'):
        if archivo.endswith('.csv') and archivo.startswith('Reporte'):
            print(f'{reportes}/{hoy}/{archivo}')
            with open(f'{reportes}/{hoy}/{archivo}', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                encabezado = next(reader)  # Guarda el encabezado
                for row in reader:
                    fecha = row[1]
                    tipo_pago = row[13]
                    if tipo_pago != 'DECLINED_PAYMENT' and tipo_pago != 'DECLINED_WITHDRAWAL':
                        datos_limpios.append(row)
    return datos_limpios

#Extraemos y guardamos datos donde tipo es igual a REFUND
def reembolso():
    datos = reporte_conciliacion()
    reembolsos = []

    for row in datos:
        if row[13] == 'REFUNDED':
            reembolsos.append(row)

    return reembolsos

def guardar_duplicados():
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion_hoy = fr'{control}\Duplicados\{hoy}'

    reembolsados = reembolso()

    with open(f'{conciliacion_hoy}/Reembolos.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(reembolsados)

def main():
    guardar_duplicados()

if __name__ == '__main__':
    main()