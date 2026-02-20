# Título: Algoritmos de búsqueda en rutas urbanas en Sevilla
# Autor: Ivana Sánchez Pérez

import time
import heapq
from collections import deque
from math import inf
from grafo import ruta_euclidea as GRAFO, coordenadas as COORDENADAS 

import matplotlib.pyplot as plt
import io
import base64
import networkx as nx 

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


# Clase Nodo (estructura común para todos los algoritmos). Representa un nodo en el espacio de búsqueda
class Nodo:
    def __init__(self, nombre, padre=None, coste=0, heuristica=0):
        self.nombre = nombre 
        self.padre = padre   
        self.coste = coste   
        self.heuristica = heuristica 

    def __lt__(self, otro):
        """Define la comparación para la cola de prioridad (heapq). Prioriza el menor coste total estimado f(n) = g(n) + h(n)."""
        return (self.coste + self.heuristica) < (otro.coste + otro.heuristica)

# Función para reconstruir el camino desde el nodo final. Reconstruye la secuencia de nodos desde el objetivo hasta el inicio

def reconstruir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.nombre)
        nodo = nodo.padre
    return list(reversed(camino))

# Búsqueda en anchura (BFS), Encuentra el camino más corto en números de pasos --> PROFUNDIDAD
def busqueda_bfs(grafo, inicio, objetivo):
    frontera = deque([Nodo(inicio)]) 
    visitados = {inicio} 
    nodos_explorados = 0

    while frontera:
        actual = frontera.popleft()
        nodos_explorados += 1

        if actual.nombre == objetivo:
            return reconstruir_camino(actual), nodos_explorados
        
        for vecino in grafo.get(actual.nombre, {}):
            if vecino not in visitados:
                visitados.add(vecino)
                coste_arista = grafo[actual.nombre][vecino]
                nuevo_coste = actual.coste + coste_arista
                frontera.append(Nodo(vecino, actual, nuevo_coste))
    
    return None, nodos_explorados

# Búsqueda en profundidad (DFS). Explora primero la rama más profunda

def busqueda_dfs(grafo, inicio, objetivo):
    
    frontera = [Nodo(inicio)] 
    visitados = set()
    nodos_explorados = 0

    while frontera:
        actual = frontera.pop()
        nodos_explorados += 1

        if actual.nombre == objetivo:
            return reconstruir_camino(actual), nodos_explorados
        
        if actual.nombre in visitados:
            continue
            
        visitados.add(actual.nombre)

        for vecino in reversed(list(grafo.get(actual.nombre, {}).keys())):
            if vecino not in visitados:
                coste_arista = grafo[actual.nombre][vecino]
                nuevo_coste = actual.coste + coste_arista
                frontera.append(Nodo(vecino, actual, nuevo_coste))
    
    return None, nodos_explorados

# Búsqueda de coste uniforme (UCS). Encuentra el camino de menor coste acumulado g(n) 

def busqueda_ucs(grafo, inicio, objetivo):
    
    frontera = [(0, Nodo(inicio))] 
    visitados = {inicio: 0}
    nodos_explorados = 0

    while frontera:
        coste, actual = heapq.heappop(frontera)
        nodos_explorados += 1
        
        if actual.nombre == objetivo:
            return reconstruir_camino(actual), coste, nodos_explorados

        if actual.nombre in visitados and coste > visitados[actual.nombre]:
            continue
        
        for vecino, c in grafo.get(actual.nombre, {}).items():
            nuevo_coste = coste + c
            
            if vecino not in visitados or nuevo_coste < visitados.get(vecino, inf):
                visitados[vecino] = nuevo_coste
                heapq.heappush(frontera, (nuevo_coste, Nodo(vecino, actual, nuevo_coste, heuristica=0)))
    
    return None, inf, nodos_explorados

# Búsqueda voraz (Greedy Best-First). Encuentra un camino siguiendo la mejor heurística h(n)
def busqueda_greedy(grafo, inicio, objetivo, heuristica):
    
    h_inicio = heuristica.get(inicio, 0)
    frontera = [(h_inicio, Nodo(inicio, heuristica=h_inicio))]
    visitados = set() 
    nodos_explorados = 0

    while frontera:
        _, actual = heapq.heappop(frontera)
        nodos_explorados += 1

        if actual.nombre == objetivo:
            return reconstruir_camino(actual), actual.coste, nodos_explorados
        
        if actual.nombre in visitados:
            continue
            
        visitados.add(actual.nombre)

        for vecino, c in grafo.get(actual.nombre, {}).items():
            nuevo_coste = actual.coste + c
            h_vecino = heuristica.get(vecino, 0)
            
            if vecino not in visitados:
                heapq.heappush(frontera, (h_vecino, Nodo(vecino, actual, nuevo_coste, h_vecino)))
            
    return None, inf, nodos_explorados

