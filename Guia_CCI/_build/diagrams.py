"""Genera esquemas (SVG) para la guia CCI: HTML combinado + PNG para Word."""
import html, math, os, subprocess

OUT = '/projects/sandbox/Guia_CCI'
PNG_DIR = f'{OUT}/04_Esquemas_PNG'
os.makedirs(PNG_DIR, exist_ok=True)
CHROME = '/opt/playwright/chromium_headless_shell-1232/chrome-headless-shell-linux64/chrome-headless-shell'
FONT = "'Noto Sans', 'Segoe UI', Arial, sans-serif"
NAVY = '#1F3864'
PAL = ['#2E75B6', '#C55A11', '#548235', '#7030A0', '#BF8F00', '#C00000', '#00838F', '#5B6770']

def esc(s):
    return html.escape(s)

def text_lines(x, y, lines, size=14, color='#222', weight='normal', anchor='middle', lh=1.25):
    out = []
    y0 = y - (len(lines) - 1) * size * lh / 2
    for i, l in enumerate(lines):
        out.append(f'<text x="{x:.1f}" y="{y0 + i*size*lh:.1f}" font-size="{size}" fill="{color}" font-weight="{weight}" '
                   f'text-anchor="{anchor}" dominant-baseline="middle" font-family="{FONT}">{esc(l)}</text>')
    return ''.join(out)

def box(x, y, w, h, lines, fill='#FFFFFF', stroke=NAVY, color='#222', size=14, weight='normal', rx=10, sw=2):
    return (f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            + text_lines(x, y, lines, size, color, weight))

def diamond(x, y, w, h, lines, fill='#FFF2CC', stroke='#BF8F00', size=13):
    pts = f'{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}'
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>' + text_lines(x, y, lines, size, '#222', 'bold')

def arrow(x1, y1, x2, y2, label=None, color='#444', lx=0, ly=0):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#ah)"/>'
    if label:
        s += f'<text x="{(x1+x2)/2+lx}" y="{(y1+y2)/2+ly}" font-size="13" font-weight="bold" fill="{color}" text-anchor="middle" font-family="{FONT}">{esc(label)}</text>'
    return s

def path_arrow(d, color='#444', label=None, lx=0, ly=0):
    s = f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" marker-end="url(#ah)"/>'
    if label:
        s += f'<text x="{lx}" y="{ly}" font-size="13" font-weight="bold" fill="{color}" text-anchor="middle" font-family="{FONT}">{esc(label)}</text>'
    return s

def svg(w, h, body, title=None):
    t = text_lines(w/2, 32, [title], 22, NAVY, 'bold') if title else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker></defs>'
            f'<rect width="{w}" height="{h}" fill="white"/>{t}{body}</svg>')

DIAGS = []   # (slug, titulo, descripcion, svg, w, h)

# ------------------------------------------------------------------ 1. MAPA MENTAL
MM = ('CCI', ['Concurso Carteras', 'de Inversión'], [
    ('El concurso', ['Bolsa de Santiago (nuam)', '$20 MM ficticios', 'Acciones (hist. del IPSA)', 'Comisión ~0,5% por operación', 'Equipos de hasta 5', 'Marcha blanca + ~8 semanas', 'Ranking por rentabilidad']),
    ('Mercado chileno', ['S&P IPSA (30 acciones)', 'Sectores y pesos', 'Liquidez y spread', 'Órdenes y horario', 'Hechos esenciales (CMF)', 'Dividendos y fecha ex']),
    ('Macro', ['Precio del cobre', 'Dólar / peso', 'TPM del Banco Central', 'Inflación y UF', 'China y la Fed', 'Política y regulación']),
    ('Riesgo y retorno', ['Retorno simple vs log', 'Volatilidad × raíz(252)', 'Correlación', 'Diversificación', 'Drawdown', 'Colas gordas']),
    ('Teoría de carteras', ['Markowitz', 'Frontera eficiente', 'CAPM y beta', 'SML / CML', 'Sharpe · Treynor · Jensen', 'Tracking error']),
    ('Análisis', ['Fundamental: P/U, P/VL', 'EV/EBITDA, ROE, DY', 'Resultados trimestrales', 'Técnico: MM, RSI, MACD', 'Momentum', 'Catalizadores']),
    ('Estrategia de torneo', ['Premio convexo', 'Volatilidad y probabilidad', 'Core–satélite', 'Tamaño de posiciones', 'Costo de rotar', 'Plan según ranking']),
    ('Psicología', ['Sobreconfianza', 'Efecto disposición', 'Aversión a pérdidas', 'FOMO y efecto manada', 'Anclaje', 'Diario de decisiones']),
])

