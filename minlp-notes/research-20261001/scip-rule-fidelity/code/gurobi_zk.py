"""Solver-reported z_K estimates by Gurobi (nonconvex QCQP) for rho >= 4 records.

For a record (inst, k) the corner of analyze.py is rebuilt (rays of fixed columns / equality rows
dropped, rates floored at 1e-9 max w) and reduced to the coordinates of zk_fast.reduce_space.  The
problem  min w^T lam  s.t.  u = s_r + P_r lam,  sum_i theta_i u_i^2 + b_r^T u + c <= 0,  lam >= 0,
w^T lam <= zK2 (the support-<=2 upper bound)  is written in LP format and solved by gurobi_cl
(NonConvex=2, Threads=1, TimeLimit, MIPGap=1e-6). Output: reported best objective and best bound.
These are not certificates; badly scaled corners can yield inconsistent optimality reports
(see note.md, Section 5).
Usage: python3 gurobi_zk.py OUT.jsonl TIMELIMIT SELECT ANALYSIS.jsonl [...]
  SELECT = upper (records with zK_kind 'upper') | validate:N (N records with zK_kind exact or kkt3)
           | lowratio:N (N exact/kkt3 records with z_C/z_K < 0.1).
Records already in OUT.jsonl are skipped (checkpoint)."""

import sys, os, json, subprocess, tempfile, re, collections
import numpy as np
import dumpio as D
import zk_fast as Z

GUROBI = '/opt/gurobi1302/linux64/bin/gurobi_cl'
LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')


def corner(rec):
    Q, b, c = D.quadratic(rec)
    P, w, stat, lppos = D.rays(rec)
    keep = ~D.fixed_rays(rec)
    P, w = P[:, keep], w[keep]
    sbar = np.array(rec['zlp'], float)
    wpos = np.maximum(w, 1e-9 * max(1e-300, w.max()))
    return Q, b, c, sbar, P, wpos


def write_lp(path, Qr, br, cr, sr, Pr, w, cap):
    k, N = Pr.shape
    th = np.diag(Qr)
    L = ['Minimize', ' obj: ' + ' + '.join('%.17g l%d' % (w[j], j) for j in range(N)), 'Subject To']
    for i in range(k):
        terms = ' '.join('%+.17g l%d' % (-Pr[i, j], j) for j in range(N) if Pr[i, j] != 0)
        L.append(' e%d: u%d %s = %.17g' % (i, i, terms, sr[i]))
    lin = ' '.join('%+.17g u%d' % (br[i], i) for i in range(k) if br[i] != 0)
    quad = ' + '.join('%.17g u%d ^2' % (th[i], i) for i in range(k) if th[i] != 0).replace('+ -', '- ')
    L.append(' qc: %s + [ %s ] <= %.17g' % (lin if lin else '0 u0', quad, -cr))
    if np.isfinite(cap):
        L.append(' cap: ' + ' + '.join('%.17g l%d' % (w[j], j) for j in range(N)) + ' <= %.17g' % (cap * (1 + 1e-9)))
    L.append('Bounds')
    for i in range(k):
        L.append(' u%d free' % i)
    if np.isfinite(cap):
        for j in range(N):
            L.append(' 0 <= l%d <= %.17g' % (j, cap * (1 + 1e-9) / w[j]))
    L.append('End')
    open(path, 'w').write('\n'.join(L) + '\n')


