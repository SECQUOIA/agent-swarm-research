Checks run for the camshape dossier (2026-10-04). Nothing here was run in the main tree.
Inputs were copied to the scratch directory /tmp/camshape_dossier_o5 and every script was run there with
OMP_NUM_THREADS=1, one core per process, at most two processes at a time. Each script reads its inputs from
the current directory. Input sha256 prefixes are in input_sha256.txt:
  camshape{100,200,400,800}.osil   from ~/.cache/minlplib/minlplib/osil/ (sha256-identical to the 2026-10-02 refresh)
  camshape{100,200,400,800}.gms    MINLPLib .gms (identical to R/publication/solver-runs/gms/)
  QPLIB_{2738,2480,2703,3177}.gms/.sol   from R/publication/literature/control/sources/qplib/camshape_copies/
  camshape*.p1.sol, *.p2.sol       from R/open-instances/minlplib_sol/

check_exact.py      own OSIL reader (xml.etree, decimal strings -> Fraction); structure assertions; Chebyshev
                    U_m >= 0 and the rational test c/2 > cos(pi/n); S, R, B, envelope E, v_n = -c0 sum E exactly;
                    generic exact evaluation of every OSIL row/bound at (E, diff E); hypotheses C1-C5 of the
                    dossier's Theorem 1; row-by-row case split of Lemma 3; omitted COPS row; MINLPLib p1/p2.
                    Log: check_exact.log, check_exact.json. 6 min 9 s for all four sizes.
check_gms.py        own recursive-descent parser for the GAMS scalar files; maps each file to the template;
                    MINLPLib .gms constants equal the OSIL ones; for the QPLIB copies: comparison bound and exact
                    feasibility of the copy's own envelope (=> exact optimum of the copy). Log: check_gms.log.
eval_qplib_points.py  exact evaluation of the QPLIB reference points in their own models vs the copy optima.
tol_check.py        independent re-derivation of the worst-case tolerance deficit D_n(eps) (solvers dossier
                    Proposition 3). Log: tol_check.log.
cops_consts.py      distance of the decimal constants from the exact COPS constants (mpmath iv, 60 digits).
omitted_row_hi.py   omitted COPS curvature row |r2 - r1| <= alpha at the perturbed ("hi") corner envelope.
robust.py           optimum enclosures valid for all constants within eta = 1e-14 (monotonicity argument of
                    dossier I-6). Log: robust.log.

These checks were written by the dossier author and have not been independently reviewed.
