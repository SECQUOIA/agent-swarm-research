# Author report: sparse and constrained sections, round 1

Author: Opus, sparse/constraint block. Date: 2026-10-05.

Files owned and written:

- `sections/05-sparse.tex` (Section 5, labels `sp:`)
- `sections/06-constraints.tex` (Section 6, labels `con:`)
- `appendices/C-sparse.tex` (Appendix C, labels `sp:`)
- `appendices/D-constraints.tex` (Appendix D, labels `con:`)

No other file was edited. No experiment was rerun, no literature search was
made, nothing was committed, and no work was delegated.

## 1. Structure

| Label | Content |
| --- | --- |
| `def:sp:instance`, eq. `eq:sp:curv`, `eq:sp:Lmon`, `eq:sp:kappa` | Sparse mixed polynomial instance; status of the curvature premise (promised, or verified by the monomial bound `L_mon`); derivative row-sum bounds. |
| `thm:sp:main` | Unified theorem: fixed-degree polynomial on a mixed box, ambient grid noise, exact on every draw, expected work `C_0^p[4+(1+n/2)L w_max/(2 sigma)]^p poly_d(I)`, patch or fallback output, `q`-bit evaluation. |
| `lem:sp:cells`, `lem:sp:allowed`, `lem:sp:dp`, `lem:sp:round`, `prop:sp:prune` | Nested cells, allowed grid, sparse two-pass DP, fixed-cell rounding, sound pruning with one global witness per retained cell. |
| `lem:sp:compare`, `prop:sp:count` | Conditional comparison intervals and the expected retained-cell count `Theta_beta`. |
| `sec:sp:width` | Why treewidth controls the tables but the global allowance `E_j = nLh_j^2/8` keeps `n^{O(p)}`; cites `prop:lim:local` and `thm:lim:width`. |
| `def:sp:closure`, `prop:sp:closure-sound`, `prop:sp:closure-stop` | Closure test (integer singletons, original-bound gradient signs, strongly convex patch); soundness on every draw; success under growth and margins. |
| `lem:sp:tails`, `def:sp:schedule`, `lem:sp:rare`, `def:sp:algorithm` | Finite-law tails (cited from Appendix A), base schedule `B -> rho, g_0, tau -> J -> M`, rare late closure, the algorithm. |
| `prop:sp:eval`, `cor:sp:qp` | Polynomial-bit evaluation of the patch; quadratic and MIQP corollary with rational output on every draw. |
| `lem:sp:bezout`, `lem:sp:gls`, `lem:sp:faces` (Appendix C) | Nonsingular-zero count; general GLS evaluation lemma (polytopes, lower-dimensional patches, approximate oracles, 2- or infinity-norm repairs); quadratic face enumeration. |
| `lem:con:uniform` | Uniform schedules for families of objectives indexed by conditioned noise. |
| `def:con:graph`, `lem:con:expand`, `thm:con:graph`, `def:con:charted`, `lem:con:chart`, `lem:con:approx`, `ex:con:graph-curv`, `ex:con:chain` | Global graph parameterizations: explicit bounded-depth case (E) and monotone implicit case (I) in one theorem with distinct constants and outputs. |
| `def:con:actuator`, `thm:con:actuator`, `ex:con:dyn`, `ex:con:actuator` | Affine-state recurrences with polynomial actuators, any horizon. |
| `def:con:simplex`, `thm:con:simplex`, `lem:con:simplex-round`, `lem:con:simplex-count`, `lem:con:simplex-close`, `lem:con:simplex-tail` | Disjoint inequality/equality simplices with integer intervals and whole-block bags. |
| `def:con:order`, `thm:con:order`, `lem:con:order-vertices`, `lem:con:transport`, `prop:con:order-count`, `lem:con:lpgap`, `lem:con:order-close`, `lem:con:order-tail`, `ex:con:premature` | Order constraints with continuous and binary coordinates; continuous case is `n_z=0`. |
| `lem:con:approx-closure`, `lem:con:kkt` (Appendix D) | Certified closure and KKT margin tail for implicit graphs. |
| `sec:con:scope` | What is not covered (general TU, overlapping budgets, affine images, general integer ranges in orders, extra constraints cutting a chart, nonlinear recurrences). |

