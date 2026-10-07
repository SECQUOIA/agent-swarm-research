Checks run for the dtoc5/optcdeg2 dossier (2026-10-04). Nothing here was run in the main tree.
Inputs were copied to the scratch directory /tmp/dossier-dtoc5-optcdeg2 and every script was run there
with OMP_NUM_THREADS=1, one core. Each script reads its inputs from the current directory.

dtoc5_checks.py      inputs: dtoc5.gms (sha256 4fc80f6b...), dtoc5_point.txt.gz (sha256 6e963788...),
                     dtoc5_check_objective_exact.txt (both from R/publication/primal/dtoc5-lukvle10/).
                     A: exact text check of the GAMS model. B: exact-rational Lagrangian dual from the
                     stored exactly feasible point (lam_t = -2 u_t, lam_{T-1} = 0); no floating point. 2.6 s.
optcdeg2_gms_check.py  input: optcdeg2.gms (sha256 42171d55...). Exact text check of rows, objective, bounds.
optcdeg2_primal_int.py input: optcdeg2_kkt_u.npy (R/theory-bangbang/logs/). Integer fixed-point interval
                     simulation (2^-320 grid, floor/ceil), IVT bracket for u_47290, objective enclosure,
                     negative test. No mpmath, no floating point in the proof part. 1.5 s.
rerun_reviewer_*.json  outputs of unmodified copies of R/reviews/bangbang-verification/v_states.py (4.7 s) and
                     v_qcal_exact.py (16.2 s) run in /tmp/dossier-dtoc5-optcdeg2/repo/research-20260929/...
                     with copied inputs (optcdeg2_qcal_data.npz sha256 08311d33..., optcdeg2_vbounds.npy,
                     optcdeg2_qcal_stage_lb.npy). The regenerated V_t array is identical to the stored
                     vt_reviewer.npy; bound_str is identical (29387607509587509237940 = LB * 1e20, truncated).
These checks were written by the dossier author and have not been independently reviewed.
