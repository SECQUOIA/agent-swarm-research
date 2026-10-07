"""Reviewer check: split the LS-versus-oracle size difference of Section C.2 of extension-adaptive.md
into a slope part and an incumbent part.

For each random instance: run LS; take its final pass's slopes lam_LS and the incumbent it started that
pass with (UBD_0 at the point xbest). Then run single passes with
  (A) exact slopes lam*, exact incumbent (x0 = x*)          -- the note's "oracle";
  (B) LS slopes lam_LS,  exact incumbent                    -- slope effect only;
  (C) exact slopes lam*, LS's starting incumbent xbest      -- incumbent effect only;
  (D) LS slopes lam_LS,  LS's starting incumbent            -- should reproduce LS's final pass.
"""
import sys
import time
import numpy as np
import indep_ls as R


def main():
    n = int(sys.argv[1])
    eps = float(sys.argv[2])
    for seed in (0, 1):
        c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
        xs, fs, _ = R.global_min_indep(n, c)
        lams = R.slopes(xs, c)
        t0 = time.time()
        res, _ = R.ls(n, c, eps, np.zeros(n), pmax=30)
        st = res["start"]
        nu = float(np.linalg.norm(st["lam"] - lams))
        print("seed %d n=%d: LS size=%d (pass %d); final-pass slopes nu=%.3e; incumbent at pass start "
              "UBD0-f*=%.3e (%.2f eps); final UBD-f*=%.3e  [%.1fs]" % (
                  seed, n, res["size"], res["p"], nu, st["UBD"] - fs, (st["UBD"] - fs) / eps, res["UBD"] - fs,
                  time.time() - t0), flush=True)
        base = None
        for tag, lam, x0 in (("A exact slopes, exact inc", lams, xs),
                             ("B LS slopes,    exact inc", st["lam"], xs),
                             ("C exact slopes, LS inc   ", lams, st["xbest"]),
                             ("D LS slopes,    LS inc   ", st["lam"], st["xbest"])):
            r, _ = R.ls(n, c, eps, x0.copy(), pmax=30, fixed_lam=lam)
            base = base or r["size"]
            print("   %s: size=%7d level=%s pairs=%8d  size/oracle=%.3f" % (
                tag, r["size"], r["i"], r["npairs"], r["size"] / base), flush=True)


if __name__ == "__main__":
    main()
