# Stage 7 independent review 02

Date: 2026-09-09. Reviewer: stage07_review02. No delegation or manuscript edits.
No other reviewers' reports were read.

## Verdict

**Accept after one minor attribution correction. No major issue identified.**
The new synthesis describes the proved theorem classes accurately. The accuracy-bit
construction, inverse approximation dependency, sharp response modulus, and upper
feasibility qualifications withstand this review. A close 2026 predecessor for the
response exponent should be credited before accepting this stage. It does not
invalidate the global algorithm or the moving-resource modulus.

This is the stage 7 synthesis review, not the separately required final whole-paper
review. I have not re-proved every boundary reduction or rerun the timing campaign.

## Inputs and independent verification

I read the supplied global AGENTS instructions and `literature/AGENTS.md`; no root
filesystem AGENTS.md was present. The immutable input was
`process/snapshots/stage07-round01`. Its SHA256.json hash is
`8291e480da66a12a69a046e702818c268420be847c4af81b324baca6868ce1b6`.
All 31 file hashes match. Evidence is in
`verification/stage07-review02/hash-check.json`.

I generated and read the stage 7 diff against stage06-accepted, including the new
abstract, all Section 1 prose, Section 4 and 6 attribution changes, all conclusions,
all new bibliography entries, README and coverage changes. I read the full
bibliography, README and coverage map. I read the full accuracy section and
Appendices B and C, rather than relying on the author's audit. I checked the other
introductory claims against their theorem statements, including exact semantics,
constant-Hessian degree, criterion-specific robustness, dense recovery, and
near-identity hardness/condition-dependent approximation.

An independent source-only build in `verification/stage07-review02/standalone`
uses just the 17 LaTeX/bibliography/figure/table inputs. `latexmk -pdf
-interaction=nonstopmode -halt-on-error -outdir=build main.tex` exits successfully,
producing 77 pages. The final main.log contains no warnings, undefined references
or citations, overfull boxes, or underfull boxes. The separate build.log preserves
all passes. I rendered and inspected the first page: the title, blank author area,
abstract, keywords and beginning of the introduction are legible and fit. I did not
visually inspect all 77 pages.

## Finding R02-1: credit the uniform-convexity response exponent predecessor

**Severity: minor. Locations:** `sections/01-foundations.tex`, recent first-order
literature paragraph; `appendices/c-quantitative-bounds.tex`, paragraph preceding
`prop:accuracy-response-modulus`; `references.bib`.

Wu, Gong, Hao and Liu, *Bilevel Optimization with Lower-Level Uniform Convexity:
Theory and Algorithm*, ICLR 2026, is missing from the literature discussion.
It is directly relevant to the response modulus highlighted in the abstract and
contributions. Their Lemma 4.2 gives exponent `1/(p-1)` for a lower objective with
uniform convexity of order `p`; setting `p=P+1` gives `1/P`.

