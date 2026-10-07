$if not set N $set N 1000
Set i /1*%N%/;
Variables x(i), f;
Equations obj, c(i);
obj.. f =e= sum(i$(mod(ord(i),2)=1), rPower(sqr(x(i)), sqr(x(i+1))+1) + rPower(sqr(x(i+1)), sqr(x(i))+1));
c(i)$(ord(i) <= card(i)-2).. 3*x(i+1) - x(i) - 2*x(i+2) - 2*sqr(x(i+1)) =e= -1;
x.l(i)$(mod(ord(i),2)=1) = -1;
x.l(i)$(mod(ord(i),2)=0) = 1;
Model m /all/;
option nlp = %solver%;
Solve m using nlp minimizing f;
file res /lukv_res.txt/; res.ap = 1; res.nd = 9;
put res '%N% %solver% ' f.l ' ' m.modelstat ' ' m.solvestat ' ' m.sumInfes /;
