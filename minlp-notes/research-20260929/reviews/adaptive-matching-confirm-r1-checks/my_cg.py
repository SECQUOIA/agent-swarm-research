"""Independent check (confirm round 1) of the c_g brackets quoted in adaptive-matching.md, Sections 8.3-8.4.
F(x) = sum (x_v^2 - 0.1 x_v^4) + b sum_edges x_u x_v on [-1,1]^m, x* = 0, f* = 0.
lower bound 0.9 - |b| rho(A)/2 (rho closed form for paths, numerical for trees);
upper bounds from feasible points: (i) bottom eigenvector of b*A scaled to sup norm 1 (closed form ratio),
(ii) best of 20 random starts of a projected-gradient descent on F(x)/|x|^2 with my own code.
Also: the couplings b that hold the lower bound fixed. Double precision."""
import numpy as np

def adj(fam, m):
    A = np.zeros((m, m))
    if fam == "path":
        i = np.arange(m - 1); A[i, i + 1] = A[i + 1, i] = 1
    else:
        v = np.arange(1, m); A[(v - 1) // 2, v] = A[v, (v - 1) // 2] = 1
    return A

def ratio(x, A, b):
    return (np.sum(x * x - 0.1 * x ** 4) + 0.5 * b * x @ A @ x) / (x @ x)

def grad_ratio(x, A, b):
    n2 = x @ x
    num = np.sum(x * x - 0.1 * x ** 4) + 0.5 * b * x @ A @ x
    gnum = 2 * x - 0.4 * x ** 3 + b * A @ x
    return gnum / n2 - num * 2 * x / n2 ** 2

def pgd(x, A, b, steps=3000, lr=0.05):
    for _ in range(steps):
        x = np.clip(x - lr * grad_ratio(x, A, b), -1, 1)
        if np.linalg.norm(x) < 1e-3:
            return None
    return x

rng = np.random.default_rng(7)
rows = [("path", 0.8, n) for n in (8, 64, 256)] + [("path", 0.88, n) for n in (8, 16, 32, 64)]
rows += [("tree", b, m) for b in (0.55, 0.62) for m in (7, 15, 31, 63, 127)]
rows += [("path", 0.841253, 16), ("path", 0.830691, 32), ("path", 0.827896, 64), ("path", 0.920531, 8)]
rows += [("tree", 0.759342, 7), ("tree", 0.663689, 15), ("tree", 0.595954, 63)]
for fam, b, m in rows:
    A = adj(fam, m)
    ev, V = np.linalg.eigh(A)
    rho = 2 * np.cos(np.pi / (m + 1)) if fam == "path" else ev[-1]
    lo = 0.9 - b * rho / 2
    v = V[:, 0]; v = v / np.abs(v).max()
    up1 = ratio(v, A, b)
    up2 = up1
    for s in range(20 if m <= 64 else 4):
        x0 = v * rng.uniform(0.5, 1) + 0.05 * rng.normal(size=m) if s else v.copy()
        x = pgd(np.clip(x0, -1, 1), A, b, steps=3000 if m <= 64 else 1500)
        if x is not None:
            up2 = min(up2, ratio(x, A, b))
    print("%s b=%.6f m=%3d rho=%.4f  c_g in [%.4f, %.4f]  (eigvec bound %.4f)" % (fam, b, m, rho, lo, up2, up1), flush=True)
print("couplings b = 2(0.9 - target)/rho(A):")
t1 = 0.9 - 0.88 * np.cos(np.pi / 9); t2 = 0.9 - 0.88 * np.cos(np.pi / 17)
rt = np.linalg.eigvalsh(adj("tree", 31))[-1]; t3 = 0.9 - 0.62 * rt / 2
print("  targets %.4f %.4f %.4f" % (t1, t2, t3))
for n in (16, 32, 64):
    print("  path target1 n=%d b=%.6f" % (n, 2 * (0.9 - t1) / (2 * np.cos(np.pi / (n + 1)))))
print("  path target2 n=8 b=%.6f" % (2 * (0.9 - t2) / (2 * np.cos(np.pi / 9))))
for m in (7, 15, 63):
    print("  tree target3 m=%d b=%.6f" % (m, 2 * (0.9 - t3) / np.linalg.eigvalsh(adj("tree", m))[-1]))
