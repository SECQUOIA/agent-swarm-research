Critic checks for the lnts-lukvle10 dossier (written 2026-10-04; independent of the dossier author's code).

Run only from a scratch copy, never inside the repository ($R = research-20260929):

  mkdir -p /tmp/lnts-critic && cd /tmp/lnts-critic
  cp <this dir>/*.py .
  cp $R/publication/primal/lnts/points/lnts{50,100,200,400}_point.json .
  cp $R/reviews/open-instances-verification/logs/{lukvle10_bnb.json,lukvle10_lam_kkt.npy} .
  cp $R/publication/primal/dtoc5-lukvle10/logs/lukvle10_kkt_lam.txt .
  cp ../lnts-lukvle10/lnts_exact_opt.json .          # dossier's enclosures, for comparison only
  OMP_NUM_THREADS=1 python3 thm3_iv.py 50 100 200 400   # ~11 s; writes thm3_iv.json
  OMP_NUM_THREADS=1 python3 misc_checks.py               # needs thm3_iv.json
  OMP_NUM_THREADS=1 python3 lukv_checks.py

thm3_iv.py: Theorem 3 sign check and optimum enclosure in mpmath iv (130 digits), c_j from an
impulse simulation of the recursion, own bisection root and an asymmetric bracket; free Newton
on (mu, nu, h) without the symmetry ansatz; Proposition 2 residual at the exact multipliers.
misc_checks.py: stored 60-digit primal h enclosures vs the optimum; author float duals vs N*h2;
lnts50 listed relative gap; COPS six-digit display; B&B leaf count.
lukv_checks.py: lambda-bar closed form, middle-pair Hessian, multiplier deviation from the
40-digit KKT multipliers, full q range.
