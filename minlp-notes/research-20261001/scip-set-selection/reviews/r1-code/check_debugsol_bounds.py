"""Review r1: final/root dual bounds and reported optima of the debug-solution runs against minlplib.solu."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recompute import parse, load_ref, LOGS
ref, tag, sense = load_ref()
for d in ('debugsol', 'debugsol_withsym'):
    recs = [parse(os.path.join(LOGS, d, f)) for f in sorted(os.listdir(os.path.join(LOGS, d))) if f.endswith('.s0.log')]
    nf = nr = bf = br = 0
    for r in recs:
        i = r['inst']; sg = -1 if sense[i] == 'max' else 1; tol = 1e-6 * max(1, abs(ref[i]))
        if r['dual'] is not None:
            nf += 1; bf += sg * (r['dual'] - ref[i]) > tol
        if r['rootdb'] is not None:
            nr += 1; br += sg * (r['rootdb'] - ref[i]) > tol
        if r['status'] and 'optimal' in r['status'] and abs(r['primal'] - ref[i]) > tol:
            print(d, 'reported optimum differs:', i, r['setting'], '%.15g' % r['primal'], 'ref', ref[i], 'diff %.4g' % (r['primal'] - ref[i]))
    print(d, 'runs', len(recs), 'final bounds', nf, 'excluding ref', bf, 'root bounds', nr, 'excluding ref', br)
