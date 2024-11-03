import requests
from bs4 import BeautifulSoup

# Función para extraer datos de una temporada dada para estadísticas avanzadas de porteros
def extraer_datos_temporada_porteros(url, temporada):
    # Realizamos la solicitud a la página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla correcta en la página
    tabla = soup.find('table', {'id': 'stats_squads_keeper_adv_for'})

    # Verificamos si se encontró la tabla
    if tabla:
        print(f"Tabla de porteros avanzada encontrada para la temporada {temporada}, comenzando a extraer datos...")

        # Extraemos las filas de la tabla
        filas = tabla.find('tbody').find_all('tr')  # type: ignore

        estadisticas_temporada = []

        # Iteramos sobre las filas de la tabla
        for fila in filas:
            columnas = fila.find_all('td')
            equipo = fila.find('th').text.strip()  # Nombre del equipo
            if len(columnas) == 27:  # Ajustamos el número de columnas esperadas para porteros avanzados
                estadisticas = {
                    'Equipo': equipo,
                    'PL': columnas[0].text.strip(),
                    '90 Jugados': columnas[1].text.strip(),
                    'Goles en contra': columnas[2].text.strip(),
                    'Penales concedidos': columnas[3].text.strip(),
                    'Goles de tiro libre': columnas[4].text.strip(),
                    'Goles de tiro de esquina': columnas[5].text.strip(),
                    'Goles propios': columnas[6].text.strip(),
                    'Goles esperados': columnas[7].text.strip(),
                    'PSxG/SoT': columnas[8].text.strip(),
                    'PSxG-GA': columnas[9].text.strip(),
                    'PSxG-GA/90': columnas[10].text.strip(),
                    'Pases completados (Iniciado)': columnas[11].text.strip(),
                    'Pases intentados (Iniciado)': columnas[12].text.strip(),
                    'Porcentaje pase (Iniciado)': columnas[13].text.strip(),
                    'Pases Intentados (GK)': columnas[14].text.strip(),
                    'Tiros intentados': columnas[15].text.strip(),
                    '% Lanzamiento': columnas[16].text.strip(),
                    'Promedio longitud pase': columnas[17].text.strip(),
                    'Saques de meta': columnas[18].text.strip(),
                    '% Lanzamiento (Saques)': columnas[19].text.strip(),
                    'Promedio longitud saques': columnas[20].text.strip(),
                    'Cruces superados': columnas[21].text.strip(),
                    'Cruces detenidos': columnas[22].text.strip(),
                    '% Cruces detenidos': columnas[23].text.strip(),
                    'Acciones defensivas fuera del área': columnas[24].text.strip(),
                    'OPA/90': columnas[25].text.strip(),
                    'Distancia promedio defensiva': columnas[26].text.strip(),
                    'Temporada': temporada  # Añadimos la temporada como campo adicional
                }
                estadisticas_temporada.append(estadisticas)
            else:
                print(f"Fila incompleta encontrada en temporada {temporada}: {len(columnas)} columnas, se omite.")

        # Devolvemos los datos extraídos
        return estadisticas_temporada
    else:
        print(f"No se encontró la tabla de porteros avanzada para la temporada {temporada}")
        return []


# Función para guardar los datos en un archivo .txt
def guardar_en_txt_porteros(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribimos los encabezados
        archivo.write('Equipo,PL,90 Jugados,Goles en contra,Penales concedidos,Goles de tiro libre,Goles de tiro de esquina,Goles propios,Goles esperados,PSxG/SoT,PSxG-GA,PSxG-GA/90,Pases completados (Iniciado),Pases intentados (Iniciado),Porcentaje pase (Iniciado),Pases Intentados (GK),Tiros intentados,% Lanzamiento,Promedio longitud pase,Saques de meta,% Lanzamiento (Saques),Promedio longitud saques,Cruces superados,Cruces detenidos,% Cruces detenidos,Acciones defensivas fuera del área,OPA/90,Distancia promedio defensiva,Temporada\n')
        # Escribimos cada fila de estadísticas
        for estadistica in datos:
            archivo.write(','.join([estadistica.get(col, '') for col in estadistica]) + '\n')


# URL base para las temporadas de porteros avanzadas
url_base_porteros = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/keepersadv/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Lista para almacenar todas las estadísticas avanzadas de porteros
estadisticas_porteros_totales = []

# Iteramos sobre los años de la temporada desde 2013-2014 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_porteros.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos avanzados de porteros de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual para porteros avanzados
    estadisticas_temporada_porteros = extraer_datos_temporada_porteros(url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_porteros_totales.extend(estadisticas_temporada_porteros)

# Guardamos todos los datos en un solo archivo
guardar_en_txt_porteros(estadisticas_porteros_totales, "estadisticas_porteria.txt")
print("Datos avanzados de porteros de todas las temporadas guardados en estadisticas_porteria.txt")
