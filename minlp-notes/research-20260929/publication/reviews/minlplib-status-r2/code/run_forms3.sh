#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# exact .gms vs OSIL comparison for the other Part B instances (one process at a time)
cd "${_PUBLIC_REPO}"/research-20260929/publication/reviews/minlplib-status-r2
for n in glider100 ghg_3veh eniplac stockcycle rocket100 rocket200 rocket400 sssd20-04persp sssd22-08persp sssd25-04persp sssd25-08persp smallinvDAXr1b150-165 smallinvDAXr2b150-165 smallinvDAXr1b200-220 smallinvDAXr2b200-220 nd_netgen-2000-3-4-b-a-ns_7 topopt-cantilever_60x40_50 watercontamination0303; do
  timeout 1200 python3 code/cmp_forms.py $n > logs/cmp_forms_$n.log 2>&1; echo "$n rc=$?"
done
echo DONE