I independently found this paper while searching for bilevel Hölder response
bounds. I retrieved and read its actual primary PDF from
[arXiv:2603.00027](https://arxiv.org/pdf/2603.00027), including model (1),
Assumption 3.2(i),(iii), Lemma 4.2 on printed page 6, and its proof in Appendix B.1
on printed page 17. The author's
[code repository](https://github.com/MingruiLiu-ML-Lab/bilevel-optimization-lower-level-uniform-convexity)
confirms authors, title and ICLR 2026 publication. Direct OpenReview access returned
a browser challenge/403; I did not bypass it. The openly available arXiv PDF and
[primary HTML](https://arxiv.org/html/2603.00027v1) supplied the result itself.
The PDF and extracted text are retained under `verification/stage07-review02/`.

Their model has the unconstrained follower `argmin_{y in R^dy} g(x,y)`. The proof
combines order-p growth with Lipschitz variation of the lower gradient in the
leader. It divides the value-difference estimate by the response displacement to
obtain exponent `1/(p-1)`. The theorem does not address changing affine resource
right-hand sides, the polynomially encoded constant established here, or global
optimization in accuracy bits with exact rational base feasibility. Its algorithmic
conclusion concerns stationarity under additional oracle/smoothness assumptions.
It therefore does **not** subsume either of this paper's complete novelty classes.

The manuscript already avoids claiming universal priority for the exponent, so
this omission is not a major false novelty claim. Nevertheless, an explicit close
comparison is needed to support the requested careful review and to prevent the
reader from construing the highlighted exponent as having no direct bilevel
predecessor. The general-polynomial one-sided result of Jeyakumar et al. is useful
but does not replace this closer comparison.

**Required correction:** add the Wu et al. reference and a short comparison near
the modulus. Credit the established `1/(p-1)` exponent for their unconstrained
uniformly convex follower, then identify the present contribution as the structured
polynomial model with moving affine resources and an effective polynomial-bit
constant. In the introduction, distinguish the strongly convex stationarity work
of Chen et al. from this newer uniform-convexity work, while retaining the global
versus stationarity distinction. Do not claim to improve their stationarity rate.
No theorem or proof alteration is indicated.

Their Appendix B.1 explicitly cites the proof of Proposition 4.32 in Bonnans and
Shapiro, *Perturbation Analysis of Optimization Problems*. I checked that this
citation appears in the primary paper, but found no Bonnans–Shapiro package in the
local literature folder and did not inspect the original proposition. Thus its
exact scope is **not verified** here. It is reasonable to mention that Wu et al.
identify a classical perturbation lineage, but not to assert that the original
proposition covers moving resource sets without reading it. Root subsequently
independently verified the Wu et al. result and informed me of the same lineage;
the finding above was reached independently before that message.

## Mathematical assessment of the accuracy claims

1. **Model and output.** Strictly increasing polynomial marginals imply strict
   convexity on the box even when second derivatives vanish. A convex aggregate
   preserves uniqueness. Fixed rational resource normals and affine right-hand
   sides give the rational polytope `X_F`; the stated minima follow from response
   continuity and compactness. The introduction properly qualifies arbitrary
   polynomial upper data by explicit monomial encoding and numerical degrees.
   It does not claim rational exact optima or common-field response output in
   the accuracy model.
2. **Inverse approximation.** The interpolation increment bound is valid for
   signed coefficients. The proof includes the real parts of *complex* critical
   values; rational padded bad intervals have bounded total width. The geometric
   panel count depends on logarithmic precision. Centering at a rational response
   makes Taylor reversion coefficients rational. The proper-polynomial covering
   argument supplies the complex inverse disk, and Cauchy plus the displayed
   common-denominator recurrence controls both output and intermediate bit
   lengths. I found no hidden curvature lower bound, sparse-binary degree claim,
   or exponential Cartesian branch enumeration. Positive coefficients are used
   only in the separately labelled sharper construction.
3. **Residual certificate and recovery.** The Gram/cofactor constant controls
   both active-normal multipliers and feasible repair without Slater. The
   residual certificate includes absolute complementarity, accounting for large
   negative inactive slack. Nonlinear branch sets are closed validity sets, not
   unjustified closures of nonlinear sign cells. Rational recovery remains in
   `Q_0`, compares true clipped inverses across boundaries, and never relies on
   evaluating the old branch outside its validity set. The 4/5/4 transferred
   residual allowances and the polynomial upper Lipschitz ledger are consistent.
4. **Sharp exponent.** On a common active pattern, both optimal gradients lie in
   the common active-row span. The bounded right-hand-side correction leaves a
   tangent displacement; the displayed cancellation and two Bregman inequalities
   yield the stated `1/P` estimate. Semialgebraic component counting is used only
   to obtain a finite uniform encoded constant, not as a claimed polynomial-time
   enumeration in growing follower dimension. Squared slack and reciprocal-square
   variables correctly handle weak and strict inequalities. Their number and
   degree fit the given deliberately loose bound. Taking limits extends the
   same-pattern estimate to endpoints; summing finitely many subinterval bounds
   gives the global constant. The scalar power example verifies sharpness.
5. **Upper feasibility.** Outer surrogate emptiness certifies original
   infeasibility, while returned outer points need not be exactly feasible.
   The inner scheme guarantees original upper rows and compares against
   `V(delta)`, and its emptiness has the weaker advertised meaning. Rational
   recovery tolerances leave a strict inner margin. The convex-anchor result
   requires convexity of the *reduced* constraints, not follower convexity alone.
   Reserve controls are actual controls independent of the follower. The
   isolated-optimum and irrational-only-feasibility examples justify these
   qualifications. I checked their equations and found no contradiction between
   the abstract, introduction, theorems and conclusion.

## Existing attribution verified directly

- **Hochbaum–Shanthikumar (1990):** I extracted the actual local original PDF and
  read printed pages 844 and 846–847, Sections 1.2–1.3 and Theorem 1.1. They
  explicitly approximate the optimizer vector and obtain logarithmic precision
  dependence with numerical subdeterminant dependence and function-value
  access. The revised Section 4 gives the source appropriate credit. The
  remaining global-upper/input-bit distinction is accurate.
- **Vigneron (2014):** I extracted the actual local original and read Sections
  2.1 and 2.3, Theorems 6 and 9. Nonnegative algebraic functions have constant
  description complexity; the approximation bounds depend polynomially on
  inverse relative accuracy. Section 2.3 explicitly permits bit complexity with
  additional polynomial factors. The paper's comparison acknowledges this,
  rather than falsely distinguishing by the existence of any bit-model treatment.
- **Jeyakumar–Lasserre–Li–Pham (2016):** I extracted the actual local original,
  read Theorem 2.3 and context/proof beginning on printed pages 5–6, and checked
  the primary publisher abstract at
  [SIAM](https://epubs.siam.org/doi/abs/10.1137/15M1017922).
  Its feasible follower set is compact and independent of the leader; the
  solution-map inclusion is relative to a fixed reference point. Appendix C's
  description is accurate. This source supports global polynomial relaxation
  lineage and general regularity, without supplying the present bit guarantee.
- **Chen–Ji–Zhang (2026):** the primary
  [version 4 abstract/history](https://arxiv.org/abs/2511.22331v4) confirms the
  August 11 version and the nonconvex/strongly convex stationarity-oracle task.
  I did not audit its rates, and the manuscript imports none.

Searches also included `bilevel polynomial accuracy bits`, `bilevel fixed
separable polynomial optimization logarithmic`, `bilevel Hölder 1/P`, and
`polynomial inverse bit complexity approximation`, followed by title-specific
primary retrieval. Search results are discovery aids, not evidence of absence.
The single qualified novelty passage is scoped to complete theorem classes and
outputs. I found no source in this bounded search establishing those complete
classes; this is not proof of priority.

## Integration and limits of this review

The abstract and contribution overview preserve fixed structural dimensions,
numerical degree, optimistic versus universally feasible pessimistic selection,
attainment decisions versus guarantees, fixed measurement count *per criterion*,
and screening preprocessing costs. The conclusion properly separates exact
hardness from inverse-error approximation and path representation size from
pointwise follower evaluation. The scalar baseline is credited as classical
face enumeration extended to the full task, and the added envelope paragraph
claims no asymptotic improvement. All executable sources/data and the relevant
proof files were unchanged in the stage 7 diff.

The manuscript is self-contained as a mathematical and LaTeX document. README
honestly identifies the remaining stage gates and repository-dependent diagnostic
commands. This review does not treat the 77-page length, arbitrary absence of
future research, or journal acceptance as a mechanically certifiable property.
The required final integrated review remains necessary. Apart from R02-1, I found
no valid additional minor issue in the reviewed synthesis and accuracy dependencies.
