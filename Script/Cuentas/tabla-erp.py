import os, csv, datetime, shutil
import xml.etree.ElementTree as ET

def leer_documento():
    with open('PagosAutorizados.csv', 'r', encoding='utf-8') as f:
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
    subtotal_xml = impuesto_16 = exentos = importe_total = total_xml = impuesto_retenido = impuesto_traslado = propina = uuid = ish = impuesto_8 = cuenta_menor_16 = ieps = resico = cotejo = diferencia = 0.0
    datos = abrir_reporte()
    datos_encontrados = []
    empleados = r'C:\ProduccionRpa\Mendel\Empleados'  # Corregido para ser una ruta de cadena directamente
    categorias_insumos = ['Servicios Gráficos y de Impresión','Honorarios y Servicios Profesionales','Indumentaria','Electrodomésticos','Librerías',
                          'Equipos de Oficina y Suministros','Construcción y Mantenimiento','Servicios de Correo y Carga']

    if datos:
        for dato in datos:
            comercio = dato[3]
            folio_dato = dato[0]
            importe_facturado = dato[30]
            importe_total = float(dato[4])
            categoria = dato[20]

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
                cuenta_menor = 18
                cuenta_menor_8 = 0
                dolar = valor_dolar()
                # Buscamos XML y obtenemos datos del documento
                if dato[26] == '':
                    print('No existe XML')
                    pass
                #elif ##Aquí vamos a validar las categorias con un arreglo de categorias, aquellos que no entren en el arreglo se guardaran para otro documento.
                else:
                    datos_xml = buscar_xml(xml)
                    total_xml = datos_xml[0]
                    subtotal_xml = datos_xml[1]
                    impuesto_16 = datos_xml[2]
                    ieps = datos_xml[3]
                    resico = datos_xml[4]
                    impuesto_traslado = datos_xml[5]
                    uuid = datos_xml[6]
                    impuesto_8 = datos_xml[7]
                    emisor = datos_xml[8]
                    ish = datos_xml[9]
                    
                    # Si el importe trasladado es mayor a 0 el IVA es del 16%
                    if impuesto_traslado > 0:
                        impuesto_16 = impuesto_traslado
                        
                    if categoria == 'Supermercados' and ieps == 0 and impuesto_16 ==  0:
                        cuenta_menor = 99
                    # Si el IEPS retenido es mayor a 0 realizamos operacion aritmetica para calcular impuestos
                    if comercio == 'CADENA COMERCIAL OXXO':
                        print(f'Comercio: {comercio}')
                        print(xml)
                        if ieps > 0:
                            print('Caso 1')
                            print(f'Total: {importe_total} - Subtotal: {subtotal_xml} - IVA 16: {impuesto_16} - IEPS: {ieps} - Exentos: {exentos}')
                            subtotal_xml = impuesto_16 / 0.16 #Base del IVA a la 18
                            subtotal_xml = round(subtotal_xml, 2)
                            exentos = importe_total - (impuesto_16 + subtotal_xml)
                            #print(f'Exentos: {exentos}')
                            #exentos = exentos + ieps
                            #print(f'Exentos + IEPS: {exentos}')
                            ieps = 0.00
                            exentos = round(exentos, 2)
                            cuenta_menor_16 = 8
                            print(f'Total: {importe_total} - Subtotal: {subtotal_xml} - IVA 16: {impuesto_16} - IEPS: {ieps} - Exentos: {exentos}')
                            
                            #pause = input()
                            
                        elif impuesto_8 == 0 and impuesto_16 > 0 and ieps == 0:
                            print('Caso 4')
                            cuenta_menor = 18
                            total_xml = datos_xml[0]
                            subtotal_xml = datos_xml[1]
                            impuesto_16 = datos_xml[2]
                            cuenta_menor_16 = 8
                            print(f'Valores: Total: {importe_total} - Subtotal: {subtotal_xml} - IVA 16: {impuesto_16}')
                            #pause = input()
                            
                        #pause = input('Es oxxo')
                        
                            
                    if comercio != 'CADENA COMERCIAL OXXO':
                        print('No es OXXO')
                        print(f'Comercio: {comercio}')
                        print(xml)
                        
                        # Si el importe facturado es mayor al importe total, se calcula el IVA con el importe total                        
                        """if importe_facturado > importe_total:
                            print(f'Importe facturado mayor al importe total. Comercio: {comercio}')
                            total = total_xml / 1.16
                            total_xml = round(total, 2)
                            impuesto_16 = total * 0.16
                            impuesto_16 = round(impuesto_16, 2)
                            propina = 0.00
                            subtotal_xml = subtotal_xml - impuesto_16
                            print(f'Nuevos valores: Total: {total_xml} - IVA 16: {impuesto_16} - Propina: {propina}')"""
                            
                        #Validamos aquellos que no son oxxo y tienen IEPS
                        if categoria == 'Supermercados' and ieps > 0:
                            print('Caso 2')
                            
                            ieps = 0.00
                            propina = 0.00
                            impuesto_8 = 0.00
                            subtotal_xml = importe_total
                            subtotal_xml = round(subtotal_xml, 2)
                            cuenta_menor_16 = 0
                            cuenta_menor = 43
                            
                        if categoria == 'Restaurantes' and ieps > 0:
                            print('Caso 2.1')
                            
                            ieps = 0.00
                            propina = 0.00
                            impuesto_8 = 0.00
                            impuesto_16 = 0.00
                            subtotal_xml = importe_total
                            subtotal_xml = round(subtotal_xml, 2)
                            cuenta_menor_16 = 0
                            cuenta_menor = 43

                        if categoria == 'Restaurantes' and impuesto_8 > 0:
                            print('Caso 2.2')
                            
                            ieps = 0.00
                            propina = 0.00
                            impuesto_8 = 0.00
                            impuesto_16 = 0.00
                            subtotal_xml = importe_total
                            subtotal_xml = round(subtotal_xml, 2)
                            cuenta_menor_16 = 0
                            cuenta_menor = 43
                            
                        if impuesto_8 > 0 and impuesto_16 == 0:
                            print('Caso 3')
                            cuenta_menor = 43
                            cuenta_menor_16 = 0
                            cuenta_menor_8 = 3
                            
                        if categoria == 'Supermercados' and impuesto_8 > 0:
                            print('Caso 6')
                            cuenta_menor = 43
                            impuesto_8 = 0.00
                            impuesto_16 = 0.00
                            subtotal_xml = importe_total
                            print(f'Importe total: {importe_total} - Subtotal: {subtotal_xml} - IVA 16: {impuesto_16} - IVA 8: {impuesto_8} - Propina: {propina}')
                        
                        if subtotal_xml > 0 and impuesto_16 > 0 and impuesto_8 ==0:
                            print('Caso 7')
                            total_xml = datos_xml[0]
                            subtotal_xml = datos_xml[1]
                            impuesto_16 = datos_xml[2]
                            #pause = input()
                    if categoria == 'Transporte de Pasajeros y Carga':
                        cuenta_menor = 43
                        #pause = input('No es oxxo')
                    
                    #Validamos la propina haciendo la resta del total del XML y el total del reporte, verificamos si la propina es el 10% o el 15%. En caso de exceder el 15% se toma como propina el 15%
                    if importe_total != subtotal_xml:
                        propina,subtotal_xml,impuesto_16 = validar_propina(total_xml, importe_total,subtotal_xml,impuesto_16)
                       
                            
                    propina = round(propina, 2)
                    cotejo = ((subtotal_xml + impuesto_16 + impuesto_8 + ish + exentos + propina + ieps) - resico)
                    cotejo = round(cotejo, 2)
                    diferencia = importe_total - cotejo
                    diferencia = round(diferencia, 2)
                    
                    """if diferencia > 0.0 or diferencia < 0.0:
                        total = total_xml / 1.16
                        #total_xml = round(total, 2)
                        impuesto_16 = total * 0.16
                        impuesto_16 = round(impuesto_16, 2)
                        cotejo = ((subtotal_xml + impuesto_16 + impuesto_8 + ish + exentos + propina) - resico)
                        cotejo = round(cotejo, 2)
                        diferencia = importe_total - cotejo
                        diferencia = round(diferencia, 2)"""
                        
                    total_xml = round(total_xml, 2)
                    subtotal_xml = round(subtotal_xml, 2)
                    ieps = round(ieps, 2)
                    impuesto_16 = round(impuesto_16, 2)
                    impuesto_8 = round(impuesto_8, 2)
                    cuenta_menor_16 = 8 if impuesto_16 > 0 else 0 and impuesto_8 == 0
                    cuenta_menor_8 = 3 if impuesto_8 > 0 else 0 and impuesto_16 == 0
                    
                    direccion_escritorio = r'C:\Users\E-EC1-3752\Desktop\Folios conta'

                    # Definimos una función auxiliar para copiar los archivos PDF y XML
                    #def copiar_archivos(folio_dato, xml, pdf):
                        #directorio_folio = os.path.join(direccion_escritorio, folio_dato)
                        # Verificamos si el directorio existe, si no, lo creamos
                        #if not os.path.exists(directorio_folio):
                            #os.makedirs(directorio_folio)
                        # Copiamos el XML y el PDF al directorio del folio
                        #shutil.copy(xml, directorio_folio)
                        #shutil.copy(pdf, directorio_folio)
                        #print(f'Archivos copiados para el folio: {folio_dato}')

                    # Lógica para determinar si se deben copiar los archivos basada en tus condiciones
                    #if comercio == 'CADENA COMERCIAL OXXO' or comercio == '7-ELEVEN MEXICO' or resico > 0 or ish > 0:
                        # Solo intentamos copiar si ambos archivos, PDF y XML, están presentes
                        #if os.path.isfile(xml) and os.path.isfile(pdf):
                            #copiar_archivos(folio_dato, xml, pdf)
                        #else:
                            #print(f'No se encontraron archivos para copiar: Folio {folio_dato}')
                    if folio_dato == 'E7BC54B9':
                        print(f'Folio: {folio_dato} - Nombre: {nombre} - Concepto: {concepto} - Cuenta Mayor: {cuenta_mayor} - Cuenta Menor: {cuenta_menor} - Subtotal: {subtotal_xml} - IVA 16: {impuesto_16} - Cuenta Mayor: {cuenta_mayor} - Cuenta Menor: {cuenta_menor_16} - IVA 8: {impuesto_8} - Cuenta Mayor: {cuenta_mayor} - Cuenta Menor: {cuenta_menor_8} - Propina: {propina} - IEPS: {ieps} - Resico: {resico} - Exentos: {exentos} - ISH: {ish} - Total: {total_xml} - Cotejo: {cotejo} - Diferencia: {diferencia} - Dolar: {dolar} - UUID: {uuid} - Cuenta 105: {cuenta} - Complemento 50: {comercio} - PDF: {pdf} - XML: {xml}')
                        pause = input()
                    datos_encontrados.append([folio_dato, nombre, concepto, cuenta_gasto, cuenta_menor, subtotal_xml, impuesto_16, '107', cuenta_menor_16, impuesto_8, '107', cuenta_menor_8, propina, ieps, resico, exentos, ish, importe_total, cotejo, diferencia, dolar, uuid, '105', cuenta, pdf, xml])
                    subtotal_xml = impuesto_16 = exentos = importe_total = total_xml = impuesto_retenido = impuesto_traslado = propina = uuid = ish = impuesto_8 = cuenta_menor_16 = ieps = resico = cotejo = diferencia = 0.0
                    pass
                    
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

