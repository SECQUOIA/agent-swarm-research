# Independent review: stationary-facet continuation

Reviewed `evidence/development-continuation.md`, together with the existing
edge-contact classification and its complete appendix proof. This review
concerns the mathematical arguments, using the exact Hildebrand rank-one
subtraction contract supplied by the literature lead. I did not independently
research or verify the original literature source.

## Verdict

The strengthened classification is mathematically sound under the supplied
rank-one subtraction contract. I found no counterexample or material proof
gap. It removes the three negative pair-principal-minor assumptions from
the existing edge-contact theorem when all vertex values are positive.
It still does not classify vertex-zero extreme rays or prove full family
completeness. The original-source receipt for the rank-one subtraction
criterion must be confirmed before the new result is included in the
submission manuscript.

The proof is substantially more than a formal extension of the earlier
contact argument. Its positive-definite stationary-facet argument allows
two additional zeros, whereas its rank-one argument needs and supplies a
stronger restriction: at most one additional isolated zero, or a segment
coplanar with the base zero segment. That distinction is essential.

## Proof audit

1. **Rank-one subtraction transfer.** The vertex matrix `R` has rank four,
   and its nonnegative column span is exactly the homogenized cube cone.
   For a nonzero copositive zero `u >= 0`, the mass `sum(u)` is strictly
   positive, so normalization gives an actual cube zero. An affine form
   vanishing on every cube zero therefore annihilates every zero of
   `R^T A R`. Subtraction of its vertex-value rank-one matrix is precisely
   subtraction of the affine square from the original quadratic. Extreme
   non-square quadratics must consequently have zeros with full affine
   span. No support hypothesis or converse geometric implication is being
   added to the supplied criterion.

2. **Positive-definite block: active sets.** I reconstructed the
   unconstrained velocities and all boundary paths. They are exhaustive.
   If both free coordinates decrease, the first lower bound remains
   active because its multiplier derivative is nonnegative. If the first
   coordinate increases, the second decreases. An upper bound reached
   by the increasing coordinate cannot release before the other coordinate
   reaches zero: its multiplier derivative has the strict sign required
   to retain it. At the resulting corner, the increasing upper multiplier
   can release that coordinate, after which the other lower bound stays
   active. Initial stationary facet-edge points merely truncate these
   paths. Simultaneous transitions and zero unconstrained velocities do
   not create an extra phase.

3. **Positive-definite block: zero count.** The upper-bound path has
   curvature sequence `S0, Sy, t, Sx, t`, with `S0 < 0`, `t > 0`, and
   `Sx > Sy`. Strictly concave pieces cannot contain an interior zero of
   a nonnegative value function. At an interior transition zero, its
   derivative is zero; any adjacent strictly concave piece would then
   become negative. The two positive-curvature corner phases can supply
   at most two isolated outside zeros. When the later free-edge curvature
   is nonnegative, the tail is convex and its zero set is connected.
   A zero interval lies on a single affine minimizer segment and cannot
   coexist with a separate earlier or later zero. The simpler decreasing
   path gives the same conclusion. Thus the base point plus the outside
   zeros always lies in an affine plane.

4. **Rank-one block: allocation and zero count.** With unequal ratios
   `r/d1` and `s/d2`, minimizing at fixed weighted sum uniquely allocates
   mass to the cheaper coordinate first for each positive height. The
   two active paths and their curvature sequences follow directly.
   Two distinct isolated outside zeros could occur only if the first
   corner supplies a zero and the subsequent cheaper free-edge curvature
   is negative. At that corner zero, vertex positivity forces an interior
   vertical position. The vertical double-zero equation gives
   `z = (h-d1)/sqrt(t)`. The inward derivative of the upper coordinate
   then gives `r/d1 <= sqrt(t)`, making that later curvature nonnegative
   and excluding the proposed pair of zeros. This step is correct,
   including equality and transition zeros.

5. **Rank-one block: coplanarity.** One additional isolated point is
   automatically coplanar with the base segment. A zero interval on
   either free edge forces its two-variable quadratic to be a rank-one
   square. Its coefficient identities put that interval in the plane
   `d1*x + d2*y + sqrt(t)*z = h`, which also contains the entire base
   segment. The equal-cost case reduces to one weighted-sum variable.
   Either the free-sum value function vanishes identically and the full
   quadratic is an affine square, or its only possible free-sum outside
   zero is on the upper facet. That zero segment is again coplanar with
   the base segment. A later corner zero cannot coexist with a final
   upper-facet zero within the height interval.

6. **Reduction to strict edge contacts.** The proof does not assume that
   a nonnegative pair determinant produces a stationary facet zero. It
   instead deals with actual zeros. An interior cube zero yields a PSD
   Taylor quadratic. A facet-interior zero gives a stationary PSD facet.
   At an edge zero with zero derivative into a neighboring facet, every
   negative two-variable quadratic direction can be reversed to point
   inward in its constrained coordinate while retaining a feasible small
   displacement in the free edge coordinate. Hence its facet block must
   be PSD. Excluding these cases by the stationary-facet lemma leaves
   precisely edge-interior zeros with strict inward derivatives.

