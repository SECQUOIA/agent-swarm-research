"""Root cutting loop on cached McCormick instances with many set-selection rules and
diagnostics (multiround stream).

Loop (as research-20260928b/sfree/code/exp_loop.py): each round solves the LP (HiGHS),
takes the optimal basis cone, and for every bilinear term violated by more than 1e-6 adds
the cut(s) of the rule.  Cut sum_j a_j lam_j >= 1 with lam = rhsB - Ab x, i.e.
(a^T Ab) x <= a^T rhsB - 1, scaled by max |coefficient|.

Rules (u = weights whose corner bound the orbit set maximizes; floors as in exp_loop):
  scip        Python model of SCIP's Case-4 set (default lambda)          [exp_loop 'scip']
  orbit_core  best orbit set, bisection capped by core.corner_bound      [exp_loop 'orbit']
  orbit       best orbit set, bisection capped by the checked zk_vec
  orbitB      completion (B) of the orbit set's F
  corner      corner-optimal cut w^T lam >= z_K
  pertD       best orbit set for u = w/max(w) + D (D = 0.01, 0.1, 1)
  geo         best orbit set for u_j = ||r_j|| (maximize the smallest Euclidean step)
  pertED      best orbit set for u_j = ||r_j|| (what_j + D), what_j = (w_j/||r_j||)/max_i(w_i/||r_i||)
              (objective rate per unit length along r_j, normalized; D = 0.1, 1)
  alt         orbit in even rounds (0, 2, 4, ...; rounds are counted from 0), scip in odd rounds
  alt2        scip in even rounds, orbit in odd rounds
  first_orbit orbit in round 0 (the root), scip afterwards
  lexE        among orbit sets with corner bound >= (1-E) * best orbit bound, the one with the
              largest smallest Euclidean step (E = 0.1)
  both        scip and orbit cut for every term
  bothpert    scip and pert0.1 cut for every term
  oracle      per term, the candidate (scip, orbit, pert0.1, pert1, geo) with the largest
              LP value when added alone to the current LP
  oracle_seq  as oracle, but terms are processed in order and each candidate is evaluated
              together with the cuts already chosen in this round
  eff         same pool, largest efficacy (Euclidean distance from xbar to the cut)
  depth       same pool, largest dist(xbar, K cap cut)
  sumstep     same pool, largest sum_j min(1, alpha_j / t_j) (t_j = first hit of ray j)
Added on 2026-10-02 (continuation; existing rules unchanged):
  oKs         orbit in rounds 0..K-1, scip afterwards (o1s = first_orbit)
  sKo         scip in rounds 0..K-1, orbit afterwards
  eff2        per term, the larger-efficacy cut of the two sets scip and orbit
  hybT        per term, scip if z_C(scip) >= T z_K (floored w), else orbit (T = 0.9, 0.5)
Added on 2026-10-02 (revision after review round 1; existing rules unchanged):
  maj2        per term, the orbit set if its step is at least SCIP's step on more than half of the
              rays where either step is finite, else SCIP's set (test of the "smaller sets" factor)
  rndP        per term, the orbit set with probability P, else SCIP's set (control for maj2 with a
              geometry-blind choice; deterministic pseudo-random draw seeded by the round and the
              term's point sbar)
Usage: python3 mrloop.py INST.json RULES(comma) ROUNDS OUT.jsonl I0 I1 [diag] [swap] [swapgamma] [swappot]
(swappot: swapgamma plus the potential max_e z_K / (z_bil - z) and the counts of tiny normalized
reduced costs at the vertex reached by each swap alternative)
(swapgamma: also record pointedness, zero reduced costs and total violation at the vertex
reached by each swap alternative)
"""
import sys, re, json, time, warnings, zlib
import numpy as np
warnings.filterwarnings('ignore')
import mrcore as M
from core import corner_bound, bilinear_quadratic
from bilinear import step_B

POOL = ('scip', 'orbit', 'pert0.1', 'pert1', 'geo')


