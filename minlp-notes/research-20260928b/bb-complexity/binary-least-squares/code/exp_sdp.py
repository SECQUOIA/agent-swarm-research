"""E5: SDP relaxation at the root.
(a) Tightness at x*: lambda_min(A'A + diag(x* o A'w)) >= 0 (Prop. 7.1), as a
    function of c = rho/log N, for beta in {1, 1.5, 2, 3, 4}.  Compared with
    the necessary scale 2 log N/beta, the proved sufficient condition
    2 beta log N/(sqrt(beta)-1)^4 and the heuristic 2 beta log N/(beta-1)^2.
(b) Square systems: root gaps of the SDP and box relaxations relative to OPT
    (OPT from box B&B), small N.
Usage: python3 exp_sdp.py OUT.jsonl [a|b]
"""
import sys, json, os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from core import instance, sdp_certificate_eig, sdp_value, box_min, bnb


def part_a(out):
    """Per seed, the exact SDP tightness threshold rho*: with G = H'H/N and
    z = x* o H'w/sqrt(N), tightness at rho <=> G + diag(z)/sqrt(rho) is psd.
    t -> lambda_min(G + t diag z) is concave with value >= 0 at t = 0, so the
    tight set is rho >= rho* = 1/t*^2; t* is found by bisection."""
    for beta in (1.0, 1.5, 2.0, 3.0, 4.0):
        for N in (100, 400, 1600):
            M = int(beta * N)
            ns = 40 if N <= 400 else 10
            for s in range(ns):
                A, y, xs, B, w = instance(N, M, 1.0, s)   # rho = 1: A = H/sqrt(N)
                G = A.T @ A
                z = xs * (A.T @ w)                         # = zeta at rho = 1
                lo, hi = 0.0, 1.0
                while np.linalg.eigvalsh(G + hi * np.diag(z))[0] >= 0:
                    hi *= 2.0
                    if hi > 1e8:
                        break
                for it in range(40):
                    mid = 0.5 * (lo + hi)
                    if np.linalg.eigvalsh(G + mid * np.diag(z))[0] >= 0:
                        lo = mid
                    else:
                        hi = mid
                tstar = lo
                rho_star = np.inf if tstar == 0 else 1.0 / tstar ** 2
                # the diagonal (one-bit, ML) condition alone: G_ii + t z_i >= 0
                neg = z < 0
                t_diag = np.min(np.diag(G)[neg] / (-z[neg])) if neg.any() else np.inf
                out.write(json.dumps(dict(part="a", beta=beta, N=N, M=M, seed=s,
                                          rho_star=float(rho_star), c_star=float(rho_star / np.log(N)),
                                          c_diag=float(1.0 / t_diag ** 2 / np.log(N)))) + "\n")
                out.flush()


def part_b(out):
    for N in (16, 24, 32, 40):
        for tag in ("c2", "c4", "c8", "r4"):
            rho = N / 4 if tag == "r4" else float(tag[1:]) * np.log(N)
            for s in range(6):
                A, y, xs, B, w = instance(N, N, rho, s)
                r = bnb(B, w, rule="maxfrac", max_nodes=200000)
                OPT = r["OPT"]
                R, Rlb, u, ina = box_min(B, w)
                sv, slb = sdp_value(A, y)
                out.write(json.dumps(dict(part="b", N=N, tag=tag, rho=rho, seed=s, done=r["done"],
                                          OPT=OPT, box=R, sdp=sv, sdp_lb=slb,
                                          box_gap_rel=(OPT - R) / OPT, sdp_gap_rel=(OPT - slb) / OPT,
                                          xstar_opt=bool(OPT >= float(w @ w) * (1 - 1e-12)),
                                          eig_cert=sdp_certificate_eig(A, xs, w))) + "\n")
                out.flush()


if __name__ == "__main__":
    with open(sys.argv[1], "a") as out:
        which = sys.argv[2] if len(sys.argv) > 2 else "ab"
        if "a" in which:
            part_a(out)
        if "b" in which:
            part_b(out)
