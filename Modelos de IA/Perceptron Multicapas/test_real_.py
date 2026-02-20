"""
Programa para reconocer dígitos escritos a mano usando un modelo entrenado con MNIST.
Carga un modelo preentrenado, procesa una imagen de entrada y predice el dígito.
"""
import os
import cv2
import joblib
import numpy as np
import matplotlib.pyplot as plt

rojo = '\033[91m'
lima = '\33[38;5;46m'
reset = '\033[0m'

# Detectar carpeta actual de forma automática
carpeta = os.path.dirname(os.path.abspath(__file__))

# Rutas dinámicas
path_modelo = os.path.join(carpeta, 'modelo_ocr_mnist.pkl')
path_imagen = os.path.join(carpeta, 'mi_numero.png')

# Cargar modelo 
if os.path.exists(path_modelo):
    modelo = joblib.load(path_modelo)
    
    # Leer imagen en escalas de grises 
    img = cv2.imread(path_imagen, cv2.IMREAD_GRAYSCALE) # Convierte la imagen a blanco y negro
    if img is not None:
        img_resized = cv2.resize(img, (28, 28))
        img_ready = img_resized.reshape(1, 784) / 255.0 # Redimensionamos la imagen a un vector de 784 elementos y normaliza los valores de píxeles
        
        # Predicción 
        pred = modelo.predict(img_ready)
        print(f"{lima}\nLA RED PREDICE EL NÚMERO:{reset} {pred[0]}")
        
        plt.imshow(img_resized, cmap='gray')
        plt.title(f"Resultado: {pred[0]}")
        plt.show()
    else:
        print(f"\n{rojo}No se encuentra la imagen en:{reset} {path_imagen}")
else:
    print(f"\n{rojo}No se encuentra el modelo en:{reset} {path_modelo}")