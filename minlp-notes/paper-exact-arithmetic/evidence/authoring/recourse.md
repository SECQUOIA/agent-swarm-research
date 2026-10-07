# Author report: recourse (Section 10 and Appendix I)

Author: recourse writer (Opus). Date: 2026-10-05.

## Files written

- `sections/10-recourse.tex` (617 lines): Section 10, "Core noise: values,
  selected cores, and full recourse points", label `sec:recourse`.
- `appendices/I-recourse.tex` (about 1,900 lines): Appendix I, "Proofs for
  core noise and recourse", label `app:recourse`.

No other file was edited. Standalone compilation of the two files gives
29 pages (about 12 main, 17 appendix).

## Coverage (coverage-map IDs)

Under decision D1, the full expected-work chain is proved in Appendix I.
No claimed theorem is conditional on an unproved selected-core oracle,
and no proof is delegated to a repository note.

| ID | Where stated | Where proved |
| --- | --- | --- |
| V1 value Cauchy oracle, product box, every core dimension | `thm:recourse-core` (type B, value part) | I.4 cells, I.5 all-scale count, I.2 finite law, I.3 fallback, I.7 |
| V2 selected lexicographic core, retained hull | `thm:recourse-core` (core part) | I.6 growth tail, I.7 (hull, terminal depth, failure event, work) |
| V3 coupled polytope with supplied convexifier alpha | `thm:recourse-core` (type P) | type-P cell oracle in `lem:recourse-cell-oracle`; same count, growth, and fallback lemmas |
| V4 joint convexity, no inverse-noise factor | `cor:recourse-joint` | I.8 |
| V5 exact rational QP output | `cor:recourse-qp` | I.9 (`lem:recourse-qp-height`) |
| RQ1 cubic coupled completion, convexifier on X | `thm:recourse-convexified`(i) | I.10, I.11 |
| RQ2 globally convex convexifier, fixed degree; affine powers | `thm:recourse-convexified`(ii), `cor:recourse-affine-power` | I.10 (`lem:recourse-bregman`), I.11 |
| RQ3 residual-convex cubic, product box, no convexifier (central) | `thm:recourse-cubic`, with `lem:recourse-face`, `lem:recourse-lattice`, `prop:recourse-margin-probability`, `prop:recourse-completion` | I.12--I.16 |
| RQ4 fixed face kernels, conditional bound, obstructions | `prop:recourse-fiber`, `prop:recourse-examples` | I.12 |
| k<=2 growth-only count (historical, sharper factor) | sketch in `rem:recourse-low-dim` | remark only; not used by any theorem |
| Degree-four barrier under core noise | `rem:recourse-quartic` | proof at end of I.16; conditional on `thm:points-quartic-lower` |

Section 10 explains why these results belong to the output account:
a single finite rational law fixed before any accuracy request, correctness
on every draw with exact real-algebraic fallback under the same selector,
and a sharp separation between values, selected cores, and full points.
Unrelated sparse/treewidth smoothed algorithms are not included.

## Labels defined

Main text: `sec:recourse`, `sec:recourse-model`, `sec:recourse-core`,
`sec:recourse-convexified`, `sec:recourse-cubic`, `sec:recourse-scope`,
`def:recourse-instance`, `thm:recourse-core`, `eq:recourse-core-output`,
`cor:recourse-joint`, `cor:recourse-qp`, `thm:recourse-convexified`,
`cor:recourse-affine-power`, `prop:recourse-fiber`,
`prop:recourse-examples`, `thm:recourse-cubic`, `lem:recourse-face`,
`lem:recourse-lattice`, `prop:recourse-margin-probability`,
`prop:recourse-completion`, `rem:recourse-quartic`,
`rem:recourse-value-certificate`.

