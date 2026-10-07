# Dossier: why these instances stayed open, the common certificate pattern, and coverage

Family key: `pattern-theory`. Revision r2, written 2026-10-04 for the MPC paper in
`paper-open-minlplib/`. `R/` means `research-20260929/`. This revision replaces
the earlier version of this file (written 02:01 the same day, kept verbatim as
`checks/pattern-theory/previous-dossier-0201.md`). It re-derives every proof,
re-runs every count with new code, keeps what survived, and corrects six points
(Section 0, item 7). Nothing under `R/` or `literature/` was edited. No solver,
certificate or research script was run or imported. All checks read copies of
saved data in a temporary directory. Scripts and logs:
`checks/pattern-theory/r2_checks.py`, `r2_band_checks.py`, `logs/r2_*.log`
(earlier: `coverage_checks.py`, `band_checks.py`, `scip_log_facts.sh`).

## 0. Main findings

1. **Nothing here invalidates a claimed result.** No certificate depends on
   the theory in this family. Validity of the staged certificates rests on two
   elementary lemmas (Lemma 1: telescoping split bounds; Lemma 1′:
   value-function minorants by induction) and on Propositions 3 and 4 (windows,
   cellwise slopes), plus the instance computations documented in the family
   dossiers. The band results (Theorems 5 and 6, Propositions 7 and 8) explain
   when such certificates can be exact; they prove nothing about an instance.
2. **The common pattern covers 15 of the 31 closures, not "most".** These are
   lnts50–400, dtoc5, lukvle10, optcdeg2, chain50–400 and catmix100–800. Each
   is a split (Lagrangian, discrete calibration or value-function minorant)
   along the stage structure whose stage problems are small enough to be
   minimized rigorously. Exact low-dimensional windows occur in only two
   families: lukvle10 (3-pair tail, 2-D entry state) and chain (the 2-D end
   values). lnts handles its global step `h` by monotonicity, and dtoc5,
   catmix and the final optcdeg2 certificate use no window. camshape (4 more
   closures) also works along the chain, but by a comparison argument, not a
   split. The waterno2 improvements use the pattern with 166-variable period
   bags, which are not low-dimensional. The summary's sentence "Most
   certificates … combine … exact treatment of a few low-dimensional windows"
   must be rewritten (PT-3).
3. **"Open" has two meanings; the paper must define both.**
   - (a) **No solved mark.** MINLPLib marks an instance solved (S) when "at
     least 3 solvers claim global optimality (up to a relative optimal
     tolerance (gap) of 10⁻⁶)" for the best known solution, or at least 3
     solvers claim infeasibility. This definition is in the MINLPLib
     documentation, `literature/papers/vigerske2026-minlplib-documentation-database-snapshot-2026`.
     All 43 paper instances lack the S mark.
   - (b) **The scout's 1e-4 rule.** The best listed single-solver relative gap
     exceeds 1e-4. This rule gives "146 open among 283 candidates".
     camshape100 (1.2157e-6) and lnts50 (3.8249e-5) are open under (a) but not
     under (b).
   - The scout's candidate rule applied to all 1632 census instances gives 294
     candidates (283 plus the 11 first-wave instances) and 155 open ones. The
     certificates close 29 of the 155. All counts reproduce exactly from two
     independent page parses.
4. **"Relaxation, not branching" is an interpretation, and the dichotomy is not
   sharp.** The saved one-hour campaign supports it for the 15 staged
   closures. For 14 of them, no unqualified one-hour solver dual beats the
   listed dual. The exception is lnts200, where it closes 2.8% of the listed
   gap. For chain the solver duals are −36 to −1673 against a certified 5.07,
   and for catmix no solver gives a finite dual with a globality guarantee.
   Counter-evidence:
   - camshape: SCIP's dual improves steadily with branching, from −5.163 to
     −4.529 over 1,179,749 nodes on camshape100, yet stops 5.7% short;
   - eg_disc2_s: our own certificate needed 1,114,361 leaves;
   - ex6_2_5: one 2-D sub-B&B needed 5.9M boxes.

   The defensible statement: the decisive step was a bounding argument adapted
   to the model's structure, after which any branching was low-dimensional
   or small. The weakness of termwise relaxations is our reading of why solvers
   failed (PT-2).
5. **Which theory belongs in this paper.** Include a short "split certificates"
   section with Lemma 1, Lemma 1′, Propositions 2–4, Theorem 5 (band identity)
   and Proposition 8 (constant cells). Theorem 6 (path sandwich) and
   Proposition 7 (counterexample) can go in an appendix. All are proved below
   in the extended-value, constrained form the certificates need; each proof is
   a few lines.
   - Cite as companion results, with no theorem in this paper: the single-tree
     lower bound for termwise McCormick (face-exact note, Theorem 1) and the
     separation of calibration note Corollary 3.8.
   - Exclude: the decomposition-certificate complexity theory, which overlaps
     `paper-decomposition-aware/`; split-robust bounds, RLCT, coupling, the hp
     and polynomial rates, and the bang-bang asymptotics, which no certificate
     uses.
6. **Older documents are outdated in places** (PT-5). Use the summary and
   READINESS for every number and status.
7. **Corrections to the earlier version of this dossier.**
   - (i) catmix's validity is Lemma 1′, not Lemma 1 (PT-4).
   - (ii) MINLPLib's S definition is now quoted; the earlier version had left
     it as an open lookup (PT-1).
   - (iii) `fct` is missing from the census. Over the whole library the rule
     gives 295 candidates; the open count stays 155 (PT-7).
   - (iv) chain's census nonlinear-primal width N+1 is a parsing artifact; the
     true value is 1. The earlier argument "chain's nonlinear-primal width is
     N+1 because of the dense length row" is withdrawn (PT-7).
   - (v) "Our certificates branch, if at all, in at most four continuous
     dimensions" is false for pindyck: its concavity proof uses 9 boxes in a
     112-dimensional parameter box (PT-11).
   - (vi) The claim that no affine band element exists on optcdeg2's arcs is
     not proved; it is replaced by a conditional statement (PT-13).

---

## 1. Instances and models

### 1.1 Population and mechanism classes

The paper has 43 instances:
- 31 closures;
- six KAN models, for which only the relaxation R is certified because the
  OSIL models are exactly infeasible;
- five waterno2 models;
- ann_cumene_tanh.

Mechanism labels come from the summary and the family reports.

| class | mechanism | instances | count |
|---|---|---|---|
| A. staged split | a split (Lagrangian, discrete calibration or value-function minorant) along the stage structure; every stage problem is minimized rigorously; exact windows only where the split cannot be exact | lnts50/100/200/400, dtoc5, lukvle10, optcdeg2, chain50/100/200/400, catmix100/200/400/800 | 15 |
| A′. chain comparison | discrete Sturm comparison in `u = 1/r` plus a min-plus DP along the chain; the calibration note reads it as affine calibrations of auxiliary LPs (§2.4 item 7) | camshape100/200/400/800 | 4 |
| B. Lagrangian over a few dense rows | dualize ≤ 5 coupling rows; the blocks separate and are minimized rigorously | ex6_2_5, ex6_2_7 (3 mass balances; tangent-plane test by 2-D interval B&B), pricing050 (5 rows; 50 univariate blocks) | 3 |
| C. global duality or convexity | SDP/Lagrangian dual with exact LDLᵀ PSD proof (powerflow; 0039 adds a leaf-bus identity and B&B on 3 leaf coordinates); convex relaxation plus KKT tangent plane (etamac); reduced objective concave on a polytope plus tangent plane (pindyck) | powerflow0030p/0039p/0039r, etamac, pindyck | 5 |
| D. identity | objective constant on the feasible set | hvycrash | 1 |
| E. reduced-space B&B with strong local enclosures | second-order Taylor models that keep signed cancellation, per-box LP over the 24 minimax rows, under A1/A2 | eg_int_s, eg_disc_s, eg_disc2_s | 3 |

Total 31. Classes A and A′ (19 instances) exploit a chain structure. Classes A
and B (18) are split bounds in the sense of Lemma 1 or Lemma 1′. Among the
unclosed instances, the waterno2 improvements are class A with large bags
(Proposition 4). KAN (on R) and ann_cumene_tanh were bounded by reduced-space
branch and bound.

### 1.2 The model class behind class A

Every class-A instance, and waterno2, is a path of bags. Bag `t = 1, …, N`
holds a vector `z_t ∈ R^{d_t}`. Neighbouring bags share a separator vector,
which is a selection of coordinates:
`s_t = π^R_t z_t = π^L_{t+1} z_{t+1}` (t < N). Each bag has a set
`K_t ⊆ R^{d_t}` (bounds and every row involving only bag t) and a cost
`F_t : K_t → R` bounded below:

```
(P)   f* = inf { Σ_{t=1}^N F_t(z_t) :  z_t ∈ K_t,  π^R_t z_t = π^L_{t+1} z_{t+1}  (t < N) },   Z = feasible set.
```

For a transcribed control problem, bag t is the stage `(x_t, u_t, x_{t+1})`. Its
separator is the state, or the pair (state, nodal control) for trapezoidal
schemes. Three features recur.

- **Global variables** lie in every separator. lnts's step `h` is one. The lnts
  certificate never branches on `h`: one Lagrangian argument proves
  infeasibility for every `h ≤ h2` at once, by monotonicity in `h`. The lnts
  report says that "the treewidth/separator structure is irrelevant here; what
  matters is that the dynamics are linear in the state for fixed h"
  (`R/open-instances/open-instances-report.md` §3.4).
- **Dense rows are lifted into the state.** chain's length row couples all
  slopes. Its certificate sums by parts and carries the cumulative weight
  `v_k = V + Σ_{j<k} λ_j` as a second state (`R/open-instances-wave2/cops/report.md` §2).
- **States can be eliminated.** In dtoc5, `u_t` is eliminated; in catmix,
  homogeneity reduces the 2-D state to a 1-D ray; in lukvle10, the recurrence
  fixes a window from its entry pair.

**Per-instance structure.** Sizes and free-variable counts come from the OSIL
files (`logs/r2_checks.log` §D). "Free" means both bounds infinite. Widths are
the census heuristic upper bounds (factor-incidence / nonlinear-primal). The
other columns come from the family reports.

| instance(s) | vars (free) | width fac/nl | stages; separator | split class | window | stage problems |
|---|---|---|---|---|---|---|
| lnts50–400 | 256–2006 (197–1597) | 12–11 / 2 | N = 50–400; (py, vx, vy, θ, h), dim 5 incl. global h | Lagrangian of the aggregated linear dynamics, multipliers (μ, ν), for each fixed h; equivalently an affine calibration with the states eliminated | none; global h by monotonicity | closed form `max_θ (w cos θ + b sin θ) = √(w²+b²)`, mpmath iv |
| dtoc5 | 99,999 (99,998) | 2 / 0 | T = 49,999; y_t (dim 1) | affine (costates λ_t = −2u_t) | none | closed form: each term is a strictly convex quadratic because λ_t < 1/4 |
| lukvle10 | 1000 (1000) | 4 / 1 | 998 recurrence rows; (x_j, x_{j+1}), dim 2 | affine (pair Lagrangian) | rows 994–997 kept (3 pairs), 2-D entry state | 34 distinct 2-D pair problems plus the tail, interval B&B |
| optcdeg2 | 150,002 (50,000 free y; 49,999 with v ≥ −1) | 4 / 0 | N = 50,000; (y, v), dim 2; u ∈ [−0.2, 0.2] | quadratic: `S_t = py_t·y + pv_t·v + (q_t/2)(v − v̄_t)²`, q_t = 0 at both switches | none (the superseded certificate used a 3080-stage head block) | exact minimization in y and u, 1-D cells in v; 1.33e6 cells in total |
| chain50–400 | 102–802 (100–800) | 4 / 1 (census: N+1, artifact) | N = 50–400; lifted state (z_k, v_k) | field type: `S_k(z, v) = G(v) − v z + k c` (discrete catenary calibration) | 2-D end values (z_1, z_N), per-box field parameters (V, H′) | closed-form lemma, checked in exact rationals |
| catmix100–800 | 303–2403 (200–1600) | 4 / 1 | N = 100–800; (x1, x2) → 1-D ray θ by homogeneity | concave, positively homogeneous value functions bounded below by chords on rays (about 14,080 rays per stage in the author run) | none | per-ray 1-D interval B&B over u |
| waterno2_06–24 (not closed) | 996–3984 (348 free in _06) | 9 / 2 | T = 6–24 periods of 166 variables and 9 binaries; 3 tank levels, plus one horizon row | Lagrangian on 3(T−1) level copies plus the horizon row; for _06, cellwise slopes and a shortest path (Proposition 4) | each period is a 166-variable bag | per-period and per-cell-pair rigorous B&B |

