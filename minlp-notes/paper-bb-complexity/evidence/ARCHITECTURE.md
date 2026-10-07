# Architecture: the certificate complexity of branch-and-bound

Date: 2026-10-05. Author: lead writing architect (Opus). This is a planning
record for the manuscript in `paper-bb-complexity/`. It is not submission
text. It fixes the scope, the unifying mechanism, the theorem spine, the
proof dependencies, the notation, the chapter allocation and the submission
framing. [COVERAGE-INITIAL.md](COVERAGE-INITIAL.md) maps every claim to its
source, proof status, reviews and planned location.

No literature research was done for this file. Literature statements below
are the source notes' own records and are listed in Section 10 as requests
for Luna. No experiment was rerun. Novelty statements are provisional until
Luna's audit returns.

## 0. Inputs read

Primary notes (read in full or at the level of every numbered statement and
its proof sketch; revision records read in full):

| Abbrev. | File |
|---|---|
| CN | `research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md` |
| FE | `research-20260928b/bb-complexity/spatial-face-exact/face-exact-node-complexity.md` |
| CP | `research-20260928b/bb-complexity/cutoff-propagation/cutoff-propagation.md` |
| CB | `research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md` |
| ND | `research-20260928b/bb-complexity/branching-competitiveness/n-dimensional.md` |
| SO | `research-20260928b/bb-complexity/branching-competitiveness/separable-omega.md` |
| RB | `research-20260928b/bb-complexity/robust-branching-points/robust-branching.md` |
| IC | `research-20260928b/bb-complexity/integer-core/relaxation-intrinsic-bounds.md` |
| SR | `research-20260928b/bb-complexity/sparse-regression/phase-transition.md` |
| SR2 | `research-20260928b/bb-complexity/sparse-regression/stronger-relaxations/thresholds.md` (summary only) |
| BL | `research-20260928b/bb-complexity/binary-least-squares/certification-thresholds.md` |
| SV | `research-20260928b/bb-complexity/solver-validation/scip-node-exponents.md` |
| MB | `research-20260928b/bb-complexity/minlplib-branching/branching-point-study.md` |
| RL | `research-20260929/rlct/rlct-node-complexity.md` |
| ST | `research-20260929/theory-face-exact/face-exact-exponential.md` (the single-tree note) |
| DC | `research-20260929/theory-decomposition/decomposition-certificates.md` |
| EA, AM, CU | `research-20260929/theory-decomposition/{extension-adaptive,adaptive-matching,covering-upper-half}.md` (statements only) |
| RC, RLB | `research-20260929/theory-robust-lb/{robust-chains,robust-lower-bound}.md` (statements only) |
| KC | `research-20260929/theory-consistency/consistency-relaxations.md` (opening only) |
| SS | `research-20260929/computation/scaling-study.md` (summary) |
| LA | `research-20260929/literature/decomposition-bb-prior.md` (verdicts and positioning) |

Also read: both `SYNTHESIS.md` files, both `closing-research-results.md`
files, `research-20260928b/bb-complexity/PROGRAM.md`, closing audits A and B,
the PWE verification report, the integer-core and competitive rechecks, the
Lean statement review of topic 33, and the overlap papers' READMEs and
abstracts (`paper-relaxation-limits`, `paper-decomposition-aware`,
`paper-open-minlplib`, `paper-adaptive-obbt`,
`paper-sparse-indicator-quadratics`).

**Path discrepancy.** The brief lists
`research-20260929/theory-single-tree/`. That directory does not exist. The
single-tree lower bound is in `research-20260929/theory-face-exact/` (ST),
with numerical support in `theory-decomposition/single_tree_lb.py`. This
file treats ST as the intended source. Root should confirm (Section 13).

## 1. Key decisions

1. **One object, one question.** The paper is about the *certificate
   complexity* `N_eps`: the least number of pieces on which the node
   relaxation reaches the target `f* - eps`. Every lower bound in the
   repository has the same three steps: a run yields a valid family; validity
   forces near-optimal points close to the zero set of the relaxation gap
   inside their piece; a covering, integral or counting argument converts
   this into a size bound. Every upper bound is a bisection localization
   argument. The paper is organized around this mechanism, not around the
   chronology of the notes.
2. **Main message.** Up to explicit factors, the relaxation and the
   geometry of near-optimal sets determine tree size; branching rules move
   it by constant or logarithmic factors in the vertex-vanishing case, and
   by polynomial factors only where the gap vanishes on faces. Upper bounds
   need only the upper (convergence-order) gap. Lower bounds are decided by
   where the gap vanishes. This is the precise sense in which convergence
   order does not determine node counts.
3. **Scope (Section 3).** Included: spatial covering law, box-face and
   stratified integral laws, singular minima (RLCT) and relaxation order,
   constraint-gap schemes, face-exact relaxations, the single-tree
   dimension bound, a decomposition contrast, objective-cutoff propagation,
   branching rules, the class number, and random sparse regression and
   binary least squares. Excluded: stronger lifted relaxations for sparse
   regression (SR2), adaptive decomposition algorithms (EA, AM), the covering
   upper half (CU), consistency relaxations (KC), split-robust lower bounds
   (RLB, RC), calibrations and bang-bang work, open-instance certificates
   (covered by `paper-open-minlplib`), the treewidth census, and the side
   results on GCS, split separation and intersection cuts.
4. **Two characterizations, not one.** The general constrained statement
   is the covering law within `C log(1/eps)` (CN Theorem 6.3). The box
   statement for `C^{1,1}` objectives is the face-integral law with
   `eps`-independent constants (RL Corollary 3.4). The paper presents both
   and says exactly where the log factor is real (bisection at sharp
   non-vertex minimizers, which needs nonsmoothness or constraints) and
   where it is not.
