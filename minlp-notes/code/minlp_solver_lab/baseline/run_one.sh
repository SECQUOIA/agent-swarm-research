#!/bin/bash
# usage: run_one.sh NAME SOLVER RESLIM
set -u
NAME=$1; SOLVER=$2; RESLIM=${3:-60}
D=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
OUT=$D/baseline/out/$NAME.$SOLVER.txt
[ -s "$OUT" ] && exit 0
W=$D/baseline/wrap/$NAME.$SOLVER.gms
cat > "$W" <<EOG
\$include "$D/instances/gms/$NAME.gms"
scalar ms, ss, ov, oe, ru, nn;
ms = m.modelstat; ss = m.solvestat; ov = m.objval; oe = m.objest; ru = m.resusd; nn = m.nodusd;
file f / "$OUT" /; put f; put ms:0:0 ',' ss:0:0 ',' ov:0:10 ',' oe:0:10 ',' ru:0:3 ',' nn:0:0 /; putclose f;
EOG
cd "$D/baseline/wrap" && timeout $((RESLIM+90)) gams "$W" minlp=$SOLVER reslim=$RESLIM optcr=1e-4 optca=1e-6 threads=4 lo=2 lf="$D/baseline/lst/$NAME.$SOLVER.log" o="$D/baseline/lst/$NAME.$SOLVER.lst" > /dev/null 2>&1
[ -s "$OUT" ] || echo "NA,NA,NA,NA,NA,NA" > "$OUT"
