#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
# Reviewer's own runs of the small reproducers on every local SCIP binary (sequential, 1 thread).
T="${_PUBLIC_REPO}"/research-20260929/publication/scip-bug
EX=$T/install/extralib/usr/lib/x86_64-linux-gnu
export OMP_NUM_THREADS=1
SD="${_PUBLIC_REPO}"/research-20260929/publication/reviews/scip-bug-r1/tmp
for p in a b n; do echo "constraints/nonlinear/varboundrelax = $p" > $SD/vbr_$p.set; done
for s in 0 1 2 3 4 5 6 7 8 9; do echo "randomization/randomseedshift = $s" > $SD/seed_$s.set; done
run() { # label exe ldpath args...
  local lab=$1 exe=$2 ld=$3; shift 3
  LD_LIBRARY_PATH=$ld "$exe" "$@" < /dev/null 2>&1 | grep -E "^SCIP version|SCIP Status|Primal Bound|Dual Bound|Solving Nodes|feasible solution given|^b[0-9]? |^objective value" | sed "s/^/[$lab] /"
}
for v in 10.0.2 10.0.3 10.1.0 master; do
  if [ $v = master ]; then exe=$T/build/scip-master/bin/scip; ld=$T/conda-env/lib; else exe=$T/install/$v/scipoptsuite-$v/bin/scip; ld=$T/install/$v/scipoptsuite-$v/lib64:$EX; fi
  for s in 0 1 2 3 4 5; do
    echo "== $v fm336 default seed $s"
    run "$v fm336 s$s" $exe $ld -s $SD/seed_$s.set -c "read $T/min/fm336_v1010.cip" -c optimize -c "display solution" -c quit
  done
  echo "== $v fm336 witness read as .sol"
  run "$v fm336 readsol" $exe $ld -c "read $T/min/fm336_v1010.cip" -c "read $T/min/fm336_v1010.witness.sol" -c optimize -c quit
  for p in b n a; do
    echo "== $v fm336 varboundrelax=$p seed 0"
    run "$v fm336 vbr$p" $exe $ld -s $SD/vbr_$p.set -c "read $T/min/fm336_v1010.cip" -c optimize -c quit
  done
  echo "== $v tiny2 default"
  run "$v tiny2 default" $exe $ld -c "read $T/minimal/tiny2.cip" -c optimize -c "display solution" -c quit
  echo "== $v tiny2 heur+sepa off"
  run "$v tiny2 hsoff" $exe $ld -c "set heuristics emphasis off" -c "set separating emphasis off" -c "read $T/minimal/tiny2.cip" -c optimize -c "display solution" -c quit
  echo "== $v tiny2 heur+sepa off varboundrelax=b"
  run "$v tiny2 hsoff vbrb" $exe $ld -c "set heuristics emphasis off" -c "set separating emphasis off" -s $SD/vbr_b.set -c "read $T/minimal/tiny2.cip" -c optimize -c quit
done
echo RV_RUNS_DONE
