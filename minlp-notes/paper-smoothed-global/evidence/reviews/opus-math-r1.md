# Opus mathematical review, round 1: complete-proof-draft-r1

Reviewer: Opus 5.5 (`claude-opus-5-5`), maximum effort, delegated review
round 1. Completed 2026-10-06.

Target: the immutable snapshot
`evidence/snapshots/complete-proof-draft-r1/` (20 TeX files and
`manifest.json`; the bibliography is pending by design). This is a review of
that snapshot's written proofs and cross-route interfaces. It is not approval
of the final paper.

An earlier session of this same review stopped at a provider limit and left
only a progress note, `reviews/opus-math-partial-r1.md`, with no findings.
This report is the completed round-1 Opus mathematical record for the
snapshot and replaces that note. In this session I re-read all 20 snapshot
files in full.

Several parallel and later reviews exist. I read the live integration
contract and the complete Sol reviews of the same snapshot
(`complete-recourse-sol-r1.md`, `complete-sparse-domain-sol-r1.md`) only to
avoid reporting their findings as new. Later snapshots (up to
`final-submission-r4`) are outside my scope. I searched them only to say
whether my new findings persist there.

**Locators.** `NN:L` means `sections/NN-*.tex` line `L`, and `X:L` means
`appendices/X-*.tex` line `L`, both in the r1 snapshot.

## Snapshot integrity

| Check | Time | Result |
| --- | --- | --- |
| Before review | 2026-10-05T23:00:47-04:00 | All 20 files match manifest SHA-256, byte count, and line count |
| After review | 2026-10-06T01:53:26-04:00 | All 20 files match; no file added or removed (20 sources + manifest) |

`manifest.json` SHA-256:
`d9ca80c5c376344069ed0fec75fac23470b5bdbb85b89a424e8ff9a9a07462c7`
(unchanged before and after).

## Decision

**No theorem-invalidating or subject-defeating defect.** I checked every
substantive proof in the snapshot (Section 2 below). Every theorem's intended
statement is supported by its written proof, up to the localized repairs
listed in this report.

**Appendix F's solver proof is correct.** The joint critical-limit solver
handles poles, repeated roots, and reconstruction rigorously (Section 2.6).
The appendix proves more than the Section 8 summary text says, and the
summary text is where most of the known solver corrections lie.

**The snapshot is not publication-ready.** The blockers are:

1. The known pending integrations that are still absent from r1
   (Section 1.4). The most important are the common-root output of the
   general fallback, the solver's value map and integer root polynomial,
   the Gaussian two-direction accuracy bound, the empty mixed-feasibility
   contract, the simplex equality-multiplier exclusion, and the coverage
   additions A0, B10, X8, X15 (direct Square Root Sum), and X16.
2. Six new local findings (Section 1.2). One is a proof gap in a lemma
   that the bilinear-flow and bilinear-TU results need for polynomial
   sampling precision. The written argument is invalid as stated, although
   the lemma is true and the repair is one line. That gap is still present
   verbatim in `final-submission-r4`. The other five are interface or
   editorial corrections.

## 1. Findings

### 1.1 Theorem-invalidating or subject-defeating

None found.

### 1.2 New findings

These items do not appear in the earlier reports, the live integration
contract, or the parallel complete reviews of this snapshot, as far as my
searches show. Severity scale: *proof gap* (conclusion true, written argument
invalid), *interface* (contract, encoding, or scope mismatch between
results), *editorial*.

| ID | Kind | r1 location | Still in `final-submission-r4`? |
| --- | --- | --- | --- |
| NEW-1 | proof gap | F:803–807 (`lem:int:affine-margin`) | yes, verbatim, F:945–950 |
| NEW-2 | interface | 02:116–118 versus 08:533–539, F:964–976 | yes, 02:119–121 versus 08:676 |
| NEW-3 | interface | 08:561–562 | no; 08:711 now cites `thm:count:cells` |
| NEW-4 | interface | 03:556–562 | sentence not found verbatim (grep only) |
| NEW-5 | interface | 02:322–324 | yes, 02:398–400 |
| NEW-6 | editorial | 04:577–579 | yes, 04:638 |

