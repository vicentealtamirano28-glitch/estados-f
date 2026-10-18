import sys, random, math, datetime as dt
sys.path.insert(0, '/projects/sandbox/.libs/xlsxwriter')
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell as rc, xl_col_to_name as cn

OUT = '/projects/sandbox/Guia_CCI/03_Laboratorio_CCI.xlsx'
wb = xlsxwriter.Workbook(OUT, {'use_future_functions': True})


import re as _re
_orig_add_chart = wb.add_chart
def _q(v):
    return _re.sub(r"^=(\d\w*)!", r"='\1'!", v) if isinstance(v, str) else v
def _add_chart(opts):
    c = _orig_add_chart(opts)
    _orig = c.add_series
    def _add_series(o):
        o = dict(o)
        for k in ('name', 'categories', 'values'):
            if k in o: o[k] = _q(o[k])
        return _orig(o)
    c.add_series = _add_series
    return c
wb.add_chart = _add_chart

# ---------- formatos ----------
NAVY = '#1F3864'; BLUE = '#2E75B6'; LIGHT = '#DDEBF7'; YEL = '#FFF2CC'; GRN = '#E2EFDA'; RED = '#FCE4D6'
F = lambda **k: wb.add_format(k)
title = F(bold=True, font_size=16, font_color=NAVY)
sub = F(italic=True, font_color='#595959', text_wrap=True, valign='top')
h = F(bold=True, font_color='white', bg_color=NAVY, border=1, align='center', valign='vcenter', text_wrap=True)
h2 = F(bold=True, bg_color=LIGHT, border=1, text_wrap=True)
inp = F(bg_color=YEL, border=1)
inp_pct = F(bg_color=YEL, border=1, num_format='0.00%')
inp_num = F(bg_color=YEL, border=1, num_format='#,##0')
inp_px = F(bg_color=YEL, border=1, num_format='#,##0.00')
inp_date = F(bg_color=YEL, border=1, num_format='dd-mm-yyyy')
pct = F(num_format='0.00%', border=1)
pct_b = F(num_format='0.00%', border=1, bold=True, bg_color=GRN)
num = F(num_format='#,##0', border=1)
num_b = F(num_format='#,##0', border=1, bold=True, bg_color=GRN)
px = F(num_format='#,##0.00', border=1)
dec = F(num_format='0.000', border=1)
dec_b = F(num_format='0.000', border=1, bold=True, bg_color=GRN)
date = F(num_format='dd-mm-yyyy', border=1)
txt = F(border=1, text_wrap=True, valign='top')
bold = F(bold=True)
note = F(font_color='#7F7F7F', italic=True, text_wrap=True, valign='top')
warn = F(bold=True, font_color='#C00000')
box = F(bg_color=GRN, border=1, text_wrap=True, valign='top')

def header(ws, row, col, labels, widths=None):
    for i, l in enumerate(labels):
        ws.write(row, col + i, l, h)
    if widths:
        for i, w in enumerate(widths):
            ws.set_column(col + i, col + i, w)

# ---------- datos ficticios ----------
random.seed(2026)
ASSETS = ['BANCO', 'RETAIL', 'MINERA', 'ENERGIA', 'CONSUMO']
BETAS = [1.05, 1.30, 1.45, 0.60, 0.75]
IDIO = [0.009, 0.015, 0.020, 0.008, 0.010]
DRIFT = [0.0004, 0.0002, 0.0006, 0.0003, 0.0001]
START = [5200.0, 2100.0, 41000.0, 95.0, 6800.0]
N = 252
days = []
d = dt.date(2025, 1, 2)
while len(days) < N:
    if d.weekday() < 5:
        days.append(d)
    d += dt.timedelta(days=1)
mkt = [random.gauss(0.0004, 0.0095) for _ in range(N - 1)]
prices = {a: [START[i]] for i, a in enumerate(ASSETS)}
ipsa = [7000.0]
for t in range(N - 1):
    ipsa.append(ipsa[-1] * (1 + mkt[t]))
    for i, a in enumerate(ASSETS):
        r = DRIFT[i] + BETAS[i] * (mkt[t] - 0.0004) + random.gauss(0, IDIO[i])
        prices[a].append(prices[a][-1] * (1 + r))
COLS = ASSETS + ['IPSA']
FIRST, LAST = 2, N + 1            # filas Excel de precios: 2..253
RF, RL = 2, N                     # filas Excel de retornos: 2..252
def rng(sheet, col_letter, r1, r2):
    return f"{sheet}!${col_letter}${r1}:${col_letter}${r2}"

# =============== 0. INICIO ===============
ws = wb.add_worksheet('0_Inicio')
ws.set_column('A:A', 4); ws.set_column('B:B', 28); ws.set_column('C:C', 95)
ws.write('B2', 'LABORATORIO CCI - Concurso Carteras de Inversion', title)
ws.write('B3', 'Herramientas para estudiar y practicar teoria de portafolios y gestionar tu cartera durante el concurso.', sub)
ws.write('B5', 'COLORES', bold)
ws.write('B6', 'Celda amarilla', inp); ws.write('C6', 'Dato que TU ingresas o puedes cambiar.')
ws.write('B7', 'Celda verde', box); ws.write('C7', 'Resultado clave calculado con formulas (no escribir encima).')
ws.write('B8', 'Texto rojo', warn); ws.write('C8', 'Alertas automaticas (caja negativa, concentracion excesiva, etc.).')
ws.write('B10', 'HOJA', h); ws.write('C10', 'PARA QUE SIRVE', h)
sheets = [
    ('1_Precios', 'Precios diarios de 5 acciones y el IPSA. DATOS FICTICIOS para practicar: reemplazalos por datos reales (ver abajo).'),
    ('2_Retornos', 'Retornos diarios, retorno y volatilidad anualizados, Sharpe, retorno acumulado.'),
    ('3_Cov_Correl', 'Matriz de covarianzas y correlaciones (con mapa de calor). Base de la diversificacion.'),
    ('4_Frontera_2A', 'Frontera eficiente con 2 activos: cambia la correlacion y mira como cambia el riesgo. Portafolio de minima varianza.'),
    ('5_Cartera', 'Tu cartera de N acciones: pesos editables, retorno, riesgo, Sharpe, beta, Treynor, alfa de Jensen, tracking error, drawdown. Optimizable con Solver.'),
    ('6_Beta_CAPM', 'Beta de cada accion vs IPSA (regresion), R2 y retorno exigido por CAPM.'),
    ('7_Tecnico', 'Analisis tecnico de la accion que elijas: medias moviles 20/50, cruces, RSI(14) y bandas de Bollinger.'),
    ('8_Drawdown', 'Caida maxima desde el peak de cada activo.'),
    ('9_Simulador_CCI', 'Tu cuaderno de operaciones del concurso: registra compras/ventas, cobra la comision, calcula caja, posiciones, rentabilidad vs IPSA y alertas.'),
    ('10_Torneo', 'Costos de rotar la cartera y probabilidad de alcanzar una rentabilidad objetivo segun la volatilidad (logica de torneo).'),
    ('11_Screener', 'Plantilla de analisis fundamental: P/U, P/VL, dividend yield, EV/EBITDA, ROE, momentum y puntaje compuesto.'),
    ('12_Calendario', 'Planificador semanal del concurso + checklist antes de cada operacion.'),
    ('13_Plan_Estudio', 'Plan de 21 dias para dominar el tema, con avance automatico.'),
]
for i, (s, dsc) in enumerate(sheets):
    ws.write_url(10 + i, 1, f"internal:'{s}'!A1", string=s)
    ws.write(10 + i, 2, dsc, txt)
