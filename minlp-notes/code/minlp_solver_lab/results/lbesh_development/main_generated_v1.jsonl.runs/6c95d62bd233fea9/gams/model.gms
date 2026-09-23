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


c1_hi.. x1 + x2 =l= 1.091919990225652 ;
c2_hi.. x3 + x4 =l= 0.9217210066623412 ;
c3_hi.. x5 + x6 =l= 0.893169318423166 ;
c4_lo.. 0.81390688828712476 =l= x1 + x3 + x5 ;
c5_lo.. 0.639498269368455 =l= x2 + x4 + x6 ;
c6_hi.. 0.8441562375261966*x1 + 1.1842029720413245*x2 + 0.99222089869902907*x3 + 0.86300086587517*x4 + 0.92854735460674986*x5 + 0.9162954536845886*x6 =l= 1.4967744613292213 ;
c7_hi.. power(((x1 + 0.34999999999999998*x4)/1.091919990225652), 2) + power(((x3 + 0.34999999999999998*x6)/0.9217210066623412), 2) + power(((x5 + 0.34999999999999998*x2)/0.893169318423166), 2) =l= 0.41553180490195235 ;
c8.. x7 + x8 + x9 =e= 1 ;
c9.. x10 + x11 + x12 =e= 1 ;
c10.. x13 + x14 + x15 =e= 1 ;
c11_hi.. x1 + x2 - 2.183839980451304*(1 - x7) =l= 0 ;
c12_lo.. 0 =l= x16 - 0*(1 - x7) ;
c13_hi.. x16 - 11.307507202480847*(1 - x7) =l= 0 ;
c14_hi.. x1 + x2 - 1.522831241684234*(1 - x8) =l= 0.6610087387670701 ;
c15_hi.. 1.1999134744264952*(1.1730343668746852*(- log(1 + (-0.8325618334938989)*x1)/0.69314718055994529) + 1.0039768596425933*(- log(1 + (-0.8325618334938989)*x2)/0.69314718055994529) + 0.4173048877664651*(- log(1 - (x1 + x2)/2.4022239784964348)/0.69314718055994529)) - x16 - 10.769054478553185*(1 - x8) =l= 0 ;
c16_hi.. x1 + x2 - 1.091919990225652*(1 - x9) =l= 1.091919990225652 ;
c17_hi.. 0.7310789871474228*(1.1730343668746852*(- log(1 + (-0.8325618334938989)*x1)/0.69314718055994529) + 1.0039768596425933*(- log(1 + (-0.8325618334938989)*x2)/0.69314718055994529) + 0.4173048877664651*(- log(1 - (x1 + x2)/2.4022239784964348)/0.69314718055994529)) - x16 - 6.5613309697009905*(1 - x9) =l= 0 ;
c18_hi.. x3 + x4 - 1.8434420133246825*(1 - x10) =l= 0 ;
c19_lo.. 0 =l= x17 - 0*(1 - x10) ;
c20_hi.. x17 - 8.464766699415019*(1 - x10) =l= 0 ;
c21_hi.. x3 + x4 - 1.2502425826445296*(1 - x11) =l= 0.593199430680153 ;
c22_hi.. 0.9825831672446248*(1.037863174798965*(- log(1 + (-0.98629726622249037)*x3)/0.69314718055994529) + 1.1089212438475844*(- log(1 + (-0.98629726622249037)*x4)/0.69314718055994529) + 0.22487118249070664*(- log(1 - (x3 + x4)/2.027786214657151)/0.69314718055994529)) - x17 - 8.061682570871445*(1 - x11) =l= 0 ;
c23_hi.. x3 + x4 - 0.9217210066623412*(1 - x12) =l= 0.9217210066623412 ;
c24_hi.. 0.6554868442164625*(1.037863174798965*(- log(1 + (-0.98629726622249037)*x3)/0.69314718055994529) + 1.1089212438475844*(- log(1 + (-0.98629726622249037)*x4)/0.69314718055994529) + 0.22487118249070664*(- log(1 - (x3 + x4)/2.027786214657151)/0.69314718055994529)) - x17 - 5.3779944981896799*(1 - x12) =l= 0 ;
c25_hi.. x5 + x6 - 1.786338636846332*(1 - x13) =l= 0 ;
c26_lo.. 0 =l= x18 - 0*(1 - x13) ;
c27_hi.. x18 - 8.919147205234002*(1 - x13) =l= 0 ;
c28_hi.. x5 + x6 - 1.2253070071361272*(1 - x14) =l= 0.5610316297102049 ;
c29_hi.. 1.0261931359024588*(1.0379780541047494*(- log(1 + (-1.0178259489430868)*x5)/0.69314718055994529) + 0.9852612982025166*(- log(1 + (-1.0178259489430868)*x6)/0.69314718055994529) + 0.36952636046639897*(- log(1 - (x5 + x6)/1.9649725005309655)/0.69314718055994529)) - x18 - 8.494425909746668*(1 - x14) =l= 0 ;
c30_hi.. x5 + x6 - 0.893169318423166*(1 - x15) =l= 0.893169318423166 ;
c31_hi.. 0.67965436920051936*(1.0379780541047494*(- log(1 + (-1.0178259489430868)*x5)/0.69314718055994529) + 0.9852612982025166*(- log(1 + (-1.0178259489430868)*x6)/0.69314718055994529) + 0.36952636046639897*(- log(1 - (x5 + x6)/1.9649725005309655)/0.69314718055994529)) - x18 - 5.6259133699352466*(1 - x15) =l= 0 ;
c32.. GAMS_OBJECTIVE =e= 0 + 0.12024949298488265*x8 + 0.32881569856231413*x9 + x16 + 0 + 0.087347653789608848*x11 + 0.24094525998072877*x12 + x17 + 0 + 0.08334388820747865*x14 + 0.2240568066906454*x15 + x18 ;

x7.l = 0;
x8.l = 1;
x9.l = 0;
x10.l = 0;
x11.l = 1;
x12.l = 0;
x13.l = 0;
x14.l = 1;
x15.l = 0;
x1.up = 1.091919990225652;
x1.l = 0.3057375972631826;
x2.up = 1.091919990225652;
x2.l = 0.24022239784964344;
x3.up = 0.9217210066623412;
x3.l = 0.25808188186545555;
x4.up = 0.9217210066623412;
x4.l = 0.20277862146571507;
x5.up = 0.893169318423166;
x5.l = 0.25008740915848654;
x6.up = 0.893169318423166;
x6.l = 0.19649725005309654;
x16.up = 11.307507202480847;
x16.l = 1.170604092877028;
x17.up = 8.464766699415019;
x17.l = 0.8651569880387294;
x18.up = 8.919147205234002;
x18.l = 0.9179694349664168;

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
