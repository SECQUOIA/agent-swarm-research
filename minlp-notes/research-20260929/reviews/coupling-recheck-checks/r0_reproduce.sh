#!/usr/bin/env bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
# Rerun the author's summary scripts (theory-coupling/) and two review checks
# into a scratch directory and diff their output with the saved logs.
# Nothing in theory-coupling/ or coupling-review-checks/ is written.
# Usage: bash r0_reproduce.sh
set -u
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
TC="${_PUBLIC_REPO}"/research-20260929/theory-coupling
RC="${_PUBLIC_REPO}"/research-20260929/reviews/coupling-review-checks
TMP=$(mktemp -d)
check() {  # dir, command, saved log
  (cd "$1" && timeout 1200 $2 > "$TMP/out.log" 2>&1)
  if diff -q "$TMP/out.log" "$3" > /dev/null; then r=identical; else r=DIFFERENT; fi
  echo "$2 vs ${3#${_PUBLIC_REPO}/research-20260929/}: $r"
}
check "$TC" "python3 census_k_analyze.py" "$TC/logs/census_k_summary.log"
check "$TC" "python3 census_k_rows.py" "$TC/logs/census_k_rows.log"
check "$TC" "python3 jeroslow_bb.py" "$TC/logs/jeroslow_bb.log"
check "$TC" "python3 jn_lifted_cert.py" "$TC/logs/jn_lifted_cert.log"
check "$RC" "python3 c1_jeroslow.py" "$RC/logs/c1_jeroslow.log"
check "$RC" "python3 c2_min_tree.py" "$RC/logs/c2_min_tree.log"
rm -rf "$TMP"