def mindmap():
    W, H = 1800, 1180
    cx, cy = W/2, H/2 + 10
    branches = MM[2]
    left, right = branches[:4], branches[4:]
    body = []
    leaf_h, gap = 30, 8
    def side(brs, sign, colors):
        nonlocal body
        blocks = [len(b[1]) * (leaf_h + gap) + 30 for b in brs]
        total = sum(blocks)
        y = cy - total/2
        for (name, leaves), bh, col in zip(brs, blocks, colors):
            by = y + bh/2
            bx = cx + sign * 330
            # rama central -> nodo
            body.append(f'<path d="M{cx + sign*120},{cy} C{cx + sign*220},{cy} {bx - sign*180},{by} {bx - sign*95},{by}" stroke="{col}" stroke-width="5" fill="none"/>')
            body.append(box(bx, by, 190, 46, [name], fill=col, stroke=col, color='white', size=16, weight='bold', rx=23))
            ly = by - (len(leaves)-1)*(leaf_h+gap)/2
            for lf in leaves:
                lx = bx + sign * 290
                body.append(f'<path d="M{bx + sign*95},{by} C{bx + sign*140},{by} {lx - sign*150},{ly} {lx - sign*105},{ly}" stroke="{col}" stroke-width="2" fill="none" opacity="0.8"/>')
                body.append(box(lx, ly, 210, leaf_h, [lf], fill='white', stroke=col, color='#222', size=12.5, rx=14, sw=1.5))
                ly += leaf_h + gap
            y += bh
    side(left, -1, PAL[:4]); side(right, 1, PAL[4:])
    body.append(f'<ellipse cx="{cx}" cy="{cy}" rx="125" ry="62" fill="{NAVY}"/>')
    body.append(text_lines(cx, cy - 14, ['CCI'], 30, 'white', 'bold'))
    body.append(text_lines(cx, cy + 22, MM[1], 13, 'white', 'normal'))
    return svg(W, H, ''.join(body), 'Mapa mental: todo lo que hay que dominar para el CCI'), W, H
s, w, hh = mindmap()
DIAGS.append(('01_mapa_mental', 'Mapa mental general', 'Los 8 bloques de conocimiento del concurso y sus conceptos clave.', s, w, hh))

# ------------------------------------------------------------------ 2. LINEA DE TIEMPO
def timeline():
    W, H = 1700, 520
    b = []
    y = 250
    b.append(f'<line x1="80" y1="{y}" x2="{W-80}" y2="{y}" stroke="{NAVY}" stroke-width="6"/>')
    phases = [
        (80, 420, 'PREPARACIÓN', '#5B6770', ['Leer bases', 'Estudiar teoría', 'Armar equipo y roles', 'Escribir estrategia']),
        (420, 760, 'MARCHA BLANCA', '#BF8F00', ['Probar la plataforma', 'Medir comisión y ejecución', 'Ensayar la estrategia', 'No cuenta para el ranking']),
        (760, 1180, 'CONCURSO OFICIAL (S1–S4)', '#2E75B6', ['Construir cartera inicial', 'Temporada de resultados', 'Revisión semanal', 'Ajustes por catalizadores']),
        (1180, 1500, 'OFICIAL (S5–S8)', '#C00000', ['Mirar el ranking', 'Ajustar riesgo según posición', 'Evitar rotar por impulso', 'Cierre disciplinado']),
        (1500, 1620, 'CIERRE', '#548235', ['Premiación', 'Post-mortem']),
    ]
    for x1, x2, name, col, items in phases:
        b.append(f'<rect x="{x1}" y="{y-22}" width="{x2-x1}" height="44" fill="{col}"/>')
        b.append(text_lines((x1+x2)/2, y, [name], 14 if x2-x1 > 200 else 12, 'white', 'bold'))
        for i, it in enumerate(items):
            b.append(text_lines((x1+x2)/2, y + 60 + i*26, ['• ' + it], 13, '#222'))
    marks = [(420, 'Inicio inscripciones', 'ago–sep (hist.)'), (760, 'Partida oficial', 'oct (hist.)'), (1500, 'Fin', 'nov–dic (hist.)')]
    for x, l1, l2 in marks:
        b.append(f'<line x1="{x}" y1="{y-90}" x2="{x}" y2="{y-24}" stroke="#444" stroke-width="2" stroke-dasharray="5,4"/>')
        b.append(text_lines(x, y - 120, [l1, l2], 13, '#222', 'bold'))
    b.append(text_lines(W/2, H - 30, ['Fechas históricas: 2023 marcha blanca 21-ago a 9-oct y oficial 10-oct a 1-dic (~8 semanas). Confirmar fechas en las bases vigentes.'], 13, '#7F7F7F'))
    return svg(W, H, ''.join(b), 'Línea de tiempo del concurso y qué hacer en cada fase'), W, H