r = 10 + len(sheets) + 2
ws.write(r, 1, 'COMO PONER DATOS REALES', bold)
steps = [
    '1) Yahoo Finance: busca el ticker con sufijo .SN (ej. SQM-B.SN, CHILE.SN, FALABELLA.SN). Indice: ^IPSA. Pestana "Historical Data" > Descargar.',
    '2) Alternativas: Investing.com (Chile), TradingView, terminal de tu corredora o el sitio de la Bolsa de Santiago / nuam.',
    '3) Pega los precios de CIERRE (ajustados por dividendos si vas a medir retorno total) en 1_Precios, misma estructura (columna = accion, fila = fecha).',
    '4) Cambia los nombres de la fila 1 de 1_Precios por los tickers reales: todas las hojas se actualizan solas.',
    '5) Si cambias el numero de filas, ajusta los rangos (las formulas usan filas 2 a 253 = 252 dias habiles ~ 1 ano).',
    'ADVERTENCIA: los datos de ejemplo son simulados con un modelo de mercado. No representan precios reales de ninguna empresa.',
]
for j, s in enumerate(steps):
    ws.write(r + 1 + j, 2, s, warn if j == len(steps) - 1 else txt)

# =============== 1. PRECIOS ===============
ws = wb.add_worksheet('1_Precios')
header(ws, 0, 0, ['Fecha'] + COLS, [12] + [12] * 6)
ws.freeze_panes(1, 1)
for t in range(N):
    ws.write_datetime(t + 1, 0, dt.datetime.combine(days[t], dt.time()), inp_date)
    for i, a in enumerate(ASSETS):
        ws.write_number(t + 1, i + 1, round(prices[a][t], 2), inp_px)
    ws.write_number(t + 1, 6, round(ipsa[t], 2), inp_px)
ws.write('I1', 'DATOS FICTICIOS (simulados). Reemplazar por precios reales de cierre.', warn)
ch = wb.add_chart({'type': 'line'})
for i, c in enumerate(['G']):
    ch.add_series({'name': '=1_Precios!$G$1', 'categories': f'=1_Precios!$A$2:$A${LAST}', 'values': f'=1_Precios!$G$2:$G${LAST}', 'line': {'color': NAVY, 'width': 1.5}})
ch.set_title({'name': 'IPSA (ficticio)'}); ch.set_legend({'none': True}); ch.set_x_axis({'date_axis': True, 'num_format': 'mmm-yy'})
ws.insert_chart('I3', ch, {'x_scale': 1.4, 'y_scale': 1.1})

# =============== 2. RETORNOS ===============
ws = wb.add_worksheet('2_Retornos')
header(ws, 0, 0, ['Fecha'] + COLS, [12] + [11] * 6)
ws.freeze_panes(1, 1)
for t in range(1, N):
    er = t + 1
    ws.write_formula(t, 0, f"='1_Precios'!A{er}", date)
    for c in range(1, 7):
        L = cn(c)
        ws.write_formula(t, c, f"='1_Precios'!{L}{er}/'1_Precios'!{L}{er-1}-1", pct)
ws.set_column('I:I', 30); ws.set_column('J:O', 12)
ws.write('I1', 'PARAMETROS', h); ws.write('J1', '', h)
ws.write('I2', 'Tasa libre de riesgo anual (rf)', h2); ws.write('J2', 0.0475, inp_pct)
ws.write('K2', 'Ej.: TPM o BCP/BTP en pesos. Editable.', note)
ws.write('I3', 'Dias habiles por ano', h2); ws.write('J3', 252, inp_num)
header(ws, 4, 8, ['ESTADISTICO'] + COLS)
for c in range(6):
    D = cn(c + 1); S = cn(9 + c)
    fs = [
        ('Retorno medio diario', f"=AVERAGE({D}{RF}:{D}{RL})", pct),
        ('Retorno anualizado (compuesto)', f"=(1+{S}6)^$J$3-1", pct_b),
        ('Volatilidad diaria', f"=STDEV.S({D}{RF}:{D}{RL})", pct),
        ('Volatilidad anualizada', f"={S}8*SQRT($J$3)", pct_b),
        ('Ratio de Sharpe anual', f"=({S}7-$J$2)/{S}9", dec_b),
        ('Retorno acumulado periodo', f"=INDEX('1_Precios'!{D}${FIRST}:{D}${LAST},{N})/'1_Precios'!{D}${FIRST}-1", pct),
        ('Mejor dia', f"=MAX({D}{RF}:{D}{RL})", pct),
        ('Peor dia', f"=MIN({D}{RF}:{D}{RL})", pct),
        ('% dias positivos', f'=COUNTIF({D}{RF}:{D}{RL},">0")/COUNT({D}{RF}:{D}{RL})', pct),
        ('Asimetria (skew)', f"=SKEW({D}{RF}:{D}{RL})", dec),
        ('Curtosis (exceso)', f"=KURT({D}{RF}:{D}{RL})", dec),
    ]
    for k, (lab, f, fm) in enumerate(fs):
        ws.write(5 + k, 8, lab, h2)
        ws.write_formula(5 + k, 9 + c, f, fm)
ws.write('I18', 'Como leer:', bold)
ws.write('I19', 'Volatilidad anual = vol diaria x RAIZ(252). Sharpe = (retorno anual - rf) / volatilidad anual: retorno por unidad de riesgo total. '
         'Curtosis > 0 = colas gordas (mas dias extremos que una normal).', note)
ws.set_row(18, 60)

# =============== 3. COV / CORREL ===============
ws = wb.add_worksheet('3_Cov_Correl')
ws.set_column('A:A', 14); ws.set_column('B:G', 12)
ws.write('A1', 'Matriz de COVARIANZAS anualizadas (x252)', title)
header(ws, 2, 0, [''] + COLS)
for i in range(6):
    ws.write(3 + i, 0, COLS[i], h2)
    for j in range(6):
        Li, Lj = cn(i + 1), cn(j + 1)
        ws.write_formula(3 + i, 1 + j, f"=COVARIANCE.S('2_Retornos'!{Li}${RF}:{Li}${RL},'2_Retornos'!{Lj}${RF}:{Lj}${RL})*'2_Retornos'!$J$3", F(num_format='0.0000', border=1))
ws.write('A11', 'Matriz de CORRELACIONES', title)
header(ws, 12, 0, [''] + COLS)
for i in range(6):
    ws.write(13 + i, 0, COLS[i], h2)
    for j in range(6):
        Li, Lj = cn(i + 1), cn(j + 1)
        ws.write_formula(13 + i, 1 + j, f"=CORREL('2_Retornos'!{Li}${RF}:{Li}${RL},'2_Retornos'!{Lj}${RF}:{Lj}${RL})", F(num_format='0.00', border=1))
