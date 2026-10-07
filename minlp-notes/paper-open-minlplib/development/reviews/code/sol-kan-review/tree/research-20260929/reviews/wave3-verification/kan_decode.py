"""Independent exact decoder for the MINLPLib kan_* instances (verifier's own code).

Reads the OSIL with the decimal-preserving reader osilx.py and derives, in exact
rational arithmetic, the network that every feasible point must satisfy:

  obj = A * (beta0 + sum_j psi_j(h_j)) + B,
  h_j = beta_j + sum_i phi_ij(u_i),
  phi(z) = P_k(z) + wb * silu(z) for the knot interval k selected by the edge's
  one-hot binaries, with z in I_k (the interval implied by the big-M rows).

P_k is obtained by symbolic propagation of the equality rows with b = e_k:
each solved row has exactly one unknown, which enters linearly with a constant
coefficient, so the propagated value is forced.  Every row and every variable
of the model is classified; unclassified rows raise an error.

Rows that the relaxation R drops: partition-of-unity rows, all bounds on
basis/spline/edge/output variables.  R keeps: one-hot + big-M rows (as
"z in I_k"), the recursion rows (as P_k), the silu rows, edge rows, sum rows,
copy/scaling rows, the objective row, the bounds of the input class and of the
hidden class (h_j and its copies).
"""
import os
import sys
from collections import defaultdict
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "open-instances-verification"))
import osilx  # noqa: E402

OSIL = os.environ["MINLPLIB_OSIL_ROOT"]

# ---- polynomials in Z (edge argument) and S (silu symbol): dict {(pz, ps): Fr}


def pconst(c):
    return {(0, 0): Fr(c)} if c else {}


def padd(a, b, cb=Fr(1)):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, Fr(0)) + cb * v
        if r[k] == 0:
            del r[k]
    return r


def pmul(a, b):
    r = {}
    for (i, j), v in a.items():
        for (k, l), w in b.items():
            key = (i + k, j + l)
            r[key] = r.get(key, Fr(0)) + v * w
            if r[key] == 0:
                del r[key]
    return r


def pscale(a, c):
    return {k: v * c for k, v in a.items()} if c else {}


def fbound(s, default):
    if osilx.isinf(s):
        return None
    return Fr(s)


