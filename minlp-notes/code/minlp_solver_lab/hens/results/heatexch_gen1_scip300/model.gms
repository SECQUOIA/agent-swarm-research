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
	c65
	c66
	c67
	c68
	c69
	c70
	c71
	c72
	c73
	c74
	c75
	c76
	c77
	c78
	c79
	c80
	c81
	c82
	c83
	c84
	c85
	c86
	c87
	c88
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
	c120_hi
	c121;

BINARY VARIABLES
	x97
	x98
	x99
	x100
	x101
	x102
	x103
	x104
	x105
	x106
	x107
	x108;

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
	x59
	x61
	x64
	x66
	x69
	x71
	x74
	x76
	x77
	x78
	x79
	x80
	x81
	x82
	x83
	x84
	x86
	x88
	x90
	x92
	x93
	x94
	x95
	x96
	x109
	x110
	x111
	x112;

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
	x57
	x58
	x60
	x62
	x63
	x65
	x67
	x68
	x70
	x72
	x73
	x75
	x85
	x87
	x89
	x91;


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
c65.. - (x57 - x58)/log(x57/(9.9999999999999995e-07 + x58)) + x59 =e= 0 ;
c66.. - (x58 - x60)/log(x58/(9.9999999999999995e-07 + x60)) + x61 =e= 0 ;
c67.. - (x62 - x63)/log(x62/(9.9999999999999995e-07 + x63)) + x64 =e= 0 ;
c68.. - (x63 - x65)/log(x63/(9.9999999999999995e-07 + x65)) + x66 =e= 0 ;
c69.. - (x67 - x68)/log(x67/(9.9999999999999995e-07 + x68)) + x69 =e= 0 ;
c70.. - (x68 - x70)/log(x68/(9.9999999999999995e-07 + x70)) + x71 =e= 0 ;
c71.. - (x72 - x73)/log(x72/(9.9999999999999995e-07 + x73)) + x74 =e= 0 ;
c72.. - (x73 - x75)/log(x73/(9.9999999999999995e-07 + x75)) + x76 =e= 0 ;
c73.. (-2)*x3/(0.01 + x59) + x77 =e= 0 ;
c74.. (-2)*x6/(0.01 + x61) + x78 =e= 0 ;
c75.. (-2)*x4/(0.01 + x64) + x79 =e= 0 ;
c76.. (-2)*x7/(0.01 + x66) + x80 =e= 0 ;
c77.. (-2)*x10/(0.01 + x69) + x81 =e= 0 ;
c78.. (-2)*x13/(0.01 + x71) + x82 =e= 0 ;
c79.. (-2)*x11/(0.01 + x74) + x83 =e= 0 ;
c80.. (-2)*x14/(0.01 + x76) + x84 =e= 0 ;
c81.. - ((-70) + x85)/log(0.0142857140816327*x85) + x86 =e= 0 ;
c82.. - ((-70) + x87)/log(0.0142857140816327*x87) + x88 =e= 0 ;
c83.. - ((-30) + x89)/log(0.0333333322222223*x89) + x90 =e= 0 ;
c84.. - ((-180) + x91)/log(0.00555555552469136*x91) + x92 =e= 0 ;
c85.. (-2)*x21/(0.01 + x86) + x93 =e= 0 ;
c86.. (-2)*x22/(0.01 + x88) + x94 =e= 0 ;
c87.. (-1.2)*x23/(0.01 + x90) + x95 =e= 0 ;
c88.. (-1.2)*x24/(0.01 + x92) + x96 =e= 0 ;
c89_hi.. (-2800)*x97 + x3 =l= 0 ;
c90_hi.. (-2800)*x98 + x6 =l= 0 ;
c91_hi.. (-1950)*x99 + x4 =l= 0 ;
c92_hi.. (-1950)*x100 + x7 =l= 0 ;
c93_hi.. (-3600)*x101 + x10 =l= 0 ;
c94_hi.. (-3600)*x102 + x13 =l= 0 ;
c95_hi.. (-1950)*x103 + x11 =l= 0 ;
c96_hi.. (-1950)*x104 + x14 =l= 0 ;
c97_hi.. (-3600)*x105 + x23 =l= 0 ;
c98_hi.. (-1950)*x106 + x24 =l= 0 ;
c99_hi.. (-2800)*x107 + x21 =l= 0 ;
c100_hi.. (-4400)*x108 + x22 =l= 0 ;
c101_hi.. 280*x97 - x1 + x15 + x57 =l= 280 ;
c102_hi.. 280*x98 - x2 + x16 + x58 =l= 280 ;
c103_hi.. 130*x99 - x1 + x18 + x62 =l= 130 ;
c104_hi.. 130*x100 - x2 + x19 + x63 =l= 130 ;
c105_hi.. 280*x101 - x8 + x15 + x67 =l= 280 ;
c106_hi.. 280*x102 - x9 + x16 + x68 =l= 280 ;
c107_hi.. 130*x103 - x8 + x18 + x72 =l= 130 ;
c108_hi.. 130*x104 - x9 + x19 + x73 =l= 130 ;
c109_hi.. 280*x97 - x2 + x16 + x58 =l= 280 ;
c110_hi.. 280*x98 - x5 + x17 + x60 =l= 280 ;
c111_hi.. 130*x99 - x2 + x19 + x63 =l= 130 ;
c112_hi.. 130*x100 - x5 + x20 + x65 =l= 130 ;
c113_hi.. 280*x101 - x9 + x16 + x68 =l= 280 ;
c114_hi.. 280*x102 - x12 + x17 + x70 =l= 280 ;
c115_hi.. 130*x103 - x9 + x19 + x73 =l= 130 ;
c116_hi.. 130*x104 - x12 + x20 + x75 =l= 130 ;
c117_hi.. -x5 + x85 =l= -320 ;
c118_hi.. -x12 + x87 =l= -320 ;
c119_hi.. x15 + x89 =l= 680 ;
c120_hi.. x18 + x91 =l= 680 ;
c121.. GAMS_OBJECTIVE =e= 5500*x97 + 5500*x98 + 5500*x99 + 5500*x100 + 5500*x101 + 5500*x102 + 5500*x103 + 5500*x104 + 5500*x107 + 5500*x108 + 5500*x105 + 5500*x106 + 15*x21 + 15*x22 + 80*x23 + 80*x24 + 150*x77 + 150*x78 + 150*x109 + 150*x79 + 150*x80 + 150*x110 + 150*x81 + 150*x82 + 150*x111 + 150*x83 + 150*x84 + 150*x112 + 150*x93 + 150*x94 + 150*x95 + 150*x96 ;

