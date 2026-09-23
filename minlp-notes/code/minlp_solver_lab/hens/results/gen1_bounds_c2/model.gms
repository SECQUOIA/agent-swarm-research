$offlisting
$offdigit

EQUATIONS
	c1
	c2
	c3
	c4
	c5
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
	c17_lo
	c18_lo
	c19_lo
	c20_lo
	c21_lo
	c22_lo
	c23_lo
	c24_lo
	c25_lo
	c26_lo
	c27_lo
	c28_lo
	c29
	c30
	c31
	c32
	c33
	c34
	c35
	c36
	c37
	c38
	c39
	c40
	c41
	c42
	c43
	c44
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
	c60
	c61
	c62
	c63
	c64
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
	c97;

BINARY VARIABLES
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
	x68;

POSITIVE VARIABLES
	x3
	x4
	x6
	x7
	x10
	x11
	x13
	x14
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
	x85
	x86
	x87
	x88
	x89
	x90
	x91
	x92
	x93
	x94
	x95
	x96
	x97
	x98
	x99
	x100;

VARIABLES
	GAMS_OBJECTIVE
	x1
	x2
	x5
	x8
	x9
	x12
	x15
	x16
	x17
	x18
	x19
	x20
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
	x84;


c1.. 10*x1 + (-10)*x2 - x3 - x4 =e= 0 ;
c2.. 10*x2 + (-10)*x5 - x6 - x7 =e= 0 ;
c3.. 20*x8 + (-20)*x9 - x10 - x11 =e= 0 ;
c4.. 20*x9 + (-20)*x12 - x13 - x14 =e= 0 ;
c5.. 15*x15 + (-15)*x16 - x3 - x10 =e= 0 ;
c6.. 15*x16 + (-15)*x17 - x6 - x13 =e= 0 ;
c7.. 13*x18 + (-13)*x19 - x4 - x11 =e= 0 ;
c8.. 13*x19 + (-13)*x20 - x7 - x14 =e= 0 ;
c9.. 10*x5 - x21 =e= 3700 ;
c10.. 20*x12 - x22 =e= 7400 ;
c11.. -x3 - x6 - x4 - x7 - x21 =e= -2800 ;
c12.. -x10 - x13 - x11 - x14 - x22 =e= -4400 ;
c13.. (-15)*x15 - x23 =e= -9750 ;
c14.. (-13)*x18 - x24 =e= -6500 ;
c15.. -x3 - x6 - x10 - x13 - x23 =e= -3600 ;
c16.. -x4 - x7 - x11 - x14 - x24 =e= -1950 ;
c17_lo.. 0 =l= x1 - x2 ;
c18_lo.. 0 =l= x2 - x5 ;
c19_lo.. 0 =l= x8 - x9 ;
c20_lo.. 0 =l= x9 - x12 ;
c21_lo.. 0 =l= x15 - x16 ;
c22_lo.. 0 =l= x16 - x17 ;
c23_lo.. 0 =l= x18 - x19 ;
c24_lo.. 0 =l= x19 - x20 ;
c25_lo.. 370 =l= x5 ;
c26_lo.. 370 =l= x12 ;
c27_lo.. -650 =l= -x15 ;
c28_lo.. -500 =l= -x18 ;
c29.. -x1 =e= -650 ;
c30.. -x8 =e= -590 ;
c31.. -x17 =e= -410 ;
c32.. -x20 =e= -350 ;
c33.. -x25 - x26 =e= -10 ;
c34.. -x27 - x28 =e= -10 ;
c35.. -x29 - x30 =e= -20 ;
c36.. -x31 - x32 =e= -20 ;
c37.. -x33 - x34 =e= -15 ;
c38.. -x35 - x36 =e= -15 ;
c39.. -x37 - x38 =e= -13 ;
c40.. -x39 - x40 =e= -13 ;
c41.. -x25*(x1 - x41) + x3 =e= 0 ;
c42.. -x27*(x2 - x42) + x6 =e= 0 ;
c43.. -x26*(x1 - x43) + x4 =e= 0 ;
c44.. -x28*(x2 - x44) + x7 =e= 0 ;
c45.. -x29*(x8 - x45) + x10 =e= 0 ;
c46.. -x31*(x9 - x46) + x13 =e= 0 ;
c47.. -x30*(x8 - x47) + x11 =e= 0 ;
c48.. -x32*(x9 - x48) + x14 =e= 0 ;
c49.. -x33*(-x16 + x49) + x3 =e= 0 ;
c50.. -x35*(-x17 + x50) + x6 =e= 0 ;
c51.. -x37*(-x19 + x51) + x4 =e= 0 ;
c52.. -x39*(-x20 + x52) + x7 =e= 0 ;
c53.. -x34*(-x16 + x53) + x10 =e= 0 ;
c54.. -x36*(-x17 + x54) + x13 =e= 0 ;
c55.. -x38*(-x19 + x55) + x11 =e= 0 ;
c56.. -x40*(-x20 + x56) + x14 =e= 0 ;
c57.. -x25*x41 - x26*x43 + 10*x2 =e= 0 ;
c58.. -x27*x42 - x28*x44 + 10*x5 =e= 0 ;
c59.. -x29*x45 - x30*x47 + 20*x9 =e= 0 ;
c60.. -x31*x46 - x32*x48 + 20*x12 =e= 0 ;
c61.. -x33*x49 - x34*x53 + 15*x15 =e= 0 ;
c62.. -x35*x50 - x36*x54 + 15*x16 =e= 0 ;
c63.. -x37*x51 - x38*x55 + 13*x18 =e= 0 ;
c64.. -x39*x52 - x40*x56 + 13*x19 =e= 0 ;
c65_hi.. (-2800)*x57 + x3 =l= 0 ;
c66_hi.. (-2800)*x58 + x6 =l= 0 ;
c67_hi.. (-1950)*x59 + x4 =l= 0 ;
c68_hi.. (-1950)*x60 + x7 =l= 0 ;
c69_hi.. (-3600)*x61 + x10 =l= 0 ;
c70_hi.. (-3600)*x62 + x13 =l= 0 ;
c71_hi.. (-1950)*x63 + x11 =l= 0 ;
c72_hi.. (-1950)*x64 + x14 =l= 0 ;
c73_hi.. (-3600)*x65 + x23 =l= 0 ;
c74_hi.. (-1950)*x66 + x24 =l= 0 ;
c75_hi.. (-2800)*x67 + x21 =l= 0 ;
c76_hi.. (-4400)*x68 + x22 =l= 0 ;
c77_hi.. 280*x57 - x1 + x15 + x69 =l= 280 ;
c78_hi.. 280*x58 - x2 + x16 + x70 =l= 280 ;
c79_hi.. 130*x59 - x1 + x18 + x71 =l= 130 ;
c80_hi.. 130*x60 - x2 + x19 + x72 =l= 130 ;
c81_hi.. 280*x61 - x8 + x15 + x73 =l= 280 ;
c82_hi.. 280*x62 - x9 + x16 + x74 =l= 280 ;
c83_hi.. 130*x63 - x8 + x18 + x75 =l= 130 ;
c84_hi.. 130*x64 - x9 + x19 + x76 =l= 130 ;
c85_hi.. 280*x57 - x2 + x16 + x70 =l= 280 ;
c86_hi.. 280*x58 - x5 + x17 + x77 =l= 280 ;
c87_hi.. 130*x59 - x2 + x19 + x72 =l= 130 ;
c88_hi.. 130*x60 - x5 + x20 + x78 =l= 130 ;
c89_hi.. 280*x61 - x9 + x16 + x74 =l= 280 ;
c90_hi.. 280*x62 - x12 + x17 + x79 =l= 280 ;
c91_hi.. 130*x63 - x9 + x19 + x76 =l= 130 ;
c92_hi.. 130*x64 - x12 + x20 + x80 =l= 130 ;
c93_hi.. -x5 + x81 =l= -320 ;
c94_hi.. -x12 + x82 =l= -320 ;
c95_hi.. x15 + x83 =l= 680 ;
c96_hi.. x18 + x84 =l= 680 ;
c97.. GAMS_OBJECTIVE =e= 5500*x57 + 5500*x58 + 5500*x59 + 5500*x60 + 5500*x61 + 5500*x62 + 5500*x63 + 5500*x64 + 5500*x67 + 5500*x68 + 5500*x65 + 5500*x66 + 15*x21 + 15*x22 + 80*x23 + 80*x24 + 150*x85 + 150*x86 + 150*x87 + 150*x88 + 150*x89 + 150*x90 + 150*x91 + 150*x92 + 150*x93 + 150*x94 + 150*x95 + 150*x96 + 150*x97 + 150*x98 + 150*x99 + 150*x100 ;

