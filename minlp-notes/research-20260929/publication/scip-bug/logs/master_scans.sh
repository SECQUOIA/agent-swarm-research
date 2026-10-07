#!/bin/sh
# Seed scans of all models on the local SCIP master build (default settings, seed shift varies).
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1
python3 run_binary.py minimal/pumps_default.cip 0.612 master 0-19 > logs/master_pumps_default.log 2>&1
python3 run_binary.py minimal/variants/pumps4_default.cip 1.029 master 0-9 > logs/master_pumps4_default.log 2>&1
python3 run_binary.py models/pair2236.cip 55.689908409449 master 0-29 > logs/master_pair2236.log 2>&1
python3 run_binary.py models/p4.cip -6.730643699816 master 0-9 > logs/master_p4.log 2>&1
python3 run_binary.py models/p5.cip -232.172853003462 master 0-9 > logs/master_p5.log 2>&1
python3 run_binary.py models/p0.cip 168.108652029808 master 0-9 > logs/master_p0.log 2>&1
echo SCANS_DONE
