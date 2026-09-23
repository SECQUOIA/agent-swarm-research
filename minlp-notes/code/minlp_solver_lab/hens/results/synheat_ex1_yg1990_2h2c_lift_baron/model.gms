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
	c17_hi
	c18_hi
	c19_hi
	c20_hi
	c21_hi
	c22_hi
	c23_hi
	c24_hi
	c25
	c26
	c27
	c28
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
	c59_hi
	c60_hi
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
	c93;

BINARY VARIABLES
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
	x36;

POSITIVE VARIABLES
	x1
	x2
	x3
	x4
	x5
	x6
	x7
	x8
	x9
	x10
	x11
	x12
	x53
	x54
	x55
	x56
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
	x68
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

VARIABLES
	GAMS_OBJECTIVE
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
	x52;


c1.. x1 + x2 + x3 + x4 + x5 =e= 2800 ;
c2.. x6 + x7 + x8 + x9 + x10 =e= 4400 ;
c3.. x1 + x2 + x6 + x7 + x11 =e= 3600 ;
c4.. x3 + x4 + x8 + x9 + x12 =e= 1950 ;
c5.. 10*(x13 - x14) - (x1 + x3) =e= 0 ;
c6.. 10*(x14 - x15) - (x2 + x4) =e= 0 ;
c7.. 20*(x16 - x17) - (x6 + x8) =e= 0 ;
c8.. 20*(x17 - x18) - (x7 + x9) =e= 0 ;
c9.. 15*(x19 - x20) - (x1 + x6) =e= 0 ;
c10.. 15*(x20 - x21) - (x2 + x7) =e= 0 ;
c11.. 13*(x22 - x23) - (x3 + x8) =e= 0 ;
c12.. 13*(x23 - x24) - (x4 + x9) =e= 0 ;
c13.. x13 =e= 650 ;
c14.. x16 =e= 590 ;
c15.. x21 =e= 410 ;
c16.. x24 =e= 350 ;
c17_hi.. x14 - x13 =l= 0 ;
c18_hi.. x15 - x14 =l= 0 ;
c19_hi.. x17 - x16 =l= 0 ;
c20_hi.. x18 - x17 =l= 0 ;
c21_hi.. x20 - x19 =l= 0 ;
c22_hi.. x21 - x20 =l= 0 ;
c23_hi.. x23 - x22 =l= 0 ;
c24_hi.. x24 - x23 =l= 0 ;
c25.. x5 - 10*(x15 + (-370)) =e= 0 ;
c26.. x10 - 20*(x18 + (-370)) =e= 0 ;
c27.. x11 - 15*(650 - x19) =e= 0 ;
c28.. x12 - 13*(500 - x22) =e= 0 ;
c29_hi.. x1 + (-2800)*x25 =l= 0 ;
c30_hi.. x2 + (-2800)*x26 =l= 0 ;
c31_hi.. x3 + (-1950)*x27 =l= 0 ;
c32_hi.. x4 + (-1950)*x28 =l= 0 ;
c33_hi.. x6 + (-3600)*x29 =l= 0 ;
c34_hi.. x7 + (-3600)*x30 =l= 0 ;
c35_hi.. x8 + (-1950)*x31 =l= 0 ;
c36_hi.. x9 + (-1950)*x32 =l= 0 ;
c37_hi.. x5 + (-2800)*x33 =l= 0 ;
c38_hi.. x10 + (-4400)*x34 =l= 0 ;
c39_hi.. x11 + (-3600)*x35 =l= 0 ;
c40_hi.. x12 + (-1950)*x36 =l= 0 ;
c41_hi.. x37 - (x13 - x19 + 520*(1 - x25)) =l= 0 ;
c42_hi.. x38 - (x14 - x20 + 520*(1 - x26)) =l= 0 ;
c43_hi.. x39 - (x13 - x22 + 430*(1 - x27)) =l= 0 ;
c44_hi.. x40 - (x14 - x23 + 430*(1 - x28)) =l= 0 ;
c45_hi.. x41 - (x16 - x19 + 460*(1 - x29)) =l= 0 ;
c46_hi.. x42 - (x17 - x20 + 460*(1 - x30)) =l= 0 ;
c47_hi.. x43 - (x16 - x22 + 370*(1 - x31)) =l= 0 ;
c48_hi.. x44 - (x17 - x23 + 370*(1 - x32)) =l= 0 ;
c49_hi.. x38 - (x14 - x20 + 520*(1 - x25)) =l= 0 ;
c50_hi.. x45 - (x15 - x21 + 520*(1 - x26)) =l= 0 ;
c51_hi.. x40 - (x14 - x23 + 430*(1 - x27)) =l= 0 ;
c52_hi.. x46 - (x15 - x24 + 430*(1 - x28)) =l= 0 ;
c53_hi.. x42 - (x17 - x20 + 460*(1 - x29)) =l= 0 ;
c54_hi.. x47 - (x18 - x21 + 460*(1 - x30)) =l= 0 ;
c55_hi.. x44 - (x17 - x23 + 370*(1 - x31)) =l= 0 ;
c56_hi.. x48 - (x18 - x24 + 370*(1 - x32)) =l= 0 ;
c57_hi.. x49 - (x15 + (-320) + 280*(1 - x33)) =l= 0 ;
c58_hi.. x50 - (x18 + (-320) + 220*(1 - x34)) =l= 0 ;
c59_hi.. x51 - (680 - x19 + 240*(1 - x35)) =l= 0 ;
c60_hi.. x52 - (680 - x22 + 150*(1 - x36)) =l= 0 ;
c61.. x53 - x54*x37 =e= 0 ;
c62.. x55 - x56*x38 =e= 0 ;
c63.. x57 - x58*x39 =e= 0 ;
c64.. x59 - x60*x40 =e= 0 ;
c65.. x61 - x62*x41 =e= 0 ;
c66.. x63 - x64*x42 =e= 0 ;
c67.. x65 - x66*x43 =e= 0 ;
c68.. x67 - x68*x44 =e= 0 ;
c69.. x69 - x54*x38 =e= 0 ;
c70.. x70 - x56*x45 =e= 0 ;
c71.. x71 - x58*x40 =e= 0 ;
c72.. x72 - x60*x46 =e= 0 ;
c73.. x73 - x62*x42 =e= 0 ;
c74.. x74 - x64*x47 =e= 0 ;
c75.. x75 - x66*x44 =e= 0 ;
c76.. x76 - x68*x48 =e= 0 ;
c77.. x77 - x78*x49 =e= 0 ;
c78.. x79 - x80*x50 =e= 0 ;
c79.. x81 - x82*x51 =e= 0 ;
c80.. x83 - x84*x52 =e= 0 ;
c81_hi.. x1 - 0.5*(x53*x69*(x53 + x69)/2) ** 0.3333333333333333 =l= 0 ;
c82_hi.. x2 - 0.5*(x55*x70*(x55 + x70)/2) ** 0.3333333333333333 =l= 0 ;
c83_hi.. x3 - 0.5*(x57*x71*(x57 + x71)/2) ** 0.3333333333333333 =l= 0 ;
c84_hi.. x4 - 0.5*(x59*x72*(x59 + x72)/2) ** 0.3333333333333333 =l= 0 ;
c85_hi.. x6 - 0.5*(x61*x73*(x61 + x73)/2) ** 0.3333333333333333 =l= 0 ;
c86_hi.. x7 - 0.5*(x63*x74*(x63 + x74)/2) ** 0.3333333333333333 =l= 0 ;
c87_hi.. x8 - 0.5*(x65*x75*(x65 + x75)/2) ** 0.3333333333333333 =l= 0 ;
c88_hi.. x9 - 0.5*(x67*x76*(x67 + x76)/2) ** 0.3333333333333333 =l= 0 ;
c89_hi.. x5 - 0.5*(x77*(70*x78)*(x77 + 70*x78)/2) ** 0.3333333333333333 =l= 0 ;
c90_hi.. x10 - 0.5*(x79*(70*x80)*(x79 + 70*x80)/2) ** 0.3333333333333333 =l= 0 ;
c91_hi.. x11 - 0.83333333333333337*(30*x82*x81*(30*x82 + x81)/2) ** 0.3333333333333333 =l= 0 ;
c92_hi.. x12 - 0.83333333333333337*(180*x84*x83*(180*x84 + x83)/2) ** 0.3333333333333333 =l= 0 ;
c93.. GAMS_OBJECTIVE =e= 5500*(x25 + x26 + x27 + x28 + x29 + x30 + x31 + x32 + x33 + x34 + x35 + x36) + 150*(x54 + x56 + x58 + x60 + x62 + x64 + x66 + x68 + x78 + x80 + x82 + x84) + 15*(x5 + x10) + 80*(x11 + x12) ;

