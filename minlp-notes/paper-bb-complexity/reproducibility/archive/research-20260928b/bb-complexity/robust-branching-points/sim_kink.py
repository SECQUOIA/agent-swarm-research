"""Exact-model branch-and-bound on the kink families, for branching-point rules.

1D exact-gap kink (Proposition 4 of competitive-branching.md): f = 2 alpha |y - a| on [0,1],
relaxation f - alpha (y-l)(u-y).  A node [l,u] is open iff a is interior and
alpha (a-l)(u-a) > eps; its relaxation minimizer is a.

2D McCormick kink (Section 5 of face-exact-node-complexity.md): f = 2|x-a| - (x-a)(y-b) on
[0,1]^2 (c = -1, L = 2), termwise McCormick.  A box is open iff l_x < a < u_x and
w_y (a-l_x)(u_x-a)/w_x > eps; the relaxation minimizer is (a, l_y + rho w_y) with
rho = (a-l_x)/w_x (proof of Proposition 5.7 there).  Boxes with a not interior in x are valid.

Point rules (applied to the chosen coordinate i, with relaxation point p and node [l,u], w = u-l):
  clip:th        s = clip(p, l + th w, u - th w)                      (SCIP's clamp with midpull 0)
  rclip:t0:t1    same with th ~ U[t0, t1] drawn independently at every node
  recenter:th    s = p if p in [l + th w, u - th w]; else, if p < l + th w,
                 s = l + max(th w, 2 (p - l)) (the point lands at the child's centre when possible);
                 mirror image above
  noclamp        s = p (only for the kink, where p is interior at open nodes)
  inc:th         split at the incumbent coordinate if it lies strictly inside, else clip:th
  kclip:t0:t1    th ~ U[t0, t1] keyed on (variable, interval): one draw per distinct interval of
                 each variable, shared by all nodes that split that variable on that interval
                 ('keyed randomization'; the first version keyed on the interval only, so x- and
                 y-splits on equal intervals shared a draw; corrected after the review)
Selection: 'x' (x at every open node: identical to 1D), 'w' (widest side, ties to x).

Counts T = number of processed nodes (= 1 + 2 * internal nodes).
"""
import json
import math
import random
import sys
import zlib


def point(rule, p, l, u, rng, inc=None, var=0):
    w = u - l
    kind = rule[0]
    if kind == "noclamp":
        return p
    if kind == "inc":
        if inc is not None and l < inc < u:
            return inc
        th = rule[1]
        return min(max(p, l + th * w), u - th * w)
    if kind == "clip":
        th = rule[1]
    elif kind == "rclip":
        th = rng.uniform(rule[1], rule[2])
    elif kind == "kclip":
        key = (var, l, u)  # per (variable, interval); the first version keyed on (l, u) only
        if key not in rng.keyed:
            rng.keyed[key] = rng.uniform(rule[1], rule[2])
        th = rng.keyed[key]
    elif kind == "recenter":
        th = rule[1]
        if p < l + th * w:
            return l + max(th * w, 2 * (p - l))
        if p > u - th * w:
            return u - max(th * w, 2 * (u - p))
        return p
    else:
        raise ValueError(rule)
    return min(max(p, l + th * w), u - th * w)


def run1d(a, eps, rule, rng, alpha=1.0, cap=10 ** 7):
    """Returns (T, number of splits on the chain, whether the split hit a)."""
    l, u = 0.0, 1.0
    T = 1
    splits = 0
    while True:
        if not (l < a < u) or alpha * (a - l) * (u - a) <= eps:
            return T, splits, False
        s = point(rule, a, l, u, rng, inc=a)
        T += 2
        splits += 1
        if s == a:
            return T, splits, True
        if a < s:
            u = s
        else:
            l = s
        if T > cap:
            return None, splits, False


def run2d(a, eps, rule, sel, rng, ystar=0.5, cap=2 * 10 ** 6):
    stack = [(0.0, 1.0, 0.0, 1.0)]
    T = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        T += 1
        if T > cap:
            return None
        if not (lx < a < ux):
            continue
        wx, wy = ux - lx, uy - ly
        if wy * (a - lx) * (ux - a) / wx <= eps:
            continue
        rho = (a - lx) / wx
        if sel == "x" or wx >= wy:
            s = point(rule, a, lx, ux, rng, inc=a, var=0)
            stack.append((s, ux, ly, uy))
            stack.append((lx, s, ly, uy))
        else:
            s = point(rule, ly + rho * wy, ly, uy, rng, inc=ystar, var=1)
            stack.append((lx, ux, s, uy))
            stack.append((lx, ux, ly, s))
    return T


def parse(r):
    f = r.split(":")
    return (f[0],) + tuple(float(x) for x in f[1:])


def stats(Ts):
    Ts = sorted(Ts)
    n = len(Ts)
    mean = sum(Ts) / n
    sd = (sum((t - mean) ** 2 for t in Ts) / max(1, n - 1)) ** 0.5
    q = lambda p: Ts[min(n - 1, int(p * n))]  # noqa: E731
    return dict(mean=mean, sem=sd / n ** 0.5, q50=q(0.5), q90=q(0.9), q99=q(0.99), max=Ts[-1],
                frac_gt_100=sum(t > 100 for t in Ts) / n)


if __name__ == "__main__":
    # usage: sim_kink.py OUT.jsonl  (runs the grid defined below)
    out = sys.argv[1]
    A = [1 / 6, 3 / 238, 1 / 3, 0.1999, 0.25, 0.4]
    rng0 = random.Random(12345)
    A += [rng0.random() for _ in range(4)]
    RULES = ["clip:0.2", "rclip:0.1:0.3", "rclip:0.05:0.35", "recenter:0.2", "inc:0.2"]
    EPS1 = [10.0 ** -k for k in (2, 4, 8, 16, 32)]
    EPS2 = [10.0 ** -k for k in (2, 3, 4, 5, 6, 7, 8)]
    with open(out, "w") as fh:
        for a in A:
            for r in RULES:
                rule = parse(r)
                rand = rule[0] == "rclip"
                for model, sel, EPS, reps in (("1d", "x", EPS1, 20000 if rand else 1),
                                              ("2d", "w", EPS2, 1000 if rand else 1)):
                    for eps in EPS:
                        rng = random.Random(zlib.crc32(repr((a, r, model, eps)).encode()))
                        if model == "1d":
                            Ts = [run1d(a, eps, rule, rng)[0] for _ in range(reps)]
                        else:
                            Ts = [run2d(a, eps, rule, sel, rng) for _ in range(reps)]
                        capped = sum(t is None for t in Ts)
                        Ts = [t for t in Ts if t is not None]
                        fh.write(json.dumps(dict(model=model, a=a, rule=r, sel=sel, eps=eps, reps=reps,
                                                 capped=capped, **stats(Ts))) + "\n")
                        fh.flush()
                print(f"{a:.4f} {r}", flush=True)
