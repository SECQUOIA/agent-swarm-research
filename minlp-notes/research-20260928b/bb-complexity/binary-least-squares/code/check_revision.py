"""Checks added in the revision after review (Section 10 of the note).
 A  Face law for sign-symmetric designs (R1): for fixed columns in general
    position and every S, exactly one of the 2^n sign patterns eps has
    projection face S for cone{eps_j g_j} (deterministic identity), and the
    face frequencies for Laplace / correlated columns are uniform.
 B  SDP exactness threshold in closed form (R9): rho* = lambda_max(-D; K)^2,
    K = H'H/N, D = Diag(x* o H'w)/sqrt(N), versus the bisection values in
    data/sdp.jsonl; for square systems, the bottom-eigenvector prediction
    (v1'Dv1/lambda_1(K))^2 versus the coordinate prediction.
 C  Top-K refinement of Theorem 4.1 (S1): sum of the K largest -g_i versus
    K max(-g_i) and versus the bound K(sqrt(2 log(N/K)) + 1) + sqrt(2 K log N).
 D  Fincke-Pohst (natural order, radius^2 = f(x*)) versus box static-order
    B&B on the same instances (hard-review C3), beta = 1, rho = 4 log N.
 E  Midpoint-clique upper bound (hard-review C5): largest n_1 with a
    non-negligible first-moment count of improving ternary points, versus
    N^{1 - c/8}.
 F  Scope (hard-review C7): the diagonal-shift reformulation
    f + d sum(1 - x_i^2), d = 0.99 lambda_min(A'A), versus the box
    relaxation: relative root gaps, beta = 2; exactness of Prop. 6.3 with
    d = lambda_min(A'A) (min zeta_i >= -d).
 G  The proved loss factor kappa_rho of Theorem 4.1 at practical rho (recheck F9).
Usage: python3 check_revision.py [A|B|C|D|E|F ...]   (default: all)
"""
import sys, os, json, itertools
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import nnls, lsq_linear
from scipy.linalg import eigh, cholesky
from scipy.special import gammaln, logsumexp
from core import instance, box_min, bnb, fval_u

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def face(G, v):
    u, _ = nnls(G, v, maxiter=5000)
    return tuple(np.nonzero(u > 1e-12)[0])


def part_A():
    rng = np.random.default_rng(1)
    bad = 0; tot = 0
    for t in range(200):
        n = int(rng.integers(2, 6)); M = n + int(rng.integers(0, 4))
        kind = t % 3
        if kind == 0:
            G = rng.laplace(size=(M, n))
        elif kind == 1:
            L = rng.standard_normal((M, M)); G = L @ rng.standard_normal((M, n))
        else:
            G = rng.standard_normal((M, n)) + 0.8   # not sign-symmetric in law, identity is deterministic anyway
        v = rng.standard_normal(M)
        counts = {}
        for eps in itertools.product([-1.0, 1.0], repeat=n):
            f = face(G * np.array(eps), v)
            counts[f] = counts.get(f, 0) + 1
        tot += 1
        bad += not (len(counts) == 2 ** n and all(c == 1 for c in counts.values()))
    print("A1 deterministic sign-pattern identity (each face exactly once over the 2^n patterns): failures %d / %d" % (bad, tot))
    # frequencies for sign-symmetric non-Gaussian laws
    from scipy.stats import chisquare
    for name in ("laplace", "correlated"):
        n, M = 4, 6
        cnt = np.zeros(2 ** n)
        Sig = rng.standard_normal((M, M))
        v = rng.standard_normal(M)
        for t in range(16000):
            if name == "laplace":
                G = rng.laplace(size=(M, n))
            else:
                G = Sig @ rng.standard_normal((M, n))
            f = face(G, v)
            cnt[sum(1 << j for j in f)] += 1
        print("A2 %s columns (n=4, M=6, fixed v): chi-square p-value for uniform faces = %.3f" % (name, chisquare(cnt).pvalue))


