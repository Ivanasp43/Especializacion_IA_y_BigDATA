# Título: Conexión Bluesky + Análisis de Gemini
# Autor: Ivana Sánchez Pérez

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

import os
import sys
from atproto import Client
from google import genai


# Variables de Entorno (Bluesky)
BSKY_IDENTIFIER = os.environ.get('BSKY_IDENTIFIER')
BSKY_PASSWORD = os.environ.get('BSKY_PASSWORD')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 


# Cliente Bluesky 
if not BSKY_IDENTIFIER or not BSKY_PASSWORD:
    print(f"{rojo} ¡¡ERROR!! Las variables BSKY_IDENTIFIER o BSKY_PASSWORD no están configuradas.{reset}")
    sys.exit(1)

print("Conectando a Bluesky...")
client_bsky = Client()
try:
    client_bsky.login(BSKY_IDENTIFIER, BSKY_PASSWORD)
    print(f"\n\n{lima}Conexión a Bluesky exitosa.{reset}")
except Exception as e:
    print(f"{rojo} Error al iniciar sesión en Bluesky: {e}{reset}")
    sys.exit(1)

# Cliente Gemini
if not GEMINI_API_KEY:
    print(f"{rojo}¡¡ERROR!! La variable GEMINI_API_KEY no está configurada (usa 'set GEMINI_API_KEY=...' en la terminal).{reset}")
    sys.exit(1)
    
try:
    client_gemini = genai.Client(api_key=GEMINI_API_KEY)
    print(f"\n{rosa}Cliente Gemini inicializado correctamente.{reset}")
except Exception as e:
    print(f"{rojo}Error al inicializar el cliente Gemini: {e}{reset}")
    sys.exit(1)


# EXTRACCIÓN DE DATOS DE BLUESKY


CUENTA_OBJETIVO = "bsky.app" 

def obtener_datos_perfil(cliente, actor_handle):

    print(f"\n{turquesa}Extrayendo datos de la cuenta: @{actor_handle}{reset}...")
    
    # Obtener la Biografía 
    try:
        profile = cliente.get_profile(actor=actor_handle)
        bio = profile.description if hasattr(profile, 'description') else "No se encontró biografía."
    except Exception:
        bio = "No se pudo obtener la biografía."

    # Obtener el Feed (posts recientes)
    posts_textos = []
    try:
        feed_response = cliente.get_author_feed(actor=actor_handle, limit=25) 
        posts_textos = [
            item.post.record.text.strip().replace('\n', ' ') 
            for item in feed_response.feed
        ]
        print(f"{azul_marino}Se obtuvieron {len(posts_textos)} posts del feed.{reset}")
    except Exception:
        print(f"{rojo}Error al obtener el feed del autor.{reset}")
        
    return bio, posts_textos

def obtener_posts_gustados(cliente, actor_handle):
    # Simulamos la obtención de posts gustados con un marcador para el análisis de Gemini.

    print(f"\n{turquesa}Obteniendo posts a los que el perfil ha dado 'like'...{reset}")

    posts_gustados = [
        "Post 1: Me encanta cómo la tecnología conecta a las personas de forma creativa.",
        "Post 2: El diseño de interfaces debe centrarse en la accesibilidad y la empatía.",
        "Post 3: Iniciativa increíble sobre sostenibilidad en el desarrollo digital.",
        "Post 4: Gran artículo sobre ética en la inteligencia artificial."
    ]

    print(f"{azul_marino}Se incluyeron {len(posts_gustados)} posts gustados para el análisis.{reset}")
    return posts_gustados

# PREPARAR LOS DATOS PARA EL ANÁLISIS DE GEMINI

bio_perfil, posts_feed = obtener_datos_perfil(client_bsky, CUENTA_OBJETIVO)
posts_gustados = obtener_posts_gustados(client_bsky, CUENTA_OBJETIVO)

# Formatear el feed para el prompt
feed_formato = "\n".join([f"Post {i+1}: {text}" for i, text in enumerate(posts_feed)])

# Crear el Prompt Completo
contexto_previo = (
    "Eres un analista de redes sociales experto. Tu tarea es analizar el contenido del perfil "
    f"de Bluesky @{CUENTA_OBJETIVO}. Debes resumir el tema principal, el tono y las intenciones "
    "de la cuenta basándote en la biografía, sus publicaciones recientes y los intereses indicados."
)
datos_analisis = (
    "\n\n--- DATOS DE ANÁLISIS ---"
    f"\nBiografía del perfil: \"{bio_perfil}\""
    "\n\n--- PUBLICACIONES RECIENTES DEL AUTOR ---"
    f"\n{feed_formato}"
    "\n\n--- POSTS A LOS QUE HA DADO LIKE ---"
    f"\n{posts_gustados[0]}" 
)
formato_respuesta = (
    "\n\n--- FORMATO DE RESPUESTA REQUERIDO ---"
    "\nProporciona el análisis en formato de Markdown con las siguientes secciones obligatorias:\n"
    "## 1. Tema Principal y Enfoque del Perfil\n"
    "## 2. Tono y Estilo de Comunicación\n"
    "## 3. Resumen del Contenido: Los 3 puntos clave\n"
    "## 4. Análisis de Intereses (Comentarios sobre los 'Likes' o la Bio)"
)

prompt = contexto_previo + datos_analisis + formato_respuesta

# Llamar a Gemini y Mostrar/Guardar la Respuesta
print(f"\n{amarillo}Enviando datos a Gemini para análisis (Modelo: gemini-2.5-flash)...{reset}")

try:
    response = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    analisis_texto = response.text

    print()
    print()
    print(f"{azul}########################################################{reset}")
    print(f"{azul}                  ANÁLISIS DE GEMINI {reset}")
    print(f"{azul}########################################################{reset}")
    print()
    print(analisis_texto)

    # Guardar el análisis en un archivo .md
    nombre_archivo_salida = "analisis_gemini.md"
    with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
        f.write("# ANÁLISIS GENERADO POR GEMINI\n\n")
        f.write(analisis_texto)
    
    print("\n" + "_"*85)
    print(f"\n{verde}¡ANÁLISIS GUARDADO CON ÉXITO! Revisa en tu escritorio el archivo {nombre_archivo_salida}.{reset}")
    print()
    
except Exception as e:
    print(f"{rojo}ERROR en la llamada a la API de Gemini: {e}{reset}")
    print(f"{lima}Asegúrate de que tu GEMINI_API_KEY es válida.{reset}")