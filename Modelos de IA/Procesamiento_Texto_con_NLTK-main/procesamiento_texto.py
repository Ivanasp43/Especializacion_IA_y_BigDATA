
# Actividad 3.1 - Procesamiento del Texto
# Autor: Ivana Sánchez Pérez
# Librerías utilizadas: NLTK + Langdetect


import nltk
import string
import re
import os
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer
from langdetect import detect

# colores
rojo = '\033[91m'
verde = '\033[92m'
azul = '\033[94m'
magenta = '\033[95m'
amarillo = '\033[93m'
rosa = '\033[38;5;200m'
turquesa = '\033[38;5;44m'
azul_marino = '\33[38;5;67m'
lima = '\33[38;5;46m'
reset = '\033[0m'

# DESCARGAS NECESARIAS
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# CARGA AUTOMÁTICA DEL ARCHIVO .txt
archivo_txt = None
for archivo in os.listdir():
    if archivo.endswith(".txt"):
        archivo_txt = archivo
        break

if archivo_txt is None:
    raise FileNotFoundError(f"\n{rojo}No se encontró ningún archivo .txt en la carpeta.{reset}")

with open(archivo_txt, "r", encoding="utf-8") as f:
    texto_original = f.read()

print(f"\n\n{lima}        ARCHIVO{reset}{magenta} {archivo_txt} {reset}{lima}CARGADO{reset}")

# DETECCIÓN DE IDIOMA
idioma_detectado = detect(texto_original)

# REGISTRO DE MAYÚSCULAS (ANTES DE LIMPIAR)
tokens_originales = word_tokenize(texto_original)
palabras_mayusculas = [w for w in tokens_originales if w.isupper()]
conteo_mayusculas = len(palabras_mayusculas)
top_3_mayusculas = Counter(palabras_mayusculas).most_common(3)

# NORMALIZACIÓN
texto = texto_original.lower()
tokens = word_tokenize(texto)

# SIGNOS DE PUNTUACIÓN
signos_puntuacion = [c for c in texto_original if c in string.punctuation]
conteo_puntuacion = len(signos_puntuacion)
conteo_exclamaciones = texto_original.count("!")

# NÚMEROS
numeros = [int(t) for t in tokens if t.isdigit()]
conteo_numeros = len(numeros)
numero_mas_grande = max(numeros) if numeros else None

# LIMPIEZA Y STOPWORDS
tokens_alpha = [t for t in tokens if t.isalpha()]

stop_words = set(stopwords.words('spanish'))
stopwords_encontradas = [t for t in tokens_alpha if t in stop_words]
conteo_stopwords = len(stopwords_encontradas)
top_3_stopwords = Counter(stopwords_encontradas).most_common(3)

tokens_limpios = [t for t in tokens_alpha if t not in stop_words]

# CONTEO DE PALABRAS
total_palabras = len(tokens)
total_palabras_limpias = len(tokens_limpios)

# 20 PALABRAS MÁS FRECUENTES
top_20_palabras = Counter(tokens_limpios).most_common(20)

# STEMMING (RAÍCES)
stemmer = SnowballStemmer("spanish")
stems = [stemmer.stem(t) for t in tokens_limpios]
top_5_stems = Counter(stems).most_common(5)

# VERBOS (APROXIMACIÓN POR TERMINACIONES)
terminaciones_verbos = (
    "ar", "er", "ir",
    "ado", "ido",
    "aba", "ía",
    "aste", "iste",
    "aron", "ieron",
    "ando", "iendo"
)

verbos_aprox = [w for w in tokens_limpios if w.endswith(terminaciones_verbos)]
top_5_verbos = Counter(verbos_aprox).most_common(5)

# ADJETIVOS (APROXIMACIÓN POR TERMINACIONES)
terminaciones_adj = (
    "oso", "osa",
    "ivo", "iva",
    "al", "able",
    "ible", "ente"
)

adjetivos_aprox = [w for w in tokens_limpios if w.endswith(terminaciones_adj)]
top_5_adjetivos = Counter(adjetivos_aprox).most_common(5)

# N-GRAMAS
bigramas = list(ngrams(tokens_limpios, 2))
trigramas = list(ngrams(tokens_limpios, 3))

top_5_bigramas = Counter(bigramas).most_common(5)
top_5_trigramas = Counter(trigramas).most_common(5)

# TOKENIZACIÓN DE FRASES (2 MÉTODOS)
frases_nltk = sent_tokenize(texto_original)
num_frases_nltk = len(frases_nltk)

frases_manual = re.split(r'[.!?]+', texto_original)
num_frases_manual = len([f for f in frases_manual if f.strip() != ""])

# POSIBLES PERSONAJES (POR MAYÚSCULAS)
posibles_personajes = Counter(palabras_mayusculas).most_common(10)

# ESTIMACIÓN DE PÁGINAS
paginas_estimadas = round(total_palabras / 275, 2)

# RESULTADOS

print(f"{azul}\n================ RESULTADOS ================\n{reset}")

print(f"{turquesa}Idioma detectado:{reset}{amarillo}{idioma_detectado}{reset}")

