import re, sys
def cells(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|') and not s.endswith('\\|'): s = s[:-1]
    # split on unescaped pipes (GFM splits even inside code spans)
    parts = re.split(r'(?<!\\)\|', s)
    return len(parts)
delim = re.compile(r'^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$')
for path in sys.argv[1:]:
    lines = open(path, encoding='utf-8').read().split('\n')
    i = 0
    in_code = False
    while i < len(lines):
        l = lines[i]
        if l.strip().startswith('```'):
            in_code = not in_code; i += 1; continue
        if not in_code and '|' in l and i + 1 < len(lines) and delim.match(lines[i+1]) and '-' in lines[i+1]:
            h = cells(l); d = cells(lines[i+1])
            if h != d:
                print(f"{path}:{i+1}: header {h} cells vs delimiter {d} (table not rendered)")
            j = i + 2
            while j < len(lines) and lines[j].strip() and '|' in lines[j]:
                c = cells(lines[j])
                if c != d:
                    print(f"{path}:{j+1}: {c} cells vs {d}")
                j += 1
            i = j; continue
        i += 1
