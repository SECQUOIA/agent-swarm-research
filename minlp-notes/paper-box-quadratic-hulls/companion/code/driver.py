"""Run the relaxation comparison on one instance.

Methods (each starts from the converged base relaxation B = Shor + RLT + TRI):
  B     base only
  K     + Khajavirad (17) on selected triples
  A     + Anstreicher-Puges (14)-(16) on selected triples
  KA    + both
  KAF   KA (converged) + family blocks (5x5 PSD + 6 auxiliaries) for violated
        (triple, orientation) pairs, by exact StQP separation
  KAFc  KA (converged) + individual family cuts (linear), same separation
  F     B + family blocks
  KAX   KA (converged) + exact 5-tetrahedron DNN lift on selected triples
  X     B + exact lift on selected triples
  Xc    B + certified linear cuts from the exact hull separation SDP
  XF    B + exact lift on the triples selected by the family separation
        (a triple is selected when some orientation is violated)
Triple selection for K, A, X, Xc: triples whose moment matrix is outside QPB3
(depth < -seltol from hullsep.depth) at the current point, most violated first,
at most `cap` new triples per round.  Triples with a coordinate within 1e-6
of a bound are skipped: there the base (McCormick + Shor) forces the triple
moment matrix to reduce to a pair, where Shor + RLT is exact.
Family selection: all triples, all 24 orientations, StQP value < -famtol.
"""

import argparse
import copy
import json
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from relax import (Relax, read_boxqp, separate_triangles, separate_family,
                   triple_moment_matrices, ORIENTS)
import hullsep
from instances import load_json


def summarize(res, R, t_sep, method, rnd, extra=None):
    d = {'method': method, 'round': rnd, 'status': res['status'], 'pobj': res['pobj'], 'dobj': res['dobj'],
         'safe': res['safe'], 'pinf': res['pinf'], 'iters': res['iters'], 'time_solve': res['time_solve'],
         'time_build': res['time_build'], 'time_sep': t_sep, 'size': R.size()}
    if extra:
        d.update(extra)
    return d


