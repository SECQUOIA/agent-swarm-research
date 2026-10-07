#!/bin/bash
# Runs every line of jobs2.txt as "python3 bb_path.py <line>", 24 in parallel; one log line per job.
cd "$(dirname "$0")"
xargs -P 24 -L 1 -I{} sh -c 'python3 bb_path.py {} 2>&1' < jobs2.txt > logs/bb_runs2.log
