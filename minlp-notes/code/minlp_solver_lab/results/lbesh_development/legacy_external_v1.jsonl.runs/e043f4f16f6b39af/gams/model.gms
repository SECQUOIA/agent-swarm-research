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
	c9_hi
	c10_hi
	c11_hi
	c12_lo
	c12_hi
	c13_lo
	c13_hi
	c14_lo
	c14_hi
	c15_lo
	c15_hi
	c16_lo
	c16_hi
	c17_lo
	c17_hi
	c18_hi
	c19_hi
	c20_hi
	c21_hi
	c22_hi
	c23_hi
	c24
	c25
	c26
	c27_hi
	c28_hi
	c29_hi
	c30_hi
	c31_hi
	c32_hi
	c33_hi
	c34_hi
	c35_hi
	c36_hi
	c37_hi
	c38_hi
	c39;

BINARY VARIABLES
	x15
	x16
	x17
	x18
	x19
	x20
	x21
	x22
	x23
	x24
	x25
	x26;

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
	x10
	x11
	x12
	x13
	x14;

VARIABLES
	GAMS_OBJECTIVE
	;


c1_hi.. x1 + x2 - x3 =l= 0 ;
c2_hi.. x4 + x5 - x3 =l= 0 ;
c3_hi.. x6 + x7 - x3 =l= 0 ;
c4_hi.. x8 + x9 - x10 =l= 0 ;
c5_hi.. x11 + x12 - x10 =l= 0 ;
c6_hi.. x13 + x14 - x10 =l= 0 ;
c7_hi.. 40/x9 - x2 =l= 0 ;
c8_hi.. 50/x12 - x5 =l= 0 ;
c9_hi.. 60/x14 - x7 =l= 0 ;
c10_hi.. x3 =l= 30 ;
c11_hi.. x10 =l= 30 ;
c12_lo.. 1 =l= x2 ;
c12_hi.. x2 =l= 40 ;
c13_lo.. 1 =l= x5 ;
c13_hi.. x5 =l= 50 ;
c14_lo.. 1 =l= x7 ;
c14_hi.. x7 =l= 60 ;
c15_lo.. 1 =l= x9 ;
c15_hi.. x9 =l= 40 ;
c16_lo.. 1 =l= x12 ;
c16_hi.. x12 =l= 50 ;
c17_lo.. 1 =l= x14 ;
c17_hi.. x14 =l= 60 ;
c18_hi.. x1 =l= 29 ;
c19_hi.. x4 =l= 29 ;
c20_hi.. x6 =l= 29 ;
c21_hi.. x8 =l= 29 ;
c22_hi.. x11 =l= 29 ;
c23_hi.. x13 =l= 29 ;
c24.. x15 + x16 + x17 + x18 =e= 1 ;
c25.. x19 + x20 + x21 + x22 =e= 1 ;
c26.. x23 + x24 + x25 + x26 =e= 1 ;
c27_hi.. x1 + x2 - x4 - 60*(1 - x15) =l= 0 ;
c28_hi.. x8 + x9 - x11 - 60*(1 - x16) =l= 0 ;
c29_hi.. x4 + x5 - x1 - 60*(1 - x17) =l= 0 ;
c30_hi.. x11 + x12 - x8 - 60*(1 - x18) =l= 0 ;
c31_hi.. x1 + x2 - x6 - 60*(1 - x19) =l= 0 ;
c32_hi.. x8 + x9 - x13 - 60*(1 - x20) =l= 0 ;
c33_hi.. x6 + x7 - x1 - 60*(1 - x21) =l= 0 ;
c34_hi.. x13 + x14 - x8 - 60*(1 - x22) =l= 0 ;
c35_hi.. x4 + x5 - x6 - 60*(1 - x23) =l= 0 ;
c36_hi.. x11 + x12 - x13 - 60*(1 - x24) =l= 0 ;
c37_hi.. x6 + x7 - x4 - 60*(1 - x25) =l= 0 ;
c38_hi.. x13 + x14 - x11 - 60*(1 - x26) =l= 0 ;
c39.. GAMS_OBJECTIVE =e= 2*(x3 + x10) ;