**NEW-1. Proof gap in the affine margin lemma.** `lem:int:affine-margin`
(F:795–811) asserts, for a nonzero affine `p(x)=p_0+π^T x` on `[0,1]^q` with a
nonempty zero set `Z_p`, that `|p(x)| ≥ 2^{-H_0} dist(x, Z_p)`. The proof
(F:803–807) takes *some* vertex with `p ≤ 0`, moves toward it one coordinate
at a time, and claims that `p` decreases at rate at least `π_min` along the
whole path. For an arbitrary vertex with `p ≤ 0` this is false, and so is the
resulting path-length bound.

Counterexample to the written argument: take `q=2`,
`p(x)=x_1-2x_2+1/2`, `x=(0,0)`, so `p(x)=1/2` and `π_min=1`. The vertex
`(1,1)` has `p=-1/2 ≤ 0`. Moving `x_1` toward it, from 0 to 1, raises `p`
from `1/2` to `3/2`, so the claimed monotone decrease fails. If coordinate 1
is moved first, the zero is reached only after an `ℓ_1` path of length
`7/4`, while the claimed bound is `p(x)/π_min = 1/2`. The lemma itself holds
here: moving `x_2` to `1/4` reaches `Z_p` at distance `1/4`.

Repair: use the vertex that minimizes `p`, namely `v_i=0` if `π_i>0`,
`v_i=1` if `π_i<0`, and `v_i=x_i` if `π_i=0`. Every leg then lowers `p` at
rate `|π_i| ≥ π_min ≥ 2^{-H_0}`. Since `Z_p ≠ ∅` gives `min_cube p = p(v) ≤ 0`,
the path meets `Z_p` within `ℓ_1` length `p(x)/π_min`, which bounds the
Euclidean distance. Negative values are symmetric. The empty-zero-set case
(F:807–810) is correct.

Why it matters: `cor:int:bilinear` (F:813–826) and the bilinear part of
`thm:int:tu` replace the parameter-dependent value margin `μ_0` by
`2^{-(k+1)H_0}δ/2` through this lemma. That replacement is what gives
`log_2 M ≤ poly_d(I)` in the bilinear case. Both later reviews that
checked the lemma (`complete-recourse-sol-r1.md:214`,
`final-recourse-integer-sol-r1.md:223`) marked it verified.

**NEW-2. The aligned perturbation model is narrower than the lattice
theorem's law.** `def:model:perturbation`(iii) (02:116–118) draws
`ξ_1,…,ξ_k` independently from one marginal law `𝒟`. `thm:int:lowrank`
(08:533–539; proof F:964–976) draws `ξ_i` from `U_{σ_i,M}` with row-specific
scales `σ_i` and one common `M`. A row rescaling of `T` does not reduce
this to the model, because `T` also defines the concave term
`-(α/2)‖Tx‖²`. Repair: let the aligned model, and the base-chosen-law
paragraph (02:141–154), allow independent coordinates with per-coordinate
scales from one grid family with a common resolution, or state the lattice
law as an explicit extension. Keep the common `M` explicit: the lattice
denominator `1/[D_0(M-1)]` (F:976–980) depends on it.

**NEW-3. The lattice proof is attributed to the wrong search.** 08:561–562
says that "the core search of `sec:rec:value` on the `k` auxiliary
coordinates" finishes the lattice argument. That search runs on the unit
cube with dyadic cells `h_j=2^{-j}` and a current-level incumbent. The actual
proof (F:961–967) correctly runs `thm:count:cells` with isotropic balanced
meshes on the unequal-width box `𝒜`. Cite `thm:count:cells` and
`cor:count:levels`. (Resolved in `final-submission-r4`, 08:711.)

**NEW-4. The closure template overstates the bit length of pre-draw
quantities.** The template (03:556–562) covers "the exact results built on
growth tails" and says all pre-sampling quantities "have polynomial bit
length in `I`". The boundary-flow and nonlinear-TU results are built on
growth tails, but they choose `log_2 M ≤ f_d(k) poly_d(I)` (`thm:int:flow-boundary`,
08:374–375; F:760–761). The model section already defines this
parameter-dependent precision (02:156–163). Qualify the template sentence
accordingly.

