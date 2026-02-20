# 1. Imagen base con R ya instalado
FROM rocker/tidyverse:latest

# 2. Crear carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar los archivos al contenedor
COPY tutorial.R /app/tutorial.R
COPY ipc.csv /app/ipc.csv

# 4. Comando por defecto: ejecutar el script
CMD ["Rscript", "tutorial.R"]
