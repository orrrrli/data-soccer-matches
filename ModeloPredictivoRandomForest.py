import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Cargar los datos
data = pd.read_csv("merged_full_statistics.txt")

# Crear columna objetivo: 1 si el equipo local gana, 0 si pierde, -1 si empata
data['target'] = data.apply(lambda x: 1 if x['golesLocal'] > x['golesVisitante'] else (0 if x['golesLocal'] < x['golesVisitante'] else -1), axis=1)

# Crear nuevas características (diferencias entre local y visitante)
data['SCA90_dif'] = data['SCA90_local'] - data['SCA90_visitante']
data['GCA90_dif'] = data['GCA90_local'] - data['GCA90_visitante']
data['Pases_Completados_dif'] = data['Pases Completados_local'] - data['Pases Completados_visitante']
data['Distancia_Progresiva_dif'] = data['Distancia Progresiva de Pase_local'] - data['Distancia Progresiva de Pase_visitante']
data['Asistencias_Esperadas_dif'] = data['Asistencias Esperadas_local'] - data['Asistencias Esperadas_visitante']
# Puedes crear más diferencias de esta forma para capturar el rendimiento relativo de cada equipo

# Separar características y objetivo
X = data.drop(columns=['idPartido', 'EquipoLocal', 'EquipoVisitante', 'golesLocal', 'golesVisitante', 'Temporada', 'target'])
y = data['target']

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Optimización con GridSearchCV (ajustando hiperparámetros de Random Forest)
param_grid = {
    'n_estimators': [100, 200, 300],  # Aumentar el número de árboles
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']  # Ajustar el número de características
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Mejor modelo encontrado
best_rf_model = grid_search.best_estimator_

# Evaluación del modelo optimizado
y_pred = best_rf_model.predict(X_test)
print("\nMejor Modelo de Random Forest")
print(f"Exactitud: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

# Mostrar la importancia de las características en el modelo optimizado
importances = best_rf_model.feature_importances_
feature_names = X.columns

# Ordenar las características por importancia
feature_importances = pd.DataFrame({'feature': feature_names, 'importance': importances})
feature_importances = feature_importances.sort_values(by='importance', ascending=False)

print("\nImportancia de las características:")
print(feature_importances)
