# TU cluster report (KEY = tu)

Coupled constraints: TU fibers, filtering, state count, exact output,
equality-tangent curvature, initial mesh, nonunique TU unions.

Paper fragment: `process/w1/tu-proofs.tex`. Exact checks:
`process/w1/checks/check_tu_*.py` (shared helper `tu_exact_util.py`).

## Verdict

**Sound with fixes.** Every mathematical claim in the cluster survived a
line-by-line rederivation and targeted exact-arithmetic checks. No critical
issue was found. Two gaps are serious for a journal paper:

- The exact-output argument for nonunique optima imports a recovery lemma
  from a companion note.
- The explicit height and threshold constants are deferred to the companion
  note.

Both gaps are now closed in `tu-proofs.tex`, with complete proofs and sharper
constants. The remaining issues concern notation, citations and wording.

Two new structural-limit results sharpen the open question:

- A tightness proposition shows that the factor `n_c^{p/2}` is really incurred
  by the uniform-mesh algorithm.
- An unsoundness proposition and an example show that graded or non-aligned
  grids with curvature-only corrections give invalid bounds under TU coupling.

## What was verified (questions (a)–(e))

**(a) Feasible correlated corner rounding and the allowance `E_j = n_c L h^2/8`.**

- **Rounding.** Write `x = t + hθ`. The fiber
  `{θ' : Aθ' ≤ (b−Bz−At)/h, 0 ≤ θ' ≤ 1, θ'_i ≤ 0 on grid coordinates}` has an
  integral right side. This holds because `(b−Bz)/h = 2^j(b−Bz)/η` is integral
  by alignment, `A` is integral and `t/h` is integral. Its matrix is TU with
  unit rows appended. By Hoffman–Kruskal its vertices are 0/1. A vertex
  decomposition gives a law on feasible cell corners with mean `x`, and each
  coordinate has two-point variance at most `h²/4`.
- **Boundary cases.** All of these are handled in the fragment's proof:
  - a node coordinate (its variance is forced to zero by the mean);
  - disconnected retained domains;
  - singleton components;
  - points on cell boundaries;
  - integer columns `B` (fixed labels only change the integral right side).
- **Why full directional curvature is needed.** The rounding is correlated, so
  the off-diagonal covariances `Σ_{i≠k} H_ik Cov(Y_i,Y_k)` do not vanish.
  Independent rounding in the box case kills them. The allowance
  `E F(Y) ≤ F(x) + (L/2)E‖Y−x‖²` needs `w^T∇²F w ≤ L‖w‖²` along every
  displacement `w = Y − x`.
  - The report's example (`x1=x2`, `F=2x1x2`, excess `h²/2`) shows that the
    rounding inequality fails with coordinate curvature.
  - I strengthened it to show that the *certificate* itself fails. On
    `{x1=x2}`, `F = 2x1x2 − h(x1+x2)` has `F* = −h²/2`, but every
    feasible mesh-`h` point has `F ≥ 0`. Coordinate curvature is 0, so
    curvature-only corrections certify the false bound 0. `L=2` gives exactly
    the right allowance (Example `ex:tu-fullcurv`).
- **Checks.** `check_tu_rounding.py` covers four TU systems (network, interval,
  `x+y=2z` with a non-TU full matrix, and order constraints) at two levels:
  - no non-corner fiber vertex in any sampled cell;
  - 534 exact Carathéodory decompositions checked for mean, support,
    feasibility and the variance and Taylor bounds;
  - a non-TU control row `x+2y=2` shows non-corner vertices;
  - the full-curvature example is tight.

**(b) Filtering, state count `5+2√(n_c L/g)`, cost formula.**

- **Filtering.**
  - Removals are sound because Lemma 1 keeps `Y_i` in the endpoints of the
    cell containing `x_i`, and keeps labels fixed.
  - The incumbent survives, and its coordinates are nodes of the next grid, so
    `U_j = v_j` and the certified gap is exactly `E_j` at every level.
  - The full-history certificate argument is correct.
  - An empty level-0 grid certifies infeasibility.
