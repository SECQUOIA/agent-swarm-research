"""Independent exact checks of quaternion exposing forms and shared parents."""

import sympy as sp


def mul(a, b):
    w, x, y, z = a
    s, u, v, t = b
    return sp.Matrix([w*s-x*u-y*v-z*t, w*u+x*s+y*t-z*v,
                      w*v-x*t+y*s+z*u, w*t+x*v-y*u+z*s])


def conjugate(q):
    return sp.Matrix([q[0], -q[1], -q[2], -q[3]])


def norm2(q):
    return q.dot(q)


def check_symbolic():
    a = sp.Matrix(sp.symbols('a0:4'))
    b = sp.Matrix(sp.symbols('b0:4'))
    c = sp.Matrix(sp.symbols('c0:4'))
    p = sp.Matrix(sp.symbols('p0:4'))
    residual = c-mul(a, b)
    E = norm2(c)-1-2*p.dot(residual)-(norm2(a)-1)-(norm2(b)-1)
    distance = norm2(c-p)-norm2(a-mul(p, conjugate(b)))
    assert sp.expand(distance-E-(norm2(p)-1)*(1-norm2(b))) == 0
    repeated = dict(zip(b, a))
    assert sp.expand((distance-E).subs(repeated)
                     -(norm2(p)-1)*(1-norm2(a))) == 0
    assert sp.expand(norm2(mul(a, b))-norm2(a)*norm2(b)) == 0
    assert sp.expand(p.dot(mul(a, b))-a.dot(mul(p, conjugate(b)))) == 0
    # Every distinct-parent bilinear coordinate is a signed orthogonal form.
    for coordinate in mul(a, b):
        K = sp.Matrix(4, 4, lambda i, j: sp.diff(coordinate, a[i], b[j]))
        assert K.T*K == sp.eye(4)
    # Repeated-parent residual quadratic matrices have norm at most one.
    for coordinate in mul(a, a):
        H = sp.hessian(coordinate, a)/2
        assert all(value >= 0 for value in (sp.eye(4)-H*H).eigenvals())


def check_shared_circuit():
    instructions = [('constant', sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0, 0])),
                    ('constant', sp.Matrix([sp.Rational(1, 2)]*4)),
                    ('product', 0, 1), ('product', 0, 0), ('inverse', 2),
                    ('product', 3, 1), ('product', 0, 4), ('product', 2, 2)]
    size = len(instructions)
    points = []
    blocks = [sp.Matrix(sp.symbols(f'x{i}_0:4')) for i in range(size)]
    variables = [x for block in blocks for x in block]
    residuals = []
    exact = sp.Integer(0)
    rounded = sp.Integer(0)
    mesh = sp.Rational(1, 2**60)
    for i, instruction in enumerate(instructions):
        kind = instruction[0]
        q_i = norm2(blocks[i])-1
        penalty = 0
        if kind == 'constant':
            point = instruction[1]
            residual = blocks[i]-point
        elif kind == 'product':
            a, b = instruction[1:]
            point = mul(points[a], points[b])
            residual = blocks[i]-mul(blocks[a], blocks[b])
            penalty = norm2(blocks[a])+norm2(blocks[b])-2
        else:
            a = instruction[1]
            point = conjugate(points[a])
            residual = blocks[i]-conjugate(blocks[a])
            penalty = norm2(blocks[a])-1
        assert norm2(point) == 1
        points.append(point)
        residuals.extend(residual)
        weight = sp.Rational(1, 16**i)
        exact += weight*(q_i-2*point.dot(residual)-penalty)
        approximate = point.applyfunc(lambda value: sp.floor(value/mesh)*mesh)
        rounded += weight*(q_i-2*approximate.dot(residual)-penalty)
    substitutions = dict(zip(variables, [q for point in points for q in point]))
    assert sp.expand(exact).subs(substitutions) == 0
    assert sp.expand(rounded).subs(substitutions) == 0
    gradient = sp.Matrix([sp.diff(exact, x) for x in variables])
    assert gradient.subs(substitutions) == sp.zeros(len(variables), 1)
    J = sp.Matrix(residuals).jacobian(variables).subs(substitutions)
    assert J.det() == 1
    H = sp.hessian(exact, variables)/2
    lower = sp.Rational(11, 15*16**(size-1))
    _, D = (H-lower*sp.eye(4*size)).LDLdecomposition(hermitian=False)
    assert all(D[i, i] > 0 for i in range(D.rows))
    Hhat = sp.hessian(rounded, variables)/2
    coefficient_error = Hhat-H
    assert sum(q*q for q in coefficient_error) <= (8*size*mesh)**2
    rounded_gradient = sp.Matrix([sp.diff(rounded, x) for x in variables]).subs(substitutions)
    assert norm2(rounded_gradient) <= (12*size*mesh)**2


if __name__ == '__main__':
    check_symbolic()
    check_shared_circuit()
    print('PASS: symbolic quaternion norm/inner-product/exposer identities;')
    print('distinct and repeated-parent quadratic bounds; an exact shared circuit')
    print('with inversion, weighted PD exposer, rounded zero, and error margins.')
