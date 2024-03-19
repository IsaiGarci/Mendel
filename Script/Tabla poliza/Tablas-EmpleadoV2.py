from collections import defaultdict
import datetime
import csv
import os
import sys

# Asegura que Python pueda encontrar el módulo DOF.py añadiendo su directorio al sys.path
sys.path.append(r'C:\ProduccionRpa\Mendel\Script\Tasa')

# Ahora importa la función o clase DOF desde el módulo DOF.py
from DOF import DOF

# Rutas de archivos y carpetas
hoy = datetime.datetime.now().date().strftime('%Y%m%d')
numero_semana = datetime.datetime.now().isocalendar()[1]
año = str(datetime.datetime.now().year)[-2:]
dia = datetime.datetime.now().day

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
tasa = r'C:\ProduccionRpa\Mendel\Control\tasa_conversion.txt'
control = r'C:\ProduccionRpa\Mendel\Control'


reporte = fr'{reportes}\{hoy}\Reporte-*{hoy}.csv'


with open(reporte, 'r', ) as file:
    reader = csv.reader(file)
    data = [row for row in reader]

with open(reporte, 'w', newline='',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)
    print('Reporte creado con éxito')


def carpetas_control():
    os.makedirs(f'{control}', exist_ok=True)

def leer_tasa_conversion():
    DOF()
    with open(tasa, 'r') as file:
        return float(file.read().strip())

def leer_reporte():
    data = []
    for file in os.listdir(f'{reportes}\{hoy}'):
        if file.endswith('.csv'):
            with open(f'{reportes}\{hoy}\{file}', 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                data.extend([row for row in reader])
    return data

def calcular_dls(valor, tasa_conversion):
    return round(float(valor) / tasa_conversion, 2)

def calcular_pesos(valor, tasa_conversion):
    return round(float(valor) * tasa_conversion, 2)

def crear_reporte_general(tasa_conversion):
    reporte_general_data = []

    for row in leer_reporte():
        Folio = row[0]
        Empleado = row[42]
        Nombre = row[2]
        Concepto = '*'.join([row[0], row[20], row[3]])
        Fecha = row[1][:10]
        Moneda = row[5]
        Adjunto_pdf = row[25]
        Adjunto_xml = row[26]
        Correo = row[41]
        Comercio = row[3]
        Cargo = row[4]
        Cargo = float(Cargo) if Cargo else 0.00
        Cargo = round(Cargo, 2)

        
        base_cuenta = '10550'
        longitud_total = 9
        longitud_restante = longitud_total - len(base_cuenta) - len(Empleado)
        Cuenta = base_cuenta + '0' * longitud_restante + Empleado

        if Moneda == 'MXN':
            Cargo_DLS = calcular_dls(Cargo, tasa_conversion)
            data_cargo = ['201031417', 'D', Fecha, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}"]
            # Nota: Aquí se necesita una lógica para generar la cuenta basada en el empleado o algún criterio específico
            data_abono = [Cuenta, 'D', Fecha, f'S{numero_semana}V{año}-{dia}', Concepto, f"{Cargo:.2f}", '0.00', f"{Cargo_DLS:.2f}", '0.00']
        else:
            Cargo_Pesos = calcular_pesos(Cargo, tasa_conversion)
            data_cargo = ['201031417', 'D', Fecha, f'S{numero_semana}V{año}-{dia}', Concepto, '0.00', f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}"]
            # Nota: Aquí se necesita una lógica para generar la cuenta basada en el empleado o algún criterio específico
            data_abono = [Cuenta, 'D', Fecha, f'S{numero_semana}V{año}-{dia}', Concepto, f"{Cargo_Pesos:.2f}", '0.00', f"{Cargo:.2f}", '0.00']

        reporte_general_data.append(data_cargo)
        reporte_general_data.append(data_abono)

    # Guardar el reporte general
    with open(fr'{control}\reporte_general_{hoy}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Cuenta', 'Diario', 'Fecha', 'Referencia', 'Concepto', 'Cargo', 'Abono', 'Cargo DLS', 'Abono DLS'])
        writer.writerows(reporte_general_data)

carpetas_control()                        
crear_reporte_general(leer_tasa_conversion())
