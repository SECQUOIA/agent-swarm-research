# Core cluster checks (exact `fractions.Fraction` arithmetic)

These are finite checks that support, but do not replace, the proofs in
`../core-proofs.tex`. Each runs in seconds. They were run from this
directory with `nice python3 <script>`; outputs are copied below.

- `core_lib.py`: an independent implementation of the per-coordinate
  algorithm (curvature `L_i = max(0, H_ii)`, dyadic meshes, grading `2^-mu`, cap
  `10 * 2^mu * ceil(log2(n_P + 2))`, min-marginal filtering, restart at the lower
  endpoint vector), a minimal path-certificate checker (grids, one bound, one
  point), and an exact face-enumeration solver for small box QPs.
- `check_pipeline.py`: convex mixed-integer paths and the nonconvex block family
  with proved weighted growth (stage invariants, gap and radius bounds, no abort
  in the admissible trial); random nonconvex mixed-integer paths without growth
  (bracket around the exact optimum, termination); certificate acceptance and
  rejection of tampered certificates.
  Output: `{'growth_instances': 12, 'admissible_stage_checks': 9,
  'nonconvex_instances': 12, 'nonconvex_stages': 53, 'certificates_accepted': 24,
  'tampered_rejected': 23, 'max_nodes': 9}` and
  `{'stress_admissible_stage_checks': 201, 'max_nodes': 9}`.
- `check_grid_count.py`: graded grids built at the worst admissible
  localization radius for `mu = 2..7`, `n_P` up to `10^4`, continuous and
  integer; mesh inequality, the per-side count formula, and the cap.
  Output: `{'grid_cases': 720, 'max_nodes_over_cap': 0.3125}`.
- `check_families.py`: the ETH width family (unique vertex optimizer,
  `floor(Psi*/2^n) = -alpha`, growth `>= 1/(2n)` at 9000 rational points), the
  Subset Sum width-3 family (exhaustive: uniqueness, gap one, yes/no
  equivalence, growth and `kappa` bounds), and the nonconvex block family
  (64 strict local minima on a 2x3 block grid, growth `1/2` at 2000 points).
  Output: `{'A_growth_points': 9000, 'B_instances': 6,
  'C_strict_local_minima': 64, 'C_growth_points': 2000}`.
- `check_clique_gadget.py`: the multicolored-clique encoding, checked with an
  exact min-sum DP with minimizer counting on the stated tree decomposition
  (`Phi = 0` iff a clique exists, number of minimizers equals the number of
  minimum-weight cliques, threshold `W`, bag size `max(k, 7)`).
  Output: `{'instances': 14, 'yes': 10, 'no': 4, 'unique_cases': 10}`.

The LaTeX fragment was also compiled in a throwaway wrapper under `/tmp`
(no errors; only the new citation keys are undefined).
