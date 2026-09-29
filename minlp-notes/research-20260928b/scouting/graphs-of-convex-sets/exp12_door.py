"""Exp 12: region formulation vs door (line-graph) formulation on the ring and on
simply connected corridors. Door gap is certified from above by randomized rounding:
gap_door <= (UB - REL_door)/UB, UB = best convex restriction over sampled paths."""
import numpy as np
from gcs import relax, path_cost
from mp import MP
from door import door_inst
from exp8_mp import ring, simply_connected
from exp9_corridor import corridor


def rounding_ub(I, y, rng, samples=60):
    out = {}
    for (u, v), val in y.items():
        if val > 1e-6:
            out.setdefault(u, []).append(((u, v), val))
    best, seen = np.inf, set()
    for _ in range(samples):
        v, path = I.s, [I.s]
        while v != I.t:
            opts = [(e, w) for e, w in out.get(v, []) if e[1] not in path]
            if not opts:
                break
            p = np.array([w for _, w in opts]); p /= p.sum()
            e = opts[rng.choice(len(opts), p=p)][0]
            v = e[1]; path.append(v)
        if v != I.t or tuple(path) in seen:
            continue
        seen.add(tuple(path))
        best = min(best, path_cost(I, path))
    return best


if __name__ == "__main__":
    rng = np.random.default_rng(0); rr = np.random.default_rng(1)
    for eps in [0.0, 0.2]:
        m = ring(eps); I = door_inst(m)
        r, sol = relax(I, return_sol=True); ub = rounding_ub(I, sol['y'], rr)
        print(f"ring eps={eps}: region OPT={m.exact():.4f}; door REL={r:.4f} UB={ub:.4f} gap<={(ub-r)/ub:.3%}", flush=True)
    rows = []
    for trial in range(40):
        boxes, pts = corridor(rng, legs=rng.integers(2, 4), W=rng.uniform(0.8, 2.0))
        B = [(np.array(a), np.array(b)) for a, b in boxes]
        if not simply_connected(B):
            continue
        m = MP(boxes, pts[0], pts[-1], two_cycle=True)
        if not m.paths() or len(m.paths()) > 3000:
            continue
        I = door_inst(m)
        rR, _ = m.relax(); oR = m.exact()
        rD, sol = relax(I, return_sol=True); ub = rounding_ub(I, sol['y'], rr)
        rows.append(((oR - rR)/oR, (ub - rD)/ub, (oR - ub)/oR, (oR - rD)/oR))
        print(f"regions={len(boxes):2} doors={len(I.sets)-2:2} |E|={len(I.edges):3} region gap={(oR-rR)/oR:.3%} "
              f"door gap<={(ub-rD)/ub:.3%} (OPT_region-UB_door)/OPT_region={(oR-ub)/oR:.3%}", flush=True)
    rows = np.array(rows)
    print(f"n={len(rows)} mean region gap={rows[:,0].mean():.3%} mean door gap<={rows[:,1].mean():.3%} "
          f"max door gap<={rows[:,1].max():.3%} #door certified exact(1e-4)={np.sum(rows[:,1]<1e-4)}; "
          f"(OPT_region-REL_door)/OPT_region mean {rows[:,3].mean():.3%}")
