# Título: Algoritmo de Colonia de Hormigas (ACO) 
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
import random 
import numpy as np 

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


# Clase Nodo
class Nodo:
    def __init__(self, nombre, padre=None, coste=0, heuristica=0):
        self.nombre = nombre 
        self.padre = padre   
        self.coste = coste   
        self.heuristica = heuristica 

    def __lt__(self, otro):
        return (self.coste + self.heuristica) < (otro.coste + otro.heuristica)

# Función para reconstruir el camino desde el nodo final.
def reconstruir_camino(nodo):
    camino = []
    while nodo:
        camino.append(nodo.nombre)
        nodo = nodo.padre
    return list(reversed(camino))

# Función para calcular el coste total de un camino
def calcular_coste(grafo, camino):
    if not camino or len(camino) < 2:
        return 0
    coste = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i+1]
        coste += grafo.get(origen, {}).get(destino, 0) 
    return coste

# Búsqueda en anchura (BFS) - SOLO PARA CALCULAR COSTE DE REFERENCIA PARA ACO (tau_0)
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


# Funciones para ACO

def calcular_visibilidad(grafo):
    # Calcula la visibilidad (atractivo) para ACO: 1 / distancia.
    visibilidad = {}
    for origen, conexiones in grafo.items():
        visibilidad[origen] = {}
        for destino, coste in conexiones.items():
            if coste > 0:
                visibilidad[origen][destino] = 1.0 / coste
            else:
                visibilidad[origen][destino] = 1.0 / 1000000.0
    return visibilidad

VISIBILIDAD = calcular_visibilidad(GRAFO)

# Algoritmo de Colonia de Hormigas (ACO) 

def algoritmo_aco(grafo, inicio, objetivo, num_hormigas=15, num_iteraciones=150, alpha=1.0, beta=5.0, rho=0.1, Q=1000):
    
    print(f"\n{azul}{'#'*110}{reset}")
    print(f"{turquesa}INICIANDO ALGORITMO DE COLONIA DE HORMIGAS (ACO){reset}")
    print(f"{azul}{'#'*110}{reset}")
    print(f"{rosa}Parámetros:{reset}{lima} Hormigas={reset}{amarillo}{num_hormigas}{reset}, {lima}Iteraciones={reset}{amarillo}{num_iteraciones}{reset}, {lima}Alpha={reset}{amarillo}{alpha}{reset}, {lima}Beta={reset}{amarillo}{beta}{reset},{lima} Rho={reset}{amarillo}{rho}{reset}, {lima}Q={reset}{amarillo}{Q}{reset}")
    
    # Inicialización
    nodos = list(grafo.keys())
    
    # Usamos un coste de referencia para el valor inicial de feromona
    coste_bfs, _ = busqueda_bfs(grafo, inicio, objetivo)
    coste_ref = calcular_coste(grafo, coste_bfs)
    tau_0 = Q / coste_ref if coste_bfs and coste_ref > 0 else 1.0
    print(f"{rosa}Coste de referencia (BFS):{reset} {amarillo}{coste_ref:.2f}.{ResourceWarning} {rosa}Valor inicial de feromona (tau_0):{reset}{amarillo} {tau_0:.4f}{reset}")
    
    feromonas = {}
    for origen in nodos:
        feromonas[origen] = {}
        for destino in grafo.get(origen, {}):
            feromonas[origen][destino] = tau_0
            
    visibilidad = VISIBILIDAD 
    mejor_camino_global = None
    menor_coste_global = inf
    nodos_explorados = 0 
    
    # Bucle Principal de Iteraciones 
    for iteracion in range(num_iteraciones):
        
        caminos_hormigas = [] 
        # Construcción del Camino
        for k in range(num_hormigas):
            camino_k = [inicio]
            coste_k = 0
            nodo_actual = inicio
            nodos_visitados = {inicio}
            nodos_explorados += 1 
            
            while nodo_actual != objetivo:
                
                vecinos = [n for n in grafo.get(nodo_actual, {}) if n not in nodos_visitados]
                
                if not vecinos:
                    coste_k = inf 
                    break

                # Cálculo de Probabilidades P_ij^k
                probabilidades_raw = {}
                suma_total = 0
                
                for j in vecinos:
                    tau = feromonas[nodo_actual].get(j, tau_0)
                    eta = visibilidad[nodo_actual][j]
                    
                    # Numerador: (feromona ^ alpha) * (visibilidad ^ beta)
                    numerador = (tau ** alpha) * (eta ** beta) 
                    probabilidades_raw[j] = numerador
                    suma_total += numerador
                
                # Normalizar probabilidades y seleccionar
                nombres = []
                probs = []
                if suma_total > 0:
                    for j, numerador in probabilidades_raw.items():
                        nombres.append(j)
                        probs.append(numerador / suma_total)
                else:
                    nombres = vecinos
                    probs = [1.0 / len(vecinos)] * len(vecinos)
                
                # Selección del Siguiente Nodo (Regla de la Ruleta)
                siguiente_nodo = random.choices(nombres, weights=probs, k=1)[0]
                
                # Actualizar
                coste_arista = grafo[nodo_actual][siguiente_nodo]
                coste_k += coste_arista
                camino_k.append(siguiente_nodo)
                nodos_visitados.add(siguiente_nodo)
                nodo_actual = siguiente_nodo
                nodos_explorados += 1 
            
            # Almacenar y actualizar el mejor camino global
            if coste_k != inf:
                caminos_hormigas.append((camino_k, coste_k))
                
                if coste_k < menor_coste_global:
                    menor_coste_global = coste_k
                    mejor_camino_global = camino_k
                    # Mantener el print de iteración para el diseño de salida
                    print(f"  > Iteración {iteracion+1}: Nuevo mejor coste global = {menor_coste_global:.2f}")
        
        # Actualización de Feromonas 
        
        # Evaporación
        for origen in feromonas:
            for destino in feromonas[origen]:
                feromonas[origen][destino] = (1.0 - rho) * feromonas[origen][destino]
                
        # Depósito 
        for camino_k, coste_k in caminos_hormigas:
            delta_tau = Q / coste_k 
            
            for i in range(len(camino_k) - 1):
                origen = camino_k[i]
                destino = camino_k[i+1]
                
                feromonas[origen][destino] += delta_tau
                if destino in feromonas and origen in feromonas[destino]:
                    feromonas[destino][origen] += delta_tau
    
    print(f"\n{azul}{'#'*110}{reset}")
    print(f"{turquesa}RESULTADO FINAL DE ACO{reset}")
    print(f"{azul}{'#'*110}{reset}")
    print(f"{rosa}Mejor camino global: {reset}{amarillo} {'->'.join(mejor_camino_global) if mejor_camino_global else 'No encontrado'}{reset}")
    print(f"{rosa}Menor coste global: {reset}{lima}{menor_coste_global:.2f} m{reset}")
    print(f"{rosa}Total de nodos explorados (pasos de hormigas):{reset}{lima} {nodos_explorados}{reset}")
    
    return mejor_camino_global, menor_coste_global, nodos_explorados

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


