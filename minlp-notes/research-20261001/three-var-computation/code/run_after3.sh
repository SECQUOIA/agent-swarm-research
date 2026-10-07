#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../.." && pwd)"
cd "${_PUBLIC_REPO}"/research-20261001/three-var-computation/code
while pgrep -f "run_after2.sh" > /dev/null; do sleep 15; done
./run_queue.sh ../data/tmp/queue_late.txt 3
