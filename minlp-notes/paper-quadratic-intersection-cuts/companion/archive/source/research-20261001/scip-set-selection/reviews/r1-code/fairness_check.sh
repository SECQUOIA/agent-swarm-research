#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../../../../.." && pwd)"
# Review r1: does the patched binary with setrule = 0 (setting "scip") follow the same path as unpatched SCIP 10.0.3?
# The unpatched binary /tmp/r1chk/scip-pristine-lapack was produced by compiling the pristine nlhdlr_quadratic.c from
# the 10.0.3 tarball with the flags of build-lapack and relinking the build-lapack objects (see review-r1.md).
# Usage: fairness_check.sh NODELIMIT INST...
OUT="${_PUBLIC_REPO}"/research-20261001/scip-set-selection/reviews/r1-logs/fairness
OSIL=$HOME/.cache/minlplib/minlplib/osil
P="${HOME}"/build-scip/selection/build-lapack/bin/scip
U=/tmp/r1chk/scip-pristine-lapack
NODES=$1; shift
export OMP_NUM_THREADS=1
for inst in "$@"; do
  for b in P U; do
    bin=${!b}
    c="set limits memory 6000 set limits time 600 set timing clocktype 1 set nlhdlr quadratic useintersectioncuts TRUE set limits nodes $NODES read $OSIL/$inst.osil opt display statistics quit"
    timeout 700 $bin -c "$c" > $OUT/$inst.n$NODES.$b.log 2>&1 &
  done
  wait
done
