# Review of the focused cubic bounds

Review date: 2026-09-16. Mathematical claim review: **PASS**. The complete
focused manuscript, supporting identities, and final Lean statements have
been reviewed. No substantive mathematical coverage gap remains. Integrated
verification and distribution checks are recorded separately. This is an
internal agent review, not external peer review or a publication-priority check.

The review independently examined the calculations in the
universal bound (original repository source note),
the analytic family (original repository source note),
and the existing canonical `CubicGap` statements. Earlier review notes were
read as additional context, not treated as substitutes for checking the claims.
The developing [coverage map](../formal/COVERAGE.md) separates existing proofs from
new obligations. No mathematical flaw was found in the two result notes.

## Universal bound and fixed-mixture optimality

The endpoint-orientation, independent, and biased-threshold distributions
must be defined for the entire ambient marginal vector. Their definitions
cannot choose a separate law after inspecting a support. Conditional
independence in the first and third constructions is part of the definition.
Each law preserves every coordinate mean, including zero and one.
The threshold classification consistently places `x = 1/2` in the low class.

For sorted cubic marginals `u ≤ v ≤ w`, the termwise gap is
`min(u, (1-v)+(1-w))`. All deficiencies are nonnegative. The low-count cases
and their stated estimates are valid, including shared boundaries and zero
gaps. In the one-low case, the four min-function cases exhaust `a ≥ b ≥ 0`.
In the all-high case, the independence estimate `7T/16` follows from
`ab ≤ (a+b)^2/4`; both branches `a+b ≤ u` and `u ≤ a+b` are required.
The weighted constants sum to exactly `12/31`. The separate bilinear cases
are necessary: bilinear terms also arise from affine box expansion.

The final inequality concerns the original term-by-term envelopes on each
nonnegative box. The proved box transfer from topic 1 supports this step,
including fixed coordinates. A bound only for expanded cube terms would
not, by itself, be the claimed original-box statement.

Fixed-mixture optimality has a narrower meaning than sharpness of the cubic
gap ratio. For weights `(w,r,v)` on the three specified laws, the necessary
uniform-fraction bounds are

```
α ≤ 1/2 - v/2,
α ≤ 3/8 + 3v/8 - 3r/8,
α ≤ 3/8 + r/16.
```

Their convex combination with weights `3/31, 4/31, 24/31` cancels the unknown
weights and proves `α ≤ 12/31`. To connect this algebraic certificate to the
actual laws, the following test configurations must also be proved:

| Marginals | Required parameter range | Normalized deficiencies `(O,I,B)` |
|---|---|---|
| `(u,1/2)` | `0 < u ≤ 1/2` | `(1/2,1/2,0)` |
| `(ε,1-ε²,1-ε²)` | `0 < ε ≤ 1/2`, tending to zero | `(3/8, ε-ε³/2, 3/4)` |
| `(u,1-u/2,1-u/2)` | `1/2 < u < 2/3`, tending to `1/2` | `(3/8, u-u²/4, 3/8)` |

The last parameter restriction ensures the anchor is the smallest marginal
and all three coordinates are high. The result excludes neither better laws
nor coefficient-aware analyses of these same laws. It does not prove
`R(3) = 31/12`.

## Analytic lower family

The existing Bernstein theorem proves the stronger continuous inequality
`F ≥ affine + 901/120000`, not just nonnegativity at a finite sample. Its five
intervals cover the required domain, and their Bernstein basis coefficients
sum against a partition of unity. The two completed-square bounds justify
the elimination of the other variables without assuming an optimizer lies
in an unproved active set.

For the six-orbit family, the normalized binary-count expansion and the
uniform correction bound `72/m` are correct. They apply at binary vertices;
the paper must not identify the count polynomial with the original
multilinear polynomial away from vertices. All joint laws with the prescribed
individual means have normalized expected counts `(1/4,1/2,3/4)`, regardless
of dependence. This gives the convex-envelope lower bound.

The exact normalized concave-envelope and termwise-gap formulas are

