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
	c15_hi
	c16_hi
	c17_hi
	c18_hi
	c19_hi
	c20_hi
	c21_hi
	c22_hi
	c23_hi
	c24_hi
	c25
	c26
	c27
	c28
	c29
	c30
	c31
	c32
	c33
	c34
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
	c67_hi
	c68_hi
	c69_hi
	c70_hi
	c71_hi
	c72_hi
	c73_hi
	c74_hi
	c75_hi
	c76_hi
	c77_hi
	c78_hi
	c79_hi
	c80_hi
	c81_hi
	c82_hi
	c83_hi
	c84_hi
	c85_hi
	c86_hi
	c87_hi
	c88_hi
	c89_hi
	c90_hi
	c91_hi
	c92_hi
	c93_hi
	c94_hi
	c95_hi
	c96_hi
	c97_hi
	c98_hi
	c99_hi
	c100_hi
	c101_hi
	c102_hi
	c103_hi
	c104_hi
	c105_hi
	c106_hi
	c107;

BINARY VARIABLES
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
	x42
	x43
	x44
	x45
	x46
	x47
	x48
	x49
	x50
	x51
	x52
	x53
	x54
	x55
	x56;

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
	x12
	x13
	x14
	x15
	x16
	x17
	x18
	x19
	x20;


