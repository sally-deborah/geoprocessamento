# ================================================================
# Script: reproject_shapefile_utm.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Reprojeta um shapefile de coordenadas geográficas (EPSG:4326)
#            para o sistema métrico UTM (EPSG:32721 - WGS 84 / UTM zone 21S).
# Linguagem: Python
# Dependência: geopandas
# Data: 2025-10-25
# ================================================================

import geopandas as gpd
from pathlib import Path

# --------------------
# ENTRADA
# --------------------
# caminho do shapefile original (em EPSG:4326)
shp_path = Path(r"D:\.shp")

# --------------------
# PROCESSAMENTO
# --------------------
gdf = gpd.read_file(shp_path)
gdf = gdf.to_crs("EPSG:32721")  # reprojeta para UTM 21S (sul do Brasil)

# --------------------
# SAÍDA
# --------------------
gdf.to_file(shp_path, driver="ESRI Shapefile")
print(f"Reprojeção concluída: {shp_path.name} → EPSG:32721")
