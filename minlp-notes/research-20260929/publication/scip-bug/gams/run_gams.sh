#!/bin/sh
# usage: run_gams.sh MODEL.gms TAG [optfile-contents-file]
# Runs GAMS/SCIP on MODEL with an optional SCIP option file; log in logs/gams_TAG.log
G="${HOME}"/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams
D=$(mktemp -d /tmp/gamsrun.XXXXXX)
cp "$1" "$D/model.gms"
if [ -n "$3" ]; then cp "$3" "$D/scip.opt"; OPT="--scipopt=1"; else OPT=""; fi
(cd "$D" && $G model.gms lo=3 $OPT > run.log 2>&1)
cat "$D/run.log" > "$(dirname "$0")/logs/gams_$2.log"
grep -E "^\*\*\*\* (MODEL STATUS|SOLVER STATUS|OBJECTIVE VALUE)|SCIP version|Dual Bound|Primal Bound|SCIP Status|Solving Nodes" "$D/run.log" "$D/model.lst" 2>/dev/null | sed "s|$D/||"
grep -A8 "VARIABLE obj.L\|----.*VARIABLE" "$D/model.lst" 2>/dev/null | head -0
rm -rf "$D"
