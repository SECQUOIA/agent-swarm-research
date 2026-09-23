"""Independent exact signed-state and corruption checks for Bregman bounds."""
from dataclasses import replace
from fractions import Fraction as F
from envelope_bregman_bounds import divergence, sharpen, verify_bounds
from envelope_rational_certificates import law, make_certificate


def require(condition):
    if not condition:
        raise RuntimeError("independent Bregman check failed")


def reject(call):
    try:
        call()
    except (ValueError, TypeError):
        return
    raise RuntimeError("malformed Bregman bound accepted")


def run():
    edges = [(0, 1), (1, 2), (0, 2)]
    b, positive, negative, exact, potentials = [list(map(F, v)) for v in
        ([3, 0, -3], [3, 1, 1], [2, 7, 5], [1, 1, 2], [4, 1, 0])]
    states = corruptions = 0
    for t in [F(i, 8) for i in range(-24, 25)]:
        y = [1+t, 1+t, 2-t]
        cert = make_certificate(edges, b, positive, negative, y, potentials)
        bounds = sharpen(positive, negative, cert, steps=35)
        require(sum(divergence(v, z, cp, cm) for v, z, cp, cm in
                    zip(y, exact, positive, negative)) == cert.gap)
        for j, (lo, hi) in enumerate(bounds):
            require(lo <= exact[j] <= hi)
            require(y[j]-cert.radius <= lo <= hi <= y[j]+cert.radius)
            require(law(lo, positive[j], negative[j]) <=
                    potentials[edges[j][0]]-potentials[edges[j][1]] <=
                    law(hi, positive[j], negative[j]))
            if cert.gap:
                step = cert.radius / (1 << 35)
                require(divergence(y[j], lo+step, positive[j], negative[j]) < cert.gap)
                require(divergence(y[j], hi-step, positive[j], negative[j]) < cert.gap)
        if not cert.gap:
            require(bounds == [(x, x) for x in exact])
        else:
            for bad in [
                [(y[0], bounds[0][1])] + bounds[1:],
                [(bounds[0][0], y[0])] + bounds[1:],
                [(bounds[0][1], bounds[0][0])] + bounds[1:],
                [(float(bounds[0][0]), bounds[0][1])] + bounds[1:],
                bounds[:-1],
            ]:
                reject(lambda: verify_bounds(positive, negative, cert, bad))
                corruptions += 1
        reject(lambda: verify_bounds([F(0)]+positive[1:], negative, cert, bounds))
        reject(lambda: verify_bounds(positive, negative, replace(cert, gap=float(cert.gap)), bounds))
        corruptions += 2
        states += 1
    # A zero physical state and zero energy gap are separate from a nonzero
    # exact state. Wider containing intervals are also valid at zero gap.
    cert = make_certificate([(0, 1)], [F(0), F(0)], [F(2)], [F(7)],
                            [F(0)], [F(0), F(0)])
    require(sharpen([F(2)], [F(7)], cert) == [(F(0), F(0))])
    require(verify_bounds([F(2)], [F(7)], cert, [(F(-1), F(2))]))
    reject(lambda: verify_bounds([F(2)], [F(7)], cert, [(F(1), F(2))]))
    # Independent residual bound on two known physical states with the same b.
    residuals = 0
    for t in [F(i, 32) for i in range(-20, 41) if i]:
        other = [1+t, 1+t, 2-t]
        beta = [F(3)/other[0]**2, F(1)/other[1]**2, F(4)/other[2]**2]
        r = [abs(c*x*x-d) for c, x, d in zip(beta, exact, [3, 1, 4])]
        require(max(abs(x-z) for x, z in zip(exact, other))**2 <= 2*sum(r)/min(beta))
        residuals += 1
    print(f"PASS: {states+1} exact signed/zero-gap states, {corruptions+1} "
          f"malformed-bound rejections, {residuals} conserved physical residual bounds.")


if __name__ == "__main__":
    run()
