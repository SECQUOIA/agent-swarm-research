# Review of the exact polynomial-box fallback proofs

Date: 2026-10-02. Status: approved; no mathematical or bit-complexity
blocker in either proof.

Reviewed the complete
[construction](../new-direction/polynomial-exact-fallback-construction.md),
including completeness on exceptional draws, the coefficient-height
dependence, exact comparisons, and requested-precision evaluation. A
second reader separately checked the complete construction and its
Sections 5--7.

The subsequent complete-file review of the shorter
[main proof](../new-direction/polynomial-exact-fallback.md) is recorded
below, including its feasible-rational-point and lower-bound contract.

## Resolved statement clarifications

The preserved construction now explicitly requires closed continuous
intervals, rejects domains made empty by inward integer rounding, and
assumes the remaining mixed domain is nonempty. These are the compactness
assumptions used by the proof. Its face equations also explicitly use
the restriction of the objective to that face. Substituting rational
endpoints preserves all displayed coefficient bounds. The earlier
statement clarifications are resolved.

## Construction checks

The pure-power leading monomials in the perturbed stationary equations
are pairwise relatively prime. They give the claimed finite quotient
basis for every nonzero perturbation parameter. Radical ideals and
simple stationary roots are unnecessary.

Normalizing a coordinate characteristic polynomial by its smallest
Laurent exponent leaves a nonzero polynomial after specialization at
zero. A convergent subsequence of perturbed minimizers has a fixed
relative-interior face. Its limit is an original optimizer, and every
free coordinate of that limit is a root of the corresponding specialized
polynomial. A nonzero constant polynomial safely discards a face with no
bounded stationary limit. Additional coordinate-root combinations cause
no problem: retained tuples are feasible, and the list contains a true
optimizer.

The reduction depth, determinant degrees, integer denominator clearing,
and candidate count keep every dimension-dependent factor within
`exp(poly_d(I))`. Coordinate coefficient heights remain linear in the
added coefficient-length bound, up to a base-only factor. Univariate
isolation and refinement consequently have an absolute polynomial
exponent in that length.

The separation proof is valid. Multiplying each coordinate by the
leading coefficient of any supplied integer defining polynomial makes
it an algebraic integer, even when the polynomial is reducible. For two
tuples, the field degree is at most `E=N^(2n)`. The scaled objective
difference has all conjugates bounded by `2^R`, so its nonzero integer
norm gives the displayed gap `2^(-ER)`. The rational-endpoint gap follows
from the same argument. These bounds include exact ties and coordinates
on box boundaries.

Approximation error at most one quarter of the gap makes the stated
half-gap equality test valid. The derivative bound proves the displayed
coordinate precision for objective comparisons. It also gives point
and value enclosures at requested precision `q`, with work polynomial
in `I+b+q` after the base factor is removed.

All counts and height bounds are effective. The specified polynomial
arithmetic and univariate algorithms therefore permit a sufficiently
large computable base-only constant `B`; its selection does not depend
on the sampled coefficients or subsequent precision. The output
convention correctly allows exponential base-dependent length and an
exact polynomial expression for the value.

## Main proof checks

Successive coordinate minimization over the compact global optimizer
set selects exactly one lexicographic optimizer. Formula (7) rejects
every nonoptimal point at a better feasible point, and rejects every
noncanonical optimum at the lexicographic optimizer. Its scalar
coordinate projections and value projection are therefore singletons.
All independently represented coordinates belong to that same point.

The expanded integer-label predicates have exponential base-dependent
length but labels of polynomial base bit length. The two quantified
blocks have size `n`, with one free scalar. Substitution into the
displayed primary quantifier-elimination bound leaves every dimension
factor within `exp(poly_d(I))`, while the coefficient-height exponent
remains absolute. Positive denominator clearing and Boolean formula
evaluation preserve this separation. The primary theorem's transcription
was separately checked from its rendered page by other reviewers; this
review checked the stated theorem's application and subsequent bounds.

The singleton-recovery argument is correct. Away from all output
polynomial roots, every atom has locally constant sign, so a true
singleton must occur at one of those roots. Multiplying the nonconstant
atoms, taking a squarefree part, isolating roots, and evaluating their
signs produces the unique selected root. Degree, output length, and
coefficient-height growth through these univariate operations preserve
an absolute polynomial exponent in added coefficient bits. Requested
coordinate and value refinement requires no additional elimination.

Section 6 supplies the stronger approximation contract. An isolating
interval of width less than one recovers each selected integer label
exactly. Clipping a rational continuous-coordinate approximation to its
closed interval cannot increase its distance from the exact coordinate.
The resulting point is feasible, and its continuous segment to the
optimizer preserves every integer label. The gradient's `l1` bound
pairs with coordinatewise error in `l_infinity`, so continuous-coordinate
error at most `delta/(2G)` gives objective error at most `delta/2` without
an additional dimension factor.

A rational enclosure of the exact value with width at most `delta/2`
has a lower endpoint `a` below every feasible value. Consequently the
feasible rational point satisfies `0<=F_gamma(y)-a<=delta`. Termwise
monomial bounds give `G` polynomial encoding length in `I+b`; thus these
refinements require only `q+poly_d(I+b)` bits. Rational evaluation also
fits the stated budget. A second reader independently checked the
canonical singleton formulas and this complete approximation argument.

## Verification scope

Both complete files received mathematical review. Independent second
reads checked the construction's arithmetic bounds and the main proof's
canonical selection and Section 6. No mathematical checker, project-wide
verification, CI inspection, or literature search was run as part of
this review. An optional local PDF-rendering attempt could not run
because `fitz` was unavailable; separate primary-source verification is
recorded in the main note. Neither review makes a novelty claim.
