#!/bin/bash
# Verifier: convert a GAMS file to OSiL and scalar GAMS with GAMS 54.3 Convert.
# usage: conv.sh SRC.gms OUTDIR NAME
set -e
G="${HOME}"/.local/opt/gams/gams54.3_linux_x64_64_sfx/gams
mkdir -p "$2"; cp "$1" "$2/$3.gms"; cd "$2"
printf 'OSiL out.osil\nGams scalar.gms\n' > convert.opt
$G "$3.gms" solver=convert optfile=1 lo=2 o=out.lst > /dev/null 2>&1 || echo "GAMS rc=$?"
ls -la out.osil scalar.gms 2>&1 | awk '{print $5, $9}'
