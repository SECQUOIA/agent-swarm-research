"""Equilibrium-cycle simulation in power variables p = phi*k for a fixed reload assignment.

Power-variable model (see assessment.md, Section 1):
  k_{t+1} = k_t - a p_t,   V'p_t = 1,   0 <= p_t <= c,   lam_t p_t = k_t o (G p_t),   k_1 = KF f + R k_T.
For k_t > 0 and G irreducible, the only p_t >= 0 with V'p_t = 1 solving the eigen rows is the
normalized Perron vector of diag(k_t) G, and lam_t = rho(G diag(k_t)).  So a fixed assignment leaves
only the fixed-point equation k_1 = Phi(k_1) := KF f + R(k_1 - a sum_{t<T} p_t(k_1)).

Assignment encodings
  F1: typ[i] = fuel type at node i (tied half-nodes carry the same type).
      reload: k_1[i] = KF if fresh(typ[i]) else sum_j V_j k_T[j] [typ[j] == pred(typ[i])] (a V-weighted mean).
  F2: src[i] = -1 (fresh) or node j whose end-of-cycle fuel is moved to i.
"""
import numpy as np
import nucmodel


class Data:
    def __init__(self, name):
        I = nucmodel.load(name)
        self.I = I; self.name = name
        self.N, self.T = I.N, I.T
        self.G = np.array([[float(x) for x in r] for r in I.G])
        self.V = np.array([float(x) for x in I.V])
        self.c = float(min(min(r) for r in I.c)); assert all(float(x) == self.c for r in I.c for x in r)
        self.a, self.KF, self.fam = float(I.a), float(I.KF), I.fam
        if I.fam == "F1":
            self.ntypes = I.ntypes; self.fresh = list(I.fresh); self.pred = list(I.pred); self.ties = list(I.ties)
            # chains: fresh type -> successor types by age
            succ = {I.pred[g]: g for g in range(I.ntypes) if I.pred[g] is not None}
            self.chains = []
            for g in range(I.ntypes):
                if I.fresh[g]:
                    ch = [g]
                    while ch[-1] in succ: ch.append(succ[ch[-1]])
                    self.chains.append(ch)
            self.age = {g: a for ch in self.chains for a, g in enumerate(ch)}
            self.nages = len(self.chains[0]); assert all(len(ch) == self.nages for ch in self.chains)

    # ---------- reload as an affine map k_1 = KF f + R k_T ----------
    def reload_matrix(self, asg):
        N = self.N; R = np.zeros((N, N)); f = np.zeros(N)
        if self.fam == "F1":
            typ = asg
            for i in range(N):
                g = typ[i]
                if self.fresh[g]: f[i] = 1.0
                else:
                    for j in range(N):
                        if typ[j] == self.pred[g]: R[i, j] = self.V[j]
        else:
            for i, s in enumerate(asg):
                if s < 0: f[i] = 1.0
                else: R[i, s] = 1.0
        return f, R


def perron(G, k):
    """rho(G diag(k)) and the Perron vector p of diag(k) G (p = k o phi with phi the right Perron vector
    of G diag(k)), both from the right eigenvector of G diag(k)."""
    M = G * k[None, :]
    ev, W = np.linalg.eig(M)
    m = np.argmax(ev.real); lam = ev[m].real
    phi = np.abs(W[:, m].real)
    return lam, phi


def cycle(D, k1):
    """Simulate one cycle from k_1. Returns (k list, p list, lam list)."""
    ks, ps, lams = [], [], []
    k = k1.copy()
    for t in range(D.T):
        lam, phi = perron(D.G, k)
        p = phi * k; p = p / (D.V @ p)
        ks.append(k); ps.append(p); lams.append(lam)
        if t < D.T - 1:
            k = k - D.a * p
    return ks, ps, lams


def equilibrium(D, asg, k1=None, tol=1e-13, maxit=2000, newton=True):
    """Fixed point k_1 = KF f + R k_T(k_1) by damped iteration then Newton (finite-difference Jacobian).
    Returns dict(k1, lam_T, peak, ps, ks, lams, it, res)."""
    f, R = D.reload_matrix(asg)
    Phi = lambda k: D.KF * f + R @ cycle(D, k)[0][-1]
    k = np.full(D.N, D.KF) if k1 is None else np.array(k1, float)
    res = np.inf; it = 0
    for it in range(maxit):
        kn = Phi(k); res = np.max(np.abs(kn - k)); k = kn
        if res < 1e-9: break
    if newton:
        for _ in range(8):
            r = Phi(k) - k
            if np.max(np.abs(r)) < tol: break
            J = np.zeros((D.N, D.N)); h = 1e-7
            for j in range(D.N):
                e = np.zeros(D.N); e[j] = h
                J[:, j] = (Phi(k + e) - Phi(k - e)) / (2 * h)
            k = k - np.linalg.solve(J - np.eye(D.N), r)
        res = np.max(np.abs(Phi(k) - k))
    ks, ps, lams = cycle(D, k)
    return dict(k1=k, lam_T=lams[-1], peak=max(p.max() for p in ps), ps=ps, ks=ks, lams=lams, it=it, res=res,
                feasible=max(p.max() for p in ps) <= D.c + 1e-9)


def jacobian_Phi(D, asg, k):
    f, R = D.reload_matrix(asg)
    Phi = lambda kk: D.KF * f + R @ cycle(D, kk)[0][-1]
    J = np.zeros((D.N, D.N)); h = 1e-7
    for j in range(D.N):
        e = np.zeros(D.N); e[j] = h
        J[:, j] = (Phi(k + e) - Phi(k - e)) / (2 * h)
    return J


# ---------- random assignments ----------
def random_asg(D, rng):
    if D.fam == "F1":
        # slots: tied pairs count as one slot
        tied = {j: i for i, j in D.ties}
        slots = [i for i in range(D.N) if i not in tied]
        types = rng.permutation(D.ntypes)
        assert len(slots) == D.ntypes
        typ = [None] * D.N
        for s, g in zip(slots, types): typ[s] = g
        for i, j in D.ties: typ[j] = typ[i]
        return typ
    else:
        nf = int(D.I.nfresh)
        # random partition into nf chains (paths): random permutation cut at nf-1 random places
        perm = list(rng.permutation(D.N)); cuts = sorted(rng.choice(np.arange(1, D.N), nf - 1, replace=False))
        chains = np.split(np.array(perm), cuts)
        src = [None] * D.N
        for ch in chains:
            src[ch[0]] = -1
            for u, v in zip(ch[:-1], ch[1:]): src[v] = u
        return src
