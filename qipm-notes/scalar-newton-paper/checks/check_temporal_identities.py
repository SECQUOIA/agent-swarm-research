"""Deterministic finite diagnostics for Sections 8--9; not proofs."""
from itertools import product

import numpy as np
from numpy.testing import assert_allclose
from scipy.optimize import linprog


def rho(z):
    z = np.asarray(z, dtype=float)
    return 2 * z / (1 + np.hypot(1, 2 * z))


def f(z):
    return 1 - 1 / np.hypot(1, 2 * np.asarray(z))


def check_kernels():
    rng = np.random.default_rng(43891)
    for gamma in (256., 2.**20):
        d0 = rho(gamma**.5) - rho(gamma**-.5)
        assert d0 >= 1 - 1.5 / gamma**.5
        for blocks in (1, 2, 5, 9):
            amplitudes = rng.uniform(-1, 1, blocks)
            ix = np.arange(1, blocks + 1)
            for j in range(1, blocks + 1):
                d = rho(gamma**(j - ix + .5)) - rho(gamma**(j - ix - .5))
                assert abs(d @ amplitudes - d0 * amplitudes[j - 1]) <= 1-d0+1e-14
                for xi in (.001, .1, .25):
                    scales = gamma**(j-ix)
                    actual = np.sum(f(scales*np.sqrt(1+xi*amplitudes)))
                    baseline = np.sum(f(scales))
                    main = f(np.sqrt(1+xi*amplitudes[j-1])) - f(1.)
                    assert abs(actual-baseline-main) <= .4*xi/(gamma-1)+1e-14
                    # Compare the closed decrement with the radial inverse Hessian.
                    radius = rho(scales*np.sqrt(1+xi*amplitudes))
                    direct = 2*radius**2/(1+radius**2)
                    assert_allclose(direct, f(scales*np.sqrt(1+xi*amplitudes)), atol=1e-14)
    for xi in np.linspace(.0001, .25, 151):
        psi = lambda x: f(np.sqrt(1+xi*x))-f(1.)
        low_width = psi(.01)-psi(-.01)
        high_width = psi(1.)-psi(.6)
        gap = psi(.6)-psi(.01)
        assert low_width/2/xi < .0018
        assert high_width/2/xi < .035778
        assert gap/xi > .079
        norm_gap = rho(np.sqrt(1+.6*xi))-rho(np.sqrt(1+.01*xi))
        assert norm_gap/xi > .056


def threshold_constraints(amplitude, alpha=.01, beta=.6):
    center = (alpha+beta)/2
    gain = 2/(beta-alpha)
    # Variables z,r,t. Bounds implement 0<=z<=1,0<=r<=2,t>=0.
    matrix = np.array([[-1.,0.,1.], [0.,-gain,1.], [amplitude-center,-1.,0.]])
    objective = np.array([4*gain,-2*gain,1.])
    return matrix, objective


def check_threshold_and_xor():
    for amplitude in (-.01, 0., .01, .6, .8, 1.):
        matrix, objective = threshold_constraints(amplitude)
        result = linprog(-objective, A_ub=matrix, b_ub=np.zeros(3),
                         bounds=[(0,1),(0,2),(0,None)], method='highs')
        assert result.success
        bit = int(amplitude >= .6)
        assert_allclose(result.x[[0,2]], [1,bit], atol=1e-10)
        optimum = objective@result.x
        rng = np.random.default_rng(8491)
        for _ in range(100):
            z = rng.uniform(0,1)
            r = rng.uniform(max(0,(amplitude-.305)*z), 2)
            t = rng.uniform(0,min(z,2/(.6-.01)*r))
            assert optimum-objective@np.array([z,r,t]) >= abs(t-bit)-1e-12
    # Every Boolean input has a unique XOR extension; fractional gate bounds
    # are nonempty and satisfy the deterministic error recursion.
    rng = np.random.default_rng(831)
    for bits in product((0,1), repeat=4):
        fractional = np.clip(np.asarray(bits)+rng.uniform(-.1,.1,4),0,1)
        p = fractional[0]
        exact = bits[0]
        error_sum = abs(p-exact)
        for t, bit in zip(fractional[1:], bits[1:]):
            lo = abs(p-t)
            hi = min(p+t,2-p-t)
            assert lo <= hi+1e-14
            p = (lo+hi)/2
            exact ^= bit
            error_sum += abs(t-bit)
            assert abs(p-exact) <= error_sum+1e-14


