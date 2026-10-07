"""Reviewer's independent recomputation on the sample in r1-logs/sample_records.jsonl.gz.

Written without importing the stream's code. For each dumped attempt record:
  * rebuild the violated side q(s) = s^T Q s + b^T s + c <= 0 (S), the LP point sbar, the rays P
    (columns, on the constraint variables [quad vars, lin vars, aux var]) and the objective rates w;
  * SCIP's set (Chmiela-Munoz-Serrano Cases 1-4, point rule lambda = xhat(sbar)/|xhat(sbar)|),
    built from an eigendecomposition of the quadratic-variable block only (as SCIP does), with
    w(s) collecting zero-eigenvalue, linear and auxiliary terms;
  * step t_j = sup{t : G(sbar + t p_j) <= 0} by bracketing + scipy brentq (G is convex along rays);
    compared with SCIP's dumped step (relative 1e-6, or both infinite, no exit before 1e18);
  * validity along rays: q(sbar + tau t_j p_j) > 0 for tau in (0, 1) (SCIP's own t_j);
  * z_C = min_j w_j t_j (rates floored at 1e-9 max w, rays of fixed columns/equality rows dropped);
  * z_K for n_+ <= 1 (rho <= 2): minimum over single rays and ray pairs, each pair by a 2001-point
    theta grid with bounded-Brent refinement, final point checked q <= 1e-9 scale;
    degeneracy: some single zero-rate ray or pair of zero-rate rays meets S.
Output: one JSON line per record (r1-logs/indep_check.jsonl).
Usage: python3 indep_check.py [MAXN_FOR_ZK [SHARD NSHARDS]]  (shards write indep_check_<SHARD>.jsonl)"""
import sys, os, json, gzip, math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
INP = os.path.join(HERE, '../r1-logs/sample_records.jsonl.gz')
OUT = os.path.join(HERE, '../r1-logs/indep_check.jsonl')
EPS = 1e-9


def build(rec):
    nq, nl = rec['nquad'], rec['nlin']
    aux = rec['auxvar'] is not None
    nv = nq + nl + int(aux)
    Q = np.zeros((nv, nv)); b = np.zeros(nv)
    for i, a in enumerate(rec['qsqr']):
        Q[i, i] += a
    for i, j, a in rec['bilin']:
        Q[i, j] += 0.5 * a; Q[j, i] += 0.5 * a
    b[:nq] = rec['qlin']; b[nq:nq + nl] = rec['lincoefs']
    const = rec['constant']
    if aux:
        b[nv - 1] = -1.0
        if rec['over']:
            Q, b, c = -Q, -b, -const
        else:
            c = const
    else:
        if rec['over']:      # lhs <= q violated: lhs - q <= 0
            Q, b, c = -Q, -b, rec['lhs'] - const
        else:                # q <= rhs violated
            c = const - rec['rhs']
    sbar = np.array(rec['zlp'], float)
    N = rec['nrays']
    P = np.zeros((nv, N))
    for j, ent in enumerate(rec['rays']):
        for i, v in ent:
            P[i, j] = v
    lppos = np.array(rec['raylppos']); stat = np.array(rec['raystat']); rate = np.array(rec['rayrate'], float)
    # nonbasic column at lower bound (0) moves up: rate = reduced cost; at upper (2) moves down: -redcost.
    # row slack: activity leaves lhs (status 0) upwards: rate = dual; leaves rhs (status 2): -dual.
    w = np.where(stat == 2, -rate, rate)
    width = np.array(rec['raywidth'], float)
    return Q, b, c, sbar, P, w, width, nq