s, w, hh = timeline(); DIAGS.append(('02_linea_tiempo', 'Línea de tiempo del concurso', 'Fases del CCI y tareas en cada una.', s, w, hh))

# ------------------------------------------------------------------ 3. PROCESO DE CONSTRUCCION DE CARTERA
def proceso():
    W, H = 1700, 640
    steps = [('1', 'Leer las bases', ['universo, comisión,', 'límites, ranking']), ('2', 'Diagnóstico macro', ['cobre, dólar, TPM,', 'inflación, China']),
             ('3', 'Visión sectorial', ['qué sectores ganan', 'con ese escenario']), ('4', 'Filtrar acciones', ['liquidez + screener', 'fundamental']),
             ('5', 'Catalizadores', ['resultados, dividendos,', 'noticias en 8 semanas']), ('6', 'Confirmar timing', ['tendencia, momentum,', 'RSI, soportes']),
             ('7', 'Tamaño de posiciones', ['core–satélite,', 'límite por acción']), ('8', 'Ejecutar', ['pocas órdenes,', 'cuidar comisión']),
             ('9', 'Monitorear', ['diario de operaciones,', 'stops, hechos esenciales']), ('10', 'Revisar y ajustar', ['semanal vs IPSA', 'y vs ranking'])]
    b = []
    per = 5; bw, bh = 270, 150
    for i, (n, t, d) in enumerate(steps):
        row, col = divmod(i, per)
        if row == 1: col = per - 1 - col
        x = 170 + col * 340; y = 190 + row * 270
        c = PAL[i % len(PAL)]
        b.append(f'<rect x="{x-bw/2}" y="{y-bh/2}" width="{bw}" height="{bh}" rx="14" fill="white" stroke="{c}" stroke-width="3"/>')
        b.append(f'<circle cx="{x-bw/2+30}" cy="{y-bh/2+30}" r="20" fill="{c}"/>' + text_lines(x-bw/2+30, y-bh/2+31, [n], 16, 'white', 'bold'))
        b.append(text_lines(x + 15, y - 35, [t], 17, c, 'bold'))
        b.append(text_lines(x, y + 25, d, 14, '#333'))
        if i < len(steps) - 1:
            if i == per - 1:
                b.append(arrow(x, y + bh/2, x, y + 270 - bh/2 - 4))
            elif row == 0:
                b.append(arrow(x + bw/2, y, x + 340 - bw/2 - 4, y))
            else:
                b.append(arrow(x - bw/2, y, x - 340 + bw/2 + 4, y))
    b.append(text_lines(W/2, H - 30, ['El ciclo 9-10 se repite cada semana: vuelve al paso 2 si cambia el escenario.'], 14, '#7F7F7F'))
    return svg(W, H, ''.join(b), 'Proceso de construcción y gestión de la cartera (10 pasos)'), W, H
s, w, hh = proceso(); DIAGS.append(('03_proceso_cartera', 'Proceso de construcción de cartera', 'Los 10 pasos, de las bases a la revisión semanal.', s, w, hh))

# ------------------------------------------------------------------ 4. FLUJO DE DECISION DE UNA OPERACION
def decision():
    W, H = 1500, 1120
    b = []
    X = 560
    b.append(box(X, 90, 360, 56, ['Idea de operación'], fill=NAVY, stroke=NAVY, color='white', size=17, weight='bold'))
    qs = [(200, ['¿Tesis clara en', '1–2 frases?']), (350, ['¿Catalizador dentro', 'del concurso?']), (500, ['¿Movimiento esperado', '> 3× el costo (~3%)?']),
          (650, ['¿Respeta límite por', 'acción y correlación?']), (800, ['¿Stop y objetivo', 'definidos?'])]
    nos = ['Escribe la tesis o descarta', 'Sin catalizador: espera / descarta', 'No compensa la comisión: no operes', 'Reduce el tamaño o elige otra', 'Defínelos antes de entrar']
    prev = 118
    for (y, q), no in zip(qs, nos):
        b.append(arrow(X, prev, X, y - 52))
        b.append(diamond(X, y, 330, 100, q))
        b.append(arrow(X + 165, y, 1010, y, 'NO', '#C00000', 0, -8))
        b.append(box(1180, y, 330, 54, [no], fill='#FCE4D6', stroke='#C00000', size=14))
        b.append(text_lines(X + 22, y + 66, ['SÍ'], 13, '#548235', 'bold'))
        prev = y + 50
    b.append(arrow(X, prev, X, 905))
    b.append(box(X, 935, 400, 56, ['EJECUTAR y registrar en el diario'], fill='#548235', stroke='#548235', color='white', size=16, weight='bold'))
    b.append(arrow(X, 963, X, 1015))
    b.append(box(X, 1045, 520, 56, ['Monitorear: ¿se cumple la tesis? Mantener / ajustar / salir'], fill='#E2EFDA', stroke='#548235', size=14))
    b.append(text_lines(170, 520, ['Regla de oro:', 'si dudas, no operes.', 'Cada operación cuesta', '~0,5% de entrada', 'y ~0,5% de salida.'], 15, NAVY, 'bold'))
    return svg(W, H, ''.join(b), 'Flujo de decisión antes de cada operación'), W, H
