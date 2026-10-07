#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Chain H: heavy independent checks, started after chains A and C have finished.
#  H0 regenerate the review selections and build the samples (one process)
#  H1 69 period jobs (vbb2 for waterno2_09-24, vbb for waterno2_06), 4 at a time
#  H2 record re-bounding samples for waterno2_06 cert3 and certB, 4 workers
OUT="${_PUBLIC_REPO}"/research-20260929/publication/reproduction/water-audit
R=$OUT/tools/run.sh
WD="${_PUBLIC_REPO}"-clean/research-20260929
W=$WD/open-instances-wave2/waterno2
CS=$W/cellslopes/logs
SR=$WD/reviews/waterno2-sepbranch-review-checks
CR=$WD/reviews/waterno2-cellslopes-review-checks
S=/tmp/wa_scratch
while pgrep -f chain_certify.sh > /dev/null || pgrep -f chain_c.sh > /dev/null; do sleep 30; done
mkdir -p $S /tmp/wa_tools && cp $OUT/tools/*.py /tmp/wa_tools/
# H0
$R w06_make_selection_certB $CR clean "python3 make_selection.py $CS/certB_cert.pkl.gz logs/repro_ind_verify_certB.json $S/repro_sel_certB.json 300 && zcat logs/sel_certB.json.gz | cmp - $S/repro_sel_certB.json && echo 'selection identical to logs/sel_certB.json.gz'"
$R w06_select_records_cert3 $SR clean "python3 select_records.py $W/sepbranch/logs/cert3.pkl $S/repro_sel_cert3.json 0.05 60 30 30 930 && python3 -c \"import json; a=json.load(open('logs/sel_cert3.json')); b=json.load(open('$S/repro_sel_cert3.json')); print('selection identical to logs/sel_cert3.json:', a==b)\""
$R w06_make_samples $S clean "python3 /tmp/wa_tools/make_samples.py $S/repro_sel_certB.json $S/repro_sel_cert3.json $S"
# H1
xargs -P 4 -d '\n' -I CMD bash -c CMD < $OUT/tools/jobs_H1.txt
# H2
$R w06_vrebound_certB_sample $CR clean "python3 vrebound_cs.py $CS/certB_cert.pkl.gz $S/sel_vbb2_certB.json $S/vrebound_certB_sample.jsonl 4 900"
$R w06_rebound_cert3_sel $SR clean "python3 rebound.py $W/sepbranch/logs/cert3.pkl $S/repro_sel_cert3.json $S/rebound_cert3_sel.jsonl 4 900"
$R w06_rbb_rerun_certB_sample $W/cellslopes clean "PYTHONPATH=../sepbranch:.. python3 /tmp/wa_tools/rerun_rbb_records.py logs/certB_cert.pkl.gz $S/sel_rbb_certB.json $S/rbb_rerun_certB_sample.jsonl 4"
$R w06_rbb_rerun_cert3_sel $W/cellslopes clean "PYTHONPATH=../sepbranch:.. python3 /tmp/wa_tools/rerun_rbb_records.py logs/certB_cert.pkl.gz $S/sel_rbb_cert3.json $S/rbb_rerun_cert3_sel.jsonl 4"
$R w06_crosscheck_pairs_cert3 $W/sepbranch clean "python3 crosscheck_pairs.py logs/cert3.json 'path+random:18:2' $S/crosscheck_cert3.json 1200 4"
$R w06_crosscheck_cs_leaf $W/cellslopes clean "PYTHONPATH=../sepbranch:.. python3 crosscheck_cs.py logs/certB_cert.pkl.gz logs/certB_verify.json $S/crosscheck_certB_leaf.jsonl 0 1 4 900 leaf"
cp $S/*.json $S/*.jsonl $OUT/data/ 2>/dev/null
echo "chain H done $(date -Is)"
