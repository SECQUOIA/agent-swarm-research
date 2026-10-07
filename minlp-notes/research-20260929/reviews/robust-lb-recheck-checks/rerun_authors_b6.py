"""Rerun of the authors' robust_bb.bb for class b6 on small chains: theorem base split ('gadget')
for G = 1, 2 and the old balanced base split for G = 2 (the superseded 44)."""
import sys, time
sys.path.insert(0, "../../theory-robust-lb")
from robust_bb import gadget_chain, bb
for base, G in [("gadget", 1), ("gadget", 2), ("balanced", 2)]:
    t0 = time.time()
    r = bb(gadget_chain(G), "b6", 1e-4, base=base, fstar=0.0)
    print("authors' bb: cls=b6 base=%s G=%d n=%d %s (%.1fs)" % (base, G, 3 * G, r, time.time() - t0), flush=True)