s, w, hh = decision(); DIAGS.append(('04_flujo_decision', 'Flujo de decisión de una operación', 'Cinco filtros que debe pasar toda compra o venta.', s, w, hh))

# ------------------------------------------------------------------ 5. CADENA MACRO -> SECTORES
def macro():
    W, H = 1700, 900
    b = []
    drivers = [('Sube el cobre', '#C55A11'), ('Sube el dólar', '#2E75B6'), ('Baja la TPM', '#548235'), ('Sube inflación / UF', '#7030A0'), ('China crece', '#BF8F00'), ('Suben tasas EE.UU.', '#C00000')]
    sectors = [('Minería / materiales', 'Exportadores, venden en USD'), ('Forestal y celulosa', 'Exportadores (precio celulosa)'), ('Bancos', 'Margen, carteras en UF, riesgo crédito'),
               ('Retail y consumo', 'Demanda interna, tasas de crédito'), ('Utilities / energía', 'Defensivas; sensibles a tasas'), ('Inmobiliario / centros comerciales', 'Sensibles a tasas y UF'),
               ('Aerolínea / transporte', 'Costo del combustible y dólar')]
    ys_d = [160 + i * 115 for i in range(len(drivers))]
    ys_s = [140 + i * 105 for i in range(len(sectors))]
    for (d, c), y in zip(drivers, ys_d):
        b.append(box(230, y, 300, 62, [d], fill=c, stroke=c, color='white', size=17, weight='bold'))
    for (sname, sdesc), y in zip(sectors, ys_s):
        b.append(box(1380, y, 470, 72, [sname, sdesc], fill='white', stroke=NAVY, size=14))
    G, R = '#548235', '#C00000'
    links = [(0, 0, G), (0, 3, G), (1, 0, G), (1, 1, G), (1, 6, R), (1, 3, R), (2, 3, G), (2, 5, G), (2, 4, G), (2, 2, R),
             (3, 2, G), (3, 5, G), (3, 3, R), (4, 0, G), (4, 1, G), (5, 4, R), (5, 5, R), (5, 3, R)]
    for di, si, c in links:
        y1, y2 = ys_d[di], ys_s[si]
        b.append(f'<path d="M380,{y1} C750,{y1} 800,{y2} 1141,{y2}" stroke="{c}" stroke-width="2.4" fill="none" opacity="0.75" marker-end="url(#ah)"/>')
    b.append(f'<line x1="560" y1="{H-70}" x2="610" y2="{H-70}" stroke="{G}" stroke-width="4"/>' + text_lines(700, H-70, ['efecto positivo'], 14, G, 'bold'))
    b.append(f'<line x1="830" y1="{H-70}" x2="880" y2="{H-70}" stroke="{R}" stroke-width="4"/>' + text_lines(970, H-70, ['efecto negativo'], 14, R, 'bold'))
    b.append(text_lines(W/2, H-32, ['Relaciones típicas, no reglas fijas: siempre revisa la exposición concreta de cada empresa (moneda en que reporta, deuda, mercados).'], 13, '#7F7F7F'))
    return svg(W, H, ''.join(b), 'Cadena de transmisión: variables macro y sectores del IPSA'), W, H
s, w, hh = macro(); DIAGS.append(('05_macro_sectores', 'Macro y sectores', 'Cómo las variables macro mueven a los sectores de la bolsa chilena.', s, w, hh))