**NEW-5. The fixed-parameter list includes non-fixed-parameter results.**
02:322–324 says that "the low-negative-inertia, core, and integer-dimension
results" have the fixed-parameter form. But `thm:qp:uniform` is expressly
not fixed-parameter (04:550–553), and `thm:qp:two` covers only `k ≤ 2`. The
introduction already scopes this correctly to aligned and Gaussian-like noise
(01:268–271). Use the same qualification in the model section. This is
separate from editorial finding P4 (numerical ratios inside the parameter),
which should be applied in the same sentence.

**NEW-6. A regret bound uses the auxiliary-width symbol.** `rem:qp:regret`
(04:577–579) bounds the ambient regret by `σ̄ Σ_i w_i`. Throughout Section 4,
`w_i` denotes auxiliary search-box widths (04:538, 04:558). The valid
ambient bound uses the original coordinate widths, `S` as in
`lem:qp:growth-sections` (04:229–231), or the relaxation's widths for a mixed
polytope. The aligned sentence (04:579) is already correct. This location
should be included in the contract's `W_noise` repair
(`root-integration-scope-r1.md` item 6).

### 1.3 Concurrently recorded findings that I confirm

I found these independently while reading r1. The live integration contract
or a parallel review of the same snapshot records them, so I list them only
as confirmations.

- **Simplex equality multipliers.** `lem:con:simplex-close` (D:470–475) and
  `lem:con:simplex-tail` (D:529–536) speak of "every multiplier of an active
  constraint". An equality-budget multiplier is unrestricted. Both proofs
  actually use only zero-coordinate and tight-inequality multipliers, which
  is the valid version. Restrict the statements accordingly.
- **Coarse simplex corners.** D:354 defines corners as points of `(hℤ)^b`.
  At levels with `h ≥ 2` this set is `{0}` for an inequality simplex and empty
  for an equality simplex. The lemma at D:372–373 intends the simplex
  vertices; define them as the corners at coarse levels. The center formula
  (D:496–499) also needs a branch for blocks with no free coordinate.
- **Integer root polynomial.** Step (3) forms `P=p/G ∈ ℚ[T]` (F:59–61), while
  08:72–73 promises a squarefree integer polynomial and `lem:int:values`
  asserts `Res_T(P, q_0W-h) ∈ ℤ[W]` (F:251–253). Clear a positive common
  denominator of `P` before forming the modular maps. Roots, squarefreeness,
  and the maps `r_i` are unchanged.
- **Euclidean refinement for the solver.** The refinement in
  `lem:int:cost` (F:293–296) gives coordinatewise accuracy. The model's
  `q`-bit contract (02:288–291) uses Euclidean distance, so add
  `⌈(1/2)log_2 max{1,k}⌉` bits. This is the same repair as for the general
  fallback.
- **Flow residual set and short cycles.** The flow model (08:256–265) must
  assume a nonempty residual set. The necessity proof of
  `lem:int:potentials` (F:493–496) must also cover two-cycles formed by
  different parallel arcs; the same one-unit augmentation argument applies.
- **Conditioned algorithm.** Step (3) of `thm:qp:conditioned` (B:209–212)
  compares with `f̂`, which exists only after step (2) has succeeded, so it
  needs that guard. The proof of `lem:qp:aux`(b) (B:105–106) should say "a
  minimum over a compact family of affine functions", not "a finite minimum".

### 1.4 Known pending repairs still absent from r1

These items are recorded in the earlier reports or the integration contract.
They are not newly discovered here, and r1 does not resolve them. I verified
that each is still present at the stated location.

**Shared foundations (02, 03, A)**

- The general fallback returns separate scalar root representations
  (03:518–527, 03:543–550; A:475–492), while the model requires one common
  root (02:265–269). Integrate `author-reports/fallback-shared-root-sol.md`
  and enlarge the pre-draw factor `B` before the thresholds are chosen.
- "The output may have length up to `B`" (03:540–541). Use
  `B poly_d(I+b)`.
- The rare budget divides by `S` (03:470; A:416–423) without `S>0`.
- "A Turing machine can sample only from laws with finitely many rational
  atoms" (03:264). Say that a worst-case bound on random bits forces finite
  support.
