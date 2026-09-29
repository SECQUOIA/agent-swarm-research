"""Independent interval propagator for the recheck of the revised cutoff note.

Written from scratch for this recheck; it does not import the author's or the
first reviewer's code. Floating point, no outward rounding: illustrations only.

A DAG is a list of nodes in topological order (children first, root last):
  ('var', i)
  ('const', v)
  ('sum', [children], [coefs], b)      b + sum coef * child   (no repeated child)
  ('mul', a, b)                        a * b                  (a != b)
  ('pow', a, k)                        a ** k, integer k >= 2

Steps (each is a "run step" of Section 1 of the note):
  fwd k  : W_k := W_k ∩ image(children)
  bwd k  : every child := hull of the projection of E_k ∩ Z onto that child
  cut    : root := root ∩ (-inf, c]
Extra constraint roots (for the interleaved-constraint test) are given as a
list of node indices whose interval is capped at 0 by the cut step.
"""
import math
import random

INF = math.inf


class Empty(Exception):
    pass


def isect(a, b):
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    if lo > hi:
        raise Empty
    return (lo, hi)


# ---------------------------------------------------------------- images
def img_mul(A, B):
    p = (A[0] * B[0], A[0] * B[1], A[1] * B[0], A[1] * B[1])
    return (min(p), max(p))


def img_pow(A, k):
    lo, hi = A
    if k % 2 == 1 or lo >= 0:
        return (lo ** k, hi ** k)
    if hi <= 0:
        return (hi ** k, lo ** k)
    return (0.0, max(-lo, hi) ** k)


def image(node, iv):
    kind = node[0]
    if kind == 'const':
        return (node[1], node[1])
    if kind == 'sum':
        lo = hi = node[3]
        for c, a in zip(node[1], node[2]):
            x = iv[c]
            if a >= 0:
                lo += a * x[0]
                hi += a * x[1]
            else:
                lo += a * x[1]
                hi += a * x[0]
        return (lo, hi)
    if kind == 'mul':
        return img_mul(iv[node[1]], iv[node[2]])
    if kind == 'pow':
        return img_pow(iv[node[1]], node[2])
    raise ValueError(kind)


# ------------------------------------------------------------ projections
def mul_pre(W, B, A):
    """Hull of {a in A : a*b in W for some b in B}."""
    wl, wu = W
    bl, bu = B
    if bl > 0 or bu < 0:
        q = (wl / bl, wl / bu, wu / bl, wu / bu)
        return isect(A, (min(q), max(q)))
    if wl <= 0 <= wu:
        return A
    pieces = []
    if wl > 0:
        if bu > 0:
            pieces.append((wl / bu, INF))
        if bl < 0:
            pieces.append((-INF, wl / bl))
    else:
        if bu > 0:
            pieces.append((-INF, wu / bu))
        if bl < 0:
            pieces.append((wu / bl, INF))
    out = []
    for p in pieces:
        lo, hi = max(A[0], p[0]), min(A[1], p[1])
        if lo <= hi:
            out.append((lo, hi))
    if not out:
        raise Empty
    return (min(p[0] for p in out), max(p[1] for p in out))


def pow_pre(W, k, A):
    """Hull of {a in A : a**k in W}."""
    wl, wu = W
    if k % 2 == 1:
        def rt(v):
            return math.copysign(abs(v) ** (1.0 / k), v)
        return isect(A, (rt(wl), rt(wu)))
    if wu < 0:
        raise Empty
    if k == 2:
        R, s = math.sqrt(wu), math.sqrt(max(wl, 0.0))
    else:
        R, s = wu ** (1.0 / k), max(wl, 0.0) ** (1.0 / k)
    out = []
    for p in ((-R, -s), (s, R)):
        lo, hi = max(A[0], p[0]), min(A[1], p[1])
        if lo <= hi:
            out.append((lo, hi))
    if not out:
        raise Empty
    return (min(p[0] for p in out), max(p[1] for p in out))


def backward(dag, k, iv):
    node = dag[k]
    kind = node[0]
    W = iv[k]
    if kind == 'sum':
        ch, co, b = node[1], node[2], node[3]
        terms = [(a * iv[c][0], a * iv[c][1]) if a >= 0 else (a * iv[c][1], a * iv[c][0])
                 for c, a in zip(ch, co)]
        new = []
        for i, (c, a) in enumerate(zip(ch, co)):
            rlo = sum(t[0] for j, t in enumerate(terms) if j != i)
            rhi = sum(t[1] for j, t in enumerate(terms) if j != i)
            lo, hi = W[0] - b - rhi, W[1] - b - rlo
            new.append((c, (lo / a, hi / a) if a > 0 else (hi / a, lo / a)))
        for c, cand in new:           # simultaneous update from the pre-step box
            iv[c] = isect(iv[c], cand)
    elif kind == 'mul':
        a, b = node[1], node[2]
        na = mul_pre(W, iv[b], iv[a])
        nb = mul_pre(W, iv[a], iv[b])
        iv[a], iv[b] = na, nb
    elif kind == 'pow':
        iv[node[1]] = pow_pre(W, node[2], iv[node[1]])


def forward_step(dag, k, iv):
    if dag[k][0] != 'var':
        iv[k] = isect(iv[k], image(dag[k], iv))


