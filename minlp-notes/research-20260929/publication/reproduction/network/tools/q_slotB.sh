#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Sequential queue for the second CPU slot: KAN, powerflow, ANN primal checks.
# Waits until the ANN run-1 replay (python PID given as $1) has exited.
R="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/network/tools/run.sh
W="${_PUBLIC_REPO}"-clean/research-20260929
S="${_PUBLIC_REPO}"-clean/scratch-repro-network
while kill -0 "$1" 2>/dev/null; do sleep 15; done
K=(kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9 kan_r5_h1_n3 kan_r5_h1_n5 kan_r5_h1_n8)
# ---- KAN: certificate runs (authors), checks, verifier, primal points
for n in kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9; do $R kan.run_kan.$n $W/open-instances-wave3/kan python3 -u run_kan.py $n 1e-10 1800; done
for n in kan_r5_h1_n3 kan_r5_h1_n5 kan_r5_h1_n8; do $R kan.run_kan.$n $W/open-instances-wave3/kan python3 -u run_kan.py $n 1e-10 7200; done
for n in "${K[@]}"; do $R kan.check_random.$n $W/open-instances-wave3/kan python3 -u kan_check.py $n random; done
$R kan.summary $W/open-instances-wave3/kan python3 -u kan_summary.py
for n in "${K[@]}"; do $R kan.verifier_bnb.$n $W/reviews/wave3-verification python3 -u kan_bnb.py $n 4e-11 1800 1024; done
for n in "${K[@]}"; do $R kan.verifier_infeas.$n $W/reviews/wave3-verification python3 -u kan_infeas_cert.py $n; done
for n in "${K[@]}"; do $R kan.verifier_primal.$n $W/reviews/wave3-verification python3 -u kan_primal.py $n $W/open-instances-wave3/sol/$n.wave3.sol; done
for n in "${K[@]}"; do $R kan.nn_exact.$n $W/publication/primal/water-ann-kan/code python3 -u nn_exact.py $n; done
for n in "${K[@]}"; do $R kan.check_nn_point.$n $W/publication/primal/water-ann-kan/code python3 -u check_nn_point.py ../points/$n.point.json; done
for n in "${K[@]}"; do $R kan.rev_nn.$n $W/publication/reviews/primal-water-ann-kan-r1 python3 -u rev_nn.py $n; done
# ---- powerflow0030p: SDP/Lagrangian certificate
$R pf.verifier_root_stored.powerflow0030p $W/reviews/wave3-verification/powerflow python3 -u run_root.py powerflow0030p
$R pf.pf_cert.powerflow0030p $W/open-instances-wave3/powerflow python3 -u pf_cert.py powerflow0030p
$R pf.verifier_root_regen.powerflow0030p $W/reviews/wave3-verification/powerflow python3 -u run_root.py powerflow0030p
$R pf.pf_check.powerflow0030p $W/open-instances-wave3/powerflow python3 -u pf_check.py powerflow0030p
# ---- powerflow0039p/r: leaf branch and bound (tight run), new tag bb3t_repro keeps the stored bb3t files
$R pf.bb3.powerflow0039p $W/open-instances-wave3/powerflow/ext python3 -u pf_bb3.py powerflow0039p 2400 41869.0515113202 1/10000 1e-10 bb3t_repro
$R pf.bb3.powerflow0039r $W/open-instances-wave3/powerflow/ext python3 -u pf_bb3.py powerflow0039r 2400 41869.0515113208 1/10000 1e-10 bb3t_repro
for n in powerflow0039p powerflow0039r; do for t in bb3t bb3t_repro; do
  $R pf.verify_bb3.$n.$t $W/open-instances-wave3/powerflow/ext python3 -u verify_bb3.py $n $t
  $R pf.verify_exact.$n.$t $W/open-instances-wave3/powerflow/ext python3 -u verify_exact.py $n $t
  $R pf.verifier_leaves.$n.$t $W/reviews/powerflow0039-review-checks python3 -u verify_leaves.py $n $t
done; $R pf.verifier_p1.$n $W/reviews/powerflow0039-review-checks python3 -u p1_check.py $n bb3t bb3t_repro; done
$R pf.verifier_cmp_rows $W/reviews/powerflow0039-review-checks python3 -u cmp_rows.py powerflow0039p powerflow0039r
$R pf.verifier_leaf_struct $W/reviews/powerflow0039-review-checks python3 -u leaf_struct.py powerflow0039p powerflow0039r
# ---- powerflow exactly feasible points: stored certificate, independent check, then regeneration
P=$W/publication/primal/powerflow
for n in powerflow0030p powerflow0039p powerflow0039r; do
  $R pf.primal_certify.$n $P python3 -u certify.py $n
  $R pf.primal_certify_r1e-30.$n $P python3 -u certify.py $n 1e-30
  $R pf.primal_scip_check.$n $P python3 -u scip_check.py $n
  $R pf.primal_reviewer_verify.$n $W/publication/reviews/primal-powerflow-r1 python3 -u verify.py $n
  [ $n = powerflow0030p ] && $R pf.primal_reviewer_verify_r1e-30.$n $W/publication/reviews/primal-powerflow-r1 python3 -u verify.py $n 1e-30
  cp $P/points/$n.json $S/$n.stored.json
  $R pf.primal_construct.$n $P python3 -u construct.py $n
  cp $P/points/$n.json $S/$n.regen.json
  $R pf.primal_certify_regen.$n $P python3 -u certify.py $n
  cp $S/$n.stored.json $P/points/$n.json
done
# ---- ann_cumene_tanh primal point
$R ann.ann_point $W/open-instances-wave3/ann python3 -u ann_point.py 370.9280572920674 0.7863373968889928 1.620252679906157 0.9494678019619749 0.734065236105183
$R ann.verifier_points $W/reviews/wave3-verification/ann python3 -u annv.py points
$R ann.nn_exact $W/publication/primal/water-ann-kan/code python3 -u nn_exact.py ann_cumene_tanh
$R ann.check_nn_point $W/publication/primal/water-ann-kan/code python3 -u check_nn_point.py ../points/ann_cumene_tanh.point.json
$R ann.rev_nn $W/publication/reviews/primal-water-ann-kan-r1 python3 -u rev_nn.py ann_cumene_tanh
$R gaps $W/publication/primal/water-ann-kan/code python3 -u gaps.py
echo "slotB queue done $(date -Is)"
