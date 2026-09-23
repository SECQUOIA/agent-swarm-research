$offlisting
$offdigit

EQUATIONS
	c1_hi
	c2_hi
	c3_hi
	c4_hi
	c5_hi
	c6_hi
	c7_lo
	c8_lo
	c9_lo
	c10_lo
	c11_lo
	c12_lo
	c13_hi
	c14
	c15
	c16
	c17_lo
	c18_lo
	c19_lo
	c20
	c21
	c22
	c23_hi
	c24_lo
	c25_lo
	c26_hi
	c27_lo
	c28_hi
	c29_hi
	c30_lo
	c31_lo
	c32_hi
	c33_lo
	c34_hi
	c35_hi
	c36_lo
	c37_lo
	c38_hi
	c39_lo
	c40_hi
	c41
	c42
	c43
	c44
	c45
	c46
	c47
	c48
	c49
	c50_lo
	c51_hi
	c52_lo
	c53_hi
	c54_lo
	c55_hi
	c56_lo
	c57_hi
	c58_lo
	c59_hi
	c60_lo
	c61_hi
	c62_lo
	c63_hi
	c64_lo
	c65_hi
	c66_lo
	c67_hi
	c68_lo
	c69_hi
	c70_lo
	c71_hi
	c72_lo
	c73_hi
	c74_lo
	c75_hi
	c76_lo
	c77_hi
	c78_lo
	c79_hi
	c80_lo
	c81_hi
	c82_lo
	c83_hi
	c84_lo
	c85_hi
	c86;

BINARY VARIABLES
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
	x42
	x43
	x44
	x45
	x46
	x47
	x48
	x49;

POSITIVE VARIABLES
	x1
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
	x19;

VARIABLES
	GAMS_OBJECTIVE
	x2
	x3
	x4;