x57.l = 0;
x58.l = 0;
x59.l = 0;
x60.l = 0;
x61.l = 0;
x62.l = 0;
x63.l = 0;
x64.l = 0;
x65.l = 0;
x66.l = 0;
x67.l = 0;
x68.l = 0;
x3.l = 2800;
x4.l = 1950;
x6.l = 2800;
x7.l = 1950;
x10.l = 3600;
x11.l = 1950;
x13.l = 3600;
x14.l = 1950;
x21.l = 0;
x22.l = 0;
x23.l = 0;
x24.l = 0;
x25.up = 10;
x25.l = 10;
x26.up = 10;
x26.l = 10;
x27.up = 10;
x27.l = 10;
x28.up = 10;
x28.l = 10;
x29.up = 20;
x29.l = 20;
x30.up = 20;
x30.l = 20;
x31.up = 20;
x31.l = 20;
x32.up = 20;
x32.l = 20;
x33.up = 15;
x33.l = 15;
x34.up = 15;
x34.l = 15;
x35.up = 15;
x35.l = 15;
x36.up = 15;
x36.l = 15;
x37.up = 13;
x37.l = 13;
x38.up = 13;
x38.l = 13;
x39.up = 13;
x39.l = 13;
x40.up = 13;
x40.l = 13;
x85.l = 0;
x86.l = 0;
x87.l = 0;
x88.l = 0;
x89.l = 0;
x90.l = 0;
x91.l = 0;
x92.l = 0;
x93.l = 0;
x94.l = 0;
x95.l = 0;
x96.l = 0;
x97.l = 0;
x98.l = 0;
x99.l = 0;
x100.l = 0;
x1.lo = 370;
x1.up = 650;
x1.l = 650;
x2.lo = 370;
x2.up = 650;
x2.l = 650;
x5.lo = 370;
x5.up = 650;
x5.l = 650;
x8.lo = 370;
x8.up = 590;
x8.l = 590;
x9.lo = 370;
x9.up = 590;
x9.l = 590;
x12.lo = 370;
x12.up = 590;
x12.l = 590;
x15.lo = 410;
x15.up = 650;
x15.l = 410;
x16.lo = 410;
x16.up = 650;
x16.l = 410;
x17.lo = 410;
x17.up = 650;
x17.l = 410;
x18.lo = 350;
x18.up = 500;
x18.l = 350;
x19.lo = 350;
x19.up = 500;
x19.l = 350;
x20.lo = 350;
x20.up = 500;
x20.l = 350;
x41.lo = 370;
x41.up = 650;
x41.l = 650;
x42.lo = 370;
x42.up = 650;
x42.l = 650;
x43.lo = 370;
x43.up = 650;
x43.l = 650;
x44.lo = 370;
x44.up = 650;
x44.l = 650;
x45.lo = 370;
x45.up = 590;
x45.l = 590;
x46.lo = 370;
x46.up = 590;
x46.l = 590;
x47.lo = 370;
x47.up = 590;
x47.l = 590;
x48.lo = 370;
x48.up = 590;
x48.l = 590;
x49.lo = 410;
x49.up = 650;
x49.l = 410;
x50.lo = 410;
x50.up = 650;
x50.l = 410;
x51.lo = 350;
x51.up = 500;
x51.l = 350;
x52.lo = 350;
x52.up = 500;
x52.l = 350;
x53.lo = 410;
x53.up = 650;
x53.l = 410;
x54.lo = 410;
x54.up = 650;
x54.l = 410;
x55.lo = 350;
x55.up = 500;
x55.l = 350;
x56.lo = 350;
x56.up = 500;
x56.l = 350;
x69.lo = 10;
x69.l = 240;
x70.lo = 10;
x70.l = 240;
x71.lo = 10;
x71.l = 300;
x72.lo = 10;
x72.l = 300;
x73.lo = 10;
x73.l = 180;
x74.lo = 10;
x74.l = 180;
x75.lo = 10;
x75.l = 240;
x76.lo = 10;
x76.l = 240;
x77.lo = 10;
x77.l = 240;
x78.lo = 10;
x78.l = 300;
x79.lo = 10;
x79.l = 180;
x80.lo = 10;
x80.l = 240;
x81.lo = 10;
x81.l = 330;
x82.lo = 10;
x82.l = 270;
x83.lo = 10;
x83.l = 270;
x84.lo = 10;
x84.l = 330;

MODEL GAMS_MODEL /all/ ;
option minlp=baron;
option solprint=off;
option limrow=0;
option limcol=0;
option solvelink=5;
option savepoint=1;

* START USER ADDITIONAL OPTIONS

option reslim=600.0;
option optcr=1e-06;
option threads=4;
option optca=1e-3;

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


execute_unload 'results_s.gdx', MODELSTAT, SOLVESTAT, OBJEST, OBJVAL, NUMVAR, NUMEQU, NUMDVAR, NUMNZ, ETSOLVE;
