import datetime, os, csv

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')

def reporte_conciliacion():
    control = r'C:\ProduccionRpa\Mendel\Control'
    datos_limpios = []

    for archivo in os.listdir(f'{reportes}/{hoy}'):
        if archivo.endswith('.csv') and archivo.startswith('Reporte'):
            print(f'{reportes}/{hoy}/{archivo}')
            with open(f'{reportes}/{hoy}/{archivo}', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                encabezado = next(reader)
                for row in reader:
                    fecha = row[1]
                    tipo_pago = row[13]
                    if tipo_pago != 'DECLINED_PAYMENT' and tipo_pago != 'DECLINED_WITHDRAWAL':
                        datos_limpios.append(row)
    return datos_limpios

def convertir_fecha(fecha_str):
    #Convierte una cadena de fecha 'YYYY/MM/DD HH:MM' a un objeto datetime.
    return datetime.datetime.strptime(fecha_str, '%Y/%m/%d %H:%M')

def buscar_duplicados():
    datos = reporte_conciliacion()
    duplicados = []
    transacciones_vistas = {}

    for row in datos:
        if row[11] == 'PHYSICAL_CARD':
            fecha = convertir_fecha(row[1])
            identificador = (row[2], row[4])  # Nombre, Importe

            if identificador in transacciones_vistas:
                # Comprobar si la transacción actual está dentro de los 10 minutos de alguna anterior
                for fecha_previa in transacciones_vistas[identificador]:
                    if abs((fecha - fecha_previa).total_seconds()) <= 600:  # 10 minutos = 600 segundos
                        duplicados.append(row)
                        break
                transacciones_vistas[identificador].append(fecha)
            else:
                transacciones_vistas[identificador] = [fecha]

    return duplicados

def guardar_duplicados():
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion_hoy = fr'{control}\Duplicados\{hoy}'

    duplicados = buscar_duplicados()

    with open(f'{conciliacion_hoy}/Duplicados.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(duplicados)

def carpetas_control():
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion = fr'{control}\Duplicados'
    conciliacion_hoy = fr'{control}\Duplicados\{hoy}'

    if not os.path.exists(conciliacion):
        os.makedirs(conciliacion)
    if not os.path.exists(conciliacion_hoy):
        os.makedirs(conciliacion_hoy)

def main():
    carpetas_control()
    guardar_duplicados()

if __name__ == '__main__':
    main()
