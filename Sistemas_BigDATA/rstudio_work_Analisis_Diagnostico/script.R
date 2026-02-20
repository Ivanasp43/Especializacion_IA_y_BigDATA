# --- ACTIVIDAD 2.2: ANÁLISIS DIAGNÓSTICO ---

# Carga de datos
salarios <- read.csv("salarios.csv", sep = ";", dec = ",", fileEncoding = "Latin1")
vivienda <- read.csv("vivienda.csv", sep = ";", dec = ".", fileEncoding = "Latin1")

# Preparación de vectores (Datos extraídos del INE)
anios <- c(2021, 2022, 2023, 2024)
s <- c(2076.5, 2118.8, 2273.0, 2385.6)
v <- c(134.2, 142.6, 147.3, 159.6)

# Análisis de Correlación
cor(s, v)

# Gráfico Diagnóstico
plot(s, v, 
     main="Diagnóstico: Salario vs Vivienda (Nacional)",
     xlab="Salario Medio (€)", 
     ylab="Índice Precio Vivienda",
     pch=19, col="blue")
abline(lm(v ~ s), col="red", lwd=2)

# Modelo de Regresión
modelo <- lm(v ~ s)
summary(modelo)