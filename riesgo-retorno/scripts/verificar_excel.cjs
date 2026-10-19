// Recalcula el Excel con un motor independiente (HyperFormula) y compara las fórmulas
// deterministas con valores esperados calculados aparte (JSON de verificar.py).
// Uso: node verificar_excel.cjs <xlsx> <esperados.json>   (requiere npm install xlsx hyperformula)
const fs = require('fs');
const X = require('xlsx');
const { HyperFormula } = require('hyperformula');

const wb = X.readFile(process.argv[2], { cellFormula: true, sheetStubs: true });
const esperados = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const sheets = {};
let formulas = 0;
for (const n of wb.SheetNames) {
  const s = wb.Sheets[n];
  const rg = X.utils.decode_range(s['!ref']);
  sheets[n] = [];
  for (let r = 0; r <= rg.e.r; r++) {
    const row = [];
    for (let c = 0; c <= rg.e.c; c++) {
      const cell = s[X.utils.encode_cell({ r, c })];
      if (cell && cell.f) formulas++;
      row.push(!cell ? null : cell.f ? '=' + cell.f.replace(/_xlfn\./g, '') : cell.v);
    }
    sheets[n].push(row);
  }
}
const hf = HyperFormula.buildFromSheets(sheets, { licenseKey: 'gpl-v3' });
const valor = (ref) => {
  const [hoja, celda] = ref.split('!');
  const { r, c } = X.utils.decode_cell(celda);
  return hf.getCellValue({ sheet: hf.getSheetId(hoja), row: r, col: c });
};

// 1) Ninguna fórmula debe dar error.
const errores = [];
for (const n of wb.SheetNames) {
  const s = wb.Sheets[n];
  for (const a of Object.keys(s).filter((k) => !k.startsWith('!') && s[k].f)) {
    const v = valor(`${n}!${a}`);
    if (typeof v !== 'number' || !isFinite(v)) errores.push(`${n}!${a} = ${s[a].f} -> ${v?.value ?? v}`);
  }
}
// 2) Las fórmulas deterministas deben coincidir con el cálculo independiente.
const fallas = [];
for (const [ref, esp] of Object.entries(esperados)) {
  const v = valor(ref);
  if (typeof v !== 'number' || Math.abs(v - esp) > 1e-9 * Math.max(1, Math.abs(esp))) fallas.push(`${ref}: ${v} (esperado ${esp})`);
}
console.log(`${formulas} fórmulas, ${errores.length} con error; ${Object.keys(esperados).length} valores comparados, ${fallas.length} con diferencias`);
[...errores, ...fallas].slice(0, 15).forEach((f) => console.log('  ' + f));
process.exit(errores.length || fallas.length ? 1 : 0);
