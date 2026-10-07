"""Statistics of a cell-slope state: cells, slopes, SCIP evaluations, records.

usage: python3 stats_cs.py state.pkl [state0.pkl]
"""
import pickle
import sys

import numpy as np

import cs  # noqa: F401


def evals_summary(st):
    n, cpu = 0, 0.0
    for key, d in st.evals.items():
        for sk, ev in d.items():
            n += 1
            cpu += ev.get("time", 0.0) or 0.0
    return n, cpu


def main():
    st = cs.load(sys.argv[1])
    base = cs.load(sys.argv[2]) if len(sys.argv) > 2 else None
    T = st.T
    print("leaves per link", [len(l) for l in st.leaves])
    for l in range(T - 1):
        lam = st.lam_arr(l)
        d = lam - np.array(st.base[l])
        lo, hi = st.boxes(l)
        w = hi - lo
        print(f"link {l}: distinct slopes {len({tuple(x) for x in lam})}; |slope - wave2| median "
              f"{np.round(np.median(np.abs(d), 0), 2).tolist()} max {np.round(np.abs(d).max(0), 2).tolist()}; "
              f"slope range tank1 [{lam[:, 0].min():.1f}, {lam[:, 0].max():.1f}] tank2 [{lam[:, 1].min():.1f}, "
              f"{lam[:, 1].max():.1f}] tank3 [{lam[:, 2].min():.1f}, {lam[:, 2].max():.1f}]; leaf widths median "
              f"{np.round(np.median(w, 0), 3).tolist()} max {np.round(w.max(0), 3).tolist()}")
    n, cpu = evals_summary(st)
    print(f"SCIP evaluations stored {n}, cpu {cpu:.0f}s; pool points {[len(p) for p in st.pts]}")
    if base is not None:
        n0, cpu0 = evals_summary(base)
        print(f"  of which new (not in {sys.argv[2]}): {n - n0}, cpu {cpu - cpu0:.0f}s")
    src = {}
    for r in st.recs:
        k = r.get("src", ("cert3",))[0]
        s = src.setdefault(k, dict(n=0, cpu=0.0, nodes=0, maxt=0.0, below=0, inf=0))
        s["n"] += 1
        s["cpu"] += r.get("time", 0.0)
        s["nodes"] += r.get("nodes", 0)
        s["maxt"] = max(s["maxt"], r.get("time", 0.0))
        s["below"] += int(r["bound"] < r.get("target", -np.inf))
        s["inf"] += int(r["bound"] == np.inf)
    for k, s in src.items():
        print(f"records {k}: {s['n']} runs, cpu {s['cpu']:.0f}s, max {s['maxt']:.0f}s, nodes {s['nodes']}, "
              f"below target {s['below']}, proved empty {s['inf']}")


if __name__ == "__main__":
    main()
