#!/bin/sh
# Simple job queue: runs the lines of JOBFILE ("SIZE I0 I1 RULES TAG") keeping at most MAXP
# main mrloop processes (those writing to logs/main) alive.  Usage: sh run_queue.sh JOBFILE MAXP
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
while read -r s i0 i1 rules tag; do
  while [ "$(pgrep -fc 'mrloop.py .* ../logs/main/')" -ge "$2" ]; do sleep 20; done
  nohup python3 mrloop.py ../data/inst_$s.json $rules 20 ../logs/main/main_${s}_$i0$tag.jsonl $i0 $i1 > ../logs/main/main_${s}_$i0$tag.log 2>&1 &
  sleep 2
done < "$1"
wait
