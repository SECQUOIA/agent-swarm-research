"""Triple-level audit of the base relaxation B on a BoxQP (spar) instance, with checkpoints.

Same computation as triple_audit.py, restructured so that an interrupted run can
resume: the B solution is saved to <out>.base.npz after the triangle loop, and
QPB3 depths are saved in chunks to <out>.depth.npz.

Steps.
1. B = dense Shor + McCormick + Y_ii <= x_i + triangle inequalities, separated
   (violation > 1e-7, at most 10000 per round) until none is violated, or until at most
   50 are violated, all by less than 1e-5, after the third round (Clarabel).  The
   remaining violation is recorded; the added triangles are checkpointed.
2. For every triple T of {0..n-1}: delta_T = QPB3 depth of M_T (hullsep.depth).
3. Family: min over all triples and all 24 orientations of the exact simplex
   minimum of A = B - bb' (relax.stqp_min).
4. eps = max(0, -min delta_T); by Lemma 3 of note.md, any constraints valid for
   QPB3 on triples (with per-triple auxiliaries) raise the bound by at most
   eps * (f(y_c) - f(y*)) / (1 + eps), y_c = uniform moments.
Usage: python spar_audit.py spar_name out.json"""
import glob
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from relax import Relax, read_boxqp, separate_triangles, triple_moment_matrices, all_triples, family_AB, stqp_min, ORIENTS
import hullsep

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../sources/BoxQP_instances-master/')
CHUNK = 20000
CAP = 10000        # triangle inequalities added per round (version 2; version 1 used 5000)
MAX_ROUNDS = 12


def family_min(x, Y, T):
    best = 0.0
    nviol = 0
    for o in ORIENTS:
        for s in range(0, len(T), 50000):
            bv, B = family_AB(x, Y, T[s:s + 50000], o)
            A = B - bv[:, :, None] * bv[:, None, :]
            w = np.linalg.eigvalsh(A)[:, 0]
            cand = np.nonzero(w < 0)[0]
            if len(cand) == 0:
                continue
            val, _ = stqp_min(A[cand])
            best = min(best, float(val.min()))
            nviol += int((val < -1e-6).sum())
    return best, nviol


def main():
    name, out = sys.argv[1], sys.argv[2]
    H, g = read_boxqp(glob.glob(D + '*/' + name + '.in')[0])
    n = len(g)
    t0 = time.time()
    bpath = out + '.base.npz'
    if os.path.exists(bpath):
        z = np.load(bpath)
        x, Y = z['x'], z['Y']
        info = json.loads(str(z['info']))
    else:
        R = Relax(H, g, name)
        rounds = []
        tpath = out + '.tri.json'          # checkpoint of the triangle inequalities added so far
        if os.path.exists(tpath):
            for c in json.load(open(tpath)):
                R.add_triangle(*c)
        for rnd in range(MAX_ROUNDS):
            res = R.solve('clarabel')
            cuts, mv = separate_triangles(res['xv'], res['Y'], tol=1e-7, cap=None)
            cuts = [c for c in cuts if c not in R.tri_added]
            rounds.append({'pobj': res['pobj'], 'safe': res['safe'], 'status': res['status'],
                           't': res['time_solve'], 'newtri': len(cuts), 'maxviol': mv})
            print(name, rounds[-1], flush=True)
            # stop when nothing is violated by more than 1e-7, or when only a few triangles
            # remain violated by less than 1e-5 (solver-accuracy level; see note.md, Section 4.1)
            if not cuts or (rnd >= 2 and len(cuts) <= 50 and mv < 1e-5):
                break
            for c in cuts[:CAP]:
                R.add_triangle(*c)
            json.dump(sorted(R.tri_added), open(tpath, 'w'))
        x, Y = res['xv'], res['Y']
        info = {'B': res['pobj'], 'B_safe': res['safe'], 'status': res['status'], 'pinf': res['pinf'],
                'max_triangle_violation': rounds[-1]['maxviol'],
                'tri': len(R.tri_added), 'rounds': rounds, 'time_base': time.time() - t0}
        np.savez(bpath, x=x, Y=Y, info=json.dumps(info))
    T = all_triples(n)
    dpath = out + '.depth.npz'
    depths = np.full(len(T), np.nan)
    if os.path.exists(dpath):
        depths = np.load(dpath)['depths']
    t1 = time.time()
    for s in range(0, len(T), CHUNK):
        if not np.isnan(depths[s:s + CHUNK]).any():
            continue
        M = triple_moment_matrices(x, Y, T[s:s + CHUNK])
        depths[s:s + CHUNK] = [hullsep.depth(Mi)[0] for Mi in M]
        np.savez(dpath, depths=depths)
        print(name, 'depth chunk', s, 'min so far %.3e' % np.nanmin(depths), flush=True)
    t_hull = time.time() - t1
    fam_min, fam_nviol = family_min(x, Y, T)
    f_star = info['B']
    f_c = float(np.trace(H) / 3 + (H.sum() - np.trace(H)) / 4 + g.sum() / 2)
    eps = max(0.0, -float(depths.min()))
    opt = None
    for line in open(D + 'README.txt'):
        t = line.split()
        if len(t) == 2 and t[0] == name:
            opt = -float(t[1])
    rec = {'name': name, 'n': n, 'opt_min': opt, 'B': f_star, 'B_safe': info['B_safe'], 'status': info['status'],
           'pinf': info['pinf'], 'tri': info['tri'], 'max_triangle_violation': info.get('max_triangle_violation'), 'gap_safe': opt - info['B_safe'],
           'relgap_safe': (opt - info['B_safe']) / abs(opt), 'triples': len(T),
           'min_depth': float(depths.min()), 'count_depth_lt_1e-6': int((depths < -1e-6).sum()),
           'count_depth_lt_1e-7': int((depths < -1e-7).sum()), 'count_depth_lt_1e-8': int((depths < -1e-8).sum()),
           'family_stqp_min': fam_min, 'family_violated_pairs_1e-6': fam_nviol, 'f_uniform': f_c, 'eps': eps,
           'max_triple_level_improvement': eps * (f_c - f_star) / (1 + eps), 'time_hull_tests': t_hull,
           'time_base': info.get('time_base'), 'interior': int(((x > 1e-6) & (x < 1 - 1e-6)).sum())}
    json.dump(rec, open(out, 'w'), indent=1)
    print(json.dumps(rec), flush=True)


if __name__ == '__main__':
    main()