- **State count.**
  - A *qualifying* endpoint (not every endpoint; the companion review's
    correction) has a feasible witness `w` with `F(w) ≤ F*+2E_j`. Growth then
    puts it within `a_j=√(n_c L/(4g))h_j` of `S`.
  - Cells add `h_j`. An interval of length `2a_j+2h_j` contains at most
    `⌊4a_j/h_j⌋+5 = 5+⌊2√(n_c L/g)⌋` points of `h_{j+1}ℤ`.
  - This holds for every `j ≥ 0`, giving the bound at levels `≥ 1`.
- **Cost.** The stated `O(p(N+|A|+#rows)[K_0^p+(J+1)K^p])` is correct; it
  slightly overcounts, since level 0 uses `K_0` and levels `1..J` use `K`.
  `J = O(I+q+1)` is correct.
- **Checks.** `check_tu_filtering.py` brute-forces all feasible grid points
  without DP:
  - Instance A: `x+y=2z`, unique optimizer, `g=117/125`.
  - Instance B: two-optima block, `g=1/6`, `L=12`.
  - Over 9 levels it checks the brackets `β ≤ F* ≤ U = v ≤ F*+E`, optimizer
    and incumbent retention, qualifying-endpoint distances, node counts
    against `r(5+⌊2√(n_cL/g)⌋)`, and removal soundness on random feasible
    points.
  - The hull variant of B exceeds the union-type bound at level 7 (69 nodes
    against the bound 68), as expected.

**(c) Exact output: explicit height/determinant bounds via the KKT saddle matrix.**

- **Height constant.** The fragment uses `P = ΔH` (with `Δ` clearing monomial
  coefficients, as in the exact-output section), `C_P = max(1, max|P_xx|)` and
  `M=[A;I;−I]`. It proves the following. Every vertex of the stationary face
  polytope solves a nonsingular saddle system `K=[[P_xx,E^T],[E,0]]`. Here
  `E` is a row basis of the active rows, and `P_xx` is positive definite on
  `ker E`, because the vertex property combines with positive
  semidefiniteness on the optimal face. By Hadamard's row inequality,
  `|det K| ≤ (√2 n_c C_P)^{n_c} ≤ R := (2n_cC_P)^{n_c}`.
- **Derived constants.**
  - Coordinate height: `D_0 R`.
  - Value height: `Ω = Δ(D_0R)²`.
  - Here `D_0` is the denominator of the mesh unit `η`, which covers the
    rational-data case flagged by the companion review.
- **Comparison with the report.**
  - This is much smaller than the report's `R=(4n_cC)^{2n_c}`, which is also
    valid (Leibniz bound on a `2n_c`-dimensional matrix).
  - The saddle lemma is stated for *every vertex of the stationary polytope*,
    not only for a minimum-dimensional optimal face. One lemma therefore gives
    the height bound, the isolated-minimizer case and the recovery lemma.
- **Check.** `check_tu_height.py` uses 60 random indefinite TU QPs with exact
  face enumeration. A global minimizer has denominator dividing `|det K|`,
  `|det K|² ≤ (2n²C_P²)^n`, and the value denominator divides `Δ·det²`.

**(d) Equality-tangent curvature and initial-mesh test.**

- **Equality-tangent curvature.**
  - Both rounded and original points satisfy every equality pair with the
    same `z`, so `Y − x ∈ ker C`. The whole Taylor segment uses that
    direction, so the bound is needed only on `ker C`.
  - `V^T(LI−H)V ⪰ 0` for any basis `V` is exactly right; no orthonormality is
    needed.
  - The projector row-sum bound is valid.
  - It must be an *imposed* equality, not a merely active inequality.
  - The penalty remark (`ρ‖Cx+Ez−a‖²`) is correct but trivial: the penalty is
    identically zero on `X`. Recommend dropping it or reducing it to one
    clause.
