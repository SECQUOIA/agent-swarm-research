#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Verifier runner: run one command inside /tmp/rcv_r1/tree with the main tree AND the clean
# worktree hidden (bwrap tmpfs), under /usr/bin/time -v, recording uptime at start/end.
# usage: vrun.sh NAME CWD_REL CMD [ARGS...]   (CWD_REL relative to /tmp/rcv_r1/tree/research-20260929)
name=$1; cwdrel=$2; shift 2
L="${_PUBLIC_REPO}"/research-20260929/publication/reviews/repro-cops-r1/logs
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cwd=/tmp/rcv_r1/tree/research-20260929/$cwdrel
{ echo "name: $name"; echo "cwd: $cwd"; printf 'cmd:'; printf ' %q' "$@"; echo
  echo "start: $(date -Is)"; echo "uptime_start: $(uptime)"; } > "$L/$name.meta"
/usr/bin/time -v -o "$L/$name.time" bwrap --dev-bind / / --tmpfs "${_PUBLIC_REPO}" \
  --tmpfs "${_PUBLIC_REPO}"-clean --chdir "$cwd" -- "$@" > "$L/$name.log" 2>&1
rc=$?
{ echo "exit: $rc"; echo "end: $(date -Is)"; echo "uptime_end: $(uptime)"; } >> "$L/$name.meta"
exit $rc
