#!/bin/sh
# Cross-version seed scans (default settings, seeds 0-9) of the minimized fuzz reproducers,
# plus constraints/nonlinear/varboundrelax=b on master and 10.1.0.
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1
python3 run_binary.py min/fm318_master.cip 1.458 master,10.1.0,10.0.3,10.0.2,dbgsol 0-9
python3 run_binary.py min/fm336_v1010.cip 0.692592592593 master,10.1.0,10.0.3,10.0.2,dbgsol 0-9
python3 run_binary.py min/fm318_master.cip 1.458 master,10.1.0 0-9 constraints/nonlinear/varboundrelax=b
python3 run_binary.py min/fm336_v1010.cip 0.692592592593 master,10.1.0 0-9 constraints/nonlinear/varboundrelax=b
python3 seed_scan.py min/fm318_master.cip 1.458 10
python3 seed_scan.py min/fm336_v1010.cip 0.692592592593 10
echo FM_SCAN_DONE
