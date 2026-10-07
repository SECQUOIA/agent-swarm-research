# Protocol: campaign 5 (fixed 2026-10-03, before any campaign-5 code or run)

Campaign 5 answers the second internal review round (`evidence/review2-*.md`).
It adds four parts. Earlier campaigns remain separate records. Every run below
is reported.

## Code

A new snapshot (`v5/snapshot`) of the campaign-4 snapshot with two additions to
`research-20261003-convexification/solver/integration.py`, both off by default
so that every campaign-3 and campaign-4 mode behaves exactly as before:

1. `Config.aggregate_directions` (bool, default False). When True, the
   separator first tries, for each block, the *block direction*: lambda = 1 for
   every chosen source side of the block and `a` equal to the sum of these
   sides' affine coefficients of the block variables (the exact support of the
   sum of the block's rows). Then the directions of the mode follow as before
   (whole-row directions if `row_directions`, then remainder directions, then
   LP directions).
2. `Config.star_leaves` (int, default 0 = off). When positive, discovery also
   forms *star blocks*: for each variable c that occurs in admissible
   two-variable sides together with at least two other variables, the block
   with variables {c} and up to `star_leaves` of these other variables (in
   variable order), with all admissible sides whose variables lie in it (up to
   `star_leaves` sides; the cap on rows per block is raised to `star_leaves`
   for star blocks only) and the affine domain rows of the block (up to
   `max_domain_rows`, raised to 2 * `star_leaves` + 4 for star blocks only).
   Star blocks precede the other blocks. The dimension cap of four applies to
   all other blocks unchanged. For blocks with more than four variables the
   separator uses only the block direction and the whole-row directions (no
   sampling, no LP directions). Certification is unchanged: the polytope
   enumeration (Theorem 4.1) when its dimension and face budgets allow, else the
   inherited constrained-star oracle (`theory/quadratic_star.py` of
   `research-20261002-convexification`, certificate `quadratic_star`, replayed by
   the inherited replay), else no cut.

No other code changes. The runner (worker, driver, replay wrapper,
summarizer) is a copy of `v4/` with the new modes and parts.

## Part 5S: quadratic stars in the solver

Instances (k, n, s) with k in {4, 8, 16} leaves per star, n in {10, 20} stars,
s in {0, ..., 4} (30 instances), one `random.Random(100000*k + 1000*n + s)`:
for each star i = 1..n and leaf j = 1..k draw two distinct values from
{m/64 : m = 0..48} in random order as (a1, a2), and a slack d from
{1/8, 1/4, 1/2, 1}.

- Variables: centers y_i in [0, 1]; leaves x_ij in [0, 1]; t_ij in [-10, 10].
- Rows: Phi_ij(x_ij, y_i) - t_ij <= 0 with
  Phi_ij(x, y) = (y - a1 - (a2 - a1) x)^2 + x (1 - x), expanded exactly;
  one center-leaf row x_ij - y_i <= d per leaf; the coupling row
  sum_i y_i <= 0.8 n.
- Objective: minimize sum_ij t_ij.
- Phi_ij is concave in x (coefficient (a2 - a1)^2 - 1 < 0), so for fixed y its
  minimum over the leaf interval [0, min(1, y + d)] is attained at an endpoint.
  The optimum of star i is min over y in [0, 1] of sum_j phi_ij(y), with
  phi_ij(y) = min{Phi_ij(0, y), Phi_ij(min(1, y + d), y)}, a piecewise quadratic
  function; the generator computes it exactly in rational arithmetic (piece
  enumeration) and checks it against the independent sweep of
  `verification/M3_star_sweep.py`. The generator checks that the sum of the
  smallest minimizing y_i is at most 0.8 n (the coupling row does not bind);
  the instance optimum is then the sum of the star optima. Known witness: the
  exact minimizer, y rounded down and t rounded up to binary64, checked with the
  archived primal check.

Modes: baseline, baseline-novarlocks, baseline-extra, gurobi (as in campaign
4); and three cut modes with the *star-family limits* (max_blocks n k,
max_cuts 4 n k, max_cuts_per_round n k, max_support_calls 10 n k,
max_rounds 10, max_separation_seconds 60, separation_budget_fraction 0.5):

| Mode | Blocks | First directions |
|---|---|---|
| rowdir-star4 | at most four variables (campaign-4 discovery) | whole row, then remainder, then LP |
| agg-star4 | at most four variables | block direction, whole row, remainder, LP |
| agg-star | star blocks (star_leaves 16) first, then blocks of at most four variables | block direction, whole row (stars); as agg-star4 otherwise |

Runs: root (node limit 1, 120 s soft / 180 s hard) for all SCIP modes; full
(300 s / 360 s) for all modes including gurobi. Seed 0. 30 instances x
(6 SCIP modes x 2 + 1) = 390 runs.

Metrics: root gap closed relative to the baseline root bound and the known
optimum; solved counts; times (SGM over commonly solved; time excluding the
callback); funnel; certification method of every cut (polytope or star) and
the star oracle's time per call; replay of every cut with tampering controls.

## Part 5C: path-family additions

- 5C-a: mode baseline-novarlocks on the 20 instances of 4C3 and the 20 of 4C4:
  root (120 s) and full (300 s) runs (80 runs).
- 5C-b: 4C4 instances, root runs (node limit 1, 300 s soft / 360 s hard) with
  larger cut caps, for remainder and whole-row directions:
  `frozen-cap32`, `rowdir-cap32` (max_cuts 32n, max_cuts_per_round 8n,
  max_support_calls 80n) and `frozen-cap64`, `rowdir-cap64` (64n, 16n, 160n);
  max_blocks n, max_rounds 10, max_separation_seconds 150,
  separation_budget_fraction 0.5 (80 runs). Metric: distance of the root bound
  to bound (ii) and gap closed relative to bound (ii), compared with the
  16n-cap runs of 4C4.

## Part 5U3: a numerical global solve instead of a certificate (offline)

For every recorded cut with an exact certificate in the MINLPLib parts of
campaigns 3 and 4 (the 5,116 cuts of Part U) and for the same 1,000 sampled
path-family cuts, solve the support problem min a^T u + lambda^T g(u) over the
block box and domain rows, for the recorded binary64 direction, with Gurobi
13.0.3 (NonConvex 2, Threads 1, default tolerances: MIPGap 1e-4,
FeasibilityTol 1e-6, OptimalityTol 1e-6; TimeLimit 10 s; Seed 0), built from
the exact quadratic coefficients rounded to binary64. Constants:
U3 = Gurobi's best bound (ObjBound), U3p = its objective value (ObjVal), and
U3s = U3 - 1e-6 max(1, |U3|) (a fixed safety shift). Each is compared exactly
with the certified value, and invalid, materially invalid and removing cuts
are counted exactly as in Part U (same tolerances, same incumbents). Gurobi
statuses and times are reported.

## Execution

At most six single-threaded worker processes. The host is shared; timings are
descriptive. Replay of every recorded cut; independent recomputation of the
reported numbers.
