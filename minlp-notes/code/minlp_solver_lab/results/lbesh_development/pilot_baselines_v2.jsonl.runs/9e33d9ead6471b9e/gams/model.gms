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
	c8_hi
	c9_hi
	c10_hi
	c11_hi
	c12_hi
	c13_hi
	c14_hi
	c15_hi
	c16_hi
	c17;

BINARY VARIABLES
	x8
	x9
	x10
	x11
	x12
	x13
	x14
	x15
	x16;

POSITIVE VARIABLES
	x7;

VARIABLES
	GAMS_OBJECTIVE
	x1
	x2
	x3
	x4
	x5
	x6;


c1_lo.. 0 =l= x1 + x2 + x3 ;
c2_lo.. 0.30000000000000004 =l= x4 + x5 + x6 ;
c3_hi.. power((x1 + (-0.5)*x5), 2) + power((x2 + (-0.5)*x6), 2) + power((x3 + (-0.5)*x4), 2) - x7 =l= 0 ;
c4_hi.. power((x1 - x2), 2) + power((x4 - x5), 2) + power((x2 - x3), 2) + power((x5 - x6), 2) + power((x3 - x1), 2) + power((x6 - x4), 2) =l= 1.6500000000000001 ;
c5.. x8 + x9 + x10 =e= 1 ;
c6.. x11 + x12 + x13 =e= 1 ;
c7.. x14 + x15 + x16 =e= 1 ;
c8_hi.. exp((-2.2413974379505786)*(x1 + 0.79548599408505949)) + exp(2.2413974379505786*(x1 + 0.79548599408505949)) + exp((-2.2610185217626659)*(x4 + 0.3500631893367298)) + exp(2.2610185217626659*(x4 + 0.3500631893367298)) - 780.8676671849463*(1 - x8) =l= 5.0374919729440855 ;
c9_hi.. exp((-1.828342266502224)*(x1 + (-0.21726773178804015))) + exp(1.828342266502224*(x1 + (-0.21726773178804015))) + exp((-1.709449556218052)*(x4 + (-0.6945521750474358))) + exp(1.709449556218052*(x4 + (-0.6945521750474358))) - 187.83457194154562*(1 - x9) =l= 5.241518653105727 ;
c10_hi.. exp((-2.2225480933387378)*(x1 + (-0.75649660550182429))) + exp(2.2225480933387378*(x1 + (-0.75649660550182429))) + exp((-2.1663007063013837)*(x4 + 0.3762358759076642)) + exp(2.1663007063013837*(x4 + 0.3762358759076642)) - 674.4392566732971*(1 - x10) =l= 4.953656966002545 ;
c11_hi.. exp((-1.9567298129489383)*(x2 + 0.676820809326646)) + exp(1.9567298129489383*(x2 + 0.676820809326646)) + exp((-1.8941792431172026)*(x5 + 0.38981394118895168)) + exp(1.8941792431172026*(x5 + 0.38981394118895168)) - 310.2775639274634*(1 - x11) =l= 4.869826123955877 ;
c12_hi.. exp((-1.9942886358149636)*(x2 + (-0.3184859638974657))) + exp(1.9942886358149636*(x2 + (-0.3184859638974657))) + exp((-1.7616045663576472)*(x5 + (-0.7178382449590601))) + exp(1.7616045663576472*(x5 + (-0.7178382449590601))) - 254.94059648282493*(1 - x12) =l= 5.1352627189871605 ;
c13_hi.. exp((-2.2150492536570394)*(x2 + (-0.85860396447360077))) + exp(2.2150492536570394*(x2 + (-0.85860396447360077))) + exp((-1.7693075496182604)*(x5 + 0.3866157238788881)) + exp(1.7693075496182604*(x5 + 0.3866157238788881)) - 655.06501693194946*(1 - x13) =l= 5.2991615452255667 ;
c14_hi.. exp((-1.8569992947855787)*(x3 + 0.68998816524527029)) + exp(1.8569992947855787*(x3 + 0.68998816524527029)) + exp((-1.9971920568474222)*(x6 + 0.33469587081365759)) + exp(1.9971920568474222*(x6 + 0.33469587081365759)) - 287.5978438672335*(1 - x14) =l= 5.2708263317594426 ;
c15_hi.. exp((-2.0411587596911058)*(x3 + (-0.22129126889933406))) + exp(2.0411587596911058*(x3 + (-0.22129126889933406))) + exp((-1.8433357530224233)*(x6 + (-0.7530323811484729))) + exp(1.8433357530224233*(x6 + (-0.7530323811484729))) - 295.836866128072*(1 - x15) =l= 4.925010968124564 ;
c16_hi.. exp((-1.7847896638219376)*(x3 + (-0.7838342426513255))) + exp(1.7847896638219376*(x3 + (-0.7838342426513255))) + exp((-2.134020166708317)*(x6 + 0.48549627827648939)) + exp(2.134020166708317*(x6 + 0.48549627827648939)) - 374.07660650081743*(1 - x16) =l= 4.995879103147696 ;
c17.. GAMS_OBJECTIVE =e= 1.075537807718994*x1 + 0.19763982998511553*x4 + 0.8235423418770354*x2 + 0.31018907460392697*x5 + 0.9861376130090131*x3 + 0.26553382734445485*x6 + 0.1*x7 + 0.044375208275198738*x8 + 0.02175070858398935*x9 + 0.021692129208850594*x10 + 0.07907240739740091*x11 + 0.04673213371643675*x12 + 0.054279054609292249*x13 + 0.06109969305650875*x14 + 0.065640124257064059*x15 + 0.032762148628116987*x16 ;

x8.l = 0;
x9.l = 1;
x10.l = 0;
x11.l = 0;
x12.l = 1;
x13.l = 0;
x14.l = 0;
x15.l = 1;
x16.l = 0;
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
put c1_lo ' ' c1_lo.l ' ' c1_lo.m /;
put c2_lo ' ' c2_lo.l ' ' c2_lo.m /;
put c3_hi ' ' c3_hi.l ' ' c3_hi.m /;
put c4_hi ' ' c4_hi.l ' ' c4_hi.m /;
put c5 ' ' c5.l ' ' c5.m /;
put c6 ' ' c6.l ' ' c6.m /;
put c7 ' ' c7.l ' ' c7.m /;
put c8_hi ' ' c8_hi.l ' ' c8_hi.m /;
put c9_hi ' ' c9_hi.l ' ' c9_hi.m /;
put c10_hi ' ' c10_hi.l ' ' c10_hi.m /;
put c11_hi ' ' c11_hi.l ' ' c11_hi.m /;
put c12_hi ' ' c12_hi.l ' ' c12_hi.m /;
put c13_hi ' ' c13_hi.l ' ' c13_hi.m /;
put c14_hi ' ' c14_hi.l ' ' c14_hi.m /;
put c15_hi ' ' c15_hi.l ' ' c15_hi.m /;
put c16_hi ' ' c16_hi.l ' ' c16_hi.m /;
put c17 ' ' c17.l ' ' c17.m /;
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
