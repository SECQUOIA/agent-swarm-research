Dossier checks, round 2 (independent re-implementation; author: Claude, dossier for family `solvers`).
Never run these inside the repository tree. Copy this folder to /tmp, then copy inputs next to it:
  - camshape{100,200,400,800}.gms from research-20260929/publication/solver-runs/gms/
  - QPLIB_{2738,2480,2703,3177}.gms from research-20260929/publication/literature/control/sources/qplib/camshape_copies/
  - results_table.csv, references.csv from research-20260929/publication/solver-runs/
  - the eight CIP models and JSON witnesses named in cipchk.py from research-20260929/publication/scip-bug/
  - m_p.gdx savepoints renamed <instance>__<solver>.gdx from research-20260929/publication/solver-runs/runs/
pattern_scan.py reads ~/.cache/minlplib/minlplib/osil/*.osil (1632 files, read-only), 128 s on one core.
Commands (one core, seconds each): python3 recount.py; python3 margins.py; python3 cipchk.py;
python3 cambd.py camshape100.gms QPLIB_2738.gms ...; python3 tol.py (18 s); python3 ev.py camshape100.gms camshape100__BARON.gdx -4.28414712174675 (needs gdxdump).
Logs here are the outputs of those commands on 2026-10-04.
