import pandas as pd
import unidecode

# Cargar archivos de partidos y estadisticas de portería
partidos_df = pd.read_csv("DataSetPartidos.txt")
porteria_df = pd.read_csv("estadisticas_porteria.txt")

# Función para normalizar los nombres de equipos
def normalize_team_name(name):
    name = unidecode.unidecode(name).lower().strip()
    name = name.replace(" cf", "").replace(" fc", "").replace(" ud", "").replace(" cd", "")
    return name

# Normalizar nombres de equipo en ambos DataFrames
partidos_df['EquipoLocal'] = partidos_df['EquipoLocal'].apply(normalize_team_name)
partidos_df['EquipoVisitante'] = partidos_df['EquipoVisitante'].apply(normalize_team_name)
porteria_df['Equipo'] = porteria_df['Equipo'].apply(normalize_team_name)

# Realizar correcciones manuales en los nombres de equipo
nombre_corregido = {
    "athletic": "athletic club",
    "betis": "real betis",
    "real sociedad cf": "real sociedad",
    "rcd espanyol": "espanyol",
    "celta de vigo": "rc celta",
    "alaves": "deportivo alaves",
    "las palmas": "ud las palmas",
    "cadiz": "cadiz cf",
    # Añadir otras correcciones específicas si es necesario
}

# Aplicar las correcciones a ambos DataFrames
partidos_df['EquipoLocal'] = partidos_df['EquipoLocal'].replace(nombre_corregido)
partidos_df['EquipoVisitante'] = partidos_df['EquipoVisitante'].replace(nombre_corregido)
porteria_df['Equipo'] = porteria_df['Equipo'].replace(nombre_corregido)

# Realizar el merge para `EquipoLocal` y `EquipoVisitante` por separado
# `porteria_local` y `porteria_visitante` para diferenciar las estadísticas

partidos_df = partidos_df.merge(
    porteria_df,
    left_on=['EquipoLocal', 'temporada'],
    right_on=['Equipo', 'Temporada'],
    suffixes=('', '_porteria_local'),
    how='left'
)

partidos_df = partidos_df.merge(
    porteria_df,
    left_on=['EquipoVisitante', 'temporada'],
    right_on=['Equipo', 'Temporada'],
    suffixes=('', '_porteria_visitante'),
    how='left'
)

# Exportar el DataFrame resultante a un archivo .txt separado por comas
partidos_df.to_csv("MasterDataSet.txt", index=False, sep=',')

print("Exportación a 'MasterDataSet.txt' completada.")
