import { getDocument } from 'pdfjs-dist/legacy/build/pdf.mjs';
const [file, from = '1', to = '3'] = process.argv.slice(2);
const doc = await getDocument({ url: file, verbosity: 0 }).promise;
console.log(`# ${file} (${doc.numPages} págs)`);
for (let p = +from; p <= Math.min(+to, doc.numPages); p++) {
  const c = await (await doc.getPage(p)).getTextContent();
  let line = '', out = [], lastY;
  for (const it of c.items) { const y = Math.round(it.transform[5]); if (lastY !== undefined && Math.abs(y - lastY) > 2) { out.push(line); line = ''; } line += it.str + ' '; lastY = y; }
  out.push(line);
  console.log(`--- p${p}\n` + out.map(s => s.replace(/\s+/g, ' ').trim()).filter(Boolean).join('\n'));
}