5. **No characterization is claimed for face-exact relaxations.** Two
   conjectured characterizations were refuted (FE Conjectures 7.1, 7.1').
   The face-exact chapter gives lower-bound tools, structure theorems,
   sharpness on examples and the failure of the tools on a curved
   non-transversal surface, and leaves the characterization open.
6. **The exponential single-tree bound is stated as a property of the
   relaxation class.** ST Theorem 1 holds for a strictly convex QP written
   with separate bilinear terms, and PSD-minor cuts escape it. The
   decomposition contrast fixes the same termwise relaxations on both sides
   and states its dependence on the factorization (DC Section 4.1,
   Observation 4.2).
7. **Proofs.** Core statements get complete proofs in the paper (main text
   or appendix). Sketch-level items of the notes are excluded from theorem
   statements and listed as open. Results that rest on external inputs
   (Lin 2017 asymptotics, Hu–Lu, Jaldén–Martin–Ottersten, Gläser–Pfetsch,
   Aoyagi–Watanabe via Drton–Plummer, Siegel's mean value theorem, Federer's
   reach theorem) state the input explicitly; conditional statements stay
   conditional.
8. **Length.** About 95 pages of main text and 65 pages of appendices. The
   manuscript is modular: Part V (random instances) and Section 9
   (decomposition contrast) can be detached if an editor asks for a split,
   without breaking the spine.
9. **Evidence.** All experiments are archived evidence, not reruns.
   Floating-point toy counts are labelled as illustrations; exact-arithmetic
   checks are labelled as such; the two MINLPLib studies and the SCIP
   exponent study are labelled empirical, one solver version.

## 2. Thesis and unifying mechanism

### 2.1 The object

A **node relaxation scheme** assigns to every box `B ⊆ X0` a relaxed set
`R_B ⊇ F ∩ B` and a function `f_B ≤ f` on `F ∩ B`, with bound
`LB(B) = inf_{R_B} f_B`. A **certificate at tolerance `eps`** is a finite
family of boxes with disjoint interiors covering `X0` such that every member
has `LB ≥ f* - eps`. `N_eps` is the least size of a certificate. Integer
branching uses convex pieces instead of boxes and the projected relaxation
bound `r(Q)` (IC Definitions 1.1–1.2). Propagation adds a second
certification rule (CP Lemma 2.1). Decomposition certificates replace one
box family by a family per bag with cell minorants on separators (DC
Definition 1.2).

### 2.2 The three-step lower-bound template

1. **Runs to certificates.** Every terminated run, with any branching rule,
   split points, node order, valid incumbents, inherited bounds and
   reductions that use only the relaxation or remove only infeasible
   points, yields a family of leaves and frame pieces (at most `2n` per
   reduction round) on which a pointwise validity condition holds (CN
   Lemma 2.1; FE Lemma 1.2; ST Lemma 1.2; CP Lemma 2.1; IC Lemma 1.3 and
   Theorem 1.8). Its size is at most leaves plus `2n` per reduction round.
2. **Validity localizes near-optimal points.** For vertex-vanishing gaps,
   `m(y) + eps ≥ alpha q_C(y)` puts every point of `E(eta)` within
   `sqrt((eps + eta)/alpha)` of a vertex of its box. For termwise McCormick
   the fixed coordinates near `y` must form a vertex cover of the
   interaction graph. For cutoff propagation under a no-dominant-term
   condition, removed points lie near a vertex (CND) or a face (ND1). For
   integer branching, the points of one leaf form an admissible class.
3. **Counting.** Covering numbers (CN Theorem 4.6), arcsine integrals
   (CN Theorem 3.1; RL Theorem 3.1; CN Lemma 4.1 on strata), transversal
   volume (FE Theorems 3.6, 3.8), centre-volume products (ST Lemma 2.1),
   class numbers (IC Theorem 1.6).

### 2.3 The upper-bound template

A non-pruned cell of uniform bisection at level `j` contains a relaxed
point with `m < Lambda s_j^2 - eps`; with an error bound and a Lipschitz
objective this gives a feasible point of `E(Lambda s_j^2)` within one cell
(CN Lemma 6.1). Counting such cells gives the covering upper bound (CN
Theorem 6.3), the face integrals (RL Theorem 3.3, after projecting to
faces with Lemma 3.2), and the stratified integrals (CN Theorem 6.6). These
use only the **upper** gap: second-order pointwise convergence, or its
vertex-vanishing form `(U^q)`. McCormick satisfies `(U^q)` (CN Lemma 1.1;
FE Lemma 2.5), so the upper bounds hold for it; the lower bounds do not.

### 2.4 One sentence per part

- Vertex-vanishing gaps: certificate size is a multiscale covering number of
  the near-optimal sets (within `log(1/eps)` in general, within constants on
  boxes for `C^{1,1}` objectives); the exponent is a singularity invariant.
- Face-exact gaps: certificate size depends on how near-optimal sets meet the
  vertex-cover faces; at fixed tolerance it can be exponential in `n` at a
  unique nondegenerate minimizer on a path, while decomposition certificates
  with the same relaxations stay polynomial.
- Propagation: a second node bound that depends on the expression graph; it
  removes the cost exactly when the representation is one-sided.
- Branching rules: within the bounds above, a node-local rule can be
  constant-competitive in one dimension, every node-local rule loses an
  exponential factor in `n` on separable instances, and practical safeguards
  lose logarithmic or polynomial factors in the models, while on MINLPLib
  they are neutral or protective.
- Integer branching: the class number is the exact semantic tree size; on
  random closest-vector problems it is exponential for every basis, and on
  random sparse regression and binary least squares it separates root
  exactness, linear trees and exponential certificates at explicit
  thresholds.

## 3. Scope

### 3.1 Included in the main text (statements, mechanisms, short proofs)

| Topic | Sources | Role |
|---|---|---|
| Model, gap hypotheses, runs to certificates | CN 1–2; FE 1.2; ST 1.3; CP 2; IC 1.2 | foundation (Part I) |
| Covering law, running supremum, log factor, tightening | CN 4.3, 6, 6.1, 6.3, 8.3 | Theorem II |
| Box-face law for `C^{1,1}` objectives | RL 3 | Theorem III(a) |
| Stratified integral lower bound, key lemma, regular instances, Morse–Bott, symmetry | CN 3.1, 4, 7, 8.1–8.2 | Theorem IV |
| RLCT form, boundary counterexample, examples, singular learning example | RL 4–6 | Theorem III(b) |
| Relaxation order (first order, order `k`) | CN 8.4; RL 7 | Theorem III(c) |
| Constraint-gap schemes | CN 5 | Theorem IV(d) |
| Face-exact relaxations | FE 2–6 | Theorem V |
| Single-tree dimension bound and chordal escape | ST 2–3, 5.4, 9 | Theorem VI(a) |
| Decomposition contrast | DC 1, 2.6, 3.3–3.4 (statement), 4, 4.1 | Theorem VI(b)–(d) |
| Objective-cutoff propagation | CP 1–6 | Theorem VII |
| Branching rules | CB 1–5; ND 3; SO 6; FE 5.2–5.4; RB 2, 4, 5 | Theorem VIII |
| Class number and comparisons | IC 1–2, 5 | Theorem IX |
| Random CVP | IC 3 | Theorem IX(d) |
| Random sparse regression; binary least squares | SR 1–4; BL 1–6 | Theorem X |
| Computational evidence (archived) | CN 9; RL 5; SV; MB; RB 6; ST 7; CP 7; FE 8; SS | Section 14 |

### 3.2 Included in appendices only

- Geometric-measure tools behind CN Lemma 4.1, tube volumes for CN Theorem
  8.2(d), the integral upper bound under stratified regularity (CN Theorems
  6.6–6.7).
- RLCT analytic input (RL Lemmas 2.1–2.4), Newton-polyhedron examples.
- The McCormick certificate integral (FE Lemma 3.1, Theorem 3.2, Corollary
  3.3).
- The `log(1/eps)` single-tree factor with base 1.072 (ST Proposition 5.3),
  the per-factor envelope bound (ST Theorem 2) and per-factor alphaBB (ST
  Proposition 6.1; DC Corollary 2.1).
- The proof of DC Theorem 3.4.
- HC4 partial steps and the chain-minimum proof (CP Section 1, Lemma 2.1(b)).
- Exact instances for CB Theorem 3, Propositions 4 and 4'; SO Theorems C and
  C' with the computed values `G(2..6)`; ND Theorem N3; FE Propositions
  5.4–5.7 and Theorem 5.3; RB Theorem B, Propositions E and F.
- IC Lemma 1.7a, Theorem 1.8, Theorem 2.3, Section 3 proofs, one
  perspective gadget (IC Section 4.4).
- SR and BL proofs.
- Computational protocols and data provenance.

### 3.3 Excluded, with reasons

| Item | Reason |
|---|---|
| SR2 (stronger lifted relaxations keep the sparse thresholds) | about 15 further pages of delicate random-matrix arguments; a refinement of Part V, not part of the spine; best as a separate paper. The paper does not claim anything about lifted relaxations |
| EA, AM (adaptive decomposition algorithms, LS and GR) | algorithmic decomposition theory with long proofs and numerically vacuous constants; belongs with a decomposition paper. Section 9 states that its upper bound is an existence result centred at `x*` |
| CU (graded exact split, covering upper half) and KC (consistency relaxations) | concern gaps of decomposition relaxations, not tree size; would need new notation and about 15 pages |
| RLB, RC (split-robust lower bounds) | qualitative only (proved bases about 1.003 and 1.001–1.009); Section 9 uses only DC Observation 4.2 for split dependence |
| Calibrations, bang-bang and singular-arc work; open-instance certificates; census; coupling | different topics; open-instance closures are covered by `paper-open-minlplib` |
| Side results (GCS gap bounds, split separation, intersection cuts) | different topics |
| Sketch-level statements | not proved: CN Lemma 5.5 for nonlinear exact constraints, DC Proposition 2.6 beyond a child of the root, SO Theorem B for `n - 1` sharp coordinates, RL Conjecture 6.3 and Remark 4.1a corner sketch, CP Heuristic 3.8a, ST route to `theta^-n log(1/eps)` |
| Results known only from abstracts | ND's binary-space-partition bounds (Berman–DasGupta–Muthukrishnan; Hershberger–Suri–Tóth): drop unless Luna verifies; the self-contained bound `N_guill ≤ (2N_eps - 1)^n` suffices |

SO Theorem B (one arbitrary and one sharp coordinate, `omega ≤ 112 N_opt`)
and the Phase Lemma are proved in SO but excluded: they need the Phase
Lemma machinery (about 8 pages) for a special case, and the paper's
branching message does not depend on them. The open question about `omega`
is stated without them.

### 3.4 Overlap and attribution with companion manuscripts

| Companion | Overlap | Treatment |
|---|---|---|
| `paper-relaxation-limits` | defines region-oracle certificates and proves fixed-tolerance exponential region counts for fractional-cardinality quadratics and random cubic XOR | cite as companion for the general "covers bound every branching order" observation and for fixed-tolerance lower bounds; our results are `eps`-asymptotic and instance-dependent, plus the path-family bound of Section 8 |
| `paper-adaptive-obbt` | OBBT limits and stalling under a cutoff | cite where same-relaxation tightening is discussed (CN Corollary 8.1): our statement concerns tree size, theirs the operator |
| `paper-decomposition-aware` | tree-decomposition certificates by curvature-corrected grids, polynomial under growth | cite in Section 9 as a different decomposition method; do not claim the first decomposition-aware certified method; our Section 9 is a separation under fixed termwise relaxations |
| `paper-open-minlplib` | instance certificates where the relaxation, not branching, was the obstacle | one sentence in the discussion, as interpretation, citing the companion |
| `paper-sparse-indicator-quadratics` | indicator quadratics on tree supports | no theorem overlap; cite only if the perspective-relaxation discussion needs it |

Whether unpublished companions may be cited in the submission is a root
decision (Section 13). If not, the overlapping statements are attributed
to their primary literature only.

## 4. Main theorem spine

The introduction states ten headline results, each a pointer to chapter
theorems. Hypotheses below are the minimal ones the proofs use. Notation is
that of Section 7.

**Theorem I (runs yield certificates; Section 2).** For every terminated run
with axis-parallel splits, any node order, incumbents `UBD ≥ f*`, inherited
bounds, and rounds of (R-inf) and (R-rel) reductions, the leaves together
with at most `2n` frame pieces per round form an `alpha`-valid family under
`(G^pt_alpha)`; without (R-rel) rounds, `(G^LB_alpha)` suffices. The same
holds with pointwise McCormick validity for termwise relaxations, with (V)
or (Π) certification for hybrid runs with cutoff propagation, and with
admissible classes for convex-piece integer trees, where incumbent-based
removals add to the leaf count. Sources: CN Lemma 2.1; FE Lemma 1.2; ST
Lemma 1.2; CP Lemma 2.1; IC Lemma 1.3, Theorems 1.6, 1.8.

**Theorem II (covering law; Section 3).** Let `X0` be a cube. Under
`(G^LB_alpha)`, `(U_c)`, `(EB)` and `(Lip)`, for every `eps > 0`
`2^-n Phi_alpha(eps) ≤ N_eps ≤ |T_bis| ≤ C_0 + C_1 J_eps Phi_alpha(eps)`,
with `J_eps = O(log(1/eps))` and `C_0, C_1` independent of `eps`
(exponential in `n`). `Phi_alpha` is within `2^n` of the running supremum
over `eta ≥ eps` of a Munos-type profile; the supremum is necessary; the log
factor is attained by bisection at sharp non-vertex minimizers, while
`N_eps = O(1)` there. Same-relaxation tightening saves at most a factor
`O(log(1/eps))`. Under quadratic growth the exponent is half the
box-counting dimension of `X*`. Sources: CN Theorems 4.6, 6.2–6.4,
Remark 6.3a, Corollaries 4.7, 6.5, 8.1, Example 3.4, Proposition 6.8,
Remark 6.9.

**Theorem III (box faces, singularities and order; Sections 4–5).**
(a) If `X0` is a cube, `grad f` is Lipschitz on `X0`, and the scheme
satisfies `(G^LB_alpha)` and `(U^q_alpha')`, then
`N_eps ≍ |T_bis| ≍ max(1, max_F I_F(eps))` with constants independent of
`eps`, with no doubling condition and no log loss at optimal vertices.
(b) If `f` is real analytic near `X0`, then
`N_eps ≍ max_F eps^(lambda_F - d_F/2) (log 1/eps)^(theta_F - 1)` (with the
stated conventions at `lambda_F ≥ d_F/2`), where `(lambda_F, theta_F)` is
the real log canonical threshold of `m|_F`; for interior minimizers, or
when `m ≥ 0` on a neighbourhood of `X0`, the full-dimensional RLCT alone
decides, and the interior statement fails at boundary minimizers.
(c) With a gap of order `k`, the covering scale is `(eps + eta)^(1/k)`; the
volume law holds for `k ≤ 2`, and for `k > 2` the exponent is not a
function of the RLCT. First-order gaps give `Theta(eps^(-(n+p)/2))` at
Morse–Bott sets, the cluster effect as a lower bound for every tree.
Sources: RL Theorems 3.1, 3.3, 4.1, 7.1, Lemma 3.2, 3.3a, Corollaries 3.4,
4.2, Example 4.3, Propositions 6.1–6.2, 7.2–7.3; CN Theorem 8.2.

**Theorem IV (strata, regular instances and constraint gaps; Sections 4,
6).** (a) Stratified integral lower bound over every feasible `C^1` stratum
of positive reach, with an explicit constant and a multiplicity factor that
cannot be dropped (bounded curvature does not suffice). (b) Finitely many
nondegenerate KKT minimizers with active strata of dimension `d ≥ 1`:
`Theta(log(1/eps))` with lower prefactor `(alpha/M_L)^(d/2)`; a unique
vertex (`d = 0`) minimizer: `N_eps = O(1)` for all `eps ≥ 0`, bisection
`Theta(log(1/eps))` for generic positions. (c) Morse–Bott optimal manifold of
dimension `p`: `Theta(eps^(-p/2))`; continuous symmetries acting on `X*`
cost `eps^(-1/2)` each, and exact symmetry-breaking constraints restore the
lower exponent. (d) Constraint-gap schemes: tube dichotomy, infeasible-side
covering bound, Lagrangian transfer under outward descent, and
`Omega(log(1/eps))` at KKT points with a relaxed active constraint, even
with the objective relaxed exactly. Sources: CN Lemma 4.1, Proposition 4.4,
Theorems 4.5, 5.2, 5.4, 5.7, 7.1, 7.2, Example 5.3, Section 8.1.

**Theorem V (face-exact relaxations; Section 7).** For termwise McCormick
(and joint multilinear envelopes where stated): the gap vanishes exactly on
faces whose fixed coordinates form a vertex cover of the interaction graph;
transversal `p`-dimensional near-optimal strata force `Omega(eps^(-p/2))`
leaves (sharp constant on the tilted stratum); a smooth interior minimizer
with an active bilinear term costs `Omega(log(1/eps))` and has no exact
finite certificate; in 2D a full aligned optimal segment has a 2-box
certificate for every convex `g`; the exponent of a near-optimal cube is
the fractional vertex cover number; McCormick and alphaBB can have the same
convergence order and prefactor while `N_eps` is 2 versus
`Theta(eps^(-1/2))`; and on a curved non-transversal surface every one of
these lower-bound tools gives `O(eps^(-3/4))` while
`N_eps ≥ 0.307/(eps(1 + ln(1/(2 eps))))`, so they do not characterize
`N_eps`. Sources: FE Lemmas 2.1–2.5, Theorems 3.4, 3.6, 3.8, 4.2, 4.4, 4.5,
6.1, Corollaries 3.5, 3.11, Propositions 3.10, 3.13, 3.14, 4.6, 4.7,
Example 3.12(b).

**Theorem VI (dimension and decomposition; Sections 8–9).** (a) On the path
family `sum g_i(x_i) + sum b_i x_i x_{i+1}` (`|b_i| = b`, `g_i'' ≤ D` near
`x*`), every certified cover for every relaxation whose gap is at least the
termwise McCormick gap has at least `(1 + 1/S)^n exp(-lambda_S (1 + eps/(b r^2)))`
members when `D/(2b) ≤ 1.99`, `S = sqrt(1 + D/(2b))`; for the explicit family
this is `≥ 0.57 (5/3)^n` at `eps ≤ 1e-4`, at a unique nondegenerate interior
minimizer and also for a strictly convex QP; dyadic refinement uses at most
`C^n O(log(n/eps))` leaves; clique-wise PSD cuts are exact for the convex
member. (b) Decomposition certificates with affine cell minorants exist with
size `O(|T| C^(tw+1) log(|T|/eps))` under quadratic growth, Lipschitz factor
gradients and `(U^q)`, as an existence result centred at `x*`. (c) Constant
child minorants need `Omega(eps^(-1/2))` cells at a separator with nonzero
optimal multiplier (child of the root, one-dimensional separator). (d) With
the same termwise relaxations the ratio of the single-tree lower bound to
the decomposition upper bound is at least `3e-10 (2e/pi)^(n/2)/sqrt(n)` for
every `n ≥ 3`, `eps ≤ 1e-4` (alphaBB terms), and `c (5/3)^n/(n log(n/eps))`
for termwise McCormick; no lower bound holds uniformly over functional
splits for relaxations exact at factor minima. Sources: ST Lemma 2.1,
Lemma 3.1, Theorem 1, Corollary 1.3, Proposition 5.5, Lemma 9.1; DC Lemmas
1.3–1.5, Proposition 2.6, Theorems 3.4, 4.1, Observation 4.2.

**Theorem VII (cutoff propagation; Section 10).** Fixed-point interval
propagation of `f ≤ c` on a factorable DAG `D` is the node bound
`pi_D(C) = min{c : Z*(C, c) ≠ ∅}`, with `F_lo(C) ≤ pi_D(C) ≤ min_C f`; every
schedule removes at most what the fixed point removes. Hybrid runs yield
families certified pointwise by (V) or (Π), with propagation phases merged
into one frame. No lower bound holds for every representation. For flat
sums of univariate terms the fixed point is characterized exactly;
one-sided representations are exact and give `eps`-independent node counts
for idealized propagation (the cost can move into `Theta(eps^(-1/2))`
rounds); under the coordinatewise no-dominant-term condition every
(V)-based lower bound survives with `alpha_eff = min(alpha, D0/(2 n s0))`,
and under the weaker cube condition the `log(1/eps)` and transversal-curve
bounds survive. The same `f` with the same relaxation needs 1 node or
`Omega(eps^(-1/2))` nodes depending only on the DAG. Sources: CP Lemmas 1.1,
1.2, 2.1, 4.1, 4.4, Propositions 1.4, 2.3, 3.6, 3.9, 3.10, Theorems 2.2,
3.1, 3.8, 5.1, 5.2, 5.4, 5.5, Corollaries 3.3, 4.2.

**Theorem VIII (branching rules; Section 11).** In the exact-gap model
`f_B = f - alpha q_B`: (a) in 1D, splitting at the relaxation minimizer uses
at most `8 N_eps - 9` nodes (ratio below 4), and at most 5 when `N_eps = 2`;
every rule that sees the relaxation solution and the germ of `f` there has
ratio at least 5/3 on piecewise-quadratic classes; every oblivious rule has
ratio at least `c_n log(1/eps)` in every dimension; every fixed clamped
convex combination other than the pure minimizer rule, and SCIP 10's
width-dependent default, need order `log(1/eps)` nodes on explicit
instances with `N_eps = 2`. (b) For `n ≥ 2`, every deterministic node-local
rule with this information has ratio at least `(2G(n)+1)/3` on separable
convex instances with `N_eps = 2` (`7/3, 11/3, 19/3, 31/3, 17` for
`n = 2..6`), at least of order `2^(n+2)/(3n)` in general; splitting every
coordinate at the minimizer is not competitive. (c) For termwise McCormick
on the kink family: the unclamped relaxation point and incumbent branching
take 3 nodes; a clamp `beta` misses the optimal face on an uncountable null
Cantor set of kink positions (at `a = 1/6`, `beta = 1/5`: at least
`0.0745 eps^(-1/2)` nodes against `N_eps = 2`); a fixed midpoint weight
misses it for all but countably many positions; every oblivious rule loses a
factor of order `eps^(-1/2)` on average. (d) Every `theta0`-safe rule needs
`J + 1` splits on a kink at relative distance `a < theta0` from a bound,
and the recentring clamp attains this exactly. Sources: CB Theorems 1–3,
Propositions 2, 4, 4'; SO Theorems C, C', Proposition 6.2; ND Theorem N3;
FE Theorem 5.3, Propositions 5.4–5.7; RB Theorem A, Propositions C, D.

**Theorem IX (integer branching; Section 12).** The class number
`kappa_eps(P)` bounds the leaves of every `P`-covering convex-piece
`eps`-certificate (variable, split, multiway, SOS, semantic), equals the
minimum for arbitrary convex pieces (multiway or binary hemispace trees), is
unchanged by valid cuts in the integer variables and by feasibility-based
reductions, and with incumbent-based removals satisfies
`kappa ≤ #leaves + #certified removals`. It is at most `m + 1` for pure
integer programs with `m` constraints; split trees can be `2^(L^Omega(1))`
while `kappa ≤ L`; a quadratic Jeroslow instance has `kappa = 2` and needs
`C(n+1, (n+1)/2)` leaves under variable branching; for a Haar-random lattice
and uniform target, w.h.p. `kappa ≥ 2^((0.2925 - o(1)) n)` for every basis.
Sources: IC Theorems 1.6–1.8, 2.2, 2.3, 3.4, 3.5, Propositions 2.1, 2.4,
3.6, Example 2.1a.

**Theorem X (random instances; Section 13).** Sparse regression with the
perspective relaxation (Gaussian design, asymptotic regime stated in full):
root exactness at `tau^2 = 2 log p`, hence `N ≈ 2k log p` samples; every
variable-branching tree is linear-size above `tau^2 = 2 log(p nu/N)`, hence
`N ≈ 2k log(p/sqrt N)`, strictly below root exactness for `k = p^gamma`;
pure noise and low total SNR force conflict cliques `C(p,k)^(c')`. Binary
least squares with the box relaxation: root exactness probability at most
`((1 + 2(1 + 4 rho)^(-beta/2))/2)^n` at every SNR; linear trees iff
`rho > (1 + o(1)) n/(4(2 beta - 1))` (for `beta = 1` given the Hu–Lu input);
between `log n` and `n` every convex-piece certificate has
`exp(Theta((n/rho) log rho))` leaves; the SDP and the eigenvalue-shift
relaxation are exact at `rho = Theta(log n)` for `beta > 1`. Sources: SR
Theorems 3.1, 3.2, 4.3, 4.4, Corollaries 3.3, 3.4; BL Proposition 1.1,
Theorems 1.2, 2.2, 3.1, 4.1, 4.3, 6.2, Proposition 6.3.

### 4.1 Rate table for the introduction

| Structure near `X*` | vertex-vanishing second order | termwise McCormick | first order |
|---|---|---|---|
| finitely many nondegenerate interior minimizers | `Theta(log 1/eps)` | `Omega(log 1/eps)` with an active bilinear term; `O(log 1/eps)` for `C^{1,1}` `f` | `Theta(eps^(-n/2))` |
| unique sharp (vertex) minimizer | `O(1)` for all `eps ≥ 0` | `O(1)` on the tested instance only | `O(1)` |
| `p`-dimensional Morse–Bott set | `Theta(eps^(-p/2))` | `Theta(eps^(-p/2))` if transversal; 2 for a full aligned segment in 2D | `Theta(eps^(-(n+p)/2))` |
| analytic, interior minimizers | `eps^(lambda - n/2) (log 1/eps)^(theta - 1)` | open | `eps^(lambda - n)` up to logs |
| minimizers on the boundary | face-wise maximum of the above | open | |

## 5. Proof dependencies and imported results

### 5.1 Dependency graph (core spine)

```
Model (CN 1) ── Run lemma (CN 2.1) ──┬─ Covering LB (CN 4.6) ──┐
                                     │                          ├─ Covering law (CN 6.3, Rem 6.3a, Cor 6.5)
Localization (CN 6.1; needs U_c, EB, Lip) ─ Bisection UB (CN 6.2, 6.4) ┘
Arcsine bound (CN 3.1) ─ face LB (RL 3.1) ─┐
Projection to faces (RL 3.2) ─ bisection UB without QD (RL 3.3) ─ vertex lemma (RL 3.3a) ─┴─ Box-face law (RL 3.4)
Box-face law + Lin asymptotics (RL 2.1, imported) + RL 2.2 ─ RLCT form (RL 4.1, 4.2)
Key lemma (CN 4.1: Cauchy–Binet, area formula, Federer reach) ─ stratified LB (CN 4.5) ─ KKT, Morse–Bott (CN 7.1, 7.2)
Tube dichotomy (CN 5.1) ─ CN 5.2, 5.4 ─ Lemma 5.5 (LICQ, polyhedral P_ex) ─ CN 5.7
McCormick gap (FE 2.1) ─ gap graph (2.1) ─ FE 3.6, 3.8 (needs Lemma 3.9), 3.10/3.11; chord bound (FE 2.4) ─ FE 3.4 ─ Cor 3.5
Lemma 4.1 (convex analysis) ─ FE 4.2 ─ FE 4.4, 4.5; FE 6.1 uses 4.4, CN 3.2 (=4.6), FE 5.1(b)
Centre-volume (ST 2.1) + Lemma 3.1 ─ ST Theorem 1; ST 5.5 (UB); chordal split (ST 9.1, Griewank–Toint)
DC 1.3 (validity) ─ 1.4, 1.5 (Lagrangian unfolding); DC 3.1, 3.2 ─ DC 3.4; DC 4.1 = DC Cor 2.1 + ST Thm 1 + DC 3.4 (+ bag lemma 2.2 for part c)
CP 1.1, 1.2 ─ Prop 1.4 ─ Lemma 2.1 (chain minimum) ─ Thm 2.2; Thm 3.1 ─ Cor 3.3, Prop 3.6 ─ Thm 3.8; Lemma 4.1 ─ 4.4 ─ Thm 5.1 ─ Thm 5.2 (uses CN 4.6, 3.1); Thm 5.4, 5.5
CB Lemmas 1, 2 ─ Thm 1; CB Thm 2 (adversary chain); CB Thm 3 (exact instances); SO Lemma 6.1 ─ Thm C ─ Thm C' (Yao, Pareto DP values)
IC Lemma 1.3 ─ Thm 1.6; Lemma 1.7a ─ Thm 1.7; Thm 1.8; Lemma 1.5 ─ CVP Thms 3.4, 3.5 (Siegel mean value)
IC path lemma (Sec. 5) ─ C1 ─ SR Thm 3.2, BL Thm 3.1; IC Thm 1.6 ─ SR Thm 4.3/4.4, BL Thm 4.3 (entropy Lemma 4.2)
```

### 5.2 Imported results (cite; do not re-prove)

| Input | Used in | Note |
|---|---|---|
| Federer (1959), Theorem 4.18(2) and 4.8(12) | CN Lemma 4.2 remark, Theorem 8.2(d) | reach and two-point inequality |
| Niyogi–Smale–Weinberger (2008), Lemma 5.3 | CN Theorem 7.2 | volume of small balls on manifolds |
| Weyl (1939); Gray, *Tubes* | CN Theorem 8.2(d) | tube volumes |
| Area formula with multiplicity (Federer 3.2.20; Evans–Gariepy) | CN Lemma 4.1 | |
| Robinson (1976); Bonnans–Shapiro (2000) Thm 2.87 | (EB) from MFCQ | |
| SOSC implies local quadratic growth (classical; e.g. Bonnans–Shapiro) | CN Theorem 7.1 | CN cites an internal repository note; replace by the classical source |
| Lin (2017) Cor. 2.6, Thm 2.10, Props 2.5, 3.2–3.7, Thm 1.3, Props 4.3, 4.5, 4.12; Karamata | RL Lemmas 2.1, 2.3 | box faces as compact semianalytic sets; the orthant extension at boundary zeros is proved in RL |
| Aoyagi–Watanabe (2005) via Drton–Plummer (2017) | RL Proposition 6.1 | the learning coefficient formula is not re-derived; rows `0 < r < H` not claimed |
| Łojasiewicz inequality | RL Proposition 7.3(a) | |
| Minkowski–Radon centroid theorem; Dirichlet integral | FE Theorem 3.6, Lemma 3.1 | |
| McCormick (1976); Al-Khayyal–Falk (1983) | FE Lemma 2.1 | envelope of a bilinear term |
| Rockafellar, *Convex Analysis* (faces of epigraphs; Theorem 11.3) | FE Lemma 4.1; IC Lemma 1.7a | |
| Griewank–Toint (1984) Thm 4; Agler et al. (1988); Vandenberghe–Andersen (2015) | ST Lemma 9.1, Consequences A–B | chordal PSD decomposition |
| Vorob'ev (1962); Lasserre (2006) | DC Observation 4.2 (measure form) | |
| Belotti–Cafieri–Lee–Liberti (2012) | CP Lemma 1.1 | FBBT greatest fixed point; not claimed new |
| Moore's single-use theorem | CP Corollary 4.2 | |
| Yao's principle | SO Theorem C' | |
| Kakutani/Stone hemispaces | IC Lemma 1.7a (proved in IC) | |
| Gläser–Pfetsch lower bound | IC Theorem 2.3 | exponent conventions to verify |
| Jeroslow instance | IC Proposition 2.4 | |
| Reis–Rothvoss flatness | IC Proposition 2.5 | |
| Siegel (1945) mean value theorem; Kabatiansky–Levenshtein | IC Theorems 3.4–3.5, Proposition 3.6 | |
| Gaussian concentration, Bai–Yin | SR Section 3.2; BL Sections 0.4, 6 | |
| Gilbert–Varshamov | SR Section 4 | |
| Hug–Schneider; McCoy–Tropp; Godland–Kabluchko–Thäle | BL Section 1.2 | BL gives a self-contained proof of the extension it uses |
| Hansen–Hassibi–Dimakis–Xu; Hassibi et al. | BL Theorem 2.2 (`beta = 1` achievability) | |
| Hu–Lu (2020) | BL Theorem 3.1 (`beta = 1`), Section 1 | statements depending on it stay conditional |
| Jaldén–Martin–Ottersten (2003) | BL Theorem 6.2 | SDP tightness condition |
| Papailiopoulos (2026) | BL interpretation (polynomial search at `rho = c log n`) | must be verified; otherwise drop the search comparison |

### 5.3 Results the paper must prove in full (core)

Main text or appendix, complete proofs: Theorem I (all variants), CN 4.6,
6.1–6.4, Remark 6.3a, Proposition 6.8, Corollaries 6.5, 8.1; RL 3.1–3.4,
4.1–4.2 given Lemma 2.1; CN 3.1, 4.1–4.5, 7.1–7.2, 8.2; CN 5.1–5.4, 5.7 with
Lemma 5.5 (polyhedral `P_ex` only); FE 2.1–2.5, 3.4–3.11, 3.13–3.14,
4.2–4.7, 5.1–5.7, 6.1; ST 2.1, 3.1, Theorem 1, 5.5, 9.1; DC 1.3–1.5, 2.6,
3.4, 4.1, 4.2; CP 1.1–1.4, 2.1–2.3, 3.1, 3.3, 3.5–3.10, 4.1–4.4, 5.1–5.5;
CB 1–3, Propositions 2, 4, 4'; SO C, C'; FE 5.3–5.7; RB A, C, D; IC 1.3–1.8,
2.1–2.5, 3.4–3.6, 5; SR 3.1–3.4, 4.3–4.4; BL 1.1–1.3, 2.2, 3.1, 4.1–4.3,
6.2–6.3.

## 6. Critical findings

These are the places where the paper must not simply transcribe the notes.
Each finding names the required treatment. Other agents are auditing the
mathematics in parallel; items marked **audit** need their confirmation.

### 6.1 Statement-level corrections and scope limits already in the notes, which the paper must keep

1. **Counting with tightening.** Lower bounds for runs count leaves plus `2n`
   frame pieces per (R-rel) round, not leaves alone (CN Lemma 2.1(d)). Node
   counts follow only with a bound on rounds per node.
2. **Exponent equals half the box-counting dimension only under (QG).**
   Without quadratic growth the cusp `(x^2 - y^3)^2` has exponent `7/12`
   on a curve (RL Section 5), and finite optimal sets can have positive
   exponent (quartic growth). State Corollary 6.5 with (QG) and refer to
   Theorem III for the general exponent.
3. **The interior RLCT statement is false at boundary minimizers** (RL
   Example 4.3: predicted `eps^(-1/4)`, true `eps^(-3/4)`). Only the
   face-wise form is a theorem.
4. **Log factor.** The log in the covering law is necessary for bisection
   only at sharp minimizers that are not vertices of `X0`, which requires
   nonsmooth `f` or constraints (CN Example 3.4; RL Corollary 3.4 and the
   remark after it). It is never claimed necessary for `N_eps`.
5. **Face-exact characterization.** FE Conjectures 7.1 and 7.1' are false
   (Example 3.12(b), Proposition 3.14). The paper states Question 7.1'' as
   open and claims no characterization.
6. **Clamp scope.** RB Theorem A(ii): the McCormick bound with `K'` holds only
   at the two alternating points; at run-length-2 points the bound is
   `T ≥ 2K' - 1` (closing audit A).
7. **Theorem C' needs node-locality and corner information.** The I1 model
   is extended by the germ of `f` near the box corners; rules with memory
   across nodes (pseudocosts) are not covered. State this in the theorem.
8. **CB Theorem 3 concerns non-analytic classes.** For analytic `f` the germ
   determines `f`, and I1 collapses to full information.
9. **Single-tree bound is about relaxations.** ST Theorem 1 holds for the
   convex member `kappa = 0`; SCIP's PSD-minor cuts escape it; ST Theorem 2
   depends on the factorization (balanced split removes it near `x*`).
10. **Decomposition upper bound is an existence result centred at `x*`.**
    `c_g` is global (a second local minimizer at `f* + delta` and distance
    `D` makes the base `(C M_a D^2/delta)^(tw+1)`); constants are
    numerically vacuous (`theta = 2^-10` from (T2), crossovers at `n = 29`
    against computed certificates and `n = 49` proven against proven).
11. **DC Proposition 2.6** is proved for a child of the root with a
    one-dimensional separator only.
12. **CP Theorem 3.8 is idealized.** It assumes that propagation decides
    emptiness of `Z*`, which may take infinitely many rounds. Heuristic 3.8a
    and Conjecture 3.11 are not results.
13. **Random-instance theorems are asymptotic.** SR needs
    `log^6 p ≤ N ≤ p` and more (implying `p ≥ e^17`); every SR experiment
    lies outside the regime. The SR hard-side constant satisfies
    `c' < 3 - 2 sqrt 2 ≈ 0.17` (closing audit B corrected an earlier 0.11).
    BL's class-number constant (`c_1 = 1.8e-5`, range `rho ≤ 1.4e-4 n`) is
    vacuous below `n ≈ 1.7e7`.
14. **BL Theorem 4.1** needs the hockey-stick count of closing audit B for the
    logarithmic form at `rho = Theta(n)`; the note applied it. Use the
    corrected count.
15. **Conditional inputs.** BL Theorem 3.1 for `beta = 1` depends on Hu–Lu;
    BL's "certification superpolynomially harder than search" depends on the
    Papailiopoulos citation. Both stay conditional until Luna verifies them.

### 6.2 Weak or fragile points that need repair or rewording in the paper

1. **ST Lemma 3.1 threshold.** `S_max ≈ 1.72932` and `rho_max ≈ 1.99055`
   are computed numerically. State the theorem for `rho ≤ 1.99` and prove
   `F(S) = (1+S)/(2S^2) - log(1 + 1/S) ≥ 0` on `[1, sqrt(2.99)]` rigorously
   (monotonicity of `F` is proved in ST; one certified evaluation at
   `sqrt(2.99)` suffices). **Proof task (Sol).**
2. **ST Theorem 2 base 1.205** comes from a floating-point one-dimensional
   maximization. Either certify it (interval arithmetic on a compact
   interval) or state a weaker rational base with a symbolic proof. It is
   appendix material; the main text cites only its qualitative content.
   **Proof task (Sol)**, low priority.
3. **CN Theorem 7.1** cites the repository's cluster-free note for quadratic
   growth from SOSC. Replace by the classical result; keep the description
   independence remark (any `C^2` description of `F` near `z*`).
4. **CN Theorem 6.3 needs a cube.** The dyadic refinement is defined on a
   cube. For general boxes, either rescale (which changes the gap constants
   anisotropically; the anisotropic arcsine form is in CN Theorem 3.1's
   remarks) or state the theorem for cubes. Recommendation: cubes in the
   theorem, a remark for boxes.
5. **Face-exact Theorem 5.1(a) is subsumed.** For `C^{1,1}` objectives, RL
   Theorem 3.3 needs only `(U^q_alpha')`, which McCormick satisfies (FE Lemma
   2.5), and no (QD). Use RL Theorem 3.3 for the McCormick upper bounds
   with smooth `f`, and FE Theorem 5.1(b) for sharp strata of nonsmooth `f`.
   This simplifies the face-exact chapter and makes the "upper bounds need
   only the upper gap" message exact.
6. **CN Theorems 6.6–6.7** (integral upper bound under stratified
   regularity) are long and largely superseded on boxes by RL Corollary 3.4.
   Keep them in an appendix for constrained strata; Morse–Bott upper bounds
   come from CN Theorem 7.2 directly.
7. **SO Theorem C' constants.** Use the analytic bound
   `max_i N_i ≥ (2^(n+1) - n - 3)/(n - 1)` (closing audit A sharpening)
   for general `n`, and the computed exact `G(n)` for `n ≤ 6` as a
   computer-assisted table (Pareto DP; `G(6) = 25` rests on the audit's
   computation; the author's inline run did not finish). The asymptotic
   order `2^(n+2)/(3n)` is a lower-bound statement.
8. **ND guillotine statements** use binary-space-partition results known
   only from abstracts. Keep only the self-contained bounds unless Luna
   verifies the sources.
9. **CP literature claim about Schichl–Markót–Neumaier.** The note says the
   order-1 overestimation statement is "false for one-sided
   representations". The quotation came through a delegated reading of a
   2014 preprint. Phrase as "the statement ... holds in node-count form for
   flat sums with first-order loss (Theorems ...) and fails for one-sided
   representations (Corollary ...)", and only after Luna verifies the quote
   and the journal version.
10. **PWE Theorem 2.** SR Remark 3.5 shows that Theorem 2 of
    Pilanci–Wainwright–El Ghaoui (Math. Program. 151, 2015) fails as stated
    under per-entry noise, by a four-step argument that uses their own
    Corollary 2. The argument is short and checkable, and two independent
    verifications support it. In the paper: a remark in Section 13 with the
    self-contained argument, written factually, crediting what survives
    (their Corollary 2, the algorithms, the total-energy reading). It is not
    in the abstract. Luna must verify the printed statement, page numbers
    and erratum status. Whether to contact the authors before submission is
    a user decision (Section 13).
11. **RL Proposition 6.1** depends on a recalled formula checked against
    Drton–Plummer's Table 1. Present as "with `lambda` the Aoyagi–Watanabe
    learning coefficient" and cite; do not tabulate rows not covered.
12. **Not rechecked by the notes' own review chains**: DC Section 8.1 fixes
    (base rounding to `(2e/pi)^(n/2)`, `x̂ ∈ X0`, scope of Observation 4.2,
    Berenguel et al.); ST Section 13 item 5 fixes; RL Section 11.2 root edits;
    SR and BL closing-audit edits; CP Section 11.2. **Audit** these
    statements during proof review.
13. **The SV and MB studies** are single-solver, single-machine studies; MB
    was not independently reviewed (its default and LP-point counts were
    reproduced exactly by RB). The SS scaling study fits exponential and
    power laws equally well on `n = 4..10`. Wording must not exceed this.
14. **"SCIP follows the predicted exponents"** means: once node order,
    incumbent and propagation are aligned with the model, fitted slopes
    agree; each default departure has an identified cause. It is not a
    statement that SCIP satisfies the gap hypotheses.

### 6.3 Mathematical points checked here

- ST Theorem 1: the admissibility reduction, the use of the path's degree
  bound, the summed form of Lemma 3.1 and the PROGRAM constants
  (`S = 3/2`, `theta_S = 3/5`, `lambda_S = 5/9`,
  `exp(-(5/9)(1.000125)) ≈ 0.5738`) are correct. Lemma 3.1 holds with
  equality at `s0 = 1/(1+S)`, and at `s = 0` its slack is
  `lambda_S - log(1 + 1/S) = 0.5556 - 0.5108 > 0`.
- IC Theorem 3.5 "for every basis" is correct as stated: unimodular basis
  changes map integer points bijectively and preserve the projected
  relaxation, so `kappa` is basis-invariant; Schnorr–Euchner sphere decoding
  is variable branching with the continuous-relaxation bound (partial
  distances are exact minima over the free continuous coordinates), so it is
  covered.
- RL Theorem 3.3 and Lemma 3.3a use only `(U^q_alpha')` and the gradient
  Lipschitz bound; hence the upper half of RL Corollary 3.4 applies to
  termwise McCormick on `C^{1,1}` objectives. The lower half needs
  `(G^LB_alpha)`, which McCormick fails; this is exactly the face-exact
  phenomenon (FE Theorem 4.4, where `N_eps = 2` while `I_F` grows).
- CN Remark 6.3a(i): the factor in `2^-n sup psi ≤ Phi ≤ sup psi` uses
  `ceil(sqrt 2) = 2`; correct.

## 7. Unified notation

### 7.1 Global symbols

| Symbol | Meaning | Source symbols replaced |
|---|---|---|
| `n` | number of variables (spatial); number of integer variables (Section 12); number of unknowns (binary least squares) | sparse regression keeps `p` features, see 7.2 |
| `X0 = prod [L_i, U_i]`, `s0` | root box, largest side; a cube where bisection is analysed | |
| `F`, `P_ex`, `v(z)` | feasible set, exactly kept constraints, violation | |
| `f`, `f*`, `m = f - f*` | objective, optimal value, optimality gap | CB/ND/SO `m = f - f* + eps` becomes `m + eps` |
| `E(eta)`, `X*` | near-optimal set `{y ∈ F : m(y) ≤ eta}`, optimal set `E(0)` | CN `M` (optimal set) |
| `B = prod [l_i, u_i]`, `w(B)` | box, largest side | |
| `a_i^B(y)`, `q_B(y)` | `(y_i - l_i)(u_i - y_i)`, `sum_i a_i^B` | |
| `d_i^B(y)`, `delta_B(y)` | distance to the nearer face in coordinate `i`; `max_i d_i^B` | |
| `Q(x, r)`, `cN_inf(A, delta)` | sup-norm ball; least number of cubes of side `delta` covering `A` (`\mathcal N_\infty`) | CN `N_inf` |
| `(R_B, f_B)`, `LB(B)`, `Gamma_B = f - f_B` | node relaxation, bound, pointwise gap | |
| `(G^pt_alpha)`, `(G^LB_alpha)`, `(T_{alpha,beta})` | lower gap hypotheses | CN 1.4 |
| `(U^q_alpha')`, `(U_c)` | vertex-vanishing upper gap; width form `f_B ≥ f - c_U w(B)^2`, `v ≤ c_U w(B)^2` | CN `tau` in `(U_tau)` becomes `c_U` |
| `(EB)` with `c_E`, `(Lip)` with `L` | error bound `dist_2(z, F) ≤ c_E v(z)` for `v ≤ v_0`; Lipschitz constant | CN `kappa` becomes `c_E` |
| `Lambda = c_U (1 + L c_E)` | localization constant | |
| `L_grad` | Lipschitz constant of `grad f` | RL `M`, CN Lemma 3.6 `M` |
| `(QG)` with `c_g`, `(QD)` with `K` | quadratic growth to `X*`; quadratic doubling | |
| `N_eps`, `N_eps^cov`, `N_eps^guill` | least certificate (partition), least valid cover, least guillotine certificate | CN `N_opt(eps)`, FE `N_cov`, ST `N_cert` |
| `|T_bis|`, `T_R(f, eps)` | nodes of uniform dyadic refinement with `UBD = f*`; nodes of rule `R` | |
| `Phi_alpha(eps)`, `psi_alpha(eta)` | covering profile; Munos-type profile | |
| `I_F(eps)` | `integral_F (m + eps)^(-d_F/2) dsigma` over a face `F` of dimension `d_F` | |
| `C_{n,d}`, `M(S)`, `tau_S` | key-lemma constant, coordinate multiplicity, two-point constant (reach) of a stratum `S` | CN `tau` (two-point) becomes `tau_S` |
| `G`, `E_alpha`, `tau*(G)`, `vartheta(V, E)` | interaction graph, gap graph, fractional vertex cover number, gap-nondegeneracy constant | FE `tau(V, E)` becomes `vartheta(V, E)` |
| `kappa_eps(P)`, `phi`, `r(Q)`, `omega_mid` | class number at threshold `OPT - eps`; projected relaxation; relaxation bound of a convex set; midpoint clique number | IC `kappa_tau` (keep `kappa_tau` for a general threshold `tau`) |
| `cD`, `pi_cD(C)`, `pi_cD(C, y)`, `Z*(C, c)`, `F_lo(C)` | representation DAG (`\mathcal D`), propagation bounds, greatest hull-consistent box, forward bound | CP `D` (clashes with ST `D`) |
| `Phi_fs`, `Phi_full` | flat-sum fixed-point functional, full-range witness | CP `Phi` (clashes with `Phi_alpha`) |
| `(V)`, `(Π)` | relaxation and propagation certification of a point | |
| `cT = (T, {V_t})`, `|cT|`, `tw`, `S_t`, `phi_t` | rooted tree decomposition, number of bags, width `max |V_t| - 1`, separators, subtree value functions | DC `T`, `w` (clash with `w(B)`) |

### 7.2 Local notation (declared at the start of the section)

- Section 5: `(lambda, theta)` and `(lambda_F, theta_F)` for RLCTs and
  multiplicities.
- Section 8: `b`, `D`, `r`, `S = sqrt(1 + D/(2b))`, `vartheta_S = S/(1+S)`,
  `lambda_S = (1+S)/(2S^2)` (ST `theta`, `lambda`).
- Section 9: `lambda_t` slopes, `theta` shell ratio, `M_a`, `c_g`, `k`
  (bags per variable), `Delta_T` (children per bag).
- Section 11: rules `R_{mu,beta}` that split at
  `clip(mu yhat + (1 - mu) mid, [l + beta w, u - beta w])` (CB
  `R_{lambda,theta}`, FE `R(alpha, beta)`); safe rules use clamp `theta`;
  information models `I0`, `I1`, `I_inf`.
- Section 13: sparse regression uses `N` samples, `p` features, `k`
  sparsity, ridge `nu` (SR `n`, `lam`), threshold `tau_nu`; binary least
  squares uses `n` unknowns, `beta n` observations, SNR `rho`.

### 7.3 Conventions

- "With high probability" means with probability `1 - o(1)` in the stated
  limit. Every asymptotic theorem lists its regime in the statement.
- `log` is natural unless stated; `log2` explicit.
- Tolerances are absolute; a remark in Section 2 reduces relative ones
  (CN Section 1.2).
- Exact arithmetic is assumed in the node model; floating-point
  infeasibility verdicts are outside it.
- Every lower bound names the quantity it bounds: certificate size, valid
  cover size, leaves plus frame pieces, or nodes.

## 8. Chapter allocation

Page counts are rough (11pt, single column). Label prefixes give
ownership; the root assigns owners. Each section opens with one paragraph
on what it shows and ends, where relevant, with what it means for solvers.

### Front matter

- `sections/00-abstract.tex` (lead): abstract, keywords, MSC.
- `sections/01-introduction.tex` (lead, `intro:`; 6 pp). Question; the
  certificate object; Theorems I–X as a guided list; rate table (Section
  4.1); what is not claimed; relation to prior work in one structured
  subsection (cluster problem; Lipschitz and bandit complexity; MILP
  tree-size lower bounds; FBBT; branching-point practice; integer and
  statistical thresholds; companions); organization. No novelty claim
  beyond Luna's audit.

### Part I. Model

- `sections/02-model.tex` (`mod:`; 6 pp). Node relaxations; certificates and
  their variants (`N_eps`, covers, guillotine); gap hypotheses and which
  relaxations satisfy them (CN 1.4–1.5, Lemma 1.1; FE Lemma 2.5); reductions
  (R-inf), (R-rel); **Theorem I** with the frame decomposition and the
  per-round remark; what is excluded (cutoff propagation, cuts beyond the
  relaxation, lifted branching, child bounds, tolerance incumbents) with the
  `t^2 - 2t^4` example; information models deferred to Section 11. Proof of
  Theorem I in full (short).

### Part II. Vertex-vanishing gaps

- `sections/03-covering.tex` (`cov:`; 6 pp). CN Theorem 4.6 (proof),
  localization Lemma 6.1 (proof), Theorem 6.2–6.3 (**Theorem II**, proof),
  Remark 6.3a (both parts, proofs), Example 3.4, Proposition 6.8, Remark 6.9,
  Theorem 6.4, Corollary 6.5 (with (QG)), Corollary 8.1 (tightening), binary
  bisection remark (Remark 6.10). Figure: covering at parabolic scale.
- `sections/04-integrals.tex` (`int:`; 8 pp). Arcsine bound (CN Theorem
  3.1, with anisotropic and low-rank remarks); face lower bound (RL Theorem
  3.1); projection to faces (RL Lemma 3.2), bisection bound without (QD) (RL
  Theorem 3.3), vertex lemma (RL Lemma 3.3a), **Theorem III(a)** (RL
  Corollary 3.4) with proofs; strata: key lemma (CN Lemma 4.1, proof in
  App. A), Proposition 4.4, Theorem 4.5; regular instances (CN Theorems 7.1,
  7.2; Example 7.3); dimension and symmetry (CN 8.1–8.2). Stratified upper
  bound (CN 6.6–6.7) stated as a remark, proved in App. B.
- `sections/05-singular-order.tex` (`sing:`; 6 pp). RLCT definitions; RL
  Lemma 2.2 (proved), Lemma 2.1 and 2.3 (imported, App. C); **Theorem
  III(b)** (RL Theorem 4.1, Corollary 4.2); Example 4.3; examples table (RL
  Table 5.1); singular learning example (RL Propositions 6.1, 6.2); order of
  the relaxation: first order (CN Theorem 8.2), order `k` (RL Theorem 7.1,
  Propositions 7.2, 7.3; **Theorem III(c)**); Remark 7.4 (certified
  Lipschitz complexity in RLCT form). Open: Remark 4.1a, Conjecture 6.3,
  `k > 2` invariant.
- `sections/06-constraint-gaps.tex` (`cg:`; 4 pp). Modelling convention for
  `P_ex`; tube dichotomy (CN Lemma 5.1); infeasible-side covering (Theorem
  5.2); isotropic versus anisotropic loosening (Example 5.3); Lagrangian
  transfer (Theorem 5.4); KKT `log(1/eps)` (Theorem 5.7, proof in App. D,
  with Lemma 5.5 for polyhedral `P_ex` only); what propagation of the
  original constraints removes (Remark 5.8). **Theorem IV(d).** Credit
  Kannan–Barton for the infeasible-side mechanism with upper estimates.

### Part III. Face-exact relaxations, dimension and decomposition

- `sections/07-face-exact.tex` (`fe:`; 10 pp). Gap geometry (FE Lemmas
  2.1–2.5, Definitions 2.6–2.8); lower bounds (Theorem 3.4, Corollary 3.5,
  Theorems 3.6, 3.8, Lemmas 3.7, 3.9, Proposition 3.10, Corollary 3.11);
  sharpness (Proposition 3.13); structure (Lemma 4.1, Theorem 4.2,
  Corollary 4.3, Theorems 4.4, 4.5, Propositions 4.6, 4.7, Example
  3.12(b)); failure of the tools (Proposition 3.14); upper bounds (RL
  Theorem 3.3 for smooth `f`; FE Theorem 5.1(b), Proposition 5.2);
  convergence order (Theorem 6.1). **Theorem V.** McCormick certificate
  integral in App. E. Open: Question 7.1'', Conjecture 4.8, Open 7.2–7.4.
  Figure: gap-zero sets of alphaBB and McCormick on a square; the kink and
  tilted families.
- `sections/08-dimension.tex` (`dim:`; 5 pp). Path family (ST Lemma 1.1);
  centre-volume lemma (ST Lemma 2.1, proof); Lemma 3.1 (with the rigorous
  threshold of 6.2(1)); **Theorem VI(a)** (ST Theorem 1, Corollary 1.3);
  remarks (what the proof uses, scale, tolerance, ceiling on the base,
  where the constant is lost); orthant boxes (Proposition 5.2) as the
  `eps -> 0` picture; upper bound (Proposition 5.5); chordal split (Lemma
  9.1) and Consequence A; Theorem 2 and Consequence B as factorization
  dependence (proof in App. F). Open: the base (data 2.7–3.5), a
  `log(1/eps)` factor with a good base (Conjecture 5.4).
- `sections/09-decomposition.tex` (`dec:`; 6 pp). Model (DC Definition 1.2,
  Lemmas 1.1, 1.3, remark on touching pairs), virtual boxes (Lemma 1.4),
  Lagrangian unfolding (Lemma 1.5); slopes are necessary (Proposition 2.6,
  proof); existence (Theorem 3.4, statement and path specialization; proof
  in App. F); separation (**Theorem VI(b)–(d)**, DC Theorem 4.1 with
  proof, including the two-regime ratio argument and the base-rounding
  caveat); what the separation is about (Section 4.1 table, Observation
  4.2 with proof and measure form); worst case (Theorem 3.3) as a remark,
  known in substance (Zhang–Sun; Bienstock–Muñoz). Positioning per LA
  Section 4: discrete AND/OR antecedents, MILP treewidth-2 lower bounds
  with ties (Basu et al.; Dey–Shah; Cheng–Basu), Berenguel et al. as
  algorithmic precursor, Robertson–Cheng–Scott for the first-order copy
  error. State plainly that finding such certificates without `x*` is not
  addressed here.

### Part IV. Propagation and branching

- `sections/10-propagation.tex` (`prop:`; 9 pp). Model (CP Section 1;
  Lemma 1.1 credited to Belotti et al. for the fixed point; HC4 steps in
  App. G); `pi_cD` as a node bound (Proposition 1.4); hybrid certificates
  (Lemma 2.1, proof of (b) in App. G; Theorem 2.2; Proposition 2.3);
  exactness (Theorem 3.1, Corollary 3.3, Remark 3.4, Corollary 3.5,
  Proposition 3.6, Examples 3.7, Theorem 3.8 with its idealization stated);
  rounds (Propositions 3.9, 3.10; observed `pi a eps^(-1/2)` as data);
  dependency loss (Lemma 4.1, Remark 4.1a, Corollary 4.2, Example 4.3,
  Lemma 4.4, CND and ND1); surviving lower bounds (Theorems 5.1, 5.2,
  Proposition 5.1a, Theorems 5.4, 5.5, Remark 5.6); the representation table
  (CP Section 6). **Theorem VII.** Open: Conjecture 3.11, face-type loss for
  `p ≥ 3`, constrained problems, general DAGs.
- `sections/11-branching.tex` (`br:`; 9 pp). Information models (CB 1.4,
  germ caveat); 1D structure (CB Proposition 1); **Theorem VIII(a)**: CB
  Theorem 1 with Lemmas 1–2 in full (and Corollary 1), Proposition 2,
  Theorem 3 (instances in App. H), Theorem 2 (proof), Propositions 4 and 4'
  (App. H; SCIP 10.0.2 rule as read from source); full information is
  trivial in 1D (Proposition 0); **(b)** SO Theorems C, C' (App. H), ND
  Theorem N3 (App. H), guillotine bound `(2N_eps - 1)^n`; **(c)** FE
  Theorem 5.3, Propositions 5.4–5.7 (App. H for proofs), incumbent branching
  as the Shectman–Sahinidis/BARON mechanism with the tie-rule caveat;
  **(d)** RB Theorem A (corrected scope), Proposition C, Proposition D,
  Theorem B and Proposition E as one paragraph each (App. H). Short
  pointer to Section 14 for the MINLPLib evidence. Open: `C_n`-competitive
  `omega`, Question 5.9, polynomial classes, a model with boundary
  relaxation points.

### Part V. Integer branching and random instances

- `sections/12-integer.tex` (`ic:`; 7 pp). Problem and projected relaxation
  (IC 1.1); convex-piece trees and certificates (Definitions 1.1–1.2, Lemma
  1.3); classes and conflicts (Definition 1.4, Lemma 1.5); **Theorem IX**:
  Theorem 1.6 (proof), Theorem 1.7 (statement; Lemma 1.7a in App. I),
  Theorem 1.8 (statement; proof in App. I), comparisons (Proposition 2.1,
  Example 2.1a, Theorem 2.2, Theorem 2.3 with the Gläser–Pfetsch input,
  Proposition 2.4, Proposition 2.5); random CVP (Theorems 3.4, 3.5,
  Proposition 3.6; proofs in App. I); perspective versus pairwise hull (one
  theorem for the asymmetric gadget; App. I); path lemma and condition C1
  (IC Section 5, Proposition 5.2). Credit DDM (midpoint and counting
  mechanisms), Kaibel–Weltge and Averkov et al. (relaxation complexity),
  Gläser–Pfetsch (hiding sets). Open: split trees versus `kappa` for convex
  quadratics; true CVP exponents; Gaussian bases.
- `sections/13-random.tex` (`rnd:`; 7 pp). Local notation box. Sparse
  regression: model, perspective relaxation, midpoint formula (SR Lemma 1.5),
  removal-half certificate (Lemma 1.3); **Theorem X**: SR Theorems 3.1, 3.2,
  Corollaries 3.3, 3.4 (statements; proofs in App. J); hard side Theorems
  4.3, 4.4 (statements; App. J); the fixed-ridge remark; Remark on PWE
  Theorem 2 (self-contained argument). Binary least squares: model; root
  (Proposition 1.1, Theorem 1.2), ML (Theorem 2.2), C1 (Theorem 3.1,
  conditional part flagged), certificates (Theorems 4.1, 4.3), SDP and
  eigenvalue shift (Theorem 6.2, Proposition 6.3); midpoint blindness above
  `8 log n` (Theorem 2.3) as a remark if space allows. Interpretation:
  thresholds for root exactness, linear trees and exponential certificates
  differ; certification can be superpolynomially harder than search
  (conditional on the cited algorithm). Open: SR Conjecture 5.2, BL
  Conjectures 3.3 and 4.5, finite-size versions.

### Part VI. Evidence and discussion

- `sections/14-computation.tex` (`comp:`; 4 pp). Archived evidence only,
  each with its provenance and arithmetic: toy B&B exponents (CN Tables
  9.1–9.2; RL Table 5.2), face-exact rule tables (FE Section 8.2, exact rows
  labelled), single-tree toy and SCIP counts with and without the minor
  separator (ST Sections 7.3–7.4, 8), propagation counts (CP Table 7.1),
  SCIP node exponents (SV), MINLPLib branching-point studies (MB; RB 6.4),
  chain scaling (SS). One table per study; statements limited per 6.2(13).
- `sections/15-discussion.tex` (`disc:`; 3 pp). What determines complexity:
  relaxation gap geometry, representation, class structure; when branching
  helps (constants, logs; polynomial factors only for face-exact
  placement); what solvers can and cannot gain (symmetry breaking, stronger
  relaxations, representation, decomposition); proved versus observed;
  consolidated open questions (Section 12 of this file).

### Appendices

| File | Content | Pages |
|---|---|---|
| `appendices/A-geometric-tools.tex` | CN Lemma 4.1 (Cauchy–Binet, area formula), Lemmas 4.2–4.3, Proposition 4.4, tube volumes and `|II| ≤ 1/tau` for CN Theorem 8.2(d) | 5 |
| `appendices/B-vertex-gap-proofs.tex` | CN Theorems 6.6–6.7, 7.1 (full), 7.2, 8.2; Lemma 3.6 and RL Lemma 3.5, Proposition 3.6 | 7 |
| `appendices/C-rlct.tex` | RL Lemmas 2.1 (imported, hypotheses checked), 2.3 (with orthant extension), 2.4; Section 5 derivations; Propositions 6.1–6.2; Theorem 7.1, Propositions 7.2–7.3 | 6 |
| `appendices/D-constraint-gap-proofs.tex` | CN Theorem 5.4, Lemma 5.5, Proposition 5.6, Theorem 5.7 | 4 |
| `appendices/E-face-exact-proofs.tex` | FE Lemma 3.1, Theorem 3.2, Corollary 3.3; Proposition 3.14 in full; Theorems 4.4–4.5, Propositions 4.6–4.7; Theorem 6.1(b) | 6 |
| `appendices/F-dimension-decomposition.tex` | ST Theorem 2, Proposition 5.3, Proposition 6.1; DC Corollary 2.1, Lemma 2.2, Lemmas 3.1–3.2, Theorem 3.4 in full, Theorem 4.1(c) | 9 |
| `appendices/G-propagation-proofs.tex` | HC4 steps as run steps; Lemma 1.2; Lemma 2.1(b) chain minimum; Theorem 3.1 and Remark 3.2; Propositions 3.9–3.10 | 5 |
| `appendices/H-branching-proofs.tex` | CB Theorem 3 instances, Propositions 4, 4'; SO Lemma 6.1, Theorems C, C' and the `G(n)` table; ND Theorem N3; FE Theorem 5.3, Propositions 5.4–5.7; RB Theorem A, Propositions C–F, Theorem B | 8 |
| `appendices/I-integer-proofs.tex` | IC Lemma 1.7a, Theorems 1.7–1.8, 2.2–2.3, Propositions 2.4–2.5, Section 3 proofs, the asymmetric gadget | 7 |
| `appendices/J-random-proofs.tex` | SR Sections 2–4 proofs; BL Sections 1–4 and 6 proofs | 14 |
| `appendices/K-computation.tex` | protocols, solver settings, data provenance, archive manifest | 3 |

Total: about 95 pages of main text and 75 of appendices including
references. If the editor requires length reduction, detach Section 13 with
App. J, then Section 9 with the decomposition part of App. F.

### 8.1 Suggested ownership blocks

| Block | Files | Main sources |
|---|---|---|
| Lead | 00, 01, 14, 15, K; integration | all |
| 1 (vertex-vanishing gaps) | 02, 03, 04, 05, 06; A, B, C, D | CN, RL |
| 2 (face-exact, dimension, decomposition) | 07, 08, 09; E, F | FE, ST, DC |
| 3 (propagation and branching) | 10, 11; G, H | CP, CB, ND, SO, RB |
| 4 (integer and random) | 12, 13; I, J | IC, SR, BL |

Cross-block contracts: Block 1 owns Theorem I and the gap-hypothesis
definitions, which every other block cites; Block 2 cites Block 1's
Theorem 3.1 (arcsine) and Lemma 6.1; Block 3 cites Block 1's Theorems 4.6
and 3.1 for Theorem 5.2 of Section 10; Block 4 cites the path lemma from its
own Section 12 in Section 13.

### 8.2 Figures and tables

- Table 1 (intro): headline results with hypotheses and section pointers.
- Table 2 (intro): the rate table of Section 4.1.
- Figure 1 (Section 2): gap zero sets (alphaBB vertices; McCormick
  vertex-cover faces) on a square and a cube.
- Figure 2 (Section 3): multiscale covering of near-optimal sets at
  parabolic scale `sqrt((eps + eta)/alpha)`.
- Figure 3 (Section 7): kink family, tilted stratum, curved non-transversal
  surface (schematic).
- Figure 4 (Section 9): virtual boxes of a decomposition certificate.
- Table 3 (Section 10): same function, same relaxation, different DAG.
- Figure 5 (Section 11): clamp map orbit and the Cantor set for
  `beta = 1/5`.
- Table 4 (Section 13): thresholds for root exactness, C1 and certificate
  size in both random models.
- Tables 5–8 (Section 14): archived counts and ratios.

Figures are analytic schematics (TikZ) or plots from archived logs; no
experiment is rerun.

## 9. Computational evidence plan

| Study | Archive | What it supports | Required wording |
|---|---|---|---|
| CN toy sphere/ball B&B | `spatial-constrained/logs/analyze_sweep.log`, `sweep_*.jsonl` | exponents `0, 1/4, 1/2, 1`; boundary stratum governs ball instances | floating point; Lagrangian dual bounds validated on 582 boxes |
| RL bisection sweeps | `rlct/logs/analyze_sweep.log`, `revision_sweep.jsonl`, `fit_constants.log` | RLCT exponents within 0.021; leading constants to 3–5 digits | idealized bisection with exact alphaBB, not a solver |
| FE rule tables | `spatial-face-exact/` logs, exact rational replays (`kink_exact_runs.log`, closing audit B) | clamp failure, unclamped point, incumbent rule counts | label exact versus floating-point rows |
| ST toy and SCIP | `theory-face-exact/logs/` (v2, v3 certified runs; SCIP with and without the minor separator) | growth per variable 2.7–3.5 termwise; SCIP 2.1–2.3 default, 2.9–3.5 without minor cuts | certified node bounds by weak duality; floating point |
| CP propagation counts | `cutoff-propagation/logs/tables.md`, `rounds.log` | representation dependence; rounds | floating point HC4 without outward rounding |
| SV (SCIP exponents) | `solver-validation/results/summary.md` | fitted slopes match predicted exponents under the model setting; five identified departures | one solver version; not independently reproduced |
| MB, RB 6.4 (MINLPLib) | `minlplib-branching/results/`, `robust-branching-points/results/summary.md` | theory's branching-point recommendation does not transfer; clamp protective; safe variants neutral | 57 instances, 3 seeds, 60 s; MB not independently reviewed; seed noise large |
| SS (chains) | `research-20260929/computation/` | SCIP ~5x per two variables at `n = 4..10`; chain DP B&B solves certified instances to `n = 8192` | power laws of degree 5–6 fit equally well; prototype bounds by a rounding analysis, not interval arithmetic |

The root packages these archives as archival computational references.
Section 14 cites them by archive path inside the supplement, not by
repository path.

## 10. Literature requests for Luna

Each request names the claim it supports. Writers use only Luna's verified
citations.

1. Cluster problem and box counts: Du–Kearfott (1994); Kearfott–Du (1992);
   Neumaier (2004, §15, the "n replaced by n - a" heuristic and pp. 29,
   35–44); Wechsung–Schaber–Barton (2014, threshold `K ≤ 9 lambda_1/4`,
   minimizer at box centre); Kannan–Barton (2017 §3.2, Lemmas 2–3, 8, 10,
   Remark 4, Corollary 4; 2018 Definition 13); Bompadre–Mitsos (2012).
   Interval box-count literature not yet examined (Ratschek–Rokne;
   Csendes–Ratz; Kearfott 1996; Schöbel–Scholz 2010; Hansen–Walster 2004).
2. Lipschitz and bandit complexity: Hansen–Jaumard–Lu (1991);
   Perevozchikov (1990) via Bouttier et al.; Munos (2011);
   Bachoc–Cesari–Gerchinovitz (2021, Theorem 3, Assumption 4); Bubeck et al.
   (2011, Example 3); post-2021 work on the log factor.
3. Geometric tools: Federer (1959) Theorems 4.8(12), 4.18(2);
   Niyogi–Smale–Weinberger (2008) Lemma 5.3, Proposition 6.1; Weyl (1939);
   Gray (2004); Evans–Gariepy; Robinson (1976); Bonnans–Shapiro (2000)
   Theorem 2.87 and the SOSC quadratic growth theorem.
4. RLCT: Lin (2017, arXiv:1003.5338 and the J. Algebraic Statistics
   version: theorem numbering); Watanabe (2009); Varchenko (1976);
   Arnold–Gusein-Zade–Varchenko Vol. II; Aoyagi–Watanabe (2005);
   Drton–Plummer (2017, Example 2.2, Table 1); Lau et al. (local learning
   coefficient); Potfer–Perchet (2026) and Grulha (2026) (abstracts only).
5. Face-exact and branching points: McCormick (1976); Al-Khayyal–Falk
   (1983); Rikun (1997); Tawarmalani–Sahinidis (2002 book pp. 215, 243;
   2004); Shectman–Sahinidis (1998); Al-Khayyal–Sherali (2000);
   Speakman–Lee (2018, Table 1 and pp. 3, 22–23); Belotti et al. (2009,
   Couenne, pp. 18, 29–30); Liu–Sahinidis–Shectman (1996); Dey–Santana–Wang
   (2019); Epperly–Pistikopoulos (1997); SCIP 10 documentation and
   `branch.c` for `midpull`, `midpullreldomtrig`, `clamp`; Wechsung's thesis
   as reported by Kannan–Barton p. 2.
6. Single tree and decomposition: Basu–Conforti–Di Summa–Jiang (2023,
   Theorems 2.2, 3.11); Dey–Shah (2022); Cheng–Basu (2026, Lemma 3.2);
   Griewank–Toint (1984, Theorem 4); Agler–Helton–McCullough–Rodman (1988);
   Vandenberghe–Andersen (2015); Waki et al. (2006); Zhang–Sun (2022,
   Corollary 1); Bienstock–Muñoz (2018); Berenguel et al. (JOGO 2013);
   Robertson–Cheng–Scott (2025); Cao–Zavala; MUSE-BB; Dechter–Mateescu
   (AND/OR search, Theorem 30); Vorob'ev (1962); Lasserre (2006);
   SCIP `sepa_minor` documentation.
7. Propagation: Benhamou et al. (1999); Belotti–Cafieri–Lee–Liberti (2012
   preprint or journal version, p. 10); Schichl–Neumaier (2005);
   **Schichl–Markót–Neumaier (2014) exact wording and journal version**;
   Araya–Trombettoni–Neveu (2010); Vu–Schichl–Sam-Haroud (2009); Faltings
   (1994); Domes–Neumaier (2010); Puranik–Sahinidis (2017); Vigerske–Gleixner
   (2017); Bestuzheva et al. (2025); Hansen–Walster (2004) (not yet
   examined).
8. Competitive analysis: Daskalakis–Diakonikolas–Yannakakis (chord
   algorithm); Baran–Demaine–Katz; Berman–DasGupta–Muthukrishnan (2002) and
   Hershberger–Suri–Tóth (2005) only if the guillotine remark is kept.
9. Integer: Dey–Dubey–Molinaro (lower bounds on B&B tree size, Section 6,
   Lemma 12); Kaibel–Weltge; Averkov et al. (relaxation complexity);
   Gläser–Pfetsch (statement and exponent conventions); Jeroslow (1974);
   Reis–Rothvoss (flatness constant); Siegel (1945); Kabatiansky–Levenshtein
   (1978); lattice-reduction and sphere-decoding references used in the
   remarks.
10. Random instances: **Pilanci–Wainwright–El Ghaoui (2015) Theorem 2, its
    Section 3.1 noise model, Corollary 2, Appendix 7.1, erratum status**;
    Pilanci thesis (2016); Dong (arXiv 1603.04572); Bertsimas–Pauphilet–Van
    Parys (2019); Bandeira et al. (low-degree hardness of sparse recovery);
    Hansen–Hassibi–Dimakis–Xu; Hassibi et al. (2014); **Hu–Lu (2020)**;
    **Papailiopoulos (2026)**; Jaldén–Martin–Ottersten (2003);
    Hug–Schneider; McCoy–Tropp; Godland–Kabluchko–Thäle.

## 11. Submission framing

### 11.1 Title

Recommended: *The certificate complexity of branch-and-bound with nonlinear
relaxations*. Alternative: *What determines the size of branch-and-bound
trees with nonlinear relaxations*.

### 11.2 Venue

Mathematical Programming, Series A, as a long research article with
appendices in the main PDF (or as electronic supplementary material, if
the journal prefers). It is the natural audience for B&B tree-size theory
(Dey–Dubey–Molinaro; Basu et al.), global-optimization convergence theory
and the integer results. The length is well above a typical article; the
cover letter explains the single-object design and offers the
detachments of Section 8. If the root prefers a venue with an explicit
monograph-length track, that is a user decision.

### 11.3 Proposed abstract (draft, about 240 words)

> Branch-and-bound certifies the optimal value of a nonconvex or
> mixed-integer problem by covering the domain with pieces on which a node
> relaxation reaches the target. We study the least number of such pieces,
> the certificate complexity of an instance and a relaxation, and show that
> it determines tree size up to explicit factors for every branching rule,
> node order, incumbent and bound tightening that uses the relaxation. For
> spatial branch-and-bound with relaxations whose gap vanishes only at box
> vertices, certificate size and uniform bisection lie within a logarithmic
> factor of a multiscale covering number of the near-optimal sets, and within
> constant factors of a sum of face integrals when the objective has a
> Lipschitz gradient on a box. The tolerance exponent is half the
> box-counting dimension of the optimal set under quadratic growth and, for
> analytic objectives, is given face by face by real log canonical
> thresholds. Relaxations that are exact on box faces, such as McCormick
> envelopes, follow a different law set by how near-optimal sets meet those
> faces. On a path-structured problem with a unique nondegenerate minimizer
> they force exponentially many boxes in the dimension, while certificates
> that follow a tree decomposition with affine child bounds and the same
> relaxations need polynomially many. Objective-cutoff propagation is a
> further node bound that depends on the expression graph. Splitting at the
> relaxation minimizer is 4-competitive in one dimension, while every
> node-local rule loses a factor exponential in the dimension. For integer
> branching the class number bounds every convex-piece tree; it is
> exponential for random closest-vector problems, and random sparse
> regression and binary least squares show distinct thresholds for root
> exactness, linear trees and exponential certificates.

Keywords: branch-and-bound; spatial branch-and-bound; global optimization;
mixed-integer nonlinear programming; certificate complexity; convex
relaxation; McCormick relaxation; covering numbers; real log canonical
threshold; bound tightening; branching rules; class number.

MSC 2020: 90C26 (primary), 90C11, 90C57, 90C60, 68Q25, 49J52 (verify with
Luna; 14B05 for the RLCT part is optional).

### 11.4 Contribution statement (for the introduction and cover letter)

Contributions are stated relative to the sources Luna verifies. The notes'
own positioning, to be confirmed:

- New as far as the notes' searches found: rigorous lower bounds for
  relaxation-based spatial B&B that hold for adaptive trees with
  same-relaxation tightening and constraints; the per-box arcsine bound on
  strata and the necessity of the multiplicity; the constraint-gap lower
  bounds (Kannan–Barton as precedent for the mechanism with upper
  estimates); the covering law for constrained problems; the box-face law
  without log loss and its RLCT form; the face-exact lower bounds through
  vertex covers and transversality, the fractional vertex cover exponent,
  and the separation of convergence order from node counts at equal order
  and prefactor; the single-tree bound at a unique nondegenerate minimizer
  for termwise McCormick; the instance-dependent decomposition-certificate
  bound and the slope lower bound; the propagation bound as a
  representation-dependent node bound, the flat-sum fixed-point
  characterization and the surviving lower bounds; competitive bounds for
  quadratic-gap relaxations and the exponential-in-`n` lower bound for
  node-local rules; the class number as exact semantic tree size, its
  separation from split trees, and the random-CVP exponents; the sparse
  regression C1 threshold below root exactness; the binary least-squares
  root and certificate laws.
- Known in substance and credited: the unconstrained covering and integral
  arguments (Hansen–Jaumard–Lu; Perevozchikov; Munos; Bachoc et al.), the
  Lipschitz first-order law, the McCormick gap formula, the convex-analysis
  lemma on affine segments, branching at the incumbent (Shectman–Sahinidis),
  first-order sufficiency at nondifferentiable minima (Wechsung's thesis),
  "exact bounds give no cluster" (Du–Kearfott; Wechsung et al.), the FBBT
  fixed point (Belotti et al.), the DDM counting mechanisms, relaxation
  complexity (Kaibel–Weltge; Averkov et al.), Jeroslow and Gläser–Pfetsch,
  the ML threshold and SDP tightness condition in MIMO detection, the
  Gaussian cone law, chordal decompositions (Griewank–Toint), worst-case
  decomposition bounds (Zhang–Sun; Bienstock–Muñoz), and the RLCT–volume
  link (Arnold–Gusein-Zade–Varchenko; Watanabe).
- Originality ratings recorded by the reviews: low to modest for the
  unconstrained covering package; modest for the key lemma and regular
  instances; modest to moderate for constraint-gap schemes; modest for
  branching competitiveness; random CVP the most novel integer part. The
  paper's framing should match these ratings, not exceed them.

### 11.5 What the paper does not claim

- No practical speedup and no recommended rule change. The MINLPLib studies
  show that the branching-point theory does not transfer, and that SCIP's
  clamp is protective because relaxation points sit on variable bounds,
  which the models exclude.
- The exponential single-tree bound is not a statement about search alone.
- The decomposition upper bound is not an algorithm.
- Random-instance results are asymptotic; they do not predict practical
  sizes.
- No open question is declared solved beyond the proved statements; the
  face-exact characterization, `C_n`-competitiveness of `omega`, split trees
  versus `kappa` for quadratics and the sharp random constants stay open.

### 11.6 Risks and mitigations

| Risk | Mitigation |
|---|---|
| Length | modular parts; detachable Section 13 and Section 9 |
| "Transfer of known arguments" | credit explicitly; foreground the new mechanisms (constraint gaps, box-face law, face-exact geometry, propagation, class number) |
| "Abstract relaxation models are far from solvers" | Section 14 aligns SCIP with the model and names each departure; Section 10 treats propagation; Section 11 reports the negative MINLPLib result |
| Constants exponential in `n` | state them; separate exponents in `eps` from dimension dependence |
| A published theorem shown false | factual remark in Section 13, Luna-verified wording, user decision on contacting authors |

## 12. Open questions for the paper's final section

1. A characterization of face-exact node complexity (does adding row-slice
   bounds suffice? FE Question 7.1'').
2. Whether `omega` (most central coordinate at the minimizer) is
   `C_n`-competitive in `n ≥ 2` dimensions; any constant must be exponential
   in `n`. Competitive rules for face-exact relaxations (FE Question 5.9).
3. The right base of the single-tree bound and a `log(1/eps)` factor with a
   good base (ST Conjecture 5.4).
4. Whether split-tree size is polynomial in `kappa` for convex quadratic
   objectives (IC Open problem 2.6); the true random-CVP exponents
   (Conjecture 3.7); Gaussian bases.
5. Bounded-round propagation in the exact case (CP Conjecture 3.11) and
   face-type loss for `p ≥ 3`.
6. A branching-point model with relaxation points on variable bounds.
7. RLCT faces with `lambda_F = d/2`, `theta_F ≥ 2` (RL Remark 4.1a); an
   invariant for order-`k` gaps with `k > 2`; noisy singular models (RL
   Conjecture 6.3).
8. Constrained strata in the box-face law (RL Section 9); propagation of the
   original constraints on curved strata (CN Open 3).
9. Sharp constants and finite-size versions of the random thresholds (SR
   Conjecture 5.2; BL Conjectures 3.3, 4.5).
10. Finding decomposition certificates of the size of Theorem VI(b) without
    knowing `x*` (stated as outside this paper's scope).

## 13. Blockers and requests to root

No mathematical blocker prevents writing. Requests:

1. **Path discrepancy.** Confirm that the brief's
   `research-20260929/theory-single-tree/` means
   `research-20260929/theory-face-exact/` (ST).
2. **Scope confirmation.** Confirm the exclusions of Section 3.3, in
   particular SR2 (stronger relaxations) and EA/AM (adaptive decomposition
   algorithms), which are proved and reviewed but would add about 30 pages.
   If the user wants them, the natural place is a second paper.
3. **Companion citations.** Decide whether unpublished companion manuscripts
   (`paper-relaxation-limits`, `paper-decomposition-aware`,
   `paper-open-minlplib`, `paper-adaptive-obbt`) may be cited in the
   submission.
4. **PWE remark.** User decision on whether to contact the authors before
   submission; Luna verification is required either way.
5. **Lean artifact.** Decide whether the Lean formalization of CB Theorem 1
   (formal topic 33) goes into the supplementary archive and is mentioned in
   a footnote. The paper's proof stands on its own.
6. **Proof tasks for Sol** (Section 6.2): rigorous ST Lemma 3.1 threshold;
   optional certification of the ST Theorem 2 base; a confirmation pass over
   the unrechecked edits listed in 6.2(12).
7. **Venue.** Confirm Mathematical Programming, Series A, or name another.
