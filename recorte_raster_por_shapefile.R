# ================================================================
# Script: recorte_raster_por_shapefile.R
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
#
# Descrição: Realiza o recorte (crop + mask) de imagens raster (.tif)
#             utilizando um shapefile como limite da área de interesse.
#             Garante compatibilidade de CRS (reprojeção automática)
#             e exporta os arquivos recortados para um diretório definido.
# Linguagem: R
# Dependências: terra, sf, tools
# Data: 2025-10-27
# ================================================================

# ------------------------------------------------------------
# 1. Carregar pacotes
# ------------------------------------------------------------
library(terra)
library(sf)
library(tools)

# ------------------------------------------------------------
# 2. Definir diretórios
# ------------------------------------------------------------
dir_bandas <- "data/rasters"
dir_shape  <- "data/shapes"
dir_saida  <- "results/recortes"

if (!dir.exists(dir_saida)) dir.create(dir_saida, recursive = TRUE)

# ------------------------------------------------------------
# 3. Carregar shapefile e verificar CRS
# ------------------------------------------------------------
shape_path <- file.path(dir_shape, "area_experimental.shp")
shape <- vect(shape_path)
shp_crs <- crs(shape)

# ------------------------------------------------------------
# 4. Listar arquivos raster (.tif)
# ------------------------------------------------------------
arquivos <- list.files(dir_bandas, pattern = "\\.tif$", full.names = TRUE)

# ------------------------------------------------------------
# 5. Recortar e exportar cada raster
# ------------------------------------------------------------
for (arquivo in arquivos) {
  r <- rast(arquivo)
  
  # Reprojetar o raster, se necessário
  if (!identical(crs(r), shp_crs)) {
    message("Reprojetando CRS de: ", basename(arquivo))
    r <- project(r, shp_crs)
  }
  
  # Recorte e máscara
  r_crop <- crop(r, shape)
  r_mask <- mask(r_crop, shape)
  
  # Gerar nome de saída
  nome_banda <- file_path_sans_ext(basename(arquivo))
  nome_saida <- file.path(dir_saida, paste0(nome_banda, "_recorte.tif"))
  
  # Exportar
  writeRaster(r_mask, nome_saida, overwrite = TRUE)
  message("✅ Raster recortado salvo em: ", nome_saida)
}

cat("Processamento concluído. Resultados em:", dir_saida, "\n")
