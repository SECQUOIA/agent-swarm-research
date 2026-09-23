"""Exact symbolic replay for the two-level positive cubic family."""
import sympy as s
from fractions import Fraction as Q

a,c,m=s.symbols('a c m',real=True)
F=a*c*c+s.Rational(5,4)*a*a
plane=s.Rational(11,6)*a+s.Rational(20,27)*c-s.Rational(95,108)
residual=s.Rational(5,4)*(a-(11-6*c*c)/15)**2+(1-c)*(3*c-2)**2*(3*c+7)/135
assert s.expand(F-plane-residual)==0
atoms=[{a:s.Rational(1,3),c:1},{a:s.Rational(5,9),c:s.Rational(2,3)}]
assert all(s.simplify((F-plane).subs(pt))==0 for pt in atoms)
weights=[s.Rational(1,4),s.Rational(3,4)]
assert sum(w*pt[a] for w,pt in zip(weights,atoms))==s.Rational(1,2)
assert sum(w*pt[c] for w,pt in zip(weights,atoms))==s.Rational(3,4)
assert sum(w*F.subs(pt) for w,pt in zip(weights,atoms))==s.Rational(16,27)
counts=a*m*(c*m)*(c*m-1)/2+s.Rational(5,4)*m*(a*m)*(a*m-1)/2
assert s.expand(2*counts/m**3-F+(a*c+s.Rational(5,4)*a)/m)==0
assert Q(9,8)-Q(16,27)==Q(115,216)
assert Q(1,2)+Q(5,4)/2==Q(9,8)
assert Q(9,8)/Q(115,216)==Q(243,115)
assert Q(243,115)*Q(19,20)==Q(4617,2300)>2
print('PASS: exact square-factor identity and both equality points.')
print('PASS: two-atom means and expected scalar value 16/27.')
print('PASS: finite count expansion and all rational gap constants.')
print('PASS: limiting ratio 243/115; m20 lower bound 4617/2300>2.')

checked=0
for A in range(17):
    for C in range(17):
        cost=A*C*(C-1)//2+20*A*(A-1)//2
        assert 2*cost>=428*A+177*C-3372,(A,C)
        checked+=1
assert 8*12*11//2+20*8*7//2==1088
assert 428*8+177*12-3372==2*1088
assert Q(2160,2160-1088)==Q(135,67)>2
print('PASS:',checked,'integer-grid dual inequalities for m16; exact ratio135/67.')

assert 16*(16*15//2)+20*(16*15//2)==4320
assert Q(1,2)+Q(3,4)+Q(3,4)-2==0
assert Q(1,2)+Q(1,2)+Q(999,1000)-2<0
assert 120*20*Q(1,1000)==Q(12,5)
assert Q(2160)/(Q(1072)+Q(12,5))==Q(2700,1343)>2
print('PASS: explicit52-variable unit-coefficient homogeneous cubic bound2700/1343>2.')
