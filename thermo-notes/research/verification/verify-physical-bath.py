"""Deterministic formula checks; these are not microscopic simulation results."""
import numpy as np


def residual(E, gap, capacity, beta=1.):
    total = gap / (-np.expm1(-beta*gap/capacity))
    return beta*E + capacity*np.log1p(-E/total)


def interface(theta):
    return np.minimum(np.minimum(2*np.sqrt(np.pi*theta),2.),
                      2*np.sqrt(np.pi*(1-theta)))


if __name__ == '__main__':
    theta=np.linspace(0,1,10001)
    assert np.all(interface(theta) >= 8*theta*(1-theta)-1e-13)
    print('Isotropic square torus: beta=latent-energy-density-gap=tau=1')
    print('Predicted gamma*=1/16=0.0625; gamma=capacity/N^1.5')
    for gamma in [.04,.0625,.10]:
        cost=interface(theta)-theta*(1-theta)/(2*gamma)
        argmin=theta[np.argmin(cost)]
        print(f'gamma={gamma:.4f}, minimum cost={cost.min():.6f}, one minimizing fraction={argmin:.4f}')
        if gamma<1/16:
            assert abs(argmin-.5)<1e-5
        if gamma>1/16:
            assert argmin in [0.,1.]
    print('\nExact power-law bath approaching the interfacial tilt, gamma=0.1')
    gamma=.1
    goal=theta*(1-theta)/(2*gamma)
    errors=[]
    for n in [100,10000,1000000]:
        cap=gamma*n**1.5
        scaled=residual(theta*n,n,cap)/np.sqrt(n)
        error=np.max(abs(scaled-goal))
        errors.append(error)
        assert abs(scaled[0])<1e-8 and abs(scaled[-1])<1e-8
        print(f'N={n:7d}, max |exact scaled log-weight - quadratic limit|={error:.8f}')
    assert errors[2]<errors[1]<errors[0]