def load(path):
    D = json.load(open(path))
    out = []
    for r in D['instances']:
        I = dict(p=r['p'], pairs=[tuple(q) for q in r['pairs']], n=r['n'], lo=np.array(r['lo']),
                 hi=np.array(r['hi']), A=np.array(r['A']), b=np.array(r['b']), c=np.array(r['c']))
        out.append((I, r['zlp'], r['zbil']))
    return out


class Corner:
    """Data of one violated term at the current vertex."""
    def __init__(self, side, sbar, P, w, R, Ab, rhs):
        self.side, self.sbar, self.P, self.w, self.R, self.Ab, self.rhs = side, sbar, P, w, R, Ab, rhs
        self.wpos = M.floor_pos(w)
        self._zk = None; self._cache = {}

    @property
    def zk(self):
        if self._zk is None:
            self._zk = M.zk_vec(self.side, self.sbar, self.P, self.wpos)
        return self._zk

    def alpha(self, name):
        """Step lengths of the set chosen by a single-set rule (cached)."""
        if name in self._cache:
            return self._cache[name]
        s, sb, P = self.side, self.sbar, self.P
        al = None
        if name == 'scip':
            al = M.scip_alpha(s, sb, P)
        elif name.startswith('lex'):
            nr = np.linalg.norm(self.R, axis=0)
            F = M.FO.best_orbit_lex(s, sb, P, self.wpos, nr, self.zk, M.zk_vec(s, sb, P, nr), eta=float(name[3:]))
            al = None if F is None else M.FO.steps_A(F, s, sb, P)
        elif name in ('orbit', 'orbit_core', 'orbitB') or name.startswith('pert') or name == 'geo':
            if name in ('orbit', 'orbitB'):
                u = self.wpos
            elif name == 'orbit_core':
                u = self.wpos
            elif name == 'geo':
                u = np.linalg.norm(self.R, axis=0)
            elif name.startswith('pertE'):
                # u_j = ||r_j|| (what_j + D), what_j = (w_j/||r_j||) / max_i (w_i/||r_i||):
                # perturbed corner bound in Euclidean units (Theorem: uniform depth)
                nr = np.linalg.norm(self.R, axis=0); rate = self.w / nr
                u = nr * (rate / max(rate.max(), 1e-300) + float(name[5:]))
            else:
                d = float(name[4:]); u = self.w / max(self.w.max(), 1e-300) + d
            u = M.floor_pos(u)
            if name == 'orbit_core':
                Q, b, c = bilinear_quadratic(s)
                zhi = corner_bound(Q, b, c, sb, P, u)
            else:
                zhi = M.zk_vec(s, sb, P, u)
            if name == 'orbitB' and 'orbit' in self._cache and self._cache.get('_F_orbit') is not None:
                F = self._cache['_F_orbit']
            else:
                _, _, F = M.FO.best_orbit(s, sb, P, u, min(zhi, 1e6), iters=25)
            if F is not None:
                if name == 'orbitB':
                    al = np.array([step_B(F, s, sb, P[:, j]) for j in range(P.shape[1])])
                else:
                    al = M.FO.steps_A(F, s, sb, P)
                if name == 'orbit':
                    self._cache['_F_orbit'] = F
            if name == 'orbit_core':
                self._cache['_zk_core'] = zhi
        self._cache[name] = al
        return al

    def cutvec(self, name):
        if name == 'corner':
            z = self.zk
            return None if (not np.isfinite(z) or z <= 0) else self.wpos / z
        al = self.alpha(name)
        if al is None:
            return None
        a = M.inv(al)
        if not np.all(np.isfinite(a)) or not np.any(a > 0):
            return None
        return a

    def row(self, a):
        row = a @ self.Ab; rr = a @ self.rhs - 1.0
        sc = np.abs(row).max()
        if sc < 1e-12:
            return None
        return row / sc, rr / sc

    def first_hits(self):
        if '_t' not in self._cache:
            self._cache['_t'] = M.first_hits(self.side, self.sbar, self.P)
        return self._cache['_t']


def bound_of(a, w):
    """z_C(w) = min_{a_j > 0} w_j / a_j."""
    v = [w[j] / a[j] for j in range(len(a)) if a[j] > 0]
    return min(v) if v else np.inf


