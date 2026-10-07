#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
while pgrep -f "queue_driver.txt" > /dev/null; do sleep 15; done
./run_queue.sh ../data/tmp/queue_chain_audit.txt 3
python make_ub_queue.py
./run_queue.sh ../data/tmp/queue_ub.txt 3
