"""Exact finite checks for the finite-aggregation approximation section.

Only Python 3's standard library is needed. These checks cover integer
meshes, Gram realization bounds, aggregate values, and radial identities.
They do not prove the universal pigeonhole argument, asymptotic theorem,
Hausdorff estimates, or conic separation proposition.
"""

from fractions import Fraction as Q


def check_meshes():
    for m in range(1, 65):
        mesh = {(m*m, j*j, 2*m*j) for j in range(m+1)}
        mesh |= {(j*j, m*m, 2*m*j) for j in range(m+1)}
        assert len(mesh) == 2*m+1
        assert (m*m, 0, 0) in mesh and (0, m*m, 0) in mesh
        for a, b, c in mesh:
            assert c*c == 4*a*b
            assert 0 <= min(a, b, c) <= max(a, b, c) <= 2*m*m
        # Adjacent rational slopes on the first half-interval.
        slopes = [Q(j, m) for j in range(m+1)]
        assert all(t-s == Q(1, m) for s, t in zip(slopes, slopes[1:]))
    return 64


def check_witnesses():
    count = 0
    for n in (2, 3, 5, 9, 17, 33):
        eta = Q(1, 400*n*n)
        a = 1+10*eta
        assert 16*(a*a-1) == Q(4, 5*n*n) + Q(1, 100*n**4)
        assert 16*(a*a-1) < Q(1, n*n)
        for j in range(101):
            tau = 1 + Q(j, 100)
            g11, g12, g22 = 1-Q(1, 10)/tau, Q(2, 5)-eta, 1-tau/10
            assert min(g11, g22) >= Q(4, 5)
            assert g11*g22-g12*g12 >= Q(12, 25)
            f1, f2, f3 = g11-1, g22-1, Q(1, 2)-g12
            assert (f1, f2, f3) == (-Q(1, 10)/tau, -tau/10, Q(1, 10)+eta)
            assert tau*f1 + f2/tau + 2*f3 == 2*eta
            assert tau + 1/tau <= Q(5, 2)
            assert f1 < 0 and f2 < 0
            # Verify the aggregate identity also for non-extreme good cuts.
            for l1, l2, l3 in ((1, 1, 1), (2, 3, 4), (0, 1, 0), (1, 0, 0)):
                assert l3*l3 <= 4*l1*l2
                assert l1*f1+l2*f2+l3*f3 == (
                    -Q(1, 10)*(l1/tau+l2*tau-l3)+eta*l3
                )
            count += 1
    return count


def check_radial_identity():
    # Matrix entries depend only on ||u||^2, ||v||^2, and u.v.
    for u in ((Q(0), Q(0)), (Q(1, 3), Q(1, 2))):
        for v in ((Q(1, 4), Q(-1, 3)), (Q(0), Q(0))):
            for s in (Q(0), Q(1, 4), Q(1)):
                uu, vv = sum(t*t for t in u), sum(t*t for t in v)
                uv = sum(a*b for a, b in zip(u, v))
                direct = (1-s*s*uu, s*s*uv-Q(1, 2), 1-s*s*vv)
                b = (1-uu, uv-Q(1, 2), 1-vv)
                b0 = (Q(1), -Q(1, 2), Q(1))
                assert direct == tuple(s*s*a+(1-s*s)*z for a, z in zip(b, b0))
    for a in (Q(0), Q(1, 100), Q(1), Q(10)):
        s_squared = 1/(1+2*a)
        assert -s_squared*a + (1-s_squared)/2 == 0


if __name__ == "__main__":
    meshes = check_meshes()
    witnesses = check_witnesses()
    check_radial_identity()
    print(f"PASS: {meshes} rational meshes; {witnesses} exact Gram witnesses; radial identities")
