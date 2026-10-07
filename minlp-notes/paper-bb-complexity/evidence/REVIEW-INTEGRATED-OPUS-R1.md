# Integrated manuscript review, Opus round 1

**Disposition: PASS for the frozen, delivered manuscript, with six minor
optional precision edits and one optional literature check.** I found no
substantive mathematical, hypothesis-consistency, novelty-scope, or
abstract/body defect. Separately, a transient post-freeze overwrite of three
chapter files occurred during this review. The files were restored before
this report was written; one confirmation step for root remains
(Section 2).

Reviewer: independent Opus delegated review, new T3 round
(`bb-paper-review-integrated-r1`, run ordinal 2, which resumed with "continue
where you left off"). The review is complete; no rate limit occurred. This
file is the only file I wrote in the repository.

## 1. Versions and read scope

All 29 frozen submission inputs matched `delivery/source-freeze.json`
(frozen 2026-10-06T04:25:39Z) at 05:50:38Z, and again at 06:21:27Z, after
the restoration described below. Selected hashes:

| File | SHA256 |
|---|---|
| `main.tex` | `210e17b7e1193f329bffb16fed02e47ce3dd45ec8df05f2a6333d3f819f6e770` |
| `sections/abstract.tex` | `ef5d8464f1c0df6662d7476a9afad3a770a0a963959310b5e8d908ed5a95e269` |
| `sections/introduction.tex` | `babc03bcd1f337123b36d793dbc37b8319ad5dfb5156c3e5cbee93342693254a` |
| `sections/regression.tex` | `abb0dd9920afe7fcfe466c766d4c38e2982bb4ff4dadcaa3c9776e047d600d09` |
| `appendices/regression-proofs.tex` | `759760aff46a9376db68a325f9207a642bd0c3d02b0957d404c2db59fc8274a9` |
| `sections/experiments.tex` | `455ef17d3c7ec4042e93d2b3d01f8e283813e6db9942c13debbdea17a5c47350` |
| `sections/binary-least-squares.tex` | `bd256b308009b27da0bf3bd01b6fff6bb4ac645b978bdfd54054aec1b3ed7043` |
| `appendices/bls-proofs.tex` | `8fb602516aba588cceee13ced87b89d2799ca05db1498cc1400c55405ffe8e6c` |
| `references.bib` | `9409dbc80bc83a5888806b2a7e6efb014f47af1623bb930ec4d5e2c7fc2c9d32` |

The other 20 inputs have the hashes recorded in `source-freeze.json`. The
delivered `main.pdf` (`42ac972a…298fe`), source ZIP (`ecddcd20…ded6d`), and
evidence ZIP (`6143dc1f…e190`) matched `delivery/ARTIFACTS.json` at
06:21:27Z.

While the working tree was modified, I read the regression chapter, its
appendix, the experiments chapter, the BLS chapter, and the BLS appendix
from an extraction of the verified source ZIP. The extraction is
`/tmp/bbreview/frozen`, and all 30 entries in its `SHA256SUMS` passed. All
other files were read in the working tree while they matched the freeze.

Read in full: the abstract, all twelve main sections, all eight proof
appendices, the three tables, the figure caption, `main.tex`, and
`macros.tex`. I cross-checked bibliography keys: 32 unique cited keys, all
present; 38 entries, of which 6 are uncited and harmless with natbib. I also
read `BRIEF.md`, `AUTHORING-CONVENTIONS.md`, `ARCHITECTURE-DECISION.md`,
`ISSUES.md`, `INCOMING-AUDITS.md`, `STATUS.md`, `FINAL-VERIFICATION.md`,
`SUBMISSION-CHECKLIST.md`, `KB-HANDOFF.md`, the scope and gap sections of
`LITERATURE.md`, and keyword searches of the prior `REVIEW-*`,
`REVIEW-RESOLUTION`, `COVERAGE-FINAL`, and `AUTHOR-*` reports to check
whether my findings had already been raised.

Not done: no TeX build, solver run, experiment rerun, literature browsing,
project-wide check, or CI inspection. I did not inspect every PDF page; the
editorial review and root's build record cover the layout.

## 2. Transient overwrite of frozen sources (now restored)

Observed sequence (UTC):

- 05:50: about 13 Claude sessions resumed with `--resume`, including this
  review and the earlier rate-limited Opus writer threads
  `bb-paper-write-regression-r1` and `bb-paper-write-experiments-r1`
  (parent `28ea4d58-2a6a-4267-9b65-3405b5386891`). The parent's last run had
  completed at 04:54:46.
- 06:03–06:13: the writers replaced `sections/regression.tex` (69,944 B),
  `appendices/regression-proofs.tex` (twice), and `sections/experiments.tex`
  (twice). They also created `tables/empirical-{exponents,mechanisms,kinks,
  minlplib}.tex`.
- At 06:10–06:13 the working tree was inconsistent: the new regression
  chapter removed nine labels used by the introduction and appendix
  (including `regression:window`), referenced five undefined
  `app:regression-*` labels, and cited `atamturkGomez2019SafeScreening`,
  which is absent from `references.bib`.
- 06:15:21 and 06:17:46: `experiments.tex`, `regression.tex`, and
  `regression-proofs.tex` were rewritten with exactly their frozen bytes,
  and the four new tables were deleted. The writer threads reached
  `completed` at 06:18:05 and 06:19:22.
- 06:21:27: all 29 inputs and all 3 delivery artifacts again matched their
  recorded hashes. No other file under `paper-bb-complexity` changed after
  05:45, except the evidence files `ARCHITECTURE.md` and
  `COVERAGE-INITIAL.md` (05:55, not submission inputs) and this report.

Requested root confirmations; I made no edits outside this file:

1. Rerun the read-only release guard (the `release-check.json` comparison),
   because three frozen files now have new mtimes with unchanged hashes.
2. Confirm that both writer threads are terminal and will not resume again.
   If an Opus rewrite is wanted, run it in a separate copy. The frozen
   chapters are complete and correct as reviewed.
3. Optionally check the 05:55 edits to `ARCHITECTURE.md` and
   `COVERAGE-INITIAL.md`. Both are superseded internal evidence, not
   submission inputs.

## 3. Mathematical verification by chapter (frozen versions)

I reconstructed each argument at the level of its displayed inequalities.
Unless a minor item in Section 5 notes otherwise, every statement and proof
below checked out.

- **Certificates (§2).** The ownership construction gives disjoint
  half-open owners and at most 2n slab owners per same-relaxation round.
  Slab validity follows from q_C ≤ q_B and the pointwise gap. The counts
  K_F ≤ ℓ_aug + 2nR_rel, T_aug ≥ H/(1+2nr), and K_eval ≤ (2n+1)S_eval are
  correct. The closed-slab counterexample is correct.
- **Geometry (§3, App. A).**
  - Vertex covering bound; arcsine lemma, including the constant
    (π²/d)^{d/2}·C(n,d)^{1/2} via J_I ≥ C(n,d)^{−1/2}.
  - Localization lemma: 5^n neighbor count and level sum. Running-supremum
    comparison (2.4) and its √2/2^n equivalence.
  - Quadratic-growth exponent and manifold corollary. Stratum integral
    comparison: separated-family packing and the Tonelli geometric sum.
  - Owned tube dichotomy and the infeasible-witness cover.
  - Nonlinear KKT transfer: the e₀ construction, IFT, the descent and
    violation constants, the a = η+ε covering step and α_eff = μβ/(12c),
    the injectivity and contraction of Ψ_ε, the uniform multiplicity via
    Lemma A.1, the Jacobian bound j_*, and the radial logarithm.
  - Regular KKT corollary: quadratic growth, sharp growth, and the exact
    grid certificate constant K′. The odd-denominator middle position.
  - McCormick gap formulas and zero set; flat graph theorem (centroid at
    least W/(p+1), τ ≥ Δ); curved transversal strata; fractional cover with
    the substitution w_i = W(ρ/W)^{2z_i} and a half-integral optimum;
    matching slices; one-sided ray (limit-interval argument); 2D aligned
    certificate (constancy of transverse derivatives and endpoint products
    for both signs of c); 3D aligned example (lower bound 1/(2√ε) and
    O(2^j) unpruned cubes).
  - Many-wells example: f″ ≥ −4π² − 4e^{−3/2}, ε_K = 0.2K^{−2}, and the
    count of at least K/2.
- **Face integrals (§4, App. B).**
  - Per-face arcsine lower bound.
  - Projection lemma, with constants (1+n−d) and K_n = (n+2)²/4.
  - Dyadic packing with the 8^n count. Vertex levels absorbed into an edge
    integral, (3M/2+1)^{−1/2}·log₊(s₀/ρ). Affine rescaling.
  - Regularized-integral lemma in all three regimes, including the extra
    logarithm at λ = a.
  - Full-box dominance: ‖∇m‖² ≤ 2Mm, the 4^{−d}t^{(n−d)/2} volume
    transfer, and the layer-cake bound.
  - Interior/Morse corollary, including λ ≤ (n−1)/2+1/3 for a Hessian null
    vector.
  - Examples: the x⁴ rate; the ζ = 4/(1−2z)² pair (1/2, 2) with
    I ~ πε^{−1/2}log(1/ε); and the boundary-face example, with pairs
    (7/4, 1) on D and (3/4, 1) on F, giving ε^{−3/4}.
- **Decomposition (§5, App. C).**
  - Validity and reuse chain; unfolding lemma; shell partition with
    (J+1)(4/θ)^d members.
  - Existence proof: the drift recursion d ≤ b + Γd with ‖Γ‖₂ ≤ 1/2 (row
    sums (k−1)·4θ, column sums 4θD_k); the K₁ bound; the slope telescoping
    identity; the E ≤ (3c_g/4)X*² + MH₀h² chain.
  - Path family: the growth bound f ≥ 0.1‖x‖²; det H_n = (4/3)(8/5)^n −
    (1/3)(2/5)^n; Πα = (4/5)^n/4; the Stirling constant (> 0.068); the
    scalar inequality maximized at s = 2/5; the volume bound (3/5)^n·e^{…};
    the parameters Q = 159, H₀ = 122114.4, θ = 2^{−10} (condition value
    0.0291 ≤ 0.05); the bound 2·4096²; the two-case uniform ratio; and the
    McCormick transfer.
- **Propagation (§6, App. D).**
  - Greatest fixed box, preservation, continuity along decreasing boxes,
    threshold attainment, and Z ⊆ Z₀(Π_xZ).
  - Flat-sum formula, both directions. The −3, 2, 2 example: Φ([−a, a]) =
    −a², same-side subintervals give min x², and intervals crossing zero
    give ≥ −1.
  - One-sided corollary, including the G_k decomposition; the h(z)
    expansion; local exactness via the integer potential; the witness
    lemma.
  - Coordinatewise loss: the Taylor remainder K₀; the localization
    δ < 2g/d₀; the phase preservation of H_Φ with inherited boxes; and the
    covering and integral transfers.
  - Aggregate-loss arc and integral bounds.
  - Slow schedule: the updates y′, x′, the potential drop ≤ 4√ε/a, and the
    (π/8)aε^{−1/2} count. Fast schedule: 2U_{k+1} ≤ (2U_k)².
- **Branching (§7, App. E).**
  - 4-competitive proof: the crossing inequality
    t₁(λ−t₁) < (t₁−t₂)(e−t₁) and the 4N−5 count.
  - Five-node refinement.
  - Information pair: lines, germs, unique breakpoints, and the 5/3 and 4/3
    ratios; smoothing.
  - Dimension obstruction: margins 11/200 and 3ε/(8(n−1)), corner
    invalidity, and Σ2^d(n−d) = 2^{n+1}−n−2.
  - Persistent clamp fixed point. Safety bound J =
    ⌈log(θ/a)/log(1/θ)⌉ and recentring 2J+3. Multisection separation
    (F_x, spine, (5/36)16^{−k}).
  - Phase lemma (κ(κ+1) steps, c_κ) and the sharp induction (b ≥ ε,
    frontier refinement, C_r recursion, slice argument).
- **Integer classes (§8, App. F).**
  - Lower bound and semantic attainment: the hemispace induction and the
    binary chain coverage at the final split.
  - Removal accounting and the binary (n+1) factor.
  - Linear descriptions (see minor item m1).
  - Jeroslow-type parity count binom(n+1, h).
  - Lattice-free facets, using BCCZ as the external input.
  - Siegel/torus moments with Var = V; cap occupancy (pairwise negative
    inner products, at most n+1).
  - CVP lower bound: (3/2)(1−δ)² − q and the failure terms.
  - Spherical cap cover; CVP upper bound (sinθ = 1/R₊ and √a₊ ≥ √τ/g_n).
    The exponent bounds ½·log₂(3/2−q₀) and ½·log₂(2−q₀) are correct.
  - Midpoint clique: η = (2−ρ)/ρ, a² = 4(ρ−1)r₀²/ρ, monotonicity iff
    ρ ≥ 2/n.
  - Curvature gadget: block minorant with π, midpoint conflict, hull root
    value OPT, and the rational family.
  - Path lemma and its examples.
- **Sparse regression (§10, App. G; frozen).**
  - Exactness condition and strict version; capped witness identities;
    certificate bound τ² < n/k; the 2k+1 removal-half certificate.
  - (a) root two-sided threshold.
  - (b) C1 proof: Π ≤ C√n·p^{−δ/8}, Γ bound, M ≤ m₀(1−ζ+3γ₁), m² − M² ≥
    (2−o(1))ζm₀², ratio → 0.
  - Forced-in primal lemma (budget identity and rearrangement) and the (c)
    converse.
  - Ridge optimization and the window corollary.
  - Hull calculus, mixture lemma, completion (Schur complements), and the
    lift thresholds with helper halves.
  - Integer-optimum lower bound (exponential Markov); hard theorem
    (parameters with 2x > e^x − 1, packing, χ² union, midpoint value
    B₀/(B₀+A), planted variant, uniform design event for the ℓ₂
    completion).
  - Variance price. Fixed-dimension PWE limit, including the global
    transfer through the event U_n.
- **Binary least squares (§11, App. H; frozen).**
  - Recovery Chernoff bound (λ = 1/4), value gap (0.28x split, c₀),
    planted root probability 2^{−N}, and the global vertex bound (λ = 2).
  - Sign-orbit identity; Student density via H = GT^{−1/2}; coefficient
    mixture; projection mixture; concentration with the factor 2t.
  - Finite tail sum (n/2)q^{M−n+1}((1+q)/2)^{n−1}.
  - Simultaneous C1: q_θ, union over N nodes, the expansion r_i − W =
    N[2θ(2β_N−1) − ½] + O(√(N log N)), and the threshold
    θ_c = 1/(4(2β−1)).
  - Root cutoff: pathwise ρ_box and the scale log N/(2β_N−1); finite tail.
  - Static-order upper bound: a_N, η_N, L_N, the union count, node count
    1 + 2Σbinom(N, i), and (eN/K)^K.
  - Entropy lemma and convex-piece lower bound: barycenter identity, X/W <
    1/2, Σp_i² ≥ λk, c_β·(N/ρ)·log ρ − log(8N).
- **Experiments and discussion.** Theory references are consistent:
  - predicted exponents p/2, n/2 − Σ1/q_i (qflat), and additive growth at
    nondegenerate minima;
  - a = 1/6 is exactly the persistent-clamp fixed point for clamp 0.2;
    recentring gives 5 = 2J+3 nodes with J = 1;
  - C1 constants 1/4 and 1/12.
  The archived numbers were trusted as instructed.

## 4. Targeted identity checks actually run

All scripts are in `/tmp/bbreview/`. I ran each with `python3 -I`, outside
the repository.

- `check_branching.py` (exact fractions): the eleven-node example gives T =
  11, with the five invalid nodes, unique minimizers, and values exactly as
  tabulated. The three-piece certificate minima are 209/160000, 0, and
  209/160000. The two-piece exclusion constants are a = 12209/30000 and
  1 − a = 17791/30000.
- `check_lattice.py` (exact fractions): gadget values 16/5, 48/25, 48/25,
  16/13, and 16/9; d₀ = 32/225; improvement difference 192/325.
- `check_nnls.py` (Monte Carlo, 40,000 draws, M = 6, n = 4, a = 0.7,
  c = 1.3): support sizes match Bin(4, 1/2); conditional coefficient
  quantiles match (c/a)|Z|/√χ²_{M−s+1} for s = 1, …, 4; mean fitted and
  residual energies match χ²_s and χ²_{M−s}. This is a sanity check, not a
  proof.

## 5. Findings

**Substantive:** none.

**Minor, optional precision and wording edits.** None blocks submission.
Line numbers refer to the frozen files, which are identical to the current
working tree.

- **m1.** `sections/lattice.tex` 246–249 and proof 258–263
  (`lattice:linear`): the mixed clause reads "For a rational mixed-integer
  linear relaxation". The proof calls the sublevel polyhedron
  "integer-free", which requires φ(x) > τ at every integer x. This holds
  for the natural LP relaxation of a MILP, where φ equals the exact fiber
  value, which is at least OPT > τ. It can fail for a polyhedral relaxation
  of a nonlinear problem. Example: C = [0, 3], f = (x − 3/2)² + 1, K̂ = C,
  φ̂ ≡ 1, τ = 1.1 < OPT = 1.25. Then the sublevel set [0, 3] has q = 2
  rows, but κ = +∞. Suggested fix: "For a rational mixed-integer linear
  program with its natural LP relaxation (so φ(x) ≥ OPT at every integer
  x)". This matches the hypothesis already stated in the appendix's
  constrained variant.
- **m2.** `sections/geometry.tex` 434–440 (`geom:thm-tube-kkt`): "on a
  fixed relatively open feasible patch S of that manifold" should be
  existential and centered: "there is a fixed relatively open feasible
  patch S containing z_*". The proof constructs S around z_*, and the
  log(1/ε) lower bound fails for a patch away from z_*. The development
  review states it this way.
- **m3.** `sections/discussion.tex` 99–101: "while a particular lifted
  representation has a much smaller round count" suggests a second
  representation of the same quadratic. The fast example
  (u = t², v = u², f = u − 2v) is a different objective. Suggested
  wording: "while a different exposed-endpoint graph empties in
  O(log log(1/ε)) rounds".
- **m4.** `sections/introduction.tex` 156–158: "A two-dimensional convex
  example with an aligned optimal segment has a two-leaf exact certificate"
  understates `geom:prop-aligned-two`. That proposition covers g + cxy with
  g convex, so f itself may be nonconvex. Suggested wording: "A
  two-dimensional convex-plus-bilinear example".
- **m5.** `sections/geometry.tex` 302–304 vs 328–330
  (`geom:thm-integral`): the hypotheses fix d_k ≥ 1, but the theorem then
  discusses strata that are finite sets. Suggested fix: phrase the last
  sentence as a remark ("If finite zero-dimensional strata are added, …").
- **m6.** `sections/regression.tex`: within one chapter, M denotes both the
  maximum null correlation (line 130) and M_S (line 60). κ (lines 358–359)
  denotes the SNR limit, while κ_τ is the class number elsewhere. Renaming
  them (for example C_max and ν) would avoid confusion. Very minor.

**Literature need, routed to the Luna lead (I did no browsing).** The
bibliography holds an uncited, post-cutoff entry: Papailiopoulos (2026),
arXiv 2609.19405, "Polynomial-Time MIMO Detection at the Maximum-Likelihood
Threshold", v1 dated 16 September 2026. It is excluded under the recorded
10 September cutoff. Section 11 opens by separating finding an optimal
vertex from certifying it with the box relaxation, so a one-sentence
concurrent-work mention may help a referee. Luna should read the source and
decide whether it overlaps any BLS claim. It cannot affect the proofs.

## 6. Hypotheses, novelty, narrative, and abstract agreement

- **Hypothesis consistency.**
  - Every chapter states its own oracle, incumbent, and cost measure.
  - Covers, partitions, and trees, and their counting units (leaves vs
    nodes, owned events, evaluations, rounds), stay distinct throughout.
  - The C1 path lemma (§8) is used consistently in §10 and §11, including
    the strict-bound/best-bound variant and the requirement that the
    singleton supplies a feasible extension.
  - The helper-column convention, planted-vs-global distinction, sandwich
    hypotheses, and qmax < 1 appear wherever they are used.
  - The compatible original exact/relaxed tuple is required in both the
    theorem and the corollary.
- **Novelty scope.** Claims are bounded and attribute prior work:
  - classical McCormick and αBB formulas, Lin's analytic asymptotics,
    Gaussian cone laws (Hug–Schneider, McCoy–Tropp), the PWE
    reformulation, Dey–Dubey–Molinaro midpoint conflicts, and FBBT fixed
    points;
  - the decomposition separation is limited to the fixed path family and
    oracle.
  The ledger's "no universal first claim" holds for the manuscript text.
  The PWE limitation is phrased precisely and narrowly.
- **Narrative.**
  - The introduction maps each result paragraph to its theorem, and Table 1
    gives the model-by-model scope.
  - The discussion separates obstruction, search, and statistical-event
    interpretations.
  - The chapters read coherently despite the 125-page length.
- **Abstract/body agreement.** I checked every abstract sentence against
  the cited results: profile comparison; all-face characterization;
  analytic rates; McCormick, constraint, propagation, and branching
  analyses; path separation; 4-competitiveness; class number;
  sparse-regression window; BLS certificate law; C1 and orthant
  thresholds; NNLS bound; separation of costs. All agree with the body.

## 7. Disposition

The frozen manuscript is correct and submission-ready as reviewed. Items
m1–m6 are optional precision edits. If any is applied, it needs a narrow
re-review, rebuild, and repackage. Root should complete the two
confirmations in Section 2 before treating the current working tree as the
final delivery state.