def cut_step(dag, iv, c, cons=()):
    r = len(dag) - 1
    iv[r] = isect(iv[r], (-INF, c))
    for g in cons:
        iv[g] = isect(iv[g], (-INF, 0.0))


# ---------------------------------------------------------------- boxes
def z0(dag, box):
    """Forward (natural interval extension) lifted box of an x-box."""
    iv = []
    for node in dag:
        iv.append(tuple(box[node[1]]) if node[0] == 'var' else image(node, iv))
    return iv


def xbox(dag, iv):
    n = 1 + max(nd[1] for nd in dag if nd[0] == 'var')
    out = [None] * n
    for k, nd in enumerate(dag):
        if nd[0] == 'var':
            out[nd[1]] = iv[k]
    return out


def meet_boxes(Y, Z):
    return [isect(a, b) for a, b in zip(Y, Z)]


def changed(old, new, rtol):
    for a, b in zip(old, new):
        s = rtol * (1.0 + max(abs(a[0]), abs(a[1])))
        if abs(a[0] - b[0]) > s or abs(a[1] - b[1]) > s:
            return True
    return False


def run(dag, start, c, rounds, schedule='hc4', cons=(), rtol=0.0, rng=None):
    """Run from the lifted box `start`. Returns (status, lifted box, rounds).
    status: 'empty', 'fixed' (no change beyond rtol in a full round), 'limit'."""
    iv = list(start)
    ops = [k for k, nd in enumerate(dag) if nd[0] != 'var']
    for r in range(1, rounds + 1):
        old = list(iv)
        try:
            if schedule == 'hc4':
                for k in ops:
                    forward_step(dag, k, iv)
                cut_step(dag, iv, c, cons)
                for k in reversed(ops):
                    backward(dag, k, iv)
            else:  # random order of partial steps, each step once per round (fair)
                steps = [('f', k) for k in ops] + [('b', k) for k in ops] + [('c', None)]
                rng.shuffle(steps)
                for s, k in steps:
                    if s == 'f':
                        forward_step(dag, k, iv)
                    elif s == 'b':
                        backward(dag, k, iv)
                    else:
                        cut_step(dag, iv, c, cons)
        except Empty:
            return 'empty', None, r
        if not changed(old, iv, rtol):
            return 'fixed', iv, r
    return 'limit', iv, rounds


def fixpoint(dag, box, c, max_rounds=100000, cons=(), start=None, rtol=1e-14,
             schedule='hc4', rng=None):
    """Approximate Z*(box, c) by a long run from Z0(box) (∩ start)."""
    try:
        Z = z0(dag, box)
        if start is not None:
            Z = meet_boxes(start, Z)
    except Empty:
        return 'empty', None, 0
    return run(dag, Z, c, max_rounds, schedule=schedule, cons=cons, rtol=rtol, rng=rng)


def inside(A, B, tol=1e-9):
    return all(a[0] >= b[0] - tol * (1 + abs(b[0])) and a[1] <= b[1] + tol * (1 + abs(b[1]))
               for a, b in zip(A, B))


def evaluate(dag, x):
    v = []
    for nd in dag:
        k = nd[0]
        if k == 'var':
            v.append(x[nd[1]])
        elif k == 'const':
            v.append(nd[1])
        elif k == 'sum':
            v.append(nd[3] + sum(a * v[c] for c, a in zip(nd[1], nd[2])))
        elif k == 'mul':
            v.append(v[nd[1]] * v[nd[2]])
        else:
            v.append(v[nd[1]] ** nd[2])
    return v


# ------------------------------------------------------------ builders
class DAG:
    def __init__(self, n):
        self.nodes = [('var', i) for i in range(n)]

    def add(self, nd):
        self.nodes.append(nd)
        return len(self.nodes) - 1

    def sum(self, ch, co, b=0.0):
        assert len(set(ch)) == len(ch) and all(a != 0 for a in co)
        return self.add(('sum', list(ch), [float(a) for a in co], float(b)))

    def mul(self, a, b):
        assert a != b
        return self.add(('mul', a, b))

    def pow(self, a, k):
        return self.add(('pow', a, int(k)))

    def monomial(self, exps):
        """Fresh (unshared) nodes for x^e1 * y^e2 * ...: a single-use term."""
        fac = [i if e == 1 else self.pow(i, e) for i, e in sorted(exps.items()) if e]
        node = fac[0]
        for f in fac[1:]:
            node = self.mul(node, f)
        return node


def expanded(expr, syms):
    """Flat sum of single-use monomials of the expanded polynomial (FS1)."""
    import sympy as sp
    P = sp.Poly(sp.expand(expr), *syms)
    d = DAG(len(syms))
    ch, co, b = [], [], 0.0
    for mon, coef in P.terms():
        if all(e == 0 for e in mon):
            b += float(coef)
        else:
            ch.append(d.monomial({i: e for i, e in enumerate(mon) if e}))
            co.append(float(coef))
    d.sum(ch, co, b)
    return d.nodes


def in_base(d, base, coeffs):
    """Terms sum_k coeffs[k] * base^k (k >= 1) as fresh pow nodes of one base node;
    returns (children, coefs, const)."""
    ch, co, b = [], [], 0.0
    for k, a in enumerate(coeffs):
        if a == 0:
            continue
        if k == 0:
            b += a
        elif k == 1:
            ch.append(base); co.append(a)
        else:
            ch.append(d.pow(base, k)); co.append(a)
    return ch, co, b
