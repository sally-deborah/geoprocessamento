# ================================================================
# Script: filter_and_export_features.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Filtra feições específicas de um shapefile e exporta
#            tanto um shapefile único contendo todas as feições
#            desejadas quanto shapefiles individuais por feição.
# Linguagem: Python
# Dependências: geopandas, os
# Data: 2025-10-25
# ================================================================

import geopandas as gpd
import os

# ================================================================
# 1. ENTRADAS DO USUÁRIO
# ================================================================
shapefile_path = input("Informe o caminho completo do shapefile: ").strip()
if not os.path.isfile(shapefile_path):
    raise FileNotFoundError(f"Shapefile não encontrado: {shapefile_path}")

# Lista de valores do campo desejado
valores_desejados = ['011M']

# Campo de identificação (altere conforme seu shapefile)
campo = 'CD_TALHAO'

# Pasta de saída
output_folder = os.path.join(os.path.dirname(shapefile_path), "filtrados")
os.makedirs(output_folder, exist_ok=True)

# ================================================================
# 2. LEITURA E FILTRAGEM
# ================================================================
print(f"\n📂 Lendo shapefile: {shapefile_path}")
gdf = gpd.read_file(shapefile_path)
if campo not in gdf.columns:
    raise ValueError(f"O campo '{campo}' não existe no shapefile. Colunas disponíveis: {list(gdf.columns)}")

# Filtra as feições desejadas
filtro = gdf[gdf[campo].isin(valores_desejados)]
if filtro.empty:
    raise ValueError("Nenhuma feição encontrada com os valores informados.")

# ================================================================
# 3. EXPORTA SHAPEFILE ÚNICO COM TODAS AS FEIÇÕES FILTRADAS
# ================================================================
output_path = os.path.join(output_folder, "feicoes_filtradas.shp")
filtro.to_file(output_path)
print(f"✅ Shapefile com feições filtradas salvo em: {output_path}")

# ================================================================
# 4. EXPORTA SHAPEFILES INDIVIDUAIS
# ================================================================
print("\n📤 Exportando shapefiles individuais...")

for valor in valores_desejados:
    filtro_valor = gdf[gdf[campo] == valor]
    if not filtro_valor.empty:
        nome_arquivo = f"{valor}.shp"
        out_path = os.path.join(output_folder, nome_arquivo)
        filtro_valor.to_file(out_path)
        print(f"✅ {nome_arquivo} exportado")
    else:
        print(f"⚠️ Valor '{valor}' não encontrado no campo '{campo}'.")

print(f"\n🚀 Exportação concluída. Arquivos salvos em: {output_folder}")
