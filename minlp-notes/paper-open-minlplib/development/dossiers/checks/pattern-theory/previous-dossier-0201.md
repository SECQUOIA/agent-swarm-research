# Dossier: why these instances stayed open, the common certificate pattern, and coverage

Family key: `pattern-theory`. Written 2026-10-04 for the MPC paper in
`paper-open-minlplib/`. `R/` means `research-20260929/`. Checks run for this
dossier are in `paper-open-minlplib/development/dossiers/checks/pattern-theory/`
(scripts and `logs/`). Nothing under `R/` or `literature/` was edited. No solver,
certificate or scientific module was run; the checks read saved data files (copied
to a temporary directory first) and saved solver logs.

## 0. Main findings

1. **Nothing here invalidates a claimed result.** No certificate's validity
   depends on the theory in this family. Validity rests on an elementary
   telescoping lemma (Lemma 1 below), its window and cell variants (Propositions
   3 and 4), and the instance-specific computations recorded in the family
   dossiers. The band theorems (Theorems 5 and 6, Proposition 8) only explain
   when such certificates can be exact.
2. **The common pattern holds for 15 of the 31 closures, not "most".** These 15 are
   lnts50–400, dtoc5, lukvle10, optcdeg2, chain50–400 and catmix100–800. The
   waterno2 improvements use the same pattern. In all 15, the certificate is a split
   (Lagrangian or discrete calibration) along the stage structure, and each stage
   problem is small enough to minimize rigorously. Exact windows occur only in
   lukvle10 and chain (2-D each). lnts handles its global step variable `h` by
   monotonicity instead of a window. dtoc5, catmix and the final optcdeg2
   certificate use no window at all. Three more closures (ex6_2_5, ex6_2_7,
   pricing050) are Lagrangian splits over a few dense rows rather than along a
   chain. The summary's sentence "Most certificates ... combine ... and exact
   treatment of a few low-dimensional windows" therefore needs rewording
   (Section 8, PT-3).
3. **"Open" has two meanings in the record; the paper must define both.**
   (a) MINLPLib's listing has no solved mark (S). This is true for all 31 closures
   and all 12 other paper instances. (b) The scout's rule: the best listed
   single-solver relative gap exceeds 1e-4. That rule produces "146 open among
   283 candidates". camshape100 (1.2157e-6) and lnts50 (3.8249e-5) are open under
   (a) but not under (b). Applying the scout's rule to all of MINLPLib, including
   the first-wave instances it excluded, gives 294 candidates and 155 open; this work
   closed 29 of the 155 (Section 2). The counts reproduce exactly: from the scout's
   file and from the bound audit's independent page parse.
4. **"Relaxation, not branching" is an interpretation, and the dichotomy is not
   sharp.** The saved one-hour SCIP 10.0.3 logs give cheap supporting evidence:
   - hvycrash: the dual bound stays at −2.185e8 through 504,455 nodes.
   - catmix100–800: no finite dual bound.
   - powerflow0030p: the dual bound stays at 0 through 23,036 nodes.
   - dtoc5 and optcdeg2: one node in one hour, in an overloaded batch.

   camshape100 is a counterexample to the strict dichotomy. SCIP's bound rises
   from about −5.16 to −4.529 over 1,179,749 nodes but stops 5.7% short of the
   optimum −4.28414712. A weak relaxation makes branching slow; it does not make
   branching irrelevant (Section 5.3, PT-2).
5. **Which theory belongs in this paper.** Include a short "split certificate"
   section: Lemma 1, Propositions 2–4, Theorem 5 (band identity), Theorem 6 (path
   sandwich) with the counterexample (Proposition 7), and Proposition 8 (cells with
   constant splits). All are proved below in the constrained, extended-value form
   the certificates need. Each proof is a few lines.

   Exclude the following:
   - the single-tree lower bounds (face-exact note): they concern a synthetic
     path family with termwise McCormick relaxations and say nothing provable
     about these instances;
   - the decomposition-certificate complexity theorems: they are existence results
     on synthetic families, and the `paper-decomposition-aware/` manuscript already
     occupies this territory;
   - the split-robust bounds, RLCT, coupling, hp and polynomial rates;
   - the bang-bang asymptotics and the calibration transfer theorem: no
     certificate uses them.

   Cite the excluded results as companion reports at most (Section 3.11).
6. **Several older documents are outdated.** The paper must use the summary
   (`R/open-instances-summary.md`), not those documents (PT-4).
   - `R/SYNTHESIS.md` and `R/closing-research-results.md` still say no exactly
     feasible point exists for 13 closures.
   - Both documents also still describe the eg_disc2_s re-certification as a sample.
   - `R/SYNTHESIS.md` gives waterno2_06 as 1.67% (round-to-nearest; the exact
     value with displays is 1.674%, so the safe display is ≤ 1.68%).
   - The calibration note's §2.4 still lists optcdeg2 as "affine + head block".
     It also says "quadratic calibrations were not needed by any closed
     instance"; optcdeg2's final certificate is a quadratic calibration.

---

## 1. Instances and models

### 1.1 Population and mechanism classes

The paper's 43 instances are 31 closures, the six KAN models (relaxation R only;
the OSIL models are exactly infeasible), five waterno2 models and
ann_cumene_tanh. The 31 closures fall into five classes by certificate
mechanism. Sources are the summary's mechanism column and the family reports.

| class | mechanism | instances | count |
|---|---|---|---|
| A. staged split | Lagrangian or discrete calibration along the stage (chain) structure; each stage residual is minimized rigorously; exact windows only where the split is not exact | lnts50/100/200/400, dtoc5, lukvle10, optcdeg2, chain50/100/200/400, catmix100/200/400/800 | 15 |
| B. Lagrangian over a few dense rows | dualize ≤ 5 coupling rows; independent blocks minimized rigorously | ex6_2_5, ex6_2_7 (3 mass balances, 3 phase blocks, tangent-plane test by 2-D interval B&B); pricing050 (5 rows, 50 univariate blocks) | 3 |
| C. global duality or convexity | SDP/Lagrangian dual with exact LDLᵀ PSD proof (powerflow0030p, 0039p, 0039r; 0039 adds a leaf-bus identity and B&B on 3 leaf coordinates); convex relaxation plus KKT tangent plane (etamac); reduced objective concave on a polytope containing the feasible set, plus tangent plane (pindyck) | powerflow0030p/0039p/0039r, etamac, pindyck | 5 |
| D. comparison or identity | discrete Sturm comparison in u = 1/r (camshape); objective constant on the feasible set (hvycrash) | camshape100/200/400/800, hvycrash | 5 |
| E. reduced-space B&B with strong local enclosures | second-order Taylor models keeping signed cancellation, per-box LP over the 24 minimax rows, under A1/A2 | eg_int_s, eg_disc_s, eg_disc2_s | 3 |

Total: 31. Classes A and B are both split certificates in the sense of Lemma 1
(18 of 31). Not closed: the waterno2 models were improved by a class-A mechanism;
KAN (on R) and ann_cumene_tanh were bounded by reduced-space B&B.

### 1.2 The model class behind class A

All class-A instances, and waterno2, have a path structure. Write the model as a
sequence of bags `t = 1, …, N`. Bag `t` holds a variable vector `z_t`. The
*separator* `s_t` (t = 1, …, N−1) is the sub-vector shared by bags `t` and
`t+1`; write `s_t = π^R_t(z_t) = π^L_{t+1}(z_{t+1})`. Each bag has a set
`K_t ⊆ R^{d_t}` and a cost `F_t : K_t → R`:

```
(P)   f* = inf { Σ_{t=1}^N F_t(z_t) :  z_t ∈ K_t (all t),  π^R_t(z_t) = π^L_{t+1}(z_{t+1}) (t < N) }.
```

`K_t` holds the bounds and every row that involves only bag `t`'s variables
(dynamics rows, stage rows). It may be replaced by any valid enclosure of the
bag's projection of the feasible set. Interval bound propagation enters here.
For transcribed control problems, bag `t` is the stage `(x_t, u_t, x_{t+1})`.
The separator is the state, or (state, control) for trapezoidal schemes with
nodal controls. Two features recur:

- *Global variables* belong to every separator. lnts's step `h` is one. The lnts
  certificate does not branch on `h`. It proves infeasibility for every
  `h ≤ h2` by one Lagrangian argument and uses monotonicity in `h`. The lnts
  report notes that "the treewidth/separator structure is irrelevant here; what
  matters is that the dynamics are linear in the state for fixed `h`"
  (`R/open-instances/open-instances-report.md` §3.4).
- *Dense rows* are lifted into the state. chain's length row couples all
  slopes. Its certificate uses summation by parts with the cumulative weight
  `v_k = V + Σ_{j<k} λ_j` as an extra state variable
  (`R/open-instances-wave2/cops/report.md` §2).

Per-instance structure. Variable counts and the census width upper bounds are
from `R/bound-audit/pages.json` and `R/treewidth-census/census_merged.json`;
the other entries come from the family reports.

