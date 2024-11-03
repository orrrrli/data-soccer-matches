from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Configura el driver de Selenium
driver = webdriver.Chrome()

# Temporadas con el formato correcto
temporadas = [f"{year}-{year+1}" for year in range(2017, 2024)]
estadisticas_totales = []

# Mapeo de nombres de equipos para que coincidan con el otro dataset
nombres_equipos = {
    "FC Barcelona": "Barcelona",
    "Atlético Madrid": "Atlético Madrid",
    "Real Madrid": "Real Madrid",
    "Valencia CF": "Valencia",
    "Villarreal CF": "Villarreal",
    "Real Betis Balompié": "Betis",
    "Sevilla FC": "Sevilla",
    "Getafe CF": "Getafe",
    "SD Eibar": "Eibar",
    "Girona FC": "Girona",
    "RCD Espanyol": "Espanyol",
    "Real Sociedad": "Real Sociedad",
    "RC Celta de Vigo": "Celta Vigo",
    "Deportivo Alavés": "Alavés",
    "Levante UD": "Levante",
    "Athletic Club": "Athletic Club",
    "CD Leganés": "Leganés",
    "RC Deportivo de La Coruña": "La Coruña",
    "UD Las Palmas": "Las Palmas",
    "Málaga CF": "Málaga"
}

# Iterar sobre cada temporada
for i, temporada in enumerate(temporadas):
    # URL de la temporada actual
    url = f"https://www.transfermarkt.es/laliga/tabelle/wettbewerb/ES1?saison_id={2017 + i}"
    driver.get(url)

    # Esperar hasta que la tabla esté presente en la página
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "responsive-table"))
        )
        print(f"Extrayendo datos de la temporada {temporada}...")

        # Obtener el HTML de la página ya cargada
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Buscar la tabla de clasificación
        tabla = soup.find("table", {"class": "items"})

        # Extraer las filas de la tabla si se encuentra
        if tabla:
            filas = tabla.find("tbody").find_all("tr") # type: ignore
            for fila in filas:
                try:
                    # Extraer los datos de cada columna necesarios
                    posicion = fila.find("td", {"class": "rechts hauptlink"}).text.strip()
                    equipo_html = fila.find("td", {"class": "no-border-links hauptlink"}).text.strip()
                    equipo = nombres_equipos.get(equipo_html, equipo_html)  # Usar el nombre mapeado
                    puntos = fila.find_all("td", {"class": "zentriert"})[7].text.strip()  # Índice ajustado para "Ptos."

                    # Agregar los datos de la temporada actual a la lista de estadísticas totales
                    estadisticas_totales.append(f"{equipo},{posicion},{puntos},{temporada}")

                except Exception as e:
                    print(f"Error al procesar una fila en la temporada {temporada}: {e}")
        else:
            print(f"No se encontró la tabla para la temporada {temporada}")

        # Esperar un breve momento antes de la próxima solicitud
        time.sleep(2)

    except Exception as e:
        print(f"Error al extraer la tabla para la temporada {temporada}: {e}")

# Guardar los datos en un archivo .txt en el formato solicitado
with open("estadisticas_forma_equipo_laliga.txt", "w", encoding="utf-8") as file:
    # Escribir encabezado
    file.write("Equipo,Posicion,Puntos,Temporada\n")
    # Escribir datos
    for linea in estadisticas_totales:
        file.write(linea + "\n")

print("Datos guardados en estadisticas_forma_equipo_laliga.txt")

# Cerrar el navegador
driver.quit()
