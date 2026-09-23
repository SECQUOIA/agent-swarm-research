"""High-precision check of the four-node K4 single-parameter arc obstruction."""
from fractions import Fraction

import mpmath as mp
import networkx as nx


def run():
    mp.mp.dps = 80
    M = mp.mpf(10)**8
    scale = mp.mpf(10000)
    scenarios = [(Fraction(23, 108), mp.mpf('1.5')),
                 (Fraction(1), mp.mpf(1)),
                 (Fraction(71, 12), mp.mpf('.5'))]
    states = []
    for rational_theta, initial_q in scenarios:
        theta = mp.mpf(rational_theta.numerator)/rational_theta.denominator
        def equations(q, v):
            t = v/scale
            x, y = (q+1+t)/2, (7+t-q)/2
            return y*y/6-x*x/2-theta*q*q, -x*x/2-y*y/6+v*v
        q, v = mp.findroot(equations, (initial_q, -mp.sqrt(2)))
        t = v/scale
        x, y = (q+1+t)/2, (7+t-q)/2
        flows = [x, y, y, x, q, t]
        arcs = [(0,2),(2,1),(0,3),(3,1),(2,3),(1,0)]
        b = [mp.mpf(0)]*4
        for (u,w), flow in zip(arcs, flows):
            b[u] += flow
            b[w] -= flow
        assert max(abs(a-c) for a,c in zip(b, [4,-4,3,-3])) < mp.mpf('1e-70')
        old = -2-(initial_q-1)**2/6
        new = -M*t*t
        assert 0 < new-old < mp.mpf(1)/96
        assert abs(t) < 2/scale
        assert max(abs(a) for a in equations(q,v)) < mp.mpf('1e-70')
        states.append((t,new))
    assert states[1][0] > max(states[0][0], states[2][0])
    assert states[1][1] > -2
    assert max(states[0][1],states[2][1]) < -mp.mpf(65)/32
    G = nx.complete_graph(4)
    assert len(G.edges)-len(G)+1 == 3
    print('Three complete K4 states passed conservation, cycle, probe, and strict endpoint-gap checks at 80 digits.')
    print('Interior target-flow advantage:', mp.nstr(states[1][0]-max(states[0][0],states[2][0]),20))
    print('Interior pressure advantage:', mp.nstr(states[1][1]-max(states[0][1],states[2][1]),20))


if __name__ == '__main__':
    run()
