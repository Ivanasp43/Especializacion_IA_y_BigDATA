# ACTIVIDAD 3.2: ANÁLISIS SINTÁCTICO Y SEMÁNTICO
# Análisis de Voz del Cliente - PlayStation 5
# Autor: Ivana Sánchez Pérez

# colores
rojo = '\033[91m'
verde = '\033[92m'
azul = '\033[94m'
magenta = '\033[95m'
amarillo = '\033[93m'
turquesa = '\033[38;5;44m'
lima = '\33[38;5;46m'
reset = '\033[0m'

import spacy
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from transformers import pipeline
from spacy.tokens import Doc
from spacy.language import Language
from spacy import displacy
from pathlib import Path


# PREPARACIÓN DEL ENTORNO NPL

print(f"{lima}\nCargando modelo spaCy...{reset}")
# Cargamos el modelo grande de español que incluye vectores de palabras para mayor precisión
nlp = spacy.load("es_core_news_lg")

# Mostrar arquitectura del pipeline
print(f"\n{lima}Componentes del pipeline:{reset},{amarillo} {nlp.pipe_names}{reset}")

print(f"\n{lima}Cargando modelo de sentimiento (Transformers)...{reset}\n\n")
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="finiteautomata/beto-sentiment-analysis"
)

# Crear extensión personalizada
# Registramos una extensión en el objeto Doc para almacenar el resultado del análisis de sentimiento
if not Doc.has_extension("sentiment"):
    Doc.set_extension("sentiment", default=None)

# Definimos un componente personalizado para integrar Transformers dentro del flujo de spaCy
@Language.component("analizador_sentimiento")
def analizar_sentimiento(doc):
    resultado = sentiment_pipeline(doc.text[:512])[0]
    doc._.sentiment = resultado
    return doc

# Añadimos el componente al final de la tubería de procesamiento
nlp.add_pipe("analizador_sentimiento", last=True)


# CARGA DE Y PROCESAMIENTO DE DATOS
with open("PlayStation5.txt", "r", encoding="utf-8") as f:
    texto_completo = f.read()

# Procesamos el texto completo para el análisis morfosintáctico global
# El objeto 'doc_global' es un Doc
# Cada palabra es un Token
# Cada oración es un Span
doc_global = nlp(texto_completo)

# ANÁLISIS MORFOSINTÁCTICO
print(f"{lima}\nGenerando imagen del árbol sintáctico...{reset}")

# Visualización Árbol Sintáctico 
# 1 Forma- Descarga directa generando un archivo SVG

# Listado de oraciones detectadas mediante segmentación automática
print(f"\n\n{magenta}ORACIONES DETECTADAS: {reset}\n")
for i, sent in enumerate(doc_global.sents):
    print(f"{turquesa}{i}: {sent.text}{reset}")

# Seleccionamos una oración representativa para el análisis profundo
oracion_ejemplo = list(doc_global.sents)[2]

# Análisis de etiquetas gramaticales (POS - Part of Speech) y dependencias (DEP)
print(f"{magenta}ETIQUETAS GRAMATICALES (POS y DEP):\n{reset}")

# Identificación del núcleo de la oración (ROOT)
for token in oracion_ejemplo:
    print(f"{turquesa}{token.text:15} → {token.pos_} ({token.dep_}){reset}")

for token in oracion_ejemplo:
    if token.dep_ == "ROOT":
        print(f"{magenta}\nVERBO PRINCIPAL (ROOT):{reset}, {amarillo}{token.text}{reset}")

for token in oracion_ejemplo:
    if token.dep_ == "aux":
        print(f"{magenta}AUXILIAR:{reset}, {amarillo}{token.text}{reset}")


# Generación del gráfico de árbol sintáctico en formato SVG (escalable)
svg_tree = displacy.render(oracion_ejemplo, style="dep", jupyter=False)

# Lo guardamos en un archivo
output_path = Path("arbol_sintactico.svg")
output_path.open("w", encoding="utf-8").write(svg_tree)

