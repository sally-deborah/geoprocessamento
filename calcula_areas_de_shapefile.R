# pacotes
library(sf)
library(dplyr)
library(units)
library(readr)

# --------------------
# ENTRADAS
# --------------------
# área do talhão (hectares)
talhao_ha <- 26

# caminhos dos 4 shapefiles
arquivos <- c(
  "D:/classificacao/class_0_estress.shp",
  "D:/classificacao/class_1_saudaveis.shp",
  "D:/classificacao/class_2_mortas.shp"
)
rotulos  <- c("Doentes","Saudaveis", "Mortas")
classes  <- tibble(arquivo = arquivos, classe = rotulos)

# --------------------
# LEITURA + PREP
# --------------------
# lê todos os shapes, força validade e garante CRS métrico
gdfs <- lapply(arquivos, \(f) st_read(f, quiet = TRUE) |> st_make_valid())

# pega CRS do primeiro; se estiver em graus, projeta para LAEA local (m)
is_deg <- isTRUE(st_is_longlat(st_crs(gdfs[[1]])))
if (is_deg) {
  # centroide aproximado para definir LAEA local
  cen <- gdfs[[1]] |> st_union() |> st_centroid() |> st_transform(4326) |> st_coordinates()
  laea <- paste0("+proj=laea +lat_0=", cen[2], " +lon_0=", cen[1],
                 " +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs")
  gdfs <- lapply(gdfs, \(g) st_transform(g, laea))
}

# garante todos no mesmo CRS e multipolígonos válidos
crs_ref <- st_crs(gdfs[[1]])
gdfs <- lapply(gdfs, \(g) {
  if (st_crs(g) != crs_ref) g <- st_transform(g, crs_ref)
  st_make_valid(g)
})

# adiciona rótulo da classe por arquivo e une tudo
for (i in seq_along(gdfs)) gdfs[[i]]$arquivo <- arquivos[i]
gdf_total <- do.call(rbind, gdfs) |>
  left_join(classes, by = "arquivo") |>
  mutate(classe = factor(classe, levels = rotulos))

# --------------------
# CÁLCULO DE ÁREA
# --------------------
# dissolve por classe e calcula áreas
resumo <- gdf_total |>
  group_by(classe) |>
  summarise(geom = st_union(geometry), .groups = "drop") |>
  st_make_valid() |>
  mutate(
    area_m2 = as.numeric(set_units(st_area(geom), "m^2")),
    area_ha = area_m2 / 10000,
    pct_talhao = (area_ha / talhao_ha) * 100
  ) |>
  st_drop_geometry() |>
  arrange(match(classe, rotulos))

# totais úteis
totais <- tibble(
  classe = c("TOTAL_CLASSIFICADO","TOTAL_PLANTAS"),
  area_m2 = c(
    sum(resumo$area_m2),
    sum(resumo$area_m2[resumo$classe %in% c("Doentes","Saudaveis", "Mortas")])
  )
) |>
  mutate(
    area_ha = area_m2 / 10000,
    pct_talhao = (area_ha / talhao_ha) * 100
  )


# tabela final
tabela_final <- bind_rows(resumo, totais)

# --------------------
# SAÍDA
# --------------------
print(tabela_final, n = Inf)
write_csv(tabela_final, "D:/classificacao/quantificacao_areas_por_classe.csv")
