"""Review r2 (m1 spot check): st_glmp_fp2 intersection-row reports in logs/debugsol.

For every 'violated row <...intersection...>' printout: helper coefficient sign, line position
relative to the first incumbent ('*' or letter-prefixed display line with a primal bound),
and slack with t_nlobjvar = x3*x4 = 7.6275.
"""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
H = 5.65 * 1.35
tot, minslack, pos, before = 0, 1e9, 0, 0
for s in ('scip', 'corner', 'eff', 'cornerS', 'effS'):
    lines = (BASE / f'logs/debugsol/st_glmp_fp2.{s}.s0.log').read_text(errors='replace').splitlines()
    inc = next((k for k, l in enumerate(lines) if re.match(r'^\s*[a-zA-Z*]\s*[0-9.]+s\|', l)
                or 'feasible solution found' in l), len(lines))
    n = 0
    for k, l in enumerate(lines):
        if l.startswith('***** debug: violated row <') and 'intersection' in l:
            row = lines[k + 1]
            lhs = float(row.split('<=')[0])
            terms = re.findall(r'([+-][0-9.eE+-]+)<(\w+)>\[([^\]]+)\]', row)
            act = sum(float(c) * (H if v == 't_nlobjvar' else float(x)) for c, v, x in terms)
            const = re.search(r'<=\s*([+-]?[0-9.eE+-]+)\s', row.split('<=', 1)[1])
            c0 = float(row.split('<=')[1].split()[0])
            slack = act + c0 - lhs
            hc = [float(c) for c, v, _ in terms if v == 't_nlobjvar']
            n += 1; tot += 1
            minslack = min(minslack, slack)
            pos += bool(hc and hc[0] > 0)
            before += k < inc
    print(s, 'intersection rows', n, 'first incumbent line', inc + 1)
print('total', tot, 'positive helper coef', pos, 'reported before first incumbent', before, 'min slack', repr(minslack))
