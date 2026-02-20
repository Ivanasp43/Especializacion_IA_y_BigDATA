
############################################################
# ANÁLISIS DE COMPONENTES PRINCIPALES (PCA)
# Dataset: mtcars
# Autor: Ivana Sánchez Pérez 
# Fecha: 17/01/2026
############################################################

# Cargar dataset nativo
data(mtcars)

# Inspección inicial
head(mtcars)
str(mtcars)

# Comprobar valores nulos
sum(is.na(mtcars))

# Calcular matriz de correlación
cor_mtcars <- cor(mtcars)

# Visualizar matriz de correlaciones
corrplot::corrplot(
  cor_mtcars,
  method = "color",
  type = "upper",
  tl.cex = 0.8
)

# Ejecutar PCA escalando los datos
pca_mtcars <- prcomp(mtcars, scale = TRUE)

# Resumen del modelo PCA
summary(pca_mtcars)

# Ver cargas (loadings)
pca_mtcars$rotation


# Scree Plot usando funciones base de R
plot(pca_mtcars, type = "lines")


# Biplot con las dos primeras componentes
biplot(pca_mtcars)


