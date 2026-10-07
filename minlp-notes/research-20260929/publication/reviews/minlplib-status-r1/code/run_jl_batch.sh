#!/bin/bash
_PUBLIC_REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../../../.." && pwd)"
# Verifier: compare 2017 MINLPLib.jl copies with cached OSIL (one process, serial).
cd "${_PUBLIC_REPO}"/research-20260929/publication/reviews/minlplib-status-r1
for n in rocket100 rocket200 rocket400 nuclear14 eniplac stockcycle lop97icx glider100 methanol50 emfl050_3_3 emfl050_5_5 emfl100_3_3 emfl100_5_5 waterno2_06 waterno2_09 waterno2_12 waterno2_18 waterno2_24 powerflow0030p powerflow0039p powerflow0039r lukvle10 hvycrash camshape100 camshape200 camshape400 camshape800 catmix100 catmix200 catmix400 catmix800 chain50 chain100 chain200 chain400 lnts50 lnts100 lnts200 lnts400 eg_int_s eg_disc_s eg_disc2_s pindyck etamac ex6_2_5 ex6_2_7 watercontamination0303; do
  echo "== $n"; timeout 1500 python3 code/jl_cmp.py "${_PUBLIC_REPO}"/research-20260929/publication/minlplib-status/pages/sources/jl2017/$n.jl ~/.cache/minlplib/minlplib/osil/$n.osil 2 2>&1 | tail -6
done
echo BATCH_DONE
