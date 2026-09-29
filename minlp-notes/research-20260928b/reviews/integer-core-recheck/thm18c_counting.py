"""Recheck of the revised Theorem 1.8(c), exact rational arithmetic.

Model: phi = ||A x - y||^2 on K = box (natural relaxation), P = integer points of the
box, UB = OPT known from the start, tau = OPT - eps.  All node bounds are exact minima
over boxes; kappa is exact (subset DP over all partitions of P).

Reductions (each removal certified on the CURRENT box, one piece per bound change):
  binaries  : incumbent probing: if r(box cap {x_i = v}) >= tau, fix x_i = 1 - v.
  integers  : bound tightening by any amount: new l_i = c + 1 with c the largest value
              such that r(box cap {x_i <= c}) >= tau (symmetric for u_i).  This removes
              at least as much as OBBT's ceil rule and is one piece per change.
  modes     : 'one'  = one pass per node (each of the 2n bounds visited once);
              'iter' = passes repeated until nothing changes (fixpoint).
A node stops reducing as soon as its current box is prunable (r >= tau), so S is as
small as the rule allows (the stringent case for kappa <= L + S).

For every instance we compute, over ALL variable-branching trees (all variables and all
split values), the minimum number of nodes N and, separately, the minimum of L + S.  We
check kappa <= min(L + S), the node forms (kappa <= (2n+1) N for one pass,
kappa <= (n+1) N for binaries), and we build the tree T' of the proof for the min-N run
and verify Definition 1.1 on it directly: covering at every chain node and every
branching node for all P-points, and exact leaf bounds >= tau; its leaf count must be
L + S (binaries: an emptied node's own leaf is dropped).
"""
import functools
import itertools
import random
import sys
from fractions import Fraction as Fr

from exact import phi, box_min, bad_masks, admissible_table, min_cover, solve


def exact_kappa(A, y, P, tau):
    ok = admissible_table(len(P), bad_masks(A, y, P, tau))
    return min_cover(len(P), ok)[-1]


class Run:
    def __init__(self, A, y, lo0, hi0, tau, mode, order, early_stop=True):
        self.A, self.y, self.tau, self.mode, self.order = A, y, tau, mode, order
        self.early_stop = early_stop
        self.n = len(lo0)
        self.lo0, self.hi0 = tuple(lo0), tuple(hi0)
        self.bound = functools.lru_cache(maxsize=None)(self._bound)

    def _bound(self, lo, hi):
        v = box_min(self.A, self.y, lo, hi)
        return None if v is None else v  # None = empty box (+inf)

    def certified(self, lo, hi):
        b = self.bound(lo, hi)
        return b is None or b >= self.tau

    @functools.lru_cache(maxsize=None)
    def reduce(self, lo, hi):
        """returns (steps, lo', hi'); steps = list of (lo, hi, piece_lo, piece_hi, new_lo,
        new_hi) for the chain; lo' > hi' somewhere means the box has no P-points."""
        lo, hi = list(lo), list(hi)
        steps = []
        visits = 0
        while True:
            changed = False
            for i in self.order:
                for side in (0, 1):
                    if any(l > h for l, h in zip(lo, hi)):
                        return steps, tuple(lo), tuple(hi)
                    if self.early_stop and self.certified(tuple(lo), tuple(hi)):
                        return steps, tuple(lo), tuple(hi)
                    if side == 0:  # raise lo_i
                        c = None
                        for cc in range(lo[i], hi[i] + 1):
                            h2 = list(hi); h2[i] = cc
                            if self.certified(tuple(lo), tuple(h2)):
                                c = cc
                            else:
                                break
                        if c is not None:
                            pl, ph = list(lo), list(hi); ph[i] = c
                            nl = list(lo); nl[i] = c + 1
                            steps.append((tuple(lo), tuple(hi), tuple(pl), tuple(ph), tuple(nl), tuple(hi)))
                            lo = nl
                            changed = True
                    else:  # lower hi_i
                        c = None
                        for cc in range(hi[i], lo[i] - 1, -1):
                            l2 = list(lo); l2[i] = cc
                            if self.certified(tuple(l2), tuple(hi)):
                                c = cc
                            else:
                                break
                        if c is not None:
                            pl, ph = list(lo), list(hi); pl[i] = c
                            nh = list(hi); nh[i] = c - 1
                            steps.append((tuple(lo), tuple(hi), tuple(pl), tuple(ph), tuple(lo), tuple(nh)))
                            hi = nh
                            changed = True
            if self.mode == 'one' or not changed:
                return steps, tuple(lo), tuple(hi)

    @functools.lru_cache(maxsize=None)
    def best(self, lo, hi, key):
        """min over branching trees of key in {'N', 'LS'}; returns (N, L, S, tree)"""
        steps, rl, rh = self.reduce(lo, hi)
        s = len(steps)
        if any(l > h for l, h in zip(rl, rh)) or self.certified(rl, rh):
            return (1, 1, s, ('leaf', lo, hi, steps, rl, rh))
        cands = []
        for i in range(self.n):
            for c in range(rl[i], rh[i]):
                h1 = list(rh); h1[i] = c
                l2 = list(rl); l2[i] = c + 1
                a = self.best(rl, tuple(h1), key)
                b = self.best(tuple(l2), rh, key)
                cands.append((1 + a[0] + b[0], a[1] + b[1], s + a[2] + b[2],
                              ('branch', lo, hi, steps, rl, rh, a[3], b[3])))
        if key == 'N':
            return min(cands, key=lambda t: (t[0], t[1] + t[2]))
        return min(cands, key=lambda t: (t[1] + t[2], t[0]))


