"""Keyed randomization on the kink families (companion to sim_kink.py): E[T] and quantiles."""
import json
import random
import sys
import zlib

from sim_kink import run1d, run2d, parse, stats

if __name__ == "__main__":
    out = sys.argv[1]
    with open(out, "w") as fh:
        for a in (1 / 6, 3 / 238, 0.1999, 0.25, 1 / 3):
            for r in ("kclip:0.1:0.3", "kclip:0.05:0.35"):
                rule = parse(r)
                for model, sel, EPS, reps in (("1d", "x", [1e-2, 1e-4, 1e-8, 1e-16, 1e-32], 20000),
                                              ("2d", "w", [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8], 1000)):
                    for eps in EPS:
                        rng = random.Random(zlib.crc32(repr((a, r, model, eps)).encode()))
                        Ts = []
                        for _ in range(reps):
                            rng.keyed = {}
                            Ts.append(run1d(a, eps, rule, rng)[0] if model == "1d" else run2d(a, eps, rule, sel, rng))
                        capped = sum(t is None for t in Ts)
                        Ts = [t for t in Ts if t is not None]
                        fh.write(json.dumps(dict(model=model, a=a, rule=r, sel=sel, eps=eps, reps=reps,
                                                 capped=capped, **stats(Ts))) + "\n")
                        fh.flush()
                print(a, r, flush=True)
