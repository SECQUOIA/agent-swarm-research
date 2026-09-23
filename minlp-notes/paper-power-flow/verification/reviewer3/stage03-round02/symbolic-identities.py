import sympy as S
from pathlib import Path
x,y=S.symbols('x y')
q=S.Rational
b=x+q(1,2); bp=1/b; ap=1/x; c=ap+q(1,2); d=c-q(2,3)
e=d+q(1,2); f=e-bp; g=2*f; h=g-q(2,3); i=1/h
j=i-q(1,2); k=j+q(3,4); ell=b/2; out=k-ell
assert S.cancel(h-1/(x*(x+q(1,2))))==0
assert S.simplify(out-x*x)==0
r=((x+q(1,2))/2+(y+q(1,2))/2)-q(1,2)
u=r*r+q(1,2)
d2=(((x*x+q(1,2))/2)+((y*y+q(1,2))/2))/2
out2=2*(u-d2)-q(1,2)
assert S.expand(out2-x*y)==0
s,t,z=S.symbols('s t z')
m=(1+s)*(1+t); f=m+q(1,2); g=f-(t+q(3,4)); h=g+q(3,4)
assert S.expand(h-((z+q(3,4))+(s+q(3,4))))==s*t-z
print('PASS: exact symbolic elimination proves reciprocal-square, square-product, and shifted-product identities.')
