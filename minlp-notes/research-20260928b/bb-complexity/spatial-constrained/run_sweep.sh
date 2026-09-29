#!/bin/bash
# One process per (instance, eps); results appended as JSON lines to logs/sweep_sphere.jsonl
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
jobs=()
for inst in S2_iso S2_circ S3_iso S3_circ B2_circ B3_iso B3_circ; do
  for e in 1e-1 1e-2 1e-3 1e-4 1e-5 1e-6; do jobs+=("$inst $e"); done
done
for inst in S3_all B3_all; do
  for e in 1e-1 3e-2 1e-2 3e-3 1e-3 3e-4 1e-4; do jobs+=("$inst $e"); done
done
printf '%s\n' "${jobs[@]}" | xargs -P 30 -L 1 sh -c 'python3 sbb_sphere.py $0 $1' > logs/sweep_sphere.jsonl 2> logs/sweep_sphere.err
