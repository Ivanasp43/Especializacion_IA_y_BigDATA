# Título: Identificación y extracción de datos del INE
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
print()

print(f"{azul}----------------------------------------------------------------------------------------------{reset}")
print(f"\n{azul}                        IDENTIFICACIÓN Y EXTRACCIÓN DE DATOS DEL INE                          {reset}")
print(f"{azul}----------------------------------------------------------------------------------------------{reset}")

import requests
import re
import json
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone


# URL de la API del INE para la tabla 25171 (IPV)
URL_INE = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/25171"

print(f"\n{azul_marino}     Haciendo la petición a la URL: {URL_INE}{reset}")
# Hacemos la petición GET a la URL
try:
    response = requests.get(URL_INE)
    # Levantamos una excepción si la petición falla (código de estado 4xx o 5xx)
    response.raise_for_status() 

    # Guardamos la respuesta como una lista de diccionarios de Python (el JSON)
    datos_json = response.json()
    print(f"\n{turquesa}     Petición exitosa. Datos JSON cargados.{reset}")

except requests.exceptions.RequestException as e:
    print(f"{rojo}Error al realizar la petición {e}{reset}")
    exit()

# Filtrar la información

datos_filtrados = []

# Iteramos sobre cada 'serie' de datos en el JSON 
for serie in datos_json:
    nombre_serie = serie.get("Nombre", "")
   
    if "General" in nombre_serie and not ("Variación" in nombre_serie or "Tasa" in nombre_serie):
        lugar = nombre_serie.replace("IPV - ", "").replace(" - General", "").strip()
        valores_por_tiempo = serie.get("Data", [])

        for dato in valores_por_tiempo:
            anyo = dato.get("Anyo")
            periodo = dato.get("Periodo")
            valor = dato.get("Valor")
            fecha = str(dato.get("Fecha", ""))  # convertir siempre a texto para evitar TypeError

            # Si el periodo no existe, intentamos deducirlo del campo Fecha
            if periodo is None and fecha:
                match = re.search(r'[TQ](\d)', fecha)
                if match:
                    periodo = f"T{match.group(1)}"
    
            if periodo is None:
                periodo = "T?"
            
            registro = {
                "Lugar": lugar,
                "Año":anyo,
                "Periodo": periodo,
                "IPV": valor
            }
            
            # Añadimos el nuevo diccionario a nuestra lista de resultados
            datos_filtrados.append(registro)

print(f"\n{verde}     Datos filtrados. Total de registros para el análisis:{reset} {lima}{len(datos_filtrados)}{reset}")
print()


# Creación de un Dataframe de Pandas

df_ipv = pd.DataFrame(datos_filtrados)

# Convertimos tipos con control de errores
df_ipv['Año'] = pd.to_numeric(df_ipv['Año'], errors='coerce')
df_ipv['IPV'] = pd.to_numeric(df_ipv['IPV'], errors='coerce')

# Eliminamos filas sin año o sin valor IPV
df_ipv = df_ipv.dropna(subset=['Año', 'IPV'])

# Mostrar las primeras filas y los tipos de datos (dtype)
print(f"\n{azul_marino}DataFrame Inicial{reset}")
print(f"{azul_marino}================={reset}")
print(df_ipv.head())
print(f"\n{azul_marino}Tipos de Datos (Dtype) Iniciales{reset}")
print(f"{azul_marino}================================{reset}")
print(df_ipv.dtypes)

# Ajuste de las columnas

df_ipv['Año'] = df_ipv['Año'].astype(int)
df_ipv['IPV'] = df_ipv['IPV'].astype(float)
df_ipv['Periodo'] = df_ipv['Periodo'].astype(str).fillna("T?")

# Crear columna "Tiempo" sin None
df_ipv['Tiempo'] = df_ipv['Año'].astype(str) + '-' + df_ipv['Periodo']


print(f"\n{azul_marino}DataFrame Final{reset}")
print(f"{azul_marino}==============={reset}")
print(df_ipv.head())
print(f"\n{azul_marino}Tipos de Datos (Dtype) Finales{reset}")
print(f"{azul_marino}=============================={reset}")
print(df_ipv.dtypes)


# Guardar Dataframe en CSV

print(f"\n{lima}     Guardando el DataFrame en formato CSV...{reset}")

tiempo_unix = int(datetime.now(timezone.utc).timestamp())

nombre_archivo = f"IPV_{tiempo_unix}.csv"
df_ipv.to_csv(nombre_archivo, index=False)

print(f"\n{verde}     ¡Éxito! El archivo CSV se ha guardado como:{reset} {lima}{nombre_archivo}{reset}")
print()
print(f"{rosa}     ¡Actividad 1.4 finalizada!{reset}")
print()



# ANÁLISIS ESTADÍSTICOS

print(f"\n{azul_marino}                Análisis Estadísticos{reset}")
print(f"{azul_marino}============================================================={reset}")

media_ipv_ccaa = df_ipv.groupby('Lugar')['IPV'].mean().sort_values(ascending=False)
print(f"\n{turquesa}      Media Histórica del IPV por CCAA (IPV General){reset}")
print(f"{turquesa}-------------------------------------------------------------{reset}")
print(media_ipv_ccaa)

extremos_ipv_ccaa = df_ipv.groupby('Lugar')['IPV'].agg(['min', 'max'])
print(f"\n{turquesa}     Valores Mínimo y Máximo Histórico del IPV por CCAA{reset}")
print(f"{turquesa}--------------------------------------------------------------{reset}")
print(extremos_ipv_ccaa)
print()

# REPRESENTACIÓN GRÁFICA

# Filtrar Andalucía
df_andalucia = df_ipv[df_ipv['Lugar'].str.contains('Andalucía', case=False, na=False)].copy()
print(f"{turquesa}  Registros para Andalucía{reset}", len(df_andalucia))
print(f"{turquesa}-----------------------------------{reset}")
print()

# Si hay valores extraños en Periodo (como T?), los normalizamos
df_andalucia['periodo_num'] = df_andalucia['Periodo'].str.extract(r'T(\d+)').astype(float)
df_andalucia['periodo_num'] = df_andalucia['periodo_num'].fillna(1)
df_andalucia = df_andalucia.sort_values(by=['Año', 'periodo_num']).reset_index(drop=True)

print(df_andalucia[['Año', 'Periodo', 'IPV', 'Tiempo']].head(10))

# Gráfico
if not df_andalucia.empty:
    plt.figure(figsize=(12, 6))
    x_idx = range(len(df_andalucia))
    plt.plot(x_idx, df_andalucia['IPV'].values, marker='o', linestyle='-', color='blue')
    
    # Etiquetas del eje X
    step = max(1, len(df_andalucia) // 12)
    plt.xticks(list(x_idx)[::step], df_andalucia['Tiempo'].tolist()[::step], rotation=45, ha='right')
    plt.title('Evolución del IPV General en Andalucía')
    plt.xlabel('Tiempo (Año-Trimestre)')
    plt.ylabel('Índice de Precios de Vivienda (IPV)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
else:
    print(f"\n{rojo} ¡¡ERROR!! No se encontraron datos para Andalucía.{reset}")
