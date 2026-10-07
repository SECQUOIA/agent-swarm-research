#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
# Triple-level audits of B on the spar instances whose base relative gap exceeds 1e-6
# (spar050-050-1 and spar080-050-1 were audited earlier with triple_audit.py; spar040-050-2 by hand).
# At most 5 parallel processes; wall-clock limit 6 h per instance; resumable (checkpoints).
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
for t in spar125-075-2 spar125-050-1 spar125-075-3 spar125-025-1 spar125-050-2 spar125-050-3 \
         spar100-050-1 spar100-075-2 spar100-050-2 spar100-075-1 spar090-075-2 spar090-075-1 \
         spar050-030-3 spar050-050-3; do
  if [ ! -e ../logs/spar_audit/$t.json ]; then echo $t; fi
done | OMP_NUM_THREADS=1 xargs -P 5 -I{} sh -c "timeout 21600 python spar_audit.py {} ../logs/spar_audit/{}.json > ../logs/spar_audit/{}.out 2>&1"