Two width facts matter for the paper.

1. lnts's factor-incidence width (11–12) comes from the hub variable `h`, which
   the certificate handles by monotonicity.
2. chain's census nonlinear-primal width bound N+1 is an artifact. The
   OSIL objective and length row are written as `product(sum(…), constant)`,
   and the census reader splits only top-level sums. With the constant
   distributed, the nonlinear-primal graph of chain50 has 51 edges and maximum
   degree 1, so its width is 1 (`logs/r2_checks.log` §E).

The census report itself does not quote chain's nonlinear-primal width, so
only the raw census data and the earlier dossier are affected. Even so,
nonlinear-primal width bounds can be loose for models written as constant ×
sum (PT-7).

### 1.3 Model-provenance issues that cut across families

- Every certificate concerns the stored MINLPLib **OSIL** model, with decimal
  constants read as exact rationals. Source-model differences belong to the
  family dossiers:
  - CUTEst scaling for dtoc5 and optcdeg2;
  - COPS 2.0 versus 3.0 for catmix;
  - rounded QPLIB copies;
  - MATPOWER data dropped in powerflow.
- The scout's OSIL reader ignored the objective constant. Nonzero constants
  occur in 36 of the 283 candidates, including catmix (−1), powerflow0039p/r,
  methanol, pinene and popdynm. The certificate scripts read the constant
  (`R/open-instances-scout/targets.md` §1 item 4). Any table that recomputes
  objectives must add it.
- For catmix100–800 (and methanol50 and lop97icx), OSIL and .gms coefficients
  differ by double rounding (`R/publication/minlplib-status/report.md`). The
  claims are for OSIL.
- The six KAN OSIL models have no exactly feasible point. They count as open
  under both definitions, but have no optimum.

---

## 2. Listed status and coverage

### 2.1 What MINLPLib lists

From the MINLPLib documentation (database snapshot 2026-09-14,
`literature/papers/vigerske2026-minlplib-documentation-database-snapshot-2026/fulltext.md`,
lines 105–119):

- **Points.** Points with constraint violation below the feasibility tolerance
  determine the primal bound. The tolerance value is not stated there. The
  scout used ≤ 1e-8.
- **Dual bounds.** These are "dual bounds on the optimal value as reported by
  some solvers. The 1st, 2nd, and 3rd best bound are in bold." The FAQ adds
  that they are "just the best value as computed in some run with some option
  settings on some machine at some time in the past".
- **S (solved).** "Whether for the best known feasible solution, at least 3
  solvers claim global optimality (up to a relative optimal tolerance (gap) of
  10⁻⁶), or at least 3 solvers claim infeasibility of the instance."
- **Listing dual.** The dual shown in the instance listing, which the summary
  calls the "three-solver metadata value", is the third-best per-solver bound.
  - In 1565 of 1568 instances with at least three finite bounds, it agrees
    with the third-best bound up to the listing's display rounding.
  - The three exceptions (ball_mk4_15, chp_shorttermplan2c, powerflow0057r)
    agree once a solver's `inf` entry is counted (`logs/r2_checks.log` §B).
- **Example.** 4stufen has two solvers (ANTIGONE, XPRESS) at the primal value
  and no S mark; its listing dual is COUENNE's.
- **The S mark records claims, not displayed bounds.** A naive test "at least
  three displayed duals within relative gap 1e-6 of the best displayed point
  with infeasibility ≤ 1e-6" agrees with the S mark in 1612 of 1633 instances
  (`logs/r2_checks.log` §H). The mark records solvers' optimality claims,
  while the displayed bounds are rounded.
- **No paper instance is near the S criterion.** For all 43, no listed dual
  lies within relative 1e-6 of the best listed point with infeasibility
  ≤ 1e-8. With a 1e-6 point tolerance there is one: optcdeg2's GUROBI bound,
  which equals the objective of point p2 (listed infeasibility 1e-6).

### 2.2 Two meanings of "open"

- **(a) Listed as open = no S mark.** All 31 closures, the six KAN, the five
  waterno2 and ann_cumene_tanh lack the S mark (`R/bound-audit/pages.json`,
  fetched 2026-09-30). The status refresh found the marks unchanged on
  2026-10-02.
- **(b) Open under the 1e-4 rule.** Take the best listed single-solver dual
  bound and the best listed point with infeasibility ≤ 1e-8, and compute
  `|p − d|/min(|p|,|d|)` (∞ if the signs differ or one value is 0). The
  instance is open if this exceeds 1e-4, or if there is no listed point or no
  finite listed dual.
- **The scout's candidate set** (`R/open-instances-scout/targets.md` §1)
  contains instances that:
  - are nonconvex;
  - have heuristic factor-incidence width ≤ 16, or nonlinear-primal width ≤ 6
    with ≥ 50 nonlinear variables;
  - have a metadata (listing) gap > 1e-4 or infinite;
  - are not among the 11 first-wave instances.

### 2.3 Coverage funnel

Recomputed twice: by the earlier code and by new code from both page parses
(`logs/coverage_checks.log`, `logs/r2_checks.log` §A–C).

| step | count | source |
|---|---|---|
| MINLPLib instance pages | 1633 | `R/bound-audit/pages.json` |
| nonconvex (MINLPLib flag) | 1257 | same |
| … without S mark | 596 | same |
| … meeting the width rule | 360 | `R/treewidth-census/census_merged.json` (1632 instances; `fct` missing, see below) |
| … with metadata gap > 1e-4 or ∞ | **294** = 283 scout candidates + the 11 first-wave instances (set equality checked) | same |
| … with best single-solver gap > 1e-4 (rule (b)) | **155** = 146 scout + 9 first-wave | `R/open-instances-scout/fetched.json`; independent recount from `pages.json`, zero mismatches |
| closed by this work, among the 155 | **29** (20 from wave 2 on + 9 first-wave) | summary |
| closed, but with best single-solver gap ≤ 1e-4 before | 2: camshape100 (1.2157e-6 against the exact optimum; 1.2161e-6 against the listed primal), lnts50 (3.8249e-5; 3.8241e-5) | summary; recount |
| other paper instances among the 155 | 12: 6 KAN (R certified, OSIL infeasible), 5 waterno2 and ann_cumene_tanh (improved) | summary |

- The S filter removes nothing at the last steps: no instance in the 294 has an
  S mark.
- `fct` has no OSIL in the census cache. It is nonconvex, unsolved, has 11
  variables and an empty listing dual, so the rule would admit it, giving 295
  candidates. Its best single-solver gap is 0 (LINDO dual 0 = primal 0), so
  the open count stays 155.

**The 146 scout instances by band** (identical from both parsers):
- 25 have no listed feasible point;
- 3 have no finite listed dual (quantum, cesam2cent, ann_cumene_tanh);
- 15 have an infinite relative gap;
- 33 have a relative gap ≥ 1;
- 30 have a relative gap in [0.1, 1);
- 19 have a relative gap in [0.01, 0.1);
- 21 have a relative gap in (1e-4, 0.01).

Four have absolute gaps below 1e-5 (bayes2_20, bayes2_30, wastepaper5,
ex8_5_1).

**Selection caveats the paper must state.**
- The first wave was not selected by this rule. It was picked from the partial
  census: constant-width families whose gaps grow with size (camshape, lnts),
  and very long chains with trivial listed bounds (dtoc5, optcdeg2, lukvle10)
  (`R/root-research-log.md`, 2026-09-29). The funnel is a post hoc
  reconstruction.
- The later targets were ranked by judged tractability × payoff (scout §1,
  §6). So 29/155 describes what a targeted effort achieved. It is not a solve
  rate and does not measure the difficulty of the open population.
- The widths are min-degree elimination upper bounds. Neither the census nor the
  scout was independently reviewed. Their counts and shares reproduce from the
  saved data; the closing audit checked 13.6% and 62.7%.

### 2.4 Census context (optional for the paper)

Among the 582 nonconvex census instances with ≥ 100 nonlinear variables
(recounted):

| width bound | factor-incidence | nonlinear-primal |
|---|---|---|
| ≤ 4 | 27 (4.6%) | 278 (47.8%) |
| ≤ 12 | 79 (13.6%) | 365 (62.7%) |

The coupling note found that dualizing up to 8 linear rows raises the
factor-incidence share only to about 17%, from its own 14.8% baseline, which
the coupling recheck reproduced. Small width among the nonlinear terms is
common; small width with all rows counted is not.

---

## 3. The certificate pattern: statements and proofs

### 3.0 The idea in plain words

A single-tree solver bounds the whole model at once and relaxes each nonconvex
term separately. The staged certificates instead cut the model along its
stages. Each separator gets a function of the shared variables. It is added in
one stage and subtracted in the next, so the total objective is unchanged
(a "split"). Each stage, with its two split functions, is a small problem whose
minimum can be computed rigorously, and the sum of these minima is a valid
lower bound.

Affine split functions are Lagrange multipliers. Nonlinear ones are discrete
calibrations (Krotov functions, approximate value functions). In practice the
split comes from a good local solution.

The bound is exact iff one feasible point minimizes every stage problem. With a
split of a given class, the loss at one separator is exactly twice the distance
from the class to the "band". The band is the set of functions lying between
`f* − (cost-to-come)` and the cost-to-go; it is pinched at the optimal
separator values. Where no function of the class fits in the band, a few stages
are merged into one exact window and handled by a small rigorous computation.

### 3.1 Notation

Use (P) of Section 1.2. Assume `Z ≠ ∅` and each `F_t` bounded below on `K_t`,
so `f*` is finite. A **split** is `φ = (φ_1, …, φ_{N−1})` with real-valued
`φ_t : R^{k_t} → R`; put `φ_0 = φ_N = 0`. Define

```
F_t^φ(z_t) = F_t(z_t) + φ_t(π^R_t z_t) − φ_{t−1}(π^L_t z_t),        B(φ; K′) = Σ_{t=1}^N inf_{z ∈ K′_t} F_t^φ(z),
```

with `B(φ) = B(φ; K)`. A **class** `Φ_t` is a linear space of real functions on
`R^{k_t}` that contains the constants. The gap of a product class is
`gap(Φ) = f* − sup_{φ ∈ ΠΦ_t} B(φ)`.

**Value functions at a separator τ ∈ {1, …, N−1}** (with `inf ∅ = +∞`):

```
Γ_τ(s) = inf { Σ_{t≤τ} F_t(z_t) : z_t ∈ K_t (t ≤ τ), consecutive copies agree, π^R_τ z_τ = s }      (cost-to-come)
V_τ(s) = inf { Σ_{t>τ} F_t(z_t) : z_t ∈ K_t (t > τ), consecutive copies agree, π^L_{τ+1} z_{τ+1} = s }   (cost-to-go)
```

