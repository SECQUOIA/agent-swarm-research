"""Reviewer check of z_K with Gurobi in the full constraint space (no eigen-reduction, own LP writer).

For sample records (r1-logs/sample_records.jsonl.gz) that the stream classified as 'ratio' (z_K > 0):
all with n_+ >= 2 (rho >= 3, where the stream uses 3-ray KKT or Gurobi in reduced space) and up to
NLOW with n_+ <= 1.  Problem:  min sum_j wf_j lam_j  s.t.  s = sbar + P lam,  s^T Q s + b^T s + c <= 0,
lam >= 0,  sum wf_j lam_j <= cap,  cap = 2 * max(stream z_K, reviewer pair value if finite).
Rates floored at 1e-9 max w, rays of fixed columns / equality rows dropped (the stream's corner).
gurobi_cl: NonConvex=2, Threads=1, MIPGap=1e-6, FeasibilityTol=1e-9.
Usage: python3 gurobi_fullspace.py TIMELIMIT NLOW NPAR"""

import sys, os, json, gzip, glob, re, subprocess, tempfile, random
import numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indep_check import build, EPS

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, '../../logs')
GUROBI = '/opt/gurobi1302/linux64/bin/gurobi_cl'
ENV = dict(os.environ, GUROBI_HOME='/opt/gurobi1302/linux64',
           LD_LIBRARY_PATH='/opt/gurobi1302/linux64/lib')


def stream_results():
    S = {}
    for f in [os.path.join(LOGS, 'an_mc11.jsonl'), os.path.join(LOGS, 'an_mc12.jsonl')] + \
            glob.glob(os.path.join(LOGS, 'an_minlplib*', '*.jsonl')):
        for l in open(f):
            r = json.loads(l)
            if r.get('status') == 'ok':
                S[(r['inst'], r['k'])] = r
    G = {}
    p = os.path.join(LOGS, 'gurobi_zk.jsonl')
    for l in open(p):
        g = json.loads(l); G[(g['inst'], g['k'])] = g
    return S, G


def write_lp(path, Q, b, c, sbar, P, wf, cap):
    nv, N = P.shape
    L = ['Minimize', ' obj: ' + ' + '.join('%.17g l%d' % (wf[j], j) for j in range(N)), 'Subject To']
    for i in range(nv):
        t = ' '.join('%+.17g l%d' % (-P[i, j], j) for j in range(N) if P[i, j] != 0)
        L.append(' e%d: s%d %s = %.17g' % (i, i, t, sbar[i]))
    lin = ' '.join('%+.17g s%d' % (b[i], i) for i in range(nv) if b[i] != 0) or '0 s0'
    qt = []
    for i in range(nv):
        if Q[i, i] != 0:
            qt.append('%+.17g s%d ^2' % (Q[i, i], i))
        for j in range(i + 1, nv):
            if Q[i, j] != 0:
                qt.append('%+.17g s%d * s%d' % (2 * Q[i, j], i, j))
    L.append(' qc: %s + [ %s ] <= %.17g' % (lin, ' '.join(qt), -c))
    L.append(' cap: ' + ' + '.join('%.17g l%d' % (wf[j], j) for j in range(N)) + ' <= %.17g' % cap)
    L.append('Bounds')
    for i in range(nv):
        L.append(' s%d free' % i)
    for j in range(N):
        L.append(' 0 <= l%d <= %.17g' % (j, cap / wf[j]))
    L.append('End')
    open(path, 'w').write('\n'.join(L) + '\n')


def solve(args):
    key, Q, b, c, sbar, P, wf, cap, tl = args
    with tempfile.TemporaryDirectory() as td:
        lp = os.path.join(td, 'm.lp'); log = os.path.join(td, 'g.log'); sol = os.path.join(td, 'm.sol')
        write_lp(lp, Q, b, c, sbar, P, wf, cap)
        subprocess.run([GUROBI, 'NonConvex=2', 'Threads=1', 'TimeLimit=%g' % tl, 'MIPGap=1e-6', 'FeasibilityTol=1e-9',
                        'LogFile=' + log, 'LogToConsole=0', 'ResultFile=' + sol, lp], env=ENV,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3 * tl + 120)
        txt = open(log).read() if os.path.exists(log) else ''
        lam = None
        if os.path.exists(sol):
            vals = dict(l.split() for l in open(sol) if l and not l.startswith('#'))
            lam = np.array([float(vals.get('l%d' % j, 0.0)) for j in range(P.shape[1])])
    m = re.search(r'Best objective ([-+0-9.eE]+|-), best bound ([-+0-9.eE]+|-)', txt)
    st = 'optimal' if 'Optimal solution found' in txt else ('timelimit' if 'Time limit reached' in txt else
         ('infeasible' if 'infeasible' in txt.lower() else 'other'))
    obj = bnd = None
    if m:
        obj = None if m.group(1) == '-' else float(m.group(1)); bnd = None if m.group(2) == '-' else float(m.group(2))
    qpt = None
    if lam is not None:
        pt = sbar + P @ np.maximum(lam, 0)
        qpt = float(pt @ Q @ pt + b @ pt + c)
    return key, dict(status=st, obj=obj, bound=bnd, q_at_sol=qpt)


def main():
    tl, nlow, npar = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    S, G = stream_results()
    mine = {}
    for f in glob.glob(os.path.join(HERE, '../r1-logs/indep_check_*.jsonl')):
        for l in open(f):
            r = json.loads(l); mine[(r['inst'], r['k'])] = r
    jobs = []; low = []
    for l in gzip.open(os.path.join(HERE, '../r1-logs/sample_records.jsonl.gz'), 'rt'):
        rec = json.loads(l); key = (rec['inst'], rec['k'])
        s = S.get(key)
        if s is None or s['wmax'] <= 0 or s.get('zeroface_meets_S'):
            continue
        Q, b, c, sbar, P, w, width, nq = build(rec)
        keep = width > 1e-9
        P, w = P[:, keep], w[keep]
        wf = np.maximum(w, 1e-9 * w.max())
        npos = int(np.sum(np.linalg.eigvalsh(Q) > EPS))
        zk = s['zK']
        g = G.get(key)
        if g and g.get('obj') is not None:
            zk = min(zk, g['obj'])
        zp = mine.get(key, {}).get('zK_pairs')
        cands = [z for z in (zk, zp) if z is not None and np.isfinite(z) and z > 0]
        if not cands:
            continue
        cap = 2 * max(cands)
        job = (key, Q, b, c, sbar, P, wf, cap, tl)
        (jobs if npos >= 2 else low).append(job)
    random.Random(7).shuffle(low)
    jobs += low[:nlow]
    out = os.path.join(HERE, '../r1-logs/gurobi_fullspace.jsonl')
    with open(out, 'w') as fo, ThreadPoolExecutor(npar) as ex:
        for key, res in ex.map(solve, jobs):
            s = S[key]; g = G.get(key, {})
            res.update(inst=key[0], k=key[1], zK_stream=s['zK'], zK_kind=s['zK_kind'], zK_stream_gurobi=g.get('obj'),
                       zK_stream_gurobi_bound=g.get('bound'), zK_pairs_reviewer=mine.get(key, {}).get('zK_pairs'),
                       npos=s['npos'], zC_scip=s['zC_scip'], zC_fixed=s['zC_fixed'])
            fo.write(json.dumps(res) + '\n'); fo.flush()
    print('jobs', len(jobs))


if __name__ == '__main__':
    main()
