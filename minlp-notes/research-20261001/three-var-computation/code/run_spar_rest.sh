#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
# Base relaxation on the remaining extended spar instances (skips instances already started).
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
for t in $(cat ../data/tmp/extended_rest.txt); do
  if [ ! -e ../logs/spar_base/$t.out ]; then echo $t; fi
done | OMP_NUM_THREADS=1 xargs -P 1 -I{} sh -c "python spar_base.py {} ../logs/spar_base/{}.json > ../logs/spar_base/{}.out 2>&1"
