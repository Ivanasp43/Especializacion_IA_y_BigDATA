library(tidyverse)
library(lubridate)
library(forecast)
library(tseries)

# Cargar datos
netflix <- read.csv("Netflix_stock_data.csv")

# Convertir fecha a formato Date
netflix$Date <- as.Date(netflix$Date)

# Ordenar por fecha
netflix <- netflix %>% arrange(Date)

# Crear serie temporal (precio de cierre)
netflix_ts <- ts(netflix$Close, frequency = 252)

# Gráfico inicial
plot(netflix_ts,
     main = "Precio de cierre de Netflix",
     ylab = "Precio",
     xlab = "Tiempo")

# Descomposición de la serie
descomposicion <- stl(netflix_ts, s.window = "periodic")
plot(descomposicion)

# Test de estacionariedad
adf.test(netflix_ts)

# Número de diferencias necesarias
ndiffs(netflix_ts)

# Diferenciación
netflix_diff <- diff(netflix_ts)
plot(netflix_diff,
     main = "Serie diferenciada del precio de Netflix")

# Modelo ARIMA automático
modelo_arima <- auto.arima(netflix_ts)
summary(modelo_arima)

# ACF y PACF
acf(netflix_diff, main = "ACF")
pacf(netflix_diff, main = "PACF")

# Validación de residuos
checkresiduals(modelo_arima)

Box.test(residuals(modelo_arima),
         lag = 20,
         type = "Ljung-Box")

# Predicción a 30 días
prediccion <- forecast(modelo_arima, h = 30)

autoplot(prediccion) +
  labs(title = "Predicción del precio de Netflix",
       y = "Precio",
       x = "Tiempo")