Then `Γ_τ, V_τ > −∞` everywhere and `f* = inf_s [Γ_τ(s) + V_τ(s)]`. Put
`L_τ = f* − Γ_τ` (values in `[−∞, ∞)`) and `U_τ = V_τ` (values in `(−∞, ∞]`).
Then `L_τ ≤ U_τ` everywhere, with equality exactly at the optimal separator
values (the **pinch set**).

The **band** is `Band_τ = {ψ : R^{k_τ} → R : L_τ ≤ ψ ≤ U_τ}`. It is nonempty,
since it contains `min(max(0, L_τ), U_τ)`. Distances use the sup norm over all
of `R^{k_τ}`:
- `dist(Φ, 𝓑) = inf{ sup_s |φ(s) − ψ(s)| : φ ∈ Φ, ψ ∈ 𝓑 }`, possibly `+∞`;
- `osc(g) = sup g − inf g`.

### 3.2 Lemma 1 (validity of split bounds)

**Lemma 1.**
- (a) For every split `φ` and every family `K′_t ⊇ proj_t(Z)`,
  `B(φ; K′) ≤ f*`.
- (b) *Infeasibility form.* If `F_t ≡ 0` and `B(φ; K′) > 0` for some split and
  enclosures as in (a), then `Z = ∅`.
- (c) *Case split.* If `Z ⊆ Z_1 ∪ … ∪ Z_m` and `β_c ≤ inf_{Z_c} Σ_t F_t` for
  each `c`, then `min_c β_c ≤ f*`. In particular, `β_c` may be a split bound
  for the problem restricted to `Z_c`, with a split that depends on `c`.
- (d) *Row form.* Let `h_k(z) = 0` (k = 1..K) hold at every point of `Z` (for
  example sums or other linear combinations of model rows), let `μ_k ∈ R`, and
  let `Y ⊇ Z`. Then `inf_Y [Σ_t F_t + Σ_k μ_k h_k] ≤ f*`. In particular, if
  every `F_t ≡ 0` and this infimum is positive, then `Z = ∅` (infeasibility
  version). Splits are the case in which the `h_k` are the copy rows
  (Proposition 2(a)). Class B and lnts use this form; when the Lagrangian
  separates over blocks of variables, the infimum is a sum of block minima.

*Proof.* For `z ∈ Z`, each `φ_t(s_t)` occurs once with `+` (bag t) and once
with `−` (bag t+1) at the same point `s_t`, so
`Σ_t F_t^φ(z_t) = Σ_t F_t(z_t)`. Since `z_t ∈ proj_t(Z) ⊆ K′_t`, each term is at
least `inf_{K′_t} F_t^φ`. Take the infimum over `z ∈ Z`; this gives (a). In
(b), a point `z ∈ Z` would give `0 = Σ F_t(z_t) ≥ B > 0`. (c) is immediate. In
(d), the added terms vanish on `Z ⊆ Y`. □

*Status.* Classical in substance: Krotov's discrete sufficient condition
(`krotov1967-sufficient-conditions-for-the-optimality`), the Bellman inequality
of approximate dynamic programming, and cost shifting in graphical models. It is
calibration note Lemma 2.1 (reviewed, rechecked, confirmed). The theory needs
no computation. For an instance, what must be trusted is the rigorous
evaluation of each `inf_{K′_t} F_t^φ` and the validity of the enclosures
`K′_t`; see the family dossiers.

*Use.*
- dtoc5, lukvle10 (with Proposition 3) and optcdeg2 (with interval state
  enclosures `K′_t`): (a).
- lnts: the infeasibility version of (d) for each `h ∈ (0, h2]`, with one
  multiplier pair `(μ, ν)` that works for all such `h` by monotonicity. The
  rows are the three aggregated (summed) dynamics identities, and the
  Lagrangian separates over the controls `θ_j`. For fixed h the aggregated
  rows give `A(h) = Σ_j [w_j cos θ_j + (μ w_j + ν c_j) sin θ_j] − νB(h)` at
  every feasible θ. The right side is at most `S(μ,ν) − νB(h2) < A(h2) ≤ A(h)`
  because A and B decrease in h and `ν ≥ 0`.
- chain: (c) over boxes of the end values `(z_1, z_N)`, with the field
  parameters `(V, H′)` chosen per box and (a) inside each box.

### 3.3 Lemma 1′ (value-function minorants by induction; catmix)

Consider a transcription with states `y_i ∈ Y_i`, controls `u_i ∈ U`, dynamics
`y_i = g_i(y_{i−1}, u_i)`, terminal cost `Φ` and value functions
`V_N = Φ`, `V_{i−1}(y) = inf_{u∈U} V_i(g_i(y, u))`, so that
`f* = inf_{y_0 ∈ Y_0} V_0(y_0)` (catmix has only a terminal cost).

**Lemma 1′.** If functions `W_i` satisfy `W_i ≤ V_i` on `Y_i` for all i, then
`inf_{Y_0} W_0 ≤ f*`.

**Induction step for cone-valued linear dynamics.** Let `Y_i = K = R²_+`,
`g_i(y, u) = M_i(u) y` with `M_i(u)` entrywise nonnegative, and let
`r_1, …, r_J` be rays ordered in K and spanning it. Suppose:
- each `V_{i−1}` is concave and positively homogeneous on K;
- `W_i ≤ V_i` on K;
- `w_j ≤ inf_{u∈U} W_i(M_i(u) r_j)` for every j;
- `W_{i−1}` is the chord interpolant, `W_{i−1}(s r_j + t r_{j+1}) = s w_j + t w_{j+1}` for `s, t ≥ 0`.

Then `W_{i−1} ≤ V_{i−1}` on K.

*Proof.* `w_j ≤ inf_u W_i(M r_j) ≤ inf_u V_i(M r_j) = V_{i−1}(r_j)`. A concave
positively homogeneous function is superadditive, so
`V_{i−1}(s r_j + t r_{j+1}) ≥ s V_{i−1}(r_j) + t V_{i−1}(r_{j+1}) ≥ s w_j + t w_{j+1}`. □

For catmix, `V_{N−1}(y) = min_u (1,1)·P(u)^{−1} y` is a minimum of linear
functions, so it is concave and positively homogeneous. The recursion
`V_{i−1}(y) = min_u V_i(M(u) y)` preserves both properties. Clipping the ray
values at 0 is valid because `V ≥ 0` on K (COPS report §3).

*Status and remark.* The induction uses concavity of the **true** value
functions; the computed `W_i` need not be concave. This is not a split bound in
the sense of Lemma 1: there the stage residual `W_i(M(u)y) − W_{i−1}(y)` must be
bounded below for every y, which holds when `W_i` is itself concave (calibration
note Proposition 2.3) but was not checked for the computed `W_i`. The catmix
certificates rely on Lemma 1′ (calibration note §2.4 item 6; chain-catmix
dossier, which states the same). The independent COPS verification (item 2b)
verified concavity, homogeneity and the chord lower bounds, and the catmix
recheck confirmed the 400/800 certificates.

### 3.4 Proposition 2 (affine splits: Lagrangian duality, exactness, forced slopes)

Let `φ_t(s) = λ_t^T s + c_t`.

- (a) `B(φ)` does not depend on the constants `c`. It equals the Lagrangian dual
  function of the copy formulation, in which each bag has its own copy of every
  separator coordinate and the copy rows `π^R_t z_t − π^L_{t+1} z_{t+1} = 0` are
  dualized with multipliers `λ_t`.
- (b) *Exactness.* If some `z̄ ∈ Z` has `z̄_t ∈ argmin_{K_t} F_t^φ` for every t,
  then `B(φ) = f* = Σ_t F_t(z̄_t)`, and `z̄` is a global minimizer. Conversely,
  if `B(φ) = f*` and `f*` is attained at `z*`, then `z*_t ∈ argmin_{K_t} F_t^φ`
  for every t.
- (c) *Forced slopes.* Suppose `B(φ) = f*`, `f*` is attained at `z*`, each
  `F_t` is differentiable at `z*_t`, and `z*_t ∈ int K_t`. Then, for every
  coordinate c of `s_τ`,
  `λ_{τ,c} = −Σ_{t=a}^{τ} ∂F_t/∂z_{t,c}(z*_t)`,
  where bags `a, …, τ` hold the copies of coordinate c linked up to separator
  τ. So the slopes are unique: they are the copy-row multipliers at `z*`.
  - When dynamics rows are kept inside `K_t` (so `int K_t = ∅`), the same
    argument in the coordinates `(x_t, u_t)` gives the discrete costate
    recursion (calibration note Theorem 3.1(3)).
  - Interior controls at a stage pin the switching coefficient there.

*Proof.*
- (a) In `Σ_t F_t^φ` the constants telescope. The remaining terms
  `λ_t^T(π^R_t z_t − π^L_{t+1} z_{t+1})` are the dualized copy rows.
- (b) `Σ_t inf F_t^φ = B(φ) ≤ f* ≤ Σ_t F_t(z̄_t) = Σ_t F_t^φ(z̄_t)`; if each
  `z̄_t` attains its infimum, the outer terms agree. For the converse,
  `Σ_t F_t^φ(z*_t) = f* = Σ_t inf F_t^φ`, and every term is at least its
  infimum, so each one attains it.
- (c) An interior minimizer of `F_t^φ` has zero gradient. In the first bag of
  coordinate c this reads `∂F_a/∂z_c + λ_{a,c} = 0`. In a bag `a < t ≤ τ` it
  reads `∂F_t/∂z_c + λ_{t,c} − λ_{t−1,c} = 0`. Induct on t. □

*Status.* Classical in substance: discrete Mangasarian/Arrow sufficiency
(`mangasarian1966-sufficient-conditions-for-the-optimal`; Arrow, unread) and
Krotov. Wald–Globerson's tightness result is the convex case. This is
consistency note Proposition 5.1 and calibration note Theorem 3.1 (review:
"correct (small fix F4)"); the converse in (b) needs `f*` attained.

*Use.* (c) is why every class-A certificate takes its multipliers from one
local KKT solve. (b) is the per-stage exactness test:
- dtoc5: each stage term is a strictly convex quadratic because `λ_t < 1/4`
  (discrete Mangasarian);
- lnts: the per-stage maximum is in closed form (the linear-tangent law,
  Arrow);
- lukvle10: exact on all pairs except the end transient (a float grid estimate
  gives 352.152 with all rows dualized; not rechecked).

### 3.5 Proposition 3 (exact windows)

For `1 ≤ a ≤ b ≤ N` let

```
β_{[a,b]}(φ) = inf { Σ_{t=a}^b F_t(z_t) + φ_b(π^R_b z_b) − φ_{a−1}(π^L_a z_a) : z_t ∈ K_t (a ≤ t ≤ b), consecutive copies agree }.
```

Then `B(φ) ≤ B_{[a,b]}(φ) := Σ_{t∉[a,b]} inf_{K_t} F_t^φ + β_{[a,b]}(φ) ≤ f*`.
Disjoint windows combine.

*Proof.* Inside the window the split terms telescope, so the window objective
equals `Σ_{t=a}^b F_t^φ(z_t)`, whose infimum is at least the sum of the separate
infima. The upper bound is Lemma 1(a) for the path in which bags a..b are
merged into one bag. □

*Status.* Calibration note Proposition 4.4 (proved, reviewed). A window
carries the full function class on separators a, …, b−1. Its cost is one global
problem in the window's free variables. A window of `m` stages has dimension
`n + m·(control dim)` once states are eliminated, so generic branching is
exponential in `m`. The closed instances avoided this in three ways:
- lukvle10: there are no controls, so the window is 2-D (its entry pair);
- chain: the end pieces are kept exact, and a 2-D case split on their free
  values is combined with Lemma 1(c);
