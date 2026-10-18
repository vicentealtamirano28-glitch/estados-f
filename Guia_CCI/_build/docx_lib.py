"""Generador minimo de .docx (WordprocessingML) sin dependencias externas."""
import zipfile, struct, re, datetime
from xml.sax.saxutils import escape

NAVY = '1F3864'; BLUE = '2E75B6'
EMU_CM = 360000

def _esc(t):
    return escape(t, {'"': '&quot;'})

def _png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    w, h = struct.unpack('>II', head[16:24])
    return w, h

def _runs(text, size=None, color=None, bold=False, italic=False, font=None):
    """Convierte texto con **negrita** y __cursiva__ en runs."""
    out = []
    parts = re.split(r'(\*\*.+?\*\*|__.+?__)', text)
    for p in parts:
        if not p:
            continue
        b, i = bold, italic
        if p.startswith('**') and p.endswith('**'):
            p = p[2:-2]; b = True
        elif p.startswith('__') and p.endswith('__'):
            p = p[2:-2]; i = True
        rpr = ''
        if font: rpr += f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>'
        if b: rpr += '<w:b/>'
        if i: rpr += '<w:i/>'
        if color: rpr += f'<w:color w:val="{color}"/>'
        if size: rpr += f'<w:sz w:val="{int(size*2)}"/><w:szCs w:val="{int(size*2)}"/>'
        segs = p.split('\n')
        for k, sgm in enumerate(segs):
            br = '<w:br/>' if k > 0 else ''
            out.append(f'<w:r><w:rPr>{rpr}</w:rPr>{br}<w:t xml:space="preserve">{_esc(sgm)}</w:t></w:r>')
    return ''.join(out)


