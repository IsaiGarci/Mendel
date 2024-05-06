from collections import defaultdict
import datetime
import pandas as pd
import csv
import os
import sys

# Asegura que Python pueda encontrar el módulo DOF.py añadiendo su directorio al sys.path
sys.path.append(r'C:\ProduccionRpa\Mendel\Script\Tasa')
sys.path.append(r'C:\ProduccionRpa\Mendel\Script\Formato')

# Ahora importa la función o clase DOF desde el módulo DOF.py
from DOF import DOF
from Formato_archivo import Formato_archivo as formatear

# Rutas de archivos y carpetas
hoy = datetime.datetime.now().date().strftime('%Y%m%d')
numero_semana = datetime.datetime.now().isocalendar()[1]
año = str(datetime.datetime.now().year)[-2:]
dia = datetime.datetime.now().day
mes = datetime.datetime.now().month

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
empleados = r'C:\ProduccionRpa\Mendel\Empleados'
tasa = r'C:\ProduccionRpa\Mendel\Control\tasa_conversion.txt'
archivo_control_adjuntos = r'C:\ProduccionRpa\Mendel\Control\Adjuntos'
archivo_control_correos = r'C:\ProduccionRpa\Mendel\Control\Correos'
archivo_control_diarios = r'C:\ProduccionRpa\Mendel\Control\Diario'
archivo_control_externos = r'C:\ProduccionRpa\Mendel\Control\PagosExternos'
control = r'C:\ProduccionRpa\Mendel\Control'
correos_path = r'C:\ProduccionRpa\Mendel\Correo'
catalogo = r'C:\ProduccionRpa\Mendel\Control\Catalogo\catalogo_cuentas.csv'



