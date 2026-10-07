"""Reviewer r2: read Zenodo 14961066 xlsx sheets with zipfile+XML (no openpyxl) and print KAN rows."""
import zipfile, re, sys, xml.etree.ElementTree as ET
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def sheets(path):
    z = zipfile.ZipFile(path)
    ss = []
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', NS):
            ss.append(''.join(t.text or '' for t in si.iter('{%s}t' % NS['m'])))
    wb = ET.fromstring(z.read('xl/workbook.xml'))
    rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
    rmap = {r.get('Id'): r.get('Target') for r in rels}
    out = {}
    for sh in wb.find('m:sheets', NS):
        tgt = rmap[sh.get('{%s}id' % NS['r'])]
        tgt = tgt.lstrip('/'); tgt = tgt if tgt.startswith('xl/') else 'xl/' + tgt
        rows = []
        for row in ET.fromstring(z.read(tgt)).iter('{%s}row' % NS['m']):
            vals = {}
            for c in row.findall('m:c', NS):
                col = re.match(r'[A-Z]+', c.get('r')).group(0)
                v = c.find('m:v', NS); t = c.get('t')
                if v is None:
                    isv = c.find('m:is', NS)
                    val = ''.join(x.text or '' for x in isv.iter('{%s}t' % NS['m'])) if isv is not None else ''
                else:
                    val = ss[int(v.text)] if t == 's' else v.text
                vals[col] = val
            rows.append(vals)
        out[sh.get('name')] = rows
    return out
want = sys.argv[2].split(',')
for name, rows in sheets(sys.argv[1]).items():
    hdr = rows[0]
    for r in rows[1:]:
        if r.get('A') in want:
            print(name, {hdr.get(k, k): v for k, v in r.items()})
