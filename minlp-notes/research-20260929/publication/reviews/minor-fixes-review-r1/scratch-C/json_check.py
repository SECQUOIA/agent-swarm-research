"""Group C: compare the seven point JSONs with git HEAD; only the construction string may differ."""
import json, subprocess, difflib
from pathlib import Path
REPO = Path(__file__).resolve().parents[5]
D = 'research-20260929/publication/primal/water-ann-kan/points'
OLD = '(mid, rad)'; NEW = '{lo, hi}'

def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, f'{path}/{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f'{path}[{i}]')
    else:
        yield path, o

files = sorted((REPO / D).glob('*.point.json'))
print(len(files), 'files')
for f in files:
    new_b = f.read_bytes()
    old_b = subprocess.run(['git', '-C', str(REPO), 'show', f'HEAD:{D}/{f.name}'], capture_output=True, check=True).stdout
    # byte level: the only differing bytes must be the replacement
    assert old_b.count(OLD.encode()) == 1 and new_b.count(NEW.encode()) == 1, f.name
    byte_ok = old_b.replace(OLD.encode(), NEW.encode()) == new_b
    o, n = json.loads(old_b), json.loads(new_b)
    lo, ln = dict(walk(o)), dict(walk(n))
    diffkeys = [k for k in set(lo) | set(ln) if lo.get(k, '<missing>') != ln.get(k, '<missing>')]
    # interval format: every dict value in x has exactly lo/hi (no mid/rad), lo <= hi
    from fractions import Fraction as F
    nint = nrat = 0; bad = []
    for name, v in n['x'].items():
        if isinstance(v, dict):
            nint += 1
            if set(v) != {'lo', 'hi'}: bad.append((name, sorted(v)))
            elif not F(v['lo']) <= F(v['hi']): bad.append((name, 'lo>hi'))
        else:
            nrat += 1; F(v)
    other_mid = [k for k in ln if k.split('/')[-1] in ('mid', 'rad')]
    print(f.name, 'byte-identical-after-replacement', byte_ok, 'differing leaves', diffkeys,
          'x: intervals', nint, 'rationals', nrat, 'bad', bad[:3], 'mid/rad keys anywhere', len(other_mid))
    print('   construction tail:', n['construction'][-70:])
