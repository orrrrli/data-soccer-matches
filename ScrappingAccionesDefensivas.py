from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import unidecode

# Configuración del driver de Selenium
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# URL base para las temporadas defensivas
url_base_defensiva = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/defense/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Diccionario de nombres de equipos para estandarizar
nombres_equipos = {
    "Alavés": "Alaves",
    "Athletic Club": "Athletic Club",
    "Atlético Madrid": "Atletico de Madrid",
    "Barcelona": "Barcelona",
    "Betis": "Betis",
    "Celta Vigo": "Celta Vigo",
    "Eibar": "Eibar",
    "Espanyol": "Espanyol",
    "Getafe": "Getafe",
    "Girona": "Girona",
    "Deportivo La Coruña": "Deportivo de La Coruna",
    "Las Palmas": "Las Palmas",
    "Leganés": "Leganes",
    "Levante": "Levante",
    "Málaga": "Malaga",
    "Real Madrid": "Real Madrid",
    "Real Sociedad": "Real Sociedad",
    "Sevilla": "Sevilla",
    "Valencia": "Valencia",
    "Villarreal": "Villarreal"
}

# Función para extraer datos de la tabla defensiva de una temporada dada
def extraer_datos_temporada_defensiva(driver, url, temporada):
    driver.get(url)
    time.sleep(5)

    # Intentar hacer clic en el botón "por 90" si existe
    try:
        boton_por_90 = driver.find_element(By.ID, "stats_squads_defense_for_per_match_toggle")
        driver.execute_script("arguments[0].click();", boton_por_90)
        print("Botón 'por 90' clicado mediante JavaScript.")
    except (NoSuchElementException, StaleElementReferenceException):
        print(f"Botón 'por 90' no encontrado para la temporada {temporada}.")
        return []

    # Esperar hasta que aparezca la clase 'modified' en las celdas de estadísticas
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td.modified"))
        )
        print("La tabla se ha actualizado con estadísticas 'por 90'.")
    except TimeoutException:
        print("La tabla no se actualizó con estadísticas 'por 90'.")
        return []

    # Obtener el HTML actualizado de la página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tabla = soup.find('table', {'id': 'stats_squads_defense_for'})

    if not tabla:
        print(f"No se encontró la tabla defensiva para la temporada {temporada}")
        return []

    print(f"Tabla defensiva encontrada para la temporada {temporada}, comenzando a extraer datos...")

    # Estructura de los datos esperados con 'data-stat'
    columnas_esperadas = {
        'team': 'Equipo',
        'tackles_won': 'Derribos conseguidos',
        'challenge_tackles_pct': '% Dribladores derribados',
        'challenges_lost': 'Desafíos Perdidos',
        'blocked_shots': 'Disparos Bloqueados',
        'interceptions': 'Intercepciones',
        'errors': 'Errores',
        'Temporada': 'Temporada'
    }

    filas = tabla.find('tbody').find_all('tr') # type: ignore
    estadisticas_temporada = []

    for fila in filas:
        estadisticas = {'Temporada': temporada}
        equipo_celda = fila.find('th')
        if equipo_celda:
            equipo = unidecode.unidecode(equipo_celda.text.strip())
            equipo = nombres_equipos.get(equipo, equipo)
            estadisticas['team'] = equipo

        columnas = fila.find_all('td')
        for columna in columnas:
            data_stat = columna.get('data-stat')
            if data_stat in columnas_esperadas:
                estadisticas[data_stat] = columna.text.strip()

        if len(estadisticas) > 1:
            estadisticas_temporada.append(estadisticas)

    return estadisticas_temporada

# Función para guardar los datos en un archivo .txt
def guardar_en_txt_defensiva(datos, nombre_archivo):
    columnas = [
        'Equipo', 'Derribos conseguidos', '% Dribladores derribados', 
        'Desafíos Perdidos', 'Disparos Bloqueados', 'Intercepciones', 'Errores', 'Temporada'
    ]
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(",".join(columnas) + "\n")
        for estadistica in datos:
            archivo.write(','.join([
                estadistica.get('team', ''),
                estadistica.get('tackles_won', ''),
                estadistica.get('challenge_tackles_pct', ''),
                estadistica.get('challenges_lost', ''),
                estadistica.get('blocked_shots', ''),
                estadistica.get('interceptions', ''),
                estadistica.get('errors', ''),
                estadistica.get('Temporada', '')
            ]) + '\n')

# Lista para almacenar todas las estadísticas defensivas
estadisticas_defensivas_totales = []

# Iteramos sobre los años de la temporada desde 2017-2018 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_defensiva.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos defensivos de la temporada: {temporada}")
    estadisticas_temporada_defensiva = extraer_datos_temporada_defensiva(driver, url_temporada, temporada)
    estadisticas_defensivas_totales.extend(estadisticas_temporada_defensiva)

# Guardar todos los datos en un archivo
guardar_en_txt_defensiva(estadisticas_defensivas_totales, "estadisticas_defensivas.txt")
print("Datos defensivos de todas las temporadas guardados en estadisticas_defensivas.txt")

# Cerrar el navegador
driver.quit()
