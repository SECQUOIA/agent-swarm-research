#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
# Run a queue file of shell commands with at most P parallel processes (single-threaded BLAS).
# Usage: run_queue.sh queuefile P
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 xargs -P $2 -I{} sh -c "{}" < $1
