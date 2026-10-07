#!/bin/bash
# Index all dumps (8 parallel processes, 1 h wall-clock limit per dump). Writes logs/index/<set>__<inst>.jsonl.
cd "$(dirname "$0")"
for d in runs_mc11 runs_mc12 runs_minlplib; do
  for f in ../logs/$d/*.jsonl.gz; do
    n=$(basename $f .jsonl.gz); o=../logs/index/${d#runs_}__$n.jsonl
    [ -s $o ] && continue          # checkpoint: skip finished dumps
    echo "$f $o"
  done
done | xargs -P 8 -n 2 sh -c 'OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 3600 python3 index_dumps.py $1.tmp $0 && mv $1.tmp $1' 
echo INDEXDONE
