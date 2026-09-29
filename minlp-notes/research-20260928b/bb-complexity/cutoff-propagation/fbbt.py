"""Interval FBBT (HC4-style forward/backward propagation) on a factorable DAG.

Floating-point illustration only: no outward rounding.

A DAG is a list of nodes in topological order (children before parents).
Node kinds:
  ('var', i)                      original variable x_i
  ('const', v)
  ('lin', [c1..ck], [a1..ak], b)  a1*w_c1 + ... + ak*w_ck + b   (n-ary sum)
  ('mul', c1, c2)                 w_c1 * w_c2
  ('pow', c, k)                   w_c ** k, integer k >= 2
The last node is the root f.

hc4(dag, box, cutoff, max_rounds) runs rounds of
  forward pass (every node intersected with its interval image),
  root := root ∩ (-inf, cutoff],
  backward pass (every node revises its children with the exact
  projection of its own elementary constraint),
until nothing changes (relative 1e-15) or max_rounds is reached.
Returns (status, var_box, rounds) with status in {'empty', 'fixed', 'limit'}.
Each revise operator is the hull of the projection of one elementary
constraint (exact in real arithmetic), so the run contains the greatest
hull-consistent box (Lemma 1.1 of the note).
"""
import math

INF = math.inf


class Empty(Exception):
    pass


def imul(a, b):
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    p = [0.0 if math.isnan(x) else x for x in p]
    return (min(p), max(p))


def ipow(a, k):
    lo, hi = a
    if k % 2 == 1:
        return (lo ** k, hi ** k)
    if lo >= 0:
        return (lo ** k, hi ** k)
    if hi <= 0:
        return (hi ** k, lo ** k)
    return (0.0, max(-lo, hi) ** k)


