// Genera wacc/WACC_2020_2025.xlsx con fórmulas a la vista a partir de data/*.json.
// Uso (desde una carpeta con exceljs instalado): node excel.mjs <ruta a wacc/>
import ExcelJS from 'exceljs';
import fs from 'node:fs';
import path from 'node:path';

const dir = path.resolve(process.argv[2] ?? '.');
const read = (f) => JSON.parse(fs.readFileSync(path.join(dir, 'data', f), 'utf8'));
const filas = read('wacc.json');
const mercado = read('mercado.json');
const dam = mercado.damodaran;
const ANIOS = [2020, 2021, 2022, 2023, 2024, 2025];
const ARCHIVO = { SQM: 'sqm', CAP: 'cap', Molymet: 'molymet', Enaex: 'enaex', 'Minera Valparaíso': 'minera_valparaiso' };
const PCT = '0.00%';
const NUM = '#,##0';
const AZUL = 'FF1A2740';

const wb = new ExcelJS.Workbook();
wb.creator = 'WACC tesina opciones reales';
const res = wb.addWorksheet('Resumen', { properties: { tabColor: { argb: 'FF2E7D32' } } });

function encabezado(ws, titulos, anchos) {
  ws.addRow(titulos);
  const r = ws.getRow(1);
  r.font = { bold: true, color: { argb: 'FFFFFFFF' } };
  r.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: AZUL } };
  r.alignment = { wrapText: true, vertical: 'middle' };
  r.height = 32;
  anchos.forEach((w, i) => (ws.getColumn(i + 1).width = w));
  ws.views = [{ state: 'frozen', ySplit: 1 }];
}

const sup = wb.addWorksheet('Supuestos');
encabezado(sup, ['Año', 'Rf (T-Bond 10 años EE.UU.)', 'ERP implícita (Damodaran)', 'Riesgo país Chile (CRP)',
  'Rating Moody\'s Chile', 'Fuente Rf y ERP', 'Fuente CRP', '', 'Tasa de impuesto (t)', 'Valor'],
  [7, 14, 14, 14, 10, 48, 52, 2, 26, 10]);
ANIOS.forEach((a) => sup.addRow([a, dam.rf_tbond_10y.valores[a], dam.erp_implicita.valores[a],
  dam.crp_chile.valores[a], dam.crp_chile.rating[a], dam.rf_tbond_10y.fuente, dam.crp_chile.fuentes[a]]));
for (const c of ['B', 'C', 'D']) for (let r = 2; r <= 7; r++) sup.getCell(`${c}${r}`).numFmt = PCT;
sup.getCell('I2').value = 'Tasa legal Chile (régimen general)';
sup.getCell('J2').value = 0.27;
sup.getCell('J2').numFmt = PCT;
sup.getCell('A10').value = 'Notas';
sup.getCell('A10').font = { bold: true };
[
  'Rf y ERP: columnas "T.Bond Rate" e "Implied ERP (FCFE)" de histimpl.xls, valor al cierre de cada año.',
  'CRP: columna "Country Risk Premium" (basada en rating) de cada archivo anual ctryprem; cada archivo se publica el 1 de enero siguiente y refleja el cierre del año.',
  'Control: la ERP madura de cada ctryprem (Total ERP − CRP) coincide con la ERP implícita de histimpl para ese año.',
  'No se usa "Rf ajustada" por default spread de EE.UU.: se usa el rendimiento del T-Bond tal cual.',
  'Todas las empresas reportan en USD, así que Ke y WACC son tasas en USD (sin ajuste por devaluación del peso).',
].forEach((t, i) => (sup.getCell(`A${11 + i}`).value = t));

const bet = wb.addWorksheet('Betas');
encabezado(bet, ['Industria (Damodaran, mercados emergentes)', ...ANIOS, 'Fuente'], [40, 9, 9, 9, 9, 9, 9, 60]);
for (const [ind, v] of Object.entries(dam.beta_desapalancado_em.industrias))
  bet.addRow([ind, ...ANIOS.map((a) => v[a]), 'Unlevered beta, hoja "Industry Averages" de betaemerg (un archivo por año, ver Supuestos)']);
