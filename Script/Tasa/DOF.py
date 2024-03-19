## IMPORTS DEL CÓDIOGO.
import requests
from datetime import datetime
from datetime import timedelta

## Ruta de archivo para guardar el tipo de cambio
tasa = r'C:\ProduccionRpa\Mendel\Control\tasa_conversion.txt'
def DOF():
    ## VARIABLES DEL CÓDIGO.
    ##url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno"
    TodayDate = datetime.now().strftime('%Y-%m-%d')
    YesterdayDate = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/{YesterdayDate}/{YesterdayDate}"
    ApiKey = "bac3b8898ba485a9674a473ff9176061076bff4f8dce5260453f8bef15e8ab60"

    Header = {
        "Bmx-Token": ApiKey,
        "Accept": "application/json",
        "Accept-Encoding": "gzip"
    }

    ## MAIN DEL CÓDIGO.
    try:
        Response = requests.get(url, headers=Header)

        if Response.status_code == 200:
            Data = Response.json()
            # Asegúrate de que esta línea está descomentada y correctamente escrita
            if 'datos' in Data['bmx']['series'][0]:  # Verifica si hay datos disponibles
                DataRecibida = Data['bmx']['series'][0]['datos'][0]['dato']
                with open(tasa, 'w') as file:
                    print(f"Tipo de cambio de {TodayDate}: {DataRecibida}")
                    file.write(DataRecibida)
            else:
                print("No hay datos disponibles para la fecha especificada.")
    except requests.exceptions.RequestException as e:
        print("Error en la petición:", e)