def validar_propina(total_xml, total_reporte,subtotal_xml,impuesto_16):
    print('Propinas')
    total_xml = float(total_xml)
    total_reporte = float(total_reporte)
    propina = total_reporte - total_xml
    print(propina)
    porcentaje = (propina / total_xml) * 100
    
    if porcentaje > 16:
        propina = total_xml * 0.16
    if propina == -0.01:
        propina = 0.00
    if propina < -1:
        subtotal_xml = total_reporte / 1.16
        impuesto_16 = subtotal_xml * 0.16
        impuesto_16 = round(impuesto_16, 2)
        propina = 0.00    
    
    
    return propina, subtotal_xml, impuesto_16
   
def buscar_xml(ruta, nivel=0):
    # Lee el archivo XML
    arbol = ET.parse(ruta)
    raiz = arbol.getroot()
    total = subtotal = impuesto_16 = ieps = impuesto_retenido = impuesto_traslado = uuid = rfc_emisor = nombre_emisor = impuesto_8 = emisor = descuentos = ish = 0.0
    
    # Define el espacio de nombres
    ns = '{http://www.sat.gob.mx/cfd/4}'
    tfd_ns = '{http://www.sat.gob.mx/TimbreFiscalDigital}'
    implocal_ns = '{http://www.sat.gob.mx/implocal}' 
    
    # Función interna para procesar los elementos
    def procesar_elemento(elemento, nivel):
        nonlocal total, subtotal, impuesto_16, ieps, impuesto_retenido, impuesto_traslado, uuid, rfc_emisor, nombre_emisor, impuesto_8, emisor, descuentos, ish

        espacios = "  " * nivel

        if elemento.tag == f'{ns}Comprobante':
            total = float(elemento.attrib.get('Total', '0'))
            subtotal = float(elemento.attrib.get('SubTotal', '0'))
            descuentos = float(elemento.attrib.get('Descuento', '0'))
            if descuentos > 0:
                subtotal -= descuentos
            impuestos_elemento = elemento.find(f'{ns}Impuestos')
            if impuestos_elemento is not None:
                impuesto_retenido = float(impuestos_elemento.attrib.get('TotalImpuestosRetenidos', '0.0'))
                impuesto_traslado = float(impuestos_elemento.attrib.get('TotalImpuestosTrasladados', '0.0'))
            # Busca el elemento Complemento y luego TimbreFiscalDigital para el UUID
            complemento = elemento.find(f'{ns}Complemento')
            if complemento is not None:
                tfd = complemento.find(f'{tfd_ns}TimbreFiscalDigital')
                if tfd is not None:
                    uuid = tfd.attrib.get('UUID', '')
            emisor = elemento.find(f'{ns}Emisor')
            if emisor is not None:
                rfc_emisor = emisor.attrib.get('Rfc', '')
                nombre_emisor = emisor.attrib.get('Nombre', '')
            
        elif elemento.tag == f'{ns}Concepto':
            descripcion = elemento.attrib.get('Descripcion')
            importe_concepto = elemento.attrib.get('Importe')

            # Busca dentro del elemento Concepto los impuestos
            impuestos_elemento = elemento.find(f'{ns}Impuestos')
            if impuestos_elemento is not None:
                traslados_elemento = impuestos_elemento.find(f'{ns}Traslados')
                if traslados_elemento is not None:
                    for traslado in traslados_elemento.findall(f'{ns}Traslado'):
                        base = float(traslado.attrib.get('Base'))
                        impuesto = traslado.attrib.get('Impuesto')
                        tipo_factor = traslado.attrib.get('TipoFactor')
                        if tipo_factor == 'Exento':
                            impuesto_16 = 0.0
                            ieps = 0.0
                            continue
                        tasa_o_cuota = traslado.attrib.get('TasaOCuota')
                        importe = float(traslado.attrib.get('Importe'))
                        if nombre_emisor == 'CADENA COMERCIAL OXXO':
                            if impuesto == '002':
                                print(f'Importes: {importe}')
                                impuesto_16 += importe
                            elif impuesto == '003':
                                ieps += importe
                        if nombre_emisor != 'CADENA COMERCIAL OXXO':
                            if impuesto == '002':
                                impuesto_16 += importe
                            elif impuesto == '003':
                                ieps += importe
        elif elemento.tag == f'{implocal_ns}ImpuestosLocales':
            traslados_locales = elemento.findall(f'{implocal_ns}TrasladosLocales')
            for traslado in traslados_locales:
                if traslado.attrib.get('ImpLocTrasladado') == 'ISH' or traslado.attrib.get('ImpLocTrasladado') == 'IMPUESTO POR SERVICIOS DE HOSPEDAJE' or traslado.attrib.get('ImpLocTrasladado') == 'I.S.H.' or traslado.attrib.get('ImpLocTrasladado') == 'Impuesto Sobre Hospedaje':
                    ish += float(traslado.attrib.get('Importe', '0.0'))
                if traslado.atrib.get('ImpLocTrasladado') == 'ISA':
                    ish += float(traslado.attrib.get('Importe', '0.0'))
                if traslado.atrib.get('ImpLocTrasladado') == 'DSA':
                    ish += float(traslado.attrib.get('Importe', '0.0'))
        # Itera sobre los subelementos del elemento actual
        for subelemento in elemento:
            procesar_elemento(subelemento, nivel + 1)

    # Inicia el procesamiento desde la raíz
    procesar_elemento(raiz, nivel)

    return total, subtotal, impuesto_16, ieps, impuesto_retenido, impuesto_traslado, uuid, impuesto_8, emisor, ish

