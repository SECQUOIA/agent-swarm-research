"""Explicit known-Partition yes states with the new SP target-arc probe."""
from fractions import Fraction
from math import ceil

import mpmath as mp
import numpy as np


def as_mp(value):
    value=Fraction(value)
    return mp.mpf(value.numerator)/value.denominator


def run():
    mp.mp.dps=110
    rng=np.random.default_rng(992560)
    count=0
    worst=mp.mpf(0)
    for _ in range(24):
        half=list(map(int,rng.integers(1,12,int(rng.integers(2,6)))))
        values=half+half
        n=len(values)
        K=sum(values)
        eps0=1-(1-Fraction(1,8*K*K))**2
        M0=max(1-eps0+eps0**2,1-eps0**2/Fraction(K*K))
        eps1=(1-M0)/5
        T=max(1-eps1**2/Fraction(K*K*n*n),M0+4*eps1)
        gamma=1-T
        assert gamma>0
        assert gamma==eps0**4/Fraction(25*K**6*n*n)
        D=ceil(Fraction(1000*K*(3*K+2),1)/gamma)
        H=1-gamma/2
        M=H*D*D
        probe=1/(mp.sqrt(as_mp(M)+mp.mpf(1)/(K*K))+mp.mpf(1)/K)
        pressure=1-2*probe/K
        residual=abs(as_mp(M)*probe*probe-pressure)
        worst=max(worst,residual)
        source_total=mp.mpf(0)
        sink_total=mp.mpf(0)
        for i,Si in enumerate(values):
            internal=-Si if i<len(half) else Si
            left=mp.mpf(Si)*(pressure+(1 if internal<0 else -1))/2
            right=left+internal
            source_total+=left
            sink_total+=right
            assert abs((left*abs(left)+right*abs(right))/(Si*Si)-pressure)<mp.mpf('1e-95')
            # The corresponding pendant is Si for negative internal load, zero otherwise.
            pendant=Si if internal<0 else 0
            nomination=0 if internal<0 else Si
            assert abs(right+pendant-left-nomination)<mp.mpf('1e-95')
        assert abs(source_total+probe-mp.mpf(K)/2)<mp.mpf('1e-95')
        assert abs(sink_total+probe-mp.mpf(K)/2)<mp.mpf('1e-95')
        capacity=mp.mpf(1)/D
        gap=as_mp(gamma)/ (4*(6*K+1)*D)
        assert probe-capacity>gap
        assert 0<1-pressure<as_mp(gamma)/4
        assert probe<mp.mpf(6*K)/D<1
        assert M>0 and M.denominator>0
        count+=1
    assert worst<mp.mpf('1e-95')
    print(f'{count} explicit Partition yes nominations passed full branch/probe conservation, pressure, and arc-gap checks at110digits.')
    print('Max probe residual:',mp.nstr(worst,8))


if __name__=='__main__':
    run()
