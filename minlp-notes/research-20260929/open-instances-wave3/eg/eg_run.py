"""Best-first rigorous B&B for the eg_* instances with the eg_bb.Prob bounds (natural interval
enclosure of each Gaussian-sum row intersected with its mean-value form; objective lower
bound = max over objective rows; side rows prune).  Time-limited: the result is the certified
global lower bound at the time limit (min over open and discarded boxes).

    python3 eg_run.py <name> <time_limit_s>
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os
import sys
import time

import numpy as np

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
import bbcore  # noqa: E402
import ev  # noqa: E402

import eg_bb as eb  # noqa: E402


def make_fn(P):
    def fn(lo, hi):
        lb, G, enc = P.bound(lo, hi)
        c = 0.5 * (lo + hi)
        c[:, P.isint] = np.clip(np.round(c[:, P.isint]), lo[:, P.isint], hi[:, P.isint])
        c = np.clip(c, P.lo_in, P.hi_in)
        fc, _ = P.fpoint(c)
        Gm = np.stack([np.maximum(np.abs(g.lo), np.abs(g.hi)).max(axis=1) for g in G], axis=1)
        return dict(lb=lb, ub=fc, x=c, smear=Gm * (hi - lo))
    return fn


def main(name, tlim):
    P = eb.Prob(name)
    here = os.path.dirname(os.path.abspath(__file__))
    vals = ev.read_sol(os.path.join(here, "..", "sol", f"{name}.p1.sol"))
    x0 = np.array([float(vals.get(n, "0")) for n in P.M["names"]])
    xl = eb.local_minimax(P, x0)
    fl, _ = P.fpoint(xl[None, :])
    print(f"== {name}: polished listed point: rigorous F = {fl[0]!r} at {xl.tolist()}", flush=True)
    UB = float(fl[0])
    t0 = time.time()
    r = bbcore.run(make_fn(P), P.lo0, P.hi0, 1e-9 * max(1.0, abs(UB)) if np.isfinite(UB) else 1e-8, tlim,
                   UB=UB, xbest=xl, batch=400, isint=P.isint, log_every=25, mode="best")
    print(f"B&B: done={r['done']} processed {r['processed']} open {r['open']} time {r['time']:.0f}s")
    print(f"  certified lower bound {r['LB']!r}; best point value {r['UB']!r} at {r['x'].tolist()}")


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]))
