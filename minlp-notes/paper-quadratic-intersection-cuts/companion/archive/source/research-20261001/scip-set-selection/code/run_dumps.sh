#!/bin/bash
# Root runs with corner dumps (nlhdlr/quadratic/dumpfile) for rules 1 and 2; one process at a time.
# Usage: run_dumps.sh OUTDIR INST...
B="${HOME}"/build-scip/selection/build-lapack/bin/scip
O=$HOME/.cache/minlplib/minlplib/osil
out=$1; shift
mkdir -p $out
for inst in "$@"; do
  for rule in 1 2; do
    d=$out/$inst.r$rule.jsonl
    [ -s $d.gz ] && continue
    rm -f $d
    timeout 300 $B -c "set nlhdlr quadratic useintersectioncuts TRUE set nlhdlr quadratic setrule $rule set nlhdlr quadratic dumpfile $d set limits nodes 1 set limits time 120 set timing clocktype 1 read $O/$inst.osil opt quit" > $out/$inst.r$rule.log 2>&1
    gzip -f $d
  done
done
