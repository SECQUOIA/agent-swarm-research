"""Exact checks for the endpoint full-set theorem and its face-pattern CSP.

F(x) = 1/2 x^T H x + b^T x + c on a mixed box, H_ii <= 0 on every coordinate
with more than two feasible values.  Checks, with fractions.Fraction:
  * the Bellman residual identity on random rational points of the hull;
  * the characterization of all optimizers on a fine rational test set;
  * the face-pattern CSP: admissible patterns <-> optimal relatively open faces;
  * tree DP for dist(y,S)^2, dimension, and uniqueness vs. brute force over
    all 3^n patterns.
Also checks the two-label integer preprocessing (positive H_ii allowed when
the integer domain is {l, l+1}).
Run: python3 -B check_endpoint.py
"""
import random
from fractions import Fraction as Fr
from itertools import product

random.seed(20261003)


def rand_instance(n, bags_kind):
    # tree decomposition: list of bags and parent pointers
    if bags_kind == "path":
        bags = [tuple(range(i, min(i + 3, n))) for i in range(max(1, n - 2))]
        parent = [None] + list(range(len(bags) - 1))
    else:  # branching: root bag {0,1,2}, children {1,2,3}, {0,2,4}, {2,4,5}
        bags = [(0, 1, 2), (1, 2, 3), (0, 2, 4), (2, 4, 5)][: max(1, n - 2)]
        parent = [None, 0, 0, 2][: len(bags)]
    # domains
    dom = []
    for i in range(n):
        kind = random.choice(["C", "C", "Z", "Z2"])
        lo = Fr(random.randint(-2, 1), random.choice([1, 2]))
        if kind == "C":
            dom.append(("C", lo, lo + Fr(random.randint(1, 4), random.choice([1, 2, 3]))))
        elif kind == "Z":
            lo = Fr(random.randint(-2, 1))
            dom.append(("Z", lo, lo + random.randint(2, 4)))
        else:
            lo = Fr(random.randint(-2, 1))
            dom.append(("Z", lo, lo + 1))
    H = [[Fr(0)] * n for _ in range(n)]
    for B in bags:
        for i in B:
            for j in B:
                if i < j and random.random() < 0.6:
                    v = Fr(random.choice([-2, -1, 0, 1, 2]))
                    H[i][j] = H[j][i] = v
    for i in range(n):
        two = dom[i][0] == "Z" and dom[i][2] - dom[i][1] == 1
        H[i][i] = Fr(random.choice([1, 2, 0, -1])) if two else Fr(random.choice([0, 0, -1, -2]))
    b = [Fr(random.choice([-2, -1, 0, 1, 2]), random.choice([1, 2])) for _ in range(n)]
    c = Fr(0)
    return bags, parent, dom, H, b, c


def F(H, b, c, x):
    n = len(x)
    return sum(H[i][j] * x[i] * x[j] for i in range(n) for j in range(n)) / 2 + sum(b[i] * x[i] for i in range(n)) + c


def preprocess_two_label(dom, H, b, c):
    """Replace H_ii x_i^2/2 by its chord on {l,l+1}; agrees on X."""
    n = len(dom)
    H = [row[:] for row in H]
    b = b[:]
    for i in range(n):
        kind, lo, hi = dom[i]
        if kind == "Z" and hi - lo == 1 and H[i][i] != 0:
            # x^2 = (lo+hi) x - lo*hi on {lo,hi}
            b[i] += H[i][i] / 2 * (lo + hi)
            c -= H[i][i] / 2 * lo * hi
            H[i][i] = Fr(0)
    return H, b, c


def assign_factors(n, bags, H, b, c):
    """Assign monomials to the first bag containing their scope."""
    owner = {}
    for i in range(n):
        for j in range(i, n):
            if H[i][j] != 0:
                t = next(t for t, B in enumerate(bags) if i in B and j in B)
                owner.setdefault(t, []).append(("q", i, j))
        if b[i] != 0:
            t = next(t for t, B in enumerate(bags) if i in B)
            owner.setdefault(t, []).append(("l", i))
    owner.setdefault(0, []).append(("c",))
    return owner


def phi(t, owner, H, b, c, xd):
    s = Fr(0)
    for term in owner.get(t, []):
        if term[0] == "q":
            _, i, j = term
            s += (H[i][j] if i != j else H[i][i] / 2) * xd[i] * xd[j]
        elif term[0] == "l":
            s += b[term[1]] * xd[term[1]]
        else:
            s += c
    return s


