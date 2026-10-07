#!/bin/bash
# All analysis jobs with the final code: mc11 (1 job), mc12 (4 chunks), MINLPLib first sample
# (50 attempts per instance) and second sample (150 more for the instances in
# logs/second_sample_instances.txt).  8 parallel processes, 3 h limit per job, per-job checkpoints.
cd "$(dirname "$0")"
mkdir -p ../logs/an_parts ../logs/an_minlplib ../logs/an_minlplib2
ls ../logs/runs_mc12/*.jsonl.gz > /tmp/mc12files.txt
{
  [ -s ../logs/an_parts/mc11.jsonl ] || echo "full ../logs/an_parts/mc11.jsonl $(ls ../logs/runs_mc11/*.jsonl.gz | tr '\n' ' ' | sed 's/ *$//')"
  for c in 0 1 2 3; do
    [ -s ../logs/an_parts/mc12_$c.jsonl ] || echo "full ../logs/an_parts/mc12_$c.jsonl $(awk -v c=$c 'NR % 4 == c' /tmp/mc12files.txt | tr '\n' ' ' | sed 's/ *$//')"
  done
  for f in ../logs/runs_minlplib/*.jsonl.gz; do
    o=../logs/an_minlplib/$(basename $f .jsonl.gz).jsonl
    [ -s $o ] || echo "first $o $f"
  done
  for i in $(cat ../logs/second_sample_instances.txt); do
    o=../logs/an_minlplib2/$i.jsonl
    [ -s $o ] || echo "second $o ../logs/runs_minlplib/$i.jsonl.gz"
  done
} | xargs -P 8 -L 1 bash -c '
  mode=$0; o=$1; shift
  case $mode in full) opt="";; first) opt="--max-records 50";; second) opt="--second-sample 150";; esac
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 timeout 10800 python3 analyze.py $opt $o.tmp "$@" 2>/dev/null && mv $o.tmp $o || echo "FAILED $o"'
cat ../logs/an_parts/mc11.jsonl > ../logs/an_mc11.jsonl && cat ../logs/an_parts/mc12_?.jsonl > ../logs/an_mc12.jsonl
echo ALLDONE
