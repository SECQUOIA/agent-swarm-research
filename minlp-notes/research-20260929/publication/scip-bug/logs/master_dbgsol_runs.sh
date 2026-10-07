#!/bin/sh
# Debug-solution runs on the local SCIP master build with the diagnostic patch
# (build/scip-master-dbgsol). One run at a time. Output: logs/mdbg_<tag>.log
cd "$(dirname "$0")/.."
H=$PWD
B=$H/build/scip-master-dbgsol/bin/scip
export LD_LIBRARY_PATH=$H/conda-env/lib OMP_NUM_THREADS=1 SCIPBUG_SB=1 SCIPBUG_EXPR=1
run() { # tag model solfile seed [extra set lines]
  tag=$1; model=$2; sol=$3; seed=$4; shift 4
  s=$H/tmp/mdbg_$tag.set
  printf 'misc/debugsol = "%s"\nrandomization/randomseedshift = %s\nlimits/time = 600\n' "$sol" "$seed" > $s
  for x in "$@"; do echo "$x" >> $s; done
  timeout 900 $B -s $s -c "read $model" -c optimize -c "display solution" -c quit > $H/logs/mdbg_$tag.log 2>&1
  echo "$tag exit $?: $(grep -c 'SCIPBUG REVCUT' $H/logs/mdbg_$tag.log) REVCUT, $(grep -c 'debugging solution was cut off\|ERROR' $H/logs/mdbg_$tag.log) debug errors; $(grep 'Dual Bound' $H/logs/mdbg_$tag.log)"
}
run fm336_s0 $H/min/fm336_v1010.cip $H/min/fm336_v1010.witness.sol 0
run fm336_vbrn_s0 $H/min/fm336_v1010.cip $H/min/fm336_v1010.witness.sol 0 "constraints/nonlinear/varboundrelax = n"
run fm318_s0 $H/min/fm318_master.cip $H/min/fm318_master.witness.sol 0
run pumps_default_s3 $H/minimal/pumps_default.cip $H/minimal/pumps_default_witness.sol 3
printf 'misc/debugsol = "%s"\n' $H/minimal/tiny2_witness.sol > $H/tmp/mdbg_tiny2.set
timeout 300 $B -s $H/tmp/mdbg_tiny2.set -c "set heuristics emphasis off" -c "set separating emphasis off" -c "read $H/minimal/tiny2.cip" -c optimize -c "display solution" -c quit > $H/logs/mdbg_tiny2_hsoff.log 2>&1
echo "tiny2_hsoff exit $?: $(grep -c 'SCIPBUG REVCUT' $H/logs/mdbg_tiny2_hsoff.log) REVCUT; $(grep 'Dual Bound' $H/logs/mdbg_tiny2_hsoff.log)"
run pair2236_s14 $H/models/pair2236.cip $H/witness/pair2236.sol 14
run p4_s0 $H/models/p4.cip $H/witness/p4.sol 0
run p5_s3 $H/models/p5.cip $H/witness/p5.sol 3
echo MDBG_DONE
