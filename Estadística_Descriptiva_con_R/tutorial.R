# -----------------------------------------------------------------------------
# PASO 0: Configuración del entorno
# -----------------------------------------------------------------------------
# Cargamos el "navaja suiza" de la ciencia de datos en R: Tidyverse
# Incluye: ggplot2 (gráficos), dplyr (manipulación), readr (lectura), etc.
library(tidyverse)

# -----------------------------------------------------------------------------
# PASO 1: Importación de datos (Data Loading)
# -----------------------------------------------------------------------------
# El archivo usa ';' como separador y ',' para decimales (formato español/europeo).
# Por eso usamos 'read_csv2' en lugar de 'read_csv'.

ruta_archivo <- "ipc.csv" # Asegúrate de que el archivo esté en tu directorio de trabajo

datos_raw <- read_csv2(ruta_archivo)

# -----------------------------------------------------------------------------
# PASO 2: Exploración inicial (Data Inspection)
# -----------------------------------------------------------------------------
print("--- Primeras filas ---")
head(datos_raw) # Muestra las primeras 6 filas

print("--- Estructura de los datos ---")
str(datos_raw)  # Muestra tipos de variables (carácter, numérico, etc.)

print("--- Nombres de columnas originales ---")
colnames(datos_raw)

# --- CONCEPTO CLAVE: CLASES Y VECTORES ---
# En R, las columnas de una tabla son "vectores".
# La función class() nos dice qué tipo de dato contiene un objeto.

print("--- Revisión de tipos de datos (class) ---")
# Vemos la clase del dataframe completo
print(class(datos_raw)) 

# Vemos la clase de una columna específica (un vector)
# El símbolo '$' se usa para extraer una columna específica
clase_periodo <- class(datos_raw$Periodo)
clase_valor   <- class(datos_raw$Total)

print(paste("La columna Periodo es de tipo:", clase_periodo))
print(paste("La columna Total es de tipo:", clase_valor))

# -----------------------------------------------------------------------------
# PASO 3: Limpieza y Transformación 
# -----------------------------------------------------------------------------
# Vamos a renombrar columnas para que sean más fáciles de usar (sin espacios ni tildes)
# y arreglar la fecha (actualmente es texto tipo "2025M11").

datos_limpios <- datos_raw %>%
  # 1. Renombrar columnas
  rename(
    grupo = `Grupos COICOP 2011`,
    tipo_dato = `Tipo de dato`,
    periodo_txt = Periodo,
    valor = Total
  ) %>%
  
  # 2. Filtrar o limpiar filas vacías si las hubiera
  filter(!is.na(valor)) %>%
  
  # 3. Crear una fecha real.
  # El formato es "2025M01". Reemplazamos "M" por "-" y añadimos el día "01".
  mutate(
    fecha = paste0(sub("M", "-", periodo_txt), "-01"), # Convierte "2025M01" a "2025-01-01"
    fecha = as.Date(fecha) # Le dice a R que interprete ese texto como fecha
  )

print("--- Datos limpios ---")
glimpse(datos_limpios)

# -----------------------------------------------------------------------------
# PASO 4: Manipulación con dplyr (Filtrar y Seleccionar)
# -----------------------------------------------------------------------------
# El dataset tiene muchos tipos de datos (índices, variaciones mensuales, anuales).
# Vamos a centrarnos solo en el "Índice general" y el tipo "Índice".

ipc_general <- datos_limpios %>%
  filter(
    grupo == "Índice general",
    tipo_dato == "Índice"
  ) %>%
  arrange(fecha) # Ordenamos cronológicamente

# -----------------------------------------------------------------------------
# PASO 5: Análisis Estadístico Básico
# -----------------------------------------------------------------------------
print("--- Resumen estadístico del IPC General ---")
summary(ipc_general$valor)

# Ejemplo: Calcular la media del IPC por Año
resumen_anual <- ipc_general %>%
  mutate(anio = format(fecha, "%Y")) %>% # Extraer solo el año
  group_by(anio) %>%                     # Agrupar por año
  summarise(
    media_ipc = mean(valor),
    max_ipc = max(valor),
    min_ipc = min(valor)
  )

print("--- Tabla resumen por año (primeros 5) ---")
head(resumen_anual)

