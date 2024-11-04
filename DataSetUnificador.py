import pandas as pd
import unidecode

# Cargar archivos de partidos y estadísticas de portería
partidos_df = pd.read_csv("DataSetPartidos.txt")
porteria_df = pd.read_csv("estadisticas_porteria.txt")

# Función para normalizar los nombres de equipos
def normalize_team_name(name):
    name = unidecode.unidecode(name).lower().strip()
    name = name.replace(" cf", "").replace(" fc", "").replace(" ud", "").replace(" cd", "")
    
    # Corrección específica para "Celta de Vigo" a "Celta Vigo"
    if name == "celta de vigo":
        name = "celta vigo"
    
    return name

# Normalizar nombres de equipo en ambos DataFrames
partidos_df['EquipoLocal'] = partidos_df['EquipoLocal'].apply(normalize_team_name)
partidos_df['EquipoVisitante'] = partidos_df['EquipoVisitante'].apply(normalize_team_name)
porteria_df['Equipo'] = porteria_df['Equipo'].apply(normalize_team_name)

# Formatear la columna Temporada en ambos DataFrames al mismo formato
partidos_df['Temporada'] = partidos_df['Temporada'].apply(lambda x: x.replace('-', ''))
porteria_df['Temporada'] = porteria_df['Temporada'].apply(lambda x: x.replace('-', ''))

# Realizar correcciones manuales en los nombres de equipo
nombre_corregido = {
    "athletic": "athletic club",
    "betis": "real betis",
    "real sociedad cf": "real sociedad",
    "rcd espanyol": "espanyol",
    "celta de vigo": "celta vigo",  # Ajuste específico
    "alaves": "deportivo alaves",
    "las palmas": "ud las palmas",
    "cadiz": "cadiz cf",
}

# Aplicar las correcciones a ambos DataFrames
partidos_df['EquipoLocal'] = partidos_df['EquipoLocal'].replace(nombre_corregido)
partidos_df['EquipoVisitante'] = partidos_df['EquipoVisitante'].replace(nombre_corregido)
porteria_df['Equipo'] = porteria_df['Equipo'].replace(nombre_corregido)

# Realizar el merge para `EquipoLocal` y `EquipoVisitante` por separado
# Agregamos un sufijo para diferenciar las estadísticas del equipo local y visitante

# Merge para el equipo local
partidos_df = partidos_df.merge(
    porteria_df,
    left_on=['EquipoLocal', 'Temporada'],
    right_on=['Equipo', 'Temporada'],
    suffixes=('', '_porteria_local'),
    how='left'
)

print("Tamaño de DataFrame después del primer merge (EquipoLocal):", partidos_df.shape)

# Merge para el equipo visitante
partidos_df = partidos_df.merge(
    porteria_df,
    left_on=['EquipoVisitante', 'Temporada'],
    right_on=['Equipo', 'Temporada'],
    suffixes=('', '_porteria_visitante'),
    how='left'
)

print("Tamaño de DataFrame después del segundo merge (EquipoVisitante):", partidos_df.shape)

# Exportar el DataFrame resultante a un archivo .txt separado por comas
partidos_df.to_csv("MasterDataSet.txt", index=False, sep=',')

print("Exportación a 'MasterDataSet.txt' completada.")
