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


c1_hi.. x1 + x2 =l= 0.8862850147873512 ;
c2_hi.. x3 + x4 =l= 1.110867137534256 ;
c3_hi.. x5 + x6 =l= 1.1712149097436644 ;
c4_lo.. 0.88714277737827618 =l= x1 + x3 + x5 ;
c5_lo.. 0.6970407536543598 =l= x2 + x4 + x6 ;
c6_hi.. 0.70944955621805217*x1 + 1.222548093338738*x2 + 1.2744219650250774*x3 + 0.850697720541431*x4 + 0.7693075496182604*x5 + 0.75236959296690797*x6 =l= 1.5820735531700474 ;
c7_hi.. power(((x1 + 0.34999999999999998*x4)/0.8862850147873512), 2) + power(((x3 + 0.34999999999999998*x6)/1.110867137534256), 2) + power(((x5 + 0.34999999999999998*x2)/1.1712149097436644), 2) =l= 0.4175702837328236 ;
c8.. x7 + x8 + x9 =e= 1 ;
c9.. x10 + x11 + x12 =e= 1 ;
c10.. x13 + x14 + x15 =e= 1 ;
c11_hi.. x1 + x2 - 1.7725700295747024*(1 - x7) =l= 0 ;
c12_lo.. 0 =l= x16 - 0*(1 - x7) ;
c13_hi.. x16 - 25.618658662377765*(1 - x7) =l= 0 ;
c14_hi.. x1 + x2 - 1.2395667497372445*(1 - x8) =l= 0.53300327983745799 ;
c15_hi.. 1.0905434109600063*(0.9998025333227194*(1/(1 + (-1.0257320093683742)*x1) + (-1)) + 0.8977116618376255*(1/(1 + (-1.0257320093683742)*x2) + (-1)) + 0.33978532821394225*(1/(1 - (x1 + x2)/1.9498270325321729) + (-1))) - x16 - 24.398722535597869*(1 - x8) =l= 0 ;
c16_hi.. x1 + x2 - 0.8862850147873512*(1 - x9) =l= 0.8862850147873512 ;
c17_hi.. 0.74182602923057916*(0.9998025333227194*(1/(1 + (-1.0257320093683742)*x1) + (-1)) + 0.8977116618376255*(1/(1 + (-1.0257320093683742)*x2) + (-1)) + 0.33978532821394225*(1/(1 - (x1 + x2)/1.9498270325321729) + (-1))) - x16 - 16.596870216242117*(1 - x9) =l= 0 ;
c18_hi.. x3 + x4 - 2.221734275068512*(1 - x10) =l= 0 ;
c19_lo.. 0 =l= x17 - 0*(1 - x10) ;
c20_hi.. x17 - 28.791588143842038*(1 - x10) =l= 0 ;
c21_hi.. x3 + x4 - 1.5742984507476869*(1 - x11) =l= 0.647435824320825 ;
c22_hi.. 1.2566692205558732*(0.8984324830900534*(1/(1 + (-0.8183615109082972)*x3) + (-1)) + 1.0259491581910796*(1/(1 + (-0.8183615109082972)*x4) + (-1)) + 0.25762136225095456*(1/(1 - (x3 + x4)/2.4439077025753635) + (-1))) - x17 - 27.420560136992382*(1 - x11) =l= 0 ;
c23_hi.. x3 + x4 - 1.110867137534256*(1 - x12) =l= 1.110867137534256 ;
c24_hi.. 0.72854632150844278*(0.8984324830900534*(1/(1 + (-0.8183615109082972)*x3) + (-1)) + 1.0259491581910796*(1/(1 + (-0.8183615109082972)*x4) + (-1)) + 0.25762136225095456*(1/(1 - (x3 + x4)/2.4439077025753635) + (-1))) - x17 - 15.896902617436735*(1 - x12) =l= 0 ;
c25_hi.. x5 + x6 - 2.3424298194873288*(1 - x13) =l= 0 ;
c26_lo.. 0 =l= x18 - 0*(1 - x13) ;
c27_hi.. x18 - 38.230424358923926*(1 - x13) =l= 0 ;
c28_hi.. x5 + x6 - 1.562586277646758*(1 - x14) =l= 0.77984354184057059 ;
c29_hi.. 1.344667401242384*(1.055744515497063*(1/(1 + (-0.7761947884439717)*x5) + (-1)) + 1.1831373889800023*(1/(1 + (-0.7761947884439717)*x6) + (-1)) + 0.46884551772708488*(1/(1 - (x5 + x6)/2.5766728014360618) + (-1))) - x18 - 36.409927960879877*(1 - x14) =l= 0 ;
c30_hi.. x5 + x6 - 1.1712149097436644*(1 - x15) =l= 1.1712149097436644 ;
c31_hi.. 0.7853404202088383*(1.055744515497063*(1/(1 + (-0.7761947884439717)*x5) + (-1)) + 1.1831373889800023*(1/(1 + (-0.7761947884439717)*x6) + (-1)) + 0.46884551772708488*(1/(1 - (x5 + x6)/2.5766728014360618) + (-1))) - x18 - 21.264877915647979*(1 - x15) =l= 0 ;
c32.. GAMS_OBJECTIVE =e= 0 + 0.078989399819706207*x8 + 0.3067455280686752*x9 + x16 + 0 + 0.1194779605770668*x11 + 0.30417754516765594*x12 + x17 + 0 + 0.11374291175959307*x14 + 0.33070799821951735*x15 + x18 ;

x7.l = 0;
x8.l = 1;
x9.l = 0;
x10.l = 0;
x11.l = 1;
x12.l = 0;
x13.l = 0;
x14.l = 1;
x15.l = 0;
x1.up = 0.8862850147873512;
x1.l = 0.24815980414045838;
x2.up = 0.8862850147873512;
x2.l = 0.19498270325321726;
x3.up = 1.110867137534256;
x3.l = 0.3110427985095917;
x4.up = 1.110867137534256;
x4.l = 0.24439077025753633;
x5.up = 1.1712149097436644;
x5.l = 0.32794017472822606;
x6.up = 1.1712149097436644;
x6.l = 0.25766728014360618;
x16.up = 25.618658662377765;
x16.l = 0.72604101411461086;
x17.up = 28.791588143842038;
x17.l = 0.803062026807973;
x18.up = 38.230424358923926;
x18.l = 1.067905556481807;

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
