"""Item (4): size of the Proposition 5.3 fraction frac(A) = (Lmax - Lmin)/(lam + Lmax), Lmax/min = extreme
eigenvalues of X_A'X_A, for Gaussian X.

 - fixed A (first s columns, independent of X): claimed ~ 4 sqrt(s/n);
 - data-dependent A ("arrow": a column j0 plus the s-1 columns most correlated with it): a lower bound
   on the worst case over |A| = s. Heuristic size 2 sqrt(2 (s-1) log(p/s)/n);
 - the note's union-bound upper bound 4 (sqrt s + sqrt(2 s log(ep/s)))/sqrt n.
The claim to check: the worst case is of order sqrt(s log(ep/s)/n) (not sqrt(s/n)), and it is Theta(1) at
s ~ k, n ~ 2 k log p.
usage: python3 rc_frac.py > rc_frac.log
"""
from rc_common import np


def frac(XA, lam):
    ev = np.linalg.eigvalsh(XA.T @ XA)
    return (ev[-1] - ev[0]) / (lam + ev[-1])


def arrow(X, s, j0=0):
    c = X.T @ X[:, j0]
    c[j0] = 0
    top = np.argsort(-np.abs(c))[:s - 1]
    return np.concatenate([[j0], top])


def run(n, p, s, reps, rng, lam=0.0):
    fx, ar = [], []
    for _ in range(reps):
        X = rng.standard_normal((n, p))
        fx.append(frac(X[:, :s], lam))
        ar.append(max(frac(X[:, arrow(X, s, j0)], lam) for j0 in range(3)))
    ub = 4 * (np.sqrt(s) + np.sqrt(2 * s * np.log(np.e * p / s))) / np.sqrt(n)
    print(f"n={n:5d} p={p:6d} s={s:3d}: fixed A {np.mean(fx):.3f} (4 sqrt(s/n) = {4 * np.sqrt(s / n):.3f}); "
          f"arrow A {np.mean(ar):.3f} (2 sqrt(2(s-1)log(p/s)/n) = {2 * np.sqrt(2 * (s - 1) * np.log(p / s) / n):.3f}); "
          f"note's union bound {ub:.3f}; sqrt(s log(ep/s)/n) = {np.sqrt(s * np.log(np.e * p / s) / n):.3f}")


def main():
    rng = np.random.default_rng(7)
    print("A. s log(ep/s) << n: fixed-A vs data-dependent A")
    for s in (2, 5, 10, 20):
        run(2000, 10000, s, 3, rng)
    print("B. threshold scale s = k, n = round(2 k log p), p = 20000 (lam = 0)")
    for k in (5, 10, 20, 40):
        n = int(round(2 * k * np.log(20000)))
        run(n, 20000, k, 3, rng)


if __name__ == "__main__":
    main()