| instance(s) | vars (OSIL) | width fac/nl | stages and separator | split class | window | stage check |
|---|---|---|---|---|---|---|
| lnts50–400 | 256–2006 | 12–11 / 2 | N = 50–400; separator (py, vx, vy, θ, h), dim 5 incl. global h | Lagrangian of the aggregated (summed) dynamics with multipliers (μ, ν): affine in the state for fixed h | none; global h by monotonicity | closed form max_θ (w cos θ + b sin θ) = √(w²+b²), mpmath iv |
| dtoc5 | 99,999 | 2 / 0 | T = 49,999 stages; separator y_t (dim 1); all variables free except y_0 | affine (costates λ_t = −2u_t) | none | closed form: residual strictly convex quadratic because λ_t < 1/4 |
| lukvle10 | 1000 | 4 / 1 | 998 recurrence rows; separator (x_j, x_{j+1}), dim 2; no controls; all free | affine calibration (pair Lagrangian; the rows give quadratic terms) | last 3 pairs (rows 994–997 kept), 2-D interval B&B | 34 distinct 2-D pair problems plus the tail, interval B&B |
| optcdeg2 | 150,002 | 4 / 0 | N = 50,000; state (y, v), dim 2; control u ∈ [−0.2, 0.2] | quadratic: S_t = p_t·x + (q_t/2)(v − v̄_t)²; q_t = 0 at both switches | none (the earlier certificate used an exact 3080-stage head block by monotonicity) | 1-D interval computation after exact elimination of y and u; 1.33e6 cells |
| chain50–400 | 102–802 | 4 / N+1 | N = 50–400; lifted state (z_k, v_k); slopes free | field type: S_k(z, v) = G(v) − v z + k c (discrete catenary calibration) | 2-D end window (z_1, z_N), interval B&B with per-box field parameters (V, H′) | closed-form lemma, checked in exact rationals |
| catmix100–800 | 303–2403 | 4 / 1 | N = 100–800; state (x1, x2), reduced by homogeneity to a 1-D projective separator θ; control u ∈ [0,1] | concave, piecewise linear, positively homogeneous value-function bounds (chords on about 14,080 rays per stage) | none | per-ray 1-D interval B&B over u |
| waterno2_06–24 (not closed) | 996–3984 | 9 / 2 | T = 6–24 periods of 166 variables and 9 binaries; separator: 3 tank levels; plus one horizon-wide row | Lagrangian on 3(T−1) level copies + horizon row; for _06, cellwise slopes with a shortest path over cell pairs (Proposition 4) | per-period rigorous B&B (the bag itself, 166 variables) | per-period and per-cell-pair B&B |

Note the widths. chain's nonlinear-primal width is N+1, caused by the dense
length row. Its small width (4) appears only in the factor-incidence graph, which
splits long sums with partial-sum nodes. lnts's factor width (11–12) is set by the
hub `h`. Small width is therefore neither necessary nor sufficient for the
pattern. The census report says the same: "it does not show that width causes
the difficulty."

### 1.3 Model-provenance issues that cut across families

- All certificates concern the stored MINLPLib **OSIL** models, with decimal
  constants read as exact rationals. Families with source-model differences
  (CUTEst scaling for dtoc5 and optcdeg2; COPS 2.0 vs 3.0 for catmix; rounded
  QPLIB copies) are covered in their own dossiers.
- The scout's OSIL reader (`R/open-instances-scout/structure.py` via `osil.py`)
  ignored the objective constant. The scout found nonzero constants in 36 of the
  283 candidates (catmix −1, powerflow0039p/r +2, methanol, pinene, popdynm).
  The certificate scripts read the constant
  (`R/open-instances-scout/targets.md` §1, item 4; COPS report §1). Any
  pattern-level table that recomputes objectives must add it.
- For catmix100–800, methanol50 and lop97icx, the OSIL and .gms coefficients
  differ by double rounding, at most 2.4e-16 relative per coefficient
  (`R/publication/minlplib-status/report.md`). Claims are for the OSIL models.
- The six KAN OSIL models have no exactly feasible point. Their listed "feasible
  points" are tolerance artifacts. This matters for coverage: these instances are
  counted as "open" by both definitions, yet no optimum exists.

---

## 2. Listed status and coverage

### 2.1 Two definitions of "open"

- **(a) No solved mark.** MINLPLib's instance listing marks some instances "S".
  All 31 closures, the six KAN, the five waterno2 and ann_cumene_tanh carry no S
  mark. This was checked here from `R/bound-audit/pages.json`, fetched
  2026-09-30. The status refresh found the marks unchanged on 2026-10-02. The
  record refers to "MINLPLib's 1e-6 rule", but the S mark is not a function of the
  best single-solver gap alone. For example, 4stufen lists an ANTIGONE dual bound
  equal to its primal value and still has no S mark; its listing dual is
  COUENNE's. The paper should quote MINLPLib's own definition of "solved" (PT-10)
  and use (a) for the phrase "listed as open".
- **(b) The scout's rule.** Take the best listed single-solver dual bound and the
  best listed point with infeasibility ≤ 1e-8. Compute
  `|p − d| / min(|p|, |d|)` (∞ if the signs differ or one value is 0). The
  instance is open if this exceeds 1e-4, or if it has no listed point or no finite
  listed dual. The candidate set
  (`R/open-instances-scout/targets.md` §1) consists of the instances that are
  nonconvex, have a heuristic factor-incidence width ≤ 16 (or a nonlinear-primal
  width ≤ 6 with ≥ 50 nonlinear variables), have a metadata gap > 1e-4 (or ∞),
  and are not among the 11 first-wave instances.

### 2.2 Coverage funnel

All counts were recomputed for this dossier
(`checks/pattern-theory/logs/coverage_checks.log`).

| step | count | source |
|---|---|---|
| MINLPLib instances (listing, 2026-09-30) | 1633 | `R/bound-audit/pages.json` |
| nonconvex (MINLPLib flag) | 1257 | same |
| nonconvex without S mark | 596 | same |
| … and width rule (census heuristic upper bounds) | 360 | `R/treewidth-census/census_merged.json` (1632 instances; `fct` has no OSIL in the cache) |
| … and metadata gap > 1e-4 or ∞ | **294** = 283 scout candidates + 11 first-wave instances | same |
| … and best single-solver gap > 1e-4 (rule (b)) | **155** = 146 scout + 9 first-wave | `R/open-instances-scout/fetched.json`; recount from `pages.json` |
| closed by this work, among the 155 | **29** (20 second-wave and later + 9 first-wave) | summary |
| closed by this work with a prior best single-solver gap ≤ 1e-4 | 2 (camshape100 1.2157e-6; lnts50 3.8249e-5) | summary; recount |
| other paper instances among the 155 | 12 (6 KAN: relaxation R certified, OSIL infeasible; 5 waterno2 and ann_cumene_tanh: improved) | summary |

The 146 scout instances by band (recounted):

- 25 have no listed feasible point.
- 3 have no finite listed dual: ann_cumene_tanh, cesam2cent, quantum.
- 15 have an infinite relative gap.
- 33 have a gap ≥ 1; 30 are in [0.1, 1); 19 in [0.01, 0.1); 21 in (1e-4, 0.01).
- 4 have absolute gaps below 1e-5: bayes2_20, bayes2_30, wastepaper5, ex8_5_1.

A second recount from the bound audit's independent page parse (fetched one day
later with different code) gives the same 146 with zero mismatches. None of the
294 candidates carries an S mark.

**Selection caveats the paper must state.**

- The first wave was not selected by this rule. It was picked from the partial
  census: constant-width families whose metadata gaps grow with size (camshape,
  lnts), plus very large chain instances with trivial dual bounds (dtoc5,
  optcdeg2, lukvle10) (`R/root-research-log.md`, 2026-09-29). The funnel above
  is a post hoc reconstruction.
- The second-wave targets were ranked by judged tractability × payoff (scout §6).
  So 29/155 measures what this targeted effort achieved. It does not measure how
  hard the open population is.
- The widths are min-degree elimination upper bounds. Neither the census nor the
  scout was independently reviewed. The counts and shares reproduce from the
  saved data (this dossier; the closing audit checked the census shares 13.6% and
  62.7%).

### 2.3 Census context (optional for the paper)

The census covers 582 nonconvex instances with ≥ 100 nonlinear variables
(recounted):

| width bound | factor-incidence width | nonlinear-primal width |
|---|---|---|
| ≤ 4 | 27 (4.6%) | 278 (47.8%) |
| ≤ 12 | 79 (13.6%) | 365 (62.7%) |

The coupling note found that dualizing up to 8 linear rows raises the
factor-incidence share only to about 17%. That note uses a 14.8% baseline,
reproduced exactly by the coupling recheck. Small interaction width among the
nonlinear terms is common; small width once linear rows are counted is not.

---

## 3. The certificate pattern: statements and proofs

### 3.0 The idea in plain words

