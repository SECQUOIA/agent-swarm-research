#!/usr/bin/env python3
"""Exact arithmetic certificates for the scalar-dilation appendix. Uses only the standard library."""
from fractions import Fraction as F
from math import factorial


def y_bounds(z, n=1200):
    power = z
    halfpower = F(1)
    total = F(0)
    for j in range(n + 1):
        total += (2 - halfpower) * power / (2*j + 1)
        power *= z*z
        halfpower /= 2
    tail = 2*power / ((2*n+3)*(1-z*z))
    return total, total+tail


def log_bounds(z, n=200):
    assert z > 1
    q = (z-1)/(z+1)
    total, power = F(0), q
    for j in range(n+1):
        total += 2*power/(2*j+1)
        power *= q*q
    return total, total+2*power/((2*n+3)*(1-q*q))


def main():
    a, k = F(69, 50), F(107, 200)
    assert sum(F(1099,1000)**j / factorial(j) for j in range(7)) > 3
    assert 2497**2 * 41 < 64 * 2000**2
    assert F(2497,2000)**2 * F(225,656) == F(56115081,104960000) < k
    assert 1+F(19,50)+F(19,50)**2/2 == F(7261,5000) > F(100,69)
    r, s = F(31,69), F(19,119)
    log_small_lower = -2*(r+r**3/3+r**5/(5*(1-r*r)))
    log_large_lower = 2*(s+s**3/3)
    assert log_small_lower == -F(9064603453,9362506500)
    assert log_large_lower == F(1628072,5055477)
    margin = log_small_lower+1+k*(log_large_lower-(a-1))
    assert margin == F(255839420916449,315546241820670000) > 0
    print('Upper certificate: exact margin', margin, flush=True)

    v, w, a0 = F(3787,4000), F(9797031,10**7), F(68743,50000)
    vl, vu = y_bounds(v)
    wl, _ = y_bounds(w)
    vlow, vup = F(2453756741730599,10**15), F(12268783708653,5*10**12)
    wlow = F(134943211257327,4*10**13)
    avlow = F(405367307458211,4*10**13)
    awup = F(25381942601625079,10**15)
    assert vlow < vl < vu < vup
    assert wlow < wl
    assert avlow**2*(1-v*v)**2 < 2-v*v
    assert awup**2*(1-w*w)**2 > 2-w*w
    margin1 = wlow-a0*vup
    margin2 = vlow*avlow-w*awup
    assert margin1 == F(2071874360571,250000000000000000) > 0
    assert margin2 == F(2049519399569150216498389,40000000000000000000000000000) > 0
    print('Lower certificate: both exact margins positive.', flush=True)

    loga_lower, _ = log_bounds(a0)
    for kval, eval_, certificate in (
        (F(1), F(2), F(2589087717927,40000000000000000)),
        (k, F(571,250), F(2011885403423,100000000000000000)),
        (k, F(773,250), F(8579961311243,500000000000000000)),
    ):
        _, loge_upper = log_bounds(eval_)
        assert kval*loga_lower+(a0-1)*(eval_-kval)-loge_upper > certificate > 0
    assert F(571,250) < 1/(a0-1) < F(773,250)
    vleft, vright = F(4611,5000), F(9701,10000)
    _, left_upper = y_bounds(vleft)
    right_lower, _ = y_bounds(vright)
    assert F(571,250)*vleft-left_upper > F(159652343530451,200000000000000000)
    assert right_lower-F(773,250)*vright > F(19492543073837,250000000000000000)
    assert vleft*vleft > F(43,50)**2*(2-vleft*vleft)
    assert vright*vright < F(943,1000)**2*(2-vright*vright)
    print('Every-maximizer localization: logarithm, Y, and radical bounds passed.', flush=True)
    print('All rational, series-tail, and squared-radical checks passed.')


if __name__ == '__main__':
    main()
