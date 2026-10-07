#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
cd "${_PUBLIC_REPO}"/research-20260929/publication/reviews/minlplib-status-r2
for n in catmix200 catmix400 catmix800; do timeout 1500 python3 code/cmp_forms.py $n > logs/cmp_forms_$n.log 2>&1; done
timeout 1500 python3 code/cmp_forms.py lop97icx "${_PUBLIC_REPO}"/research-20260929/bound-audit/sol/lop97icx.p2.sol > logs/cmp_forms_lop97icx.log 2>&1
timeout 2400 python3 code/cmp_forms.py methanol50 "${_PUBLIC_REPO}"/research-20260929/bound-audit/sol/methanol50.p4.sol > logs/cmp_forms_methanol50.log 2>&1
for n in spring nuclear14 stockcycle; do timeout 1500 python3 code/cmp_forms.py $n > logs/cmp_forms_$n.log 2>&1; done
echo DONE
