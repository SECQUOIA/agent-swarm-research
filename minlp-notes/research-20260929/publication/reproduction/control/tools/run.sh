#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Run one reproduction command in the clean worktree, measured and sandboxed.
# usage: run.sh ID CWD CMD [ARGS...]
#   - bubblewrap hides the main working tree (/workspace/minlp-notes) behind an
#     empty tmpfs, so a script that still refers to it fails instead of silently using it;
#   - /usr/bin/time -v measures wall time, CPU time and peak RSS (of bwrap and all its
#     descendants: rusage of waited-for children; peak RSS is the largest single process);
#   - one BLAS/OpenMP thread; load average recorded at start and end.
set -u
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/control
ID=$1; CWD=$2; shift 2
L=$OUT/logs/$ID
{
  echo "id: $ID"
  echo "cwd: $CWD"
  printf 'cmd:'; printf ' %q' "$@"; echo
  echo "start_utc: $(date -u +%FT%TZ)"
  echo "uptime_start: $(uptime)"
} > "$L.meta"
/usr/bin/time -v -o "$L.time" \
  bwrap --dev-bind / / --tmpfs "${_PUBLIC_REPO}" --chdir "$CWD" \
    --setenv OMP_NUM_THREADS 1 --setenv OPENBLAS_NUM_THREADS 1 --setenv MKL_NUM_THREADS 1 \
    --setenv PYTHONUNBUFFERED 1 \
    -- "$@" > "$L.out" 2>&1
rc=$?
{
  echo "exit: $rc"
  echo "end_utc: $(date -u +%FT%TZ)"
  echo "uptime_end: $(uptime)"
} >> "$L.meta"
exit $rc
