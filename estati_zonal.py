# ================================================================
# Script: zonal_statistics_batch.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Executa cálculo automatizado de estatísticas zonais (min, max,
#            média e mediana) entre múltiplos shapefiles e rasters (.tif),
#            salvando os resultados em planilha Excel.
# Linguagem: Python
# Dependências: geopandas, rasterio, rasterstats, numpy, pandas, tqdm
# Data: 2025-10-25
# ================================================================

import os
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats
import geopandas as gpd
from tqdm import tqdm

# --------------------
# CONFIGURAÇÃO DE DIRETÓRIOS
# --------------------
shp_folder = r"D:\shps"
tif_folder = r"D:\camadas_raster"

# --------------------
# LISTAGEM DE ARQUIVOS
# --------------------
shp_files = [f for f in os.listdir(shp_folder) if f.endswith('.shp')]
tif_files = [f for f in os.listdir(tif_folder) if f.endswith('.tif')]

# --------------------
# DATAFRAME PRINCIPAL
# --------------------
results_df = pd.DataFrame()

# --------------------
# LOOP PRINCIPAL: PROCESSA TODOS OS SHAPEFILES E RASTERS
# --------------------
for shp_file in tqdm(shp_files, desc="Processando Shapefiles"):
    shp_path = os.path.join(shp_folder, shp_file)
    gdf = gpd.read_file(shp_path)

    for tif_file in tqdm(tif_files, desc=f"Processando Rasters para {shp_file}", leave=False):
        tif_path = os.path.join(tif_folder, tif_file)

        # Estatísticas zonais: média, mediana, mínimo, máximo
        stats = zonal_stats(shp_path, tif_path, stats=['mean', 'median', 'min', 'max'])

        # Cria DataFrame temporário
        temp_df = pd.DataFrame(stats)
        temp_df['shapefile'] = shp_file
        temp_df['raster'] = tif_file
        temp_df['polygon_id'] = range(1, len(temp_df) + 1)

        # Concatena resultados
        results_df = pd.concat([results_df, temp_df], ignore_index=True)

# --------------------
# ORGANIZAÇÃO E SAÍDA
# --------------------
cols = ['shapefile', 'raster', 'polygon_id', 'min', 'max', 'mean', 'median']
results_df = results_df[cols]

# Caminho de saída
output_path = os.path.join(os.path.dirname(shp_folder), 'estatisticas_zonais.xlsx')
results_df.to_excel(output_path, index=False)

print(f"Processo concluído! Resultados salvos em: {output_path}")