- the superseded optcdeg2 certificate: a 3080-stage head block handled by
  coordinatewise monotonicity, with no branching.

### 3.6 Proposition 4 (cellwise slopes and shortest paths; waterno2)

For each separator `t ∈ {1, …, N−1}`, let `𝒫_t` be a finite family of sets
(cells) whose union contains every feasible separator value `s_t`. Give each
cell `D` a slope vector `λ_{t,D}`, and put `𝒫_0 = 𝒫_N = {∗}` with zero slope.
For each bag t and pair `(D, D′) ∈ 𝒫_{t−1} × 𝒫_t`, let

```
b_t(D, D′) ≤ inf { F_t(z) + λ_{t,D′}^T π^R_t z − λ_{t−1,D}^T π^L_t z : z ∈ K_t, π^L_t z ∈ D, π^R_t z ∈ D′ }   (inf ∅ = +∞).
```

Then `f* ≥ SP := min over (D_1, …, D_{N−1}) of Σ_{t=1}^N b_t(D_{t−1}, D_t)`, a
shortest path in a layered graph.

*Proof.* Let `z ∈ Z`, and pick `D_t ∋ s_t` for each t. The term
`λ_{t,D_t}^T s_t` occurs with `+` in bag t and with `−` in bag t+1, at the same
point. So
`Σ_t F_t(z_t) = Σ_t [F_t(z_t) + λ_{t,D_t}^T s_t − λ_{t−1,D_{t−1}}^T s_{t−1}] ≥ Σ_t b_t(D_{t−1}, D_t) ≥ SP`. □

*Remarks.*
1. The only coupling condition is that a cell's slope is used by both bags at
   that separator. This is exactly the validity condition of
   `R/open-instances-wave2/waterno2/cell-slopes.md` Proposition 1; its review
   calls it "correct; the only coupling condition is one vector per cell".
2. Per-cell constants add nothing, because they telescope along every path.
   Suppose the cells partition the separator space and the `b_t` are exact
   infima. Then SP equals the supremum of `B(φ)` over cellwise-affine splits
   with these slopes, and the supremum is attained.
   *Proof.* For any constants `c_{t,D}`, the per-layer minimum of
   `b_t(D,D′) + c_{t,D′} − c_{t−1,D}` is at most its value on an SP-optimal
   path, and these values telescope to SP. Conversely, set `c_{t,D} = −d_t(D)`,
   where `d_t(D)` is the shortest distance to cell D at layer t. The Bellman
   inequality makes every reduced edge cost nonnegative, with equality on
   shortest-path edges. So the per-layer minima are 0 for `t < N` and SP at
   `t = N`. □
3. One cell per separator gives Proposition 2. Zero slopes give the
   cell-constant DP that failed on camshape100 (Proposition 8 and PT-9).

*Status.* Validity proved and reviewed for waterno2_06. The generic form and
Remark 2 are written here and have no independent review yet; both are
elementary. The closest prior analogue is Junge–Osinga (2004): shortest paths
on cell graphs give value-function lower bounds (`R/literature/decomposition-bb-prior.md` §1.6).

### 3.7 Theorem 5 (band identity for one separator)

For a separator τ and `φ : R^{k_τ} → R`, let

```
Δ_τ(φ) = f* − inf_s [Γ_τ(s) + φ(s)] − inf_s [V_τ(s) − φ(s)]   ∈ [0, +∞].
```

`Δ_τ(φ)` is the gap of the split bound in which bags 1..τ and bags τ+1..N are
each merged into one exact window and only separator τ carries a split.

**Theorem 5.** For every class Φ (a linear space of real functions on
`R^{k_τ}` that contains the constants),
`inf_{φ ∈ Φ} Δ_τ(φ) = 2 dist(Φ, Band_τ)`, with both sides possibly `+∞`.

*Proof.* Because `f*` is finite,
`Δ_τ(φ) = sup_s (L_τ − φ) + sup_s (φ − U_τ)`, where the first supremum runs over
`{L_τ > −∞}` and the second over `{U_τ < ∞}`. Both sets are nonempty because
`Z ≠ ∅`.

- (≤) Let `ψ ∈ Band_τ` and `φ ∈ Φ`. From `L_τ ≤ ψ ≤ U_τ`,
  `Δ_τ(φ) ≤ sup(ψ − φ) + sup(φ − ψ) = osc(φ − ψ)`. Because Φ contains the
  constants, `inf_{φ∈Φ} osc(φ − ψ) = 2 inf_{φ∈Φ} sup|φ − ψ|`. Now take the
  infimum over ψ.
- (≥) If `Δ_τ ≡ +∞` on Φ, there is nothing to prove. Otherwise fix `φ` with
  `Δ_τ(φ) < ∞`.
  - Put `a = sup(φ − U_τ)` and `b = sup(L_τ − φ)`. Both exceed `−∞`, and their
    sum is finite, so both are finite.
  - `a + b ≥ sup_s (L_τ − U_τ)` over the common finite domain, and that
    supremum equals `f* − inf(Γ_τ + V_τ) = 0`.
  - Let `φ̃ = φ + (b − a)/2 ∈ Φ`. Then both suprema equal `δ = (a + b)/2 ≥ 0`,
    and `Δ_τ(φ̃) = Δ_τ(φ)`.
  - Clip: `ψ = min(max(φ̃, L_τ), U_τ)`. It is real-valued because
    `L_τ < +∞` and `U_τ > −∞`, and it lies in `Band_τ` because `L_τ ≤ U_τ`.
  - Where `φ̃ > U_τ`, `ψ = U_τ` and `0 < φ̃ − ψ ≤ δ`. Where `φ̃ < L_τ`,
    `ψ = L_τ` and `0 < ψ − φ̃ ≤ δ`. Elsewhere `ψ = φ̃`.
  - So `dist(Φ, Band_τ) ≤ sup|φ̃ − ψ| ≤ δ = Δ_τ(φ)/2`. □

*Consequences.*
1. **No loss iff the class touches the band.** One separator loses nothing iff
   `dist(Φ, Band_τ) = 0`. For a finite-dimensional class with continuous band
   edges on a compact domain, the infimum is attained, so this happens iff Φ
   contains a band element. For affine Φ on a box, the condition is
   `cav(L_τ) ≤ vex(U_τ)` (consistency note Corollary 2.2(1), Proposition 5.1(4)).
2. **The loss is decided near the optimal separator values.** Every band
   element passes through the pinch points. Elsewhere the band has width
   `Γ_τ + V_τ − f* > 0`, so errors there are free up to that width, and kinks of
   value functions away from the optimum are harmless.
3. **Pinch regularity** (remark; classical). If `V_τ` is semiconcave and `Γ_τ`
   semiconvex near an interior pinch point, both are differentiable there with
   a common gradient, namely the multiplier of Proposition 2(c). The tangent
   plane then lies within `O(|s − s*|²)` of the band (consistency note Lemma
   4.2). On product domains semiconcavity is automatic (Lemma 4.1). For
   dynamics-constrained stages it is a hypothesis (calibration note §2.3).

*Status.* Consistency note Theorem 2.1. The review found it "correct, with the
exact constant 2"; a recheck and two confirmations found no error. The note
assumes a common box, bounded value functions and equal projections. The
version above assumes only `Z ≠ ∅` and costs bounded below. The calibration
review (F1) already noted that the one-separator proof carries over to extended
values; the full proof is written here.

### 3.8 Theorem 6 (path sandwich) and Proposition 7 (per-separator band membership is not enough)

**Theorem 6.** For classes `Φ_1, …, Φ_{N−1}`,

```
2 max_τ dist(Φ_τ, Band_τ)  ≤  gap(Φ)  ≤  2 inf_{ψ ∈ E} Σ_τ dist(ψ_τ, Φ_τ),
```

where `E` is the set of real-valued splits with `B(ψ) = f*`, and `inf ∅ = +∞`.

*Proof.*
- *Lower bound.* Fix τ and `φ ∈ ΠΦ_t`.
  - Apply Lemma 1(a) to the head problem (bags 1..τ, with `F_τ` replaced by
    `F_τ + φ_τ∘π^R_τ`) with the split `(φ_1, …, φ_{τ−1})`. This gives
    `Σ_{t≤τ} inf F_t^φ ≤ inf_s [Γ_τ + φ_τ]`.
  - Likewise for the tail (bags τ+1..N, with `F_{τ+1} − φ_τ∘π^L_{τ+1}`):
    `Σ_{t>τ} inf F_t^φ ≤ inf_s [V_τ − φ_τ]`.
  - Adding gives `f* − B(φ) ≥ Δ_τ(φ_τ) ≥ 2 dist(Φ_τ, Band_τ)` by Theorem 5.
    Take the supremum over φ and the maximum over τ.
- *Upper bound.* Let `ψ ∈ E`, `φ ∈ ΠΦ_t` and `r_t = φ_t − ψ_t` (`r_0 = r_N = 0`).
  - Then `F_t^φ = F_t^ψ + r_t∘π^R_t − r_{t−1}∘π^L_t ≥ inf F_t^ψ + inf r_t − sup r_{t−1}`.
  - Summing gives `B(φ) ≥ f* − Σ_τ osc(r_τ)`.
  - Minimizing `osc(φ_τ − ψ_τ)` over `φ_τ ∈ Φ_τ` gives `2 dist(ψ_τ, Φ_τ)`,
    because the constants are in `Φ_τ`. □

This lower-bound proof uses only weak duality on the head and tail. The
consistency note's proof enlarges every other class to the full class of
bounded functions, so it needs bounded value functions, which constrained
stages do not have.

**Proposition 7.** On `[0, 1]²` take three bags `a(s_1) = 10(1 − s_1)`,
`b(s_1, s_2) = s_1 + s_2 − s_1 s_2` and `c(s_2) = 10(1 − s_2)`, with constant
classes on both separators. Each band contains a constant, yet `gap = 1`.

*Proof.*
- F is multilinear, so `f* = min over vertices = F(1,1) = 1`. Constant splits
  telescope, so `B = min a + min b + min c = 0`.
- Separator 1: `Γ_1 = 10(1 − s_1)`, and `V_1 ≡ 1`, because the coefficient of
  `s_2` in `b + c` is `−9 − s_1 < 0`. The constant 1 lies in
  `[10 s_1 − 9, 1]`.
- Separator 2: `Γ_2 ≡ 1` (by the symmetric argument) and `V_2 = 10(1 − s_2)`.
  The constant 0 lies in `[0, 10(1 − s_2)]`. □

So edge-by-edge diagnostics computed from the original bands can report zero
loss on every separator while the gap is 1; the upper bound of Theorem 6 needs
one *jointly* exact split. This matters for any "window detection" heuristic.
Checking Proposition 2(b) bag by bag for **one fixed split** is a joint
condition and is safe. Checking per-separator band membership is not.

*Status.* Consistency note Theorem 3.1 and Proposition 3.3 (proved, reviewed,
"correct"). Both ends of the sandwich are attained in some instances:
- the upper end in a separable example (T1, K = 0);
- the lower end in 515 of 900 random three-bag instances (93 of them with both
  edge terms positive), and in 169 of 300 in the r2 check here.

The path case with the DP split is the deterministic finite-horizon
approximate-LP bound of de Farias–Van Roy.

### 3.9 Proposition 8 (constant cell splits: the worst cell decides, and many cells are needed)

Let `𝒫` partition `R^{k_τ}`, and let `PC(𝒫)` be the functions that are
constant on each cell.

