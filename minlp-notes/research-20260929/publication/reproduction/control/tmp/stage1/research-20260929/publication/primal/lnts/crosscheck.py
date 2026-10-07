"""Second, separately coded check of the saved lnts points.

Usage: python3 crosscheck.py 50 100 200 400

Reads only the point files points/lnts<N>_point.json and the OSIL files.
It differs from lnts_primal.py in three ways:
  * the OSIL file is parsed with the verifier's reader
    (reviews/open-instances-verification/osilx.py), not with osil_iv.py;
  * F and its Jacobian come from the closed-form sums
        vx_N = a h sum_j w_j cos th_j,  vy_N = a h sum_j w_j sin th_j,
        py_N = a h^2 sum_j c_j sin th_j
    with hand-written derivatives (no automatic differentiation); the sums
    are first checked against the exact recursion in rational arithmetic;
  * the Krawczyk test is rerun on the stored box (centre +- radius).
Finally every row and bound of the parsed OSIL is evaluated in interval
arithmetic over the stored 60-digit enclosures of all variables, and the
objective is enclosed from the stored box of h.
"""
import json
import sys
from fractions import Fraction as Q

from mpmath import iv, mp

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
sys.path.insert(0, _REPO + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402

DPS = 110
POINTS = "points"


def I(q):
    q = Q(q)
    return iv.mpf(q.numerator) / q.denominator


def lo_hi(x):
    def f(t):
        s, m, e, _ = t
        assert m != 0 or e == 0
        v = Q(int(m)) * Q(2) ** e
        return -v if s else v
    return f(x._mpi_[0]), f(x._mpi_[1])


def dec(q, k, up):
    """q rounded outward to k decimals, as a string (q > 0 assumed)."""
    n = q * 10**k
    n = -((-n.numerator) // n.denominator) if up else n.numerator // n.denominator
    return f"{n // 10**k}.{n % 10**k:0{k}d}"


def weights(N):
    """w_j and c_j = sum_k w_k W_kj, W_kj = ([j <= k-1] + [1 <= j <= k]) / 2, in O(N)."""
    w = [Q(1, 2)] + [Q(1)] * (N - 1) + [Q(1, 2)]
    # c_j = (sum_{k >= j+1} w_k + [j >= 1] sum_{k >= j} w_k) / 2 (suffix sums)
    suf = [Q(0)] * (N + 2)
    for k in range(N, -1, -1):
        suf[k] = suf[k + 1] + w[k]
    c = [(suf[j + 1] + (suf[j] if j >= 1 else 0)) / 2 for j in range(N + 1)]
    return w, c


def identity_check(N, w, c):
    """Exact check of the closed forms against the row recursion, on every
    unit vector (this proves the linear identities at h = 1, a = 1) and on one
    rational point with h = 3/7, a = 100."""
    def rec(k_, s_, h, a):
        vx, vy, py = Q(0), Q(0), Q(0)
        for i in range(N):
            vx_n = vx + h / 2 * (a * k_[i] + a * k_[i + 1])
            vy_n = vy + h / 2 * (a * s_[i] + a * s_[i + 1])
            py = py + h / 2 * (vy + vy_n)
            vx, vy = vx_n, vy_n
        return vx, vy, py
    for j in range(N + 1):
        e = [Q(0)] * (N + 1)
        e[j] = Q(1)
        vx, vy, py = rec(e, e, Q(1), Q(1))
        assert vx == w[j] and vy == w[j] and py == c[j], j
    k_ = [Q((7 * j) % 11 - 5, 13) for j in range(N + 1)]
    s_ = [Q((5 * j) % 9 - 4, 17) for j in range(N + 1)]
    h, a = Q(3, 7), Q(100)
    vx, vy, py = rec(k_, s_, h, a)
    assert vx == a * h * sum(x * y for x, y in zip(w, k_))
    assert vy == a * h * sum(x * y for x, y in zip(w, s_))
    assert py == a * h * h * sum(x * y for x, y in zip(c, s_))


def FJ(t0, tN, h, Kc, Ks, Ls, w0, wN, c0, cN, a):
    C0, S0, CN, SN = iv.cos(t0), iv.sin(t0), iv.cos(tN), iv.sin(tN)
    Sc = w0 * C0 + wN * CN + Kc
    Ss = w0 * S0 + wN * SN + Ks
    Sl = c0 * S0 + cN * SN + Ls
    F = [a * h * Sc - 45, a * h * Ss, a * h * h * Sl - 5]
    J = [[-a * h * w0 * S0, -a * h * wN * SN, a * Sc],
         [a * h * w0 * C0, a * h * wN * CN, a * Ss],
         [a * h * h * c0 * C0, a * h * h * cN * CN, 2 * a * h * Sl]]
    return F, J


def run(N):
    mp.dps = iv.dps = DPS
    P = json.load(open(f"{POINTS}/lnts{N}_point.json"))
    M = osilx.read(P["osil"])
    names = M["names"]
    idx = {nm: j for j, nm in enumerate(names)}
    th = list(range(N + 1))
    h_i = 5 * N + 5
    a = I(100)
    # the stored controls must be exactly the OSIL theta variables 1..N-1
    assert sorted(idx[nm] for nm in P["fixed_controls"]) == th[1:N]
    w, c = weights(N)
    identity_check(N, w, c)
    thq = {idx[nm]: Q(s) for nm, s in P["fixed_controls"].items()}
    Kc = Ks = Ls = iv.mpf(0)
    for j in range(1, N):
        t = I(thq[j])
        Kc += I(w[j]) * iv.cos(t)
        Ks += I(w[j]) * iv.sin(t)
        Ls += I(c[j]) * iv.sin(t)
    box = {idx[nm]: (Q(d["centre"]), Q(d["radius"])) for nm, d in P["unknowns_box"].items()}
    assert sorted(box) == [0, N, h_i]
    order = [0, N, h_i]
    X = [iv.mpf([I(box[k][0] - box[k][1]).a, I(box[k][0] + box[k][1]).b]) for k in order]
    Y = [I(box[k][0]) for k in order]
    consts = (Kc, Ks, Ls, I(w[0]), I(w[N]), I(c[0]), I(c[N]), a)
    Fy, _ = FJ(*Y, *consts)
    _, JX = FJ(*X, *consts)
    Cm = mp.matrix([[mp.make_mpf(JX[i][j].mid._mpi_[0]) for j in range(3)] for i in range(3)]) ** -1
    K = []
    for i in range(3):
        s = Y[i] - sum((iv.mpf(Cm[i, k]) * Fy[k] for k in range(3)), iv.mpf(0))
        for j in range(3):
            m = iv.mpf(1 if i == j else 0) - sum((iv.mpf(Cm[i, k]) * JX[k][j] for k in range(3)), iv.mpf(0))
            s += m * (X[j] - Y[j])
        K.append(s)
    ok = all(lo_hi(K[k])[0] > lo_hi(X[k])[0] and lo_hi(K[k])[1] < lo_hi(X[k])[1] for k in range(3))
    assert ok, "Krawczyk failed"
    # the zero lies in the exact decimal box centre +- radius
    for k, key in enumerate(order):
        kl, kh = lo_hi(K[k])
        assert box[key][0] - box[key][1] < kl and kh < box[key][0] + box[key][1]
    hK = lo_hi(K[2])
    # rows and bounds over the stored enclosures, with the verifier's reader and evaluator
    enc = P["enclosures"]
    assert [e[0] for e in enc] == names
    Xf = [iv.mpf([I(Q(e[1])).a, I(Q(e[2])).b]) for e in enc]
    num = lambda s: I(Q(s))
    fns = {"cos": iv.cos, "sin": iv.sin}
    assert all(t == "C" for t in M["vt"])
    for j in range(len(names)):
        lo, hi = Q(enc[j][1]), Q(enc[j][2])
        assert lo <= hi
        if not osilx.isinf(M["lb"][j]):
            assert lo >= Q(M["lb"][j]), (names[j], "lb")
        if not osilx.isinf(M["ub"][j]):
            assert hi <= Q(M["ub"][j]), (names[j], "ub")
    worst = 0
    for r, row in enumerate(M["cons"]):
        R = osilx.ev_row(row, Xf, num, fns)
        rl, rh = lo_hi(R)
        assert rl <= Q(row["lb"]) and Q(row["ub"]) <= rh, (r, R)
        worst = max(worst, float(rh - rl))
    obj = osilx.ev_row(M["obj"], Xf, num, fns)
    ol, oh = lo_hi(obj)
    out = dict(instance=f"lnts{N}", krawczyk_closed_form=ok,
               h_enclosure_width=float(hK[1] - hK[0]),
               N_h_upper_25=dec(N * hK[1], 25, up=True),
               obj_from_stored_enclosures_25=[dec(ol, 25, up=False), dec(oh, 25, up=True)],
               max_row_enclosure_width=worst)
    print(json.dumps(out), flush=True)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--points"]:  # alternative point folder (used for the mutation tests)
        POINTS, args = args[1], args[2:]
    res = [run(int(a)) for a in args]
    if POINTS == "points":
        with open("logs/crosscheck_" + "_".join(args) + ".json", "w") as f:
            json.dump(res, f, indent=1)
