"""Families x eps: omega/deficit leaves vs exact guillotine grid optimum; charging statistics.
usage: python3 exp1.py FAMILY [G]"""
import sys
from fractions import Fraction as Fr
from sepexact import run, guill_grid, slice_bound, product_bound
import fam

A, B = Fr(1, 3), Fr(29, 70)


def family(name, eps):
    if name == "sharp_quad":
        return fam.sharp(A), fam.quad(B, 1, rmin=Fr(1, 10 ** 8))
    if name == "quad_quad":
        return fam.quad(A, 1, rmin=Fr(1, 10 ** 8)), fam.quad(B, 1, rmin=Fr(1, 10 ** 8))
    if name == "quad_flatquad":
        return fam.quad(A, 1, rmin=Fr(1, 10 ** 8)), fam.quad(B, Fr(1, 20), rmin=Fr(1, 10 ** 8))
    if name == "caps_quad":
        return fam.caps([Fr(k, 7) for k in range(1, 7)]), fam.quad(B, 1, rmin=Fr(1, 10 ** 8))
    raise ValueError(name)


def charge_stats(res, cert):
    cnt = [0] * len(cert)
    phs = [set() for _ in cert]
    for box, y, i, ph in res["internal"]:
        for k, (bx, bz) in enumerate(cert):
            if bx[0] <= y[0] <= bx[1] and bz[0] <= y[1] <= bz[1]:
                cnt[k] += 1
                phs[k].add(ph)
                break
    return max(cnt), sum(cnt), max(len(p) for p in phs)


if __name__ == "__main__":
    name = sys.argv[1]
    G = int(sys.argv[2]) if len(sys.argv) > 2 else 70
    for k in (3, 4, 5, 6, 7, 8):
        eps = Fr(1, 10 ** k)
        c1, c2 = family(name, eps)
        ro = run([c1, c2], eps, "omega", record=True)
        rd = run([c1, c2], eps, "deficit")
        cuts = fam.cut_positions(ro)
        g = []
        for c, cu in zip((c1, c2), cuts):
            pts = {c.L, c.U} | cu
            extra = fam.greedy_multi(c, eps, K=10)
            pts = set(fam.thin(sorted(pts), G // 2)) | set(fam.thin(sorted(extra), G - G // 2))
            g.append(fam.thin(sorted(pts), G))
        N, cert = guill_grid(c1, c2, g[0], g[1], eps)
        mx, tot, mph = charge_stats(ro, cert)
        print(f"{name} eps=1e-{k} grid={len(g[0])}x{len(g[1])} Ngrid={N} slice={slice_bound([c1,c2],eps)} "
              f"prod={product_bound(c1,c2,eps,16)} omega={ro['leaves']} deficit={rd['leaves']} "
              f"ratio={ro['leaves']/N:.2f} maxcharge/C={mx} maxphases/C={mph} phases={ro['phases']} internal={tot}", flush=True)
