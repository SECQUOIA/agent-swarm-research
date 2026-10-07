Second-pass dossier checks for the eg family (2026-10-04). All scripts ran in a scratch copy
/tmp/egd2 (never inside research-20260929/), single-threaded, one process at a time.

Layout of the scratch copy:
  /tmp/egd2/{eg_int_s,eg_disc_s,eg_disc2_s}.osil      copies of ~/.cache/minlplib/minlplib/osil/*.osil
  /tmp/egd2/*.retry.sol                                copies of open-instances-wave3/eg/retry/sol/
  /tmp/egd2/res/                                       copies of publication/eg-recheck/res/*.npz
  /tmp/egd2/ic/   indep_cert.py, gms_model.py, data/*.gms (copies from reviews/eg-retry-review-checks/)
  /tmp/egd2/kiv/  kan_iv.py, ia.py (copies)

Commands (from /tmp/egd2 unless noted) and logs (logs/):
  python3 osil_iv.py eg_int_s eg_disc_s eg_disc2_s   -> osil_iv.log   (own OSIL parser; structure; primal points in mpmath iv)
  python3 struct2.py                                  -> struct2.log   (gamma ranges, c_k range, side-row slacks)
  python3 displays.py                                 -> displays.log  (exact binary64 values, displays, gaps)
  python3 exp_path.py                                 -> exp_path.log  (which exp numpy runs)
  python3 margins2.py                                 -> margins2.log  (margin distribution, certifier statistics)
  (kiv) python3 table_exact.py                        -> table_exact.log (exact check of the interval-exp constants)
  (kiv) python3 fexp_audit_cost.py                    -> fexp_audit_cost.log (speed/width of a tight exp enclosure)
  (ic)  python3 timing.py                             -> timing.log    (certifier cost per leaf, exp arguments per piece)
  (ic)  python3 ../../sens.py, sens_int.py, pad_int.py (scripts of the first pass, in checks/eg/) -> sens_*.log, pad_int.log
