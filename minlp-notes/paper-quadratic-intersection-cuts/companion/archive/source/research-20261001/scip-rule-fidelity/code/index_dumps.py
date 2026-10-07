"""One compact JSON line per intersection-cut attempt of a dump (plus the counter lines).

Fields: outcome classification, size, case, inertia of the violated side, node data.
outcome: 'added' (cut added to the LP), 'cleanup_fail' (generated, rejected by
SCIPcleanupRowprep), 'highre' (generated, rejected by the range/efficacy test),
'fail:<reason>' (generation aborted; reasons from the instrumentation: zerostat, numerics,
phi0_restrict, minrep_phi0, minrep_numerics, badnonbasic), 'nogen' (failed without reason).
For 'fail:numerics' the subreason is 'phi0' (phi(0) >= 0) or 'dyn' (max/min of |A|,|B|,|C| huge),
from the nlhdlr counters before and after the attempt.
Usage: python3 index_dumps.py OUT.jsonl DUMP.jsonl.gz [...]
"""
import sys, json, os
import numpy as np
import dumpio as D


def summarize(rec):
    out = {k: rec.get(k) for k in ('lp', 'node', 'depth', 'cons', 'expr', 'over', 'isroot', 'nquad', 'nlin',
                                    'nrays', 'nv', 'kappa', 'case4', 'case2', 'usemonoidal', 'exprncuts',
                                    'violation', 'lpobj', 'eff', 're')}
    out['aux'] = rec.get('auxvar') is not None
    out['lpcuts'] = rec.get('lpcuts')        # this expression's intersection cuts in the LP: [side, LP number]
    ev = np.array(rec.get('eigval') or [], float) * (-1.0 if rec.get('over') else 1.0)
    out['npos'] = int(np.sum(ev > 1e-9)); out['nneg'] = int(np.sum(ev < -1e-9)); out['nzero'] = int(ev.size - out['npos'] - out['nneg'])
    if rec.get('added') == 1:
        oc = 'added'
    elif rec.get('highre') == 1:
        oc = 'highre'
    elif rec.get('gen') == 1:
        oc = 'cleanup_fail' if rec.get('cleanup') == 0 else 'gen_other'
    elif rec.get('fail'):
        oc = 'fail:' + rec['fail']
    else:
        oc = 'nogen'
    if rec.get('fail') == 'numerics':
        dphi = rec.get('nphinonneg1', 0) - rec.get('nphinonneg0', 0)
        ddyn = rec.get('nbadray1', 0) - rec.get('nbadray0', 0)
        out['sub'] = 'phi0' if dphi > 0 else ('dyn' if ddyn > 0 else '?')
    out['outcome'] = oc
    if 'case4' in rec:
        out['case'] = 4 if rec['case4'] else (2 if rec['kappa'] > 0 else (3 if rec['kappa'] < 0 else 1))
    if 'rayrate' in rec:
        P, w, stat, lppos = D.rays(rec)
        fx = D.fixed_rays(rec)
        wk = w[~fx]
        out['nfixed'] = int(fx.sum())
        out['nzerorate'] = int(np.sum(wk <= 1e-9 * max(1e-300, np.abs(wk).max()))) if wk.size else 0
    if 'perray' in rec:
        out['nmono'] = int(sum(1 for e in rec['perray'] if e.get('mono')))
    return out


def main():
    outp = sys.argv[1]
    with open(outp, 'w') as fo:
        for path in sys.argv[2:]:
            inst = os.path.basename(path).split('.')[0]
            for rec in D.records(path):
                if 'counters' in rec or 'nlhdlrstats' in rec:
                    fo.write(json.dumps(dict(inst=inst, **rec)) + '\n')
                elif rec.get('corrupt'):
                    fo.write(json.dumps(dict(inst=inst, outcome='corrupt')) + '\n')
                elif 'v' in rec:
                    s = summarize(rec); s['inst'] = inst
                    fo.write(json.dumps(s) + '\n')


if __name__ == '__main__':
    main()
