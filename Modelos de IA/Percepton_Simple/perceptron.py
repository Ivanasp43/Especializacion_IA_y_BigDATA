import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# colores
azul = '\033[94m'
magenta = '\033[95m'
turquesa = '\033[38;5;44m'
lima = '\33[38;5;46m'
reset = '\033[0m'

# PREPARACIÓN DE LOS DATOS 

# Cargamos el archivo que me has pasado
df = pd.read_csv('mountains_vs_beaches_preferences.csv')

# Elegimos 4 variables que ya son numéricas
columnas_interes = ['Age', 'Travel_Frequency', 'Proximity_to_Mountains', 'Proximity_to_Beaches', 'Preference']
datos = df[columnas_interes].copy()

# ESCALADO DE DATOS 
# Separamos X e y
X = datos.drop('Preference', axis=1).values
y = datos['Preference'].values

# Escalado estándar (media 0, desviación 1)
X = (X - X.mean(axis=0)) / X.std(axis=0)

# Dividimos el dataset: 80% para entrenar y 20% para probar si el modelo aprendió
limite = int(len(datos) * 0.8)
X_train = X[:limite]
y_train = y[:limite]

X_test = X[limite:]
y_test = y[limite:]


# MODELO PERCEPTRÓN 

class PerceptronSimple:
    def __init__(self, aprendizaje=0.01, epocas=50):
        self.eta = aprendizaje  
        self.n_iter = epocas    
        self.w_ = None          
        self.b_ = None  
        self.errors_ = []        

    def fit(self, X, y):
        self.w_ = np.zeros(X.shape[1])
        self.b_ = 0.0

        for _ in range(self.n_iter):
            errores = 0
            for xi, objetivo in zip(X, y):
                prediccion = self.predict(xi)
                error = objetivo - prediccion

                if error != 0:
                    actualizacion = self.eta * error
                    self.w_ += actualizacion * xi
                    self.b_ += actualizacion
                    errores += 1

            self.errors_.append(errores)

        return self

    def net_input(self, X):
        return np.dot(X, self.w_) + self.b_

    def predict(self, X):
        # Si el resultado es positivo o cero, devuelve 1. Si es negativo, 0.
        return np.where(self.net_input(X) >= 0.0, 1, 0)
    

# ENTRENAMIENTO Y RESULTADOS

# Creamos la neurona
mi_neurona = PerceptronSimple(aprendizaje=0.1, epocas=10)

# Le enseñamos con los datos de entrenamiento
print(f"{lima}\nEntrenando la neurona...{reset}")
mi_neurona.fit(X_train, y_train)

# 4. REPRESENTACIÓN GRÁFICA (Criterio obligatorio de la rúbrica)
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(mi_neurona.errors_) + 1), mi_neurona.errors_, marker='o', color='#38d62e', linewidth=2)
plt.xlabel('Épocas')
plt.ylabel('Número de errores (Actualizaciones)')
plt.title('Proceso de Entrenamiento: Evolución del Error por Época')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('grafica_entrenamiento.png') # Guarda la imagen para la memoria
print(f"{lima}Gráfica generada y guardada como 'grafica_entrenamiento.png'{reset}")

# Probamos la neurona con los datos que nunca ha visto (Test)
predicciones_finales = mi_neurona.predict(X_test)

# Calculamos cuántas veces acertó
aciertos = np.sum(predicciones_finales == y_test)
precision = (aciertos / len(y_test)) * 100

print(f"{azul}\n                      RESULTADOS{reset}")
print(f"{azul}======================================================{reset}")
print()
print(f"{turquesa}La neurona ha acertado el {reset}{magenta}{precision:.2f}% {reset}{turquesa}de los casos.{reset}")
print(f"{turquesa}Pesos finales (importancia):{reset}{magenta} {mi_neurona.w_}{reset}")
print(f"{turquesa}Sesgo final (bias): {reset}{magenta}{mi_neurona.b_}{reset}")

