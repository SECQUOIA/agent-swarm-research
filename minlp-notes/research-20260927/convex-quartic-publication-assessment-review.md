# Independent review of the quartic publication assessment

Date: 2026-09-28. Reviewed
[the publication assessment](convex-quartic-publication-assessment.md).
The reviewer did not author that assessment.

**Verdict:** the assessment is supportable within its stated scope after
the qualifications identified below. The author incorporated the
degree-one exception, the rational Gram distinction, the inaccessible
proceedings version, and the updated Zhu--Cartis source; those changes
were read again. No remaining substantive error was found in the
minimality claims, the witness consequence, or the inspected comparisons.
Publication priority remains unestablished.

This review checks mathematical scope, source comparisons, and wording.
It does not repeat the full construction proofs, independently establish
their polynomial bit bounds, rerun Lean, or provide a fresh exhaustive
literature search. The construction reviews and the
[latest-status audit](quartic-latest-status-prior.md) retain those separate
roles.

## The precise consequence and minimality

Table 1 in the inspected Slot--Steurer--Wiedmer version distinguishes
compact rational feasible-point witnesses from the complexity of exact
decision. A nonempty zero sublevel with no rational point answers the
former negatively, irrespective of the encoding size of rational points.
It supplies no conclusion about alternative certificates or NP
membership. The assessment keeps these claims separate and also preserves
the distinction from approximate optimization.
[Primary Section 1.3 and Appendix C](https://arxiv.org/html/2511.03440v1).

The arXiv version check alone does not establish the current wording of
the STOC proceedings. The revised assessment explicitly records that the
proceedings text was inaccessible and limits its resolution claim to the
question in the inspected version. That is the appropriate qualification.

The degree and dimension arguments are correct for one globally convex
rational polynomial:

- Restriction to a line through a direction where the leading homogeneous
  part is nonzero excludes odd degree greater than one.
- A nonempty quadratic nonpositive sublevel either has interior or is a
  zero-minimum set. In the latter case, its points solve the rational
  linear gradient equations, which admit a rational solution whenever
  they are consistent.
- A univariate quartic singleton zero has a repeated algebraic root.
  Its irreducible polynomial therefore occurs with multiplicity at least
  two and has degree at most two. The quadratic case would give two real
  conjugate zeros, contradicting the singleton.

The assessment correctly excludes arbitrary descriptions of convex sets,
convexity only on a restricted domain, and systems of convex quadratic
constraints from these minimality claims. The general construction's
variable count needed a separate qualification: its \(d-1\) count applies
to \(d>1\); rational inputs are handled in one variable. Likewise,
degree-four minimality concerns the irrational singleton case. Both
qualifications are now explicit.

## Closely related source comparisons

Bienstock--Del Pia--Hildebrand's Example 1 and Observation 3 give the same
cubic point and rational zero level on the stated rectangle. The displayed
Hessian has positive first leading minor and determinant throughout that
compact rectangle, which establishes uniform strong convexity there.
At the origin its determinant is negative. The assessment correctly
labels the Hessian comparison as an inference and identifies global
convexity as the additional requirement.
[Primary manuscript, printed page 9](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf).

Ahmadi--Parrilo Theorem 5.6 proves real SOS-convexity of every convex
bivariate quartic, using the Hessian biform and Theorem 5.3. Theorem 5.1
gives the corresponding dimension-degree classification. These results
justify the assessment's warning against claiming the explicit example's
real SOS-convexity as an independent novelty. The cited proof does not
give the example's displayed rational certificate or its bit bounds.
[Primary Section 5.1](https://arxiv.org/pdf/1111.4587).

The inspected Baldi--Krick--Mourrain Theorem 2.1 has the stated radical,
zero-dimensional, strictly-positive hypotheses. Its later sections supply
height bounds and nonnegative extensions. The assessment does not
identify these quotient-algebra identities with a globally convex quartic
having the prescribed zero set.
[Primary text](https://arxiv.org/html/2410.04845v2).

Ahmadi--Chaudhry--Zhang Lemma 2 does prove the stated interior
SOS-convexity result, and its proof uses positive definite Hessian Gram
matrices and a Schur complement. Crediting those techniques as prior is
appropriate. Preserving a prescribed irrational zero with rational
coefficients is an additional arithmetic condition.
[Primary Lemma 2 and subsequent regularization argument](https://arxiv.org/html/2311.06374v2).

## The KMS shortcut is qualified correctly

Krick--Mourrain--Szanto's equations (4) and (6) permit the stated formal
zero-target specialization. The nonreal conjugate-pair interpolation
terms give a real PSD Gram matrix whose kernel is spanned by the
evaluation vector at the sole real root. Proposition 2.2 and Corollary
2.4 assume strict positivity at the real roots. The assessment correctly
calls the specialization an inference from their formulas rather than a
conclusion of those propositions.
[Primary Section 2.1](https://arxiv.org/pdf/2112.00490).

The distinction between the full Gram matrix and its quadratic block is
essential. In the rational linear space defined by vanishing modulo the
irreducible polynomial, rational approximations are dense. A sufficiently
close approximation preserves positive definiteness of the quadratic
block, exact vanishing at the target, and a small gradient there. It need
not preserve PSD of the full matrix.

Indeed, if a rational PSD matrix in that space satisfied the exact
vanishing congruence, it would annihilate the root's power-basis
evaluation vector. Every row would give a rational polynomial of degree
below the minimal polynomial vanishing at that root, so the matrix would
be zero. The assessment now includes this obstruction.

The shortcut therefore supplies the claimed qualitative input. It is not
by itself a reviewed replacement for the effective construction. The
quantitative argument newly recorded in the
[universal-realization audit](quartic-universal-publication-prior.md)
remains explicitly pending a fresh full proof review before replacement.
This review does not certify that new quantitative argument.

## Significance and verification limits

The relative ranking of the explicit counterexample, the effective
realization theorem, and its rational Hessian certificate is a defensible
editorial judgment. The assessment identifies the candidate contribution
as their combination of arithmetic prescription, exact zero preservation,
global convexity, fixed degree, and effective certificates. It does not
claim novelty for generic algebraic degree, interpolation, coefficient
projection, or Schur complements alone.

The solver consequence is appropriately limited to the impossibility of
always returning a rational feasible point. No hardness result, general
exact solver, or measured practical improvement is asserted. The
publication recommendation is explicitly conditional on priority.

The final boundary-degeneracy clarification is correct. Since \(F\geq0\)
and its only feasible point is its minimizer, \(F\leq0\) has no strictly
feasible point and its gradient vanishes there. An interior Hessian Gram
certificate does not give strict feasibility of this primal constraint.
For any positive constant \(\varepsilon\), continuity gives interior to
\(\{F-\varepsilon\leq0\}\), while \(\{F+\varepsilon\leq0\}\) is empty.
A lower Hessian bound alone supplies no upper Hessian bound or favorable
condition number. These facts properly limit claims of numerical
robustness or practical solver benefit.

The Lean discussion distinguishes its reported constant \(4096\) from
the separate hand-proved constant \(4124\), and does not claim that this
assessment reran the formal check.

Targeted verification for this review consisted of direct reading of the
assessment, the linked construction statements and review records, and
the primary passages identified above. An inline standard-library Python
check of this review covered its final newline, whitespace, control
characters, mathematical delimiters, and relative Markdown links.
The following targeted command returned no diagnostics:

    git diff --check -- research-20260927/convex-quartic-publication-assessment-review.md

No project-wide verification or CI inspection was performed.
