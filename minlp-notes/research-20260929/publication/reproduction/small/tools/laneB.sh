#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Lane B: the eg review chain (decoding check, tree recordings, independent leaf certification).
R="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/small/tools/run_step.sh
C="${_PUBLIC_REPO}"-clean/research-20260929
RV=$C/reviews/eg-retry-review-checks
echo "lane B start $(date -Is)"
$R B01_rv_check_decode   $RV "timeout 3600 python3 check_decode.py"
$R B02_rv_rec_int        $RV "timeout 4000 python3 record_run.py eg_int_s 1e-9 3600 logs/rec_int.npz"
$R B03_rv_verify_int     $RV "timeout 7200 python3 verify_tree.py logs/rec_int.npz eg_int_s 6.4531031529331155 1.0"
$R B04_rv_rec_disc_p0    $RV "timeout 6000 python3 record_run.py eg_disc_s 1e-9 5400 logs/rec_disc_p0.npz 0 2"
$R B05_rv_verify_disc_p0 $RV "timeout 7200 python3 verify_tree.py logs/rec_disc_p0.npz eg_disc_s 5.760539610694994 1.0"
$R B06_rv_rec_disc_p1    $RV "timeout 6000 python3 record_run.py eg_disc_s 1e-9 5400 logs/rec_disc_p1.npz 1 2"
$R B07_rv_verify_disc_p1 $RV "timeout 7200 python3 verify_tree.py logs/rec_disc_p1.npz eg_disc_s 5.760539610694994 1.0"
$R B08_rv_rec_disc2_p1   $RV "timeout 7200 python3 record_run.py eg_disc2_s 1e-9 7000 logs/rec_disc2_p1.npz 1 8"
$R B09_rv_verify_disc2_p1 $RV "timeout 9000 python3 verify_tree.py logs/rec_disc2_p1.npz eg_disc2_s 5.642100574331458 1.0"
echo "lane B end $(date -Is)"
