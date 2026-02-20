import matplotlib.pyplot as plt
import numpy as np 
import joblib # para la ampliación: guarda el modelo
import os # para la ampliación
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score

lima = '\33[38;5;46m'
turquesa = '\033[38;5;44m'
reset = '\033[0m'

# Selección y Preparación del Dataset
print(f"\n{lima}Cargando MNIST... (esto puede tardar unos segundos){reset}")
mnist = fetch_openml('mnist_784', version=1, as_frame=False)
X, y = mnist.data, mnist.target

# Normalización [0, 1]
X = X / 255.0 # Dividimos para que el valor de los pixeles estén entre 0 y 1

# División en entrenamiento (80%) y test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Diseño del Experimento (Grid Search) 
# Definimos qué variantes queremos que la máquina pruebe sola
param_grid = {
    'hidden_layer_sizes': [(50,), (100,)], # Una capa de 50 neuronas o una de 100
    'activation': ['relu', 'logistic'],    # Funciones de activación
    'learning_rate_init': [0.001, 0.01],    # Velocidad de aprendizaje
    'solver': ['sgd', 'adam'] # Ampliación: comparativa
}

print(f"{lima}\nIniciando Grid Search (Buscando la mejor configuración)...{reset}")
mlp = MLPClassifier(max_iter=10) # max_iter bajo para que el ejemplo sea rápido
grid = GridSearchCV(MLPClassifier(max_iter=20), param_grid, cv=3, n_jobs=-1)
grid.fit(X_train[:2000], y_train[:2000]) # Usamos una muestra pequeña para ir rápido

print(f"{turquesa}\nMejor configuración encontrada:{reset} {grid.best_params_}")

# Entrenamiento del Modelo Final
# Entrenamos el mejor modelo con más datos
best_mlp = grid.best_estimator_
best_mlp.fit(X_train, y_train)

# Ampliación: Persistencia. Guardar el modelo
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_modelo = os.path.join(directorio_actual, 'modelo_ocr_mnist.pkl')
joblib.dump(best_mlp, ruta_modelo)
print(f"\n{lima}Modelo guardado exitosamente en:{reset} {ruta_modelo}")

# Análisis de Resultados
predictions = best_mlp.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Precisión final (Accuracy): {accuracy * 100:.2f}%")

# Matriz de Confusión
cm = confusion_matrix(y_test, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)

# Traqducción de los títulos de la matriz
plt.title("Matriz de Confusión")
plt.xlabel("Etiqueta Predicha")  
plt.ylabel("Etiqueta Real")     
plt.show()

# Identificar fallos
fallos_idx = np.where(predictions != y_test)[0]
plt.figure(figsize=(10, 4))
for i, idx in enumerate(fallos_idx[:3]):
    plt.subplot(1, 3, i + 1)
    plt.imshow(X_test[idx].reshape(28, 28), cmap='gray')
    plt.title(f"Pred: {predictions[idx]} | Real: {y_test[idx]}")
plt.tight_layout()
plt.show()