def lp_value(I, rows, rhs):
    out = M.E.solve_lp(I, rows, rhs)
    return None if out is None else out[0].getInfo().objective_function_value


def choose(rule, rnd):
    """Single-set rules used in this round for 'alt' rules."""
    m = re.fullmatch(r'o(\d+)s', rule)
    if m:
        return 'orbit' if rnd < int(m.group(1)) else 'scip'
    m = re.fullmatch(r's(\d+)o', rule)
    if m:
        return 'scip' if rnd < int(m.group(1)) else 'orbit'
    if rule == 'alt':
        return 'orbit' if rnd % 2 == 0 else 'scip'
    if rule == 'alt2':
        return 'scip' if rnd % 2 == 0 else 'orbit'
    if rule == 'first_orbit':
        return 'orbit' if rnd == 0 else 'scip'
    return rule


def cuts_for_term(rule, cor, rnd, I, rows, rhs):
    rule = choose(rule, rnd)
    if rule == 'both':
        return [('scip', cor.cutvec('scip')), ('orbit', cor.cutvec('orbit'))]
    if rule == 'bothpert':
        return [('scip', cor.cutvec('scip')), ('pert0.1', cor.cutvec('pert0.1'))]
    if rule.startswith('hyb'):
        a_s = cor.cutvec('scip')
        if a_s is not None and np.isfinite(cor.zk) and bound_of(a_s, cor.wpos) >= float(rule[3:]) * cor.zk:
            return [('scip', a_s)]
        a_o = cor.cutvec('orbit')
        return [('orbit', a_o)] if a_o is not None else [('scip', a_s)]
    if rule.startswith('rnd'):
        seed = zlib.crc32(np.round(cor.sbar, 9).tobytes() + bytes([rnd % 256]))
        nm = 'orbit' if np.random.default_rng(seed).random() < float(rule[3:]) else 'scip'
        a = cor.cutvec(nm)
        return [(nm, a)] if a is not None else [('scip', cor.cutvec('scip'))]
    if rule == 'maj2':
        a_s, a_o = cor.cutvec('scip'), cor.cutvec('orbit')
        if a_o is None:
            return [('scip', a_s)]
        if a_s is None:
            return [('orbit', a_o)]
        m = (a_s > 0) | (a_o > 0)          # a = 1/alpha; orbit step >= SCIP step iff a_o <= a_s
        return [('orbit', a_o)] if 2 * int(np.sum(a_o[m] <= a_s[m])) > int(m.sum()) else [('scip', a_s)]
    if rule in ('oracle', 'oracle_seq', 'eff', 'eff2', 'depth', 'sumstep'):
        best, bestv = None, -np.inf
        for nm in (('scip', 'orbit') if rule == 'eff2' else POOL):
            a = cor.cutvec(nm)
            if a is None:
                continue
            if rule in ('oracle', 'oracle_seq'):
                rw = cor.row(a)
                if rw is None:
                    continue
                v = lp_value(I, rows + [rw[0]], rhs + [rw[1]])
                v = -np.inf if v is None else v
            elif rule in ('eff', 'eff2'):
                v = 1.0 / np.linalg.norm(a @ cor.Ab)
            elif rule == 'depth':
                v = M.conedepth(cor.R, a)
            else:
                t = cor.first_hits(); al = cor.alpha(nm)
                v = sum(min(1.0, al[j] / t[j]) if np.isfinite(t[j]) else (1.0 if not np.isfinite(al[j]) else 0.0)
                        for j in range(len(t)))
            if v > bestv + 1e-12:
                best, bestv = (nm, a), v
        return [best] if best is not None else []
    return [(rule, cor.cutvec(rule))]