- **Initial mesh.** `(b−Bz)/η = (b−Bz⁰)/η − Σ_k B_k(z_k−z⁰_k)/η` gives
  sufficiency. Necessity also holds, because each test is a difference of two
  admissible label vectors. The test costs `1+Σ|Z_k|` vector checks.
  Generalizing the model to rational data aligned to `η` (with `D_0` in the
  heights) merges the "initial mesh" and "rational data" paragraphs.

**(e) Union of cells and the recovery lemma.**

- **Union of cells.**
  - Disconnected domains are harmless because the cell of a non-node point
    lies in its own component.
  - Singleton components need their own test. A singleton test for isolated
    nodes inside interval components is unnecessary: removal of the adjacent
    cells already certifies those points.
  - The per-optimal-value count `r(5+⌊2√(n_cκ)⌋)` is correct.
  - The two-optima example (`g=1/6`, `L=12`) is correct; I reproved the growth
    constant by hand.
- **Recovery lemma.** I proved it fully for TU slices (Lemmas
  `lem:tu-statpoly`, `lem:tu-snap`), with
  `τ = 1/(4m'D_0R)` and distance threshold `τ/(2√n_c)`:
  - it reduces to one integer label slice;
  - the stationary face polytope consists of minimizers;
  - its vertex height is at most `D_0R`;
  - simultaneous slack snapping uses a linear functional with values in
    `(D_0δ)^{-1}ℤ`;
  - every point of the recovery polytope is optimal, with unrestricted
    multipliers.
- **Termination without growth.** Termination needs **only compactness**,
  not Luo–Sturm. Luo–Sturm is needed only to say that the rate statement
  `poly(I)+O(log κ)` is never vacuous.
- **Checks.** `check_tu_recovery.py` uses the fragment's exact constants and
  covers 84 probes within the distance threshold:
  - a diagonal continuum;
  - near-boundary optima that force extra row snapping;
  - the two-optima block;
  - a nonconvex continuum;
  - an optimal face on a TU row.

  It also checks the vertex heights of the stationary polytopes, and shows
  that premature recovery (`x−x²` on `x=t`) returns a nonglobal stationary
  point (value 1/4), which acceptance rejects.

## Issues

