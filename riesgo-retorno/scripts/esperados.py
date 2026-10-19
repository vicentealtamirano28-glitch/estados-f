"""Calcula con pandas, sin leer las fórmulas, los valores que deben dar las celdas deterministas del Excel.
Uso: python3 riesgo-retorno/scripts/esperados.py > /tmp/esperados.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
precios = pd.read_excel(RAIZ / "Base de Datos Riesgo-Retorno.xlsx", sheet_name="PRECIOS").set_index("Date")
out = {}
ret = {}
for ticker, corto in (("CMIG4.SA", "CMIG4"), ("OIBR4.SA", "OIBR4")):
    p = precios[ticker].astype(float)
    s, l = p.pct_change().dropna(), np.log(p / p.shift()).dropna()
    ret[corto] = s
    m = f"{corto} Mensual"
    for i, (vs, vl) in enumerate(zip(s, l)):
        out[f"{m}!C{5 + i}"], out[f"{m}!D{5 + i}"], out[f"{m}!E{5 + i}"] = vs, vs + 1, vl
    for col, x in (("H", s), ("I", l)):
        out[f"{m}!{col}3"], out[f"{m}!{col}4"], out[f"{m}!{col}5"] = x.mean(), x.var(), x.std()
    a_s = (1 + s).groupby(s.index.year).prod() - 1
    a_l = l.groupby(l.index.year).sum()
    an = f"{corto} Anual"
    for i, y in enumerate(a_s.index):
        out[f"{an}!C{3 + i}"], out[f"{an}!D{3 + i}"] = a_s[y], a_l[y]
    base = 3 + len(a_s) + 1
    for col, x in (("C", a_s.iloc[:-1]), ("D", a_l.iloc[:-1])):  # 2023 (solo enero) excluido
        se = x.std() / np.sqrt(len(x))
        out[f"{an}!{col}{base}"], out[f"{an}!{col}{base + 1}"] = x.mean(), x.var()
        out[f"{an}!{col}{base + 2}"], out[f"{an}!{col}{base + 4}"] = x.std(), se
        out[f"{an}!{col}{base + 6}"], out[f"{an}!{col}{base + 7}"] = x.mean() + 1.96 * se, x.mean() - 1.96 * se
for col, corto in (("B", "CMIG4"), ("C", "OIBR4")):
    for r, ref in zip(range(4, 12), ["Mensual!H3", "Mensual!H5", "Mensual!I3", "Mensual!I5",
                                       "Anual!C13", "Anual!C15", "Anual!D13", "Anual!D15"]):
        hoja, celda = ref.split("!")
        out[f"Comparación!{col}{r}"] = out[f"{corto} {hoja}!{celda}"]
out["Comparación!B12"] = float(np.corrcoef(ret["CMIG4"], ret["OIBR4"])[0, 1])
print(json.dumps({k: float(v) for k, v in out.items()}, indent=1))
