$if not set T $set T 10
$if not set D $set D 0.05
Set t /0*%T%/; Set tc(t); tc(t)=yes$(ord(t)<card(t));
Scalar dt; dt = 20/%T%;
Variables x(t), y(t), u(t), f;
Equations obj, e1(t), e2(t);
obj.. f =e= (dt/2)*sum(t, sqr(x(t)));
e1(tc(t)).. x(t+1) - x(t) - dt*y(t) =e= 0;
e2(tc(t)).. y(t+1) - y(t) - dt*u(t) + 0.02*dt*x(t) + %D%*dt*sqr(y(t)) =e= 0;
y.lo(t) = -1; u.lo(t) = -0.2; u.up(t) = 0.2;
x.fx('0') = 10; y.fx('0') = 0; y.fx('%T%') = 0;
y.l(t)$(ord(t)>1 and ord(t)<card(t)) = -1;
Model m /all/; m.optfile=0;
option nlp=ipopt;
Solve m using nlp minimizing f;
file res /'optc_%T%_%D%.txt'/; put res; put 'T=%T% D=%D% obj=' f.l:20:10 ' ms=' m.modelstat:3:0 ' ss=' m.solvestat:3:0 /; putclose;
