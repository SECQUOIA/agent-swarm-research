#!/bin/sh
_PUBLIC_REPO="$(cd -- "$(dirname -- "$0")/../../../../.." && pwd)"
# Re-run the r2 dossier checks in a fresh temporary directory (copies only; nothing in the main tree is executed).
# Usage: sh run.sh   (single-threaded; about 5 minutes, dominated by gibbs_cert.py)
# gibbs_check.py and gibbs_cert.py read the verifier's saved multipliers (JSON) from $R read-only.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
R="${_PUBLIC_REPO}"/research-20260929
W=$(mktemp -d /tmp/smallchk-r2-XXXXXX)
cp "$HERE"/*.py "$W"/
mkdir -p "$W/gmscheck/gms"
cp "$HERE"/gmscheck/gms_vs_osil.py "$HERE"/gmscheck/osil_own.py "$W/gmscheck/"
for f in hvycrash ex6_2_5 ex6_2_7 etamac pricing050 pindyck; do cp "$R/publication/solver-runs/gms/$f.gms" "$W/gmscheck/gms/"; cp ~/.cache/minlplib/minlplib/osil/$f.osil "$W/gmscheck/"; done
for f in hvycrash ex6_2_5 ex6_2_7 etamac pricing050 pindyck; do cp ~/.cache/minlplib/minlplib/osil/$f.osil "$W"/; done
cp "$R/open-instances-wave2/small/logs/pricing050_primal.txt" "$R/open-instances-wave2/small/logs/etamac_primal.txt" "$W"/
cp "$R/reviews/pindyck-review-checks/logs/primal_enclosure.txt" "$W"/
cd "$W"
export OMP_NUM_THREADS=1
python3 hvy_check.py > hvy_check.log 2>&1
python3 gibbs_check.py > gibbs_check.log 2>&1
python3 gibbs_deriv_check.py ex6_2_7 > gibbs_deriv_check.log 2>&1
python3 gibbs_deriv_check.py ex6_2_5 >> gibbs_deriv_check.log 2>&1
python3 gibbs_cert.py ex6_2_7 > gibbs_cert_ex6_2_7.log 2>&1
python3 gibbs_cert.py ex6_2_5 > gibbs_cert_ex6_2_5.log 2>&1
python3 etamac_point.py > etamac_point.log 2>&1
python3 pricing_check.py > pricing_check.log 2>&1
python3 pindyck_sc.py > pindyck_sc.log 2>&1
(cd gmscheck && python3 gms_vs_osil.py > gms_vs_osil.log 2>&1)
echo "logs in $W"
