# ================================================================
# Script: unifica_shapefiles.R
# Autor: Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Faz a união de múltiplos shapefiles (.shp) em um único arquivo vetorial.
# Linguagem: R
# Dependência: terra
# Data: 2025-06-11
# ================================================================

### Faz a união de vários shapefiles separados em um único shapefile ###

# --------------------
# PACOTE
# --------------------
if (!requireNamespace("terra", quietly = TRUE)) install.packages("terra")
library(terra)

# --------------------
# ENTRADAS
# --------------------
# pasta com os shapefiles
dir_shp <- "D:/"

# pasta onde o shapefile unificado será salvo
dir_out <- "D:/"
if (!dir.exists(dir_out)) dir.create(dir_out, recursive = TRUE)

# --------------------
# LEITURA E UNIÃO
# --------------------
# lista arquivos .shp
arquivos <- list.files(dir_shp, "\\.shp$", full.names = TRUE)

# lê e une (terra ignora coordenadas Z automaticamente)
shapes_list <- lapply(arquivos, vect)
shapes_unificado <- do.call(rbind, shapes_list)

# --------------------
# SAÍDA
# --------------------
# caminho completo do shapefile de saída
output_shp <- file.path(dir_out, ".shp")

# grava shapefile unificado em 2D
writeVector(shapes_unificado, output_shp, overwrite = TRUE)

