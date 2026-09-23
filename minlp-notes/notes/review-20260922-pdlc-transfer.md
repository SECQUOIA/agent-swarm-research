# Independent review of the strict PDLC four-aggregation transfer

Date: 2026-09-22. Reviewed draft:
[research-20260922-pdlc-frontier.md](research-20260922-pdlc-frontier.md).

## Verdict and scope

I found no mathematical gap in Lemmas A–E or their combination for three
linearly independent quadrics, dimension `n>=3`, PDLC, strict feasibility,
and a proper ordinary convex hull. The resulting bound is four strict good
aggregations. This is an independent mathematical review, not a formal
verification or a novelty certificate. The published four-aggregation theorem
is an external input; I checked its statement and relevant proof discussion,
but did not independently reconstruct its spectral-sequence arguments.

The most vulnerable steps are genuine proof obligations. In particular,
pointwise convergence alone does not preserve strict goodness, and an affine
projective formula alone does not justify a global pullback. The draft supplies
separate arguments for both. I initially flagged these issues before receiving
the full draft; they are resolved in the version reviewed here.

## Independent proof audit

**Generic inward levels.** The local-minimum-value argument is valid. The set
of local minimizers of a continuous semialgebraic function on a semialgebraic
set is semialgebraic, using quantified neighborhoods. If its values contained
an interval, definable selection followed by restriction to a continuity
interval would contradict local minimality at any interior selected value.
Thus only finitely many levels can fail the strict-sublevel closure property.
Applying this on the unit sphere treats every direction simultaneously. No
claim that every positive perturbation is regular is needed.

**Initial cone and perturbation.** Strict feasibility forces the initial
permissible aggregate to have a negative eigenvalue; permissibility gives
exactly one. A real quadratic form with one negative eigenvalue, including a
singular form, has two antipodal open convex negative cones. Strict goodness
puts the connected lifted ordinary convex hull in one cone. Adding `epsilon I`
raises all zero eigenvalues and preserves the single negative eigenvalue for
small epsilon. Its negative cones lie in the corresponding old cones. The
original multiplier remains good for the inward strict system. PDLC and
linear independence are open conditions on the matrix triple.

**Chart and original homogenizing coordinate.** Write `t` for the original
last coordinate and `l` for the oriented negative-eigenvector functional of
the perturbed aggregate. A strict homogeneous feasible point with `l>0,t<0`
would have an antipode whose normalization to `t=1` is an original-chart
feasible point in the wrong cone. This is impossible. A strict point with
`l>0,t=0` would give such points by openness. Therefore the complete strict
system in the chart `l=1` is precisely the projective image of `S_epsilon`.
This is not an implicit addition of a fourth constraint.

The aggregate is positive definite on `ker(l)`. Hence the nonstrict chart
system has no nonzero feasible vector at infinity and lies in a bounded
ellipsoid. The sphere closure property transfers to the chart by normalizing
nearby homogeneous strict points by their positive `l` values. It follows
that the chart set is the closure of its nonempty open strict part and thus
the closure of its interior. These are exactly the geometric assumptions
needed for the external four-bound.

**Strictification.** A quadratic polynomial that is nonpositive on a
neighborhood and vanishes at its center has zero gradient and negative
semidefinite Hessian there. Taylor's formula is exact, so it is globally
nonpositive. Consequently a nonredundant quadratic in a finite closed
description cannot vanish in the interior of the described set. Removing
globally nonpositive quadratics leaves at most four inequalities and makes
their strict intersection the interior of the closed hull. The identity
`int(cl(conv T))=conv T` applies because `T` is nonempty and open.

Deleting these tautological closed inequalities is necessary in principle:
`-x_1^2<=0` imposes no restriction, whereas `-x_1^2<0` removes a hyperplane.
The draft does not make this invalid direct strictification.

**Global pullback.** A nonzero point strictly satisfying every selected
homogeneous aggregate cannot lie on `l=0`: nearby strict points with arbitrarily
small positive `l` would normalize to unbounded points of the bounded chart
hull. Thus the full homogeneous strict intersection has only its positive
and negative chart cones. On the positive one, `t>0`, since this holds on the
chart feasible set and is preserved by convex combinations and positive
scaling. The negative cone has `t<0`. The section `t=1` therefore selects
exactly the positive cone. Positive projective normalization preserves
convex combinations with the usual denominator-adjusted weights. This proves
the equality globally in the original affine space, not just in the initial
domain of the projective map.

