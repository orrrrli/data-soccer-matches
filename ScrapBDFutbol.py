# -*- coding: utf-8 -*-
__author__ = 'Orlando Castaneda Sanchez'

from bs4 import BeautifulSoup
from FutbolClass import Partido
import requests
import re
import unicodedata
import Const

# En este fichero voy a obtener un historico de partidos de futbol de todas
# las temporadas anteriores a la actual a partir de la web:
# http://www.bdfutbol.com/

# Guardo los partidos de futbol con un id
partidos = dict()

# Guardo los equipos de futbol con su id y su nombre
equipos = dict()

# Contador de Partidos
contador = 0


import unicodedata



import unicodedata

# Función para normalizar los nombres de los equipos y eliminar los acentos
def normalize_text(text):
    # Descompone el texto para separar los acentos de los caracteres base
    normalized = unicodedata.normalize('NFKD', text)
    # Elimina los caracteres de acento
    return normalized.encode('ASCII', 'ignore').decode('utf-8')

# Función para procesar los equipos y normalizarlos
def find_equipos(str_resultados):
    match = re.findall(r'SE\[\d+\]=\"(\d+)\|(.*?)\";', str_resultados)
    print(f"Equipos encontrados: {len(match)}")  # Verifica cuántos equipos se encuentran
    for mat in match:
        id_equipo = mat[0]
        nombre_equipo = mat[1]
        nombre_normalizado = normalize_text(nombre_equipo)  # Normaliza el nombre del equipo
        equipos[id_equipo] = nombre_normalizado
        print(f"Equipo agregado: {nombre_normalizado}")




def find_partidos(str_partidos, temporada, division):
    global contador

    # Encontrar todas las entradas de partidos en el array SP
    partidos_encontrados = re.findall(r'SP\[\d+\]\.push\((\{.*?\})\);', str_partidos)
    print(f"Partidos encontrados: {len(partidos_encontrados)}")

    for partido_json in partidos_encontrados:
        partido = eval(partido_json)  # Convertimos el JSON en un diccionario

        fecha = partido['d']
        equipo_local = equipos[partido['a1']]
        equipo_visitante = equipos[partido['a2']]
        goles_local = partido['g1']
        goles_visitante = partido['g2']
        jornada = partido.get('jornada', '1')  # Agrega la jornada si existe

        contador += 1
        partidos[contador] = Partido(
            contador, temporada, division, jornada, equipo_local, equipo_visitante, goles_local, goles_visitante, fecha
        )



def get_partidos():
    # Genero las URLs y scrapeo los datos para cada temporada
    for temporada in Const.TEMPORADAS:
        print(f"****  PROCESANDO TEMPORADA {temporada} ****")
        
        # Mantener el guion medio en la temporada
        url_primera = f"https://www.bdfutbol.com/en/t/t{temporada}.html"
        
        print(f"Procesando la URL: {url_primera}")

        # Realizo la petición a la URL
        req_primera = requests.get(url_primera)
        
        # Verificar si la solicitud fue exitosa
        if req_primera.status_code != 200:
            print(f"Error al obtener datos para la temporada {temporada}: {req_primera.status_code}")
            continue

        # Paso la request a un objeto BeautifulSoup
        soup_primera = BeautifulSoup(req_primera.text, "html.parser")

        # Obtengo los datos de la temporada
        datos_primera = str(soup_primera)

        # Procesar equipos
        find_equipos(datos_primera)

        # Procesar partidos
        find_partidos(datos_primera, temporada, 1)

    return partidos




# Devuelvo el valor del contador
def get_contador():
    return contador

