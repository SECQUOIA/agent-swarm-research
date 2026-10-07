#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Queue line format: NAME<TAB>CWD_REL<TAB>COMMAND (COMMAND split by bash word splitting).
S="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/cops/scripts
while IFS=$'\t' read -r name cwd cmd; do
  [ -z "$name" ] && continue
  case "$name" in \#*) continue;; esac
  echo "$(date -Is) start $name"
  # shellcheck disable=SC2086
  "$S/run_sandboxed.sh" "$name" "$cwd" $cmd
  rc=$?
  echo "$(date -Is) done $name exit=$rc"
done < "$1"
