* Minimal reproducer (same model as minimal/tiny2.cip)
*   min 0.2 b - 2.4 s + p  s.t.  p = s^3,  s - 0.3 b <= 0.7,
*   b binary, 0.7 <= s <= 1, 0.343 <= p <= 1.
* True optimum -1.337 at b = 0, s = 0.7, p = 0.343 (exactly feasible).
Variables obj, s, p;
Binary Variable b;
s.lo = 0.7; s.up = 1; p.lo = 0.343; p.up = 1;
* start at a feasible point with b = 1 (GAMS would otherwise pass the lower bounds,
* which happen to be the optimum, as starting point)
b.l = 1; s.l = 1; p.l = 1;
Equations defobj, cube, speed;
defobj.. obj =e= 0.2*b - 2.4*s + p;
cube..   -p + power(s,3) =e= 0;
speed..  s - 0.3*b =l= 0.7;
Model m / all /;
m.optcr = 0; m.optca = 0;
option minlp = scip, threads = 1;
$if set scipopt m.optfile = 1;
Solve m using minlp minimizing obj;
display obj.l, b.l, s.l, p.l, m.objest, m.modelstat, m.solvestat;