- (a) `inf_{φ ∈ PC(𝒫)} Δ_τ(φ) = sup_{D ∈ 𝒫} g_D`, where
  `g_D = sup_D L_τ − inf_D U_τ`. Hence every path split bound whose class at
  separator τ is `PC(𝒫)` has a gap of at least this value (Theorem 6, lower-bound
  step).
- (b) Let `k_τ = 1` and let `s*` be a pinch point. Put
  `W = [s* − r, s* + r]` with `r = √(2ε/M)`, and suppose that on W:
  - `L_τ` is monotone with `|L_τ(s″) − L_τ(s′)| ≥ (|λ|/2)|s″ − s′|`;
  - `U_τ − L_τ ≤ (M/2)(s − s*)²`.

  If such a bound has gap ≤ ε, then at least `|λ|/√(2Mε)` cells meet W.
  The gap bound must hold at every separator, and each separator has its own
  partition, so the total cell count is at least `Σ_τ |λ_τ|/√(2M_τ ε)` over the
  separators where the hypotheses hold.

*Proof.*
- (a) For `φ = Σ_D c_D 1_D`, `sup(L − φ) = sup_D (sup_D L − c_D)` and
  `sup(φ − U) = sup_D (c_D − inf_D U)`. For any single cell D, the two terms
  sum to `g_D`, so `Δ ≥ g_D` for every choice of constants. Taking
  `c_D = (sup_D L + inf_D U)/2` makes each cell term `g_D/2` (cells with an
  infinite edge are handled by taking `c_D` large or small). Then
  `Δ = sup_D g_D`, which is ≥ 0 because `sup_D g_D ≥ sup_s (L_τ − U_τ) = 0`.
- (b) Take `s′ < s″` in `D ∩ W` with `L` increasing (the decreasing case is
  symmetric). Then
  `g_D ≥ L(s″) − U(s′) = [L(s″) − L(s′)] − (U − L)(s′) ≥ (|λ|/2)(s″ − s′) − ε`.
  So gap ≤ ε forces `diam(D ∩ W) ≤ 4ε/|λ|`. Covering W, of length
  `2√(2ε/M)`, then needs at least `|λ|/√(2Mε)` cells. □

*Status.* (a) is consistency note Proposition 2.3 (proved; checked against a
joint LP). (b) is its Proposition 5.2 (proved, 1-D). The additivity remark is
written here. The analogue in the decomposition note is Proposition 2.6:
constant child bounds need `|λ*|/(6√(M_F ε))` cells. It is the certificate-size
form of Robertson–Cheng–Scott's distinction (`robertson2025-on-the-convergence-order-of`,
metadata only locally): constant bounds converge at first order, Lagrangian
bounds at second order.

*Use.* The proposition explains, in the idealized exact-bag model, why every
working staged certificate used slopes (affine, quadratic, field-type, or
concave chords). It is *consistent with* the failure of the cell-constant DP
on camshape100, but does not explain it (PT-9).

### 3.10 Duality (remark, one sentence in the paper)

For compact bags and continuous data, `sup_{φ∈ΠΦ_t} B(φ)` equals the minimum
over bag probability measures whose neighbouring separator marginals agree on
`Φ_t` (consistency note Theorem 1.1). This also holds for weak*-compact convex
per-bag relaxations such as sparse moment relaxations, which correspond to
polynomial classes. It is known in substance:
- cost-shifting and reparametrization duality (Wainwright–Jaakkola–Willsky
  2005; Werner 2007; Sontag–Globerson–Jaakkola 2011; Wald–Globerson 2014);
- sparse moments (`waki2006-sums-of-squares-and-semidefinite`,
  `lasserre2006-convergent-sdprelaxations-in-polynomial-optimization`);