ws.conditional_format('B14:G19', {'type': '3_color_scale', 'min_color': '#63BE7B', 'mid_color': '#FFFFFF', 'max_color': '#F8696B', 'min_type': 'num', 'min_value': -1, 'mid_type': 'num', 'mid_value': 0, 'max_type': 'num', 'max_value': 1})
ws.write('I3', 'Interpretacion', bold)
ws.set_column('I:I', 70)
for k, s in enumerate([
    'Correlacion +1: se mueven igual (no diversifica). 0: independientes. -1: cobertura perfecta.',
    'En Chile las acciones suelen tener correlaciones positivas entre si (todas dependen del ciclo local, el cobre y el dolar).',
    'Combinar sectores con correlacion baja (ej. utilities vs mineria) reduce el riesgo de la cartera sin sacrificar retorno esperado.',
    'Diagonal de la covarianza = varianza de cada activo (volatilidad^2).',
    'Ojo: las correlaciones cambian en crisis (tienden a subir hacia 1 justo cuando mas necesitas diversificar).']):
    ws.write(3 + k, 8, s, note)

# =============== 4. FRONTERA 2 ACTIVOS ===============
ws = wb.add_worksheet('4_Frontera_2A')
ws.set_column('A:A', 34); ws.set_column('B:F', 13)
ws.write('A1', 'Frontera eficiente con 2 activos', title)
ws.write('A2', 'Cambia las celdas amarillas (sobre todo la correlacion) y observa el grafico.', sub)
ws.write('A4', 'Retorno esperado activo 1 (E1)', h2); ws.write_formula('B4', "='2_Retornos'!L7", inp_pct); ws.write('C4', '= MINERA (editable)', note)
ws.write('A5', 'Retorno esperado activo 2 (E2)', h2); ws.write_formula('B5', "='2_Retornos'!M7", inp_pct); ws.write('C5', '= ENERGIA (editable)', note)
ws.write('A6', 'Volatilidad activo 1 (s1)', h2); ws.write_formula('B6', "='2_Retornos'!L9", inp_pct)
ws.write('A7', 'Volatilidad activo 2 (s2)', h2); ws.write_formula('B7', "='2_Retornos'!M9", inp_pct)
ws.write('A8', 'Correlacion (rho)', h2); ws.write_formula('B8', "='3_Cov_Correl'!E16", F(bg_color=YEL, border=1, num_format='0.00'))
ws.write('C8', 'Prueba con -1, 0, 0,5 y 1', note)
ws.write('A10', 'Peso optimo minima varianza en activo 1 (w1*)', h2)
ws.write_formula('B10', "=(B7^2-B8*B6*B7)/(B6^2+B7^2-2*B8*B6*B7)", pct_b)
ws.write('A11', 'Retorno de la cartera de minima varianza', h2); ws.write_formula('B11', "=B10*B4+(1-B10)*B5", pct_b)
ws.write('A12', 'Volatilidad de la cartera de minima varianza', h2)
ws.write_formula('B12', "=SQRT(B10^2*B6^2+(1-B10)^2*B7^2+2*B10*(1-B10)*B8*B6*B7)", pct_b)
ws.write('C10', 'w1* = (s2^2 - rho*s1*s2) / (s1^2 + s2^2 - 2*rho*s1*s2)', note)
header(ws, 14, 0, ['w1 (activo 1)', 'w2 (activo 2)', 'Retorno E(Rp)', 'Volatilidad sp', 'Sharpe'])
for k in range(21):
    rr = 15 + k; R = rr + 1
    ws.write_number(rr, 0, k * 0.05, pct)
    ws.write_formula(rr, 1, f"=1-A{R}", pct)
    ws.write_formula(rr, 2, f"=A{R}*$B$4+B{R}*$B$5", pct)
    ws.write_formula(rr, 3, f"=SQRT(A{R}^2*$B$6^2+B{R}^2*$B$7^2+2*A{R}*B{R}*$B$8*$B$6*$B$7)", pct)
    ws.write_formula(rr, 4, f"=(C{R}-'2_Retornos'!$J$2)/D{R}", dec)
ch = wb.add_chart({'type': 'scatter', 'subtype': 'smooth_with_markers'})
ch.add_series({'name': 'Combinaciones', 'categories': '=4_Frontera_2A!$D$16:$D$36', 'values': '=4_Frontera_2A!$C$16:$C$36', 'marker': {'type': 'circle', 'size': 5}, 'line': {'color': BLUE}})
ch.add_series({'name': 'Min. varianza', 'categories': '=4_Frontera_2A!$B$12', 'values': '=4_Frontera_2A!$B$11', 'marker': {'type': 'diamond', 'size': 10, 'fill': {'color': '#C00000'}}, 'line': {'none': True}})
ch.set_title({'name': 'Riesgo vs retorno'}); ch.set_x_axis({'name': 'Volatilidad anual', 'num_format': '0%'}); ch.set_y_axis({'name': 'Retorno anual', 'num_format': '0%'})
ws.insert_chart('G4', ch, {'x_scale': 1.3, 'y_scale': 1.3})
ws.write('G26', 'La parte de la curva SOBRE el punto rojo es la frontera eficiente: mas retorno para cada nivel de riesgo.', note)

# =============== 5. CARTERA ===============
ws = wb.add_worksheet('5_Cartera')
ws.set_column('A:A', 34); ws.set_column('B:G', 13); ws.set_column('I:L', 13)
ws.write('A1', 'Mi cartera de N acciones', title)
ws.write('A2', 'Ingresa los pesos (deben sumar 100%). Luego usa Solver para maximizar el Sharpe (ver instrucciones abajo).', sub)
header(ws, 3, 0, ['', *ASSETS, 'SUMA'])
ws.write('A5', 'Peso (w)', h2)
for i in range(5):
    ws.write_number(4, 1 + i, 0.2, inp_pct)
ws.write_formula('G5', '=SUM(B5:F5)', pct_b)
ws.write_formula('H5', '=IF(ROUND(G5,4)<>1,"LOS PESOS NO SUMAN 100%","OK")', warn)
ws.write('A6', 'Retorno anual del activo', h2)
ws.write('A7', 'Volatilidad anual del activo', h2)
for i in range(5):
    ws.write_formula(5, 1 + i, f"='2_Retornos'!{cn(9+i)}7", pct)
    ws.write_formula(6, 1 + i, f"='2_Retornos'!{cn(9+i)}9", pct)
res = [
    ('Retorno anual de la cartera', "=(1+AVERAGE(J{a}:J{b}))^'2_Retornos'!$J$3-1", pct_b),
    ('Volatilidad anual de la cartera', "=STDEV.S(J{a}:J{b})*SQRT('2_Retornos'!$J$3)", pct_b),
    ('Ratio de Sharpe', "=(B9-'2_Retornos'!$J$2)/B10", dec_b),
    ('Beta de la cartera vs IPSA', "=SLOPE(J{a}:J{b},K{a}:K{b})", dec_b),
    ('Ratio de Treynor', "=(B9-'2_Retornos'!$J$2)/B12", dec),
    ('Retorno anual IPSA', "='2_Retornos'!O7", pct),
    ('Alfa de Jensen (anual)', "=B9-('2_Retornos'!$J$2+B12*(B14-'2_Retornos'!$J$2))", pct_b),
    ('Tracking error vs IPSA', "=STDEV.S(L{a}:L{b})*SQRT('2_Retornos'!$J$3)", pct),
    ('Information ratio', "=(B9-B14)/B16", dec),
    ('Volatilidad promedio ponderada (sin diversificar)', "=SUMPRODUCT(B5:F5,B7:F7)", pct),
    ('Reduccion de riesgo por diversificacion', "=1-B10/B18", pct_b),
    ('Max. drawdown de la cartera', "=MIN(N{a}:N{b})", pct_b),
]
a, b = 3, N + 1   # filas de retornos diarios en esta hoja (J3:J253 -> 251 retornos)
for k, (lab, f, fm) in enumerate(res):
    ws.write(8 + k, 0, lab, h2)
    ws.write_formula(8 + k, 1, f.format(a=a, b=b), fm)