```
18 cav(f_m)/m³ = 167/4 - 153/(4m) + 9/m²,
18 T(f_m)/m³   = 161/4 - 135/(4m) + 6/m².
```

Only the `2 E₃(W)` orbit has a nonzero individual lower envelope. The common
upper law makes the concave-envelope formula exact. The family has positive
integer coefficients when `m` is a positive multiple of nine. Its point is
strictly interior. A positive hull gap requires a proof, for example by
comparing the common upper law with independent rounding, or with the
original interior graph value. It cannot be inferred merely from a positive
upper bound on the hull gap.

The asymptotic argument concerns a sequence of certified lower bounds on
actual ratios. Neither exactness of the convex-envelope lower bound nor
convergence of the actual ratios is claimed. The bound without slack tends
to `483/223`; incorporating the proved slack gives

```
(161/4) / (223/12 - 901/120000)
  = 4830000/2229099
  = 1610000/743033.
```

The last fraction is reduced and is recommended for the headline theorem.
The displayed non-slack finite certificate at `m=36` is `16985/8436 > 2`.
Formalization must prove denominator positivity and membership of actual
family ratios in the specified supremum set before passing to the limit.

## Recommended focused paper structure

1. Define the original graph-hull and termwise gaps and the all-box supremum
   `R(3)`. State `1610000/743033 ≤ R(3) ≤ 31/12` and state the fixed-mixture
   optimality result with its restricted meaning.
2. Give the vertex-law interpretation, exact individual envelopes, and the
   support-independent three-law construction. Prove the cubic and bilinear
   deficiency estimates and transfer the result to boxes.
3. Prove fixed-mixture optimality with the three explicit configurations and
   the rational averaging certificate.
4. Define the six-orbit analytic family. Prove the scalar minorant using the
   existing completed-square and Bernstein certificates, derive its exact
   finite formulas and ratio lower bounds, and pass to the supremum.
5. Present exact finite witnesses in a compact table. The existing seven
   ratio theorems may be reused. An optional explicit homogeneous
   unit-coefficient witness is already formalized; it does not require a
   general coefficient-removal theorem.
6. Provide a claim-to-declaration appendix, reproducible verification
   commands, trust boundary, and the precise exclusions below.

The general two-level family is unnecessary for the two-sided bound or the
mixture theorem and should remain outside this focused paper. Existing
finite two-level examples can still appear as table rows. Exclude general
coefficient removal, equal-marginal classification, dimensional minimality,
and claims of the exact value of `R(3)`.

## Verification handoff

The subsequent manuscript and source review is recorded below. Completion
also requires the integrated warning-free build, import coverage, transitive
axiom audit, kernel replay, matching standalone export, and paper/bundle
checks. The final verification record must identify the checks actually run
rather than reusing historical verification records from the finite-witness
package.


## Review of the complete focused manuscript and final interfaces

The reviewer subsequently read the complete
[`paper-cubic-gap/main.tex`](../main.tex) and inspected
the new source statements and proof arguments. The final manuscript defines
`O` by the conditional probabilities used in `OrientationRounding` directly.
It makes no extra equivalence claim about an unfurled orientation construction.
The actual optimality tests use `(1/2,1/2)`, `0 < ε ≤ 1/8`, and
`1/2 < u ≤ 5/8`, exactly matching the formal domains. These smaller domains
still supply the required limiting obstructions.

The following source checks were completed independently of their authors:

- `RoundingScalar`: the full min-function case split, the all-high `7/16`
  independent estimate, both min branches, two-low estimates, and bilinear
  inequalities agree with the paper. The inequalities retain zero and equality
  boundaries and do not require dividing by a possibly zero gap.
- `RoundingLaws` and `RoundingUpper`: the mixture is a single law on the full
  ambient coordinate set. Its actual pair/triple expectations satisfy the
  estimates, sorting covers arbitrary supports, and constants/singletons are
  handled explicitly. The box theorem bounds original-term gaps, and the
  supremum theorem uses a proved nonempty ratio set.
