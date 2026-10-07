Checks run for the independent critique of dossiers/eg.md (2026-10-04). All ran in /tmp/egcrit, single-threaded,
never importing or executing scientific code inside research-20260929/ (r1exp.py contains a copied excerpt of
publication/reviews/eg-recheck-r1/own_ia.py lines 27-106).

  ./libpaths.sh      -> logs/libpaths.log   numpy 2.5.1 dispatch and call targets of DOUBLE_exp_X86_V4 and DOUBLE_power_X86_V4
                                            (objdump window of 0x700 bytes; for exp it also reaches into the following log loop)
  python3 powtest.py -> logs/powtest.log    x**3 and x**4 on float64 arrays: np.power (SVML pow), not repeated products; error vs exact
  python3 l1l2.py    -> logs/l1l2.log       egfast.fexp Cody-Waite constants L1, L2 checked against ln2/64 from the rational series
  python3 r1exp.py   -> logs/r1exp.log      width and speed of r1's interval exp (candidate auditor for option (f))