def meet(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    if lo > hi:
        raise Empty
    return (lo, hi)


def div_hull(n, b, a):
    """Hull of {x in a : x*y in n for some y in b} (projection of x*y=w)."""
    bl, bh = b
    nl, nh = n
    if bl > 0 or bh < 0:
        q = [nl / bl, nl / bh, nh / bl, nh / bh]
        return meet(a, (min(q), max(q)))
    # 0 in b
    if nl <= 0 <= nh:
        return a  # x arbitrary (take y = 0)
    parts = []
    if nl > 0:
        if bh > 0:
            parts.append((nl / bh, INF))
        if bl < 0:
            parts.append((-INF, nl / bl))
    else:  # nh < 0
        if bh > 0:
            parts.append((-INF, nh / bh))
        if bl < 0:
            parts.append((nh / bl, INF))
    pieces = []
    for p in parts:
        lo, hi = max(a[0], p[0]), min(a[1], p[1])
        if lo <= hi:
            pieces.append((lo, hi))
    if not pieces:
        raise Empty
    return (min(p[0] for p in pieces), max(p[1] for p in pieces))


def pow_inv(n, k, a):
    """Hull of {x in a : x**k in n}."""
    nl, nh = n
    if k % 2 == 1:
        def root(v):
            return math.copysign(abs(v) ** (1.0 / k), v)
        return meet(a, (root(nl), root(nh)))
    if nh < 0:
        raise Empty
    r = nh ** (1.0 / k)
    s = max(nl, 0.0) ** (1.0 / k)
    pieces = []
    for p in ((-r, -s), (s, r)):
        lo, hi = max(a[0], p[0]), min(a[1], p[1])
        if lo <= hi:
            pieces.append((lo, hi))
    if not pieces:
        raise Empty
    return (min(p[0] for p in pieces), max(p[1] for p in pieces))


def forward(node, iv):
    kind = node[0]
    if kind == 'var':
        return None
    if kind == 'const':
        return (node[1], node[1])
    if kind == 'lin':
        _, ch, co, b = node
        lo = hi = b
        for c, a in zip(ch, co):
            x = iv[c]
            if a >= 0:
                lo += a * x[0]; hi += a * x[1]
            else:
                lo += a * x[1]; hi += a * x[0]
        return (lo, hi)
    if kind == 'mul':
        return imul(iv[node[1]], iv[node[2]])
    if kind == 'pow':
        return ipow(iv[node[1]], node[2])
    raise ValueError(kind)


def backward(node, k, iv):
    kind = node[0]
    n = iv[k]
    if kind in ('var', 'const'):
        return
    if kind == 'lin':
        _, ch, co, b = node
        terms = []
        for c, a in zip(ch, co):
            x = iv[c]
            terms.append((a * x[0], a * x[1]) if a >= 0 else (a * x[1], a * x[0]))
        slo = sum(t[0] for t in terms)
        shi = sum(t[1] for t in terms)
        for idx, (c, a) in enumerate(zip(ch, co)):
            t = terms[idx]
            rest_lo, rest_hi = slo - t[0], shi - t[1]
            # a*x in [n_lo - b - rest_hi, n_hi - b - rest_lo]
            lo, hi = n[0] - b - rest_hi, n[1] - b - rest_lo
            if a > 0:
                cand = (lo / a, hi / a)
            else:
                cand = (hi / a, lo / a)
            iv[c] = meet(iv[c], cand)
        return
    if kind == 'mul':
        a, c2 = node[1], node[2]
        if a == c2:
            iv[a] = pow_inv(n, 2, iv[a])
            return
        iv[a] = div_hull(n, iv[c2], iv[a])
        iv[c2] = div_hull(n, iv[a], iv[c2])
        return
    if kind == 'pow':
        iv[node[1]] = pow_inv(n, node[2], iv[node[1]])
        return
    raise ValueError(kind)


def init_intervals(dag, box):
    iv = []
    for node in dag:
        if node[0] == 'var':
            iv.append(tuple(box[node[1]]))
        else:
            iv.append(forward(node, iv))
    return iv


def var_box(dag, iv, nvar):
    out = [None] * nvar
    for k, node in enumerate(dag):
        if node[0] == 'var':
            out[node[1]] = iv[k]
    return out


def hc4(dag, box, cutoff, max_rounds=100000, rtol=1e-15, start=None, lifted=False):
    """start: optional lifted box to start from (e.g. inherited bounds);
    lifted=True additionally returns the final lifted box."""
    nvar = len(box)
    try:
        if start is None:
            iv = init_intervals(dag, box)
        else:
            iv = [meet(a, b) for a, b in zip(start, init_intervals(dag, box))]
    except Empty:
        return ('empty', None, 0, None) if lifted else ('empty', None, 0)
    root = len(dag) - 1
    rounds = 0
    while rounds < max_rounds:
        rounds += 1
        old = list(iv)
        try:
            for k, node in enumerate(dag):
                fw = forward(node, iv)
                if fw is not None:
                    iv[k] = meet(iv[k], fw)
            iv[root] = meet(iv[root], (-INF, cutoff))
            for k in range(root, -1, -1):
                backward(dag[k], k, iv)
        except Empty:
            return ('empty', None, rounds, None) if lifted else ('empty', None, rounds)
        changed = False
        for a, b in zip(old, iv):
            if a != b:
                scale = 1.0 + max(abs(a[0]), abs(a[1]))
                if abs(a[0] - b[0]) > rtol * scale or abs(a[1] - b[1]) > rtol * scale:
                    changed = True
                    break
        if not changed:
            out = ('fixed', var_box(dag, iv, nvar), rounds)
            return out + (list(iv),) if lifted else out
    out = ('limit', var_box(dag, iv, nvar), rounds)
    return out + (list(iv),) if lifted else out


def forward_lb(dag, box):
    """Natural interval extension lower bound of the root."""
    return init_intervals(dag, box)[-1][0]


def evaluate(dag, x):
    val = []
    for node in dag:
        kind = node[0]
        if kind == 'var':
            val.append(x[node[1]])
        elif kind == 'const':
            val.append(node[1])
        elif kind == 'lin':
            val.append(node[3] + sum(a * val[c] for c, a in zip(node[1], node[2])))
        elif kind == 'mul':
            val.append(val[node[1]] * val[node[2]])
        elif kind == 'pow':
            val.append(val[node[1]] ** node[2])
    return val[-1]


class Builder:
    """Small helper to build DAGs; identical subexpressions are not merged
    unless the caller reuses the returned node index."""

    def __init__(self, nvar):
        self.nodes = [('var', i) for i in range(nvar)]

    def add(self, node):
        self.nodes.append(node)
        return len(self.nodes) - 1

    def lin(self, children, coeffs, const=0.0):
        return self.add(('lin', list(children), [float(c) for c in coeffs], float(const)))

    def mul(self, a, b):
        return self.add(('mul', a, b))

    def pow(self, a, k):
        return self.add(('pow', a, int(k)))

    def monomial(self, exps):
        """Product of powers of variables, e.g. {0:3, 1:1} -> x0^3 * x1 (SUE term)."""
        factors = []
        for i, e in sorted(exps.items()):
            if e == 0:
                continue
            factors.append(i if e == 1 else self.pow(i, e))
        node = factors[0]
        for f in factors[1:]:
            node = self.mul(node, f)
        return node

    def poly(self, terms, const=0.0):
        """Flat sum of monomial terms: terms = [(coef, {var: exp})]."""
        ch, co = [], []
        for coef, exps in terms:
            if coef == 0:
                continue
            ch.append(self.monomial(exps))
            co.append(coef)
        return self.lin(ch, co, const)

    def dag(self):
        return list(self.nodes)
