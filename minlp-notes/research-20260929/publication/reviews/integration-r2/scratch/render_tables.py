# Render Markdown with markdown-it (GFM tables) and report every table: header cells, body rows,
# rows whose source cell count differs from the header, and pipe-led lines not inside any table.
import sys, re
from markdown_it import MarkdownIt
md = MarkdownIt('commonmark').enable('table')
def cells(line):
    s = line.strip()
    s = re.sub(r'\\\|', '', s)
    # ignore pipes inside inline code spans
    s = re.sub(r'`[^`]*`', '', s)
    return s.strip('|').count('|') + 1
for path in sys.argv[1:]:
    src = open(path).read().split('\n')
    toks = md.parse('\n'.join(src))
    in_table = set(); tables = []
    for i, t in enumerate(toks):
        if t.type == 'table_open':
            a, b = t.map; in_table.update(range(a, b))
            hdr = cells(src[a]); body = [src[k] for k in range(a + 2, b)]
            bad = [a + 3 + j for j, l in enumerate(body) if cells(l) != hdr]
            tables.append((a + 1, hdr, len(body), bad))
    orphans = [k + 1 for k, l in enumerate(src) if l.lstrip().startswith('|') and k not in in_table]
    print(f'== {path}: {len(tables)} tables')
    for start, hdr, n, bad in tables:
        print(f'  line {start}: {hdr} columns, {n} body rows' + (f'; cell-count mismatch at lines {bad}' if bad else ''))
    print('  pipe-led lines outside tables:', orphans if orphans else 'none')
