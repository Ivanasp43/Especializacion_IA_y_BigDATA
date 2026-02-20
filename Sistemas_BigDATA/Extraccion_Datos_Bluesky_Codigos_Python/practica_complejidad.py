import random
import timeit
import itertools

# ------------------------------------------------------------
# Función 1
# ------------------------------------------------------------
def funcion_alpha(lista):
    longitud = len(lista)                                     # O(1)
    suma_elementos = sum(lista)                               # O(n)
    media = suma_elementos / longitud if longitud > 0 else 0  # O(1)
    lista_modificada = [x + 1 for x in lista]                 # O(n)
    lista_ordenada = sorted(lista_modificada)                 # O(n log n)
    return lista_ordenada, media                              # O(1)
# orden de complejidad de la función alpha =                    O(n log n)


# ------------------------------------------------------------
# Función 2
# ------------------------------------------------------------
def funcion_beta(n):
    resultados = []                       # O(1)
    for i in range(2 ** n):               # O(2^n)
        combinacion = []                  # O(1)
        for j in range(n):                # O(n)
            if (i >> j) & 1:              # O(1)
                combinacion.append(1)     # O(1)
            else:
                combinacion.append(0)     # O(1)
        resultados.append(combinacion)    # O(n)
    return resultados                     # O(1)
# orden de complejidad de la función beta = O(n * 2^n)


# ------------------------------------------------------------
# Función 3
# ------------------------------------------------------------
def funcion_gamma(lista):
    x = 10                                 # O(1)
    y = 20                                 # O(1)
    z = x * y                              # O(1)
    elemento = lista[0]                    # O(1)
    resultado = elemento + z               # O(1)
    valor_extra = resultado * 2 - 3        # O(1)
    return valor_extra                     # O(1)
# orden de complejidad de la función gamma = O(1)


# ------------------------------------------------------------
# Función 4
# ------------------------------------------------------------
def funcion_delta(estructura):
    total = 0                              # O(1)
    for bloque in estructura:              # O(n)
        for fila in bloque:                # O(n)
            for valor in fila:             # O(n)
                total += valor             # O(1)
    return total                           # O(1)
# orden de complejidad de la función delta = O(n^3)


# ------------------------------------------------------------
# Función 5
# ------------------------------------------------------------
def funcion_epsilon(lista):
    suma = 0                                 # O(1)
    promedio = sum(lista) / len(lista)       # O(n)
    for elemento in lista:                   # O(n)
        suma += elemento * 2                 # O(1)
    maximo = max(lista)                      # O(n)
    minimo = min(lista)                      # O(n)
    diferencia = maximo - minimo             # O(1)
    return suma + promedio + diferencia      # O(1)
# orden de complejidad de la función epsilon = O(n)


# ------------------------------------------------------------
# Función 6
# ------------------------------------------------------------
def funcion_zeta(matriz):
    total = 0                             # O(1)
    for fila in matriz:                   # O(n)
        for valor in fila:                # O(n)
            total += valor                # O(1)
    return total                          # O(1)
# orden de complejidad de la función zeta = O(n^2)


# ------------------------------------------------------------
# Función 7
# ------------------------------------------------------------
def funcion_theta(n):                                        # O(1)
    elementos = list(range(n))                               # O(n)
    permutaciones = list(itertools.permutations(elementos))  # O(n!)
    return permutaciones                                     # O(1)
# orden de complejidad de la función theta =                   O(n!)


# ------------------------------------------------------------
# Función 8
# ------------------------------------------------------------
def funcion_omega(lista, objetivo):          
    izquierda, derecha = 0, len(lista) - 1 # O(1)
    while izquierda <= derecha:            # O(log n)
        medio = (izquierda + derecha) // 2 # O(1))
        if lista[medio] == objetivo:       # O(1)
            return True                    # O(1)
        elif lista[medio] < objetivo:      # O(1)
            izquierda = medio + 1          # O(1)
        else:
            derecha = medio - 1            # O(1)
    return False                           # O(1)
# orden de complejidad de la función omega = O(log n)
