#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Chain A: documented period-Lagrangian certificate command for each waterno2 size,
# run in the clean worktree with the main tree hidden. 3 rbb/SCIP workers.
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/water-audit
W="${_PUBLIC_REPO}"-clean/research-20260929/open-instances-wave2/waterno2
for TT in ${@:-06 09 12 18 24}; do
  T=$((10#$TT))
  $OUT/tools/run.sh w${TT}_certify "$W" clean \
    "WATERNO2_IMPLIED=logs/implied_${TT}.json python3 certify.py $T logs/mult_${TT}_w1_impl.json 1 logs/repro_cert_${TT}_w1_impl.json 3 300000 3600"
done