| # | Severity | Location | Issue | Fix (done in `tu-proofs.tex` unless noted) |
|---|---|---|---|---|
| 1 | major | extensions.tex §"Nonunique TU minima", paragraph starting "For exact output, the general-polytope recovery lemma in the companion work…" | Exact output for arbitrary optimal sets rests on an imported companion lemma; the paper has no proof. | Self-contained Definition `def:tu-statpoly`, Lemma `lem:tu-statpoly`, Lemma `lem:tu-snap`, Theorem `thm:tu-exact`, with explicit TU constants. |
| 2 | major | extensions.tex §"A complete extension for integral TU fibers", exact-output paragraph ("The companion TU note supplies explicit determinants and thresholds") | Height and threshold constants are not in the paper. | Corollary `cor:tu-height`: `R=(2n_cC_P)^{n_c}`, `Ω=Δ(D_0R)²`, `τ=1/(4m'D_0R)`. |
| 3 | minor | extensions.tex and sections/constraints.tex | `L` and `κ` denote a full-Hessian bound here but coordinate curvature elsewhere, and `\bar\kappa` is now taken by the weighted condition number. | Use `\hat L` (directional bound on `𝒦`) and `\hat\kappa=max{1,\hat L/g}` throughout the TU section. |
| 4 | minor | extensions.tex: "This is classical box integrality \cite{ChervetGrappeRobert2018}" | Wrong primary source. | Cite Hoffman–Kruskal 1956 and Schrijver 1986, Section 19.1 (unit rows preserve TU). |
| 5 | minor | extensions.tex: "A retained endpoint or label has a full feasible grid witness…" | Only a *qualifying* endpoint has a witness (`F(x)=x²` example in the companion review). The numbers are unaffected. | Wording fixed in Theorem `thm:tu-states` proof. |
| 6 | minor | extensions.tex nonunique paragraph | Luo–Sturm is invoked for termination; compactness suffices, and Luo–Sturm is only needed for the rate. | Theorem `thm:tu-exact`(b) uses compactness. |
| 7 | minor | extensions.tex union paragraph and companion note ("Keep a singleton node if its own marginal passes") | It is ambiguous which nodes get a singleton test. | Only single-point *components* are tested alone (algorithm step 3). |
| 8 | minor | extensions.tex: "Correlations in this rounding explain why a diagonal-curvature bound alone would not suffice" | Asserted without an example showing the bound is actually invalid. | Example `ex:tu-fullcurv`, where curvature-only corrections certify a false bound. |
| 9 | minor | extensions.tex penalty sentence | Trivial (the penalty vanishes on `X`). | Drop it, or keep one clause (Remark `rem:tu-curv` covers checking). |
| 10 | minor | sections/constraints.tex draft proof of Theorem `thm:tu`: "Once `E_j<1/(4Δ²R_c⁴)`, every label set is a singleton and every continuous hull is shorter than…" | Reads as if small `E_j` implies short hulls; it does not without growth. The listed conditions are meant jointly. | Reword to state the three conditions jointly, or use the recovery route (Theorem `thm:tu-exact`). The draft's `R_c=(4n_cC_H)^{2n_c}` is valid but much weaker than `(2n_cC_P)^{n_c}`. Not edited (other cluster's file). |
| 11 | minor | extensions.tex `R=D_0R` rational data vs. initial mesh paragraph | "The existing KKT height bound does not acquire a scaling factor just from choosing this mesh" is true only for integral data. | The model in `def:tu-model` allows rational data aligned to `η`; heights carry `D_0`. |
| 12 | minor | extensions.tex cost formula `(J+1)K^p` | Slight overcount (level 0 uses `K_0`). Harmless. | `Σ_j K_j^p` with `K_0`, `K` (Theorem `thm:tu-approx`). |
| 13 | minor (coherence) | exact.tex (box snapping lemma) vs. the TU recovery | Two recovery mechanisms. | The TU lemma is written in the same form as the box version (stationary polytope, then snapping, then acceptance). Keep the box version for its sharper diagonal constants and present the TU one as its polyhedral analog. Optionally state one lemma for `M` with `{0,±1}` rows that specializes to both. |
| 14 | minor | `tu-proofs.tex` LP citation | The exact-output draft cites GLS88 "Theorem 6.4.12" for rational LP feasibility; I could not verify the theorem number. | Cited GLS88 without a theorem number. Verify before submission. |

## Classical vs. new, closest prior work

- **TU cell integrality and feasible corner rounding.** Classical.
  - Hoffman–Kruskal 1956; Schrijver 1986, Chapter 19.
  - Dependent or pipage rounding in approximation algorithms is related in
    spirit (Gandhi–Khuller–Parthasarathy–Srinivasan, J. ACM 2006; *not
    checked this session*).
  - New but elementary: pairing it with a second-order allowance under
    directional curvature, and the observation that only `A` must be TU.
- **Tree DP with 0/∞ row tables.** Classical (junction tree / bucket
  elimination / CSP). Bienstock–Muñoz Theorem 9 is the exact binary analog
  (`O(2^ω n)` LP).
- **Growth-based filtering with feasible rounding.** This includes
  accuracy-independent counts, the union-of-cells representation and the
  finite-projection bound. These are new compositions as far as I know.
  - The closest classical mechanism is **proximity scaling** over TU or
    bounded-subdeterminant matrices for *separable convex* objectives
    (Hochbaum–Shanthikumar, J. ACM 1990; local KB, verified). It also refines
    aligned grids in windows of radius `~ n·scale`.
  - Proximity for (convex) quadratic integer programs: Granot–Skorin-Kapov,
    Math. Prog. 47 (1990) 259–268 (verified by web search).
  - Here the objective is nonconvex and nonseparable, and the window comes
    from growth.
- **Rational height.** The existence of polynomial-size QP optima is classical
  (Vavasis 1990; Del Pia–Dey–Molinaro, Math. Prog. 162 (2017) 225–240,
  verified). The explicit constant using only `P_xx` and `{0,±1}` rows is
  routine but new in this form.
