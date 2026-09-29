"""Phase-segment accounting: for each omega phase P (maximal run of splits along one coordinate
with the other interval frozen), n_P = number of certificate boxes meeting the phase segment
(A x {h} for an x-phase with frozen z-minimizer h).  Reports sum_P n_P / N_cert and max_C
(#phases whose segment meets C), using the exact grid-optimal guillotine certificate.
usage: python3 exp4.py FAMILY [G]"""
import sys
from fractions import Fraction as Fr
from sepexact import run, guill_grid
import fam
from exp1 import family


def phase_segments(res):
    seg = {}
    for box, y, i, ph in res["internal"]:
        if ph not in seg:
            j = 1 - i
            seg[ph] = (i, box[i], y[j])   # coordinate split, interval of phase root, frozen height
    return seg


def meets(C, i, A, h):
    j = 1 - i
    return C[j][0] <= h <= C[j][1] and C[i][0] < A[1] and A[0] < C[i][1]


if __name__ == "__main__":
    name = sys.argv[1]
    G = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    for k in (3, 4, 5, 6, 7, 8):
        eps = Fr(1, 10 ** k)
        c1, c2 = family(name, eps)
        ro = run([c1, c2], eps, "omega", record=True)
        cuts = fam.cut_positions(ro)
        g = []
        for c, cu in zip((c1, c2), cuts):
            pts = {c.L, c.U} | cu
            extra = fam.greedy_multi(c, eps, K=10)
            pts = set(fam.thin(sorted(pts), G // 2)) | set(fam.thin(sorted(extra), G - G // 2))
            g.append(fam.thin(sorted(pts), G))
        N, cert = guill_grid(c1, c2, g[0], g[1], eps)
        seg = phase_segments(ro)
        tot = 0
        per = [0] * len(cert)
        for ph, (i, A, h) in seg.items():
            for q, C in enumerate(cert):
                if meets(C, i, A, h):
                    tot += 1
                    per[q] += 1
        print(f"{name} eps=1e-{k} N={N} omega_internal={len(ro['internal'])} phases={len(seg)} "
              f"sum_nP={tot} sum_nP/N={tot/N:.2f} max_phases_per_box={max(per)}", flush=True)
