# ================================================================
# Script: convert_dn_to_reflectance.R
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Converte imagens multibanda (.tif) de valores digitais (DN)
#            para reflectância normalizada (0–1), salvando novos arquivos.
# Linguagem: R
# Dependência: terra
# Data: 2025-10-25
# ================================================================

# --------------------
# PACOTE
# --------------------
if (!requireNamespace("terra", quietly = TRUE)) install.packages("terra")
library(terra)

# --------------------
# ENTRADAS
# --------------------
# pasta com os arquivos TIFF de entrada
dir_bandas <- "D:/01-TESE/03-Capitulo_IV/orto_teste"

# pasta de saída para os arquivos convertidos
dir_saida  <- "D:/"
if (!dir.exists(dir_saida)) dir.create(dir_saida, recursive = TRUE)

# lista de arquivos .tif
arquivos <- list.files(dir_bandas, "\\.tif$", full.names = TRUE)
stopifnot(length(arquivos) > 0)

# --------------------
# FUNÇÃO DE CONVERSÃO DN → REFLECTÂNCIA
# --------------------
convert_to_reflectance <- function(path_in, path_out) {
  r <- rast(path_in)
  r_ref <- r / 65535
  writeRaster(r_ref, path_out, overwrite = TRUE)
}

# --------------------
# LOOP DE PROCESSAMENTO
# --------------------
for (f in arquivos) {
  nome <- tools::file_path_sans_ext(basename(f))
  out  <- file.path(dir_saida, paste0(nome, "_ref.tif"))
  convert_to_reflectance(f, out)
}

# --------------------
# VERIFICAÇÃO FINAL
# --------------------
# imprime valores mínimo e máximo das bandas convertidas
arquivos_ref <- list.files(dir_saida, "_ref.tif$", full.names = TRUE)
for (f in arquivos_ref) {
  r <- rast(f)
  v <- terra::global(r, c("min", "max"), na.rm = TRUE)
  message(sprintf("%s: min=%.4f, max=%.4f", basename(f), v[1], v[2]))
}
