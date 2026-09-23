$offlisting
$offdigit

EQUATIONS
	c1_hi
	c2_hi
	c3_lo
	c4_hi
	c5_lo
	c6
	c7
	c8
	c9
	c10
	c11
	c12
	c13
	c14
	c15
	c16
	c17
	c18
	c19
	c20
	c21
	c22
	c23
	c24
	c25
	c26
	c27
	c28
	c29
	c30
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
	c56;

BINARY VARIABLES
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
	x55;

POSITIVE VARIABLES
	x2
	x4
	x56;

VARIABLES
	GAMS_OBJECTIVE
	x1
	x3
	x5;


c1_hi.. x1 - x2 + x3 + x4 + x5 =l= 10 ;
c2_hi.. 0.59999999999999998*x1 + (-0.9)*x2 + (-0.5)*x3 + 0.1*x4 + x5 =l= -0.64 ;
c3_lo.. 0.6899999999999999 =l= x1 - x2 + x3 - x4 + x5 ;
c4_hi.. 0.157*x1 + 0.05*x2 =l= 1.5 ;
c5_lo.. 4.5 =l= 0.25*x2 + 1.05*x4 + (-0.29999999999999999)*x5 ;
c6.. x6 + x7 =e= 1 ;
c7.. x8 + x9 =e= 1 ;
c8.. x10 + x11 =e= 1 ;
c9.. x12 + x13 =e= 1 ;
c10.. x14 + x15 =e= 1 ;
c11.. x16 + x17 =e= 1 ;
c12.. x18 + x19 =e= 1 ;
c13.. x20 + x21 =e= 1 ;
c14.. x22 + x23 =e= 1 ;
c15.. x24 + x25 =e= 1 ;
c16.. x26 + x27 =e= 1 ;
c17.. x28 + x29 =e= 1 ;
c18.. x30 + x31 =e= 1 ;
c19.. x32 + x33 =e= 1 ;
c20.. x34 + x35 =e= 1 ;
c21.. x36 + x37 =e= 1 ;
c22.. x38 + x39 =e= 1 ;
c23.. x40 + x41 =e= 1 ;
c24.. x42 + x43 =e= 1 ;
c25.. x44 + x45 =e= 1 ;
c26.. x46 + x47 =e= 1 ;
c27.. x48 + x49 =e= 1 ;
c28.. x50 + x51 =e= 1 ;
c29.. x52 + x53 =e= 1 ;
c30.. x54 + x55 =e= 1 ;
c31_hi.. 9.57*power((x1 + (-2.2599999999999998)), 2) + 2.74*power((x2 + (-5.15)), 2) + 9.75*power((x3 + (-4.03)), 2) + 3.96*power((x4 + (-1.74)), 2) + 8.6699999999999999*power((x5 + (-4.74)), 2) + (-77.839848) - x56 - 565.64739700000007*(1 - x6) =l= 0 ;
c32_hi.. 8.38*power((x1 + (-5.5099999999999998)), 2) + 3.93*power((x2 + (-9.009999999999999)), 2) + 5.1799999999999997*power((x3 + (-3.8399999999999999)), 2) + 5.2*power((x4 + (-1.47)), 2) + 7.82*power((x5 + (-9.9199999999999999)), 2) + (-175.970966) - x56 - 723.08940100000007*(1 - x8) =l= 0 ;
c33_hi.. 9.81*power((x1 + (-4.0599999999999996)), 2) + 0.04*power((x2 + (-1.8)), 2) + 4.21*power((x3 + (-0.70999999999999996)), 2) + 7.3799999999999999*power((x4 + (-9.089999999999999)), 2) + 4.11*power((x5 + (-8.13)), 2) + (-201.82262100000008) - x56 - 810.5723929999999*(1 - x10) =l= 0 ;
c34_hi.. 7.41*power((x1 + (-6.2999999999999998)), 2) + 6.08*power((x2 + (-0.11)), 2) + 5.46*power((x3 + (-4.08)), 2) + 4.86*power((x4 + (-7.29)), 2) + 1.48*power((x5 + (-4.24)), 2) + (-143.95333100000002) - x56 - 811.1004549999999*(1 - x12) =l= 0 ;
c35_hi.. 9.96*power((x1 + (-2.81)), 2) + 9.13*power((x2 + (-1.6499999999999999)), 2) + 2.95*power((x3 + (-8.08)), 2) + 8.25*power((x4 + (-3.99)), 2) + 3.58*power((x5 + (-3.5099999999999998)), 2) + (-154.389533) - x56 - 600.461311*(1 - x14) =l= 0 ;
c36_hi.. 9.39*power((x1 + (-4.29)), 2) + 4.2699999999999996*power((x2 + (-9.49)), 2) + 5.0899999999999999*power((x3 + (-2.24)), 2) + 1.81*power((x4 + (-9.779999999999999)), 2) + 7.58*power((x5 + (-1.52)), 2) + (-433.31765300000006) - x56 - 951.2862930000001*(1 - x16) =l= 0 ;
c37_hi.. 1.8799999999999999*power((x1 + (-9.759999999999999)), 2) + 7.2*power((x2 + (-3.64)), 2) + 6.65*power((x3 + (-6.62)), 2) + 1.74*power((x4 + (-3.66)), 2) + 2.8599999999999999*power((x5 + (-9.08)), 2) + (-109.07635999999997) - x56 - 325.26075599999996*(1 - x18) =l= 0 ;
c38_hi.. 4.0099999999999998*power((x1 + (-1.37)), 2) + 2.6699999999999999*power((x2 + (-6.99)), 2) + 4.86*power((x3 + (-7.19)), 2) + 2.5499999999999998*power((x4 + (-3.0299999999999998)), 2) + 6.91*power((x5 + (-3.39)), 2) + (-41.595915999999995) - x56 - 538.79247199999986*(1 - x20) =l= 0 ;
c39_hi.. 4.1799999999999997*power((x1 + (-8.89)), 2) + 1.9199999999999999*power((x2 + (-8.289999999999999)), 2) + 2.6*power((x3 + (-6.0499999999999998)), 2) + 7.15*power((x4 + (-7.48)), 2) + 2.8599999999999999*power((x5 + (-4.0899999999999999)), 2) + (-144.06226600000005) - x56 - 710.44761*(1 - x22) =l= 0 ;
c40_hi.. 7.8099999999999996*power((x1 + (-7.4199999999999999)), 2) + 2.14*power((x2 + (-4.5999999999999996)), 2) + 9.63*power((x3 + (-0.29999999999999999)), 2) + 7.61*power((x4 + (-0.96999999999999997)), 2) + 9.1699999999999999*power((x5 + (-8.769999999999999)), 2) + (-99.83416399999998) - x56 - 1236.009962*(1 - x24) =l= 0 ;
c41_hi.. 8.96*power((x1 + (-1.54)), 2) + 3.47*power((x2 + (-7.0599999999999996)), 2) + 5.49*power((x3 + (-0.01)), 2) + 4.73*power((x4 + (-1.23)), 2) + 9.429999999999999*power((x5 + (-3.1099999999999999)), 2) + (-149.17912500000003) - x56 - 1060.873372*(1 - x26) =l= 0 ;
c42_hi.. 9.939999999999999*power((x1 + (-7.74)), 2) + 1.6299999999999999*power((x2 + (-4.4)), 2) + 1.23*power((x3 + (-7.9299999999999997)), 2) + 4.33*power((x4 + (-5.95)), 2) + 7.08*power((x5 + (-4.8799999999999999)), 2) + (-123.807402) - x56 - 604.034346*(1 - x28) =l= 0 ;
c43_hi.. 0.31*power((x1 + (-9.939999999999999)), 2) + 5*power((x2 + (-5.21)), 2) + 0.16*power((x3 + (-8.58)), 2) + 2.52*power((x4 + (-0.13)), 2) + 3.08*power((x5 + (-4.57)), 2) + (-27.221972) - x56 - 283.603948*(1 - x30) =l= 0 ;
c44_hi.. 6.0199999999999996*power((x1 + (-9.539999999999999)), 2) + 0.92*power((x2 + (-1.57)), 2) + 7.4699999999999998*power((x3 + (-9.66)), 2) + 9.74*power((x4 + (-5.24)), 2) + 1.76*power((x5 + (-7.9)), 2) + (-89.92682699999994) - x56 - 915.900069*(1 - x32) =l= 0 ;
c45_hi.. 5.0599999999999996*power((x1 + (-7.46)), 2) + 4.5199999999999996*power((x2 + (-8.81)), 2) + 1.8899999999999999*power((x3 + (-1.6699999999999999)), 2) + 1.22*power((x4 + (-6.4699999999999998)), 2) + 9.05*power((x5 + (-1.81)), 2) + (-293.07655700000004) - x56 - 968.2515350000001*(1 - x34) =l= 0 ;
c46_hi.. 5.9199999999999999*power((x1 + (-0.56)), 2) + 2.56*power((x2 + (-8.099999999999999)), 2) + 7.74*power((x3 + (-0.19)), 2) + 6.96*power((x4 + (-6.11)), 2) + 5.1799999999999997*power((x5 + (-6.4)), 2) + (-174.31702) - x56 - 1013.2571220000002*(1 - x36) =l= 0 ;
c47_hi.. 6.45*power((x1 + (-3.8599999999999999)), 2) + 1.52*power((x2 + (-6.6799999999999997)), 2) + 0.059999999999999998*power((x3 + (-6.4199999999999999)), 2) + 5.3399999999999999*power((x4 + (-7.29)), 2) + 8.47*power((x5 + (-4.66)), 2) + (-125.10278300000002) - x56 - 491.056095*(1 - x38) =l= 0 ;
c48_hi.. 1.04*power((x1 + (-2.98)), 2) + 1.36*power((x2 + (-2.98)), 2) + 5.99*power((x3 + (-3.0299999999999998)), 2) + 8.099999999999999*power((x4 + (-0.02)), 2) + 5.2199999999999998*power((x5 + (-0.67)), 2) + (-222.84169700000007) - x56 - 682.60115200000007*(1 - x40) =l= 0 ;
c49_hi.. 1.3999999999999999*power((x1 + (-3.6099999999999999)), 2) + 1.35*power((x2 + (-7.62)), 2) + 0.58999999999999997*power((x3 + (-1.79)), 2) + 8.58*power((x4 + (-7.7999999999999998)), 2) + 1.21*power((x5 + (-9.81)), 2) + (-50.485931) - x56 - 625.05264899999997*(1 - x42) =l= 0 ;
c50_hi.. 6.6799999999999997*power((x1 + (-5.6799999999999997)), 2) + 9.48*power((x2 + (-4.24)), 2) + 1.6*power((x3 + (-4.1699999999999999)), 2) + 6.74*power((x4 + (-6.75)), 2) + 8.9199999999999999*power((x5 + (-1.08)), 2) + (-361.19734399999999) - x56 - 953.84331399999996*(1 - x44) =l= 0 ;
c51_hi.. 1.95*power((x1 + (-5.48)), 2) + 0.46*power((x2 + (-3.74)), 2) + 2.8999999999999999*power((x3 + (-3.3399999999999999)), 2) + 1.79*power((x4 + (-6.2199999999999998)), 2) + 0.98999999999999999*power((x5 + (-7.94)), 2) + (-40.326419) - x56 - 169.160597*(1 - x46) =l= 0 ;
c52_hi.. 5.1799999999999997*power((x1 + (-8.13)), 2) + 5.0999999999999996*power((x2 + (-8.72)), 2) + 8.81*power((x3 + (-3.93)), 2) + 3.27*power((x4 + (-8.8)), 2) + 9.63*power((x5 + (-8.56)), 2) + (-161.85179900000009) - x56 - 1100.5237200000001*(1 - x48) =l= 0 ;
c53_hi.. 1.47*power((x1 + (-1.37)), 2) + 5.71*power((x2 + (-0.54)), 2) + 6.95*power((x3 + (-1.55)), 2) + 1.4199999999999999*power((x4 + (-5.5599999999999996)), 2) + 3.49*power((x5 + (-5.8499999999999996)), 2) + (-66.858266) - x56 - 755.060025*(1 - x50) =l= 0 ;
c54_hi.. 5.4*power((x1 + (-8.789999999999999)), 2) + 3.12*power((x2 + (-5.04)), 2) + 5.37*power((x3 + (-4.83)), 2) + 6.0999999999999996*power((x4 + (-6.94)), 2) + 3.71*power((x5 + (-0.38)), 2) + (-340.580732) - x56 - 718.1504769999998*(1 - x52) =l= 0 ;
c55_hi.. 6.32*power((x1 + (-2.66)), 2) + 0.81*power((x2 + (-4.19)), 2) + 6.12*power((x3 + (-6.49)), 2) + 6.73*power((x4 + (-8.039999999999999)), 2) + 7.9299999999999997*power((x5 + (-1.6599999999999999)), 2) + (-407.51996599999984) - x56 - 689.253555*(1 - x54) =l= 0 ;
c56.. GAMS_OBJECTIVE =e= 10*x56 - (x6 + 0.2*x8 + x10 + 0.2*x12 + 0.9*x14 + 0.9*x16 + 0.1*x18 + 0.8*x20 + x22 + 0.4*x24 + x26 + 0.29999999999999999*x28 + 0.1*x30 + 0.29999999999999999*x32 + 0.5*x34 + 0.9*x36 + 0.8*x38 + 0.1*x40 + 0.9*x42 + x44 + x46 + x48 + 0.2*x50 + 0.69999999999999996*x52 + 0.69999999999999996*x54) + 0.59999999999999998*power(x1, 2) + (-0.9)*x2 + (-0.5)*x3 + 0.1*power(x4, 2) + x5 ;

