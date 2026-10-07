# Mathematical correctness review of the main text

**Verdict: minor revision for this area.**

Scope: Sections 2, 4, 5 and 6, Appendix A, and Appendix B
(`sections/G-proofs-split.tex`), with the referenced supplement statements
and proofs checked for consistency. Locations below are source lines in
the reviewed working copy. No blocker or major mathematical issue was
found. The four issues below need small changes to assumptions or wording;
none refutes a displayed instance bound or an exact-optimum theorem.

## Numbered issues

1. **Minor — state the admissibility assumption in the value-function setting.**

   **Location:** `sections/04-split.tex:59`; compare
   `sections/G-proofs-split.tex:103`–`110`.

   **Problem:** The main text permits states constrained to arbitrary
   `Y_i` but writes `V_{i-1}(y) = inf_{u in U_i} V_i(g_i(y,u))` without
   saying that all these images belong to `Y_i`. For constrained dynamics
   this recursion can be undefined or include forbidden transitions. The
   appendix supplies the missing assumption explicitly: `U_i` is
   nonempty and `g_i : Y_{i-1} × U_i → Y_i`.

   **Evidence:** Take `Y_0 = Y_1 = {0}`, `U_1 = {0,1}`,
   `g_1(0,u) = u`, and a terminal cost defined only on `Y_1`. The control
   `1` makes the displayed recursion evaluate the terminal cost outside
   its domain. Extending that cost arbitrarily would instead allow an
   inadmissible transition. The appendix's induction is correct with its
   stronger setting. The nonnegative matrices used for `catmix` preserve
   the stated cone, so this does not affect that certificate.

   **Concrete fix:** Replace the beginning of the paragraph by:

   > For nonempty control sets `U_i` and maps
   > `g_i : Y_{i-1} × U_i → Y_i`, consider the dynamics
   > `y_i = g_i(y_{i-1},u_i)` with `y_i ∈ Y_i` and `u_i ∈ U_i`.
   > For a terminal cost `Φ : Y_n → R`, let …

   This is the simplest repair. If transitions outside `Y_i` are meant
   to be allowed as arguments, explicitly extend `V_i` by `+∞` there
   instead, and use that convention in the appendix too.

2. **Minor — the tolerance-deficit function is not rational-valued for arbitrary real tolerances.**

   **Location:** `sections/05-other.tex:82`; its construction is in
   `sections/B3-camshape.tex:206`–`208`.

   **Problem:** The proposition quantifies over every real
   `0 ≤ ε < 1` and calls `D_n(ε)` an “explicit rational.” The supplied
   construction uses `ε` itself in rational operations. It gives a
   rational number when `ε` is rational, but not for every real `ε`.

   **Evidence:** This is more than a question of how to represent the
   input. As `ε → 1⁻`, `β_ε = ε/(1-ε)^3 → +∞`, whereas each
   `S_j^ε` remains bounded. For `j ≥ 2`, `W_j ≥ U_0 = 1` by (K1).
   Thus, for all sufficiently large `ε < 1`, every denominator in
   `R_j^ε`, `j ≥ 2`, is nonpositive. The caps then give
   `E_1^ε = ū + ε` and `E_j^ε = 2 + ε`, `j ≥ 2`. Consequently

   `D_n(ε) = c_0 [n ε + Σ_{j=2}^n (2-E_j)]`.

   The constants in this expression are rational and `c_0 n > 0`.
   It is irrational for irrational `ε` in that range. The deficit
   inequality itself is correct, and all tabulated tolerances are rational.

   **Concrete fix:** Write:

   > For `0 ≤ ε < 1` there is an explicit bound `D_n(ε)`, rational
   > when `ε` is rational, such that …

