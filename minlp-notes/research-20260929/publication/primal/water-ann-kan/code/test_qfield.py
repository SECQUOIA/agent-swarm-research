"""Randomized test of qfield.py (quadratic-field arithmetic, root isolation, exact signs, inverses) against mpmath at 60 digits."""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../../..'))
import sys, random
sys.path.insert(0,_REPRO_ROOT + '/research-20260929/publication/primal/water-ann-kan/code')
from fractions import Fraction as Fr
import mpmath as mp
import qfield as Q
mp.mp.dps=60
random.seed(1)
bad=0
for trial in range(300):
    k=Q.SYM.new(f"t{trial}")
    w=Q.Val(k,(Fr(0),Fr(1)))
    A=Fr(random.randint(1,10**6),10**4); B=Fr(random.randint(-10**6,10**6),10**4); C=-Fr(random.randint(1,10**6),10**4)
    # build expressions before solving
    e1 = w*w*Fr(3) - w*Fr(2) + Fr(1,3)
    e2 = w*w*w - w
    Q.solve_symbol(k,(C,B,A),near=1.0)
    wv=Q.to_mpf(w)
    assert abs(A*0+ (mp.mpf(A.numerator)/A.denominator)*wv**2+(mp.mpf(B.numerator)/B.denominator)*wv+(mp.mpf(C.numerator)/C.denominator))<mp.mpf(10)**-40
    for e,f in ((e1,3*wv**2-2*wv+mp.mpf(1)/3),(e2,wv**3-wv)):
        v=Q.to_mpf(e.norm())
        assert abs(v-f)<mp.mpf(10)**-35*(1+abs(f)), (v,f)
    # sign tests: p + r w with z near w
    for _ in range(20):
        r=Fr(random.choice([-1,1])*random.randint(1,1000),random.randint(1,1000))
        z=Fr(mp.nstr(wv+mp.mpf(random.uniform(-1,1))*mp.mpf(10)**random.randint(-50,-1),70))
        v=Q.Val(k,(-r*z,r))
        sg=Q.sign(v); fv=r*(wv- mp.mpf(z.numerator)/z.denominator)
        if (sg>0)!=(fv>0): bad+=1
    inv=(w*Fr(2)+Fr(1)).inv()
    assert abs(Q.to_mpf(inv*(w*Fr(2)+Fr(1)))-1)<mp.mpf(10)**-40
print('bad',bad)
