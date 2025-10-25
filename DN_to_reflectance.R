library(terra)

# Definir pastas
dir_bandas <- "D:/01-TESE/03-Capitulo_IV/orto_teste"
dir_saida  <- "D:/01-TESE/03-Capitulo_IV/orto_teste/reflectancia"
if (!dir.exists(dir_saida)) dir.create(dir_saida)

# Listar arquivos TIFF
arquivos <- list.files(dir_bandas, "\\.tif$", full.names=TRUE)
stopifnot(length(arquivos)>0)

# Função de conversão DN -> reflectância
convert_to_reflectance <- function(path_in, path_out) {
  r <- rast(path_in)
  r_ref <- r / 65535
  writeRaster(r_ref, path_out, overwrite=TRUE)
}

# Loop de conversão
for (f in arquivos) {
  nome <- tools::file_path_sans_ext(basename(f))
  out  <- file.path(dir_saida, paste0(nome, "_ref.tif"))
  convert_to_reflectance(f, out)
}

# Verificação final: min e max das bandas convertidas
arquivos_ref <- list.files(dir_saida, "_ref.tif$", full.names=TRUE)
for (f in arquivos_ref) {
  r <- rast(f)
  v <- terra::global(r, c("min","max"), na.rm=TRUE)
  print(sprintf("%s: min=%.4f, max=%.4f", basename(f), v[1], v[2]))
}
