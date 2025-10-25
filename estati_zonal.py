import os
import numpy as np
import pandas as pd
import rasterio
from rasterstats import zonal_stats
import geopandas as gpd
from tqdm import tqdm

# Configuração dos diretórios
shp_folder = r"D:\01-TESE\03-Capitulo_IV\09-ortomosaicos\07-camadas_raster_120m\shps"
tif_folder = r"D:\01-TESE\03-Capitulo_IV\09-ortomosaicos\07-camadas_raster_120m"

# Lista todos os arquivos shapefile e raster
shp_files = [f for f in os.listdir(shp_folder) if f.endswith('.shp')]
tif_files = [f for f in os.listdir(tif_folder) if f.endswith('.tif')]

# DataFrame para armazenar todos os resultados
results_df = pd.DataFrame()

# Processa cada shapefile
for shp_file in tqdm(shp_files, desc="Processando Shapefiles"):
    shp_path = os.path.join(shp_folder, shp_file)
    gdf = gpd.read_file(shp_path)

    # Processa cada raster para o shapefile atual
    for tif_file in tqdm(tif_files, desc=f"Processando Rasters para {shp_file}", leave=False):
        tif_path = os.path.join(tif_folder, tif_file)

        # Extrai estatísticas zonais para cada polígono
        stats = zonal_stats(shp_path, tif_path, stats=['mean', 'median', 'min', 'max'])

        # Cria DataFrame temporário com os resultados
        temp_df = pd.DataFrame(stats)
        temp_df['shapefile'] = shp_file
        temp_df['raster'] = tif_file
        temp_df['polygon_id'] = range(1, len(temp_df) + 1)  # ID para cada polígono

        # Concatena com o DataFrame principal
        results_df = pd.concat([results_df, temp_df], ignore_index=True)

# Reorganiza as colunas
cols = ['shapefile', 'raster', 'polygon_id', 'min', 'max', 'mean', 'median']
results_df = results_df[cols]

# Salva os resultados em Excel
output_path = os.path.join(os.path.dirname(shp_folder), 'estatisticas_zonais_IVs.xlsx')
results_df.to_excel(output_path, index=False)

print(f"Processo concluído! Resultados salvos em: {output_path}")