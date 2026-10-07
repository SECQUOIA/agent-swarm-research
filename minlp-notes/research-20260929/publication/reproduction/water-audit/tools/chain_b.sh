#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Chain B: cheap deterministic waterno2 checks (exact DP recomputations, terminal row,
# exact sums, structure, implied bounds), one process at a time, main tree hidden.
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/water-audit
R=$OUT/tools/run.sh
WD="${_PUBLIC_REPO}"-clean/research-20260929
W=$WD/open-instances-wave2/waterno2
CS=$W/cellslopes/logs
D=$W/data
V1=$WD/reviews/waterno2-verification
RC=$WD/reviews/waterno2-recheck
SR=$WD/reviews/waterno2-sepbranch-review-checks
CR=$WD/reviews/waterno2-cellslopes-review-checks
$R w06_terminal $W/sepbranch clean "python3 terminal.py 2 3 4 6 9 12 18 24"
$R w06_cert3_verify $W/sepbranch clean "python3 verify.py logs/cert3.json"
$R w06_certB_verify $W/cellslopes clean "PYTHONPATH=../sepbranch:.. python3 verify_cs.py logs/certB_cert.pkl.gz ../logs/implied_06.json logs/repro_certB_verify.json ../data/waterno2_06.p1.sol ../data/waterno2_06.p2.sol ../data/waterno2_06.p3.sol ../data/waterno2_06.p4.sol"
$R w06_vimplied $V1 clean "python3 vimplied.py 6 2"
$R w06_ind_verify_cert3 $SR clean "python3 ind_verify.py $W/sepbranch/logs/cert3.pkl $V1/logs/my_implied_06.json logs/repro_ind_verify_cert3.json"
$R w06_terminal_allT $SR clean "python3 terminal_allT.py 2 3 4 6 9 12 18 24"
$R w06_point_check_cert3 $SR clean "python3 point_check.py $W/sepbranch/logs/cert3.pkl $D/waterno2_06.p1.sol $D/waterno2_06.p2.sol $D/waterno2_06.p3.sol $D/waterno2_06.p4.sol"
$R w06_ind_verify_certB $CR clean "python3 ind_verify_cs.py $CS/certB_cert.pkl.gz logs/repro_ind_verify_certB.json $CS/certB_verify.json"
$R w06_point_check_certB $CR clean "python3 point_check_cs.py $CS/certB_cert.pkl.gz logs/repro_ind_verify_certB.json $D/waterno2_06.p4.sol $D/waterno2_06.p3.sol $D/waterno2_06.p2.sol $D/waterno2_06.p1.sol"
$R wall_vstruct $V1 clean "python3 vstruct.py 1 2 3 4 6 9 12 18 24"
$R wall_vsum $V1 clean "python3 vsum.py 6 9 12 18 24"
$R wall_vsum2 $RC clean "python3 vsum2.py 9 12 18 24"
for TT in 06 09 12 18 24; do
  $R w${TT}_implied $W clean "python3 implied.py $((10#$TT)) logs/repro_implied_${TT}.json 2"
done
for TT in 09 12 18 24; do
  $R w${TT}_vimplied2 $RC clean "python3 vimplied2.py $((10#$TT)) 2"
done
$R wall_evalpt_listed $W clean "python3 evalpt.py 6 data/waterno2_06.p1.sol data/waterno2_06.p2.sol data/waterno2_06.p3.sol data/waterno2_06.p4.sol"
for TT in 09 12 18 24; do
  $R w${TT}_veval_primal $V1 clean "python3 veval.py $((10#$TT)) $W/logs/primal_${TT}_w2.json"
done