def generar_mapa_ruta(grafo, coordenadas, camino_optimo, inicio, objetivo):
    
    plt.figure(figsize=(10, 12)) 
    
    for origen, conexiones in grafo.items():
        if origen in coordenadas:
            x1, y1 = coordenadas[origen]
            for destino, _ in conexiones.items():
                if destino in coordenadas:
                    x2, y2 = coordenadas[destino]
                    plt.plot([x1, x2], [y1, y2], 'k-', alpha=0.3, zorder=1) 
    
    nombres_nodos = list(coordenadas.keys())
    x_coords = [coordenadas[n][0] for n in nombres_nodos]
    y_coords = [coordenadas[n][1] for n in nombres_nodos]
    
    plt.scatter(x_coords, y_coords, c="#6579DC", s=300, alpha=0.9, zorder=2, edgecolor='k') 

    if camino_optimo:
        ruta_x = [coordenadas[n][0] for n in camino_optimo]
        ruta_y = [coordenadas[n][1] for n in camino_optimo]
        plt.plot(ruta_x, ruta_y, linewidth=4, color="#26b41f", zorder=3, label='Ruta Óptima (ACO)') 
    
    plt.scatter(coordenadas[inicio][0], coordenadas[inicio][1], c='lime', s=400, marker='o', zorder=4, label=f'Inicio: {inicio}', edgecolor='k') 
    plt.scatter(coordenadas[objetivo][0], coordenadas[objetivo][1], c='red', s=400, marker='X', zorder=4, label=f'Objetivo: {objetivo}', edgecolor='k') 
    
    offset_map = {
        'Hospital Virgen del Rocío': (-60, 5), 
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
        plt.annotate(nombre, (x, y), textcoords="offset points", xytext=offset, ha='left', fontsize=9, bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.6, ec="none")) 
    
    plt.title('Ruta Óptima encontrada por ACO en el Grafo de Sevilla', fontsize=16)
    plt.legend(loc='lower right')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks([]) 
    plt.yticks([]) 
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_base64


def generar_graficos_mapa(resultado_aco, inicio, objetivo):
    camino_optimo = resultado_aco[0][1] 
    img_mapa = generar_mapa_ruta(GRAFO, COORDENADAS, camino_optimo, inicio, objetivo)
    return img_mapa

