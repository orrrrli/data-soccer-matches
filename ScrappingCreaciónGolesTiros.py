import requests
from bs4 import BeautifulSoup

# Función para extraer datos de una temporada dada
def extraer_datos_temporada(url, temporada):
    # Realizamos la solicitud a la página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla correcta en la página
    tabla = soup.find('table', {'id': 'stats_squads_gca_for'})

    # Verificamos si se encontró la tabla
    if tabla:
        print(f"Tabla encontrada para la temporada {temporada}, comenzando a extraer datos...")

        # Extraemos las filas de la tabla
        filas = tabla.find('tbody').find_all('tr') # type: ignore

        estadisticas_temporada = []

        # Iteramos sobre las filas de la tabla
        for fila in filas:
            columnas = fila.find_all('td')
            equipo = fila.find('th').text.strip()  # Aquí obtenemos el nombre del equipo
            if len(columnas) == 18:  # Solo procesamos filas con 18 columnas
                estadisticas = {
                    'Equipo': equipo,
                    'PL': columnas[0].text.strip(),
                    '90 Jugados': columnas[1].text.strip(),
                    'ACT': columnas[2].text.strip(),
                    'SCA90': columnas[3].text.strip(),
                    'PassLiveSCA': columnas[4].text.strip(),
                    'PassDeadSCA': columnas[5].text.strip(),
                    'TakeOnsSCA': columnas[6].text.strip(),
                    'ShotsSCA': columnas[7].text.strip(),
                    'FouledSCA': columnas[8].text.strip(),
                    'DefenseSCA': columnas[9].text.strip(),
                    'ACG': columnas[10].text.strip(),
                    'GCA90': columnas[11].text.strip(),
                    'PassLiveGCA': columnas[12].text.strip(),
                    'PassDeadGCA': columnas[13].text.strip(),
                    'TakeOnsGCA': columnas[14].text.strip(),
                    'ShotsGCA': columnas[15].text.strip(),
                    'FouledGCA': columnas[16].text.strip(),
                    'DefenseGCA': columnas[17].text.strip(),
                    'Temporada': temporada  # Añadimos la temporada como campo adicional
                }
                estadisticas_temporada.append(estadisticas)
            else:
                print(f"Fila incompleta encontrada en temporada {temporada}: {len(columnas)} columnas, se omite.")

        # Devolvemos los datos extraídos
        return estadisticas_temporada
    else:
        print(f"No se encontró la tabla para la temporada {temporada}")
        return []


# Función para guardar los datos en un archivo .txt
def guardar_en_txt(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribimos los encabezados
        archivo.write('Equipo,PL,90 Jugados,ACT,SCA90,PassLiveSCA,PassDeadSCA,TakeOnsSCA,ShotsSCA,FouledSCA,DefenseSCA,ACG,GCA90,PassLiveGCA,PassDeadGCA,TakeOnsGCA,ShotsGCA,FouledGCA,DefenseGCA,Temporada\n')
        # Escribimos cada fila de estadísticas
        for estadistica in datos:
            archivo.write(f"{estadistica['Equipo']},{estadistica['PL']},{estadistica['90 Jugados']},{estadistica['ACT']},{estadistica['SCA90']},{estadistica['PassLiveSCA']},{estadistica['PassDeadSCA']},{estadistica['TakeOnsSCA']},{estadistica['ShotsSCA']},{estadistica['FouledSCA']},{estadistica['DefenseSCA']},{estadistica['ACG']},{estadistica['GCA90']},{estadistica['PassLiveGCA']},{estadistica['PassDeadGCA']},{estadistica['TakeOnsGCA']},{estadistica['ShotsGCA']},{estadistica['FouledGCA']},{estadistica['DefenseGCA']},{estadistica['Temporada']}\n")


# URL base para las temporadas
url_base = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/gca/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Lista para almacenar todas las estadísticas
estadisticas_totales = []

# Iteramos sobre los años de la temporada desde 2013-2014 hasta 2023-2024
for anio in range(2013, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual
    estadisticas_temporada = extraer_datos_temporada(url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_totales.extend(estadisticas_temporada)

# Guardamos todos los datos en un solo archivo
guardar_en_txt(estadisticas_totales, "estadisticas_creacion_goles_tiros.txt")
print("Datos de todas las temporadas guardados en estadisticas_creacion_goles_tiros.txt")