def validate_Tprime(run, tree, P, binary):
    """Build T' (chain per node) and check Definition 1.1 directly.  Returns
    (valid, number of leaves of T')."""
    tau = run.tau
    inbox = lambda p, lo, hi: all(l <= x <= h for x, l, h in zip(p, lo, hi))
    leaves = 0
    ok = True

    def leafbound_ok(lo, hi):
        b = run.bound(lo, hi)
        return b is None or b >= tau

    def visit(t, parent_box):
        nonlocal leaves, ok
        kind, lo, hi, steps, rl, rh = t[:6]
        # the node's set must lie in the parent's final set (nested sets)
        if parent_box is not None:
            plo, phi_ = parent_box
            ok &= all(pl <= l and h <= ph for l, h, pl, ph in zip(lo, hi, plo, phi_))
        cur = (lo, hi)
        for (clo, chi, pl, ph, nl, nh) in steps:
            ok &= (clo, chi) == cur
            # piece leaf: current box cap D, certified
            ok &= leafbound_ok(pl, ph)
            leaves += 1
            # covering: P-points of the chain node lie in the piece or in the next node
            for p in P:
                if inbox(p, clo, chi):
                    ok &= inbox(p, pl, ph) or inbox(p, nl, nh)
            cur = (nl, nh)
        ok &= cur == (rl, rh)
        emptied = any(l > h for l, h in zip(rl, rh))
        if kind == 'leaf':
            if emptied and binary and steps:
                pass  # the last chain node keeps only its D-child: no own leaf
            else:
                ok &= leafbound_ok(rl, rh)
                leaves += 1
            return
        a, b = t[6], t[7]
        # branching covering: P-points of the final box lie in one of the two children
        for p in P:
            if inbox(p, rl, rh):
                ok &= inbox(p, a[1], a[2]) or inbox(p, b[1], b[2])
        visit(a, (rl, rh))
        visit(b, (rl, rh))

    visit(tree, None)
    return ok, leaves


def count_emptied(tree):
    kind = tree[0]
    rl, rh = tree[4], tree[5]
    e = int(kind == 'leaf' and any(l > h for l, h in zip(rl, rh)) and len(tree[3]) > 0)
    if kind == 'branch':
        e += count_emptied(tree[6]) + count_emptied(tree[7])
    return e