**Limit and strict goodness.** The multipliers lie in a compact simplex;
padding by repetitions makes simultaneous subsequences legitimate. Every
limit matrix has at most one negative eigenvalue by inertia continuity and
has at least one by evaluation at a fixed original strict feasible point.
Its negative eigenvalue is simple and separated from the nonnegative
spectrum. Negative eigenvectors can therefore be selected along a convergent
subsequence and oriented at that point.

For each original strict feasible point, eventual membership in every inward
set puts its lift on the positive side of each oriented negative eigenvector.
The limit scalar product is nonnegative. It cannot be zero, because the
limiting quadratic value there is strictly negative, while the quadratic is
nonnegative on the orthogonal complement of its negative eigenvector. All
original feasible lifts therefore lie in one open convex negative cone of
each limit aggregate. This proves strict validity on the entire ordinary
convex hull. Conversely, simultaneous strict satisfaction of the four limit
inequalities persists for all sufficiently large indices and hence implies
membership in an inward hull, which lies in the original hull. No interchange
of closure and convex hull is being assumed in this step.

This argument also handles a rank-one negative-semidefinite limiting matrix.
That case is a useful stress test: mere nonstrict validity could allow the
zero hyperplane to cross the hull, but the orientation argument forbids it.

## Dependent triples

The draft's reduction to extreme rays is correct. Evaluation at a strict
feasible lift is strictly negative on every nonzero conical combination of
the defining matrices. The generated cone is therefore pointed. In dimension
at most two it has at most two extreme rays, each represented by a defining
matrix. Every other strict constraint follows from their strict constraints.

There is a direct source route for completing this case. In the local BDS
text, Theorem 2.17 applies with `m=2`: its condition on distinct triples is
vacuous, HHC holds for two forms, and the bound is `m^2-m=2`. The adjacent
paragraph headed “Span of Q1,...,Qm is two dimensional” explicitly gives the
same reduction and cites Yildiran's Theorem 1. This does not require treating
an uninspected version of Yildiran's theorem as a new assumption. Dimension
one in matrix span cannot combine PDLC with a nonempty proper strict hull:
the feasible inequalities must be negative multiples of a positive definite
form and are then true everywhere in the affine chart.

## Literature and novelty audit

