"""Rebuild the network data of a MINLPLib pq-formulation pooling instance (pooling_spp*pq) from its OSiL file.

The pq model has rows w = q*y (path flow = proportion * pool-output flow), simplex rows
sum q = 1 (one per pool), unit capacity rows, and quality rows sum gamma*flow <= 0.
The result is an Inst-compatible object for instance.py.
"""
from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../..').resolve()

import sys, json
from collections import defaultdict
sys.path.insert(0, (str(_NOTES_ROOT) + '/research-20260922/scouting/minlplib-open-data'))
import osil
import instance as I


class SppInst(I.Inst):
    def __init__(self, path):
        d = osil.read(path); rows = d["rows"]; n = len(d["lb"])
        self.name = path.split("/")[-1].replace(".osil", ""); self.opt = None
        wq, wy = {}, {}
        for k, r in rows.items():
            if k >= 0 and r["quad"]:
                (w,), ((a, b, c),) = r["lin"].keys(), r["quad"]
                assert r["lin"][w] == 1.0 and c == -1.0 and r["lb"] == r["ub"] == 0
                wq[w], wy[w] = a, b
        W = set(wq); Qv = set(wq.values()); Yv = set(wy.values())
        pool_of_q = {}
        simplex = [k for k, r in rows.items() if k >= 0 and not r["quad"] and set(r["lin"]) <= Qv]
        for idx, k in enumerate(simplex):
            for qv in rows[k]["lin"]: pool_of_q[qv] = f"l{idx}"
        Z = set(range(n)) - W - Qv - Yv
        Z = {v for v in Z if any(v in r["lin"] for k, r in rows.items() if k >= 0)}
        qual = [k for k, r in rows.items() if k >= 0 and not r["quad"] and r["ub"] == 0 and set(r["lin"].values()) - {1.0}]
        # outputs: union-find over quality rows sharing a variable, and over path flows sharing a y
        parent = {}
        def find(u):
            while parent.setdefault(u, u) != u:
                parent[u] = parent[parent[u]]; u = parent[u]
            return u
        def union(u, v):
            parent[find(u)] = find(v)
        for k in qual:
            for v in rows[k]["lin"]: union(("r", k), ("v", v))
        for w in W: union(("v", w), ("y", wy[w]))
        comp = defaultdict(list)
        for k in qual: comp[find(("r", k))].append(k)
        self.J = {}; self.qrows = {}; out_of = {}
        for idx, (root, ks) in enumerate(sorted(comp.items(), key=lambda t: min(t[1]))):
            j = f"j{idx}"; self.qrows[j] = ks
        root_to_j = {find(("r", ks[0])): j for j, ks in self.qrows.items()}
        for v in list(W) + list(Z):
            if ("v", v) in parent and find(("v", v)) in root_to_j:
                out_of[v] = root_to_j[find(("v", v))]
        unit0 = [k for k, r in rows.items() if k >= 0 and not r["quad"] and k not in qual and k not in simplex]
        for v in Z:
            if v in out_of: continue
            for k in unit0:
                others = [u for u in rows[k]["lin"] if u != v]
                if v in rows[k]["lin"] and others and all(u in out_of for u in others) and len({out_of[u] for u in others}) == 1:
                    out_of[v] = out_of[others[0]]; break
        Z = {v for v in Z if v in out_of}
        # rows with differing supports per output: extend each quality row to the output's flows (zero coefficients)
        unit = [k for k, r in rows.items() if k >= 0 and not r["quad"] and k not in qual and k not in simplex]
        flows = W | Z
        # input identity: a unit capacity row whose flows leave one input. Identify inputs by q-var groups:
        # each q var is (input, pool); inputs are identified through capacity rows containing w's of that q.
        cap_rows = {k: set(rows[k]["lin"]) for k in unit}
        # output capacity rows: support == all flows into an output
        into = defaultdict(set)
        for v in flows: into[out_of[v]].add(v)
        self.J = {j: dict(name=j, lower=0, upper=None, price=0.0) for j in into}
        pool_rows = {}
        input_rows = []
        for k, s in cap_rows.items():
            outs = {out_of[v] for v in s}
            if len(outs) == 1 and s == into[next(iter(outs))]:
                self.J[next(iter(outs))]["upper"] = rows[k]["ub"]; continue
            if s <= W and len({pool_of_q[wq[v]] for v in s}) == 1 and s == {w for w in W if pool_of_q[wq[w]] == pool_of_q[wq[next(iter(s))]]}:
                pool_rows[pool_of_q[wq[next(iter(s))]]] = rows[k]["ub"]; continue
            input_rows.append(k)
        # inputs: each input row groups flows from one input
        inp_of = {}
        self.I = {}
        for idx, k in enumerate(input_rows):
            i = f"i{idx}"; self.I[i] = dict(name=i, lower=0, upper=rows[k]["ub"], price=0.0)
            for v in cap_rows[k]: inp_of[v] = i
        # flows not in any input row belong to uncapacitated inputs: identify by q var
        for w in W:
            if w not in inp_of:
                i = f"iq{wq[w]}"; self.I.setdefault(i, dict(name=i, lower=0, upper=None, price=0.0)); inp_of[w] = i
        for v in Z:
            if v not in inp_of:
                i = f"iz{v}"; self.I.setdefault(i, dict(name=i, lower=0, upper=None, price=0.0)); inp_of[v] = i
        self.L = {l: pool_rows.get(l, float("inf")) for l in set(pool_of_q.values())}
        self.IL, self.LJ, self.IJ = {}, {}, {}
        self.cpath, self.cIJ = {}, {}
        self.cIL = defaultdict(float); self.cLJ = defaultdict(float)
        obj = rows[-1]["lin"]
        self.inl = defaultdict(list)
        self.qvar = {}
        self.idx_w, self.idx_q, self.idx_y, self.idx_z = {}, {}, {}, {}
        for w in W:
            i, l, j = inp_of[w], pool_of_q[wq[w]], out_of[w]
            assert (i, l, j) not in self.idx_w
            self.idx_w[(i, l, j)] = w; self.idx_q[(i, l)] = wq[w]; self.idx_y[(l, j)] = wy[w]
            if (i, l) not in self.IL:
                self.IL[(i, l)] = d["ub"][wq[w]] if d["ub"][wq[w]] < float("inf") else 1.0
                self.inl[l].append(i)
            self.LJ[(l, j)] = d["ub"][wy[w]]
            self.cpath[(i, l, j)] = obj.get(w, 0.0)
        for v in Z:
            assert (inp_of[v], out_of[v]) not in self.idx_z
            self.idx_z[(inp_of[v], out_of[v])] = v
            self.IJ[(inp_of[v], out_of[v])] = d["ub"][v]; self.cIJ[(inp_of[v], out_of[v])] = obj.get(v, 0.0)
        # quality coefficients
        self.K = list(range(max(len(v) for v in self.qrows.values())))
        self.attrs = {j: [(a, "G") for a in range(len(self.qrows[j]))] for j in self.J}
        self.gam = {}
        flow_of = {}
        for w in W: flow_of[w] = (inp_of[w], out_of[w])
        for v in Z: flow_of[v] = (inp_of[v], out_of[v])
        for j, ks in self.qrows.items():
            for a, k in enumerate(ks):
                for v, cf in rows[k]["lin"].items():
                    i, j2 = flow_of[v]
                    old = self.gam.get((i, j, a))
                    assert old is None or abs(old - cf) < 1e-9, "gamma must depend on (input, output) only"
                    self.gam[(i, j, a)] = cf
        self.nvar_check = (len(W), len(Z), len(Qv), len(Yv))

    def gamma(self, i, j, a):
        return self.gam.get((i, j, a[0]), 0.0)


if __name__ == "__main__":
    P = SppInst(sys.argv[1])
    print(P.name, "I", len(P.I), "L", len(P.L), "J", len(P.J), "K", len(P.K), "IL", len(P.IL), "LJ", len(P.LJ), "IJ", len(P.IJ), P.nvar_check)
    m = I.build_pq(P)[0]; m.optimize(); print("pq LP bound", m.ObjVal)