def crear_tabla():
    archivos = 0 #Incrementador para ver cuantos archivos procesamos
    
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
    base_path = fr'C:\ProduccionRpa\Mendel\Control\Tabla'
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    daily_path = os.path.join(base_path, hoy)
    if not os.path.exists(daily_path):
        os.makedirs(daily_path)
    

    with open(fr'{daily_path}\tabla2-test.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Folio', 'Nombre','Referencia', 'Concepto', 'Cuenta Mayor', 'Cuenta Menor','Subtotal S/IVA (18)', 'IVA 16 (107-8)', 'Cuenta Mayor', 'Cuenta gasto', 'IVA 8 (107-3)', 'Cuenta Mayor', 'Cuenta gasto','Propina (43)','IEPS (43)', 'Resico (203-000026)','Exentos (99)', 'ISH', 'Total','COTEJO','Diferencia','Dolar','UUID', 'Cuenta 105', 'Complemento 50', 'PDF', 'XML'])
        data.sort(key=lambda x: x[1])

        for row in data:
            #print(f'Archivo numero: {archivos}')
            referencia = f'Men{año}{mes}{dia}-{contador_nombre}'
            # Reordenamos los datos para que coincidan con el orden de las columnas y agregamos nuevos datos
            #El 107 pertenece a la cuenta mayor de IVA, la cuenta menor nos dice si es del 16 o el 8
            """if row[0] == 'B83160F1':

                print(f'Folio: {row[0]} - Nombre: {row[1]} - Concepto: {row[2]} - Cuenta Mayor: {row[3]} - Cuenta Menor: {row[4]} - Subtotal: {row[5]} - IVA 16: {row[6]} - Cuenta Mayor: {row[7]} - Cuenta Menor: {row[8]} - IVA 8: {row[9]} - Cuenta Mayor: {row[10]} - Cuenta Menor: {row[11]} - Propina: {row[12]} - IEPS: {row[13]} - Resico: {row[14]} - Exentos: {row[15]} - ISH: {row[16]} - Total: {row[17]} - Cotejo: {row[18]} - Diferencia: {row[19]} - Dolar: {row[20]} - UUID: {row[21]} - Cuenta 105: {row[22]} - Complemento 50: {row[23]} - PDF: {row[24]} - XML: {row[25]}')
                
                pause = input()
            if row[0] == '8875482D':
                print(f'Folio: {row[0]} - Nombre: {row[1]} - Concepto: {row[2]} - Cuenta Mayor: {row[3]} - Cuenta Menor: {row[4]} - Subtotal: {row[5]} - IVA 16: {row[6]} - Cuenta Mayor: {row[7]} - Cuenta Menor: {row[8]} - IVA 8: {row[9]} - Cuenta Mayor: {row[10]} - Cuenta Menor: {row[11]} - Propina: {row[12]} - IEPS: {row[13]} - Resico: {row[14]} - Exentos: {row[15]} - ISH: {row[16]} - Total: {row[17]} - Cotejo: {row[18]} - Diferencia: {row[19]} - Dolar: {row[20]} - UUID: {row[21]} - Cuenta 105: {row[22]} - Complemento 50: {row[23]} - PDF: {row[24]} - XML: {row[25]}')
                
                pause = input()"""     
            datos_reordenados = [row[0], row[1], referencia, row[2], row[3], row[4],row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12],row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24],row[25]]
            writer.writerow(datos_reordenados)
            archivos += 1
            

    print('Tabla creada con éxito')

