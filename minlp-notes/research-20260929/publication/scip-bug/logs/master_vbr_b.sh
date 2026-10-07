#!/bin/sh
# Master's wrong runs repeated with constraints/nonlinear/varboundrelax = b (relax all variable bounds by epsilon).
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1
X=constraints/nonlinear/varboundrelax=b
python3 run_binary.py minimal/pumps_default.cip 0.612 master 3 $X > logs/master_vbr_b_pumps_default.log 2>&1
python3 run_binary.py models/pair2236.cip 55.689908409449 master 14,16,25,26,27 $X > logs/master_vbr_b_pair2236.log 2>&1
python3 run_binary.py models/p5.cip -232.172853003462 master 3,4,7,8 $X > logs/master_vbr_b_p5.log 2>&1
python3 run_binary.py models/p4.cip -6.730643699816 master 0-9 $X > logs/master_vbr_b_p4.log 2>&1
echo DONE