class Set:
    def __init__(self, Q, b, c, sbar, nq, case4_scip):
        self.nq = nq
        Qq = Q[:nq, :nq]
        th, V = np.linalg.eigh(Qq)
        self.th, self.V = th, V
        self.beta = V.T @ b[:nq]
        self.bl = b[nq:]
        self.ip, self.im = th > EPS, th < -EPS
        self.i0 = ~(self.ip | self.im)
        nz = self.ip | self.im
        kap = c - 0.25 * np.sum(self.beta[nz] ** 2 / th[nz])
        self.kappa = 0.0 if abs(kap) <= EPS else kap
        self.case4_py = bool(len(self.bl) > 0 or np.any(np.abs(self.beta[self.i0]) > 1e-12))
        self.case4 = bool(case4_scip)
        if self.case4:
            self.case = 4
        else:
            self.case = 1 if self.kappa == 0 else (2 if self.kappa > 0 else 3)
        x, y, wv = self.xyw(sbar[:, None])
        x, wv = x[:, 0], wv[0]
        if self.case in (1, 3):
            lam = x
        elif self.case == 2:
            lam = np.append(x, math.sqrt(self.kappa))
        else:
            r = math.sqrt(1 + self.kappa ** 2)
            lam = np.append(x, (wv + self.kappa + r) / (2 * math.sqrt(r)))
        self.lam = lam / np.linalg.norm(lam)

    def xyw(self, S):
        nq = self.nq
        psi = self.V.T @ S[:nq]
        th, be = self.th, self.beta
        x = np.sqrt(th[self.ip])[:, None] * (psi[self.ip] + (be[self.ip] / (2 * th[self.ip]))[:, None])
        y = np.sqrt(-th[self.im])[:, None] * (psi[self.im] + (be[self.im] / (2 * th[self.im]))[:, None])
        wv = be[self.i0] @ psi[self.i0] + self.bl @ S[nq:]
        return x, y, wv

    def G(self, S):
        x, y, wv = self.xyw(S)
        L, k = self.lam, self.kappa
        if self.case == 1:
            return np.linalg.norm(y, axis=0) - L @ x
        if self.case == 2:
            return np.linalg.norm(y, axis=0) - (L[:-1] @ x + L[-1] * math.sqrt(k))
        if self.case == 3:
            return np.sqrt(np.sum(y ** 2, 0) - k) - L @ x
        r = math.sqrt(1 + k ** 2); f = 2 * math.sqrt(r)
        xh = np.vstack([x, (wv + k + r) / f]); yh = np.vstack([y, (wv + k - r) / f])
        le = L[-1]; ny = np.linalg.norm(yh, axis=0); ye = yh[-1]
        phi = np.where(ye <= le * ny, ny, np.sqrt(np.maximum((1 - le ** 2) * (ny ** 2 - ye ** 2), 0)) + le * ye)
        return phi - L @ xh


def step(st, sbar, p, tmax=1e18):
    f = lambda t: float(st.G((sbar + t * p)[:, None])[0])
    if not np.any(p):
        return math.inf
    lo, t = 0.0, 2.0 ** -40
    while t <= tmax:
        if f(t) > 0:
            return brentq(f, lo, t, xtol=1e-300, rtol=1e-15, maxiter=500)
        lo, t = t, 2 * t
    return math.inf


def qval(Q, b, c, S):
    return np.einsum('ij,ij->j', S, Q @ S) + b @ S + c


