# Values, points, and exact comparisons in polynomial optimization

This is the completed development and review package for topic 2. The
[integrated report](document/main.pdf) brings the earlier results and the new
extensions into one document; its [LaTeX source](document/main.tex) and complete
companion proofs are included. The program is complete as a research
deliverable. The unrestricted constrained exact-comparison question remains
open, so this is not a claim that every mathematical extension is solved.

The organizing distinction is the required output: an objective gap,
distance to the optimizer set, approximation of one fixed optimizer, exact
comparison, or an exact representation. These tasks can have different
complexities even for convex quartics. Ordinary binary arithmetic, shared
arithmetic circuits, and computation with a PosSLP oracle are stated
separately throughout.

## Results developed in this continuation

Every result below has a saved proof and an internal independent review.
Internal review is not external peer review. Publication priority is not
established.

| Result | Guarantee and main assumptions | Proof and review |
| --- | --- | --- |
| Global point oracle on arbitrary rational polyhedra | For explicit sparse globally convex polynomials, `poly(I,D,q)` feasible approximation of the fixed minimum-Euclidean-norm optimizer. Includes infeasibility, unboundedness, finite attainment, a computable radius, and a global distance bound. Dependence is on numerical degree `D`. | [Theorem](global-point/theorem.md); [point review](reviews/point-core/global-extension-review.md); [radius review](global-point/radius-independent-review.md) |
| Full cubic recourse without joint core convexification | Residual-convex cubics on product boxes admit one finite core-noise law and one selected full optimizer for all precisions, with expected work `f(k)(1+L/sigma)^k poly(I+q)`. All draws are correct; rare draws use a same-selector exact fallback. | [Theorem](cubic-recourse/theorem.md); [review](reviews/cubic-extension/review.md) |
| Exact comparison parameterized by nonlinear dimension | Globally strongly convex quartics over arbitrary rational polyhedra admit ordinary deterministic FPT exact comparison and active-set recovery in the dimension of the cubic/quartic part. Includes a mixed-integer corollary parameterized by nonlinear plus integer dimension. | [Theorem](constrained-exact/theorem.md); [review](constrained-exact/independent-review.md) |
| Structured constrained exact comparison | `P^PosSLP` for boxes with forest, Stieltjes, or positive definite comparison-matrix Hessians; and for separable strongly convex polynomial network flows. Constraint rank is unrestricted. Infinite bounds and every fixed degree are covered. | [Box/transfer theorem](constrained-exact/structural-newton.md), [review](constrained-exact/review-structural-newton.md); [flow theorem](constrained-exact/network-flow.md), [review](constrained-exact/network-flow-review.md) |
| Variable-degree unconstrained exact upper bound | Each exact sign/equality predicate reduces to one PosSLP instance for explicit sparse globally strongly convex polynomials with unary degree bounds and supplied curvature. Polynomial observables are included. | [Theorem](reviews/exact-core/general-degree/strong-convex-polynomial-posslp-upper.md); [review](reviews/exact-core/general-degree/general-degree-review.md) |
| Short circuit representations of interior Grams | A full rational positive definite Hessian Gram for a quartic allows polynomial-time construction, without a sign oracle, of a shared rational-circuit Gram that is positive definite exactly when the global minimum is positive. | [Theorem](reviews/exact-core/general-degree/circuit-interior-gram.md); [review](reviews/exact-core/general-degree/circuit-interior-gram-review.md) |

Here `I` includes every supplied rational coefficient, constraint, and
structural parameter. In the cubic result, `k` is core dimension, `L` is
the supplied upper coordinate curvature, and `sigma` is noise amplitude.
The polynomial exponent is absolute; `f` is a computable parameter-only
factor. No lower residual-curvature bound is assumed.

## Earlier results audited and integrated

The report includes the domain-convex cubic point theorem and the quartic
point reductions from
[October 2](../research-20261002/new-direction/convex-cubic-polytope-point-oracle.md),
with a fresh [positive-result review](reviews/point-core/review.md) and
[hardness review](reviews/point-core/hardness-audit.md). The quartic reductions
are conditional implications from Sum-of-Square-Roots or PosSLP; they are
not claims of NP-hardness or proved separations from P.

The [exact-core audit](reviews/exact-core/review.md) integrates September 27's
certified strongly convex quartic sign completeness, rational-optimizer
coordinate hardness, an irrational unique optimizer at rational minimum
zero, and expanded rational witness/positive definite Gram lower bounds.
The report keeps strict and non-strict comparisons separate from equality,
and positive definite Grams separate from arbitrary positive semidefinite
Grams. These historical results were checked, not relabeled as new work.

## Literature and implementation

The [source audit](literature/source-audit.md),
[exact-arithmetic comparison](literature/exact-prior.md), and
[constrained comparison](literature/constrained-prior.md) reconcile the
results with prior work. In particular, *Hesse's Redemption* already gives
value-gap optimization, effective radii, and structural decompositions.
Essential-variable extraction, error-bound theory, proximal Newton
convergence, and the structured quadratic solvers are also credited.

The [source ledger](literature/source-ledger.md) identifies inspected
versions. Yang's full primary text and the proceedings version of *Hesse's
Redemption* were not accessible. No novelty claim is based on their absence,
and no novelty is claimed for the degree-based error exponent. The source
formula diagnostics concern proof transfer, not a claimed refutation of the
external main theorems.

The [reference implementation](implementation/README.md) checks exact rational
witnesses for three separate output contracts: objective gap, distance to
the optimizer set, and distance to the fixed minimum-norm optimizer. It
derives lower bounds and error constants from checked data. It is a sound
but incomplete witness checker for a certified subclass, not an optimizer.
Its ten focused tests and deterministic demonstrations are reproducible.

## Remaining questions and precise limits

The most substantial remaining question is deterministic `P^PosSLP` exact
comparison for an unrestricted globally strongly convex quartic over an
arbitrary rational polyhedron. The
[boundary analysis](constrained-exact/general-boundary.md) isolates what the
current Newton proof needs: exact quadratic subproblems with a polynomial
arithmetic operation count when their Hessians are circuit-encoded. General
polynomial-bit QP algorithms do not supply that interface. The new low
nonlinear-dimension, box, and flow results cover useful alternatives without
claiming the unrestricted conclusion.

Other exclusions are arbitrary coupled domains or degree four in the cubic
recourse theorem; exponentially large binary degree or circuit polynomial
input in the global point theorem; a matching equality-hardness theorem;
and ordinary polynomial-time validation of compact exact Grams. The
reference checker does not implement the general algorithms in the proofs.

## Verification and files

[VERIFICATION.md](VERIFICATION.md) records targeted commands and actual
outcomes. It separates finite diagnostics from proof review and reports no
project-wide checks or CI results. [PROGRAM.md](PROGRAM.md) records the scope
and completion standard; [PROGRESS.md](PROGRESS.md) records the research
decisions and closeout.

Build the document from its own directory:

```sh
cd research-20261003-arithmetic/document
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Keep the PDF in `document/` so that its relative links to companion proofs
resolve. The bibliography is included in the source tree. Build intermediates
are ignored. The local reference checker has no third-party dependencies;
some mathematical diagnostics use SymPy.