x97.l = 0;
x98.l = 0;
x99.l = 0;
x100.l = 0;
x101.l = 0;
x102.l = 0;
x103.l = 0;
x104.l = 0;
x105.l = 0;
x106.l = 0;
x107.l = 0;
x108.l = 0;
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
x59.l = 0;
x61.l = 0;
x64.l = 0;
x66.l = 0;
x69.l = 0;
x71.l = 0;
x74.l = 0;
x76.l = 0;
x77.l = 0;
x78.l = 0;
x79.l = 0;
x80.l = 0;
x81.l = 0;
x82.l = 0;
x83.l = 0;
x84.l = 0;
x86.l = 0;
x88.l = 0;
x90.l = 0;
x92.l = 0;
x93.l = 0;
x94.l = 0;
x95.l = 0;
x96.l = 0;
x109.l = 0;
x110.l = 0;
x111.l = 0;
x112.l = 0;
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
x57.lo = 10;
x57.l = 240;
x58.lo = 10;
x58.l = 240;
x60.lo = 10;
x60.l = 240;
x62.lo = 10;
x62.l = 300;
x63.lo = 10;
x63.l = 300;
x65.lo = 10;
x65.l = 300;
x67.lo = 10;
x67.l = 180;
x68.lo = 10;
x68.l = 180;
x70.lo = 10;
x70.l = 180;
x72.lo = 10;
x72.l = 240;
x73.lo = 10;
x73.l = 240;
x75.lo = 10;
x75.l = 240;
x85.lo = 10;
x85.l = 330;
x87.lo = 10;
x87.l = 270;
x89.lo = 10;
x89.l = 270;
x91.lo = 10;
x91.l = 330;

MODEL GAMS_MODEL /all/ ;
option minlp=scip;
option solprint=off;
option limrow=0;
option limcol=0;
option solvelink=5;
option savepoint=1;

* START USER ADDITIONAL OPTIONS

option reslim=300.0;
option optcr=0.0001;
option threads=4;

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