c1_hi.. x1 - x2 - x3 =l= 0 ;
c2_hi.. x4 - x2 - x5 =l= 0 ;
c3_hi.. x6 - x2 - x7 =l= 0 ;
c4_hi.. x4 - x1 - x8 =l= 0 ;
c5_hi.. x6 - x1 - x9 =l= 0 ;
c6_hi.. x6 - x4 - x10 =l= 0 ;
c7_hi.. x2 - x1 - x3 =l= 0 ;
c8_hi.. x2 - x4 - x5 =l= 0 ;
c9_hi.. x2 - x6 - x7 =l= 0 ;
c10_hi.. x1 - x4 - x8 =l= 0 ;
c11_hi.. x1 - x6 - x9 =l= 0 ;
c12_hi.. x4 - x6 - x10 =l= 0 ;
c13_hi.. x11 - x12 - x13 =l= 0 ;
c14_hi.. x14 - x12 - x15 =l= 0 ;
c15_hi.. x16 - x12 - x17 =l= 0 ;
c16_hi.. x14 - x11 - x18 =l= 0 ;
c17_hi.. x16 - x11 - x19 =l= 0 ;
c18_hi.. x16 - x14 - x20 =l= 0 ;
c19_hi.. x12 - x11 - x13 =l= 0 ;
c20_hi.. x12 - x14 - x15 =l= 0 ;
c21_hi.. x12 - x16 - x17 =l= 0 ;
c22_hi.. x11 - x14 - x18 =l= 0 ;
c23_hi.. x11 - x16 - x19 =l= 0 ;
c24_hi.. x14 - x16 - x20 =l= 0 ;
c25.. x21 + x22 + x23 + x24 =e= 1 ;
c26.. x25 + x26 + x27 + x28 =e= 1 ;
c27.. x29 + x30 + x31 + x32 =e= 1 ;
c28.. x33 + x34 + x35 + x36 =e= 1 ;
c29.. x37 + x38 + x39 + x40 =e= 1 ;
c30.. x41 + x42 + x43 + x44 =e= 1 ;
c31.. x45 + x46 + x47 =e= 1 ;
c32.. x48 + x49 + x50 =e= 1 ;
c33.. x51 + x52 + x53 =e= 1 ;
c34.. x54 + x55 + x56 =e= 1 ;
c35_hi.. x2 + 2.5 - (x1 + (-3.5)) - 46*(1 - x21) =l= 0 ;
c36_hi.. x12 + 3 - (x11 + (-2.5)) - 81*(1 - x22) =l= 0 ;
c37_hi.. x1 + 3.5 - (x2 + (-2.5)) - 46*(1 - x23) =l= 0 ;
c38_hi.. x11 + 2.5 - (x12 + (-3)) - 81*(1 - x24) =l= 0 ;
c39_hi.. x2 + 2.5 - (x4 + (-1.5)) - 46*(1 - x25) =l= 0 ;
c40_hi.. x12 + 3 - (x14 + (-1.5)) - 81*(1 - x26) =l= 0 ;
c41_hi.. x4 + 1.5 - (x2 + (-2.5)) - 46*(1 - x27) =l= 0 ;
c42_hi.. x14 + 1.5 - (x12 + (-3)) - 81*(1 - x28) =l= 0 ;
c43_hi.. x2 + 2.5 - (x6 + (-1)) - 46*(1 - x29) =l= 0 ;
c44_hi.. x12 + 3 - (x16 + (-1.5)) - 81*(1 - x30) =l= 0 ;
c45_hi.. x6 + 1 - (x2 + (-2.5)) - 46*(1 - x31) =l= 0 ;
c46_hi.. x16 + 1.5 - (x12 + (-3)) - 81*(1 - x32) =l= 0 ;
c47_hi.. x1 + 3.5 - (x4 + (-1.5)) - 46*(1 - x33) =l= 0 ;
c48_hi.. x11 + 2.5 - (x14 + (-1.5)) - 81*(1 - x34) =l= 0 ;
c49_hi.. x4 + 1.5 - (x1 + (-3.5)) - 46*(1 - x35) =l= 0 ;
c50_hi.. x14 + 1.5 - (x11 + (-2.5)) - 81*(1 - x36) =l= 0 ;
c51_hi.. x1 + 3.5 - (x6 + (-1)) - 46*(1 - x37) =l= 0 ;
c52_hi.. x11 + 2.5 - (x16 + (-1.5)) - 81*(1 - x38) =l= 0 ;
c53_hi.. x6 + 1 - (x1 + (-3.5)) - 46*(1 - x39) =l= 0 ;
c54_hi.. x16 + 1.5 - (x11 + (-2.5)) - 81*(1 - x40) =l= 0 ;
c55_hi.. x4 + 1.5 - (x6 + (-1)) - 46*(1 - x41) =l= 0 ;
c56_hi.. x14 + 1.5 - (x16 + (-1.5)) - 81*(1 - x42) =l= 0 ;
c57_hi.. x6 + 1 - (x4 + (-1.5)) - 46*(1 - x43) =l= 0 ;
c58_hi.. x16 + 1.5 - (x14 + (-1.5)) - 81*(1 - x44) =l= 0 ;
c59_hi.. power((x2 + (-2.5) + (-15)), 2) + power((x12 + 3 + (-10)), 2) - 6814*(1 - x45) =l= 36 ;
c60_hi.. power((x2 + (-2.5) + (-15)), 2) + power((x12 + (-3) + (-10)), 2) - 5950*(1 - x45) =l= 36 ;
c61_hi.. power((x2 + 2.5 + (-15)), 2) + power((x12 + 3 + (-10)), 2) - 7189*(1 - x45) =l= 36 ;
c62_hi.. power((x2 + 2.5 + (-15)), 2) + power((x12 + (-3) + (-10)), 2) - 6325*(1 - x45) =l= 36 ;
c63_hi.. power((x2 + (-2.5) + (-50)), 2) + power((x12 + 3 + (-80)), 2) - 6556*(1 - x46) =l= 25 ;
c64_hi.. power((x2 + (-2.5) + (-50)), 2) + power((x12 + (-3) + (-80)), 2) - 7432*(1 - x46) =l= 25 ;
c65_hi.. power((x2 + 2.5 + (-50)), 2) + power((x12 + 3 + (-80)), 2) - 6171*(1 - x46) =l= 25 ;
c66_hi.. power((x2 + 2.5 + (-50)), 2) + power((x12 + (-3) + (-80)), 2) - 7047*(1 - x46) =l= 25 ;
c67_hi.. power((x2 + (-2.5) + (-30)), 2) + power((x12 + 3 + (-50)), 2) - 2025*(1 - x47) =l= 16 ;
c68_hi.. power((x2 + (-2.5) + (-30)), 2) + power((x12 + (-3) + (-50)), 2) - 2541*(1 - x47) =l= 16 ;
c69_hi.. power((x2 + 2.5 + (-30)), 2) + power((x12 + 3 + (-50)), 2) - 2209*(1 - x47) =l= 16 ;
c70_hi.. power((x2 + 2.5 + (-30)), 2) + power((x12 + (-3) + (-50)), 2) - 2725*(1 - x47) =l= 16 ;
c71_hi.. power((x1 + (-3.5) + (-15)), 2) + power((x11 + 2.5 + (-10)), 2) - 6678*(1 - x48) =l= 36 ;
c72_hi.. power((x1 + (-3.5) + (-15)), 2) + power((x11 + (-2.5) + (-10)), 2) - 5953*(1 - x48) =l= 36 ;
c73_hi.. power((x1 + 3.5 + (-15)), 2) + power((x11 + 2.5 + (-10)), 2) - 7189*(1 - x48) =l= 36 ;
c74_hi.. power((x1 + 3.5 + (-15)), 2) + power((x11 + (-2.5) + (-10)), 2) - 6464*(1 - x48) =l= 36 ;
c75_hi.. power((x1 + (-3.5) + (-50)), 2) + power((x11 + 2.5 + (-80)), 2) - 6697*(1 - x49) =l= 25 ;
c76_hi.. power((x1 + (-3.5) + (-50)), 2) + power((x11 + (-2.5) + (-80)), 2) - 7432*(1 - x49) =l= 25 ;
c77_hi.. power((x1 + 3.5 + (-50)), 2) + power((x11 + 2.5 + (-80)), 2) - 6172*(1 - x49) =l= 25 ;
c78_hi.. power((x1 + 3.5 + (-50)), 2) + power((x11 + (-2.5) + (-80)), 2) - 6907*(1 - x49) =l= 25 ;
c79_hi.. power((x1 + (-3.5) + (-30)), 2) + power((x11 + 2.5 + (-50)), 2) - 2106*(1 - x50) =l= 16 ;
c80_hi.. power((x1 + (-3.5) + (-30)), 2) + power((x11 + (-2.5) + (-50)), 2) - 2541*(1 - x50) =l= 16 ;
c81_hi.. power((x1 + 3.5 + (-30)), 2) + power((x11 + 2.5 + (-50)), 2) - 2290*(1 - x50) =l= 16 ;
c82_hi.. power((x1 + 3.5 + (-30)), 2) + power((x11 + (-2.5) + (-50)), 2) - 2725*(1 - x50) =l= 16 ;
c83_hi.. power((x4 + (-1.5) + (-15)), 2) + power((x14 + 1.5 + (-10)), 2) - 6958*(1 - x51) =l= 36 ;
c84_hi.. power((x4 + (-1.5) + (-15)), 2) + power((x14 + (-1.5) + (-10)), 2) - 6517*(1 - x51) =l= 36 ;
c85_hi.. power((x4 + 1.5 + (-15)), 2) + power((x14 + 1.5 + (-10)), 2) - 7189*(1 - x51) =l= 36 ;
c86_hi.. power((x4 + 1.5 + (-15)), 2) + power((x14 + (-1.5) + (-10)), 2) - 6748*(1 - x51) =l= 36 ;
c87_hi.. power((x4 + (-1.5) + (-50)), 2) + power((x14 + 1.5 + (-80)), 2) - 6985*(1 - x52) =l= 25 ;
c88_hi.. power((x4 + (-1.5) + (-50)), 2) + power((x14 + (-1.5) + (-80)), 2) - 7432*(1 - x52) =l= 25 ;
c89_hi.. power((x4 + 1.5 + (-50)), 2) + power((x14 + 1.5 + (-80)), 2) - 6748*(1 - x52) =l= 25 ;
c90_hi.. power((x4 + 1.5 + (-50)), 2) + power((x14 + (-1.5) + (-80)), 2) - 7195*(1 - x52) =l= 25 ;
c91_hi.. power((x4 + (-1.5) + (-30)), 2) + power((x14 + 1.5 + (-50)), 2) - 2317*(1 - x53) =l= 16 ;
c92_hi.. power((x4 + (-1.5) + (-30)), 2) + power((x14 + (-1.5) + (-50)), 2) - 2584*(1 - x53) =l= 16 ;
c93_hi.. power((x4 + 1.5 + (-30)), 2) + power((x14 + 1.5 + (-50)), 2) - 2458*(1 - x53) =l= 16 ;
c94_hi.. power((x4 + 1.5 + (-30)), 2) + power((x14 + (-1.5) + (-50)), 2) - 2725*(1 - x53) =l= 16 ;
c95_hi.. power((x6 + (-1) + (-15)), 2) + power((x16 + 1.5 + (-10)), 2) - 7033*(1 - x54) =l= 36 ;
c96_hi.. power((x6 + (-1) + (-15)), 2) + power((x16 + (-1.5) + (-10)), 2) - 6592*(1 - x54) =l= 36 ;
c97_hi.. power((x6 + 1 + (-15)), 2) + power((x16 + 1.5 + (-10)), 2) - 7189*(1 - x54) =l= 36 ;
c98_hi.. power((x6 + 1 + (-15)), 2) + power((x16 + (-1.5) + (-10)), 2) - 6748*(1 - x54) =l= 36 ;
c99_hi.. power((x6 + (-1) + (-50)), 2) + power((x16 + 1.5 + (-80)), 2) - 6985*(1 - x55) =l= 25 ;
c100_hi.. power((x6 + (-1) + (-50)), 2) + power((x16 + (-1.5) + (-80)), 2) - 7432*(1 - x55) =l= 25 ;
c101_hi.. power((x6 + 1 + (-50)), 2) + power((x16 + 1.5 + (-80)), 2) - 6825*(1 - x55) =l= 25 ;
c102_hi.. power((x6 + 1 + (-50)), 2) + power((x16 + (-1.5) + (-80)), 2) - 7272*(1 - x55) =l= 25 ;
c103_hi.. power((x6 + (-1) + (-30)), 2) + power((x16 + 1.5 + (-50)), 2) - 2362*(1 - x56) =l= 16 ;
c104_hi.. power((x6 + (-1) + (-30)), 2) + power((x16 + (-1.5) + (-50)), 2) - 2629*(1 - x56) =l= 16 ;
c105_hi.. power((x6 + 1 + (-30)), 2) + power((x16 + 1.5 + (-50)), 2) - 2458*(1 - x56) =l= 16 ;
c106_hi.. power((x6 + 1 + (-30)), 2) + power((x16 + (-1.5) + (-50)), 2) - 2725*(1 - x56) =l= 16 ;
c107.. GAMS_OBJECTIVE =e= 300*(power(x3, 2) + power(x13, 2)) ** 0.5 + 240*(power(x5, 2) + power(x15, 2)) ** 0.5 + 210*(power(x7, 2) + power(x17, 2)) ** 0.5 + 100*(power(x8, 2) + power(x18, 2)) ** 0.5 + 150*(power(x9, 2) + power(x19, 2)) ** 0.5 + 120*(power(x10, 2) + power(x20, 2)) ** 0.5 ;

