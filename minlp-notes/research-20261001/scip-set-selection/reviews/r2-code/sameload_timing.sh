#!/bin/bash
# Review r2: run patched and stock binaries concurrently (same load) on identical-path instances.
# Four processes per instance: {patched, stock} x {off, scip}. Same command string as the benchmark.
set -u
P="${HOME}"/build-scip/selection/build-lapack/bin/scip
S="${HOME}"/build-scip/selection/revision-r1-stock/scip-stock
O=$HOME/.cache/minlplib/minlplib/osil
OUT=$(dirname "$0")/../r2-logs/sameload
mkdir -p "$OUT"
export OMP_NUM_THREADS=1
cmd() { # inst setting seed
  local c="set table nlhdlr_quadratic active TRUE set limits memory 6000 set limits time 300 set timing clocktype 1 "
  [ "$2" = scip ] && c+="set nlhdlr quadratic useintersectioncuts TRUE "
  c+="set randomization permutationseed $3 read $O/$1.osil opt display statistics quit"
  echo "$c"
}
for job in "$@"; do
  inst=${job%:*}; seed=${job#*:}
  uptime > "$OUT/$inst.s$seed.load"
  for b in patched stock; do
    bin=$P; [ $b = stock ] && bin=$S
    for s in off scip; do
      timeout 700 "$bin" -c "$(cmd $inst $s $seed)" > "$OUT/$inst.$s.s$seed.$b.log" 2>&1 &
    done
  done
  wait
  uptime >> "$OUT/$inst.s$seed.load"
done
