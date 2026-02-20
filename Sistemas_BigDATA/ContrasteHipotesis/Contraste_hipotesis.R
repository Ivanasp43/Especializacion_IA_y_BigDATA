# 2.4 - Contraste de Hipótesis

# =========================
# PARTE 1: EL Z-TEST
# =========================

# Simulación de datos
set.seed(123)
muestra_cpus <- rnorm(n = 50, mean = 58, sd = 5)

# Cálculo de valores necesarios
media_muestral <- mean(muestra_cpus)
mu_teorica <- 60
sigma_conocida <- 5
n <- length(muestra_cpus)

# Cálculo del Z-score
z_score <- (media_muestral - mu_teorica) / (sigma_conocida / sqrt(n))
z_score

# Cálculo del p-valor (test bilateral)
p_valor <- 2 * pnorm(-abs(z_score))
p_valor

# Interpretación:
# El p-valor es menor que 0.05, por lo que podemos decir que el cambio
# de pasta térmica ha afectado a la temperatura media de los procesadores.
# La temperatura es diferente a los 60ºC habituales y, en este caso, menor.


# =========================
# PARTE 2: EL T-TEST
# =========================

# Tomamos una muestra pequeña en 20 pedidos con la nueva función
tiempos_nuevos <- c(28, 29, 30, 25, 27, 29, 31, 24, 26, 29,
                    28, 27, 30, 26, 25, 28, 29, 30, 24, 27)

# Comprobación de normalidad
shapiro.test(tiempos_nuevos)

# Interpretación:
# El resultado del test indica que los datos siguen una distribución normal,
# por lo que es adecuado utilizar un t-test.


# Planteamiento de hipótesis:
# H0: El tiempo medio de entrega es mayor o igual a 30 minutos
# H1: El tiempo medio de entrega es menor a 30 minutos

# Ejecución del t-test
t.test(tiempos_nuevos, mu = 30, alternative = "less")

# Interpretación:
# El p-valor es menor que 0.05, lo que indica que el tiempo medio de entrega
# con la nueva funcionalidad es menor a 30 minutos. Esto demuestra que la
# funcionalidad reduce los tiempos de entrega.


# =============================================
# COMPARACIÓN DE DOS MUESTRAS (ANDROID vs iOS)
# =============================================

# Datos simulados de gasto medio
set.seed(456)
gasto_android <- rnorm(30, mean = 15, sd = 5)
gasto_ios <- rnorm(30, mean = 18, sd = 5)

# T-test bilateral
t.test(gasto_android, gasto_ios)

# Interpretación:
# El test muestra que existen diferencias en el gasto medio entre usuarios
# de Android e iOS. Los usuarios de iOS presentan un gasto medio mayor.


# ======================
# PARTE 3: CHI-CUADRADO
# ======================

# Creación de la tabla de contingencia
datos_campana <- matrix(c(30, 70,
                          50, 50),
                        nrow = 2,
                        byrow = FALSE)

colnames(datos_campana) <- c("Campaña_A", "Campaña_B")
rownames(datos_campana) <- c("Compró", "No_Compró")

datos_campana


# Planteamiento de hipótesis:
# H0: Las variables son independientes (la compra no depende de la campaña)
# H1: Las variables son dependientes (el tipo de campaña influye)


# Ejecución del test Chi-cuadrado
test_chi <- chisq.test(datos_campana)
print(test_chi)

# Valores esperados
test_chi$expected

# Interpretación:
# El p-valor es menor que 0.05, por lo que se rechaza la hipótesis nula.
# Esto indica que la compra depende del tipo de campaña y que la campaña B
# obtiene mejores resultados que la campaña A.
# Si los datos no siguieran una distribución normal (p-valor < 0.05),
# no sería adecuado usar un t-test. En ese caso, se podría utilizar
# el test de Wilcoxon (wilcox.test), que no asume normalidad.

# =========================
# AMPLIACIÓN: VISUALIZACIÓN
# =========================

library(ggplot2)

# Creamos un data frame con los gastos
datos_gasto <- data.frame(
  gasto = c(gasto_android, gasto_ios),
  plataforma = c(rep("Android", length(gasto_android)),
                 rep("iOS", length(gasto_ios)))
)

# Gráfico de densidad
ggplot(datos_gasto, aes(x = gasto, fill = plataforma)) +
  geom_density(alpha = 0.5) +
  labs(title = "Distribución del gasto por plataforma",
       x = "Gasto",
       y = "Densidad")

# Interpretación:
# En el gráfico se observa que la distribución del gasto de los usuarios
# de iOS está desplazada hacia valores más altos que la de Android.
# Esto coincide con el resultado del t-test, que indicaba una diferencia
# en el gasto medio entre ambas plataformas.
