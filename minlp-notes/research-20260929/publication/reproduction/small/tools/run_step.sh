#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Run one reproduction step and record its resources and the machine load.
#   run_step.sh ID CWD CMD...
# Writes logs/ID.meta (cwd, command, start/end time, uptime and /proc/loadavg at start and end,
# exit code), logs/ID.out (stdout+stderr), logs/ID.time (/usr/bin/time -v) and, if the clean
# checkout guard saw an access to the main tree, logs/ID.guard.
# Environment: single-threaded BLAS, no bytecode files, the guard (strict unless
# REPRO_GUARD_MODE=log) loaded from a copy outside the main tree.
ID=$1; CWD=$2; shift 2
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/small/logs
G=/tmp/repro_small_guard
mkdir -p "$G"
cp "${_PUBLIC_REPO}"/research-20260929/publication/reproduction/small/guard/usercustomize.py "$G/"
rm -f "$G/access_$ID.log"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$G" REPRO_GUARD_LOG="$G/access_$ID.log" REPRO_GUARD_MODE="${REPRO_GUARD_MODE:-strict}"
{
  echo "id: $ID"
  echo "cwd: $CWD"
  echo "cmd: $*"
  echo "guard_mode: $REPRO_GUARD_MODE"
  echo "start: $(date -Is)"
  echo "uptime_start: $(uptime)"
  echo "loadavg_start: $(cat /proc/loadavg)"
} > "$OUT/$ID.meta"
cd "$CWD" || { echo "rc: 127 (cd failed)" >> "$OUT/$ID.meta"; exit 127; }
/usr/bin/time -v -o "$OUT/$ID.time" bash -c "$*" > "$OUT/$ID.out" 2>&1
rc=$?
{
  echo "rc: $rc"
  echo "end: $(date -Is)"
  echo "uptime_end: $(uptime)"
  echo "loadavg_end: $(cat /proc/loadavg)"
} >> "$OUT/$ID.meta"
[ -s "$G/access_$ID.log" ] && cp "$G/access_$ID.log" "$OUT/$ID.guard"
exit $rc