# Búsqueda A*. Encuentra el camino de menor coste f(n) = g(n) + h(n)

def busqueda_a_estrella(grafo, inicio, objetivo, heuristica):

    h_inicio = heuristica.get(inicio, 0)
    frontera = [(0 + h_inicio, Nodo(inicio, heuristica=h_inicio))]
    visitados = {inicio: 0}
    nodos_explorados = 0

    while frontera:
        f_coste, actual = heapq.heappop(frontera)
        nodos_explorados += 1

        if actual.nombre == objetivo:
            return reconstruir_camino(actual), actual.coste, nodos_explorados
        
        if actual.nombre in visitados and actual.coste > visitados.get(actual.nombre, inf):
            continue

        for vecino, c in grafo.get(actual.nombre, {}).items():
            nuevo_coste_g = actual.coste + c
            h_vecino = heuristica.get(vecino, 0)
            nuevo_coste_f = nuevo_coste_g + h_vecino
            
            if nuevo_coste_g < visitados.get(vecino, inf):
                visitados[vecino] = nuevo_coste_g
                heapq.heappush(frontera, (nuevo_coste_f, Nodo(vecino, actual, nuevo_coste_g, h_vecino)))

    return None, inf, nodos_explorados

# Heurísticas

def heuristic_zero(grafo, objetivo):
      # Heurística nula h(n) = 0.
    return {n: 0 for n in grafo}

def heuristic_direct_path_cost(grafo, objetivo):
    """Heurística basada en el coste de arista directa al objetivo (si existe)."""
    h = {}
    for n in grafo:
        h[n] = grafo.get(n, {}).get(objetivo, 0)
    return h

# Función  para calcular el coste total de un camino
def calcular_coste(grafo, camino):

    if not camino or len(camino) < 2:
        return 0
    coste = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i+1]
        coste += grafo.get(origen, {}).get(destino, 0) 
    return coste

# Visualización de los resultados

def mostrar_tabla(resultados, titulo):

    print(f"\n{azul}{'#'*110}{reset}")
    print(f"{turquesa}{titulo:^110}{reset}")
    print(f"{azul}{'#'*110}{reset}")
    print()
    print(f"{'Algoritmo':<20}{'Camino encontrado':<60}{'Coste total':<15}{'Nodos expl.':<10}{'Tiempo(ms)':<10}")
    print(f"{'-'*110}")
    for r in resultados:
        alg, camino, coste, explorados, tiempo = r
        
        if camino is None:
             coste_str = "inf" if coste == inf else f"{coste:.2f}"
             camino_str = "No encontrado"
        else:
             coste_str = f"{coste:.2f}"
             camino_str = '->'.join(camino)
        
        if len(camino_str) > 58:
            camino_str = camino_str[:55] + '...'
            
        print(f"{rosa}{alg:<20}{reset}{camino_str:<60}{lima}{coste_str:<15}{reset}{magenta}{explorados:<10}{reset}{tiempo:<10.2f}")


# Funciones de Gráficos 
 # Genera un gráfico de barras comparando la métrica por algoritmo
def generar_grafico(data, metric, title, filename):
   
    algoritmos = [d['Algoritmo'] for d in data] 
    valores = [d[metric] for d in data]
    
    colores = ['#9467bd', '#d62728', '#2ca02c', '#ff7f0e', '#1f77b4'] 
    
    plt.figure(figsize=(10, 5))
    barras = plt.bar(algoritmos, valores, color=colores)
    
    plt.title(title, fontsize=14)
    plt.xlabel('Algoritmo de Búsqueda', fontsize=12)
    plt.ylabel(metric.replace('_', ' ').title(), fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    
    for bar in barras:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.0f}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_base64