c1_hi.. 0.69314718055994529 + x1 - x2 =l= 0 ;
c2_hi.. 1.0986122886681098 + x1 - x3 =l= 0 ;
c3_hi.. 1.3862943611198906 + x1 - x4 =l= 0 ;
c4_hi.. 1.3862943611198906 + x5 - x2 =l= 0 ;
c5_hi.. 1.791759469228055 + x5 - x3 =l= 0 ;
c6_hi.. 1.0986122886681098 + x5 - x4 =l= 0 ;
c7_lo.. 2.0794415416798357 =l= x6 + x7 ;
c8_lo.. 2.9957322735539909 =l= x8 + x7 ;
c9_lo.. 1.3862943611198906 =l= x9 + x7 ;
c10_lo.. 2.3025850929940459 =l= x6 + x10 ;
c11_lo.. 2.4849066497880004 =l= x8 + x10 ;
c12_lo.. 1.0986122886681098 =l= x9 + x10 ;
c13_hi.. 200000*exp(x7 - x1) + 150000*exp(x10 - x5) =l= 6000 ;
c14.. x6 - (x11 + x12 + x13) =e= 0 ;
c15.. x8 - (x14 + x15 + x16) =e= 0 ;
c16.. x9 - (x17 + x18 + x19) =e= 0 ;
c17_lo.. 1 =l= x20 ;
c18_lo.. 1 =l= x21 ;
c19_lo.. 1 =l= x22 ;
c20.. x20 + x23 =e= 1 ;
c21.. x21 + x24 =e= 1 ;
c22.. x22 + x25 =e= 1 ;
c23_hi.. x26 + x27 + x28 - 3*(1 - x29 + 1 - x23) =l= 0 ;
c24_lo.. 2 =l= x26 + x27 + x28 - (-2)*(1 - x30 + 1 - x23) ;
c25_lo.. 1 =l= x26 + x27 + x28 + (1 - x20) ;
c26_hi.. x26 + x27 + x28 - 2*(1 - x20) =l= 1 ;
c27_lo.. 1 =l= x29 + x30 + (1 - x23) ;
c28_hi.. x29 + x30 - (1 - x23) =l= 1 ;
c29_hi.. x31 + x32 + x33 - 3*(1 - x34 + 1 - x24) =l= 0 ;
c30_lo.. 2 =l= x31 + x32 + x33 - (-2)*(1 - x35 + 1 - x24) ;
c31_lo.. 1 =l= x31 + x32 + x33 + (1 - x21) ;
c32_hi.. x31 + x32 + x33 - 2*(1 - x21) =l= 1 ;
c33_lo.. 1 =l= x34 + x35 + (1 - x24) ;
c34_hi.. x34 + x35 - (1 - x24) =l= 1 ;
c35_hi.. x36 + x37 + x38 - 3*(1 - x39 + 1 - x25) =l= 0 ;
c36_lo.. 2 =l= x36 + x37 + x38 - (-2)*(1 - x40 + 1 - x25) ;
c37_lo.. 1 =l= x36 + x37 + x38 + (1 - x22) ;
c38_hi.. x36 + x37 + x38 - 2*(1 - x22) =l= 1 ;
c39_lo.. 1 =l= x39 + x40 + (1 - x25) ;
c40_hi.. x39 + x40 - (1 - x25) =l= 1 ;
c41.. x36 + x41 =e= 1 ;
c42.. x26 + x42 =e= 1 ;
c43.. x31 + x43 =e= 1 ;
c44.. x37 + x44 =e= 1 ;
c45.. x27 + x45 =e= 1 ;
c46.. x32 + x46 =e= 1 ;
c47.. x38 + x47 =e= 1 ;
c48.. x28 + x48 =e= 1 ;
c49.. x33 + x49 =e= 1 ;
c50_lo.. 0 =l= x11 - 0*(1 - x26) ;
c51_hi.. x11 - 1.0986122886681098*(1 - x26) =l= 0 ;
c52_lo.. 0 =l= x11 - 0*(1 - x42) ;
c53_hi.. x11 - 1.0986122886681098*(1 - x42) =l= 0 ;
c54_lo.. 0 =l= x14 - 0*(1 - x31) ;
c55_hi.. x14 - 1.0986122886681098*(1 - x31) =l= 0 ;
c56_lo.. 0 =l= x14 - 0*(1 - x43) ;
c57_hi.. x14 - 1.0986122886681098*(1 - x43) =l= 0 ;
c58_lo.. 0 =l= x17 - 0*(1 - x36) ;
c59_hi.. x17 - 1.0986122886681098*(1 - x36) =l= 0 ;
c60_lo.. 0 =l= x17 - 0*(1 - x41) ;
c61_hi.. x17 - 1.0986122886681098*(1 - x41) =l= 0 ;
c62_lo.. 0.69314718055994529 =l= x12 - (-0.69314718055994529)*(1 - x27) ;
c63_hi.. x12 - 0.4054651081081645*(1 - x27) =l= 0.69314718055994529 ;
c64_lo.. 0 =l= x12 - 0*(1 - x45) ;
c65_hi.. x12 - 1.0986122886681098*(1 - x45) =l= 0 ;
c66_lo.. 0.69314718055994529 =l= x15 - (-0.69314718055994529)*(1 - x32) ;
c67_hi.. x15 - 0.4054651081081645*(1 - x32) =l= 0.69314718055994529 ;
c68_lo.. 0 =l= x15 - 0*(1 - x46) ;
c69_hi.. x15 - 1.0986122886681098*(1 - x46) =l= 0 ;
c70_lo.. 0.69314718055994529 =l= x18 - (-0.69314718055994529)*(1 - x37) ;
c71_hi.. x18 - 0.4054651081081645*(1 - x37) =l= 0.69314718055994529 ;
c72_lo.. 0 =l= x18 - 0*(1 - x44) ;
c73_hi.. x18 - 1.0986122886681098*(1 - x44) =l= 0 ;
c74_lo.. 1.0986122886681098 =l= x13 - (-1.0986122886681098)*(1 - x28) ;
c75_hi.. x13 - 0*(1 - x28) =l= 1.0986122886681098 ;
c76_lo.. 0 =l= x13 - 0*(1 - x48) ;
c77_hi.. x13 - 1.0986122886681098*(1 - x48) =l= 0 ;
c78_lo.. 1.0986122886681098 =l= x16 - (-1.0986122886681098)*(1 - x33) ;
c79_hi.. x16 - 0*(1 - x33) =l= 1.0986122886681098 ;
c80_lo.. 0 =l= x16 - 0*(1 - x49) ;
c81_hi.. x16 - 1.0986122886681098*(1 - x49) =l= 0 ;
c82_lo.. 1.0986122886681098 =l= x19 - (-1.0986122886681098)*(1 - x38) ;
c83_hi.. x19 - 0*(1 - x38) =l= 1.0986122886681098 ;
c84_lo.. 0 =l= x19 - 0*(1 - x47) ;
c85_hi.. x19 - 1.0986122886681098*(1 - x47) =l= 0 ;
c86.. GAMS_OBJECTIVE =e= 250*exp(x6 + 0.59999999999999998*x2) + 500*exp(x8 + 0.59999999999999998*x3) + 340*exp(x9 + 0.59999999999999998*x4) ;