- **Snapping recovery.** The technique parallels optimal-face identification
  in LP (Ye 1992; Mehrotra–Ye, Math. Prog. 62 (1993) 497–515, verified) and
  active-set identification (Burke–Moré, SIAM J. Numer. Anal. 25 (1988)
  1197–1211, verified). Those results need convexity or nondegeneracy. The
  version here has a global nonconvex objective, an arbitrary optimal set,
  unrestricted multipliers and explicit thresholds; I do not know it as a
  standard result, but its ingredients are classical. Claim modest novelty
  only.
- **Existence of set growth.** Luo–Sturm 2000, Theorem 3.3 (local KB).
- **Obstructions** (Propositions `prop:tu-tight`, `prop:tu-misaligned`,
  Example `ex:tu-sum`). New and elementary.
- **Bienstock–Muñoz 2018.** Theorems 4 and 15: scaled-ε-feasible LP of size
  `O((2π/ε)^{ω+1} n log(π/ε))` for mixed-binary polynomial problems with a
  linear objective, and an argument that the pseudopolynomial `1/ε`
  dependence and the coefficient scaling cannot be removed for the class
  unless P=NP (local KB fulltext, §2.0.3). The comparison is in Remark
  `rem:tu-bm`:
  - exact feasibility, but only for TU continuous columns with aligned data;
  - the objective is handled directly;
  - under growth with finite projections the dependence on `ε` is
    `O(log 1/ε)` levels, which does not conflict with their class-wide lower
    bound;
  - without growth the `1/ε` exponent is `p/2` against their `ω+1`, a halving
    from the second-order allowance, and only indicative because the
    tolerances are normalized differently;
  - neither result contains the other.

## Placement recommendations

| Result | Recommendation | Reason |
|---|---|---|
| `def:tu-model`, Lemma `lem:tu-round`, Lemma `lem:tu-allow`, Example `ex:tu-fullcurv` | main | The key mechanism of the constrained extension. The example justifies the full-Hessian hypothesis concretely. |
| Proposition `prop:tu-sound` | main (short) | Mirrors the box certificate. Without growth and uniqueness. |
| Theorem `thm:tu-states` (union, set growth, finite projections) + continuum remark | main | Subsumes the unique-optimizer hull theorem (case `r=1`), so one statement replaces two. |
| Theorem `thm:tu-approx` | main | The complexity statement. Also states the XP character honestly. |
| Lemma `lem:tu-statpoly`, Corollary `cor:tu-height`, Lemma `lem:tu-snap`, Theorem `thm:tu-exact` | statement in main, proofs in appendix | Complete exact output for arbitrary optimal sets. Parallels the box exact-output section. |
| Remark `rem:tu-cf` (continued-fraction reconstruction, unique case) | remark | Optional, LP-free route. |
| Proposition `prop:tu-align` (alignment test), Remark `rem:tu-curv` (tangent curvature checks) | remark/appendix | Practical. Short proofs. |
| Example `ex:tu-union` (two optima per block) | main or appendix | Shows why unions, not hulls, are needed. |
| Proposition `prop:tu-tight` | main, in "structural limits" | Shows the `n_c^{p/2}` factor is real for the algorithm, not slack in the analysis. Fits the paper's "structural limits" story. |
| Proposition `prop:tu-misaligned` + Example `ex:tu-sum` | main, in "structural limits" | Explains precisely why the box FPT theorem does not transfer. |
| Remark `rem:tu-hybrid` (only coupled coordinates need uniform meshes) | remark (outline) or drop | Correct in outline. I did not write out the full proof (initial pseudopolynomial levels, common aligned mesh for coupled coordinates). Keep it only as a clearly labelled outline. |
| Remark `rem:tu-bm` (Bienstock–Muñoz, Hochbaum–Shanthikumar) | main text, related-work paragraph | Needed to place the result. |
| Penalty `ρ‖Cx+Ez−a‖²` paragraph | drop | Trivial. |
| Network/interval application sentences | one sentence in main | Useful, but the width cost of conservation rows must be stated. |