# Genera un gráfico de árbol jerárquico
def generar_arbol_busqueda_visualizacion(grafo, inicio):
    
    arbol_layout = {
        'IES Punta del Verde': (5, 0), 
        
        'Estadio Benito Villamarín': (3, -2),
        'Pabellón de México': (7, -2),
        
        'Hospital Virgen del Rocío': (3, -4),
        'Plaza de España': (5, -4),
        'Palacio de San Telmo': (9, -4),
        
        'Avenida de la paz': (3, -6),
        'Sta. Justa': (5, -6),
        'Plaza de Cuba': (8, -6),
        'Puente de Triana': (10, -6),
        
        'Nervión Plaza': (2, -8),
        'Pandora': (4, -8),
        'Parlamento de Andalucía': (6, -8),
        'Parque de los Príncipes': (8, -8),
        'Plaza de Armas': (9, -8),
        'Torre Sevilla': (11, -8),
        
        'Glorieta Olímpica': (4, -10),
        'Puente de la Barqueta': (6, -10),
        'Malandar': (9, -10),
        'Estadio La Cartuja': (11, -10)
    }

    # Definición de las conexiones
    conexiones_arbol = [
        ('IES Punta del Verde', 'Estadio Benito Villamarín'),
        ('IES Punta del Verde', 'Pabellón de México'),
        ('Estadio Benito Villamarín', 'Hospital Virgen del Rocío'),
        ('Hospital Virgen del Rocío', 'Avenida de la paz'),
        ('Avenida de la paz', 'Nervión Plaza'),
        
        ('Pabellón de México', 'Plaza de España'),
        ('Pabellón de México', 'Palacio de San Telmo'),
        
        ('Plaza de España', 'Sta. Justa'),
        ('Sta. Justa', 'Pandora'),
        ('Sta. Justa', 'Parlamento de Andalucía'),
        
        ('Pandora', 'Glorieta Olímpica'),
        ('Parlamento de Andalucía', 'Puente de la Barqueta'),
        
        ('Palacio de San Telmo', 'Plaza de Cuba'),
        ('Palacio de San Telmo', 'Puente de Triana'), 
        
        ('Plaza de Cuba', 'Parque de los Príncipes'),
        
        ('Puente de Triana', 'Plaza de Armas'),
        ('Puente de Triana', 'Torre Sevilla'),
        
        ('Plaza de Armas', 'Malandar'),
        ('Torre Sevilla', 'Estadio La Cartuja')
    ]
    
    # Construcción del grafo
    G = nx.DiGraph()
    G.add_edges_from(conexiones_arbol)
    
    plt.figure(figsize=(15, 12)) 

    # Dibujo de los nodos
    nx.draw_networkx_nodes(G, arbol_layout, node_size=2500, node_color='#90EE90', # Verde claro
                           edgecolors='black', linewidths=1.5, alpha=1.0)
    
    # Dibujo de las aristas
    nx.draw_networkx_edges(G, arbol_layout, edgelist=G.edges(), edge_color='k', 
                           width=1.0, alpha=0.8)

    # Etiquetas
    nx.draw_networkx_labels(G, arbol_layout, font_size=10, font_weight='bold')
    
    plt.title(f"Árbol generado desde '{inicio}'", fontsize=16)
    plt.axis('off') 
    plt.tight_layout()
    
    # Guardar en Base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_base64

