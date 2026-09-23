"""Independent symbolic audit; does not import the author checker."""
from itertools import product
import sympy as s
x,y,z,I,W=s.symbols('x y z I W')
H=s.Rational(1,2)
comp=lambda v:s.Rational(5,2)-v
# Original fixed-injection residuals for C_I,I,D, respectively.
rC=(1-I)+(1-comp(x))+H
rI=I*((I-W)+(I-1))+1
rD=(1-W)+2*(1-comp(x))+(1-comp(y))+s.Rational(5,2)
gb=s.groebner([rC,rI,rD],I,W,x,y)
expected=s.groebner([I-x,W-2*x+1-y,x*y-1],I,W,x,y)
assert gb==expected
print('PASS: inversion original-bus ideal equals <I-x, W-2x+1-y, xy-1>.')
rA=(1-x)+(1-y)+(1-comp(z))-H
assert s.expand(rA)==z-x-y
assert s.expand((1-x)+(1-y)+H)==s.Rational(5,2)-x-y
print('PASS: addition and complement original-bus residuals.')
h=2*x-1+1/x
assert s.diff(h,x)==2-1/x**2
assert s.simplify(h.subs(x,s.sqrt(2)/2))==2*s.sqrt(2)-1
assert h.subs(x,H)==2 and h.subs(x,2)==s.Rational(7,2)
print('PASS: auxiliary voltage extremum and endpoints.')
# Independently enumerate all parity-request sequences through length 12,
# and check allocation extension bounds, uniqueness and max path+gadget degree.
count=0
for length in range(13):
 for seq in product((0,1),repeat=length):
  endpoint=0; used=set(); old=0
  for requested in seq:
   while endpoint%2 != requested or endpoint in used: endpoint+=1
   assert endpoint-old<=2
   used.add(endpoint); old=endpoint
  assert len(used)==length and endpoint<=2*length
  for vertex in range(endpoint+1):
   degree=(vertex>0)+(vertex<endpoint)+(vertex in used)
   assert degree<=3
  count+=1
print(f'PASS: {count} independently enumerated copy-request sequences, length <=12.')
