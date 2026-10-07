"""Map each references.bib key to the provenance comment that sits directly above
the same key in the W1 source files process/w1/lit-core.bib and lit-ext.bib."""
import re

def entries_with_comments(path):
    lines = open(path).read().split('\n')
    out = {}
    for i, l in enumerate(lines):
        m = re.match(r'@\w+\{([^,]+),', l)
        if not m:
            continue
        j, com = i - 1, []
        while j >= 0 and lines[j].startswith('%') and not lines[j].startswith('% ---'):
            com.insert(0, lines[j]); j -= 1
        out[m.group(1)] = com
    return out

def bib_entries(path):
    t = open(path).read()
    return {m.group(2): m.group(0) for m in re.finditer(r'@(\w+)\{([^,]+),.*?\n\}', t, re.S)}

if __name__ == '__main__':
    core = entries_with_comments('process/w1/lit-core.bib')
    ext = entries_with_comments('process/w1/lit-ext.bib')
    cur = bib_entries('references.bib')
    for k in sorted(cur, key=str.lower):
        src = 'core' if k in core else 'ext' if k in ext else '-'
        com = core.get(k) or ext.get(k) or []
        both = ' (BOTH)' if k in core and k in ext else ''
        print(f'{k:34s} {src}{both}: {" / ".join(com)}')
