# WACC y Ke 2020–2025: SQM, CAP, Molymet, Enaex y Minera Valparaíso

Tasas de descuento por empresa y año para la tesina *"Las opciones reales como componente del valor bursátil"*. El resultado está en **`WACC_2020_2025.xlsx`** (hoja `Resumen`). Todas las tasas están en USD, porque las cinco empresas reportan en dólares.

## Fórmulas

| Componente | Cálculo | Fuente |
|---|---|---|
| Rf | Rendimiento del T-Bond de EE.UU. a 10 años al cierre del año | Damodaran, `histimpl.xls` |
| ERP | Prima por riesgo de mercado implícita (FCFE) al cierre del año | Damodaran, `histimpl.xls` |
| CRP | Riesgo país de Chile, basado en su rating de Moody's | Damodaran, `ctryprem` de cada año |
| βU | Beta desapalancado de la industria, mercados emergentes | Damodaran, `betaemerg` de cada año |
| βL | βU × (1 + (1 − t) × D/E) (Hamada) | — |
| **Ke** | Rf + βL × ERP + CRP | — |
| Kd | Costos financieros ÷ deuda financiera promedio (inicio + fin) / 2 | Estados financieros |
| t | 27%, tasa legal en Chile | — |
| **WACC** | E/(D+E) × Ke + D/(D+E) × Kd × (1 − t) | — |

- **D (deuda):** préstamos bancarios y bonos consolidados, a valor libro. No incluye derivados ni arrendamientos NIIF 16.
- **E (patrimonio):** capitalización bursátil al cierre (acciones en circulación × precio, convertido con el dólar observado) más las participaciones no controladoras a valor libro. La deuda es consolidada, así que el patrimonio también tiene que serlo.

Los archivos de Damodaran de cada año se publican el 1 de enero siguiente, así que reflejan el cierre del año. Como control, la ERP madura de cada `ctryprem` coincide con la `histimpl` de ese año.

## Industria usada para el beta

| Empresa | Base | Alternativa (sensibilidad) |
|---|---|---|
| SQM | Chemical (Specialty): litio, yodo, nutrientes | Metals & Mining |
| CAP | Steel: hierro y acero | Metals & Mining |
| Molymet | Metals & Mining: procesamiento de molibdeno | Steel |
| Enaex | Chemical (Basic): nitrato de amonio y explosivos | Chemical (Specialty) |
| Minera Valparaíso | Power: consolida Colbún, casi todos sus ingresos son de energía | Investments & Asset Management |

Se usa el beta por industria y no la regresión de cada acción porque algunas transan poco. Por ejemplo, Molymet tuvo 30 semanas sin transacciones en el período. Además, el beta por industria se calcula igual para las cinco empresas.

## Advertencias para la tesina

1. **Con V = capitalización bursátil, la tasa consistente para AiP es Ke, no el WACC.** El flujo también debe ser del accionista. Varias de estas empresas clasifican los intereses pagados en financiamiento, así que su flujo operacional va antes de intereses. Para que flujo y tasa calcen, resten los intereses pagados (están en los JSON) o usen el WACC con V = empresa completa.
2. **Kd de 2020 usa solo la deuda de cierre**, porque no hay balance 2019 en el repositorio. En CAP eso da un Kd alto (12%).
3. **Minera Valparaíso es un holding:** consolida Colbún con 48% de propiedad. Si Colbún entra en la muestra, la estaría contando dos veces.
4. **CAP 2024–2025:** la siderúrgica Huachipato quedó como operación discontinuada, así que esos años no son comparables con los anteriores.
5. **SQM 2025:** la asociación con Codelco sube las no controladoras a USD 2.363 millones.
6. **SQM 2024:** la tasa efectiva de impuesto es 141% por el impuesto específico al litio. No afecta el cálculo, porque se usa el 27% legal.

## Reproducir

```sh
python3 scripts/mercado.py          # precios (Yahoo Finance), dólar (mindicador.cl) y valores de Damodaran
python3 scripts/calcular_wacc.py    # escribe data/wacc.json e imprime la tabla
node scripts/excel.mjs .            # arma el Excel con fórmulas (requiere npm install exceljs)
node scripts/verificar_excel.cjs WACC_2020_2025.xlsx   # recalcula las fórmulas con otro motor (xlsx, hyperformula)
```

`data/<empresa>.json` tiene cada cifra contable con su archivo, la página del PDF y la línea exacta leída.
