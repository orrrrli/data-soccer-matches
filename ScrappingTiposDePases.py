from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Función para extraer datos de tipos de pases de una temporada dada
def extraer_datos_temporada_pases(driver, url, temporada):
    driver.get(url)
    
    # Esperamos unos segundos para que la página se cargue completamente
    time.sleep(5)

    # Cambiar a formato por 90 minutos
    try:
        boton_por_90 = driver.find_element(By.ID, "stats_squads_passing_types_for_per_match_toggle")
        driver.execute_script("arguments[0].click();", boton_por_90)
        print(f"Formato cambiado a 'por 90' para la temporada {temporada}.")
    except Exception as e:
        print(f"No se pudo cambiar al formato 'por 90' para la temporada {temporada}: {e}")
        return []

    # Esperar a que se actualice la tabla con el formato 'por 90'
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "td.modified"))
    )
    
    # Obtener el HTML actualizado
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabla = soup.find('table', {'id': 'stats_squads_passing_types_for'})
    
    if not tabla:
        print(f"No se encontró la tabla de tipos de pases para la temporada {temporada}")
        return []

    print(f"Tabla de tipos de pases encontrada para la temporada {temporada}, extrayendo datos...")

    # Estructura de los datos esperados sin 'PL' y '90 Jugados'
    columnas_esperadas = [
        'team', 'passes', 'passes_live', 'passes_dead', 
        'passes_free_kicks', 'through_balls', 'passes_switches', 'crosses', 
        'throw_ins', 'corner_kicks', 'corner_kicks_in', 'corner_kicks_out', 
        'corner_kicks_straight', 'passes_completed', 'passes_offsides', 
        'passes_blocked'
    ]

    filas = tabla.find('tbody').find_all('tr') # type: ignore
    estadisticas_temporada = []

    for fila in filas:
        estadisticas = {'Temporada': temporada}

        # Extraemos el nombre del equipo
        equipo_celda = fila.find('th', {'data-stat': 'team'})
        estadisticas['team'] = equipo_celda.text.strip() if equipo_celda else "N/A"

        # Extraemos el resto de los datos usando `data-stat`
        columnas = fila.find_all('td')
        for columna in columnas:
            data_stat = columna.get('data-stat')
            if data_stat in columnas_esperadas:
                estadisticas[data_stat] = columna.text.strip()

        # Verificación de que se hayan extraído los datos suficientes
        if estadisticas['team'] != "N/A":
            estadisticas_temporada.append(estadisticas)

    return estadisticas_temporada

# Función para guardar los datos en un archivo .txt
def guardar_en_txt_pases(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Encabezados sin 'PL' y '90 Jugados'
        archivo.write(','.join(['Equipo', 'Pases Intentados', 'Pases de Balón Vivo', 
                                'Pases de Balón Muerto', 'Pases de Tiros Libres', 'Pases Largos', 
                                'Cambios', 'Pases Cruzados', 'Lanzamientos Tomados', 'Saques de Esquina', 
                                'SE hacia adentro', 'SE hacia afuera', 'SE rectos', 'Pases Completados', 
                                'Pases Fuera de Juego', 'Pases Bloqueados', 'Temporada']) + '\n')

        for estadistica in datos:
            archivo.write(','.join([estadistica.get(col, '') for col in [
                'team', 'passes', 'passes_live', 'passes_dead', 
                'passes_free_kicks', 'through_balls', 'passes_switches', 'crosses', 
                'throw_ins', 'corner_kicks', 'corner_kicks_in', 'corner_kicks_out', 
                'corner_kicks_straight', 'passes_completed', 'passes_offsides', 
                'passes_blocked', 'Temporada'
            ]]) + '\n')

# URL base para las temporadas de tipos de pases
url_base_pases = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/passing_types/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Configuración de Selenium
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# Lista para almacenar todas las estadísticas de tipos de pases
estadisticas_pases_totales = []

# Iteramos sobre los años de la temporada desde 2017-2018 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_pases.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos de tipos de pases de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual
    estadisticas_temporada_pases = extraer_datos_temporada_pases(driver, url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_pases_totales.extend(estadisticas_temporada_pases)

# Guardamos todos los datos en un solo archivo
guardar_en_txt_pases(estadisticas_pases_totales, "estadisticas_tipos_pases.txt")
print("Datos de tipos de pases de todas las temporadas guardados en estadisticas_tipos_pase.txt")

# Cerramos el navegador
driver.quit()
