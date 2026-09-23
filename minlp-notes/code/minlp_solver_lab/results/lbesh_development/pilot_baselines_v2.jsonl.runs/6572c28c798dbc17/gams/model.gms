$offlisting
$offdigit

EQUATIONS
	c1_lo
	c2_lo
	c3_hi
	c4_hi
	c5
	c6
	c7
	c8
	c9
	c10
	c11
	c12
	c13
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
	c59;

BINARY VARIABLES
	x26
	x27
	x28
	x29
	x30
	x31
	x32
	x33
	x34;

POSITIVE VARIABLES
	x7;

VARIABLES
	GAMS_OBJECTIVE
	x1
	x2
	x3
	x4
	x5
	x6
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
	x25;


c1_lo.. 0 =l= x1 + x2 + x3 ;
c2_lo.. 0.30000000000000004 =l= x4 + x5 + x6 ;
c3_hi.. power((x1 + (-0.5)*x5), 2) + power((x2 + (-0.5)*x6), 2) + power((x3 + (-0.5)*x4), 2) - x7 =l= 0 ;
c4_hi.. power((x1 - x2), 2) + power((x4 - x5), 2) + power((x2 - x3), 2) + power((x5 - x6), 2) + power((x3 - x1), 2) + power((x6 - x4), 2) =l= 1.6500000000000001 ;
c5.. x1 - (x8 + x9 + x10) =e= 0 ;
c6.. x4 - (x11 + x12 + x13) =e= 0 ;
c7.. x2 - (x14 + x15 + x16) =e= 0 ;
c8.. x5 - (x17 + x18 + x19) =e= 0 ;
c9.. x3 - (x20 + x21 + x22) =e= 0 ;
c10.. x6 - (x23 + x24 + x25) =e= 0 ;
c11.. x26 + x27 + x28 =e= 1 ;
c12.. x29 + x30 + x31 =e= 1 ;
c13.. x32 + x33 + x34 =e= 1 ;
c14_hi.. (0.9999*x26 + 0.0001)*(exp((-2.2413974379505786)*(x8/(0.9999*x26 + 0.0001) + 0.79548599408505949)) + exp(2.2413974379505786*(x8/(0.9999*x26 + 0.0001) + 0.79548599408505949)) + exp((-2.2610185217626659)*(x11/(0.9999*x26 + 0.0001) + 0.3500631893367298)) + exp(2.2610185217626659*(x11/(0.9999*x26 + 0.0001) + 0.3500631893367298))) - 0.000877567465305259*(1 - x26) + (-5.0374919729440855)*x26 =l= 0 ;
c15_hi.. (-2)*x26 - x8 =l= 0 ;
c16_hi.. x8 + (-2)*x26 =l= 0 ;
c17_hi.. (-2)*x26 - x11 =l= 0 ;
c18_hi.. x11 + (-2)*x26 =l= 0 ;
c19_hi.. (0.9999*x27 + 0.0001)*(exp((-1.828342266502224)*(x9/(0.9999*x27 + 0.0001) + (-0.21726773178804015))) + exp(1.828342266502224*(x9/(0.9999*x27 + 0.0001) + (-0.21726773178804015))) + exp((-1.709449556218052)*(x12/(0.9999*x27 + 0.0001) + (-0.6945521750474358))) + exp(1.709449556218052*(x12/(0.9999*x27 + 0.0001) + (-0.6945521750474358)))) - 0.0005743152942596822*(1 - x27) + (-5.241518653105727)*x27 =l= 0 ;
c20_hi.. (-2)*x27 - x9 =l= 0 ;
c21_hi.. x9 + (-2)*x27 =l= 0 ;
c22_hi.. (-2)*x27 - x12 =l= 0 ;
c23_hi.. x12 + (-2)*x27 =l= 0 ;
c24_hi.. (0.9999*x28 + 0.0001)*(exp((-2.2225480933387378)*(x10/(0.9999*x28 + 0.0001) + (-0.75649660550182429))) + exp(2.2225480933387378*(x10/(0.9999*x28 + 0.0001) + (-0.75649660550182429))) + exp((-2.1663007063013837)*(x13/(0.9999*x28 + 0.0001) + 0.3762358759076642)) + exp(2.1663007063013837*(x13/(0.9999*x28 + 0.0001) + 0.3762358759076642))) - 0.000826081510425313*(1 - x28) + (-4.953656966002545)*x28 =l= 0 ;
c25_hi.. (-2)*x28 - x10 =l= 0 ;
c26_hi.. x10 + (-2)*x28 =l= 0 ;
c27_hi.. (-2)*x28 - x13 =l= 0 ;
c28_hi.. x13 + (-2)*x28 =l= 0 ;
c29_hi.. (0.9999*x29 + 0.0001)*(exp((-1.9567298129489383)*(x14/(0.9999*x29 + 0.0001) + 0.676820809326646)) + exp(1.9567298129489383*(x14/(0.9999*x29 + 0.0001) + 0.676820809326646)) + exp((-1.8941792431172026)*(x17/(0.9999*x29 + 0.0001) + 0.38981394118895168)) + exp(1.8941792431172026*(x17/(0.9999*x29 + 0.0001) + 0.38981394118895168))) - 0.0006596161816023457*(1 - x29) + (-4.869826123955877)*x29 =l= 0 ;
c30_hi.. (-2)*x29 - x14 =l= 0 ;
c31_hi.. x14 + (-2)*x29 =l= 0 ;
c32_hi.. (-2)*x29 - x17 =l= 0 ;
c33_hi.. x17 + (-2)*x29 =l= 0 ;
c34_hi.. (0.9999*x30 + 0.0001)*(exp((-1.9942886358149636)*(x15/(0.9999*x30 + 0.0001) + (-0.3184859638974657))) + exp(1.9942886358149636*(x15/(0.9999*x30 + 0.0001) + (-0.3184859638974657))) + exp((-1.7616045663576472)*(x18/(0.9999*x30 + 0.0001) + (-0.7178382449590601))) + exp(1.7616045663576472*(x18/(0.9999*x30 + 0.0001) + (-0.7178382449590601)))) - 0.00062410208913057637*(1 - x30) + (-5.1352627189871605)*x30 =l= 0 ;
c35_hi.. (-2)*x30 - x15 =l= 0 ;
c36_hi.. x15 + (-2)*x30 =l= 0 ;
c37_hi.. (-2)*x30 - x18 =l= 0 ;
c38_hi.. x18 + (-2)*x30 =l= 0 ;
c39_hi.. (0.9999*x31 + 0.0001)*(exp((-2.2150492536570394)*(x16/(0.9999*x31 + 0.0001) + (-0.85860396447360077))) + exp(2.2150492536570394*(x16/(0.9999*x31 + 0.0001) + (-0.85860396447360077))) + exp((-1.7693075496182604)*(x19/(0.9999*x31 + 0.0001) + 0.3866157238788881)) + exp(1.7693075496182604*(x19/(0.9999*x31 + 0.0001) + 0.3866157238788881))) - 0.0009334013278776068*(1 - x31) + (-5.2991615452255667)*x31 =l= 0 ;
c40_hi.. (-2)*x31 - x16 =l= 0 ;
c41_hi.. x16 + (-2)*x31 =l= 0 ;
c42_hi.. (-2)*x31 - x19 =l= 0 ;
c43_hi.. x19 + (-2)*x31 =l= 0 ;
c44_hi.. (0.9999*x32 + 0.0001)*(exp((-1.8569992947855787)*(x20/(0.9999*x32 + 0.0001) + 0.68998816524527029)) + exp(1.8569992947855787*(x20/(0.9999*x32 + 0.0001) + 0.68998816524527029)) + exp((-1.9971920568474222)*(x23/(0.9999*x32 + 0.0001) + 0.33469587081365759)) + exp(1.9971920568474222*(x23/(0.9999*x32 + 0.0001) + 0.33469587081365759))) - 0.0006342735256065191*(1 - x32) + (-5.2708263317594426)*x32 =l= 0 ;
c45_hi.. (-2)*x32 - x20 =l= 0 ;
c46_hi.. x20 + (-2)*x32 =l= 0 ;
c47_hi.. (-2)*x32 - x23 =l= 0 ;
c48_hi.. x23 + (-2)*x32 =l= 0 ;
c49_hi.. (0.9999*x33 + 0.0001)*(exp((-2.0411587596911058)*(x21/(0.9999*x33 + 0.0001) + (-0.22129126889933406))) + exp(2.0411587596911058*(x21/(0.9999*x33 + 0.0001) + (-0.22129126889933406))) + exp((-1.8433357530224233)*(x24/(0.9999*x33 + 0.0001) + (-0.7530323811484729))) + exp(1.8433357530224233*(x24/(0.9999*x33 + 0.0001) + (-0.7530323811484729)))) - 0.0006464263096119238*(1 - x33) + (-4.925010968124564)*x33 =l= 0 ;
c50_hi.. (-2)*x33 - x21 =l= 0 ;
c51_hi.. x21 + (-2)*x33 =l= 0 ;
c52_hi.. (-2)*x33 - x24 =l= 0 ;
c53_hi.. x24 + (-2)*x33 =l= 0 ;
c54_hi.. (0.9999*x34 + 0.0001)*(exp((-1.7847896638219376)*(x22/(0.9999*x34 + 0.0001) + (-0.7838342426513255))) + exp(1.7847896638219376*(x22/(0.9999*x34 + 0.0001) + (-0.7838342426513255))) + exp((-2.134020166708317)*(x25/(0.9999*x34 + 0.0001) + 0.48549627827648939)) + exp(2.134020166708317*(x25/(0.9999*x34 + 0.0001) + 0.48549627827648939))) - 0.0007470850591407722*(1 - x34) + (-4.995879103147696)*x34 =l= 0 ;
c55_hi.. (-2)*x34 - x22 =l= 0 ;
c56_hi.. x22 + (-2)*x34 =l= 0 ;
c57_hi.. (-2)*x34 - x25 =l= 0 ;
c58_hi.. x25 + (-2)*x34 =l= 0 ;
c59.. GAMS_OBJECTIVE =e= 1.075537807718994*x1 + 0.19763982998511553*x4 + 0.8235423418770354*x2 + 0.31018907460392697*x5 + 0.9861376130090131*x3 + 0.26553382734445485*x6 + 0.1*x7 + 0.044375208275198738*x26 + 0.02175070858398935*x27 + 0.021692129208850594*x28 + 0.07907240739740091*x29 + 0.04673213371643675*x30 + 0.054279054609292249*x31 + 0.06109969305650875*x32 + 0.065640124257064059*x33 + 0.032762148628116987*x34 ;

