# ================================================================
# Script: generate_composite_samples.py
# Autor: Eng. Florestal MSc. Sally Deborah P. da Silva
# Descrição: Gera amostras compostas a partir de dados tabulares contendo
#            classes e preditores, calculando médias por bloco e exportando
#            o resultado em formato wide (.csv).
# Linguagem: Python
# Dependências: pandas, numpy
# Data: 2025-10-25
# ================================================================

import pandas as pd
import numpy as np
import os

# --------------------
# 1. LEITURA DO ARQUIVO
# --------------------
file_path = input("Informe o caminho completo do arquivo CSV: ").strip()
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

df = pd.read_csv(file_path, sep=';', decimal='.')
df.columns = df.columns.str.strip()

print(f"Colunas detectadas: {df.columns.tolist()}")
print(df.head())

# --------------------
# 2. PARÂMETROS
# --------------------
n_amostras = 15  # número de amostras compostas desejadas por classe
amostras_por_preditor = {}

# --------------------
# 3. GERAÇÃO DAS AMOSTRAS COMPOSTAS
# --------------------
for classe in df['classe'].unique():
    for pred in df['preditoras'].unique():
        df_pred = (
            df[(df['classe'] == classe) & (df['preditoras'] == pred)]
            .sample(frac=1, random_state=42)
            .reset_index(drop=True)
        )
        splits = np.array_split(df_pred, n_amostras)
        for i, bloco in enumerate(splits):
            key = (classe, i + 1)
            if key not in amostras_por_preditor:
                amostras_por_preditor[key] = {'amostra_id': i + 1, 'classe': classe}
            amostras_por_preditor[key][pred] = bloco['median'].mean()

# --------------------
# 4. ORGANIZAÇÃO E EXPORTAÇÃO
# --------------------
amostras = list(amostras_por_preditor.values())
df_final = pd.DataFrame(amostras)

# organiza colunas
cols = ['amostra_id', 'classe'] + sorted(
    [c for c in df_final.columns if c not in ['amostra_id', 'classe']]
)
df_final = df_final[cols]

print("\nPrévia das amostras compostas:")
print(df_final.head(20))

# salva arquivo final
output_path = os.path.join(os.path.dirname(file_path), 'amostras_compostas_wide.csv')
df_final.to_csv(output_path, index=False)

print(f"\nProcesso concluído! Arquivo salvo em: {output_path}")
