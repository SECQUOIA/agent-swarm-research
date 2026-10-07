Second-pass dossier checks for the powerflow family (powerflow0030p, 0039p, 0039r), 2026-10-04.
These are dossier-author checks, not an independent review. Nothing under research-20260929/
was imported, executed or edited; every script ran in /tmp/pfd2 on copies, one thread
(OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1, PYTHONDONTWRITEBYTECODE=1), at most 2 processes.

Inputs copied to /tmp/pfd2 (sha256 checked):
  osil/powerflow0030p.osil 5c4b386b...  osil/powerflow0039p.osil 0a27073f...  osil/powerflow0039r.osil d8ba3132...
  data/powerflow0030p.sdpcert.json 63cf1e21...  data/powerflow0039p.bb3t.json 8af24081...
  data/powerflow0039r.bb3t.json 09e1a62a...     data/powerflow00{30p,39p,39r}.json (exact points;
  4b063599..., acef65da..., e851cfb4...)
  code copies: osilx.py (4bcdc1d8...), pf_model.py (patched: local paths; rectangular busmap
  returned), leafcut.py (unchanged). Reviewer code copies in /tmp/pfd2/rev: own_osil.py,
  own_relax.py, cmp_rows.py from reviews/powerflow0039-review-checks (patched: local paths).
  GAMS copies from publication/literature/network/sources (f17e87ee..., af99868d..., 4053321f...).

Scripts (own code unless stated):
  mycheck.py   own exact Lagrangian assembly from the stored multipliers; positive definiteness of
               A + eps*I proved by integer Bareiss elimination (Sylvester criterion: all leading
               principal minors > 0), eps tried in {0, 1e-10, 1e-9, ..., 1e-6} as exact decimals;
               own exact check H >= F at all 8 vertices for each plane; 60-digit evaluation of the
               Lagrangian at the exactly feasible primal centres. Rows come from pf_model.decode
               (copy) and leafcut.planes3/cut_rows3 (copy), i.e. this is not independent of the
               row construction (the reviews cover that).
  pointeval.py 0039r: Lagrangian at the exact point for the leaf containing it (containment with
               tolerance 1e-40, because the active row W_LL = 1.1236 holds at the true point but
               the 60-digit centre exceeds it by 9e-60).
  cover.py     exact grid-cell coverage of the root box by the leaf boxes.
  gaps.py      exact gap and display arithmetic (run inline first; rerun output identical).
  rev/cmp_rows.py (0039 reviewer's code, run by me on powerflow0030p, which that review did not
               cover): rebuilds R from the OSIL with the reviewer's own reader and compares with
               pf_model row by row, exactly.
  gv/gms_vs_osil.py (first-pass dossier script, rerun): exact term-by-term GAMS vs OSIL.

Commands (from /tmp/pfd2):
  python3 mycheck.py root                                   -> root.log
  python3 -u mycheck.py leaves powerflow0039p bb3t          -> leaves_0039p.log
  python3 -u mycheck.py leaves powerflow0039r bb3t          -> leaves_0039r.log
  python3 -u mycheck.py leaves powerflow0039p bb3t noangle  -> leaves_0039p_noangle.log
  python3 -u pointeval.py powerflow0039r bb3t               -> pointeval_0039r.log
  python3 cover.py                                          -> cover.log
  python3 gaps.py                                           -> gaps.log
  (cd rev; python3 cmp_rows.py powerflow0030p)              -> cmp_rows_0030p.log
  (cd gv; python3 gms_vs_osil.py powerflow0030p powerflow0039p powerflow0039r) -> gms_vs_osil.log
Wall times: root 0.4 s; leaves 7-47 s each (about 4 min for 0039p, 2 min for 0039r, 1 min
noangle); the rest seconds. No solver, SDP or branch and bound was run.
