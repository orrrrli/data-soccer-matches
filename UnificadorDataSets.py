import pandas as pd

# Cargar los archivos de datos
df_partidos = pd.read_csv("DataSetPartidos.txt")
df_estadisticas_tiros = pd.read_csv("estadisticas_tiros_2017_2024.txt")

# Asegurar que las temporadas tengan un formato consistente en ambos datasets
df_partidos['Temporada'] = df_partidos['Temporada'].str.replace("2017-18", "2017-2018")
df_estadisticas_tiros['Temporada'] = df_estadisticas_tiros['Temporada'].str.replace("2017-18", "2017-2018")

# Merge con estadísticas de tiros del equipo visitante
merged_df = df_partidos.merge(
    df_estadisticas_tiros.add_suffix('_visitante'),
    how="left",
    left_on=["EquipoVisitante", "Temporada"],
    right_on=["Equipo_visitante", "Temporada_visitante"]
).drop(columns=["Equipo_visitante", "Temporada_visitante"])

# Merge con estadísticas de tiros del equipo local
merged_df = merged_df.merge(
    df_estadisticas_tiros.add_suffix('_local'),
    how="left",
    left_on=["EquipoLocal", "Temporada"],
    right_on=["Equipo_local", "Temporada_local"]
).drop(columns=["Equipo_local", "Temporada_local"])

# Guardar el resultado en un archivo .txt separado por comas
output_path = 'merged_partidos_estadisticas_tiros.txt'
merged_df.to_csv(output_path, index=False, sep=",")

print(f"Archivo guardado en {output_path}")
