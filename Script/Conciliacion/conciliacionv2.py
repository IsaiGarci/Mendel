
import datetime, os, csv
from fpdf import FPDF

reportes = r'C:\ProduccionRpa\Mendel\Reportes'
hoy = datetime.datetime.now().date().strftime('%Y%m%d')


def reporte_conciliacion():
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion_hoy = fr'{control}\Conciliacion\{hoy}'
    fecha_inicio =  datetime.datetime(2024, 5, 1, 0, 0)
    fecha_fin = datetime.datetime(2024, 5, 31, 23, 59)
    tipos_aceptados = ['AUTHORIZED_PAYMENT', 'ADJUSTMENT','AUTHORIZED_WITHDRAWAL','DECLINED_PAYMENT','REFUNDED']
    folio_aplicado = ''
    importe_total = importe = comision = 0.0
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
                    metodo_pago = row[11]
                    if row[8] != '':
                        comision_bancaria = float(row[8])
                    motivo = row[14]
                    folio = row[0]
                    importe_total = float(row[4])
                    if folio != folio_aplicado:
                        if fecha >= fecha_inicio.strftime('%Y/%m/%d %H:%M') and fecha <= fecha_fin.strftime('%Y/%m/%d %H:%M') and row[15] != '':
                            if '\n' in row[21]:
                                row[21] = row[21].replace('\n', ' ')
                            for tipo in tipos_aceptados:
                                if tipo_pago == tipo:
                                    if tipo_pago == 'DECLINED_PAYMENT' and metodo_pago == 'PHYSICAL_CARD':
                                        if motivo == 'INSUFFICIENT_COMPANY_FUNDS':
                                            datos_limpios.append(row)
                                        else:
                                            continue
                                    elif metodo_pago == 'PHYSICAL_CARD':
                                        datos_limpios.append(row)
                                        if tipo_pago == 'AUTHORIZED_WITHDRAWAL':
                                            importe += (importe_total-comision_bancaria)
                                            comision += comision_bancaria
                                            round(importe, 2)
                                    folio_aplicado = folio
                datos_retiros = [round(importe, 2),round(comision,2),round((importe * 0.05), 2),'5%']

                    # Escribir los datos de retiros en el archivo Reporte.csv
                with open(f'{conciliacion_hoy}/Reporte.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Disposición de efectivo','Comisión bancaria','Comisiones por disposición','% de comisión'])  # Escribir encabezado
                    writer.writerow([datos_retiros[0],datos_retiros[1],datos_retiros[2],datos_retiros[3]])  # Escribir los datos de retiros
                                            
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


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        # Agregar la primera imagen (logo)
        self.image(r'C:\ProduccionRpa\Mendel\img\image.png', 10, 8, 33)  # Ajustar la posición y tamaño según sea necesario
        self.cell(0, 10, 'Conciliación', 0, 1, 'C')
        # Agregar la segunda imagen (bot)
        self.image(r'C:\ProduccionRpa\Mendel\img\bot.png', 160, 8, 33)  # Ajustar la posición y tamaño según sea necesario
        self.ln(20)  # Espacio después del encabezado

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_table_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'C')
        self.ln(5)  # Espacio después del título

    def table(self, header, data, x_margin=10):
        self.set_font('Arial', 'B', 10)
        table_width = self.w - 2 * x_margin  # Usar todo el ancho de la página menos los márgenes
        col_width = table_width / len(header)  # Ancho de cada columna
        margin = x_margin  # Margen izquierdo y derecho

        self.set_x(margin)  # Establecer margen izquierdo
        # Header
        for col in header:
            self.cell(col_width, 10, col, 1, 0, 'C')
        self.ln()

        self.set_font('Arial', '', 12)
        # Data
        for row in data:
            self.set_x(margin)  # Establecer margen izquierdo
            for item in row:
                self.cell(col_width, 10, str(item), 1, 0, 'C')
            self.ln()

def generar_reporte_pdf(conciliacion_hoy, datos_retiros, datos_importes):
    # Generar el reporte en PDF
    pdf = PDF()
    pdf.add_page()

    # Agregar el título y la primera tabla al PDF (Disposiciones de efectivo mendel)
    pdf.add_table_title("Disposiciones de efectivo mendel")
    header_retiros = datos_retiros[0]
    data_retiros = datos_retiros[1:]
    pdf.table(header_retiros, data_retiros)

    pdf.ln(10)  # Espacio entre las dos tablas

    # Agregar el título y la segunda tabla al PDF (Consumos mendel)
    pdf.add_table_title("Consumos mendel")
    header_importes = datos_importes[0]
    data_importes = datos_importes[1:]
    pdf.table(header_importes, data_importes)

    # Guardar el PDF
    pdf_output_path = f'{conciliacion_hoy}/Reporte.pdf'
    pdf.output(pdf_output_path)

def reporte():
    hoy = datetime.datetime.now().date().strftime('%Y%m%d')
    control = r'C:\ProduccionRpa\Mendel\Control'
    conciliacion_hoy = fr'{control}\Conciliacion\{hoy}'
    total_factura = 0.0

    # Leer el archivo Conciliado.csv y calcular el total de la columna 5
    with open(f'{conciliacion_hoy}/Conciliado.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        encabezado = next(reader)  # Guarda el encabezado
        for row in reader:
            if row[4]:  # Verifica si la columna 5 tiene valor
                total_factura += float(row[4])

    # Redondear el total_factura a dos decimales
    total_factura = round(total_factura, 2)

    # Datos para el reporte
    total_mendel = 1331655.0
    diferencia = round((total_factura - total_mendel), 2)
    datos_reporte = [
        ['Total importes', 'Total mendel', 'Diferencia'],
        [total_factura, total_mendel, diferencia]
    ]

    # Escribir el reporte en Reporte.csv
    with open(f'{conciliacion_hoy}/Reporte.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in datos_reporte:
            writer.writerow(row)

    # Leer todo el contenido del archivo Reporte.csv para el PDF
    with open(f'{conciliacion_hoy}/Reporte.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        all_data = [row for row in reader]

    # Separar los datos en dos tablas diferentes
    datos_retiros = [all_data[0], all_data[1]]  # 'Importe total de retiros,Comisiones' y sus datos
    datos_importes = [all_data[2], all_data[3]]  # 'Total importes,Total mendel,Diferencia' y sus datos

    # Llamar a la función para generar el PDF
    generar_reporte_pdf(conciliacion_hoy, datos_retiros, datos_importes)

def main():
    carpetas_control()
    reporte_conciliacion()
    reporte()

if __name__ == '__main__':
    main()