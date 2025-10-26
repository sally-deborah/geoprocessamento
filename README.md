# 🌎 Rotinas Automatizadas de Geoprocessamento  
Scripts em **R** e **Python** para tarefas de geoprocessamento, sensoriamento remoto e manipulação vetorial, desenvolvidos por **Eng. Florestal MSc. Sally Deborah P. da Silva**.

---

## 📂 Estrutura do Repositório
├── R/

├── calcula_areas_classes_shp.R

├── unifica_shapefiles.R

├── convert_dn_to_reflectance.R

├── Python/

├── reproject_shapefile_utm.py

├── zonal_statistics_batch.py

├── get_file_crs.py

├── generate_composite_samples.py

├── convert_dms_to_utm.py 

├── convert_kml_shp_auto.py

├── generate_kml_points.py

├── merge_shapefiles.py

├── filter_and_export_features.py

---
## ⚙️ Requisitos
### 🧮 R
- R ≥ 4.2
### 🧮Python
- Python ≥ 3.10

📜 Scripts em R
🔹 calcula_areas_classes_shp.R

Calcula área (m², ha) e porcentagem por classe temática (ex.: espécies de plantas, ou classes de saúde).
Entrada: shapefiles e área total (ha).
Saída: CSV com áreas e percentuais.

🔹 unifica_shapefiles.R

Une múltiplos shapefiles .shp em um único arquivo vetorial.
Entrada: pasta com shapefiles.
Saída: shapefile unificado.

🔹 convert_dn_to_reflectance.R

Converte imagens .tif com valores digitais (DN) em reflectância normalizada (0–1).
Entrada: imagens TIFF.
Saída: imagens convertidas com sufixo _ref.tif.

🐍 Scripts em Python
🔹 reproject_shapefile_utm.py

Reprojeta shapefile de coordenadas geográficas (ex: EPSG:4326) para métrico (ex: EPSG:32721 – UTM 21S).
Entrada: shapefile.
Saída: mesmo arquivo reprojetado.

🔹 zonal_statistics_batch.py

Executa cálculo automatizado de estatísticas zonais (mínimo, máximo, média e mediana) entre múltiplos shapefiles e rasters.
Saída: planilha .xlsx com estatísticas.

🔹 get_file_crs.py

Obtém o sistema de referência de coordenadas (CRS) de arquivos .shp e .tif.

🔹 generate_composite_samples.py

Gera amostras compostas a partir de dados tabulares (classes e preditores).
Entrada: CSV com colunas classe, preditoras, median.
Saída: CSV amostras_compostas_wide.csv.

🔹 convert_dms_to_utm.py

Converte coordenadas em graus, minutos e segundos (DMS) para:

Graus decimais;

Coordenadas UTM (zona, hemisfério, easting, northing).
Detecta automaticamente encoding e separador.
Saída: dois arquivos CSV — coordenadas_para_kml.csv e coordenadas_utm.csv.

🔹 convert_kml_shp_auto.py

Converte automaticamente:

Todos os arquivos KML → SHP
Todos os arquivos SHP → KML
Cria pastas kmls/ e shapefiles/, e compacta resultados em .zip.

🔹 generate_kml_points.py

Gera arquivos KML individuais para cada ponto em um CSV (latitude, longitude e altitude).
Inclui log detalhado (generate_kml_points.log) e compacta todos em kml_individuais.zip.

🔹 merge_shapefiles.py

Une múltiplos shapefiles em um único arquivo vetorial, adicionando campo source_file com o nome de origem.
Saída: shapefile_unificado.shp e .zip.

🔹 filter_and_export_features.py

Filtra feições específicas de um shapefile e:

Cria um shapefile único (feicoes_filtradas.shp);

Exporta shapefiles individuais para cada valor filtrado.

🧾 Licença

Distribuído sob a MIT License.
Livre para uso, modificação e redistribuição com atribuição.




