Dossier checks for the eg family (eg_int_s, eg_disc_s, eg_disc2_s), 2026-10-04.
All scripts were run in a scratch copy under /tmp/egdossier, never inside research-20260929/.
Inputs copied there first:
  - OSIL: ~/.cache/minlplib/minlplib/osil/eg_{int,disc,disc2}_s.osil
  - points: research-20260929/open-instances-wave3/eg/retry/sol/*.retry.sol
  - per-leaf results: research-20260929/publication/eg-recheck/res/*.npz  -> /tmp/egdossier/res/
  - reviewer certifier: research-20260929/reviews/eg-retry-review-checks/{indep_cert.py,gms_model.py,data/*.gms} -> /tmp/egdossier/ic/
  - interval exp: research-20260929/open-instances-wave3/kan/kan_iv.py and open-instances-wave2/small/ia.py -> /tmp/egdossier/kiv/
Scripts (working directory in brackets) and logs (logs/):
  displays.py      [/tmp/egdossier]      exact binary64 values of the dual displays; exact gaps        -> displays.log
  margins.py       [/tmp/egdossier]      distribution of indep_cert margins, all eg_disc2_s leaves     -> margins.log
  primal_iv.py     [/tmp/egdossier]      mpmath iv (200 bits) evaluation of all OSIL rows at the points -> primal_iv.log
  rows_detail.py   [/tmp/egdossier]      active objective rows and side-row slacks at the points       -> rows_detail.log
  exp_path.py      [/tmp/egdossier]      which exp numpy 2.5.1 runs (vs glibc; strided; scalar)        -> exp_path.log
  table_exact.py   [/tmp/egdossier/kiv]  exact rational check of the kan_iv exp table, ln2 bracket     -> table_exact.log
  sens.py          [/tmp/egdossier/ic]   tightest eg_disc2_s leaves: reproduce, multipliers, S         -> sens_disc2.log
  sens_int.py      [/tmp/egdossier/ic]   LP multipliers and S near the eg_int_s optimum                -> sens_int.log
  pad_int.py       [/tmp/egdossier/ic]   padding G - aL of rows e12, e26 near the eg_int_s optimum     -> pad_int.log
  structure.py     [/tmp/egdossier/ic]   shared centres, gamma ranges, sum|a|, e27 = e28, linear terms -> structure.log
Environment: python 3.13.11, numpy 2.5.1 (SVML linked; __svml_exp8_ha present), scipy (HiGHS), mpmath 1.3.0;
OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1, single process at a time.