# ------------------------------------------------------------------ 6. RIESGO Y DIVERSIFICACION (grafico)
def diversif():
    W, H = 1500, 760
    b = []
    x0, y0, x1, y1 = 140, 120, 900, 640
    sig, rho = 0.35, 0.30
    def sp(n): return math.sqrt(sig**2/n + (1-1/n)*rho*sig**2)
    mx = sig * 1.05
    b.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#222" stroke-width="2"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#222" stroke-width="2"/>')
    pts = []
    for n in range(1, 31):
        X = x0 + (n-1)/29*(x1-x0); Y = y1 - sp(n)/mx*(y1-y0); pts.append(f'{X:.1f},{Y:.1f}')
    sysY = y1 - math.sqrt(rho)*sig/mx*(y1-y0)
    b.append(f'<rect x="{x0}" y="{sysY}" width="{x1-x0}" height="{y1-sysY}" fill="#DDEBF7"/>')
    b.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#C00000" stroke-width="4"/>')
    b.append(f'<line x1="{x0}" y1="{sysY}" x2="{x1}" y2="{sysY}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="8,5"/>')
    for n in [1, 5, 10, 15, 20, 25, 30]:
        X = x0 + (n-1)/29*(x1-x0); b.append(text_lines(X, y1 + 22, [str(n)], 13))
    for v in [0, 0.1, 0.2, 0.3]:
        Y = y1 - v/mx*(y1-y0); b.append(text_lines(x0 - 30, Y, [f'{int(v*100)}%'], 13))
    b.append(text_lines((x0+x1)/2, y1 + 55, ['Número de acciones en la cartera (pesos iguales)'], 15, '#222', 'bold'))
    b.append(f'<text x="45" y="{(y0+y1)/2}" font-size="15" font-weight="bold" transform="rotate(-90 45 {(y0+y1)/2})" text-anchor="middle" font-family="{FONT}">Volatilidad de la cartera</text>')
    b.append(text_lines(620, sysY + 60, ['RIESGO SISTEMÁTICO (de mercado)', 'no se elimina diversificando; se paga con la prima (beta)'], 14, NAVY, 'bold'))
    b.append(text_lines(560, y0 + 60, ['RIESGO IDIOSINCRÁTICO', 'se elimina diversificando'], 14, '#C00000', 'bold'))
    b.append(text_lines(1200, 230, ['Lectura del gráfico'], 18, NAVY, 'bold'))
    for i, l in enumerate([f'Supuesto: cada acción σ = {int(sig*100)}%,', f'correlación promedio ρ = {rho}.', '',
                           f'1 acción: {sp(1)*100:.0f}%', f'5 acciones: {sp(5)*100:.1f}%', f'10 acciones: {sp(10)*100:.1f}%', f'30 acciones: {sp(30)*100:.1f}%',
                           f'Límite: raíz(ρ)·σ = {math.sqrt(rho)*sig*100:.1f}%', '', 'Con 8–10 acciones ya se', 'captura casi toda la reducción.',
                           'En un torneo, concentrar', '= aceptar más riesgo propio', 'a cambio de opciones de ganar.']):
        b.append(text_lines(1200, 280 + i*28, [l], 15, '#222'))
    b.append(text_lines(W/2, H - 28, ['Fórmula: σp² = σ²/n + (1 − 1/n)·ρ·σ²'], 15, '#7F7F7F', 'bold'))
    return svg(W, H, ''.join(b), 'Diversificación: el riesgo que se elimina y el que no'), W, H
s, w, hh = diversif(); DIAGS.append(('06_diversificacion', 'Diversificación', 'Riesgo de la cartera según el número de acciones.', s, w, hh))

