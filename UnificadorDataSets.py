import pandas as pd

# Cargar los archivos de datos
df_partidos = pd.read_csv("DataSetPartidos.txt")
df_estadisticas_goles = pd.read_csv("estadisticas_creacion_goles.txt")
df_estadisticas_pases = pd.read_csv("estadisticas_pases.txt")
df_estadisticas_defensivas = pd.read_csv("estadisticas_defensivas.txt")
df_estadisticas_porteria = pd.read_csv("estadisticas_porteria.txt")

# Asegurar que las temporadas tengan un formato consistente
df_partidos['Temporada'] = df_partidos['Temporada'].str.replace("2017-18", "2017-2018")

# Merge con estadísticas de creación de goles del equipo visitante
merged_df = df_partidos.merge(
    df_estadisticas_goles.add_suffix('_visitante'),
    how="left",
    left_on=["EquipoVisitante", "Temporada"],
    right_on=["Equipo_visitante", "Temporada_visitante"]
).drop(columns=["Equipo_visitante", "Temporada_visitante"])

# Merge con estadísticas de creación de goles del equipo local
merged_df = merged_df.merge(
    df_estadisticas_goles.add_suffix('_local'),
    how="left",
    left_on=["EquipoLocal", "Temporada"],
    right_on=["Equipo_local", "Temporada_local"]
).drop(columns=["Equipo_local", "Temporada_local"])

# Merge con estadísticas de pases del equipo visitante
merged_df = merged_df.merge(
    df_estadisticas_pases.add_suffix('_visitante'),
    how="left",
    left_on=["EquipoVisitante", "Temporada"],
    right_on=["Equipo_visitante", "Temporada_visitante"]
).drop(columns=["Equipo_visitante", "Temporada_visitante"])

# Merge con estadísticas de pases del equipo local
merged_df = merged_df.merge(
    df_estadisticas_pases.add_suffix('_local'),
    how="left",
    left_on=["EquipoLocal", "Temporada"],
    right_on=["Equipo_local", "Temporada_local"]
).drop(columns=["Equipo_local", "Temporada_local"])

# Merge con estadísticas defensivas del equipo visitante
merged_df = merged_df.merge(
    df_estadisticas_defensivas.add_suffix('_visitante'),
    how="left",
    left_on=["EquipoVisitante", "Temporada"],
    right_on=["Equipo_visitante", "Temporada_visitante"]
).drop(columns=["Equipo_visitante", "Temporada_visitante"])

# Merge con estadísticas defensivas del equipo local
merged_df = merged_df.merge(
    df_estadisticas_defensivas.add_suffix('_local'),
    how="left",
    left_on=["EquipoLocal", "Temporada"],
    right_on=["Equipo_local", "Temporada_local"]
).drop(columns=["Equipo_local", "Temporada_local"])

# Merge con estadísticas de portería del equipo visitante
merged_df = merged_df.merge(
    df_estadisticas_porteria.add_suffix('_visitante'),
    how="left",
    left_on=["EquipoVisitante", "Temporada"],
    right_on=["Equipo_visitante", "Temporada_visitante"]
).drop(columns=["Equipo_visitante", "Temporada_visitante"])

# Merge con estadísticas de portería del equipo local
merged_df = merged_df.merge(
    df_estadisticas_porteria.add_suffix('_local'),
    how="left",
    left_on=["EquipoLocal", "Temporada"],
    right_on=["Equipo_local", "Temporada_local"]
).drop(columns=["Equipo_local", "Temporada_local"])

# Guardar el resultado en un archivo .txt separado por comas
output_path = 'merged_full_statistics.txt'
merged_df.to_csv(output_path, index=False, sep=",")

print(f"Archivo guardado en {output_path}")