# Gráfico del mapa del grafo resaltando la ruta óptima
def generar_mapa_ruta(grafo, coordenadas, camino_optimo, inicio, objetivo):
    
    plt.figure(figsize=(10, 12)) 
    
    # Aristas
    for origen, conexiones in grafo.items():
        if origen in coordenadas:
            x1, y1 = coordenadas[origen]
            for destino, _ in conexiones.items():
                if destino in coordenadas:
                    x2, y2 = coordenadas[destino]
                    plt.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, zorder=1) 
    
    # nodos
    nombres_nodos = list(coordenadas.keys())
    x_coords = [coordenadas[n][0] for n in nombres_nodos]
    y_coords = [coordenadas[n][1] for n in nombres_nodos]
    
    plt.scatter(x_coords, y_coords, c="#6579DC", s=300, alpha=0.9, zorder=2, edgecolor='k') 

    # Resaltar el camino óptimo 
    if camino_optimo:
        ruta_x = [coordenadas[n][0] for n in camino_optimo]
        ruta_y = [coordenadas[n][1] for n in camino_optimo]
        # Color azul oscuro para la ruta óptima, más grueso para destacar
        plt.plot(ruta_x, ruta_y, linewidth=4, color="#26b41f", zorder=3, label='Ruta Óptima') 
    
    # Resaltar inicio y objetivo 
    plt.scatter(coordenadas[inicio][0], coordenadas[inicio][1], 
                c='lime', s=400, marker='o', zorder=4, label=f'Inicio: {inicio}', edgecolor='k') 
    plt.scatter(coordenadas[objetivo][0], coordenadas[objetivo][1], 
                c='red', s=400, marker='X', zorder=4, label=f'Objetivo: {objetivo}', edgecolor='k') 
    
    # Añadir etiquetas de texto
    offset_map = {
        'Hospital Virgen del Rocio': (-60, 5), 
        'Estadio Benito Villamarín': (-50, 5),
        'Avenida de la paz': (-100, -10),    
        'Nervión Plaza': (5, -20),           
        'Sta. Justa': (5, 5),                
        'Plaza de España': (5, 5),           
        'Palacio de San Telmo': (5, 5),
        'Puente de Triana': (5, 5),
        'Plaza de Cuba': (5, 5),
        'Torre Sevilla': (5, 5),
        'Plaza de Armas': (-100, 5),
    }

    for nombre, (x, y) in coordenadas.items():
        offset = offset_map.get(nombre, (5, 5)) 
    
        plt.annotate(nombre, (x, y), textcoords="offset points", 
                     xytext=offset, ha='left', fontsize=9, 
                     bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6, ec="none")) 
    
    plt.title('Ruta Óptima (A* / UCS) en el Grafo de Sevilla', fontsize=16)
    plt.legend(loc='lower right')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Ocultar ejes para un mapa más limpio
    plt.xticks([]) 
    plt.yticks([]) 
    
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_base64


def generar_graficos(resultados1, resultados2, inicio, objetivo):
    
    img_arbol = generar_arbol_busqueda_visualizacion(GRAFO, inicio)
    
    # Preparar datos para los gráficos de barras
    data1 = [{'Algoritmo': d[0], 'Coste_Total': d[2], 'Nodos_Explorados': d[3]} for d in resultados1]
    data2 = [{'Algoritmo': d[0], 'Coste_Total': d[2], 'Nodos_Explorados': d[3]} for d in resultados2]

    # Generar gráficos de barras
    img_coste_h0 = generar_grafico(data1, 'Coste_Total', 'Comparativa de Coste Total (Heurística Cero)', 'coste_h0.png')
    img_nodos_h_approx = generar_grafico(data2, 'Nodos_Explorados', 'Nodos Explorados (Heurística Aproximada)', 'nodos_h_approx.png')
    
    # Encontrar el mejor camino para la visualización del mapa
    camino_optimo = next((r[1] for r in resultados2 if r[0] == 'A*'), None)

    # Generar el mapa de ruta
    img_mapa = generar_mapa_ruta(GRAFO, COORDENADAS, camino_optimo, inicio, objetivo)
    
    # Se devuelve el árbol primero.
    return img_arbol, img_coste_h0, img_nodos_h_approx, img_mapa 

# Guardar informe con los gráficos en .html 