# ------------------------------------------------------------------ 7. CAPM / SML / CML
def capm():
    W, H = 1500, 720
    b = []
    def axes(ox, title):
        x0, y0, x1, y1 = ox, 130, ox + 560, 590
        b.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#222" stroke-width="2"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#222" stroke-width="2"/>')
        b.append(text_lines((x0+x1)/2, y0 - 30, [title], 18, NAVY, 'bold'))
        return x0, y0, x1, y1
    # SML
    x0, y0, x1, y1 = axes(110, 'SML: retorno exigido vs beta (CAPM)')
    rf, erp = 0.0475, 0.0533
    def P(beta, ret): return x0 + beta/2*(x1-x0), y1 - ret/0.16*(y1-y0)
    a = P(0, rf); c = P(2, rf + 2*erp)
    b.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{c[0]}" y2="{c[1]}" stroke="#2E75B6" stroke-width="4"/>')
    m = P(1, rf+erp); b.append(f'<circle cx="{m[0]}" cy="{m[1]}" r="9" fill="{NAVY}"/>' + text_lines(m[0] - 80, m[1] - 22, ['Mercado (β = 1)'], 13, NAVY, 'bold'))
    u = P(1.3, 0.135); b.append(f'<circle cx="{u[0]}" cy="{u[1]}" r="8" fill="#548235"/>' + text_lines(u[0], u[1] - 22, ['Sobre la SML: α > 0 (barata)'], 13, '#548235', 'bold'))
    o = P(1.5, 0.095); b.append(f'<circle cx="{o[0]}" cy="{o[1]}" r="8" fill="#C00000"/>' + text_lines(o[0]+20, o[1] + 26, ['Bajo la SML: α < 0 (cara)'], 13, '#C00000', 'bold'))
    b.append(text_lines(a[0] + 30, a[1] + 18, ['rf'], 14, '#222', 'bold'))
    b.append(text_lines((x0+x1)/2, y1 + 32, ['Beta (riesgo sistemático)'], 14, '#222', 'bold'))
    b.append(text_lines((x0+x1)/2, y1 + 62, ['E(Ri) = rf + βi · [E(Rm) − rf]'], 16, NAVY, 'bold'))
    # CML / frontera
    x0, y0, x1, y1 = axes(800, 'Frontera eficiente y CML')
    def Q(s_, r_): return x0 + s_/0.40*(x1-x0), y1 - r_/0.16*(y1-y0)
    pts = []
    for k in range(0, 41):
        t = -1 + 2*k/40
        s_ = 0.12 + 0.20*t*t; r_ = 0.085 + 0.055*t
        pts.append('%.1f,%.1f' % Q(s_, r_))
    b.append(f'<polyline points="{" ".join(pts[20:])}" fill="none" stroke="#2E75B6" stroke-width="4"/>')
    b.append(f'<polyline points="{" ".join(pts[:21])}" fill="none" stroke="#9DC3E6" stroke-width="3" stroke-dasharray="6,5"/>')
    rfp = Q(0, rf)
    _best = max(((0.12 + 0.20*t*t, 0.085 + 0.055*t) for t in [k/1000 for k in range(0, 1001)]), key=lambda p_: (p_[1]-rf)/p_[0])
    tg = Q(*_best)
    slope = (tg[1]-rfp[1])/(tg[0]-rfp[0]); endy = y0 + 20; endx = rfp[0] + (endy-rfp[1])/slope
    b.append(f'<line x1="{rfp[0]}" y1="{rfp[1]}" x2="{endx}" y2="{endy}" stroke="#C55A11" stroke-width="3"/>')
    b.append(f'<circle cx="{tg[0]}" cy="{tg[1]}" r="9" fill="#C55A11"/>' + text_lines(tg[0] + 105, tg[1] + 28, ['Cartera tangente (máx. Sharpe)'], 13, '#C55A11', 'bold'))
    mv = Q(0.12, 0.085); b.append(f'<circle cx="{mv[0]}" cy="{mv[1]}" r="7" fill="{NAVY}"/>' + text_lines(mv[0] + 85, mv[1] + 6, ['Mínima varianza'], 13, NAVY, 'bold'))
    b.append(text_lines(endx + 30, endy + 10, ['CML'], 15, '#C55A11', 'bold'))
    b.append(text_lines(rfp[0] + 28, rfp[1] + 18, ['rf'], 14, '#222', 'bold'))
    b.append(text_lines((x0+x1)/2, y1 + 32, ['Volatilidad (riesgo total σ)'], 14, '#222', 'bold'))
    b.append(text_lines((x0+x1)/2, y1 + 62, ['Pendiente de la CML = Sharpe de la tangente'], 16, NAVY, 'bold'))
    return svg(W, H, ''.join(b), 'CAPM, SML y frontera eficiente'), W, H
s, w, hh = capm(); DIAGS.append(('07_capm_frontera', 'CAPM y frontera eficiente', 'Las dos gráficas centrales de la teoría de carteras.', s, w, hh))

# ------------------------------------------------------------------ 8. ESTRATEGIA SEGUN RANKING
def ranking():
    W, H = 1600, 760
    b = []
    cols = [('Vas en el TOP del ranking', '#548235', ['Proteger la ventaja', 'Bajar volatilidad', 'Parecerse a los que te persiguen', 'Menos operaciones', 'Evitar apuestas binarias']),
            ('Vas en la MITAD', '#BF8F00', ['Mantener la tesis si sigue vigente', 'Buscar 1–2 catalizadores', 'Subir convicción, no rotación', '¿Tu riesgo alcanza para el top?']),
            ('Vas ATRÁS', '#C00000', ['Lo seguro no te sirve para ganar', 'Concentrar en mejores ideas', 'Aceptar más volatilidad / beta', 'Hacerlo temprano, no el último día', 'Sin violar las bases'])]
    for i, (t, c, items) in enumerate(cols):
        x = 280 + i * 520
        b.append(f'<rect x="{x-235}" y="110" width="470" height="80" rx="12" fill="{c}"/>' + text_lines(x, 150, [t], 19, 'white', 'bold'))
        b.append(f'<rect x="{x-235}" y="205" width="470" height="330" rx="12" fill="white" stroke="{c}" stroke-width="3"/>')
        for j, it in enumerate(items):
            b.append(text_lines(x - 210, 250 + j * 58, ['• ' + it], 16, '#222', anchor='start'))
    b.append(f'<rect x="45" y="570" width="1510" height="140" rx="12" fill="#DDEBF7"/>')
    b.append(text_lines(W/2, 605, ['Por qué: en un torneo se premia la POSICIÓN RELATIVA, no el retorno ajustado por riesgo.'], 17, NAVY, 'bold'))
    b.append(text_lines(W/2, 640, ['Quien lidera gana si "no pasa nada"; quien va atrás necesita que pase algo distinto a lo que tienen los demás.'], 15, '#222'))
    b.append(text_lines(W/2, 675, ['(Literatura: torneos de fondos mutuos, Brown, Harlow y Starks, 1996). Gestiona el riesgo de ruina: un −40% temprano te saca del juego.'], 14, '#555'))
    return svg(W, H, ''.join(b), 'Ajustar el riesgo según tu posición en el ranking'), W, H
