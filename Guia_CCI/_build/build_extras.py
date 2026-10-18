import csv, html, sys
sys.path.insert(0, '/projects/sandbox/Guia_CCI/_build')
from diagrams import MM
O = '/projects/sandbox/Guia_CCI/'

CARDS = [
 ('Concurso', '¿Quién organiza el CCI?', 'La Bolsa de Santiago (parte de nuam).'),
 ('Concurso', 'Capital ficticio histórico del CCI', '$20.000.000.'),
 ('Concurso', 'Universo histórico de inversión del CCI', 'Acciones del IPSA (confirmar en bases vigentes).'),
 ('Concurso', 'Comisión histórica del CCI', '0,5% por operación (2021).'),
 ('Concurso', 'Tamaño máximo de equipo (2023)', 'Hasta 5 personas del mismo curso o carrera.'),
 ('Concurso', '¿Qué es la marcha blanca?', 'Fase de ensayo previa al concurso oficial; no cuenta para el ranking.'),
 ('Concurso', 'Duración típica del concurso oficial', '~8 semanas (2016, 2023); 4 semanas en 2020.'),
 ('Concurso', 'Rentabilidad del ganador universitario 2016 vs IPSA', '64,2% vs 1,23% del IPSA en el mismo período.'),
 ('Concurso', 'Alza de empate de una ida y vuelta con c = 0,5%', '(1+c)/(1−c) − 1 ≈ 1,005%.'),
 ('Concurso', 'Costo de rotar la cartera 10 veces (c = 0,5%)', '≈ 9,5% del capital (20 veces ≈ 18%).'),
 ('Torneo', '¿A qué se parece el pago de un torneo?', 'A una opción de compra sobre la rentabilidad: sube de valor con la volatilidad.'),
 ('Torneo', 'Estrategia si vas primero', 'Reducir volatilidad y parecerse a los perseguidores.'),
 ('Torneo', 'Estrategia si vas atrás', 'Diferenciarse y aceptar más riesgo, con tiempo, no el último día.'),
 ('Torneo', 'Alza necesaria tras una caída d', '1/(1−d) − 1. −25% → +33%; −50% → +100%.'),
 ('Torneo', 'Paper sobre torneos de fondos mutuos', 'Brown, Harlow y Starks (1996): los perdedores a mitad de año suben el riesgo.'),
 ('Torneo', 'P(R>30% en 8 semanas) con σ=20% vs σ=60% (μ=10%)', '≈0,07% vs ≈12%.'),
 ('Mercado', '¿Qué es nuam?', 'Holding que integra las bolsas de Santiago, Lima y Colombia (2023).'),
 ('Mercado', 'Número de acciones del S&P IPSA', '30 (desde 2019; antes 40).'),
 ('Mercado', 'Cómo se pondera el IPSA', 'Por capitalización ajustada por free float, con límites por acción.'),
 ('Mercado', '¿Qué es un hecho esencial?', 'Información relevante que la empresa debe informar de inmediato a la CMF.'),
 ('Mercado', 'Fecha ex-dividendo', 'Desde ese día el comprador ya no recibe el dividendo; el precio cae ~ por su monto.'),
 ('Mercado', 'Orden límite vs a mercado', 'Límite: solo a tu precio o mejor. Mercado: inmediata al mejor precio disponible.'),
 ('Mercado', 'Spread', 'Diferencia entre mejor precio de compra y de venta: costo oculto.'),
 ('Mercado', 'Sufijo de acciones chilenas en Yahoo Finance', '.SN (ej. SQM-B.SN); índice ^IPSA.'),
 ('Mercado', 'Liquidación habitual de acciones en Chile', 'Contado normal, T+2.'),
 ('Macro', 'Efecto típico de un alza del cobre', 'Aprecia el peso, ayuda a mineras y al sentimiento local.'),
 ('Macro', 'Quién gana con un dólar alto', 'Exportadores que venden en USD (minería, forestal).'),
 ('Macro', 'Quién gana con recortes de TPM', 'Consumo, retail, inmobiliario, utilities.'),
 ('Macro', 'Quién gana con inflación/UF alta', 'Bancos con activos en UF y negocios indexados.'),
 ('Macro', 'Frecuencia de las RPM del Banco Central', '8 reuniones al año.'),
 ('Macro', 'Cuándo publica el INE el IPC', 'Alrededor del día 8 de cada mes.'),
 ('Macro', 'Gran catalizador de oct–dic', 'Temporada de resultados del 3er trimestre.'),
 ('Riesgo', 'Retorno simple con dividendo', 'R = (P₁ + D − P₀)/P₀.'),
 ('Riesgo', 'Retorno logarítmico', 'r = ln(P₁/P₀); se suma en el tiempo.'),
 ('Riesgo', 'Anualizar volatilidad diaria', 'σ anual = σ diaria × √252.'),
 ('Riesgo', 'Anualizar retorno medio diario', '(1 + r̄)^252 − 1.'),
 ('Riesgo', 'Máximo drawdown', 'Mayor caída desde un máximo previo: mín(P/máx(P) − 1).'),
 ('Riesgo', 'Curtosis en exceso > 0', 'Colas gordas: más eventos extremos que una normal.'),
 ('Riesgo', 'Asimetría positiva', 'Cola derecha larga: posibles alzas explosivas (atractivo en un torneo).'),
 ('Carteras', 'Varianza de una cartera de 2 activos', 'w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂.'),
 ('Carteras', 'Peso de mínima varianza (2 activos)', 'w₁* = (σ₂² − ρσ₁σ₂)/(σ₁² + σ₂² − 2ρσ₁σ₂).'),
 ('Carteras', 'Pesos de riesgo cero con ρ = −1', 'w₁ = σ₂/(σ₁ + σ₂).'),
 ('Carteras', 'Correlación', 'ρ = σ₁₂/(σ₁σ₂), entre −1 y 1.'),
 ('Carteras', 'Límite del riesgo al diversificar (pesos iguales)', '√ρ · σ: el riesgo sistemático.'),
 ('Carteras', '¿Con cuántas acciones se logra casi toda la diversificación?', 'Con unas 8–10 acciones de sectores distintos.'),
 ('Carteras', 'Frontera eficiente', 'Carteras con máximo retorno esperado para cada riesgo (Markowitz, 1952).'),
 ('Carteras', 'Cartera tangente', 'La de máximo Sharpe; donde la CML toca la frontera.'),
 ('Carteras', 'CML', 'Recta desde rf hasta la cartera tangente; pendiente = Sharpe de la tangente.'),
 ('CAPM', 'Fórmula del CAPM', 'E(Ri) = rf + βi[E(Rm) − rf].'),
 ('CAPM', 'Definición de beta', 'β = Cov(Ri, Rm)/Var(Rm).'),
 ('CAPM', 'Beta de la cartera', 'Promedio ponderado: βp = Σ wiβi.'),
 ('CAPM', 'SML', 'Retorno exigido vs beta; sobre la SML = alfa positivo.'),
 ('CAPM', '¿Qué riesgo paga el mercado según el CAPM?', 'Solo el sistemático (beta).'),
 ('CAPM', 'Fórmula de Hamada', 'βL = βU × [1 + (1 − t) × D/E].'),
 ('CAPM', 'R² de la regresión de beta', 'Proporción del riesgo explicada por el mercado; 1 − R² es idiosincrático.'),
 ('Desempeño', 'Ratio de Sharpe', '(Rp − rf)/σp.'),
 ('Desempeño', 'Ratio de Treynor', '(Rp − rf)/βp.'),
 ('Desempeño', 'Alfa de Jensen', 'Rp − [rf + βp(Rm − rf)].'),
 ('Desempeño', 'Tracking error', 'σ(Rp − Rb): cuánto te alejas del benchmark.'),
 ('Desempeño', 'Information ratio', '(Rp − Rb)/TE.'),
 ('Desempeño', 'Ratio de Sortino', '(Rp − rf)/σ a la baja.'),
 ('Fundamental', 'P/U', 'Precio / utilidad por acción.'),
 ('Fundamental', 'P/VL y su relación con la tesina', 'Precio / valor libro por acción = 1/BME.'),
 ('Fundamental', 'EV/EBITDA', '(Capitalización + deuda neta)/EBITDA; no sirve para bancos.'),
 ('Fundamental', 'Dividend yield', 'Dividendo / precio.'),
 ('Fundamental', 'ROE y DuPont', 'Utilidad/patrimonio = margen × rotación × apalancamiento.'),
 ('Fundamental', 'Deuda neta/EBITDA alta', '> 3–4x suele indicar estrés (empresas no financieras).'),
 ('Fundamental', 'PEAD', 'Tras una sorpresa de utilidades, el precio sigue en esa dirección por semanas.'),
 ('Fundamental', '¿Qué mueve el precio en un resultado?', 'La sorpresa vs lo esperado, no el resultado en sí.'),
 ('Técnico', 'RSI', '100 − 100/(1 + G/P); >70 sobrecompra, <30 sobreventa.'),
 ('Técnico', 'MACD', 'EMA12 − EMA26, con señal EMA9.'),
 ('Técnico', 'Bandas de Bollinger', 'SMA20 ± 2 desviaciones estándar.'),
 ('Técnico', 'Cruce dorado', 'SMA50 cruza sobre la SMA200 (señal alcista).'),
 ('Técnico', 'Momentum', 'Ganadores de 3–12 meses siguen ganando (Jegadeesh y Titman, 1993).'),
 ('Técnico', 'Reversión de corto plazo', 'Extremos de 1 semana – 1 mes tienden a corregirse.'),
 ('Conducta', 'Efecto disposición', 'Vender ganadoras rápido y mantener perdedoras (Shefrin y Statman, 1985).'),
 ('Conducta', 'Aversión a pérdidas', 'Las pérdidas duelen ~2 veces más (Kahneman y Tversky, 1979).'),
 ('Conducta', 'Sobreconfianza', 'Sobreestimar la capacidad propia → operar de más (Barber y Odean, 2000).'),
 ('Conducta', 'Anclaje', 'Fijarse en un precio de referencia pasado.'),
 ('Conducta', 'Antídoto principal contra los sesgos', 'Tesis escrita, checklist y diario de decisiones.'),
 ('Estrategia', 'Estructura core–satélite', 'Núcleo 50–70% diversificado + satélites 30–50% de alta convicción.'),
 ('Estrategia', 'Tamaño de posición por presupuesto de riesgo', 'Riesgo aceptado / distancia al stop (1%/8% = 12,5%).'),
 ('Estrategia', 'Regla de operación mínima', 'Movimiento esperado ≥ 3 veces el costo (~3%).'),
 ('Estrategia', 'Criterio de Kelly', 'f* = (p·b − q)/b; en la práctica se usa una fracción.'),
 ('Estrategia', 'Qué probar en la marcha blanca', 'Precio de ejecución, comisiones, horario, dividendos y ranking.'),
 ('Estrategia', 'Límite por acción recomendado', '25–35% aunque las bases no lo exijan.'),
]

