Checks for the audit dossier, second pass (2026-10-04). Not independently reviewed.

All scripts ran in /tmp/audit-dossier2 on copies of the inputs, with
OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1, one process at a time; each finished in
seconds. Nothing was imported or executed inside research-20260929/.
The earlier pass's checks are in ../audit/ (unchanged).

Inputs copied read-only into /tmp/audit-dossier2:
  research-20260929/bound-audit/{pages.json,screen.json,results.json,summary.json,pages/minlplib.solu}
  ~/.cache/minlplib/minlplib/osil/*.osil (read in place, read-only)
  research-20260929/publication/minlplib-status/{exact_forms.py, pages/models/gms/<name>.gms}
  research-20260929/reviews/bound-audit-verification/{ad.py,ivl.py,kraw.py,osil.py}
  research-20260929/open-instances-wave2/small/logs/rocket{100,200,400}.conopt.polished.txt

recount.py / .log        exact-decimal recount of pages, points, bounds, screen and ties;
                         compares the pair set with screen.json.
margins.py / .log        exact margins, relative margins, display units and margin/slack for
                         the 19 class (i) and 12 class (i-r) (instance, solver) pairs.
safe_margins.py / .log   the same, displayed rounded DOWN (3 significant digits), for
                         "at least" statements; reads margin_figure.csv.
figdata.py               writes margin_figure.csv (31 pairs + 3 rocket LINDO bounds).
solu.py / .log           relation between minlplib.solu =bestdual= and the per-solver bounds:
                         equal to min(third-best bound, lowest listed point value) in 585 of
                         589 cases; the 4 exceptions have no listed point.
agg.py / .log            third-best per-solver bound and the .solu value of every instance in
                         the family against the proven exactly feasible objective values.
class_recount.py / .log  per-(instance, solver) class counts and instance lists from results.json.
emfl_shortfalls.py / .log
                         listed emfl primal values and best duals against the exact lower bounds
                         (audit and recheck), read literally and widened by half a display unit.
spring_scan.py / .log    60-digit mpmath scan of all 1100 (i4, wire) assignments of spring
                         (evidence; the proof is publication/audit-ir and its review).
gms_osil_drive.py        exact comparison of the .gms text and the OSIL file: rows and
                         objective via exact_forms.compare (status track code, run on a /tmp
                         copy), plus an own exact comparison of variable names, types and bounds.
                         Handles the epigraph objective of smallinvDAX*.
gms_osil_drive_fn.py     extension: exp/sqrt/log treated as opaque symbols whose arguments are
                         compared exactly (glider100, ghg_3veh, rocket100/200/400, methanol50).
gms_osil_exact.log, gms_osil_exact_fn.log
                         results: every row, the objective, and every variable name, type and
                         bound identical for 23 instances; methanol50 differs in 360 objective
                         coefficients only (known; positive control).
gms_osil_negative_controls.log
                         a 1e-13 change of one row coefficient (sssd20-04persp e30), of one bound
                         (spring x3.up) and of one exp argument (ghg_3veh e28) is detected.
rocket_kraw.py           second, independent existence proof for rocket100/200/400: own setup
                         (thrust fixed at the authors' CONOPT values, step and masses computed
                         exactly), interval arithmetic and Krawczyk test of the first bound-audit
                         verifier (ivl.py, kraw.py), not the wave-2 reviewer's krawczyk.py.
rocket_kraw_{100,200,400}.log
                         Krawczyk ok (max ratio about 1.1e-4), box check ok, objective
                         enclosures (outward, 13 decimals):
                         rocket100 [-1.0128320069151, -1.0128320069130]
                         rocket200 [-1.0128356770698, -1.0128356770677]
                         rocket400 [-1.0128365294843, -1.0128365294821]

Commands (from /tmp/audit-dossier2; xf/ holds the exact_forms.py copy and the .gms copies;
rocket/ holds copies of the verifier's ad.py, ivl.py, kraw.py, osil.py and the data):
  python3 recount.py > recount.log
  python3 margins.py > margins.log
  python3 solu.py > solu.log; python3 agg.py > agg.log
  python3 spring_scan.py > spring_scan.log
  python3 figdata.py; python3 safe_margins.py > safe_margins.log
  cd xf; python3 drive.py <18 names> > ../gms_osil_exact.log
         python3 drive_fn.py ghg_3veh glider100 rocket100 rocket200 rocket400 methanol50 > ../gms_osil_exact_fn.log
  cd xf/ctl (perturbed .gms copies); python3 drive.py sssd20-04persp spring; python3 drive_fn.py ghg_3veh
  cd rocket; python3 rocket_kraw.py 100|200|400