def next_state(I, x2, R2, w2, zbil, z2):
    """Potential of an LP vertex: max over violated terms of z_K / (z_bil - z2), number of
    normalized reduced costs <= 1e-6 and <= 1e-3 (swappot diagnostics)."""
    wn = w2 / max(float(w2.max()), 1e-300)
    pot = 0.0
    for e2, (i2, j2) in enumerate(I['pairs']):
        idx2 = [i2, j2, I['p'] + e2]; sb2 = x2[idx2]
        if abs(sb2[2] - sb2[0] * sb2[1]) < 1e-6:
            continue
        side2 = '+' if sb2[2] > sb2[0] * sb2[1] else '-'
        zk2 = M.zk_vec(side2, sb2, R2[idx2, :], M.floor_pos(w2))
        if np.isfinite(zk2):
            pot = max(pot, zk2)
    rem = zbil - z2
    return dict(pot=float(pot / rem) if rem > 0 else None, n6=int(np.sum(wn <= 1e-6)), n3=int(np.sum(wn <= 1e-3)))


def run(I, rule, rounds, diag=False, swap=False, swapgamma=False, zbil=None):
    rows, rhs, normals = [], [], []
    hist, rinfo, cinfo = [], [], []
    setcount = {}                      # number of cuts per chosen set name (bookkeeping only)
    for r in range(rounds + 1):
        out = M.E.solve_lp(I, rows, rhs)
        if out is None:
            run.setcount = setcount
            return hist, rinfo, cinfo, 'lp_fail'
        h, A, bb = out
        z = h.getInfo().objective_function_value
        hist.append(z)
        bc = M.E.basis_cone(I, h, A, bb)
        if r == rounds or bc is None:
            if bc is None and r < rounds:
                hist += [z] * (rounds - r)
            break
        x, R, w, Ab, rhsB, _ = bc
        wmax = max(1.0, float(w.max()))
        ri = dict(r=r, z=z, nzero=int(np.sum(w <= 1e-9 * wmax)), nnear=int(np.sum(w <= 1e-6 * wmax)),
                  ncutrows_in_basis=int(sum(1 for k in range(I['A'].shape[0], A.shape[0])
                                            if h.getBasis().row_status[k] != M.E.highspy.HighsBasisStatus.kBasic)))
        if diag:
            ri['gamma'] = M.pointedness(R)
        newrows, newrhs, newnorm = [], [], []
        corners = []
        for e, (i, j) in enumerate(I['pairs']):
            idx = [i, j, I['p'] + e]
            sbar = x[idx]
            if abs(sbar[2] - sbar[0] * sbar[1]) < 1e-6:
                continue
            side = '+' if sbar[2] > sbar[0] * sbar[1] else '-'
            cor = Corner(side, sbar, R[idx, :], w, R, Ab, rhsB)
            corners.append((e, cor))
            base_r, base_b = (rows + newrows, rhs + newrhs) if rule == 'oracle_seq' else (rows, rhs)
            for nm, a in cuts_for_term(rule, cor, r, I, base_r, base_b):
                if a is None:
                    continue
                rw = cor.row(a)
                if rw is None:
                    continue
                newrows.append(rw[0]); newrhs.append(rw[1])
                setcount[nm] = setcount.get(nm, 0) + 1
                nv = rw[0] / np.linalg.norm(rw[0])
                if diag:
                    nrm = np.linalg.norm(R, axis=0)
                    ci = dict(r=r, e=e, set=nm, zk=cor.zk, zC=bound_of(a, cor.wpos),
                              viol=float(abs(sbar[2] - sbar[0] * sbar[1])),
                              minstep=float(min([nrm[q] / a[q] for q in range(len(a)) if a[q] > 0], default=np.inf)),
                              cosobj=float(nv @ (-I['c']) / np.linalg.norm(I['c'])),
                              eff=float(1.0 / np.linalg.norm(a @ Ab)), depth=M.conedepth(R, a),
                              maxcos_prev=float(max([abs(nv @ q) for q in normals], default=0.0)),
                              maxcos_round=float(max([abs(nv @ q) for q in newnorm], default=0.0)),
                              nnz=int(np.sum(np.abs(rw[0]) > 1e-9)))
                    gs = lp_value(I, rows + [rw[0]], rhs + [rw[1]])
                    ci['gain_single'] = None if gs is None else gs - z
                    if nm == 'orbit_core':
                        ci['zk_core'] = cor._cache.get('_zk_core')
                    a_s = cor.cutvec('scip')
                    if a_s is not None:
                        ci['zC_scip'] = bound_of(a_s, cor.wpos)
                        ci['w'] = (cor.w / max(cor.w.max(), 1e-300)).round(6).tolist()
                        ci['a'] = a.tolist(); ci['a_scip'] = a_s.tolist()
                        a_o = cor.cutvec('orbit')
                        if a_o is not None:
                            ci['a_orbit'] = a_o.tolist()
                    cinfo.append(ci)
                newnorm.append(nv)
        ri['ncuts'] = len(newrows)
        if swap and corners:
            for alt in ('scip', 'orbit'):
                rr_, bb_ = [], []
                for e, cor in corners:
                    a = cor.cutvec(alt)
                    if a is None:
                        continue
                    rw = cor.row(a)
                    if rw is not None:
                        rr_.append(rw[0]); bb_.append(rw[1])
                if swapgamma and rr_:
                    o2 = M.E.solve_lp(I, rows + rr_, rhs + bb_)
                    v = None if o2 is None else o2[0].getInfo().objective_function_value
                    bc2 = None if o2 is None else M.E.basis_cone(I, *o2)
                    if bc2 is not None:
                        x2 = bc2[0]
                        ri['swapgamma_' + alt] = M.pointedness(bc2[1])
                        ri['swapnzero_' + alt] = int(np.sum(bc2[2] <= 1e-9 * max(1.0, float(bc2[2].max()))))
                        ri['swapviol_' + alt] = float(sum(abs(x2[I['p'] + e2] - x2[i2] * x2[j2]) for e2, (i2, j2) in enumerate(I['pairs'])))
                        if zbil is not None:
                            ri['swappot_' + alt] = next_state(I, x2, bc2[1], bc2[2], zbil, v)
                else:
                    v = lp_value(I, rows + rr_, rhs + bb_) if rr_ else z
                ri['swap_' + alt] = v
        rinfo.append(ri)
        if not newrows:
            hist += [z] * (rounds - r)
            break
        rows += newrows; rhs += newrhs; normals += newnorm
    run.setcount = setcount
    return hist, rinfo, cinfo, 'ok'


