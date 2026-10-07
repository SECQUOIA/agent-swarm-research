#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Run the jobs of a queue file one after another (one process slot).
# Queue line format: NAME<TAB>CWD<TAB>COMMAND (COMMAND is split by bash word splitting).
S="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/cops/scripts
while IFS=$'\t' read -r name cwd cmd; do
  [ -z "$name" ] && continue
  case "$name" in \#*) continue;; esac
  echo "$(date -Is) start $name"
  # shellcheck disable=SC2086
  "$S/run_measured.sh" "$name" "$cwd" $cmd
  rc=$?
  echo "$(date -Is) done $name exit=$rc"
done < "$1"
