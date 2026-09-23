$offlisting
$offdigit

EQUATIONS
	c1_hi
	c2_hi
	c3_hi
	c4_hi
	c5_hi
	c6_hi
	c7_hi
	c8_hi
	c9_lo
	c9_hi
	c10_lo
	c10_hi
	c11_lo
	c11_hi
	c12_lo
	c12_hi
	c13_hi
	c14_hi
	c15_hi
	c16_hi
	c17
	c18_hi
	c19_hi
	c20_hi
	c21_hi
	c22;

BINARY VARIABLES
	x11
	x12
	x13
	x14;

POSITIVE VARIABLES
	x1
	x2
	x3
	x4
	x5
	x6
	x7
	x8
	x9
	x10;

VARIABLES
	GAMS_OBJECTIVE
	;


c1_hi.. x1 + x2 - x3 =l= 0 ;
c2_hi.. x4 + x5 - x3 =l= 0 ;
c3_hi.. x6 + x7 - x8 =l= 0 ;
c4_hi.. x9 + x10 - x8 =l= 0 ;
c5_hi.. 40/x7 - x2 =l= 0 ;
c6_hi.. 50/x10 - x5 =l= 0 ;
c7_hi.. x3 =l= 30 ;
c8_hi.. x8 =l= 30 ;
c9_lo.. 1 =l= x2 ;
c9_hi.. x2 =l= 40 ;
c10_lo.. 1 =l= x5 ;
c10_hi.. x5 =l= 50 ;
c11_lo.. 1 =l= x7 ;
c11_hi.. x7 =l= 40 ;
c12_lo.. 1 =l= x10 ;
c12_hi.. x10 =l= 50 ;
c13_hi.. x1 =l= 29 ;
c14_hi.. x4 =l= 29 ;
c15_hi.. x6 =l= 29 ;
c16_hi.. x9 =l= 29 ;
c17.. x11 + x12 + x13 + x14 =e= 1 ;
c18_hi.. x1 + x2 - x4 - 60*(1 - x11) =l= 0 ;
c19_hi.. x6 + x7 - x9 - 60*(1 - x12) =l= 0 ;
c20_hi.. x4 + x5 - x1 - 60*(1 - x13) =l= 0 ;
c21_hi.. x9 + x10 - x6 - 60*(1 - x14) =l= 0 ;
c22.. GAMS_OBJECTIVE =e= 2*(x3 + x8) ;

x1.up = 30;
x2.up = 30;
x4.up = 30;
x5.up = 30;
x6.up = 30;
x7.up = 30;
x7.l = 1;
x9.up = 30;
x10.up = 30;
x10.l = 1;

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
put x9 ' ' x9.l ' ' x9.m /;
put x10 ' ' x10.l ' ' x10.m /;
put x11 ' ' x11.l ' ' x11.m /;
put x12 ' ' x12.l ' ' x12.m /;
put x13 ' ' x13.l ' ' x13.m /;
put x14 ' ' x14.l ' ' x14.m /;
put c1_hi ' ' c1_hi.l ' ' c1_hi.m /;
put c2_hi ' ' c2_hi.l ' ' c2_hi.m /;
put c3_hi ' ' c3_hi.l ' ' c3_hi.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5_hi ' ' c5_hi.l ' ' c5_hi.m /;
put c6_hi ' ' c6_hi.l ' ' c6_hi.m /;
put c7_hi ' ' c7_hi.l ' ' c7_hi.m /;
put c8_hi ' ' c8_hi.l ' ' c8_hi.m /;
put c9_lo ' ' c9_lo.l ' ' c9_lo.m /;
put c9_hi ' ' c9_hi.l ' ' c9_hi.m /;
put c10_lo ' ' c10_lo.l ' ' c10_lo.m /;
put c10_hi ' ' c10_hi.l ' ' c10_hi.m /;
put c11_lo ' ' c11_lo.l ' ' c11_lo.m /;
put c11_hi ' ' c11_hi.l ' ' c11_hi.m /;
put c12_lo ' ' c12_lo.l ' ' c12_lo.m /;
put c12_hi ' ' c12_hi.l ' ' c12_hi.m /;
put c13_hi ' ' c13_hi.l ' ' c13_hi.m /;
put c14_hi ' ' c14_hi.l ' ' c14_hi.m /;
put c15_hi ' ' c15_hi.l ' ' c15_hi.m /;
put c16_hi ' ' c16_hi.l ' ' c16_hi.m /;
put c17 ' ' c17.l ' ' c17.m /;
put c18_hi ' ' c18_hi.l ' ' c18_hi.m /;
put c19_hi ' ' c19_hi.l ' ' c19_hi.m /;
put c20_hi ' ' c20_hi.l ' ' c20_hi.m /;
put c21_hi ' ' c21_hi.l ' ' c21_hi.m /;
put c22 ' ' c22.l ' ' c22.m /;
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