3. **Minor — qualify the claim that the `lukvle10` gap equals the summed search tolerances.**

   **Location:** `sections/04-split.tex:335`; repeated in
   `sections/B1-lnts-lukvle10.tex:314`–`315`.

   **Problem:** The enclosure is proved, but exact equality between its
   gap and the sum of branch-and-bound tolerances is not established.
   The subproblem incumbents are upper bounds on separate minima,
   evaluated at numerical KKT pairs. Their sum is not proved to equal
   the objective of the exactly feasible seed-defined point. Logged
   lower bounds are also reduced before assembly.

   **Evidence:** The supplement's proof at lines 293–306 explicitly
   separates the assembly from the primal enclosure. If `l_i` and
   `u_i` denote subproblem lower bounds and incumbents, and `Λ` is the
   multiplier constant, the exact accounting is

   `f(x*) - (Λ + Σ l_i) = [f(x*) - (Λ + Σ u_i)] + Σ(u_i-l_i)`.

   The first bracket is not shown to vanish. It includes the mismatch
   between the numerical KKT pairs and the exactly feasible point and
   the arithmetic enclosures; the downward adjustment of logged bounds
   adds another assembly allowance. Numerical agreement at a tiny scale
   supports “dominated by,” not an exact equality. This does not weaken
   the proved `1.42 × 10^-9` enclosure.

   **Concrete fix:** Replace the main-text sentence by:

   > The certified gap is at most `1.42 × 10^-9` and is dominated by
   > the summed branch-and-bound tolerances; global optimality of the
   > exactly feasible point is not proved.

   Use the same wording in the supplement. If an equality is desired,
   provide an exact accounting that includes the bracket and the assembly
   allowances above.

4. **Minor — classify the `catmix` dual evidence consistently with the actual check.**

   **Location:** `sections/04-split.tex:307`; also the `catmix` row of
   `tables/tab-trust.tex:27`, included by Section 2.

   **Problem:** The certificate box and trust table call the dual evidence
   `stored`, while the supplement says the per-stage minorant values
   are not stored and checking requires a rerun. This overstates what
   an archived output alone permits a checker to establish.

   **Evidence:** `sections/B4-chain-catmix.tex:412` explicitly says that
   the per-stage `w^(i)` are not stored and a check takes about 45 minutes.
   By `sections/02-semantics.tex:178`–`179`, `stored` means checking a
   stored finite certificate, whereas `rerun` means rerunning the search.
   The mathematics is correct, but the input/output logs alone do not
   check conditions (T), (S) and (I) of the minorant induction.

   **Concrete fix:** Change the dual evidence tag to `rerun` in the
   certificate box and in the source that generates the trust table.
   A more informative label is:

   > Dual: `rerun` (the minorant computation); primal: `stored`
   > (exact rational state evaluation).

   Alternatively, archive sufficient stage values and per-ray checking
   data to check (T), (S) and (I) directly, and document that checker.

## Explicit resolution of open item 1

**The extended-value proofs in Appendix B are correct under the appendix's
stated assumptions.** In particular, the value-function minorant induction
and the finite-potentials construction for cellwise slopes are correct.
Issue 1 concerns the shorter main-text setting, not an error in those
appendix proofs.

- **Extended sums and split bounds:** Pointwise stage residuals have
  values in `R ∪ {+∞}`; only their infima can be `-∞`. With the explicitly
  stated convention that `+∞` dominates in a finite sum, (F1) is correct,
  including an empty factor or an everywhere-infinite stage. On a
  nonempty feasible set every feasible stage value is finite, so no stage
  infimum can be `+∞`. Telescoping and comparison with the feasible
  objective therefore do not use undefined `+∞ - +∞` arithmetic.
  The row-form, case-split and infeasibility arguments are valid.
- **Minorants:** Infima over nested nonempty control sets commute without
  attainment. The terminal cost is real, so a continuation infimum may
  be `-∞`; this does not invalidate the dynamic-programming identity or
  part (a). Part (b) explicitly assumes the true value function is
  real-valued. Concavity plus positive homogeneity then gives
  superadditivity and `V(0)=0`; the sector interpolation is well defined
  on shared rays and at zero. No concavity of a computed minorant is
  assumed. The supplement's `catmix` induction also correctly clips
  negative computed ray values to zero using nonnegativity of the true
  value functions.
- **Affine exactness and windows:** The converse exactness argument uses
  attainment, which makes the optimum and all stage infima finite.
  The forced-slope recursion uses injectivity of the transpose of a
  coordinate-selection map with distinct coordinates. The appendix
  correctly excludes equality-constrained bags from the literal
  interior-point hypothesis. Merging windows preserves feasibility,
  separator agreement and costs; both window inequalities remain valid
  under the extended-sum convention.
