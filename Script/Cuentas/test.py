import os, csv, datetime

##Definir ruta del archivo con las autorizaciones

def leer_documento():
    with open('PagosAceptadosParaPolizas20240321.csv', 'r', encoding='utf-8') as f:
        print('Procesando archivo')
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip header
        data = [row[0] for row in reader]
        return data
        #filtrar_datos(data)

def filtrar_datos(datos):
    autorizados = []
    no_autorizados = []
    for dato in datos:
        if dato[7] == 'Aprobado':
            autorizados.append([dato[1]])  # Aseguramos que cada elemento sea una lista
        else:
            no_autorizados.append(dato)
    # Guardamos los datos autorizados
    with open('autorizados.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(autorizados)
        print('Reporte de autorizados creado con éxito')

def abrir_reporte():
    reportes = r'C:\ProduccionRpa\Mendel\Reportes'
    hoy = datetime.datetime.now().date().strftime('%Y%m%d')

    data = []
    for file in os.listdir(f'{reportes}\{hoy}'):
        if file.endswith('.csv'):
            with open(f'{reportes}\{hoy}\{file}', 'r',encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                data.extend([row for row in reader])
        break
    return data

def buscar_folios():
    folios_set = leer_documento()

    datos = abrir_reporte()
    datos_encontrados = []
    empleados = r'C:\ProduccionRpa\Mendel\Empleados'  # Corregido para ser una ruta de cadena directamente

    if datos:
        for dato in datos:
            folio_dato = dato[0]
            if folio_dato in folios_set:
                nombre = dato[2]
                adjuntos_folder_path = os.path.join(empleados, nombre, 'Adjuntos')  # Corregido para construir correctamente la ruta

                concepto = '*'.join([dato[0], dato[20], dato[3], dato[42]])
                cuenta_mayor = dato[40]
                cuenta_gasto = cuenta_gastos(cuenta_mayor)
                empleado = dato[42]
                cuenta = cuenta_105(empleado)
                pdf = os.path.join(adjuntos_folder_path, dato[25])
                xml = os.path.join(adjuntos_folder_path, dato[26])
                datos_encontrados.append([folio_dato, nombre, concepto, cuenta_gasto, 'cuenta menor de gastos', '105', cuenta, 'total', pdf, xml])

    return datos_encontrados

def cuenta_105(Empleado):
        base_cuenta = '50'
        longitud_total = 6
        longitud_restante = longitud_total - len(base_cuenta) - len(Empleado)
        Cuenta = base_cuenta + '0' * longitud_restante + Empleado
        return Cuenta

def cuenta_gastos(Cuenta_mayor):
    archivo = r'C:\ProduccionRpa\Mendel\Control\Catalogo\cuentas_sucursal.csv'

    with open(archivo, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for cuenta in reader:
            if Cuenta_mayor in cuenta[0]:
                return cuenta[1]
            
def valor_dolar():
    tasa = r'C:\ProduccionRpa\Mendel\Control\tasa_conversion.txt'
    with open(tasa, 'r') as f:
        tasa = f.read()
        return tasa

def buscar_ieps_total(folio):
    reportes = r'C:\ProduccionRpa\Mendel\Reportes'
    hoy = datetime.datetime.now().date().strftime('%Y%m%d')

    for file in os.listdir(f'{reportes}\{hoy}'):
        if file.endswith('.csv'):
            with open(f'{reportes}\{hoy}\{file}', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for dato in reader:
                    if folio == dato[0]:
                        total = dato[4]
                        ieps = dato[32]
                        comercio = dato[10]
                        categoria = dato[20]
                        if ieps == '':
                            ieps = 0.00
                        if total == '':
                            total = 0.00
                        return total, ieps, comercio, categoria
    # Retorna valores por defecto si no se encuentra el folio
    return 0, 0, " "
                        
def validar_propina(total_xml, total_reporte):
    propina = total_reporte - total_xml
    porcentaje = (propina / total_xml) * 100
    if porcentaje > 15:
        propina = total_xml * 0.15
    if propina == -0.01:
        propina = 0.00
    return propina

def crear_tabla():
    data = buscar_folios()
    hoy = datetime.datetime.now().date().strftime('%Y%m%d')
    año = datetime.datetime.now().date().strftime('%Y')
    año = año[2:]
    mes = datetime.datetime.now().date().strftime('%m')
    dia = datetime.datetime.now().date().strftime('%d')
    semana = datetime.datetime.now().date().isocalendar()[1]
    dolar = valor_dolar()
    contador_nombre = 1
    nombre_anterior = None
    dolar = valor_dolar()

    with open('PagosAceptadosParaPolizas20240321.csv', 'r', encoding='utf-8') as f:
        print('Procesando archivo')
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip header
        auditados = [row for row in reader]


    with open('tabla.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Folio', 'Nombre','Referencia', 'Concepto', 'Cuenta Mayor', 'Cuenta Menor','Subtotal S/IVA', 'IVA 16', 'Cuenta Mayor', 'Cuenta gasto', 'IVA 8', 'Cuenta Mayor', 'Cuenta gasto','Dolar','UUID', 'Cuenta 105', 'Complemento 50', 'Total','Propina','IEPS', 'PDF', 'XML'])
        data.sort(key=lambda x: x[1])

        for row in data:
            if nombre_anterior != row[1]:
                if nombre_anterior is not None:  # Si no es la primera iteración, incrementamos el contador
                    contador_nombre += 1
                    nombre_anterior = row[1] 
        
        for row in data:
            folio = row[0]
            # Extraemos datos de la auditoría al XML
            for auditado in auditados:
                if auditado[0] == folio:
                    total_xml = float(auditado[1])
                    subtotal_xml = float(auditado[2])
                    uuid = auditado[3]
                    impuesto_16 = float(auditado[4])
                    impuesto_8 = float(auditado[5])
                    cuenta_menor = 18

                    cuenta_menor_16 = 8 if impuesto_16 > 0 else 0
                    cuenta_menor_8 = 3 if impuesto_8 > 0 else 0 
                    #Traemos el total y el IEPS del reporte
                    datos_reporte = buscar_ieps_total(folio)
                    if datos_reporte:  # Verifica que datos_reporte no sea None
                        comercio = datos_reporte[2]
                        ieps_reporte = float(datos_reporte[1])
                        total_reporte = float(datos_reporte[0])
                        categoria = datos_reporte[3]
                        # Continuamos asumiendo que datos_reporte es válido
                    else:
                        # Manejo del caso en que datos_reporte es None
                        # Por ejemplo, establecer valores por defecto o saltar el procesamiento actual
                        continue  # O manejar de otra forma adecuada

                    if comercio == 'CADENA COMERCIAL OXXO' and ieps_reporte > 0:
                        impuesto_16 = ieps_reporte
                        ieps_reporte = 0

                    elif categoria == 'Supermercados' and ieps_reporte > 0:
                        cuenta_menor_16 = 0
                        cuenta_menor_8 = 0
                        cuenta_menor = 43
                        #En caso de que tenga ieps y no sea OXXO, se va todo a la cuenta mayor de la sucursal y a la cuenta menor 43

                    total_reporte = float(total_reporte)

                    #Validamos la propina haciendo la resta del total del XML y el total del reporte, verificamos si la propina es el 10% o el 15%. En caso de exceder el 15% se toma como propina el 15%
                    propina = validar_propina(total_xml, total_reporte)

                    propina = round(propina, 2)
                    if propina == -0.01:
                        propina = 0.00

            referencia = f'Men{año}{mes}{dia}-{contador_nombre}'
            # Reordenamos los datos para que coincidan con el orden de las columnas y agregamos nuevos datos
            #El 107 pertenece a la cuenta mayor de IVA, la cuenta menor nos dice si es del 16 o el 8
            datos_reordenados = [row[0], row[1], referencia, row[2], row[3], cuenta_menor,subtotal_xml, impuesto_16, '107', cuenta_menor_16, impuesto_8, '107', cuenta_menor_8, dolar, uuid, row[5],row[6], total_xml, propina, ieps_reporte, row[8], row[9]]
            writer.writerow(datos_reordenados)

    print('Tabla creada con éxito')

def main():
    leer_documento()
    crear_tabla()

if __name__ == '__main__':
    main()