def endpoint_dp(n, bags, parent, dom, owner, H, b, c):
    children = {t: [u for u in range(len(bags)) if parent[u] == t] for t in range(len(bags))}
    sep = {t: (tuple(sorted(set(bags[t]) & set(bags[parent[t]]))) if parent[t] is not None else ()) for t in range(len(bags))}
    order = []

    def post(t):
        for u in children[t]:
            post(u)
        order.append(t)
    root = parent.index(None)
    post(root)
    M = {}
    r = {}
    for t in order:
        B = bags[t]
        table = {}
        for labs in product(*[(dom[i][1], dom[i][2]) for i in B]):
            xd = dict(zip(B, labs))
            val = phi(t, owner, H, b, c, xd) + sum(M[u][tuple(xd[i] for i in sep[u])] for u in children[t])
            table[labs] = (xd, val)
        msg = {}
        for labs, (xd, val) in table.items():
            key = tuple(xd[i] for i in sep[t])
            msg[key] = min(msg.get(key, val), val)
        M[t] = msg
        r[t] = {labs: val - msg[tuple(xd[i] for i in sep[t])] for labs, (xd, val) in table.items()}
    fstar = M[root][()]
    return fstar, r, sep, children, root


def weights(B, dom, x, labs):
    w = Fr(1)
    for i, v in zip(B, labs):
        lo, hi = dom[i][1], dom[i][2]
        w *= (hi - x[i]) / (hi - lo) if v == lo else (x[i] - lo) / (hi - lo)
    return w


def identity_rhs(n, bags, dom, r, H, x):
    s = Fr(0)
    for t, B in enumerate(bags):
        for labs, val in r[t].items():
            s += val * weights(B, dom, x, labs)
    for i in range(n):
        lo, hi = dom[i][1], dom[i][2]
        s -= H[i][i] / 2 * (x[i] - lo) * (hi - x[i])
    return s


def pattern(dom, x):
    p = []
    for i, xi in enumerate(x):
        p.append("l" if xi == dom[i][1] else ("u" if xi == dom[i][2] else "*"))
    return tuple(p)


def cube(B, dom, pat):
    opts = []
    for i, s in zip(B, pat):
        lo, hi = dom[i][1], dom[i][2]
        opts.append((lo,) if s == "l" else ((hi,) if s == "u" else (lo, hi)))
    return list(product(*opts))


def admissible_local(t, B, dom, r, pat_B):
    return all(r[t][labs] == 0 for labs in cube(B, dom, pat_B))


def allowed_labels(i, dom, H):
    kind, lo, hi = dom[i]
    labs = ["l", "u"]
    star_ok = (kind == "C" or hi - lo >= 2) and H[i][i] == 0
    if star_ok:
        labs.append("*")
    return labs


def unary_cost(i, dom, s, y):
    kind, lo, hi = dom[i]
    if s == "l":
        return (y[i] - lo) ** 2
    if s == "u":
        return (y[i] - hi) ** 2
    if kind == "C":
        z = min(max(y[i], lo), hi)
        return (y[i] - z) ** 2
    # integer: nearest feasible label (interior labels or endpoints, closed face)
    cands = [Fr(k) for k in range(int(lo), int(hi) + 1)]
    return min((y[i] - z) ** 2 for z in cands)


def tree_csp_min(n, bags, parent, sep, children, root, dom, r, H, cost):
    """min over admissible patterns of sum_i cost(i, s_i); each variable cost counted once
    (in the highest bag containing it, i.e. where it is eliminated)."""
    # variable i is 'owned' by the bag t where i in B_t and i not in sep[t]
    own = {}
    for t, B in enumerate(bags):
        for i in B:
            if i not in sep[t]:
                own[i] = t
    msgs = {}

    def solve(t):
        for u in children[t]:
            solve(u)
        B = bags[t]
        best = {}
        for pat in product(*[allowed_labels(i, dom, H) for i in B]):
            if not admissible_local(t, B, dom, r, pat):
                continue
            d = dict(zip(B, pat))
            val = sum(cost(i, d[i]) for i in B if own[i] == t)
            ok = True
            for u in children[t]:
                key = tuple(d[i] for i in sep[u])
                if key not in msgs[u]:
                    ok = False
                    break
                val += msgs[u][key]
            if not ok:
                continue
            key = tuple(d[i] for i in sep[t])
            if key not in best or val < best[key]:
                best[key] = val
        msgs[t] = best
    solve(root)
    return msgs[root].get(())


STATS = []