ws.write('C11', 'Retorno extra por unidad de riesgo total', note)
ws.write('C12', '>1 mas agresiva que el mercado; <1 mas defensiva', note)
ws.write('C15', 'Retorno sobre lo que exige el CAPM dado su beta', note)
ws.write('C19', 'Cuanto riesgo "gratis" eliminaste combinando acciones', note)
ws.write('A22', 'SOLVER (Datos > Solver; si no aparece: Archivo > Opciones > Complementos > Solver):', bold)
for k, s in enumerate(['Establecer objetivo: $B$11 (Sharpe)  ->  Max',
                       'Cambiando las celdas: $B$5:$F$5',
                       'Restricciones: $G$5 = 1   y   $B$5:$F$5 >= 0  (sin ventas cortas). Opcional: $B$5:$F$5 <= 0,35 (limite por accion)',
                       'Metodo: GRG Nonlinear. Repite con objetivo $B$10 -> Min para la cartera de minima varianza.']):
    ws.write(22 + k, 0, s, note)
header(ws, 1, 8, ['Fecha', 'Ret. cartera', 'Ret. IPSA', 'Diferencia', 'Indice cartera', 'Drawdown', 'Indice IPSA'])
for t in range(1, N):
    rr = t + 1; R = rr + 1   # filas 3..253
    ws.write_formula(rr, 8, f"='2_Retornos'!A{t+1}", date)
    ws.write_formula(rr, 9, f"=SUMPRODUCT($B$5:$F$5,'2_Retornos'!B{t+1}:F{t+1})", pct)
    ws.write_formula(rr, 10, f"='2_Retornos'!G{t+1}", pct)
    ws.write_formula(rr, 11, f"=J{R}-K{R}", pct)
    prev = 100 if t == 1 else f"M{R-1}"
    ws.write_formula(rr, 12, f"={prev}*(1+J{R})", px)
    ws.write_formula(rr, 13, f"=M{R}/MAX($M$3:M{R})-1", pct)
    ws.write_formula(rr, 14, f"={'100' if t==1 else f'O{R-1}'}*(1+K{R})", px)
ws.set_column('O:O', 12)
ch = wb.add_chart({'type': 'line'})
ch.add_series({'name': 'Mi cartera', 'categories': f'=5_Cartera!$I$3:$I${N+1}', 'values': f'=5_Cartera!$M$3:$M${N+1}', 'line': {'color': '#C00000', 'width': 1.75}})
ch.add_series({'name': 'IPSA', 'categories': f'=5_Cartera!$I$3:$I${N+1}', 'values': f'=5_Cartera!$O$3:$O${N+1}', 'line': {'color': NAVY, 'width': 1.25}})
ch.set_title({'name': 'Cartera vs IPSA (base 100)'}); ch.set_x_axis({'date_axis': True, 'num_format': 'mmm-yy'})
ws.insert_chart('A28', ch, {'x_scale': 1.5, 'y_scale': 1.1})

# =============== 6. BETA CAPM ===============
ws = wb.add_worksheet('6_Beta_CAPM')
ws.set_column('A:A', 36); ws.set_column('B:F', 13)
ws.write('A1', 'Beta y CAPM', title)
ws.write('A3', 'Tasa libre de riesgo anual (rf)', h2); ws.write_formula('B3', "='2_Retornos'!J2", pct)
ws.write('A4', 'Prima por riesgo de mercado (ERP)', h2); ws.write_number('B4', 0.0533, inp_pct)
ws.write('C4', 'Ej.: prima total Chile Damodaran ene-2026 (verificar). Editable.', note)
header(ws, 6, 0, ['Metrica', *ASSETS])
rows6 = [
    ('Beta (pendiente vs IPSA)', lambda L: f"=SLOPE('2_Retornos'!{L}${RF}:{L}${RL},'2_Retornos'!$G${RF}:$G${RL})", dec_b),
    ('R2 (riesgo explicado por el mercado)', lambda L: f"=RSQ('2_Retornos'!{L}${RF}:{L}${RL},'2_Retornos'!$G${RF}:$G${RL})", pct),
    ('Riesgo idiosincratico (1 - R2)', lambda L: None, pct),
    ('Alfa diario (intercepto)', lambda L: f"=INTERCEPT('2_Retornos'!{L}${RF}:{L}${RL},'2_Retornos'!$G${RF}:$G${RL})", F(num_format='0.000%', border=1)),
    ('Retorno exigido CAPM: rf + beta x ERP', lambda L: None, pct_b),
    ('Retorno observado anual', lambda L: None, pct),
    ('Diferencia (observado - CAPM)', lambda L: None, pct),
]
for k, (lab, fn, fm) in enumerate(rows6):
    ws.write(7 + k, 0, lab, h2)
    for i in range(5):
        L = cn(i + 1); C = cn(1 + i)
        if k == 2: f = f"=1-{C}9"
        elif k == 4: f = f"=$B$3+{C}8*$B$4"
        elif k == 5: f = f"='2_Retornos'!{cn(9+i)}7"
        elif k == 6: f = f"={C}13-{C}12"
        else: f = fn(L)
        ws.write_formula(7 + k, 1 + i, f, fm)
ws.write('A16', 'Lectura: beta 1,4 => si el IPSA sube 1%, la accion tiende a subir 1,4%. En un torneo, las betas altas amplifican el resultado (para bien y para mal).', note)
ws.set_row(15, 30)
ch = wb.add_chart({'type': 'scatter'})
ch.add_series({'name': 'MINERA vs IPSA', 'categories': f"='2_Retornos'!$G${RF}:$G${RL}", 'values': f"='2_Retornos'!$D${RF}:$D${RL}",
               'marker': {'type': 'circle', 'size': 3, 'fill': {'color': BLUE}}, 'trendline': {'type': 'linear', 'display_equation': True, 'display_r_squared': True}})
ch.set_title({'name': 'Regresion de la beta (MINERA)'}); ch.set_x_axis({'name': 'Retorno IPSA', 'num_format': '0%'}); ch.set_y_axis({'name': 'Retorno MINERA', 'num_format': '0%'}); ch.set_legend({'none': True})
ws.insert_chart('A18', ch, {'x_scale': 1.4, 'y_scale': 1.2})