s, w, hh = ranking(); DIAGS.append(('08_estrategia_ranking', 'Estrategia según el ranking', 'Cómo cambia la gestión del riesgo según vas arriba, al medio o atrás.', s, w, hh))

# ------------------------------------------------------------------ 9. CORE - SATELITE + ROLES DE EQUIPO
def core():
    W, H = 1600, 700
    b = []
    cx, cy = 380, 380
    b.append(f'<circle cx="{cx}" cy="{cy}" r="250" fill="#DDEBF7" stroke="#2E75B6" stroke-width="3"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="140" fill="{NAVY}"/>')
    b.append(text_lines(cx, cy - 10, ['NÚCLEO (core)', '50–70%'], 20, 'white', 'bold'))
    b.append(text_lines(cx, cy + 50, ['4–6 acciones líquidas,', 'diversificadas por sector'], 13, 'white'))
    for ang, lab in [(-60, 'Satélite 1'), (20, 'Satélite 2'), (110, 'Satélite 3'), (200, 'Satélite 4')]:
        x = cx + 200*math.cos(math.radians(ang)); y = cy + 200*math.sin(math.radians(ang))
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="44" fill="#C55A11"/>' + text_lines(x, y, [lab], 13, 'white', 'bold'))
    b.append(text_lines(cx, 690 - 25, ['SATÉLITES 30–50%: 2–4 apuestas de alta convicción con catalizador'], 14, '#C55A11', 'bold'))
    # roles
    b.append(text_lines(1150, 110, ['Roles en un equipo de hasta 5'], 20, NAVY, 'bold'))
    roles = [('Estratega macro', 'cobre, dólar, TPM; define el escenario', '#2E75B6'), ('Analista de sectores', 'screener, resultados, valoración', '#548235'),
             ('Analista técnico / timing', 'tendencia, momentum, puntos de entrada', '#7030A0'), ('Gestor de riesgo y registro', 'pesos, límites, diario, comisiones', '#C55A11'),
             ('Abogado del diablo', 'ataca cada tesis antes de operar', '#C00000')]
    for i, (r, d, c) in enumerate(roles):
        y = 175 + i * 95
        b.append(f'<rect x="800" y="{y-38}" width="700" height="76" rx="12" fill="white" stroke="{c}" stroke-width="3"/>')
        b.append(f'<rect x="800" y="{y-38}" width="16" height="76" rx="6" fill="{c}"/>')
        b.append(text_lines(840, y - 13, [r], 17, c, 'bold', anchor='start'))
        b.append(text_lines(840, y + 16, [d], 14, '#333', anchor='start'))
    return svg(W, H, ''.join(b), 'Estructura core–satélite y roles del equipo'), W, H
s, w, hh = core(); DIAGS.append(('09_core_satelite_roles', 'Core–satélite y roles', 'Cómo repartir el capital y el trabajo del equipo.', s, w, hh))

