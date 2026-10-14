# Pinda Export — versión HTML autónoma

**Abre `index.html` con doble clic.** No necesita instalar nada, ni Node, ni
conexión a internet.

Un solo archivo (~2.100 líneas, 125 KB) con el CSS y el JavaScript dentro.
Puedes enviarlo por correo, subirlo a Drive, abrirlo desde un pendrive o
publicarlo en cualquier hosting estático sin cambiar nada.

## Fotos de las latas — pon las tuyas

El sitio **no trae fotos**: no tuve acceso a internet para descargarlas de
pindakombucha.cl. Mientras falten, cada tarjeta de sabor muestra una
**ilustración SVG de la lata** en el tono del ingrediente, para que no se vea
vacía ni con el icono de imagen rota.

Para poner las reales, copia cuatro archivos en `images/` con estos nombres:

```
images/maqui-cacao.jpg
images/arandano-lavanda.jpg
images/frambuesa-limon-menta.jpg
images/pina-albahaca.jpg
```

No hay que tocar el HTML. Al recargar, cada foto sustituye a su ilustración.
Acepta `.jpg`, `.png`, `.webp` y `.jpeg`: la página los prueba en ese orden y,
si no encuentra ninguno, se queda la ilustración.

Detalles en `images/LEEME.txt`. Recomendado: proporción cercana a 4:5, fondo
transparente o blanco, menos de 300 KB cada una.

## Qué incluye

- Conmutador **ES / EN** (el programa pide uso del inglés; competencia N°9)
- Modo claro / oscuro, que recuerda tu elección
- **Matriz de selección de mercados interactiva**: mueve los pesos de los seis
  criterios y el ranking se recalcula y reordena
- Acordeón por mercado con los hechos, sus fuentes y el razonamiento de cada
  puntaje
- Sección de fuentes con nivel de confianza, incluidas las descartadas
- Formulario de distribuidores (maqueta: no envía datos a ningún servidor)

## Mapeo al programa de la asignatura

| Sección | Unidad | Contenido |
|---|---|---|
| Propuesta, Etapas | 1 | Etapas de internacionalización, perspectiva global |
| Producto | — | Gama, formatos y referente competitivo |
| Entorno | 2 | Entorno político y legal, acuerdos comerciales |
| Mercados, Entrada | 3 | Selección de mercados y modos de ingreso |
| Estrategia | 4 | Adaptación del mix, canales, marca país |
| Distribuidores | 4 | Canal B2B, gestión de venta internacional |
| Fuentes | — | Investigación de marketing y trazabilidad |

## La decisión metodológica

**No hay ninguna cifra de "tamaño del mercado de kombucha".** Es deliberado.

Cinco agregadores de informes dan, para el mercado global de 2025: USD 2,90 /
3,25 / 4,74 / 5,19 / 9,60 mil millones. Divergen hasta **3x para el mismo año**
y ninguno publica metodología. Citar una es un riesgo innecesario.

El caso se apoya en fuentes institucionales (SUBREI, Aduana de Chile,
Siscomex, MAPA, ANVISA, ProChile) y el criterio de tamaño usa **población**
como aproximación declarada. La sección de fuentes documenta la descartada y
el motivo: rechazar datos malos es parte del método.

## El argumento central

Los seis mercados tienen acuerdo vigente con Chile, por dos vías: **ACE N° 35**
(Mercosur, desde 1996) y **Alianza del Pacífico** (protocolo comercial desde el
1 de mayo de 2016). Brasil alcanzó libre comercio en todo el universo tarifario
en enero de 2015; Chile y Uruguay completaron la desgravación.

Eso neutraliza el arancel como variable de decisión y desplaza el peso a
regulación sanitaria y logística. Y ahí aparece el hallazgo que invierte la
conclusión obvia: **Brasil es el único de los seis que define legalmente la
kombucha** (IN n.º 41/2019 del MAPA), pero esa misma norma habilitó a la
industria local — se reportan 249 fabricantes registrados. Claridad regulatoria
y saturación competitiva llegaron juntas.

De ahí la secuencia propuesta: **Argentina → Uruguay → Brasil**. Argentina
primero porque es el único accesible por tierra desde Valdivia, donde
equivocarse sale barato.

## Verificación ejecutada

A diferencia de la versión Next.js, este archivo **sí se pudo ejecutar**. El
JavaScript real se corrió en Node contra un DOM mínimo:

