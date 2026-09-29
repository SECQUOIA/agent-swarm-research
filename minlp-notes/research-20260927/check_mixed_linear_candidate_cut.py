"""Exact targeted checks of mixed-linear approximate primal-dual cuts.

Finite checks and identities only; not an implementation of the FPT
integer-query algorithm or the general weak-optimization subroutines.
"""

from fractions import Fraction as Q


def one_sided_case(z, perturb, scale=Q(1), duplicate=False):
    # f(z,y)=(z^2+y^2)/2, fiber y>=z. The rescaled inequality is
    # scale*z-scale*y<=0. Extra duplicates do not change the fiber.
    p = max(Q(0), z)
    yhat = p + perturb
    assert yhat >= z
    slack = scale * (yhat-z)
    true_multiplier = p/scale
    assert true_multiplier*slack == p*(yhat-p)
    # E(lambda)=slack*lambda+(yhat-scale*lambda)^2/2.
    lam = max(Q(0), z/scale)
    residual = yhat-scale*lam
    error = lam*slack + residual**2/2
    q = z+scale*lam
    if duplicate:
        # Split a nonunique multiplier across duplicate active rows.
        l1, l2 = lam/Q(3), 2*lam/Q(3)
        assert l1+l2 == lam
        assert (l1+l2)*slack+(yhat-scale*(l1+l2))**2/2 == error
    assert error <= Q(1, 4)
    gz = (z*z+p*p)/2
    for w in map(Q, range(-5, 6)):
        pw = max(Q(0), w)
        gw = (w*w+pw*pw)/2
        assert gw-gz >= q*(w-z)+(w-z)**2/2-error
        if w != z:
            assert gw-gz >= q*(w-z)+(w-z)**2/4
            if gw <= gz:
                assert q*(w-z) <= -Q(1, 4)
    return true_multiplier


def equality_fiber(z):
    # y=z encoded by two opposite inequalities; every fiber has empty
    # interior in R. f=(z^2+y^2)/2, multiplier need not be unique.
    yhat = z
    lam_lower = max(z, Q(0))
    lam_upper = max(-z, Q(0))
    residual = yhat-lam_lower+lam_upper
    assert residual == 0
    q = z+lam_lower-lam_upper
    assert q == 2*z
    for shift in (Q(0), Q(7), Q(10**20)):
        assert yhat-(lam_lower+shift)+(lam_upper+shift) == 0
    for w in map(Q, range(-5, 6)):
        assert w*w-z*z >= q*(w-z)+(w-z)**2/2


def farkas_projection():
    # y>=z and y<=-z project exactly to z<=0. The two row multipliers
    # alpha=(1,1) cancel the y coefficient and give 2z<=0.
    a = (Q(1), Q(1))
    b = (Q(-1), Q(1))
    alpha = (Q(1), Q(1))
    assert sum(x*y for x, y in zip(alpha, b)) == 0
    projected_normal = sum(x*y for x, y in zip(alpha, a))
    for z in map(Q, range(-5, 6)):
        if z > 0:
            assert projected_normal*z > 0
        else:
            assert z <= 0 <= -z
            assert projected_normal*z <= 0


def residual_constants():
    for mu in (Q(1, 100), Q(1), Q(100)):
        for gradient in (Q(0), Q(1), Q(10**30)):
            for lipschitz in (Q(1), Q(17), Q(10**15)):
                delta = min(Q(1), mu/(16*(gradient+1)), mu/(4*lipschitz))
                bound = gradient*delta+lipschitz**2*delta**2/(2*mu)
                assert bound <= 3*mu/32
                assert bound+mu/8 <= 7*mu/32 < mu/4


if __name__ == "__main__":
    cases = 0
    for z in map(Q, range(-5, 6)):
        equality_fiber(z)
        for denominator in (100, 1000):
            for scale in (Q(1), Q(1, 10**40), Q(10**40)):
                one_sided_case(z, Q(1, denominator), scale, duplicate=True)
                cases += 1
    huge = one_sided_case(Q(1), Q(1, 1000), Q(1, 10**100))
    assert huge == 10**100
    farkas_projection()
    residual_constants()
    print(f"PASS: {cases} scaled/degenerate constrained-fiber residual cuts.")
    print("PASS: equality fibers, redundant multipliers, Farkas projection, E constants.")
    print("PASS: multiplier 10^100 with scale-independent residual bound.")