def solve(Qr, br, cr, sr, Pr, w, cap, tl):
    with tempfile.TemporaryDirectory() as td:
        lp = os.path.join(td, 'm.lp'); log = os.path.join(td, 'g.log')
        write_lp(lp, Qr, br, cr, sr, Pr, w, cap)
        cmd = [GUROBI, 'NonConvex=2', 'Threads=1', 'TimeLimit=%g' % tl, 'MIPGap=1e-6', 'FeasibilityTol=1e-9', 'LogFile=' + log, 'LogToConsole=0', lp]
        env = dict(os.environ, GUROBI_HOME='/opt/gurobi1302/linux64',
                   LD_LIBRARY_PATH='/opt/gurobi1302/linux64/lib')
        subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=tl * 3 + 120)
        txt = open(log).read() if os.path.exists(log) else ''
    m = re.search(r'Best objective ([-+0-9.eE]+|-), best bound ([-+0-9.eE]+|-), gap ([-+0-9.eE]+%|-)', txt)
    status = 'optimal' if 'Optimal solution found' in txt else ('timelimit' if 'Time limit reached' in txt else
             ('infeasible' if 'infeasible' in txt.lower() else 'other'))
    rt = re.search(r'Explored .* in ([0-9.]+) seconds', txt)
    obj = bound = None
    if m:
        obj = None if m.group(1) == '-' else float(m.group(1))
        bound = None if m.group(2) == '-' else float(m.group(2))
    return dict(obj=obj, bound=bound, status=status, seconds=float(rt.group(1)) if rt else None)


def main():
    out, tl, sel = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    done = set()
    # checkpoint: records in OUT and in the files listed in env DONE_FILES (colon separated) are skipped
    for f in [out] + [x for x in os.environ.get('DONE_FILES', '').split(':') if x]:
        if os.path.exists(f):
            for l in open(f):
                g = json.loads(l); done.add((g['inst'], g['k']))
    targets = collections.defaultdict(dict)
    pool = []
    for f in sys.argv[4:]:
        for l in open(f):
            r = json.loads(l)
            if r.get('status') != 'ok' or r['wmax'] <= 0 or r.get('zeroface_meets_S'):
                continue
            pool.append(r)
    if sel == 'upper':
        chosen = [r for r in pool if r['zK_kind'] == 'upper']
    elif sel.startswith('lowratio:'):          # exact/kkt3 records with z_C/z_K < 0.1 (check z_K is not too large)
        n = int(sel.split(':')[1])
        ex = []
        for r in pool:
            zc = r['zC_scip'] if r['zC_scip'] is not None else r['zC_fixed']
            if r['zK_kind'] in ('exact', 'kkt3') and np.isfinite(r['zK']) and r['zK'] > 0 and zc is not None and zc / r['zK'] < 0.1:
                ex.append(r)
        idx = np.random.default_rng(8).choice(len(ex), min(n, len(ex)), replace=False)
        chosen = [ex[i] for i in sorted(idx)]
    else:
        n = int(sel.split(':')[1])
        ex = [r for r in pool if r['zK_kind'] in ('exact', 'kkt3') and np.isfinite(r['zK'])]
        idx = np.random.default_rng(7).choice(len(ex), min(n, len(ex)), replace=False)
        chosen = [ex[i] for i in sorted(idx)]
    if os.environ.get('SHARD'):              # SHARD=r/m: keep every m-th chosen record, offset r
        sr, sm = (int(x) for x in os.environ['SHARD'].split('/'))
        chosen = [r for i, r in enumerate(chosen) if i % sm == sr]
    for r in chosen:
        if (r['inst'], r['k']) not in done:
            targets[r['inst']][r['k']] = r
    with open(out, 'a') as fo:
        for inst, recs in targets.items():
            k = -1
            for rec in D.records(os.path.join(LOGS, 'runs_minlplib', inst + '.jsonl.gz')):
                if 'v' not in rec:
                    continue
                k += 1
                if k not in recs:
                    continue
                r = recs[k]
                Q, b, c, sbar, P, w = corner(rec)
                Qr, br, cr, sr, Pr, rho, _ = Z.reduce_space(Q, b, c, sbar, P)
                res = solve(Qr, br, cr, sr, Pr, w, r['zK2'], tl)
                res.update(inst=inst, k=k, rho=rho, nrays=int(P.shape[1]), zK2=r['zK2'], zK_analysis=r['zK'],
                           zK_kind=r['zK_kind'], select=sel)
                fo.write(json.dumps(res) + '\n'); fo.flush()


if __name__ == '__main__':
    main()
