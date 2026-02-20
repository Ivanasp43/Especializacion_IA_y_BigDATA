############################################################
# AMPLIACIÓN: PCA con Dataset USArrests
############################################################

# 1. Carga de datos (Estadísticas de criminalidad en EE.UU.)
data("USArrests")

# 2. PCA con escalado (Indispensable: Murder y Assault tienen escalas muy distintas)
pca_ampliacion <- prcomp(USArrests, scale = TRUE)

# 3. Visualización del Scree Plot (Varianza explicada)
plot(pca_ampliacion, type = "lines", main = "Scree Plot: USArrests")

# 4. Biplot interpretativo
biplot(pca_ampliacion, cex = 0.7, main = "Biplot de Criminalidad por Estado")