Appendix: `app:recourse` and `app:recourse-{tools,sections,fallback,cells,
count,growth,core-proof,joint,qp,analytic,convexified,fiber,face,lattice,
margin,cubic-proof}`; `thm:recourse-qe`, `thm:recourse-univariate`,
`thm:recourse-lll`; lemmas `lem:recourse-{sections,replacement,
selected-point,fallback,cell-oracle,refinement,simplex,cell-count,conjugate,
vitali,weak-tail,count-formula,growth,qp-height,hoffman,transverse,bregman,
selection,relative,surrogate,convexified-error,minor-heights,sublevel,
contact}`; `cor:recourse-face-rules`, `cor:recourse-margin-union`,
`rem:recourse-low-dim`; equations `eq:recourse-{cv,two-block,H,singleton,
cell-oracle,growth,core-params,core-tails,accepted-bound}`.

The architecture proposed `thm:recourse-completion`; I used
`prop:recourse-completion` because it is a deterministic certification
statement relative to the core evaluators.

## Shared labels consumed (owners must define them)

| Label | Owner | Use and required contract |
| --- | --- | --- |
| `sec:models` | framing | Output contracts referred to in the opening paragraph. |
| `lem:convex-value` | points | Used as stated in (I.1, eq. `eq:recourse-cv`): explicit rational polyhedron Q in a supplied box, possibly empty or lower-dimensional; explicit rational polynomial of degree <= D convex on Q only; given rational eta, decide emptiness or return rational feasible x and **a rational certified lower bound ell** with ell <= min_Q phi <= phi(x) <= ell+eta, in P_D(L_Q+log(2+1/eta)). The lower bound is essential (cell pruning, V4 probes). If the points lemma states only a value-gap point, please add the lower bound, which the weak-optimization argument already produces. |
| `lem:integer-hoffman`, `lem:selector`, `lem:points-cubic-transverse`, `lem:points-cubic-slice` | points | Cited only as the shared versions. Appendix I includes self-contained forms it needs: real rows with a supplied nonzero-minor margin (`lem:recourse-hoffman`), real-coefficient cubic transverse/slice with a center in the domain (`lem:recourse-transverse`), and selection with an inexact objective and general exponent (`lem:recourse-selection`). Root may dedupe if the points versions cover these exact forms (real coefficients; margin mu; error exponent 1/D_e; perturbed objective). |
| `thm:cubic-point` | points | k=0 case of `thm:recourse-cubic`; cited for the case-(i) mechanism. |
| `thm:global-point` | points | Cited for the case-(ii) mechanism. `lem:recourse-bregman` restates the needed gradient-row estimate for **real** coefficients with majorants (the surrogate has an unknown irrational linear term), with full proof. |
| `thm:points-quartic-lower` | points | `rem:recourse-quartic` and a consistency comment after `cor:recourse-joint`. Requires: box-convex quartic on a unit box, unique minimizer, designated coordinate 0/1 by the source predicate, one query at distance 1/4. |
| `prop:points-active` | points | Scope sentence on exact active labels. |

## Macros

No new macros are required. The files use only `macros.tex` plus
standard `amsmath/amssymb` (`\operatorname{...}`, `\mathfrak d`,
`\mathcal`, `\vartriangleright`, `\mathsf T`, `\textsc`). Optional
conveniences if root wants them globally: `\relint`, `\Leb`.

## Citation keys

Already in `references.bib`: `LenstraLenstraLovasz1982`,
`GroetschelLovaszSchrijver1988`, `KozlovTarasovKhachiyan1980`,
`KannanRademacher2009`.

Proposed new keys for Luna (with the pinpoints I used; please verify or
correct):

