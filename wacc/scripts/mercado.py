#!/usr/bin/env python3
"""Descarga los datos de mercado de cierre de cada año (2020-2025) y los guarda en data/mercado.json.

- Precios de cierre del último día hábil del año: Yahoo Finance (Bolsa de Santiago, CLP).
- Dólar observado del último día del año: mindicador.cl (Banco Central de Chile).
- Damodaran (Rf, ERP, riesgo país Chile, betas desapalancados de mercados emergentes):
  valores leídos de sus archivos y fijados en DAMODARAN, con la URL de cada archivo.
"""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ANIOS = range(2020, 2026)
TICKERS = {"SQM-A.SN": "sqm_a", "SQM-B.SN": "sqm_b", "CAP.SN": "cap", "MOLYMET.SN": "molymet",
           "ENAEX.SN": "enaex", "MINERA.SN": "minera_valparaiso"}
BASE = "https://pages.stern.nyu.edu/~adamodar/pc/"
DAMODARAN = {
    "rf_tbond_10y": {"fuente": BASE + "datasets/histimpl.xls", "columna": "T.Bond Rate (cierre de año)",
                     "valores": {2020: 0.0093, 2021: 0.0151, 2022: 0.0388, 2023: 0.0388, 2024: 0.0458, 2025: 0.0418}},
    "erp_implicita": {"fuente": BASE + "datasets/histimpl.xls", "columna": "Implied ERP (FCFE)",
                      "valores": {2020: 0.0472, 2021: 0.0424, 2022: 0.0594, 2023: 0.0460, 2024: 0.0433, 2025: 0.0423}},
    "crp_chile": {"columna": "Country Risk Premium (basado en rating Moody's), hoja 'ERPs by country'",
                  "fuentes": {2020: BASE + "archives/ctryprem20.xlsx", 2021: BASE + "archives/ctryprem21.xlsx",
                              2022: BASE + "archives/ctryprem22.xlsx", 2023: BASE + "archives/ctryprem23.xlsx",
                              2024: BASE + "archives/ctryprem24.xlsx", 2025: BASE + "datasets/ctryprem.xlsx"},
                  "rating": {2020: "A1", 2021: "A1", 2022: "A2", 2023: "A2", 2024: "A2", 2025: "A2"},
                  "valores": {2020: 0.006815, 2021: 0.006959, 2022: 0.014606, 2023: 0.012376, 2024: 0.011294,
                              2025: 0.010955}},
    "beta_desapalancado_em": {
        "columna": "Unlevered beta, hoja 'Industry Averages' (mercados emergentes)",
        "fuentes": {2020: BASE + "archives/betaemerg20.xls", 2021: BASE + "archives/betaemerg21.xls",
                    2022: BASE + "archives/betaemerg22.xls", 2023: BASE + "archives/betaemerg23.xls",
                    2024: BASE + "archives/betaemerg24.xls", 2025: BASE + "datasets/betaemerg.xls"},
        "industrias": {
            "Chemical (Basic)":       {2020: 0.8795, 2021: 0.9509, 2022: 0.9065, 2023: 0.8282, 2024: 0.8458, 2025: 0.9690},
            "Chemical (Specialty)":   {2020: 0.9764, 2021: 1.0241, 2022: 0.9395, 2023: 0.8626, 2024: 0.8835, 2025: 1.0271},
            "Metals & Mining":        {2020: 0.8530, 2021: 1.0761, 2022: 1.0408, 2023: 1.0022, 2024: 1.0918, 2025: 1.3013},
            "Steel":                  {2020: 0.8617, 2021: 0.9816, 2022: 0.9393, 2023: 0.9048, 2024: 0.8113, 2025: 0.8371},
            "Power":                  {2020: 0.4870, 2021: 0.5177, 2022: 0.4160, 2023: 0.4218, 2024: 0.4047, 2025: 0.4331},
            "Investments & Asset Management": {2020: 0.1883, 2021: 0.3532, 2022: 0.2756, 2023: 0.2790,
                                               2024: 0.2810, 2025: 0.3996},
        }},
    "nota_fechas": "Cada archivo anual de Damodaran se publica el 1 de enero siguiente (ej. ctryprem20 = 'Updated "
                   "January 1, 2021'), es decir, refleja el cierre del año. Verificado: la ERP madura de cada "
                   "ctryprem (Total ERP - CRP) coincide con la ERP implícita de histimpl para ese año.",
}


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=40))


def cierres_anuales(ticker):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
           f"?period1=1577836800&period2=1767312000&interval=1d")
    r = get_json(url)["chart"]["result"][0]
    out = {}
    for ts, close in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
        if close is None:
            continue
        d = datetime.fromtimestamp(ts, tz=timezone.utc)
        if d.year in ANIOS:
            out[d.year] = {"fecha": d.strftime("%Y-%m-%d"), "precio_clp": round(close, 2)}
    return url, out


def dolar_cierre(anio):
    url = f"https://mindicador.cl/api/dolar/{anio}"
    serie = get_json(url)["serie"]
    ultimo = max(serie, key=lambda x: x["fecha"])
    return url, {"fecha": ultimo["fecha"][:10], "clp_por_usd": ultimo["valor"]}


def main():
    precios = {}
    for ticker, clave in TICKERS.items():
        url, datos = cierres_anuales(ticker)
        precios[clave] = {"ticker": ticker, "fuente": url, "cierres": datos}
    dolar = {}
    for a in ANIOS:
        url, d = dolar_cierre(a)
        dolar[a] = {**d, "fuente": url}
    out = {"descargado": datetime.now(timezone.utc).strftime("%Y-%m-%d"), "precios": precios,
           "dolar_observado": dolar, "damodaran": DAMODARAN}
    path = Path(__file__).resolve().parent.parent / "data" / "mercado.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in precios.items():
        print(k, {a: c["precio_clp"] for a, c in v["cierres"].items()})
    print("dolar", {a: d["clp_por_usd"] for a, d in dolar.items()})


if __name__ == "__main__":
    main()