- "All numbers have `O(b)` bits" for the exact Taylor sum (A:218).
- Euclidean `q`-bit refinement of the fallback (03:528–530) needs
  `O(log N)` extra bits.
- Renegar's statement (A:328–346) lacks positive block sizes, at least one
  free variable, and positive logarithm conventions.

**Few negative directions (04, B)**

- `thm:qp:two`(b) gives only the lower bound `2^b ≥ 2n𝖣B` (04:251–252);
  bound `b` or charge it.
- `rem:qp:moments` uses the wrong lower integration limit (04:280–283).
- Empty mixed feasibility: `def:qp:instance` (04:33–48) and the statement of
  `thm:qp:uniform` (04:534–548) are inconsistent with the proof's
  feasibility check (B:616–617) and with `thm:qp:gauss` (04:507).
- `lem:qp:pieces`(b): the region contains `a` only for `ζ'=ζ` (04:341–342).
- A supplied frame constant must be rational to be checked (04:83–91).
- It is the near-optimal corners, not the retained cells, that lie in the
  stated ball (04:215–216).
- "Use different laws" (04:288–290), and the summary table's intrinsic-`ν`
  qualification (04:853).
- The mixed-integer version of the conditioned foundation (inventory A0)
  is absent; `thm:qp:conditioned` is stated for `n_z=0` (04:186–189).

**Sparse and constrained domains (05, 06, C, D)**

- The all-fixed case `n=0` before maxima and divisions (05:35–41,
  05:62–65).
- The patch descriptor fixes singleton-hull continuous values (05:110–114),
  but the model lists only labels and original bounds (02:247–249). "Never
  fixes an artificial endpoint" (05:644–646) holds only for the gradient
  rule.
- The threshold sentence at 05:901–906 claims more than
  `prop:lim:threshold` proves.
- "A dimension-free count would require exact or certified conditional
  values" (05:562–565). The barriers show that conditional values are
  sufficient, not that they are necessary.
- The uniform-family lemma requires coefficient bit length at most `I+b`
  (06:69). The reductions give `poly(I+b)`.
- The actuator curvature `L=1+L_q+ΛG_2` allows a negative `L_q` (06:426–433).
- "Each of which supplies (P1)–(P4)" (06:24–25), whereas order constraints
  replace (P1) by transport (06:597–599).

**Recourse (07, E)**

- For `k=0`, `E_j=0` makes `prop:rec:search`(b) false in certified mode
  (07:193–199). The appendix treats `k=0` separately and correctly
  (E:305–307, E:352–358); the statement must match.
- Residual convexity is certified "by an explicit sum of squares"
  (07:402–404). The certificate must be for the residual Hessian form.
- "For `k=0` the problem is a convex polynomial on a box" (07:437–438). A
  certified global oracle is the actual assumption.

**Integer recourse and components (08, F)**

- The solver returns the value by its own defining polynomial (08:73–74).
  The appendix already computes the common-root value map
  `h/q_0 = f(r(T)) mod P` (F:251); return it.
- "A Gröbner basis for every value of `ε`" (08:85–86). The appendix's
  `z`-parameterization (F:69–75) is correct, including `z=0`.
- The unqualified leading-coefficient, "harmless candidates", and
  convergence sentences (08:88–96). The appendix proves the qualified
  versions: good forms, rejection tests, and subsequences (F:57–61,
  F:160–247).
- The affine margin sentence omits the empty-zero-set case (08:408–410).
  The appendix lemma has both cases (F:795–810), subject to NEW-1.
- `thm:int:tu` does not restate the flow model's premises (08:417–425).
- The polynomial bit length of the potentials needs rational marginal costs
  of polynomial length (08:229–238).
- The strong-field result calls a gap certificate a "`q`-bit evaluation"
  (08:483–484).
- "The previous results need small noise" (08:451).
- The `k=0` lattice case (08:533–537; handled at F:981–982) and the
  all-pinned strong-field case.
- The lattice theorem is proved for quartic unaries only (08:531), while the
  introduction and results table already claim separable convex polynomial
  terms (01:69–71, 01:155–157). Integrate
  `author-reports/integer-lattice-generalization-sol.md`, or narrow the front
  matter until then.