# ------------------------------------------------------------------ 10. INDICADORES (CHEAT VISUAL)
def ratios():
    W, H = 1600, 860
    b = []
    groups = [
        ('RETORNO Y RIESGO', '#2E75B6', ['Retorno = (P1 + D − P0) / P0', 'Log-retorno = ln(P1 / P0)', 'Vol. anual = σ diaria × raíz(252)', 'Ret. anual = (1 + r̄)^252 − 1', 'Drawdown = P / máx(P) − 1']),
        ('CARTERAS', '#548235', ['E(Rp) = Σ wi · E(Ri)', 'σp² = Σ Σ wi wj σij', '2 activos: w1²σ1² + w2²σ2² + 2w1w2ρσ1σ2', 'βp = Σ wi · βi', 'ρ = σ12 / (σ1 · σ2)']),
        ('DESEMPEÑO', '#C55A11', ['Sharpe = (Rp − rf) / σp', 'Treynor = (Rp − rf) / βp', 'α Jensen = Rp − [rf + βp(Rm − rf)]', 'Info ratio = (Rp − Rb) / TE', 'TE = σ(Rp − Rb)']),
        ('VALORACIÓN', '#7030A0', ['P/U = Precio / Utilidad por acción', 'P/VL = Precio / Valor libro por acción', 'Div. yield = Dividendo / Precio', 'EV/EBITDA = (Cap. + deuda neta) / EBITDA', 'ROE = Utilidad / Patrimonio']),
        ('TÉCNICO', '#BF8F00', ['SMA n = promedio de n cierres', 'RSI = 100 − 100 / (1 + G/P) (promedios)', 'MACD = EMA12 − EMA26 (señal EMA9)', 'Bollinger = SMA20 ± 2σ', 'Cruce dorado: SMA50 > SMA200']),
        ('COSTOS DEL CONCURSO', '#C00000', ['Comisión c: ~0,5% por lado', 'Empate ida y vuelta = (1+c)/(1−c) − 1', 'aprox. 1,005% con c = 0,5%', 'n rotaciones: 1 − ((1−c)/(1+c))^n', '10 rotaciones: aprox. −9,5%']),
    ]
    for i, (t, c, items) in enumerate(groups):
        r, col = divmod(i, 3)
        x = 40 + col * 515; y = 80 + r * 380
        b.append(f'<rect x="{x}" y="{y}" width="495" height="350" rx="14" fill="white" stroke="{c}" stroke-width="3"/>')
        b.append(f'<rect x="{x}" y="{y}" width="495" height="56" rx="14" fill="{c}"/>')
        b.append(text_lines(x + 247, y + 29, [t], 18, 'white', 'bold'))
        for j, it in enumerate(items):
            b.append(text_lines(x + 22, y + 95 + j * 52, [it], 15.5, '#222', anchor='start'))
    return svg(W, H, ''.join(b), 'Fórmulas esenciales en una sola página'), W, H
s, w, hh = ratios(); DIAGS.append(('10_formulas', 'Fórmulas esenciales', 'Hoja de fórmulas visual para repasar.', s, w, hh))

# ------------------------------------------------------------------ salida
def render_png(slug, svgtxt, w, h):
    f = f'/tmp/diag_{slug}.html'
    open(f, 'w', encoding='utf-8').write(f'<html><head><meta charset="utf-8"><style>body{{margin:0}}</style></head><body>{svgtxt}</body></html>')
    out = f'{PNG_DIR}/{slug}.png'
    subprocess.run([CHROME, '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                    f'--screenshot={out}', f'--window-size={w},{h}', f'file://{f}'], capture_output=True, timeout=120)
    return out

if __name__ == '__main__':
    for slug, t, d, s_, w_, h_ in DIAGS:
        print(render_png(slug, s_, w_, h_))
    secs = ''.join(f'<section id="{slug}"><h2>{i+1}. {esc(t)}</h2><p>{esc(d)}</p><div class="fig">{s_}</div></section>'
                   for i, (slug, t, d, s_, w_, h_) in enumerate(DIAGS))
    nav = ''.join(f'<a href="#{slug}">{i+1}. {esc(t)}</a>' for i, (slug, t, d, s_, w_, h_) in enumerate(DIAGS))
    page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>CCI - Mapas y esquemas</title>
<style>body{{font-family:{FONT};margin:0;background:#F4F6FA;color:#222}}header{{background:{NAVY};color:white;padding:18px 28px}}
header h1{{margin:0;font-size:24px}}nav{{position:sticky;top:0;background:white;padding:10px 28px;box-shadow:0 2px 6px #0002;display:flex;flex-wrap:wrap;gap:8px 18px;z-index:2}}
nav a{{color:{NAVY};text-decoration:none;font-size:14px}}nav a:hover{{text-decoration:underline}}section{{background:white;margin:22px 28px;padding:16px 22px;border-radius:12px;box-shadow:0 1px 4px #0001}}
h2{{color:{NAVY};margin:4px 0}}.fig svg{{width:100%;height:auto}}p{{color:#555}}@media print{{nav{{display:none}}section{{page-break-after:always}}}}</style></head>
<body><header><h1>CCI · Mapas mentales y esquemas</h1><div>Funciona sin internet. Para imprimir: Ctrl+P (un esquema por página).</div></header><nav>{nav}</nav>{secs}</body></html>'''
    open(f'{OUT}/04_Mapas_y_Esquemas.html', 'w', encoding='utf-8').write(page)
    print('HTML OK')
