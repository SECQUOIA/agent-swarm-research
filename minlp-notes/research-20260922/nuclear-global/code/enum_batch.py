"""Batched equilibrium-cycle evaluation of F1 patterns (va-vf layout: slots, tied half-node pairs, chains).

Pattern encoding: typ[b, i] = fuel type at node i.  Canonical patterns (modulo relabeling the identical
chains): chains are numbered by the slot order of their fresh fuel.
  count = (#slots)! / (#chains)!   (79,833,600 for va-vf)
Enumeration order: age map (which slots hold age 0..A) x chain links (which chain each non-fresh slot continues).

Evaluation: fixed-point iteration k_1 <- KF f + R k_T(k_1), Perron vectors by warm-started shifted inverse
iteration (one step per outer iteration after an eig() start); stops when max |dk_1| < tol.
Returns lam_T, max_t max_i p_it (peaking), residuals.  Floating point; see assessment.md for the
certification that a proof would add.

usage: enum_batch.py name sample NSAMPLES seed        (uniform random canonical patterns)
       enum_batch.py name shard I M                   (age maps with index = I mod M, all links)
"""
import sys, time, json, itertools, math, numpy as np
from nucsim import Data


def layout(D):
    tied = {j: i for i, j in D.ties}
    slots = [i for i in range(D.N) if i not in tied]
    partner = {i: j for i, j in D.ties}
    return slots, partner


def typ_from(D, slots, partner, agemap, links):
    """agemap: age per slot; links: for each age a >= 1, a permutation giving the chain of the slots with that
    age (slots of each age taken in increasing order).  Fresh slots get chains 0..C-1 in increasing order."""
    N = D.N; typ = np.empty(N, int)
    for a in range(D.nages):
        ss = [s for s, ag in zip(slots, agemap) if ag == a]
        chs = range(len(ss)) if a == 0 else links[a - 1]
        for s, ch in zip(ss, chs):
            g = D.chains[ch][a]; typ[s] = g
            if s in partner: typ[partner[s]] = g
    return typ


def reload_arrays(D, typ):
    """k1[b,i] = KF*fresh[b,i] + w1*kT[b,s1] + w2*kT[b,s2]"""
    B, N = typ.shape
    fresh = np.array([[D.fresh[g] for g in row] for row in typ], float)
    s1 = np.zeros((B, N), int); s2 = np.zeros((B, N), int); w1 = np.zeros((B, N)); w2 = np.zeros((B, N))
    for b in range(B):
        where = {}
        for j, g in enumerate(typ[b]): where.setdefault(g, []).append(j)
        for i, g in enumerate(typ[b]):
            if D.fresh[g]: continue
            src = where[D.pred[g]]
            s1[b, i] = src[0]; w1[b, i] = D.V[src[0]]
            if len(src) > 1: s2[b, i] = src[1]; w2[b, i] = D.V[src[1]]
            assert abs(sum(D.V[j] for j in src) - 1) < 1e-12
    return fresh, s1, s2, w1, w2


def evaluate(D, typ, tol=1e-11, maxit=200):
    B, N, T = typ.shape[0], D.N, D.T
    fresh, s1, s2, w1, w2 = reload_arrays(D, typ)
    ar = np.arange(B)[:, None]
    k1 = np.full((B, N), D.KF)
    phis = np.ones((T, B, N)) / N; lams = np.ones((T, B))
    I = np.eye(N)[None]
    first = True
    for it in range(maxit):
        k = k1.copy(); ps = []
        for t in range(T):
            M = D.G[None] * k[:, None, :]
            if first:
                ev, W = np.linalg.eig(M); m = np.argmax(ev.real, axis=1)
                phi = np.abs(W[np.arange(B), :, m].real); lam = ev[np.arange(B), m].real
            else:
                sig = lams[t] * (1 + 2e-3)
                x = np.linalg.solve(M - sig[:, None, None] * I, phis[t][:, :, None])[:, :, 0]
                phi = x / x.sum(1, keepdims=True)
                lam = (np.einsum("bij,bj->bi", M, phi)).sum(1) / phi.sum(1)
            phis[t] = phi / phi.sum(1, keepdims=True); lams[t] = lam
            p = phis[t] * k; p = p / (p @ D.V)[:, None]
            ps.append(p)
            if t < T - 1: k = k - D.a * p
        kT = k
        k1n = D.KF * fresh + w1 * kT[ar, s1] + w2 * kT[ar, s2]
        d = np.max(np.abs(k1n - k1)); k1 = k1n; first = False
        if d < tol: break
    # residuals at the final iterate (recompute cycle from k1 with exact eig)
    k = k1.copy(); eres = 0.0; peak = np.zeros(B); lamT = None
    for t in range(T):
        M = D.G[None] * k[:, None, :]
        ev, W = np.linalg.eig(M); m = np.argmax(ev.real, axis=1)
        phi = np.abs(W[np.arange(B), :, m].real); lam = ev[np.arange(B), m].real
        p = phi * k; p = p / (p @ D.V)[:, None]
        peak = np.maximum(peak, p.max(1))
        if t < T - 1: k = k - D.a * p
        else: lamT = lam
    k1n = D.KF * fresh + w1 * k[ar, s1] + w2 * k[ar, s2]
    fpres = np.max(np.abs(k1n - k1), axis=1)
    return lamT, peak, fpres, it + 1