def zk_pairs(Q, b, c, sbar, P, w, grid=2001):
    """min w^T lam over supports of size <= 2 (lam >= 0, q(sbar + P lam) <= 0)."""
    g0 = float(qval(Q, b, c, sbar[:, None])[0])
    gr = 2 * Q @ sbar + b
    N = P.shape[1]
    D = P / w[None, :]                      # unit-cost directions
    Ld = gr @ D; QD = Q @ D

    def zmin(L, M):
        # smallest z > 0 with g0 + z L + z^2 M <= 0 (g0 > 0)
        L = np.asarray(L, float); M = np.asarray(M, float)
        z = np.full(L.shape, np.inf)
        sc = np.maximum(np.abs(L) ** 2, np.abs(M * g0)) + 1e-300
        lin = np.abs(M) * g0 <= 1e-14 * sc
        m = lin & (L < 0); z[m] = -g0 / L[m]
        disc = L * L - 4 * M * g0
        with np.errstate(invalid='ignore', divide='ignore'):
            sq = np.sqrt(np.maximum(disc, 0))
            qq = -0.5 * (L - sq)                # L < 0 branch: qq = (-L + sq)/2 > 0
            r_small = g0 / qq                   # smaller root when M > 0, L < 0
            r_big = (-L + sq) / (2 * M)         # M < 0: positive root = (-L - sq)/(2M)
            r_neg = (-L - sq) / (2 * M)
        pos = ~lin & (M > 0) & (L < 0) & (disc >= 0)
        z[pos] = r_small[pos]
        neg = ~lin & (M < 0)
        z[neg] = r_neg[neg]
        return z

    M1 = np.einsum('ij,ij->j', D, QD)
    z1 = zmin(Ld, M1)
    best = float(np.min(z1)) if N else math.inf
    arg = ('1', int(np.argmin(z1))) if N else None
    if N >= 2:
        th = np.linspace(0, 1, grid)
        I, J = np.triu_indices(N, 1)
        G12 = D.T @ QD
        for s0 in range(0, len(I), 1000):
            ii, jj = I[s0:s0 + 1000], J[s0:s0 + 1000]
            a, bq, cc = M1[ii], G12[ii, jj], M1[jj]
            L = th[None, :] * Ld[ii][:, None] + (1 - th[None, :]) * Ld[jj][:, None]
            M = (th ** 2)[None, :] * a[:, None] + (2 * th * (1 - th))[None, :] * bq[:, None] + ((1 - th) ** 2)[None, :] * cc[:, None]
            Z = zmin(L, M)
            k = np.argmin(Z, axis=1); zz = Z[np.arange(len(ii)), k]
            for m in np.argsort(zz)[:5]:
                if not zz[m] < best * (1 + 1e-3):
                    break
                i, j = ii[m], jj[m]
                fz = lambda t: float(zmin(np.array([t * Ld[i] + (1 - t) * Ld[j]]),
                                          np.array([t * t * M1[i] + 2 * t * (1 - t) * G12[i, j] + (1 - t) ** 2 * M1[j]]))[0])
                t0 = th[k[m]]
                lo_, hi_ = max(0.0, t0 - 1.0 / (grid - 1)), min(1.0, t0 + 1.0 / (grid - 1))
                res = minimize_scalar(fz, bounds=(lo_, hi_), method='bounded', options=dict(xatol=1e-13))
                cand = [(fz(t0), t0), (fz(lo_), lo_), (fz(hi_), hi_)]
                if res.success and np.isfinite(res.fun):
                    cand.append((float(res.fun), float(res.x)))
                zc, tc = min(cand)
                # verify the point
                lamp = zc * (tc * D[:, i] + (1 - tc) * D[:, j])
                pt = sbar + lamp
                sc = abs(pt @ Q @ pt) + abs(b @ pt) + abs(c)
                if np.isfinite(zc) and qval(Q, b, c, pt[:, None])[0] <= 1e-9 * max(sc, 1.0) and zc < best:
                    best = float(zc); arg = ('2', int(i), int(j), float(tc))
    return best, arg, g0


def meets_S_zero_face(Q, b, c, sbar, P, zr):
    """Does a single zero-rate ray or a pair of them reach S?"""
    Pz = P[:, zr]
    if Pz.shape[1] == 0:
        return False
    z, _, _ = zk_pairs(Q, b, c, sbar, Pz, np.ones(Pz.shape[1]), grid=401)
    return bool(np.isfinite(z))


