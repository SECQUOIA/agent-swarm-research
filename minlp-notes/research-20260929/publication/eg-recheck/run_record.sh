#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
# Re-record the eight trees of eg_disc2_s run G with the reviewer's record_run.py (unchanged).
# record_run.py replays the author's egbb.BB.run with recording lines added; the replay must
# reproduce the processed-box counts and statistics of the original logs disc2_9_p*.log.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
OUT="${_PUBLIC_REPO}"/research-20260929/publication/eg-recheck
REV="${_PUBLIC_REPO}"/research-20260929/reviews/eg-retry-review-checks
for k in 0 1 2 3 4 5 6 7; do
  timeout 30000 python3 $REV/record_run.py eg_disc2_s 1e-9 25000 $OUT/rec/rec_disc2_p$k.npz $k 8 \
      > $OUT/logs/rec_disc2_p$k.log 2>&1 &
done
wait
