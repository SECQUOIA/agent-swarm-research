#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export LEAN_NUM_THREADS=1
python3 scripts/check_imports.py
lake build Formal --wfail
lake env lean Verify.lean
lake env leanchecker -v Formal
printf '%s\n' 'PASS: isolated bundle build, import coverage, axiom audit, and kernel replay.'
