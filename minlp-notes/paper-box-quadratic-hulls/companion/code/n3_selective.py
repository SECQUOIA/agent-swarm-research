"""Selective family separation on the n = 3 pool objectives.
For each pool objective: start from B (PSD+RLT+all 4 triangles), then
  blocks: add a 5x5 family block for every orientation violated (StQP < -tol)
          at the current point, re-solve; repeat.
  cuts:   add the single StQP-optimal family inequality of every violated
          orientation, re-solve; repeat.
Record rounds, blocks/cuts, and the bound after each round (X is exact).
Usage: python n3_selective.py pool.jsonl out.jsonl [tol]"""
import sys, json
import numpy as np
sys.path.insert(0, '.')
from relax import separate_family, ORIENTS
from n3_study import build


def loop(H, g, kind, tol, max_rounds=30):
    R = build(H, g, '')
    T = np.array([[0, 1, 2]])
    hist = []
    for rnd in range(max_rounds):
        res = R.solve('clarabel', tol=1e-10)
        viol = separate_family(res['xv'], res['Y'], T, tol=tol)
        hist.append({'round': rnd, 'bound': res['pobj'], 'safe': res['safe'], 'blocks': len(R.F_added),
                     'cuts': R.ncuts['Fcut'], 'nviol': len(viol), 'time': res['time_solve'],
                     'worst': min([v[2] for v in viol]) if viol else 0.0})
        if not viol:
            break
        for (r, oi, val, v, h) in viol:
            if kind == 'blocks':
                R.add_F((0, 1, 2), ORIENTS[oi])
            else:
                R.add_Fcut((0, 1, 2), ORIENTS[oi], np.append(v, h))
    return hist


def main():
    pool, out = sys.argv[1], sys.argv[2]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-7
    with open(out, 'w') as f:
        for i, line in enumerate(open(pool)):
            r = json.loads(line)
            H, g = np.array(r['H']), np.array(r['g'])
            rec = {'i': i, 'B': r['B'] - r['c0'], 'X': r['X'] - r['c0'], 'X_safe': r['X_safe'] - r['c0']}
            for kind in ('blocks', 'cuts'):
                rec[kind] = loop(H, g, kind, tol)
            f.write(json.dumps(rec) + '\n')
            f.flush()


if __name__ == '__main__':
    main()
