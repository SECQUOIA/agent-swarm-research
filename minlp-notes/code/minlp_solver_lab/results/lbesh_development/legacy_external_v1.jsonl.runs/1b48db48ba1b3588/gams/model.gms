$offlisting
$offdigit

EQUATIONS
	c1
	c2
	c3
	c4_hi
	c5_hi
	c6_hi
	c7_hi
	c8_hi
	c9_hi
	c10;

BINARY VARIABLES
	x1
	x2
	x3
	x4
	x5
	x6;

POSITIVE VARIABLES
	x8;

VARIABLES
	GAMS_OBJECTIVE
	x7;


c1.. x1 + x2 =e= 1 ;
c2.. x3 + x4 =e= 1 ;
c3.. x5 + x6 =e= 1 ;
c4_hi.. power(x7, 2) + 0.25*power((x8 + (-5)), 2) - 41.25*(1 - x1) =l= 1 ;
c5_hi.. power((x7 + (-5)), 2) + 0.25*power((x8 + (-2)), 2) - 41.25*(1 - x2) =l= 1 ;
c6_hi.. power(x7, 2) + 0.25*power((x8 + (-2)), 2) - 41.25*(1 - x3) =l= 1 ;
c7_hi.. power((x7 + (-5)), 2) + 0.25*power((x8 + (-5)), 2) - 41.25*(1 - x4) =l= 1 ;
c8_hi.. power(x7, 2) + 0.25*power((x8 + (-3.5)), 2) - 38.0625*(1 - x5) =l= 1 ;
c9_hi.. power((x7 + (-5)), 2) + 0.25*power((x8 + (-3.5)), 2) - 38.0625*(1 - x6) =l= 1 ;
c10.. GAMS_OBJECTIVE =e= 0.2*x7 + x8 ;

x8.up = 7;
x8.l = 3.5;
x7.lo = -1;
x7.up = 6;
x7.l = 0;

MODEL GAMS_MODEL /all/ ;
option minlp=gurobi;
option solprint=off;
option limrow=0;
option limcol=0;
option solvelink=5;

* START USER ADDITIONAL OPTIONS

option reslim=120.0;
option threads=1;
option optcr=0.0001;
option optca=0.000001;

* END USER ADDITIONAL OPTIONS

SOLVE GAMS_MODEL USING minlp minimizing GAMS_OBJECTIVE;

Scalars MODELSTAT 'model status', SOLVESTAT 'solve status';
MODELSTAT = GAMS_MODEL.modelstat;
SOLVESTAT = GAMS_MODEL.solvestat;

Scalar OBJEST 'best objective', OBJVAL 'objective value';
OBJEST = GAMS_MODEL.objest;
OBJVAL = GAMS_MODEL.objval;

Scalar NUMVAR 'number of variables';
NUMVAR = GAMS_MODEL.numvar

Scalar NUMEQU 'number of equations';
NUMEQU = GAMS_MODEL.numequ

Scalar NUMDVAR 'number of discrete variables';
NUMDVAR = GAMS_MODEL.numdvar

Scalar NUMNZ 'number of nonzeros';
NUMNZ = GAMS_MODEL.numnz

Scalar ETSOLVE 'time to execute solve statement';
ETSOLVE = GAMS_MODEL.etsolve


file results /'results.dat'/;
results.nd=15;
results.nw=21;
put results;
put 'SYMBOL  :  LEVEL  :  MARGINAL' /;
put x1 ' ' x1.l ' ' x1.m /;
put x2 ' ' x2.l ' ' x2.m /;
put x3 ' ' x3.l ' ' x3.m /;
put x4 ' ' x4.l ' ' x4.m /;
put x5 ' ' x5.l ' ' x5.m /;
put x6 ' ' x6.l ' ' x6.m /;
put x7 ' ' x7.l ' ' x7.m /;
put x8 ' ' x8.l ' ' x8.m /;
put c1 ' ' c1.l ' ' c1.m /;
put c2 ' ' c2.l ' ' c2.m /;
put c3 ' ' c3.l ' ' c3.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5_hi ' ' c5_hi.l ' ' c5_hi.m /;
put c6_hi ' ' c6_hi.l ' ' c6_hi.m /;
put c7_hi ' ' c7_hi.l ' ' c7_hi.m /;
put c8_hi ' ' c8_hi.l ' ' c8_hi.m /;
put c9_hi ' ' c9_hi.l ' ' c9_hi.m /;
put c10 ' ' c10.l ' ' c10.m /;
put GAMS_OBJECTIVE ' ' GAMS_OBJECTIVE.l ' ' GAMS_OBJECTIVE.m;

file statresults /'resultsstat.dat'/;
statresults.nd=15;
statresults.nw=21;
put statresults;
put 'SYMBOL   :   VALUE' /;
put 'MODELSTAT' ' ' MODELSTAT /;

put 'SOLVESTAT' ' ' SOLVESTAT /;

put 'OBJEST' ' ' OBJEST /;

put 'OBJVAL' ' ' OBJVAL /;

put 'NUMVAR' ' ' NUMVAR /;

put 'NUMEQU' ' ' NUMEQU /;

put 'NUMDVAR' ' ' NUMDVAR /;

put 'NUMNZ' ' ' NUMNZ /;

put 'ETSOLVE' ' ' ETSOLVE /;
