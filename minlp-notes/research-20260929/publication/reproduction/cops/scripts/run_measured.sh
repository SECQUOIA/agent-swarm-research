#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Run one command with /usr/bin/time -v and record load before/after.
# usage: run_measured.sh NAME CWD CMD [ARGS...]
# Writes logs/NAME.log (stdout+stderr), logs/NAME.time (time -v), logs/NAME.meta.
name=$1; cwd=$2; shift 2
L="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/cops/logs
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cd "$cwd" || { echo "cannot cd $cwd" > "$L/$name.meta"; exit 99; }
{
  echo "name: $name"
  echo "cwd: $cwd"
  printf 'cmd:'; printf ' %q' "$@"; echo
  echo "env: OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1"
  echo "start: $(date -Is)"
  echo "uptime_start: $(uptime)"
} > "$L/$name.meta"
/usr/bin/time -v -o "$L/$name.time" "$@" > "$L/$name.log" 2>&1
rc=$?
{
  echo "exit: $rc"
  echo "end: $(date -Is)"
  echo "uptime_end: $(uptime)"
} >> "$L/$name.meta"
exit $rc
