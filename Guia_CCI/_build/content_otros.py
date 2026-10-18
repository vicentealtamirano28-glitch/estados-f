from docx_lib import Doc

IMG = '/projects/sandbox/Guia_CCI/04_Esquemas_PNG'

# =====================================================================  RESUMEN EXPRESS
def resumen(path):
    d = Doc('Resumen Express CCI')
    d.p('RESUMEN EXPRESS · CONCURSO CARTERAS DE INVERSIÓN', size=18, bold=True, color='1F3864', space_after=40)
    d.p('Lo esencial en pocas páginas, para repasar antes de cada sesión de trading. Las reglas son de ediciones anteriores: confirmar en las bases vigentes.', italic=True, color='595959', size=9.5)
    d.h(2, '1. El juego en 6 líneas')
    d.bullets(['Organiza la **Bolsa de Santiago (nuam)**; simulador online con precios reales.', 'Capital ficticio de **$20.000.000**; históricamente, acciones del **IPSA**.',
               'Comisión histórica de **0,5% por operación** → una ida y vuelta cuesta **~1%**.', 'Equipos de **hasta 5** (2023); **marcha blanca** de ensayo + concurso oficial de **~8 semanas** (oct–dic).',
               'Gana la **mayor rentabilidad**; ganadores universitarios históricos: **30–65%** en ~8 semanas (IPSA 1,23% en 2016).', 'Es un **torneo**: importa la posición relativa, no el Sharpe.'])
    d.h(2, '2. Fórmulas que hay que saber')
    d.table(['Concepto', 'Fórmula'], [
        ['Retorno simple', 'R = (P₁ + D − P₀) / P₀'], ['Anualizar', 'Ret: (1 + r̄)^252 − 1   ·   Vol: σ × √252'],
        ['Cartera 2 activos', 'σp² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂'], ['Mínima varianza', 'w₁* = (σ₂² − ρσ₁σ₂) / (σ₁² + σ₂² − 2ρσ₁σ₂)'],
        ['CAPM', 'E(R) = rf + β · (E(Rm) − rf)'], ['Beta', 'β = Cov(Ri, Rm) / Var(Rm);   βp = Σ wᵢβᵢ'],
        ['Sharpe / Treynor', '(Rp − rf) / σp   ·   (Rp − rf) / βp'], ['Alfa de Jensen', 'Rp − [rf + βp(Rm − rf)]'],
        ['Recuperar una caída d', '1 / (1 − d) − 1   (−25% → +33%; −50% → +100%)'], ['Empate por comisión', '(1 + c)/(1 − c) − 1 ≈ 1,005% con c = 0,5%'],
        ['Costo de n rotaciones', '1 − ((1 − c)/(1 + c))^n   (10 → 9,5%)'], ['Tamaño de posición', 'Riesgo aceptado / distancia al stop (1% / 8% = 12,5%)'],
        ['Múltiplos', 'P/U · P/VL (=1/BME) · EV/EBITDA · Div. yield · ROE'], ['RSI', '100 − 100/(1 + G/P);  >70 sobrecompra, <30 sobreventa']], widths=[3, 7])
    d.h(2, '3. Probabilidad de superar +30% en 8 semanas (μ = 10% anual)')
    d.table(['Volatilidad anual', '15%', '20%', '40%', '60%'], [['P(R > 30%)', '~0%', '0,07%', '4,9%', '12,2%'], ['P(R < −10%)', '2,2%', '6,7%', '24,5%', '34,6%']], widths=[3, 1.7, 1.7, 1.7, 1.7])
    d.p('→ Sin aceptar volatilidad no se gana; con demasiada, se pierde fuerte. Equilibrio: **concentración con tesis + reglas de salida**.', size=10)
    d.h(2, '4. Estrategia recomendada')
    d.bullets(['**Core–satélite agresiva:** 50% núcleo (3–4 acciones líquidas de sectores distintos) + 50% satélites (2–3 apuestas con catalizador).',
               '**Límite por acción:** 25–35%. No dos acciones que sean la misma apuesta.', '**Catalizador estrella:** temporada de resultados del 3T (fines de octubre – noviembre) y PEAD.',
               '**Momentum:** preferir acciones con tendencia; entrar en retrocesos.', '**Operar poco:** solo si el movimiento esperado es ≥ 3× el costo (~3%).',
               '**Según ranking:** arriba → bajar riesgo; atrás → concentrar temprano, nunca todo el último día.'])
    d.h(2, '5. Checklist antes de operar')
    d.table(['#', 'Pregunta', '✓'], [[str(i + 1), q, '☐'] for i, q in enumerate([
        '¿Tesis escrita en 1–2 frases?', '¿Catalizador dentro del concurso?', '¿Revisé noticias y hechos esenciales (CMF)?', '¿Respeta el límite por acción y la correlación?',
        '¿Movimiento esperado ≥ 3× el costo?', '¿Stop y objetivo definidos?', '¿Estoy tranquilo (no FOMO, no "recuperar")?', '¿Registré la operación en el diario?'])], widths=[0.6, 8, 0.8])
    d.h(2, '6. Calendario a vigilar')
    d.bullets(['Resultados trimestrales de sus empresas (CMF).', 'Reunión de Política Monetaria del Banco Central.', 'IPC del INE (~día 8 de cada mes).', 'Fed (FOMC) y datos de EE.UU.',
               'Cobre, litio, celulosa, petróleo y dólar (diario).', 'Fechas ex-dividendo.'])
    d.h(2, '7. Los 6 mandamientos')
    d.numbered(['Leerás las bases antes que nada.', 'No copiarás el IPSA si quieres ganar.', 'No regalarás tu rentabilidad en comisiones.', 'Toda posición tendrá tesis, catalizador y salida.',
                'Cortarás las pérdidas y dejarás correr las ganancias con tesis vigente.', 'Ajustarás el riesgo según el ranking, con tiempo y por escrito.'])
    d.image(f'{IMG}/10_formulas.png', 16.5, 'Fórmulas esenciales (también en 04_Esquemas_PNG).')
    d.save(path, 'Resumen Express · CCI')

