# 🌎 Rotinas Automatizadas de Geoprocessamento  
Scripts em **R** e **Python** para tarefas de geoprocessamento, sensoriamento remoto e manipulação vetorial, desenvolvidos por **Eng. Florestal MSc. Sally Deborah P. da Silva**.

---

## 📂 Estrutura do Repositório
├── R/

├── calcula_areas_classes_shp.R

├── unifica_shapefiles.R

├── convert_dn_to_reflectance.R

├── recorte_raster_por_shapefile.R

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

---

## ⚙️ Requisitos

### 🧮 R
- **Versão:** R ≥ 4.2  
- **Principais pacotes:**  
  `sf`, `terra`, `dplyr`, `readr`, `writexl`

### 🧮 Python
- **Versão:** Python ≥ 3.10  
- **Principais bibliotecas:**  
  `geopandas`, `rasterio`, `numpy`, `pandas`, `fiona`, `shapely`, `openpyxl`

---

## 📜 Scripts em R

### 🔹 `calcula_areas_classes_shp.R`
Calcula área (m², ha) e porcentagem por classe temática (ex.: espécies de plantas, ou classes de saúde).  
**Entrada:** shapefiles e área total (ha).  
**Saída:** CSV com áreas e percentuais.

---

### 🔹 `unifica_shapefiles.R`
Une múltiplos arquivos `.shp` em um único shapefile.  
**Entrada:** pasta contendo arquivos `.shp`.  
**Saída:** shapefile unificado (`unificado.shp`).

---

### 🔹 `convert_dn_to_reflectance.R`
Converte imagens `.tif` com valores digitais (DN) em **reflectância normalizada (0–1)**.  
**Entrada:** imagens multiespectrais `.tif`.  
**Saída:** imagens convertidas com sufixo `_ref.tif`.

---

### 🔹 `recorte_raster_por_shapefile.R`
Realiza o **recorte automático de rasters (.tif)** utilizando um shapefile como limite da área de interesse.  
Inclui reprojeção automática para coincidir com o CRS do shapefile.  
**Fluxo:**
1. Carrega o shapefile e extrai o CRS de referência;  
2. Percorre todos os `.tif` do diretório especificado;  
3. Reprojeta e recorta cada raster com base no polígono vetorial;  
4. Salva arquivos recortados com sufixo `_recorte.tif`.

**Entrada:**  
- Pasta contendo rasters (`.tif`);  
- Shapefile da área de interesse (`.shp`).  

**Saída:**  
- Arquivos recortados em `/results/recortes/`.

---

## 🐍 Scripts em Python

### 🔹 `reproject_shapefile_utm.py`
Reprojeta shapefiles de coordenadas geográficas (ex.: EPSG:4326) para coordenadas métricas (ex.: EPSG:32721 – UTM 21S).  
**Saída:** shapefile reprojetado.

---

### 🔹 `zonal_statistics_batch.py`
Executa o cálculo automatizado de **estatísticas zonais** (mínimo, máximo, média e mediana) entre múltiplos shapefiles e rasters.  
**Saída:** planilha `.xlsx` com resultados por feição.

---

### 🔹 `get_file_crs.py`
Obtém o sistema de referência de coordenadas (CRS) de arquivos `.shp` e `.tif`.  
Útil para inspeção e padronização de sistemas de projeção.

---

### 🔹 `generate_composite_samples.py`
Gera **amostras compostas** a partir de dados tabulares contendo classes e preditores.  
**Entrada:** CSV com colunas `classe`, preditoras e medidas.  
**Saída:** `amostras_compostas_wide.csv`.

---

### 🔹 `convert_dms_to_utm.py`
Converte coordenadas em **graus, minutos e segundos (DMS)** para:  
- Graus decimais  
- Coordenadas UTM (zona, hemisfério, easting, northing)  
**Saída:**  
- `coordenadas_para_kml.csv`  
- `coordenadas_utm.csv`

---

### 🔹 `convert_kml_shp_auto.py`
Converte automaticamente:  
- Todos os arquivos **KML → SHP**  
- Todos os arquivos **SHP → KML**  
Cria pastas `kmls/` e `shapefiles/` e compacta os resultados em `.zip`.

---

### 🔹 `generate_kml_points.py`
Gera arquivos **KML individuais** para cada ponto em um CSV (latitude, longitude, altitude).  
Inclui log detalhado (`generate_kml_points.log`) e compacta todos em `kml_individuais.zip`.

---

### 🔹 `merge_shapefiles.py`
Une múltiplos shapefiles em um único arquivo vetorial, adicionando campo `source_file` com o nome de origem.  
**Saída:** `shapefile_unificado.shp` e `.zip`.

---

### 🔹 `filter_and_export_features.py`
Filtra feições específicas de um shapefile e:  
- Cria um shapefile único (`feicoes_filtradas.shp`);  
- Exporta shapefiles individuais para cada valor filtrado.

---

## 📤 Estrutura de Saída

Os resultados são salvos automaticamente nas pastas dentro de `/results/`, conforme o tipo de processamento:
- `areas_classes/` → estatísticas de área e classes  
- `recortes/` → rasters recortados  
- `estatisticas_zonais/` → planilhas com valores médios, máximos e mínimos  
- `composições/` → arquivos CSV de amostras compostas  

---
## 🧾 Licença

Distribuído sob a **MIT License**.  
Livre para uso, modificação e redistribuição

> Silva, S.D.P. (2025). *Rotinas Automatizadas de Geoprocessamento em R e Python*.  
> PPGEF – Universidade Federal de Santa Maria (UFSM)

---