if __name__ == '__main__':
    path, rules, ROUNDS, OUT = sys.argv[1], sys.argv[2].split(','), int(sys.argv[3]), sys.argv[4]
    i0, i1 = int(sys.argv[5]), int(sys.argv[6])
    diag = 'diag' in sys.argv[7:]; swap = 'swap' in sys.argv[7:] or 'swapgamma' in sys.argv[7:] or 'swappot' in sys.argv[7:]
    swapgamma = 'swapgamma' in sys.argv[7:] or 'swappot' in sys.argv[7:]
    swappot = 'swappot' in sys.argv[7:]
    insts = load(path)
    with open(OUT, 'a') as f:
        for k in range(i0, min(i1, len(insts))):
            I, zlp, zbil = insts[k]
            for rule in rules:
                t0 = time.time()
                hist, rinfo, cinfo, status = run(I, rule, ROUNDS, diag, swap, swapgamma, zbil if swappot else None)
                hist = hist + [hist[-1]] * (ROUNDS + 1 - len(hist)) if hist else [zlp] * (ROUNDS + 1)
                closed = [float(min(max((z - zlp) / (zbil - zlp), 0.0), 1.0 + 1e-9)) for z in hist]
                rec = dict(inst=k, rule=rule, status=status, zlp=zlp, zbil=zbil, closed=closed,
                           ncuts=int(sum(ri['ncuts'] for ri in rinfo)), seconds=time.time() - t0, rounds=rinfo,
                           sets=getattr(run, 'setcount', {}))
                if diag:
                    rec['cuts'] = cinfo
                f.write(json.dumps(rec) + '\n'); f.flush()
                print('inst %d %-10s closed r1 %.3f r3 %.3f final %.3f cuts %d  %.1fs' % (
                    k, rule, closed[1], closed[min(3, ROUNDS)], closed[-1], rec['ncuts'], rec['seconds']), flush=True)