# =============== 7. TECNICO ===============
ws = wb.add_worksheet('7_Tecnico')
ws.set_column('A:A', 12); ws.set_column('B:J', 12)
ws.write('A1', 'Accion:', bold); ws.write('B1', 'MINERA', inp)
ws.data_validation('B1', {'validate': 'list', 'source': "='1_Precios'!$B$1:$F$1"})
ws.write('C1', '<- elige la accion (lista desplegable)', note)
ws.write('E1', 'Ultima senal:', bold)
header(ws, 2, 0, ['Fecha', 'Precio', 'SMA 20', 'SMA 50', 'Senal cruce', 'Ganancia', 'Perdida', 'RSI 14', 'Bollinger sup', 'Bollinger inf'])
for t in range(N):
    rr = 3 + t; R = rr + 1; pr = t + 2
    ws.write_formula(rr, 0, f"='1_Precios'!A{pr}", date)
    ws.write_formula(rr, 1, f"=INDEX('1_Precios'!$B${pr}:$F${pr},MATCH($B$1,'1_Precios'!$B$1:$F$1,0))", px)
    if t >= 19:
        ws.write_formula(rr, 2, f"=AVERAGE(B{R-19}:B{R})", px)
        ws.write_formula(rr, 8, f"=C{R}+2*STDEV.S(B{R-19}:B{R})", px)
        ws.write_formula(rr, 9, f"=C{R}-2*STDEV.S(B{R-19}:B{R})", px)
    if t >= 49:
        ws.write_formula(rr, 3, f"=AVERAGE(B{R-49}:B{R})", px)
    if t >= 50:
        ws.write_formula(rr, 4, f'=IF(AND(C{R}>D{R},C{R-1}<=D{R-1}),"COMPRA (cruce alcista)",IF(AND(C{R}<D{R},C{R-1}>=D{R-1}),"VENTA (cruce bajista)",""))', txt)
    if t >= 1:
        ws.write_formula(rr, 5, f"=MAX(B{R}-B{R-1},0)", px)
        ws.write_formula(rr, 6, f"=MAX(B{R-1}-B{R},0)", px)
    if t >= 14:
        ws.write_formula(rr, 7, f'=IF(SUM(G{R-13}:G{R})=0,100,100-100/(1+AVERAGE(F{R-13}:F{R})/AVERAGE(G{R-13}:G{R})))', F(num_format='0.0', border=1))
last = 3 + N
ws.write_formula('F1', f'=IFERROR(LOOKUP(2,1/(E4:E{last}<>""),E4:E{last}),"sin senal")', box)
ws.write_formula('H1', f'="RSI actual: "&TEXT(H{last},"0.0")&IF(H{last}>70," (sobrecompra)",IF(H{last}<30," (sobreventa)",""))', box)
ws.set_column('F:F', 26); ws.set_column('E:E', 22)
ws.conditional_format(f'H4:H{last}', {'type': 'cell', 'criteria': '>', 'value': 70, 'format': F(bg_color=RED)})
ws.conditional_format(f'H4:H{last}', {'type': 'cell', 'criteria': '<', 'value': 30, 'format': F(bg_color=GRN)})
ch = wb.add_chart({'type': 'line'})
for col, nm, color, w in [('B', 'Precio', '#000000', 1.5), ('C', 'SMA 20', '#ED7D31', 1.25), ('D', 'SMA 50', BLUE, 1.25), ('I', 'Bollinger sup', '#A5A5A5', 0.75), ('J', 'Bollinger inf', '#A5A5A5', 0.75)]:
    ch.add_series({'name': nm, 'categories': f'=7_Tecnico!$A$4:$A${last}', 'values': f'=7_Tecnico!${col}$4:${col}${last}', 'line': {'color': color, 'width': w}})
ch.set_title({'name': 'Precio, medias moviles y Bollinger'}); ch.set_x_axis({'date_axis': True, 'num_format': 'mmm-yy'})
ws.insert_chart('L3', ch, {'x_scale': 1.8, 'y_scale': 1.3})
ch2 = wb.add_chart({'type': 'line'})
ch2.add_series({'name': 'RSI 14', 'categories': f'=7_Tecnico!$A$4:$A${last}', 'values': f'=7_Tecnico!$H$4:$H${last}', 'line': {'color': '#7030A0', 'width': 1.25}})
ch2.set_title({'name': 'RSI(14): >70 sobrecompra, <30 sobreventa'}); ch2.set_y_axis({'min': 0, 'max': 100, 'major_unit': 10}); ch2.set_legend({'none': True}); ch2.set_x_axis({'date_axis': True, 'num_format': 'mmm-yy'})
ws.insert_chart('L24', ch2, {'x_scale': 1.8, 'y_scale': 0.9})

# =============== 8. DRAWDOWN ===============
ws = wb.add_worksheet('8_Drawdown')
ws.set_column('A:A', 12); ws.set_column('B:M', 11)
header(ws, 0, 0, ['Fecha'] + [f'DD {c}' for c in COLS])
for t in range(N):
    rr = t + 1; R = rr + 1
    ws.write_formula(rr, 0, f"='1_Precios'!A{R}", date)
    for c in range(1, 7):
        L = cn(c)
        ws.write_formula(rr, c, f"='1_Precios'!{L}{R}/MAX('1_Precios'!{L}$2:{L}{R})-1", pct)
ws.write('I1', 'MAXIMO DRAWDOWN', h); ws.write('J1', '', h)
for c in range(6):
    ws.write(1 + c, 8, COLS[c], h2)
    ws.write_formula(1 + c, 9, f"=MIN({cn(c+1)}2:{cn(c+1)}{N+1})", pct_b)
ws.set_column('I:I', 14)
ws.write('I9', 'Drawdown = caida desde el maximo previo. Una caida de -50% exige +100% para recuperarse.', note)
ch = wb.add_chart({'type': 'area'})
ch.add_series({'name': 'DD MINERA', 'categories': f'=8_Drawdown!$A$2:$A${N+1}', 'values': f'=8_Drawdown!$D$2:$D${N+1}', 'fill': {'color': '#F8696B', 'transparency': 30}})
ch.add_series({'name': 'DD IPSA', 'categories': f'=8_Drawdown!$A$2:$A${N+1}', 'values': f'=8_Drawdown!$G$2:$G${N+1}', 'fill': {'color': NAVY, 'transparency': 40}})
ch.set_title({'name': 'Drawdown: MINERA vs IPSA'}); ch.set_y_axis({'num_format': '0%'}); ch.set_x_axis({'date_axis': True, 'num_format': 'mmm-yy'})
ws.insert_chart('I11', ch, {'x_scale': 1.5, 'y_scale': 1.1})

