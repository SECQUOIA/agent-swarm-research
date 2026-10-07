# Independent review of simplex face margins, closure, and exact output

Date: 2026-10-02. Verdict: passed after the corrections recorded below.
This review read the actual
[simplex-block extension](../new-direction/simplex-block-smoothed-extension.md),
especially Sections 4--6, and the supporting finite-tail, exact-fallback,
and convex-evaluation notes. It also checked the final equality-block
corollary in Section 7. The separate
[geometry and count review](../new-direction/simplex-block-noise-review.md)
covers feasible block rounding and face-stratified counts. This review
does not infer correctness merely from that earlier geometry check.

**Conclusion.** The original-face tests, dependent finite-grid multiplier
count, good-event closure, and polynomial-bit implicit-output evaluation
are sound for the stated product of disjoint unit simplices and native
integer intervals. The proof requires whole-block bags, a block Hessian
upper bound, and a fixed explicit polynomial degree. It does not extend
to overlapping resource constraints or establish FPT in bag size.

## 1. Original-face tests and tangent closure

All three face-forcing rules use directions feasible in the original
simplex. A positive derivative permits decreasing a positive coordinate;
a negative derivative permits increasing that coordinate when the budget
is slack; and a positive derivative difference permits transferring mass
from the first coordinate to the second. The artificial retained hull
need not admit those directions. That is harmless: the optimizer is one
of the original problem, and the derivative bounds hold at that optimizer.

The multiplier interpretation is correct. At a tight budget there is a
positive coordinate serving as anchor. Its derivative is the negative
budget multiplier. Every zero coordinate's derivative difference from
that anchor is its nonnegativity multiplier. At a slack budget the latter
multiplier is the coordinate derivative itself. Original simplex active
normals are linearly independent, so there is no ambiguous choice of
multipliers. No lower bound on a positive coordinate or on a slack budget
is needed to identify the active constraints on the stated good event.

The derivative-difference error is at most four times the Hessian row-sum
bound times the retained radius scale. Hence the stated
`h<=tau/(8 M_1 A)` condition leaves a strict sign margin. The integer
singleton argument is unchanged because it concerns physical coordinate
distances, not the shape of continuous cells.

After every active original equality has been found, point growth yields
`Z'H(a)Z>=2g_0 Z'Z` by two-sided tangent Taylor expansion. The anchor
bases have Gram matrices `I+11'` on tight blocks and identity on slack
blocks; therefore `I<=Z'Z<=nI`. Hessian variation by at most `Tr` in
ambient operator norm is exactly the generalized correction used in (9).
At the cutoff, `r<=2Ah<=g_0/(4T)`, leaving the positive margin
`g_0-2Tr>=g_0/2` in that test. Convexity on this retained affine patch,
together with its certified containment of every global optimizer,
proves exact global optimality of its unique constrained minimizer.

One substantive input-domain clarification was made during review.
A coordinate-hull midpoint can lie outside its simplex, for example the
midpoint of `[0,1]^3`. Derivative bounds verified only on the product
of simplices would not justify evaluation and line segments through that
midpoint. The final text explicitly verifies `M_1` and `T` on the enclosing
coordinate box. Monomial bounds provide this with polynomial encoding;
their magnitudes enter only the cutoff logarithm. The block-curvature
premise needed for feasible rounding remains on the original continuous
domain.

## 2. The finite-noise normal-margin bound handles dependence

The restriction of linear noise to an original product face depends only
on its tangent coefficients. On a tight simplex block, shifting all
positive-support coefficients by the same amount changes the restricted
objective only by a constant. Hence after anchor subtraction the free
stationarity equations depend on the tangent differences and on the
slack-face tangent coefficients, but on no normal coefficient.

This remains true when polynomial factors couple several simplex blocks:
one joint stationary system in the total `k` free coordinates is used.
Positive point growth makes its tangent Hessian nonsingular. Its relevant
roots are isolated over the complex numbers and number at most `D^k`.
Other stationary components may be singular or positive dimensional;
they are not assumed finite. The zero-dimensional and degree-one cases
are handled by the empty-root-system convention already stated.

The transformed finite-grid coefficients are dependent. The proof correctly
counts tuples instead of assigning an unjustified conditional density.
If there are `t<=k` anchor-difference coordinates, fix all transformed
coordinates except the normal coordinate used for one multiplier. There
are at most

```
(2M-1)^t M^(n-t-1)
```

such choices. For each joint nonsingular root, that multiplier has slope
one or minus one in the remaining original normal coefficient. Its
absolute-value slab contains at most `tau(M-1)/sigma+1` labels. Dividing
by the original `M^n` equally likely tuples and multiplying by `D^k`
proves the bound `2^k D^k (tau/sigma+1/M)`. Invalid transformed tuples
are merely overcounted. This argument covers both budget and zero-coordinate
multipliers and does not condition the probability law on positive growth.

A `b`-simplex has at most `3^b` nonempty faces and `b+1<=2b` facets.
The displayed union factor over product faces, facets, and integer
assignments is consequently safe. In particular, finite-grid atoms at
zero multipliers are covered; they are not dismissed by genericity.

