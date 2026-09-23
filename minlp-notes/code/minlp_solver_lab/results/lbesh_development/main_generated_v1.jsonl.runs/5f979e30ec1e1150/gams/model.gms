$offlisting
$offdigit

EQUATIONS
	c1_hi
	c2_hi
	c3_hi
	c4_lo
	c5_lo
	c6_hi
	c7_hi
	c8
	c9
	c10
	c11_hi
	c12_lo
	c13_hi
	c14_hi
	c15_hi
	c16_hi
	c17_hi
	c18_hi
	c19_lo
	c20_hi
	c21_hi
	c22_hi
	c23_hi
	c24_hi
	c25_hi
	c26_lo
	c27_hi
	c28_hi
	c29_hi
	c30_hi
	c31_hi
	c32;

BINARY VARIABLES
	x7
	x8
	x9
	x10
	x11
	x12
	x13
	x14
	x15;

POSITIVE VARIABLES
	x1
	x2
	x3
	x4
	x5
	x6
	x16
	x17
	x18;

VARIABLES
	GAMS_OBJECTIVE
	;


c1_hi.. x1 + x2 =l= 1.1504944249150699 ;
c2_hi.. x3 + x4 =l= 1.102655677156728 ;
c3_hi.. x5 + x6 =l= 1.065846319248452 ;
c4_lo.. 0.9293189979696701 =l= x1 + x3 + x5 ;
c5_lo.. 0.7301792126904549 =l= x2 + x4 + x6 ;
c6_hi.. 1.1648979443774312*x1 + 0.965807612944795*x2 + 1.2336012709489526*x3 + 0.8015931858243239*x4 + 1.2759249398782329*x5 + 0.78802832480143148*x6 =l= 1.9014459297525228 ;
c7_hi.. power(((x1 + 0.34999999999999998*x4)/1.1504944249150699), 2) + power(((x3 + 0.34999999999999998*x6)/1.102655677156728), 2) + power(((x5 + 0.34999999999999998*x2)/1.065846319248452), 2) =l= 0.4132578869830678 ;
c8.. x7 + x8 + x9 =e= 1 ;
c9.. x10 + x11 + x12 =e= 1 ;
c10.. x13 + x14 + x15 =e= 1 ;
c11_hi.. x1 + x2 - 2.3009888498301398*(1 - x7) =l= 0 ;
c12_lo.. 0 =l= x16 - 0*(1 - x7) ;
c13_hi.. x16 - 34.821853836838628*(1 - x7) =l= 0 ;
c14_hi.. x1 + x2 - 1.5839865526231847*(1 - x8) =l= 0.71700229720695519 ;
c15_hi.. 1.3856497539343533*(0.9448334929578201*(1/(1 + (-0.7901741107159372)*x1) + (-1)) + 1.1634620832804603*(1/(1 + (-0.7901741107159372)*x2) + (-1)) + 0.28507044043622753*(1/(1 - (x1 + x2)/2.531087734813154) + (-1))) - x16 - 33.163670320798694*(1 - x8) =l= 0 ;
c16_hi.. x1 + x2 - 1.1504944249150699*(1 - x9) =l= 1.1504944249150699 ;
c17_hi.. 0.91053271528156987*(0.9448334929578201*(1/(1 + (-0.7901741107159372)*x1) + (-1)) + 1.1634620832804603*(1/(1 + (-0.7901741107159372)*x2) + (-1)) + 0.28507044043622753*(1/(1 - (x1 + x2)/2.531087734813154) + (-1))) - x16 - 21.792380578252708*(1 - x9) =l= 0 ;
c18_hi.. x3 + x4 - 2.2053113543134559*(1 - x10) =l= 0 ;
c19_lo.. 0 =l= x17 - 0*(1 - x10) ;
c20_hi.. x17 - 35.548822806639*(1 - x10) =l= 0 ;
c21_hi.. x3 + x4 - 1.4904545255427979*(1 - x11) =l= 0.714856828770658 ;
c22_hi.. 1.3425106944861094*(1.2231682689724346*(1/(1 + (-0.82445583687109036)*x3) + (-1)) + 0.95576458123951069*(1/(1 + (-0.82445583687109036)*x4) + (-1)) + 0.34291087585000246*(1/(1 - (x3 + x4)/2.4258424897448019) + (-1))) - x17 - 33.856021720608574*(1 - x11) =l= 0 ;
c23_hi.. x3 + x4 - 1.102655677156728*(1 - x12) =l= 1.102655677156728 ;
c24_hi.. 0.913656602615721*(1.2231682689724346*(1/(1 + (-0.82445583687109036)*x3) + (-1)) + 0.95576458123951069*(1/(1 + (-0.82445583687109036)*x4) + (-1)) + 0.34291087585000246*(1/(1 - (x3 + x4)/2.4258424897448019) + (-1))) - x17 - 23.040991710815263*(1 - x12) =l= 0 ;
c25_hi.. x5 + x6 - 2.1316926384969039*(1 - x13) =l= 0 ;
c26_lo.. 0 =l= x18 - 0*(1 - x13) ;
c27_hi.. x18 - 28.90599083212131*(1 - x13) =l= 0 ;
c28_hi.. x5 + x6 - 1.474746996366238*(1 - x14) =l= 0.6569456421306657 ;
c29_hi.. 1.1465672745883366*(1.2299898989239963*(1/(1 + (-0.85292869400902549)*x5) + (-1)) + 0.9310103231526927*(1/(1 + (-0.85292869400902549)*x6) + (-1)) + 0.24003770115332956*(1/(1 - (x5 + x6)/2.3448619023465946) + (-1))) - x18 - 27.52951507821077*(1 - x14) =l= 0 ;
c30_hi.. x5 + x6 - 1.065846319248452*(1 - x15) =l= 1.065846319248452 ;
c31_hi.. 0.8712311498277498*(1.2299898989239963*(1/(1 + (-0.85292869400902549)*x5) + (-1)) + 0.9310103231526927*(1/(1 + (-0.85292869400902549)*x6) + (-1)) + 0.24003770115332956*(1/(1 - (x5 + x6)/2.3448619023465946) + (-1))) - x18 - 20.918590306357178*(1 - x15) =l= 0 ;
c32.. GAMS_OBJECTIVE =e= 0 + 0.11256162751516206*x8 + 0.29669392325824323*x9 + x16 + 0 + 0.09895140951105335*x11 + 0.37116815328954827*x12 + x17 + 0 + 0.11782007325890141*x14 + 0.3705888695637115*x15 + x18 ;

