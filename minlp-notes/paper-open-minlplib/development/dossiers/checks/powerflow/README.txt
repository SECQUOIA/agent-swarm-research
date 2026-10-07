Dossier checks for the powerflow family (powerflow0030p, 0039p, 0039r), 2026-10-04.

All scripts ran in /tmp/pfdossier (never inside the main tree), single-threaded
(OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1), on copies of:
  - OSIL files ~/.cache/minlplib/minlplib/osil/powerflow00{30p,30r,39p,39r}.osil
    (sha256 5c4b386b..., 8106e2b1..., 0a27073f..., d8ba3132...; match the status refresh),
  - GAMS files research-20260929/publication/literature/network/sources/minlplib_powerflow00{30p,39p,39r}.gms
    (sha256 f17e87ee..., af99868d..., 4053321f...; match the status refresh),
  - certificate data open-instances-wave3/logs/powerflow00*.sdpcert.json and
    open-instances-wave3/powerflow/ext/logs/powerflow0039{p,r}.bb3{,t}.json,
  - primal point files publication/primal/powerflow/points/*.json and certify logs,
  - code copies: reviews/open-instances-verification/osilx.py (sha256 4bcdc1d8...),
    open-instances-wave3/powerflow/pf_model.py (patched only to read osilx and the OSIL
    files from /tmp/pfdossier), open-instances-wave3/powerflow/ext/leafcut.py.

Scripts (paths inside refer to /tmp/pfdossier):
  gms_vs_osil.py   exact term-by-term comparison of GAMS and OSIL rows and objective
                   -> gms_vs_osil.log (0 differing rows, all three);
                   gms_vs_osil_negative.log: negative controls (last-digit change and
                   sin-argument swap detected; cos-argument swap correctly not flagged).
  my_eval.py       own exact Lagrangian assembly + natural-order exact LDL^T PSD test,
                   rows from pf_model (row order) -> root_eval.log, leaf_eval.log.
  drop_angle.py    0039p tight-run leaves with all angle-row multipliers set to 0
                   -> drop_angle.log (all leaves PSD with eps = 0; min 41869.05148528834).
  cover_planes.py  leaf coverage (grid cells), vertex-plane validity, leaf identity at the
                   exactly feasible points -> cover_planes.log.
  tan_check.py     exact check tb >= tan(0.26), ta <= tan(-0.26) -> tan_check.log.
  gaps.py          exact gap arithmetic from the primal enclosures -> gaps.log.

Commands (from /tmp/pfdossier):
  python3 code/gms_vs_osil.py powerflow0030p powerflow0039p powerflow0039r
  python3 neg/gv.py powerflow0039r powerflow0039p      (perturbed GAMS copies)
  python3 code/my_eval.py root powerflow0030p powerflow0039p powerflow0039r powerflow0030r
  python3 -u code/my_eval.py leaf powerflow0039p bb3t ; ... leaf powerflow0039r bb3t
  python3 -u code/drop_angle.py
  python3 code/cover_planes.py powerflow0039p powerflow0039r
  python3 code/tan_check.py powerflow0030p powerflow0039p
  python3 code/gaps.py
No solver, SDP or branch and bound was run. These checks are not an independent review.
