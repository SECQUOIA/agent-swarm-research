# Independent review of minor geometry and successive cuts

The four reviewed files pass the mathematical review after one missing
hypothesis was restored. No unresolved major or minor mathematical finding
remains in this scope. This review covers the final TeX versions identified
below. It does not certify literature attribution, experiments, or the full
manuscript build.

## Resolved finding

**MAJOR — resolved: missing indefinite-apex hypothesis in
`mi:other-minors`.** An earlier paragraph asserted that the maximal sets free
of the rank-one positive semidefinite projection were negative semidefinite
separating halfspaces without restricting the apex. This is false at a
positive definite apex: the positive semidefinite cone is itself free of
rank-one positive semidefinite matrices in its interior, and no negative
semidefinite matrix strictly separates that apex. The authorized source
restricted the halfspace statement to an indefinite apex. The final appendix
now explicitly says “at an indefinite apex.” The separate
`mi:principal` result continues to concern the full singular locus and is
correct at both positive definite and negative definite apices.

The author made the repair. This reviewer did not edit author-owned TeX.

## Minor geometry

The following statements and complete proofs were checked directly against
their final definitions.

- `mi:free-cones`: connectedness of the free interior fixes the positive
  determinant sign; every singular matrix has negative-determinant matrices
  arbitrarily near it; homogeneous conic enlargement proves that maximal
  sets are cones. The equality of the singular-locus and nonpositive-side
  corner bounds uses positive costs and the first zero on a segment.
- `mi:polar`, `mi:orbit`, and `mi:orbit-proof`: the rotation coordinates and
  column-interchange rule have the correct signs. The image parameter is
  `F'^T = B F^T A^{-1}`, and transposition sends `C_F` to `C_{F^{-1}}`.
  The direct enlargement argument proves maximality. The dual-cone identity
  `C_F^* = F S_+^2` proves that identical sets differ only by a positive
  scalar. The full orbit therefore has three parameters. Transformed polar
  choices give exactly `F^T Mbar` symmetric positive definite, a two-parameter
  family, and its positive definite parameter transforms by congruence.
  Polar uniqueness proves that its intersection with the one-parameter
  rotation family is the single original polar set.
- `mi:certificates`: strict positivity at the apex implies positive
  determinant of the parameter; endpoint positive semidefiniteness is
  exactly simplex containment. The displayed dual identity gives an upper
  bound on a supremum, without claiming attainment or necessity of the
  positive definite dual witness.
- `mi:support` and `mi:support-proof`: smallest-support reduction preserves
  the projected point and forces zero cost along a dependence. The
  independence assumption is necessary for the bound on every minimizer
  under discussion. The positive index two bounds a nonnegative subspace;
  the rank-one tangent space has a one-dimensional radical and quotient
  signature `(1,1)`. These facts yield support at most three and force the
  apex into the supported ray span when support equals three. The exceptional
  zero-gradient case is treated separately. A support-two minimizer has
  tangency and nonnegative edge determinant.
- `mi:pencil` and `mi:pencil-proof`: both adjugate identities, the constant
  pencil determinant, the rank-one contact condition, and the two-sided PSD
  segment argument are correct. The required scale is `theta c_0 > 0`;
  the sign need not be the same before normalizing different examples.
- `mi:examples`, `mi:example-proof`, and `mi:example-data`: exact face
  enumeration proves the corner values and unique minimizers. The printed
  coarse dual witnesses prove strict orbit supremum gaps, rather than only
  nonattainment. Full row rank of the certificate map and continuity of its
  kernel preserve the witness near A. Compact objective sublevels and a
  negative-determinant continuation beyond A's contact give the stated
  continuity of its corner bound. The additional unrestricted-attainment
  claim uses the unique contact and the verified normal product `6 > 0`
  in `fd:attainment`, followed by `mi:free-cones`.