def part_B():
    rows = [json.loads(l) for l in open(os.path.join(DATA, "sdp.jsonl")) if '"part": "a"' in l]
    maxrel = 0.0; n = 0
    sq = []
    for r in rows:
        if r["N"] > 400 or r["seed"] >= 10:
            continue
        N, M, s = r["N"], r["M"], r["seed"]
        A, y, xs, B, w = instance(N, M, 1.0, s)      # rho = 1: A = H/sqrt(N)
        K = A.T @ A
        D = np.diag(xs * (A.T @ w))
        lam = eigh(-D, K, eigvals_only=True)[-1]
        rs = lam ** 2 if lam > 0 else 0.0
        if np.isfinite(r["rho_star"]) and r["rho_star"] > 0:
            maxrel = max(maxrel, abs(rs - r["rho_star"]) / r["rho_star"]); n += 1
        if r["beta"] == 1.0:
            ev, V = eigh(K)
            v1 = V[:, 0]; q = v1 @ D @ v1
            eig1 = (q / ev[0]) ** 2 if q < 0 else np.inf
            # each test vector v with v'Dv < 0 gives the necessary condition rho >= (v'Dv/v'Kv)^2
            best5 = max([((V[:, j] @ D @ V[:, j]) / ev[j]) ** 2 for j in range(5) if V[:, j] @ D @ V[:, j] < 0] or [0.0])
            d = np.diag(D); Kinv = np.diag(np.linalg.inv(K))
            coord = max(((-d[i]) * Kinv[i]) ** 2 for i in range(N) if d[i] < 0)
            sq.append((N, s, rs, best5, coord, ev[0] * N ** 2))
    print("B1 closed form rho* = lambda_max(-D;K)^2 versus bisection: max relative difference %.2e over %d instances" % (maxrel, n))
    print("B2 square systems: N seed | rho* | best bottom-5-eigenvector lower bound | coordinate (rank-one) heuristic | lambda_min(K) N^2")
    for t in sq:
        print("   %4d %2d | %.3e | %.3e | %.3e | %.3f" % t)
    for N in (100, 400):
        L = [t for t in sq if t[0] == N]
        print("   N=%d: median log(rho*)/log N = %.2f; median log(bottom-5 bound)/log N = %.2f; median log(coordinate pred)/log N = %.2f"
              % (N, np.median([np.log(t[2]) / np.log(N) for t in L]), np.median([np.log(t[3]) / np.log(N) for t in L]),
                 np.median([np.log(t[4]) / np.log(N) for t in L])))


def part_C():
    rng = np.random.default_rng(3)
    print("C  top-K refinement: N, rho, K, K*max(-g), top-K sum, bound K(sqrt(2log(N/K))+1)+sqrt(2K log N), kappa_N, kappa'")
    for N in (10 ** 4, 10 ** 5, 10 ** 6):
        for c in (2.5, 4.0, 8.0):
            rho = c * np.log(N)
            K = int(np.ceil(N / (4 * rho)))
            g = rng.standard_normal(N)
            x = np.sort(-g)[::-1]
            topk = x[:K].sum(); kmax = K * x[0]
            bound = K * (np.sqrt(2 * np.log(N / K)) + 1) + np.sqrt(2 * K * np.log(N))
            kap = 1 - np.sqrt(2 * np.log(N) / rho)
            kap2 = 1 - topk / (K * np.sqrt(rho))
            print("   %7d %6.1f %6d  %9.1f  %9.1f  %9.1f   %.3f  %.3f" % (N, rho, K, kmax, topk, bound, kap, kap2))


def fp_nodes(A, y, W, cap=3_000_000):
    """Fincke-Pohst, natural (last-to-first) order, radius^2 = W = f(x*)."""
    N = A.shape[1]
    Q, R = np.linalg.qr(A)
    z = Q.T @ y
    r2 = W - (y @ y - z @ z)
    S = np.zeros((1, 0)); PD = np.zeros(1); total = 1
    for k in range(1, N + 1):
        i = N - k
        parts = []
        for val in (-1.0, 1.0):
            Sn = np.hstack([np.full((S.shape[0], 1), val), S])
            parts.append((Sn, PD + (z[i] - Sn @ R[i, i:]) ** 2))
        S = np.vstack([p[0] for p in parts]); PD = np.concatenate([p[1] for p in parts])
        total += S.shape[0]
        keep = PD <= r2 * (1 + 1e-12)
        S = S[keep]; PD = PD[keep]
        if S.shape[0] > cap:
            return total, False
    return total, True


