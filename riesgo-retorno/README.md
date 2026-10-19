# Riesgo y retorno: CMIG4 y OIBR4

Este análisis repite el de `BASE DE DATOS IPSA FINALIZADA.xlsx`, ahora con las dos acciones de `Base de Datos Riesgo-Retorno.xlsx`: CMIG4.SA (Cemig) y OIBR4.SA (Oi). Son precios mensuales en reales, de ene-2015 a ene-2023. El resultado está en **`Riesgo_Retorno_CMIG4_OIBR4.xlsx`**, con las fórmulas a la vista y un texto de interpretación en cada hoja.

| Hoja | Contenido (igual que en la base del IPSA) |
|---|---|
| `<acción> Mensual` | Retorno simple, retorno +1 y retorno ln; media, varianza y desviación estándar; paseo aleatorio de 36 meses |
| `<acción> Escenarios` | 5 escenarios de retornos simulados con NORM.INV(RAND(), media, SD) y su gráfico |
| `<acción> Anual` | Retornos anuales 2015–2022, retorno esperado, varianza, desviación estándar, error estándar e intervalo de confianza al 95% |
| `Comparación` | Resumen de las dos acciones y correlación de sus retornos mensuales (esta hoja es nueva) |

Igual que con el IPSA, el año 2015 entra con 11 retornos. El año 2023 queda fuera de las estadísticas anuales porque solo tiene enero.

| | CMIG4 | OIBR4 |
|---|---|---|
| Retorno mensual (simple / ln) | 1,17% / 0,42% | −0,38% / −2,36% |
| Desviación estándar mensual (simple) | 12,56% | 21,56% |
| Retorno anual (simple) | 11,40% | −5,38% |
| Desviación estándar anual (simple) | 42,44% | 69,74% |
| IC 95% del retorno anual (simple) | −18,01% a 40,81% | −53,71% a 42,95% |

Correlación mensual entre ambas: 0,46.

## Reproducir

```sh
python3 riesgo-retorno/scripts/armar_excel.py                       # arma el Excel (pandas, numpy, openpyxl)
python3 riesgo-retorno/scripts/esperados.py > esperados.json        # valores esperados calculados aparte
node riesgo-retorno/scripts/verificar_excel.cjs riesgo-retorno/Riesgo_Retorno_CMIG4_OIBR4.xlsx esperados.json   # npm install xlsx hyperformula
```