# =============== 9. SIMULADOR CCI ===============
ws = wb.add_worksheet('9_Simulador_CCI')
ws.set_column('A:A', 12); ws.set_column('B:B', 12); ws.set_column('C:C', 9); ws.set_column('D:D', 10); ws.set_column('E:E', 11)
ws.set_column('F:H', 14); ws.set_column('I:I', 10); ws.set_column('J:J', 40); ws.set_column('K:L', 11)
ws.write('A1', 'CUADERNO DE OPERACIONES - CCI', title)
ws.write('A2', 'Registra cada operacion tal como la hiciste en el simulador. Las filas de ejemplo son ficticias: borralas antes de empezar.', sub)
ws.write('A4', 'Capital inicial', h2); ws.write('C4', 20000000, inp_num)
ws.write('A5', 'Comision por operacion', h2); ws.write('C5', 0.005, inp_pct); ws.write('D5', 'Confirmar en bases vigentes', note)
ws.write('A6', 'Limite de peso por accion', h2); ws.write('C6', 0.35, inp_pct); ws.write('D6', 'Tu regla de riesgo', note)
ws.write('F4', 'IPSA al inicio', h2); ws.write('H4', 10000, inp_px)
ws.write('F5', 'IPSA hoy', h2); ws.write('H5', 10250, inp_px)
OP0, OPN = 10, 110   # filas Excel 11..110 (100 operaciones)
header(ws, 9, 0, ['Fecha', 'Ticker', 'Tipo', 'Cantidad', 'Precio', 'Monto bruto', 'Comision', 'Flujo de caja', 'Cant. +/-', 'Tesis / motivo', 'Stop', 'Objetivo'])
ws.freeze_panes(10, 0)
ex = [
    (dt.date(2026, 10, 14), 'BANCO', 'Compra', 600, 5400, 'Ciclo de tasas: TPM a la baja mejora credito', 4950, 6200),
    (dt.date(2026, 10, 14), 'MINERA', 'Compra', 110, 43000, 'Cobre al alza + resultados 3T esperados fuertes', 39500, 50000),
    (dt.date(2026, 10, 15), 'ENERGIA', 'Compra', 25000, 98, 'Defensiva, baja correlacion con mineria', 90, 110),
    (dt.date(2026, 10, 28), 'MINERA', 'Venta', 50, 47200, 'Toma de ganancia parcial tras resultados', '', ''),
]
for k, (fd, tk, tp, q, p, tes, sl, tg) in enumerate(ex):
    ws.write_datetime(OP0 + k, 0, dt.datetime.combine(fd, dt.time()), inp_date)
    ws.write(OP0 + k, 1, tk, inp); ws.write(OP0 + k, 2, tp, inp); ws.write_number(OP0 + k, 3, q, inp_num); ws.write_number(OP0 + k, 4, p, inp_px)
    ws.write(OP0 + k, 9, tes, F(bg_color=YEL, border=1, text_wrap=True))
    ws.write(OP0 + k, 10, sl, inp_px); ws.write(OP0 + k, 11, tg, inp_px)
for rr in range(OP0, OPN):
    R = rr + 1
    if rr >= OP0 + len(ex):
        for c in (0,): ws.write_blank(rr, c, None, inp_date)
        for c in (1, 2, 9): ws.write_blank(rr, c, None, inp)
        for c in (3,): ws.write_blank(rr, c, None, inp_num)
        for c in (4, 10, 11): ws.write_blank(rr, c, None, inp_px)
    ws.write_formula(rr, 5, f'=IF(OR(D{R}="",E{R}=""),"",D{R}*E{R})', num)
    ws.write_formula(rr, 6, f'=IF(F{R}="","",F{R}*$C$5)', num)
    ws.write_formula(rr, 7, f'=IF(F{R}="","",IF(C{R}="Compra",-(F{R}+G{R}),F{R}-G{R}))', num)
    ws.write_formula(rr, 8, f'=IF(D{R}="","",IF(C{R}="Compra",D{R},-D{R}))', num)
ws.data_validation(f'C{OP0+1}:C{OPN}', {'validate': 'list', 'source': ['Compra', 'Venta']})
# Resumen y posiciones a la derecha
ws.set_column('N:N', 30); ws.set_column('O:U', 14)
ws.write('N4', 'RESUMEN DE LA CARTERA', h); ws.write('O4', '', h)
summ = [
    ('Caja disponible', f"=$C$4+SUM(H{OP0+1}:H{OPN})", num_b),
    ('Valor de mercado acciones', "=SUM(S13:S27)", num_b),
    ('VALOR TOTAL CARTERA', "=O5+O6", num_b),
    ('Rentabilidad acumulada', "=O7/$C$4-1", pct_b),
    ('Rentabilidad IPSA mismo periodo', "=$H$5/$H$4-1", pct),
    ('Exceso sobre IPSA', "=O8-O9", pct_b),
    ('Comisiones pagadas (total)', f"=SUM(G{OP0+1}:G{OPN})", num),
]
for k, (lab, f, fm) in enumerate(summ):
    ws.write(4 + k, 13, lab, h2); ws.write_formula(4 + k, 14, f, fm)
ws.write('N12', 'Comisiones como % del capital', h2); ws.write_formula('O12', '=O11/$C$4', pct)
ws.write('P5', 'Alerta', h)
ws.write_formula('P6', '=IF(O5<0,"CAJA NEGATIVA: vendiste o compraste de mas",IF(MAX(U13:U27)>$C$6,"CONCENTRACION > limite","OK"))', warn)
ws.set_column('P:P', 14)
header(ws, 11, 15, ['Ticker', 'Cantidad', 'Precio medio compra', 'Precio actual', 'Valor mercado', 'P&L no realizado', 'Peso'])
ws.set_column('P:V', 13)
tick = ['BANCO', 'MINERA', 'ENERGIA'] + [''] * 12
lastpx = [5550, 46100, 101]
for k in range(15):
    rr = 12 + k; R = rr + 1
    ws.write(rr, 15, tick[k], inp)
    ws.write_formula(rr, 16, f'=IF(P{R}="","",SUMIF($B${OP0+1}:$B${OPN},P{R},$I${OP0+1}:$I${OPN}))', num)
    ws.write_formula(rr, 17, f'=IF(P{R}="","",IFERROR(SUMIFS($F${OP0+1}:$F${OPN},$B${OP0+1}:$B${OPN},P{R},$C${OP0+1}:$C${OPN},"Compra")/SUMIFS($D${OP0+1}:$D${OPN},$B${OP0+1}:$B${OPN},P{R},$C${OP0+1}:$C${OPN},"Compra"),0))', px)
    if k < 3: ws.write_number(rr, 18, lastpx[k], inp_px)
    else: ws.write_blank(rr, 18, None, inp_px)
    # columnas: P ticker(15) Q cant(16) R pmedio(17) S precio actual(18) -> reorganizamos: valor en T? ajustamos abajo
for k in range(15):
    rr = 12 + k; R = rr + 1
    ws.write_formula(rr, 19, f'=IF(OR(P{R}="",S{R}=""),"",Q{R}*S{R})', num)
    ws.write_formula(rr, 20, f'=IF(T{R}="","",T{R}-Q{R}*R{R})', num)
    ws.write_formula(rr, 21, f'=IF(T{R}="","",T{R}/$O$7)', pct)
# corregir referencias del resumen (valor mercado esta en T, peso en V)
ws.write_formula('O6', "=SUM(T13:T27)", num_b)
ws.write_formula('P6', '=IF(O5<0,"CAJA NEGATIVA",IF(MAX(V13:V27)>$C$6,"CONCENTRACION > limite","OK"))', warn)
ws.write('P29', 'Precio actual: copialo del simulador cada dia. El P&L no realizado usa el precio medio de compra.', note)
ch = wb.add_chart({'type': 'pie'})
ch.add_series({'name': 'Composicion', 'categories': '=9_Simulador_CCI!$P$13:$P$15', 'values': '=9_Simulador_CCI!$T$13:$T$15', 'data_labels': {'percentage': True}})
ch.set_title({'name': 'Composicion (acciones)'})
ws.insert_chart('X4', ch, {'x_scale': 0.9, 'y_scale': 0.9})

