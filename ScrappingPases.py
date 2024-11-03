from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Función para extraer datos de la tabla de pases de una temporada dada
def extraer_datos_temporada_pases(driver, url, temporada):
    # Accedemos a la URL
    driver.get(url)
    
    # Esperamos unos segundos para que la página se cargue completamente
    time.sleep(5)

    # Obtenemos el HTML de la página actual
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Buscamos la tabla con el ID correspondiente
    tabla = soup.find('table', {'id': 'stats_squads_passing_for'})
    
    if not tabla:
        print(f"No se encontró la tabla de pases para la temporada {temporada}")
        return []

    print(f"Tabla de pases encontrada para la temporada {temporada}, comenzando a extraer datos...")

    # Estructura de los datos esperados con 'data-stat'
    columnas_esperadas = [
        'team', 'players_used', 'minutes_90s', 'passes_completed', 'passes', 'passes_pct',
        'passes_total_distance', 'passes_progressive_distance', 'passes_completed_short', 'passes_short',
        'passes_pct_short', 'passes_completed_medium', 'passes_medium', 'passes_pct_medium',
        'passes_completed_long', 'passes_long', 'passes_pct_long', 'assists', 'xg_assist', 'pass_xa',
        'xg_assist_net', 'assisted_shots', 'passes_into_final_third', 'passes_into_penalty_area',
        'crosses_into_penalty_area', 'progressive_passes'
    ]

    filas = tabla.find('tbody').find_all('tr') # type: ignore
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
def guardar_en_txt_pases(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(','.join([
            'Equipo', 'PL', '90 Jugados', 'Pases Completados', 'Pases Intentados', '% de Pase Completo',
            'Distancia Total de Pase', 'Distancia Progresiva', 'Pases Completados Cortos', 'Pases Cortos',
            '% Pase Completo Cortos', 'Pases Completados Medios', 'Pases Medios', '% Pase Completo Medios',
            'Pases Completados Largos', 'Pases Largos', '% Pase Completo Largos', 'Asistencias', 'xAG',
            'xA', 'Asistencias - xAG', 'Pases Clave', 'Pases al Último Tercio', 'Pases al Área Penal',
            'Cruces al Área Penal', 'Pases Progresivos', 'Temporada'
        ]) + '\n')

        for estadistica in datos:
            archivo.write(','.join([estadistica.get(col, '') for col in [
                'team', 'players_used', 'minutes_90s', 'passes_completed', 'passes', 'passes_pct',
                'passes_total_distance', 'passes_progressive_distance', 'passes_completed_short', 'passes_short',
                'passes_pct_short', 'passes_completed_medium', 'passes_medium', 'passes_pct_medium',
                'passes_completed_long', 'passes_long', 'passes_pct_long', 'assists', 'xg_assist', 'pass_xa',
                'xg_assist_net', 'assisted_shots', 'passes_into_final_third', 'passes_into_penalty_area',
                'crosses_into_penalty_area', 'progressive_passes', 'Temporada'
            ]]) + '\n')

# URL base para las temporadas de pases
url_base_pases = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/passing/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Configuración de Selenium
driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome configurado
driver.implicitly_wait(10)

# Lista para almacenar todas las estadísticas de pases
estadisticas_pases_totales = []

# Iteramos sobre los años de la temporada desde 2017-2018 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_pases.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos de pases de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual
    estadisticas_temporada_pases = extraer_datos_temporada_pases(driver, url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_pases_totales.extend(estadisticas_temporada_pases)

# Guardamos todos los datos en un solo archivo
guardar_en_txt_pases(estadisticas_pases_totales, "estadisticas_pases.txt")
print("Datos de pases de todas las temporadas guardados en estadisticas_pases.txt")

# Cerramos el navegador
driver.quit()
