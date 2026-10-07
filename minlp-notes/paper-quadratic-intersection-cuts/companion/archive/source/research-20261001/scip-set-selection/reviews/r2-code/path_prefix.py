"""Review r2: do stock and patched-scip logs follow the same search path?

Compares node-display rows (all columns except time and memory) between
logs/full_stock/X.scip.sS.log and logs/full/X.scip.sS.log. Usage: path_prefix.py inst:seed ...
"""
import re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]


def rows(p):
    out = []
    for l in p.read_text(errors='replace').splitlines():
        m = re.match(r'^[ a-zA-Z*]?\s*[0-9.]+s\|(.*)$', l)
        if m:
            c = m.group(1).split('|')
            out.append('|'.join(c[:4] + c[5:]))
    return out


def last(p, pat):
    m = re.search(pat, p.read_text(errors='replace'), re.M)
    return m.group(1) if m else None


for arg in sys.argv[1:]:
    inst, seed = arg.split(':')
    a = BASE / f'logs/full_stock/{inst}.scip.s{seed}.log'
    b = BASE / f'logs/full/{inst}.scip.s{seed}.log'
    ra, rb = rows(a), rows(b)
    k = 0
    while k < min(len(ra), len(rb)) and ra[k] == rb[k]:
        k += 1
    print(f'{inst} s{seed}: stock rows {len(ra)} ({last(a, r"^SCIP Status\s*: (.*)$")}, {last(a, r"^Solving Time.*: (\S+)")} s, '
          f'{last(a, r"^Solving Nodes\s*: (\d+)")} nodes); patched rows {len(rb)} ({last(b, r"^SCIP Status\s*: (.*)$")}, '
          f'{last(b, r"^Solving Time.*: (\S+)")} s, {last(b, r"^Solving Nodes\s*: (\d+)")} nodes); identical leading rows {k}')
    if k < min(len(ra), len(rb)):
        print('   first differing stock row  :', ra[k][:110])
        print('   first differing patched row:', rb[k][:110])
    else:
        print('   last common row:', (ra if len(ra) <= len(rb) else rb)[k - 1][:110])


# Speed on the shared prefix: CPU time printed on the last identical display row.
def timed_rows(p):
    out = []
    for l in p.read_text(errors='replace').splitlines():
        m = re.match(r'^[ a-zA-Z*]?\s*([0-9.]+)s\|(.*)$', l)
        if m:
            c = m.group(2).split('|')
            out.append((float(m.group(1)), '|'.join(c[:4] + c[5:])))
    return out


print('\nCPU time on the last identical display row (stock vs patched):')
for arg in sys.argv[1:]:
    inst, seed = arg.split(':')
    ra = timed_rows(BASE / f'logs/full_stock/{inst}.scip.s{seed}.log')
    rb = timed_rows(BASE / f'logs/full/{inst}.scip.s{seed}.log')
    k = 0
    while k < min(len(ra), len(rb)) and ra[k][1] == rb[k][1]:
        k += 1
    if k:
        print(f'  {inst} s{seed}: row {k}, node col "{ra[k-1][1].split("|")[0].strip()}", stock {ra[k-1][0]} s, patched {rb[k-1][0]} s, ratio {rb[k-1][0] / max(ra[k-1][0], 1e-9):.3f}')
