from docx_lib import Doc

IMG = '/projects/sandbox/Guia_CCI/04_Esquemas_PNG'

def build(path):
    d = Doc('Guía Completa CCI', 'Vicente Altamirano')
    d.cover('Concurso Carteras de Inversión (CCI)',
            'Guía completa para prepararse, entender el mercado chileno y competir con estrategia',
            ['Preparada para: Vicente Altamirano y José Ignacio Barrientos — Ingeniería Comercial, Universidad Austral de Chile',
             'Contexto: invitación de la Prof. Roxana Pincheira (vía Prof. Leonardo Pacheco), octubre de 2026',
             'Material complementario: Resumen Express, Laboratorio en Excel, Mapas y Esquemas, Ejercicios Resueltos, Quiz interactivo, Flashcards y Plantilla de Estrategia',
             '',
             'Nota importante: esta guía supone que la invitación corresponde al CCI de la Bolsa de Santiago. Las reglas citadas son las de ediciones anteriores; '
             'antes de competir hay que confirmarlas en las bases vigentes.'])
    d.toc()
    d.pagebreak()

    # ------------------------------------------------------------ 0
    d.h(1, '0. Cómo usar esta guía')
    d.p('La guía está pensada para que pasen de "saber finanzas de la carrera" a **competir con método**. Combina tres cosas: '
        '(1) conocer las reglas del juego y su lógica de torneo, (2) dominar la teoría de inversiones que de verdad se usa al armar una cartera, '
        'y (3) traducir todo eso en una estrategia escrita, con reglas de riesgo y un registro disciplinado.')
    d.table(['Archivo', 'Para qué sirve', 'Cuándo usarlo'], [
        ['01_Guia_Completa_CCI.docx (este)', 'Teoría, mercado chileno, estrategia, glosario', 'Estudio principal (semanas 1–2)'],
        ['02_Resumen_Express_CCI.docx', 'Todo lo esencial en pocas páginas', 'Repaso rápido, la noche antes de operar'],
        ['03_Laboratorio_CCI.xlsx', '14 hojas: retornos, correlaciones, frontera, CAPM, técnico, simulador del concurso, torneo, screener, calendario', 'Practicar y luego gestionar la cartera real del concurso'],
        ['04_Mapas_y_Esquemas.html + carpeta PNG', '10 esquemas y mapa mental (sin internet)', 'Visualizar y memorizar'],
        ['04b_Mapa_Mental_CCI.mm', 'Mapa mental editable (FreeMind / XMind / MindMeister)', 'Agregar sus propias notas'],
        ['05_Ejercicios_Resueltos_CCI.docx', '18 ejercicios con solución paso a paso', 'Después de cada capítulo de teoría'],
        ['06_Quiz_Interactivo_CCI.html', 'Autoevaluación con corrección y explicación', 'Al cerrar cada bloque y antes del concurso'],
        ['07_Flashcards_Anki_CCI.txt / .csv', 'Tarjetas de memoria (importables en Anki o Quizlet)', '10 minutos diarios'],
        ['08_Plantilla_Estrategia_Equipo.docx', 'Documento de 1–2 páginas para escribir su estrategia', 'Antes de la marcha blanca'],
    ], widths=[3.2, 4.2, 2.6])
    d.h(2, 'Plan sugerido de 3 semanas')
    d.table(['Semana', 'Objetivo', 'Capítulos', 'Práctica'], [
        ['1', 'Reglas, mercado chileno y teoría de riesgo/retorno', '1–7', 'Hojas 1–6 del Excel + ejercicios 1–9 + quiz bloque 1'],
        ['2', 'Análisis fundamental, técnico, conducta y estrategia de torneo', '8–12', 'Hojas 7–11 + ejercicios 10–18 + plantilla de estrategia'],
        ['3', 'Marcha blanca y simulacro', '13–15 + repaso', 'Hojas 9 y 12 con datos reales; quiz completo; ajustar la estrategia'],
    ], widths=[1, 4, 1.6, 4])
    d.callout('Idea fuerza', 'El CCI no premia "hacerlo bien" en el sentido de la teoría (mejor Sharpe), premia **terminar arriba de miles de personas en pocas semanas**. '
              'La teoría sirve para entender qué riesgo estás tomando; la estrategia de torneo sirve para decidir cuánto riesgo te conviene tomar.', 'key')

    # ------------------------------------------------------------ 1
    d.h(1, '1. Qué es el CCI')
    d.p('El **Concurso Carteras de Inversión (CCI)** es un simulador de inversiones en línea organizado por la **Bolsa de Santiago**, que hoy forma parte de **nuam**, '
        'el holding que integra las bolsas de Santiago, Lima y Colombia (integración societaria concretada en noviembre de 2023). El concurso lleva más de 28 años realizándose y es '
        'el simulador bursátil más conocido de Chile. Su objetivo declarado es educativo: acercar a estudiantes al mercado de acciones operando con precios reales pero dinero ficticio.')
    d.h(2, '1.1 Lo que se sabe de ediciones anteriores')
    d.table(['Característica', 'Lo informado en ediciones previas', 'Fuente / año'], [
        ['Capital', '$20.000.000 ficticios por participante o equipo', 'U. de Chile, UCN, Mediabanco (varios años)'],
        ['Universo de inversión', 'Acciones de las empresas del índice IPSA', 'U. de Chile (2010), U. Autónoma (2015), UCN'],
        ['Precios', 'Precios reales de mercado, compra y venta como en la realidad', 'Diario Estrategia (2021)'],
        ['Comisión', '0,5% por operación, "similar a la del mercado real"', 'Chócale (2021)'],
        ['Participantes', 'Equipos de hasta 5 personas del mismo curso o carrera', 'U. Autónoma (2023)'],
        ['Fases', 'Inscripción + "marcha blanca" (ensayo) y luego concurso oficial', 'U. Autónoma (2023)'],
        ['Duración oficial', '~8 semanas (2016 y 2023); 4 semanas en 2020', 'La Tercera (ed. 2016), U. Autónoma (2023), Diario Sustentable (2020)'],
        ['Calendario 2023', 'Marcha blanca 21-ago a 9-oct; oficial 10-oct a 1-dic', 'U. Autónoma (2023)'],
        ['Categorías', 'Enseñanza Media y Educación Superior de Pregrado (antes también Abierta)', 'Diario Sustentable (2020), La Tercera (ed. 2016)'],
        ['Criterio de ranking', 'Mayor rentabilidad del portafolio', 'Varias fuentes'],
        ['Premios', 'Hasta $700.000 (2022) y otros premios/sorteos', 'Chócale (2022), U. Autónoma (2023)'],
        ['Tamaño', '>20.000 inscritos (2010); 15.952 (2016); >5.000 (2020)', 'U. de Chile, La Tercera, Diario Sustentable'],
    ], widths=[2.4, 5, 3])
    d.callout('Referencias de rentabilidad ganadora', [
        '• Edición 2016 (8 semanas): el ganador universitario obtuvo **64,2%**, mientras el IPSA subió solo **1,23%** en el mismo período (La Tercera).',
        '• Nota de la UDP (2020): una estudiante ganó el primer lugar de su categoría con **32,74%**.',
        '• Noticias UACh (2019): cuatro estudiantes de Ingeniería Comercial de la UACh destacaron en una categoría con más de 13 mil participantes; la Prof. Pincheira comentó su desempeño (Noticias UACh).',
        'Conclusión: para ganar hay que obtener en semanas lo que el mercado entrega en varios años. Esto define toda la estrategia (capítulo 11).'], 'info')
    d.h(2, '1.2 Lo que DEBEN confirmar en las bases vigentes')
    d.p('Las reglas cambian entre ediciones. Antes de diseñar la estrategia, lean las bases completas y respondan esta lista (está también en la Plantilla de Estrategia):')
    d.table(['Pregunta', 'Por qué importa'], [
        ['¿Qué instrumentos se pueden comprar? ¿Solo IPSA? ¿ETF, ADR, acciones fuera del índice?', 'Define el universo y la posibilidad de concentrarse en acciones más volátiles'],
        ['¿Cuál es la comisión exacta y cómo se cobra (por lado, mínimo fijo)?', 'Determina cuántas operaciones son razonables'],
        ['¿Se permiten ventas cortas, margen o apalancamiento?', 'Si no, solo se gana cuando las acciones suben (o estando en caja)'],
        ['¿Hay límites de concentración o un mínimo de acciones?', 'Restringe las carteras concentradas'],
        ['¿A qué precio se ejecutan las órdenes (último, cierre, punta)? ¿Con qué desfase?', 'Afecta el timing y el "slippage"'],
        ['¿Se reconocen dividendos? ¿Cómo se tratan la fecha ex y los aumentos de capital?', 'Una caída por dividendo podría contar como pérdida'],
        ['¿Cómo se calcula el ranking? ¿Rentabilidad total al cierre? ¿Hay premios semanales?', 'Define el objetivo exacto'],
        ['¿La caja (efectivo) rinde algo?', 'Estar en caja tiene costo de oportunidad o no'],
        ['¿Hay reglas sobre equipos, cuentas múltiples o conducta?', 'Cumplimiento: no arriesgar descalificación'],
        ['¿Fechas de marcha blanca, inicio, cierre y premiación?', 'Planificar el calendario y la temporada de resultados'],
    ], widths=[5.5, 4.5])

    # ------------------------------------------------------------ 2
    d.h(1, '2. La lógica de un torneo de inversión')
    d.p('Un concurso de rentabilidad es un **torneo**: no importa cuánto ganas en términos absolutos, sino ganar más que los demás. Esto cambia la manera correcta de pensar el riesgo.')
    d.h(2, '2.1 El premio es convexo')
    d.p('Solo los primeros lugares reciben premio. Quedar en el lugar 500 o en el 5.000 da lo mismo. Matemáticamente, el pago se parece a una **opción de compra** sobre tu rentabilidad: '
        'tiene un piso (no pierdes dinero real) y una ganancia grande si superas cierto umbral. Y como saben por la tesina de opciones reales, **el valor de una opción sube con la volatilidad**. '
        'Por eso los concursos de este tipo empujan a tomar más riesgo que el que tomaría un inversionista racional con su propio dinero.')
    d.callout('Conexión con la literatura', 'Brown, Harlow y Starks (1996) mostraron que los administradores de fondos mutuos que van perdiendo a mitad de año tienden a aumentar el riesgo '
              'de sus carteras en la segunda mitad, porque los flujos de clientes premian a los primeros del ranking. Es la misma lógica que verán en el CCI.', 'tesis')
    d.h(2, '2.2 Volatilidad y probabilidad de llegar a la meta')
    d.p('Supongan una cartera con retorno esperado de 10% anual y distintos niveles de volatilidad, en un concurso de 8 semanas. La probabilidad de superar +30% (lo que suele '
        'necesitarse para pelear el primer lugar) cambia radicalmente (modelo lognormal, hoja 10_Torneo del Excel):')
    d.table(['Volatilidad anual', 'P(retorno > 10%)', 'P(retorno > 30%)', 'P(retorno < −10%)'], [
        ['15% (≈ IPSA diversificado)', '8,3%', '~0%', '2,2%'],
        ['20%', '14,5%', '0,07%', '6,7%'],
        ['40% (cartera concentrada)', '27,8%', '4,9%', '24,5%'],
        ['60% (muy concentrada, betas altas)', '32,4%', '12,2%', '34,6%'],
    ], widths=[3, 2.3, 2.3, 2.3])
    d.p('**Lectura:** con una cartera parecida al IPSA es casi imposible ganar; con una cartera concentrada la probabilidad de ganar sube, pero también la de terminar muy abajo. '
        'El trabajo de análisis (capítulos 8 y 9) sirve para que esa volatilidad extra venga acompañada de un retorno esperado mayor, es decir, para mover la distribución completa hacia la derecha.')
    d.h(2, '2.3 El costo de operar')
    d.p('Con una comisión de 0,5% por lado, cada compra y venta posterior cuesta cerca de 1%. Para no perder, la acción debe subir:')
    d.formula('Alza de empate = (1 + c) / (1 − c) − 1 = 1,005 / 0,995 − 1 ≈ 1,005%')
    d.p('Rotar toda la cartera 10 veces durante el concurso cuesta aproximadamente **9,5%** del capital; 20 veces, cerca de **18%**. En un torneo donde gana quien obtiene 30–60%, '
        'regalar 10–18% en comisiones es muy caro. Regla práctica: **operar solo cuando el movimiento esperado sea al menos 3 veces el costo** (≈3%).')
    d.h(2, '2.4 Riesgo de ruina')
    d.p('La asimetría de las pérdidas es brutal: si caes 25% necesitas +33% para volver a cero; si caes 50%, necesitas +100%. Una mala apuesta en la primera semana puede dejarlos '
        'fuera del torneo antes de que sus buenas ideas maduren. Por eso la estrategia correcta no es "máximo riesgo siempre", sino **riesgo alto pero controlado, con reglas de salida**.')
    d.formula('Alza necesaria para recuperar una caída d = 1 / (1 − d) − 1')

    # ------------------------------------------------------------ 3
    d.h(1, '3. El mercado de acciones chileno')
    d.h(2, '3.1 Bolsa de Santiago y nuam')
    d.p('La Bolsa de Comercio de Santiago es la principal bolsa de Chile. Desde 2023 forma parte de **nuam**, que integra las bolsas de Santiago, Lima y Colombia con el objetivo de '
        'construir un mercado único regional. La regulación y supervisión corresponden a la **Comisión para el Mercado Financiero (CMF)**, donde las empresas publican sus estados '
        'financieros y **hechos esenciales** (información relevante que debe divulgarse de inmediato: fusiones, resultados extraordinarios, cambios de directorio, etc.).')
    d.h(2, '3.2 El índice S&P IPSA')
    d.bullets([
        '**Qué es:** el principal índice accionario chileno, calculado por S&P Dow Jones Indices en conjunto con la Bolsa de Santiago.',
        '**Composición:** desde 2019 tiene 30 acciones (antes eran 40). La composición se revisa periódicamente, así que verifiquen la lista vigente.',
        '**Ponderación:** por capitalización bursátil ajustada por capital flotante (free float), con límites de peso por acción.',
        '**Hito reciente:** en noviembre de 2025 superó por primera vez los 10.000 puntos (La Tercera).',
        '**Por qué importa:** históricamente es el universo del CCI y es el **benchmark** natural para evaluar si su cartera "le gana al mercado".'])
    d.h(2, '3.3 Sectores típicos del IPSA')
    d.p('La composición cambia, pero el IPSA suele incluir empresas de estos sectores (los ejemplos son referenciales; confirmen la lista vigente):')
    d.table(['Sector', 'Ejemplos habituales', 'Qué los mueve'], [
        ['Bancos', 'Banco de Chile, BCI, Santander Chile, Itaú Chile', 'Tasas (TPM), inflación/UF, crecimiento del crédito, morosidad'],
        ['Retail y centros comerciales', 'Falabella, Cencosud, Ripley, Parque Arauco, Mallplaza', 'Consumo, empleo, tasas, tipo de cambio, Perú/Colombia/Argentina'],
        ['Minería y química', 'SQM-B, CAP', 'Litio, hierro, cobre, China, regulación'],
        ['Forestal / holdings', 'CMPC, Empresas Copec', 'Precio de la celulosa, combustibles, dólar'],
        ['Energía y utilities', 'Enel Chile, Colbún, Engie Chile, AES Andes', 'Tasas (descuento de flujos estables), hidrología, regulación'],
        ['Consumo básico', 'CCU, Embotelladora Andina, Concha y Toro, SMU', 'Costos de insumos, consumo, tipo de cambio'],
        ['Transporte', 'LATAM Airlines, Vapores', 'Petróleo, demanda de viajes, fletes, dólar'],
        ['Otros', 'Entel, Quiñenco, Aguas Andinas, Sonda', 'Competencia, regulación, inversiones'],
    ], widths=[2.3, 4, 4])
    d.h(2, '3.4 Conceptos operativos')
    d.table(['Concepto', 'Qué significa', 'Implicancia en el concurso'], [
        ['Orden a mercado', 'Se ejecuta al mejor precio disponible', 'Rápida, pero el precio puede ser peor en acciones poco líquidas'],
        ['Orden límite', 'Se ejecuta solo a tu precio o uno mejor', 'Controla el precio; puede no ejecutarse'],
        ['Spread', 'Diferencia entre precio de compra (oferta) y venta (demanda)', 'Costo oculto adicional a la comisión'],
        ['Liquidez / presencia bursátil', 'Cuánto y qué tan seguido se transa', 'En el simulador puede importar menos, pero define la confiabilidad del precio'],
        ['Liquidación', 'Contado normal: habitualmente T+2', 'En el simulador normalmente no aplica; confirmar'],
        ['Series de acciones', 'Ej.: SQM-A y SQM-B, ANDINA-A y ANDINA-B', 'Distintos derechos de voto y dividendos; elegir la serie correcta'],
        ['ADR', 'Acción chilena transada en EE.UU. (ej. SQM, LATAM)', 'Señal del día anterior y de la madrugada chilena'],
        ['Fecha ex-dividendo', 'Desde ese día el comprador ya no recibe el dividendo', 'El precio cae por el monto del dividendo; ver si el simulador lo compensa'],
        ['Horario', 'Rueda principal aprox. 9:30–16:00 (hora de Chile)', 'Confirmar el horario del simulador y la hora de corte de órdenes'],
    ], widths=[2.3, 3.8, 4])
    d.h(2, '3.5 Dónde obtener información')
    d.bullets([
        '**CMF (cmfchile.cl):** estados financieros, hechos esenciales, juntas y dividendos.',
        '**Bolsa de Santiago / nuam:** precios, índices, composición del IPSA, calendario.',
        '**Banco Central de Chile (bcentral.cl):** TPM, comunicados de Reunión de Política Monetaria (RPM), Informe de Política Monetaria (IPoM), dólar observado.',
        '**INE:** IPC (se publica alrededor del día 8 de cada mes).',
        '**Prensa:** Diario Financiero, La Tercera Pulso, El Mercurio Inversiones, Ex-Ante.',
        '**Datos de precios:** Yahoo Finance (tickers con sufijo .SN, índice ^IPSA), Investing.com, TradingView.',
        '**Informes de corredoras:** muchas publican recomendaciones y "carteras recomendadas" semanales; sirven como fuente de ideas (no como verdad).',
        '**Damodaran (NYU):** primas de riesgo por país, betas sectoriales (ya los usaron en la tesina).'])

    # ------------------------------------------------------------ 4
    d.h(1, '4. Macroeconomía para invertir en Chile')
    d.p('Chile es una economía pequeña y abierta, muy dependiente del cobre y con un banco central independiente con meta de inflación de 3%. Para un concurso de pocas semanas, '
        'las variables macro importan sobre todo como **catalizadores**: sorpresas que mueven sectores completos.')
    d.image(f'{IMG}/05_macro_sectores.png', 16.5, 'Figura 4.1 – Cadena de transmisión de las variables macro a los sectores (relaciones típicas).')
    d.table(['Variable', 'Fuente y frecuencia', 'Efecto típico'], [
        ['Precio del cobre', 'LME / COMEX, diario', 'Sube: mejora términos de intercambio, aprecia el peso, ayuda a mineras y al sentimiento general'],
        ['Tipo de cambio (dólar/peso)', 'Banco Central, diario', 'Dólar alto favorece a exportadores que reportan en USD y perjudica a importadores, retail y aerolíneas con costos en USD'],
        ['TPM (Tasa de Política Monetaria)', 'RPM del Banco Central, 8 veces al año', 'Recortes favorecen consumo, inmobiliario y utilities; en bancos el efecto es mixto'],
        ['Inflación (IPC) y UF', 'INE, mensual', 'Inflación alta ayuda a bancos con activos en UF y a negocios indexados; perjudica consumo'],
        ['China', 'PMI, datos de crecimiento', 'Demanda de cobre, litio y celulosa'],
        ['Tasas en EE.UU. (Fed)', 'FOMC, 8 veces al año', 'Tasas altas encarecen el capital, fortalecen el dólar y castigan a emergentes'],
        ['Política local', 'Elecciones, reformas', 'Cambios en la prima de riesgo país (pensiones, impuestos, regulación del litio)'],
    ], widths=[2.4, 2.6, 5])
    d.callout('Calendario que suele coincidir con el CCI (octubre – diciembre)', [
        '• **Temporada de resultados del tercer trimestre:** las empresas chilenas suelen publicar sus estados financieros a fines de octubre y en noviembre. Es el principal catalizador del concurso.',
        '• **Reuniones de Política Monetaria** del Banco Central (revisen el calendario anual en bcentral.cl).',
        '• **IPC** de octubre y noviembre (INE, alrededor del día 8).',
        '• **Reunión de la Fed** de diciembre y datos de empleo de EE.UU.',
        '• **Anuncios de dividendos provisorios** de algunas empresas.'], 'key')

    # ------------------------------------------------------------ 5
    d.h(1, '5. Retorno y riesgo')
    d.h(2, '5.1 Medir el retorno')
    d.formula('Retorno simple: R = (P₁ + D − P₀) / P₀', 'D = dividendo recibido en el período')
    d.formula('Retorno logarítmico: r = ln(P₁ / P₀)', 'Se suman en el tiempo; útil para modelos y para series largas')
    d.p('Los retornos simples se agregan entre activos (el retorno de la cartera es el promedio ponderado), mientras que los logarítmicos se agregan en el tiempo (el retorno de '
        'varios días es la suma). Para el concurso, lo que cuenta es el **retorno simple acumulado** de la cartera.')
    d.h(2, '5.2 Anualizar')
    d.formula('Retorno anual ≈ (1 + r̄ diario)^252 − 1        Volatilidad anual = σ diaria × √252')
    d.p('Se usan 252 días hábiles al año. Si una acción tiene volatilidad diaria de 1,2%, su volatilidad anual es 1,2% × √252 ≈ 19%. '
        'Para un concurso de 8 semanas (≈40 días hábiles), la volatilidad del período es σ anual × √(40/252) ≈ 0,40 × σ anual.')
    d.h(2, '5.3 Volatilidad, drawdown y colas gordas')
    d.bullets([
        '**Volatilidad (σ):** desviación estándar de los retornos. Mide dispersión total, al alza y a la baja.',
        '**Máximo drawdown:** mayor caída desde un peak. Es la métrica que "se siente": cuánto podrías estar perdiendo en el peor momento.',
        '**Colas gordas:** los retornos reales tienen más días extremos que una distribución normal (curtosis > 0). Los eventos "imposibles" pasan más seguido de lo que dice la campana.',
        '**Asimetría:** muchas acciones tienen asimetría negativa (caídas bruscas, alzas graduales). Las acciones con asimetría positiva (posibles alzas explosivas) son atractivas en un torneo.'])
    d.callout('En el Excel', 'Hojas 2_Retornos (estadísticos de cada acción, incluida curtosis y asimetría) y 8_Drawdown (caída desde el máximo).', 'tip')

    # ------------------------------------------------------------ 6
    d.h(1, '6. Diversificación y teoría de Markowitz')
    d.h(2, '6.1 Covarianza y correlación')
    d.formula('ρ₁₂ = σ₁₂ / (σ₁ · σ₂)        con −1 ≤ ρ ≤ 1')
    d.p('La correlación mide si dos activos se mueven juntos. Es la clave de la diversificación: combinar activos que **no** se mueven perfectamente juntos reduce el riesgo '
        'de la cartera sin reducir su retorno esperado. En Chile las correlaciones entre acciones son en general positivas, porque todas dependen del ciclo local, el cobre y el dólar.')
    d.h(2, '6.2 Cartera de dos activos')
    d.formula('E(Rp) = w₁E(R₁) + w₂E(R₂)')
    d.formula('σp² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρ₁₂σ₁σ₂')
    d.formula('Peso de mínima varianza: w₁* = (σ₂² − ρσ₁σ₂) / (σ₁² + σ₂² − 2ρσ₁σ₂)')
    d.p('Casos extremos: con ρ = 1 no hay beneficio de diversificación (el riesgo es el promedio ponderado de las volatilidades); con ρ = −1 se puede construir una cartera de riesgo cero '
        'con w₁ = σ₂ / (σ₁ + σ₂).')
    d.h(2, '6.3 N activos y número de acciones')
    d.formula('σp² = Σᵢ Σⱼ wᵢ wⱼ σᵢⱼ')
    d.image(f'{IMG}/06_diversificacion.png', 16, 'Figura 6.1 – El riesgo idiosincrático desaparece al diversificar; el sistemático no.')
    d.p('Con pesos iguales, volatilidad individual σ y correlación promedio ρ: σp² = σ²/n + (1 − 1/n)ρσ². Al aumentar n, el primer término desaparece y queda el **riesgo sistemático** ρσ². '
        'Con 8–10 acciones ya se captura casi todo el beneficio. **Implicancia para el concurso:** pasar de 10 a 4 acciones no aumenta tanto el riesgo como parece, pero sí aumenta '
        'la exposición a sus mejores ideas.')
    d.h(2, '6.4 Frontera eficiente')
    d.p('El conjunto de carteras que entregan el **máximo retorno esperado para cada nivel de riesgo** es la frontera eficiente (Markowitz, 1952). Todo inversionista racional '
        'debería elegir una cartera sobre ella. La cartera de **mínima varianza** es su punto más a la izquierda.')
    d.callout('En el Excel', 'Hoja 4_Frontera_2A: cambien la correlación entre −1 y 1 y miren cómo se curva la frontera. Hoja 5_Cartera: usen Solver para encontrar la cartera de máximo Sharpe y la de mínima varianza.', 'tip')
    d.callout('Límite práctico', 'Markowitz necesita retornos esperados, que son muy difíciles de estimar: pequeños errores producen carteras extremas. Por eso en la práctica se usan restricciones (pesos máximos, sin ventas cortas) y se combinan con juicio.', 'warn')

    # ------------------------------------------------------------ 7
    d.h(1, '7. CAPM, beta y medidas de desempeño')
    d.h(2, '7.1 CAPM')
    d.formula('E(Rᵢ) = rf + βᵢ · [E(Rm) − rf]')
    d.formula('βᵢ = Cov(Rᵢ, Rm) / Var(Rm)')
    d.p('El CAPM (Sharpe, 1964; Lintner, 1965) dice que el mercado solo paga por el **riesgo sistemático**, medido por la beta, porque el idiosincrático se puede eliminar diversificando. '
        'La **SML** (Security Market Line) grafica el retorno exigido contra la beta; un activo sobre la SML tiene alfa positivo.')
    d.image(f'{IMG}/07_capm_frontera.png', 16.5, 'Figura 7.1 – SML (izquierda) y frontera eficiente con la CML (derecha).')
    d.callout('Conexión con su tesina', 'En la tesina ya calcularon Ke = rf + β × prima de riesgo con datos de Damodaran (prima total de Chile) y betas reapalancadas con Hamada '
              '(βL = βU × [1 + (1 − t) × D/E]). Es exactamente el mismo CAPM. Una diferencia: allí usaron una beta sectorial fija; en el concurso conviene estimar la beta de cada acción '
              'contra el IPSA (hoja 6_Beta_CAPM), porque lo que les importa es cuánto amplifica cada acción los movimientos del mercado en el corto plazo.', 'tesis')
    d.h(2, '7.2 Beta en la práctica')
    d.bullets([
        'Se estima con una regresión de los retornos de la acción contra los del índice (función PENDIENTE / SLOPE en Excel).',
        'La beta de la cartera es el promedio ponderado de las betas: βp = Σ wᵢβᵢ.',
        'β > 1: acción agresiva (amplifica el mercado). β < 1: defensiva. En un mercado alcista, las betas altas ganan más; en uno bajista, pierden más.',
        'El R² de la regresión indica qué parte del riesgo es de mercado; el resto (1 − R²) es idiosincrático.'])
    d.h(2, '7.3 Medidas de desempeño')
    d.table(['Medida', 'Fórmula', 'Qué mide', 'Cuándo usarla'], [
        ['Sharpe', '(Rp − rf) / σp', 'Retorno extra por unidad de riesgo total', 'Comparar carteras completas'],
        ['Treynor', '(Rp − rf) / βp', 'Retorno extra por unidad de riesgo sistemático', 'Cartera dentro de un portafolio diversificado'],
        ['Alfa de Jensen', 'Rp − [rf + βp(Rm − rf)]', 'Retorno sobre lo que exige el CAPM', 'Saber si hubo habilidad'],
        ['Tracking error', 'σ(Rp − Rb)', 'Cuánto se aleja la cartera del benchmark', 'Medir el "riesgo activo"'],
        ['Information ratio', '(Rp − Rb) / TE', 'Exceso de retorno por unidad de riesgo activo', 'Evaluar gestión activa'],
        ['Sortino', '(Rp − rf) / σ a la baja', 'Como Sharpe, pero solo castiga la volatilidad negativa', 'Estrategias con asimetría'],
        ['Máx. drawdown', 'mín(P / máx(P) − 1)', 'Peor caída desde un peak', 'Evaluar el riesgo de ruina'],
    ], widths=[1.6, 2.6, 3.2, 2.6])
    d.p('**En el torneo:** el ranking se basa en el retorno bruto, no en el Sharpe. Igual conviene medir estas métricas: un tracking error alto les dice que se están diferenciando '
        'del resto (necesario para ganar), y un drawdown grande les avisa que están cerca de la ruina.')

    # ------------------------------------------------------------ 8
    d.h(1, '8. Análisis fundamental')
    d.p('El análisis fundamental busca estimar si una acción está barata o cara respecto de sus utilidades, flujos y activos. En un horizonte de 8 semanas su función principal es '
        '**identificar catalizadores**: eventos que harán que el mercado revalorice la acción durante el concurso.')
    d.h(2, '8.1 Múltiplos esenciales')
    d.table(['Múltiplo', 'Fórmula', 'Interpretación', 'Cuidado'], [
        ['P/U (PER)', 'Precio / Utilidad por acción', 'Años de utilidades que pagas', 'Utilidades extraordinarias o negativas lo distorsionan'],
        ['P/VL', 'Precio / Valor libro por acción', '< 1: el mercado la valora bajo su patrimonio contable', 'Clave en bancos; es 1/BME de su tesina'],
        ['EV/EBITDA', '(Cap. bursátil + deuda neta) / EBITDA', 'Valor de la empresa respecto de su caja operacional', 'No sirve para bancos'],
        ['Dividend yield', 'Dividendo / Precio', 'Rentabilidad por dividendos', 'Revisar si el dividendo es sostenible'],
        ['ROE', 'Utilidad / Patrimonio', 'Rentabilidad del capital del accionista', 'Descomponer con DuPont (margen × rotación × apalancamiento)'],
        ['Deuda neta / EBITDA', 'Deuda financiera − caja, sobre EBITDA', 'Años de EBITDA para pagar la deuda', '> 3–4x suele indicar estrés en empresas no financieras'],
    ], widths=[1.8, 3, 3, 3])
    d.callout('Conexión con su tesina', 'Su variable BME (patrimonio contable / valor de mercado) es el inverso del P/VL. Encontraron que un BME alto se asocia con menor valor de '
              'opciones reales (ProxyOR/V). Traducido al concurso: las acciones con P/VL bajo son "value" y su precio depende de los activos actuales; las de P/VL alto tienen más valor '
              'de crecimiento, y por eso suelen reaccionar con más fuerza a noticias sobre su futuro.', 'tesis')
    d.h(2, '8.2 Leer resultados trimestrales en 15 minutos')
    d.numbered([
        'Busquen el **análisis razonado** y el comunicado de prensa de resultados (más útiles que los estados financieros completos para una primera lectura).',
        'Comparen ingresos, EBITDA y utilidad contra el **mismo trimestre del año anterior** y contra lo que esperaba el mercado (informes de corredoras, prensa).',
        'Revisen márgenes (EBITDA / ingresos): ¿mejoran o empeoran?',
        'Revisen deuda neta y flujo de caja operacional.',
        'Lean las perspectivas o la guía de la administración.',
        'Lo que mueve el precio es la **sorpresa**: un resultado "bueno" que ya se esperaba puede hacer caer la acción.'])
    d.p('**Post-Earnings Announcement Drift (PEAD):** la literatura documenta que, tras una sorpresa positiva (o negativa) de utilidades, los precios tienden a seguir moviéndose en la '
        'misma dirección durante semanas (Ball y Brown, 1968; Bernard y Thomas, 1989). Es una de las anomalías más útiles para un concurso que coincide con la temporada de resultados.')
    d.h(2, '8.3 Catalizadores que buscar')
    d.bullets(['Publicación de resultados trimestrales y conferencias con inversionistas.', 'Anuncios de dividendos (provisorios o adicionales) y recompras de acciones.',
               'Cambios regulatorios o tributarios que afecten a un sector.', 'Fusiones, adquisiciones, OPAs y aumentos de capital.', 'Cambios en la composición del IPSA.',
               'Movimientos fuertes del cobre, el litio, la celulosa o el petróleo.', 'Decisiones de tasas del Banco Central o la Fed que sorprendan al mercado.'])

    # ------------------------------------------------------------ 9
    d.h(1, '9. Análisis técnico, momentum y reversión')
    d.p('El análisis técnico estudia precios y volúmenes para identificar tendencias y puntos de entrada. Su utilidad científica es debatida, pero dos fenómenos tienen sólido respaldo '
        'empírico y son relevantes para un horizonte de semanas: el **momentum** y la **reversión de corto plazo**.')
    d.h(2, '9.1 Herramientas básicas')
    d.table(['Herramienta', 'Cómo se calcula', 'Señal típica'], [
        ['Media móvil simple (SMA)', 'Promedio de los últimos n cierres (20, 50, 200 días)', 'Precio sobre la SMA = tendencia alcista; cruce de SMA50 sobre SMA200 = "cruce dorado"'],
        ['RSI (14)', '100 − 100 / (1 + ganancia promedio / pérdida promedio)', '> 70 sobrecompra; < 30 sobreventa'],
        ['MACD', 'EMA12 − EMA26, con una señal EMA9', 'MACD cruza sobre su señal = impulso alcista'],
        ['Bandas de Bollinger', 'SMA20 ± 2 desviaciones estándar', 'Precio fuera de las bandas = movimiento extremo; bandas angostas anticipan volatilidad'],
        ['Soportes y resistencias', 'Niveles donde el precio rebotó antes', 'Zonas para entrar, salir o poner stops'],
        ['Volumen', 'Cantidad transada', 'Movimientos con volumen alto son más confiables'],
    ], widths=[2.4, 3.6, 4])
    d.h(2, '9.2 Momentum y reversión')
    d.bullets([
        '**Momentum (3–12 meses):** las acciones que más subieron en los últimos meses tienden a seguir subiendo en los meses siguientes (Jegadeesh y Titman, 1993). Para un concurso corto, '
        'favorece comprar líderes con tendencia y no "las que cayeron mucho".',
        '**Reversión de corto plazo (1 semana – 1 mes):** los extremos de muy corto plazo tienden a corregirse parcialmente. Advierte contra comprar justo después de un alza explosiva sin noticia.',
        '**Combinación práctica:** elegir acciones con tendencia de mediano plazo y entrar en retrocesos de corto plazo (por ejemplo, RSI que vuelve desde sobrecompra, precio que toca la SMA20).'])
    d.callout('En el Excel', 'Hoja 7_Tecnico: elijan una acción en la lista desplegable y verán SMA20, SMA50, cruces, RSI(14) y bandas de Bollinger con gráficos.', 'tip')
    d.callout('Advertencia', 'El análisis técnico funciona mejor como **filtro de timing** que como razón para comprar. Úsenlo para decidir cuándo entrar en una idea que ya tiene fundamento '
              '(catalizador, valoración, macro), no para operar todos los días: las comisiones se comen la ventaja.', 'warn')

    # ------------------------------------------------------------ 10
    d.h(1, '10. Finanzas conductuales: el enemigo es uno mismo')
    d.table(['Sesgo', 'Qué es', 'Cómo se manifiesta en el CCI', 'Antídoto'], [
        ['Sobreconfianza', 'Sobreestimar la propia capacidad', 'Operar demasiado; concentrar sin tesis', 'Escribir la tesis y medir aciertos'],
        ['Efecto disposición', 'Vender rápido las ganadoras y mantener las perdedoras', 'Cortar ganancias, dejar correr pérdidas', 'Reglas de salida definidas antes de entrar'],
        ['Aversión a pérdidas', 'Las pérdidas duelen ~2 veces más que las ganancias equivalentes', 'No vender una posición mala "hasta recuperar"', 'Preguntarse: ¿la compraría hoy?'],
        ['Anclaje', 'Fijarse en un precio de referencia', '"Estaba a $X, debe volver"', 'Analizar la información nueva, no el precio pasado'],
        ['Efecto manada / FOMO', 'Seguir a la multitud por miedo a quedarse fuera', 'Comprar lo que todos comentan tras una gran alza', 'Checklist antes de cada operación'],
        ['Sesgo de confirmación', 'Buscar solo información que confirma lo que pienso', 'Ignorar señales contrarias', 'Rol de "abogado del diablo" en el equipo'],
        ['Falacia del jugador', 'Creer que tras varias caídas "toca" un alza', 'Comprar más de una perdedora sin razón', 'Cada día es independiente salvo que haya un motivo'],
        ['Recuperar pérdidas a toda costa', 'Subir el riesgo de forma desordenada tras perder', 'Apuestas impulsivas en la última semana', 'Plan de riesgo según el ranking, decidido con anticipación'],
    ], widths=[1.8, 2.6, 2.8, 2.8])
    d.p('Kahneman y Tversky (1979) formalizaron la aversión a pérdidas en la **teoría prospectiva**; Shefrin y Statman (1985) describieron el efecto disposición; Barber y Odean (2000) mostraron '
        'que los inversionistas individuales que más operan obtienen menores retornos netos. El mejor antídoto es un **diario de decisiones** (hoja 9_Simulador_CCI) con la tesis escrita antes de operar.')

    # ------------------------------------------------------------ 11
    d.h(1, '11. Diseñar la estrategia para el concurso')
    d.image(f'{IMG}/03_proceso_cartera.png', 16.5, 'Figura 11.1 – Proceso de construcción y gestión de la cartera.')
    d.h(2, '11.1 Tres arquetipos de estrategia')
    d.table(['Estrategia', 'Cómo es', 'Ventaja', 'Desventaja', 'Probabilidad de ganar'], [
        ['A. Indexada / defensiva', '10+ acciones, pesos parecidos al IPSA', 'Bajo riesgo, resultado parecido al índice', 'Imposible destacar entre miles', 'Muy baja'],
        ['B. Core–satélite', 'Núcleo 50–70% diversificado + 2–4 apuestas de alta convicción', 'Equilibrio entre aprender, controlar riesgo y tener opción de ganar', 'Puede quedar "a medio camino"', 'Media'],
        ['C. Concentrada de convicción', '3–5 acciones, betas altas, ligadas a catalizadores', 'Máxima opción de quedar arriba', 'Alta probabilidad de quedar muy abajo', 'La más alta, con alta varianza'],
    ], widths=[2, 2.6, 2.3, 2.3, 1.4])
    d.image(f'{IMG}/09_core_satelite_roles.png', 15.5, 'Figura 11.2 – Estructura core–satélite y roles del equipo.')
    d.callout('Recomendación para ustedes', 'Partir con una **core–satélite agresiva** (por ejemplo 50% núcleo y 50% satélites, con 5–7 acciones en total) y moverse hacia la '
              'concentrada **solo si el ranking lo exige** a mitad del concurso (ver 11.4). Así combinan lo aprendido en la tesina (riesgo y valoración) con la lógica del torneo.', 'key')
    d.h(2, '11.2 Tamaño de las posiciones')
    d.bullets([
        '**Límite por acción:** definan un máximo (por ejemplo 25–35%) aunque las bases no lo exijan.',
        '**Presupuesto de riesgo por idea:** si están dispuestos a perder 1% del capital en una idea y su salida está 8% bajo la entrada, la posición debe ser 1% / 8% = 12,5% del capital ($2,5 millones de $20 millones).',
        '**Correlación:** dos acciones del mismo sector cuentan casi como una sola apuesta.',
        '**Convicción:** las ideas con catalizador cercano y mayor potencial reciben más peso.',
        '**Criterio de Kelly (referencia):** f* = (p·b − q) / b. Sirve para entender que apostar demasiado reduce el crecimiento; en la práctica se usa una fracción (½ Kelly o menos).'])
    d.h(2, '11.3 Reglas de entrada y salida')
    d.bullets([
        '**Entrada:** solo con tesis escrita, catalizador identificado y un movimiento esperado de al menos 3 veces el costo (~3%).',
        '**Stop (salida si se equivocan):** un precio o una condición ("si el resultado no muestra mejora de márgenes, vendo"). Si el simulador no tiene órdenes stop, lo revisan diariamente.',
        '**Toma de ganancias:** por objetivo de precio o cuando el catalizador ya ocurrió y el mercado lo incorporó.',
        '**Revisión semanal obligatoria:** ¿sigue vigente la tesis? ¿La compraría hoy a este precio?'])
    d.image(f'{IMG}/04_flujo_decision.png', 13.5, 'Figura 11.3 – Filtros que debe pasar cada operación.')
    d.h(2, '11.4 Ajustar el riesgo según el ranking')
    d.image(f'{IMG}/08_estrategia_ranking.png', 16.5, 'Figura 11.4 – Gestión del riesgo según la posición en el ranking.')
    d.p('Si van arriba, conviene reducir la volatilidad y parecerse a quienes los persiguen; si van atrás, necesitan diferenciarse y aceptar más riesgo, idealmente **temprano** '
        '(con varias semanas por delante) y no como apuesta desesperada el último día.')
    d.h(2, '11.5 Organización del equipo')
    d.table(['Rol', 'Responsabilidad', 'Entregable semanal'], [
        ['Estratega macro', 'Escenario de cobre, dólar, tasas, inflación y China', 'Una página: escenario base y riesgos'],
        ['Analista de sectores', 'Screener, resultados, valoración, catalizadores', 'Ranking de ideas con tesis'],
        ['Analista técnico / timing', 'Tendencia, momentum y puntos de entrada', 'Niveles de entrada y salida'],
        ['Gestor de riesgo y registro', 'Pesos, límites, diario, comisiones, ranking', 'Planilla actualizada (hoja 9) y alertas'],
        ['Abogado del diablo', 'Atacar cada tesis antes de ejecutar', 'Riesgos de cada idea'],
    ], widths=[2.3, 4.2, 3.5])
    d.p('Con dos personas (Vicente e Ignacio), cada uno puede asumir dos o tres roles y alternar el de abogado del diablo. Decidan **por escrito** quién ejecuta las órdenes y cómo se resuelven los desacuerdos.')

    # ------------------------------------------------------------ 12
    d.h(1, '12. Gestión durante el concurso')
    d.image(f'{IMG}/02_linea_tiempo.png', 16.5, 'Figura 12.1 – Fases del concurso y tareas en cada una.')
    d.h(2, '12.1 Marcha blanca: qué probar')
    d.bullets(['¿A qué precio exacto se ejecutan las órdenes y con qué demora?', '¿Cómo se descuenta la comisión? ¿Hay mínimos?', '¿Qué pasa con una orden enviada fuera de horario?',
               '¿Se reflejan los dividendos? (prueben con una acción que tenga fecha ex en esos días, si la hay)', '¿Cómo se muestra el ranking y con qué frecuencia se actualiza?',
               'Ensayen la estrategia completa: armar la cartera, registrar en la hoja 9, revisar el viernes.'])
    d.h(2, '12.2 Rutina diaria (15–20 minutos)')
    d.numbered(['Revisar noticias de la mañana, ADR y futuros (cobre, S&P 500).', 'Revisar hechos esenciales de sus empresas en la CMF.', 'Actualizar precios en la hoja 9 y revisar alertas (caja, concentración, stops).',
                'Decidir: ¿hay alguna operación que pase el checklist? Si no, no operar.', 'Registrar cualquier operación con su tesis.'])
    d.h(2, '12.3 Revisión semanal (viernes, 45 minutos)')
    d.numbered(['Comparar la rentabilidad contra el IPSA y la posición en el ranking.', 'Revisar el calendario de la próxima semana (resultados, RPM, IPC).', 'Revisar cada posición: ¿sigue la tesis?',
                'Decidir ajustes de riesgo según el ranking (11.4).', 'Escribir 3 lecciones de la semana en la hoja 12_Calendario.'])
    d.h(2, '12.4 Cierre y post-mortem')
    d.p('Al terminar, comparen sus decisiones con los resultados: ¿qué ganancias vinieron de buen análisis y cuáles de suerte? ¿Qué errores conductuales cometieron? '
        'Esa reflexión es lo que más vale para su formación y para una entrevista de trabajo (pueden contarla con datos de su diario).')

    # ------------------------------------------------------------ 13
    d.h(1, '13. Los 12 errores más comunes')
    d.numbered([
        'No leer las bases (universo, comisiones, dividendos, ranking).', 'Armar una cartera igual al IPSA y esperar ganar.', 'Operar todos los días y pagar 10–20% en comisiones.',
        'Concentrar todo en una sola acción sin salida definida.', 'Comprar después de un alza explosiva sin noticia que la respalde (FOMO).', 'Mantener perdedoras "hasta que se recuperen".',
        'Ignorar la temporada de resultados.', 'Tener tres acciones del mismo sector y creerse diversificado.', 'No registrar las operaciones ni la tesis.',
        'Cambiar de estrategia cada semana.', 'Apostar todo el último día en vez de ajustar el riesgo con tiempo.', 'Confundir suerte con habilidad al ir ganando.'])

    # ------------------------------------------------------------ 14
    d.h(1, '14. Glosario')
    gl = [
        ('Acción', 'Parte del capital de una empresa; da derecho a dividendos y, según la serie, a voto.'), ('ADR', 'Certificado que representa acciones extranjeras y se transa en EE.UU.'),
        ('Alfa', 'Retorno por sobre lo que exige el CAPM dado el riesgo sistemático.'), ('Asimetría (skew)', 'Medida de si la distribución tiene una cola más larga a la derecha (+) o a la izquierda (−).'),
        ('Benchmark', 'Índice de referencia contra el que se compara una cartera (el IPSA en el CCI).'), ('Beta', 'Sensibilidad de una acción a los movimientos del mercado.'),
        ('Capitalización bursátil', 'Precio × número de acciones.'), ('Catalizador', 'Evento que puede hacer que el mercado revalorice una acción.'),
        ('CML', 'Línea del mercado de capitales: combina el activo libre de riesgo con la cartera tangente.'), ('CMF', 'Comisión para el Mercado Financiero, el regulador chileno.'),
        ('Comisión', 'Costo por operación; en el CCI históricamente 0,5%.'), ('Correlación', 'Grado en que dos activos se mueven juntos (entre −1 y 1).'),
        ('Covarianza', 'Medida conjunta de variación de dos activos.'), ('Curtosis', 'Medida de colas gordas; en exceso > 0 implica más eventos extremos que la normal.'),
        ('Dividend yield', 'Dividendo anual / precio.'), ('Drawdown', 'Caída desde el máximo anterior.'), ('EBITDA', 'Resultado operacional antes de depreciación y amortización.'),
        ('EV (Enterprise Value)', 'Capitalización + deuda neta: valor de la empresa completa.'), ('Fecha ex-dividendo', 'Desde esa fecha el comprador ya no recibe el dividendo anunciado.'),
        ('Free float', 'Porcentaje de acciones que realmente se transa (no en manos de controladores).'), ('Frontera eficiente', 'Carteras con máximo retorno esperado para cada nivel de riesgo.'),
        ('Hecho esencial', 'Información relevante que la empresa debe informar de inmediato a la CMF.'), ('IPSA', 'Principal índice accionario de Chile (30 acciones).'),
        ('IPoM', 'Informe de Política Monetaria del Banco Central (trimestral).'), ('Liquidez', 'Facilidad para comprar o vender sin mover el precio.'),
        ('Marcha blanca', 'Fase de ensayo del CCI, que no cuenta para el ranking.'), ('Momentum', 'Tendencia de los ganadores recientes a seguir ganando.'),
        ('nuam', 'Holding que integra las bolsas de Santiago, Lima y Colombia.'), ('Orden límite', 'Orden que se ejecuta solo a un precio determinado o mejor.'),
        ('P/U', 'Precio / utilidad por acción.'), ('P/VL', 'Precio / valor libro por acción (inverso del BME).'), ('PEAD', 'Tendencia de los precios a seguir la dirección de la sorpresa de utilidades.'),
        ('Prima por riesgo de mercado', 'Retorno extra que exige el mercado sobre la tasa libre de riesgo.'), ('R²', 'Proporción de la varianza explicada por la regresión.'),
        ('Riesgo idiosincrático', 'Riesgo propio de la empresa; se diversifica.'), ('Riesgo sistemático', 'Riesgo de mercado; no se diversifica.'), ('RPM', 'Reunión de Política Monetaria del Banco Central.'),
        ('RSI', 'Índice de fuerza relativa; oscilador entre 0 y 100.'), ('Sharpe', 'Retorno sobre la tasa libre de riesgo dividido por la volatilidad.'), ('SML', 'Línea del mercado de valores: retorno exigido según beta.'),
        ('Spread', 'Diferencia entre el mejor precio de compra y el de venta.'), ('Stop', 'Precio o condición predefinida para salir de una posición perdedora.'),
        ('TPM', 'Tasa de Política Monetaria del Banco Central de Chile.'), ('Tracking error', 'Volatilidad de la diferencia entre la cartera y el benchmark.'),
        ('UF', 'Unidad de Fomento, unidad de cuenta reajustada por inflación.'), ('Volatilidad', 'Desviación estándar de los retornos.')]
    d.table(['Término', 'Definición'], [[a, b] for a, b in gl], widths=[2.4, 7.6], font_size=9, first_col_bold=True)

    # ------------------------------------------------------------ 15
    d.h(1, '15. Referencias')
    d.h(2, 'Sobre el CCI y el mercado chileno')
    d.bullets([
        'Universidad Autónoma de Chile (2023). "Concurso Carteras de Inversión de la Bolsa de Santiago para estudiantes" (fases, equipos, fechas 2023). uautonoma.cl',
        'Chócale (2021). "Hoy finalizan las inscripciones para el Concurso de Carteras de Inversión" (comisión de 0,5%). chocale.cl',
        'Chócale (2022). "Concurso de Carteras de Inversión 2022" (premios de hasta $700.000). chocale.cl',
        'La Tercera. "Vencedor del Concurso Carteras de Inversión logra rentar más de 73%" (resultados de la edición 2016). latercera.com',
        'Diario Sustentable (2020). Resultados del CCI 2020 (4 semanas, más de 5.000 participantes). diariosustentable.com',
        'Universidad de Chile, Facultad de Agronomía (2010). "Convocan a Concurso Carteras de Inversión" ($20 millones, acciones del IPSA). uchile.cl',
        'Noticias UACh (2019). "Cuatro estudiantes de Ingeniería Comercial destacaron en concurso organizado por la Bolsa de Comercio de Santiago". diario.uach.cl',
        'BioBioChile (2025). "¿Qué es nuam?". biobiochile.cl   ·   La Tercera (2025). "El IPSA supera por primera vez los 10.000 puntos". latercera.com'])
    d.h(2, 'Teoría')
    d.bullets([
        'Bodie, Z., Kane, A. y Marcus, A. Investments. McGraw-Hill (texto base de teoría de carteras).', 'Damodaran, A. Investment Valuation. Wiley; y datos en pages.stern.nyu.edu/~adamodar.',
        'Markowitz, H. (1952). Portfolio Selection. Journal of Finance.', 'Sharpe, W. (1964). Capital Asset Prices. Journal of Finance.',
        'Jegadeesh, N. y Titman, S. (1993). Returns to Buying Winners and Selling Losers. Journal of Finance.', 'Bernard, V. y Thomas, J. (1989). Post-Earnings-Announcement Drift. Journal of Accounting Research.',
        'Brown, K., Harlow, W. y Starks, L. (1996). Of Tournaments and Temptations. Journal of Finance.', 'Kahneman, D. y Tversky, A. (1979). Prospect Theory. Econometrica.',
        'Barber, B. y Odean, T. (2000). Trading Is Hazardous to Your Wealth. Journal of Finance.', 'Shefrin, H. y Statman, M. (1985). The Disposition to Sell Winners Too Early. Journal of Finance.'])
    d.p('Contenido de fuentes periodísticas reformulado para cumplir restricciones de licencia.', size=9, italic=True, color='7F7F7F')
    d.save(path, 'Guía Completa · Concurso Carteras de Inversión (CCI)')
