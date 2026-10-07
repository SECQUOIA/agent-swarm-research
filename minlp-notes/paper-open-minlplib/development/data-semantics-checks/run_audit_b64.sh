#!/bin/bash
# Re-run the class (i) point certificates and the rocket proofs with the OSIL data rounded to
# binary64 (reading (c)). Works only on /tmp copies; nothing in the repository is modified.
# usage: bash run_audit_b64.sh <repo-root> <scratch-dir> <log-dir>
set -e
REPO=$1; W=$2; L=$3; HERE=$(cd "$(dirname "$0")" && pwd)
R=$REPO/research-20260929; D=$REPO/paper-open-minlplib/development/dossiers/checks/audit-r2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
rm -rf "$W"; mkdir -p "$W/bound-audit/sol" "$W/bound-audit/logs/verify" "$W/reviews/open-instances-verification" "$W/rk/data" "$L"
cp "$R"/bound-audit/{audit_eval.py,verify.py,verify_one.py,cert_linear.py,cert_ndnetgen.py,cert_topopt.py} "$W/bound-audit/"
cp "$R"/bound-audit/sol/*.sol "$W/bound-audit/sol/"
cp "$R/reviews/open-instances-verification/osilx.py" "$W/reviews/open-instances-verification/osilx_orig.py"
cp "$HERE/osilx_b64_wrapper.py" "$W/reviews/open-instances-verification/osilx.py"
cd "$W/bound-audit"
for t in smallinvDAXr1b150-165.p2 smallinvDAXr2b150-165.p2 smallinvDAXr1b200-220.p2 smallinvDAXr2b200-220.p2 \
         ghg_3veh.p2 glider100.p2 methanol50.p4 nuclear14.p3 sssd20-04persp.p3 sssd22-08persp.p4 \
         sssd25-04persp.p3 sssd25-08persp.p4; do
  python3 verify_one.py $t > "$L/b64_verify_$t.log" 2>&1; tail -1 "$L/b64_verify_$t.log"
done
python3 cert_linear.py watercontamination0303.p2 > "$L/b64_cert_linear_watercontamination0303.p2.log" 2>&1
python3 cert_ndnetgen.py nd_netgen-2000-3-4-b-a-ns_7.p2 > "$L/b64_cert_ndnetgen.p2.log" 2>&1
for p in p5 p4; do python3 cert_topopt.py topopt-cantilever_60x40_50.$p > "$L/b64_cert_topopt.$p.log" 2>&1; done
cd "$W/rk"
cp "$D/rocket_kraw.py" .; cp "$R"/reviews/bound-audit-verification/{osil.py,kraw.py,ivl.py,ad.py} .
for n in 100 200 400; do cp ~/.cache/minlplib/minlplib/osil/rocket$n.osil data/; cp "$R/open-instances-wave2/small/logs/rocket$n.conopt.polished.txt" data/; done
python3 "$HERE/rocket_b64.patch.py"
for n in 100 200 400; do python3 rocket_kraw.py $n > "$L/b64_rocket_kraw_$n.log" 2>&1; done
echo done
