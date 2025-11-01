import pandas as pd
from pathlib import Path

input_path = Path("data/processed/ibge_cafe_2024_processed.csv")
output_path = Path("data/processed/data_audit_report.csv")

df = pd.read_csv(input_path)

expected_cols = ["Município", "UF"]
numeric_cols = [c for c in df.columns if c not in expected_cols]

missing_cols = [c for c in expected_cols if c not in df.columns]
if missing_cols:
    raise ValueError(f"Colunas ausentes: {missing_cols}")

df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

total_rows = len(df)
null_rows = df[numeric_cols].isnull().any(axis=1).sum()
zero_rows = (df[numeric_cols].sum(axis=1) == 0).sum()
complete_rows = total_rows - (null_rows + zero_rows)
completude = round(complete_rows / total_rows * 100, 2)

audit = pd.DataFrame(
    [{
        "Total de linhas": total_rows,
        "Linhas com valores nulos": null_rows,
        "Linhas zeradas": zero_rows,
        "Completude (%)": completude
    }]
)

audit.to_csv(output_path, index=False)
