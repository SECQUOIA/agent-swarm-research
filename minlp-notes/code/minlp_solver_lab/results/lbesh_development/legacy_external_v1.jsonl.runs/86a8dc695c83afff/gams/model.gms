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
	c21_lo
	c21_hi
	c22_lo
	c22_hi
	c23_lo
	c23_hi
	c24_lo
	c24_hi
	c25_lo
	c25_hi
	c26_lo
	c26_hi
	c27_lo
	c27_hi
	c28_lo
	c28_hi
	c29_lo
	c29_hi
	c30_lo
	c30_hi
	c31_lo
	c31_hi
	c32_lo
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
	c45
	c46
	c47
	c48
	c49
	c50
	c51
	c52
	c53
	c54
	c55
	c56
	c57
	c58
	c59
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
	c107_hi
	c108_hi
	c109_hi
	c110_hi
	c111_hi
	c112_hi
	c113_hi
	c114_hi
	c115_hi
	c116_hi
	c117_hi
	c118_hi
	c119_hi
	c120;

BINARY VARIABLES
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
	x56
	x57
	x58
	x59
	x60
	x61
	x62
	x63
	x64
	x65
	x66
	x67
	x68
	x69
	x70
	x71
	x72
	x73
	x74
	x75
	x76
	x77
	x78
	x79
	x80
	x81
	x82
	x83
	x84
	x85
	x86;

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
	x18
	x19
	x20
	x21
	x22
	x23
	x24
	x25
	x26;

VARIABLES
	GAMS_OBJECTIVE
	;


