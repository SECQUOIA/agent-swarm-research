Dossier checks for lnts50-400 and lukvle10 (written 2026-10-04 by the dossier author; not an independent review).

Run only from a scratch copy, never inside the repository:

  mkdir -p /tmp/lnts-check && cd /tmp/lnts-check
  cp <this dir>/lnts_exact_opt.py <this dir>/lukvle10_sum.py .
  cp $R/publication/primal/lnts/points/lnts{50,100,200,400}_point.json .
  cp $R/reviews/open-instances-verification/logs/{lukvle10_bnb.json,lukvle10_lam_kkt.npy,lukvle10_x5.npy} .
  OMP_NUM_THREADS=1 python3 lnts_exact_opt.py 50 100 200 400   # 0.6 s; writes lnts_exact_opt.json
  OMP_NUM_THREADS=1 python3 lukvle10_sum.py                     # < 1 s

($R = research-20260929.) lnts_exact_opt.py proves the sign change of g with Python
integers and Fractions only (isqrt enclosures); mpmath only locates the root.
lnts_negative_test.log: shifting the bracket by 1e-55 makes the sign test fail.
