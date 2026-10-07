"""Generate and cache loop instances: random bilinear programs with McCormick envelopes
(generator of exp_mccormick.make_instance, unchanged), root LP value z_LP (HiGHS) and the
bilinear optimum z_bil (SCIP 10 via PySCIPOpt, time limit TL).  Kept: LP optimal with a
simplicial basis cone, SCIP status optimal, z_bil - z_LP > 1e-6 (the filters of exp_loop.py).
Usage: python3 gen_instances.py P NPAIRS NLIN SEED NKEEP MAXTRY TL OUT.json"""
import sys, json, time
import numpy as np
import pyscipopt as ps
import mrcore as M

p, npairs, nlin, seed, NKEEP, MAXTRY, TL = [int(a) for a in sys.argv[1:8]]
OUT = sys.argv[8]
M.E.rng = np.random.default_rng(seed)


def bilinear_opt(I, timelimit):
    m = ps.Model(); m.hideOutput(); m.setParam('limits/time', timelimit); m.setParam('parallel/maxnthreads', 1)
    n = I['n']; xs = [m.addVar(lb=I['lo'][v], ub=I['hi'][v]) for v in range(n)]
    for k_ in range(len(I['b'])):
        m.addCons(ps.quicksum(I['A'][k_, v] * xs[v] for v in range(n)) <= I['b'][k_])
    for e, (i, j) in enumerate(I['pairs']):
        m.addCons(xs[I['p'] + e] == xs[i] * xs[j])
    m.setObjective(ps.quicksum(I['c'][v] * xs[v] for v in range(n)))
    t0 = time.time(); m.optimize()
    return m.getDualbound(), m.getPrimalbound(), m.getStatus(), time.time() - t0


keep, stats = [], dict(tried=0, lp_fail=0, scip_not_optimal=0, small_gap=0)
for k in range(MAXTRY):
    if len(keep) >= NKEEP:
        break
    I = M.E.make_instance(p, npairs, nlin)
    stats['tried'] += 1
    out = M.E.solve_lp(I)
    if out is None or M.E.basis_cone(I, *out) is None:
        stats['lp_fail'] += 1
        continue
    zlp = out[0].getInfo().objective_function_value
    zd, zp, st, sec = bilinear_opt(I, TL)
    if st != 'optimal':
        stats['scip_not_optimal'] += 1
        print('try %d: SCIP status %s after %.1fs (dual %.6g primal %.6g)' % (k, st, sec, zd, zp), flush=True)
        continue
    if zd - zlp < 1e-6:
        stats['small_gap'] += 1
        continue
    rec = dict(try_index=k, p=I['p'], pairs=[list(map(int, q)) for q in I['pairs']], n=I['n'],
               lo=I['lo'].tolist(), hi=I['hi'].tolist(), A=I['A'].tolist(), b=I['b'].tolist(), c=I['c'].tolist(),
               zlp=zlp, zbil=zd, zbil_primal=zp, scip_seconds=sec)
    keep.append(rec)
    print('try %d kept #%d  zlp %.6g zbil %.6g  scip %.1fs' % (k, len(keep), zlp, zd, sec), flush=True)
stats['kept'] = len(keep)
print('STATS', json.dumps(stats))
json.dump(dict(size=[p, npairs, nlin], seed=seed, stats=stats, instances=keep), open(OUT, 'w'))
