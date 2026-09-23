$offlisting
$offdigit

EQUATIONS
	c1
	c2_hi
	c3_lo
	c4_hi
	c5_hi
	c6_lo
	c7_hi
	c8_hi
	c9_lo
	c10_hi
	c11;

BINARY VARIABLES
	x1
	x2
	x3;

POSITIVE VARIABLES
	x4
	x5
	x6;

VARIABLES
	GAMS_OBJECTIVE
	;


c1.. x1 + x2 + x3 =e= 1 ;
c2_hi.. power(x4, 2) + power(x5, 2) - 127*(1 - x1) =l= 1 ;
c3_lo.. 2 =l= x6 - (-2)*(1 - x1) ;
c4_hi.. x6 - (1 - x1) =l= 2 ;
c5_hi.. power((x4 + (-4)), 2) + power((x5 + (-1)), 2) - 64*(1 - x2) =l= 1 ;
c6_lo.. 3 =l= x6 - (-3)*(1 - x2) ;
c7_hi.. x6 - 0*(1 - x2) =l= 3 ;
c8_hi.. power((x4 + (-2)), 2) + power((x5 + (-4)), 2) - 51*(1 - x3) =l= 1 ;
c9_lo.. 1 =l= x6 + (1 - x3) ;
c10_hi.. x6 - 2*(1 - x3) =l= 1 ;
c11.. GAMS_OBJECTIVE =e= power((x4 + (-3)), 2) + power((x5 + (-2)), 2) + x6 ;

x4.up = 8;
x5.up = 8;
x6.up = 3;

MODEL GAMS_MODEL /all/ ;
option minlp=scip;
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
put c1 ' ' c1.l ' ' c1.m /;
put c2_hi ' ' c2_hi.l ' ' c2_hi.m /;
put c3_lo ' ' c3_lo.l ' ' c3_lo.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5_hi ' ' c5_hi.l ' ' c5_hi.m /;
put c6_lo ' ' c6_lo.l ' ' c6_lo.m /;
put c7_hi ' ' c7_hi.l ' ' c7_hi.m /;
put c8_hi ' ' c8_hi.l ' ' c8_hi.m /;
put c9_lo ' ' c9_lo.l ' ' c9_lo.m /;
put c10_hi ' ' c10_hi.l ' ' c10_hi.m /;
put c11 ' ' c11.l ' ' c11.m /;
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
