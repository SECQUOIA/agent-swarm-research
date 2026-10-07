"""High-precision evaluation of KAN points (verifier's own code).

  python3 kan_primal.py <name> <solfile>

Evaluates every OSIL row and bound at 60 digits (decimal-exact constants),
reports the objective, the max violation split into partition rows and all
other rows, bound and integrality violations, and cross-checks
  (a) the decoder's partition residual polynomials against the actual row
      values at the point, and
  (b) the reduced network value V(u) (decoder: P_k + wb*silu, pieces taken from
      the point's binaries) against the point's objective variable.
"""
import sys

from mpmath import mp, mpf

from kan_decode import decode, osilx

mp.dps = 60


def readsol(path):
    x = {}
    for line in open(path):
        p = line.split()
        if len(p) >= 2:
            x[p[0]] = p[1]
    return x


def main(name, solpath):
    D = decode(name)
    m, names = D["m"], D["names"]
    xs = readsol(solpath)
    idx = {n: i for i, n in enumerate(names)}
    x = [mpf(0)] * len(names)
    for n, v in xs.items():
        if n in idx:
            x[idx[n]] = mpf(v)
    fns = {"exp": mp.exp}
    worst = {}
    for r, c in enumerate(m["cons"]):
        val = osilx.ev_row(c, x, mpf, fns)
        v = mpf(0)
        if not osilx.isinf(c["lb"]):
            v = max(v, mpf(c["lb"]) - val)
        if not osilx.isinf(c["ub"]):
            v = max(v, val - mpf(c["ub"]))
        cls = D["rowcls"][r][0]
        cls = "partition" if cls == "partition" else "other"
        if v > worst.get(cls, (mpf(-1),))[0]:
            worst[cls] = (v, c["name"])
    bv, iv = mpf(0), mpf(0)
    for j in range(len(names)):
        if not osilx.isinf(m["lb"][j]):
            bv = max(bv, mpf(m["lb"][j]) - x[j])
        if not osilx.isinf(m["ub"][j]):
            bv = max(bv, x[j] - mpf(m["ub"][j]))
        if m["vt"][j] == "B":
            iv = max(iv, min(abs(x[j]), abs(x[j] - 1)))
    obj = x[D["objvar"]]
    print("%s  %s" % (name, solpath.split("/")[-1]))
    print("  objective %s" % mp.nstr(obj, 20))
    for k, (v, n) in sorted(worst.items()):
        print("  max violation %-9s rows: %s (%s)" % (k, mp.nstr(v, 3), n))
    print("  max bound violation %s, max integrality violation %s" % (mp.nstr(bv, 3), mp.nstr(iv, 3)))
    # (a) residual cross-check and (b) reduced network value
    maxdiff = mpf(0)
    for e in D["edges"]:
        ks = [kk for kk, b in enumerate(e["bins"]) if x[b] > 0.5]
        assert len(ks) == 1
        kk = ks[0]
        z = x[e["z"]]
        for r, c, n in e["resid"][kk]:
            rowval = sum(x[j] for j in D["rows"][r]["lin"]) - 1
            polyval = sum(mpf(cc.numerator) / cc.denominator * z ** d for d, cc in enumerate(c))
            maxdiff = max(maxdiff, abs(rowval - polyval))
        e["_k"] = kk
    print("  partition residual: |row value - decoder polynomial| max %s" % mp.nstr(maxdiff, 3))

    def fr(q):
        return mpf(q.numerator) / q.denominator

    def phi(e, z):
        P = e["P"][e["_k"]]
        return sum(fr(c) * z ** d for d, c in enumerate(P)) + fr(e["wb"]) * z / (1 + mp.exp(-z))
    u = [x[inp["edges"][0]["z"]] for inp in D["inputs"]]
    y = fr(D["beta0"])
    hin = []
    for h in D["hiddens"]:
        hv = fr(h["beta"]) + sum(phi(h["edge_from"][i], u[i]) for i in range(len(u)))
        hin.append((hv, fr(h["lo"]), fr(h["hi"])))
        y += phi(h["edge2"], hv)
    V = fr(D["A"]) * y + fr(D["B"])
    print("  inputs u = [%s]" % ", ".join(mp.nstr(t, 17) for t in u))
    print("  reduced network value V(u) = %s  (|V - objvar| = %s)" % (mp.nstr(V, 20), mp.nstr(abs(V - obj), 3)))
    print("  hidden h_j margins to [L_j, U_j]: min %s" % mp.nstr(min(min(hv - lo, hi - hv) for hv, lo, hi in hin), 3))
    return V


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
