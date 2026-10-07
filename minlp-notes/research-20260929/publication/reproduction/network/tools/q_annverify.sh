#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# ANN aggregation and independent re-certification of the replayed regions.
# $1 = python PID of the run-2 replay, $2 = PID of the slot-B queue.
R="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/network/tools/run.sh
W="${_PUBLIC_REPO}"-clean/research-20260929
S="${_PUBLIC_REPO}"-clean/scratch-repro-network
C=$W/reviews/ann-extension-review-checks
L=-3386.5402291369187
while kill -0 "$1" 2>/dev/null; do sleep 15; done
$R ann.leaves_extract_run1 $C python3 -u leaves.py extract $S/replay_run1.npz $S/regions_run1.npz
$R ann.leaves_extract_run2 $C python3 -u leaves.py extract $S/replay_run2.npz $S/regions_run2.npz
$R ann.leaves_check $C python3 -u leaves.py $S/replay_run1.npz $S/replay_run2.npz $S/leaves_all.npz 2000
np() { if kill -0 "$1" 2>/dev/null; then echo 1; else echo 2; fi; }
n=$(np $2); $R ann.verify_regions_run1.p$n $C python3 -u verify_boxes.py $S/regions_run1.npz $S/ver_regions_run1.npz $L $n
n=$(np $2); $R ann.verify_open_run2.p$n $C python3 -u verify_boxes.py $S/replay_run2.npz $S/ver_open_run2.npz $L $n
while kill -0 "$2" 2>/dev/null; do sleep 15; done
$R ann.verify_regions_run2.p2 $C python3 -u verify_boxes.py $S/regions_run2.npz $S/ver_regions_run2.npz $L 2
echo "annverify queue done $(date -Is)"