A single-tree solver bounds the whole model at once by relaxing each nonconvex
term separately. The class-A certificates instead cut the model along its stage
structure. Each stage gets an extra function of the variables it shares with its
neighbours: added on one side, subtracted on the other, so the total objective is
unchanged. Each stage, with its extra functions, is then a small problem, and its
minimum can be computed rigorously. The sum of these minima is a valid lower bound.
The extra functions are Lagrange multipliers (when affine) or approximate value
functions (calibrations). They are taken from a good local solution.

The bound is exact if a single feasible point minimizes every stage problem. This
fails only where no function of the chosen kind fits between the cost-to-come and
the cost-to-go at that separator; the theorems below call the region between these
two functions the "band". There, a few stages are merged into one exact window and
solved by a small branch and bound.

### 3.1 Setting and notation

Use the path form (P) of Section 1.2. Assume `f*` is finite and each `F_t` is
bounded below on `K_t`. A **split** is a tuple `φ = (φ_1, …, φ_{N−1})` of
real-valued functions `φ_t : R^{k_t} → R`, with `φ_0 = φ_N = 0`. The split bag
functions and the split bound are

```
F_t^φ(z_t) = F_t(z_t) + φ_t(π^R_t z_t) − φ_{t−1}(π^L_t z_t),        B(φ) = Σ_{t=1}^N inf_{K_t} F_t^φ.
```

For a transcription with stages `ρ_t = ℓ_t + S_{t+1} − S_t`, `φ` is a family of
discrete calibration (Krotov) functions `S_t`, and `B` is the calibration bound of
`R/theory-calibration/scouting.md` Definition 2.1. A **class** `Φ_t` is a linear
space of real functions on `R^{k_t}` containing the constants.
`gap(Φ) = f* − sup_{φ ∈ ΠΦ_t} B(φ)`.

For a separator `τ ∈ {1, …, N−1}`, define the head and tail value functions
(with `inf ∅ = +∞`):

```
Γ_τ(s) = inf { Σ_{t≤τ} F_t(z_t) : bags 1..τ feasible and consistent, π^R_τ z_τ = s }   (cost-to-come),
V_τ(s) = inf { Σ_{t>τ} F_t(z_t) : bags τ+1..N feasible and consistent, π^L_{τ+1} z_{τ+1} = s }   (cost-to-go).
```

Then `f* = inf_s (Γ_τ + V_τ)`, `Γ_τ > −∞` and `V_τ > −∞`. Put `L_τ = f* − Γ_τ`
(values in `[−∞, ∞)`) and `U_τ = V_τ` (values in `(−∞, ∞]`). Then `L_τ ≤ U_τ`
everywhere, with equality exactly at the optimal separator values (the *pinch
set*). The **band** is
`Band_τ = {ψ : R^{k_τ} → R : L_τ ≤ ψ ≤ U_τ}`; it is nonempty, since
`min(max(0, L_τ), U_τ)` is in it. Distances use the sup norm over `R^{k_τ}`:
`dist(Φ, B) = inf{ sup_s |φ(s) − ψ(s)| : φ ∈ Φ, ψ ∈ B }`, and
`osc(g) = sup g − inf g`.

### 3.2 Lemma 1 (validity of split bounds)

**Lemma 1.** For every split `φ`, `B(φ) ≤ f*`. The same holds if every `K_t` is
replaced by a set `K′_t` that contains the projection on bag `t` of the feasible set
of (P).

*Proof.* For consistent `z`, every `φ_t(s_t)` appears once with a plus sign (bag
`t`) and once with a minus sign (bag `t+1`), so
`Σ_t F_t^φ(z_t) = Σ_t F_t(z_t)`. For feasible `z`, each `F_t^φ(z_t) ≥ inf_{K′_t} F_t^φ`. □

*Status.* Classical: Krotov's discrete sufficient condition, the Bellman
inequality of approximate DP, cost shifting in graphical models. It is Lemma 2.1
of the calibration note (reviewed, rechecked, confirmed). Nothing computational is
trusted here. For an instance, what must be trusted is the rigorous evaluation of
each `inf_{K′_t} F_t^φ` (family dossiers) and the validity of the enclosures `K′_t`.

### 3.3 Proposition 2 (affine splits: Lagrangian duality, exactness, forced slopes)

Let `φ_t(s) = λ_t^T s + c_t`.

(a) `B(φ)` does not depend on `c`. It equals the Lagrangian dual function of the
*copy formulation*: each bag gets its own copy of every separator, and the copy
constraints `π^R_t z_t − π^L_{t+1} z_{t+1} = 0` are dualized with multipliers
`λ_t`.

(b) *Exactness criterion.* If a feasible `z̄` has `z̄_t ∈ argmin_{K_t} F_t^φ` for
every `t`, then `B(φ) = f* = Σ_t F_t(z̄_t)`, and `z̄` is globally optimal.
Conversely, if `B(φ) = f*` and `f*` is attained at `z*`, then
`z*_t ∈ argmin_{K_t} F_t^φ` for every `t`.

(c) *Slopes are forced.* Suppose `B(φ) = f*`, `f*` is attained at `z*`, each `F_t`
is `C¹` near `z*_t`, and `z*_t` is interior to `K_t`. Then for every coordinate
`i` of `s_τ`,
`λ_{τ,i} = −Σ_{t ≤ τ, i ∈ z_t} ∂_i F_t(z*_t)`.
So the slopes are uniquely determined: they are the multipliers of the copy
constraints at `z*`. For transcriptions in which the dynamics rows are kept as
`x_{t+1} = g_t(x_t, u_t)` and the controls stay interior, the same argument gives
the discrete costate recursion `p_t = ∇_x ℓ_t + (D_x g_t)^T p_{t+1}`
(calibration note, Theorem 3.1(3)).

*Proof.*
- (a) Expand `Σ_t F_t^φ`. The constants telescope. The terms
  `λ_t^T π^R_t z_t − λ_t^T π^L_{t+1} z_{t+1}` are exactly the dualized copy
  constraints.
- (b) Write `Σ_t inf F_t^φ = B(φ) ≤ f* ≤ Σ_t F_t(z̄_t) = Σ_t F_t^φ(z̄_t)`. If every
  `z̄_t` attains its infimum, the outer terms are equal.
  For the converse: `Σ_t F_t^φ(z*_t) = f* = Σ_t inf F_t^φ`, and each term is at
  least its infimum, so each term attains it.
- (c) An interior minimizer of `F_t^φ` has zero gradient. In bag 1 this gives
  `∂_i F_1 + λ_{1,i} = 0`. A coordinate `i` shared by bags `a..b` appears in
  bag `t` (`a < t < b`) with `+λ_{t,i} − λ_{t−1,i}`, so
  `λ_{t,i} = λ_{t−1,i} − ∂_i F_t`. Induct. □

*Status.* Classical in substance: discrete Mangasarian/Arrow sufficiency (Tamminen;
Krotov); Wald–Globerson's tightness result is the convex case. It is consistency
note Proposition 5.1 and calibration note Theorem 3.1, both reviewed. The
calibration review found Theorem 3.1 correct (small fix F4); the converse needs
`f*` attained.

*Use.* (c) is why every class-A certificate takes its multipliers from one local
KKT solve. (b) is the per-stage check:
- dtoc5: each residual is a strictly convex quadratic because `λ_t < 1/4`
  (discrete Mangasarian);
- lnts: the per-stage maximum is in closed form (Arrow, linear-tangent law);
- lukvle10: exact on all pairs except the end transient.

### 3.4 Proposition 3 (exact windows)

For `1 ≤ a ≤ b ≤ N` define

```
β_{[a,b]}(φ) = inf { Σ_{t=a}^b F_t(z_t) + φ_b(π^R_b z_b) − φ_{a−1}(π^L_a z_a) : z_t ∈ K_t, consecutive copies agree }.
```

Then `B(φ) ≤ B_{[a,b]}(φ) := Σ_{t∉[a,b]} inf_{K_t} F_t^φ + β_{[a,b]}(φ) ≤ f*`.
Disjoint windows combine.

*Proof.* Inside the window the split terms telescope, so the window objective is
`Σ_{t=a}^b F_t^φ(z_t)`. Its infimum is at least the sum of the separate
infima. The upper bound is Lemma 1 for the path in which bags `a..b` are merged
into one bag. □

*Status.* Calibration note Proposition 4.4 (proved; reviewed). A window is the
"full class" on separators `a, …, b−1`. Its cost is one global problem in the
window's free variables:
- lukvle10: 2-D, because the recurrence fixes the window from its entry pair;
- chain: the 2-D end values with per-box field parameters;
- optcdeg2 (earlier certificate only): 3080 stages, solved by a monotonicity
  argument without branching.

### 3.5 Proposition 4 (cellwise slopes and shortest paths; the waterno2 scheme)

For each separator `t ∈ {1, …, N−1}`, let `𝒫_t` be a finite family of sets (cells)
whose union contains the bag-`t` projection of every feasible point's `s_t`. Give
each cell `D ∈ 𝒫_t` a slope vector `λ_{t,D}`. Put `𝒫_0 = 𝒫_N = {∗}` with zero
slopes. For each bag `t` and pair `(D, D′) ∈ 𝒫_{t−1} × 𝒫_t`, let