class Doc:
    def __init__(self, title='Documento', author='Guia CCI'):
        self.body = []
        self.media = []
        self.title = title
        self.author = author
        self._bm = 0

    # ---------- bloques ----------
    def h(self, level, text):
        self._bm += 1
        self.body.append(f'<w:p><w:pPr><w:pStyle w:val="Heading{level}"/></w:pPr>'
                         f'<w:bookmarkStart w:id="{self._bm}" w:name="_h{self._bm}"/>{_runs(text)}<w:bookmarkEnd w:id="{self._bm}"/></w:p>')

    def p(self, text, align=None, size=None, color=None, bold=False, italic=False, space_after=None, style=None):
        ppr = ''
        if style: ppr += f'<w:pStyle w:val="{style}"/>'
        if space_after is not None: ppr += f'<w:spacing w:after="{space_after}"/>'
        if align: ppr += f'<w:jc w:val="{align}"/>'
        self.body.append(f'<w:p><w:pPr>{ppr}</w:pPr>{_runs(text, size, color, bold, italic)}</w:p>')

    def bullets(self, items, numbered=False, level=0):
        nid = 2 if numbered else 1
        if numbered:
            self._numinst = getattr(self, '_numinst', 2) + 1
            nid = self._numinst
            self._numbered_ids = getattr(self, '_numbered_ids', []) + [nid]
        for it in items:
            lvl = level
            if isinstance(it, tuple):
                lvl, it = it
            self.body.append(f'<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr><w:ilvl w:val="{lvl}"/><w:numId w:val="{nid}"/></w:numPr>'
                             f'<w:spacing w:after="60"/></w:pPr>{_runs(it)}</w:p>')

    def numbered(self, items):
        self.bullets(items, numbered=True)

    def formula(self, text, note=None):
        self.body.append('<w:p><w:pPr><w:pStyle w:val="Formula"/></w:pPr>' + _runs(text, font='Cambria Math') + '</w:p>')
        if note:
            self.p(note, align='center', size=9, color='595959', italic=True)

    def table(self, header, rows, widths=None, header_fill=NAVY, font_size=9.5, zebra=True, first_col_bold=False):
        n = len(header)
        total = 9600
        if not widths:
            widths = [total // n] * n
        else:
            s = sum(widths); widths = [int(w * total / s) for w in widths]
        grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
        def cell(t, w, fill=None, bold=False, color=None):
            shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ''
            paras = ''.join(f'<w:p><w:pPr><w:spacing w:before="20" w:after="20"/></w:pPr>{_runs(line, font_size, color, bold)}</w:p>' for line in str(t).split('\n\n'))
            return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{shd}<w:tcMar><w:top w:w="50" w:type="dxa"/><w:bottom w:w="50" w:type="dxa"/></w:tcMar></w:tcPr>{paras}</w:tc>'
        trs = '<w:tr><w:trPr><w:tblHeader/></w:trPr>' + ''.join(cell(t, w, header_fill, True, 'FFFFFF') for t, w in zip(header, widths)) + '</w:tr>'
        for i, r in enumerate(rows):
            fill = 'EEF3FA' if (zebra and i % 2 == 1) else None
            trs += '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + ''.join(cell(t, w, fill, first_col_bold and j == 0) for j, (t, w) in enumerate(zip(r, widths))) + '</w:tr>'
        borders = ''.join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>' for b in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'])
        self.body.append(f'<w:tbl><w:tblPr><w:tblW w:w="{total}" w:type="dxa"/><w:tblBorders>{borders}</w:tblBorders>'
                         f'<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="90" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr>'
                         f'<w:tblGrid>{grid}</w:tblGrid>{trs}</w:tbl>')
        self.p('', space_after=60)

    def callout(self, title, text, kind='info'):
        colors = {'info': ('DDEBF7', '2E75B6'), 'tip': ('E2EFDA', '548235'), 'warn': ('FCE4D6', 'C00000'), 'key': ('FFF2CC', 'BF8F00'), 'tesis': ('EDE2F6', '7030A0')}
        fill, edge = colors[kind]
        paras = f'<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>{_runs(title, 10.5, edge, True)}</w:p>'
        for blk in text if isinstance(text, list) else [text]:
            paras += f'<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>{_runs(blk, 10)}</w:p>'
        b = f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{edge}"/>'
        self.body.append(f'<w:tbl><w:tblPr><w:tblW w:w="9600" w:type="dxa"/><w:tblBorders>{b}</w:tblBorders>'
                         f'<w:tblCellMar><w:top w:w="100" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tblCellMar></w:tblPr>'
                         f'<w:tblGrid><w:gridCol w:w="9600"/></w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc><w:tcPr><w:tcW w:w="9600" w:type="dxa"/>'
                         f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:tcPr>{paras}</w:tc></w:tr></w:tbl>')
        self.p('', space_after=40)

    def image(self, path, width_cm=16.5, caption=None):
        w, h = _png_size(path)
        cx = int(width_cm * EMU_CM); cy = int(cx * h / w)
        max_h = int(22 * EMU_CM)
        if cy > max_h:
            cy = max_h; cx = int(cy * w / h)
        idx = len(self.media) + 1
        rid = f'rIdImg{idx}'
        self.media.append((rid, f'image{idx}.png', path))
        self.body.append(
            f'<w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="center"/></w:pPr><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{idx}" name="Imagen {idx}"/>'
            f'<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="{idx}" name="image{idx}.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            f'</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
        if caption:
            self.p(caption, align='center', size=9, color='595959', italic=True)

    def pagebreak(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def toc(self, title='Contenido'):
        self.p(title, size=16, bold=True, color=NAVY)
        self.body.append('<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
                         '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Haz clic derecho aquí y elige "Actualizar campo" para ver el índice (Word lo hace solo al abrir).</w:t></w:r>'
                         '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>')

    def cover(self, title, subtitle, lines, band_text='GUÍA DE ESTUDIO'):
        self.body.append(f'<w:p><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="{NAVY}"/><w:spacing w:before="0" w:after="0"/></w:pPr>'
                         f'{_runs("  " + band_text, 12, "FFFFFF", True)}</w:p>')
        for _ in range(5): self.p('')
        self.p(title, size=30, bold=True, color=NAVY, space_after=120)
        self.p(subtitle, size=15, color=BLUE, space_after=400)
        for l in lines:
            self.p(l, size=11, color='404040', space_after=60)
        self.pagebreak()

    # ---------- empaquetado ----------
    def save(self, path, header_text=None):
        W = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
             'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
             'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
             'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
             'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
        sect = ('<w:sectPr><w:headerReference w:type="default" r:id="rIdHdr"/><w:footerReference w:type="default" r:id="rIdFtr"/>'
                '<w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1300" w:right="1300" w:bottom="1200" w:left="1300" w:header="600" w:footer="600" w:gutter="0"/>'
                '<w:titlePg/></w:sectPr>')
        document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>{"".join(self.body)}{sect}</w:body></w:document>'
        ht = header_text or self.title
        header = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {W}><w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" w:color="{BLUE}"/></w:pBdr>'
                  f'<w:jc w:val="right"/></w:pPr>{_runs(ht, 8.5, "7F7F7F")}</w:p></w:hdr>')
        footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr {W}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                  '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">Página </w:t></w:r>'
                  '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
                  '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="18"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
                  '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
                  '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="18"/></w:rPr><w:t>1</w:t></w:r>'
                  '<w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')
        def hstyle(n, size, color, before, after, page_break=False):
            pb = '<w:pageBreakBefore/>' if page_break else ''
            border = f'<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="2" w:color="{BLUE}"/></w:pBdr>' if n == 1 else ''
            return (f'<w:style w:type="paragraph" w:styleId="Heading{n}"><w:name w:val="heading {n}"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
                    f'<w:pPr><w:keepNext/><w:keepLines/>{pb}{border}<w:spacing w:before="{before}" w:after="{after}"/><w:outlineLvl w:val="{n-1}"/></w:pPr>'
                    f'<w:rPr><w:b/><w:color w:val="{color}"/><w:sz w:val="{size*2}"/><w:szCs w:val="{size*2}"/></w:rPr></w:style>')
        styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                  '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                  '<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/><w:sz w:val="21"/><w:szCs w:val="21"/><w:lang w:val="es-CL"/></w:rPr></w:rPrDefault>'
                  '<w:pPrDefault><w:pPr><w:spacing w:after="110" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
                  '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="both"/></w:pPr></w:style>'
                  + hstyle(1, 18, NAVY, 240, 160, True) + hstyle(2, 13.5 if False else 14, BLUE, 260, 100) + hstyle(3, 12, '404040', 200, 80) +
                  '<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720"/><w:jc w:val="left"/></w:pPr></w:style>'
                  '<w:style w:type="paragraph" w:styleId="Formula"><w:name w:val="Formula"/><w:basedOn w:val="Normal"/><w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>'
                  '<w:spacing w:before="60" w:after="60"/><w:jc w:val="center"/></w:pPr><w:rPr><w:color w:val="1F3864"/><w:sz w:val="23"/></w:rPr></w:style>'
                  '<w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:after="60"/></w:pPr><w:rPr><w:b/></w:rPr></w:style>'
                  '<w:style w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:after="40"/><w:ind w:left="300"/></w:pPr></w:style>'
                  '<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/><w:rPr><w:color w:val="0563C1"/><w:u w:val="single"/></w:rPr></w:style>'
                  '</w:styles>')
        def absnum(aid, fmt_list):
            lv = ''
            for i, (fmt, txt, ind) in enumerate(fmt_list):
                rpr = '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr>' if fmt == 'bullet' and txt == '\uf0b7' else ''
                lv += (f'<w:lvl w:ilvl="{i}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/><w:lvlText w:val="{txt}"/><w:lvlJc w:val="left"/>'
                       f'<w:pPr><w:ind w:left="{ind}" w:hanging="300"/></w:pPr>{rpr}</w:lvl>')
            return f'<w:abstractNum w:abstractNumId="{aid}"><w:multiLevelType w:val="hybridMultilevel"/>{lv}</w:abstractNum>'
        nums = [absnum(0, [('bullet', '\uf0b7', 600), ('bullet', 'o', 1100), ('bullet', '\u25aa', 1600)]),
                absnum(1, [('decimal', '%1.', 600), ('lowerLetter', '%2)', 1100), ('lowerRoman', '%3.', 1600)])]
        inst = '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num><w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>'
        for nid in getattr(self, '_numbered_ids', []):
            inst += f'<w:num w:numId="{nid}"><w:abstractNumId w:val="1"/><w:lvlOverride w:ilvl="0"><w:startOverride w:val="1"/></w:lvlOverride></w:num>'
        numbering = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                     + ''.join(nums) + inst + '</w:numbering>')
        settings = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                    '<w:defaultTabStop w:val="708"/><w:updateFields w:val="true"/><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>')
        rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                '<Relationship Id="rIdNum" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
                '<Relationship Id="rIdSet" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
                '<Relationship Id="rIdHdr" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>'
                '<Relationship Id="rIdFtr" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
                + ''.join(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fn}"/>' for rid, fn, _ in self.media)
                + '</Relationships>')
        ctypes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                  '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
                  '<Default Extension="png" ContentType="image/png"/>'
                  '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                  '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                  '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
                  '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
                  '<Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>'
                  '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
                  '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
                  '</Types>')
        root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                     '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                     '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>')
        now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                f'<dc:title>{_esc(self.title)}</dc:title><dc:creator>{_esc(self.author)}</dc:creator>'
                f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created></cp:coreProperties>')
        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', ctypes); z.writestr('_rels/.rels', root_rels); z.writestr('docProps/core.xml', core)
            z.writestr('word/document.xml', document); z.writestr('word/styles.xml', styles); z.writestr('word/numbering.xml', numbering)
            z.writestr('word/settings.xml', settings); z.writestr('word/header1.xml', header); z.writestr('word/footer1.xml', footer)
            z.writestr('word/_rels/document.xml.rels', rels)
            for rid, fn, src in self.media:
                z.write(src, f'word/media/{fn}')
        return path
