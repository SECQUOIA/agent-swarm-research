#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export PATH="$HOME/.elan/bin:$PATH"
export LEAN_NUM_THREADS=1
python3 scripts/check_imports.py
lake build --wfail
lake env lean Verify.lean
lake env leanchecker -v CertifiedMinlp
printf '%s\n' 'PASS: build, axiom audit, module coverage, and kernel replay.'
