"""Exact rational SOS certificate for the irrational-zero quartic's Hessian.

Run only this targeted check: python research-20260927/check_convex_quartic_rational_sos.py
SymPy is the sole dependency. No numerical solver is used for verification.
"""

import sympy as sp


M = sp.Matrix([
    [50768581447, -44366840880, 1413637800, -1525142380, -762571190, 931147600],
    [-44366840880, 54369630883, 0, 465573800, 0, -352760910],
    [1413637800, 0, 47623440300, -18898500000, -18898500000, 19999652600],
    [-1525142380, 465573800, -18898500000, 14999826300, 10000000000, -11905500000],
    [-762571190, 0, -18898500000, 10000000000, 14999826300, -11905500000],
    [931147600, -352760910, 19999652600, -11905500000, -11905500000, 18901790700],
])

N = sp.Matrix([
    [812297303152, 102427849072, 22618204800, -13093175680, 5654551200, -130053040],
    [102427849072, 262472489120, 22618204800, -5643994880, 1929960800, -3911932400],
    [22618204800, 22618204800, 761975044800, 78611522400, 39305761200, -2034439000],
    [-13093175680, -5643994880, 78611522400, 128114982000, -15939729800, -13708914300],
    [5654551200, 1929960800, 39305761200, -15939729800, 112025966300, 13144848050],
    [-130053040, -3911932400, -2034439000, -13708914300, 13144848050, 120298532375],
])

MARGINS = [668373469360, 125940547168, 596786912600,
           1117644940, 36051115250, 87368345585]

PRINCIPAL_MINORS = [
    50768581447,
    791852464055672853301,
    37602087809621501397054685710300,
    280993148508166601254733045220120801330000,
    1873166972279421324215746068355899924560061972000000,
    13762610926131499144712721124744763054915409487405217600000000,
]


def verify():
    x, y, X, Y, a, b = sp.symbols("x y X Y a b", real=True)
    A = 12599*x**2 - 10000*x*y + 7937*y**2 - 15874*x - 12599*y + 20000
    F = A**2 + 10000*((x**2-y)**2 + (y**2-2*x)**2)
    hessian = sp.hessian(F, (x, y))
    translated = hessian.subs({x: sp.Rational(63, 50) + X/100,
                              y: sp.Rational(1587, 1000) + Y/100})
    direction = sp.Matrix([a, b])
    gap = (direction.T*(translated - 4096*sp.eye(2))*direction)[0]
    w = sp.Matrix([a, b, X*a, X*b, Y*a, Y*b])
    assert sp.expand(250000*gap - (w.T*M*w)[0]) == 0
    assert M == M.T

    # A small rational change of basis avoids large LDL fractions.
    half = sp.Rational(1, 2)
    U = sp.Matrix([
        [1, -1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0],
        [0, 0, 1, -half, -half, half], [0, 0, 0, 1, half, -half],
        [0, 0, 0, 0, 1, -half], [0, 0, 0, 0, 0, 1],
    ])
    assert U.det() == 1
    assert N == N.T and U.T*N*U == 16*M
    margins = [N[i, i] - sum(abs(N[i, j]) for j in range(6) if j != i)
               for i in range(6)]
    assert margins == MARGINS and all(d > 0 for d in margins)

    # Check the diagonal-dominance SOS identity first for arbitrary vectors.
    z = sp.Matrix(sp.symbols("z0:6", real=True))
    sos = sum(margins[i]*z[i]**2 for i in range(6))
    sos += sum(abs(N[i, j])*(z[i] + sp.sign(N[i, j])*z[j])**2
               for i in range(6) for j in range(i + 1, 6))
    assert sp.expand((z.T*N*z)[0] - sos) == 0

    v = sp.Matrix([2*a - 2*b, 2*b, 2*X*a-X*b-Y*a+Y*b,
                   2*X*b+Y*a-Y*b, 2*Y*a-Y*b, 2*Y*b])
    assert v == 2*U*w
    actual_sos = sos.subs(dict(zip(z, v)), simultaneous=True)
    assert sp.expand(16000000*gap - actual_sos) == 0

    # Recheck the complete identity in the original, unshifted coordinates.
    original_gap = (direction.T*(hessian - 4096*sp.eye(2))*direction)[0]
    original_sos = actual_sos.subs({X: 100*x-126, Y: 100*y-sp.Rational(1587, 10)})
    assert sp.expand(16000000*original_gap - original_sos) == 0

    # A separate exact matrix check, beyond diagonal dominance.
    minors = [M[:i, :i].det() for i in range(1, 7)]
    assert minors == PRINCIPAL_MINORS and all(d > 0 for d in minors)
    lower, diagonal = M.LDLdecomposition(hermitian=False)
    assert lower*diagonal*lower.T == M
    assert all(diagonal[i, i] > 0 for i in range(6))

    print("PASS: exact differentiated Hessian, translated and original SOS identities")
    print("PASS: integer diagonal-dominance certificate, 21 positive square weights")
    print("PASS: six positive leading principal minors and exact positive LDL")
    print("CONCLUSION: Hessian(F)(x,y) >= 4096 I for every real x,y")


if __name__ == "__main__":
    verify()