x2.up = 8;
x4.up = 5;
x56.up = 5000;
x1.lo = 2;
x1.up = 4.5;
x3.lo = 3;
x3.up = 9;
x5.lo = 4;
x5.up = 10;

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
put c3_lo ' ' c3_lo.l ' ' c3_lo.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5_lo ' ' c5_lo.l ' ' c5_lo.m /;
put c6 ' ' c6.l ' ' c6.m /;
put c7 ' ' c7.l ' ' c7.m /;
put c8 ' ' c8.l ' ' c8.m /;
put c9 ' ' c9.l ' ' c9.m /;
put c10 ' ' c10.l ' ' c10.m /;
put c11 ' ' c11.l ' ' c11.m /;
put c12 ' ' c12.l ' ' c12.m /;
put c13 ' ' c13.l ' ' c13.m /;
put c14 ' ' c14.l ' ' c14.m /;
put c15 ' ' c15.l ' ' c15.m /;
put c16 ' ' c16.l ' ' c16.m /;
put c17 ' ' c17.l ' ' c17.m /;
put c18 ' ' c18.l ' ' c18.m /;
put c19 ' ' c19.l ' ' c19.m /;
put c20 ' ' c20.l ' ' c20.m /;
put c21 ' ' c21.l ' ' c21.m /;
put c22 ' ' c22.l ' ' c22.m /;
put c23 ' ' c23.l ' ' c23.m /;
put c24 ' ' c24.l ' ' c24.m /;
put c25 ' ' c25.l ' ' c25.m /;
put c26 ' ' c26.l ' ' c26.m /;
put c27 ' ' c27.l ' ' c27.m /;
put c28 ' ' c28.l ' ' c28.m /;
put c29 ' ' c29.l ' ' c29.m /;
put c30 ' ' c30.l ' ' c30.m /;
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
put c56 ' ' c56.l ' ' c56.m /;
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
