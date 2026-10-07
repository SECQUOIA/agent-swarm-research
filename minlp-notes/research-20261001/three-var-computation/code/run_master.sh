#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
# Sequential master queue (3 parallel slots): chain audits, UB runs, small dense study, late jobs.
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
./run_queue.sh ../data/tmp/queue_chain_audit.txt 3
python make_ub_queue.py
./run_queue.sh ../data/tmp/queue_ub.txt 3
./run_queue.sh ../data/tmp/queue_small.txt 3
./run_queue.sh ../data/tmp/queue_late.txt 3
echo MASTER_DONE
