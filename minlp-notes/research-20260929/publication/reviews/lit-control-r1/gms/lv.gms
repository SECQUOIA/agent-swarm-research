$if not set tol $set tol 0
Set i /1*1000/; Set k(i); k(i)=yes$(ord(i)<=998);
Set odd(i); odd(i)=yes$(mod(ord(i),2)=1);
Variables x(i), f;
Equations obj, cu(i), cl(i);
obj.. f =e= sum(odd(i), rpower(sqr(x(i)), sqr(x(i+1))+1) + rpower(sqr(x(i+1)), sqr(x(i))+1));
cu(k(i)).. (3-2*x(i+1))*x(i+1) + 1 - x(i) - 2*x(i+2) =l= %tol%;
cl(k(i)).. (3-2*x(i+1))*x(i+1) + 1 - x(i) - 2*x(i+2) =g= -%tol%;
$include lv_start.inc
Model m /all/; option nlp=ipopt;
Solve m using nlp minimizing f;
file res /'lv_%tol%.txt'/; put res; put 'tol=%tol% obj=' f.l:20:10 ' ms=' m.modelstat:3:0 /; putclose;