- `mi:embedding` and `mi:comparison-certificates`: the slice `h=1` preserves
  both the bilinear corner bound and family-A ray steps. Every printed
  rational primal and dual endpoint verifies the stated bracket. The
  comparisons concern the three specified bilinear examples. The infimum
  comparison obtained by embedding does not assert a comparison among
  full-dimensional corners with fixed conditioning.
- `mi:contact`, `mi:scaling`, and `mi:scaling-proof`: the contact cone is
  exactly `{F^{-T} b b^T}`. The support-one polar condition is the single
  stated linear condition. The scaling example has corner bound one,
  the four printed polar and point-family ray steps, and the rotation
  upper bound with constant `(16 + 2 sqrt(73))/3`.
- `mi:principal` and `mi:other-minors`: the positive-determinant symmetric
  components give the unique semidefinite maximal cone and its exact cut.
  The full singular locus is distinguished from the rank-one PSD
  projection. The one-diagonal projection has precisely the printed
  closure; all three boundary cases in its limiting construction work.

## Successive cuts

The final Section 7 and Appendix E proofs are complete within their stated
hypotheses.

- `cv:uniform-depth`: compactness supplies an accumulation subsequence.
  A term with positive limiting distance receives a cut with a fixed
  positive depth. Every later vertex satisfies that retained cut and lies
  in the earlier basis cone, contradicting convergence of the subsequence.
  This proves feasibility of every accumulation point and convergence of
  the monotone LP values to the nonlinear optimum. The proof needs neither
  strictly positive reduced costs nor maximal free sets. The chosen basis
  is explicitly an optimal nonsingular basis.
- `cv:cone-depth` and `cv:pointed-convergence`: scaling each ray to unit
  norm separates total step length from cone cancellation and gives
  `d >= gamma delta`. The sufficient condition requires a uniform lower
  bound on pointedness, not merely a positive bound in each round.
- `cv:one-term`: both maximum-distance selection and maximum-residual
  selection give the cut required by the accumulation argument. Pairwise
  distinct term indices justify changing only the product coordinate to
  show `distance <= residual`. Arbitrary term selection is not covered.
- `cv:rule-steps` and `cv:ball-proofs`: both signed affine coordinate maps,
  the Case-4 support function, and the exceptional endpoint are handled
  correctly. The default set contains the norm-cone ball with radius
  `q/(sqrt(2)(a+b))`. The inverse-apex orbit set contains the ball with
  radius at least `q/sqrt(3 B^2+1)`. Projection decreases ray norm because
  indices are distinct. The geometric and perturbed objectives transfer
  that radius to the returned set using the stated uniform multiplicative
  accuracy `theta`; perturbation `tau` is fixed and positive. These are
  idealized rules. The manuscript expressly declines to infer a uniform
  multiplicative accuracy from a fixed absolute bisection error.
- `cv:shallow-optimal`: midpoint freeness gives the universal intercept
  product bound. The exhibited orbit epigraph is maximal and attains the
  corner bound, while its exact depth tends to zero. The distance to the
  forbidden side is exactly one. This example varies the objective and
  does not prove failure of a bound-optimal loop for one fixed problem;
  the final text states this limit of the claim.
- `cv:dual-ties`: equality of the two inequalities forces equality for
  each supported term, so the minimizing point lies in the relative
  interior of the supported intercept simplex. A support of size at
  least two forces the additional zero reduced cost at each intercept
  basis. The conclusion concerns the corner LP. It does not force ties
  for support one or imply an explanation of full-LP reoptimization time.
- `cv:stalling` and `cv:stalling-proof`: the direct strict-enlargement
  proof establishes maximality. The induction verifies interior
  containment, every basis ray, every exit step, and the exact next cut.
  All reduced costs remain strictly positive, so each displayed LP
  optimum is unique. The fixed separating vector gives the printed
  uniform positive pointedness bound. The next retained vertex bounds
  cut depth above by the successive difference, which tends to zero.
  The fixed-problem limit remains infeasible and below the nonlinear
  optimum. The final paragraph correctly limits the construction to
  adversarial maximal-set selection and records the one-round
  bound-optimal alternative; it is not a failure example for the default
  rule or the bound-optimal rule.