x26.l = 0;
x27.l = 1;
x28.l = 0;
x29.l = 0;
x30.l = 1;
x31.l = 0;
x32.l = 0;
x33.l = 1;
x34.l = 0;
x7.up = 27;
x7.l = 0.039304798216809406;
x1.lo = -2;
x1.up = 2;
x1.l = 0.21726773178804015;
x2.lo = -2;
x2.up = 2;
x2.l = 0.3184859638974657;
x3.lo = -2;
x3.up = 2;
x3.l = 0.22129126889933406;
x4.lo = -2;
x4.up = 2;
x4.l = 0.6945521750474358;
x5.lo = -2;
x5.up = 2;
x5.l = 0.7178382449590601;
x6.lo = -2;
x6.up = 2;
x6.l = 0.7530323811484729;
x8.lo = -2;
x8.up = 2;
x8.l = 0;
x9.lo = -2;
x9.up = 2;
x9.l = 0.21726773178804015;
x10.lo = -2;
x10.up = 2;
x10.l = 0;
x11.lo = -2;
x11.up = 2;
x11.l = 0;
x12.lo = -2;
x12.up = 2;
x12.l = 0.6945521750474358;
x13.lo = -2;
x13.up = 2;
x13.l = 0;
x14.lo = -2;
x14.up = 2;
x14.l = 0;
x15.lo = -2;
x15.up = 2;
x15.l = 0.3184859638974657;
x16.lo = -2;
x16.up = 2;
x16.l = 0;
x17.lo = -2;
x17.up = 2;
x17.l = 0;
x18.lo = -2;
x18.up = 2;
x18.l = 0.7178382449590601;
x19.lo = -2;
x19.up = 2;
x19.l = 0;
x20.lo = -2;
x20.up = 2;
x20.l = 0;
x21.lo = -2;
x21.up = 2;
x21.l = 0.22129126889933406;
x22.lo = -2;
x22.up = 2;
x22.l = 0;
x23.lo = -2;
x23.up = 2;
x23.l = 0;
x24.lo = -2;
x24.up = 2;
x24.l = 0.7530323811484729;
x25.lo = -2;
x25.up = 2;
x25.l = 0;

MODEL GAMS_MODEL /all/ ;
option minlp=shot;
option solprint=off;
option limrow=0;
option limcol=0;
option solvelink=5;

* START USER ADDITIONAL OPTIONS

option reslim=30.0;
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
put c1_lo ' ' c1_lo.l ' ' c1_lo.m /;
put c2_lo ' ' c2_lo.l ' ' c2_lo.m /;
put c3_hi ' ' c3_hi.l ' ' c3_hi.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5 ' ' c5.l ' ' c5.m /;
put c6 ' ' c6.l ' ' c6.m /;
put c7 ' ' c7.l ' ' c7.m /;
put c8 ' ' c8.l ' ' c8.m /;
put c9 ' ' c9.l ' ' c9.m /;
put c10 ' ' c10.l ' ' c10.m /;
put c11 ' ' c11.l ' ' c11.m /;
put c12 ' ' c12.l ' ' c12.m /;
put c13 ' ' c13.l ' ' c13.m /;
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
put c59 ' ' c59.l ' ' c59.m /;
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
