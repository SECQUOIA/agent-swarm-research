"""Independent recovery of the period structure of waterno2_T (verifier's code).

Rule used here (different from wmodel.partition): remove the horizon row and
ALL copy rows (-x_a + x_b = 0); the remaining rows split the variables into
'atoms'.  Copy rows are then classified by the atoms of their two variables:
same atom / atom-to-singleton (kept inside a period) or core-to-core (link).
Each period is additionally compared with the single period of waterno2_01
(row signatures up to variable renaming).
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys, collections, json
sys.path.insert(0, _RESEARCH + "/reviews/open-instances-verification")
import osilx
from fractions import Fraction as F

OSIL = _os.path.expanduser("~/.cache/minlplib/minlplib/osil/waterno2_{:02d}.osil")


def varset(c):
    s = set(c["lin"])
    for i, j, a in c["quad"]:
        s |= {i, j}

    def walk(t):
        if t[0] == "var":
            s.add(t[1])
        elif t[0] != "num":
            for u in t[1:]:
                walk(u)
    if c["nl"] is not None:
        walk(c["nl"])
    return s


def sig(c):
    """Row signature invariant under variable renaming."""
    lin = tuple(sorted(str(F(a)) for a in c["lin"].values()))
    quad = tuple(sorted((i == j, str(F(a))) for i, j, a in c["quad"]))
    nl = repr(c["nl"][0]) if c["nl"] else None
    if c["nl"]:
        t = c["nl"]
        assert t[0] == "power" and t[1][0] == "var" and t[2][0] == "num", t
        nl = ("power", str(F(t[1][2])), str(F(t[2][1])))
    return (lin, quad, nl, c["lb"], c["ub"])


def analyse(T):
    m = osilx.read(OSIL.format(T))
    assert m["obj"]["constant"] == "0" and m["obj"]["sense"] == "min"
    assert not m["obj"]["quad"] and m["obj"]["nl"] is None
    assert all(c["constant"] == "0" for c in m["cons"])
    assert all(F(a) == 1 for a in m["obj"]["lin"].values())
    cons = m["cons"]
    n = len(m["names"])
    V = [varset(c) for c in cons]
    copy = [i for i, c in enumerate(cons) if not c["quad"] and c["nl"] is None and len(c["lin"]) == 2
            and sorted(F(a) for a in c["lin"].values()) == [-1, 1]
            and c["lb"] != "-INF" and c["ub"] != "INF" and F(c["lb"]) == 0 and F(c["ub"]) == 0]
    hor = [i for i, c in enumerate(cons) if len(V[i]) == T and not c["quad"] and c["nl"] is None
           and all(F(a) == 1 for a in c["lin"].values()) and c["ub"] == "INF" and i not in copy]
    assert len(hor) == 1, hor
    par = list(range(n))

    def f(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    rem = set(copy) | set(hor)
    for i in range(len(cons)):
        if i in rem:
            continue
        l = sorted(V[i])
        for v in l[1:]:
            par[f(v)] = f(l[0])
    atoms = collections.defaultdict(list)
    for v in range(n):
        atoms[f(v)].append(v)
    cores = [a for a, vs in atoms.items() if len(vs) > 1]
    single = [a for a, vs in atoms.items() if len(vs) == 1]
    assert len(cores) == T, len(cores)
    # attach singletons via copy rows; classify copy rows
    owner = {a: a for a in cores}
    link = []
    for i in copy:
        a, b = (f(v) for v in cons[i]["lin"])
        if a == b:
            continue
        if a in cores and b in cores:
            link.append(i)
        else:
            s, c = (a, b) if b in cores else (b, a)
            assert c in cores and s in single
            assert owner.get(s, c) == c
            owner[s] = c
    assert all(s in owner for s in single), "unattached singleton"
    per = {c: [] for c in cores}
    for a, vs in atoms.items():
        per[owner[a]] += vs
    pid = {v: c for c in cores for v in per[c]}
    rows_in = {c: [] for c in cores}
    other = []
    for i in range(len(cons)):
        ks = {pid[v] for v in V[i]}
        if i in hor:
            other.append(i)
        elif len(ks) == 1:
            rows_in[ks.pop()].append(i)
        else:
            other.append(i)
    assert sorted(other) == sorted(link + hor), (len(other), len(link), len(hor))
    # chain order
    adj = collections.defaultdict(collections.Counter)
    for i in link:
        a, b = (pid[v] for v in cons[i]["lin"])
        adj[a][b] += 1
        adj[b][a] += 1
    fixed = {c: [v for v in per[c] if m["lb"][v] == m["ub"][v]] for c in cores}
    if T > 1:
        ends = [c for c in cores if len(adj[c]) == 1]
        assert len(ends) == 2 and all(len(adj[c]) <= 2 for c in cores)
        assert all(k == 3 for c in cores for k in adj[c].values())
        start = [c for c in ends if len(fixed[c]) == max(len(fixed[e]) for e in ends)]
        assert len(start) == 1
        order = [start[0]]
        while len(order) < T:
            nx = [c for c in adj[order[-1]] if c not in order]
            assert len(nx) == 1
            order.append(nx[0])
    else:
        order = cores
    # link direction: which variable is in the earlier period, sign convention
    pos = {c: t for t, c in enumerate(order)}
    links = []
    for i in link:
        (va, ca), (vb, cb) = sorted(((v, a) for v, a in cons[i]["lin"].items()), key=lambda p: pos[pid[p[0]]])
        assert pos[pid[vb]] == pos[pid[va]] + 1
        links.append((cons[i]["name"], pos[pid[va]], m["names"][va], ca, m["names"][vb], cb))
    h = cons[hor[0]]
    hv = sorted(h["lin"], key=lambda v: pos[pid[v]])
    assert [pos[pid[v]] for v in hv] == list(range(T))
    out = dict(T=T, nvars=n, nrows=len(cons),
               per_nvars=[len(per[c]) for c in order],
               per_nbin=[sum(m["vt"][v] == "B" for v in per[c]) for c in order],
               per_nrows=[len(rows_in[c]) for c in order],
               per_nobj=[sum(v in m["obj"]["lin"] for v in per[c]) for c in order],
               per_nfixed=[len(fixed[c]) for c in order],
               nlink=len(link), link_per_transition=[sum(1 for l in links if l[1] == t) for t in range(T - 1)],
               horizon=(h["name"], [m["names"][v] for v in hv], h["lb"], h["ub"]),
               links_first=links[:3] if T > 1 else [])
    # coefficient sign convention of every link: -x_end(t) + x_start(t+1)
    out["link_sign_ok"] = all(F(ca) == -1 and F(cb) == 1 for (_, _, _, ca, _, cb) in links)
    # compare row-signature multisets with waterno2_01's period
    sigs = [collections.Counter(sig(cons[i]) for i in rows_in[c]) for c in order]
    return m, out, sigs, order, per, rows_in, pid, links, hor


if __name__ == "__main__":
    _, _, ref, *_ = analyse(1)
    ref = ref[0]
    for T in [int(a) for a in sys.argv[1:]]:
        m, out, sigs, *_ = analyse(T)
        diffs = []
        for t, s in enumerate(sigs):
            d = (s - ref) + (ref - s)
            diffs.append(sum(d.values()))
        out["sig_diff_vs_T1"] = diffs
        print(json.dumps(out))