x1.up = 6.437751649736401;
x5.up = 6.032286541628237;
x6.up = 1.0986122886681098;
x7.up = 2.9311937524164193;
x8.up = 1.0986122886681098;
x9.up = 1.0986122886681098;
x10.up = 2.8134107167600368;
x11.up = 1.0986122886681098;
x12.up = 1.0986122886681098;
x13.up = 1.0986122886681098;
x14.up = 1.0986122886681098;
x15.up = 1.0986122886681098;
x16.up = 1.0986122886681098;
x17.up = 1.0986122886681098;
x18.up = 1.0986122886681098;
x19.up = 1.0986122886681098;
x2.lo = 5.521460917862246;
x2.up = 7.8240460108562919;
x3.lo = 5.521460917862246;
x3.up = 7.8240460108562919;
x4.lo = 5.521460917862246;
x4.up = 7.8240460108562919;

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
put x43 ' ' x43.l ' ' x43.m /;
put x44 ' ' x44.l ' ' x44.m /;
put x45 ' ' x45.l ' ' x45.m /;
put x46 ' ' x46.l ' ' x46.m /;
put x47 ' ' x47.l ' ' x47.m /;
put x48 ' ' x48.l ' ' x48.m /;
put x49 ' ' x49.l ' ' x49.m /;
put c1_hi ' ' c1_hi.l ' ' c1_hi.m /;
put c2_hi ' ' c2_hi.l ' ' c2_hi.m /;
put c3_hi ' ' c3_hi.l ' ' c3_hi.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5_hi ' ' c5_hi.l ' ' c5_hi.m /;
put c6_hi ' ' c6_hi.l ' ' c6_hi.m /;
put c7_lo ' ' c7_lo.l ' ' c7_lo.m /;
put c8_lo ' ' c8_lo.l ' ' c8_lo.m /;
put c9_lo ' ' c9_lo.l ' ' c9_lo.m /;
put c10_lo ' ' c10_lo.l ' ' c10_lo.m /;
put c11_lo ' ' c11_lo.l ' ' c11_lo.m /;
put c12_lo ' ' c12_lo.l ' ' c12_lo.m /;
put c13_hi ' ' c13_hi.l ' ' c13_hi.m /;
put c14 ' ' c14.l ' ' c14.m /;
put c15 ' ' c15.l ' ' c15.m /;
put c16 ' ' c16.l ' ' c16.m /;
put c17_lo ' ' c17_lo.l ' ' c17_lo.m /;
put c18_lo ' ' c18_lo.l ' ' c18_lo.m /;
put c19_lo ' ' c19_lo.l ' ' c19_lo.m /;
put c20 ' ' c20.l ' ' c20.m /;
put c21 ' ' c21.l ' ' c21.m /;
put c22 ' ' c22.l ' ' c22.m /;
put c23_hi ' ' c23_hi.l ' ' c23_hi.m /;
put c24_lo ' ' c24_lo.l ' ' c24_lo.m /;
put c25_lo ' ' c25_lo.l ' ' c25_lo.m /;
put c26_hi ' ' c26_hi.l ' ' c26_hi.m /;
put c27_lo ' ' c27_lo.l ' ' c27_lo.m /;
put c28_hi ' ' c28_hi.l ' ' c28_hi.m /;
put c29_hi ' ' c29_hi.l ' ' c29_hi.m /;
put c30_lo ' ' c30_lo.l ' ' c30_lo.m /;
put c31_lo ' ' c31_lo.l ' ' c31_lo.m /;
put c32_hi ' ' c32_hi.l ' ' c32_hi.m /;
put c33_lo ' ' c33_lo.l ' ' c33_lo.m /;
put c34_hi ' ' c34_hi.l ' ' c34_hi.m /;
put c35_hi ' ' c35_hi.l ' ' c35_hi.m /;
put c36_lo ' ' c36_lo.l ' ' c36_lo.m /;
put c37_lo ' ' c37_lo.l ' ' c37_lo.m /;
put c38_hi ' ' c38_hi.l ' ' c38_hi.m /;
put c39_lo ' ' c39_lo.l ' ' c39_lo.m /;
put c40_hi ' ' c40_hi.l ' ' c40_hi.m /;
put c41 ' ' c41.l ' ' c41.m /;
put c42 ' ' c42.l ' ' c42.m /;
put c43 ' ' c43.l ' ' c43.m /;
put c44 ' ' c44.l ' ' c44.m /;
put c45 ' ' c45.l ' ' c45.m /;
put c46 ' ' c46.l ' ' c46.m /;
put c47 ' ' c47.l ' ' c47.m /;
put c48 ' ' c48.l ' ' c48.m /;
put c49 ' ' c49.l ' ' c49.m /;
put c50_lo ' ' c50_lo.l ' ' c50_lo.m /;
put c51_hi ' ' c51_hi.l ' ' c51_hi.m /;
put c52_lo ' ' c52_lo.l ' ' c52_lo.m /;
put c53_hi ' ' c53_hi.l ' ' c53_hi.m /;
put c54_lo ' ' c54_lo.l ' ' c54_lo.m /;
put c55_hi ' ' c55_hi.l ' ' c55_hi.m /;
put c56_lo ' ' c56_lo.l ' ' c56_lo.m /;
put c57_hi ' ' c57_hi.l ' ' c57_hi.m /;
put c58_lo ' ' c58_lo.l ' ' c58_lo.m /;
put c59_hi ' ' c59_hi.l ' ' c59_hi.m /;
put c60_lo ' ' c60_lo.l ' ' c60_lo.m /;
put c61_hi ' ' c61_hi.l ' ' c61_hi.m /;
put c62_lo ' ' c62_lo.l ' ' c62_lo.m /;
put c63_hi ' ' c63_hi.l ' ' c63_hi.m /;
put c64_lo ' ' c64_lo.l ' ' c64_lo.m /;
put c65_hi ' ' c65_hi.l ' ' c65_hi.m /;
put c66_lo ' ' c66_lo.l ' ' c66_lo.m /;
put c67_hi ' ' c67_hi.l ' ' c67_hi.m /;
put c68_lo ' ' c68_lo.l ' ' c68_lo.m /;
put c69_hi ' ' c69_hi.l ' ' c69_hi.m /;
put c70_lo ' ' c70_lo.l ' ' c70_lo.m /;
put c71_hi ' ' c71_hi.l ' ' c71_hi.m /;
put c72_lo ' ' c72_lo.l ' ' c72_lo.m /;
put c73_hi ' ' c73_hi.l ' ' c73_hi.m /;
put c74_lo ' ' c74_lo.l ' ' c74_lo.m /;
put c75_hi ' ' c75_hi.l ' ' c75_hi.m /;
put c76_lo ' ' c76_lo.l ' ' c76_lo.m /;
put c77_hi ' ' c77_hi.l ' ' c77_hi.m /;
put c78_lo ' ' c78_lo.l ' ' c78_lo.m /;
put c79_hi ' ' c79_hi.l ' ' c79_hi.m /;
put c80_lo ' ' c80_lo.l ' ' c80_lo.m /;
put c81_hi ' ' c81_hi.l ' ' c81_hi.m /;
put c82_lo ' ' c82_lo.l ' ' c82_lo.m /;
put c83_hi ' ' c83_hi.l ' ' c83_hi.m /;
put c84_lo ' ' c84_lo.l ' ' c84_lo.m /;
put c85_hi ' ' c85_hi.l ' ' c85_hi.m /;
put c86 ' ' c86.l ' ' c86.m /;
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