```
b_t(D, D′) ≤ inf { F_t(z) + λ_{t,D′}^T π^R_t z − λ_{t−1,D}^T π^L_t z : z ∈ K_t, π^L_t z ∈ D, π^R_t z ∈ D′ }.
```

Then

```
f* ≥ SP := min over cell sequences (D_1, …, D_{N−1}) of Σ_{t=1}^N b_t(D_{t−1}, D_t),
```

a shortest path in a layered graph.

*Proof.* Let `z` be feasible. For each `t`, choose `D_t ∈ 𝒫_t` containing `s_t`.
The terms `λ_{t,D_t}^T s_t` appear with `+` in bag `t` and `−` in bag `t+1`, at the
same point `s_t`. So
`Σ_t F_t(z_t) = Σ_t [F_t(z_t) + λ_{t,D_t}^T s_t − λ_{t−1,D_{t−1}}^T s_{t−1}] ≥ Σ_t b_t(D_{t−1}, D_t) ≥ SP`. □

*Remarks.*

1. The only coupling condition is that a cell's slope be used for both bags meeting
   at that separator. This is exactly the validity condition of
   `R/open-instances-wave2/waterno2/cell-slopes.md` Proposition 1, which the
   cell-slope review found correct.
2. Per-cell constants add nothing. They telescope along every path. With exact pair
   infima, SP equals the supremum of `B(φ)` over cellwise-affine splits with these
   slopes. This is LP duality for shortest paths: take the constants to be Bellman
   distance labels.
3. One cell per separator recovers Proposition 2. Zero slopes give the
   cell-constant DP that failed on camshape100 (Proposition 8 explains why constant
   cells are expensive).

*Status.* The validity statement was proved and reviewed for waterno2_06. The
generic form and Remark 2 were written for this dossier and have not been
independently reviewed; they are elementary. The closest prior analogue: shortest
paths on a cell graph with per-cell minima give value-function lower bounds
(Junge–Osinga 2004, per the literature audit).

### 3.6 Theorem 5 (band identity for one separator)

For `τ ∈ {1, …, N−1}` and `φ : R^{k_τ} → R`, let

```
Δ_τ(φ) = f* − inf_s [Γ_τ(s) + φ(s)] − inf_s [V_τ(s) − φ(s)]  ≥ 0.
```

This is the gap of the split bound in which bags `1..τ` and bags `τ+1..N` are
each merged into one exact window and only separator `τ` carries the split `φ`.

**Theorem 5.** For every class `Φ_τ`, `inf_{φ ∈ Φ_τ} Δ_τ(φ) = 2 dist(Φ_τ, Band_τ)`.

*Proof.* The identity
`Δ_τ(φ) = sup_s (L_τ − φ) + sup_s (φ − U_τ)`
holds because `f*` is a finite constant. Points where `L_τ = −∞` (or `U_τ = +∞`)
contribute nothing to the first (or second) supremum. Both suprema are taken over
nonempty sets, because `f*` is finite.

- (≤) Let `ψ ∈ Band_τ` and `φ ∈ Φ_τ`. From `L_τ ≤ ψ ≤ U_τ` we get
  `Δ_τ(φ) ≤ sup(ψ − φ) + sup(φ − ψ) = osc(φ − ψ)`. Because `Φ_τ` contains the
  constants, `inf_{φ∈Φ_τ} osc(φ − ψ) = 2 inf_{φ∈Φ_τ} sup|φ − ψ|`. Take the infimum
  over `ψ`.
- (≥) Fix `φ` with `Δ_τ(φ) < ∞`. Put `a = sup(φ − U_τ)` and
  `b = sup(L_τ − φ)`; both are finite.
  - On the common domain, `L_τ − U_τ = f* − Γ_τ − V_τ`, whose supremum is 0. So
    `a + b ≥ 0`.
  - Let `φ̃ = φ + (b − a)/2 ∈ Φ_τ`. Then both suprema equal `δ = (a + b)/2`, and
    `Δ_τ(φ̃) = Δ_τ(φ) = 2δ`.
  - Clip: `ψ = min(max(φ̃, L_τ), U_τ)`. It is real-valued because
    `L_τ < +∞` and `U_τ > −∞`. It lies in `Band_τ` because `L_τ ≤ U_τ`.
  - Where `φ̃ > U_τ`: `ψ = U_τ` and `0 < φ̃ − ψ ≤ δ`. Where `φ̃ < L_τ`:
    `ψ = L_τ` and `−δ ≤ φ̃ − ψ < 0`. Elsewhere `ψ = φ̃`.
  - So `dist(Φ_τ, Band_τ) ≤ sup|φ̃ − ψ| ≤ δ = Δ_τ(φ)/2`. □

*Consequences.*

1. One separator loses nothing iff `dist(Φ_τ, Band_τ) = 0`. For finite-dimensional
   classes and continuous band edges on a compact domain, the infimum is attained,
   so this happens iff the class contains a band element (consistency note,
   Corollary 2.2(1)). For the affine class on a box, this means an affine function
   lies between `f* − Γ_τ` and `V_τ`, that is, `cav(f* − Γ_τ) ≤ vex V_τ`
   (consistency note, Proposition 5.1(4)).
2. Every band element passes through the pinch points, where
   `L_τ(s*) = U_τ(s*)`. Away from them the band has width `Γ_τ + V_τ − f* > 0`, and
   errors are free up to that width. So the loss of a split is decided near the
   optimal separator values. Kinks of value functions elsewhere are harmless.
3. *Pinch regularity (remark, not needed in the paper).* Suppose `V_τ` is
   semiconcave and `Γ_τ` semiconvex near an interior pinch point. Then both are
   differentiable there with a common gradient (the multiplier of Proposition
   2(c)), and the tangent plane lies within `O(|s − s*|²)` of the band
   (consistency note, Lemma 4.2; classical). On product domains semiconcavity holds
   automatically (Lemma 4.1). For dynamics-constrained stages it is a hypothesis
   (calibration note §2.3).

