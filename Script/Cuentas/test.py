import os, csv, datetime

"""def leer_documento():
    with open('PagosAceptadosParaPólizas20240327.csv', 'r', encoding='utf-8') as f:
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
                        comercio = dato[3]
                        categoria = dato[20]
                        recico = dato[35]
                        ish = dato[33]
                        importe_facturado = dato[30]
                        if importe_facturado == '':
                            importe_facturado = 0.00
                        if recico == '' and ish == '':
                            recico = 0.00
                            ish = 0.00
                        if ieps == '':
                            ieps = 0.00
                        if total == '':
                            total = 0.00
                        return total, ieps, comercio, categoria, recico, ish, importe_facturado
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

def buscar_cuenta_menor(departamento):
    control = r'C:\ProduccionRpa\Mendel\Control\Catalogo'

    with open(fr'{control}\{departamento}.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        cuenta = [row for row in reader]
        return cuenta

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


    with open('PagosAceptadosParaPólizas20240327.csv', 'r', encoding='utf-8') as f:
        print('Procesando archivo')
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip header
        auditados = [row for row in reader]


    with open('tabla.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Folio', 'Nombre','Referencia', 'Concepto', 'Cuenta Mayor', 'Cuenta Menor','Subtotal S/IVA', 'IVA 16', 'Cuenta Mayor', 'Cuenta gasto', 'IVA 8', 'Cuenta Mayor', 'Cuenta gasto','Dolar','UUID', 'Cuenta 105', 'Complemento 50', 'Total','Propina','IEPS', 'Recico', 'ISH', 'PDF', 'XML'])
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
                    subtotal_xml = float(auditado[2]) # Verificar descuentos existentes en el XML y aplicarlos al subtotal.
                    uuid = auditado[3]
                    impuesto_16 = float(auditado[4])
                    impuesto_8 = float(auditado[5])
                    cuenta_menor = 18

                    cuenta_menor_16 = 8 if impuesto_16 > 0 else 0 and impuesto_8 == 0
                    cuenta_menor_8 = 3 if impuesto_8 > 0 else 0 and impuesto_16 == 0

                    #Traemos el total y el IEPS del reporte
                    datos_reporte = buscar_ieps_total(folio)
                    if datos_reporte:  # Verifica que datos_reporte no sea None
                        comercio = datos_reporte[2]
                        ieps_reporte = float(datos_reporte[1])

                        total_reporte = float(datos_reporte[0])
                        categoria = datos_reporte[3]
                        recico = datos_reporte[4]
                        ish = datos_reporte[5]
                        importe_facturado = float(datos_reporte[6])

                        # Continuamos asumiendo que datos_reporte es válido
                    else:
                        # Manejo del caso en que datos_reporte es None
                        # Por ejemplo, establecer valores por defecto o saltar el procesamiento actual
                        continue  # O manejar de otra forma adecuada

                    if comercio == 'CADENA COMERCIAL OXXO' and ieps_reporte > 0:
                        subtotal_xml = impuesto_16 / 0.16 #Base del IVA a la 18
                        subtotal_xml = round(subtotal_xml, 2)
                        ieps_reporte = total_xml - (impuesto_16 + subtotal_xml) #Falta validar.
                        ieps_reporte = round(ieps_reporte, 2)                        
                        impuesto_8 = 0.00
                        cuenta_menor_8 = 0


                    elif categoria == 'Supermercados' and ieps_reporte > 0 and not comercio == 'CADENA COMERCIAL OXXO':
                        ieps_reporte = 0.00
                        propina = 0.00
                        impuesto_8 = 0.00
                        subtotal_xml = total_xml
                        subtotal_xml = round(subtotal_xml, 2)
                        cuenta_menor_16 = 0
                        cuenta_menor_8 = 0
                        cuenta_menor = 43
                    
                    if categoria == 'Supermercados' and ieps_reporte == 0 and impuesto_16 ==  0:
                        cuenta_menor = 99

                    if ieps_reporte > 0 and not categoria == 'Supermercados':
                        subtotal_xml = total_xml
                        cuenta_menor = 99
                        ieps_reporte = 0.00
                        propina = 0.00
                        impuesto_8 = 0.00
                        cuenta_menor_16 = 0
                        cuenta_menor_8 = 0
                            
                    # Agregar validación cuando la factura es mayor que el importe pagado, cuando nos da propina negativa el total de la factura lo dividimos entre 0.16 y el resultado lo multiplicamos por 0.16
                    if importe_facturado > total_reporte:
                        total_xml = total_xml / 1.16
                        total = round(total_xml, 2)
                        impuesto_16 = total * 0.16
                        impuesto_16 = round(impuesto_16, 2)
                        propina = 0.00
                        #En caso de que tenga ieps y no sea OXXO, se va todo a la cuenta mayor de la sucursal y a la cuenta menor 43
                    total_reporte = float(total_reporte)

                    #Validamos la propina haciendo la resta del total del XML y el total del reporte, verificamos si la propina es el 10% o el 15%. En caso de exceder el 15% se toma como propina el 15%
                    propina = validar_propina(total_xml, total_reporte)

                    propina = round(propina, 2)
                    if propina == -0.01:
                        propina = 0.00
                    elif propina == 0.01:
                        propina = 0.00
                    
                    # Redondeamos todas nuestras variables a 2 decimales
                    total_xml = round(total_xml, 2)
                    total_reporte = round(total_reporte, 2)
                    subtotal_xml = round(subtotal_xml, 2)
                    impuesto_16 = round(impuesto_16, 2)
                    impuesto_8 = round(impuesto_8, 2)
                    ieps_reporte = round(ieps_reporte, 2)


            referencia = f'Men{año}{mes}{dia}-{contador_nombre}'
            # Reordenamos los datos para que coincidan con el orden de las columnas y agregamos nuevos datos
            #El 107 pertenece a la cuenta mayor de IVA, la cuenta menor nos dice si es del 16 o el 8
            datos_reordenados = [row[0], row[1], referencia, row[2], row[3], cuenta_menor,subtotal_xml, impuesto_16, '107', cuenta_menor_16, impuesto_8, '107', cuenta_menor_8, dolar, uuid, row[5],row[6], total_xml, propina, ieps_reporte, recico, ish, row[8], row[9]]
            writer.writerow(datos_reordenados)

    print('Tabla creada con éxito')

def verificacion_cuentas():
    cuenta_sucursal = [561,562,563,565,566,567,571,581,582,591,592,953,594,595,597,598,599,600,601,602]

    datos_reporte = abrir_reporte()

    control = r'C:\ProduccionRpa\Mendel\Control\Catalogo'

    # Descripciones de cada departamento
    administrativo = ['GERENTE SUC GUADALAJARA','GERENTE SUC MEXICO','GERENTE SUCURSAL PUEBLA','GERENTE SUCURSAL CULIACAN','GERENTE DE SUCURSAL VERACRUZ',
                      'GERENTE DE SUCURSAL MERIDA','GERENTE SUC MONTERREY','GERENTE SUCURSAL QUERETARO','GERENTE SUCURSAL TEPOTZOTLAN','GERENTE SUCURSAL VILLAHERMOSA',
                      'GERENTE DE SUCURSAL TOLUCA','GERENTE SUCURSAL TORREON','GERENTE SUCURSAL CD JUAREZ','GERENTE SUC MEXICO','GERENTE SUCURSAL HERMOSILLO',
                      'GERENTE SUCURSAL TIJUANA','GERENTE SUCURSAL SAN LUIS POTOSI','GERENTE DE SUCURSAL CANCUN','GERENTE DE SUCURSAL LEON','COLABORADOR ADMINISTRATIVO']
    
    ventas = ['EJEC VTAS SEGURIDAD', 'EJEC VTAS RADIOCOM', 'EJEC VTAS DESARROLLO DE NEGOCIOS', 'COLABORADOR DE VTAS SEGURIDAD', 'COLABORADOR DE VTAS RADIOCOMUNICACION',
              'EJEC DE CUENTAS CLAVE']
    
    almacen = ['COLABORADOR DE ALMACEN','COLABORADOR DE ALMACEN MXS', 'LIDER DE ALMACEN', 'AUDITOR DE ALMACEN']
    
    soporte = ['INGENIERO DE SOPORTE', 'INGENIERO DE CUMPLIMIENTO', 'INGENIERO DE IMPLEMENTACION','PRODUCT MANAGER','JEFE DE INGENIERIA INDUSTRIAL',
               'JEFE ADMVO DE CENTRO DE SERVICIOS']

    # Leer Empleados.csv
    with open(fr'{control}\Empleados.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Omitir encabezado
        cuentas = [row for row in reader]

    data = []
    # Leer tabla.csv
    with open('tabla.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Guardar encabezado
        for row in reader:
            cuenta_mayor = int(row[4])
            if cuenta_mayor in cuenta_sucursal:
                for datos in datos_reporte:
                    if datos[0] == row[0]:
                        empleado = datos[42]
                        nombre = datos[2]
                        for cuenta in cuentas:
                            if empleado == cuenta[3]:
                                descripcion = cuenta[2]
                                if int(cuenta[0]) in cuenta_sucursal:
                                    cuenta_menor_original = row[5]
                                    if descripcion in ventas:
                                        row[5] = '10' + cuenta_menor_original
                                    elif descripcion in administrativo:
                                        row[5] = '20' + cuenta_menor_original
                                    elif descripcion in almacen:
                                        row[5] = '30' + cuenta_menor_original
                                    elif descripcion in soporte:
                                        row[5] = '40' + cuenta_menor_original
                                    print(f'Actualización realizada. Nueva cuenta menor: {row[5]}')
            data.append(row)
                                     # Reescribir tabla.csv con los datos actualizados
    with open('tabla.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # Escribir encabezado
        writer.writerows(data)  # Escribir datos actualizados


def main():
    leer_documento()
    crear_tabla()
    verificacion_cuentas()

if __name__ == '__main__':
    main()"""

