#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../.." && pwd)"
# Dossier checks for the waterno2 family. Copies inputs into a scratch directory
# and runs the checks there (nothing is run inside the repository tree).
# usage: bash run_all.sh <scratch-dir>      (about 1 minute, one core)
# The vbb2 replay is separate: bash replay_vbb2.sh <scratch-dir>  (about 2 minutes, two cores)
set -euo pipefail
R="${_PUBLIC_REPO}"/research-20260929
HERE=$(cd "$(dirname "$0")" && pwd)
W=${1:-/tmp/wn2dossier-run}
mkdir -p "$W"; cd "$W"
cp "$HERE"/*.py .
for T in 02 03 04 06 09 12 18 24; do cp ~/.cache/minlplib/minlplib/osil/waterno2_$T.osil .; done
cp $R/open-instances-wave2/waterno2/cellslopes/logs/certB_cert.pkl.gz .
cp $R/reviews/waterno2-cellslopes-review-checks/load_cs.py .
cp $R/reviews/open-instances-verification/osilx.py .
cp $R/reviews/waterno2-verification/logs/my_implied_06.json .
for T in 06 09 12 18 24; do
  cp $R/publication/minlplib-status/pages/models/gms/waterno2_$T.gms .
  cp $R/open-instances-wave2/waterno2/logs/cert_${T}_w1_impl.json $R/open-instances-wave2/waterno2/logs/mult_${T}_w1_impl.json .
  cp $R/open-instances-wave2/waterno2/logs/implied_$T.json .
  cp $R/publication/primal/water-ann-kan/points/waterno2_$T.exact.json .
done
for T in 09 12 18 24; do cp $R/reviews/waterno2-recheck/logs/my_implied_$T.json .; done
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python3 terminal_check.py          > terminal_check.log
python3 wave2_sums.py              > wave2_sums.log
python3 dp_check.py certB_cert.pkl.gz > dp_check.log
python3 rootbox_check.py           > rootbox_check.log
python3 gms_mutation_control.py    > gms_vs_osil.log
for T in 06 09 12 18 24; do echo -n "T=$T: " >> gms_vs_osil.log; python3 gms_vs_osil.py waterno2_$T.gms waterno2_$T.osil >> gms_vs_osil.log; done
for M in mut_coef_09 mut_bound_09; do echo "negative control $M:" >> gms_vs_osil.log; python3 gms_vs_osil.py $M.gms waterno2_09.osil >> gms_vs_osil.log; done
python3 osilx_cmp.py               > osilx_cmp.log
python3 point_dp_check.py          > point_dp_check.log
python3 tank3_hand_bound.py        > tank3_hand_bound.log
python3 gaps.py                    > gaps.log
for T in 6 9 12 18 24; do python3 point_consistency.py $T; done > point_consistency.log
python3 binary64_residuals.py      > binary64_residuals.log
python3 data_facts.py              > data_facts.log
python3 ratios.py                  > ratios.log
tail -n 3 *.log