x1.up = 30;
x2.up = 30;
x4.up = 30;
x5.up = 30;
x6.up = 30;
x7.up = 30;
x8.up = 30;
x9.up = 30;
x11.up = 30;
x12.up = 30;
x13.up = 30;
x14.up = 30;

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
put x7 ' ' x7.l ' ' x7.m /;
put x8 ' ' x8.l ' ' x8.m /;
put x9 ' ' x9.l ' ' x9.m /;
put x10 ' ' x10.l ' ' x10.m /;
put x11 ' ' x11.l ' ' x11.m /;
put x12 ' ' x12.l ' ' x12.m /;
put x13 ' ' x13.l ' ' x13.m /;
put x14 ' ' x14.l ' ' x14.m /;
put x15 ' ' x15.l ' ' x15.m /;
put x16 ' ' x16.l ' ' x16.m /;
put x17 ' ' x17.l ' ' x17.m /;
put x18 ' ' x18.l ' ' x18.m /;
put x19 ' ' x19.l ' ' x19.m /;
put x20 ' ' x20.l ' ' x20.m /;
put x21 ' ' x21.l ' ' x21.m /;
put x22 ' ' x22.l ' ' x22.m /;
put x23 ' ' x23.l ' ' x23.m /;
put x24 ' ' x24.l ' ' x24.m /;
put x25 ' ' x25.l ' ' x25.m /;
put x26 ' ' x26.l ' ' x26.m /;
put c1_hi ' ' c1_hi.l ' ' c1_hi.m /;
put c2_hi ' ' c2_hi.l ' ' c2_hi.m /;
put c3_hi ' ' c3_hi.l ' ' c3_hi.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5_hi ' ' c5_hi.l ' ' c5_hi.m /;
put c6_hi ' ' c6_hi.l ' ' c6_hi.m /;
put c7_hi ' ' c7_hi.l ' ' c7_hi.m /;
put c8_hi ' ' c8_hi.l ' ' c8_hi.m /;
put c9_hi ' ' c9_hi.l ' ' c9_hi.m /;
put c10_hi ' ' c10_hi.l ' ' c10_hi.m /;
put c11_hi ' ' c11_hi.l ' ' c11_hi.m /;
put c12_lo ' ' c12_lo.l ' ' c12_lo.m /;
put c12_hi ' ' c12_hi.l ' ' c12_hi.m /;
put c13_lo ' ' c13_lo.l ' ' c13_lo.m /;
put c13_hi ' ' c13_hi.l ' ' c13_hi.m /;
put c14_lo ' ' c14_lo.l ' ' c14_lo.m /;
put c14_hi ' ' c14_hi.l ' ' c14_hi.m /;
put c15_lo ' ' c15_lo.l ' ' c15_lo.m /;
put c15_hi ' ' c15_hi.l ' ' c15_hi.m /;
put c16_lo ' ' c16_lo.l ' ' c16_lo.m /;
put c16_hi ' ' c16_hi.l ' ' c16_hi.m /;
put c17_lo ' ' c17_lo.l ' ' c17_lo.m /;
put c17_hi ' ' c17_hi.l ' ' c17_hi.m /;
put c18_hi ' ' c18_hi.l ' ' c18_hi.m /;
put c19_hi ' ' c19_hi.l ' ' c19_hi.m /;
put c20_hi ' ' c20_hi.l ' ' c20_hi.m /;
put c21_hi ' ' c21_hi.l ' ' c21_hi.m /;
put c22_hi ' ' c22_hi.l ' ' c22_hi.m /;
put c23_hi ' ' c23_hi.l ' ' c23_hi.m /;
put c24 ' ' c24.l ' ' c24.m /;
put c25 ' ' c25.l ' ' c25.m /;
put c26 ' ' c26.l ' ' c26.m /;
put c27_hi ' ' c27_hi.l ' ' c27_hi.m /;
put c28_hi ' ' c28_hi.l ' ' c28_hi.m /;
put c29_hi ' ' c29_hi.l ' ' c29_hi.m /;
put c30_hi ' ' c30_hi.l ' ' c30_hi.m /;
put c31_hi ' ' c31_hi.l ' ' c31_hi.m /;
put c32_hi ' ' c32_hi.l ' ' c32_hi.m /;
put c33_hi ' ' c33_hi.l ' ' c33_hi.m /;
put c34_hi ' ' c34_hi.l ' ' c34_hi.m /;
put c35_hi ' ' c35_hi.l ' ' c35_hi.m /;
put c36_hi ' ' c36_hi.l ' ' c36_hi.m /;
put c37_hi ' ' c37_hi.l ' ' c37_hi.m /;
put c38_hi ' ' c38_hi.l ' ' c38_hi.m /;
put c39 ' ' c39.l ' ' c39.m /;
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
