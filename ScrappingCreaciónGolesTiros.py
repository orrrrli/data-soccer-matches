from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Función para extraer datos de la tabla de creación de goles y tiros de una temporada dada
def extraer_datos_temporada_creacion(driver, url, temporada):
    # Accedemos a la URL
    driver.get(url)
    
    # Esperamos unos segundos para que la página se cargue completamente
    time.sleep(5)

    # Obtenemos el HTML de la página actual
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Buscamos la tabla con el ID correspondiente
    tabla = soup.find('table', {'id': 'stats_squads_gca_for'})
    
    if not tabla:
        print(f"No se encontró la tabla de creación de goles para la temporada {temporada}")
        return []

    print(f"Tabla de creación de goles encontrada para la temporada {temporada}, comenzando a extraer datos...")

    # Estructura de los datos esperados con 'data-stat'
    columnas_esperadas = ['team', 'sca_per90', 'gca_per90', 'Temporada']

    filas = tabla.find('tbody').find_all('tr')  # type: ignore
    estadisticas_temporada = []

    for fila in filas:
        estadisticas = {'Temporada': temporada}

        # Extraemos el nombre del equipo en el <th> o, si no existe, en el primer <td>
        equipo_celda = fila.find('th')
        if equipo_celda:
            estadisticas['team'] = equipo_celda.text.strip()
        else:
            estadisticas['team'] = fila.find('td').text.strip() if fila.find('td') else "N/A"

        # Extraemos el resto de los datos usando `data-stat`
        columnas = fila.find_all('td')
        for columna in columnas:
            data_stat = columna.get('data-stat')
            if data_stat in columnas_esperadas:
                estadisticas[data_stat] = columna.text.strip()

        # Añadimos solo las filas con datos
        if len(estadisticas) > 1:
            estadisticas_temporada.append(estadisticas)

    return estadisticas_temporada

# Función para guardar los datos en un archivo .txt
def guardar_en_txt_creacion(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribimos los encabezados
        archivo.write('Equipo,SCA90,GCA90,Temporada\n')

        for estadistica in datos:
            archivo.write(','.join([estadistica.get(col, '') for col in [
                'team', 'sca_per90', 'gca_per90', 'Temporada'
            ]]) + '\n')

# URL base para las temporadas de creación de goles y tiros
url_base_creacion = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/gca/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Configuración de Selenium
driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome configurado
driver.implicitly_wait(10)

# Lista para almacenar todas las estadísticas de creación de goles y tiros
estadisticas_creacion_totales = []

# Iteramos sobre los años de la temporada desde 2017-2018 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_creacion.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos de creación de goles de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual
    estadisticas_temporada_creacion = extraer_datos_temporada_creacion(driver, url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_creacion_totales.extend(estadisticas_temporada_creacion)

# Guardamos todos los datos en un solo archivo
guardar_en_txt_creacion(estadisticas_creacion_totales, "estadisticas_creacion_goles.txt")
print("Datos de creación de goles de todas las temporadas guardados en estadisticas_creacion_goles.txt")

# Cerramos el navegador
driver.quit()