c1_hi.. x1 + x2 - x3 =l= 0 ;
c2_hi.. x4 + x5 - x3 =l= 0 ;
c3_hi.. x6 + x7 - x3 =l= 0 ;
c4_hi.. x8 + x9 - x3 =l= 0 ;
c5_hi.. x10 + x11 - x3 =l= 0 ;
c6_hi.. x12 + x13 - x3 =l= 0 ;
c7_hi.. x14 + x15 - x16 =l= 0 ;
c8_hi.. x17 + x18 - x16 =l= 0 ;
c9_hi.. x19 + x20 - x16 =l= 0 ;
c10_hi.. x21 + x22 - x16 =l= 0 ;
c11_hi.. x23 + x24 - x16 =l= 0 ;
c12_hi.. x25 + x26 - x16 =l= 0 ;
c13_hi.. 40/x15 - x2 =l= 0 ;
c14_hi.. 50/x18 - x5 =l= 0 ;
c15_hi.. 60/x20 - x7 =l= 0 ;
c16_hi.. 35/x22 - x9 =l= 0 ;
c17_hi.. 75/x24 - x11 =l= 0 ;
c18_hi.. 20/x26 - x13 =l= 0 ;
c19_hi.. x3 =l= 30 ;
c20_hi.. x16 =l= 30 ;
c21_lo.. 1 =l= x2 ;
c21_hi.. x2 =l= 40 ;
c22_lo.. 1 =l= x5 ;
c22_hi.. x5 =l= 50 ;
c23_lo.. 1 =l= x7 ;
c23_hi.. x7 =l= 60 ;
c24_lo.. 1 =l= x9 ;
c24_hi.. x9 =l= 35 ;
c25_lo.. 1 =l= x11 ;
c25_hi.. x11 =l= 75 ;
c26_lo.. 1 =l= x13 ;
c26_hi.. x13 =l= 20 ;
c27_lo.. 1 =l= x15 ;
c27_hi.. x15 =l= 40 ;
c28_lo.. 1 =l= x18 ;
c28_hi.. x18 =l= 50 ;
c29_lo.. 1 =l= x20 ;
c29_hi.. x20 =l= 60 ;
c30_lo.. 1 =l= x22 ;
c30_hi.. x22 =l= 35 ;
c31_lo.. 1 =l= x24 ;
c31_hi.. x24 =l= 75 ;
c32_lo.. 1 =l= x26 ;
c32_hi.. x26 =l= 20 ;
c33_hi.. x1 =l= 29 ;
c34_hi.. x4 =l= 29 ;
c35_hi.. x6 =l= 29 ;
c36_hi.. x8 =l= 29 ;
c37_hi.. x10 =l= 29 ;
c38_hi.. x12 =l= 29 ;
c39_hi.. x14 =l= 29 ;
c40_hi.. x17 =l= 29 ;
c41_hi.. x19 =l= 29 ;
c42_hi.. x21 =l= 29 ;
c43_hi.. x23 =l= 29 ;
c44_hi.. x25 =l= 29 ;
c45.. x27 + x28 + x29 + x30 =e= 1 ;
c46.. x31 + x32 + x33 + x34 =e= 1 ;
c47.. x35 + x36 + x37 + x38 =e= 1 ;
c48.. x39 + x40 + x41 + x42 =e= 1 ;
c49.. x43 + x44 + x45 + x46 =e= 1 ;
c50.. x47 + x48 + x49 + x50 =e= 1 ;
c51.. x51 + x52 + x53 + x54 =e= 1 ;
c52.. x55 + x56 + x57 + x58 =e= 1 ;
c53.. x59 + x60 + x61 + x62 =e= 1 ;
c54.. x63 + x64 + x65 + x66 =e= 1 ;
c55.. x67 + x68 + x69 + x70 =e= 1 ;
c56.. x71 + x72 + x73 + x74 =e= 1 ;
c57.. x75 + x76 + x77 + x78 =e= 1 ;
c58.. x79 + x80 + x81 + x82 =e= 1 ;
c59.. x83 + x84 + x85 + x86 =e= 1 ;
c60_hi.. x1 + x2 - x4 - 60*(1 - x27) =l= 0 ;
c61_hi.. x14 + x15 - x17 - 60*(1 - x28) =l= 0 ;
c62_hi.. x4 + x5 - x1 - 60*(1 - x29) =l= 0 ;
c63_hi.. x17 + x18 - x14 - 60*(1 - x30) =l= 0 ;
c64_hi.. x1 + x2 - x6 - 60*(1 - x31) =l= 0 ;
c65_hi.. x14 + x15 - x19 - 60*(1 - x32) =l= 0 ;
c66_hi.. x6 + x7 - x1 - 60*(1 - x33) =l= 0 ;
c67_hi.. x19 + x20 - x14 - 60*(1 - x34) =l= 0 ;
c68_hi.. x1 + x2 - x8 - 60*(1 - x35) =l= 0 ;
c69_hi.. x14 + x15 - x21 - 60*(1 - x36) =l= 0 ;
c70_hi.. x8 + x9 - x1 - 60*(1 - x37) =l= 0 ;
c71_hi.. x21 + x22 - x14 - 60*(1 - x38) =l= 0 ;
c72_hi.. x1 + x2 - x10 - 60*(1 - x39) =l= 0 ;
c73_hi.. x14 + x15 - x23 - 60*(1 - x40) =l= 0 ;
c74_hi.. x10 + x11 - x1 - 60*(1 - x41) =l= 0 ;
c75_hi.. x23 + x24 - x14 - 60*(1 - x42) =l= 0 ;
c76_hi.. x1 + x2 - x12 - 60*(1 - x43) =l= 0 ;
c77_hi.. x14 + x15 - x25 - 60*(1 - x44) =l= 0 ;
c78_hi.. x12 + x13 - x1 - 60*(1 - x45) =l= 0 ;
c79_hi.. x25 + x26 - x14 - 60*(1 - x46) =l= 0 ;
c80_hi.. x4 + x5 - x6 - 60*(1 - x47) =l= 0 ;
c81_hi.. x17 + x18 - x19 - 60*(1 - x48) =l= 0 ;
c82_hi.. x6 + x7 - x4 - 60*(1 - x49) =l= 0 ;
c83_hi.. x19 + x20 - x17 - 60*(1 - x50) =l= 0 ;
c84_hi.. x4 + x5 - x8 - 60*(1 - x51) =l= 0 ;
c85_hi.. x17 + x18 - x21 - 60*(1 - x52) =l= 0 ;
c86_hi.. x8 + x9 - x4 - 60*(1 - x53) =l= 0 ;
c87_hi.. x21 + x22 - x17 - 60*(1 - x54) =l= 0 ;
c88_hi.. x4 + x5 - x10 - 60*(1 - x55) =l= 0 ;
c89_hi.. x17 + x18 - x23 - 60*(1 - x56) =l= 0 ;
c90_hi.. x10 + x11 - x4 - 60*(1 - x57) =l= 0 ;
c91_hi.. x23 + x24 - x17 - 60*(1 - x58) =l= 0 ;
c92_hi.. x4 + x5 - x12 - 60*(1 - x59) =l= 0 ;
c93_hi.. x17 + x18 - x25 - 60*(1 - x60) =l= 0 ;
c94_hi.. x12 + x13 - x4 - 60*(1 - x61) =l= 0 ;
c95_hi.. x25 + x26 - x17 - 60*(1 - x62) =l= 0 ;
c96_hi.. x6 + x7 - x8 - 60*(1 - x63) =l= 0 ;
c97_hi.. x19 + x20 - x21 - 60*(1 - x64) =l= 0 ;
c98_hi.. x8 + x9 - x6 - 60*(1 - x65) =l= 0 ;
c99_hi.. x21 + x22 - x19 - 60*(1 - x66) =l= 0 ;
c100_hi.. x6 + x7 - x10 - 60*(1 - x67) =l= 0 ;
c101_hi.. x19 + x20 - x23 - 60*(1 - x68) =l= 0 ;
c102_hi.. x10 + x11 - x6 - 60*(1 - x69) =l= 0 ;
c103_hi.. x23 + x24 - x19 - 60*(1 - x70) =l= 0 ;
c104_hi.. x6 + x7 - x12 - 60*(1 - x71) =l= 0 ;
c105_hi.. x19 + x20 - x25 - 60*(1 - x72) =l= 0 ;
c106_hi.. x12 + x13 - x6 - 60*(1 - x73) =l= 0 ;
c107_hi.. x25 + x26 - x19 - 60*(1 - x74) =l= 0 ;
c108_hi.. x8 + x9 - x10 - 60*(1 - x75) =l= 0 ;
c109_hi.. x21 + x22 - x23 - 60*(1 - x76) =l= 0 ;
c110_hi.. x10 + x11 - x8 - 60*(1 - x77) =l= 0 ;
c111_hi.. x23 + x24 - x21 - 60*(1 - x78) =l= 0 ;
c112_hi.. x8 + x9 - x12 - 60*(1 - x79) =l= 0 ;
c113_hi.. x21 + x22 - x25 - 60*(1 - x80) =l= 0 ;
c114_hi.. x12 + x13 - x8 - 60*(1 - x81) =l= 0 ;
c115_hi.. x25 + x26 - x21 - 60*(1 - x82) =l= 0 ;
c116_hi.. x10 + x11 - x12 - 60*(1 - x83) =l= 0 ;
c117_hi.. x23 + x24 - x25 - 60*(1 - x84) =l= 0 ;
c118_hi.. x12 + x13 - x10 - 60*(1 - x85) =l= 0 ;
c119_hi.. x25 + x26 - x23 - 60*(1 - x86) =l= 0 ;
c120.. GAMS_OBJECTIVE =e= 2*(x3 + x16) ;