7. **Reuse of the contact classification.** Once strict edge contacts
   are known, the earlier perturbation bound supplies at least five
   contacts. The incident-edge inequality only needs to be weak; its sign
   still forces equal Hamming levels. Three incident contacts yield an
   affine square plus nonnegative coordinate products, excluding
   non-square extremality even if some product coefficients are zero.
   The central-cycle decomposition and the three impossible graph types
   do not use strict pair determinants. Recovering the final five-contact
   graph gives positive `k` from a strict inward derivative and therefore
   gives all three negative pair determinants as a conclusion.

8. **Positive-diagonal cone bridge.** If a quadratic has strictly positive
   square coefficients, a nontrivial two-sided perturbation feasible in
   the full nonnegative cone remains feasible in the positive-square
   cone for sufficiently small perturbation size. Thus extremality in
   the latter implies extremality in the former, as used in the
   completeness discussion.

## Revisions made during review

I requested two clarifications, both now present in the evidence proof:

- A zero at an interior active-set transition has zero value-function
  derivative, so a neighboring negative-curvature phase is impossible.
- In the unequal-cost rank-one case, the hypothetical two outside zeros
  require a first-corner zero and a later zero after the cheaper
  negative-curvature phase. The corner derivative explicitly excludes
  exactly that configuration.

No numerical optimization, archived experiment rerun, executable check,
literature command, KB mutation, project-wide verification, or CI inspection
was performed for this review.

## Second pass: manuscript integration and sign hypothesis

I reviewed the actual TeX integration in
`sections/05b-contact-classification.tex`,
`appendices/E-contact-classification.tex`, and
`appendices/F-facet-classification.tex`. The following labels identify the
new mathematical content:

- `three:edge-classification`: classification without vertex zeros;
- `three:zero-span`: affine-square subtraction from a common zero plane;
- `three:stationary-facet`: stationary PSD-facet exclusion;
- `app:three:facet-classification`: full stationary-facet proof;
- `eq:three:pd-paths` and `eq:three:pd-curvature-sequence`: the PD active
  paths and curvature order;
- `eq:three:allocation-curvature`: the rank-one allocation curvature order.

The TeX faithfully transcribes the independently reviewed proof. In
particular, the aligned-cost proof now explicitly treats interior active
transitions and excludes a transition at the final height by vertex
positivity. The weak incident-edge inequality in Appendix E is sufficient:
it forces the same Hamming-level rule, and the three-incident-edge
decomposition excludes extremality unless all residual coefficients vanish,
which gives the already excluded affine square. No negative pair-minor
hypothesis remains hidden in that appendix.

I also checked the proposed additional use of the already supplied
Burer--Natarajan--Willemsen exactness contract to remove the positive
mixed-product hypothesis from the theorem. After a cube symmetry makes
all mixed coefficients nonpositive, its exact SDP is

`M = [[1,m^T],[m,Y]] >= 0`, `m_i-Y_ij >= 0` for all ordered `i,j`.

This primal set is compact: its diagonal inequalities and PSD principal
minors imply `m_i^2 <= Y_ii <= m_i`, hence `0 <= m_i <= 1` and bounded
diagonal and off-diagonal entries. Independent uniform coordinates give
`m_i=1/2`, `Y_ii=1/3`, `Y_ij=1/4` for distinct indices. The moment matrix
has positive-definite covariance `I/12`, and every entrywise inequality
is strict. Thus Slater's condition and finiteness give dual attainment.
The attained dual certificate has the polynomial form

`q = min(q) + (1,x)^T S (1,x) + sum_ordered lambda_ij*x_i*(1-x_j)`,

with `S` PSD and `lambda_ij >= 0`. Using ordered multipliers correctly
accounts for both nonsymmetric inequalities involving a mixed moment.
The symmetric-matrix trace convention supplies the factor of two for
off-diagonal quadratic coefficients; no extra factor belongs in the
displayed polynomial certificate. The diagonal multiplier terms are the
caps `x_i*(1-x_i)`.

Each summand is nonnegative on the cube. At an extreme ray with all square
coefficients strictly positive, every nonzero summand must be proportional
to `q`. Neither a constant nor any cap or off-diagonal bound product has
all three square coefficients positive, so those summands must vanish.
A PSD factorization then makes `q` proportional to a single affine square.
Such a square with all three square coefficients positive has all three
affine slopes nonzero and has strictly positive mixed-coefficient product.
Consequently there are no extreme rays with strictly positive square
coefficients and nonpositive mixed product. Vertex positivity is not
needed for this sign-class consequence.

This argument justifies dropping the mixed-product hypothesis from
`three:edge-classification`, while retaining positive vertex values for
the stationary-facet and edge-contact parts. Appendix E should invoke the
new sign-class consequence before normalizing all mixed coefficients to
positive values. The author and integrating agent were notified of this
point. The only source gate added by the stronger classification remains
the original Hildebrand rank-one subtraction receipt; this review did not
start literature work.

I subsequently checked the saved final integration. The theorem now assumes
only strictly positive square coefficients and strictly positive vertex
values. Appendix E begins with the nonpositive-product SDP argument, proves
dual attainment, states the correct polynomial certificate with ordered
multiplier indices, and excludes its product summands by vertex positivity.
It then normalizes the remaining mixed coefficients to positive values.
This is sound. The stronger diagonal-only exclusion is optional, not needed
for the stated theorem. I requested one notation cleanup in the new primal
display: use the established `\mathcal L_{m,Y}` pairing in place of plain
`L_{m,Y}`. There are no unresolved mathematical objections to the actual
TeX integration under the stated external source contract.
