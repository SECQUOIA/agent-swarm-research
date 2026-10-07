#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../../../../.." && pwd)"
# Review r2: rerun the stream's key certificate checks (stream code run unchanged from code/), and the r1 reviewer's
# independent box verifier on the rerun box file; at most 3 processes at a time, each with a timeout.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
C="${_PUBLIC_REPO}"/research-20261001/ratio-bound/code
R1="${_PUBLIC_REPO}"/research-20261001/ratio-bound/reviews/r1-code
O="${_PUBLIC_REPO}"/research-20261001/ratio-bound/reviews/r2-logs/rerun_stream
Z="${_PUBLIC_REPO}"/research-20261001/ratio-bound/logs
run() { name=$1; dir=$2; shift 2
  while [ $(jobs -r | wc -l) -ge 3 ]; do sleep 2; done
  ( cd $dir && /usr/bin/time -f "elapsed %e s" timeout 1500 "$@" > $O/$name.out 2>&1; echo "exit $?" >> $O/$name.out ) &
}
run lower_found $C python3 certify_lower_found.py
run adv3_191_6250 $C python3 certify_adv3_upper.py 191/6250
run adv3_default $C python3 certify_adv3_upper.py
run verify_rho137_rerun $C python3 verify_zB.py $Z/rev1/leaves_rho137_rerun.jsonl.gz 137
run r1indep_rho137_rerun $R1 python3 indep_verify_boxes.py $Z/rev1/leaves_rho137_rerun.jsonl.gz 137 B
run verify_tan_k49_25 $C python3 verify_zB.py $Z/zB_cert/leaves_tan_eta1e-3_k49_25_rho11_10.jsonl.gz 11/10 tan:1/1000:49/25
run zB_lower $C python3 certify_zB_lower.py
run sharpA $C python3 certify_sharpA.py
run support_one $C python3 certify_support_one.py
run scip_kD $C python3 scip_kD_family.py
wait
echo ALL_RERUNS_DONE > $O/DONE
