#!/bin/sh
# Read-only extraction from the saved one-hour SCIP 10.0.3 campaign logs
# (research-20260929/publication/solver-runs/runs/*__SCIP/gams.log).
# Columns: instance | B&B nodes | dual bound on the first logged progress line | final dual bound.
# The first logged value is not necessarily the final root bound.
R=$(cd "$(dirname "$0")/../../../../../research-20260929/publication/solver-runs/runs" && pwd)
for d in "$R"/*__SCIP; do
  f=$d/gams.log; inst=$(basename "$d" __SCIP)
  nodes=$(grep -m1 "Solving Nodes" "$f" | awk '{print $4}')
  first=$(grep -m1 -E "^ *[A-Za-z*]? *[0-9.]+s\|" "$f" | awk -F'|' '{print $(NF-3)}' | tr -d ' ')
  fin=$(grep -m1 "^Dual Bound" "$f" | awk -F: '{print $2}' | tr -d ' ')
  echo "$inst | $nodes | $first | $fin"
done
