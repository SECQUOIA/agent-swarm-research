"""Treewidth census of MINLPLib instances (upper bounds by min-degree elimination).
Graphs: primal (vars in a common row form a clique), incidence (bipartite var-row),
and nonlinear primal (only nonlinear terms: quadratic pairs, nl-expression variable sets).
"""
import sys, os, json, glob, heapq, time
from pathlib import Path
_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "research-20260922/scouting/minlplib-open-data"))
from osil import read, V
OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")

def min_degree_width(adj, limit=None, tmax=60):
    """adj: dict node->set. Returns an upper bound on treewidth via min-degree elimination
    (lazy heap). Stops early if width exceeds limit or time exceeds tmax (returns None)."""
    adj = {v: set(nb) for v, nb in adj.items()}
    heap = [(len(nb), v) for v, nb in adj.items()]; heapq.heapify(heap)
    width = 0; t0 = time.time(); alive = set(adj)
    while heap:
        d, v = heapq.heappop(heap)
        if v not in alive or d != len(adj[v]): continue
        width = max(width, d)
        if limit is not None and width > limit: return None
        if time.time() - t0 > tmax: return None
        nb = list(adj[v])
        for a in nb:
            adj[a].discard(v)
        for i, a in enumerate(nb):
            for b in nb[i+1:]:
                if b not in adj[a]:
                    adj[a].add(b); adj[b].add(a)
        for a in nb: heapq.heappush(heap, (len(adj[a]), a))
        alive.discard(v); del adj[v]
    return width

def degeneracy(adj):
    """A treewidth lower bound: the degeneracy (max over subgraphs of min degree) is <= tw? No:
    degeneracy is a LOWER bound for tw? tw >= degeneracy is true (min degree of minors)."""
    adj = {v: set(nb) for v, nb in adj.items()}
    heap = [(len(nb), v) for v, nb in adj.items()]; heapq.heapify(heap)
    best = 0; alive = set(adj)
    while heap:
        d, v = heapq.heappop(heap)
        if v not in alive or d != len(adj[v]): continue
        best = max(best, d)
        for a in adj[v]:
            adj[a].discard(v); heapq.heappush(heap, (len(adj[a]), a))
        alive.discard(v); del adj[v]
    return best

def split_terms(t):
    """Top-level additive terms of an expression tree."""
    if t[0] == "sum":
        out = []
        for c in t[1:]: out += split_terms(c)
        return out
    if t[0] == "negate": return split_terms(t[1])
    return [t]

def graphs(I):
    """rowvars: variable set per row (pure incidence).
    nlsets: variable sets of nonlinear terms (quadratic pairs, additive terms of nl expressions).
    rowterms: per row, (linear variables, list of nonlinear-term variable sets)."""
    n = len(I["lb"]); rowvars = []; nlsets = []; rowterms = []
    for r, row in I["rows"].items():
        vs = set(row["lin"]); terms = []
        for (a, b, c) in row["quad"]:
            vs.add(a); vs.add(b); terms.append({a, b})
        if row["nl"] is not None:
            for tt in split_terms(row["nl"]):
                s = V(tt)
                if s: terms.append(set(s)); vs |= s
        # linear-looking terms inside nl expressions with one variable are harmless
        nlsets += [s for s in terms if len(s) >= 1]
        if vs:
            rowvars.append(vs); rowterms.append((set(row["lin"]), terms))
    return n, rowvars, nlsets, rowterms

def factor_incidence(n, rowterms):
    """Nodes: variables 0..n-1, row nodes, term nodes. Row -- linear vars and term nodes;
    term -- its variables. Single-variable terms attach directly to the row."""
    adj = {}; nxt = n
    def add(a, b):
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    for lin, terms in rowterms:
        rnode = nxt; nxt += 1; adj.setdefault(rnode, set())
        for v in lin: add(rnode, v)
        for s in terms:
            if len(s) == 1:
                add(rnode, next(iter(s)))
            else:
                tn = nxt; nxt += 1
                add(rnode, tn)
                for v in s: add(tn, v)
    return adj

def primal(n, sets):
    adj = {}
    for s in sets:
        s = list(s)
        for v in s: adj.setdefault(v, set())
        for i, a in enumerate(s):
            for b in s[i+1:]:
                if a != b: adj[a].add(b); adj[b].add(a)
    return adj

def incidence(n, sets):
    adj = {}
    for k, s in enumerate(sets):
        rnode = n + k; adj[rnode] = set()
        for v in s:
            adj.setdefault(v, set()).add(rnode); adj[rnode].add(v)
    return adj

def main(names, out):
    with open(out, "a") as fo:
        for nm in names:
            p = os.path.join(OSIL_DIR, nm + ".osil")
            if not os.path.exists(p): continue
            try:
                I = read(p)
            except Exception as e:
                fo.write(json.dumps({"name": nm, "error": str(e)[:100]}) + "\n"); continue
            n, rowvars, nlsets, rowterms = graphs(I)
            nlvars = set().union(*nlsets) if nlsets else set()
            if not nlvars: continue
            nint = sum(1 for t in I["vt"] if t in ("B", "I"))
            maxrow = max((len(s) for s in rowvars), default=0)
            rec = {"name": nm, "n": n, "nint": nint, "m": len(rowvars), "n_nl": len(nlvars), "maxrow": maxrow}
            gf = factor_incidence(n, rowterms); rec["tw_fac_ub"] = min_degree_width(gf, tmax=90)
            rec["fac_degeneracy_lb"] = degeneracy(gf)
            gn = primal(n, [s for s in nlsets if len(s) >= 2]); rec["tw_nlprimal_ub"] = min_degree_width(gn, tmax=60) if gn else 0
            rec["nlprimal_degeneracy_lb"] = degeneracy(gn) if gn else 0
            fo.write(json.dumps(rec) + "\n"); fo.flush()

if __name__ == "__main__":
    names = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(OSIL_DIR, "*.osil")))
    k, K = int(sys.argv[1]), int(sys.argv[2])
    main(names[k::K], f"census_part{k}.jsonl")