## Open questions and development (question (f) and others)

**(f) Width-FPT under coupled constraints.**

- **Precise failure of graded grids.**
  - **Cell integrality.** After scaling a cell with widths `w` to the unit
    cube, the constraint matrix becomes `A·diag(w)`. This is generally not TU,
    and the scaled right side is not integral.
  - **Sum rows (≥3 nonzeros).** A common graded offset pattern around a
    *feasible* center already gives non-corner fiber vertices. Example
    `ex:tu-sum`: on `x1+x2=x3` in `[0,3]³` with the box-theorem grid
    `{0,1,9/4,3}` (`h=1`, `θ=1/4`), the corrected grid minimum is `31L/64`,
    while `F*=0`. So the bound is invalid with no multiplier effect. An exact
    search also finds a violating optimizer only `√(37/8)` mesh widths from
    the center, so this is not a far-field artifact.
  - **Difference rows `x_i−x_j ≤ c`.** With a common pattern, threshold
    rounding (one shared uniform variable) preserves every row that is
    *tight at the center*. This is my development: the rounding is monotone
    when both coordinates share a grid. Rows with small positive slack break
    alignment. Proposition `prop:tu-misaligned` shows that this is fatal for
    *any* correction depending only on (`L`, `g`, grids): the order-row
    multiplier `λ` is unbounded at fixed `L`, `g`. This is the grid analog of
    the constraint-obstruction note's multiplier phenomenon.
- **Clean obstruction for uniform meshes (Proposition `prop:tu-tight`).** On a
  box instance with one redundant TU row (which forces a bag of size `p`),
  `κ̂=2`, the algorithm keeps exactly `4⌊√n_c/2⌋+5 ≥ 2√n_c+1` nodes per
  coordinate at every level once the window fits in the box. That is at
  least `(2√n_c+1)^p` table entries per level, within a factor `√2` of the
  upper bound. Exact simulation for `n_c ∈ {4,…,400}` matches the formula.
  So the XP factor is intrinsic to uniform meshes. Combined with (a), the
  constraints force uniformity in the coupled coordinates.
- **Partial positive result (outline only).** Coordinates that occur in no
  coupling row can keep graded grids. The non-FPT factor becomes `n^{p_c/2}`,
  with `p_c` the largest number of coupled continuous coordinates in a bag
  (Remark `rem:tu-hybrid`). I verified the two properties the growth-section
  proofs need:
  - the composite rounding inequality, under block curvature on coupled
    coordinates and coordinate curvature on free ones;
  - the mesh bound.

  I did not write out the initial pseudopolynomial levels or the constants.
  Status: partial.
- **What failed.**
  - **Special TU classes.**
    - Difference *equalities* are trivial by elimination: contraction is a
      minor, so width does not increase.
    - Difference *inequalities* (order constraints) need an activity margin
      `γ`, since each row must be either tight at `x*` or slack by `≥ γ`. Even
      then, the early levels, where windows exceed `γ`, still pay the uniform
      cost `(n κ)^{p/2}` per level. The window/mesh ratio `√(nκ)` is
      level-independent, so the margin does not help.
    - Interval matrices via prefix sums become difference systems, but they
      require a common period-1 grid. That grid must be fine near every
      `x*_i mod 1`, so it can need `Ω(n)` nodes per window.
    - Network conservation rows are sum rows and fail as in `ex:tu-sum`.
  - **Lagrangian dualization of rows.** This keeps curvature and scopes and
    gives valid bounds by the box algorithm. But nonconvex duality gaps, and
    the lack of box growth for the Lagrangian, block a general theorem.
  - **Sharpened open question.** Is there an `f(p,κ)·poly(I)` algorithm for
    TU-coupled sparse QPs with growth? Any such method must use non-unary
    (row-coupled or multiplier-aware) corrections or a non-grid
    discretization. A general lower bound beyond the uniform-mesh method
    remains open.

**Other open points.**

