#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
Q=$1
while IFS=$'\t' read -r name cwd cmd; do
  [ -z "$name" ] && continue
  "${_PUBLIC_REPO}"/research-20260929/publication/reviews/repro-cops-r1/code/vrun.sh "$name" "$cwd" $cmd
  rc=$?
  echo "$(date -Is) $name exit=$rc"
done < "$Q"