def random_canonical(D, rng, n):
    slots, partner = layout(D)
    C = len(D.chains); out = []
    for _ in range(n):
        agemap = rng.permutation(np.repeat(np.arange(D.nages), C))
        links = [list(rng.permutation(C)) for _ in range(D.nages - 1)]
        out.append(typ_from(D, slots, partner, agemap, links))
    return np.array(out)


def agemaps(D):
    slots, _ = layout(D); C = len(D.chains); n = len(slots)
    # all arrangements of the multiset {0^C, 1^C, ..., A^C}
    def rec(pref, cnt):
        if len(pref) == n: yield tuple(pref); return
        for a in range(D.nages):
            if cnt[a] < C:
                cnt[a] += 1; yield from rec(pref + [a], cnt); cnt[a] -= 1
    yield from rec([], [0] * D.nages)


if __name__ == "__main__":
    name, mode = sys.argv[1], sys.argv[2]
    D = Data(name); slots, partner = layout(D); C = len(D.chains)
    if mode == "sample":
        n, seed = int(sys.argv[3]), int(sys.argv[4]); rng = np.random.default_rng(seed)
        res = []; t0 = time.time()
        for s in range(0, n, 2000):
            typ = random_canonical(D, rng, min(2000, n - s))
            lamT, peak, fpres, its = evaluate(D, typ)
            res.append(np.c_[lamT, peak, fpres])
        R = np.vstack(res); dt = time.time() - t0
        np.save(f"../runs/sample_{name}_{seed}.npy", R)
        feas = R[:, 1] <= D.c + 1e-9
        print(f"{name}: {n} random canonical patterns in {dt:.1f}s ({dt / n * 1e3:.3f} ms/pattern); feasible {feas.mean():.3f}; "
              f"max fp residual {R[:, 2].max():.1e}; lam_T feasible: max {R[feas, 0].max():.6f} "
              f"q99 {np.quantile(R[feas, 0], .99):.6f} median {np.median(R[feas, 0]):.6f}")
    else:
        I_, M_ = int(sys.argv[3]), int(sys.argv[4])
        links_all = list(itertools.product(*[list(itertools.permutations(range(C)))] * (D.nages - 1)))
        best = (-1, None); cnt = 0; nfeas = 0; hist = np.zeros(400, int); t0 = time.time(); maxres = 0.0
        for q, am in enumerate(agemaps(D)):
            if q % M_ != I_: continue
            typ = np.array([typ_from(D, slots, partner, am, lk) for lk in links_all])
            lamT, peak, fpres, its = evaluate(D, typ)
            feas = peak <= D.c + 1e-9; cnt += len(typ); nfeas += feas.sum(); maxres = max(maxres, fpres.max())
            if feas.any():
                j = np.argmax(np.where(feas, lamT, -1))
                if lamT[j] > best[0]: best = (float(lamT[j]), [int(x) for x in typ[j]], float(peak[j]))
                hist += np.histogram(lamT[feas], bins=400, range=(0.9, 1.1))[0]
        json.dump(dict(name=name, shard=I_, of=M_, count=cnt, feasible=int(nfeas), best=best, maxres=maxres,
                       hist=hist.tolist(), time=time.time() - t0), open(f"../runs/enum_{name}_{I_}_{M_}.json", "w"))
        print(name, I_, M_, cnt, nfeas, best, time.time() - t0)
