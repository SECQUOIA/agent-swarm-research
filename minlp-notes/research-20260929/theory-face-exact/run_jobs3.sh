#!/bin/bash
# Runs every line of jobs3.txt as "python3 bb_path.py <line>", 26 in parallel; one log line per job.
cd "$(dirname "$0")"
xargs -P 26 -L 1 -I{} sh -c 'python3 bb_path.py {} 2>&1; true' < jobs3.txt > logs/bb_runs3.log
