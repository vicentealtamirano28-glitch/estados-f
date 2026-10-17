#!/usr/bin/env python3
"""Calcula Ke y WACC por empresa y año (2020-2025) y escribe data/wacc.json.

Ke (USD)  = Rf + beta_L * ERP + CRP_Chile            (CAPM con riesgo país aditivo, Damodaran)
beta_L    = beta_U * (1 + (1 - t) * D / E)           (Hamada)
Kd bruto  = costos financieros / deuda financiera promedio (inicio + fin) / 2
WACC      = E/(D+E) * Ke + D/(D+E) * Kd * (1 - t)

D = préstamos bancarios + bonos (sin derivados ni arrendamientos NIIF 16), valor libro consolidado.
E = capitalización bursátil al cierre + participaciones no controladoras a valor libro
    (la deuda es consolidada, así que el patrimonio también debe serlo).
t = 27% (tasa legal Chile). Todas las empresas reportan en USD, así que Ke y WACC quedan en USD.
"""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
ANIOS = [str(a) for a in range(2020, 2026)]
T = 0.27
EMPRESAS = {
    "sqm": {"nombre": "SQM", "precio": ["sqm_a", "sqm_b"], "industria": "Chemical (Specialty)",
            "industria_alt": "Metals & Mining"},
    "cap": {"nombre": "CAP", "precio": ["cap"], "industria": "Steel", "industria_alt": "Metals & Mining"},
    "molymet": {"nombre": "Molymet", "precio": ["molymet"], "industria": "Metals & Mining",
                "industria_alt": "Steel"},
    "enaex": {"nombre": "Enaex", "precio": ["enaex"], "industria": "Chemical (Basic)",
              "industria_alt": "Chemical (Specialty)"},
    "minera_valparaiso": {"nombre": "Minera Valparaíso", "precio": ["minera_valparaiso"], "industria": "Power",
                          "industria_alt": "Investments & Asset Management"},
}


def val(campo):
    return campo["valor"] if isinstance(campo, dict) and "valor" in campo else campo


def acciones(y, series):
    a = y["acciones_emitidas"]
    if len(series) == 2:
        return [val(a["en_circulacion_serie_A"]), val(a["en_circulacion_serie_B"])]
    if isinstance(a, dict) and "valor" in a:
        return [a["valor"]]
    vals = [val(v) for v in a.values() if isinstance(val(v), (int, float))]
    return [vals[0]]


def main():
    mercado = json.loads((DATA / "mercado.json").read_text(encoding="utf-8"))
    dam = mercado["damodaran"]
    filas = []
    for clave, cfg in EMPRESAS.items():
        raw = json.loads((DATA / f"{clave}.json").read_text(encoding="utf-8"))
        anios = raw.get("anios") or raw.get("anos")
        deuda_prev = None
        for a in ANIOS:
            y = anios[a]
            D = val(y["prestamos_que_devengan_intereses_total"])
            nci = val(y["patrimonio_total"]) - val(y["patrimonio_atribuible_controladora"])
            fx = mercado["dolar_observado"][a]["clp_por_usd"]
            n = acciones(y, cfg["precio"])
            precios = [mercado["precios"][p]["cierres"][a]["precio_clp"] for p in cfg["precio"]]
            mcap = sum(q * p for q, p in zip(n, precios)) / fx / 1000
            E = mcap + nci
            d_prom = D if deuda_prev is None else (D + deuda_prev) / 2
            kd = val(y["costos_financieros"]) / d_prom
            rf = dam["rf_tbond_10y"]["valores"][a]
            erp = dam["erp_implicita"]["valores"][a]
            crp = dam["crp_chile"]["valores"][a]
            res = {}
            for etiqueta, ind in (("base", cfg["industria"]), ("alt", cfg["industria_alt"])):
                bu = dam["beta_desapalancado_em"]["industrias"][ind][a]
                bl = bu * (1 + (1 - T) * D / E)
                ke = rf + bl * erp + crp
                wacc = E / (D + E) * ke + D / (D + E) * kd * (1 - T)
                res[etiqueta] = {"industria": ind, "beta_u": bu, "beta_l": bl, "ke": ke, "wacc": wacc}
            filas.append({
                "empresa": cfg["nombre"], "anio": int(a), "deuda": D, "deuda_promedio": d_prom,
                "deuda_promedio_nota": "solo saldo 2020 (no hay balance 2019)" if deuda_prev is None else "",
                "acciones": n, "precios_clp": precios, "dolar": fx, "market_cap": mcap, "nci_libro": nci,
                "E": E, "wd": D / (D + E), "we": E / (D + E), "d_e": D / E,
                "costos_financieros": val(y["costos_financieros"]), "kd_bruto": kd, "kd_neto": kd * (1 - T),
                "tasa_efectiva": val(y["gasto_impuesto_ganancias"]) / val(y["ganancia_antes_impuestos"])
                if val(y["ganancia_antes_impuestos"]) > 0 else None,
                "rf": rf, "erp": erp, "crp": crp, "base": res["base"], "alt": res["alt"],
                "flujo_operacion": val(y["flujo_operacion"]),
            })
            deuda_prev = D
    (DATA / "wacc.json").write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{'Empresa':18}{'Año':>5}{'MCap':>10}{'D':>10}{'D/E':>6}{'Kd':>7}{'βU':>6}{'βL':>6}"
          f"{'Ke':>7}{'WACC':>7}{'WACCalt':>8}")
    for f in filas:
        b = f["base"]
        print(f"{f['empresa']:18}{f['anio']:>5}{f['market_cap']:>10,.0f}{f['deuda']:>10,.0f}{f['d_e']:>6.2f}"
              f"{f['kd_bruto']:>7.2%}{b['beta_u']:>6.2f}{b['beta_l']:>6.2f}{b['ke']:>7.2%}{b['wacc']:>7.2%}"
              f"{f['alt']['wacc']:>8.2%}")


if __name__ == "__main__":
    main()
