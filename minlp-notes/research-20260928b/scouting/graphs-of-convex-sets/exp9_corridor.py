"""Exp 9: simply connected zigzag corridors covered by overlapping boxes with parallel
lanes (forks/merges) and bends. Test exactness of the order-1 MP-GCS relaxation."""
import numpy as np, sys
from mp import MP
from exp8_mp import simply_connected

def corridor(rng, legs, W):
    # centre-line polyline with axis-aligned legs, alternating direction, turning left/right
    pts = [np.zeros(2)]; dirs = [np.array([1., 0.]), np.array([0., 1.])]
    d = 0; boxes = []
    for k in range(legs):
        L = rng.uniform(2.0, 4.0)
        dv = dirs[k % 2] * (1 if (k % 2 == 0 or rng.random() < 0.5) else -1)
        p0 = pts[-1]; p1 = p0 + L*dv
        pts.append(p1)
        lo = np.minimum(p0, p1) - W/2; hi = np.maximum(p0, p1) + W/2
        # split leg into two lanes across its width, plus the full-width leg box with prob 0.5
        ax = 1 if abs(dv[0]) > 0 else 0   # transverse axis
        mid = (lo[ax] + hi[ax])/2 + rng.uniform(-0.2, 0.2)*W
        l1lo, l1hi = lo.copy(), hi.copy(); l1hi[ax] = mid + rng.uniform(0, 0.1)*W
        l2lo, l2hi = lo.copy(), hi.copy(); l2lo[ax] = mid - rng.uniform(0, 0.1)*W
        boxes += [(l1lo, l1hi), (l2lo, l2hi)]
        if rng.random() < 0.4: boxes.append((lo, hi))
        # random extra sub-box inside the leg
        if rng.random() < 0.5:
            a = rng.uniform(lo, hi); b = rng.uniform(lo, hi)
            boxes.append((np.minimum(a, b), np.maximum(a, b)))
    return boxes, pts

if __name__ == "__main__":
    rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    TWO = len(sys.argv) > 2 and sys.argv[2] == "two"
    res = []
    for trial in range(40):
        boxes, pts = corridor(rng, legs=rng.integers(2, 4), W=rng.uniform(0.8, 2.0))
        B = [(np.array(a), np.array(b)) for a, b in boxes]
        if not simply_connected(B): continue
        m = MP(boxes, pts[0], pts[-1], two_cycle=TWO)
        if not m.paths(): continue
        if len(m.paths()) > 3000: continue
        r, y = m.relax(); o = m.exact()
        g = (o - r)/o
        res.append(g)
        frac = sum(1 for v in y.values() if 1e-4 < v < 1 - 1e-4)
        print(f"regions={len(boxes):2} paths={len(m.paths()):4} REL={r:.4f} OPT={o:.4f} relgap={g:.3%} fractional_edges={frac}")
    res = np.array(res)
    print(f"n={len(res)} #gap>1e-4: {(res>1e-4).sum()} max={res.max():.3%}")