def guardar_informe(resultados1, resultados2, inicio, objetivo):
    
    # Generamos los gráficos en Base64
    img_arbol, img_coste_h0, img_nodos_h_approx, img_mapa = generar_graficos(resultados1, resultados2, inicio, objetivo)
    
    with open("informe_resultados_busqueda.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang='es'>\n")
        f.write("<head>\n")
        f.write("    <meta charset='UTF-8'>\n")
        f.write("    <title>Informe de Comparativa de Algoritmos de Búsqueda</title>\n")
        f.write("    <style>\n")
        f.write("        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }\n")
        f.write("        h1, h2, h3 { color: #333; }\n")
        f.write("        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n")
        f.write("        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }\n")
        f.write("        th { background-color: #4CAF50; color: white; }\n")
        f.write("        tr:nth-child(even) { background-color: #f2f2f2; }\n")
        f.write("        .analysis { background-color: #e6f7ff; padding: 15px; border-radius: 5px; margin-bottom: 30px; border-left: 5px solid #2196F3; }\n")
        f.write("        .graph-container { text-align: center; margin-bottom: 40px; }\n")
        f.write("        img { max-width: 100%; height: auto; border: 1px solid #ccc; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }\n")
        f.write("    </style>\n")
        f.write("</head>\n")
        f.write("<body>\n")
        
        f.write("<h1>Informe de Comparativa de Algoritmos de Búsqueda de Rutas</h1>\n")
        f.write("<h2>Tarea: Ruta del IES Punta del Verde al Estadio La Cartuja</h2>\n")
        f.write("<p>A continuación se presentan los resultados de los cinco algoritmos de búsqueda aplicados al grafo de rutas de Sevilla.</p>\n")

        # Generamos la tabla HTML
        def generate_html_table(results, title):
            html = f"<h2>{title}</h2>\n"
            html += "<table>\n"
            html += "<thead>\n"
            html += "<tr><th>Algoritmo</th><th>Camino encontrado</th><th>Coste total (m)</th><th>Nodos explorados</th><th>Tiempo (ms)</th></tr>\n"
            html += "</thead>\n"
            html += "<tbody>\n"
            for alg, camino, coste, explorados, tiempo in results:
                camino_str = '->'.join(camino) if camino else "No encontrado"
                coste_str = f"{coste:.2f}" if coste != inf else "inf"
                html += f"<tr><td>{alg}</td><td>{camino_str}</td><td>{coste_str}</td><td>{explorados}</td><td>{tiempo:.2f}</td></tr>\n"
            html += "</tbody>\n"
            html += "</table>\n"
            return html
        
        # Gráfico del Árbol de Búsqueda
        f.write("<div class='graph-container'>\n")
        f.write(f"<h3>Árbol de Búsqueda Jerárquico generado desde '{inicio}'</h3>\n")
        f.write(f"<img src='data:image/png;base64,{img_arbol}' alt='Árbol generado con NetworkX en layout jerárquico forzado'>\n")
        f.write("<p>Visualización jerárquica de la estructura del árbol de búsqueda (posibles caminos) desde el nodo inicial.</p>")
        f.write("</div>\n")
        f.write("<hr>\n")

        # Gráfico del mapa de ruta 
        f.write("<div class='graph-container'>\n")
        f.write("<h3>Mapa de la Ruta Óptima (Visualización A* / UCS)</h3>\n")
        f.write(f"<img src='data:image/png;base64,{img_mapa}' alt='Mapa del grafo con la ruta óptima resaltada en azul oscuro'>\n")
        f.write("<p>La ruta óptima (7458.00 m) está resaltada en <strong>azul oscuro</strong>. Los nodos y aristas se dibujan según sus coordenadas relativas.</p>")
        f.write("</div>\n")


        # Tabla 1: Heurística Cero
        f.write(generate_html_table(resultados1, "1. Comparativa con Heurística Nula (h(n) = 0)"))
        
        f.write("<div class='analysis'>\n")
        f.write("<h3>Análisis (h=0):</h3>\n")
        f.write("<ul>\n")
        f.write("<li><strong>UCS</strong> y <strong>A*</strong> (con h=0, que se comporta como UCS) encuentran la ruta <strong>óptima en coste</strong> (7458.00 m).</li>\n")
        f.write("<li><strong>BFS</strong> encuentra la ruta con menos pasos (más corta en profundidad) pero no es la de menor coste.</li>\n")
        f.write("<li><strong>DFS</strong> encuentra una ruta mucho más larga y costosa (16452.00 m), explorando menos nodos debido a su enfoque de profundidad.</li>\n")
        f.write("<li>El algoritmo <strong>Greedy</strong> con heurística nula se comporta de forma similar a UCS.</li>\n")
        f.write("</ul>\n")
        f.write("</div>\n")
        
        # Gráfico 1 (Coste)
        f.write("<div class='graph-container'>\n")
        f.write("<h3>Gráfico: Comparación de Coste Total (Heurística Cero)</h3>\n")
        f.write(f"<img src='data:image/png;base64,{img_coste_h0}' alt='Comparación de Coste Total'>\n")
        f.write("</div>\n")

        # Heurística Aproximada (Direct Path Cost)
        f.write(generate_html_table(resultados2, "2. Comparativa con Heurística Aproximada (Coste de camino directo)"))

        f.write("<div class='analysis'>\n")
        f.write("<h3>Análisis (con Heurística):</h3>\n")
        f.write("<ul>\n")
        f.write("<li><strong>A*</strong> utiliza la heurística para guiar su búsqueda, manteniendo la <strong>optimalidad</strong> (7458.00 m) mientras <strong>explora menos nodos</strong> que UCS, demostrando su eficiencia.</li>\n")
        f.write("<li><strong>Greedy</strong> (Voraz) con la heurística encuentra una ruta <strong>sub-óptima</strong> (10171.00 m). Esto ocurre porque Greedy solo mira el coste estimado restante (h(n)) e ignora el coste ya acumulado (g(n)), lo que lleva a elecciones 'voraces' que resultan caras a largo plazo.</li>\n")
        f.write("</ul>\n")
        f.write("</div>\n")
        
        # Gráfico 2
        f.write("<div class='graph-container'>\n")
        f.write("<h3>Gráfico: Nodos Explorados (Heurística Aproximada)</h3>\n")
        f.write(f"<img src='data:image/png;base64,{img_nodos_h_approx}' alt='Nodos Explorados'>\n")
        f.write("</div>\n")

        f.write("<hr>\n")
        f.write("</body>\n")
        f.write("</html>\n")
    
    print()
    print(f"\n{verde}Informe guardado en la carpeta {reset}{amarillo}'practica_busqueda'{reset} {verde}como{reset} {amarillo}'informe_resultados_busqueda.html'{reset}")
    print(f"{verde}¡ÁBRELO EN TU NAVEGADOR (Chrome, Firefox, Edge) para ver la tabla, los gráficos y el mapa!{reset}")
    print()


