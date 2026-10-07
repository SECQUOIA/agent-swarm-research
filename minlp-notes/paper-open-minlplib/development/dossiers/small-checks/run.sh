#!/bin/sh
# Re-run the small-family dossier checks in a fresh temporary directory (reads inputs, writes nothing in the tree).
# Usage: sh run.sh   (from any directory; needs python3 with mpmath and sympy)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$HERE/../../../../research-20260929" && pwd)
W=$(mktemp -d /tmp/small-checks.XXXXXX)
cp "$HERE"/*.py "$W"/
for n in hvycrash ex6_2_5 ex6_2_7 etamac pricing050 pindyck; do cp "$HOME/.cache/minlplib/minlplib/osil/$n.osil" "$W"/; done
mkdir -p "$W/gms"
for n in hvycrash ex6_2_5 ex6_2_7 etamac pricing050 pindyck; do cp "$R/publication/solver-runs/gms/$n.gms" "$W/gms/"; done
cp "$R/reviews/wave2-small-verification/logs/ex6_2_7_bound.json" "$R/reviews/wave2-small-verification/logs/ex6_2_5_bound.json" \
   "$R/reviews/wave2-small-verification/sol/etamac.p1.sol" \
   "$R/open-instances-wave2/small/logs/pindyck_primal.txt" "$R/open-instances-wave2/small/logs/pricing050_primal.txt" "$W"/
cd "$W"
for s in hvy_analytic pricing_check gibbs_assembly etamac_check pindyck_hess_sym own_osil_checks gms_vs_osil; do
  echo "== $s"; OMP_NUM_THREADS=1 python3 "$s.py" > "$s.log" 2>&1; tail -n 3 "$s.log"
done
echo "outputs in $W"