*Status.* Consistency note Theorem 2.1 (proved; review: "correct, with the exact
constant 2"; recheck and two confirmations found no error). The version above
allows extended-valued value functions and needs only `f*` finite and `F_t`
bounded below. The calibration review (F1) checked that the one-separator identity
carries over to extended values. The statement here was rewritten for this
dossier.

### 3.7 Theorem 6 (path sandwich) and Proposition 7 (per-separator band membership is not enough)

**Theorem 6.** For classes `Φ_1, …, Φ_{N−1}`,

```
2 max_τ dist(Φ_τ, Band_τ)  ≤  gap(Φ)  ≤  2 inf_{ψ ∈ E} Σ_τ dist(ψ_τ, Φ_τ),
```

where `E` is the set of real-valued splits with `B(ψ) = f*` and `inf ∅ = +∞`.

*Proof.*
- *Lower bound.* Fix `τ` and `φ ∈ ΠΦ_t`.
  - Apply Lemma 1 to the head problem: bags `1..τ`, with `F_τ` replaced by
    `F_τ + φ_τ(π^R_τ z_τ)`, using the split `(φ_1, …, φ_{τ−1})`. This gives
    `Σ_{t≤τ} inf F_t^φ ≤ inf_s[Γ_τ(s) + φ_τ(s)]`.
  - Apply it to the tail problem: bags `τ+1..N`, with `F_{τ+1}` replaced by
    `F_{τ+1} − φ_τ(π^L_{τ+1} z_{τ+1})`. This gives
    `Σ_{t>τ} inf F_t^φ ≤ inf_s[V_τ(s) − φ_τ(s)]`.
  - Adding: `f* − B(φ) ≥ Δ_τ(φ_τ) ≥ 2 dist(Φ_τ, Band_τ)` by Theorem 5. Take the
    supremum over `φ` and the maximum over `τ`.
- *Upper bound.* Let `ψ ∈ E`, `φ ∈ ΠΦ_t` and `r_t = φ_t − ψ_t`. Then
  `F_t^φ = F_t^ψ + r_t − r_{t−1} ≥ inf F_t^ψ + inf r_t − sup r_{t−1}`.
  Summing gives `B(φ) ≥ f* − Σ_t osc(r_t)`. Minimizing `osc(φ_t − ψ_t)` over
  `φ_t ∈ Φ_t` gives `2 dist(ψ_t, Φ_t)`, because the constants are in `Φ_t`. □

This lower-bound proof is simpler than the one in the consistency note, which
first enlarges every other class to the full class and uses exactness of full-class
splits. It needs no compactness or continuity.

**Proposition 7.** On `[0, 1]²`, take three bags `a(s_1) = 10(1 − s_1)`,
`b(s_1, s_2) = s_1 + s_2 − s_1 s_2` and `c(s_2) = 10(1 − s_2)`, with constant
classes on both separators. Each band contains a constant, yet `gap = 1`.

*Proof.* `F` is multilinear, so `f* = min over vertices = F(1,1) = 1`. Constant
splits telescope, so `B = min a + min b + min c = 0`.
- Separator 1: `Γ_1 = 10(1 − s_1)` and `V_1(s_1) = min_{s_2}(b + c) = 1`, because the
  coefficient of `s_2` is `−9 − s_1 < 0`. The constant 1 lies in
  `[10 s_1 − 9, 1]`.
- Separator 2: `Γ_2 = 1` and `V_2 = 10(1 − s_2)`. The constant 0 is in the band. □

(Checked in exact rationals: `checks/pattern-theory/logs/band_checks.log`.) So
diagnostics computed edge by edge from the original bands can report zero loss on
every separator while the gap is 1. The upper bound of Theorem 6 needs one *jointly*
exact split.

*Status.* Consistency note Theorem 3.1 and Proposition 3.3 (proved; reviewed;
"correct"). Both ends of the sandwich are attained in some instances. The upper end
is attained in a separable example (T1, `K = 0`). The lower end is attained in 515
of 900 random three-bag instances, with 93 of them having both edge terms positive.
In T1 the lower end is approached as `K → ∞` but not attained at finite `K`
(proved). The path specialization with the DP split is the deterministic
finite-horizon approximate-LP bound of de Farias–Van Roy.

### 3.8 Proposition 8 (cells with constant splits: the worst cell decides, and many cells are needed)

Let `𝒫` partition `R^{k_τ}`, and let `PC(𝒫)` be the functions constant on each cell.

(a) `inf_{φ ∈ PC(𝒫)} Δ_τ(φ) = max_{D ∈ 𝒫} ( sup_D L_τ − inf_D U_τ )`. Hence every
path split bound whose class on separator `τ` is `PC(𝒫)` has a gap at least this
large.

(b) Let `k_τ = 1` and let `s*` be a pinch point. Suppose that on
`W = [s* − r, s* + r]`, with `r = √(2ε/M)`, `L_τ` is monotone with
`|L_τ(s″) − L_τ(s′)| ≥ (|λ|/2)|s″ − s′|`, and `U_τ − L_τ ≤ (M/2)(s − s*)²`.
If a path split bound with class `PC(𝒫)` on separator `τ` has gap `≤ ε`, then at
least `|λ| / √(2Mε)` cells meet `W`. Since the gap bound must hold at every
separator, the cell counts add over separators. With constant cells, the total is
at least `Σ_τ |λ_τ| / √(2 M_τ ε)` over the separators where the hypotheses hold.

*Proof.*
- (a) For `φ = Σ_D c_D 1_D`, `sup(L − φ) = max_D (sup_D L − c_D)` and
  `sup(φ − U) = max_D (c_D − inf_D U)`. Each cell's pair sums to
  `g_D = sup_D L − inf_D U`, independent of `c_D`. Choosing `c_D` to split each
  `g_D` evenly makes both maxima `≤ max_D g_D / 2`. Every choice gives at least
  `max_D g_D`. The last claim follows from the lower-bound step of Theorem 6, which
  shows `gap ≥ inf_{φ∈Φ_τ} Δ_τ(φ)`.
- (b) Take `s′ < s″` in `D ∩ W` and `L` increasing (the decreasing case is
  symmetric). Then
  `g_D ≥ L(s″) − U(s′) = L(s″) − L(s′) − (U − L)(s′) ≥ (|λ|/2)(s″ − s′) − ε`.
  So gap `≤ ε` forces `diam(D ∩ W) ≤ 4ε/|λ|`, and covering `W` (length
  `2r = 2√(2ε/M)`) needs at least `2r|λ|/(4ε) = |λ|/√(2Mε)` cells. □

*Status.* (a) is consistency note Proposition 2.3 (proved; checked against a joint
LP). (b) is its Proposition 5.2 (proved, 1-D). The adding-up remark was written for
this dossier. The analogue in the decomposition note is Proposition 2.6: constant
child bounds need `|λ*|/(6√(M_F ε))` cells. It is the certificate-size form of
Robertson–Cheng–Scott's order distinction: constant bounds converge at first order,
Lagrangian bounds at second order.

*Use.* This explains, in the idealized exact-bag model, why the generic
cell-constant separator DP failed on camshape100 and why every working class-A
certificate used slopes (affine, quadratic, field-type or concave chord). It is
"consistent with" the camshape failure, not a proof of it (PT-8). The camshape
cell DP also relaxed rows cellwise, and the measured obstacle was a per-stage
constraint scale of order `1/n²`.

### 3.9 Duality (remark)

For compact bags and continuous data, `sup_{φ∈ΠΦ_t} B(φ)` equals the minimum over
bag probability measures whose neighbouring separator marginals agree on `Φ_t`.
This holds also for any weak*-compact convex per-bag relaxation, such as sparse
moment relaxations, which correspond to polynomial classes. This is consistency
note Theorem 1.1, known in substance: cost-shifting/reparametrization duality
(Wainwright–Jaakkola–Willsky; Werner; Sontag–Globerson–Jaakkola; Wald–Globerson),
sparse moment relaxations (Waki et al. 2006; Lasserre 2006), gluing (Vorob'ev
1962). The paper needs at most one sentence.

### 3.10 The class-A certificates in this language

| instance(s) | split class on separators | why the split is exact or nearly so | exact windows | branching |
|---|---|---|---|---|
| dtoc5 | affine (costates) | each residual is a strictly convex quadratic (Proposition 2(b), discrete Mangasarian) | none | none |
| lnts50–400 | affine for each fixed `h` (aggregated rows) | minimized Hamiltonian affine in the state; closed-form per-stage maximum (Arrow) | global `h` by monotonicity | none |
| lukvle10 | affine (pair Lagrangian) | exact except at the end transient, where the pair Lagrangian is nonconvex | 3 pairs, entry state 2-D | 2-D interval B&B (tail 48,628 boxes) |
| optcdeg2 | quadratic in `v`, curvature `q_t` vanishing at both switches | the affine split fails where `λ_t < 0` makes the `v`-terms concave (no affine band element there); the quadratic class contains band elements | none (final certificate) | per-stage 1-D cells |
| chain50–400 | field type in a lifted state (Weierstrass field) | closed-form lemma, equality along the optimal chain; the fixed-multiplier length Lagrangian fails because the length row is effectively reverse-convex | 2-D end window | 2-D interval B&B |
| catmix100–800 | concave piecewise-linear homogeneous value-function bounds (a DP; a "state-localized Lagrangian") | concavity makes chord interpolation second order (calibration note Proposition 2.3) | none | per-ray 1-D B&B over `u` |
| waterno2_06 (not closed) | cellwise affine (Proposition 4) | gap 1.68% remains | each period is a bag of 166 variables | per cell pair |

What the theory adds to this table:
- the exactness test (Proposition 2(b));
- where the multipliers must come from (Proposition 2(c));
- that the loss of a restricted class is decided at the optimal separator values
  (Theorem 5);
- that windows are the full class on a few separators (Proposition 3), which
  removes those separators' terms from Theorem 6;
- why constant cells need about `|λ|/√(Mε)` cells per separator while slopes avoid
  this (Proposition 8).

The theory does not predict which split class works for a given instance, and it
gives no certificate-size bound for these instances.

### 3.11 Theory results reviewed and excluded

| result (location) | status | reason for exclusion |
|---|---|---|
| Single-tree lower bound for termwise McCormick, `0.57(5/3)^n` (face-exact note, Theorem 1) | proved; reviewed and rechecked; post-recheck fixes (§13 item 5) not rechecked | concerns a synthetic path family; does not apply to the MINLPLib instances. For ODE transcriptions no exponential single-tree bound is known (calibration note, Corollary 3.8 caveats). It is about a fixed relaxation class: SCIP's PSD-minor cuts escape it. Mention at most as a pointer to a companion report |
| Decomposition certificates: Theorem 3.4, adaptive algorithms, covering upper half, GR (decomposition notes) | proved/reviewed with stated gaps; §8.1 fixes of the main note not rechecked | existence/complexity results on synthetic families with numerically vacuous constants; overlaps the theme of `paper-decomposition-aware/` |
| Split-robust lower bounds; RLCT; dense coupling | proved/reviewed, with tiny bases or largely negative results | unrelated to the certificates |
| hp and polynomial rates, sparse-moment link, shell count (consistency note §5.3–5.5) | proved, partly sketches (Proposition 4.3) | not used by any certificate |
| Window law, tangential calibrations, `κ_τ` trichotomy, singular arcs (bang-bang notes); transfer theorem (calibration note, Theorem 5.2) | proved under stated hypotheses; several parts at sketch level | asymptotics in the mesh size; no certificate in the paper depends on them. The optcdeg2 dossier may cite the `κ = 0` discussion |

---

## 4. Exactly feasible primal points

This does not apply at the pattern level. Proposition 2(b) is the only primal
statement: a split certificate is exact iff one feasible trajectory minimizes every
stage residual. In practice, class-A certificates are built around a numerically
optimal trajectory, and their exactness up to rounding confirms it. The exactly
feasible points (rational, algebraic or interval-existence proofs) are documented in
`R/publication/primal/` and in the family dossiers. For lukvle10, the KKT agreement
is numerical: attributing the remaining gap to the dual side assumes the KKT point
is globally optimal.

---

## 5. Numbers

### 5.1 Coverage numbers

See Section 2.2. Every number there was recomputed in
`checks/pattern-theory/logs/coverage_checks.log`.

### 5.2 Class-A instances (authoritative displays from `R/open-instances-summary.md`)

Gap cells are rounded upward. Exact sources are in
`R/publication/integration/gap-values.json`. Chain and catmix individual duals are
the safe displays of `R/publication/reproduction/cops/logs/exact_display_checks.json`;
the summary itself shows only ranges for them. Listed duals are best single-solver
values from `R/open-instances-scout/fetched.json` and `R/bound-audit/pages.json`.

| instance | best listed dual (solver) | our rigorous dual (safe display) | primal (upper end, exactly feasible) | gap (rounded up) |
|---|---|---|---|---|
| lnts50 | 0.55464755 (GUROBI) | 0.5546687649381 | 0.5546687649387 | ≤ 5.79e-13 |
| lnts100 | 0.55299042 (GUROBI) | 0.5545954011663 | 0.5545954011670 | ≤ 6.12e-13 |
| lnts200 | 0.55219867 (GUROBI) | 0.5545770161025 | 0.5545770161031 | ≤ 5.84e-13 |
| lnts400 | 0.55204395 (GUROBI) | 0.5545724137001 | 0.5545724137007 | ≤ 5.88e-13 |
| dtoc5 | 0.00243096 (BARON) | 5.38967211918114 | 5.389672119181141 | ≤ 4.7e-16 |
| lukvle10 | 351.223393 (SCIP) | 352.2380254050784 | 352.2380254064961 | ≤ 1.5e-9 |
| optcdeg2 | 292.41713458 (GUROBI) | 293.87607509587509 (certificate rounded down) | ≤ 293.87607509587509328 | ≤ 9e-16 |
| chain50 | 0.17451499 (ANTIGONE) | 5.0722614939828627 | 5.07226149398287232 | ≤ 9.7e-15 |
| chain100 | 0.09367008 (ANTIGONE) | 5.0697846107387505 | 5.06978461073876056 | ≤ 1.01e-14 |
| chain200 | 0.08256615 (ANTIGONE) | 5.0689173417931616 | 5.06891734179317101 | ≤ 9.5e-15 |
| chain400 | 0.09563835 (ANTIGONE) | 5.068621694604009 | 5.06862169460401902 | ≤ 1.01e-14 |
| catmix100 | −0.06655801 (LINDO) | −0.048069432031144562 | −0.0480694320309595629 | ≤ 1.85e-13 |
| catmix200 | −0.07254639 (LINDO) | −0.048059145599072769 | −0.0480591455801143935 | ≤ 1.90e-11 |
| catmix400 | −0.65810523 (LINDO) | −0.048056547824671288 | −0.0480565477566115548 | ≤ 6.81e-11 |
| catmix800 | −1.48896963 (LINDO) | −0.048055901479675652 | −0.0480559013312308003 | ≤ 1.49e-10 |

The primal displays for chain and catmix are the stored upper ends, truncated
upward. I recomputed the chain and catmix gap cells by exact subtraction (log):
9.6164e-15, 1.0057e-14, 9.4002e-15, 1.0014e-14; 1.8500e-13, 1.8958e-11,
6.8060e-11, 1.4844e-10. All are consistent with the summary. The summary's
catmix100 cell uses the verifier's stronger dual and the authors' exact point; its
catmix800 cell uses the verifier's exact DP-policy point.

No disagreement with the summary was found. Two older displays should not be used.
`R/SYNTHESIS.md` gives waterno2_06 as "1.67%": the exact ratio from the displays is
`(282.888038 − 278.230573)/278.230573 = 1.674%`, so the safe display is the
summary's ≤ 1.68%. `R/SYNTHESIS.md` gives ann_cumene_tanh as "0.194%": that is
valid only with the dual denominator (0.19365%). With the summary's primal
denominator the value is 0.19402%, displayed as ≤ 0.195%.

### 5.3 Evidence on "relaxation versus branching" from saved solver logs

The facts below were read from the one-hour SCIP 10.0.3 campaign logs (1 thread,
gap requests 1e-9; `checks/pattern-theory/logs/scip_log_facts.log`). "First
logged" is the dual bound on the first progress line; it is not necessarily the
final root bound.

| instance | B&B nodes in 1 h | first logged dual | final dual | certified value | reading |
|---|---|---|---|---|---|
| hvycrash | 504,455 | −2.185e8 | −2.185e8 | −0.2185 (exact) | bound never moves; the relaxation, driven by free `r`, is the obstacle |
| catmix100/200/400/800 | 1,347 / 1,781 / 246 / 865 | none | −1e20 (no finite bound) | ≈ −0.0481 | free states; BARON reports "globality not guaranteed (inappropriate variable bounds)" |
| powerflow0030p | 23,036 | 0 | 0 | 576.8934122988004 | bound never moves |
| dtoc5 | 1 | 1.9999e-5 | 1.9999e-5 | 5.38967211918114 | never leaves the root (overloaded first batch) |
| optcdeg2 | 1 | 200.1336 | 200.1336 | 293.87607509587509 | never leaves the root (overloaded first batch) |
| chain50 / chain400 | 53,029 / 7 | −240.69 / −1930.8 | −74.906 / −1673.2 | 5.0723 / 5.0686 | trivial bounds; free variables, dense reverse-convex length row |
| lnts50 | 79,792 | 0.45 | 0.51879 | 0.55467 | slow progress |
| camshape100 | 1,179,749 | −5.163 | −4.52868 | −4.28414712 | steady but slow progress with branching: 5.7% short |

Caveats:
- This is one solver and one budget.
- The dtoc5 and optcdeg2 runs belong to the overloaded first batch (READINESS,
  open decision 2).
- The ex6_2_5, ex6_2_7 and pindyck SCIP runs stopped at the memory limit.
- The campaign analysis was reviewed (solver-analysis review r1, issues fixed).
  This particular extraction was not.

---

## 6. Verification record

| item | evidence | verdict | remaining assumptions/caveats |
|---|---|---|---|
| Lemma 1, Proposition 2, Proposition 3 | calibration note (Lemma 2.1, Theorem 3.1, Proposition 4.4) and consistency note (Proposition 5.1); `R/reviews/calibration-review.md`, `calibration-recheck.md`, `recheck-calibration-confirm.md`; consistency reviews below | review: Theorem 3.1 "correct (small fix F4)"; recheck: no mathematical error; confirmation: all fixes correct, four wording points applied by the root (not rechecked) | classical in substance |
| Theorem 5, Theorem 6, Propositions 7 and 8 | consistency note Theorem 2.1, Theorem 3.1, Propositions 2.3, 3.3, 5.2; `R/reviews/consistency-review.md` (every proof in §§1–5 checked line by line; "I found no false theorem"), `consistency-recheck.md` ("no proof is wrong"; one false interpretive claim withdrawn), `recheck-consistency-confirm.md` and `consistency-confirm-r1.md` (no mathematical error) | proved and reviewed four times | idealized exact-bag model; the link to the open-instance certificates is interpretive (the note says so, §10) |
| Proposition 4 (validity) | `R/open-instances-wave2/waterno2/cell-slopes.md` Proposition 1; `R/reviews/waterno2-cellslopes-review.md` ("correct; the only coupling condition is one vector per cell") | reviewed | generic restatement and Remark 2 written here; not reviewed |
| Restatements in this dossier | extended-value path versions of Theorems 5–6 (simpler lower-bound proof), Proposition 2(c) sign convention, Proposition 8 adding over separators | proofs written here; numerically spot-checked (300 random one-separator instances: max \|gap − 2 dist\| = 3.9e-14; 200 random three-bag paths: no violation of the lower bound, lower end attained in 122; Proposition 7 exact) | **not independently reviewed**; recommend one confirmation pass (PT-5) |
| Scout counts (283, 146, bands) | `R/open-instances-scout/targets.md` (not reviewed); status refresh confirmed 39 of its parsed pages equal to the stored copies | reproduced here from `fetched.json` and independently from `R/bound-audit/pages.json` | widths are heuristic upper bounds; selection rule is one of many possible |
| Census shares | `R/treewidth-census/census-report.md` (not reviewed); closing audit checked 13.6%/62.7%; coupling review and recheck reproduced the related 14.8%/17% shares | reproduced here | heuristic widths; `fct` missing |
| Single-tree lower bound (excluded) | `R/reviews/face-exact-review.md`, `face-exact-recheck.md` | Theorems 1 and 2 correct | post-recheck fixes not rechecked |

---

## 7. Relation to prior work

Mechanisms (all classical):
- Lagrangian duality and decomposition.
- Discrete sufficient conditions: Krotov functions; the discrete
  Mangasarian/Arrow conditions; Tamminen's "Lagrangian minimized in state and
  control"; the pointwise form of Leitmann–Stalford.
- Bellman inequalities and the LP approach to approximate DP (de Farias–Van Roy
  2003, whose `2 ×` approximation-error bound is the one-sided form of Theorem 5 on
  paths).
- Cost-shifting/reparametrization duality in graphical models and weighted CSP
  (Wainwright–Jaakkola–Willsky 2005; Werner 2007; Sontag–Globerson–Jaakkola 2011;
  Cooper–de Givry–Schiex). Wald–Globerson (UAI 2014) give tightness for
  convex-decomposable continuous MRFs, the convex case of Proposition 2(b).
- Sparse moment relaxations as polynomial split classes:
  `waki2006-sums-of-squares-and-semidefinite`,
  `lasserre2006-convergent-sdprelaxations-in-polynomial-optimization`.
- The sufficiency direction of the band identity with positive band width:
  Grimm–Netzer–Schweighofer 2007, Lemma 3; quantitative form in
  Korda–Magron–Ríos-Zertuche 2025, Lemma 11. The zero-width identity is
  Han–Jiao–Weissman's.

New as far as the consistency note's searches found (elementary):
- the exact identity with constant 2 and its clipping proof;
- the worst-cell formula;
- the `2 max` lower bound on trees;
- the counterexample to edge-by-edge control.

These searches cannot establish priority.

Stagewise value-function minorants in multistage optimization: SDDP and nested
Benders decomposition with Lagrangian cuts are the stochastic-programming
counterpart of affine calibrations:
- Zou–Ahmed–Sun 2019;
- Zhang–Sun 2022, `zhang2022-stochastic-dual-dynamic-programming-for`;
- Füllner–Rebennack, `fullner2022-non-convex-nested-benders-decomposition`.

Junge–Osinga (2004) use shortest paths on cell graphs, with per-cell minima, for
value-function lower bounds; this is the closest analogue of Proposition 4 found by
the literature audit (`R/literature/decomposition-bb-prior.md` §1.6).
Robertson–Cheng–Scott 2025 (`robertson2025-on-the-convergence-order-of`; only
metadata in `literature/`, unread there; read via the audit) give the order-1 vs
order-2 distinction that Proposition 8 turns into a cell count. Global dynamic
optimization by branch and bound:
- Chachuat et al., `chachuat2005-global-mixed-integer-dynamic-optimization`;
- Houska–Chachuat (branch-and-lift, 2014; Hilbert space, 2019), with
  mesh-independent run-time bounds.

Why single-tree solvers struggle:
- The cluster problem: `neumaier2004-complete-search-in-continuous-global`,
  `wechsung2014-the-cluster-problem-revisited`,
  `kannan2017-the-cluster-problem-in-constrained`.
- B&B lower bounds and separations at small treewidth that rely on ties:
  `basu2023-complexity-of-branch-and-bound`, `dey2022-lower-bound-on-size-of`.
- Bound tightening for free variables: `belotti2009-branching-and-bounds-tightening-techniques`,
  `belotti2012-on-feasibility-based-bounds-tightening`.
- MINLPLib: `bussieck2003-minlpliba-collection-of-test-models`; site page
  `vigerske2026-minlplib-a-library-of-mixed`. The site states that "the reported
  dual bounds are just the best value as computed in some run with some option
  settings on some machine at some time in the past". This is useful when defining
  "listed".

Instance-level prior results (floating-point closures, likely ε-global results for
ex6_2_*, Göß–Burlacu–Martin, CAMINO) are in the summary's literature table and the
three literature reports. For the pattern section, credit the following:
- The pattern itself is not new as an idea. "Chain Lagrangian with multipliers from a
  local solution, plus exact treatment of nonconvex windows" is what DP and
  decomposition practitioners would try.
- The new elements are the rigorous certificates, the taxonomy and the explanatory
  identities.

---

## 8. Critical examination

### 8.0 What I re-derived and recomputed

- **Re-derived from scratch** (Section 3):
  - Lemma 1 and Propositions 2–4;
  - Theorem 5, in an extended-value version needing only `f*` finite and costs
    bounded below;
  - Theorem 6, with a simpler lower-bound proof by weak duality on the head and tail;
  - Proposition 7, in exact arithmetic;
  - Proposition 8, including the adding-up over separators.

  No error was found in the source proofs. The consistency note's tree lower-bound
  proof needs value functions to be bounded so that they belong to the "full class".
  The proof given here avoids that requirement, which matters for constrained stages.
- **Numerical spot checks** (`band_checks.py`, HiGHS LPs, floating point):
  - Theorem 5 on 300 random finite one-separator instances with the affine class:
    `max |gap − 2 dist| = 3.9e-14`.
  - Theorem 6 lower bound on 200 random three-bag paths: 0 violations; lower end
    attained in 122.
- **Coverage** (`coverage_checks.py`): all counts in Section 2.2, the census shares,
  and the headline ratios (camshape100 1.2157e-6; lnts50 3.8249e-5; waterno2 dual
  ratios 1.597, 3.011, 4.358, 6.216, 6.005 for wave 2, and 1.684 now for _06).
- **SCIP log facts** (`scip_log_facts.sh`): Section 5.3.

### 8.1 Issues and resolutions

**PT-1 (major, wording/definitions): two notions of "open".**
- The record says "31 instances listed as open" (no S mark) and "146 open among
  283 low-width nonconvex candidates" (scout rule). These are different
  predicates on different populations.
- camshape100 and lnts50 are open only in the first sense. The scout population
  excludes the first wave.
- *Resolution:*
  - Define "listed as open" = no S mark (quote MINLPLib's definition).
  - Define "open by the 1e-4 rule" separately.
  - Present the funnel of Section 2.2 (294 → 155 → 29 closed + 2 marginal), with
    the selection caveats.
  - No new computation is needed (done here).

**PT-2 (major, interpretation): "the obstacle was the relaxation, not the amount of
branching" is untested, and the dichotomy is not sharp.**
- Evidence for it:
  - hvycrash, powerflow0030p and catmix show no dual-bound progress in 1 h despite
    many nodes;
  - dtoc5 and optcdeg2 never leave the root;
  - the certificates branch, if at all, in ≤ 4 continuous dimensions;
  - 103 of the campaign's 109 finite solver duals carry no globality warning, and
    all 109 are weaker than the certificates.
- Evidence against a strict reading:
  - camshape100: SCIP improves steadily with branching (20% → 5.7% in 1.18M nodes);
  - eg_disc2_s's own certificate needed 1,114,361 leaves, though in a reduced
    space with strong enclosures;
  - termwise relaxations can force exponential branching even at treewidth 1, so
    weak relaxations and branching cost are linked (the face-exact theorem, on a
    synthetic family).
- *Resolution:*
  - Phrase the claim as: "In every closed case the decisive ingredient was a
    bounding argument adapted to the model's structure (a split, a duality or
    convexity certificate, a comparison, or tighter local enclosures). Our
    certificates branch only in low-dimensional reduced spaces. In our reading,
    the weak relaxations available to single-tree solvers — owing to free
    variables, long chains of nonconvex equalities, and hidden convexity or
    monotonicity — were the main obstacle. This is an interpretation, not tested
    experimentally."
  - Optionally add Table 5.3.
  - Optional experiment to make it evidence: rerun one solver (SCIP 10.0.3, 1
    thread, 1 h) on dtoc5, optcdeg2, lukvle10, chain50, catmix100 and hvycrash with
    the variable enclosures proved in the certificates added as bounds, and on
    camshape100 reformulated in `u = 1/r`. If gaps shrink sharply, the "free
    variables / formulation" part is supported.

**PT-3 (major, wording): the pattern sentence overstates.**
- The summary says "Most certificates (lnts, dtoc5, lukvle10, optcdeg2, chain,
  catmix, and the waterno2 improvements) combine a decomposition along the model's
  chain or period structure, an affine or state-dependent split ..., and exact
  treatment of a few low-dimensional windows." SYNTHESIS says "about half (15) use
  affine or state-dependent splits along chains plus short exact windows."
