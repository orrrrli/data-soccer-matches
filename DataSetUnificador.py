import pandas as pd
import unidecode

# Cargar los archivos
partidos_df = pd.read_csv("DataSetPartidos.txt")
creacion_goles_tiros_df = pd.read_csv("estadisticas_creacion_goles_tiros.txt")
defensivas_df = pd.read_csv("estadisticas_defensivas.txt")
tipos_pases_df = pd.read_csv("estadisticas_tipos_pases.txt")
porteria_df = pd.read_csv("estadisticas_porteria.txt")
sueldo_df = pd.read_csv("estadisticas_sueldos_equipos.txt")
forma_df = pd.read_csv("estadisticas_forma_equipo_laliga.txt")
experiencia_df = pd.read_csv("estadisticas_experiencia_equipos.txt")

# Normalizar nombres de equipos
def normalize_team_name(name):
    name = unidecode.unidecode(name).lower().strip()
    name = name.replace(" cf", "").replace(" fc", "").replace(" ud", "").replace(" cd", "")
    return name

# Aplicar la normalización en todos los DataFrames
partidos_df['EquipoLocal'] = partidos_df['EquipoLocal'].apply(normalize_team_name)
partidos_df['EquipoVisitante'] = partidos_df['EquipoVisitante'].apply(normalize_team_name)
creacion_goles_tiros_df['Equipo'] = creacion_goles_tiros_df['Equipo'].apply(normalize_team_name)
defensivas_df['Equipo'] = defensivas_df['Equipo'].apply(normalize_team_name)
tipos_pases_df['Equipo'] = tipos_pases_df['Equipo'].apply(normalize_team_name)
porteria_df['Equipo'] = porteria_df['Equipo'].apply(normalize_team_name)
sueldo_df['Equipo'] = sueldo_df['Equipo'].apply(normalize_team_name)
forma_df['Equipo'] = forma_df['Equipo'].apply(normalize_team_name)
experiencia_df['Equipo'] = experiencia_df['Equipo'].apply(normalize_team_name)

# Mapeo manual para nombres inconsistentes específicos
nombre_corregido = {
    "athletic": "athletic club",
    "betis": "real betis",
    "real sociedad cf": "real sociedad",
    "rcd espanyol": "espanyol",
    "celta de vigo": "rc celta",
    "alaves": "deportivo alaves",
    "las palmas": "ud las palmas",
    "cadiz": "cadiz cf",
    # Añadir otras correcciones específicas según sea necesario
}

# Aplicar correcciones manuales en todos los DataFrames
def apply_name_corrections(df, team_column):
    df[team_column] = df[team_column].replace(nombre_corregido)
    return df

partidos_df = apply_name_corrections(partidos_df, 'EquipoLocal')
partidos_df = apply_name_corrections(partidos_df, 'EquipoVisitante')
creacion_goles_tiros_df = apply_name_corrections(creacion_goles_tiros_df, 'Equipo')
defensivas_df = apply_name_corrections(defensivas_df, 'Equipo')
tipos_pases_df = apply_name_corrections(tipos_pases_df, 'Equipo')
porteria_df = apply_name_corrections(porteria_df, 'Equipo')
sueldo_df = apply_name_corrections(sueldo_df, 'Equipo')
forma_df = apply_name_corrections(forma_df, 'Equipo')
experiencia_df = apply_name_corrections(experiencia_df, 'Equipo')

# Expandir forma_df para cubrir todas las temporadas
temporadas = ["2017-2018", "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024"]
forma_expanded = pd.concat([forma_df.assign(Temporada=season) for season in temporadas], ignore_index=True)

# Expandir experiencia_df para cubrir todas las temporadas
experiencia_expanded = pd.concat([experiencia_df.assign(Temporada=season) for season in temporadas], ignore_index=True)

# Verificar equipos únicos en cada dataset
print("Equipos en partidos_df (EquipoLocal):", partidos_df['EquipoLocal'].unique())
print("Equipos en partidos_df (EquipoVisitante):", partidos_df['EquipoVisitante'].unique())
print("Equipos en creacion_goles_tiros_df:", creacion_goles_tiros_df['Equipo'].unique())
print("Equipos en defensivas_df:", defensivas_df['Equipo'].unique())
print("Equipos en tipos_pases_df:", tipos_pases_df['Equipo'].unique())
print("Equipos en porteria_df:", porteria_df['Equipo'].unique())
print("Equipos en sueldo_df:", sueldo_df['Equipo'].unique())
print("Equipos en forma_df:", forma_df['Equipo'].unique())
print("Equipos en experiencia_df:", experiencia_df['Equipo'].unique())