folios = ["BC5AE055","ACC1BAC2","26A16A3D","234A0DB0","4C6E8531","91BB4F8A","9006E8AE","3B7B8B79","2333A13D","C5DE7BBD","0A79FB07","511DE6DC",
          "6F387B1D","88CF6D80","A6CFD668","B257B964","EA59036C","4F5413F2","BAF38B31","FCAB1CE3","EF3D39CF","2FD6F8F9","8FC2BE54","E87AA2F2",
          "58850424","E970944C","9E9B0FBE","7AE3AD0E","101FD81E","C4A91648","603E0D5B","3BD599BE","0FD9CE59","88ADD000","9DAA49C0","5F61F021",
          "7E9B2FC2","63706658","66160F16","25038008","D3FB74A5","6D276605","CCC4A673","C1A61B56","58D7267C","00568A4A","E3112D91","70A20139",
          "0B20FC09","AF13F713","D927590E","A7E5C16D","D8A6132F","218256C5","E4208C18","70F2FE90","24D2D57B","3549C344","70B1B9A0","549DA93C",
          "781E67E9","94214B40","ABFD69A0","481CB751","A44ED118","CD0989A6","EA2253E8","515E02F5","01BB1308","8691F4D1","1DF40822","524EB608",
          "1A444C8E","4A6A9AE9","724CE971","86F47A9F","64FC4353","089ED010","35668137","16A1603E","05E76ECB","3EDFEBA1","82204A16","69D8CA22",
          "DA24A965","D58D479F","7D5AD344","99908E7C","18353135","61473AF9","3EEECB6F","70C0300A"]    
    
uuid_list = []
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
    next(reader)
    for row in reader:
        folios.append(row[0])
        acumulador2 += 1

for row in data:
    if row[0] in folios:
        acumulador3 += 1

print(f'Folios Autorizados: {acumulador1}\nFolios aplicados: {acumulador2}\nPorcentaje de avance de folios aplicados: {round((acumulador3/acumulador1)*100)}%')