- Facts:
  - 15 of 31 is about half, not most.
  - Windows occur only in lukvle10 and chain.
  - lnts's global `h` is handled by monotonicity (and the lnts report calls the
    separator structure irrelevant).
  - dtoc5, catmix and the final optcdeg2 certificate use no window.
  - waterno2's bags are 166-variable periods, not low-dimensional windows.
  - The split classes are affine (dtoc5, lnts, lukvle10), quadratic (optcdeg2),
    field-type in a lifted state (chain), concave piecewise linear (catmix) and
    cellwise affine (waterno2).
- *Resolution.* Use the class table of Section 1.1 and this wording: "15 of the 31
  closures share one pattern: a split (Lagrangian or discrete calibration) along
  the model's stage structure whose stage problems are small enough to be
  minimized rigorously; where the split cannot be exact, a few stages are merged
  into an exact window (lukvle10, chain; 2-D each). The waterno2 improvements use
  the same pattern with cellwise slopes."

**PT-4 (minor, documents): outdated passages that must not be quoted.**
- `R/SYNTHESIS.md`:
  - lines 42–44 and 485–489, and `R/closing-research-results.md` (§4 first bullet
    and Limits), say the 13 former tolerance-only closures have no exactly feasible
    point. Superseded: `R/publication/primal/`, summary.
  - "eg_disc2_s partly by sampling" (line 41) and the closing record's "110,676 of
    979,044" sample. Superseded by the all-leaf recheck under A1/A2.
  - waterno2_06 "1.67%" / "1.7%" (unsafe rounding; use ≤ 1.68%).
  - "Waves 2 and 3 tested this [capability]" (line 701). The certificates were
    built by hand per instance; no solver component was implemented or tested.