Compiled size of the four files alone: 38 pages.

## 2. Source-development-to-label map

Paths relative to `research-20261002/`.

| Source | Status in sources | Disposition and labels |
| --- | --- | --- |
| `new-direction/sparse-bag-cell-smoothed-qp.md` | complete, reviewed | Subsumed by `thm:sp:main` (d=2) and `cor:sp:qp`. Its PSD-face closure is replaced by the strongly convex patch test; exact rational output by `kozlov1980` on the patch and `lem:sp:faces` on fallback. The continuous active-face fallback (`B=3^n`) is the case `n_z=0` of `lem:sp:faces`. |
| `new-direction/sparse-bag-cell-smoothed-miqp.md` | complete, reviewed | Subsumed by `thm:sp:main` and `cor:sp:qp`; integer singleton transition in `lem:sp:cells`; comparison spacing `a_i` in `prop:sp:count`; integer fixing only from singleton hulls in `def:sp:closure`. |
| `new-direction/smoothed-sparse-polynomial.md` | complete, reviewed | `thm:sp:main`, `lem:sp:round`, `prop:sp:prune`, `lem:sp:compare`, `prop:sp:count`, `def:sp:closure`, `prop:sp:closure-sound`, `prop:sp:closure-stop`, `def:sp:schedule`, `lem:sp:rare`, `def:sp:algorithm`, `prop:sp:eval`. Its §7 original-objective certificate is `prop:model:regret` (model author), cited after `thm:sp:main`. |
| `new-direction/convex-patch-evaluation.md` | complete, GLS repair reviewed | Generalized as `lem:sp:gls` (Appendix C) and used in `prop:sp:eval` and in the proofs of all Section 6 theorems; also cited by Appendix E. |
| `new-direction/polynomial-finite-noise-tails.md` | complete, reviewed | Owned by Appendix A (`lem:count:finite-tails`); cited in `lem:sp:tails` and Section 6. Its active-gradient argument is `lem:count:finite-tails`(d); my variants for simplices (`lem:con:simplex-tail`), orders (`lem:con:order-tail`) and implicit graphs (`lem:con:kkt`) use `lem:sp:bezout`. |
| `new-direction/polynomial-exact-fallback.md`, `polynomial-exact-fallback-construction.md` | complete, reviewed | Owned by Appendix A (`thm:count:fallback`); cited, not reproduced. Applied to original constrained domains (see §4.4). |
| `new-direction/global-error-cell-barrier.md` | complete limitation | Owned by limitations author as `thm:lim:width`; explained and cited in `sec:sp:width`. |
| `new-direction/local-error-recourse-interface.md`, §1 | complete counterexample | Owned by limitations author as `prop:lim:local`; cited in `sec:sp:width`. Its §2 interface is not used. |
| `new-direction/smoothed-polynomial-graph-constraints.md` | complete, reviewed | `thm:con:graph` case (E), `lem:con:expand`, `ex:con:graph-curv`, `ex:con:chain`. |
| `new-direction/smoothed-implicit-graph-constraints.md` | complete, reviewed | `thm:con:graph` case (I), `lem:con:expand`, `lem:con:kkt`, `lem:con:approx`, `lem:con:approx-closure`. Its cubic-actuator dynamics example (§8) is not reproduced; `ex:con:actuator` uses the affine-state model instead. |
| `new-direction/implicit-graph-oracle-interface.md` | complete, reviewed | `lem:con:chart` (roots, smoothness, derivative bounds `Pi_1..Pi_3`, oracle), `lem:con:approx`, `lem:con:approx-closure`, `def:con:charted`, evaluation in the proof of `thm:con:graph` (I); weak separator with approximate oracle is part of `lem:sp:gls`. |
| `new-direction/smoothed-polynomial-actuator-dynamics.md` | complete, reviewed | `def:con:actuator`, `thm:con:actuator`, eq. `eq:con:adjoint`, `eq:con:Lact`, `ex:con:actuator`, Appendix D proof. Horizon renamed `N` (the source's `H` clashes with Hessian notation). |
| `reviews/stable-dynamics-bag-obstruction.md` | complete obstruction | `ex:con:dyn` (predecessor fibers) and the lost-sparsity remark after `thm:con:actuator`. |
| `new-direction/simplex-block-smoothed-extension.md` | complete, reviewed | `thm:con:simplex`, `lem:con:simplex-round`, `lem:con:simplex-count`, `lem:con:simplex-close`, `lem:con:simplex-tail`; equality-block rule changes kept; ambient-box derivative bounds kept. |
| `new-direction/smoothed-mixed-order-polynomial.md` | complete, reviewed | Main order result: `thm:con:order`, `lem:con:transport`, `prop:con:order-count`, `ex:con:premature`. |
| `new-direction/smoothed-sparse-order-polynomial.md` | complete, reviewed | Superseded by `thm:con:order` with `n_z=0` (sharper count). Its LP closure, finite schedule and evaluation are in `lem:con:lpgap`, `lem:con:order-close`, `lem:con:order-tail` and the Appendix D proof. |
| `new-direction/order-polytope-cell-count.md` | complete lemma | Superseded by the transport count; the affine-fiber chamber argument is not reproduced. Its projection and face-grid counts reappear inside `prop:con:order-count`. |
| `new-direction/order-polytope-face-closure.md` | complete lemma | `lem:con:order-vertices`, `lem:con:lpgap`, `lem:con:order-tail`, weighted test in `lem:con:order-close`, predecessor repair in the proof of `thm:con:order`. |
| `new-direction/tu-feasible-rounding.md` | developed lemma, no theorem | Preliminary for this paper. Stated without a theorem in `sec:con:scope` (aligned rounding via Hoffman–Kruskal). No TU optimization theorem is claimed. |
| `new-direction/tu-polyhedral-cell-count.md` | local count, preliminary | Not used. Its constant `C_b` is unestimated, it relies on the separate polyhedral-chamber note, and it has no closure, tails or algorithm. `sec:con:scope` states only that no input-controlled count for general TU systems is provided. |
| Reviews read | — | `sparse-bag-cell-review.md`, `sparse-bag-cell-noise-review.md`, `sparse-mixed-bag-cell-review.md`, `sparse-mixed-bag-noise-review.md`, `smoothed-sparse-polynomial-independent-review.md`, `simplex-block-noise-review.md`, `order-polytope-independent-review.md` (all in `new-direction/`); `reviews/smoothed-sparse-polynomial-review.md`, `smoothed-polynomial-graph-review.md`, `implicit-graph-tail-kkt-review.md`, `implicit-graph-oracle-review.md`, `implicit-graph-composition-review.md`, `smoothed-implicit-graph-composition-review.md`, `simplex-block-closure-review.md`, `smoothed-mixed-order-review.md`, `smoothed-polynomial-actuator-dynamics-review.md`, `global-error-cell-barrier-review.md`; and the prior-art audits for sparse QP, sparse polynomial, simplex, order, implicit/actuator and constrained MINLP. All corrections they record are in the text (GLS repair, trace size, full-hull chart premises, ambient-box derivative bounds for simplices, binary-before-exposure order, weighted versus unweighted order test). |

## 3. Incorporation of Sol's prewrite audit (`evidence/reviews/prewrite-sparse-sol.md`)

| Audit point | Where |
| --- | --- |
| One mixed polynomial box theorem, rational quadratic specialization, two graph reductions, product-simplex theorem, one continuous/binary order theorem, actuator as separate corollary | Structure of Sections 5–6 exactly. |
| Shared pruning proof: common partitions, fixed-cell rounding preserving all incident cells, one global witness, refine clipped intervals by the next common grid | `lem:sp:cells`, `lem:sp:round`, `prop:sp:prune`. |
| Sequential rounding needed beyond quadratics (`x^2y^2`) | Remark after `lem:sp:round`. |
| Copy bags to degree three; no subtraction of infinities | Paragraph before `lem:sp:dp` and its proof. |
| Count over the original outside domain; first-moment work bound; sorting overhead | `eq:sp:V`, `prop:sp:count`, proof of `thm:sp:main`. |
| Finite tails, intersection bound for active gradients, real-coefficient uniformity | `lem:sp:tails` citing `lem:count:finite-tails`(a),(b),(d). |
| Quadratic rational fallback and why it does not transfer to higher degree | `lem:sp:faces` and the remark after it. |
| Closure rules and output contract; trace versus descriptor; evaluation does not decide thresholds | `def:sp:closure`, `prop:sp:closure-sound`, `prop:sp:closure-stop`, outputs paragraph, `prop:sp:eval` and the paragraph after it. |
| GLS erosion and feasibility repair | `lem:sp:gls` proof. |
| Explicit graph: equality scopes in bags, running intersection, uniform constants, rational lifts, both counterexamples | `lem:con:expand`, `lem:con:uniform`, `thm:con:graph` (E), `ex:con:graph-curv`. |
| Implicit graph: global premises, certified lower costs, `1+n` factor, certified closure, KKT nonsingularity, original-domain fallback, implicit feasibility only | `lem:con:chart`, `lem:con:approx`, `lem:con:approx-closure`, `lem:con:kkt`, `thm:con:graph` (I). |
| Simplex: block Hessian, ambient-box derivative bounds, cube-corner vertices, face count, equality-block rules, tuple counting for dependent transformed noise, `Z'Z` metric, relative evaluator | `def:con:simplex` and its premise paragraph, `lem:con:simplex-round`, `lem:con:simplex-count`, `lem:con:simplex-close`, `lem:con:simplex-tail`, proof of `thm:con:simplex`. |
| Order: sharper transport count supersedes the continuous count; binary-before-exposure; `N`-Lipschitz gaps; sum-fiber counting; weighted versus unweighted test not mixed; propagation before fallback repair | `thm:con:order`, `lem:con:transport`, `prop:con:order-count`, `ex:con:premature`, `lem:con:lpgap`, `lem:con:order-tail`, `lem:con:order-close` and the remark after it, proof of `thm:con:order`. |
| Actuator: invariance, adjoint identity, unary terms, additive bit lengths, Lipschitz bound, exclusions | `def:con:actuator`, `eq:con:adjoint`, `thm:con:actuator`, Appendix D. |
| Dimension barrier must remain | `sec:sp:width` (cites `thm:lim:width`, `prop:lim:local`). |
| TU lemma and fixed-polytope result only as scope boundaries | `sec:con:scope`. The fixed-polytope chamber result is not stated, because it is not proved in the paper. |

## 4. Mathematical repairs and new developments

All were checked by hand derivation; details are in the proofs.

1. **Sharper order count, independently verified.** I reconstructed the
   endpoint-preserving transport (`lem:con:transport`): for a source tuple in
   the relative interior of a face of an order simplex, the piecewise-affine
   knot map is nondecreasing, fixes `0` and `1`, is affine in the target, and
   along a face edge direction moves exactly one interior group value at unit
   rate (the barycentric weight moves from `lambda_{l-1}` to `lambda_l`).
   Every coordinate then moves at rate `1-theta`, `theta` or `0`, so the
   directional curvature of the upper support is at most `n_c Lbar`. With the
   witness tolerance `2E_j = n_c Lbar h^2/4`, the interval length is
   `(3/2) n_c Lbar h`, and the face and permutation sums give
   `2^{z} c! (c+1) [2 + 3 n_c Lbar/(4 sigma)]^c`. The continuous case
   `n_c=n`, `c=p` gives `C_0^p p! (p+1) [2+3nH/(4 sigma)]^p poly(I)` as stated
   in the brief. It replaces the older bracket `[2+nH(p+1)/(2 sigma)]^p`.
2. **Weighted order closure test.** `lem:con:order-close` uses
   `D'Hess D - (kappa_3 r_y + g_0) D'D`, which removes the factor `n_c` from the
   curvature term of the stopping depth (`g_0/(4 kappa_3 A)` instead of
   `g_0/(4 n_c T A)`) and measures distance in original coordinates. I also
   proved directly that after bound propagation, cycle contraction and
   singleton removal the order patch is full-dimensional, which removes the
   need for an LP affine-hull computation and is what makes the patch lie in
   the optimizer's smallest face on the good event.
3. **Fallback interface repair.** `thm:count:fallback` (Appendix A) accepts
   only linear tilts of a fixed base instance. The graph (E) and actuator
   sources applied a fallback to the reduced polynomial, whose coefficients
   depend nonlinearly on the dependent-state noise, by appeal to a
   format/height argument for arbitrary coefficients. The paper instead runs
   the fallback on the original constrained domain with the ambient linear
   tilts on all coordinates (`lem:con:uniform`(b) and the paragraph after it;
   Appendix D proofs). Minimizers correspond through the chart or recurrence.
   This matches the cited interface exactly and needs no extension of it.
4. **Uniform-schedule lemma** `lem:con:uniform` makes explicit what the
   conditional reductions need: curvature and derivative bounds valid for every
   member, format-only tail constants, and a base-only fallback factor, all
   fixed before any noise is drawn.
5. **General evaluation lemma** `lem:sp:gls` unifies five evaluator variants
   (box, simplex relative polytope, order block polytope, implicit graph with
   approximate values and gradients, and recourse use in Appendix E). It
   handles lower-dimensional patches through a rational affine
   parameterization, approximate oracles through a widened lower plane, and
   repairs nonexpansive in `||.||_2` or `||.||_inf` with dual gradient norms.
6. **Implicit KKT tail with complex zeros.** `lem:con:kkt` defines the shift
   `b_rho` for every nonsingular zero, real or complex, so that the slab bound
   does not presuppose real zeros; the reduced-gradient identity is used only
   at the zero coming from the graph point.
7. **Simplified incumbent in the implicit DP.** `lem:con:approx` updates the
   incumbent with `m_j + E_j` (the summed error `D_j` equals `E_j` for
   `delta_j = E_j/N_bags`), still giving witnesses within `4E_j`.
8. **Corrected chart Lipschitz constant.** `K_psi = 1 + sum_j |S_j| Pi_{1,j}`,
   justified by `||grad psi_j||_2 <= sqrt(|S_j|) Pi_1 <= |S_j| Pi_1`.
9. **Simplex inner radius.** Explicit rational radius
   `min{1/2, min_s sigma_s/(k ||alpha_s||_1)}` in tangent coordinates, using
   that every coordinate of `Zt` is `t_i` or minus a sum of them.
10. **Notation alignment** with the model and boundaries sections: grid law
    `U_{sigma,M}`, bags `beta`, allowed grid `A_j`, hull `Q`, patch box `P`,
    `kappa_2`, `kappa_3` for derivative row sums, `N_Z` for the number of
    integer assignments.

No defect that defeats the topic was found. All theorems of the assigned
sources survive under their stated premises.

## 5. The required distinctions

- **Fixed law.** Every theorem uses the ambient model with marginal
  `U_{sigma,M}`, `M` a base-computed power of two, chosen last in the order
  `B -> rho, g_0, tau -> J -> M` (`def:sp:schedule` and its analogues). No
  theorem is claimed for an arbitrary or coarse finite law.
- **All-draw exactness.** Closure outputs are sound on every draw
  (`prop:sp:closure-sound` and analogues); remaining draws use
  `thm:count:fallback` on the same draw; no resampling.
- **Expected work.** Bounded through deterministic full-grid counts
  (`prop:sp:count`, `lem:con:simplex-count`, `prop:con:order-count`); the
  fallback is paid by `lem:count:rare-fallback`(a).
- **Implicit outputs.** Patch and charted outputs denote a unique point by a
  verified modulus; the global proof record is separate and has only an
  expected size bound; evaluation is `poly(I+q)` and decides no thresholds. For
  implicit graphs no rational feasible point is promised.
- **Numerical parameters.** `L w_max/sigma`, `n` inside the bracket, numerical
  integer widths, `Lbar`, `n_c`; all bounds are fixed-width polynomial, never
  described as fixed-parameter in width.
- **Value accuracy versus distance.** Paragraph after `prop:sp:eval`; distance
  conversions use the verified modulus.
- **Regret on the original objective.** Cited `prop:model:regret` with
  `omega_X(gamma) <= sigma W` after `thm:sp:main`.

## 6. Interfaces and requests to the root

1. **Model output format (b).** `def:model:outputs`(b) lists fixed values as
   "native integer labels and original continuous bounds". My patches may
   also fix a continuous coordinate whose intersected hull is a single grid
   value. Please allow "or values forced by a degenerate hull interval" there.
2. **Model output format (c).** `def:model:outputs`(c) describes a primitive
   element `theta` with polynomial maps. `thm:count:fallback` returns one root
   representation per coordinate of the lexicographically least minimizer and
   states that no primitive element is required. My sections refer to "the
   algebraic output of `thm:count:fallback`". The model definition and the
   fallback theorem should be reconciled by their owners.
3. **`thm:count:fallback`(iii)** gives a feasible rational approximation only
   for mixed boxes. My appendices supply the repairs for simplices (blockwise
   projection), order polytopes (propagation and predecessor maxima) and
   graphs (lift through the chart), so no change is needed, but the root may
   want to mention these repairs next to the theorem.
4. **`lem:count:finite-tails`** is used in the generality it states (reduced
   objective `f(x)=min_y F(x,y)` with noise on `x`), which covers implicit
   graphs; the margin variants are mine.
5. **External labels used** (all exist now): `def:model:grid`,
   `eq:model:interval`, `def:model:perturbation`, `def:model:outputs` with
   `it:model:implicit` and `it:model:charted`, `prop:model:regret`,
   `ex:model:tie`, `sec:model:input`, `sec:model:parameters`,
   `def:count:growth`, `def:count:semialg`, `thm:count:local`,
   `thm:count:cells`, `thm:count:growth-tail`, `lem:count:finite-tails`,
   `thm:count:fallback`, `lem:count:rare-fallback`, `thm:lim:width`,
   `prop:lim:local`, `thm:lim:constraints`, `ex:lim:coupled`,
   `prop:lim:threshold`, `sec:rec`.
6. **My labels used by others** (all exist): `lem:sp:gls`, `lem:sp:bezout`,
   `lem:sp:faces` (Appendix E, Section 7); `thm:sp:main`, `def:sp:algorithm`,
   `def:sp:schedule`, `sec:sp:width`, `sec:sp`, `sec:con` (Sections 1, 9);
   `thm:con:graph`, `thm:con:actuator`, `thm:con:simplex`, `thm:con:order`
   (Section 1). Their uses match the statements; `thm:lim:width` uses
   `g_0 <= sigma/(8W)`, which holds because `B >= 2` gives `rho <= 1/8`.
7. **Citation key style.** The manuscript mixes KB slugs (Appendix A,
   Section 3) and CamelCase keys (Sections 7, 9). I used KB slugs. The root
   should choose one style.
8. **Macros.** None requested; I used standard LaTeX and the existing macros.

## 7. Reference keys (for Luna verification)

| Key | Identity | Use and locator to verify |
| --- | --- | --- |
| `grotschel1988-geometric-algorithms-and-combinatorial-optimization` (KB) | Grötschel, Lovász, Schrijver, *Geometric Algorithms and Combinatorial Optimization*, Springer 1988 | Definitions of weak separation and weak optimization (§2.1, Definition 2.1.10), Corollary 4.2.7, oracle Turing conventions (§§1.2–1.3, 4.1); `lem:sp:gls`, `prop:sp:eval`. |
| `kozlov1980-the-polynomial-solvability-of-convex` (KB) | Kozlov, Tarasov, Khachiyan, "The polynomial solvability of convex quadratic programming", USSR Comput. Math. Math. Phys. 20(5), 1980 | Exact rational solution of convex QP in polynomial time; `cor:sp:qp`. |
| `pia2026-treewidth-and-the-complexity-of` (KB) | Del Pia, Khajavirad, box-constrained QP and treewidth (2026) | Exact polynomial algorithm on forests; strong NP-hardness at treewidth two; after `cor:sp:qp` and in `sec:sp:prior`. Same paper as `DelPiaKhajavirad`/`DelPiaKhajavirad2026Forest` used by Sections 7 and 9. |
| `adjiman1998-a-global-optimization-method-bb` (KB) | Adjiman, Dallwig, Floudas, Neumaier, αBB, Comput. Chem. Eng. 1998 | Maximal separation `L w^2/8` with `alpha = L/2`; `sec:sp:prior`. |
| `lee2017-generic-properties-for-semialgebraic-programs` (KB) | Lee, Phạm, SIAM J. Optim. 2017, Theorem A | Generic uniqueness and growth under linear tilts on regular compact semialgebraic sets, qualitative; `sec:sp:prior`. |
| `beier2006-typical-properties-of-winners-and` (KB) | Beier, Vöcking, typical properties of winners and losers | Isolation in smoothed discrete optimization; `sec:sp:prior`. |
| `roglin2007-smoothed-analysis-of-integer-programming` (KB) | Röglin, Vöcking, Math. Program. 2007 | Same. |
| `bienstock2018-lp-formulations-for-polynomial-optimization` (KB) | Bienstock, Muñoz, SIAM J. Optim. 2018 | Treewidth-based LP approximations with accuracy-dependent size; `sec:sp:prior`. |
| `stanley1986-two-poset-polytopes` (KB) | Stanley, Discrete Comput. Geom. 1986 | Zero-one vertices; triangulation by order simplices; `sec:con:scope`. |
| `bach2018-efficient-algorithms-for-non-convex` (KB) | Bach, NeurIPS 2018 | Common-quantile coupling for isotonic constraints; `sec:con:order`, `sec:con:scope`. |
| `wilhelm2019-global-optimization-of-stiff-dynamical` (KB) | Wilhelm, Le, Stuber 2019 | Implicit state elimination within validated global dynamic optimization; `sec:con:scope`. |
| `fulton1998-intersection-theory` (used by Appendix A; not in `literature/papers`) | Fulton, *Intersection Theory*, 2nd ed., Springer 1998 | Refined Bézout inequality, Example 8.4.6 (locator to verify); `lem:sp:bezout`. |
| `kloks1994-treewidth-computations-and-approximations` (new, not in KB) | Kloks, *Treewidth: Computations and Approximations*, LNCS 842, Springer 1994 | Binarization (nice tree decompositions) without increasing width; before `lem:sp:dp`. |
| `bertele1972-nonserial-dynamic-programming` (new, not in KB) | Bertelè, Brioschi, *Nonserial Dynamic Programming*, Academic Press 1972 | Classical tree-decomposition DP; after `lem:sp:dp`, `sec:sp:prior`. |
| `hoffman1956-integral-boundary-points-of-convex` (new, not in KB) | Hoffman, Kruskal, "Integral boundary points of convex polyhedra", in *Linear Inequalities and Related Systems*, Ann. Math. Stud. 38, 1956 | Integral vertices of TU systems; `sec:con:scope`. |

Novelty statements to confirm or soften: the last sentences of `sec:sp:prior`
and of `sec:con:scope` ("The new element ... is the composition ..."). They
rest on the scoped prior-art audits for the sparse QP, sparse polynomial,
simplex, order and implicit/actuator results, which found no source with the
full composition but are not exhaustive. No priority is claimed for any
ingredient.

## 8. Targeted checks actually run

1. Standalone compile of only my four files, outside the repository:
   `/tmp/sp-check/wrap.tex` with the preamble of `main.tex` and `macros.tex`,
   compiled with `pdflatex -interaction=nonstopmode -halt-on-error wrap.tex`
   (several passes). Result: no errors; no overfull boxes after two fixes; one
   too-tall table fixed; 38 pages. Undefined references in this wrapper are
   exactly the external labels of §6.5, and undefined citations are expected
   because `references.bib` does not exist yet.
2. Inline Python scan over `sections/*.tex` and `appendices/*.tex`: no
   duplicate labels; every `\ref`/`\cref`/`\eqref` in my four files resolves
   to a label in the current sources; every external use of my labels resolves.
3. Inline Python scan of my four files: no internal development paths, no
   unfinished markers, balanced environments, no trailing whitespace, final
   newlines present.

Not run: a full manuscript build, `verification/check_sources.py`,
project-wide verification, CI inspection, any experiment or proof fixture.
These checks are local and targeted; they are distinct from CI results.

## 9. Open items

- The evaluation lemma's GLS citation and the Bézout locator need Luna's
  confirmation.
- Sections 7 and 9 cite the treewidth box-QP paper under different keys;
  the root should unify keys with mine.
- If the root prefers an unweighted order test for uniformity with other
  sections, the stopping depth must use `g_0/(4 n_c kappa_3 A)`; the remark
  after `lem:con:order-close` records this.
