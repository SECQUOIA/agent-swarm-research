$if not set T $set T 400
$if not set damp $set damp 0.05
Set t /0*%T%/;
Scalar dt, a1, c1, c2;
dt = 20/%T%; a1 = dt/2; c1 = 0.02*dt; c2 = %damp%*dt;
Variables x(t), y(t), u(t), f;
Equations obj, cb(t), cc(t);
obj.. f =e= a1*sum(t, sqr(x(t)));
cb(t)$(ord(t) < card(t)).. x(t+1) - x(t) - dt*y(t) =e= 0;
cc(t)$(ord(t) < card(t)).. y(t+1) - y(t) - dt*u(t) + c1*x(t) + c2*sqr(y(t)) =e= 0;
y.lo(t) = -1; u.lo(t) = -0.2; u.up(t) = 0.2;
x.fx('0') = 10; y.fx('0') = 0; y.fx('%T%') = 0;
y.l(t)$(ord(t)>1 and ord(t)<card(t)) = -1;
u.fx(t)$(ord(t)=card(t)) = 0;
Model m /all/;
option nlp = %solver%;
m.optfile = 0;
Solve m using nlp minimizing f;
file res /res.txt/; res.ap = 1; res.nd = 8;
put res '%T% %damp% %solver% ' f.l ' ' m.modelstat ' ' m.solvestat /;