**Front matter, boundaries, and discussion**

- The direct width-two, bounded-coefficient Square Root Sum boundary (X15)
  is absent; 09:671–673 declines it, contrary to integration decision 11.
- The B10 conditional count, the X8 worked gap, and the X16 deterministic
  flow bound are absent.
- "The first is the model itself" (01:369–373) is listed as a contribution.
- The universal-law limitation and open question (10:66–69, 10:132–136)
  should be replaced by the uniform-resolution corollary.
- Rational outputs need a domain qualification, and the common-premise
  sentence needs the chart and transport replacements (01:187–188,
  01:253–256). The width open question says conditional values are needed
  (10:106–108).
- Original-objective calibration must use the noise-model width `W_noise`
  and keep numerical parameters explicit (01:301–306, 02:398–415, 10:16–19).

### 1.5 Earlier corrections already integrated in r1

These need no further action as defects: the threshold proposition's
`δ ≥ 0` and narrower conclusion (09:491–523); the level-0 nonclosure argument
(09:257–270); the scope of rare fallbacks (02:209–227, 03:251–260,
03:581–583); the dependent-noise qualification (01:225–231); Gaussian support
in the regret calibration (02:385–412); charted outputs (02:257–264,
02:293–300); law-specific regret bounds (04:574–583, apart from NEW-6);
`h_J ≤ 1` (B:628–638); removal of singleton auxiliary ranges (B:191–194);
extreme-point linear programs in the Hochbaum–Shanthikumar oracle
(F:474–479); the `+∞` convention for labels (F:358–359); weighted connected
sets for strong fields (F:916–924); and Euclidean precision in the sparse
fallback evaluation (C:197–212).

## 2. Verified proofs

I checked each proof below step by step against its statement, including
constants and quantifiers. "Verified" means that the written argument proves
the statement, apart from the issues listed in Section 1.

### 2.1 Model and shared tools (02, 03, A)

Verified: `prop:model:regret`; `ex:model:tie`; the Gaussian calibration
argument (02:398–412); `lem:count:interval`; `thm:count:local`;
`cor:count:levels`, including `L_i h_ij + 4E_j/h_ij ≤ C_k L_i h_ij`;
`lem:count:rounding`; `thm:count:cells` (i)–(v); `cor:count:approx`;
`ex:count:atom`; `lem:count:transfer`; `lem:count:gauss-sampler`, including
failure mass, the four Kolmogorov steps (`14e < 2^{-b}`), and the squaring
recurrence; `thm:count:growth-tail` (closedness, conjugate, proximal map,
regular points, area formula, trace bound, integration, sharpness);
`lem:count:finite-tails` (a)–(d); `lem:count:rare-fallback`; and
`thm:count:fallback`. In the fallback proof, the canonical minimizer and the
singleton formulas are correct. Degrees are bounded by base data alone, and
heights depend on `I+b` only polynomially (A:459–473). The rational point on
mixed boxes is correct.

### 2.2 Few negative directions (04, B)

Verified: `lem:qp:normalize` in full (the eigenvalue floor `μ`, halving,
rational Jacobi rotations and off-diagonal energy decay, Weyl selection,
range projection, and the `63/64` frame); `lem:qp:aux` (a)–(d);
`lem:qp:face`; `lem:qp:growth-sections`; `thm:qp:conditioned` (correctness,
growth transfer `g_W = αg/(2g+α)`, retained-cell count, both reconstruction
depths, and the `k ≤ 2` bound); `thm:qp:two` (capped moment integral);
`lem:qp:pieces`; `lem:qp:gap`; and `lem:qp:isolation` (breakpoints of the
lower envelope).

The gap threshold `αk w̄` is valid but conservative: the proof (B:350–355)
already shows that `α√k w̄` suffices.

