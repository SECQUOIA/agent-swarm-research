"""Valid linear cuts for the nuclear* models (see nuclear-bounds.md for proofs).

For every time step t (lam_t, phi_{.,t}, k_{.,t}, G_t extracted from the eigen rows):
  (UB)  k_{i,t} <= KF                                   (fresh reactivity; proved per family in nuc_verify)
  (CW)  lam_t <= nu_t,  nu_t >= sum_j G_ij w_j k_{j,t} / w_i  for all i   (w = Perron vector of G_t, > 0)
  (BURN) sum_i V_i k_{i,t+1} = sum_i V_i k_{i,t} - alpha  (sum of burnup rows weighted by the normalization)
  (LAM) lam_T <= certified constant bound from nuc_verify.
"""
import json, os
import numpy as np
from fractions import Fraction as F
from osil_eval import Model


def eigen_groups(M):
    """lam var -> list of (row, phi_i). Eigen rows: '=0', no linear part, one -1 term, other coefs > 0."""
    cand = {}
    for r, Q in M.quad.items():
        if r < 0 or M.lin[r] or M.clb[r] != "0" or M.cub[r] != "0": continue
        neg = [(a, b) for a, b, c in Q if float(c) == -1.0]
        if len(neg) == 1 and all(float(c) > 0 for a, b, c in Q if float(c) != -1.0):
            cand.setdefault(neg[0], []).append(r)
    cnt = {}
    for (a, b) in cand:
        cnt[a] = cnt.get(a, 0) + 1; cnt[b] = cnt.get(b, 0) + 1
    groups = {}
    for (a, b), rows in cand.items():
        lam, phi = (a, b) if cnt[a] > cnt[b] else (b, a)
        for r in rows: groups.setdefault(lam, []).append((r, phi))
    return groups


def time_structure(M):
    groups = eigen_groups(M)
    steps = []
    for lam, rows in groups.items():
        node = {p: n for n, (_, p) in enumerate(rows)}
        N = len(rows); G = np.zeros((N, N)); k = [None] * N
        for n, (r, p) in enumerate(rows):
            for a, b, c in M.quad[r]:
                if lam in (a, b): continue
                f, kk = (a, b) if a in node else (b, a)
                assert f in node and kk not in node
                k[node[f]] = kk if k[node[f]] is None else k[node[f]]
                assert k[node[f]] == kk
                G[n, node[f]] += float(c)
        steps.append(dict(lam=lam, phi=[p for _, p in rows], k=k, G=G))
    # normalization rows and burnup (alpha) per step
    for s in steps:
        pairs = {frozenset((s["phi"][i], s["k"][i])): i for i in range(len(s["k"]))}
        s["V"] = None
        for r in range(M.m):
            Q = M.quad.get(r, [])
            if M.clb[r] == M.cub[r] == "1" and Q and not M.lin[r] and {frozenset((a, b)) for a, b, _ in Q} == set(pairs):
                V = [0.0] * len(pairs)
                for a, b, c in Q: V[pairs[frozenset((a, b))]] = float(c)
                s["V"] = V
    nxt = {}
    for r in range(M.m):
        L, Q = M.lin[r], M.quad.get(r, [])
        if len(L) == 2 and len(Q) == 1 and M.clb[r] == M.cub[r] == "0" and sorted(float(v) for v in L.values()) == [-1, 1]:
            a = [j for j, v in L.items() if float(v) == -1][0]; b = [j for j, v in L.items() if float(v) == 1][0]
            if a in Q[0][:2]:
                phi = Q[0][1] if Q[0][0] == a else Q[0][0]
                nxt[a] = (b, float(Q[0][2]), phi)
    return steps, nxt


class Lin:
    """accumulate coefficients on solver variables (which may be unhashable)"""
    def __init__(self): self.d = {}
    def add(self, v, c):
        k = id(v); self.d[k] = (v, self.d.get(k, (v, 0.0))[1] + c); return self
    def items(self): return list(self.d.values())


def add_cuts(M, x, addlin, KF, lam_bound, model_add_var):
    """addlin(coefs: dict var->coef, sense, rhs); model_add_var(name, lb, ub) -> new var. x: list of solver vars."""
    steps, nxt = time_structure(M)
    ncuts = 0
    for s in steps:
        for kk in s["k"]:
            addlin(Lin().add(x[kk], 1.0), "<=", KF); ncuts += 1
        G = s["G"]
        ev, W = np.linalg.eig(G + 1e-9); w = np.abs(np.real(W[:, np.argmax(np.real(ev))])); w /= w.max(); w = np.maximum(w, 1e-9)
        nu = model_add_var(f"nu_{s['lam']}", 0.0, None)
        addlin(Lin().add(x[s["lam"]], 1.0).add(nu, -1.0), "<=", 0.0); ncuts += 1
        for i in range(len(w)):
            coefs = Lin().add(nu, 1.0)
            for j in np.nonzero(G[i])[0]:
                coefs.add(x[s["k"][j]], -G[i, j] * w[j] / w[i])
            addlin(coefs, ">=", 0.0); ncuts += 1
        # BURN: needs V at this step and next-k for every node with a common alpha
        if s["V"] is not None and all(kk in nxt for kk in s["k"]):
            al = {nxt[kk][1] for kk in s["k"]}
            phis_ok = all(nxt[s["k"][i]][2] == s["phi"][i] for i in range(len(s["k"])))
            if len(al) == 1 and phis_ok:
                coefs = Lin()
                for i, kk in enumerate(s["k"]):
                    coefs.add(x[nxt[kk][0]], s["V"][i]); coefs.add(x[kk], -s["V"][i])
                addlin(coefs, "==", -al.pop()); ncuts += 1
    return ncuts, len(steps)