def main():
    n_inst = 0
    n_id = 0
    n_char = 0
    n_proj = 0
    for trial in range(60):
        n = random.choice([4, 5, 6])
        kind = random.choice(["path", "branch"]) if n == 6 else "path"
        bags, parent, dom, H0, b0, c0 = rand_instance(n, kind)
        # sanity: every coordinate covered; running intersection holds by construction
        assert set().union(*map(set, bags)) == set(range(n))
        H, b, c = preprocess_two_label(dom, H0, b0, c0)
        for i in range(n):
            assert H[i][i] <= 0
        owner = assign_factors(n, bags, H, b, c)
        fstar, r, sep, children, root = endpoint_dp(n, bags, parent, dom, owner, H, b, c)
        for t in r:
            assert all(v >= 0 for v in r[t].values())
        # identity at random hull points
        for _ in range(25):
            x = [dom[i][1] + (dom[i][2] - dom[i][1]) * Fr(random.randint(0, 12), 12) for i in range(n)]
            assert F(H, b, c, x) - fstar == identity_rhs(n, bags, dom, r, H, x)
            n_id += 1
        # preprocessing agrees with the original objective on X
        test_pts = []
        for i in range(n):
            kind_i, lo, hi = dom[i]
            if kind_i == "C":
                test_pts.append([lo + (hi - lo) * Fr(k, 4) for k in range(5)])
            else:
                test_pts.append([Fr(k) for k in range(int(lo), int(hi) + 1)])
        Fvals = {}
        for x in product(*test_pts):
            x = list(x)
            assert F(H, b, c, x) == F(H0, b0, c0, x)
            Fvals[tuple(x)] = F(H, b, c, x)
        assert min(Fvals.values()) >= fstar
        # attainment at an endpoint
        assert any(v == fstar for x, v in Fvals.items() if all(xi in (dom[i][1], dom[i][2]) for i, xi in enumerate(x)))
        # characterization
        for x, v in Fvals.items():
            pat = pattern(dom, x)
            cond = all(not (H[i][i] < 0 and pat[i] == "*") for i in range(n))
            cond = cond and all(admissible_local(t, B, dom, r, tuple(pat[i] for i in B)) for t, B in enumerate(bags))
            assert (v == fstar) == cond, (x, v, fstar)
            n_char += 1
        # brute force over patterns: admissible = all faces in S
        adm = []
        for pat in product(*[allowed_labels(i, dom, H) for i in range(n)]):
            if all(admissible_local(t, B, dom, r, tuple(pat[i] for i in B)) for t, B in enumerate(bags)):
                adm.append(pat)
        # downward closure
        for pat in adm:
            for i in range(n):
                if pat[i] == "*":
                    for e in "lu":
                        q = list(pat)
                        q[i] = e
                        assert tuple(q) in adm
        # projection / dimension / uniqueness via tree DP vs brute force
        for _ in range(5):
            y = [dom[i][1] + (dom[i][2] - dom[i][1]) * Fr(random.randint(-3, 15), 12) for i in range(n)]
            brute = min(sum(unary_cost(i, dom, pat[i], y) for i in range(n)) for pat in adm)
            dp = tree_csp_min(n, bags, parent, sep, children, root, dom, r, H, lambda i, s: unary_cost(i, dom, s, y))
            assert dp == brute
            # grid points of S give an upper bound
            ub = min(sum((y[i] - x[i]) ** 2 for i in range(n)) for x, v in Fvals.items() if v == fstar)
            assert brute <= ub
            n_proj += 1
        dim_brute = max(sum(1 for i in range(n) if pat[i] == "*" and dom[i][0] == "C") for pat in adm)
        dim_dp = -tree_csp_min(n, bags, parent, sep, children, root, dom, r, H,
                               lambda i, s: Fr(-1) if (s == "*" and dom[i][0] == "C") else Fr(0))
        assert dim_dp == dim_brute
        # number of optimal points when all coords are integer: count via patterns
        n_inst += 1
        nonuniq = sum(1 for v in Fvals.values() if v == fstar)
        STATS.append((nonuniq, dim_brute, len(adm)))
    print("instances with >1 optimal test point:", sum(1 for s in STATS if s[0] > 1), "; with positive-dimensional S:", sum(1 for s in STATS if s[1] > 0), "; max admissible patterns:", max(s[2] for s in STATS))
    print(f"endpoint checks passed: {n_inst} instances, {n_id} identities, "
          f"{n_char} characterization points, {n_proj} projection DPs")


if __name__ == "__main__":
    main()
