"""Referee check 3b: run the AUTHORS' robust_bb.bb on gadget chains with the base split of Theorem 4.2
(all unary terms in the gadget factors: u(x_g) and c y_g^2 in (x_g,y_g), u(z_g) in (y_g,z_g), nothing in the
connecting factor) instead of the default balanced base, which puts half of the non-polynomial u(z_g) into
the connecting factor (z_g, x_{g+1}).  For class a this is immaterial (u_i in S_i); for b_d it is not.
Usage: python3 check3b_authors_base.py CLS G1 G2 ..."""
import sys, time
sys.path.insert(0, "../../theory-robust-lb")
import robust_bb as R

def theorem_base(n, base):
    # factor e joins variables e, e+1; variable index mod 3: 0 = x, 1 = y, 2 = z
    w = []
    for e in range(n - 1):
        k = e % 3
        if k == 0:        # (x_g, y_g): all of u(x_g), all of c y_g^2
            w.append((1.0, 1.0))
        elif k == 1:      # (y_g, z_g): all of u(z_g)
            w.append((0.0, 1.0))
        else:             # (z_g, x_{g+1}): nothing
            w.append((0.0, 0.0))
    return w

R.base_weights = theorem_base
cls = sys.argv[1]
for G in map(int, sys.argv[2:]):
    t0 = time.time()
    r = R.bb(R.gadget_chain(G), cls, 1e-4, base="theorem")
    print("authors' code, theorem base split: cls=%s G=%d n=%d %s (%.1fs)" % (cls, G, 3 * G, r, time.time() - t0), flush=True)
