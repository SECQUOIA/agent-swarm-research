#!/bin/bash
# Runs every line of jobs.txt as "python3 bb_path.py <line>", 30 in parallel; one log line per job.
cd "$(dirname "$0")"
xargs -P 30 -L 1 -I{} sh -c 'python3 bb_path.py {} 2>&1' < jobs.txt > logs/bb_runs.log
