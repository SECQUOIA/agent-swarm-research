Critic checks for the waterno2 dossier (2026-10-04). Run in a scratch copy, never in R/.

- cmp_builders.py: copy osilx.py (R/reviews/open-instances-verification), vstruct.py and vmodel.py
  (R/reviews/waterno2-verification), wmodel.py (R/open-instances-wave2/waterno2) and the five GAMS files
  (R/publication/minlplib-status/pages/models/gms) into a scratch directory, then run
  `python3 cmp_builders.py`. Compares the polynomial rows used by both B&B lines with the GAMS text.
  Output: logs/cmp_builders.log (seconds).
- replay_audit.py: reads the reproduction track's logs (R/publication/reproduction/water-audit) and
  compares them with the stored certificates. Output: logs/replay_audit.log (seconds).
