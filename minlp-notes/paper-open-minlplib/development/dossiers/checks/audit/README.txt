Cheap checks for the audit dossier (2026-10-04). Run in a disposable directory,
never inside research-20260929/. Inputs copied read-only into that directory:
  research-20260929/bound-audit/{pages.json,screen.json,results.json,summary.json}
  research-20260929/bound-audit/pages/minlplib.solu
  research-20260929/bound-audit/sol/{smallinvDAXr1b200-220.p2,smallinvDAXr2b200-220.p2,
      smallinvDAXr1b150-165.p2,sssd25-08persp.p4,sssd25-08persp.p3,sssd22-08persp.p4}.sol
  ~/.cache/minlplib/minlplib/osil/{smallinvDAX*,sssd25-08persp,sssd22-08persp,spring,emfl050_3_3}.osil
Environment: OMP/OPENBLAS/MKL_NUM_THREADS=1. Each script finishes in seconds.

count.py        exact-decimal recount of pages/points/bounds and of the screen (158 pairs,
                3851 ties); compares with the audit's float-based screen.json.   -> count.log
third.py        third-best per-solver dual (MINLPLib's bold/aggregate value) versus the proven
                exactly feasible objectives of the class (i)/(i-r) instances.   -> third.log
solu.py         relation of minlplib.solu =bestdual= to min(third-best dual, lowest listed
                point value) (display-rounding tolerance 6e-9 relative).        -> solu.log
qosil_min.py    minimal OSiL reader (linear/quadratic only, exact Fractions), own code.
smallinv_check.py  exact feasibility and objective of the smallinvDAX proving points. -> smallinv_check.log
sssd_check.py   own exact construction (q = u/(1-u)) for sssd25-08persp p3/p4 and
                sssd22-08persp p4.                                               -> sssd_check.log
spring_check.py 50-digit numerical scan of all 1100 (i4, wire) assignments of spring
                (evidence, not a proof; the proof is publication/audit-ir).       -> spring_check.log
emfl_lb.py      own weak-duality lower bound for emfl050_3_3: numerical dual SOCP (Clarabel),
                exact rational norm scaling and single-cone repair of g >= 0, exact
                final check; compares with listed values.                        -> emfl_lb.log
margins.py      exact margins, margin/slack and margin/unit from results.json.  -> margins.log
rocket_margins.log  exact margins of the LINDO rocket/methanol50 bounds against the saved
                enclosure upper ends in reviews/wave2-small-verification/logs/krawczyk_*.json.
