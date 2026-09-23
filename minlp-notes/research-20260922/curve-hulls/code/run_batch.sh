#!/bin/sh
# usage: sh run_batch.sh <jobs file> <time limit> <parallel>
# each line: <instance> <mode> [extra args]; output results/<instance>_<mode>[_pb]_<tl>.json
cd "$(dirname "$0")"
PY=~/miniconda3/envs/exact-quadratic-hull/bin/python
TL=$2
grep -v '^#' "$1" | xargs -P "$3" -L 1 sh -c '
  tag="$0_$1"; case "$*" in *--pbounds*) tag="${tag}_pb";; esac
  '"$PY"' run.py "$0" "$@" --tl '"$TL"' > "results/${tag}_'"$TL"'.out" 2> "logs/${tag}_'"$TL"'.err"'