# Verificar temporadas únicas en cada dataset
print("Temporadas en partidos_df:", partidos_df['temporada'].unique())
print("Temporadas en creacion_goles_tiros_df:", creacion_goles_tiros_df['Temporada'].unique())
print("Temporadas en defensivas_df:", defensivas_df['Temporada'].unique())
print("Temporadas en tipos_pases_df:", tipos_pases_df['Temporada'].unique())
print("Temporadas en porteria_df:", porteria_df['Temporada'].unique())
print("Temporadas en sueldo_df:", sueldo_df['Temporada'].unique())
print("Temporadas en forma_df:", forma_df['Temporada'].unique())  # Asegúrate de que esta columna existe aquí
print("Temporadas en experiencia_df:", experiencia_expanded['Temporada'].unique())


def merge_stats(df, stats_df, team_column, prefix):
    merged_df = df.merge(
        stats_df,
        left_on=[team_column, 'temporada'],
        right_on=['Equipo', 'Temporada'],
        suffixes=('', f'_{prefix}'),
        how='outer'  # Usar 'outer' para ver dónde faltan datos
    )
    
    # Verificar filas sin coincidencia
    no_match_local = merged_df[merged_df[f'Equipo_{prefix}'].isnull() | merged_df[team_column].isnull()]
    print(f"Filas sin coincidencia en {prefix} para el equipo {team_column}:", no_match_local)
    
    return merged_df

# Verificar equipos únicos en cada dataset
print("Equipos en partidos_df (EquipoLocal):", partidos_df['EquipoLocal'].unique())
print("Equipos en partidos_df (EquipoVisitante):", partidos_df['EquipoVisitante'].unique())
print("Equipos en creacion_goles_tiros_df:", creacion_goles_tiros_df['Equipo'].unique())
print("Equipos en defensivas_df:", defensivas_df['Equipo'].unique())
print("Equipos en tipos_pases_df:", tipos_pases_df['Equipo'].unique())
print("Equipos en porteria_df:", porteria_df['Equipo'].unique())
print("Equipos en sueldo_df:", sueldo_df['Equipo'].unique())
print("Equipos en forma_df:", forma_df['Equipo'].unique())
print("Equipos en experiencia_df:", experiencia_df['Equipo'].unique())

# Verificar temporadas únicas en cada dataset
print("Temporadas en partidos_df:", partidos_df['temporada'].unique())
print("Temporadas en creacion_goles_tiros_df:", creacion_goles_tiros_df['Temporada'].unique())
print("Temporadas en defensivas_df:", defensivas_df['Temporada'].unique())
print("Temporadas en tipos_pases_df:", tipos_pases_df['Temporada'].unique())
print("Temporadas en porteria_df:", porteria_df['Temporada'].unique())
print("Temporadas en sueldo_df:", sueldo_df['Temporada'].unique())
print("Temporadas en forma_df:", forma_df['Temporada'].unique())  # Asegúrate de que esta columna existe aquí
print("Temporadas en experiencia_df:", experiencia_expanded['Temporada'].unique())


# Unir cada tipo de estadística
partidos_df = merge_stats(partidos_df, creacion_goles_tiros_df, 'EquipoLocal', 'creacion_local')
partidos_df = merge_stats(partidos_df, creacion_goles_tiros_df, 'EquipoVisitante', 'creacion_visitante')
partidos_df = merge_stats(partidos_df, defensivas_df, 'EquipoLocal', 'defensiva_local')
partidos_df = merge_stats(partidos_df, defensivas_df, 'EquipoVisitante', 'defensiva_visitante')
partidos_df = merge_stats(partidos_df, tipos_pases_df, 'EquipoLocal', 'pases_local')
partidos_df = merge_stats(partidos_df, tipos_pases_df, 'EquipoVisitante', 'pases_visitante')
partidos_df = merge_stats(partidos_df, porteria_df, 'EquipoLocal', 'porteria_local')
partidos_df = merge_stats(partidos_df, porteria_df, 'EquipoVisitante', 'porteria_visitante')
partidos_df = merge_stats(partidos_df, experiencia_expanded, 'EquipoLocal', 'experiencia_local')
partidos_df = merge_stats(partidos_df, experiencia_expanded, 'EquipoVisitante', 'experiencia_visitante')
partidos_df = merge_stats(partidos_df, sueldo_df, 'EquipoLocal', 'sueldo_local')
partidos_df = merge_stats(partidos_df, sueldo_df, 'EquipoVisitante', 'sueldo_visitante')
partidos_df = merge_stats(partidos_df, forma_expanded, 'EquipoLocal', 'forma_local')
partidos_df = merge_stats(partidos_df, forma_expanded, 'EquipoVisitante', 'forma_visitante')

# Guardar el dataset maestro
partidos_df.to_csv("dataset_maestro.csv", index=False)