| Key | Source (KB id if known) | Use and pinpoint |
| --- | --- | --- |
| `Renegar1992QE` | Renegar, J. Symbolic Comput. 13(3):329--352 (KB `renegar1992-on-the-computational-complexity-and`) | `thm:recourse-qe`, Theorem 1.1. Root reports Luna verified the fixed-block output format (counts, degrees, integer coefficient height) and sequential bit cost tau log tau loglog tau (md)^{2^{O(omega)} prod n_i}; for one free variable and two blocks this is exactly the contract stated, with H=(sd)^{c(n_1+1)(n_2+1)}. Part (a) is used with real coefficients (other noise values and thresholds); please confirm the structural bound for real coefficients (real-number model, or BPR Ch. 14). |
| `BasuPollackRoy2006` | Algorithms in Real Algebraic Geometry (KB `basu2006-algorithms-in-real-algebraic-geometry`) | Chapter 14 (block quantifier elimination, cross-reference); Chapters 8 and 10 for `thm:recourse-univariate` (squarefree part, real-root isolation, sign determination, refinement in bit work polynomial in degree, height, number of polynomials, and q, absolute exponent). Please verify chapter pinpoints. |
| `Rockafellar1970` | Convex Analysis | Theorems 23.4, 23.5, 25.1, 25.5 in (F1). |
| `EvansGariepy2015` | Measure Theory and Fine Properties of Functions, revised ed. | Section 2.4: Hausdorff measure under Lipschitz maps and H^k = L^k (F2); also cited for covering arguments. A self-contained bounded-radius Vitali proof is included (`lem:recourse-vitali`). |
| `AndroulakisMaranasFloudas1995` | alphaBB global optimization (J. Global Optim. 1995) | Credit for the secant underestimator in type (P). |
| `Hoffman1952` | Hoffman, approximate solutions of linear inequalities | Credit for Hoffman bounds. |
| `Schrijver1986` | Theory of Linear and Integer Programming | Continued fractions and Legendre's theorem for rational reconstruction (V5). |
| `SpielmanTeng2004` | Smoothed analysis of algorithms | Context only. |

The sentence on `KannanRademacher2009` was made conservative: "optimize a
convex objective plus a low-dimensional polynomial perturbation to a
prescribed objective accuracy". Please check that characterization.

## External theorem contracts used

1. Block quantifier elimination (`thm:recourse-qe`): verified by Luna per
   root message. This contract carries both the scalar-section counts and
   the base-only fallback factor; a general doubly exponential CAD bound
   would not suffice, and the text says so.
2. Univariate real algebraic numbers (`thm:recourse-univariate`).
3. LLL inequality ||b_1|| <= 2^{(s-1)/2} lambda_1, polynomial time.
4. Rational LP (feasibility and basic solutions) in polynomial bit time;
   exact convex QP (KTK 1980) for V5 only.
5. Analytic facts (F1)--(F3): a.e. differentiability of convex functions,
   subgradient/Fenchel facts, Lipschitz image measure; descent lemma
   (proved inline).

## Responses to prewrite audits

`prewrite-points.md` (cubic recourse part and blockers 4--5):

- Curvature symbol: Lambda throughout; L is input length.
- Output contracts kept separate (value interval, selected core, fixed
  full selector, not expanded algebraic output, not the unperturbed
  instance).
- Blocker 4 resolved: retained hull containing every optimal core and the
  incumbent (`lem:recourse-refinement`), terminal depth, single
  growth-failure event, same-selector fallback, conditional fiber bound
  (`prop:recourse-fiber`(c) with full proof), and finite-section constants
  are all proved in Appendix I.
- Blocker 5: the exact two-block elimination contract is stated as
  `thm:recourse-qe` and flagged for Luna (now verified per root).
- Nested linear-size `LexGT` with 2k-1 atoms is used in the singleton
  formula (`lem:recourse-selected-point`), which encodes global
  optimality, lexicographically least core, and least residual norm.
- The lattice success condition uses the enlarged height R_s, and the
  union bound uses R=2^{s_*}4s_*B over all free dimensions.
- Parameter order (fallback factor, t, eta, T, then M) is explicit; the
  grid satisfies all 2k+1 baselines' lower-bound requirements and the
  margin/face budget.

