"""Targeted exact enumeration of the constant two-mode rounding witness.

Every reachable state is tracked with exact integer counts. The binary search
minimizes twice the maximum grid-prefix discrepancy, without floating point.
This checks finite examples, not the asymptotic proof.
"""
import json
from fractions import Fraction
from math import lcm


def feasible(n, arcs, twice_bound, weights=(1,1,0), denominator=2):
    states = {(i, int(i == 0), int(i == 1)) for i in range(3)}
    def good(k, cu, cv):
        return (abs(denominator*cu-weights[0]*k) <= twice_bound and
                abs(denominator*cv-weights[1]*k) <= twice_bound and
                abs(denominator*(k-cu-cv)-weights[2]*k) <= twice_bound)
    states = {s for s in states if good(1, s[1], s[2])}
    for k in range(2, n+1):
        states = {(j, cu+(j==0), cv+(j==1))
                  for i, cu, cv in states for j in arcs[i]
                  if good(k, cu+(j==0), cv+(j==1))}
        if not states:
            return False
    return bool(states)


def optimum(n, arcs, alpha=(Fraction(1,2),Fraction(1,2),Fraction(0))):
    denominator = lcm(*(a.denominator for a in alpha))
    weights = tuple(int(denominator*a) for a in alpha)
    lo, hi = -1, denominator*n
    while hi-lo > 1:
        mid = (lo+hi)//2
        if feasible(n, arcs, mid, weights, denominator):
            hi = mid
        else:
            lo = mid
    assert feasible(n, arcs, hi, weights, denominator)
    assert hi == 0 or not feasible(n, arcs, hi-1, weights, denominator)
    return Fraction(hi, denominator)


def main():
    graphs = {
        'complete': [(0,1,2), (0,1,2), (0,1,2)],
        'directed_cycle': [(0,2), (0,1), (1,2)],
        'undirected_path': [(0,2), (1,2), (0,1,2)],
        'one_way': [(0,1), (1,), (2,)],
    }
    rows = []
    for name, arcs in graphs.items():
        for n in [8,16,32,64,128]:
            d = optimum(n, arcs)
            if name in ('directed_cycle','undirected_path'):
                assert n <= 8*d*d+9*d
            rows.append({'graph':name,'N':n,'D':str(d),'D/sqrt(N)':float(d)/n**0.5,'D/N':float(d/n)})
    phase_rows = []
    for eta in [Fraction(1,32),Fraction(1,8),Fraction(1,3)]:
        alpha = ((1-eta)/2, (1-eta)/2, eta)
        for n in [16,32,64,128]:
            d = optimum(n, graphs['directed_cycle'], alpha)
            # Phase-diagram quadratic inequality for m=3, a=1, C_m=38.
            assert Fraction(2,3)*n <= 12*eta*n*d + 38*d*d
            phase_rows.append({'eta':str(eta),'N':n,'D':str(d),
                               'D/min(sqrt(N),1/eta)':float(d)/min(n**0.5,float(1/eta))})
    print(json.dumps({'boundary':rows,'interior':phase_rows}, indent=2))

if __name__ == '__main__':
    main()
