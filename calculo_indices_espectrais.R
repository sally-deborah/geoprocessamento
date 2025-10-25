library(terra)
library(sf)

# Pastas
dir_bandas <- "D:/01-TESE/03-Capitulo_IV/orto_teste/reflectancia"
dir_shape  <- "D:/01-TESE/03-Capitulo_IV/04-shapefiles/talhoes"
dir_saida  <- "D:/01-TESE/03-Capitulo_IV/09-ortomosaicos/04_IVs_120m"
if (!dir.exists(dir_saida)) dir.create(dir_saida)

arquivos <- list.files(dir_bandas, pattern="\\.tif$", full.names=TRUE)
b_blue  <- rast(arquivos[grepl("B1_blue_ref", arquivos)])
b_green <- rast(arquivos[grepl("B2_green_ref", arquivos)])
b_red   <- rast(arquivos[grepl("B3_red_ref", arquivos)])
b_re    <- rast(arquivos[grepl("B4_rededge_ref", arquivos)])
b_nir   <- rast(arquivos[grepl("B5_NIR_ref", arquivos)])

# Índices
ndvi  <- (b_nir - b_red)  / (b_nir + b_red)
ndre  <- (b_nir - b_re)   / (b_nir + b_re)
gndvi <- (b_nir - b_green)/ (b_nir + b_green)
osavi <- 1.16 * ((b_nir - b_green) / (b_nir + b_green + 0.16))
psri  <- (b_red - b_green) / b_re
ndwi  <- (b_green - b_nir) / (b_green + b_nir)
mcari <- ((b_re - b_red) - 0.2*(b_re - b_green)) * (b_re / b_red)
tcari <- 3 * ((b_re - b_red) - 0.2*(b_re - b_green)) * (b_re / b_red)
tvi   <- sqrt(((b_nir - b_red) / (b_nir + b_red)) + 0.5)

# CCCI robusto
eps <- 1e-6
mask <- (abs(b_nir + b_re) > eps) & (abs(b_nir + b_red) > eps) &
  (abs(b_nir - b_re) > eps) & (abs(b_nir - b_red) > eps)
ccci <- ifel(mask,
             ((b_nir - b_re)/(b_nir + b_re + eps)) / ((b_nir - b_red)/(b_nir + b_red + eps)),
             NA)

# Clamp índices aos intervalos típicos
ndvi  <- clamp(ndvi,  -1, 1)
ndre  <- clamp(ndre,  -1, 1)
gndvi <- clamp(gndvi, -1, 1)
osavi <- clamp(osavi, -1, 1.5)
psri  <- clamp(psri,  -1, 1)     # pode ser ajustado conforme literatura se necessário
ndwi  <- clamp(ndwi,  -1, 1)
mcari <- clamp(mcari, -1, 1)
tcari <- clamp(tcari, -1, 1)
tvi   <- clamp(tvi,    0, 1)     # TVI é positivo
ccci  <- clamp(ccci,  -1, 2)     # CCCI pode variar, normalmente 0-1 mas pode passar disso

# Empilha
indices <- rast(list(
  NDVI  = ndvi, NDRE  = ndre, GNDVI = gndvi, OSAVI = osavi,
  PSRI  = psri, NDWI  = ndwi, MCARI = mcari, TCARI = tcari,
  TVI   = tvi,  CCCI  = ccci
))

# Shape de treino
shape <- st_read(file.path(dir_shape, "17A_treino.shp")) |> st_transform(crs(indices))

# Recorte, mascare e salve com tipo float
for (nm in names(indices)) {
  r  <- mask(crop(indices[[nm]], shape), shape)
  writeRaster(r,
              file.path(dir_saida, paste0(nm, "_recortado.tif")),
              datatype="FLT4S",
              overwrite=TRUE
  )
}

# (opcional) plot visualização
par(mfrow=c(2,5), mar=c(2,2,2,2))
for(nm in names(indices)){
  plot(indices[[nm]], main=nm)
}

jpeg("D:/01-TESE/03-Capitulo_IV/indices_visualizacao.jpeg", width=3200, height=1600, res=300)
par(mfrow=c(2,5), mar=c(2,2,2,2))
for(nm in names(indices)){
  plot(indices[[nm]], main=nm)
}
dev.off()