- Los tres scripts ejecutan sin excepción; el render produce ~57 KB de HTML
- 9 secciones + hero presentes; nav, ranking, sliders, footer y logo poblados
- 7/7 fragmentos generados con etiquetas equilibradas
- 20 URLs externas, todas con `rel="noreferrer noopener"`
- 8/8 anclas del menú resuelven a una sección real
- Render verificado en español **y** en inglés
- 199 claves de texto con estructura idéntica en ambos idiomas; 0 cadenas
  largas sin traducir
- **Cero recursos externos**: ninguna imagen, fuente o script remoto

Pruebas de la matriz, contra los datos reales:

- Puntajes de 1 a 5 en rango, con razonamiento bilingüe y fuente existente
- Pesos todos en 0 → devuelve 0, sin división por cero
- Aislando cada criterio, gana el mercado con el valor más alto en él
- Con pesos uniformes el puntaje es exactamente la media normalizada
- Priorizando logística, Argentina sube al primer puesto
- Priorizando tamaño, acceso y regulación, Brasil sube al primero

Dos fallos detectados y corregidos en el proceso: cuatro fuentes estaban
declaradas pero nada las citaba (ahora integradas, incluida la del competidor
Kombuchacha), y dos bugs en mis propios tests — el umbral de detección de
fuentes huérfanas, y que `\b` en JavaScript es ASCII y hacía match de `TODO`
dentro de «método» y «todo el territorio».

### Bug visual corregido tras revisión en navegador

El primer repaso en pantalla mostró un **icono expandido hasta llenar una
tarjeta entera**. Causa: el SVG llevaba la clase `lead-icon`, pero la única
regla que le daba tamaño era `.card > svg.lead-icon`, un selector de **hijo
directo**. Al estar el SVG dentro de un `<h3>` no hacía match, quedaba sin
dimensiones y un SVG sin tamaño ocupa todo el espacio disponible.

No era un fallo puntual sino estructural: **100 de los 111 SVG** del documento
recibían tamaño sólo por selectores de contexto (`.btn svg`, `.proof-item >
svg`…). Bastaba usar un icono en un contexto nuevo sin regla para reproducir el
bug.

Arreglo de fondo: `ic()` y `mark()` añaden siempre una clase base (`ico`,
`brand-mark`) con tamaño propio en el elemento, colocada antes de las reglas de
contexto para que éstas puedan sobrescribirla. Ahora ningún icono puede quedar
sin dimensiones.

Para que no vuelva a pasar se añadió una tercera batería (`css`) que cruza el
marcado generado contra la hoja de estilos:

- Toda clase usada tiene al menos una regla (133 clases / 137 reglas)
- **Todo SVG recibe tamaño de forma autónoma**, no por contexto (111/111)
- Toda variable CSS referenciada está definida (18/18)

En el mismo pase se corrigieron dos problemas más: las tarjetas de sabor
ocultaban su nota hasta el hover —se veían vacías y el texto quedaba fuera de
alcance en táctil y teclado, así que ahora se muestra siempre— y el fondo
translúcido de la cabecera usaba `color-mix(…, transparent)`, cuyo resultado
varía entre navegadores, sustituido por un color con alfa explícito.

**Lo que sigue sin verificar:** el resto del aspecto visual. Las pruebas
validan estructura, lógica y estilos cruzados, pero no hay navegador en el
entorno. Si ves algo descolocado, dilo.

## Antes de entregar

La sección *Fuentes* del sitio los marca en rojo:

1. Población de los seis países: confirmar con Banco Mundial e indicar año
2. Partida arancelaria concreta de la kombucha en cada lista de desgravación
3. Autoridad sanitaria y requisitos de registro por país, vía ProChile
4. Estado actual de medidas no arancelarias en Argentina
5. Etimología de «Pinda»: el colibrí aparece como símbolo de marca en prensa,
   pero **no se verificó** su origen lingüístico. No lo afirmes sin comprobarlo

## Aviso

Trabajo académico para Marketing Internacional (ADMI203-14 / INGI223-20),
Universidad Austral de Chile. No es un sitio oficial de Pinda Kombucha ni está
afiliado a la empresa; las marcas y contenidos citados pertenecen a sus
titulares. El `<meta name="robots" content="noindex, nofollow">` evita que
compita con el sitio real en buscadores.