- **Pseudopolynomial `K_0` for large capacities.** Relaxed right sides
  `⌈(b−Bz)/s⌉s` keep the lower bound valid, because rounding maps `X` into the
  relaxed grid set. But filtering needs a *feasible* incumbent with `U ≤ F*+O(E)`
  at coarse levels. Repairing a relaxed point costs first-order (Lipschitz or
  multiplier) constants that are unbounded at fixed (`L`, `g`). Open. The
  sharpened statement is that a first-order parameter is needed.
- **Positive-dimensional optimal sets.** Accuracy dependence is unavoidable
  for uniform product grids: domains must contain `S_i`, giving at least
  `|I|/h_j−1` nodes. This is proved in the remark after Theorem
  `thm:tu-states`. Graded representations for continua under coupling remain
  open.
- **Exact output for non-quadratic (polynomial) objectives under TU.** Not
  addressed. Outside the cluster.

## Checks run (targeted, all passed)

All runs were from `paper-decomposition-aware/process/w1/checks/`, using
`python3 -B <script>`:

- `check_tu_rounding.py`: 4 TU systems at levels 1–2.
  - No non-corner fiber vertices.
  - 534 exact decompositions checked for mean, support, feasibility,
    `Σ Var ≤ n_c h²/4`, and `E F(Y) − F(x) ≤ (L/2)ΣVar ≤ n_cLh²/8` for random
    quadratics.
  - The non-TU control shows non-corner vertices.
  - The full-curvature example is tight.
- `check_tu_filtering.py`: brute-force union and hull filtering, 9 levels, on
  the unique `x+y=2z` instance and the two-optima block.
  - Brackets, retention, qualifying-endpoint distances, node bounds and
    removal soundness all hold.
  - Hull node counts outgrow the union-type bound, as expected.
- `check_tu_height.py`: 60 random indefinite TU QPs, using exact face
  enumeration and the Hadamard bound for the saddle matrix.
- `check_tu_recovery.py`: 84 recovery probes with the fragment's constants,
  plus stationary-polytope vertex heights and a premature-recovery rejection.
- `check_tu_obstructions.py`:
  - uniform-mesh tightness for `n_c ∈ {4,9,16,25,100,400}`;
  - misaligned order-row unsoundness: `827/7200` for the simple grids, about
    `0.245` for graded grids around `3/10` and `7/10`;
  - sum-equality unsoundness: smallest violation `3/64` near the center, and
    exactly `31/64` on `[0,3]³`.
- The fragment compiled with `pdflatex` through a minimal wrapper
  (`checks/tu_latex_build/wrap.tex`) with no LaTeX errors. The only undefined
  references are labels and citations from other sections.

These finite checks support the proofs. They do not replace them. No
project-wide verification and no CI inspection were done.

## Bibliography entries needed (not in `references.bib`)

- **HoffmanKruskal1956.** A. J. Hoffman, J. B. Kruskal, "Integral boundary
  points of convex polyhedra", in *Linear Inequalities and Related Systems*,
  Annals of Math. Studies 38, Princeton, 1956, 223–246. Verified by web
  search.
- **Schrijver1986.** A. Schrijver, *Theory of Linear and Integer Programming*,
  Wiley, 1986. Cited for Section 19.1 and Chapter 20. The edition and section
  numbers were not rechecked this session.
- **HochbaumShanthikumar1990.** D. S. Hochbaum, J. G. Shanthikumar, "Convex
  separable optimization is not much harder than linear optimization",
  J. ACM 37(4) (1990) 843–862. Local KB.
- **DelPiaDeyMolinaro2017.** A. Del Pia, S. S. Dey, M. Molinaro,
  "Mixed-integer quadratic programming is in NP", Math. Program. 162 (2017)
  225–240, doi 10.1007/s10107-016-1036-0. Verified by web search.

Already present: `BienstockMunoz2018`, `Vavasis1990`,
`GrotschelLovaszSchrijver1988`, `LuoSturm2000`. Ye 1992, Mehrotra–Ye 1993,
Burke–Moré 1988 and Granot–Skorin-Kapov 1990 appear only in this report
(verified by web search). Gandhi et al. 2006 was not checked.