def decode(name):
    m = osilx.read(os.path.join(OSIL, name + ".osil"))
    names, vt = m["names"], m["vt"]
    nv = len(names)
    lb = [fbound(s, None) for s in m["lb"]]
    ub = [fbound(s, None) for s in m["ub"]]
    assert m["obj"]["sense"] == "min" and Fr(m["obj"]["constant"]) == 0
    assert m["obj"]["weight"] in ("1", "1.0") and not m["obj"]["quad"] and m["obj"]["nl"] is None
    assert len(m["obj"]["lin"]) == 1
    (objvar, oc), = m["obj"]["lin"].items()
    assert Fr(oc) == 1
    rows = []
    for c in m["cons"]:
        assert Fr(c["constant"]) == 0
        rows.append(dict(name=c["name"], lb=fbound(c["lb"], None), ub=fbound(c["ub"], None),
                         lin={j: Fr(v) for j, v in c["lin"].items()},
                         quad=[(i, j, Fr(v)) for i, j, v in c["quad"]], nl=c["nl"]))
    nr = len(rows)
    rowcls = [None] * nr
    vrows = defaultdict(set)
    for r, R in enumerate(rows):
        for j in R["lin"]:
            vrows[j].add(r)
        for i, j, _ in R["quad"]:
            vrows[i].add(r)
            vrows[j].add(r)
        if R["nl"] is not None:
            vrows[_nlvar(R["nl"])].add(r)
    isbin = [t == "B" for t in vt]
    for j in range(nv):
        if isbin[j]:
            assert lb[j] == 0 and ub[j] == 1

    # ---- silu rows: s - z/(exp(-z)+1) = 0
    edges = []
    for r, R in enumerate(rows):
        if R["nl"] is None:
            continue
        t = R["nl"]
        assert t[0] == "negate" and t[1][0] == "divide", t
        num, den = t[1][1], t[1][2]
        assert num[0] == "var" and Fr(num[2]) == 1
        z = num[1]
        assert den[0] == "sum" and len(den) == 3
        ex, one = den[1], den[2]
        assert ex[0] == "exp" and ex[1][0] == "var" and ex[1][1] == z and Fr(ex[1][2]) == -1
        assert one[0] == "num" and Fr(one[1]) == 1
        assert not R["quad"] and len(R["lin"]) == 1 and R["lb"] == 0 and R["ub"] == 0
        (s, cs), = R["lin"].items()
        assert cs == 1
        rowcls[r] = ("silu", len(edges))
        edges.append(dict(z=z, s=s, silurow=r))
    zset = {e["z"] for e in edges}
    assert len(zset) == len(edges), "one edge per argument variable"

    # ---- binaries of each edge: products b*z
    binof = {}
    for ei, e in enumerate(edges):
        bins = set()
        for r in vrows[e["z"]]:
            for i, j, _ in rows[r]["quad"]:
                for a, b in ((i, j), (j, i)):
                    if b == e["z"] and isbin[a]:
                        bins.add(a)
        e["bins"] = sorted(bins)
        for b in bins:
            assert b not in binof
            binof[b] = ei
    assert set(binof) == {j for j in range(nv) if isbin[j]}, "every binary belongs to one edge"

    for ei, e in enumerate(edges):
        z, bins = e["z"], e["bins"]
        bset = set(bins)
        # one-hot row and big-M rows
        bigm = []
        for r in set().union(*(vrows[b] for b in bins)) | vrows[z]:
            R = rows[r]
            if R["quad"] or R["nl"] is not None:
                continue
            keys = set(R["lin"])
            if keys == bset:
                assert all(v == 1 for v in R["lin"].values()) and R["lb"] == 1 and R["ub"] == 1
                assert rowcls[r] is None
                rowcls[r] = ("onehot", ei)
            elif z in keys and keys <= bset | {z} and len(keys) <= 2:
                assert rowcls[r] is None
                rowcls[r] = ("bigm", ei)
                bigm.append(r)
        e["bigm"] = bigm
        # admissible interval for b = e_k
        ivs = []
        for k in bins:
            lo, hi = None, None
            for r in bigm:
                R = rows[r]
                a = R["lin"][z]
                ck = R["lin"].get(k, Fr(0))
                for bnd, side in ((R["lb"], "lb"), (R["ub"], "ub")):
                    if bnd is None:
                        continue
                    v = (bnd - ck) / a
                    # a z >= bnd-ck  (lb side) or a z <= bnd-ck (ub side)
                    is_lower = (side == "lb") == (a > 0)
                    if is_lower:
                        lo = v if lo is None else max(lo, v)
                    else:
                        hi = v if hi is None else min(hi, v)
            assert lo is not None and hi is not None
            ivs.append((lo, hi))
        e["I"] = ivs

    # ---- symbolic propagation per edge and piece
    def propagate(e, k):
        known = {e["z"]: {(1, 0): Fr(1)}, e["s"]: {(0, 1): Fr(1)}}
        for b in e["bins"]:
            known[b] = pconst(1 if b == k else 0)
        solved = []
        queue = set()
        for v in known:
            queue |= vrows[v]
        while queue:
            nxt = set()
            for r in sorted(queue):
                R = rows[r]
                if rowcls[r] is not None and rowcls[r][0] in ("silu", "onehot", "bigm"):
                    continue
                if not R["quad"] and len(R["lin"]) == 2:
                    continue  # copy / scaling / objective rows: not part of an edge
                if R["lb"] is None or R["lb"] != R["ub"] or R["nl"] is not None:
                    continue
                vars_ = set(R["lin"]) | {i for i, _, _ in R["quad"]} | {j for _, j, _ in R["quad"]}
                unk = [v for v in vars_ if v not in known]
                if len(unk) != 1:
                    continue
                u = unk[0]
                if u not in R["lin"] or any(u in (i, j) for i, j, _ in R["quad"]):
                    continue
                rest = pconst(0)
                for j, c in R["lin"].items():
                    if j != u:
                        rest = padd(rest, known[j], c)
                for i, j, c in R["quad"]:
                    rest = padd(rest, pmul(known[i], known[j]), c)
                known[u] = pscale(padd(pconst(R["lb"]), rest, Fr(-1)), 1 / R["lin"][u])
                solved.append((r, u))
                nxt |= vrows[u]
            queue = nxt
        return known, solved

    edge_out = {}
    for ei, e in enumerate(edges):
        # the edge row: the other row containing s
        er = [r for r in vrows[e["s"]] if r != e["silurow"]]
        assert len(er) == 1
        e["edgerow"] = er[0]
        e["P"], e["resid"], e["basis"] = [], [], None
        for kk, k in enumerate(e["bins"]):
            known, solved = propagate(e, k)
            R = rows[er[0]]
            outs = [u for r, u in solved if r == er[0]]
            assert len(outs) == 1
            out = outs[0]
            val = known[out]
            assert all(ps in (0, 1) and (ps == 0 or pz == 0) and pz <= 3 for (pz, ps) in val)
            wb = val.get((0, 1), Fr(0))
            P = [val.get((d, 0), Fr(0)) for d in range(4)]
            e["P"].append(P)
            if kk == 0:
                e["wb"] = wb
                e["out"] = out
                # rows solved (recursion rows) and spline-sum row, and the solved variables
                e["solved_rows"] = {r for r, u in solved}
                e["solved_vars"] = {u for r, u in solved}
            else:
                assert e["wb"] == wb and e["out"] == out
                assert {r for r, u in solved} == e["solved_rows"]
            # partition rows: equality rows, rhs 1, all coefs 1, all vars known basis vars of this edge
            res = []
            for r in set().union(*(vrows[v] for v in e["solved_vars"])):
                R = rows[r]
                if (not R["quad"] and R["nl"] is None and R["lb"] == 1 and R["ub"] == 1
                        and all(c == 1 for c in R["lin"].values())
                        and set(R["lin"]) <= e["solved_vars"] and r not in e["solved_rows"]):
                    tot = pconst(-1)
                    for j in R["lin"]:
                        tot = padd(tot, known[j])
                    res.append((r, [tot.get((d, 0), Fr(0)) for d in range(4)], len(R["lin"])))
                    assert all(ps == 0 for (_, ps) in tot)
            res.sort()
            e["resid"].append(res)
            # values of all basis variables (for B >= 0 checks)
            e.setdefault("vals", []).append({u: known[u] for u in e["solved_vars"]})
        for r in e["solved_rows"]:
            assert rowcls[r] is None or rowcls[r] == ("recur", ei), (r, rowcls[r])
            rowcls[r] = ("recur", ei)
        for r, _, _ in e["resid"][0]:
            rowcls[r] = ("partition", ei)
        edge_out[e["out"]] = ei
    # the solved sets may include the argument copy chain (copy/scale rows); remove those later

    # ---- linear structure: copy rows, scaling rows, sum rows, objective row
    sumrows = {}
    for r, R in enumerate(rows):
        if R["quad"] or R["nl"] is not None or R["lb"] is None or R["lb"] != R["ub"]:
            continue
        outs = [j for j in R["lin"] if j in edge_out]
        if outs and r not in {e["edgerow"] for e in edges}:
            others = [j for j in R["lin"] if j not in edge_out]
            assert len(others) == 1 and R["lin"][others[0]] == 1
            assert all(R["lin"][j] == -1 for j in outs)
            v = others[0]
            sumrows[v] = (R["lb"], sorted(outs, key=lambda o: edge_out[o]), r)
            rowcls[r] = ("sum", v)
    # objective row
    orow = [r for r in vrows[objvar]]
    assert len(orow) == 1
    R = rows[orow[0]]
    assert len(R["lin"]) == 2 and not R["quad"] and R["lb"] == R["ub"]
    yv = [j for j in R["lin"] if j != objvar][0]
    assert yv in sumrows
    # obj = (rhs - a*y)/c_obj
    A = -R["lin"][yv] / R["lin"][objvar]
    Bc = R["lb"] / R["lin"][objvar]
    rowcls[orow[0]] = ("objective",)

    # union-find over copy rows (p - q = 0) and scaling rows (a p - q = c)
    parent = list(range(nv))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    scaled = {}   # q -> (p, a, c): a p - q = c
    for r, R in enumerate(rows):
        if rowcls[r] is not None and rowcls[r][0] != "recur":
            continue
        if R["quad"] or R["nl"] is not None or R["lb"] is None or R["lb"] != R["ub"] or len(R["lin"]) != 2:
            continue
        (p, a), (q, b) = R["lin"].items()
        if a == 1 and b == -1 and R["lb"] == 0 or a == -1 and b == 1 and R["lb"] == 0:
            parent[find(p)] = find(q)
            rowcls[r] = ("copy",)
        elif b == -1 and a not in (1, -1) or a == -1 and b not in (1, -1):
            if a == -1:
                p, a, q, b = q, b, p, a
            # a p - q = c  -> q = a p - c
            assert len(vrows[q]) == 1, "scaled variable used only for bounds"
            scaled[q] = (p, a, R["lb"], r)
            rowcls[r] = ("scale",)
    # recursion rows of an edge must not be copy/scale rows
    for ei, e in enumerate(edges):
        e["solved_rows"] = {r for r in e["solved_rows"] if rowcls[r] == ("recur", ei)}

    classes = defaultdict(list)
    for e in edges:
        classes[find(e["z"])].append(e)
    hidden_vars = [v for v in sumrows if v != yv]
    hid_of_class = {}
    for v in hidden_vars:
        c = find(v)
        assert c not in hid_of_class
        hid_of_class[c] = v
    layer1, layer2 = [], []
    for c, es in classes.items():
        (layer2 if c in hid_of_class else layer1).append(c)
    # class bounds (exact)

    def class_box(c):
        members = [v for v in range(nv) if find(v) == c]
        lo, hi = None, None
        for v in members:
            if lb[v] is not None:
                lo = lb[v] if lo is None else max(lo, lb[v])
            if ub[v] is not None:
                hi = ub[v] if hi is None else min(hi, ub[v])
        for q, (p, a, cc, r) in scaled.items():
            if find(p) == c:
                # q = a p - cc in [lb_q, ub_q]
                l1, h1 = (lb[q] + cc) / a, (ub[q] + cc) / a
                if a < 0:
                    l1, h1 = h1, l1
                lo, hi = max(lo, l1), min(hi, h1)
        return members, lo, hi
    inputs = []
    for c in sorted(layer1, key=lambda c: min(e["z"] for e in classes[c])):
        members, lo, hi = class_box(c)
        inputs.append(dict(cls=c, members=members, lo=lo, hi=hi, edges=classes[c]))
    # hidden neurons in order of their layer-1 sum rows
    hiddens = []
    for c in layer2:
        v = hid_of_class[c]
        members, lo, hi = class_box(c)
        es = classes[c]
        assert len(es) == 1
        beta, outs, r = sumrows[v]
        hiddens.append(dict(var=v, cls=c, members=members, lo=lo, hi=hi, edge2=es[0], beta=beta,
                            in_edges=[edges[edge_out[o]] for o in outs]))
    hiddens.sort(key=lambda h: h["var"])
    beta0, outs0, _ = sumrows[yv]
    # consistency: output sum is over the layer-2 edges, one per hidden
    assert sorted(edge_out[o] for o in outs0) == sorted(edges.index(h["edge2"]) for h in hiddens)
    # layer-1: each hidden has one edge from each input
    inpos = {inp["cls"]: i for i, inp in enumerate(inputs)}
    for h in hiddens:
        srcs = sorted(inpos[find(e["z"])] for e in h["in_edges"])
        assert srcs == list(range(len(inputs))), srcs
        h["edge_from"] = {inpos[find(e["z"])]: e for e in h["in_edges"]}
    # ---- classify remaining rows / variables
    for r in range(nr):
        if rowcls[r] is None:
            raise AssertionError("unclassified row %s: %s" % (rows[r]["name"], rows[r]))
    return dict(name=name, A=A, B=Bc, beta0=beta0, inputs=inputs, hiddens=hiddens, edges=edges,
                rows=rows, rowcls=rowcls, names=names, lb=lb, ub=ub, yv=yv, objvar=objvar,
                scaled=scaled, sumrows=sumrows, m=m)


def _nlvar(t):
    if t[0] == "var":
        return t[1]
    for c in t[1:]:
        if isinstance(c, tuple):
            v = _nlvar(c)
            if v is not None:
                return v
    return None


if __name__ == "__main__":
    import time
    name = sys.argv[1]
    t0 = time.time()
    D = decode(name)
    print(name, "decoded in %.1fs" % (time.time() - t0))
    print("A =", float(D["A"]), "B =", float(D["B"]), "beta0 =", float(D["beta0"]))
    for i, inp in enumerate(D["inputs"]):
        print("input", i, "vars", [D["names"][v] for v in inp["members"]], "box [%.17g, %.17g]" % (inp["lo"], inp["hi"]),
              "edges", len(inp["edges"]), "pieces", [len(e["I"]) for e in inp["edges"]])
    for j, h in enumerate(D["hiddens"]):
        print("hidden", j, D["names"][h["var"]], "class", [D["names"][v] for v in h["members"]],
              "box [%.17g, %.17g]" % (h["lo"], h["hi"]), "beta %.17g" % h["beta"],
              "pieces", len(h["edge2"]["I"]))
    from collections import Counter
    print(Counter(c[0] for c in D["rowcls"]))