- gluing (Vorob'ev 1962).

### 3.11 The 15 staged certificates in this language

| instance(s) | split class | validity | why (nearly) exact | window or case split | branching |
|---|---|---|---|---|---|
| dtoc5 | affine (costates) | Lemma 1(a) | each stage term is a strictly convex quadratic (Proposition 2(b); discrete Mangasarian) | none | none |
| lnts50–400 | affine, for each fixed h (aggregated rows; states eliminated) | Lemma 1(d), infeasibility version, for all h ≤ h2 | closed-form per-control maximum (Arrow; linear-tangent law) | global h by monotonicity | none |
| lukvle10 | affine (pair Lagrangian) | Lemma 1(a) + Proposition 3 | exact except at the end transient, where the pair Lagrangian is nonconvex | 3-pair tail, 2-D entry state | 2-D interval B&B (tail 48,628 boxes; middle group 4643; others 900–3800 each) |
| optcdeg2 | quadratic in v; `q_t = 0` at both switches | Lemma 1(a) with interval state enclosures | the costate-affine split loses 0.6258 in float screening: its residual is concave in v on both u = −0.2 arcs. The quadratic class closes the gap to 9.0e-16 | none (final certificate) | 1-D cells in v per stage, 1.33e6 in total |
| chain50–400 | field type in a lifted state (discrete catenary calibration) | Lemma 1(c) over end-value boxes + Lemma 1(a) | closed-form lemma with equality along the optimal chain; the fixed-multiplier length Lagrangian fails because the length row is effectively reverse-convex | end values (z_1, z_N) | 2-D interval B&B (11,121–27,843 boxes) |
| catmix100–800 | concave, positively homogeneous chord minorants of the value functions | **Lemma 1′** | concavity makes chord interpolation second order | none | per-ray 1-D interval B&B over u |
| waterno2_06 (not closed) | cellwise affine | Proposition 4 | gap ≤ 1.68% remains | each 166-variable period is a bag | per cell pair |

What the theory adds to this table:
- the exactness test (Proposition 2(b));
- where the multipliers must come from (Proposition 2(c));
- that the loss of a restricted class is decided at the optimal separator
  values (Theorem 5);
- that windows are the full class on a few separators (Proposition 3), which
  removes those separators' terms from Theorem 6;
- why constant cells need about `|λ|/√(Mε)` cells per separator, while slopes
  avoid this (Proposition 8).

The theory does not predict which class works for a given instance, and it
gives no certificate-size bound for these instances.

### 3.12 Relation to single-tree lower bounds (cite, do not prove here)

The program behind this work asked whether single-tree spatial branch and bound
pays a price exponential in n on low-treewidth models. Two proved results bear
on the interpretation. Neither concerns the MINLPLib instances.

- **Face-exact note, Theorem 1** (`R/theory-face-exact/face-exact-exponential.md`;
  review: "the mathematics is correct"; recheck: theorem statements unchanged
  and correct; post-recheck fixes, §13 item 5, not rechecked).
  - *Setting.* The path family `f(x) = Σ g_i(x_i) + Σ_{i<n} b_i x_i x_{i+1}`
    with `|b_i| = b`, and the quadratic upper bound (Q_D) on a cube
    `x* + [−r, r]^n` inside the root box. The node relaxations have a gap at
    least the termwise McCormick gap (M_b).
  - *Claim.* For `ρ = D/(2b) ≤ 1.99055`, every certified cover at tolerance ε
    has at least `(1 + 1/S)^n exp(−λ(1 + ε/(b r²)))` members, where
    `S = √(1+ρ)` and `λ = (1+S)/(2S²)`. By Lemma 1.2 of that note, this bounds
    the leaves plus 2n per same-relaxation tightening round of any B&B run.
    For the PROGRAM family (D = 2, b = 0.8) with ε ≤ 1e-4 and r ≥ 1/2 this is
    ≥ `0.57 (5/3)^n`.
  - *Scope.* The bound holds for a strictly convex QP written with separate
    bilinear terms. It does not cover PSD-minor cuts (default SCIP),
    relaxations of aggregated sums, branching on lifted variables or
    objective-cutoff propagation.
- **Calibration note, Corollary 3.8.** On the same family (`κ + |b| ≤ 1`), the
  balanced split is an exact calibration checked by n − 1 two-variable bag
  minimizations. For b = 0.8, κ ≤ 0.2 and ε ≤ 1e-4, every single-tree
  certificate with termwise McCormick needs ≥ `0.57 (5/3)^n` members. The note
  stresses that "transcriptions of ODEs are not covered" and that "the MINLPLib
  gaps are empirical".

*Paper use.* At most one paragraph: a proved separation on a synthetic family
shows that the relaxation class, not search alone, can force exponential
branching, while a split certificate needs none. No such bound is known for the
instances studied here, and default SCIP lies outside the theorem's relaxation
class.

### 3.13 Theory results reviewed and excluded

| result (location) | status | reason for exclusion |
|---|---|---|
| single-tree lower bounds (face-exact Theorems 1–2) | proved; reviewed and rechecked; post-recheck fixes not rechecked | synthetic family; no statement about these instances; cite only (3.12) |
| decomposition certificates: Theorem 3.4, adaptive algorithms, covering upper half, algorithm GR (`R/theory-decomposition/`) | proved and reviewed with stated gaps; §8.1 fixes of the main note not rechecked | existence and complexity results on synthetic families, with numerically vacuous constants; overlaps the theme of `paper-decomposition-aware/` (corrected grids over tree decompositions) |
| split-robust lower bounds; RLCT; dense coupling | proved and reviewed; tiny bases or largely negative | unrelated to the certificates |
| consistency note §5.3–5.5 (piecewise-affine cells, shells, polynomial and hp rates, Bernstein limit) | proved, partly sketches (Proposition 4.3) and one conjecture | not used by any certificate |
| bang-bang window law, κ_τ trichotomy, singular arcs, transfer theorem | proved under stated hypotheses; several parts at sketch level | mesh-size asymptotics; no certificate depends on them; the optcdeg2 dossier may cite the κ = 0 discussion |

---

## 4. Exactly feasible primal points

This section does not apply at the pattern level. The only primal statement is
Proposition 2(b): a split certificate is exact iff one feasible point minimizes
every stage problem. In practice the staged certificates are built around a
numerically optimal trajectory, and their exactness up to rounding confirms it.

Exactly feasible points for lnts, dtoc5, lukvle10, chain and powerflow are in
`R/publication/primal/` and the family dossiers:
- lnts: a reduced-system existence proof;
- dtoc5: exact rationals;
- lukvle10: exact seeds and recurrence;
- chain: exact algebraic points.

catmix uses exactly feasible author points (100/200/400) and the verifier's
exact DP-policy point (800). optcdeg2 uses the verifier's rigorously feasible
point. For lukvle10 the KKT agreement is numerical, so attributing its
remaining gap to the dual side assumes the KKT point is globally optimal.

---

## 5. Numbers

### 5.1 Coverage numbers

See Section 2.3. Every count was recomputed by `r2_checks.py` (§A–C), which
copies the inputs first; the earlier `coverage_checks.py` gives identical
counts.

### 5.2 Staged closures (authoritative displays)

The summary is authoritative. Individual chain and catmix duals are safe
displays from `R/publication/reproduction/cops/logs/exact_display_checks.json`;
the summary shows only ranges for them. Gap cells are the summary's upward
displays; the exact values are in `R/publication/integration/gap-values.json`.
Listed duals were checked against `R/bound-audit/pages.json`.

| instance | best listed dual (solver) | our rigorous dual | primal (upper end; exactly feasible) | gap (rounded up) |
|---|---|---|---|---|
| lnts50 | 0.55464755 (GUROBI) | 0.5546687649381 | 0.5546687649387 | ≤ 5.79e-13 |
| lnts100 | 0.55299042 (GUROBI) | 0.5545954011663 | 0.5545954011670 | ≤ 6.12e-13 |
| lnts200 | 0.55219867 (GUROBI) | 0.5545770161025 | 0.5545770161031 | ≤ 5.84e-13 |
| lnts400 | 0.55204395 (GUROBI) | 0.5545724137001 | 0.5545724137007 | ≤ 5.88e-13 |
| dtoc5 | 0.00243096 (BARON) | 5.38967211918114 | 5.389672119181141 | ≤ 4.7e-16 |
| lukvle10 | 351.223393 (SCIP) | 352.2380254050784 | 352.2380254064961 | ≤ 1.5e-9 |
| optcdeg2 | 292.41713458 (GUROBI) | 293.87607509587509 (certificate rounded down) | ≤ 293.87607509587509328 | ≤ 9e-16 (from the exact certificate) |
| chain50 | 0.17451499 (ANTIGONE) | 5.0722614939828627 | 5.07226149398287232 | ≤ 9.7e-15 |
| chain100 | 0.09367008 (ANTIGONE) | 5.0697846107387505 | 5.06978461073876056 | ≤ 1.01e-14 |
| chain200 | 0.08256615 (ANTIGONE) | 5.0689173417931616 | 5.06891734179317101 | ≤ 9.5e-15 |
| chain400 | 0.09563835 (ANTIGONE) | 5.068621694604009 (17-digit safe display 5.0686216946040092) | 5.06862169460401902 | ≤ 1.01e-14 |
| catmix100 | −0.06655801 (LINDO) | −0.048069432031144562 | −0.0480694320309595629 | ≤ 1.85e-13 |
| catmix200 | −0.07254639 (LINDO) | −0.048059145599072769 | −0.0480591455801143935 | ≤ 1.90e-11 |
| catmix400 | −0.65810523 (LINDO) | −0.048056547824671288 | −0.0480565477566115548 | ≤ 6.81e-11 |
| catmix800 | −1.48896963 (LINDO) | −0.048055901479675652 | −0.0480559013312308003 | ≤ 1.49e-10 |

Notes on the table:
- The catmix duals are the verifier's (stronger) values. The catmix100/200/400
  primals are the authors' exact points; the catmix800 primal is the
  verifier's DP-policy point (exact display record).
- The chain gaps were recomputed by exact subtraction from the displayed dual
  and the stored upper end: 9.616e-15, 1.006e-14, 9.400e-15 and 1.001e-14.
  The catmix gaps, recomputed the same way, are 1.850e-13, 1.896e-11,
  6.806e-11 and 1.484e-10.
- Every displayed gap cell is ≥ its exact value in `gap-values.json`; this was
  checked for all 15 rows.

No disagreement with the summary was found. Do not use these older displays:
- `R/SYNTHESIS.md` gives waterno2_06 as "1.67%". The exact ratio from the
  displays is `(282.888038 − 278.230573)/278.230573 = 1.674%`, so the safe
  display is the summary's ≤ 1.68%.
- `R/SYNTHESIS.md` gives ann_cumene_tanh as "0.194%". That value uses the dual
  denominator (0.19365%). The summary uses the primal denominator, 0.19402%,
  displayed as ≤ 0.195%.

### 5.3 Evidence on "relaxation versus branching" (saved one-hour campaign)

Source: `R/publication/solver-runs/results_table.csv`, one thread, 3600 s,
requested gaps 1e-9; extracted in `logs/r2_checks.log` §F. The ratio
`(best − listed)/(certificate − listed)` uses the best unqualified final solver
dual: it excludes BARON values without a globality guarantee (`*`). Ratio 1
means the solver reached the certificate; a negative ratio means it stayed
below the listed dual. Flags:
- `*`: no globality guarantee (excluded);
- `t`: SCIP on slightly tightened argument bounds;
- `o`: overloaded first batch.

| instance | listed dual | certificate | BARON | GUROBI | SCIP | ratio |
|---|---|---|---|---|---|---|
| lnts50 / 100 / 200 / 400 | 0.5546–0.5520 | 0.55467–0.55457 | — | 0.554647 / 0.551893 / 0.552266 / 0.550886 | 0.5188 / 0.5195 / 0.5078 / 0.5451 | −0.033 / −0.684 / +0.028 / −0.458 |
| dtoc5 | 0.00243 | 5.3897 | 0.000273*o | −781.5 o | 1.9999e-5 o | −0.0004 |
| lukvle10 | 351.2234 | 352.2380 | 0.0117 | — | 347.647 t | −3.53 |
| optcdeg2 | 292.4171 | 293.8761 | 2.32*o | 166.8 o | 200.13 o | −63.3 |
| chain50 / 100 / 200 / 400 | 0.17–0.08 | 5.07 | −88.9 / −409 / −395 / −888 | −36.2 / −76.0 / −141 / −683 | −74.9 / −276 / −903 / −1673 | −7.4 / −15.3 / −28.3 / −137 |
| catmix100–800 | −0.067 … −1.49 | −0.0481 | −1.18 … −54.6 * | −∞ | −∞ | no finite unqualified dual |
| camshape100 / 200 / 400 / 800 | −4.284 … −5.126 | −4.284 … −4.274 | −4.28415 / −4.27850 / −4.622 / −5.145 | −4.516 / −4.802 / −5.012 / −5.158 | −4.529 / −4.843 / −5.058 / −5.203 | 0.899 / 1.000 / 0.503 / −0.022 |
| hvycrash | −2.185e8 | −0.2185 | — | −2.14e9 | −2.185e8 t | 0.000 |
| powerflow0030p / 0039p / 0039r | 572.8 / 41818 / 41805 | 576.89 / 41869.05 / 41869.05 | — / — / 41268.8 | 569.9 / 41765.7 / 41618.5 | 0 / 2 / 41745.9 | −0.73 / −1.04 / −0.92 |
| eg_int_s / eg_disc_s / eg_disc2_s | 6.326 / 3.366 / 0 | 6.453 / 5.761 / 5.642 | 0.88 / 1.09 / −5.02 | −1.91 / −2.86 / −6.37 | 5.439 / 2.716 / −2.830 | −7.0 / −0.27 / −0.50 |

SCIP node counts (saved logs, spot-checked here):
- hvycrash: 504,455 nodes; dual −2.185e8 on the first and last progress line;
  0 solutions;
- camshape100: 1,179,749 nodes, final dual −4.52868 (5.71% gap);
- lnts50: 79,792 nodes, 0.51879;
- chain50: 53,029 nodes, −74.906; chain400: 7 nodes;
- powerflow0030p: 23,036 nodes, dual 0;
- powerflow0039p: 9,563 nodes, dual 2; powerflow0039r: 67,428 nodes, 41,745.9;
- catmix100: 1,347 nodes, no finite dual;
- dtoc5 and optcdeg2: 1 node each (overloaded batch).

Reading:
1. For the 15 staged closures no unqualified one-hour dual reached the listed
   dual, except lnts200 (2.8% of the listed gap).
2. The polar and rectangular powerflow0039 models carry the same optimum.
   SCIP's dual is 2 on the polar model and 41,745.9 (0.3% below) on the
   rectangular one, so the formulation, not the search, decided.
3. camshape shows both sides.
   - SCIP improves steadily by branching (camshape100: −5.163 to −4.529 over
     1,179,749 nodes) but stops 5.7% short. This is a counterexample to a
     strict "branching is irrelevant" reading.
   - BARON reaches −4.28414764756 on camshape100 after only 3 BaR iterations,
     and −4.27850228570 on camshape200 after 723. This points to its
     relaxation and range reduction, not to search.
   - BARON's bounds coincide with its tolerance-feasible incumbents, which
     lie below the exact optima. The bounds are valid, but its optimality
     claims are contradicted by the certificates, and it returns infeasible
     points (BaR iteration counts from the saved BARON logs).

Caveats:
- one budget and one machine (shared);
- dtoc5 and optcdeg2 rows come from the overloaded first batch (READINESS,
  open decision 2);
- the SCIP runs on ex6_2_5, ex6_2_7 and pindyck stopped at the memory limit;
- the solver-analysis review r1 checked the raw values; this extraction itself
  was not reviewed.

### 5.4 How much branching each closure needed

| branching | instances |
|---|---|
| none | lnts50–400, dtoc5, camshape100–800, hvycrash, etamac, powerflow0030p (12) |
| 1-D | optcdeg2 (cells per stage), catmix100–800 (per ray), pricing050 (16,960 boxes in 50 univariate problems) (6) |
| 2-D | lukvle10, chain50–400, ex6_2_7 (488,064 boxes), ex6_2_5 (5.9M boxes in its liquid phase) (7) |
| 3-D | powerflow0039p/0039r (3 leaf-bus coordinates) (2) |
| small but high-dimensional | pindyck: 9 boxes (8 bisections) of a 112-dimensional parameter box in the concavity proof (1) |
| full original space, 7 variables (3–4 continuous plus integer splits) | eg_int_s, eg_disc_s, eg_disc2_s (1,114,361 leaves for eg_disc2_s run G) (3) |

Sources: the family reports and `R/open-instances-wave2/small/report.md` §4.3, §6;
`R/open-instances-wave2/small/pindyck-extension.md` §3.6;
`R/open-instances-wave3/eg/retry.md` §2; summary.

---

## 6. Verification record

| item | evidence | verdict | remaining assumptions and caveats |
|---|---|---|---|
| Lemma 1, Propositions 2–3 | calibration note Lemma 2.1, Theorem 3.1, Proposition 4.4; consistency note Proposition 5.1; `R/reviews/calibration-review.md`, `calibration-recheck.md`, `recheck-calibration-confirm.md` | review: Theorem 3.1 "correct (small fix F4)"; recheck: "No mathematical error was found"; confirmation: fixes correct; four wording points applied by the root, not rechecked | classical in substance |
| Lemma 1′ (catmix) | calibration note §2.4 item 6, Proposition 2.3; COPS report §3; `R/reviews/cops-verification/verification-report.md`; `R/reviews/catmix-recheck.md` | COPS verification item 2b ("concavity, homogeneity, chord lower bounds"): verified; 2c (authors' per-ray B&B): "verified by reading, with caveats"; own DP for N = 100/200; the catmix recheck confirmed 400/800 | restated here as a lemma; the induction is two lines |
| Theorems 5–6, Propositions 7–8 | consistency note Theorems 2.1, 3.1, Propositions 2.3, 3.3, 5.2; `R/reviews/consistency-review.md` ("I found no false theorem"; Theorem 2.1 "correct, with the exact constant 2"), `consistency-recheck.md` ("Correct as revised"), `recheck-consistency-confirm.md` and `consistency-confirm-r1.md` (no mathematical error) | proved; reviewed four times | the note assumes box bags and bounded value functions; the extended-value versions here are new write-ups (next row) |
| Proposition 4 (validity) | `cell-slopes.md` Proposition 1; `R/reviews/waterno2-cellslopes-review.md` | reviewed: "correct" | the generic form and Remark 2 are written here, not reviewed |
| restatements in this dossier | extended-value Theorems 5–6 (simpler lower-bound proof), Proposition 2(c) in path form, Proposition 4 Remark 2 and Proposition 8 additivity (from the earlier version of this dossier); Lemma 1(b)–(d) and Lemma 1′ (added in this revision) | this revision re-derived every proof independently and found no error. Numerical spot checks, two independent codes: Theorem 5 on 300 + 600 random separators (max deviation 3.9e-14 and 1.4e-13); Theorem 6 lower bound on 200 + 300 random paths (0 violations); Proposition 7 in exact rationals | **no independent review in the research process**; recommend one confirmation pass on the final paper text (PT-6) |
| scout counts (283, 146, bands) | `R/open-instances-scout/targets.md` (not reviewed) | reproduced from `fetched.json` and independently from the audit's page parse; the status refresh found the relevant pages unchanged on 2026-10-02 | heuristic widths; the selection rule is one of many possible; `fct` missing from the census |
| census shares | `R/treewidth-census/census-report.md` (not reviewed) | reproduced; the closing audit checked 13.6% and 62.7%; the coupling review and recheck reproduced 14.8% and 17% | heuristic widths; expression-splitting artifact (chain) |
| S-mark and listing-dual definitions | MINLPLib documentation snapshot (literature slug above) | read here. The listing dual equals the third-best bound in all 1568 instances with ≥ 3 finite bounds, counting `inf` entries, up to display rounding. A naive three-displayed-duals test matches the S mark in 1612 of 1633 instances | the documentation does not state the feasibility tolerance; S records optimality claims, not displayed bounds |
| single-tree lower bound (cited only) | `R/reviews/face-exact-review.md`, `face-exact-recheck.md` | Theorems 1 and 2 correct | post-recheck fixes not rechecked |

What must be trusted: nothing computational for the theory. For each instance,
the rigorous stage evaluations and their arithmetic are as stated in the family
dossiers: mpmath iv / ivnp outward rounding, exact rationals, and A1/A2 for eg.

---

## 7. Relation to prior work

**Mechanisms** (all classical):
- Lagrangian duality and decomposition.
- Discrete sufficient conditions: Krotov (`krotov1967-sufficient-conditions-for-the-optimality`,
  read); Mangasarian (`mangasarian1966-sufficient-conditions-for-the-optimal`,
  read); Arrow (`arrow1970-public-investment-the-rate-of`, unread); Tamminen's
  "Lagrangian minimized in state and control"; the pointwise form of
  Leitmann–Stalford (1971).
- Bellman inequalities and the LP approach to approximate DP. De Farias–Van
  Roy (2003), read via Lakshminarayanan–Bhatnagar–Szepesvári and the NeurIPS
  2001 version, give a `2×` approximation-error bound: the one-sided form of
  Theorem 5 on paths and the upper bound of Theorem 6 with the DP split.
- Cost-shifting and reparametrization duality in graphical models and weighted
  CSP (Wainwright–Jaakkola–Willsky 2005; Werner 2007; Sontag–Globerson–Jaakkola
  2011; Cooper–de Givry–Schiex). Wald–Globerson (UAI 2014, text read) give the
  convex case of Proposition 2(b).
- Sparse moment relaxations as polynomial split classes
  (`waki2006-sums-of-squares-and-semidefinite`,
  `lasserre2006-convergent-sdprelaxations-in-polynomial-optimization`).
- The sufficiency direction of the band identity with positive band width:
  Grimm–Netzer–Schweighofer 2007, Lemma 3 (read). Its quantitative form:
  Korda–Magron–Ríos-Zertuche 2025, Lemma 11 (arXiv v1 read). The zero-width
  identity is Han–Jiao–Weissman's (COLT 2018, Lemma 25).

These works are not in `literature/` except where a slug is given; their
reading status is recorded in consistency note §8. The paper's bibliography
needs entries for them.

**New as far as the consistency note's searches found** (all elementary):
- the exact identity with constant 2 and its clipping proof;
- the worst-cell formula;
- the `2 max` lower bound on trees and paths;
- the counterexample to edge-by-edge control.

The searches cannot establish priority.

**Value-function minorants in multistage optimization.** SDDP and nested
Benders with Lagrangian cuts are the stochastic counterpart of affine
calibrations: Zou–Ahmed–Sun 2019; `zhang2022-stochastic-dual-dynamic-programming-for`;
`fullner2022-non-convex-nested-benders-decomposition`. Junge–Osinga (2004)
build value-function lower bounds from shortest paths on cell graphs, the
closest analogue of Proposition 4 found by the audit
(`R/literature/decomposition-bb-prior.md` §1.6). Robertson–Cheng–Scott 2025
(`robertson2025-on-the-convergence-order-of`, metadata only locally; read via
the audit) give the order-1 versus order-2 distinction that Proposition 8 turns
into a cell count.

**Global dynamic optimization by branch and bound:**
`chachuat2005-global-mixed-integer-dynamic-optimization`; Houska–Chachuat's
branch-and-lift (JOTA 2014; control literature report), with mesh-independent
run-time bounds. Their existence is why the calibration note says
exponential growth in N is not inherent to B&B on control parametrizations.

**Why single-tree solvers struggle.**
- The cluster problem: `neumaier2004-complete-search-in-continuous-global`,
  `wechsung2014-the-cluster-problem-revisited`,
  `kannan2017-the-cluster-problem-in-constrained`.
- B&B lower bounds at small treewidth that rely on ties:
  `basu2023-complexity-of-branch-and-bound`, `dey2022-lower-bound-on-size-of`.
- Bound tightening for unbounded variables:
  `belotti2009-branching-and-bounds-tightening-techniques`,
  `belotti2012-on-feasibility-based-bounds-tightening`.

**MINLPLib:** `bussieck2003-minlpliba-collection-of-test-models`;
`vigerske2026-minlplib-a-library-of-mixed` (site);
`vigerske2026-minlplib-documentation-database-snapshot-2026` (S definition,
FAQ).

**Instance-level prior results** are in the summary's literature table and
the three literature reports: floating-point closures, likely ε-global results
for ex6_2_*, Göß–Burlacu–Martin, CAMINO.

**What is not new.** The pattern itself is not new as an idea: a chain
Lagrangian with multipliers from a local solution, plus exact treatment of
nonconvex windows, is what DP and decomposition practitioners would try. The
new elements are the rigorous certificates, the taxonomy and the explanatory
identities.

---

## 8. Critical examination

### 8.0 What was re-derived and recomputed for this revision

- **Proofs re-derived from scratch:**
  - Lemma 1(a)–(d) and Lemma 1′ (including the catmix concavity induction);
  - Proposition 2(a)–(c), including the shared-coordinate induction;
  - Proposition 3; Proposition 4 and Remark 2 (shortest-path LP duality);
  - Theorem 5 in the extended-value form, including the cases with infinite
    edges and infinite Δ;
  - Theorem 6 by weak duality on head and tail, and the osc argument;
  - Proposition 7 analytically and in exact rationals;
  - Proposition 8(a)–(b), including the arithmetic
    `2√(2ε/M)·|λ|/(4ε) = |λ|/√(2Mε)`.

  No error was found in the sources or in the earlier dossier's proofs.
- **New independent numerical spot checks** (`r2_band_checks.py`, HiGHS LPs,
  floating point, illustration only):
  - Theorem 5, affine class, 600 random separators: max
    `|inf Δ − 2 dist|` = 1.43e-13;
  - Theorem 6 lower bound on 300 random three-bag paths: 0 violations,
    lower end attained in 169.
- **Coverage, by new code** (`r2_checks.py` §A–C):
  - the funnel, the 294 = 283 + 11 set identity, 155, 29 and 12;
  - the bands from the audit parse;
  - the listing-dual rule and the S mark against all listings;
  - the `fct` case.
- **Model facts** (§D–E): free-variable counts from the OSIL files; chain's
  nonlinear-primal graph.
- **Campaign evidence** (§F): all three solvers' final duals against the
  certificates; SCIP node counts spot-checked in the raw logs.
- **camshape cell DP** (§G): local convergence order of the first-wave table.
- **Numbers:** every gap cell in Section 5.2 checked against `gap-values.json`
  (display ≥ exact), and the chain/catmix displays against the exact display
  record.

### 8.1 Issues and resolutions

**PT-1 (major, definitions): two meanings of "open".**
- The record says "31 instances listed as open" (no S mark) and "146 open
  among 283 low-width nonconvex candidates" (the scout's rule). These are
  different predicates on different populations.
- camshape100 and lnts50 are open only in the first sense, and the scout
  population excludes the first wave.
- The summary's phrase "MINLPLib's 1e-6 rule" omits the three-solver
  requirement.
- *Resolution:*
  - Quote MINLPLib's S definition (at least 3 solvers claim optimality within
    relative gap 1e-6, or infeasibility) and cite the documentation snapshot.
  - Define "listed as open" = no S mark, and "open by the 1e-4 rule" separately.
  - Present the funnel of Section 2.3 (294 → 155 → 29 closed, plus the 2
    marginal cases), with the selection caveats.
- No computation is needed; the counts are done.

**PT-2 (major, interpretation): "the obstacle was the relaxation, not the
amount of branching" is untested, and the dichotomy is not sharp.**
- *For it:*
  - Section 5.3: for the staged closures, one hour of branching left every
    unqualified solver dual below the listed dual (except lnts200, +2.8%).
  - hvycrash (504,455 nodes) and powerflow0030p (23,036 nodes) never move
    their dual.
  - powerflow0039p versus 0039r: the formulation decides.
  - Most certificates branch little (Section 5.4).
  - Free variables are pervasive in the hard chains (Section 1.2).
- *Against a strict reading:*
  - camshape: SCIP's bound improves steadily with branching (1.18M nodes) but
    stops 5.7% short. BARON's near-closure took 3 and 723 BaR iterations, so
    it reflects a stronger relaxation, which supports rather than contradicts
    the reading.
  - eg_disc2_s's certificate needed 1.1M leaves; ex6_2_5's needed 5.9M boxes
    in 2-D.
  - ex6_2_*, pricing050 and eg_* have no free variables at all.
  - The face-exact theorem shows that weak termwise relaxations and branching
    cost are linked, not alternatives.
- *Resolution:* use the wording of Section 9 ("decisive ingredient was a
  bounding argument adapted to the structure; branching, where used, was
  low-dimensional or small"), and optionally Tables 5.3 and 5.4.
- *Optional experiment* (needs user authorization; about 7–14 single-thread
  CPU-hours): rerun one solver for one hour each on dtoc5, optcdeg2,
  lukvle10, chain50, catmix100 and hvycrash, with the certified variable
  enclosures added as bounds; and on camshape100 reformulated in `u = 1/r`.
  If the gaps then shrink sharply, the "free variables / formulation" reading
  becomes evidence.

**PT-3 (major, wording): the pattern sentence overstates.**
- The summary says "Most certificates (lnts, dtoc5, lukvle10, optcdeg2, chain,
  catmix, and the waterno2 improvements) combine a decomposition …, an affine
  or state-dependent split …, and exact treatment of a few low-dimensional
  windows". SYNTHESIS says "about half (15) use affine or state-dependent
  splits along chains plus short exact windows".
- *Facts:*
  - 15 of 31 closures is not "most"; nor is 7 of the 17 families.
  - Windows occur only in lukvle10 and chain. lnts treats h by monotonicity.
    dtoc5, catmix and the final optcdeg2 certificate have no window.
  - waterno2's bags are 166-variable periods.
  - The split classes are affine (dtoc5, lnts, lukvle10), quadratic
    (optcdeg2), field-type (chain), concave chord minorants (catmix) and
    cellwise affine (waterno2).
- *Resolution:* use the class table (Section 1.1) and the wording in Section 9.

**PT-4 (major for the paper's theory section; no effect on validity): validity
basis.**
- The earlier version of this dossier said that "Validity rests on Lemma 1, its
  window and cell variants". catmix's certificate is not a split bound of
  Lemma 1: its computed `W_i` need not be concave. It is valid by Lemma 1′
  (value-function minorants), which uses concavity of the true value functions.
- *Resolution:* state Lemma 1′ in the paper (Section 3.3). The proof is two
  lines and already verified in substance by the COPS verification.

**PT-5 (minor, documents): outdated passages that must not be quoted.**
- `R/SYNTHESIS.md` lines 42–44 and 485–489 and `R/closing-research-results.md`
  (§4 first bullet; Limits) say that 13 closures have no exactly feasible
  point. This is superseded by `R/publication/primal/` and the summary.
- "eg_disc2_s partly by sampling" (SYNTHESIS line 41) and the closing record's
  "110,676 of 979,044" are superseded by the all-leaf recheck under A1/A2.
- waterno2_06 "1.67%" and "1.7–10.8%" are unsafe roundings; use ≤ 1.68%.
  ann_cumene_tanh "0.194%" uses a different denominator; use ≤ 0.195%.
- "Waves 2 and 3 tested this [capability]" (SYNTHESIS line 701): the
  certificates were hand-built per instance; no solver component was
  implemented.
- `R/theory-calibration/scouting.md` §2.4: the optcdeg2 row ("affine … head
  block") and "Quadratic (Riccati) calibrations were not needed by any closed
  instance" are false after the bang-bang closure.
- *Resolution:* cite only the summary and READINESS for numbers and statuses.

**PT-6 (minor, rigor): the theory sources assume idealized bags; the
certificates use constrained stages and enclosures.**
- The consistency note assumes box bags, bounded data and exact bag minima.
- *Resolution:*
  - Use the versions of Section 3. They allow arbitrary bag sets,
    extended-valued value functions and enclosures, and need only `Z ≠ ∅` and
    costs bounded below; all proofs are given.
  - State that certificate validity rests only on Lemmas 1 and 1′,
    Propositions 3 and 4, and the instance computations.
  - Run one confirmation pass on the final paper text: a reviewer reads the
    proofs and runs the two small check scripts, about one reviewer-hour; no
    new research computation.

**PT-7 (minor, provenance): scout and census are unreviewed root computations;
two data artifacts.**
- (i) `fct` is missing from the census, so the full-library candidate count is
  295, not 294; the open count is unchanged at 155.
- (ii) The census's nonlinear-primal width ignores constant × sum products.
  chain's bound N+1 should be 1.
- *Resolution:*
  - State both facts.
  - Report that the counts reproduce from saved data with two page parses.
  - Say that the selection is post hoc for the first wave and
    tractability-ranked afterwards.
  - Do not use chain's census nonlinear-primal width as evidence about width.
  - If the paper quotes the 62.7% share, add "heuristic upper bounds;
    expressions are split only at top-level sums". A corrected census would be
    a cheap rerun (minutes) but needs authorization; it is not needed for any
    claim.

**PT-8 (minor, scope): single-tree lower bounds.**
- *Resolution:* do not state them as theorems of this paper; use the wording
  of Section 3.12. If the paper cites face-exact Theorem 1, get one
  confirmation of its post-recheck fixes (§13 item 5); this is a short review.

**PT-9 (minor, wording): Proposition 8 and camshape.**
- The failed camshape cell DP also relaxed rows cellwise, and the report
  traces the obstacle to a per-stage constraint scale of order `1/n²`. Its
  measured error falls with local order 0.22–0.83 in the cell width
  (`logs/r2_checks.log` §G), not with the first-order rate of Proposition 8.
- *Resolution:* write "consistent with", never "explained by".

**PT-10 (minor, evidence quality): campaign rows from the overloaded batch, or
with memory stops or tightened models.**
- *Resolution:* label those rows as in Table 5.3. Rerunning them is READINESS
  open decision 2 (13 one-hour runs).

**PT-11 (minor, wording): "branch, if at all, in at most four continuous
dimensions" is false.**
- pindyck's concavity proof uses 9 boxes in a 112-dimensional parameter box.
  eg branches in the full 7-variable space, with up to 1.1M leaves.
- *Resolution:* use Table 5.4 and the wording "no branching (12 closures),
  1–3-dimensional branching (15), a 9-box concavity proof (pindyck), or
  branching in the full 7-variable space of the eg models".

**PT-12 (minor, wording): the summary's parenthesis "(affine splits plus full
consistency on short windows; reviewed, rechecked and confirmed)"** can be read
as saying that the link to the instances was verified. Only the theorems were.
- *Resolution:* attach "reviewed, rechecked and confirmed" to the theorem
  citation, and call the link an interpretation.

**PT-13 (minor, unproved claim): optcdeg2 "no affine function lies in the band
there"** (calibration note §2.4 item 3; the earlier dossier repeated it).
- What is established is narrower. The costate-affine calibration loses 0.6258
  in float screening, because its residual is concave in v on both u = −0.2
  arcs (bang-bang note §5.2).
- A conditional strengthening follows from Proposition 2(c). Suppose a global
  minimizer has interior states on an arc and a fractional control at a
  stage. Then any exact affine split has the costate slopes, with the terminal
  multiplier pinned by the fractional stage. If, at that minimizer, the forced
  costate makes the residual strictly concave in v at some interior arc
  stage, then no affine split is exact.
- Per-separator band membership was not examined, and by Proposition 7 it
  would not suffice anyway.
- *Resolution:* say "the costate-affine split cannot be exact on optcdeg2's
  u = −0.2 arcs (stage residual concave in v); a quadratic split closes the
  gap". Avoid "no affine band element".

### 8.2 Would anything invalidate a claimed result?

No. The pattern-level claims are definitional or interpretive. The theory used
to explain them was re-derived without error, and its extended-value versions
are proved above. The counts reproduce exactly. The certified numbers in
Section 5.2 match the summary and `gap-values.json` under exact recomputation.
The corrections in PT-4, PT-7, PT-11 and PT-13 change wording and scope, not
any bound.

---

## 9. What the paper may claim and must not claim

**May claim** (suggested wording):

- "We certify 31 MINLPLib instances that were not marked solved: MINLPLib marks
  an instance solved when at least three solvers claim global optimality within
  a relative gap of 10⁻⁶. The listing was fetched on 2026-09-29/30, and the
  marks were unchanged at a refresh on 2026-10-02. The bounds hold for every
  exactly feasible point of the stored OSIL models, under the stated
  assumptions (A1/A2 for the three eg_* instances)."
- "Fifteen of the 31 closures share one pattern:
  - a split of the objective along the model's stage structure (Lagrangian
    multipliers, a discrete calibration, or chord minorants of concave value
    functions);
  - stage problems small enough to be minimized rigorously;
  - where the split cannot be exact, a small exact window (Lemmas 1 and 1′,
    Propositions 2–3).

  Four more (camshape) use a comparison argument along the same chain, and
  three are Lagrangian splits over at most five dense rows."
- "For a split restricted to a class of functions at one separator, the loss
  equals exactly twice the sup-norm distance from that class to the band between
  `f*` minus the cost-to-come and the cost-to-go (Theorem 5). On a path, the
  loss of all separators together is at least twice the largest such distance
  (Theorem 6). To the best of our knowledge, the identity and this lower bound
  have not been stated before. Their one-sided forms are classical
  (de Farias–Van Roy; Grimm–Netzer–Schweighofer)."
- "Constant (zero-slope) cell bounds need at least `|λ|/√(2Mε)` cells at each
  separator with nonzero multiplier λ (Proposition 8). This is consistent with
  the failure of a cell-constant dynamic program on camshape100; every staged
  certificate that worked used slopes."
- "Applying one selection rule to MINLPLib gives 294 instances, none marked
  solved: nonconvex; heuristic factor-incidence width ≤ 16, or nonlinear-primal
  width ≤ 6 with ≥ 50 nonlinear variables; listing gap > 10⁻⁴. Of these, 155 have
  a best listed single-solver gap above 10⁻⁴. Our certificates close 29 of the
  155, and two more instances whose listed single-solver gaps were already
  1.2·10⁻⁶ and 3.8·10⁻⁵. Instances were chosen by expected tractability, so this
  proportion does not measure the difficulty of the open population."
  (Footnote: `fct` lacks census data and would satisfy the rule; its listed gap
  is 0.)
- "In every closed case, the decisive ingredient was a bounding argument
  adapted to the model's structure (a split, a duality or convexity
  certificate, a comparison or an identity, or enclosures that keep
  cancellation). After it, branching was absent in 12 closures, at most
  three-dimensional in 15, and small or confined to the 7 original variables
  in the rest. In our reading (an interpretation, not tested experimentally),
  the termwise relaxations of single-tree solvers were held back by free
  variables, long chains of nonconvex equalities, hidden convexity or
  monotonicity, and cancellation among many terms. In a one-hour run with
  three solvers, no solver's dual with a globality guarantee reached the
  listed dual on 14 of the 15 staged instances."
  Cite Tables 5.3–5.4 with their caveats.