def flashcards():
    with open(O + '07_Flashcards_Anki_CCI.txt', 'w', encoding='utf-8') as f:
        f.write('#separator:tab\n#html:false\n#tags column:3\n')
        for t, q, a in CARDS:
            f.write(f'{q}\t{a}\tCCI::{t}\n')
    with open(O + '07_Flashcards_CCI.csv', 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(['Tema', 'Pregunta', 'Respuesta'])
        for t, q, a in CARDS: w.writerow([t, q, a])

def freemind():
    e = lambda s: html.escape(s, quote=True)
    colors = ['#2E75B6', '#C55A11', '#548235', '#7030A0', '#BF8F00', '#C00000', '#00838F', '#5B6770']
    out = ['<map version="1.0.1">', f'<node TEXT="{e("CCI · Concurso Carteras de Inversión")}" BACKGROUND_COLOR="#1F3864" COLOR="#FFFFFF">',
           '<font BOLD="true" SIZE="16"/>']
    for k, (name, leaves) in enumerate(MM[2]):
        pos = 'left' if k < 4 else 'right'
        out.append(f'<node TEXT="{e(name)}" POSITION="{pos}" COLOR="{colors[k]}" FOLDED="false"><font BOLD="true" SIZE="13"/><edge COLOR="{colors[k]}" WIDTH="2"/>')
        for lf in leaves:
            out.append(f'<node TEXT="{e(lf)}"/>')
        out.append('</node>')
    out.append('</node></map>')
    open(O + '04b_Mapa_Mental_CCI.mm', 'w', encoding='utf-8').write('\n'.join(out))

flashcards(); freemind()
print(len(CARDS), 'tarjetas')
