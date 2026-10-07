"""Write a primal point as a .sol file and check it at 50 digits on the OSIL model with
open-instances-wave2/small/ev.py (decimal-preserving reader; independent of egdata/egfast).

The decision variables are the doubles found by the search, written exactly (repr); objvar is
max_k (c_k + g_k(x)) evaluated at 60 digits and rounded up at the 20th significant digit, so
every objective row holds.

    python3 verify_primal.py <name> <x1,...,x7>       (or <name> <result.npz>)
"""
import os
import sys

import mpmath as mp
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "open-instances-wave2", "small"))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "reviews", "open-instances-verification"))
import ev  # noqa: E402
import osilx  # noqa: E402


def main(name, spec):
    if spec.endswith(".npz"):
        x = [float(v) for v in np.load(spec)["xbest"]]
    else:
        x = [float(v) for v in spec.split(",")]
    I = ev.load(name)
    names = I["names"]
    objv = [j for j, n in enumerate(names) if n == "objvar"][0]
    dv = [j for j in range(len(names)) if j != objv]
    vals = {}
    for j, v in zip(dv, x):
        if I["vt"][j] == "I":
            assert v == round(v)
            vals[names[j]] = str(int(round(v)))
        else:
            vals[names[j]] = repr(v)
    # objvar: max over objective rows of (row lb + g) at 60 digits, rounded up
    with mp.workdps(60):
        xx = [mp.mpf(vals[n]) if n != "objvar" else mp.mpf(0) for n in names]
        need = mp.mpf("-inf")
        for c in I["cons"]:
            if "objvar" in [names[j] for j in c["lin"]]:
                # row: objvar + nl(x) >= lb  -> objvar >= lb - nl(x)
                v = osilx.ev_row(c, xx, ev.mpnum, ev.MPFNS)          # value with objvar = 0
                need = max(need, mp.mpf(c["lb"]) - v)
        s = mp.nstr(need, 20, strip_zeros=False)
        o = mp.mpf(s)
        if o < need:
            o = o + mp.mpf(10) ** (mp.floor(mp.log10(abs(o))) - 19)
        vals["objvar"] = mp.nstr(o, 20, strip_zeros=False)
    os.makedirs(os.path.join(HERE, "sol"), exist_ok=True)
    path = os.path.join(HERE, "sol", f"{name}.retry.sol")
    with open(path, "w") as f:
        for n in names:
            f.write(f"{n:34s}{vals[n]}\n")
    r = ev.evaluate(I, [vals[n] for n in names], 50)
    print(f"{name}: wrote {path}")
    print(f"  objective {mp.nstr(r['obj'], 20)}; max row violation {mp.nstr(r['row_viol'], 3)} ({r['worst_row']}); "
          f"max bound violation {mp.nstr(r['bound_viol'], 3)} ({r['worst_var']})")
    print(f"  point: {[vals[n] for n in names]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