**Must not claim:**
- that a general solver capability (decomposition-aware B&B, window
  detection) was implemented or tested; the certificates are hand-built per
  instance;
- that single-tree B&B provably needs exponential effort on these instances,
  or that small treewidth caused their open status (lnts's certificate ignores
  the separator structure; widths are heuristic bounds with parsing
  artifacts);
- that the band theorems prove or predict the closures; they explain when
  split certificates can be exact;
- that "most" certificates share the pattern, or that all pattern certificates
  use windows;
- that all staged certificates are instances of Lemma 1 (catmix uses Lemma 1′);
- that the certificates branch only in low dimension (pindyck, eg);
- that the 146 or 155 are MINLPLib's own set of open instances, or that 29/155
  is a solve rate;
- novelty of the mechanisms (Lagrangian and SDP duality, calibrations,
  Mangasarian/Arrow, Sturm comparison), or blanket "previously unsolved"
  statements (READINESS: "No unconditional priority claim or blanket
  'previously unsolved globally' claim is supported");
- that no affine split can be exact on optcdeg2 without the conditions of PT-13;
- any statement from the outdated passages listed under PT-5.

---

## 10. Candidate figures and tables

1. **Table (main text): mechanism taxonomy of the 31 closures** (Section 1.1),
   with columns:
   - class and mechanism;
   - instances and count;
   - branching dimension (Section 5.4);
   - arithmetic (exact rational / mpmath iv / outward-rounded binary64 /
     A1–A2).
2. **Table: the 15 staged certificates** (Sections 1.2 and 3.11 merged), with
   columns:
   - stages and separator dimension;
   - free variables;
   - split class;
   - validity lemma;
   - window;
   - stage-check method.
3. **Figure: coverage funnel.** 1633 → 1257 → 596 → 360 → 294 → 155 → {29
   closed, 6 KAN (R only), 6 improved}, with camshape100 and lnts50 marked
   separately.
4. **Figure: the band picture** (schematic, 1-D separator):
   - `V_τ` above and `f* − Γ_τ` below, pinched at `s*`;
   - an affine band element tangent at `s*`;
   - a case where no affine function fits (`cav L > vex U`), fixed by a window
     or by a quadratic split;
   - a constant-cell staircase that must shrink near `s*` (Proposition 8).
5. **Table: certificate versus one-hour solver duals** (Section 5.3), with
   caveat flags.
6. **Figure (optional): listed best dual versus certified dual** as relative gap
   before and after, on a log scale, for all 43 instances. Data: summary and
   `gap-values.json`.

---

## Appendix. Commands run for this revision

From `paper-open-minlplib/development/dossiers/checks/pattern-theory/`:

```
OMP_NUM_THREADS=1 python3 r2_checks.py > logs/r2_checks.log
OMP_NUM_THREADS=1 python3 r2_band_checks.py > logs/r2_band_checks.log
```

`r2_checks.py` copies `pages.json`, `fetched.json`, `candidates.json`,
`census_merged.json`, the campaign `results_table.csv` and 25 OSIL files from
the local MINLPLib cache into a fresh temporary directory, reads only those
copies, and deletes them. `r2_band_checks.py` is self-contained.

Also run:
- read-only `grep`/`sed` on `R/` documents, reviews and SCIP logs;
- exact-fraction checks of the gap cells against `gap-values.json`;
- a short inline count of the funnel steps (1257, 596, 360) on copied data.

No solver, certificate or research script was run; no project-wide check was
run; CI was not inspected.
