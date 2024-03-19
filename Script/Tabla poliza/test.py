import chardet

# Ejemplo de cómo detectar la codificación de un archivo
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

print(detect_encoding(fr'C:\ProduccionRpa\Mendel\Reportes\20240316\a.csv'))