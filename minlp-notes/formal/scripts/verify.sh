#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export PATH="$HOME/.elan/bin:$PATH"

# Each replay imports mathlib; a single worker keeps memory use bounded.
export LEAN_NUM_THREADS=1
python3 scripts/check_imports.py
python3 topics/03-potential-flow/generate_example.py --check
python3 topics/04-cubic-gaps/generate_large_finite.py --check
lake build --wfail
lake env lean Verify.lean
lake env leanchecker -v Formal
printf '%s\n' 'PASS: build, axiom audit, module coverage, and kernel replay.'
