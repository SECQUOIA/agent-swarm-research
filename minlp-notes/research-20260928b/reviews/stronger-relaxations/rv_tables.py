"""Check 7: independent recount of Tables 7.1-7.3 from the author's stored data (my own logic, not summ.py).
Also reports, for the perspective relaxation, the exact decision by the PWE criterion (max|a_l| <= m0,
PT Corollary 2.4) next to the 1e-6-tolerance decision used in the note."""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"]:
    _os.environ[_v] = "1"
import json, os, collections
import numpy as np

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bb-complexity', 'sparse-regression',
                 'stronger-relaxations', 'data')


def load(fn):
    return [json.loads(l) for l in open(os.path.join(D, fn))]


def mech(fn, optfn):
    rows = load(fn)
    opt = {(o['p'], o['seed']): o for o in load(optfn)}
    byp = collections.defaultdict(list)
    for r in rows:
        o = opt.get((r['p'], r['seed']))
        if o is None:
            continue
        if 'OPT' in o:
            OPT = min(o['OPT'], r['fS']); sopt = o['Sstar_opt']
        elif o.get('Sstar_opt') is True:
            OPT = r['fS']; sopt = True
        else:
            continue
        r = dict(r, OPT=OPT, sopt=sopt)
        byp[r['p']].append(r)
    print(f"{fn}")
    print("p runs S*opt med_delta med_viol persp_ex(tol) persp_ex(PWE&S*opt) SDP1_ex SDP1_closed sdp2_ex zb_ex L1cert L2cert L2kept")
    for p in sorted(byp):
        R = byp[p]
        ex = lambda key: (sum((r['OPT'] - r[key]) / r['OPT'] <= 1e-6 for r in R if r.get(key) is not None),
                          sum(r.get(key) is not None for r in R))
        pe = ex('P')
        pwe = sum(r['maxratio'] <= 1 and r['sopt'] for r in R)
        gp = [r for r in R if (r['OPT'] - r['P']) / r['OPT'] > 1e-4 and r.get('sdp1') is not None]
        cl = np.median([(r['sdp1'] - r['P']) / (r['OPT'] - r['P']) for r in gp]) if gp else float('nan')
        L1 = sum(r['L1_ub'] < r['OPT'] * (1 - 1e-7) for r in R)
        L2 = sum(r['L2_ub'] < r['OPT'] * (1 - 1e-7) for r in R)
        kept = [max(0.0, (r['OPT'] - r['L2_ub']) / (r['OPT'] - r['P'])) for r in R if (r['OPT'] - r['P']) / r['OPT'] > 1e-4]
        print(p, len(R), sum(bool(r['sopt']) for r in R), round(float(np.median([r['delta'] for r in R])), 3),
              np.median([r['nviol'] for r in R]), '%d/%d' % pe, pwe, '%d/%d' % ex('sdp1'), round(float(cl), 2),
              '%d/%d' % ex('sdp2'), '%d/%d' % ex('zb'), L1, L2, round(float(np.median(kept)), 2) if kept else None)


def hard():
    rows = load('hardzb.jsonl')
    byc = collections.defaultdict(list)
    for r in rows:
        byc[(r['k'], r['alpha'])].append(r)
    tot = collections.Counter()
    ratios = []
    print("k alpha runs zb_ex zb_in(>1e-4) zb_unclear zb_above_OPT(>1e-6) max_zb_gap SDP1_ex")
    for key in sorted(byc):
        R = byc[key]
        g = [(r['opt'] - r['zb']) / r['opt'] for r in R if r['zb'] is not None]
        ex = sum(x <= 1e-6 for x in g); inn = sum(x > 1e-4 for x in g); unc = len(g) - ex - inn
        above = sum(x < -1e-6 for x in g)
        tot.update(ex=ex, inn=inn, unc=unc, above=above, runs=len(R))
        for r in R:
            gz = (r['opt'] - r['zb']) / r['opt']
            if gz > 1e-4:
                ratios.append(((r['opt'] - r['persp_root']) / r['opt']) / gz)
        s1 = sum((r['opt'] - r['sdp1']) / r['opt'] <= 1e-6 for r in R)
        print(key[0], key[1], len(R), ex, inn, unc, above, '%.1e' % max(g), s1)
    print('totals', dict(tot), 'persp/zb gap ratio: min %.1f median %.1f max %.1f' % (min(ratios), np.median(ratios), max(ratios)))


mech('mech_n20_k3.jsonl', 'opt_mech_n20_k3.jsonl')
mech('mech_n40_k3.jsonl', 'opt_mech_n40_k3.jsonl')
hard()