def verificacion_cuentas():
    hoy = datetime.datetime.now().date().strftime('%Y%m%d')
    
    base_path = fr'C:\ProduccionRpa\Mendel\Control\Tabla'
    daily_path = os.path.join(base_path, hoy)
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
    # Leer tabla
    with open(fr'{daily_path}\tabla2-test.csv', 'r', encoding='utf-8') as f:
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
                                    #print(f'Actualización realizada. Nueva cuenta menor: {row[5]} - Cuenta menor original: {cuenta_menor_original} - Nombre: {nombre} - Empleado: {empleado} - Descripcion: {descripcion}')
            data.append(row)
                                     # Reescribir tabla con los datos actualizados
    with open(fr'{daily_path}\tabla2-test.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # Escribir encabezado
        writer.writerows(data)  # Escribir datos actualizados
        
def cargar_folios_existentes(archivo):
    folios = set()
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Omitir los encabezados si existen
            for row in reader:
                folios.add(row[0])  # Asumiendo que el folio es la primera columna
    return folios

def crear_archivos():
       
    hoy = datetime.datetime.now().date().strftime('%Y%m%d')
    basepath = fr'C:\ProduccionRpa\Mendel\Control\Tabla'
    dailypath = os.path.join(basepath, hoy)
    año = datetime.datetime.now().date().strftime('%Y')[2:]  # Obtener el año en formato corto
    mes = datetime.datetime.now().date().strftime('%m')      # Mes actual
    dia = datetime.datetime.now().date().strftime('%d')      # Día actual

    archivo_actual = None
    writer = None
    nombre_anterior = None
    contador_nombre = 0  # Inicializar el contador de nombres

    base_path = fr'C:\ProduccionRpa\Mendel\Control\Polizas'
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    daily_path = os.path.join(base_path, hoy)
    if not os.path.exists(daily_path):
        os.makedirs(daily_path)
    
    # Cargar folios ya aplicados o no aplicados
    aplicados = cargar_folios_existentes(fr'C:\ProduccionRpa\Mendel\Control\Aplicados\folio_gastos_aplicados.csv')
    no_aplicados = cargar_folios_existentes(fr'C:\ProduccionRpa\Mendel\Control\Aplicados\folio_gastos_no_aplicados.csv')
    folios_existentes = aplicados.union(no_aplicados)

    with open(fr'{dailypath}\tabla2-test.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Leer y omitir los encabezados si es necesario
        
        for row in reader:
            folio = row[0]
            if folio in folios_existentes:
                continue  # Ignorar folios que ya están en aplicados o no aplicados

            nombre = row[1]
            if nombre != nombre_anterior:
                if archivo_actual:
                    archivo_actual.close()  # Cerrar el archivo anterior si existe

                archivo = os.path.join(daily_path, f'{nombre}.csv')
                archivo_actual = open(archivo, 'w', newline='', encoding='utf-8')  # Abrir nuevo archivo
                writer = csv.writer(archivo_actual)
                writer.writerow(headers)  # Escribir encabezados en cada archivo nuevo
                contador_nombre += 1  # Incrementar el contador solo si el nombre cambia
                print(f'Archivo {archivo} creado con éxito.')
            
            referencia = f'Men{año}{mes}{dia}-{contador_nombre}'
            
            # Resto de campos como antes
            fields = row[3:25]  # Asumiendo que todas las columnas restantes deben ser escritas tal cual
            
            # Escribir fila en el archivo correspondiente
            writer.writerow(row[0:2] + [referencia] + row[3:27])
            
            nombre_anterior = nombre  # Actualizar el nombre anterior

        if archivo_actual:
            archivo_actual.close() 
def main():
    crear_tabla()
    verificacion_cuentas()
    crear_archivos()
    
if __name__ == '__main__':
    main()