# =============== 10. TORNEO ===============
ws = wb.add_worksheet('10_Torneo')
ws.set_column('A:A', 40); ws.set_column('B:H', 12)
ws.write('A1', 'Economia del torneo: costos y probabilidades', title)
ws.write('A3', 'A) COSTO DE ROTAR LA CARTERA', bold)
ws.write('A4', 'Comision por operacion', h2); ws.write_formula('B4', "='9_Simulador_CCI'!C5", pct)
ws.write('A5', 'Alza minima para empatar una compra+venta', h2); ws.write_formula('B5', '=(1+B4)/(1-B4)-1', pct_b)
ws.write('C5', 'Con 0,5% por lado necesitas ~1,005% de alza solo para no perder.', note)
header(ws, 6, 0, ['N de rotaciones completas de TODA la cartera', 'Costo acumulado', 'Comentario'])
for k, n in enumerate([1, 2, 4, 6, 8, 10, 15, 20]):
    ws.write_number(7 + k, 0, n, num)
    ws.write_formula(7 + k, 1, f'=1-((1-$B$4)/(1+$B$4))^A{8+k}', pct)
ws.write('C8', 'Un "day trader" que rota todo 20 veces pierde ~18% solo en comisiones.', note)
ws.write('A17', 'B) PROBABILIDAD DE SUPERAR UNA META (modelo lognormal)', bold)
ws.write('A18', 'Duracion del concurso (semanas)', h2); ws.write_number('B18', 8, inp_num)
ws.write('A19', 'Retorno esperado anual de la cartera (mu)', h2); ws.write_number('B19', 0.10, inp_pct)
ws.write('A20', 'Supuesto clave', h2); ws.write('B20', 'Sin habilidad especial: el retorno es aleatorio alrededor de mu', note)
targets = [0.05, 0.10, 0.20, 0.30, 0.50]
header(ws, 21, 0, ['Volatilidad anual de la cartera'] + [f'P(R > {int(t*100)}%)' for t in targets] + ['P(R < -10%)'])
for k, sig in enumerate([0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80]):
    rr = 22 + k; R = rr + 1
    ws.write_number(rr, 0, sig, pct)
    for j, tgt in enumerate(targets):
        ws.write_formula(rr, 1 + j, f"=1-NORM.DIST(LN(1+{tgt}),($B$19-A{R}^2/2)*$B$18/52,A{R}*SQRT($B$18/52),TRUE)", pct)
    ws.write_formula(rr, 6, f"=NORM.DIST(LN(0.9),($B$19-A{R}^2/2)*$B$18/52,A{R}*SQRT($B$18/52),TRUE)", pct)
ws.conditional_format('B23:F30', {'type': '2_color_scale', 'min_color': '#FFFFFF', 'max_color': '#63BE7B'})
ws.conditional_format('G23:G30', {'type': '2_color_scale', 'min_color': '#FFFFFF', 'max_color': '#F8696B'})
for k, s in enumerate([
    'LECCION: los ganadores historicos del CCI universitario rentaron 30%-65% en ~8 semanas. Con volatilidad del IPSA (~15-20%) la probabilidad de lograrlo es casi cero.',
    'Para aspirar al primer lugar entre miles hay que aceptar mas volatilidad (concentracion, betas altas). Pero la misma tabla muestra que sube la probabilidad de perder mucho.',
    'La habilidad (buen analisis) desplaza mu hacia arriba; la volatilidad abre el abanico. El objetivo es combinar ambas sin arriesgar la "ruina" temprana.',
    'Supuesto simplificado (retornos lognormales, sin saltos). Sirve para intuicion, no como prediccion.']):
    ws.write(32 + k, 0, s, note)
    ws.set_row(32 + k, 30)

# =============== 11. SCREENER ===============
ws = wb.add_worksheet('11_Screener')
ws.write('A1', 'Screener fundamental (plantilla)', title)
ws.write('A2', 'Datos de ejemplo FICTICIOS. Llena con datos reales de los estados financieros (CMF) y precios del dia.', sub)
cols11 = ['Empresa', 'Sector', 'Precio', 'UPA (12m)', 'VL por accion', 'Dividendo por accion', 'EBITDA (MM$)', 'Deuda neta (MM$)', 'N acciones (MM)', 'Var. precio 3M',
          'P/U', 'P/VL', 'Div. yield', 'Cap. bursatil (MM$)', 'EV (MM$)', 'EV/EBITDA', 'ROE', 'Rank P/U', 'Rank DivY', 'Rank Momentum', 'Rank ROE', 'PUNTAJE', 'POSICION']
header(ws, 3, 0, cols11, [14, 12, 10, 10, 10, 10, 11, 11, 10, 10] + [9] * 13)
data11 = [('BANCO', 'Financiero', 5400, 520, 3600, 300, 0, 0, 1000, 0.06), ('RETAIL', 'Consumo', 2150, 140, 2400, 45, 900, 2500, 2500, 0.12),
          ('MINERA', 'Materiales', 43000, 2600, 17000, 1100, 3200, 1500, 280, 0.18), ('ENERGIA', 'Utilities', 98, 7.5, 70, 6, 1800, 4000, 69000, 0.02),
          ('CONSUMO', 'Consumo basico', 6800, 410, 3900, 240, 700, 900, 370, -0.03), ('FORESTAL', 'Materiales', 1650, 80, 2100, 30, 1400, 3500, 2500, -0.08),
          ('AEROLINEA', 'Transporte', 18, 1.9, 9, 0.2, 2500, 6000, 600000, 0.25), ('TELECOM', 'Comunicaciones', 3100, 150, 2800, 120, 600, 1300, 300, 0.01)]
n11 = len(data11); r0 = 4; r1 = r0 + n11
for k, row in enumerate(data11):
    rr = r0 + k; R = rr + 1
    for j, v in enumerate(row):
        ws.write(rr, j, v, inp_pct if j == 9 else (inp_px if j in (2, 3, 4, 5) else (inp_num if j > 5 else inp)))
    ws.write_formula(rr, 10, f'=IFERROR(C{R}/D{R},"")', F(num_format='0.0', border=1))
    ws.write_formula(rr, 11, f'=IFERROR(C{R}/E{R},"")', F(num_format='0.00', border=1))
    ws.write_formula(rr, 12, f'=IFERROR(F{R}/C{R},"")', pct)
    ws.write_formula(rr, 13, f'=C{R}*I{R}', num)
    ws.write_formula(rr, 14, f'=N{R}+H{R}', num)
    ws.write_formula(rr, 15, f'=IF(G{R}=0,"n/a",O{R}/G{R})', F(num_format='0.0', border=1))
    ws.write_formula(rr, 16, f'=IFERROR(D{R}/E{R},"")', pct)
    ws.write_formula(rr, 17, f'=RANK(K{R},$K${r0+1}:$K${r1},1)', num)
    ws.write_formula(rr, 18, f'=RANK(M{R},$M${r0+1}:$M${r1},0)', num)
    ws.write_formula(rr, 19, f'=RANK(J{R},$J${r0+1}:$J${r1},0)', num)
    ws.write_formula(rr, 20, f'=RANK(Q{R},$Q${r0+1}:$Q${r1},0)', num)
    ws.write_formula(rr, 21, f'=AVERAGE(R{R}:U{R})', F(num_format='0.00', border=1, bold=True, bg_color=GRN))
    ws.write_formula(rr, 22, f'=RANK(V{R},$V${r0+1}:$V${r1},1)', num_b)
