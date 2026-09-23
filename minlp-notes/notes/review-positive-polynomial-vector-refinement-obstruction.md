# Independent review: positive vector powers and refinement obstruction

Date: 2026-09-05. Verdict: **PASS** for
[the candidate](positive-polynomial-vector-refinement-obstruction.md).
The integer lower bounds, binary upper bound, midpoint statement,
scalarization statement, and interval-refinement contrast all hold as stated.
No mathematical correction is required. This is a proof audit, not an
independent priority determination.

## Rational witnesses and the non-midpoint obstruction

The exponent identity `128*1024^(j-1)=2^(10j-3)` is correct. The inputs
`x_j=1-64/D_j` are distinct, rational, increasing, and belong to `[1/2,1)`.
For `j<ell`, ordinary Bernoulli with the positive integer exponent `D_j`
gives `x_ell^D_j>=1-64D_j/D_ell>=15/16`.

The two-thirds input average has the stated upper bound. Its power is at
most `exp(-64/3)<=3/67`. This estimate can alternatively be proved without
exponentials: for `u=64/(3D_j)` in `(0,1)`, Bernoulli gives
`(1-u)^(-D_j)>=(1+u)^D_j>=1+D_j*u=67/3`.
The ignored term `F_j(x_j)/3` is nonnegative. Thus the exact asserted
lower bound is

```
(7/4)[(2/3)(15/16)-3/67]=2177/2144=1+33/2144>1.
```

The strict margin is sufficient to violate the closed error box. The
argument does not require estimating the tiny value of the earlier endpoint
or imposing bounds on lift witnesses.

## Convex lifts and the two integer counts

If two unrestricted integer witnesses have the same residue vector modulo
three, their weighted average with weights `1/3,2/3` is integral in every
coordinate. All continuous auxiliaries can be averaged as well, and the
convex lift contains that point. Its projection has precisely the vector
chord error just proved. Consequently all selected witness residues must
be distinct, giving `M<=3^p`.

For binary witnesses with the same vector, every real convex combination
retains that binary vector. The same obstruction therefore forces `M`
distinct binary vectors, giving `M<=2^p`. No assumption of closedness,
compactness, rational coefficients, or bounded general integers is used.
Binary lifts are a subclass of unrestricted-integer lifts, so the direction
`p_conv<=p_bin` is correct.

The half-height points are distinct and sort into `M+1` compact intervals.
On each interval every component stays on one side of its own half-height
point, so that component's full range has length at most `7/8`. The input
interval times all output ranges is convex and stays within error `7/8`
of every graph point at the same input. The finite union has a bounded
linear disjunctive formulation with `ceil(log2(M+1))` binary bits, even
when the number of pieces is not a power of two: unused codes are excluded
by the selector-sum condition. Real coefficients are permitted in the
stated count. This upper bound does not establish a compact rational
encoding in the sparse exponent length.

## Midpoints and interval covers

The partial derivatives of the midpoint Jensen gap have the claimed signs,
so its maximum on all pairs is attained at `(0,1)`. The endpoint value is
`7/8-(7/4)2^(-D_j)<7/8`. Thus the claim is global, not restricted to the
selected rational witnesses.

The full-domain chord has component error at most `7/4<2`, proving
`N_F(2)=1`. If an interval contains two selected inputs, its component
chord lies above the convex component at both selected inputs. Subtracting
the smaller chord gives an affine function nonnegative at its endpoints,
so the containing-interval chord has at least the previously certified
error at their two-thirds average. Each error-one interval therefore
contains at most one selected witness. Overlapping intervals and shared
endpoints do not defeat the count, so `N_F(1)>=M`.

The argument is a failure of uniform error-refinement control as output
dimension grows. It does not imply an unbounded difference between binary
and unrestricted integer minima.

## Signed and affine scalarizations

The reference `Psi=sum |lambda_j|F_j` is strictly increasing when
`sum |lambda_j|=1`, and its endpoint range is exactly `7/4`. The triangle
inequality bounds every scalarized increment by the corresponding `Psi`
increment, regardless of signs. Splitting at its unique half-height point
therefore bounds the full scalar range on either compact interval by
`7/8`. Actual minima and maxima exist by continuity, even if the signed
scalarization is not monotone. Two input-output rectangles give the
claimed one-binary linear formulation at scalar tolerance one.