def rand_A(rng, n):
    while True:
        A = [[Fr(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
        if solve(A, [Fr(0)] * n) is not None:
            return A


def experiment(label, lo0, hi0, trials, modes, rng, binary, early_stop=True):
    n = len(lo0)
    P = [tuple(Fr(v) for v in p) for p in itertools.product(*[range(l, h + 1) for l, h in zip(lo0, hi0)])]
    res = {m: dict(inst=0, viol_LS=0, viol_node=0, tprime_ok=0, tprime_count_ok=0, maxratio=Fr(0),
                   minslack=None, emptied=0, kd={}, maxS_node=0) for m in modes}
    for t in range(trials):
        A = rand_A(rng, n)
        # target: image of a random interior point plus noise, so the root has a gap
        c = [Fr(rng.randint(1, 2 * (h - l) * 4 - 1), 8) + l for l, h in zip(lo0, hi0)]
        y = [sum(A[i][j] * c[j] for j in range(n)) + Fr(rng.randint(-4, 4), 10) for i in range(n)]
        OPT = min(phi(A, y, p) for p in P)
        eps = rng.choice([Fr(0), OPT / 100, OPT / 10, OPT / 3])
        tau = OPT - eps
        kappa = exact_kappa(A, y, P, tau)
        for mode in modes:
            order = list(range(n)) if rng.random() < 0.5 else list(reversed(range(n)))
            run = Run(A, y, lo0, hi0, tau, mode, order, early_stop)
            N, L, S, tree = run.best(run.lo0, run.hi0, 'N')
            N2, L2, S2, tree2 = run.best(run.lo0, run.hi0, 'LS')
            r = res[mode]
            r['inst'] += 1
            r['kd'][kappa] = r['kd'].get(kappa, 0) + 1
            r['viol_LS'] += kappa > L2 + S2
            slack = L2 + S2 - kappa
            r['minslack'] = slack if r['minslack'] is None else min(r['minslack'], slack)
            factor = (n + 1) if binary else (2 * n + 1)
            if mode == 'one' or binary:
                r['viol_node'] += kappa > factor * N
            r['maxratio'] = max(r['maxratio'], Fr(kappa, N))
            ok, leaves = validate_Tprime(run, tree, P, binary)
            e = count_emptied(tree)
            r['emptied'] += e
            r['tprime_ok'] += ok
            expected = L + S - (e if binary else 0)
            r['tprime_count_ok'] += leaves == expected and leaves >= kappa
            # the largest number of pieces at a single node, over the min-N tree
            def maxs(tr):
                m = len(tr[3])
                if tr[0] == 'branch':
                    m = max(m, maxs(tr[6]), maxs(tr[7]))
                return m
            r['maxS_node'] = max(r['maxS_node'], maxs(tree))
    for mode in modes:
        r = res[mode]
        factor = 'n+1' if binary else '2n+1'
        print(f"   {label}, mode={mode}, early_stop={early_stop}: {r['inst']} instances, kappa distribution {dict(sorted(r['kd'].items()))}")
        print(f"      kappa <= min(L+S) violations: {r['viol_LS']} (min slack {r['minslack']}); "
              f"node form kappa <= ({factor}) N violations: {r['viol_node'] if (mode == 'one' or binary) else 'not claimed'}; "
              f"max kappa/N = {r['maxratio']} ({float(r['maxratio']):.2f})")
        print(f"      T' of the proof valid (Definition 1.1 + exact leaf bounds): {r['tprime_ok']}/{r['inst']}; "
              f"leaf count = L + S (minus dropped emptied leaves) and >= kappa: {r['tprime_count_ok']}/{r['inst']}; "
              f"emptied nodes with pieces: {r['emptied']}; max pieces at one node: {r['maxS_node']}")


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 20260929)
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    print("== binaries, n = 3, box [0,1]^3, incumbent probing ==")
    experiment("binaries n=3", (0, 0, 0), (1, 1, 1), T, ('one', 'iter'), rng, True)
    print("   (probing continues even when the box is already prunable, so nodes can empty)")
    experiment("binaries n=3", (0, 0, 0), (1, 1, 1), T, ('iter',), rng, True, early_stop=False)
    print("== binaries, n = 4, box [0,1]^4, incumbent probing ==")
    experiment("binaries n=4", (0, 0, 0, 0), (1, 1, 1, 1), T // 10, ("iter",), rng, True)
    print("== general integers, n = 2, box [0,2]x[0,3], bound tightening by any amount ==")
    experiment("integers n=2", (0, 0), (2, 3), T, ('one', 'iter'), rng, False)
    print("== general integers, n = 3, box [0,1]x[0,1]x[0,2] ==")
    experiment("integers n=3", (0, 0, 0), (1, 1, 2), T, ('one', 'iter'), rng, False)
