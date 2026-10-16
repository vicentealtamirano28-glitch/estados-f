// Recalcula todas las fórmulas del Excel con un motor independiente (HyperFormula) y las compara
// con los valores calculados en Python. Uso: node verificar_excel.cjs <ruta al .xlsx>
const X = require('xlsx');
const { HyperFormula } = require('hyperformula');

const wb = X.readFile(process.argv[2], { cellFormula: true });
const sheets = {};
for (const n of wb.SheetNames) {
  const s = wb.Sheets[n];
  const rg = X.utils.decode_range(s['!ref']);
  sheets[n] = [];
  for (let r = 0; r <= rg.e.r; r++) {
    const row = [];
    for (let c = 0; c <= rg.e.c; c++) {
      const cell = s[X.utils.encode_cell({ r, c })];
      row.push(!cell ? null : cell.f ? '=' + cell.f : cell.v);
    }
    sheets[n].push(row);
  }
}
const hf = HyperFormula.buildFromSheets(sheets, { licenseKey: 'gpl-v3' });
let total = 0;
const fallas = [];
for (const n of wb.SheetNames) {
  const s = wb.Sheets[n];
  const id = hf.getSheetId(n);
  for (const addr of Object.keys(s).filter((k) => !k.startsWith('!'))) {
    if (!s[addr].f) continue;
    total++;
    const { r, c } = X.utils.decode_cell(addr);
    const v = hf.getCellValue({ sheet: id, row: r, col: c });
    const esperado = s[addr].v;
    const ok = typeof v === typeof esperado &&
      (typeof v !== 'number' || Math.abs(v - esperado) <= 1e-9 * Math.max(1, Math.abs(esperado)));
    if (!ok) fallas.push(`${n}!${addr} = ${s[addr].f} -> ${v?.value ?? v} (esperado ${esperado})`);
  }
}
console.log(`${total} fórmulas recalculadas, ${fallas.length} con diferencias`);
fallas.slice(0, 10).forEach((f) => console.log('  ' + f));
process.exit(fallas.length ? 1 : 0);
