#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Run one reproduction command in a clean room and record its resources.
#   run.sh TAG CWD CMD [ARGS...]
# The command runs inside bubblewrap with the main tree /workspace/minlp-notes
# hidden behind an empty tmpfs, so any leftover hard-coded path into the main tree
# fails loudly.  Threads are limited to 1.  /usr/bin/time -v measures wall time,
# CPU time and peak RSS of the whole process tree.  Output: logs/TAG.log (stdout and
# stderr), logs/TAG.time (time -v), logs/TAG.meta (command, cwd, load, exit code).
set -u
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/network/logs
tag=$1; cwd=$2; shift 2
meta=$OUT/$tag.meta
{
  echo "tag: $tag"
  echo "cwd: $cwd"
  printf 'cmd:'; printf ' %q' "$@"; echo
  echo "start: $(date -Is)"
  echo "uptime_start: $(uptime)"
} > "$meta"
cd "$cwd" || exit 99
/usr/bin/time -v -o "$OUT/$tag.time" \
  env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  bwrap --dev-bind / / --tmpfs "${_PUBLIC_REPO}" --chdir "$cwd" -- "$@" > "$OUT/$tag.log" 2>&1
rc=$?
{
  echo "exit: $rc"
  echo "end: $(date -Is)"
  echo "uptime_end: $(uptime)"
} >> "$meta"
exit $rc
