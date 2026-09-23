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
	c13
	c14
	c15
	c16
	c17
	c18
	c19_hi
	c20_hi
	c21_hi
	c22_hi
	c23_hi
	c24_hi
	c25_hi
	c26_hi
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
	c61_hi
	c62_hi
	c63_hi
	c64_hi
	c65_hi
	c66_hi
	c67;

BINARY VARIABLES
	x13
	x14
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
	x26
	x27
	x28
	x29
	x30
	x31
	x32
	x33;

VARIABLES
	GAMS_OBJECTIVE
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
	x12;


c1_hi.. x1 - x2 - x3 =l= 0 ;
c2_hi.. x4 - x2 - x5 =l= 0 ;
c3_hi.. x4 - x1 - x6 =l= 0 ;
c4_hi.. x2 - x1 - x3 =l= 0 ;
c5_hi.. x2 - x4 - x5 =l= 0 ;
c6_hi.. x1 - x4 - x6 =l= 0 ;
c7_hi.. x7 - x8 - x9 =l= 0 ;
c8_hi.. x10 - x8 - x11 =l= 0 ;
c9_hi.. x10 - x7 - x12 =l= 0 ;
c10_hi.. x8 - x7 - x9 =l= 0 ;
c11_hi.. x8 - x10 - x11 =l= 0 ;
c12_hi.. x7 - x10 - x12 =l= 0 ;
c13.. x13 + x14 + x15 + x16 =e= 1 ;
c14.. x17 + x18 + x19 + x20 =e= 1 ;
c15.. x21 + x22 + x23 + x24 =e= 1 ;
c16.. x25 + x26 + x27 =e= 1 ;
c17.. x28 + x29 + x30 =e= 1 ;
c18.. x31 + x32 + x33 =e= 1 ;
c19_hi.. x2 + 2.5 - (x1 + (-3.5)) - 46*(1 - x13) =l= 0 ;
c20_hi.. x8 + 3 - (x7 + (-2.5)) - 81*(1 - x14) =l= 0 ;
c21_hi.. x1 + 3.5 - (x2 + (-2.5)) - 46*(1 - x15) =l= 0 ;
c22_hi.. x7 + 2.5 - (x8 + (-3)) - 81*(1 - x16) =l= 0 ;
c23_hi.. x2 + 2.5 - (x4 + (-1.5)) - 46*(1 - x17) =l= 0 ;
c24_hi.. x8 + 3 - (x10 + (-1.5)) - 81*(1 - x18) =l= 0 ;
c25_hi.. x4 + 1.5 - (x2 + (-2.5)) - 46*(1 - x19) =l= 0 ;
c26_hi.. x10 + 1.5 - (x8 + (-3)) - 81*(1 - x20) =l= 0 ;
c27_hi.. x1 + 3.5 - (x4 + (-1.5)) - 46*(1 - x21) =l= 0 ;
c28_hi.. x7 + 2.5 - (x10 + (-1.5)) - 81*(1 - x22) =l= 0 ;
c29_hi.. x4 + 1.5 - (x1 + (-3.5)) - 46*(1 - x23) =l= 0 ;
c30_hi.. x10 + 1.5 - (x7 + (-2.5)) - 81*(1 - x24) =l= 0 ;
c31_hi.. power((x2 + (-2.5) + (-15)), 2) + power((x8 + 3 + (-10)), 2) - 6814*(1 - x25) =l= 36 ;
c32_hi.. power((x2 + (-2.5) + (-15)), 2) + power((x8 + (-3) + (-10)), 2) - 5950*(1 - x25) =l= 36 ;
c33_hi.. power((x2 + 2.5 + (-15)), 2) + power((x8 + 3 + (-10)), 2) - 7189*(1 - x25) =l= 36 ;
c34_hi.. power((x2 + 2.5 + (-15)), 2) + power((x8 + (-3) + (-10)), 2) - 6325*(1 - x25) =l= 36 ;
c35_hi.. power((x2 + (-2.5) + (-50)), 2) + power((x8 + 3 + (-80)), 2) - 6556*(1 - x26) =l= 25 ;
c36_hi.. power((x2 + (-2.5) + (-50)), 2) + power((x8 + (-3) + (-80)), 2) - 7432*(1 - x26) =l= 25 ;
c37_hi.. power((x2 + 2.5 + (-50)), 2) + power((x8 + 3 + (-80)), 2) - 6171*(1 - x26) =l= 25 ;
c38_hi.. power((x2 + 2.5 + (-50)), 2) + power((x8 + (-3) + (-80)), 2) - 7047*(1 - x26) =l= 25 ;
c39_hi.. power((x2 + (-2.5) + (-30)), 2) + power((x8 + 3 + (-50)), 2) - 2025*(1 - x27) =l= 16 ;
c40_hi.. power((x2 + (-2.5) + (-30)), 2) + power((x8 + (-3) + (-50)), 2) - 2541*(1 - x27) =l= 16 ;
c41_hi.. power((x2 + 2.5 + (-30)), 2) + power((x8 + 3 + (-50)), 2) - 2209*(1 - x27) =l= 16 ;
c42_hi.. power((x2 + 2.5 + (-30)), 2) + power((x8 + (-3) + (-50)), 2) - 2725*(1 - x27) =l= 16 ;
c43_hi.. power((x1 + (-3.5) + (-15)), 2) + power((x7 + 2.5 + (-10)), 2) - 6678*(1 - x28) =l= 36 ;
c44_hi.. power((x1 + (-3.5) + (-15)), 2) + power((x7 + (-2.5) + (-10)), 2) - 5953*(1 - x28) =l= 36 ;
c45_hi.. power((x1 + 3.5 + (-15)), 2) + power((x7 + 2.5 + (-10)), 2) - 7189*(1 - x28) =l= 36 ;
c46_hi.. power((x1 + 3.5 + (-15)), 2) + power((x7 + (-2.5) + (-10)), 2) - 6464*(1 - x28) =l= 36 ;
c47_hi.. power((x1 + (-3.5) + (-50)), 2) + power((x7 + 2.5 + (-80)), 2) - 6697*(1 - x29) =l= 25 ;
c48_hi.. power((x1 + (-3.5) + (-50)), 2) + power((x7 + (-2.5) + (-80)), 2) - 7432*(1 - x29) =l= 25 ;
c49_hi.. power((x1 + 3.5 + (-50)), 2) + power((x7 + 2.5 + (-80)), 2) - 6172*(1 - x29) =l= 25 ;
c50_hi.. power((x1 + 3.5 + (-50)), 2) + power((x7 + (-2.5) + (-80)), 2) - 6907*(1 - x29) =l= 25 ;
c51_hi.. power((x1 + (-3.5) + (-30)), 2) + power((x7 + 2.5 + (-50)), 2) - 2106*(1 - x30) =l= 16 ;
c52_hi.. power((x1 + (-3.5) + (-30)), 2) + power((x7 + (-2.5) + (-50)), 2) - 2541*(1 - x30) =l= 16 ;
c53_hi.. power((x1 + 3.5 + (-30)), 2) + power((x7 + 2.5 + (-50)), 2) - 2290*(1 - x30) =l= 16 ;
c54_hi.. power((x1 + 3.5 + (-30)), 2) + power((x7 + (-2.5) + (-50)), 2) - 2725*(1 - x30) =l= 16 ;
c55_hi.. power((x4 + (-1.5) + (-15)), 2) + power((x10 + 1.5 + (-10)), 2) - 6958*(1 - x31) =l= 36 ;
c56_hi.. power((x4 + (-1.5) + (-15)), 2) + power((x10 + (-1.5) + (-10)), 2) - 6517*(1 - x31) =l= 36 ;
c57_hi.. power((x4 + 1.5 + (-15)), 2) + power((x10 + 1.5 + (-10)), 2) - 7189*(1 - x31) =l= 36 ;
c58_hi.. power((x4 + 1.5 + (-15)), 2) + power((x10 + (-1.5) + (-10)), 2) - 6748*(1 - x31) =l= 36 ;
c59_hi.. power((x4 + (-1.5) + (-50)), 2) + power((x10 + 1.5 + (-80)), 2) - 6985*(1 - x32) =l= 25 ;
c60_hi.. power((x4 + (-1.5) + (-50)), 2) + power((x10 + (-1.5) + (-80)), 2) - 7432*(1 - x32) =l= 25 ;
c61_hi.. power((x4 + 1.5 + (-50)), 2) + power((x10 + 1.5 + (-80)), 2) - 6748*(1 - x32) =l= 25 ;
c62_hi.. power((x4 + 1.5 + (-50)), 2) + power((x10 + (-1.5) + (-80)), 2) - 7195*(1 - x32) =l= 25 ;
c63_hi.. power((x4 + (-1.5) + (-30)), 2) + power((x10 + 1.5 + (-50)), 2) - 2317*(1 - x33) =l= 16 ;
c64_hi.. power((x4 + (-1.5) + (-30)), 2) + power((x10 + (-1.5) + (-50)), 2) - 2584*(1 - x33) =l= 16 ;
c65_hi.. power((x4 + 1.5 + (-30)), 2) + power((x10 + 1.5 + (-50)), 2) - 2458*(1 - x33) =l= 16 ;
c66_hi.. power((x4 + 1.5 + (-30)), 2) + power((x10 + (-1.5) + (-50)), 2) - 2725*(1 - x33) =l= 16 ;
c67.. GAMS_OBJECTIVE =e= 300*(power(x3, 2) + power(x9, 2)) ** 0.5 + 240*(power(x5, 2) + power(x11, 2)) ** 0.5 + 100*(power(x6, 2) + power(x12, 2)) ** 0.5 ;

