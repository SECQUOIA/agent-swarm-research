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
c8_hi.. exp((-1.8467071355984399)*(x1 + 0.71323200390973929)) + exp(1.8467071355984399*(x1 + 0.71323200390973929)) + exp((-1.758605924495459)*(x4 + 0.2946290026001007)) + exp(1.758605924495459*(x4 + 0.2946290026001007)) - 232.12027000331153*(1 - x8) =l= 5.260581079678344 ;
c9_hi.. exp((-1.8521822735224505)*(x1 + (-0.25127259508562988))) + exp(1.8521822735224505*(x1 + (-0.25127259508562988))) + exp((-1.8441562375261964)*(x4 + (-0.73589594014211468))) + exp(1.8441562375261964*(x4 + (-0.73589594014211468))) - 250.43312821503559*(1 - x9) =l= 5.3742739901561345 ;
c10_hi.. exp((-2.1842029720413243)*(x1 + (-0.84050660876730487))) + exp(2.1842029720413243*(x1 + (-0.84050660876730487))) + exp((-1.8825815099935117)*(x4 + 0.4481834544571533)) + exp(1.8825815099935117*(x4 + 0.4481834544571533)) - 621.50550492964419*(1 - x10) =l= 4.866323153308551 ;
c11_hi.. exp((-1.8996879397058279)*(x2 + 0.75207442701359217)) + exp(1.8996879397058279*(x2 + 0.75207442701359217)) + exp((-1.705135490454622)*(x5 + 0.38653310243328798)) + exp(1.705135490454622*(x5 + 0.38653310243328798)) - 266.23187698887568*(1 - x11) =l= 5.088393938246118 ;
c12_hi.. exp((-1.996803807751047)*(x2 + (-0.20726772736926644))) + exp(1.996803807751047*(x2 + (-0.20726772736926644))) + exp((-2.0328405158399514)*(x5 + (-0.71215297731351979))) + exp(2.0328405158399514*(x5 + (-0.71215297731351979))) - 374.20070631384743*(1 - x12) =l= 5.4204173454783238 ;
c13_hi.. exp((-1.9888148359193805)*(x2 + (-0.7952836154248053))) + exp(1.9888148359193805*(x2 + (-0.7952836154248053))) + exp((-1.9285473546067498)*(x5 + 0.43958594108458726)) + exp(1.9285473546067498*(x5 + 0.43958594108458726)) - 396.3313205914444*(1 - x13) =l= 5.0451549144522509 ;
c14_hi.. exp((-2.086007928296888)*(x3 + 0.7384172412716103)) + exp(2.086007928296888*(x3 + 0.7384172412716103)) + exp((-1.8820113289584965)*(x6 + 0.2857780267142494)) + exp(1.8820113289584965*(x6 + 0.2857780267142494)) - 410.3260562072758*(1 - x14) =l= 5.17568993289922 ;
c15_hi.. exp((-1.8798289236046817)*(x3 + (-0.30976505371968616))) + exp(1.8798289236046817*(x3 + (-0.30976505371968616))) + exp((-2.2856134912364903)*(x6 + (-0.69708891361867809))) + exp(2.2856134912364903*(x6 + (-0.69708891361867809))) - 590.97958163789247*(1 - x15) =l= 5.074027223530047 ;
c16_hi.. exp((-2.1711478624804323)*(x3 + (-0.84571513105400486))) + exp(2.1711478624804323*(x3 + (-0.84571513105400486))) + exp((-1.9820298835348982)*(x6 + 0.50222593521669456)) + exp(1.9820298835348982*(x6 + 0.50222593521669456)) - 651.42514645663789*(1 - x16) =l= 5.0708022387615266 ;
c17.. GAMS_OBJECTIVE =e= 0.9476582735800375*x1 + 0.172816032702172*x4 + 0.9181403966481416*x2 + 0.2575331620988591*x5 + 0.9936235549325296*x3 + 0.2597113299068806*x6 + 0.1*x7 + 0.024809300257571124*x8 + 0.0383466112235165*x9 + 0.058146844691017954*x10 + 0.061225970289994117*x11 + 0.049847919352029896*x12 + 0.078515600210966138*x13 + 0.046012184474915029*x14 + 0.039683322582262148*x15 + 0.069995374120620429*x16 ;

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
x7.l = 0.03432822214410288;
x1.lo = -2;
x1.up = 2;
x1.l = 0.25127259508562988;
x2.lo = -2;
x2.up = 2;
x2.l = 0.20726772736926644;
x3.lo = -2;
x3.up = 2;
x3.l = 0.30976505371968616;
x4.lo = -2;
x4.up = 2;
x4.l = 0.73589594014211468;
x5.lo = -2;
x5.up = 2;
x5.l = 0.71215297731351979;
x6.lo = -2;
x6.up = 2;
x6.l = 0.69708891361867809;

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
