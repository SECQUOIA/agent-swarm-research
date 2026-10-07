* Own transcription of Coleman-Liao problem 5 / CUTEst DTOC5 with coefficient c on h*y^2
* (c=1: source model; c=4: MINLPLib/QPLIB 8585 variant).  y(1)=1, h=1/N.
$if not set N $set N 10
$if not set c $set c 1
Set t /1*%N%/; Set tt(t); tt(t) = yes$(ord(t) < card(t));
Scalar h; h = 1/%N%;
Variables x(t), y(t), f;
Equations obj, dyn(t);
obj.. f =e= h*sum(tt, sqr(y(tt)) + sqr(x(tt)));
dyn(tt(t)).. y(t+1) =e= y(t) + %c%*h*sqr(y(t)) - h*x(t);
y.fx('1') = 1; x.l(t) = 1; y.l(t) = 1;
x.fx(t)$(not tt(t)) = 0;
Model m /all/;
option nlp=%solver%;
Solve m using nlp minimizing f;
file res /'dtoc5_%N%_%c%_%solver%.txt'/; put res; put 'N=%N% c=%c% solver=%solver% obj=' f.l:22:12 ' ms=' m.modelstat:3:0 ' ss=' m.solvestat:3:0 /; putclose;