class Runner:
    def __init__(self, R, solver, log, cap=200, max_rounds=15, seltol=1e-6, famtol=1e-6, tritol=1e-6,
                 tricap=2000, time_budget=3600.0, solve_kw=None):
        self.R0 = R
        self.solver = solver
        self.log = log
        self.cap = cap
        self.max_rounds = max_rounds
        self.seltol = seltol
        self.famtol = famtol
        self.tritol = tritol
        self.tricap = tricap
        self.time_budget = time_budget
        self.solve_kw = solve_kw or {}
        self.records = []

    def emit(self, d):
        self.records.append(d)
        with open(self.log, 'a') as f:
            f.write(json.dumps(d) + '\n')
        print('%-5s r%-2d %-12s pobj %.8f safe %.8f  t_solve %7.2f t_sep %6.2f  %s' % (
            d['method'], d['round'], d['status'], d['pobj'], d['safe'], d['time_solve'], d['time_sep'],
            {k: v for k, v in d['size'].items() if k in ('vars', 'psd', 'soc', 'K', 'A', 'F', 'X', 'Fcut', 'Xcut', 'tri')}),
            flush=True)

    def solve(self, R):
        return R.solve(self.solver, **self.solve_kw)

    def tri_round(self, R, res):
        cuts, mv = separate_triangles(res['xv'], res['Y'], tol=self.tritol, cap=None, triples=R.triples)
        new = [c for c in cuts if c not in R.tri_added][:self.tricap]
        for c in new:
            R.add_triangle(*c)
        return len(new)

    # ------------------------------------------------------------------
    def base(self):
        R = copy.deepcopy(self.R0)
        t0 = time.time()
        for rnd in range(100):
            res = self.solve(R)
            ts = time.time()
            nt = self.tri_round(R, res)
            t_sep = time.time() - ts
            self.emit(summarize(res, R, t_sep, 'B', rnd, {'new': nt}))
            if nt == 0:
                break
        self.Rb, self.resb = R, res
        return R, res

    def select_hull(self, R, res, exclude):
        T = R.triples
        x = res['xv']
        inner = (x > 1e-6) & (x < 1 - 1e-6)
        keep = inner[T].all(axis=1)
        idx = np.nonzero(keep)[0]
        idx = [i for i in idx if tuple(int(v) for v in T[i]) not in exclude]
        if not idx:
            return [], 0, 0.0
        M = triple_moment_matrices(x, res['Y'], T[idx])
        out = []
        for t, i in enumerate(idx):
            d, C, st = hullsep.depth(M[t])
            if d < -self.seltol:
                out.append((d, tuple(int(v) for v in T[i]), C))
        out.sort(key=lambda r: r[0])
        return out[:self.cap], len(idx), (out[0][0] if out else 0.0)

    def run(self, method, R, res, rnd0=0):
        """Generic separation loop from relaxation R with solution res."""
        t_start = time.time()
        hist = [res['pobj']]
        for rnd in range(rnd0, rnd0 + self.max_rounds):
            ts = time.time()
            added = 0
            extra = {}
            if method in ('K', 'A', 'KA', 'X', 'KAX', 'Xc'):
                excl = set()
                if method in ('K', 'KA'):
                    excl = R.K_added
                elif method == 'A':
                    excl = R.A_added
                elif method in ('X', 'KAX'):
                    excl = R.X_added
                sel, ntest, worst = self.select_hull(R, res, excl if method != 'Xc' else set())
                extra.update({'tested': ntest, 'selected': len(sel), 'worst_depth': worst})
                for d, T, C in sel:
                    if method in ('K', 'KA'):
                        R.add_K(T)
                    if method in ('A', 'KA'):
                        R.add_A(T)
                    if method in ('X', 'KAX'):
                        R.add_X(T)
                    if method == 'Xc':
                        shift = hullsep.certify_cut(C)
                        C2 = C.copy()
                        C2[0, 0] += shift
                        R.add_Xcut(T, C2)
                    added += 1
            elif method in ('F', 'KAF', 'KAFc', 'XF'):
                viol = separate_family(res['xv'], res['Y'], R.triples, tol=self.famtol)
                viol.sort(key=lambda r: r[2])
                extra.update({'violated_pairs': len(viol), 'violated_triples': len(set(v[0] for v in viol)),
                              'worst_stqp': viol[0][2] if viol else 0.0})
                for (r, oi, val, v, h) in viol:
                    if added >= self.cap:
                        break
                    T = tuple(int(t) for t in R.triples[r])
                    if method == 'KAFc':
                        R.add_Fcut(T, ORIENTS[oi], np.append(v, h))
                        added += 1
                    elif method == 'XF':
                        if T not in R.X_added:
                            R.add_X(T)
                            added += 1
                    elif (T, ORIENTS[oi]) not in R.F_added:
                        R.add_F(T, ORIENTS[oi])
                        added += 1
            ntri = self.tri_round(R, res)
            t_sep = time.time() - ts
            extra.update({'new': added, 'newtri': ntri})
            if added == 0 and ntri == 0:
                self.emit(summarize(res, R, t_sep, method, rnd, extra))
                break
            # record the separation outcome with the solution it was computed from
            self.emit(summarize(res, R, t_sep, method, rnd, extra))
            res = self.solve(R)
            hist.append(res['pobj'])
            if time.time() - t_start > self.time_budget:
                self.emit(summarize(res, R, 0.0, method, rnd + 1, {'stop': 'time'}))
                break
            if len(hist) >= 4 and abs(hist[-1] - hist[-4]) <= 1e-7 * max(1.0, abs(hist[-1])):
                self.emit(summarize(res, R, 0.0, method, rnd + 1, {'stop': 'stall'}))
                break
        else:
            self.emit(summarize(res, R, 0.0, method, rnd0 + self.max_rounds, {'stop': 'rounds'}))
        return R, res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--boxqp')
    ap.add_argument('--json')
    ap.add_argument('--methods', default='K,A,KA,KAF,KAFc,F,X,KAX,Xc')
    ap.add_argument('--solver', default='clarabel')
    ap.add_argument('--log', required=True)
    ap.add_argument('--cap', type=int, default=200)
    ap.add_argument('--max_rounds', type=int, default=15)
    ap.add_argument('--time_budget', type=float, default=3600)
    ap.add_argument('--scs_eps', type=float, default=1e-6)
    a = ap.parse_args()
    if a.boxqp:
        H, g = read_boxqp(a.boxqp)
        R = Relax(H, g, a.boxqp)
    else:
        H, g, meta = load_json(a.json)
        R = Relax(H, g, a.json, cliques=meta.get('cliques'))
    kw = {'scs_eps': a.scs_eps} if a.solver == 'scs' else {}
    run = Runner(R, a.solver, a.log, cap=a.cap, max_rounds=a.max_rounds, time_budget=a.time_budget, solve_kw=kw)
    open(a.log, 'w').close()
    Rb, resb = run.base()
    meths = a.methods.split(',')
    done = {}
    for m in meths:
        if m in ('KAF', 'KAFc', 'KAX'):
            if 'KA' not in done:
                done['KA'] = run.run('KA', copy.deepcopy(Rb), resb)
            Rka, reska = done['KA']
            done[m] = run.run(m, copy.deepcopy(Rka), reska, rnd0=100)
        elif m in done:
            continue
        else:
            done[m] = run.run(m, copy.deepcopy(Rb), resb)


if __name__ == '__main__':
    main()