The support function of `[-1,1]^M` at the normalized vector is one, so the
comparison uses the proper scalarized tolerance. The normalization is not
hiding an output-dependent error scale. The claim even extends to
`lambda^T F(x)+beta*x+gamma`: apply the same formulation after the affine
output change `y'=y-beta*x-gamma`. Its rectangles become polyhedra, with
no additional binary variables. Arbitrary real scalarization coefficients
are compatible with the unrestricted-real coefficient convention for
these finite counts; rational encoding complexity is not asserted here.

## Independent exact checks

[The independent checker](../code/positive_vector_obstruction/check_first_review.py)
passed 120 rational witness-spacing pairs, 15 actual rational power-gap
calculations in the first output, and 306 modulo-three combination checks
in integer dimensions one and two. The arithmetic margin was verified
exactly as `33/2144`. These checks use exact fractions and supplement the
uniform proof.

## Addendum: output-dependent finite binary upper bounds

The subsequently appended box and unconditional-polytope corollaries both
**PASS**. Their finite real-coefficient, unrestricted-size scope is essential
and is stated correctly.

Given a convex lift with `p` integer coordinates, each input has an exact
witness in at least one of the `2^p` parity classes. The interval hulls of
those classes therefore cover the domain. If a nonempty class has infimum
`u` and supremum `v`, choose original class inputs tending to both endpoints.
Their lifted midpoint has integer coordinates. Its projected Jensen vector
belongs to the allowed error body. Continuity of `F` and closedness of the
box or polytope permit passage to the endpoint limit; closedness of the
lift itself is unnecessary. Singleton hulls cause no difficulty.

For a nonnegative concave chord-gap function vanishing at the endpoints,
`g(x)<=2g((u+v)/2)` follows by expressing the midpoint as a convex
combination of `x` and the opposite endpoint. The weight on `x` is at
least one half. Applying this coordinatewise yields the claimed doubled
box bound, and multiplying by a nonnegative facet row yields its doubled
scalarized bound for the unconditional polytope.

The scalar two-crossing refinement is valid for arbitrary continuous
convex components. If the gap exceeds the target level, the boundary
points of its strict superlevel interval have gap exactly that level.
On the outside pieces, subtracting the affine interpolation of nonnegative
endpoint gaps cannot increase the gap. On the middle piece, that affine
interpolation is the constant target level. Thus a doubled gap bound is
halved using at most three intervals. Restricting an interval cannot
increase a convex function's local chord error, so overlaying different
components' or rows' cuts preserves their guarantees.

For the box, at most `2m` cuts produce `2m+1` intervals per parity class.
If `g_j=T_j-F_j` lies between zero and `epsilon_j`, the band
`T_j-epsilon_j<=w_j<=T_j` contains `F_j` and gives
`w_j-F_j` between `g_j-epsilon_j` and `g_j`, a subset of the required
symmetric interval. There are at most `(2m+1)2^p` bounded polyhedra, so
binary disjunction gives exactly the stated integer-count upper bound.

For `K={e:A|e|<=b}` with `A>=0,b>0` and compact `K`, each row of `AF`
is convex. Two applications of the scalar refinement produce at most
nine intervals, hence eight cuts, per row: the second refinement is
performed on each of the at most three first-stage intervals. Overlaying
rows therefore produces at most `8q+1` intervals, not `9^q`. On each,
`Ag<=b/2` and `g>=0`, so `g` belongs to `K/2`. The band
`w-T in K/2` contains the graph because `-g` also belongs to `K/2`.
Every admitted error is the sum of two points in `K/2`, hence belongs to
`K` by convexity. Symmetry supplies the graph-containment direction.
The compact input interval and compact body make each band bounded;
the body has a finite linear representation, directly or with continuous
absolute-value auxiliaries. The same finite binary-disjunction argument
proves the `ceil(log2(8q+1))` overhead.

The proof does not replace `K/2` by `K` in this last construction. Such a
replacement would in general permit errors in `2K`; the caution in the
candidate is justified. Neither corollary establishes efficient knot
computation, rational encoding bounds, or a matching lower bound on the
difference between binary and unrestricted integer minima.
