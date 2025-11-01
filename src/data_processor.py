import pandas as pd
import numpy as np
import re
import os

input_file = '/home/brunatereza/cafe-ibge-2024/data/raw/Tabela 1613.xlsx'
output_file = '/home/brunatereza/cafe-ibge-2024/data/processed/tabela_1613_municipios.csv'

df = pd.read_excel(input_file)
df = df.replace('-', np.nan)
df = df[~(df.iloc[:, 1:] == '...').all(axis=1)]

def split_municipio_uf(x):
    if pd.isna(x):
        return pd.Series([np.nan, np.nan])
    match = re.search(r'\((\w{2})\)$', x.strip())
    if match:
        uf = match.group(1)
        municipio = re.sub(r'\s*\(\w{2}\)$', '', x.strip())
        return pd.Series([municipio, uf])
    else:
        return pd.Series([x.strip(), np.nan])

df[['Município', 'UF']] = df.iloc[:, 0].apply(split_municipio_uf)
cols = ['Município', 'UF'] + [c for c in df.columns if c not in ['Município', 'UF', df.columns[0]]]
df = df[cols]

for col in df.columns[2:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

numeric_cols = df.columns[2:]
df = df.dropna(subset=numeric_cols, how='all')
df = df[~(df[numeric_cols].fillna(0) == 0).all(axis=1)]

os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)