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
	c12_hi
	c13_hi
	c14_hi
	c15_lo
	c15_hi
	c16_lo
	c16_hi
	c17_lo
	c17_hi
	c18_lo
	c18_hi
	c19_lo
	c19_hi
	c20_lo
	c20_hi
	c21_lo
	c21_hi
	c22_lo
	c22_hi
	c23_hi
	c24_hi
	c25_hi
	c26_hi
	c27_hi
	c28_hi
	c29_hi
	c30_hi
	c31
	c32
	c33
	c34
	c35
	c36
	c37_hi
	c38_hi
	c39_hi
	c40_hi
	c41_hi
	c42_hi
	c43_hi
	c44_hi
	c45_hi
	c46_hi
	c47_hi
	c48_hi
	c49_hi
	c50_hi
	c51_hi
	c52_hi
	c53_hi
	c54_hi
	c55_hi
	c56_hi
	c57_hi
	c58_hi
	c59_hi
	c60_hi
	c61;

BINARY VARIABLES
	x19
	x20
	x21
	x22
	x23
	x24
	x25
	x26
	x27
	x28
	x29
	x30
	x31
	x32
	x33
	x34
	x35
	x36
	x37
	x38
	x39
	x40
	x41
	x42;

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
	x14
	x15
	x16
	x17
	x18;

VARIABLES
	GAMS_OBJECTIVE
	;


c1_hi.. x1 + x2 - x3 =l= 0 ;
c2_hi.. x4 + x5 - x3 =l= 0 ;
c3_hi.. x6 + x7 - x3 =l= 0 ;
c4_hi.. x8 + x9 - x3 =l= 0 ;
c5_hi.. x10 + x11 - x12 =l= 0 ;
c6_hi.. x13 + x14 - x12 =l= 0 ;
c7_hi.. x15 + x16 - x12 =l= 0 ;
c8_hi.. x17 + x18 - x12 =l= 0 ;
c9_hi.. 40/x11 - x2 =l= 0 ;
c10_hi.. 50/x14 - x5 =l= 0 ;
c11_hi.. 60/x16 - x7 =l= 0 ;
c12_hi.. 35/x18 - x9 =l= 0 ;
c13_hi.. x3 =l= 100 ;
c14_hi.. x12 =l= 100 ;
c15_lo.. 3 =l= x2 ;
c15_hi.. x2 =l= 13.333333333333334 ;
c16_lo.. 3 =l= x5 ;
c16_hi.. x5 =l= 16.666666666666668 ;
c17_lo.. 3 =l= x7 ;
c17_hi.. x7 =l= 20 ;
c18_lo.. 3 =l= x9 ;
c18_hi.. x9 =l= 11.666666666666666 ;
c19_lo.. 3 =l= x11 ;
c19_hi.. x11 =l= 13.333333333333334 ;
c20_lo.. 3 =l= x14 ;
c20_hi.. x14 =l= 16.666666666666668 ;
c21_lo.. 3 =l= x16 ;
c21_hi.. x16 =l= 20 ;
c22_lo.. 3 =l= x18 ;
c22_hi.. x18 =l= 11.666666666666666 ;
c23_hi.. x1 =l= 97 ;
c24_hi.. x4 =l= 97 ;
c25_hi.. x6 =l= 97 ;
c26_hi.. x8 =l= 97 ;
c27_hi.. x10 =l= 97 ;
c28_hi.. x13 =l= 97 ;
c29_hi.. x15 =l= 97 ;
c30_hi.. x17 =l= 97 ;
c31.. x19 + x20 + x21 + x22 =e= 1 ;
c32.. x23 + x24 + x25 + x26 =e= 1 ;
c33.. x27 + x28 + x29 + x30 =e= 1 ;
c34.. x31 + x32 + x33 + x34 =e= 1 ;
c35.. x35 + x36 + x37 + x38 =e= 1 ;
c36.. x39 + x40 + x41 + x42 =e= 1 ;
c37_hi.. x1 + x2 - x4 - 200*(1 - x19) =l= 0 ;
c38_hi.. x10 + x11 - x13 - 200*(1 - x20) =l= 0 ;
c39_hi.. x4 + x5 - x1 - 200*(1 - x21) =l= 0 ;
c40_hi.. x13 + x14 - x10 - 200*(1 - x22) =l= 0 ;
c41_hi.. x1 + x2 - x6 - 200*(1 - x23) =l= 0 ;
c42_hi.. x10 + x11 - x15 - 200*(1 - x24) =l= 0 ;
c43_hi.. x6 + x7 - x1 - 200*(1 - x25) =l= 0 ;
c44_hi.. x15 + x16 - x10 - 200*(1 - x26) =l= 0 ;
c45_hi.. x1 + x2 - x8 - 200*(1 - x27) =l= 0 ;
c46_hi.. x10 + x11 - x17 - 200*(1 - x28) =l= 0 ;
c47_hi.. x8 + x9 - x1 - 200*(1 - x29) =l= 0 ;
c48_hi.. x17 + x18 - x10 - 200*(1 - x30) =l= 0 ;
c49_hi.. x4 + x5 - x6 - 200*(1 - x31) =l= 0 ;
c50_hi.. x13 + x14 - x15 - 200*(1 - x32) =l= 0 ;
c51_hi.. x6 + x7 - x4 - 200*(1 - x33) =l= 0 ;
c52_hi.. x15 + x16 - x13 - 200*(1 - x34) =l= 0 ;
c53_hi.. x4 + x5 - x8 - 200*(1 - x35) =l= 0 ;
c54_hi.. x13 + x14 - x17 - 200*(1 - x36) =l= 0 ;
c55_hi.. x8 + x9 - x4 - 200*(1 - x37) =l= 0 ;
c56_hi.. x17 + x18 - x13 - 200*(1 - x38) =l= 0 ;
c57_hi.. x6 + x7 - x8 - 200*(1 - x39) =l= 0 ;
c58_hi.. x15 + x16 - x17 - 200*(1 - x40) =l= 0 ;
c59_hi.. x8 + x9 - x6 - 200*(1 - x41) =l= 0 ;
c60_hi.. x17 + x18 - x15 - 200*(1 - x42) =l= 0 ;
c61.. GAMS_OBJECTIVE =e= 2*(x3 + x12) ;