## Exact arithmetic and targeted checks

Independent arithmetic used scratch scripts written from the displayed
data, rather than invoking author scripts, certificate generators, searches,
or solvers. The delegated arithmetic reviewer and its child ran:

- `python3 /tmp/minor_arithmetic_independent.py` — final exit 0. All printed
  polar entries, apex and ray determinants, minimizers, 93 nonsingular
  A/B/S1 face systems, retained and omitted face values, KKT data, S1
  incident normal products, two pencils, ten PSD intervals, and fifteen
  coarse PD dual blocks passed. Each coarse matrix residual is exactly
  zero. Both pencil signs and constant determinants were verified.
- An inline exact SymPy certificate-map rank calculation — exit 0; rank
  four in each full-dimensional example.
- `python /tmp/qic_bracket_exact_check.py` — exit 0. All six printed
  rational primal parameters pass the apex and endpoint PSD checks;
  every endpoint block is actually positive definite. All twelve
  bilinear dual blocks are positive definite and all residuals vanish.
- `python /tmp/minlp-independent-bilinear-faces.py` — exit 0. All 45
  embedded bilinear face systems confirm the printed unique contacts
  and corner value one; singular systems are inconsistent.
- An inline exact Fraction endpoint comparison — passed all decimal
  brackets and strict comparisons.

The principal reviewer ran an inline SymPy derivation of both signed
quadratic identities, the orbit epigraph determinant and free-set slack,
the general stalling step and cut identities, the basis determinant and
reduced costs, and the exact shallow depth formula. Final exit 0. Initial
scratch runs in the arithmetic checks stopped on expression-shape
comparisons; replacing those comparisons by exact mathematical equality
resolved them. They did not expose a manuscript error.

Targeted `rg`, `cat`, `sed`, and `wc` inspections covered the four reviewed
files, the project instructions, BRIEF, AUTHOR-CONTRACT, and the relevant
minor/multiround/fidelity/selection source passages. An inline Python
structure/hash check of the four final files passed: 42 unique labels,
39 resolved owned reference occurrences, no trailing whitespace, and no
local package or macro definitions. External references are
`fd:attainment`, `fd:counterexample`, and `fd:support-one`; their global
resolution belongs to manuscript integration. The local use of
`fd:attainment` was checked against its current theorem statement.

No experiments were rerun, no web or literature research was performed,
and no project-wide checks or CI inspection were used. A combined targeted
TeX compilation was reported by the author, but was not independently run
by this reviewer and is not counted as an independent verification result.

## Final reviewed file identities

| File | SHA-256 |
| --- | --- |
| `sections/06-minors.tex` | `726d07879a35fc3ba925619a25a2dc793d6ba1d1d409e6886f6a4a6ed2400dae` |
| `appendices/D-minors.tex` | `96dd14ab308f5ab6e511804d098aa5bb666edfc409f9fac8e831e1e5deb4897d` |
| `sections/07-repeated-cuts.tex` | `a51f9821b8212e227137fb6f5f972978c48c5cfeebad032b6053b32d2912c889` |
| `appendices/E-convergence.tex` | `22bf947cf8c6846ce92b024c360dcc649421007335cd6244a8f632767df0b2ce` |

These hashes include the final integration edits inspected after the
indefinite-apex repair and final unrestricted-attainment and one-round-choice
additions. The matrix edge direction was consistently renamed
`D_{\mathrm{edge}}` in Section 6 and Appendix D to distinguish it from the
depth parameter. The source-specific polar-factor citation in Section 6 and
Case-4 citation in Section 7 were changed from `CMS2023` to
`ChmielaMunozSerrano2020ZIB` after verification by the literature lead. Scoped `rg` inspection
and `sha256sum` confirmed these final versions. These edits change notation
and attribution without changing any proof, hypothesis, numeric data, or
certificate; no additional proof arithmetic or experiments were needed.
