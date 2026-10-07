#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Verifier: GAMS 54.3 Convert of each current .gms, compared with the cached MINLPLib OSIL (serial, one process).
cd "${_PUBLIC_REPO}"/research-20260929/publication/reviews/minlplib-status-r1
for n in methanol50 lop97icx ghg_3veh nuclear14 spring catmix200 catmix400 catmix800 eniplac stockcycle rocket100 rocket200 rocket400 glider100 sssd22-08persp sssd25-04persp sssd25-08persp smallinvDAXr2b150-165 smallinvDAXr1b200-220 smallinvDAXr2b200-220 emfl050_3_3 emfl050_5_5 emfl100_3_3 emfl100_5_5 lnts50 lnts100 lnts200 lnts400 camshape100 camshape200 camshape400 camshape800 lukvle10 hvycrash ex6_2_7 ex6_2_5 etamac pricing050 chain50 chain100 chain200 chain400 powerflow0030p powerflow0039p powerflow0039r pindyck eg_int_s eg_disc_s eg_disc2_s kan_r3_h1_n4 kan_r3_h1_n5 kan_r3_h1_n9 kan_r5_h1_n3 kan_r5_h1_n5 kan_r5_h1_n8 waterno2_06 waterno2_09 waterno2_12 waterno2_18 waterno2_24 ann_cumene_tanh watercontamination0303 dtoc5 optcdeg2; do
  [ -f conv/$n.cur/out.osil ] || code/conv.sh dl/gms/$n.gms conv/$n.cur m > /dev/null 2>&1
  echo "== $n"; timeout 2400 python3 code/osil_eval_cmp.py ~/.cache/minlplib/minlplib/osil/$n.osil conv/$n.cur/out.osil 2 2>&1 | tail -6
done
echo BATCH_DONE
