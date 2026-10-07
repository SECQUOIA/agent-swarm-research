#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
for n in $(cat "${_PUBLIC_REPO}"/research-20260929/publication/solver-runs/instances.txt); do
  code=$(curl -s -o $n.gms -w '%{http_code}' https://www.minlplib.org/gms/$n.gms)
  echo "$(date -u +%FT%TZ) $n $code"
  sleep 1
done
echo DONE
