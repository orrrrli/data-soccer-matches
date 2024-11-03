import requests
from bs4 import BeautifulSoup

# Función para extraer datos de tipos de pases de una temporada dada
def extraer_datos_temporada_pases(url, temporada):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tabla = soup.find('table', {'id': 'stats_squads_passing_types_for'})
    
    if not tabla:
        print(f"No se encontró la tabla de tipos de pases para la temporada {temporada}")
        return []

    print(f"Tabla de tipos de pases encontrada para la temporada {temporada}, comenzando a extraer datos...")

    # Estructura de los datos esperados con 'data-stat'
    columnas_esperadas = [
        'team', 'players_used', 'minutes_90s', 'passes', 'passes_live', 'passes_dead', 
        'passes_free_kicks', 'through_balls', 'passes_switches', 'crosses', 'throw_ins', 
        'corner_kicks', 'corner_kicks_in', 'corner_kicks_out', 'corner_kicks_straight', 
        'passes_completed', 'passes_offsides', 'passes_blocked'
    ]

    filas = tabla.find('tbody').find_all('tr') # type: ignore
    estadisticas_temporada = []

    for fila in filas:
        estadisticas = {'Temporada': temporada}
        columnas = fila.find_all('td')
        
        # Asignamos cada dato de acuerdo con su `data-stat`
        for columna in columnas:
            data_stat = columna.get('data-stat')
            if data_stat in columnas_esperadas:
                estadisticas[data_stat] = columna.text.strip()

        # Verificación de que se hayan extraído los datos suficientes
        if len(estadisticas) > 1:  # Solo agrega filas que tengan datos adicionales a 'Temporada'
            estadisticas_temporada.append(estadisticas)
        else:
            print(f"Fila incompleta en temporada {temporada}, datos encontrados: {len(columnas)} columnas")

    return estadisticas_temporada

# Función para guardar los datos en un archivo .txt
def guardar_en_txt_pases(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Encabezados basados en `data-stat`
        archivo.write(','.join(['Equipo', 'PL', '90 Jugados', 'Pases Intentados', 'Pases de Balón Vivo', 
                                'Pases de Balón Muerto', 'Pases de Tiros Libres', 'Pases Largos', 
                                'Cambios', 'Pases Cruzados', 'Lanzamientos Tomados', 'Saques de Esquina', 
                                'SE hacia adentro', 'SE hacia afuera', 'SE rectos', 'Pases Completados', 
                                'Pases Fuera de Juego', 'Pases Bloqueados', 'Temporada']) + '\n')

        for estadistica in datos:
            # Guardamos cada dato, tomando valores vacíos si faltan
            archivo.write(','.join([estadistica.get(col, '') for col in [
                'team', 'players_used', 'minutes_90s', 'passes', 'passes_live', 'passes_dead', 
                'passes_free_kicks', 'through_balls', 'passes_switches', 'crosses', 'throw_ins', 
                'corner_kicks', 'corner_kicks_in', 'corner_kicks_out', 'corner_kicks_straight', 
                'passes_completed', 'passes_offsides', 'passes_blocked', 'Temporada'
            ]]) + '\n')

# URL base para las temporadas de tipos de pases
url_base_pases = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/passing_types/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Lista para almacenar todas las estadísticas de tipos de pases
estadisticas_pases_totales = []

# Iteramos sobre los años de la temporada desde 2017-2018 hasta 2023-2024
for anio in range(2017, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_pases.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos de tipos de pases de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada actual
    estadisticas_temporada_pases = extraer_datos_temporada_pases(url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_pases_totales.extend(estadisticas_temporada_pases)

# Guardamos todos los datos en un solo archivo
guardar_en_txt_pases(estadisticas_pases_totales, "estadisticas_pases_2017_2024.txt")
print("Datos de tipos de pases de todas las temporadas guardados en estadisticas_pases_2017_2024.txt")
