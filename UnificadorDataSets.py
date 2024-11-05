import pandas as pd

# Cargar tus datos
df_partidos = pd.read_csv("DataSetPartidos.txt")
df_estadisticas = pd.read_csv("estadisticas_creacion_goles.txt")

# Asegurar que las temporadas tengan un formato consistente
df_partidos['Temporada'] = df_partidos['Temporada'].str.replace("2017-18", "2017-2018")

# Merge con estadísticas del equipo visitante
merged_df = df_partidos.merge(
    df_estadisticas.add_suffix('_visitante'),
    how="left",
    left_on=["EquipoVisitante", "Temporada"],
    right_on=["Equipo_visitante", "Temporada_visitante"]
).drop(columns=["Equipo_visitante", "Temporada_visitante"])

# Merge con estadísticas del equipo local
merged_df = merged_df.merge(
    df_estadisticas.add_suffix('_local'),
    how="left",
    left_on=["EquipoLocal", "Temporada"],
    right_on=["Equipo_local", "Temporada_local"]
).drop(columns=["Equipo_local", "Temporada_local"])

# Reorganizar las columnas en el orden deseado
column_order = [
    'idPartido', 'EquipoLocal', 'EquipoVisitante', 'golesLocal', 'golesVisitante', 
    'Temporada', 'SCA90_local', 'GCA90_local', 'SCA90_visitante', 'GCA90_visitante'
]
merged_df = merged_df[column_order]

# Guardar el resultado en un archivo .txt separado por comas
output_path = 'merged_match_statistics.txt'
merged_df.to_csv(output_path, index=False, sep=",")

print(f"Archivo guardado en {output_path}")
