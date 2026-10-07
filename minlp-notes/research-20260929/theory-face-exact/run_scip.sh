#!/bin/bash
# Runs every line of scip_jobs.txt as "python3 scip_runs.py <line>", 6 in parallel.
cd "$(dirname "$0")"
xargs -P 6 -L 1 -I{} sh -c 'python3 scip_runs.py {} 2>&1' < scip_jobs.txt | grep -v '^$' > logs/scip_runs.log
