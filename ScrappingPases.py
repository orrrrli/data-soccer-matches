from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import unidecode  # Librería para quitar acentos fácilmente

# Configura el driver de Selenium
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# URL de la página con los datos
url = "https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/passing/Estadisticas-{anio}-{anio_siguiente}-La-Liga"

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

# Función para manejar el banner de cookies si está presente
def aceptar_cookies(driver):
    try:
        boton_cookies = driver.find_element(By.CSS_SELECTOR, "button.osano-cm-accept")
        boton_cookies.click()
        print("Banner de cookies aceptado.")
        time.sleep(2)
    except NoSuchElementException:
        print("No se encontró un banner de cookies. Continuando...")

# Función para extraer datos con estadísticas por 90 minutos
def extraer_datos_por_90(driver, url, temporada):
    driver.get(url)
    time.sleep(5)
    aceptar_cookies(driver)

    # Ocultar el elemento <a> temporalmente para evitar interferencias
    try:
        boton_por_90 = driver.find_element(By.ID, "stats_squads_passing_for_per_match_toggle")
        driver.execute_script("arguments[0].click();", boton_por_90)
        print("Botón 'por 90' clicado mediante JavaScript.")
    except (NoSuchElementException, StaleElementReferenceException):
        print(f"Botón 'por 90' no encontrado para la temporada {temporada}.")
        return []

    # Espera hasta que aparezca la clase 'modified' en las celdas de estadísticas
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td.modified"))
        )
        print("La tabla se ha actualizado con estadísticas 'por 90'.")
    except TimeoutException:
        print("La tabla no se actualizó con estadísticas 'por 90'.")
        return []

    # Capturar el HTML actualizado de la página después de esperar
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tabla = soup.find("table", {"id": "stats_squads_passing_for"})

    if not tabla:
        print(f"No se encontró la tabla de estadísticas por 90 para la temporada {temporada}")
        return []

    print(f"Tabla de estadísticas por 90 encontrada para la temporada {temporada}, extrayendo datos...")

    # Columnas que queremos extraer y su correspondencia con los nombres en el archivo
    columnas_deseadas = {
        'team': 'Equipo',
        'passes_completed': 'Pases Completados',
        'passes_progressive_distance': 'Distancia Progresiva de Pase',
        'pass_xa': 'Asistencias Esperadas',
        'crosses_into_penalty_area': 'Cruces al Área Penal',
        'progressive_passes': 'Pases Progresivos',
        'Temporada': 'Temporada'
    }

    filas = tabla.find("tbody").find_all("tr")
    estadisticas_por_90 = []

    for fila in filas:
        estadisticas = {"Temporada": temporada}
        equipo_celda = fila.find("th")
        if equipo_celda:
            equipo = equipo_celda.text.strip()
            # Normalizar el nombre del equipo
            equipo = unidecode.unidecode(equipo)  # Quita acentos y caracteres especiales
            equipo = nombres_equipos.get(equipo, equipo)  # Estandariza usando el diccionario
            estadisticas["team"] = equipo

        columnas = fila.find_all("td")
        for columna in columnas:
            data_stat = columna.get("data-stat")
            if data_stat in columnas_deseadas:
                estadisticas[data_stat] = columna.text.strip()

        if len(estadisticas) > 1:
            estadisticas_por_90.append(estadisticas)

    # Escribir datos en archivo de texto (agregación para múltiples temporadas)
    with open("estadisticas_pases.txt", "a") as file:
        for estadistica in estadisticas_por_90:
            fila = [
                estadistica.get("team", ""),
                estadistica.get("passes_completed", ""),
                estadistica.get("passes_progressive_distance", ""),
                estadistica.get("pass_xa", ""),
                estadistica.get("crosses_into_penalty_area", ""),
                estadistica.get("progressive_passes", ""),
                estadistica.get("Temporada", "")
            ]
            file.write(",".join(fila) + "\n")

    return estadisticas_por_90

# Recorrer las temporadas desde 2017-2018 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos de estadísticas por 90 para la temporada: {temporada}")
    datos_temporada = extraer_datos_por_90(driver, url_temporada, temporada)

# Cerrar el driver después de completar el scraping
driver.quit()
