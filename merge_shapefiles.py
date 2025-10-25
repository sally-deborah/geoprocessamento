# ================================================================
# Script: merge_shapefiles.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Une múltiplos shapefiles (.shp) em um único arquivo vetorial.
#            Adiciona coluna "source_file" indicando a origem de cada feição.
# Linguagem: Python
# Dependências: geopandas, pandas, shutil, glob, os
# Data: 2025-10-25
# ================================================================

import geopandas as gpd
import pandas as pd
import os
import shutil
import glob

# --------------------
# 1. CONFIGURAÇÃO DE PASTAS
# --------------------
input_dir = input("Informe o caminho da pasta com os shapefiles: ").strip()
if not os.path.isdir(input_dir):
    raise NotADirectoryError(f"Pasta não encontrada: {input_dir}")

output_dir = os.path.join(input_dir, "shapefile_unificado")
os.makedirs(output_dir, exist_ok=True)

# --------------------
# 2. LEITURA E UNIÃO
# --------------------
shapefiles = glob.glob(os.path.join(input_dir, "*.shp"))
if not shapefiles:
    raise FileNotFoundError("Nenhum arquivo .shp encontrado na pasta informada.")

print(f"\n📁 {len(shapefiles)} shapefiles encontrados. Unificando...\n")

gdfs = []
for shp_path in shapefiles:
    gdf = gpd.read_file(shp_path)
    gdf["source_file"] = os.path.basename(shp_path)
    gdfs.append(gdf)

# Garante mesmo CRS
crs_ref = gdfs[0].crs
for gdf in gdfs:
    if gdf.crs != crs_ref:
        gdf.to_crs(crs_ref, inplace=True)

merged = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs=crs_ref)

# --------------------
# 3. SALVAMENTO E COMPACTAÇÃO
# --------------------
out_path = os.path.join(output_dir, "shapefile_unificado.shp")
merged.to_file(out_path)
print(f"✅ Shapefile unificado salvo em: {out_path}")

# Compacta a pasta
zip_path = os.path.join(input_dir, "shapefile_unificado.zip")
shutil.make_archive(zip_path.replace(".zip", ""), "zip", output_dir)
print(f"📦 Arquivo compactado salvo em: {zip_path}")

print("\n🚀 Processo concluído com sucesso.")