# =====================================================================  EJERCICIOS
EJ = [
    ('Retorno con dividendo', 'Compras una acción a $5.000. Un mes después vale $5.400 y pagó un dividendo de $100. ¿Cuál fue el retorno simple y el logarítmico?',
     ['R = (5.400 + 100 − 5.000) / 5.000 = 500 / 5.000 = **10,0%**', 'r = ln(5.500 / 5.000) = ln(1,10) = **9,53%**',
      'El log-retorno siempre es menor que el simple cuando hay ganancia; se suman en el tiempo.']),
    ('Asimetría de las pérdidas', 'Tu cartera cae 25% en la primera semana del concurso. ¿Cuánto debe subir para volver a $20 millones? ¿Y si hubiera caído 50%?',
     ['Alza necesaria = 1 / (1 − 0,25) − 1 = 1 / 0,75 − 1 = **33,3%**', 'Con −50%: 1 / 0,5 − 1 = **100%**', 'Lección: proteger el capital al inicio es crucial; la ruina temprana te saca del torneo.']),
    ('Anualizar', 'Una acción tiene retorno medio diario de 0,05% y volatilidad diaria de 1,2%. Calcula retorno y volatilidad anualizados (252 días). ¿Cuál es su volatilidad en un concurso de 40 días hábiles?',
     ['Retorno anual = (1,0005)^252 − 1 = **13,4%**', 'Volatilidad anual = 1,2% × √252 = 1,2% × 15,87 = **19,0%**', 'Volatilidad en 40 días = 1,2% × √40 = **7,6%**']),
    ('Cartera de dos activos', 'Activo 1: E = 12%, σ = 30%. Activo 2: E = 6%, σ = 15%. Correlación 0,2. Pesos 60% / 40%. Calcula E(Rp) y σp.',
     ['E(Rp) = 0,6 × 12% + 0,4 × 6% = **9,6%**', 'σp² = 0,36 × 0,09 + 0,16 × 0,0225 + 2 × 0,6 × 0,4 × 0,2 × 0,30 × 0,15 = 0,0324 + 0,0036 + 0,00432 = 0,04032',
      'σp = √0,04032 = **20,1%**', 'Sin diversificación (ρ = 1) sería 0,6 × 30% + 0,4 × 15% = 24%: la diversificación quitó ~4 puntos de riesgo.']),
    ('Cartera de mínima varianza', 'Con los datos del ejercicio 4, encuentra el peso del activo 1 que minimiza el riesgo, y el retorno y la volatilidad de esa cartera.',
     ['w₁* = (σ₂² − ρσ₁σ₂) / (σ₁² + σ₂² − 2ρσ₁σ₂) = (0,0225 − 0,009) / (0,09 + 0,0225 − 0,018) = 0,0135 / 0,0945 = **14,3%**',
      'E(Rp) = 0,143 × 12% + 0,857 × 6% = **6,86%**', 'σp = **14,3%** (menor que el 15% del activo menos riesgoso: efecto de la diversificación).',
      'Compruébalo en la hoja 4_Frontera_2A escribiendo estos datos en las celdas amarillas.']),
    ('Cobertura perfecta', 'Si la correlación entre los activos del ejercicio 4 fuera −1, ¿qué pesos dan riesgo cero y qué retorno se obtiene?',
     ['w₁ = σ₂ / (σ₁ + σ₂) = 0,15 / 0,45 = **33,3%**; w₂ = 66,7%', 'E(Rp) = 0,333 × 12% + 0,667 × 6% = **8,0%** sin riesgo.',
      'Si eso existiera, sería un arbitraje frente a una tasa libre de riesgo menor; por eso en la realidad no hay ρ = −1 entre acciones.']),
    ('CAPM', 'rf = 4,75%, prima por riesgo de mercado = 5,33%, beta = 1,3. ¿Qué retorno anual exige el CAPM? Si esperas que la acción rinda 15%, ¿cuál es su alfa esperado?',
     ['E(R) = 4,75% + 1,3 × 5,33% = **11,68%**', 'Alfa esperado = 15% − 11,68% = **+3,3%** → la acción estaría "barata" (sobre la SML).']),
    ('Beta de la cartera', 'Tienes 50% en una acción con β = 1,4, 30% en una con β = 0,6 y 20% en una con β = 1,0. Si el IPSA sube 5% en una semana, ¿cuánto esperas que suba tu cartera?',
     ['βp = 0,5 × 1,4 + 0,3 × 0,6 + 0,2 × 1,0 = **1,08**', 'Movimiento esperado = 1,08 × 5% = **5,4%** (sin contar el componente idiosincrático).']),
    ('Sharpe, Treynor y Jensen', 'Cartera: Rp = 18%, σ = 25%, β = 1,2. rf = 5%, Rm = 12%. Calcula las tres medidas.',
     ['Sharpe = (18% − 5%) / 25% = **0,52**', 'Treynor = (18% − 5%) / 1,2 = **10,8%**', 'Alfa de Jensen = 18% − [5% + 1,2 × (12% − 5%)] = 18% − 13,4% = **+4,6%**']),
    ('Costo de una operación', 'Compras 1.000 acciones a $5.000 con comisión de 0,5%. ¿Cuánto pagas en total? ¿A qué precio debes vender (también con 0,5%) para no perder?',
     ['Pago = 1.000 × 5.000 × 1,005 = **$5.025.000**', 'Precio de empate: 1.000 × P × 0,995 = 5.025.000 → P = **$5.050,25**', 'Alza necesaria = 1,005% → toda operación parte "perdiendo" 1%.']),
    ('El costo de la hiperactividad', 'Un equipo rota toda su cartera 10 veces durante el concurso. ¿Qué porcentaje del capital pierde solo en comisiones? ¿Y con 20 rotaciones?',
     ['Costo = 1 − (0,995 / 1,005)^10 = **9,5%**', 'Con 20: 1 − (0,995 / 1,005)^20 = **18,1%**', 'Ver hoja 10_Torneo. Si los ganadores logran 30–60%, el día-trading destruye buena parte del margen.']),
    ('Múltiplos', 'Precio $6.800; utilidad por acción $410; valor libro por acción $3.900; dividendo $240. Calcula P/U, P/VL, dividend yield y ROE.',
     ['P/U = 6.800 / 410 = **16,6x**', 'P/VL = 6.800 / 3.900 = **1,74x** (BME = 0,57)', 'Dividend yield = 240 / 6.800 = **3,5%**', 'ROE = 410 / 3.900 = **10,5%**']),
    ('EV/EBITDA', 'Precio $2.150; 2.500 millones de acciones; deuda neta $2.500.000 millones; EBITDA $900.000 millones. Calcula capitalización, EV y EV/EBITDA.',
     ['Capitalización = 2.150 × 2.500 millones = **$5.375.000 millones**', 'EV = 5.375.000 + 2.500.000 = **$7.875.000 millones**', 'EV/EBITDA = 7.875.000 / 900.000 = **8,75x**']),
    ('Probabilidad en el torneo', 'Con retorno esperado de 10% anual y un concurso de 8 semanas, ¿qué probabilidad hay de superar +30% con volatilidad anual de 20%? ¿Y con 60%?',
     ['Modelo lognormal: ln(1 + R) ~ N((μ − σ²/2)·T, σ·√T), con T = 8/52.', 'σ = 20%: P ≈ **0,07%**   ·   σ = 60%: P ≈ **12%**',
      'Pero P(perder más de 10%) sube de 6,7% a 34,6%. Ver hoja 10_Torneo.']),
    ('Tamaño de la posición', 'Capital $20 millones. Aceptas perder como máximo 1% del capital en una idea y tu stop está 8% bajo el precio de compra. ¿Cuánto debes invertir?',
     ['Riesgo aceptado = 1% × 20.000.000 = $200.000', 'Posición = 200.000 / 0,08 = **$2.500.000** (12,5% del capital)', 'Si el stop estuviera al 4%, podrías invertir $5.000.000 (25%).']),
    ('RSI', 'En los últimos 14 días, la ganancia diaria promedio fue $1,2 y la pérdida diaria promedio $0,8. Calcula el RSI.',
     ['RS = 1,2 / 0,8 = 1,5', 'RSI = 100 − 100 / (1 + 1,5) = 100 − 40 = **60** → zona neutral-alcista (ni sobrecompra ni sobreventa).']),
    ('Drawdown', 'Valor de la cartera por semana: 100, 110, 121, 96,8, 102, 130. Calcula el drawdown de cada semana y el máximo drawdown.',
     ['Peaks: 100, 110, 121, 121, 121, 130', 'Drawdowns: 0%, 0%, 0%, **−20,0%**, −15,7%, 0%', 'Máximo drawdown = **−20%**; aun así terminó +30%.']),
    ('Caso integrador', 'Diseñen una cartera core–satélite de $20 millones para el concurso: 4 acciones núcleo de sectores distintos y 2 satélites con catalizador. Usen la hoja 5_Cartera con datos reales.',
     ['Pasos sugeridos: (1) descargar precios de 1 año de 8–10 candidatos (Yahoo .SN); (2) pegarlos en 1_Precios; (3) revisar correlaciones (hoja 3) y betas (hoja 6);',
      '(4) asignar 12,5% a cada acción núcleo (50%) y 25% a cada satélite (50%); (5) revisar Sharpe, beta, drawdown y reducción de riesgo por diversificación;',
      '(6) escribir la tesis y el catalizador de cada acción en la Plantilla de Estrategia; (7) discutir: ¿la beta total y la concentración son coherentes con su objetivo del ranking?',
      'No hay una única respuesta correcta: evalúen la coherencia entre tesis, riesgo y objetivo.']),
]

