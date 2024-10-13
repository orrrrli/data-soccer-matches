import requests
from bs4 import BeautifulSoup
import unicodedata

# Función para normalizar el texto y eliminar acentos
def normalize_text(text):
    normalized = unicodedata.normalize('NFKD', text)
    return normalized.encode('ASCII', 'ignore').decode('utf-8')

# Función para obtener las estadísticas de la temporada 2023-2024
def obtener_estadisticas_temporada_2023_2024():
    temporada = "2023-2024"
    url = f"https://fbref.com/es/comps/12/2023-2024/gca/2023-2024-La-Liga-Creacion-de-Goles"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error al obtener datos para la temporada {temporada}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Obtener la temporada desde el encabezado del HTML
    temporada_tag = soup.find('span', {'style': 'color: #666; font-size:smaller'})
    temporada_text = temporada_tag.text if temporada_tag else f"{temporada}"
    print(f"Extrayendo datos de la temporada: {temporada_text}")

    table = soup.find('table', {'id': 'stats_squads_gca_for'})

    if not table:
        print(f"No se encontró la tabla para la temporada {temporada}")
        return []

    tbody = table.find('tbody')
    estadisticas_temporada = []

    for row in tbody.find_all('tr'): # type: ignore
        cols = row.find_all('td')
        
        # Verificación para asegurarse de que la fila tiene al menos 18 columnas
        if len(cols) != 19:
            print(f"Fila incompleta encontrada en temporada {temporada}: {len(cols)} columnas, se omite.")
            continue

        equipo = normalize_text(cols[0].text.strip())  # Columna del equipo
        pl = cols[1].text.strip()  # Nro. de jugadores (PL)
        minutes_90s = cols[2].text.strip()  # 90 Jugados (minutos_90s)
        act = cols[3].text.strip()  # ACT (Acciones para la creación de tiros)
        sca90 = cols[4].text.strip()  # SCA por 90 minutos
        pass_live_sca = cols[5].text.strip()  # Pase de Balón Vivo (SCA)
        pass_dead_sca = cols[6].text.strip()  # Pase de Balón Muerto (SCA)
        take_ons_sca = cols[7].text.strip()  # ACT (Toma)
        shots_sca = cols[8].text.strip()  # ACT (Tiro)
        fouled_sca = cols[9].text.strip()  # ACT (Faltas recibidas)
        defense_sca = cols[10].text.strip()  # ACT (Acción Defensiva)
        acg = cols[11].text.strip()  # ACG (Acciones para la creación de goles)
        gca90 = cols[12].text.strip()  # GCA por 90 minutos
        pass_live_gca = cols[13].text.strip()  # Pase de Balón Vivo (GCA)
        pass_dead_gca = cols[14].text.strip()  # Pase de Balón Muerto (GCA)
        take_ons_gca = cols[15].text.strip()  # ACG (Toma)
        shots_gca = cols[16].text.strip()  # ACG (Tiro)
        fouled_gca = cols[17].text.strip()  # ACG (Faltas recibidas)
        defense_gca = cols[18].text.strip()  # ACG (Acción Defensiva)

        # Añadir los datos de esta fila a la lista
        estadisticas_temporada.append({
            'Equipo': equipo,
            'PL': pl,
            '90 Jugados': minutes_90s,
            'ACT': act,
            'SCA90': sca90,
            'PassLiveSCA': pass_live_sca,
            'PassDeadSCA': pass_dead_sca,
            'TakeOnsSCA': take_ons_sca,
            'ShotsSCA': shots_sca,
            'FouledSCA': fouled_sca,
            'DefenseSCA': defense_sca,
            'ACG': acg,
            'GCA90': gca90,
            'PassLiveGCA': pass_live_gca,
            'PassDeadGCA': pass_dead_gca,
            'TakeOnsGCA': take_ons_gca,
            'ShotsGCA': shots_gca,
            'FouledGCA': fouled_gca,
            'DefenseGCA': defense_gca,
            'Temporada': temporada_text  # Se asigna la temporada extraída del HTML
        })

    return estadisticas_temporada

# Obtener las estadísticas de la temporada 2023-2024
estadisticas_temporada_2023_2024 = obtener_estadisticas_temporada_2023_2024()

# Función para guardar los datos en un archivo .txt
def guardar_en_txt(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribir el encabezado
        archivo.write("Equipo,PL,90 Jugados,ACT,SCA90,PassLiveSCA,PassDeadSCA,TakeOnsSCA,ShotsSCA,FouledSCA,DefenseSCA,ACG,GCA90,PassLiveGCA,PassDeadGCA,TakeOnsGCA,ShotsGCA,FouledGCA,DefenseGCA,Temporada\n")
        # Escribir los datos
        for estadistica in datos:
            archivo.write(f"{estadistica['Equipo']},{estadistica['PL']},{estadistica['90 Jugados']},{estadistica['ACT']},{estadistica['SCA90']},{estadistica['PassLiveSCA']},{estadistica['PassDeadSCA']},{estadistica['TakeOnsSCA']},{estadistica['ShotsSCA']},{estadistica['FouledSCA']},{estadistica['DefenseSCA']},{estadistica['ACG']},{estadistica['GCA90']},{estadistica['PassLiveGCA']},{estadistica['PassDeadGCA']},{estadistica['TakeOnsGCA']},{estadistica['ShotsGCA']},{estadistica['FouledGCA']},{estadistica['DefenseGCA']},{estadistica['Temporada']}\n")
    print(f"Datos guardados en {nombre_archivo}")

# Guardar los datos de la temporada 2023-2024 en un archivo .txt
guardar_en_txt(estadisticas_temporada_2023_2024, "estadisticas_creacion_goles_tiros_2023_2024.txt")
