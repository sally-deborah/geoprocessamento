# ================================================================
# Script: convert_dms_to_utm.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Converte coordenadas em graus, minutos e segundos (DMS)
#            para graus decimais (latitude/longitude) e coordenadas UTM.
#            Detecta automaticamente separador e encoding do CSV.
#            Gera dois arquivos: um em coordenadas geográficas (para KML)
#            e outro em coordenadas UTM.
# Linguagem: Python
# Dependências: pandas, pyproj, re, chardet
# Data: 2025-10-25
# ================================================================

import pandas as pd
import re
import os
import chardet
from pyproj import Transformer, CRS

# --------------------
# 1. LEITURA ROBUSTA DO ARQUIVO
# --------------------
file_path = input("Informe o caminho completo do arquivo CSV: ").strip()
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

# Detecta encoding automaticamente
with open(file_path, 'rb') as f:
    raw_data = f.read(4096)
encoding_detected = chardet.detect(raw_data)['encoding'] or 'utf-8-sig'

# Detecta separador provável
with open(file_path, 'r', encoding=encoding_detected, errors='ignore') as f:
    first_line = f.readline()
sep = ';' if first_line.count(';') > first_line.count(',') else ','

print(f"→ Encoding detectado: {encoding_detected}")
print(f"→ Separador detectado: '{sep}'")

# Lê o CSV
df = pd.read_csv(file_path, sep=sep, encoding=encoding_detected, quotechar='"')
df.columns = ['ponto', 'lat', 'long', 'alt', 'sigmaLat', 'sigmaLong', 'sigmaAlt']

# --------------------
# 2. NORMALIZAÇÃO DE SÍMBOLOS
# --------------------
def normalizar_dms(dms_str: str) -> str:
    """Normaliza símbolos de coordenadas DMS."""
    dms_str = dms_str.replace('º', '°').replace("''", '"').strip()
    if dms_str.endswith("'") and not dms_str.endswith('"'):
        dms_str = dms_str[:-1] + '"'
    return dms_str

df['lat'] = df['lat'].apply(normalizar_dms)
df['long'] = df['long'].apply(normalizar_dms)

# --------------------
# 3. CONVERSÃO DMS → GRAUS DECIMAIS
# --------------------
def dms_string_to_decimal(dms_str: str) -> float:
    """Converte string DMS (graus°min'seg") em graus decimais."""
    match = re.match(r"(-?\d+)°(\d+)'([\d\.]+)\"", dms_str)
    if not match:
        raise ValueError(f"Formato inválido: {dms_str}")
    d, m, s = map(float, match.groups())
    sign = -1 if d < 0 else 1
    return sign * (abs(d) + m / 60 + s / 3600)

df['latitude'] = df['lat'].apply(dms_string_to_decimal)
df['longitude'] = df['long'].apply(dms_string_to_decimal)

# --------------------
# 4. CONVERSÃO PARA UTM
# --------------------
utm_data = []
for lat, lon in zip(df['latitude'], df['longitude']):
    utm_zone = int((lon + 180) / 6) + 1
    hemisphere = 'north' if lat >= 0 else 'south'
    crs_utm = CRS.from_proj4(
        f"+proj=utm +zone={utm_zone} +{hemisphere} +datum=WGS84 +units=m +no_defs"
    )
    transformer = Transformer.from_crs("EPSG:4326", crs_utm, always_xy=True)
    easting, northing = transformer.transform(lon, lat)
    utm_data.append((utm_zone, hemisphere, easting, northing))

df[['utm_zone', 'utm_hemisphere', 'utm_easting', 'utm_northing']] = pd.DataFrame(utm_data)

# --------------------
# 5. EXPORTAÇÃO
# --------------------
output_dir = os.path.dirname(file_path)
csv_kml = os.path.join(output_dir, "coordenadas_para_kml.csv")
csv_utm = os.path.join(output_dir, "coordenadas_utm.csv")

df[['ponto', 'latitude', 'longitude', 'alt']].to_csv(csv_kml, index=False)
df[['ponto', 'utm_zone', 'utm_hemisphere', 'utm_easting', 'utm_northing', 'alt']].to_csv(csv_utm, index=False)

print("\nConversão concluída com sucesso!")
print(f"→ Arquivo KML salvo em: {csv_kml}")
print(f"→ Arquivo UTM salvo em: {csv_utm}")