def ejercicios(path):
    d = Doc('Ejercicios Resueltos CCI')
    d.cover('Ejercicios Resueltos', 'Teoría de carteras aplicada al Concurso Carteras de Inversión',
            ['18 ejercicios de dificultad creciente, con solución paso a paso.', 'Recomendación: intenten resolverlos antes de mirar la solución (está en la página siguiente de cada bloque).',
             'Los ejercicios 4–6, 9, 11, 14 y 18 se pueden comprobar en el Laboratorio Excel.'], 'EJERCICIOS')
    d.h(1, 'Enunciados')
    for i, (t, q, _) in enumerate(EJ, 1):
        d.p(f'**Ejercicio {i} · {t}.** {q}')
    d.h(1, 'Soluciones')
    for i, (t, q, sol) in enumerate(EJ, 1):
        d.h(3, f'Ejercicio {i} · {t}')
        d.bullets(sol)
    d.save(path, 'Ejercicios Resueltos · CCI')

# =====================================================================  PLANTILLA
def plantilla(path):
    d = Doc('Plantilla de Estrategia CCI')
    d.p('PLAN DE ESTRATEGIA DEL EQUIPO · CCI', size=18, bold=True, color='1F3864', space_after=40)
    d.p('Llénenla antes de la marcha blanca y revísenla cada viernes. Un plan escrito es la mejor defensa contra los sesgos.', italic=True, color='595959', size=9.5)
    E = lambda n: [[''] * n for _ in range(1)]
    d.h(2, '1. Equipo y roles')
    d.table(['Integrante', 'Rol principal', 'Rol secundario', 'Contacto'], [['', '', '', ''] for _ in range(5)], widths=[3, 2.6, 2.6, 2.4], zebra=False)
    d.p('¿Quién ejecuta las órdenes? ____________________   ¿Cómo resolvemos desacuerdos? ______________________________________')
    d.h(2, '2. Reglas confirmadas en las bases')
    d.table(['Regla', 'Lo que dicen las bases'], [[r, ''] for r in ['Universo de instrumentos', 'Comisión (y forma de cobro)', 'Ventas cortas / margen', 'Límites de concentración',
            'Precio de ejecución y horario', 'Dividendos', 'Criterio de ranking y premios', 'Fechas (marcha blanca, inicio, fin)']], widths=[3.5, 6.5], zebra=False)
    d.h(2, '3. Escenario macro (1 párrafo)')
    d.table(['Variable', 'Nuestra visión para las próximas 8 semanas', 'Sectores que favorece / perjudica'],
            [[v, '', ''] for v in ['Cobre', 'Dólar / peso', 'TPM e inflación', 'China / Fed', 'Política local']], widths=[2, 4.5, 3.5], zebra=False)
    d.h(2, '4. Objetivo y riesgo')
    d.table(['Parámetro', 'Nuestra decisión'], [[r, ''] for r in ['Estrategia (A indexada / B core–satélite / C concentrada)', 'Número de acciones', '% núcleo / % satélites',
            'Límite máximo por acción', 'Beta objetivo de la cartera', 'Pérdida máxima aceptada por idea (% del capital)', 'Drawdown que nos obliga a revisar todo',
            'Máximo de operaciones por semana', 'Regla si vamos arriba en el ranking', 'Regla si vamos atrás en el ranking']], widths=[5, 5], zebra=False)
    d.h(2, '5. Cartera inicial')
    d.table(['Acción', 'Núcleo / satélite', 'Peso', 'Tesis (1 frase)', 'Catalizador y fecha', 'Stop', 'Objetivo'], [[''] * 7 for _ in range(8)],
            widths=[1.4, 1.3, 0.8, 3, 2, 0.9, 1], zebra=False, font_size=9)
    d.h(2, '6. Revisión semanal')
    d.table(['Semana', 'Rent. cartera', 'Rent. IPSA', 'Lugar en ranking', 'Qué funcionó', 'Qué no', 'Ajuste decidido'], [[f'S{i}', '', '', '', '', '', ''] for i in range(1, 9)],
            widths=[0.9, 1.2, 1.1, 1.3, 2, 1.7, 2], zebra=False, font_size=9)
    d.h(2, '7. Post-mortem final')
    d.bullets(['¿Qué ganancias vinieron de buen análisis y cuáles de suerte?', '¿Qué sesgos cometimos?', '¿Qué haríamos distinto?', '¿Qué historia contaremos en una entrevista?'])
    d.save(path, 'Plantilla de Estrategia · CCI')
