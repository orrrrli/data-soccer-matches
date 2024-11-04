from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Función para extraer datos de la tabla avanzada de porteros de una temporada dada
def extraer_datos_temporada_porteros(driver, url, temporada):
    # Accedemos a la URL
    driver.get(url)
    
    # Esperamos unos segundos para que la página se cargue completamente
    time.sleep(5)

    # Obtenemos el HTML de la página actual
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Buscamos la tabla con el ID correspondiente
    tabla = soup.find('table', {'id': 'stats_squads_keeper_adv_for'})
    
    if not tabla:
        print(f"No se encontró la tabla de porteros avanzada para la temporada {temporada}")
        return []

    print(f"Tabla avanzada de porteros encontrada para la temporada {temporada}, comenzando a extraer datos...")

    estadisticas_temporada = []

    # Extraemos las filas de la tabla
    filas = tabla.find('tbody').find_all('tr') # type: ignore
    for fila in filas:
        estadisticas = {'Temporada': temporada}

        # Extraemos el nombre del equipo
        equipo_celda = fila.find('th', {'data-stat': 'team'})
        estadisticas['Equipo'] = equipo_celda.text.strip() if equipo_celda else "N/A"

        # Extraemos el valor de PSxG+/-
        psxg_mas_menos = fila.find('td', {'data-stat': 'gk_psxg_net'})
        estadisticas['PSxG+/-'] = psxg_mas_menos.text.strip() if psxg_mas_menos else "N/A"

        # Extraemos el valor de % Lanzamiento
        porcentaje_lanzamiento = fila.find('td', {'data-stat': 'gk_pct_passes_launched'})
        estadisticas['% de Lanzamientos'] = porcentaje_lanzamiento.text.strip() if porcentaje_lanzamiento else "N/A"

        # Añadimos solo las filas con datos
        if estadisticas['Equipo'] != "N/A":
            estadisticas_temporada.append(estadisticas)

    return estadisticas_temporada

# Función para guardar los datos en un archivo .txt
def guardar_en_txt_porteros(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribimos los encabezados
        archivo.write('Equipo,PSxG+/-,% de Lanzamientos,Temporada\n')

        for estadistica in datos:
            archivo.write(','.join([
                estadistica.get('Equipo', ''),
                estadistica.get('PSxG+/-', ''),
                estadistica.get('% de Lanzamientos', ''),
                estadistica.get('Temporada', '')
            ]) + '\n')

# URL base para las temporadas avanzadas de porteros
url_base_porteros = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/keepersadv/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Configuración de Selenium
driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome configurado
driver.implicitly_wait(10)

# Lista para almacenar todas las estadísticas avanzadas de porteros
estadisticas_porteros_totales = []

# Iteramos sobre los años de la temporada desde 2017-2018 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_porteros.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos avanzados de porteros de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual para porteros avanzados
    estadisticas_temporada_porteros = extraer_datos_temporada_porteros(driver, url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_porteros_totales.extend(estadisticas_temporada_porteros)

# Guardamos todos los datos en un solo archivo
guardar_en_txt_porteros(estadisticas_porteros_totales, "estadisticas_porteria.txt")
print("Datos avanzados de porteros de todas las temporadas guardados en estadisticas_porteria.txt")

# Cerramos el navegador
driver.quit()
