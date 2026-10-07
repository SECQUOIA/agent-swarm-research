$if not set N $set N 1000
$if not set tol $set tol 0
Set i /1*%N%/;
Variables x(i), f;
Equations obj, cl(i), cu(i);
obj.. f =e= sum(i$(mod(ord(i),2)=1), rPower(sqr(x(i)), sqr(x(i+1))+1) + rPower(sqr(x(i+1)), sqr(x(i))+1));
cl(i)$(ord(i) <= card(i)-2).. 3*x(i+1) - x(i) - 2*x(i+2) - 2*sqr(x(i+1)) + 1 =g= -%tol%;
cu(i)$(ord(i) <= card(i)-2).. 3*x(i+1) - x(i) - 2*x(i+2) - 2*sqr(x(i+1)) + 1 =l= %tol%;
$include lukvle10_p5start.inc
Model m /all/;
option nlp = %solver%;
Solve m using nlp minimizing f;
file res /lukvtol_res.txt/; res.ap = 1; res.nd = 9;
put res '%N% tol=%tol% %solver% ' f.l ' ' m.modelstat ' ' m.solvestat /;