Also verified: `lem:qp:tube` (image hyperplanes for a nonsingular `H_ω`, a
kernel functional for a singular `H_ω`, and `‖L‖ ≥ 1` from `TL=u`);
`lem:qp:tube-prob`; `lem:qp:sections`; `lem:qp:volume` (Jacobi complementary
minors, zonotope volume, Cauchy–Binet); `lem:qp:uniform-count`; and
`lem:qp:gauss-count`. In the last lemma the factor `c_fr^{-1/2}` multiplies
only interior coordinates, because the proof uses the marginal density of
`ξ_Q`, and the lattice sum `CW'φ_s(0)+2C+4` is correct. I also verified the
sampling schedules (A), (B), (C) of the main proof and their fallback
probabilities, the containment, count, work, and intrinsic bounds;
`prop:qp:fiber-sharp` (`1-(1-q)^n`); `lem:qp:scalar`; the separable pieces
and `thm:qp:sep`; `lem:qp:aniso`; `thm:qp:sep-gauss`; and the examples
`ex:qp:atom` and `ex:qp:corner-labels`.

### 2.3 Sparse polynomials (05, C)

Verified: `lem:sp:cells`; `lem:sp:allowed`; `lem:sp:dp`; `lem:sp:round`,
including that rounding keeps every whitelist; `prop:sp:prune`;
`lem:sp:compare`; `prop:sp:count`; `prop:sp:closure-sound`;
`prop:sp:closure-stop`; `lem:sp:tails`; `lem:sp:rare`; the proof of
`thm:sp:main`; `lem:sp:bezout`; `lem:sp:gls` in full (capped epigraph, weak
separation, homothety point in `S(𝒦,-ε)`, repair, value-to-distance);
`prop:sp:eval`; `lem:sp:faces`; and `cor:sp:qp`.

### 2.4 Constrained domains (06, D)

Verified: `lem:con:expand` (running intersection along dependency paths);
case (E) of `thm:con:graph`, including the lift's Lipschitz constant;
`lem:con:chart` (unique root, smoothness, derivative bounds `Π_1`–`Π_3`,
oracle); `lem:con:approx` (summed lower-cost error `E_j` and witness
tolerance `4E_j`); `lem:con:approx-closure`; `lem:con:kkt` (degree count and
nonsingularity of the bordered KKT matrix); case (I) of `thm:con:graph`; and
`thm:con:actuator` (adjoint identity, adjoint bound `Λ`, bit lengths,
trajectory Lipschitz constant).

For simplices: `lem:con:simplex-round` (cube-corner vertices for `h ≤ 1`);
`lem:con:simplex-count` (face classification, anchor conditioning, and
`C(1/h-1, r) ≤ h^{-r}`); `lem:con:simplex-close` (soundness of tests (a)–(d),
center construction, success); `lem:con:simplex-tail` (counting transformed
tuples); and `thm:con:simplex`, including the blockwise projection repair.
The equality-multiplier wording and the coarse-level corners are the
concurrent items of Section 1.3.

For orders: `lem:con:order-vertices`; common-threshold rounding;
`lem:con:transport` (all rates in `[0,1]`, directional curvature `n_c L̄`);
`prop:con:order-count`; `lem:con:lpgap` (exposure gap at most `n_c δ`);
`lem:con:order-close` (merging, full dimension, weighted test);
`lem:con:order-tail` (fiber count with paired noise); and `thm:con:order`,
including the predecessor-maximum repair.

Examples verified: `ex:con:graph-curv`, `ex:con:chain`, `ex:con:dyn`,
`ex:con:actuator`, and `ex:con:premature`.

### 2.5 Continuous recourse (07, E)

Verified: `lem:rec:value`; `prop:rec:search` for `k ≥ 1`;
`lem:rec:exclusion` (certified lower bounds on slabs, no slab at an original
bound); `lem:rec:closure`; `lem:rec:convex-oracle` (tangent certificate,
`Δ ≤ δ/t + K_f t/2`); the base choices, algorithm, correctness,
`lem:app:rec:stopping` with all constants, and the proofs of `thm:rec:qp`
and `thm:rec:poly`; `cor:rec:forest`, modulo its citation; and
`prop:rec:rank`, including the Euler identity for the `t log t` remark.