x1.up = 2800;
x2.up = 2800;
x3.up = 1950;
x4.up = 1950;
x5.up = 2800;
x6.up = 3600;
x7.up = 3600;
x8.up = 1950;
x9.up = 1950;
x10.up = 4400;
x11.up = 3600;
x12.up = 1950;
x53.up = 134400.00000000003;
x54.up = 560.0000000000001;
x55.up = 134400.00000000003;
x56.up = 560.0000000000001;
x57.up = 117000.00000000001;
x58.up = 390.00000000000006;
x59.up = 117000.00000000001;
x60.up = 390.00000000000006;
x61.up = 129600.00000000001;
x62.up = 720.0000000000001;
x63.up = 129600.00000000001;
x64.up = 720.0000000000001;
x65.up = 93600.00000000001;
x66.up = 390.00000000000006;
x67.up = 93600.00000000001;
x68.up = 390.00000000000006;
x69.up = 134400.00000000003;
x70.up = 134400.00000000003;
x71.up = 117000.00000000001;
x72.up = 117000.00000000001;
x73.up = 129600.00000000001;
x74.up = 129600.00000000001;
x75.up = 93600.00000000001;
x76.up = 93600.00000000001;
x77.up = 60857.759055171504;
x78.up = 184.41745168233788;
x79.up = 78245.690213791939;
x80.up = 289.79885264367385;
x81.up = 64189.46571851154;
x82.up = 237.7387619204131;
x83.up = 13912.262405284204;
x84.up = 42.158370925103647;
x13.lo = 370;
x13.up = 650;
x14.lo = 370;
x14.up = 650;
x15.lo = 370;
x15.up = 650;
x16.lo = 370;
x16.up = 590;
x17.lo = 370;
x17.up = 590;
x18.lo = 370;
x18.up = 590;
x19.lo = 410;
x19.up = 650;
x20.lo = 410;
x20.up = 650;
x21.lo = 410;
x21.up = 650;
x22.lo = 350;
x22.up = 500;
x23.lo = 350;
x23.up = 500;
x24.lo = 350;
x24.up = 500;
x37.lo = 10;
x37.up = 240;
x38.lo = 10;
x38.up = 240;
x39.lo = 10;
x39.up = 300;
x40.lo = 10;
x40.up = 300;
x41.lo = 10;
x41.up = 180;
x42.lo = 10;
x42.up = 180;
x43.lo = 10;
x43.up = 240;
x44.lo = 10;
x44.up = 240;
x45.lo = 10;
x45.up = 240;
x46.lo = 10;
x46.up = 300;
x47.lo = 10;
x47.up = 180;
x48.lo = 10;
x48.up = 240;
x49.lo = 10;
x49.up = 330;
x50.lo = 10;
x50.up = 270;
x51.lo = 10;
x51.up = 270;
x52.lo = 10;
x52.up = 330;

MODEL GAMS_MODEL /all/ ;
option minlp=baron;
option solprint=off;
option limrow=0;
option limcol=0;
option solvelink=5;
option savepoint=1;

* START USER ADDITIONAL OPTIONS

option reslim=150.0;
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