x1.lo = 12.5;
x1.up = 51.5;
x2.lo = 11.5;
x2.up = 52.5;
x4.lo = 10.5;
x4.up = 53.5;
x6.lo = 10;
x6.up = 54;
x11.lo = 6.5;
x11.up = 82.5;
x12.lo = 7;
x12.up = 82;
x14.lo = 5.5;
x14.up = 83.5;
x16.lo = 5.5;
x16.up = 83.5;

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
put x34 ' ' x34.l ' ' x34.m /;
put x35 ' ' x35.l ' ' x35.m /;
put x36 ' ' x36.l ' ' x36.m /;
put x37 ' ' x37.l ' ' x37.m /;
put x38 ' ' x38.l ' ' x38.m /;
put x39 ' ' x39.l ' ' x39.m /;
put x40 ' ' x40.l ' ' x40.m /;
put x41 ' ' x41.l ' ' x41.m /;
put x42 ' ' x42.l ' ' x42.m /;
put x43 ' ' x43.l ' ' x43.m /;
put x44 ' ' x44.l ' ' x44.m /;
put x45 ' ' x45.l ' ' x45.m /;
put x46 ' ' x46.l ' ' x46.m /;
put x47 ' ' x47.l ' ' x47.m /;
put x48 ' ' x48.l ' ' x48.m /;
put x49 ' ' x49.l ' ' x49.m /;
put x50 ' ' x50.l ' ' x50.m /;
put x51 ' ' x51.l ' ' x51.m /;
put x52 ' ' x52.l ' ' x52.m /;
put x53 ' ' x53.l ' ' x53.m /;
put x54 ' ' x54.l ' ' x54.m /;
put x55 ' ' x55.l ' ' x55.m /;
put x56 ' ' x56.l ' ' x56.m /;
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
put c15_hi ' ' c15_hi.l ' ' c15_hi.m /;
put c16_hi ' ' c16_hi.l ' ' c16_hi.m /;
put c17_hi ' ' c17_hi.l ' ' c17_hi.m /;
put c18_hi ' ' c18_hi.l ' ' c18_hi.m /;
put c19_hi ' ' c19_hi.l ' ' c19_hi.m /;
put c20_hi ' ' c20_hi.l ' ' c20_hi.m /;
put c21_hi ' ' c21_hi.l ' ' c21_hi.m /;
put c22_hi ' ' c22_hi.l ' ' c22_hi.m /;
put c23_hi ' ' c23_hi.l ' ' c23_hi.m /;
put c24_hi ' ' c24_hi.l ' ' c24_hi.m /;
put c25 ' ' c25.l ' ' c25.m /;
put c26 ' ' c26.l ' ' c26.m /;
put c27 ' ' c27.l ' ' c27.m /;
put c28 ' ' c28.l ' ' c28.m /;
put c29 ' ' c29.l ' ' c29.m /;
put c30 ' ' c30.l ' ' c30.m /;
put c31 ' ' c31.l ' ' c31.m /;
put c32 ' ' c32.l ' ' c32.m /;
put c33 ' ' c33.l ' ' c33.m /;
put c34 ' ' c34.l ' ' c34.m /;
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
put c67_hi ' ' c67_hi.l ' ' c67_hi.m /;
put c68_hi ' ' c68_hi.l ' ' c68_hi.m /;
put c69_hi ' ' c69_hi.l ' ' c69_hi.m /;
put c70_hi ' ' c70_hi.l ' ' c70_hi.m /;
put c71_hi ' ' c71_hi.l ' ' c71_hi.m /;
put c72_hi ' ' c72_hi.l ' ' c72_hi.m /;
put c73_hi ' ' c73_hi.l ' ' c73_hi.m /;
put c74_hi ' ' c74_hi.l ' ' c74_hi.m /;
put c75_hi ' ' c75_hi.l ' ' c75_hi.m /;
put c76_hi ' ' c76_hi.l ' ' c76_hi.m /;
put c77_hi ' ' c77_hi.l ' ' c77_hi.m /;
put c78_hi ' ' c78_hi.l ' ' c78_hi.m /;
put c79_hi ' ' c79_hi.l ' ' c79_hi.m /;
put c80_hi ' ' c80_hi.l ' ' c80_hi.m /;
put c81_hi ' ' c81_hi.l ' ' c81_hi.m /;
put c82_hi ' ' c82_hi.l ' ' c82_hi.m /;
put c83_hi ' ' c83_hi.l ' ' c83_hi.m /;
put c84_hi ' ' c84_hi.l ' ' c84_hi.m /;
put c85_hi ' ' c85_hi.l ' ' c85_hi.m /;
put c86_hi ' ' c86_hi.l ' ' c86_hi.m /;
put c87_hi ' ' c87_hi.l ' ' c87_hi.m /;
put c88_hi ' ' c88_hi.l ' ' c88_hi.m /;
put c89_hi ' ' c89_hi.l ' ' c89_hi.m /;
put c90_hi ' ' c90_hi.l ' ' c90_hi.m /;
put c91_hi ' ' c91_hi.l ' ' c91_hi.m /;
put c92_hi ' ' c92_hi.l ' ' c92_hi.m /;
put c93_hi ' ' c93_hi.l ' ' c93_hi.m /;
put c94_hi ' ' c94_hi.l ' ' c94_hi.m /;
put c95_hi ' ' c95_hi.l ' ' c95_hi.m /;
put c96_hi ' ' c96_hi.l ' ' c96_hi.m /;
put c97_hi ' ' c97_hi.l ' ' c97_hi.m /;
put c98_hi ' ' c98_hi.l ' ' c98_hi.m /;
put c99_hi ' ' c99_hi.l ' ' c99_hi.m /;
put c100_hi ' ' c100_hi.l ' ' c100_hi.m /;
put c101_hi ' ' c101_hi.l ' ' c101_hi.m /;
put c102_hi ' ' c102_hi.l ' ' c102_hi.m /;
put c103_hi ' ' c103_hi.l ' ' c103_hi.m /;
put c104_hi ' ' c104_hi.l ' ' c104_hi.m /;
put c105_hi ' ' c105_hi.l ' ' c105_hi.m /;
put c106_hi ' ' c106_hi.l ' ' c106_hi.m /;
put c107 ' ' c107.l ' ' c107.m /;
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