if os.path.exists(f'{control}\Diario\control_{hoy}.csv'):
    os.remove(f'{control}\Diario\control_{hoy}.csv')
    #Volvemos a crear el archivo
    with open(f'{control}\Diario\control_{hoy}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

if os.path.exists(f'{control}\Adjuntos\control_adjuntos_{hoy}.csv'):
    os.remove(f'{control}\Adjuntos\control_adjuntos_{hoy}.csv')
    #Volvemos a crear el archivo
    with open(f'{control}\Adjuntos\control_adjuntos_{hoy}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

if os.path.exists(f'{control}\Correos\control_correos_{hoy}.csv'):
    os.remove(f'{control}\Correos\control_correos_{hoy}.csv')
    #Volvemos a crear el archivo
    with open(f'{control}\Correos\control_correos_{hoy}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

if not os.path.exists(f'{control}\PagosExternos\pagos_externos_{hoy}.csv'):
    with open(f'{control}\PagosExternos\pagos_externos_{hoy}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

def carpetas_control():
    os.makedirs(f'{control}\Diario', exist_ok=True)
    os.makedirs(f'{control}\Adjuntos', exist_ok=True)
    os.makedirs(f'{control}\Correos', exist_ok=True)
    os.makedirs(f'{control}\ReporteGeneral', exist_ok=True)
    os.makedirs(f'{control}\PagosExternos', exist_ok=True)

def leer_tasa_conversion():
    DOF()
    with open(tasa, 'r') as file:
        return float(file.read().strip())

def leer_reporte():
    data = []
    for file in os.listdir(f'{reportes}\{hoy}'):
        if file.endswith('.csv'):
            with open(f'{reportes}\{hoy}\{file}', 'r',encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                data.extend([row for row in reader])
    return data


def calcular_dls(valor, tasa_conversion):
    return round(float(valor) / tasa_conversion, 2)

def calcular_pesos(valor, tasa_conversion):
    return round(float(valor) * tasa_conversion, 2)

def obtener_dias_semana(fecha):
    lunes = fecha - datetime.timedelta(days=fecha.weekday())
    return [lunes + datetime.timedelta(days=d) for d in range(7)]

def obtener_domingo(fecha):
    return fecha + datetime.timedelta(days=(6-fecha.weekday()) % 7)

def crear_data(tasa_conversion):
    empleados_data = {}
    adjuntos_data = {}

    folios_aplicados = set()
    
    with open(f'{control}/polizas_aplicadas.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            folios_aplicados.add(row[0])

    for row in leer_reporte():
        Folio = row[0]
        Empleado = row[42]
        Nombre = row[2]
        Concepto = '*'.join([row[0], row[20], row[3]])
        Fecha_str = row[1][:10]
        Moneda = row[5]
        Adjunto_pdf = row[25]
        Adjunto_xml = row[26]
        Correo = row[41]
        Comercio = row[3]
        Autorizacion = row[47]
        Cargo = row[4]
        Cargo = float(Cargo) if Cargo else 0.00
        Cargo = round(Cargo, 2)

        if Folio in folios_aplicados:
            continue
        else:
            folios_aplicados.add(Folio)
                    
        if Nombre not in adjuntos_data:
            adjuntos_data[Nombre] = []
        adjuntos_data[Nombre].append([Adjunto_pdf, Adjunto_xml, Fecha_str, Correo, Comercio, Autorizacion])

        base_cuenta = '10550'
        longitud_total = 9
        longitud_restante = longitud_total - len(base_cuenta) - len(Empleado)
        Cuenta = base_cuenta + '0' * longitud_restante + Empleado

        ## Validamos el tipo de moneda para hacer la conversión a DLS o pesos mexicanos
        if Moneda == 'MXN':
            #print(f'El empleado {Nombre} tiene un cargo de {Cargo} en pesos mexicanos')
            if Cargo:
                Cargo_DLS = calcular_dls(Cargo, tasa_conversion)
                Cargo_DLS = round(Cargo_DLS, 2)
                data_cargo = ['201031417', 'D', Fecha_str, f'S{numero_semana}V{año}-{dia}-{mes}', Concepto, '0.00', f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}"]
                data_abono = [Cuenta, 'D', Fecha_str, f'S{numero_semana}V{año}-{dia}-{mes}', Concepto, f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}", '0.00']
                
                if Nombre not in empleados_data:
                    empleados_data[Nombre] = [data_cargo, data_abono]
                else:
                    empleados_data[Nombre].extend([data_cargo, data_abono])
        else:
            #print(f'El empleado {Nombre} tiene un cargo de {Cargo} en dólares')
            if Cargo:
                Cargo_Pesos = calcular_pesos(Cargo, tasa_conversion)
                Cargo_Pesos = round(Cargo_Pesos, 2)
                data_cargo = ['201031417', 'D', Fecha_str, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}"]
                data_abono = [Cuenta, 'D', Fecha_str, f'S{numero_semana}V{año}-{dia}', Concepto, f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}", '0.00']
                
                if Nombre not in empleados_data:
                    empleados_data[Nombre] = [data_cargo, data_abono]
                else:
                    empleados_data[Nombre].extend([data_cargo, data_abono])
    return empleados_data, adjuntos_data

def crear_tabla():
    tasa_conversion = leer_tasa_conversion()  # Lee la tasa de conversión al inicio
    empleados_data, adjuntos_data = crear_data(tasa_conversion)
    header = ['Cuenta', 'Diario', 'Fecha', 'Referencia', 'Concepto', 'Cargo', 'Abono', 'Cargo DLS', 'Abono DLS']

    for folder in os.listdir(empleados):
        try:
            ## Validamos que la carpeta exista, si no existe la creamos
            os.makedirs(fr'{empleados}\{folder}\Adjuntos', exist_ok=True)
            os.makedirs(fr'{empleados}\{folder}\Polizas', exist_ok=True) 
            os.makedirs(fr'{empleados}\{folder}\Correos', exist_ok=True) 
            #pause = input('Presiona enter para continuar')
        except OSError as e:
            print(e)
        
    # Mover la apertura del archivo de control de adjuntos fuera del bucle de empleados
    with open(fr'{archivo_control_adjuntos}\control_adjuntos_{hoy}.csv', 'a', newline='', encoding='utf-8') as archivo_adjuntos:
        writer_adjuntos = csv.writer(archivo_adjuntos)

        for Nombre, data in empleados_data.items():
            # Creación de la ruta del empleado
            empleado_path = os.path.join(empleados, Nombre, 'Polizas')
            #print(f'----{empleado_path}----')
            #pause = input('Presiona enter para continuar')
            # Añadir la creación de la carpeta con la fecha del día dentro de la carpeta del empleado
            fecha_path = os.path.join(empleado_path, hoy)
            os.makedirs(fecha_path, exist_ok=True)  # Asegura que la carpeta de la fecha se cree si no existe
            
            # Ajuste en la ruta del archivo para incluir la carpeta de la fecha
            file_path = os.path.join(fecha_path, f"{Nombre}_{hoy}.csv")

            # Creamos un archivo donde haremos un append de los archivos creados para llevar un control
            with open(f'{archivo_control_diarios}\control_{hoy}.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([file_path])
            
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)

            # Escribir los datos de adjuntos para cada empleado en el archivo de control de adjuntos
            adjuntos_folder_path = fr'{empleados}\{Nombre}\Adjuntos'
            if Nombre in adjuntos_data:  # Verifica si hay adjuntos para este empleado
                for adjunto in adjuntos_data[Nombre]:
                    writer_adjuntos.writerow([adjuntos_folder_path] + adjunto)

def falta_adjuntos():
    with open(fr'{archivo_control_adjuntos}\control_adjuntos_{hoy}.csv', 'r', newline='', encoding='utf-8') as archivo_adjuntos:
        reader_adjuntos = csv.reader(archivo_adjuntos)
        for row in reader_adjuntos:
            #print(row)
            #pause = input('Presiona enter para continuar')
            path = row[0]
            Fecha = datetime.datetime.strptime(row[3], '%Y/%m/%d').date()
            Correo = row[4]
            Comercio = row[5]
            autorizado = row[6]
            dias_transcurridos = (datetime.datetime.now().date() - Fecha).days

            if Fecha < datetime.datetime.now().date() and dias_transcurridos > 7 and autorizado == 'PENDING':
                if row[1] == '' or row[2] == '':
                    # Actualizando el archivo de control de correos
                    with open(fr'{archivo_control_correos}\control_correos_{hoy}.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        if 'Adjuntos' in path:
                            path_temp = path.replace('Adjuntos', 'Correos')
                        writer.writerow([Correo, Fecha.strftime('%Y-%m-%d'), Comercio, dias_transcurridos, path_temp])
                    
                    #print(f'El archivo lleva {dias_transcurridos} dias sin adjuntos, Fila {row}')
                    
                    # Generando la tabla HTML
                    registros_por_correo = defaultdict(list)
                    with open(f'{archivo_control_correos}\\control_correos_{hoy}.csv', 'r', newline='', encoding='utf-8') as archivo:
                        reader = csv.reader(archivo)
                        for row in reader:
                            registros_por_correo[row[0]].append(row)

                    # Crear directorios y tablas HTML por cada empleado
                    for correo, registros in registros_por_correo.items():
                        # Crear o asegurar que exista el directorio para el empleado
                        if 'Adjuntos' in path:
                            path_empleado = path.replace('Adjuntos', 'Correos')
                        os.makedirs(path_empleado, exist_ok=True)
                        
                        # Definir la ruta del archivo HTML
                        archivo_html = os.path.join(path_empleado, f'tabla_{hoy}.txt')
                        
                        # Generar HTML de la tabla
                        tabla_html = """
                <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr>
                    <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Fecha</th>
                    <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Comercio</th>
                    <th style="border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2;">Días Transcurridos</th>
                    </tr>
                </thead>
                <tbody>
                """
                        # Agregar filas a la tabla para cada registro del empleado
                        for registro in registros:
                            fecha, comercio, dias_transcurridos = registro[1], registro[2], registro[3]
                            tabla_html += f"""
                    <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">{fecha}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{comercio}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{dias_transcurridos}</td>
                    </tr>
                """
                        
                        tabla_html += """
                </tbody>
                </table>
                """

                        # Escribir el HTML de la tabla en el archivo
                        with open(archivo_html, 'w', encoding='utf-8') as html_file:
                            html_file.write(tabla_html)
                        
                        #print(f'Tabla HTML guardada: {archivo_html}')

def crear_reporte_general(tasa_conversion):
    reporte_general_data = data_cargo = data_abono = []
    folios_aplicados = set()
    print(f"Total de filas a procesar: {len(leer_reporte())}")
    with open(f'{control}/polizas_aplicadas.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            folios_aplicados.add(row[0])

    for row in leer_reporte():
        Folio = row[0]
        Empleado = row[42]
        Nombre = row[2]
        Concepto = '*'.join([row[0], row[20], row[3], row[42]])
        Fecha_str = row[1][:10]
        Moneda = row[5]
        Adjunto_pdf = row[25]
        Adjunto_xml = row[26]
        Correo = row[41]
        Comercio = row[3]
        Metodo_pago = row[11]
        tipo_pago = row[13]
        Cargo = row[4]
        Cargo = float(Cargo) if Cargo else 0.00
        Cargo = round(Cargo, 2)
        
        if Folio in folios_aplicados:
            continue
        else:
            folios_aplicados.add(Folio)
        
        base_cuenta = '10550'
        longitud_total = 9
        longitud_restante = longitud_total - len(base_cuenta) - len(Empleado)
        Cuenta = base_cuenta + '0' * longitud_restante + Empleado

        Fecha = datetime.datetime.strptime(Fecha_str, '%Y/%m/%d').date()
        
        dias_semana = obtener_dias_semana(Fecha)
        domingo = obtener_domingo(Fecha)
        domingo_str = domingo.strftime('%Y/%m/%d')
        hoy = datetime.datetime.now().date()
        fecha_mes = Fecha.month
        mes_actual = hoy.month
        
        hoy_str = datetime.datetime.now().date().strftime('%Y%m%d')

        # Cálculo de Cargo en Dólares o Pesos según la moneda
        if Moneda == 'MXN':
            Cargo_DLS = calcular_dls(Cargo, tasa_conversion)
            Cargo_Pesos = Cargo
        else:
            Cargo_Pesos = calcular_pesos(Cargo, tasa_conversion)
            Cargo_DLS = Cargo
        condiciones_invalidas = ['EXTERNAL_CARD', 'REFUNDED', 'DECLINED_PAYMENT', 'ADJUSTMENT', 'DECLINED_WITHDRAWAL']
        
        if Metodo_pago in condiciones_invalidas or tipo_pago in condiciones_invalidas:
            with open(f'{control}\PagosExternos\pagos_externos_{hoy_str}.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                if row in reader:
                    continue
                else:
                    with open(f'{control}\PagosExternos\pagos_externos_{hoy_str}.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(row)
            pass
        else:
            # Definición de la estructura de datos
            data_cargo = ['201031417', 'D', domingo_str, Concepto, '0.00', f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo_DLS:.2f}"]
            data_abono = [Cuenta, 'D', domingo_str, Concepto, f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo_DLS:.2f}", '0.00']

        # Agregar datos al reporte
        reporte_general_data.append(data_cargo)
        reporte_general_data.append(data_abono)

    # Ordenar el reporte general por la fecha
    print(f'Fecha en reporte general: {reporte_general_data[2]}')
    reporte_general_data.sort(key=lambda x: datetime.datetime.strptime(x[2], '%Y/%m/%d'))
    print(f"Total de filas agregadas a reporte_general_data: {len(reporte_general_data)}")

    # Separar datos por mes y guardar en archivos correspondientes
    datos_por_mes = {}
    for data in reporte_general_data:
        fecha_str = data[2]  # La fecha está en el índice 2
        fecha = datetime.datetime.strptime(fecha_str, '%Y/%m/%d').date()
        mes = fecha.month

        if mes not in datos_por_mes:
            datos_por_mes[mes] = []
        datos_por_mes[mes].append(data)

    for mes, datos in datos_por_mes.items():
        archivo = f'{control}\\ReporteGeneral\\reporte_general_{hoy_str}-{mes}.csv'
        with open(archivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Cuenta', 'Diario', 'Fecha', 'Concepto', 'Cargo MXN', 'Cargo DLS', 'Abono MXN', 'Abono DLS'])
            writer.writerows(datos)
    reporte_general_data = []

    folios_aplicados = set()
    
    with open(f'{control}/polizas_aplicadas.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            folios_aplicados.add(row[0])

    for row in leer_reporte():
        Folio = row[0]
        Empleado = row[42]
        Nombre = row[2]
        Concepto = '*'.join([row[0], row[20], row[3], row[42]])
        Fecha_str = row[1][:10]
        Moneda = row[5]
        Adjunto_pdf = row[25]
        Adjunto_xml = row[26]
        Correo = row[41]
        Comercio = row[3]
        Metodo_pago = row[11]
        Cargo = row[4]
        tipo_pago = row[13]
        Cargo = float(Cargo) if Cargo else 0.00
        Cargo = round(Cargo, 2)
        
        if Folio in folios_aplicados:
            continue
        else:
            folios_aplicados.add(Folio)
        
        base_cuenta = '10550'
        longitud_total = 9
        longitud_restante = longitud_total - len(base_cuenta) - len(Empleado)
        Cuenta = base_cuenta + '0' * longitud_restante + Empleado

        Fecha = datetime.datetime.strptime(Fecha_str, '%Y/%m/%d').date()
        
        dias_semana = obtener_dias_semana(Fecha)
        domingo = obtener_domingo(Fecha)
        domingo = domingo.strftime('%Y/%m/%d')
        hoy = datetime.datetime.now().date()
        fecha_mes = Fecha.month
        mes_actual = hoy.month
        mes_anterior = mes_actual - 1
        hoy = datetime.datetime.now().date().strftime('%Y%m%d')
        
        condiciones_invalidas = ['EXTERNAL_CARD', 'REFUNDED', 'DECLINED_PAYMENT', 'ADJUSTMENT', 'DECLINED_WITHDRAWAL']
        
        print(f'El método de pago es {Metodo_pago} y el tipo de pago es {tipo_pago}')
        if Metodo_pago in condiciones_invalidas or tipo_pago in condiciones_invalidas:
            with open(f'{control}\PagosExternos\pagos_externos_{hoy}.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                if row in reader:
                    continue
                else:
                    with open(f'{control}\PagosExternos\pagos_externos_{hoy}.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(row)
            pass
        else:
            if fecha_mes == mes_actual:
                if Moneda == 'MXN':
                    Cargo_DLS = calcular_dls(Cargo, tasa_conversion)
                    if f'{Cargo:.2f}'.startswith('-'):
                        cargo = f'{Cargo:.2f}'
                        cargo_dls = f"{Cargo_DLS:.2f}"
                        cargo = cargo.replace('-', '')
                        cargo_dls = cargo_dls.replace('-', '')
                        
                        data_cargo = ['201031417', 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, cargo, '0.00', cargo_dls, '0.00']
                        data_abono = [Cuenta, 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', cargo, '0.00', cargo_dls]

                    else:
                        data_cargo = ['201031417', 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}"]
                        data_abono = [Cuenta, 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}", '0.00']
                    # Nota: Aquí se necesita una lógica para generar la cuenta basada en el empleado o algún criterio específico
                else:
                    Cargo_Pesos = calcular_pesos(Cargo, tasa_conversion)
                    data_cargo = ['201031417', 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}"]
                    # Nota: Aquí se necesita una lógica para generar la cuenta basada en el empleado o algún criterio específico
                    data_abono = [Cuenta, 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}", '0.00']

                reporte_general_data.append(data_cargo)
                reporte_general_data.append(data_abono)

                reporte_general_data.sort(key=lambda x: x[2])  # Asumiendo que el índice 2 es la fecha en formato 'YYYY-MM-DD'

                # Guardar el reporte general ordenado
                with open(fr'{control}\ReporteGeneral\reporte_general_{hoy}-{mes_actual}.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Cuenta', 'Diario', 'Fecha', 'Referencia', 'Concepto', 'Cargo', 'Abono', 'Cargo DLS', 'Abono DLS'])
                    writer.writerows(reporte_general_data)
            elif fecha_mes == mes_anterior:
                if Moneda == 'MXN':
                    Cargo_DLS = calcular_dls(Cargo, tasa_conversion)                        
                    if '-' in f'{Cargo:.2f}':
                        cargo = f'{Cargo:.2f}'
                        cargo_dls = f"{Cargo_DLS:.2f}"
                        cargo = cargo.replace('-', '')
                        cargo_dls = cargo_dls.replace('-', '')
                        data_cargo = ['201031417', 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, cargo, '0.00', cargo_dls, '0.00']
                        data_abono = [Cuenta, 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', cargo, '0.00', cargo_dls]

                    else:
                        data_cargo = ['201031417', 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}"]
                        data_abono = [Cuenta, 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}", '0.00']
                    # Nota: Aquí se necesita una lógica para generar la cuenta basada en el empleado o algún criterio específico
                else:
                    Cargo_Pesos = calcular_pesos(Cargo, tasa_conversion)
                    data_cargo = ['201031417', 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}"]
                    # Nota: Aquí se necesita una lógica para generar la cuenta basada en el empleado o algún criterio específico
                    data_abono = [Cuenta, 'D', domingo, f'S{numero_semana}V{año}-{dia}', Concepto, f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}", '0.00']

                reporte_general_data.append(data_cargo)
                reporte_general_data.append(data_abono)

                reporte_general_data.sort(key=lambda x: x[2])  # Asumiendo que el índice 2 es la fecha en formato 'YYYY-MM-DD'

    datos_por_mes = {}
    for data in reporte_general_data:
        fecha_str = data[2]  # Asumimos que el índice 2 es la fecha
        fecha = datetime.datetime.strptime(fecha_str, '%Y/%m/%d').date()
        mes = fecha.month

        if mes not in datos_por_mes:
            datos_por_mes[mes] = []

        datos_por_mes[mes].append(data)

    hoy = datetime.datetime.now().date().strftime('%Y%m%d')

    # Escribir archivos separados por mes
    for mes, datos in datos_por_mes.items():
        print(f"Mes: {mes}, Filas: {len(datos)}")
        with open(fr'{control}\ReporteGeneral\reporte_general_{hoy}-{mes}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Cuenta', 'Diario', 'Fecha', 'Referencia', 'Concepto', 'Cargo', 'Abono', 'Cargo DLS', 'Abono DLS'])
            writer.writerows(datos)

def verificar_cuentas():
    # Leer cuentas del catálogo y almacenarlas en un conjunto para búsqueda eficiente
    print('Leyendo cuentas del catálogo...')
    with open(catalogo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        cuentas_catalogo = set(row[0] for row in reader if row[0].startswith('10550'))

    # Preparar la lista de cuentas no existentes
    cuentas_noexistentes = []
    
    mes = datetime.datetime.now().date().month
    mes_anterior = mes - 1
    # Revisar cada cuenta en el reporte general
    with open(fr'{control}\ReporteGeneral\reporte_general_{hoy}-{mes}.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].startswith('10550'): 
                #print('Revisando cuenta:', row[0])

                if row[0] not in cuentas_catalogo:

                    #Extraemos el número de empleado
                    extraer_numero_empleado(row[0])
                    datos_empleados = leer_reporte() #Extraemos los datos de los empleados

                    #Buscamos el nombre del empleado con la cuenta no existente
                    for dato in datos_empleados:
                        if dato[42] == extraer_numero_empleado(row[0]):
                            nombre = dato[2]
                            print(f'La cuenta {row[0]} no existe en el catálogo {row}')
                            
                            cuentas_noexistentes.append((row[0], nombre))
    ruta_mes =fr'{control}\ReporteGeneral\reporte_general_{hoy}-{mes_anterior}.csv'
    if os.path.exists(ruta_mes):
        with open(fr'{control}\ReporteGeneral\reporte_general_{hoy}-{mes_anterior}.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].startswith('10550'): 
                    #print('Revisando cuenta:', row[0])

                    if row[0] not in cuentas_catalogo:

                        #Extraemos el número de empleado
                        extraer_numero_empleado(row[0])
                        datos_empleados = leer_reporte() #Extraemos los datos de los empleados

                        #Buscamos el nombre del empleado con la cuenta no existente
                        for dato in datos_empleados:
                            if dato[42] == extraer_numero_empleado(row[0]):
                                nombre = dato[2]
                                print(f'La cuenta {row[0]} no existe en el catálogo')
                                cuentas_noexistentes.append((row[0], nombre))
 
    # Escribir las cuentas no existentes en un archivo, si hay alguna
    if cuentas_noexistentes:
        with open(f'{control}/Catalogo/cuentas_noexistentes.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for cuenta in cuentas_noexistentes:
                writer.writerow(cuenta)
    else:
        print('Todas las cuentas del reporte general existen en el catálogo')

def extraer_numero_empleado(cuenta_completa, base_cuenta='10550'):
    # Quitar el prefijo base de la cuenta
    num_con_ceros = cuenta_completa[len(base_cuenta):]
    # Quitar los ceros intermedios y devolver el número de empleado
    numero_empleado = num_con_ceros.lstrip('0')
    return numero_empleado

def main():
    formatear()
    carpetas_control()
    crear_tabla()
    falta_adjuntos()
    crear_reporte_general(leer_tasa_conversion())
    verificar_cuentas()

if __name__ == '__main__':
    main()