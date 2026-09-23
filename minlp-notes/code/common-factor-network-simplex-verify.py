"""Check the transportation-to-sparse-network-hull map using explicit hull vertices.

The table LP and hull-vertex LP are assembled separately.  This checks Lemma 1
on random nonnegative integer margin data; it does not implement or test the
external De Loera--Onn universality construction or enumerate ambient facets.
"""

import numpy as np
from scipy.optimize import linprog


def check(seed):
    rng = np.random.default_rng(seed)
    r, c = map(int, rng.integers(2, 6, size=2))
    table = rng.integers(0, 6, size=(r, c, 3))
    # Keep layer totals positive, also exercising some zero margins elsewhere.
    table[0, 0, :] += 1
    u = table.sum(axis=2)
    v = table.sum(axis=1)
    w = table.sum(axis=0)
    totals = table.sum(axis=(0, 1))
    big_b = int(totals.sum())
    chosen = rng.choice(r * c, size=int(rng.integers(1, r * c + 1)), replace=False)
    pairs = [divmod(int(k), c) for k in chosen]
    costs = rng.normal(size=len(pairs))

    # LP 1: table entries and three sets of prescribed line sums.
    rows, rhs = [], []
    for i in range(r):
        for j in range(c):
            row = np.zeros((r, c, 3))
            row[i, j, :] = 1
            rows.append(row.ravel())
            rhs.append(u[i, j])
    for i in range(r):
        for k in range(3):
            row = np.zeros((r, c, 3))
            row[i, :, k] = 1
            rows.append(row.ravel())
            rhs.append(v[i, k])
    for j in range(c):
        for k in range(3):
            row = np.zeros((r, c, 3))
            row[:, j, k] = 1
            rows.append(row.ravel())
            rhs.append(w[j, k])
    objective = np.zeros((r, c, 3))
    for (i, j), cost in zip(pairs, costs):
        objective[i, j, 0] = cost

    # LP 2: explicitly enumerate graph vertices: each path and simplex vertex.
    arcs = [("left", i) for i in range(r)]
    arcs += [("middle", i, j) for i in range(r) for j in range(c)]
    arcs += [("right", j) for j in range(c)]
    boundary = list(range(r)) + list(range(r + r * c, len(arcs)))
    observations = [(e, k) for e in boundary for k in range(2)]
    observations += [(r + i * c + j, 0) for i, j in pairs]
    vertices = []
    for i in range(r):
        for j in range(c):
            path = np.zeros(len(arcs))
            path[[i, r + i * c + j, r + r * c + j]] = 1
            for y in [np.array([1., 0.]), np.array([0., 1.]), np.array([0., 0.])]:
                products = [path[e] * y[k] for e, k in observations]
                vertices.append(np.r_[path, y, products])
    vertices = np.array(vertices).T
    fixed_x = np.r_[v.sum(axis=1), u.ravel(), w.sum(axis=1)] / big_b
    fixed_y = totals[:2] / big_b
    fixed_products = []
    for e, k in observations[:2 * len(boundary)]:
        if e < r:
            fixed_products.append(v[e, k] / big_b)
        else:
            fixed_products.append(w[e - r - r * c, k] / big_b)
    fixed = np.r_[fixed_x, fixed_y, fixed_products]
    a_hull = np.vstack([np.ones(vertices.shape[1]), vertices[:len(fixed)]])
    b_hull = np.r_[1., fixed]
    c_hull = costs @ vertices[len(fixed):]

    for sign in (-1, 1):
        direct = linprog(sign * objective.ravel(), A_eq=rows, b_eq=rhs,
                         bounds=(0, None), method="highs")
        hull = linprog(sign * c_hull, A_eq=a_hull, b_eq=b_hull,
                       bounds=(0, None), method="highs")
        assert direct.success and hull.success, (seed, direct.message, hull.message)
        assert abs(direct.fun / big_b - hull.fun) < 1e-8, (
            seed, direct.fun / big_b, hull.fun)


if __name__ == "__main__":
    for seed in range(150):
        check(seed)
    print("Passed 300 projected support comparisons over 150 random tables: "
          "direct transportation LP versus explicit normalized sparse hull vertices.")