def guardar_informe(resultado_aco, inicio, objetivo):
    
    img_mapa = generar_graficos_mapa(resultado_aco, inicio, objetivo)
    
    alg, camino, coste, explorados, tiempo = resultado_aco[0]

    html_content = ""
    html_content += "<!DOCTYPE html>\n"
    html_content += "<html lang='es'>\n"
    html_content += "<head>\n"
    html_content += "    <meta charset='UTF-8'>\n"
    html_content += "    <title>Informe de Resultados del Algoritmo de Colonia de Hormigas (ACO)</title>\n"
    html_content += "    <style>\n"
    html_content += "        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }\n"
    html_content += "        h1, h2, h3 { color: #333; }\n"
    html_content += "        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }\n"
    html_content += "        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }\n"
    th_color = "#2c5f2d"
    html_content += f"        th {{ background-color: {th_color}; color: white; }}\n"
    html_content += "        tr:nth-child(even) { background-color: #f2f2f2; }\n"
    html_content += "        .analysis { background-color: #e6f7ff; padding: 15px; border-radius: 5px; margin-bottom: 30px; border-left: 5px solid #2196F3; }\n"
    html_content += "        .graph-container { text-align: center; margin-bottom: 40px; }\n"
    html_content += "        img { max-width: 100%; height: auto; border: 1px solid #ccc; border-radius: 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }\n"
    html_content += "    </style>\n"
    html_content += "</head>\n"
    html_content += "<body>\n"
    
    html_content += "<h1>Informe de Resultados del Algoritmo de Colonia de Hormigas (ACO)</h1>\n"
    html_content += "<h2>Tarea: Ruta de {} a {}</h2>\n".format(inicio, objetivo)
    html_content += "<p>A continuación se presenta el resultado de la ejecución del Algoritmo de Colonia de Hormigas (ACO).</p>\n"
    

    html_content += "<h2>Resultado del Algoritmo de Colonia de Hormigas (ACO)</h2>\n"
    html_content += "<table>\n"
    html_content += "<thead>\n"
    html_content += "<tr><th>Algoritmo</th><th>Camino encontrado</th><th>Coste total (m)</th><th>Nodos explorados</th><th>Tiempo (ms)</th></tr>\n"
    html_content += "</thead>\n"
    html_content += "<tbody>\n"
    camino_str = '->'.join(camino) if camino else "No encontrado"
    coste_str = f"{coste:.2f}" if coste != inf else "inf"
    html_content += f"<tr style='font-weight: bold; background-color: #d4edda;'><td>{alg}</td><td>{camino_str}</td><td>{coste_str}</td><td>{explorados}</td><td>{tiempo:.2f}</td></tr>\n"
    html_content += "</tbody>\n"
    html_content += "</table>\n"
    
    html_content += "<div class='analysis'>\n"
    html_content += "<h3>Análisis de Resultados:</h3>\n"
    html_content += "<ul>\n"
    html_content += "<li>El algoritmo ACO encontró una ruta con un coste de <strong>{:.2f} m</strong>.</li>\n".format(coste)
    html_content += "<li>El número de nodos explorados (pasos de hormigas) fue de <strong>{}</strong>.</li>\n".format(explorados)
    html_content += "</ul>\n"
    html_content += "</div>\n"

    # Gráfico del mapa de ruta 
    html_content += "<div class='graph-container'>\n"
    html_content += "<h3>Mapa de la Ruta Óptima encontrada por ACO</h3>\n"
    html_content += f"<img src='data:image/png;base64,{img_mapa}' alt='Mapa del grafo con la ruta óptima resaltada por ACO'>\n"
    html_content += "<p>La ruta óptima encontrada por ACO está resaltada en el grafo de Sevilla.</p>"
    html_content += "</div>\n"
    
    html_content += "<hr>\n"
    html_content += "</body>\n"
    html_content += "</html>\n"
    
    with open("informe_resultados_ACO.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    
    inicio = "IES Punta del Verde"
    objetivo = "Estadio La Cartuja"  
    
    t0 = time.time()
    camino_aco, coste_aco, n_aco = algoritmo_aco(
        GRAFO, inicio, objetivo, 
        num_hormigas=15, 
        num_iteraciones=150, 
        alpha=1.0, 
        beta=5.0, 
        rho=0.1,  
        Q=1000
    )
    t1 = time.time()
    tiempo_aco = (t1-t0) * 1000
    
    resultados_final = [("ACO", camino_aco, coste_aco, n_aco, tiempo_aco)]

    mostrar_tabla(resultados_final, "RESULTADO DEL ALGORITMO DE COLONIA DE HORMIGAS (ACO)")
    guardar_informe(resultados_final, inicio, objetivo)
    print()
    print(f"\n{verde}Informe guardado en la carpeta {reset}{amarillo}'practica_busqueda'{reset} {verde}como{reset} {amarillo}'informe_resultados_ACO.html'{reset}")
    print(f"{verde}¡ÁBRELO EN TU NAVEGADOR (Chrome, Firefox, Edge) para ver la tabla y el mapa!{reset}")
    print()