print(f"\n{azul}Árbol sintáctico guardado como:{reset}{amarillo} arbol_sintactico.svg{reset}")

# 2 Forma - Abriendo el navegador --> http://127.0.0.1:5000
# Para la captura del informe, comentar toda la primera opción y descomentar la dos línea siguientes. Ejecutar el script.
# oracion_ejemplo = list(doc_global.sents)[2]
# displacy.serve(oracion_ejemplo, style="dep")
# Abre el navegador y Ctrl+c para que termine la ejecución del script en el terminal

# EXTRACCIÓN DE ENTIDADES

print(f"\n{magenta}ENTIDADES NOMBRADAS DETECTADAS:{reset}\n")
for ent in doc_global.ents:
    print(f"{turquesa}{ent.text} → {ent.label_}{reset}")


# ANÁLISIS DE SENTIMIENTO

lineas = [l.strip() for l in texto_completo.split("\n") if l.strip()]
dataset = []

# Usamos nlp.pipe para procesar la lista de forma eficiente (multithreading interno)
for doc_com in nlp.pipe(lineas):
    
    etiqueta_modelo = doc_com._.sentiment["label"]
    
    # Normalización de etiquetas para el informe final
    if etiqueta_modelo == "POS":
        etiqueta_final = "POSITIVO"
    elif etiqueta_modelo == "NEG":
        etiqueta_final = "NEGATIVO"
    else:
        etiqueta_final = "NEUTRO"
    
    dataset.append({
        "Comentario": doc_com.text,
        "Sentimiento": etiqueta_final,
        "Confianza": round(doc_com._.sentiment["score"], 4)
    })

df = pd.DataFrame(dataset)
df.to_csv("resultado_analisis_ps5.csv", index=False, encoding="utf-8-sig")


# VISUALIZACIONES ESTADÍSTICAS

# Gráfico de Seentimientos
# Forzamos el orden que queremos. Orden fijo.
orden = ["POSITIVO", "NEUTRO", "NEGATIVO"]

resumen_sent = (
    df["Sentimiento"]
    .value_counts()
    .reindex(orden, fill_value=0)
)

plt.figure(figsize=(8, 5))
plt.bar(resumen_sent.index, resumen_sent.values,
        color=["green", "purple", "red"])

plt.title("Percepción General del Cliente - PS5", fontsize=14)
plt.ylabel("Cantidad de Reseñas")
plt.xlabel("Sentimiento")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("grafico_sentimientos_ps5.png")
plt.close()

# Gráfico de Tópicos (Sustantivos más frecuentes)
# Filtramos palabras vacías y términos genéricos 
sustantivos = [t.lemma_.lower() for t in doc_global if t.pos_ == "NOUN" and not t.is_stop and len(t.text) > 3]
top_conceptos = Counter(sustantivos).most_common(10)
df_top = pd.DataFrame(top_conceptos, columns=["Concepto", "Frecuencia"])

plt.figure(figsize=(10, 6))
plt.bar(df_top["Concepto"], df_top["Frecuencia"], color='mediumpurple')
plt.title("Principales Temas de Conversación", fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top10_conceptos_ps5.png") 
plt.close()


print(f"\n{azul}Archivos generados: {reset}{amarillo} 'resultado_analisis_ps5.csv', 'grafico_sentimientos_ps5.png', 'arbol_sintactico.svg' y 'top10_conceptos_ps5.png'.{reset}")
print(f"\n\n             {lima}¡¡Proceso completado con éxito!!{reset}\n")

  
# RESUMEN FINAL

print(f"{azul}{"\n" + "="*40}{reset}")
print(f"\n{turquesa}          RESUMEN EJECUTIVO{reset}")
print(f"{azul}{"\n" + "="*40}{reset}")
print(f"{magenta}\n     Total comentarios: {len(df)}")
print(f"     Sentimiento predominante: {df['Sentimiento'].mode()[0]}")
print(f"     Confianza media: {df['Confianza'].mean():.2%}{reset}")
print(f"{azul}{"\n" + "="*40}{reset}")