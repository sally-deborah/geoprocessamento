# ================================================================
# Script: convert_kml_shp_auto.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Converte automaticamente todos os arquivos KML → SHP
#            e SHP → KML, conforme os formatos encontrados em uma pasta.
# Linguagem: Python
# Dependências: geopandas, fiona, gdal (ogr2ogr no PATH)
# Data: 2025-10-25
# ================================================================

import os
import glob
import shutil
import subprocess
import geopandas as gpd

# ================================================================
# CONFIGURAÇÕES
# ================================================================
# Caminho base (edite conforme seu ambiente)
base_folder = r"D:\dados\geometrias"
os.makedirs(base_folder, exist_ok=True)

# Subpastas automáticas
kml_folder = os.path.join(base_folder, "kmls")
shp_folder = os.path.join(base_folder, "shapefiles")
os.makedirs(kml_folder, exist_ok=True)
os.makedirs(shp_folder, exist_ok=True)

# ================================================================
# FUNÇÃO AUXILIAR: ZIPAR PASTA
# ================================================================
def zip_folder(folder_path: str, zip_name: str):
    if os.listdir(folder_path):
        zip_path = os.path.join(os.path.dirname(folder_path), zip_name)
        shutil.make_archive(zip_path.replace(".zip", ""), "zip", folder_path)
        print(f"📦 Pasta '{folder_path}' compactada em: {zip_path}")
    else:
        print(f"⚠️ Nenhum arquivo para compactar em: {folder_path}")

# ================================================================
# 1. CONVERTER KML → SHP
# ================================================================
kml_files = glob.glob(os.path.join(base_folder, "*.kml"))

if kml_files:
    print(f"\n📁 Encontrados {len(kml_files)} arquivos KML. Convertendo para SHP...\n")
    for kml_path in kml_files:
        base_name = os.path.splitext(os.path.basename(kml_path))[0]
        gdf = gpd.read_file(kml_path, driver="KML")
        gdf["Name"] = base_name
        out_shp = os.path.join(shp_folder, f"{base_name}.shp")
        gdf.to_file(out_shp, driver="ESRI Shapefile")
        print(f"✅ {base_name}.kml → {base_name}.shp")
    zip_folder(shp_folder, "shapefiles_convertidos.zip")
else:
    print("Nenhum arquivo .kml encontrado para conversão.")

# ================================================================
# 2. CONVERTER SHP → KML
# ================================================================
shp_files = glob.glob(os.path.join(base_folder, "*.shp"))

if shp_files:
    print(f"\n📁 Encontrados {len(shp_files)} arquivos SHP. Convertendo para KML...\n")
    for shp_path in shp_files:
        base_name = os.path.splitext(os.path.basename(shp_path))[0]
        out_kml = os.path.join(kml_folder, f"{base_name}.kml")

        subprocess.run(
            ["ogr2ogr", "-f", "KML", out_kml, shp_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"✅ {base_name}.shp → {base_name}.kml")
    zip_folder(kml_folder, "kml_convertidos.zip")
else:
    print("Nenhum arquivo .shp encontrado para conversão.")

# ================================================================
# RESUMO FINAL
# ================================================================
print("\n🚀 Conversões concluídas.")
print(f"→ KMLs convertidos: {kml_folder}")
print(f"→ SHPs convertidos: {shp_folder}")
