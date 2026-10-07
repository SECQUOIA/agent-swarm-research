#!/bin/bash
# check_dump.py on every dump in logs/dumps (60 corners per file, z_K for small corners), one process.
cd $(dirname $0)
for f in ../logs/dumps/*.jsonl.gz; do
  b=$(basename $f .jsonl.gz)
  [ -s ../logs/dumps/$b.check.json ] && continue
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 900 python3 check_dump.py $f 60 40 > ../logs/dumps/$b.check.out 2>&1
  python3 - ../logs/dumps/$b.check.out ../logs/dumps/$b.check.json <<'PY'
import sys
t = open(sys.argv[1]).read()
i = t.rfind('\n{')
if i >= 0 or t.startswith('{'):
    open(sys.argv[2], 'w').write(t[i + 1:] if i >= 0 else t)
PY
done
