"""Exact counterexample to the cited Toolbox Lemma A's unique extension."""
from fractions import Fraction as F

def original(x):
    return (x == 0 or x > 0) and 1-x >= 0

def transformed(x,z,w):
    # Toolbox steps 2--4, on (x=0 OR x>0) AND 1-x>=0.
    return x*(x*z-1) == 0 and 1-x-w == 0 and z >= 0 and w >= 0

assert original(F(0))
for z in (F(0),F(1),F(10),F(10**100)):
    assert transformed(F(0), z, F(1))
for n in (1,2,10,10**100):
    assert original(F(1,n)) and transformed(F(1,n),F(n),1-F(1,n))
print('CONFIRMED: the compact original set is [0,1].')
print('The transformed set contains the unbounded ray (0,z,1), z>=0.')
print('Projection is noninjective; the claimed z=1/x forward map is undefined at x=0.')
print('This refutes that source normal-form argument, not all possible realizations of [0,1].')