- `R/theory-calibration/scouting.md` §2.4: the optcdeg2 row ("affine on state
  enclosures; head block") and "Quadratic (Riccati) calibrations were not needed by
  any closed instance" are false after the bang-bang closure.

*Resolution:* cite only the summary and READINESS for numbers and statuses. No
computation is needed.

**PT-5 (minor, rigor): the theory is stated for idealized bags; the certificates
use constrained stages and enclosures.**
- The consistency note assumes box bags with bounded (or continuous) data and exact
  bag minima.
- *Resolution:* use the versions in Section 3. They allow arbitrary bag sets,
  extended-valued value functions and enclosures, and need only `f*` finite and
  costs bounded below. Their proofs are given above.
- State explicitly that certificate validity rests only on Lemma 1, Propositions 3
  and 4 and the instance computations.
- Cost of an independent confirmation of Section 3 (proof reading plus small
  numeric tests): about one reviewer-hour.

**PT-6 (minor, provenance): the scout and census are unreviewed root computations
with heuristic widths.**
- *Resolution:* say so. Report that the counts were reproduced from saved data and
  from the audit's independent page parse. Say that the selection is post hoc for
  the first wave and tractability-ranked for later waves. No computation is needed.

**PT-7 (minor, scope): single-tree lower bounds.**
- The SYNTHESIS links Theorem 1 of the face-exact note to the open instances only
  interpretively.
- *Resolution:* do not include it as a theorem. If mentioned, say: "On a synthetic
  path family with a unique nondegenerate minimizer, termwise McCormick relaxations
  force at least `0.57(5/3)^n` leaves for every single-tree certificate [companion
  report]. No such bound is known for the instances studied here." If the paper
  cites it, get one confirmation of the face-exact post-recheck fixes (§13 item 5).
  Cost: a short review.

**PT-8 (minor, wording): Proposition 8 and camshape.**
- The cell-constant DP that failed on camshape100 is not exactly the idealized
  split relaxation.
- *Resolution:* write "consistent with" (as the first-wave report does), not
  "explained by".

**PT-9 (minor, evidence quality): solver-log facts include overloaded and
memory-stopped runs.**
- *Resolution:* label those rows. The optional rerun of dtoc5/optcdeg2 under
  controlled load is READINESS's open decision 2.

**PT-10 (minor, definition): MINLPLib's solved criterion is not quoted in the
record.** The summary mentions "MINLPLib's 1e-6 rule". The 4stufen example shows
that S marks are not a function of the best single-solver gap.
- *Resolution:* quote the definition from minlplib.org's documentation (one page
  lookup) and cite it.

