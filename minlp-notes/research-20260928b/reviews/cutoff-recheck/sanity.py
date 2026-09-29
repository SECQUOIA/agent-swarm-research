"""Sanity checks of iprop.py: representations equal f; pi_D of the endpoint
example by bisection; one-round recursion of Proposition 3.9."""
import math
import sympy as sp
import iprop as P
import inst as I


def pi_bisect(dag, box, lo, hi, it=50, maxr=200000):
    """Largest c (to resolution) with nonempty fixed point; 'limit' counts as nonempty."""
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        st, _, _ = P.fixpoint(dag, box, mid, max_rounds=maxr)
        if st == 'empty':
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


if __name__ == '__main__':
    reps = dict(endpoint=I.endpoint(), lin_exp=I.linediag('exp'), lin_s=I.linediag('s'),
                rot1_exp=I.rot(1.0, 'exp'), rot1_st=I.rot(1.0, 'st'), line3_st=I.line3_st(),
                iso2=I.iso2(), nd1_mono=I.nondeg1('mono'), nd1_u=I.nondeg1('u'), cnd1=I.cnd1())
    for k, v in reps.items():
        print(f'rep {k:9s}: max |DAG - f| on 200 points = {I.check_rep(v):.1e}')
    E = I.endpoint()
    for box in ([(-1.0, 1.0)], [(-0.1, 0.1)], [(-0.1, 0.3)], [(0.2, 0.5)]):
        print(f'endpoint example: pi_D({box[0]}) = {pi_bisect(E["dag"], box, -2, 2):+.6f}')
    # Proposition 3.9 recursion, one round at a time
    a, eps = 1.0, 1e-3
    dag = I.quad(a)
    x, y = 0.2, 0.15
    Z = P.z0(dag, [(a - y, a + x)])
    worst = 0.0
    for r in range(8):
        st, Z, _ = P.run(dag, Z, -eps, 1)
        xn = math.sqrt(a * a + 2 * a * x - eps) - a
        yn = y - (y * y + eps) / (2 * a)
        lo, hi = P.xbox(dag, Z)[0]
        worst = max(worst, abs(hi - a - xn), abs(a - lo - yn))
        x, y = xn, yn
    print(f'Prop 3.9 one-round recursion vs propagator, 8 rounds: max deviation {worst:.1e}')