for (let r = 2; r <= bet.rowCount; r++) for (let c = 2; c <= 7; c++) bet.getRow(r).getCell(c).numFmt = '0.00';
const nInd = bet.rowCount;

const dat = wb.addWorksheet('Datos');
encabezado(dat, ['Empresa', 'Año', 'Acciones en circulación (serie única o A)', 'Precio cierre CLP (serie única o A)',
  'Acciones serie B', 'Precio cierre CLP serie B', 'Dólar observado (CLP/USD)', 'Deuda financiera D (MUS$)',
  'Costos financieros (MUS$)', 'Patrimonio total (MUS$)', 'Patrimonio controladora (MUS$)', 'Industria base',
  'Industria alternativa', 'Fuentes (archivo, página del PDF)'],
  [18, 6, 16, 14, 14, 14, 12, 16, 14, 16, 16, 22, 26, 90]);
const contable = Object.fromEntries(Object.entries(ARCHIVO).map(([e, f]) => {
  const raw = read(`${f}.json`);
  return [e, raw.anios ?? raw.anos];
}));
for (const f of filas) {
  const y = contable[f.empresa][String(f.anio)];
  const ref = (k) => (y[k]?.archivo ? `${k}: ${y[k].archivo} p.${y[k].pagina}` : '');
  const fuentes = ['prestamos_que_devengan_intereses_total', 'costos_financieros', 'patrimonio_total',
    'patrimonio_atribuible_controladora'].map(ref).filter(Boolean).join(' | ');
  dat.addRow([f.empresa, f.anio, f.acciones[0], f.precios_clp[0], f.acciones[1] ?? 0, f.precios_clp[1] ?? 0, f.dolar,
    f.deuda, f.costos_financieros, y.patrimonio_total.valor, y.patrimonio_atribuible_controladora.valor,
    f.base.industria, f.alt.industria, fuentes]);
}
for (let r = 2; r <= dat.rowCount; r++) {
  for (const c of ['C', 'D', 'E', 'F', 'H', 'I', 'J', 'K']) dat.getCell(`${c}${r}`).numFmt = NUM;
  dat.getCell(`G${r}`).numFmt = '#,##0.00';
}
dat.getCell(`A${dat.rowCount + 2}`).value =
  'Precios: Yahoo Finance (Bolsa de Santiago), último cierre de cada año. Dólar: mindicador.cl (Banco Central de Chile). Datos contables: estados financieros consolidados auditados de este repositorio; detalle línea por línea en wacc/data/<empresa>.json.';

const w = wb.addWorksheet('WACC');
encabezado(w, ['Empresa', 'Año', 'Capitalización bursátil (MUS$)', 'No controladoras libro (MUS$)', 'E = cap. + no contr.',
  'D deuda financiera', 'Wd = D/(D+E)', 'We = E/(D+E)', 'D/E', 'Deuda promedio', 'Kd bruto', 't', 'Kd neto',
  'Rf', 'ERP', 'CRP Chile', 'βU base', 'βL base', 'Ke base (USD)', 'WACC base (USD)', 'βU alt', 'βL alt', 'Ke alt', 'WACC alt'],
  [18, 6, 15, 15, 15, 14, 10, 10, 8, 14, 9, 7, 9, 8, 8, 8, 8, 8, 10, 10, 8, 8, 9, 9]);