- `RoundingOptimalityLaw`: the guarantee predicate quantifies over actual
  pair/triple monomials in every finite cube. The two cubic normalized
  identities prove positive denominators; applying the predicate gives the
  sequence bounds used in the limit theorem. The final obstruction and
  attaining mixture use the same predicate. This closes the gap between an
  algebraic weight certificate and actual-law optimality.
- `AnalyticValues` and `AnalyticFamily`: the coefficient order matches the
  six displayed orbits; normalized count expectations follow from all
  individual means without an independence assumption. The binary expansion,
  correction bound, and Bernstein inequality give a law bound and then a
  bound on the actual attained minimum. The upper and termwise formulas are
  exact. Actual hull-gap positivity is proved by a feasible interior graph
  point strictly below the common upper endpoint. Ratio division uses that
  positive hull gap and a nonnegative numerator.
- `ThreeSupports`: orbit sums are collected into one finite set of distinct
  supports with nonnegative aggregate coefficients and degree at most three.
  The polynomial equality and termwise-gap equality connect the analytic
  notation to the generic supremum definition. Zero coefficients on unused
  supports are permitted by the paper's class definition.
- `AnalyticLimit` and `AnalyticResults`: actual finite family ratios belong
  to the degree-three cube and all-box ratio sets. Boundedness is supplied by
  the proved universal upper bound before using `le_csSup`. The convergent
  lower approximants bound actual ratios, so their limiting bound reaches
  the actual supremum. The refined and simpler bounds, fraction reduction,
  and unrefined `m=36` certificate are correctly distinguished.

The scalar-certificate proof was checked against both printed square
completions and all five Bernstein rows. The paper calls the second quartic
`q`; the source calls it `lowerR`. The polynomial, all coefficients and
intervals, and slack are identical. The source proves the scalar result on
a domain stronger than the paper's cube: all real `b`, all `a ≤ 1`, and
`0 ≤ c ≤ 1`.

The seven finite-witness rows use the original `twoFamily` and `threeFamily`
symbols, means, and coefficient vectors. Their exact ratios match `Ratios`,
and `four_strict_counterexamples` covers the last-four assertion. The three
finite coefficient vectors are not presented as analytic-family members.
The printed variable counts are product-Fin cardinalities. Existing universal
count minorants, attaining count laws, coordinate-law lifts, and common upper
laws support the paper's description of their certificates.

A second agent independently checked both square-completion identities,
all five Bernstein expansions and coefficient bounds in exact symbolic and
rational arithmetic, the rational limit, the unrefined `m=36` value, and all
seven finite ratios. That agent also inspected the completed actual-law and
box-bound modules. No mathematical error was found. These computations and
reviews support the claim mapping; they are not substitutions for Lean's
kernel verification.

The final supporting precision item is now closed. `threeSupportCoefficients_nat`
proves that collecting equal supports preserves natural coefficient values.
`threeSupportCoefficients_card` proves that every nonzero aggregate coefficient
has support size two or three, using exact support cardinalities within each
orbit. `analytic_nonzero_support` combines these facts with the analytic
coefficient integrality to obtain positive integer monomial coefficients;
`analytic_integer_support_witness` combines this with the actual positive-gap
ratio witnesses. These statements were reviewed against their definitions
and do not assume the desired conclusion as a hypothesis.

`fixed_mixture_optimum` also packages attainment and the upper obstruction
as an `IsGreatest` theorem over nonnegative weights summing to one. The
attaining element and upper bound use the same actual-law guarantee predicate.

Separate reviewers also completed final source checks of the actual-law
optimality modules and the analytic aggregate-coefficient endpoints. Both
reported no remaining semantic issue and successful targeted warning-free
builds of their reviewed endpoints.

Mathematical source review passes with no remaining substantive gap in the
focused manuscript. Integrated verification, export identity, and paper/bundle
checks remain the responsibility of the final verification record; this
review does not declare those checks complete.
