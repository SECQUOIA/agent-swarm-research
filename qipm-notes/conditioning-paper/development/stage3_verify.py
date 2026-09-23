"""Independent finite-dimensional sanity checks for Stage 3; not theorem proofs.

Run with the qipm Python environment. Uses only Decimal, NumPy and SciPy.
The high-precision calculation uses stable quadratic roots; the float64
check separately forms the full tangent log-det Hessian by trace products.
"""
from decimal import Decimal as D, localcontext

import numpy as np
from scipy.linalg import eigh, null_space


def decimal_fractional(gap):
    with localcontext() as ctx:
        ctx.prec = 70
        g = D(gap)
        b = (-g + (3*g-2*g*g).sqrt()) / 3
        a = 1-g-b
        q = a*g-b*b
        mu = q/(1-b-2*g)
        qb, qg = -g-2*b, 1-b-2*g
        k11 = 1/(b*b)+qb*qb/(q*q)+2/q
        k12 = qb*qg/(q*q)+1/q
        k22 = qg*qg/(q*q)+2/q
        tr = (2*k11-2*k12+4*k22)/7
        det = (k11*k22-k12*k12)/7
        high = (tr+(tr*tr-4*det).sqrt())/2
        low = det/high
        a_high = (a+g+((a-g)**2+4*b*b).sqrt())/2
        a_low = q/a_high
        eig = [1/(b*a_high), low, 1/(b*a_low), high]
        assert all(eig[i] < eig[i+1] for i in range(3))
        scaled = [eig[0]*mu.sqrt(), eig[1]*mu,
                  eig[2]*mu*mu.sqrt(), eig[3]*mu*mu]
        constant = eig[-1]/eig[0]*mu*mu.sqrt()
        residual = abs(q+b*qb)/q
        print('fractional Decimal', gap,
              'scaled=', [float(v) for v in scaled],
              'kappa_mu_1.5=', float(constant),
              'stationarity_b=', float(residual))
        assert residual < D('1e-60')
        return np.array([float(v) for v in eig])


def direct_fractional(g):
    b = (-g+np.sqrt(3*g-2*g*g))/3
    a = 1-g-b
    q = a*g-b*b
    mu = q/(1-b-2*g)
    x = np.array([[a,b,0.], [b,g,0.], [0.,0.,b]])
    tangent = np.array([
        [[-1,1,0],[1,0,0],[0,0,1]],
        [[-1,0,0],[0,1,0],[0,0,0]],
        [[0,0,1],[0,0,0],[1,0,0]],
        [[0,0,0],[0,0,1],[0,1,0]]], dtype=float)
    inv = np.linalg.inv(x)
    gram = np.einsum('aij,bij->ab', tangent, tangent)
    hess = np.array([[np.trace(inv@u@inv@v) for v in tangent]
                     for u in tangent])
    eig = eigh(hess, gram, eigvals_only=True)
    exact = decimal_fractional(str(g))
    relative = np.max(np.abs(eig/exact-1))
    objective = np.diag([0.,1.,0.])
    grad = np.einsum('ij,aij->a', -inv+objective/mu, tangent)
    relative_grad = np.linalg.norm(grad)*mu
    print('direct float64', g, 'relative_eigen_error=', relative,
          'relative_centrality=', relative_grad)
    assert np.min(np.linalg.eigvalsh(x)) > 0
    assert relative < 1e-7
    assert relative_grad < 1e-10
    for sign in [-1,1]:
        b0 = np.sqrt(g)/2
        a0 = 1-g-b0
        t = sign*g**0.25/(2*np.sqrt(2))
        chord = np.array([[a0,b0,t],[b0,g,0],[t,0,b0]])
        assert np.min(np.linalg.eigvalsh(chord)) > 0


def compact_lp():
    a = np.array([[1,1,1,1], [0,1,1.5,3.]])
    c = np.array([1,1,0,1.])
    t = (-6+4*np.sqrt(3))/9
    slack = c-a.T@np.array([-1.5*t,t])
    w = null_space(a)
    eig = np.linalg.eigvalsh(w.T@np.diag(slack**2)@w)
    explicit = np.array([[-1/3,1], [1,0], [-2/3,-2], [0,1.]])
    eig2 = eigh(explicit.T@np.diag(slack**2)@explicit,
                explicit.T@explicit, eigvals_only=True)
    assert np.allclose(a@explicit, 0)
    assert np.allclose(eig, eig2, rtol=1e-13)
    assert abs(27*t*t+36*t-4) < 1e-13
    print('compact degenerate LP', 'eigenvalues=', eig.tolist(),
          'condition=', eig[-1]/eig[0])


if __name__ == '__main__':
    for gap in [1e-2, 1e-4, 1e-6]:
        direct_fractional(gap)
    decimal_fractional('1e-12')
    decimal_fractional('1e-24')
    compact_lp()