Under core-only noise: `lem:app:rec:lift` (selector Lipschitz constant `H`,
differentiability, growth lift); `lem:app:rec:core-tails`;
`prop:rec:tube` (a) dimension, (b) the three-block formulas, ending
`D_* = (2n_R+1)𝖰^3`, and (c) the Basu–Lerario bound with grid jitter, which
covers atoms on `ℰ_K`; `prop:rec:release` (branch smoothness, the bound
`K_λ = K_3(1+H)^3`, the two-sided small-gradient bound
`β_i^2 ≤ 2K_λ λ_i(a)`, Schur-complement elimination, restoration with
modulus `ν`); and `thm:rec:core-only`, including the bad events
`ℬ_1, ℬ_2, ℬ_3` and `ν ≥ 4g_*`.

Examples verified: `ex:rec:feasibility`, `ex:rec:star` and its positive
definite variant (`3 ± √5`, `q_C - U = d/16 - 3/8`), `ex:rec:fiber` and its
strictly convex variant, `ex:rec:weak`, and `ex:rec:two-sided`.

### 2.6 Integer recourse, flows, components, lattice (08, F)

**The joint critical-limit solver** (`thm:int:solver`, F:23–331) is
verified in full.

1. `lem:int:quotient`. The leading monomials `y_i^a`, with `a = D-1 ≥ d`,
   persist under every specialization of `z`, including `z=0`. So normal
   forms over `ℚ[z]` specialize correctly, and memoized reduction lowers the
   degree at every step.
2. `lem:int:triangular`. Commuting operators are triangularized
   simultaneously over the algebraically closed Puiseux field. The
   diagonal entries define ring homomorphisms that vanish on the ideal.
3. Poles (`lem:int:leading`). For `λ` off the hyperplanes
   `λ^T w^(t) = 0`, the proof writes
   `ε^κ χ = C(λ) Π_v (T - λ^T v)^{μ_v} + Ω` with `val Ω > 0`. Comparing
   exponents forces `κ ∈ ℤ` and `c_m = 0` for `m > κ`. Zariski density
   turns this into a polynomial identity.
4. Repeated roots (`lem:int:recovery`). For a good `λ`, `K_λ = κ` and
   `G = gcd(p,p') = c Π (T-α_v)^{μ_v-1}`. Then `G` divides
   `b_i = -∂_{λ_i} c_κ`, and
   `A(α_v) = κ' μ_v Π_{u≠v} (α_v - α_u) ≠ 0` because `μ_v ≠ 0` in
   characteristic zero. Hence `r_i(α_v) = v_i`.
5. Limits (`lem:int:limits`). Real critical points `y^(m)` give eigenvalues
   `λ^T y^(m)`. Letting `m → ∞` in `ε_m^κ χ = 0` gives
   `c_κ(λ, λ^T y^*) = 0` for every rational `λ`. Hence `y^* ∈ ℒ`, and `ℒ` is
   nonempty whenever such a sequence exists.
6. `lem:int:forms`. At most `(r-1)(N + C(N,2)) < Q_r` integers `t` fail.
7. Correctness. The proof passes to a subsequence of deformed minimizers on
   one face and recovers the real limit from a real root of `P` for a good
   form. The rejection tests of step (3) are exactly what bad forms need,
   and points from bad forms are filtered by membership in `B`, so they are
   feasible and harmless.
8. `lem:int:values` and `cor:int:mixed-solver`. The resultant degree,
   identification of the value root, and exact comparisons through the
   squarefree product are correct. The integer-coefficient claim needs the
   normalization of Section 1.3.
9. `lem:int:cost`. The `H` exponent does not depend on `k`, as claimed.
   `lem:int:budget` is spot-checked: my estimate of the value-map height is
   `O_d(U^13)`, inside the `U^18` envelope, and the final exponent has ample
   slack.

**Native integer recourse and oracles.** Verified: `lem:int:label`;
`lem:int:native-stop` (`E_j ≤ g_0/256`); `thm:int:native` (budget `B`,
probability, work, and an output length that does not count examined
labels); `cor:int:native-implicit`; `prop:int:hs`, at citation level; and
`lem:int:potentials`, subject to Section 1.3.