def main():
    maxn = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    shard, nsh = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 1)
    out = OUT if nsh == 1 else OUT.replace('.jsonl', '_%d.jsonl' % shard)
    with gzip.open(INP, 'rt') as fi, open(out, 'w') as fo:
        for n, line in enumerate(fi):
            if n % nsh != shard:
                continue
            rec = json.loads(line)
            o = dict(inst=rec['inst'], k=rec['k'], set=rec['set'], lp=rec['lp'], node=rec['node'], cons=rec['cons'],
                     fail=rec.get('fail'), gen=rec.get('gen'))
            if 'nrays' not in rec or 'kappa' not in rec:
                o['status'] = 'norays'; fo.write(json.dumps(o) + '\n'); continue
            Q, b, c, sbar, P, w, width, nq = build(rec)
            q0 = float(qval(Q, b, c, sbar[:, None])[0])
            o['q_sbar'] = q0; o['viol'] = rec['violation']
            kw = np.array(rec['raywidth'], float) > 1e-9
            o['wneg'] = int(np.sum(w[kw] < -1e-7 * max(1.0, np.abs(w[kw]).max(initial=0))))   # equality rows/fixed cols excluded
            st = Set(Q, b, c, sbar, nq, rec['case4'])
            o['case_scip'] = 4 if rec['case4'] else (2 if rec['kappa'] > 0 else (3 if rec['kappa'] < 0 else 1))
            o['case_mine'] = 4 if st.case4_py else (1 if st.kappa == 0 else (2 if st.kappa > 0 else 3))
            o['kappa_scip'] = rec['kappa']; o['kappa_mine'] = st.kappa
            o['npos'] = int(np.sum(np.linalg.eigvalsh(Q) > EPS))
            o['G0'] = float(st.G(sbar[:, None])[0])
            # SCIP steps
            N = rec['nrays']
            ts = np.full(N, np.nan); mono = np.zeros(N, bool)
            for e in rec.get('perray', []):
                if e.get('fail'):
                    continue
                t = e['t']
                if t is None or t >= 1e20:
                    ts[e['i']] = math.inf
                elif t >= 0:
                    ts[e['i']] = t
                mono[e['i']] = bool(e['mono'])
            tm = np.full(N, np.nan)
            cmp = {'match': 0, 'both_inf': 0, 'diff': 0, 'scip_inf': 0, 'mine_inf': 0}
            bad = []; maxrel = 0.0
            if o['G0'] < 0:
                for j in range(N):
                    tm[j] = step(st, sbar, P[:, j])
                    if np.isnan(ts[j]):
                        continue
                    a, m = ts[j], tm[j]
                    if math.isinf(a) and math.isinf(m):
                        cmp['both_inf'] += 1
                    elif math.isinf(a):
                        cmp['scip_inf'] += 1; bad.append([j, a, m])
                    elif math.isinf(m):
                        cmp['mine_inf'] += 1; bad.append([j, a, m])
                    else:
                        rel = abs(a - m) / m
                        if rel <= 1e-6:
                            cmp['match'] += 1; maxrel = max(maxrel, rel)
                        else:
                            cmp['diff'] += 1; bad.append([j, a, m])
            o['cmp'] = cmp; o['maxrel_match'] = maxrel; o['mismatch'] = bad[:10]
            # validity of SCIP's steps along each ray: q > 0 on (sbar, sbar + t p)
            fin = np.where(np.isfinite(ts))[0]
            if fin.size:
                tau = np.linspace(0, 1, 201)[1:-1]
                mins = []
                for j in fin:
                    S = sbar[:, None] + (tau * ts[j])[None, :] * P[:, [j]]
                    mins.append(float(np.min(qval(Q, b, c, S))))
                o['min_q_on_segments_rel'] = min(mins) / q0
            # corner
            keep = width > 1e-9
            Pk, wk, tk, tmk = P[:, keep], w[keep], ts[keep], tm[keep]
            o['nrays_corner'] = int(keep.sum())
            if wk.size == 0 or wk.max() <= 0:
                o['status'] = 'allzero'; fo.write(json.dumps(o) + '\n'); fo.flush(); continue
            wf = np.maximum(wk, 1e-9 * wk.max())
            if not np.any(np.isnan(tk)):
                f = np.isfinite(tk); o['zC_scip'] = float(np.min(wf[f] * tk[f])) if f.any() else math.inf
            if not np.any(np.isnan(tmk)) and o['G0'] < 0:
                f = np.isfinite(tmk); o['zC_mine'] = float(np.min(wf[f] * tmk[f])) if f.any() else math.inf
            if o['npos'] <= 1 and keep.sum() <= maxn:
                zr = wk <= 1e-9 * wk.max()
                o['degenerate'] = meets_S_zero_face(Q, b, c, sbar, Pk, zr)
                zk, arg, _ = zk_pairs(Q, b, c, sbar, Pk, wf)
                o['zK_pairs'] = zk; o['zK_arg'] = arg
            o['status'] = 'ok'
            fo.write(json.dumps(o, default=float) + '\n'); fo.flush()


if __name__ == '__main__':
    main()
