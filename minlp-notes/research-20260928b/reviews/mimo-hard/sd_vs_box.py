"""Sphere decoding (unconstrained partial-distance bound) versus box-relaxation
B&B: does the box relaxation change the order of the exponent? (review check
of the sentence in Section 8 of the note: "The box relaxation therefore does
not change the order of the exponent of enumeration.")

Part A (heuristic, typical counts).  Fincke-Pohst with natural order and
radius^2 = W: fixing k coordinates of which j are wrong gives partial
distance ~ (1 + 4 rho j/N) chi^2_{M-N+k} (Hassibi-Vikalo), so typical survivors
at level k are the j-subsets with j <= jSD_k = (N/(4rho)) (N-k)/(M-N+k).
The box-relaxation analogue (Section 4.4 of the note) is
jbox_d = N (N-d)/(4 rho (2M-N+d)).  We compare max_k log sum_{j<=j_k} C(k,j).

Part B (real instances, small N).  Exact Fincke-Pohst node counts
(1 + 2 * number of surviving partial vectors) with radius^2 = W and
natural order, beta = 1, rho = 4 log N; compared with the note's box
static-order and most-fractional B&B trees (Table 7.3).
Also the rigorous-ish lower bound: at level k all 2^k partial vectors survive
when (sqrt(k) + 4 k sqrt(rho/N))^2 <~ N, i.e. k ~ N/(4 sqrt(rho)) for beta = 1.
"""
import numpy as np
from scipy.special import gammaln, logsumexp


def log_count(jmax, k):
    j = np.arange(0, int(min(np.floor(jmax), k)) + 1)
    if len(j) == 0:
        return -np.inf
    return logsumexp(gammaln(k + 1) - gammaln(j + 1) - gammaln(k - j + 1))


def exponents(N, beta, rho):
    M = beta * N
    ks = np.unique(np.round(np.logspace(0, np.log10(N - 1), 400)).astype(int))
    sd = max(log_count(N / (4 * rho) * (N - k) / (M - N + k), k) for k in ks)
    bx = max(log_count(N * (N - k) / (4 * rho * (2 * M - N + k)), k) for k in ks)
    return sd, bx


print("Part A: typical-count exponents (log #nodes), natural order")
print("  beta     N      rho   SD      box     (N/(4(2b-1)rho))log rho   JO: (N/(4rho+2))log2   N/sqrt(rho)")
for beta in (1.0, 2.0):
    for N in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        for c in (4.0, 8.0):
            rho = c * np.log(N)
            sd, bx = exponents(N, beta, rho)
            print("  %.0f  %8d  %6.1f  %8.1f  %8.1f  %10.1f  %10.1f  %10.1f"
                  % (beta, N, rho, sd, bx, N / (4 * (2 * beta - 1) * rho) * np.log(rho),
                     N / (4 * rho + 2) * np.log(2), N / np.sqrt(rho)))


def fp_nodes(N, beta, rho, seed, cap=3_000_000):
    rng = np.random.default_rng(seed)
    M = int(round(beta * N))
    H = rng.standard_normal((M, N)); A = np.sqrt(rho / N) * H
    xs = rng.choice([-1.0, 1.0], N)
    w = rng.standard_normal(M); y = A @ xs + w
    Q, R = np.linalg.qr(A)
    z = Q.T @ y
    const = y @ y - z @ z
    r2 = w @ w - const              # radius^2 for the triangular part
    # level k: partial vectors on coordinates N-k..N-1
    S = np.zeros((1, 0)); PD = np.zeros(1)
    total = 1
    for k in range(1, N + 1):
        i = N - k
        cand = []
        for val in (-1.0, 1.0):
            Snew = np.hstack([np.full((S.shape[0], 1), val), S])
            t = z[i] - Snew @ R[i, i:]
            cand.append((Snew, PD + t ** 2))
        S = np.vstack([c[0] for c in cand]); PD = np.concatenate([c[1] for c in cand])
        total += S.shape[0]
        keep = PD <= r2 * (1 + 1e-12)
        S = S[keep]; PD = PD[keep]
        if S.shape[0] > cap:
            return total, False
    return total, True


print()
print("Part B: exact Fincke-Pohst node counts, radius^2 = W, natural order, beta = 1, rho = 4 log N")
print("  (note, Table 7.3, box B&B geometric means at rho = 4 log N: static 90, 246, 2000, >1e5;"
      " most-fractional 44, 97, 509, 15765 for N = 32, 64, 128, 256)")
for N in (32, 64, 96, 128):
    rho = 4 * np.log(N)
    res = [fp_nodes(N, 1.0, rho, 100 + s) for s in range(4)]
    vals = [r[0] for r in res]
    print("  N=%d rho=%.1f: FP nodes %s (complete: %s); geo.mean %.0f;  2^{N/(4 sqrt rho)} = %.0f"
          % (N, rho, vals, [r[1] for r in res], np.exp(np.mean(np.log(vals))), 2 ** (N / (4 * np.sqrt(rho)))),
          flush=True)
