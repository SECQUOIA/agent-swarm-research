#!/usr/bin/env bash
# Build + axiom audit. `lake build` kernel-checks declarations when it writes
# .olean files; Verify.lean enforces the axiom allowlist for all imported
# project declarations.
#
# Pass --replay to replay the whole import closure into a fresh environment.
# This uses Lean's own kernel, not an independently implemented verifier,
# and needs a large amount of memory, so it is off by default.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export PATH="$HOME/.elan/bin:$PATH"

if [[ $# -gt 1 || ( $# -eq 1 && "${1:-}" != "--replay" ) ]]; then
  echo "Usage: $0 [--replay]" >&2
  exit 2
fi

lake build

echo "--- axiom audit ---"
lake env lean Verify.lean

if [[ "${1:-}" == "--replay" ]]; then
  echo "--- fresh-environment kernel replay (whole import closure) ---"
  lake env leanchecker --fresh -v QipmFormal
fi
echo "PASS."