x1.lo = 12.5;
x1.up = 51.5;
x2.lo = 11.5;
x2.up = 52.5;
x4.lo = 10.5;
x4.up = 53.5;
x7.lo = 6.5;
x7.up = 82.5;
x8.lo = 7;
x8.up = 82;
x10.lo = 5.5;
x10.up = 83.5;

MODEL GAMS_MODEL /all/ ;
option minlp=shot;
option solprint=off;
option limrow=0;
option limcol=0;
option solvelink=5;

* START USER ADDITIONAL OPTIONS

option reslim=120.0;
option threads=1;
option optcr=0.0001;
option optca=0.000001;
GAMS_MODEL.optfile=1;

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
put c13 ' ' c13.l ' ' c13.m /;
put c14 ' ' c14.l ' ' c14.m /;
put c15 ' ' c15.l ' ' c15.m /;
put c16 ' ' c16.l ' ' c16.m /;
put c17 ' ' c17.l ' ' c17.m /;
put c18 ' ' c18.l ' ' c18.m /;
put c19_hi ' ' c19_hi.l ' ' c19_hi.m /;
put c20_hi ' ' c20_hi.l ' ' c20_hi.m /;
put c21_hi ' ' c21_hi.l ' ' c21_hi.m /;
put c22_hi ' ' c22_hi.l ' ' c22_hi.m /;
put c23_hi ' ' c23_hi.l ' ' c23_hi.m /;
put c24_hi ' ' c24_hi.l ' ' c24_hi.m /;
put c25_hi ' ' c25_hi.l ' ' c25_hi.m /;
put c26_hi ' ' c26_hi.l ' ' c26_hi.m /;
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
put c61_hi ' ' c61_hi.l ' ' c61_hi.m /;
put c62_hi ' ' c62_hi.l ' ' c62_hi.m /;
put c63_hi ' ' c63_hi.l ' ' c63_hi.m /;
put c64_hi ' ' c64_hi.l ' ' c64_hi.m /;
put c65_hi ' ' c65_hi.l ' ' c65_hi.m /;
put c66_hi ' ' c66_hi.l ' ' c66_hi.m /;
put c67 ' ' c67.l ' ' c67.m /;
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