**Flows and TU systems.** Verified: the chart family `def:int:charts`
(core degree at most `d-1`, base-bounded coefficients);
`thm:int:flow-interior` (tube set, `D_int`, probabilities, stopping, and a
reduced cost of constant positive sign on the hull); `lem:int:proximity`
(conformal circuits with entries in `{0,±1}`, charging with factor `n_R`);
`lem:int:face-general`, including the off-face Taylor bound; `thm:int:face`
(inward derivatives convex on intervals with at least three integers, and
`d+1` identities); and `lem:int:margin` (truth set `(m^2, ∞)`, height
`Ξ'_d(k)`, Cauchy bound).

Also verified: `lem:int:normal` (the face minimizer and its optimal flow set
do not depend on the normal noise); `thm:int:flow-boundary` (schedule, three
bad events, stopping, and `log_2 M ≤ f_d(k) poly_d(I)`); `cor:int:bilinear`,
subject to NEW-1; `lem:int:tu-dual` (exactness of the piecewise-linear
interpolation, pointed dual polyhedron, `{0,±1}` basis inverse, box `R`);
`thm:int:tu`; and `cor:int:tu-ineq`.

**Components and lattice.** Verified: `thm:int:strong-field` (pinning,
separation, `(4Δ_+)^{t-1}` connected sets, weighted expectation, and the
sufficient regime giving `a_i q_i ≤ 1/(8Δ_+)`); and `thm:int:lowrank`
(scalar recourse, square completion, `E_J < 1/[D_0(M-1)]`, and the common
denominator of the original values).

### 2.7 Boundaries (09, G)

Verified: `thm:lim:width` (instance, the completion bound `3p/40`,
retention by induction, failure of whole-hull closure, `J > j_*` under the
schedule, and the failure of `f(p)I^c` work); `prop:lim:local` (location of
the optimizers, nonclosure at level 0, deletion at level 1);
`thm:lim:ambient` in full (block spectrum, range `[-4,4]`, the block value
function, `Pr(ℰ_1) ≥ 41/160`, flatness `|V'| < 3/m`, gap `< 15/m`, and both
count ranges); `thm:lim:constraints`; `ex:lim:coupled`;
`prop:lim:threshold`; `prop:lim:value`; `thm:lim:posslp` (bounded pair
encoding, gate bounds, weighted Hessian `≥ I` via `‖Ê‖_2 < 1/4`, sign tests,
amplifier convexity `15/16`); and `prop:lim:flow`.

## 3. Not verified

- Exact statements and constants of external results: Renegar Theorem 1.1
  (format and height exponents), Basu–Lerario Theorem 1.1 (tube constant),
  GLS Corollary 4.2.7, Kozlov–Tarasov–Khachiyan, Del Pia's fixed-dimension
  convex MIQP contract, the Del Pia–Khajavirad forest oracle,
  Hochbaum–Shanthikumar Theorem 4.3 and Algorithm 4.2, Fulton Example 8.4.6,
  Allender et al., and Kloks. Identifying and checking these sources belongs
  to the Luna literature owner.
- The exponent-100 bound for elementary routines in `lem:int:budget`. I
  only spot-checked it; later Sol reviews (`component-solver-budget-sol-r3`
  and `-r4`) examine it on later snapshots.
- The bibliography, typesetting, and any later snapshot. For later snapshots
  I only searched the locations of NEW-1 to NEW-6.

## 4. Checks performed

- A `python3 -I` check of SHA-256, byte counts, and line counts against
  `manifest.json`, before and after the review. All 20 files passed both
  times.
- Full reads of all 20 snapshot files; of `BRIEF.md`,
  `independent-review-brief.md`, `integration-decisions.md`,
  `integration-contract.md` (re-read after it changed), `inventory.md`, and
  `root-mathematical-findings.md`; of the root and Sol early reports named
  in the task, including the updated `early-quadratic-sol.md`; of the three
  author reports; and of the root and editorial interim records needed for
  deduplication.
- Scoped `grep` searches of the snapshot for each pending anchor and for
  private paths or review history in the proof chain (none found); of the
  parallel reviews for overlap with my findings; and of later snapshots for
  persistence of NEW-1 to NEW-6.
- Analytic derivations of the steps listed in Section 2. The NEW-1
  counterexample was computed by hand.
- No optimization experiment, project-wide verification, CI inspection,
  literature research, delegation, commit, or edit of any file other than
  this report.
