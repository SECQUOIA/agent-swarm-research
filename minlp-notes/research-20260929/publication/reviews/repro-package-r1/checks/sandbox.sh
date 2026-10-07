#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Usage: sandbox.sh <tree> <cwd> cmd...   (main repo, clean worktree, earlier smoke copy and real OSIL cache hidden)
T=$1; shift; CWD=$1; shift
ROOT="${_PUBLIC_REPO}"
CACHE=$HOME/.cache/minlplib
args=(bwrap --dev-bind / / --tmpfs "$ROOT")
[ -d "${_PUBLIC_REPO}"-clean ] && args+=(--tmpfs "${_PUBLIC_REPO}"-clean)
[ -d /tmp/repro-smoke-qg8quuvd ] && args+=(--tmpfs /tmp/repro-smoke-qg8quuvd)
args+=(--tmpfs "$CACHE" --ro-bind "$T/osil" "$CACHE/minlplib/osil")
for k in OMP_NUM_THREADS OPENBLAS_NUM_THREADS MKL_NUM_THREADS RAYON_NUM_THREADS; do args+=(--setenv $k 1); done
args+=(--setenv PYTHONDONTWRITEBYTECODE 1 --chdir "$CWD" --)
exec "${args[@]}" "$@"
