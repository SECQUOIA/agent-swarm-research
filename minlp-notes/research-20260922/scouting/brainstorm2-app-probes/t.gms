variables x, z; positive variable y; y.up=3; x.lo=-2; x.up=2;
equations e1, e2; e1.. z =e= signpower(x,1.852) - y*x; e2.. x+y =g= 1;
model m /all/; option nlp=scip; solve m using nlp minimizing z; display z.l;
option nlp=baron; solve m using nlp minimizing z; display z.l;