x1.up = 30;
x2.up = 30;
x4.up = 30;
x5.up = 30;
x6.up = 30;
x7.up = 30;
x8.up = 30;
x9.up = 30;
x10.up = 30;
x11.up = 30;
x12.up = 30;
x13.up = 30;
x14.up = 30;
x15.up = 30;
x17.up = 30;
x18.up = 30;
x19.up = 30;
x20.up = 30;
x21.up = 30;
x22.up = 30;
x23.up = 30;
x24.up = 30;
x25.up = 30;
x26.up = 30;

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
put x57 ' ' x57.l ' ' x57.m /;
put x58 ' ' x58.l ' ' x58.m /;
put x59 ' ' x59.l ' ' x59.m /;
put x60 ' ' x60.l ' ' x60.m /;
put x61 ' ' x61.l ' ' x61.m /;
put x62 ' ' x62.l ' ' x62.m /;
put x63 ' ' x63.l ' ' x63.m /;
put x64 ' ' x64.l ' ' x64.m /;
put x65 ' ' x65.l ' ' x65.m /;
put x66 ' ' x66.l ' ' x66.m /;
put x67 ' ' x67.l ' ' x67.m /;
put x68 ' ' x68.l ' ' x68.m /;
put x69 ' ' x69.l ' ' x69.m /;
put x70 ' ' x70.l ' ' x70.m /;
put x71 ' ' x71.l ' ' x71.m /;
put x72 ' ' x72.l ' ' x72.m /;
put x73 ' ' x73.l ' ' x73.m /;
put x74 ' ' x74.l ' ' x74.m /;
put x75 ' ' x75.l ' ' x75.m /;
put x76 ' ' x76.l ' ' x76.m /;
put x77 ' ' x77.l ' ' x77.m /;
put x78 ' ' x78.l ' ' x78.m /;
put x79 ' ' x79.l ' ' x79.m /;
put x80 ' ' x80.l ' ' x80.m /;
put x81 ' ' x81.l ' ' x81.m /;
put x82 ' ' x82.l ' ' x82.m /;
put x83 ' ' x83.l ' ' x83.m /;
put x84 ' ' x84.l ' ' x84.m /;
put x85 ' ' x85.l ' ' x85.m /;
put x86 ' ' x86.l ' ' x86.m /;
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
put c21_lo ' ' c21_lo.l ' ' c21_lo.m /;
put c21_hi ' ' c21_hi.l ' ' c21_hi.m /;
put c22_lo ' ' c22_lo.l ' ' c22_lo.m /;
put c22_hi ' ' c22_hi.l ' ' c22_hi.m /;
put c23_lo ' ' c23_lo.l ' ' c23_lo.m /;
put c23_hi ' ' c23_hi.l ' ' c23_hi.m /;
put c24_lo ' ' c24_lo.l ' ' c24_lo.m /;
put c24_hi ' ' c24_hi.l ' ' c24_hi.m /;
put c25_lo ' ' c25_lo.l ' ' c25_lo.m /;
put c25_hi ' ' c25_hi.l ' ' c25_hi.m /;
put c26_lo ' ' c26_lo.l ' ' c26_lo.m /;
put c26_hi ' ' c26_hi.l ' ' c26_hi.m /;
put c27_lo ' ' c27_lo.l ' ' c27_lo.m /;
put c27_hi ' ' c27_hi.l ' ' c27_hi.m /;
put c28_lo ' ' c28_lo.l ' ' c28_lo.m /;
put c28_hi ' ' c28_hi.l ' ' c28_hi.m /;
put c29_lo ' ' c29_lo.l ' ' c29_lo.m /;
put c29_hi ' ' c29_hi.l ' ' c29_hi.m /;
put c30_lo ' ' c30_lo.l ' ' c30_lo.m /;
put c30_hi ' ' c30_hi.l ' ' c30_hi.m /;
put c31_lo ' ' c31_lo.l ' ' c31_lo.m /;
put c31_hi ' ' c31_hi.l ' ' c31_hi.m /;
put c32_lo ' ' c32_lo.l ' ' c32_lo.m /;
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
put c45 ' ' c45.l ' ' c45.m /;
put c46 ' ' c46.l ' ' c46.m /;
put c47 ' ' c47.l ' ' c47.m /;
put c48 ' ' c48.l ' ' c48.m /;
put c49 ' ' c49.l ' ' c49.m /;
put c50 ' ' c50.l ' ' c50.m /;
put c51 ' ' c51.l ' ' c51.m /;
put c52 ' ' c52.l ' ' c52.m /;
put c53 ' ' c53.l ' ' c53.m /;
put c54 ' ' c54.l ' ' c54.m /;
put c55 ' ' c55.l ' ' c55.m /;
put c56 ' ' c56.l ' ' c56.m /;
put c57 ' ' c57.l ' ' c57.m /;
put c58 ' ' c58.l ' ' c58.m /;
put c59 ' ' c59.l ' ' c59.m /;
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
put c107_hi ' ' c107_hi.l ' ' c107_hi.m /;
put c108_hi ' ' c108_hi.l ' ' c108_hi.m /;
put c109_hi ' ' c109_hi.l ' ' c109_hi.m /;
put c110_hi ' ' c110_hi.l ' ' c110_hi.m /;
put c111_hi ' ' c111_hi.l ' ' c111_hi.m /;
put c112_hi ' ' c112_hi.l ' ' c112_hi.m /;
put c113_hi ' ' c113_hi.l ' ' c113_hi.m /;
put c114_hi ' ' c114_hi.l ' ' c114_hi.m /;
put c115_hi ' ' c115_hi.l ' ' c115_hi.m /;
put c116_hi ' ' c116_hi.l ' ' c116_hi.m /;
put c117_hi ' ' c117_hi.l ' ' c117_hi.m /;
put c118_hi ' ' c118_hi.l ' ' c118_hi.m /;
put c119_hi ' ' c119_hi.l ' ' c119_hi.m /;
put c120 ' ' c120.l ' ' c120.m /;
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