I inspected the local BDS full text, including Theorem 2.17, Example 2.20,
Conjecture 3.2, and the dependent-span discussion. The paper gives a strict
six-bound and a four-necessary example. Its source version must be named:
the corresponding aggregation theorem is numbered 2.18 in the inspected
[arXiv v2](https://arxiv.org/html/2210.01722v2).

I independently opened [Blekherman–Dunbar arXiv v1](https://arxiv.org/html/2405.18282v1).
Theorem 1.4 assumes PDLC, nonempty interior, closure of the interior, and no
points at infinity. Section 8 explicitly removes spectral smoothness from
the PDLC discussion. Thus the transfer does not need a generic smooth
determinant curve. The chart satisfies the stronger no-infinity condition,
not merely boundedness. The publisher eprint did not load during this review;
the statement was checked in the authors' openly available preprint.

I also retrieved indexed primary-source text of [Dunbar's dissertation](https://etd.library.emory.edu/downloads/2j62s637x?locale=en).
Theorem 5.0.5 states a four-bound without the no-infinity condition, while
retaining closure of the interior and nonempty interior. The immediately
following discussion still distinguishes the strict conjecture. The full
PDF did not load. This is evidence that the proposed strict transfer goes
beyond that displayed theorem, not proof that no equivalent argument appears
elsewhere in the dissertation.

Additional searches combined “four aggregations,” “strict,” “Conjecture 3.2,”
and “Dunbar 5.0.5.” They did not locate an explicit general strict four-bound.
An unsuccessful search does not establish novelty. Full inspection of the
dissertation and a broader citation check remain appropriate before making
an unqualified priority claim.

## Significance and verification limits

Conditional on the external four-bound, the proof removes substantial
geometric restrictions and improves the known general strict upper bound
from six to four in the stated dimension range. It would rule out the
six-necessary conjecture there; the cited four-necessary example would make
the bound sharp. The added contribution is the transfer argument, not the
original topological four-bound.

This is a structural convexification theorem. It does not supply an efficient
procedure for computing the limiting multipliers, prove favorable numerical
conditioning, or establish a solver speedup. General nonstrict sets with
lower-dimensional feasible components are not covered merely by replacing
`<` with `<=` in the conclusion.

Verification consisted of an independent line-by-line mathematical audit,
targeted primary-source inspection, and the explicit rank-one and
projective-horizon stress tests above. No numerical test or Lean check was
run: neither is needed for the elementary spectral and topological steps
identified here, and no such check has been represented as certifying them.
No project-wide verification or CI inspection was performed.

## Follow-up: shorter proof and dimensions one and two

The author and root subsequently replaced the projective construction by a
shorter proof in [the result note](../results/four-aggregation-strict-pdlc.md).
I independently rechecked the replacement. It is valid and removes the need
for an initial good aggregation or the BDS dimension restriction.

If a nonzero direction `d` satisfies `d^T A_i d<0` for every defining
quadratic, then for any fixed `x`,

```
f_i(x+td)=t² d^T A_i d+2t d^T(A_i x+b_i)+f_i(x),
f_i(x-td)=t² d^T A_i d-2t d^T(A_i x+b_i)+f_i(x).
```

Both values are strictly negative for all sufficiently large `t`,
simultaneously for finitely many `i`. Thus every `x` is the midpoint of two
feasible points. A proper hull rules out such a direction. A nonzero common
nonpositive direction of `A_i+epsilon I` would be a common strictly negative
direction of the original `A_i`. Therefore every inward perturbed system has
no points at infinity in the original affine coordinates. An unbounded
feasible sequence, divided by its norm, would produce just such a direction
after passage to a unit-vector subsequence. The perturbed nonstrict set is
therefore compact.

The replacement regular-level lemma is also correct and simpler. Every
exceptional sublevel value is the infimum of the function on a member of a
countable topological base. There are consequently at most countably many
exceptional values. Compactness and semialgebraicity are unnecessary for this
lemma. Applying it to `max_i f_i(x)/(1+||x||²)` gives exactly the required
regular inward sets. The previously reviewed strictification and limiting
negative-eigenvector argument apply unchanged.

I rechecked the source dimension issue. BD Theorem 1.4 imposes no `n>=3`
restriction, and its proof explicitly separates `n=1`, `n=2`, and `n>=3`.
The new independent-triple argument therefore works for every `n>=1`.
The earlier BDS-based dependent-triple shortcut in this review applies only
for `n>=3`; it should not by itself be cited to justify lower dimensions.
The author reports separately inspecting Yildiran's all-dimension theorem.

Here is an independent way to cover the dependent case in all dimensions
without an additional external theorem. Suppose the matrix span has dimension
two, with nonzero relation `sum_i a_i Q_i=0`. Choose a positive definite
matrix `R` outside that span and a strictly positive vector `d` with
`sum_i a_i d_i!=0`. Such choices exist: the positive definite cone has full
dimension in the symmetric matrix space, which has dimension at least three
when `n>=1`, and a nonzero linear functional cannot vanish on the positive
orthant. Set

```
Q_i^epsilon=Q_i+epsilon d_i R.
```

These three matrices are independent for every nonzero epsilon. Indeed, any
relation among them first gives a relation among the `Q_i` by projection
modulo their span, and is then a multiple of `a`; its coefficient along `R`
forces that multiple to be zero. Each perturbation is positive definite, so
the no-infinity argument, strict feasibility, and PDLC persistence still
hold. Apply the countable-level lemma to

```
h(x)=max_i f_i(x)/(d_i (x,1)^T R (x,1)).
```

The denominators are positive. BD applies to generic inward levels, and the
limit matrices differ from `sum_i lambda_i Q_i` by
`epsilon (sum_i lambda_i d_i)R`, which converges to zero uniformly on the
multiplier simplex. The already reviewed limit proof yields the same four
bound. If the original matrix span has dimension one, PDLC and strict
feasibility force all defining forms to be negative multiples of a positive
definite form, so `S=R^n`; this is excluded by the proper-hull hypothesis.
Thus the universal four-bound for every `n>=1`, including dependent triples,
has an independently checked route using only BD as an external theorem.

The priority reviewer has since obtained the dissertation's full text and
documented a mismatch between its stronger theorem statement and the
no-infinity hypotheses in its proof dependencies. See
[the priority audit](review-20260922-pdlc-priority.md). This supersedes the
earlier access limitation recorded above. The argument under review uses
only the published theorem with its full hypotheses and is unaffected by
that discrepancy.