x1.up = 100;
x2.up = 100;
x4.up = 100;
x5.up = 100;
x6.up = 100;
x7.up = 100;
x8.up = 100;
x9.up = 100;
x10.up = 100;
x11.up = 100;
x13.up = 100;
x14.up = 100;
x15.up = 100;
x16.up = 100;
x17.up = 100;
x18.up = 100;

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
put x27 ' ' x27.l ' ' x27.m /;
put x28 ' ' x28.l ' ' x28.m /;
put x29 ' ' x29.l ' ' x29.m /;
put x30 ' ' x30.l ' ' x30.m /;
put x31 ' ' x31.l ' ' x31.m /;
put x32 ' ' x32.l ' ' x32.m /;
put x33 ' ' x33.l ' ' x33.m /;
put x34 ' ' x34.l ' ' x34.m /;
put x35 ' ' x35.l ' ' x35.m /;
put x36 ' ' x36.l ' ' x36.m /;
put x37 ' ' x37.l ' ' x37.m /;
put x38 ' ' x38.l ' ' x38.m /;
put x39 ' ' x39.l ' ' x39.m /;
put x40 ' ' x40.l ' ' x40.m /;
put x41 ' ' x41.l ' ' x41.m /;
put x42 ' ' x42.l ' ' x42.m /;
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
put c12_hi ' ' c12_hi.l ' ' c12_hi.m /;
put c13_hi ' ' c13_hi.l ' ' c13_hi.m /;
put c14_hi ' ' c14_hi.l ' ' c14_hi.m /;
put c15_lo ' ' c15_lo.l ' ' c15_lo.m /;
put c15_hi ' ' c15_hi.l ' ' c15_hi.m /;
put c16_lo ' ' c16_lo.l ' ' c16_lo.m /;
put c16_hi ' ' c16_hi.l ' ' c16_hi.m /;
put c17_lo ' ' c17_lo.l ' ' c17_lo.m /;
put c17_hi ' ' c17_hi.l ' ' c17_hi.m /;
put c18_lo ' ' c18_lo.l ' ' c18_lo.m /;
put c18_hi ' ' c18_hi.l ' ' c18_hi.m /;
put c19_lo ' ' c19_lo.l ' ' c19_lo.m /;
put c19_hi ' ' c19_hi.l ' ' c19_hi.m /;
put c20_lo ' ' c20_lo.l ' ' c20_lo.m /;
put c20_hi ' ' c20_hi.l ' ' c20_hi.m /;
put c21_lo ' ' c21_lo.l ' ' c21_lo.m /;
put c21_hi ' ' c21_hi.l ' ' c21_hi.m /;
put c22_lo ' ' c22_lo.l ' ' c22_lo.m /;
put c22_hi ' ' c22_hi.l ' ' c22_hi.m /;
put c23_hi ' ' c23_hi.l ' ' c23_hi.m /;
put c24_hi ' ' c24_hi.l ' ' c24_hi.m /;
put c25_hi ' ' c25_hi.l ' ' c25_hi.m /;
put c26_hi ' ' c26_hi.l ' ' c26_hi.m /;
put c27_hi ' ' c27_hi.l ' ' c27_hi.m /;
put c28_hi ' ' c28_hi.l ' ' c28_hi.m /;
put c29_hi ' ' c29_hi.l ' ' c29_hi.m /;
put c30_hi ' ' c30_hi.l ' ' c30_hi.m /;
put c31 ' ' c31.l ' ' c31.m /;
put c32 ' ' c32.l ' ' c32.m /;
put c33 ' ' c33.l ' ' c33.m /;
put c34 ' ' c34.l ' ' c34.m /;
put c35 ' ' c35.l ' ' c35.m /;
put c36 ' ' c36.l ' ' c36.m /;
put c37_hi ' ' c37_hi.l ' ' c37_hi.m /;
put c38_hi ' ' c38_hi.l ' ' c38_hi.m /;
put c39_hi ' ' c39_hi.l ' ' c39_hi.m /;
put c40_hi ' ' c40_hi.l ' ' c40_hi.m /;
put c41_hi ' ' c41_hi.l ' ' c41_hi.m /;
put c42_hi ' ' c42_hi.l ' ' c42_hi.m /;
put c43_hi ' ' c43_hi.l ' ' c43_hi.m /;
put c44_hi ' ' c44_hi.l ' ' c44_hi.m /;
put c45_hi ' ' c45_hi.l ' ' c45_hi.m /;
put c46_hi ' ' c46_hi.l ' ' c46_hi.m /;
put c47_hi ' ' c47_hi.l ' ' c47_hi.m /;
put c48_hi ' ' c48_hi.l ' ' c48_hi.m /;
put c49_hi ' ' c49_hi.l ' ' c49_hi.m /;
put c50_hi ' ' c50_hi.l ' ' c50_hi.m /;
put c51_hi ' ' c51_hi.l ' ' c51_hi.m /;
put c52_hi ' ' c52_hi.l ' ' c52_hi.m /;
put c53_hi ' ' c53_hi.l ' ' c53_hi.m /;
put c54_hi ' ' c54_hi.l ' ' c54_hi.m /;
put c55_hi ' ' c55_hi.l ' ' c55_hi.m /;
put c56_hi ' ' c56_hi.l ' ' c56_hi.m /;
put c57_hi ' ' c57_hi.l ' ' c57_hi.m /;
put c58_hi ' ' c58_hi.l ' ' c58_hi.m /;
put c59_hi ' ' c59_hi.l ' ' c59_hi.m /;
put c60_hi ' ' c60_hi.l ' ' c60_hi.m /;
put c61 ' ' c61.l ' ' c61.m /;
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