- **Finite cell potentials:** Arc weights exclude `-∞`; a finite shortest
  path therefore exists whenever `SP` is finite. The caps
  `M_t = C_0 + Σ_{s≤t} β_s` make potentials finite even at unreachable
  cells. In both branches of the proof, every finite reduced arc has
  nonnegative cost. Choosing `C_0` large enough preserves the distances
  along a shortest path, giving zero minima in the intermediate layers.
  The last-layer minimum is `SP`, including arcs from unreachable cells.
  Infinite arcs remain infinite after adding finite constants. Thus the
  construction attains the claimed maximum over real-valued splits;
  it does not merely approach a supremum. The one-stage case is immediate.
  `waterno2` uses the validity part, which also allows overlapping closed
  cells; the partition assumption is needed only for the best-constants
  assertion.

## Other mathematical findings and verification limits

The minimization/maximization conventions in Section 2 are consistent:
the `pricing050` dual is an upper bound and its primal value a lower
bound. The enclosure and refutation statements use infima and do not
assume attainment. The `dtoc5` square completion has the correct row sign,
requires positive coefficients only on the free intermediate states, and
handles the free terminal state through the zero terminal multiplier.
The `lnts` root, feasibility and support arguments prove attainment and
optimality. The `camshape` comparison, envelope feasibility and uniqueness
arguments are complete. The power-flow eigenvalue-shift bound has the
correct inequality-multiplier signs, and its leaf planes have the required
majorant direction. The `etamac` majorant and `pindyck` strong-concavity
arguments match their supplement proofs. In particular, the supplement
does not infer uniqueness merely from concavity on a nonconvex feasible
price set: it proves that every maximizer lies in an interior feasible
ball, is stationary, and maps back to a feasible full-space point.

The Section 6 Krawczyk proof is correct: strict inclusion bounds the
weighted matrix norm by a number below one, which proves nonsingularity
of the preconditioner and every interval Jacobian before zero existence
and uniqueness are concluded. The triangular induction is correct, and
the Lindemann–Weierstrass argument correctly groups equal absolute angles
before applying linear independence. Appendix A's distinctions between
exact OSIL decimals, GAMS comparisons and binary64 data are consistent
with these proofs.

The computer-assisted proof sketches identify the quantities checked and
the arithmetic used, either directly or in the cited supplement. The
`eg` sketch retains the conditional trust statement and the check of every
used exponential/power value; the ANN and KAN sketches retain the
covering and relaxation directions. I did not rerun the full `catmix`,
`waterno2`, ANN, KAN or `eg` searches. This review establishes the proof
logic and consistency of the stated computations, supplemented by the
small checks below; it is not a fresh certification of every archived
search output or checking implementation.

## Targeted commands actually run

All execution was from copies or new reviewer code in
`/tmp/sol-math-main-review`. No repository script was run in place. At
most two single-threaded Python processes ran concurrently. No paper
source was edited, no commit was made, and no project-wide or CI check
was run.

```text
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 /tmp/sol-math-main-review/check_core.py \
  > /tmp/sol-math-main-review/check_core.log

# Working directory: /tmp/sol-math-main-review
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 exactfeas.py > exactfeas.log
```

Both commands exited successfully. The first is new reviewer code using
Python integers, integer square roots and `Fraction` arithmetic only.
It exhaustively enumerates 6,561 three-stage graphs with arc weights
`{-1,0,+∞}` and checks 1,000 further deterministic random rational graphs,
including the one-stage case. All 7,561 pass; 2,793 have finite shortest
paths and unreachable internal nodes. Independently enumerated control
sequences confirm 100 cone-state minorant inequalities through four
backward steps; every computed table is deliberately nonconcave.
For each `lnts` size, 305 rational bisections with integer-square-root
enclosures produce a root bracket narrower than `10^-90` and confirm the
printed optimum enclosure. It also checks the rational constants and
cosine-series bracket in the `hvycrash` existence proof and the displayed
KAN nonzero constant residual.

The second command uses copied critique code (`exactfeas.py` and
`mine.py`) and copied OSIL inputs. Exact generic row and bound evaluation
finds zero violation for the envelope points of `camshape100` and
`camshape200`, with respectively 63 and 127 active convexity rows. The
14-decimal objective floors are `-4.28414712174675` and
`-4.27850023299273`, as printed. This is a replay of existing independent
critique code, not a newly written third implementation.