`prewrite-core-noise-chain.md`: every listed obligation is proved in
Appendix I: cell/pruning correctness (I.4), maximum-simplex/conjugate
weak-(1,1) count (I.5, with `lem:recourse-vitali`), polynomial-size QR
strict-event encoding (`lem:recourse-count-formula`), hybrid finite-law
replacement (I.2), separated-height same-selector fallback (I.3),
expanding-map projected-growth tail (I.6, the shorter uniform proof the
audit recommends), retained hull and cap/work bookkeeping (I.7), V3--V5,
RQ1--RQ2, and the RQ3 composition (I.16). Deviations, all intentional:

1. **Unified count.** Both types use whole-cell packing with padding
   [-h,h]^k (retained cells <= 2^k W, generated <= 4^k W). The Fenchel
   residual bound becomes 2 kappa_+ k h^2 and the gradient ball radius
   2 kappa_+ sqrt(k) h < 4 kappa_+ k h, so a_k=(180k^3)^k(1+kappa_+/sigma)^k
   is unchanged. This removes the separate node-count argument for boxes.
2. **V4 simplified.** Coordinate enclosures use 2k binary searches whose
   probes are convex value queries on X intersected with {v_i >= theta} or
   {v_i <= theta}. A probe that "succeeds" (empty or lower bound > U) is a
   sound exclusion; a failing probe returns a near-optimal witness. No
   monotonicity is needed. This avoids the buffered-sublevel inner-ball
   and weak linear optimization over a nonpolyhedral body, and uses only
   `lem:convex-value`. Constants: delta=min(eps, g_0 eps^2/(128k)),
   zeta=eps/(8k).
3. **V5 fallback.** The QP-specific face-enumeration fallback is not
   needed: the selected-core evaluator returns short rationals even on its
   fallback branch, and its cost is already charged to its random factor.
   Reconstruction is applied only to that short output. Only the core is
   reconstructed; the value follows from one exact convex QP on the fiber.
4. **Face-rule probability** is kt/sigma+2k/M (each interval of length t
   has grid mass <= t/(2sigma)+1/M), slightly sharper than the source.
5. **Minor heights.** Delta=d^m, B=d^m m! C_0^m with
   C_0=max{d, ceil(6 d sum|f_nu|)}; C_0 >= d also covers the identity rows.
6. **Selection lemma** is stated once for a general error exponent D_e,
   with tau=e^{2D_e-2}/(2^{3D_e-2} R^{D_e} Gamma^{D_e}); D_e=4 gives the
   source constant 1024.

No mathematical error was found in the sources. One presentation repair:
the source's RQ2 transfer relied on the global-point note's internal
interpolation steps; `lem:recourse-bregman` now proves the needed
real-coefficient estimate directly.

## Not claimed (stated in Section 10)

Coupled domains without a convexifier; degree-four residual completion
(conditional barrier in `rem:recourse-quartic`); the unperturbed
objective; exact active labels or expanded algebraic coordinates;
optimality of the k^{O(k)} factor. These are suitable for Section 11's
open problems.

## Blockers and requests to root

- No mathematical blocker.
- Points writer: confirm `lem:convex-value` returns the certified lower
  bound described above.
- Luna: verify the pinpoints listed in the citation table, especially
  BPR chapters and real-coefficient use of Renegar's structural bound.

## Verification actually run

- Read-only inspection of sources and audits with `cat`, `sed`, `grep`,
  `wc`.
- Targeted standalone compilation of only these two files in a temporary
  wrapper outside the repository (`/tmp/recourse-test/test.tex`, using the
  manuscript's package list and `macros.tex`), run twice with
  `pdflatex -interaction=nonstopmode -halt-on-error`: exit 0, no LaTeX
  errors, no overfull boxes, 29 pages. Undefined references were only the
  shared labels owned by other writers (listed above); citations were
  undefined because the test used no bibliography.
- Two rendered pages were inspected visually.

No experiments, mathematical script reruns, project-wide checks, or CI
inspection were performed. Compilation checks the document, not the
mathematics.
