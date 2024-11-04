import requests
from bs4 import BeautifulSoup

# Función para extraer datos de una temporada dada
def extraer_datos_temporada(url, temporada):
    # Realizamos la solicitud a la página
    response = requests.get(url)
    
    # Verificar si la solicitud es exitosa
    if response.status_code == 200:
        print(f"Página {temporada} cargada correctamente.")
    else:
        print(f"Error al cargar la página {temporada}: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla correcta en la página
    tabla = soup.find('table', {'id': 'stats_squads_gca_for'})

    # Verificamos si se encontró la tabla
    if tabla:
        print(f"Tabla encontrada para la temporada {temporada}, comenzando a extraer datos...")
    else:
        print(f"No se encontró la tabla con id 'stats_squads_gca_for' para la temporada {temporada}.")
        print(soup.prettify()[:1000])  # Imprime los primeros 1000 caracteres del HTML para inspección
        return []

    # Extraemos las filas de la tabla
    filas = tabla.find('tbody').find_all('tr')  # type: ignore
    estadisticas_temporada = []

    # Iteramos sobre las filas de la tabla
    for fila in filas:
        columnas = fila.find_all('td')
        equipo = fila.find('th').text.strip() if fila.find('th') else "Sin equipo"

        # Imprimir equipo y número de columnas encontradas en la fila
        print(f"Equipo: {equipo}, Columnas encontradas: {len(columnas)}")

        # Verificamos que haya al menos 12 columnas para obtener SCA90 y GCA90
        if len(columnas) >= 12:
            sca90 = columnas[4].text.strip()
            gca90 = columnas[11].text.strip()

            # Imprimir los valores de SCA90 y GCA90
            print(f"SCA90: {sca90}, GCA90: {gca90}")

            estadisticas = {
                'Equipo': equipo,
                'SCA90': sca90,
                'GCA90': gca90,
                'Temporada': temporada  # Añadimos la temporada como campo adicional
            }
            estadisticas_temporada.append(estadisticas)
        else:
            print(f"Fila incompleta encontrada en temporada {temporada}: {len(columnas)} columnas, se omite.")

    # Devolvemos los datos extraídos
    return estadisticas_temporada

# Función para guardar los datos en un archivo .txt
def guardar_en_txt(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribimos los encabezados
        archivo.write('Equipo,SCA90,GCA90,Temporada\n')
        # Escribimos cada fila de estadísticas
        for estadistica in datos:
            archivo.write(f"{estadistica['Equipo']},{estadistica['SCA90']},{estadistica['GCA90']},{estadistica['Temporada']}\n")

# URL base para las temporadas
url_base = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/gca/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Lista para almacenar todas las estadísticas
estadisticas_totales = []

# Iteramos sobre los años de la temporada desde 2013-2014 hasta 2023-2024
for anio in range(2013, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"\nExtrayendo datos de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual
    estadisticas_temporada = extraer_datos_temporada(url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_totales.extend(estadisticas_temporada)

# Guardamos todos los datos en un solo archivo
guardar_en_txt(estadisticas_totales, "estadisticas_creacion_goles_tiros_reducido.txt")
print("Datos de todas las temporadas guardados en estadisticas_creacion_goles_tiros_reducido.txt")