ws.write(r1 + 2, 0, 'Notas:', bold)
for k, s in enumerate(['P/U bajo y P/VL bajo = "barata" (value). P/VL = 1/BME de tu tesina: el BME alto se asocia a menos opciones de crecimiento.',
                       'EV/EBITDA no aplica a bancos (su deuda es materia prima). Para bancos usa P/U, P/VL y ROE.',
                       'El puntaje promedia rankings (1 = mejor). Cambia los criterios segun tu estrategia (value, dividendos, momentum, calidad).',
                       'En 8 semanas pesan mas los CATALIZADORES (resultados, dividendos, noticias) y el momentum que el valor de largo plazo.']):
    ws.write(r1 + 3 + k, 0, s, note)

# =============== 12. CALENDARIO ===============
ws = wb.add_worksheet('12_Calendario')
ws.set_column('A:A', 9); ws.set_column('B:C', 12); ws.set_column('D:G', 32)
ws.write('A1', 'Planificador semanal del concurso', title)
ws.write('A3', 'Inicio oficial:', bold); ws.write_datetime('C3', dt.datetime(2026, 10, 19), inp_date); ws.write('D3', 'Cambia por la fecha real de las bases', note)
header(ws, 5, 0, ['Semana', 'Desde', 'Hasta', 'Eventos macro (BCCh, IPC, Fed, cobre)', 'Resultados / dividendos de empresas', 'Plan de la semana', 'Revision (que funciono / que no)'])
for k in range(10):
    rr = 6 + k; R = rr + 1
    ws.write(rr, 0, f'S{k+1}' if k < 9 else 'Final', h2)
    ws.write_formula(rr, 1, f'=$C$3+{7*k}', date); ws.write_formula(rr, 2, f'=B{R}+4', date)
    for c in range(3, 7): ws.write_blank(rr, c, None, F(bg_color=YEL, border=1, text_wrap=True))
    ws.set_row(rr, 36)
ws.write('D7', 'Ej.: Reunion de Politica Monetaria; IPC (INE, ~dia 8)', F(bg_color=YEL, border=1, text_wrap=True, italic=True))
ws.write('E7', 'Ej.: temporada de resultados 3T (fines oct - nov)', F(bg_color=YEL, border=1, text_wrap=True, italic=True))
ws.write('D18', 'CHECKLIST ANTES DE CADA OPERACION', h); ws.write('E18', 'Si / No', h)
checks = ['Tengo una tesis escrita en 1-2 frases (por que subira o bajara)', 'Se cual es el catalizador y cuando ocurre', 'Revise noticias y hechos esenciales (CMF) de hoy',
          'El tamano de la posicion respeta mi limite por accion', 'Calcule cuanto debe moverse para cubrir la comision (~1%)', 'Defini precio de salida si me equivoco (stop)',
          'Defini precio objetivo / condicion de toma de ganancia', 'No estoy operando por impulso (FOMO o recuperar perdidas)', 'Revise la correlacion con lo que ya tengo',
          'Registre la operacion en 9_Simulador_CCI']
for k, s in enumerate(checks):
    ws.write(18 + k, 3, s, txt); ws.write(18 + k, 4, '', inp)
    ws.data_validation(18 + k, 4, 18 + k, 4, {'validate': 'list', 'source': ['Si', 'No']})
ws.write_formula('F18', '=IF(COUNTIF(E19:E28,"Si")=10,"LISTO PARA OPERAR",IF(COUNTIF(E19:E28,"No")>0,"NO OPERAR AUN","completa el checklist"))', box)

# =============== 13. PLAN ESTUDIO ===============
ws = wb.add_worksheet('13_Plan_Estudio')
ws.set_column('A:A', 6); ws.set_column('B:B', 48); ws.set_column('C:C', 46); ws.set_column('D:D', 10)
ws.write('A1', 'Plan de estudio: 21 dias para dominar el CCI', title)
header(ws, 2, 0, ['Dia', 'Tema', 'Material', 'Hecho'])
plan = [
    ('Que es el CCI, reglas y logica de torneo', 'Guia cap. 1-2 + Resumen Express'), ('Bolsa de Santiago, nuam, IPSA, ordenes y costos', 'Guia cap. 3'),
    ('Sectores del IPSA y empresas clave', 'Guia cap. 3 + Screener'), ('Macro Chile: cobre, dolar, TPM, inflacion', 'Guia cap. 4 + Mapas (cadena macro)'),
    ('Retorno, riesgo, anualizacion, drawdown', 'Guia cap. 5 + hojas 2 y 8'), ('Covarianza, correlacion y diversificacion', 'Guia cap. 6 + hoja 3'),
    ('Markowitz y frontera eficiente', 'Guia cap. 6 + hoja 4 + Ejercicios 4-6'), ('CAPM, beta, SML; repaso tesina', 'Guia cap. 7 + hoja 6'),
    ('Sharpe, Treynor, Jensen, info ratio', 'Guia cap. 7 + hoja 5 + Ejercicios 7-9'), ('Repaso + Quiz (bloque teoria)', 'Quiz interactivo + Flashcards'),
    ('Analisis fundamental: multiplos', 'Guia cap. 8 + hoja 11'), ('Estados financieros rapidos y resultados trimestrales', 'Guia cap. 8'),
    ('Analisis tecnico: tendencia, medias, RSI, Bollinger', 'Guia cap. 9 + hoja 7'), ('Momentum, reversion y eventos', 'Guia cap. 9'),
    ('Finanzas conductuales', 'Guia cap. 10'), ('Estrategia de torneo y tamano de posiciones', 'Guia cap. 11 + hoja 10'),
    ('Disenar TU estrategia (documento de 1 pagina)', 'Guia cap. 11 (plantilla)'), ('Marcha blanca: probar la plataforma', 'Simulador del concurso + hoja 9'),
    ('Backtest simple de tu estrategia con datos reales', 'Hojas 1-5 con datos reales'), ('Simulacro completo de 1 semana', 'Hojas 9 y 12'),
    ('Repaso final + Quiz completo + ajustes', 'Quiz + Resumen Express')]
for k, (tema, mat) in enumerate(plan):
    rr = 3 + k
    ws.write(rr, 0, k + 1, num); ws.write(rr, 1, tema, txt); ws.write(rr, 2, mat, txt); ws.write(rr, 3, '', inp)
    ws.data_validation(rr, 3, rr, 3, {'validate': 'list', 'source': ['Si', 'No']})
ws.write('F3', 'AVANCE', h); ws.write_formula('F4', f'=COUNTIF(D4:D{3+len(plan)},"Si")/{len(plan)}', pct_b)
ws.conditional_format(f'D4:D{3+len(plan)}', {'type': 'cell', 'criteria': '==', 'value': '"Si"', 'format': F(bg_color='#63BE7B')})

wb.close()
print('OK', OUT)
