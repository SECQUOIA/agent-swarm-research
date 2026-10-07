#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Sandboxed audit run: the main tree AND the clean worktree are hidden (bwrap tmpfs), so the
# command can only see the patched clean copy in $TREE, the OSIL cache and system files.
# Every file open is logged with strace (openat/open) to list the actual inputs.
# usage: run_sandboxed.sh NAME CWD_REL CMD [ARGS...]     (CWD_REL is relative to $TREE/research-20260929)
name=$1; cwdrel=$2; shift 2
TREE=/tmp/cops_patchcheck
ST=/tmp/cops_audit
L="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/cops/logs
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cwd=$TREE/research-20260929/$cwdrel
{
  echo "name: $name"
  echo "cwd: $cwd"
  printf 'cmd:'; printf ' %q' "$@"; echo
  echo "sandbox: bwrap --dev-bind / / --tmpfs "${_PUBLIC_REPO}" --tmpfs "${_PUBLIC_REPO}"-clean; strace -f --seccomp-bpf -e trace=openat,open"
  echo "start: $(date -Is)"
  echo "uptime_start: $(uptime)"
} > "$L/$name.meta"
/usr/bin/time -v -o "$L/$name.time" \
  bwrap --dev-bind / / --tmpfs "${_PUBLIC_REPO}" --tmpfs "${_PUBLIC_REPO}"-clean --chdir "$cwd" -- \
  strace -f --seccomp-bpf -e trace=openat,open -o "$ST/$name.strace" "$@" > "$L/$name.log" 2>&1
rc=$?
{
  echo "exit: $rc"
  echo "end: $(date -Is)"
  echo "uptime_end: $(uptime)"
} >> "$L/$name.meta"
exit $rc
