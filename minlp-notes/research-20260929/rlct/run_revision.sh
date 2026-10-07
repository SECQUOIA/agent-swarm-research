#!/bin/bash
# Bisection runs for the revision after review; output logs/revision_sweep.jsonl.
cd "$(dirname "$0")"
gen() { for k in $(seq $2 $3); do python3 -c "print('$1', '%.8g' % 10**(-$k/$4), '$5')"; done; }
{
gen vsharp 2 15 1 1; gen vsharp 2 15 1 8; gen vflat 2 15 1 1; gen rot 2 15 1 1
gen face4d 2 12 2 1.05
} | xargs -P 16 -L 1 python3 bisect_bb.py > logs/revision_sweep.jsonl
