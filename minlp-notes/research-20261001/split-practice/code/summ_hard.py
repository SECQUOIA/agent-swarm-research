"""Table for the hard-instance rerun (logs/hard_run2.jsonl, Theorem 1 matrices
'thm1' or Corollary 5 matrices 'cor5'): for each (q, n), planted cover (C)
and a random instance without planted cover (R); a random instance that
happens to have a cover is marked 'R has cover'.  Columns: predicted minimum of q (cover), best {0,+-1}
split with |supp| <= 3 (violation; negative = none violated), exact
enumeration (time, '*' = node cap 5e8 hit), Gurobi |v_i| <= 1 (time and
status), SCIP |v_i| <= 1 (time and status; run only for q <= 10).
Usage: python3 summ_hard.py KIND"""
import json, os, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kind = sys.argv[1] if len(sys.argv) > 1 else 'thm1'
by = collections.defaultdict(dict)
for l in open(os.path.join(ROOT, 'logs/hard_run2.jsonl')):
    d = json.loads(l)
    if d['kind'] == kind:
        by[(d['q'], d['n'])][d['planted']] = d
def e(d):
    r = d['enum']; return f"{r['time']:.2f}{'' if r['complete'] else '*'}" + ('' if r['complete'] or r['q'] < 0 or not d['cover'] else ' (not found)')
def g(d, k):
    r = d.get(k)
    if not r: return '-'
    st = 'opt' if str(r['status']).lower().startswith('optimal') else 'TL'
    found = '' if not d['cover'] else (' found' if r['q'] is not None and r['q'] < -1e-12 else ' NOT found')
    return f"{r['time']:.1f} {st}{found if st == 'TL' else ''}"
print('q | n | N | cond (C) | min q (C) | supp<=3 best (C) | enum s C / R | Gurobi s C / R | SCIP s C / R | note')
for (q, n), D in sorted(by.items()):
    C, U = D.get(True), D.get(False)
    print(f"{q} | {n} | {n+2} | {C['cond']:.0f} | {C['predicted_min_q']:.2e} | {C['fam3']['max_viol']:.3g} | {e(C)} / {e(U)} | {g(C,'grb1')} / {g(U,'grb1')} | {g(C,'scip1')} / {g(U,'scip1')} | {'R has cover' if U['cover'] else ''}")