x7.l = 0;
x8.l = 1;
x9.l = 0;
x10.l = 0;
x11.l = 1;
x12.l = 0;
x13.l = 0;
x14.l = 1;
x15.l = 0;
x1.up = 1.1504944249150699;
x1.l = 0.32213843897621963;
x2.up = 1.1504944249150699;
x2.l = 0.25310877348131539;
x3.up = 1.102655677156728;
x3.l = 0.30874358960388387;
x4.up = 1.102655677156728;
x4.l = 0.24258424897448017;
x5.up = 1.065846319248452;
x5.l = 0.2984369693895666;
x6.up = 1.065846319248452;
x6.l = 0.23448619023465944;
x16.up = 34.821853836838628;
x16.l = 0.9662632334058648;
x17.up = 35.548822806639;
x17.l = 1.0169041906832594;
x18.up = 28.90599083212131;
x18.l = 0.82936766721051747;

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
put c1_hi ' ' c1_hi.l ' ' c1_hi.m /;
put c2_hi ' ' c2_hi.l ' ' c2_hi.m /;
put c3_hi ' ' c3_hi.l ' ' c3_hi.m /;
put c4_lo ' ' c4_lo.l ' ' c4_lo.m /;
put c5_lo ' ' c5_lo.l ' ' c5_lo.m /;
put c6_hi ' ' c6_hi.l ' ' c6_hi.m /;
put c7_hi ' ' c7_hi.l ' ' c7_hi.m /;
put c8 ' ' c8.l ' ' c8.m /;
put c9 ' ' c9.l ' ' c9.m /;
put c10 ' ' c10.l ' ' c10.m /;
put c11_hi ' ' c11_hi.l ' ' c11_hi.m /;
put c12_lo ' ' c12_lo.l ' ' c12_lo.m /;
put c13_hi ' ' c13_hi.l ' ' c13_hi.m /;
put c14_hi ' ' c14_hi.l ' ' c14_hi.m /;
put c15_hi ' ' c15_hi.l ' ' c15_hi.m /;
put c16_hi ' ' c16_hi.l ' ' c16_hi.m /;
put c17_hi ' ' c17_hi.l ' ' c17_hi.m /;
put c18_hi ' ' c18_hi.l ' ' c18_hi.m /;
put c19_lo ' ' c19_lo.l ' ' c19_lo.m /;
put c20_hi ' ' c20_hi.l ' ' c20_hi.m /;
put c21_hi ' ' c21_hi.l ' ' c21_hi.m /;
put c22_hi ' ' c22_hi.l ' ' c22_hi.m /;
put c23_hi ' ' c23_hi.l ' ' c23_hi.m /;
put c24_hi ' ' c24_hi.l ' ' c24_hi.m /;
put c25_hi ' ' c25_hi.l ' ' c25_hi.m /;
put c26_lo ' ' c26_lo.l ' ' c26_lo.m /;
put c27_hi ' ' c27_hi.l ' ' c27_hi.m /;
put c28_hi ' ' c28_hi.l ' ' c28_hi.m /;
put c29_hi ' ' c29_hi.l ' ' c29_hi.m /;
put c30_hi ' ' c30_hi.l ' ' c30_hi.m /;
put c31_hi ' ' c31_hi.l ' ' c31_hi.m /;
put c32 ' ' c32.l ' ' c32.m /;
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
