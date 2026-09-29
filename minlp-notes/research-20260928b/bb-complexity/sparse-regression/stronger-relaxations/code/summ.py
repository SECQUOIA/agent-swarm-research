"""Markdown tables for Section 7 of thresholds.md from the data files.
Exactness is judged against OPT (exact enumeration, opt_check.py) when available: a relaxation value v is
'exact' if (OPT - v) <= 1e-6 OPT, 'inexact' if (OPT - v) > 1e-4 OPT.
usage: summ.py mech FILE OPTFILE | summ.py cmp OPTFILE FILE [FILE ...]"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import sys, json, collections
import numpy as np

EX, INEX = 1e-6, 1e-4   # relative gap thresholds: exact if gap <= EX*fS, inexact if gap > INEX*fS


def status(v, fS):
    if v is None:
        return None
    g = (fS - v) / fS  # fS is replaced by OPT by the callers when OPT is known
    return 'ex' if g <= EX else ('in' if g > INEX else 'unc')


def persp_exact(r):
    """Perspective root exactness: the exact PWE criterion (PT Corollary 2.4, max|a_l|/m0 <= 1) when S* is
    optimal; otherwise the numerical rule against OPT."""
    if r.get('Sstar_opt') is True:
        return r['maxratio'] <= 1.0
    return (r['fS'] - r['P']) / r['fS'] <= EX


def cnt(rows, key):
    st = [status(r.get(key), r['fS']) for r in rows if key in r]
    if not st:
        return '—'
    return '%d/%d' % (sum(s == 'ex' for s in st), len(st))


def closed(rows, key):
    vals = [(r[key] - r['P']) / (r['fS'] - r['P']) for r in rows
            if r.get(key) is not None and (r['fS'] - r['P']) / r['fS'] > INEX]
    return '%.2f' % np.median(vals) if vals else '—'


def cert(rows, key):
    return '%d/%d' % (sum((r['fS'] - r[key]) / r['fS'] > 1e-7 for r in rows), len(rows))


def remain(rows):
    vals = [max(0.0, (r['fS'] - r['L2_ub']) / (r['fS'] - r['P'])) for r in rows
            if (r['fS'] - r['P']) / r['fS'] > INEX]
    return '%.2f' % np.median(vals) if vals else '—'


def attach_opt(rows, optfn):
    opt = {}
    for l in open(optfn):
        o = json.loads(l); opt[(o['p'], o['seed'], o['n'])] = o
    for r in rows:
        o = opt.get((r['p'], r['seed'], r['n']))
        r['fS_true'] = r['fS']
        if o and 'OPT' in o:
            r['Sstar_opt'] = o['Sstar_opt']; r['fS'] = min(r['fS'], o['OPT'])   # compare with OPT
        elif o and o.get('Sstar_opt') is True:
            r['Sstar_opt'] = True        # perspective C1 at S* certifies OPT = f(S*)
        else:
            r['Sstar_opt'] = None
    return rows


def mech(fn, optfn=None):
    rows = [json.loads(l) for l in open(fn)]
    if optfn:
        rows = [r for r in attach_opt(rows, optfn) if r['Sstar_opt'] is not None]   # keep rows with OPT known
    by = collections.defaultdict(list)
    for r in rows:
        by[r['p']].append(r)
    print('| `p` | runs | `S*` optimal | median `delta` | median #viol. | persp. exact | median rel. root gap | `SDP1` exact | `SDP1` gap closed | `sdp_2` exact | `zb` exact | `L_1` cert. inexact | `L_2` cert. inexact | median `L_2` gap kept (lower bd.) |')
    print('|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for p in sorted(by):
        R = by[p]
        pe = '%d/%d' % (sum(persp_exact(r) for r in R), len(R))
        so = '%d/%d' % (sum(r.get('Sstar_opt') is True for r in R), len(R))
        print('| %d | %d | %s | %.3f | %g | %s | %.1e | %s | %s | %s | %s | %s | %s | %s |' % (
            p, len(R), so, np.median([r['delta'] for r in R]), np.median([r['nviol'] for r in R]), pe,
            np.median([(r['fS'] - r['P']) / r['fS'] for r in R]), cnt(R, 'sdp1'), closed(R, 'sdp1'),
            cnt(R, 'sdp2'), cnt(R, 'zb'), cert(R, 'L1_ub'), cert(R, 'L2_ub'), remain(R)))


def cmp_(optfn, fns):
    rows = attach_opt([json.loads(l) for fn in fns for l in open(fn)], optfn)
    by = collections.defaultdict(list)
    for r in rows:
        by[(r['p'], r['alpha'])].append(r)
    print('| `p` | `alpha` | `n` | runs | `S*` optimal | median #viol. | persp. root exact | `SDP1` exact | `sdp_2` exact | `zb` exact | `L_2` root cert. inexact | persp. C1 | `SDP1` C1 (solved) | `sdp_2` C1 (solved) | C1 fails for `L_2` (cert.) |')
    print('|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for key in sorted(by):
        R = by[key]
        pe = '%d/%d' % (sum(persp_exact(r) for r in R), len(R))
        so = '%d/%d' % (sum(r.get('Sstar_opt') is True for r in R), len(R))
        c1 = '%d/%d' % (sum(r['n_fail'] == 0 and r['c1_status'] == 'complete' for r in R), len(R))
        # C1 for SDP1/sdp2: holds if perspective holds, or all failing nodes were solved and are >= fS
        def c1r(m):
            ok, dec = 0, 0
            for r in R:
                if r['n_fail'] == 0:
                    ok += 1; dec += 1; continue
                nodes = r['fail_nodes']
                if any(m in d and d[m] is not None and status(d[m], r['fS']) == 'in' for d in nodes):
                    dec += 1; continue          # fails
                if r['n_fail'] <= len([d for d in nodes if m in d]) and all(
                        m in d and d[m] is not None and status(d[m], r['fS']) == 'ex' for d in nodes[:r['n_fail']]):
                    ok += 1; dec += 1
            return '%d/%d (%d undecided)' % (ok, len(R), len(R) - dec)
        l2f = '%d/%d' % (sum(any((r['fS'] - d['L2_ub']) / r['fS'] > 1e-7 for d in r['fail_nodes']) for r in R), sum(r['n_fail'] > 0 for r in R))
        print('| %d | %.2f | %d | %d | %s | %g | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            key[0], key[1], R[0]['n'], len(R), so, np.median([r['nviol'] for r in R]), pe, cnt(R, 'sdp1'),
            cnt(R, 'sdp2'), cnt(R, 'zb'), cert(R, 'L2_ub'), c1, c1r('sdp1'), c1r('sdp2'), l2f))


def hardzb(fn):
    rows = [json.loads(l) for l in open(fn)]
    by = collections.defaultdict(list)
    for r in rows:
        by[(r['k'], r['alpha'])].append(r)
    # zb: exact if -1e-5 <= gap <= 1e-6 (at most solver accuracy above OPT); inexact if gap > 1e-4; else unclear
    zst = lambda g: 'ex' if -1e-5 <= g <= EX else ('in' if g > INEX else 'unc')
    print('| `k` | `p` | `alpha` | `n` | runs | median persp. clique | median B&B nodes | persp. median rel. gap | `SDP1` exact | `SDP1` median rel. gap | `zb` exact | `zb` inexact (gap > 1e-4) | `zb` unclear | max `zb` rel. gap |')
    print('|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for key in sorted(by):
        R = by[key]
        g = lambda r, m: (r['opt'] - r[m]) / r['opt']
        print('| %d | %d | %.0f | %d | %d | %.1f | %d | %.1e | %d | %.1e | %d | %d | %d | %.1e |' % (
            key[0], R[0]['p'], key[1], R[0]['n'], len(R), np.median([r['clique'] for r in R]),
            int(np.median([r['nodes'] for r in R])), np.median([g(r, 'persp_root') for r in R]),
            sum(g(r, 'sdp1') <= EX for r in R), np.median([g(r, 'sdp1') for r in R]),
            sum(zst(g(r, 'zb')) == 'ex' for r in R), sum(zst(g(r, 'zb')) == 'in' for r in R),
            sum(zst(g(r, 'zb')) == 'unc' for r in R), max(g(r, 'zb') for r in R)))
    allg = [(r['opt'] - r['zb']) / r['opt'] for r in rows]
    print()
    print('totals: exact %d, inexact %d, unclear %d, runs %d' % (sum(zst(x) == 'ex' for x in allg),
          sum(zst(x) == 'in' for x in allg), sum(zst(x) == 'unc' for x in allg), len(allg)))


if __name__ == '__main__':
    if sys.argv[1] == 'mech':
        mech(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif sys.argv[1] == 'hardzb':
        hardzb(sys.argv[2])
    elif sys.argv[1] == 'cmp':
        cmp_(sys.argv[2], sys.argv[3:])
