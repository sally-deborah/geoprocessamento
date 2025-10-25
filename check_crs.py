# ================================================================
# Script: get_file_crs.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Funções utilitárias para leitura e extração do sistema
#            de referência de coordenadas (CRS) de arquivos shapefile (.shp)
#            e raster (.tif).
# Linguagem: Python
# Dependências: fiona, rasterio
# Data: 2025-10-25
# ================================================================

import os
import fiona
import rasterio
from rasterio.crs import CRS
from fiona.crs import from_epsg, from_string

# --------------------
# FUNÇÕES
# --------------------
def get_shapefile_crs(shapefile_path: str):
    """
    Obtém o CRS (Coordinate Reference System) de um arquivo shapefile (.shp).

    Parâmetros:
        shapefile_path (str): caminho completo do arquivo .shp

    Retorna:
        dict: dicionário com informações do CRS
    """
    with fiona.open(shapefile_path) as src:
        return src.crs


def get_raster_crs(raster_path: str):
    """
    Obtém o CRS (Coordinate Reference System) de um arquivo raster (.tif).

    Parâmetros:
        raster_path (str): caminho completo do arquivo .tif

    Retorna:
        rasterio.crs.CRS: objeto CRS do raster
    """
    with rasterio.open(raster_path) as src:
        return src.crs
