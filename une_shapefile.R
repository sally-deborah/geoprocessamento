### faz a uniao de varios shapefiles separados em um unico shapefile ####
### 11-06-2025

# Instale e carregue o terra
install.packages("terra")
library(terra)

# pasta com os shapefiles
dir_shp <- "D:\\01-TESE\\03-Capitulo IV - detecção de estresse\\04-shapefiles\\amostras"

# pasta onde o shapefile unificado será salvo
dir_out <- "D:\\01-TESE\\03-Capitulo IV - detecção de estresse\\04-shapefiles\\amostras\\unificado"
if (!dir.exists(dir_out)) dir.create(dir_out, recursive = TRUE)

# lista .shp
arquivos <- list.files(dir_shp, "\\.shp$", full.names = TRUE)

# leia e una (terra ignora Z automaticamente)
shapes_list <- lapply(arquivos, vect)
shapes_unificado <- do.call(rbind, shapes_list)

# caminho completo do shapefile de saída
output_shp <- file.path(dir_out, "coleta_pts_amostras.shp")

# grave o shapefile unificado 2D
writeVector(shapes_unificado, output_shp, overwrite = TRUE)