def signed_tree(length, signs):
    leaves = 2**int(np.ceil(np.log2(length)))
    parents = [-1]+list(range(length))
    edge_signs = [1]+list(signs)
    for root in (0,length):
        level = [root]
        for _ in range(int(np.log2(leaves))):
            new = []
            for parent in level:
                for _ in range(2):
                    new.append(len(parents))
                    parents.append(parent)
                    edge_signs.append(1)
            level = new
    matrix = np.eye(len(parents))
    for node in range(1,len(parents)):
        matrix[node,parents[node]] = -edge_signs[node]
    return matrix/np.sqrt(8), leaves


def check_kkt_and_tree():
    rng = np.random.default_rng(452)
    for length in (2,3,5,8,12):
        signs = rng.choice([-1,1],length)
        matrix, leaves = signed_tree(length, signs)
        n = len(matrix)
        assert n == length+4*leaves-3
        assert np.max(np.count_nonzero(matrix, axis=0)) <= 4
        assert np.max(np.count_nonzero(matrix, axis=1)) <= 2
        assert np.linalg.norm(matrix,2) <= 1+1e-12
        e = np.eye(n)[0]
        v = np.linalg.solve(matrix,e)
        for a in (0., .2, .75, .98):
            qa = 1-a*a
            diagonal = 2/qa*np.eye(n)+4*a*a/qa**2*np.outer(e,e)
            zero = np.zeros_like(matrix)
            kkt = np.block([[diagonal,zero,np.eye(n)],
                            [zero,zero,-matrix.T],
                            [np.eye(n),-matrix,zero]])
            predicted = qa**2/(1+a*a)*np.r_[e,v,np.zeros(n)]
            assert_allclose(kkt@predicted,np.r_[2*e,np.zeros(2*n)],atol=1e-12)
            assert_allclose(np.linalg.solve(kkt,np.r_[2*e,np.zeros(2*n)]),
                            predicted,atol=1e-11)


def check_rank_volume():
    rng = np.random.default_rng(5194)
    for rank in (1,2,3,5):
        ambient = 4*rank
        exact = rng.normal(size=(ambient,rank))
        basis = np.linalg.qr(exact)[0]
        width = 1e-4
        columns = basis@rng.normal(size=(rank,2*rank))
        columns += width*rng.normal(size=columns.shape)
        columns /= np.linalg.norm(columns,axis=0)
        deviation = np.max(np.linalg.norm(columns-basis@(basis.T@columns),axis=0))
        volume = np.prod(np.linalg.svd(columns,compute_uv=False))
        assert volume <= (2*rank)**rank*deviation**rank+1e-15
        # Exact residual selection cannot add more than rank rays.
        stored = np.empty((ambient,0))
        for _ in range(30):
            ray = basis@rng.normal(size=rank)
            ray /= np.linalg.norm(ray)
            residual = ray-stored@np.linalg.lstsq(stored,ray,rcond=None)[0]
            if np.linalg.norm(residual) > .1:
                stored = np.column_stack((stored,ray))
        assert stored.shape[1] <= rank


if __name__ == '__main__':
    check_kernels()
    check_threshold_and_xor()
    check_kkt_and_tree()
    check_rank_volume()
    print('Temporal diagnostics passed: kernels, threshold/XOR, sparse KKT, rank/volume.')