print(f"{turquesa}Total palabras:{reset} {amarillo}{total_palabras}{reset}")
print(f"{turquesa}Total palabras limpias:{reset} {amarillo}{total_palabras_limpias}{reset}")

print(f"\n{azul}Stopwords:{reset}")
print(f"{turquesa}Total:{reset} {amarillo}{conteo_stopwords}{reset}")
print(f"{turquesa}Top 3:{reset} {amarillo}{top_3_stopwords}{reset}")

print(f"\n{turquesa}Mayúsculas eliminadas:{reset} {amarillo}{conteo_mayusculas}{reset}")
print(f"{turquesa}Top 3 mayúsculas:{reset} {amarillo}{top_3_mayusculas}{reset}")

print(f"{turquesa}\nSignos de puntuación:{reset} {amarillo}{conteo_puntuacion}{reset}")
print(f"{turquesa}Signos de exclamación:{reset} {amarillo}{conteo_exclamaciones}){reset}")

print(f"{turquesa}\nNúmeros encontrados:{reset} {amarillo}{conteo_numeros}{reset}")
print(f"{turquesa}Número más grande:{reset} {amarillo}{numero_mas_grande}{reset}")

print(f"\n{turquesa}Top 20 palabras más frecuentes:{reset}")
print(f"{amarillo}{top_20_palabras}{reset}")

print(f"{turquesa}\nTop 5 raíces más frecuentes:{reset}")
print(f"{amarillo}{top_5_stems}{reset}")

print(f"\n{turquesa}Top 5 verbos (aprox):{reset}")
print(f"{amarillo}{top_5_verbos}{reset}")

print(f"\n{turquesa}Top 5 adjetivos (aprox):{reset}")
print(f"{amarillo}{top_5_adjetivos}{reset}")

print(f"{turquesa}\nTop 5 bigramas:{reset}")
print(f"{amarillo}{top_5_bigramas}{reset}")

print(f"\n{turquesa}Top 5 trigramas:{reset}")
print(f"{amarillo}{top_5_trigramas}{reset}")

print(f"\n{turquesa}Número de frases (NLTK):{reset} {amarillo}{num_frases_nltk}{reset}")
print(f"{turquesa}Número de frases (Manual):{reset} {amarillo}{num_frases_manual}{reset}")

print(f"\n{turquesa}Posibles personajes detectados:{reset}")
print(f"{amarillo}{posibles_personajes}{reset}")

print(f"\n{turquesa}Páginas estimadas:{reset} {amarillo}{paginas_estimadas}{reset}\n")

# ==============================
# GENERACIÓN AUTOMÁTICA DE PDF
# ==============================

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

# Crear documento
pdf = SimpleDocTemplate(
    "Resultados_obtenidos.pdf",
    pagesize=A4
)

elementos = []

styles = getSampleStyleSheet()

# Estilo personalizado
titulo_style = styles["Heading1"]
normal_style = styles["Normal"]

elementos.append(Paragraph("Actividad 3.1 - Análisis NLP", titulo_style))
elementos.append(Spacer(1, 0.3 * inch))

# Función auxiliar para añadir secciones
def añadir_seccion(titulo, contenido):
    elementos.append(Paragraph(f"<b>{titulo}</b>", styles["Heading2"]))
    elementos.append(Spacer(1, 0.2 * inch))
    
    if isinstance(contenido, list):
        lista = [ListItem(Paragraph(str(item), normal_style)) for item in contenido]
        elementos.append(ListFlowable(lista, bulletType='bullet'))
    else:
        elementos.append(Paragraph(str(contenido), normal_style))
    
    elementos.append(Spacer(1, 0.3 * inch))

# Añadir contenido
añadir_seccion("Idioma detectado", idioma_detectado)
añadir_seccion("Total palabras", total_palabras)
añadir_seccion("Total palabras limpias", total_palabras_limpias)

añadir_seccion("Stopwords (Top 3)", top_3_stopwords)
añadir_seccion("Mayúsculas (Top 3)", top_3_mayusculas)

añadir_seccion("Signos de puntuación", conteo_puntuacion)
añadir_seccion("Signos de exclamación", conteo_exclamaciones)

añadir_seccion("Números encontrados", conteo_numeros)
añadir_seccion("Número más grande", numero_mas_grande)

añadir_seccion("Top 20 palabras frecuentes", top_20_palabras)
añadir_seccion("Top 5 raíces", top_5_stems)

añadir_seccion("Top 5 verbos", top_5_verbos)
añadir_seccion("Top 5 adjetivos", top_5_adjetivos)

añadir_seccion("Top 5 bigramas", top_5_bigramas)
añadir_seccion("Top 5 trigramas", top_5_trigramas)

añadir_seccion("Número de frases (NLTK)", num_frases_nltk)
añadir_seccion("Número de frases (Manual)", num_frases_manual)

añadir_seccion("Posibles personajes", posibles_personajes)
añadir_seccion("Páginas estimadas", paginas_estimadas)

# Construir PDF
pdf.build(elementos)

print(f"{lima}\n          PDF 'Resultados_obtenidos.pdf' generado correctamente\n{reset}")