## 3. Growth, fallback, and the base-only cutoff

The point-growth formula is unchanged except for replacing continuous-box
membership by linear simplex inequalities. It still has two quantified
blocks of size `n` and one scalar free coefficient. Integer-label
disjunctions add atoms but no blocks. Thus the same primary fixed-block
quantifier-elimination bound gives `exp(poly_d(I))` components uniformly
over every fixed-noise scalar section and threshold.

The lexicographic exact fallback also carries over. Compactness supplies
one canonical selected optimizer; the same scalar singleton formulas,
bit-model elimination bounds, and univariate root isolation represent
its coordinates and value consistently. Neither box geometry nor a finite
KKT solution set is needed for this part. Projection onto the original
simplex, rather than coordinate clipping alone, repairs its rational
approximants feasibly.

The two tail substitutions each give failure probability at most `rho`.
All quantities through `J` are determined from base input; choosing `M`
afterwards introduces no dependence of the combinatorial fallback budget
on the sampled coefficient height. With `rho=1/(4B)`, the total fallback
probability is at most `1/(2B)`. The original expected-size qualification
for the full trace, in contrast with the polynomial-size local descriptor,
is preserved.

## 4. The evaluator is a complete bit argument

The revised Section 6 removes its former evaluator placeholder. A capped
simplex face with nonzero widths is either a singleton, which is substituted,
or has the displayed rational strict center. For a tight sum, the common
interpolation fraction lies strictly between zero and one. For a slack
sum, the chosen fraction leaves both every bound and the budget strict.
Dropping one anchor in equality blocks gives an explicit full-dimensional
product of rational boxes with total-sum slabs.

The minimum slack divided by `1+||a_s||_1` is a valid Euclidean inradius
in these reduced coordinates. All slacks are strictly positive rationals
of polynomial encoding length, even if numerically very small. Expansion
of the anchor substitution costs only a fixed-degree polynomial factor.
No optimizer-slack bound or positive numerical inradius promise is hidden
in this construction.

Projection onto the reduced box-and-slab product is exactly rational.
If clipping violates a sum bound, the active sum is that endpoint and
the common threshold is found among sorted rational breakpoints. On an
interval with a fixed free set, its denominator acquires at most the
number of free coordinates. Feasibility and the projection KKT conditions
hold also at breakpoints and plateaus. Thus the repair has polynomial
bit work and the nonexpansiveness required by the GLS argument.

The capped epigraph has the stated rational inner ball, bounded outer
radius, and rational strong separation. The homothety estimate handles
comparison with an eroded body; projection handles approximate feasibility.
Together they give exactly the displayed feasible upper value and lower
endpoint. The extra factor `n` in the distance tolerance safely converts
reduced-coordinate error to physical-coordinate error through `Z`.
Strong convexity need not hold outside the patch, and its minimizer need
not lie in its relative interior. These facts establish polynomial bit
evaluation of the successful compact descriptor, not merely a real-arithmetic
iteration bound.

The final text also explicitly limits the displayed algorithmic bound to
the supplied polynomial-time curvature-verification format, or adds a
more expensive verifier's actual cost separately. Proof length alone is
not treated as a polynomial verification guarantee.

## 5. Original equality-simplex blocks

The final Section 7 is sound with its explicit rule changes. A budget
equality is recorded initially, and both absolute-gradient tests are
omitted for that block. Positive partial derivatives alone cannot force
zero coordinates on an equality simplex: even a strictly convex objective
can have positive partials at its positive interior minimizer. The feasible
derivative-difference transfers remain valid and identify active zero
coordinates on the margin event.

The equality multiplier is unrestricted and properly has no positive
margin requirement. Anchor-difference counting still treats original
ambient noise without assuming independence after coordinate elimination.
All original faces are now tight-support faces, reducing rather than
increasing the preceding count. The scalar membership formulas remain
linear, and the relative evaluator already handles equality faces.
One-coordinate equality blocks are fixed points and must be substituted;
if nothing remains, direct evaluation precedes the positive-width cutoff
formulas. Sampled noise on such a fixed coordinate is only an additive
value constant.

## 6. Independent targeted verification

I wrote and ran

```
python3 -B research-20261002/reviews/check_simplex_patch_review.py
```

The [checker](check_simplex_patch_review.py) passed 668 exact finite-noise
draws on strongly convex two- and three-dimensional simplex quadratics,
154 face/multiplier probability comparisons, and 75 zero-multiplier
incidences. It also passed three rational relative-interior-ball checks
and 27 exact projection/feasibility/KKT checks, including an equality
patch with 200-bit thin coordinate widths. These checks target the new
normal-margin and evaluator interfaces; they do not implement the sparse
DP or prove the asymptotic expected bound experimentally.

The analytical review covers the complete current Sections 4--7. Scoped
document and Python syntax checks passed. No external search, delegation,
project-wide verification, CI inspection, or index edit was performed
for this review. No priority claim is implied.