# Ejecución principal

if __name__ == "__main__":
    
    # Nombres de inicio y objetivo
    inicio = "IES Punta del Verde"
    objetivo = "Estadio La Cartuja"  
    
    # Definición de Heurísticas
    h_zero = heuristic_zero(GRAFO, objetivo)
    h_approx = heuristic_direct_path_cost(GRAFO, objetivo)

    #Resultados con Heurística Nula (h=0)
    resultados = []
    
    t0 = time.time(); camino, n = busqueda_bfs(GRAFO, inicio, objetivo); t1 = time.time()
    coste_bfs = calcular_coste(GRAFO, camino)
    resultados.append(("BFS", camino, coste_bfs, n, (t1-t0)*1000))

    t0 = time.time(); camino, n = busqueda_dfs(GRAFO, inicio, objetivo); t1 = time.time()
    coste_dfs = calcular_coste(GRAFO, camino)
    resultados.append(("DFS", camino, coste_dfs, n, (t1-t0)*1000))

    t0 = time.time(); camino, coste, n = busqueda_ucs(GRAFO, inicio, objetivo); t1 = time.time()
    resultados.append(("Coste Uniforme (UCS)", camino, coste, n, (t1-t0)*1000))

    t0 = time.time(); camino, coste, n = busqueda_greedy(GRAFO, inicio, objetivo, h_zero); t1 = time.time()
    resultados.append(("Greedy (h=0)", camino, coste, n, (t1-t0)*1000))

    t0 = time.time(); camino, coste, n = busqueda_a_estrella(GRAFO, inicio, objetivo, h_zero); t1 = time.time()
    resultados.append(("A* (h=0)", camino, coste, n, (t1-t0)*1000))

    mostrar_tabla(resultados, "Comparativa general (heurística cero)")

    # Resultados con Heurística Aproximada (h_approx)
    resultados_h = []
    
    t0 = time.time(); camino, n = busqueda_bfs(GRAFO, inicio, objetivo); t1 = time.time()
    coste_bfs_h = calcular_coste(GRAFO, camino)
    resultados_h.append(("BFS", camino, coste_bfs_h, n, (t1-t0)*1000))

    t0 = time.time(); camino, n = busqueda_dfs(GRAFO, inicio, objetivo); t1 = time.time()
    coste_dfs_h = calcular_coste(GRAFO, camino)
    resultados_h.append(("DFS", camino, coste_dfs_h, n, (t1-t0)*1000))

    t0 = time.time(); camino, coste, n = busqueda_ucs(GRAFO, inicio, objetivo); t1 = time.time()
    resultados_h.append(("Coste Uniforme (UCS)", camino, coste, n, (t1-t0)*1000))

    t0 = time.time(); camino, coste, n = busqueda_greedy(GRAFO, inicio, objetivo, h_approx); t1 = time.time()
    resultados_h.append(("Greedy", camino, coste, n, (t1-t0)*1000))

    t0 = time.time(); camino, coste, n = busqueda_a_estrella(GRAFO, inicio, objetivo, h_approx); t1 = time.time()
    resultados_h.append(("A*", camino, coste, n, (t1-t0)*1000))

    mostrar_tabla(resultados_h, "Comparativa con heurística aproximada (Coste de camino directo)")

    # Guardar informe y generar gráficos finales
    guardar_informe(resultados, resultados_h, inicio, objetivo)