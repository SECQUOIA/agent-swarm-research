Critic checks for dossier `solvers` (2026-10-04). Independent code; never run inside the repository tree.
Copy this folder to /tmp and put next to it:
  camshape{100,200,400,800}.gms (research-20260929/publication/solver-runs/gms/),
  QPLIB_{2738,2480,2703,3177}.{gms,sol} (research-20260929/publication/literature/control/sources/qplib/camshape_copies/),
  ps.py = copy of ../r2/pattern_scan.py (strong_criterion.py imports it from its own folder).
Commands (one core; seconds each):
  python3 indep_bound.py camshape100.gms QPLIB_2738.gms ... > indep_bound.log   (sympy parser, presence check of rows, iterated smoothing)
  python3 eps_check.py > eps_check.log                                            (Proposition 5 recipe on indep_bound.py)
  python3 evalgms.py > qplib_sol_eval.log                                         (exact evaluation of QPLIB .sol points)
  python3 enclosure.py > enclosure.log                                            (binary64 enclosure test per (L,k))
  python3 strong_criterion.py waterno2_01 waterno2_06 waterno2_24 kall_ellipsoids_tc02b > strong_criterion.log (reads ~/.cache/minlplib OSIL, read-only)
margins_floor.log was produced by an inline fractions script (values listed in the critique).