def part_D():
    print("D  Fincke-Pohst vs box static-order B&B, beta = 1, rho = 4 log N, same instances (seeds 0-5)")
    for N in (32, 48, 64):
        rho = 4 * np.log(N)
        fps = []; box = []
        for s in range(6):
            A, y, xs, B, w = instance(N, N, rho, s)
            W = float(w @ w)
            fp, done = fp_nodes(A, y, W)
            r = bnb(B, w, rule="static", max_nodes=300000)
            fps.append(fp); box.append(r["nodes"])
        print("   N=%d: FP nodes %s  geo %.0f | box static %s geo %.0f" % (N, fps, np.exp(np.mean(np.log(fps))), box, np.exp(np.mean(np.log(box)))), flush=True)


def part_E():
    print("E  midpoint clique upper bound: largest n1 with first-moment count >= 1e-3, vs N^(1-c/8)")
    for N in (10 ** 4, 10 ** 5):
        M = N
        for c in (3.0, 4.0, 6.0):
            rho = c * np.log(N)
            last = 0
            for n1 in range(1, 100000):
                n2 = np.arange(0, 400)
                lc = (gammaln(N + 1) - gammaln(n1 + 1) - gammaln(n2 + 1) - gammaln(N - n1 - n2 + 1)
                      - (M / 2) * np.log1p(rho * (n1 + 4 * n2) / (4 * N)))
                if logsumexp(lc) >= np.log(1e-3):
                    last = n1
                elif n1 > 3 * last + 50:
                    break
            print("   N=%d c=%.0f: last n1 = %d, N^(1-c/8) = %.1f, ratio %.1f" % (N, c, last, N ** (1 - c / 8), last / N ** (1 - c / 8)))


def part_F():
    print("F  diagonal-shift reformulation vs box relaxation, beta = 2, N = 200 (relative root gaps (OPT - bound)/OPT, OPT = f(x*))")
    N, M = 200, 400
    for rho in (30.0, 60.0, 130.0, 300.0, 600.0):
        gb = []; gs = []; ex = 0
        for s in range(4):
            A, y, xs, B, w = instance(N, M, rho, s)
            W = float(w @ w)
            R, _, _, _ = box_min(B, w)
            G = A.T @ A
            lmin = np.linalg.eigvalsh(G)[0]
            d = 0.99 * lmin
            Lc = cholesky(G - d * np.eye(N))            # upper triangular, Lc'Lc = G - dI
            b = np.linalg.solve(Lc.T, A.T @ y)
            const = y @ y - b @ b + d * N
            r = lsq_linear(Lc, b, bounds=(-1.0, 1.0), method="bvls", tol=1e-12)
            val = float(np.sum((Lc @ r.x - b) ** 2) + const)   # = min over the box of f + d sum(1 - x_i^2)
            gb.append((W - R) / W); gs.append((W - val) / W)
            zeta = xs * (A.T @ w)
            ex += bool(zeta.min() >= -lmin)                   # Prop. 6.3 exactness with d = lambda_min
        print("   rho=%5.0f: box gap %.3f, shifted gap (d = 0.99 lambda_min) median %.2e max %.2e; exact with d = lambda_min (min zeta >= -lambda_min): %d/4"
              % (rho, np.median(gb), np.median(gs), np.max(gs), ex))


def part_G():
    print("G  proved loss factor kappa_rho = 1 - sqrt(2 log(4(2b-1) rho)/(rho b)) - 1/sqrt(rho b) at N = 1e6 (it does not depend on N)")
    N = 10 ** 6
    for beta in (1.0, 2.0):
        for c in (2.0, 4.0, 8.0, 16.0):
            rho = c * np.log(N) / beta
            k = 1 - np.sqrt(2 * np.log(4 * (2 * beta - 1) * rho) / (rho * beta)) - 1 / np.sqrt(rho * beta)
            print("   beta=%.0f rho beta = %2.0f log N: kappa_rho = %.2f (proved exponent / asymptotic constant = %.1f)" % (beta, c, k, 1 / k))


if __name__ == "__main__":
    parts = sys.argv[1:] or list("ABCDEFG")
    for p in parts:
        globals()["part_" + p]()