const betaRng = `Betas!$B$2:$G$${nInd}`;
const indRng = `Betas!$A$2:$A$${nInd}`;
const anioHdr = 'Betas!$B$1:$G$1';
filas.forEach((f, i) => {
  const r = i + 2;
  const prevMismaEmpresa = i > 0 && filas[i - 1].empresa === f.empresa;
  const look = (col) => ({ formula: `INDEX(Supuestos!$${col}$2:$${col}$7,MATCH(B${r},Supuestos!$A$2:$A$7,0))` });
  const beta = (indCol) => ({ formula: `INDEX(${betaRng},MATCH(Datos!${indCol}${r},${indRng},0),MATCH(B${r},${anioHdr},0))` });
  const b = f.base, a = f.alt;
  w.addRow([
    { formula: `Datos!A${r}`, result: f.empresa },
    { formula: `Datos!B${r}`, result: f.anio },
    { formula: `(Datos!C${r}*Datos!D${r}+Datos!E${r}*Datos!F${r})/Datos!G${r}/1000`, result: f.market_cap },
    { formula: `Datos!J${r}-Datos!K${r}`, result: f.nci_libro },
    { formula: `C${r}+D${r}`, result: f.E },
    { formula: `Datos!H${r}`, result: f.deuda },
    { formula: `F${r}/(E${r}+F${r})`, result: f.wd },
    { formula: `E${r}/(E${r}+F${r})`, result: f.we },
    { formula: `F${r}/E${r}`, result: f.d_e },
    { formula: prevMismaEmpresa ? `(F${r}+F${r - 1})/2` : `F${r}`, result: f.deuda_promedio },
    { formula: `Datos!I${r}/J${r}`, result: f.kd_bruto },
    { formula: 'Supuestos!$J$2', result: 0.27 },
    { formula: `K${r}*(1-L${r})`, result: f.kd_neto },
    { ...look('B'), result: f.rf }, { ...look('C'), result: f.erp }, { ...look('D'), result: f.crp },
    { ...beta('L'), result: b.beta_u },
    { formula: `Q${r}*(1+(1-L${r})*I${r})`, result: b.beta_l },
    { formula: `N${r}+R${r}*O${r}+P${r}`, result: b.ke },
    { formula: `H${r}*S${r}+G${r}*M${r}`, result: b.wacc },
    { ...beta('M'), result: a.beta_u },
    { formula: `U${r}*(1+(1-L${r})*I${r})`, result: a.beta_l },
    { formula: `N${r}+V${r}*O${r}+P${r}`, result: a.ke },
    { formula: `H${r}*W${r}+G${r}*M${r}`, result: a.wacc },
  ]);
  const row = w.getRow(r);
  [3, 4, 5, 6, 10].forEach((c) => (row.getCell(c).numFmt = NUM));
  [7, 8, 11, 12, 13, 14, 15, 16, 19, 20, 23, 24].forEach((c) => (row.getCell(c).numFmt = PCT));
  [9, 17, 18, 21, 22].forEach((c) => (row.getCell(c).numFmt = '0.00'));
  [19, 20].forEach((c) => (row.getCell(c).font = { bold: true }));
  if (!prevMismaEmpresa) row.getCell(10).note = 'Primer año: no hay balance 2019 en el repositorio, se usa solo el saldo de cierre.';
});

const empresas = [...new Set(filas.map((f) => f.empresa))];
const bloque = (fila0, titulo, col) => {
  res.getCell(`A${fila0}`).value = titulo;
  res.getCell(`A${fila0}`).font = { bold: true, size: 12 };
  const h = res.getRow(fila0 + 1);
  ['Empresa', ...ANIOS].forEach((v, i) => (h.getCell(i + 1).value = v));
  h.font = { bold: true, color: { argb: 'FFFFFFFF' } };
  h.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: AZUL } };
  empresas.forEach((e, j) => {
    const rr = res.getRow(fila0 + 2 + j);
    rr.getCell(1).value = e;
    ANIOS.forEach((a, k) => {
      const idx = filas.findIndex((f) => f.empresa === e && f.anio === a);
      const src = filas[idx];
      const val = { S: src.base.ke, T: src.base.wacc, X: src.alt.wacc }[col];
      rr.getCell(k + 2).value = { formula: `WACC!${col}${idx + 2}`, result: val };
      rr.getCell(k + 2).numFmt = PCT;
    });
  });
  return fila0 + 3 + empresas.length;
};
res.getColumn(1).width = 20;
for (let c = 2; c <= 7; c++) res.getColumn(c).width = 10;
let f0 = bloque(1, 'WACC base (USD)', 'T');
f0 = bloque(f0, 'Ke base (USD): tasa para descontar flujos del accionista, consistente con V = capitalización bursátil', 'S');
f0 = bloque(f0, 'WACC con industria alternativa (sensibilidad del beta)', 'X');
res.getCell(`A${f0}`).value = 'Fórmulas en la hoja WACC. Supuestos y fuentes en Supuestos, Betas y Datos.';

await wb.xlsx.writeFile(path.join(dir, 'WACC_2020_2025.xlsx'));
console.log('ok', path.join(dir, 'WACC_2020_2025.xlsx'));
