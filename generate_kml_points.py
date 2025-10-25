# ================================================================
# Script: generate_kml_points.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Gera arquivos KML individuais para cada ponto a partir
#            de um CSV contendo coordenadas geográficas (graus decimais).
#            Cada ponto gera um arquivo .kml com nome e altitude.
#            Inclui registro automático de log (sucesso e erros).
# Linguagem: Python
# Dependências: pandas, pyproj, simplekml, chardet, os, shutil
# Data: 2025-10-25
# ================================================================

import pandas as pd
import os
import shutil
import chardet
import simplekml
from datetime import datetime
import traceback

# ================================================================
# FUNÇÃO AUXILIAR: LOG
# ================================================================
def log_message(log_file, message):
    """Escreve mensagem no log com timestamp."""
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# ================================================================
# 1. LEITURA DO CSV
# ================================================================
file_path = input("Informe o caminho completo do arquivo CSV: ").strip()
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

# Caminhos de saída e log
base_dir = os.path.dirname(file_path)
output_dir = os.path.join(base_dir, "kml_points")
os.makedirs(output_dir, exist_ok=True)
log_file = os.path.join(base_dir, "generate_kml_points.log")

log_message(log_file, "=== Início do processamento ===")
log_message(log_file, f"Arquivo de entrada: {file_path}")

# Detecta encoding automaticamente
with open(file_path, 'rb') as f:
    raw_data = f.read(4096)
encoding_detected = chardet.detect(raw_data)['encoding'] or 'utf-8-sig'

# Detecta separador provável
with open(file_path, 'r', encoding=encoding_detected, errors='ignore') as f:
    first_line = f.readline()
sep = ';' if first_line.count(';') > first_line.count(',') else ','

log_message(log_file, f"Encoding detectado: {encoding_detected}")
log_message(log_file, f"Separador detectado: '{sep}'")

# Lê o CSV
df = pd.read_csv(file_path, sep=sep, encoding=encoding_detected)
colunas_esperadas = {'ponto', 'latitude', 'longitude', 'alt'}
if not colunas_esperadas.issubset(set(df.columns)):
    raise ValueError(f"O arquivo deve conter as colunas: {colunas_esperadas}")

log_message(log_file, f"Colunas detectadas: {list(df.columns)}")

# ================================================================
# 2. GERAÇÃO DE KML INDIVIDUAL
# ================================================================
sucesso, falhas = 0, 0
log_message(log_file, f"Gerando KMLs na pasta: {output_dir}")

for _, row in df.iterrows():
    try:
        ponto = str(row['ponto']).strip()
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        alt = row.get('alt', None)

        kml = simplekml.Kml()
        desc = f"Altitude: {alt} m" if pd.notna(alt) else "Sem altitude informada"
        kml.newpoint(name=ponto, coords=[(lon, lat)], description=desc)

        file_path_out = os.path.join(output_dir, f"{ponto}.kml")
        kml.save(file_path_out)

        print(f"✅ {ponto}.kml criado")
        log_message(log_file, f"SUCESSO: {ponto}.kml")
        sucesso += 1

    except Exception as e:
        falhas += 1
        msg = f"ERRO em {row.get('ponto', 'sem_nome')}: {str(e)}"
        print(f"❌ {msg}")
        log_message(log_file, f"{msg}\n{traceback.format_exc()}")

# ================================================================
# 3. COMPACTAÇÃO
# ================================================================
zip_path = os.path.join(base_dir, "kml_individuais.zip")
shutil.make_archive(zip_path.replace(".zip", ""), "zip", output_dir)

log_message(log_file, f"Compactação concluída: {zip_path}")
log_message(log_file, f"KMLs gerados: {sucesso} | Falhas: {falhas}")
log_message(log_file, "=== Fim do processamento ===\n")

print(f"\n📦 Arquivos KML compactados em: {zip_path}")
print(f"🧾 Log detalhado salvo em: {log_file}")
print("🚀 Processo concluído.")