# -----------------------------------------------------------------------------
# 6. CÁLCULO DE LA INFLACIÓN
# -----------------------------------------------------------------------------
# Vamos a calcular la variación mensual manualmente.
# Fórmula: (Valor_Actual - Valor_Anterior) / Valor_Anterior * 100

ipc_calculado <- datos_limpios %>%
  # Importante: Agrupar por grupo para no mezclar cálculos entre categorías
  group_by(grupo) %>%
  # Ordenar por fecha para asegurar que el cálculo sea cronológico
  arrange(fecha) %>%
  mutate(
    # lag() es una función que "mira" el valor de la fila anterior
    valor_anterior = lag(valor),
    inflacion_mensual = ((valor - valor_anterior) / valor_anterior) * 100
  ) %>%
  ungroup() # Desagrupar siempre al terminar cálculos

print("--- Datos con inflación calculada (Primeras filas) ---")
head(ipc_calculado)

# -----------------------------------------------------------------------------
# PASO 7: Visualización con ggplot2
# -----------------------------------------------------------------------------
# Vamos a graficar la evolución del IPC General a lo largo del tiempo.

grafico <- ggplot(data = ipc_general, aes(x = fecha, y = valor)) +
  # Capa de líneas
  geom_line(color = "steelblue", size = 1) +
  # Capa de puntos (para ver cada dato mensual)
  geom_point(color = "darkblue", alpha = 0.5, size = 1) +
  # Capa de suavizado (tendencia)
  geom_smooth(method = "loess", color = "red", linetype = "dashed", se = FALSE) +
  # Etiquetas y títulos
  labs(
    title = "Evolución del IPC General en España",
    subtitle = "Fuente: INE (Datos extraídos del CSV proporcionado)",
    x = "Año",
    y = "Índice de Precios",
    caption = "Generado con R y ggplot2"
  ) +
  # Tema visual limpio
  theme_minimal()

# Mostrar gráfico
print(grafico)

# GRÁFICO 1: LÍNEAS (Evolución Temporal y Comparación)
# Comparamos el "Índice general" con otro grupo (ej. Alimentos u Otros)
# Nota: Filtramos para que el gráfico no sea un caos de líneas
grupos_interes <- c("Índice general", levels(ipc_calculado$grupo)[2]) # Coge el general y el segundo grupo disponible

g1 <- ipc_calculado %>%
  filter(grupo %in% grupos_interes) %>%
  ggplot(aes(x = fecha, y = valor, color = grupo)) +
  geom_line(size = 1.2) +
  labs(title = "1. Comparativa de Evolución (Gráfico de Líneas)",
       y = "Índice (Base 2021=100)", x = "") +
  theme_minimal() +
  theme(legend.position = "bottom")

# GRÁFICO 2: BARRAS (Inflación Media por Año)
# Requiere una transformación previa de los datos
g2 <- ipc_calculado %>%
  filter(grupo == "Índice general") %>%
  mutate(anio = format(fecha, "%Y")) %>%
  group_by(anio) %>%
  summarise(inflacion_media = mean(inflacion_mensual, na.rm = TRUE)) %>%
  ggplot(aes(x = anio, y = inflacion_media, fill = inflacion_media > 0)) +
  geom_col(show.legend = FALSE) + # geom_col es para barras con valores definidos
  scale_fill_manual(values = c("red", "steelblue")) + # Rojo si baja, Azul si sube (ejemplo)
  labs(title = "2. Inflación Mensual Promedio por Año (Gráfico de Barras)",
       subtitle = "Calculado sobre el Índice General",
       y = "% Variación Mensual", x = "Año") +
  theme_minimal()

# GRÁFICO 3: BOXPLOT / CAJA Y BIGOTES (Distribución Estadística)
# Ideal para ver dispersión y valores atípicos (outliers)
g3 <- ipc_calculado %>%
  filter(grupo %in% grupos_interes) %>%
  ggplot(aes(x = grupo, y = inflacion_mensual, fill = grupo)) +
  geom_boxplot(alpha = 0.6) +
  labs(title = "3. Distribución de la Inflación (Boxplot)",
       subtitle = "Permite ver la volatilidad de los precios",
       y = "% Inflación Mensual", x = "") +
  theme_minimal() +
  theme(legend.position = "none")

# Mostrar los gráficos
print(g1)
print(g2)
print(g3)


