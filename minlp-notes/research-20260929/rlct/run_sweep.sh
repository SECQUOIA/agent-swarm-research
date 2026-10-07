#!/bin/bash
# Bisection B&B sweep for the RLCT note (eps = 10^(-k/4)); output logs/sweep.jsonl.
cd "$(dirname "$0")"
gen() { for k in $(seq $2 $3); do python3 -c "print('$1', '%.8g' % 10**(-$k/4))"; done; }
{
gen xy2 4 32; gen sep24 4 40; gen cusp 4 36; gen xy2z4 4 24; gen bdry 4 48
gen rrr1e-2 4 36; gen rrr1e-3 4 36
} | xargs -P 16 -L 1 python3 bisect_bb.py > logs/sweep.jsonl
