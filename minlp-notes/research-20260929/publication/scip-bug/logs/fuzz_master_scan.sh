#!/bin/sh
# Seed scans (0-9, default settings) of the 8 fuzz candidates found with the master oracle,
# on SCIP master and on the 10.1.0 release binary. Reference value: the varboundrelax=b claim
# from logs/fuzz_master_s11.log (approximate; exact witnesses are made afterwards).
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1
for kv in 94:1.65799999314 145:0.647999970015772 190:5.10757811286656 318:1.4579999875807 336:0.692592587054755 355:1.70999812119908 392:0.450629616888606 394:1.4999999919; do
  k=${kv%%:*}; w=${kv#*:}
  python3 run_binary.py minimal/fuzz_master/fuzz_11_$k.cip $w master,10.1.0 0-9
done
echo SCAN_DONE
