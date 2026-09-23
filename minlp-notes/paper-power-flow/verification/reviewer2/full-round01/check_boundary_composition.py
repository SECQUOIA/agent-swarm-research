"""Exact checks for the trivial connected principal-window instance and summary examples."""
from fractions import Fraction as F
import sympy as s
# A connected two-bus singleton is the proposed exceptional YES image.
v=(F(1),F(1));power=(v[0]*(v[0]-v[1]),v[1]*(v[1]-v[0]))
c=1-F(1,2**2)
assert power==(0,0) and c==F(3,4)
assert v[0]*v[1]>=c*v[0]*v[1]
print('PASS: connected two-bus voltage-one, injection-zero image uses unit conductance and c_2=3/4.')
# The six claimed feasible source solutions, checked symbolically, including bounds.
x,y,z,u,w,y1,y2,y3=s.symbols('x y z u w y1 y2 y3')
cases=[([x*x-1],{x:s.Integer(1)}),
 ([x+x-y,x*y-1],{x:1/s.sqrt(2),y:s.sqrt(2)}),
 ([x+x-y,y*y-1],{x:s.Rational(1,2),y:s.Integer(1)}),
 ([x+x-y,y+y-z],{x:s.Rational(1,2),y:s.Integer(1),z:s.Integer(2)}),
 ([x+y-z,x*z-1,y*y-1],{x:(s.sqrt(5)-1)/2,y:s.Integer(1),z:(s.sqrt(5)+1)/2}),
 ([u+u-w,w*w-1,u*y1-1,u*y2-1,u*y3-1],{u:s.Rational(1,2),w:s.Integer(1),y1:s.Integer(2),y2:s.Integer(2),y3:s.Integer(2)})]
for equations,assignment in cases:
 assert all(s.simplify(eq.subs(assignment))==0 for eq in equations)
 assert all(value>=s.Rational(1,2) and value<=2 for value in assignment.values())
print('PASS: all six feasible analytic source profiles satisfy their exact equations and bounds.')
print('The two infeasible profiles are excluded analytically: z=1 contradicts x+y>=2, or forces x=1/4.')