**PT-11 (minor, wording): the summary's parenthesis "(affine splits plus full
consistency on short windows; reviewed, rechecked and confirmed)"** can be read as
saying that the link to the instances was verified. Only the theorems were.
- *Resolution:* move "reviewed, rechecked and confirmed" next to the theorem
  citations.

### 8.2 Would anything invalidate a claimed result?

No. The pattern-level claims are interpretive or definitional. The theory used to
explain them was re-derived without error. The counts reproduce exactly. The
certified numbers in Section 5.2 match the summary and gap-values.json under exact
recomputation.

---

## 9. What the paper may claim and must not claim

**May claim** (suggested wording):

- "We certify 31 MINLPLib instances that carry no solved mark in the MINLPLib
  listing (fetched 2026-09-29; unchanged at a refresh on 2026-10-02). The bounds
  are valid for every exactly feasible point of the stored OSIL models, under the
  stated assumptions (A1/A2 for the three eg_* instances)."
- "Fifteen of the 31 closures share one certificate pattern: a split bound
  (Lagrangian or discrete calibration) along the model's stage structure, with
  stage problems small enough to be minimized rigorously, and, where the split is
  not exact, a small exact window (Lemma 1, Propositions 2–3). Three further
  closures are Lagrangian splits over at most five dense rows."
- "A split restricted to a class of functions on one separator loses exactly twice
  the sup-norm distance from that class to the band between the cost-to-come and
  the cost-to-go (Theorem 5). On a path, the loss lies between twice the largest
  such distance and twice the sum of distances to one jointly exact split
  (Theorem 6). To the best of our knowledge, the identity and the lower bound have
  not been stated before. Their one-sided forms are classical (de Farias–Van Roy;
  Grimm–Netzer–Schweighofer)."
- "Constant (zero-slope) cell bounds need at least `|λ|/√(2Mε)` cells per separator
  with nonzero multiplier `λ` (Proposition 8). This is consistent with the failure of
  a generic cell-constant dynamic program on camshape100. Every working staged
  certificate used slopes."
- "Applying one selection rule to MINLPLib gives 294 instances, none marked solved:
  nonconvex, heuristic factor-incidence width ≤ 16 or nonlinear-primal width ≤ 6
  with ≥ 50 nonlinear variables, and metadata gap > 1e-4. Of these, 155 have a best
  listed single-solver gap above 1e-4. Our certificates close 29 of the 155 and two
  more instances whose listed single-solver gaps were already 1.2e-6 and 3.8e-5. The
  instances were chosen by expected tractability, so this proportion does not
  measure the difficulty of the open population."
- "In our reading of every closed case (an interpretation, not tested
  experimentally), the decisive ingredient was a bounding argument adapted to the
  model's structure rather than more branching in the original space. Our
  certificates branch, if at all, in spaces of at most four continuous dimensions.
  Single-tree solvers were held back by weak relaxations: free variables, long
  chains of nonconvex equalities, hidden convexity or monotonicity."
  Optionally cite Table 5.3, with its caveats.

**Must not claim:**

- that a general solver capability (decomposition-aware B&B, window detection) was
  implemented or tested; the certificates are instance-specific constructions;
- that single-tree B&B provably needs exponential effort on these instances, or
  that small treewidth caused their open status (lnts's separator structure is
  irrelevant to its certificate; chain's nonlinear-primal width is N+1);
- that the band theorems prove or predict the closures; they explain when split
  certificates can be exact;
- "most" certificates share the pattern, or that all pattern certificates use
  windows;
- that the 146 or 155 are MINLPLib's own set of open instances, or that 29/155
  is a solve rate;
- novelty of the mechanisms (Lagrangian duality, calibrations, Mangasarian/Arrow,
  Sturm comparison, SDP duality) or blanket "previously unsolved" statements
  (READINESS: "No unconditional priority claim or blanket 'previously unsolved
  globally' claim is supported");
- any statement from the outdated passages listed under PT-4.

---

## 10. Candidate figures and tables

1. **Table (main text): mechanism taxonomy of the 31 closures**
   (Section 1.1). Columns: class, mechanism, instances, count, branching dimension,
   arithmetic (exact rational / mpmath iv / outward-rounded binary64 / A1–A2).
2. **Table: the 15 staged certificates** (Section 3.10 merged with the structure
   table of Section 1.2): stages N, separator dimension, split class, window,
   stage-check method.
3. **Figure: coverage funnel** 1633 → 1257 → 596 → 360 → 294 → 155 → {29 closed,
   6 KAN (R only), 6 improved}, with camshape100/lnts50 marked separately.
4. **Figure: the band picture** (schematic, 1-D separator): `V_τ` above,
   `f* − Γ_τ` below, pinched at `s*`. Show an affine band element tangent at `s*`,
   a case where no affine function fits (as in optcdeg2's concave arcs), and a
   window replacing the separator.
5. **Table: solver behaviour in 1 h** (Section 5.3), with overload and memory caveats.
6. **Figure (optional): listed best dual vs certified dual**, as relative gap before
   and after, on a log scale, for all 43 instances. Data in the summary and
   gap-values.json.

---

## Appendix. Commands run for this dossier

All were run from a shell. Scientific modules were neither imported nor executed;
data files were copied to `/tmp` or a `tempfile` directory first.

```
python3 checks/pattern-theory/coverage_checks.py > checks/pattern-theory/logs/coverage_checks.log
OMP_NUM_THREADS=1 python3 checks/pattern-theory/band_checks.py > checks/pattern-theory/logs/band_checks.log
sh checks/pattern-theory/scip_log_facts.sh > checks/pattern-theory/logs/scip_log_facts.log
```

Plus read-only `grep`/`sed` inspection of `R/` documents, reviews and solver logs.
No solver run, no certificate run, no project-wide check, no CI inspection.
