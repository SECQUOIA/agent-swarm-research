#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
# Replays the reviewers' vbb2 runs on a few saved records (dossier check, about 2 minutes on 2 cores).
# The reviewers' scripts resolve paths relative to their own location, so the needed files are copied
# into a mirror of the research-20260929 layout under the scratch directory; nothing runs in the tree.
# usage: bash replay_vbb2.sh <scratch-dir>
set -euo pipefail
R="${_PUBLIC_REPO}"/research-20260929
HERE=$(cd "$(dirname "$0")" && pwd)
W=${1:-/tmp/wn2dossier-replay}; M=$W/research-20260929
mkdir -p $M/reviews/waterno2-cellslopes-review-checks $M/reviews/waterno2-recheck/logs $M/reviews/waterno2-verification/logs \
         $M/reviews/open-instances-verification $M/open-instances-wave2/waterno2/logs
cp $R/reviews/waterno2-cellslopes-review-checks/{vrebound_cs.py,load_cs.py} $M/reviews/waterno2-cellslopes-review-checks/
cp $R/reviews/waterno2-recheck/{vbb2.py,run_period.py} $M/reviews/waterno2-recheck/
cp $R/reviews/waterno2-recheck/logs/my_implied_09.json $M/reviews/waterno2-recheck/logs/
cp $R/reviews/waterno2-verification/{vbb.py,vmodel.py,vstruct.py} $M/reviews/waterno2-verification/
cp $R/reviews/waterno2-verification/logs/my_implied_06.json $M/reviews/waterno2-verification/logs/
cp $R/reviews/open-instances-verification/osilx.py $M/reviews/open-instances-verification/
cp $R/open-instances-wave2/waterno2/logs/{mult_09_w1_impl.json,cert_09_w1_impl.json} $M/open-instances-wave2/waterno2/logs/
cp $R/open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz $W/
cp $R/reviews/waterno2-cellslopes-review-checks/logs/rebound_certB_all.jsonl.gz $R/reviews/waterno2-recheck/logs/rb_09_p06.json $W/
cp "$HERE"/replay_select.py "$HERE"/replay_compare.py $W/
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cd $W && python3 replay_select.py rebound_certB_all.jsonl.gz sel_replay.json
rm -f replay_out.jsonl
(cd $M/reviews/waterno2-cellslopes-review-checks && python3 vrebound_cs.py $W/certB_cert.pkl.gz $W/sel_replay.json $W/replay_out.jsonl 2 300)
(cd $M/reviews/waterno2-recheck && python3 run_period.py 9 6 600 logs/my_implied_09.json > $W/replay_09_p06.out)
python3 replay_compare.py rebound_certB_all.jsonl.gz replay_out.jsonl rb_09_p06.json $M/reviews/waterno2-recheck/logs/rb_09_p06.json > replay_compare.log
cat replay_compare.log
