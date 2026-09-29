#!/usr/bin/env python3
"""Exact targeted checks for quadratic-exact-gap-frontier.md."""

import sympy as sp


def zero(expression):
    assert sp.simplify(sp.expand(expression)) == 0, expression


def main():
    x, y = sp.symbols("x y")
    s = sp.sqrt(3)
    a, b = 3*s - 5, s - 1
    A = (3 + 2*s)/18
    E = -sp.Rational(4, 3) + 7*s/9
    gx, gy = x*(1-x), 1-y*y
    p = A*(y+1)*(y+a)**2

    zero(x*x - 2*x*y + y*y/2 + y/2 + sp.Rational(1, 8)
         - (2*x-y-sp.Rational(1, 2))**2/2 - gx)
    zero(p-y*y-A*(y+7-4*s)*(y-b)**2)
    zero(p+p.subs(y, -y)-y*y-2*E)
    for node, h_value, error in [
        (-1, 0, 0), (-b, 0, 2*E), (-a, 0, 0),
        (a, a*a, 2*E), (b, b*b, 0), (1, 1, 2*E),
    ]:
        zero(p.subs(y, node)-h_value-error)

    V = sp.Matrix([x*(x-b), x*(y-b),
                   (y+1)*(y+a)-(b+1)*(b+a)*x/b])
    W = sp.Matrix([x-b, y-b])
    Z = (b+a)*x-b*(y+a)
    Q = sp.Matrix([
        [2-s, (-7+3*s)/4, (s-1)/12],
        [(-7+3*s)/4, sp.Rational(7, 6), -(s+1)/12],
        [(s-1)/12, -(s+1)/12, sp.Rational(1, 12)+s/18],
    ])
    R = Q[:2, :2].copy()
    R[1, 1] = 1
    k = sp.Rational(1, 6)+7*s/72
    zero(x*x-2*x*y+p-(V.T*Q*V)[0]
         -gx*(W.T*R*W)[0]-gy*k*Z**2)
    q_minors = [2-s, (35*s-58)/24, (38-15*s)/864]
    r_minors = [2-s, (13*s-22)/8]
    for matrix, values in [(Q, q_minors), (R, r_minors)]:
        for size, expected in enumerate(values, 1):
            zero(matrix[:size, :size].det()-expected)
            assert expected > 0
    assert k > 0

    atoms = [(sp.Rational(3, 4), 0, -sp.Rational(1, 2)),
             (sp.Rational(1, 4), 1, sp.Rational(3, 2))]

    def L(poly):
        return sp.simplify(sum(weight*poly.subs({x: xx, y: yy})
                               for weight, xx, yy in atoms))

    zero(L(y))
    zero(L(y*y)-sp.Rational(3, 4))
    zero(L(gx))
    zero(L(gy)-sp.Rational(1, 4))
    zero(2*L(x*x-2*x*y)+L(y*y)+sp.Rational(1, 4))
    c = sp.sqrt(2)-1
    E1 = c*c/2
    zero(sp.Rational(1, 2)-c-E1)
    zero(c*c/2-c*c+E1)
    assert -sp.Rational(1, 4) < -2*E1

    weights = [(8-4*s)/9, sp.Rational(5, 18)+s/6,
               -sp.Rational(1, 6)+5*s/18]
    nodes = [-1, -a, b]
    assert all(weight > 0 for weight in weights)
    zero(sum(weights)-1)
    for power in range(5):
        zero(sum(weight*(node**power-(-node)**power)
                 for weight, node in zip(weights, nodes)))
    zero(weights[0]+weights[1]*a*a-weights[2]*b*b+2*E)
    print("PASS: exact order-one and order-two certificates, approximation "
          "contacts, Gram minors, and matching witnesses")


if __name__ == "__main__":
    main()
