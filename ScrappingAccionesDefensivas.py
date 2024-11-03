import requests
from bs4 import BeautifulSoup

# Función para extraer datos de una temporada dada
def extraer_datos_temporada_defensiva(url, temporada):
    # Realizamos la solicitud a la página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la tabla correcta en la página
    tabla = soup.find('table', {'id': 'stats_squads_defense_for'})

    # Verificamos si se encontró la tabla
    if tabla:
        print(f"Tabla defensiva encontrada para la temporada {temporada}, comenzando a extraer datos...")

        # Extraemos las filas de la tabla
        filas = tabla.find('tbody').find_all('tr') # type: ignore

        estadisticas_temporada = []

        # Iteramos sobre las filas de la tabla
        for fila in filas:
            columnas = fila.find_all('td')
            equipo = fila.find('th').text.strip()  # Aquí obtenemos el nombre del equipo
            if len(columnas) == 18:  # Ajustamos el número de columnas esperadas para defensa
                estadisticas = {
                    'Equipo': equipo,
                    'PL': columnas[0].text.strip(),
                    '90 Jugados': columnas[1].text.strip(),
                    'Tackles': columnas[2].text.strip(),  # Derribos
                    'Tackles Ganados': columnas[3].text.strip(),
                    'Tackles Defensa 1/3': columnas[4].text.strip(),
                    'Tackles Medio 1/3': columnas[5].text.strip(),
                    'Tackles Ataque 1/3': columnas[6].text.strip(),
                    'Dribladores Tackleados': columnas[7].text.strip(),
                    'Dribleos Desafiados': columnas[8].text.strip(),
                    '% Tackle Dribladores': columnas[9].text.strip(),
                    'Desafíos Perdidos': columnas[10].text.strip(),
                    'Bloqueos': columnas[11].text.strip(),
                    'Disparos Bloqueados': columnas[12].text.strip(),
                    'Pases Bloqueados': columnas[13].text.strip(),
                    'Intercepciones': columnas[14].text.strip(),
                    'Tackles + Intercepciones': columnas[15].text.strip(),
                    'Despejes': columnas[16].text.strip(),
                    'Errores': columnas[17].text.strip(),
                    'Temporada': temporada  # Añadimos la temporada como campo adicional
                }
                estadisticas_temporada.append(estadisticas)
            else:
                print(f"Fila incompleta encontrada en temporada {temporada}: {len(columnas)} columnas, se omite.")

        # Devolvemos los datos extraídos
        return estadisticas_temporada
    else:
        print(f"No se encontró la tabla defensiva para la temporada {temporada}")
        return []


# Función para guardar los datos en un archivo .txt
def guardar_en_txt_defensiva(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribimos los encabezados
        archivo.write('Equipo,PL,90 Jugados,Tackles,Tackles Ganados,Tackles Defensa 1/3,Tackles Medio 1/3,Tackles Ataque 1/3,Dribladores Tackleados,Dribleos Desafiados,% Tackle Dribladores,Desafíos Perdidos,Bloqueos,Disparos Bloqueados,Pases Bloqueados,Intercepciones,Tackles + Intercepciones,Despejes,Errores,Temporada\n')
        # Escribimos cada fila de estadísticas
        for estadistica in datos:
            archivo.write(f"{estadistica['Equipo']},{estadistica['PL']},{estadistica['90 Jugados']},{estadistica['Tackles']},{estadistica['Tackles Ganados']},{estadistica['Tackles Defensa 1/3']},{estadistica['Tackles Medio 1/3']},{estadistica['Tackles Ataque 1/3']},{estadistica['Dribladores Tackleados']},{estadistica['Dribleos Desafiados']},{estadistica['% Tackle Dribladores']},{estadistica['Desafíos Perdidos']},{estadistica['Bloqueos']},{estadistica['Disparos Bloqueados']},{estadistica['Pases Bloqueados']},{estadistica['Intercepciones']},{estadistica['Tackles + Intercepciones']},{estadistica['Despejes']},{estadistica['Errores']},{estadistica['Temporada']}\n")


# URL base para las temporadas defensivas
url_base_defensiva = 'https://fbref.com/es/comps/12/{anio}-{anio_siguiente}/defense/Estadisticas-{anio}-{anio_siguiente}-La-Liga'

# Lista para almacenar todas las estadísticas defensivas
estadisticas_defensivas_totales = []

# Iteramos sobre los años de la temporada desde 2013-2014 hasta 2023-2024
for anio in range(2013, 2024):
    anio_siguiente = anio + 1
    temporada = f"{anio}-{anio_siguiente}"
    url_temporada = url_base_defensiva.format(anio=anio, anio_siguiente=anio_siguiente)

    print(f"Extrayendo datos defensivos de la temporada: {temporada}")
    
    # Extraemos los datos de la temporada defensiva actual
    estadisticas_temporada_defensiva = extraer_datos_temporada_defensiva(url_temporada, temporada)
    
    # Añadimos las estadísticas de esta temporada a la lista total
    estadisticas_defensivas_totales.extend(estadisticas_temporada_defensiva)

# Guardamos todos los datos en un solo archivo
guardar_en_txt_defensiva(estadisticas_defensivas_totales, "estadisticas_defensivas.txt")
print("Datos defensivos de todas las temporadas guardados en estadisticas_defensivas.txt")
