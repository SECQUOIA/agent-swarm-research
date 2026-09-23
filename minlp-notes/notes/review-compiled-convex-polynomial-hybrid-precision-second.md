# Independent second review: hybrid construction for convex polynomials

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Candidate: [compiled convex-polynomial hybrid](compiled-convex-polynomial-hybrid-precision.md).
Analytical dependency: [signed monotone-curvature integration](certified-monotone-polynomial-curvature-quantiles.md).
Verdict: **PASS**, including an independent audit of the analytical dependency
below. This review finds no remaining mathematical or bit-complexity gap in
the stated dense rational convex-polynomial model. Other reviewers' approval
and publication priority remain separate matters.

The claimed construction uses at most `p_conv+11` declared binary variables.
Its comparison includes arbitrary convex lifts with unrestricted continuous
size and general integer variables. The result is a polynomial-time
construction, not a polynomial-time MILP solution algorithm.

## Chord perturbation and rounding an unknown optimal partition

The rational bound `M=max(1,sum k|c_k|)` controls both the Lipschitz constant
of the function and every chord slope. For an old interval `[a,b]` and its
expansion by at most `h` at either endpoint, compare the two chords at `a`
and `b`. At `a`, for example, the expanded chord differs from `f(a)` by
at most `M(a-a')+|f(a')-f(a)|<=2Mh`. The same holds at `b`, and linearity
bounds the chord difference throughout `[a,b]`. On an added strip, comparing
to its new endpoint gives a direct bound `2Mh` for the new chord gap.
Therefore an old error bound `eta` becomes at most `eta+2Mh`. Restricting
to a subinterval cannot increase a convex function's chord error.

Rounding an optimal partition's knots downward and removing duplicates
does produce the required nearby intervals. To see the only potentially
delicate point, take two consecutive distinct rounded values. The transition
between their runs in the original ordered knot list occurs at an adjacent
pair of original knots. Their rounded values are precisely the two values
under consideration, and each is within `h` of its original knot. Hence
the retained interval lies in that original interval's expansion by `h`.
The endpoints 0 and 1 remain exact dyadic grid points.

With `h<=epsilon/(32M)`, the rounded partition has error at most
`epsilon/4+epsilon/16=5epsilon/16<epsilon/2`, using no more than
`N_(epsilon/4)` intervals. Repeated knots cause no uncovered gap.
The proof only asserts existence of this comparison partition; the
algorithm does not need its unknown knots.

## Exact grid predicate and the small-count branch

For rational grid endpoints, the chord coefficients and the polynomial
`chord-f-epsilon/2` have polynomial encoding. The denominator `b-a` may
be tiny, but its binary length is at most the polynomial grid precision.
Exact univariate real-root isolation and sign tests decide whether this
polynomial is nonpositive on the interval. Testing signs between roots
handles zero maxima and repeated roots without an approximate threshold
comparison. The predicate polynomial is nonzero since its endpoint value
is `-epsilon/2`.

For a fixed left endpoint, feasibility is monotone in the right endpoint:
every smaller interval is a restriction of the larger one. A one-step
grid interval is feasible because its error is at most `2Mh<epsilon/2`.
Consequently binary search finds the farthest feasible endpoint using
`O(B)` exact decisions. Both the numerical value of `B` and the bit lengths
of all grid indices are polynomial in the input and tolerance encoding.

The farthest-endpoint greedy partition is optimal among feasible grid
partitions. Inductively its current endpoint is at least the comparison
partition's endpoint. If that comparison partition's next endpoint is
ahead, its remaining interval is a feasible restriction starting at the
greedy endpoint. Otherwise the desired dominance already holds. Thus
the eventual greedy count satisfies
`G<=N_(epsilon/4)<=9N_epsilon`.

Run at most `9D` iterations. If they reach 1, then
`G<=27*2^p_conv` by the reviewed scalar parity and refinement inequalities.
The finite union of these polynomially many rational bands uses
`ceil(log2 G)<=p_conv+5` binaries. Exact endpoint evaluation and downward
rounding by at most `epsilon/8` preserve the stated band, since the true
chord error is at most `epsilon/2`, below `13epsilon/16`.

If the procedure has not reached 1 after `9D` iterations, the full greedy
count is strictly greater than `9D`. The same existence comparison therefore
forces `N_epsilon>D`. This inference is valid even though the remainder of
the possibly enormous greedy partition is never generated.

## Rational monotone pieces and the fallback cell sum

Real-root isolation supplies disjoint rational brackets of width at most
`h` around the distinct interior roots of `f'''`. Bracket endpoints can
be chosen not to be roots and inside `(0,1)` using polynomial refinement;
rational roots need not be retained as singleton brackets. The roots at
0 or 1 require no bracket. A zero polynomial `f'''` requires no split.
Its nonzero constant case also requires no split.

Between brackets the derivative of curvature has a constant sign, so
curvature is monotone. Global convexity keeps it nonnegative. The at most
`D-3` interior roots for `D>=3` give at most `2(D-3)+1` pieces; the stated
uniform bound `b<=3D` safely covers lower degrees and all omissions of
zero-length pieces. Each narrow bracket has chord error at most
`2Mh<=epsilon/16` and is represented with one cell.

Normalizing a rational complementary interval to `[0,1]` and reflecting
decreasing curvature preserve convexity and the required curvature
monotonicity. Dense polynomial substitution has polynomial coefficient
encoding: the degree, endpoint lengths, binomial coefficients, and powers
of rational endpoints are all polynomially bounded. Reflection may change
coefficient signs, which is why the signed integration dependency is needed.

For each piece, let `n_j` be its optimal chord count at tolerance `epsilon`.
Splitting a globally optimal partition at the `b-1` new boundaries adds
at most that many intervals. Restriction preserves chord error, so
`sum n_j<=N_epsilon+b-1`. The reviewed curvature theorem and local
compiled count give `K_j<=120n_j+2`; this also bounds a bracket's single
cell and any affine piece.

Summing local counts, rather than multiplying their maximum by the piece
count, gives

```
K_total<=120N_epsilon+122b
       <=120N_epsilon+366D
       <486N_epsilon
       <=1458*2^p_conv
       <2048*2^p_conv.
```

The strict step uses only the proved fallback condition `N_epsilon>D`.
It follows that `ceil(log2 K_total)<=p_conv+11`.

## A single global index and rational decoding

Every local cell count is a power of two, except that a bracket uses
one cell. Its binary encoding is polynomial even when its numerical value
is exponential. Their cumulative sums and `K_total` therefore have
polynomial encoding. A global index identifies a piece by rational/integer
comparisons and subtraction. Invalid codes above the final cell count
can be excluded by a Boolean comparison whose output is fixed to true.

A deterministic bounded algorithm can run only the selected local routine.
Alternatively, all local routines can be run with zero as the unused
pieces' dummy local index, followed by output selection. This supplies
valid local inputs and makes the polynomial-time circuit construction
explicit; no extra declared binary selector is needed.

After the local dyadic knots are mapped back to original coordinates,
each lies on an affine rational image of a dyadic grid. The product of
all piece-endpoint denominators, multiplied by the largest required
power of two, is a common denominator for every input knot. Its bit
length is a sum over polynomially many endpoint lengths and is therefore
polynomial. Reflection uses the same denominator. The numerator is
nonnegative and at most that common denominator, with a polynomial
number of bits including the exact endpoint 1.

Exact evaluation of the original dense polynomial at a rational knot
has polynomial bit length. Round downward to a common nonnegative
fractional precision with error at most `epsilon/8`. A fixed integer
offset larger than `sum |c_k|` makes all decoded output numerators
nonnegative. This remains true after downward rounding: the negative of
the offset is itself a point of the dyadic grid below every exact value,
so downward rounding cannot cross it. Choosing fractional precision at
least zero handles large tolerance requests as well.

Linear rational decoding of the input and shifted output bits reduces
the interpolation step to the already reviewed circuit compiler. Integral
global index bits force every gate wire Boolean. Products with the common
continuous interpolation weight are then exact by their binary-product
inequalities, although the wires themselves have no integrality declaration.
Undoing the output offset is an exact affine equation.

Within any cell, the interpolated rounded output differs from the true
convex graph by an amount in `[-epsilon/8,13epsilon/16]`. The common band
therefore contains the graph and admits only absolute error at most
`15epsilon/16`. Reversed or repeated local knots do not affect this
argument. The continuous local polygonal input path joins its piece
endpoints, so its cells cover that entire piece. Taking their union covers
`[0,1]`. The integer count is exactly the global index length; neither
branching nor rational decoding introduces hidden integer variables.

## Signed monotone-curvature integration: local certificate and tree size

I independently read the whole analytical dependency, rather than assuming
coefficient positivity was irrelevant. For a nonzero polynomial `H>=0`
that is nondecreasing on `[0,1]`, it is strictly positive on `(0,1]`:
a positive interior zero would force an interval of zeros and hence the
zero polynomial. Its endpoint value bounds `H` on the domain.

The original cutoff and branch-removal error budgets remain valid with
`U=max(1,H(1))`. The branch polynomial `(1-x)^2H-1` is nonzero because
its value at 1 is `-1`; its exact rational root isolation never required
positive coefficients.

At a rational center `c>0`, the test
`sum_(k>=1)|h_k(c)|ell^k<=H(c)/2` is an exact sufficient certificate.
It puts every value of `H` on the complex disk of radius `ell` into
the right half plane and bounds the modulus of its principal square
root by `2U`. The Taylor coefficients and test have polynomial bit cost
at any polynomial-bit center and interval length.

The crucial complexity argument is valid. Factoring algebraically only
for the proof gives
`H(c+t)/H(c)=product_j(1+t/(c-alpha_j))`. If all roots are at distance
at least `8d ell`, the sum of absolute Taylor terms is bounded by
`exp(1/8)-1<1/2` times `H(c)`, so the test passes. A failure is therefore
within `8d ell` of some root's real part. At one subdivision depth,
equal-length interval centers have spacing `ell`; each root can account
for at most `16d+2` failing centers. There are at most
`d(16d+2)` failures per depth. Repeated roots only weaken this upper bound.
Constant nonzero `H` is accepted immediately.

## Signed integration: root separation, depth, and precision

Adding the artificial factors `x(x-1)` ensures that 0 and 1 occur among
the distinct roots of the integer polynomial used for separation. Its
primitive square-free part has leading coefficient dividing that of
the primitive original polynomial. The Cauchy root bound and elementary
symmetric expansion therefore justify the displayed coefficient bound
`2^B`, with `B=(n+1)T+2n`.

The square-free discriminant is a nonzero integer. Bounding every root
difference except a selected one by `2^(T+2)`, and the leading coefficient
by `2^B`, gives the asserted deliberately loose separation
`sigma=2^(-(B+2)n^2)`. There are at least two distinct roots because of
the artificial 0 and 1; repeated roots were removed before applying the
discriminant. The bound does not require computing complex roots.

There is no real root of `H` in `(0,1]`. Real roots at or below zero
are at distance at least the cutoff `lambda`; real roots above 1 are
separated from 1 by at least `sigma`. Nonreal roots have conjugates,
so their imaginary parts have magnitude at least `sigma/2`. Thus every
root is at distance at least `rho_*=min(lambda,sigma/2)` from the retained
interval. Once the subdivision length is at most `rho_*/(8d_0)`, every
test succeeds. This takes polynomially many depths, not a polynomial
number of intervals in `1/rho_*`.

Combining this depth bound with the number of failed nodes per depth
gives a polynomial-size full binary subdivision tree. Its endpoints are
dyadic of polynomial encoding, so its exact Taylor tests have polynomial
total bit cost. The proof avoids the exponential uniform mesh that the
minimum root distance alone would produce.

After intersecting an accepted panel with branch regions or a query prefix,
the new center and length satisfy
`|c'-c|+ell'<=(ell+ell')/2<=ell`. Its required analytic disk is contained
in the original disk. The earlier summed Gaussian/Taylor error proof and
positive rational weight conditioning therefore transfer unchanged.

For the node function values, `V=max(1,sum k|H_k|)` supplies a rational
derivative bound. Monotonicity, not coefficient signs, makes evaluations
at rational node-bracket endpoints enclose the exact node value. The
square-root modulus bound converts a polynomial node precision into the
needed absolute function precision without a positive lower bound for
`H`. All four error budgets from the positive-coefficient integration
proof remain valid, as do its exact rational polynomial-branch integrals.

Finally, the stronger input-accurate inverse uses the exact rational
`H(eta/4)>0`. Its encoding is polynomial despite cancellation. The same
interior density lower bound and inexact bisection proof apply. The hybrid
formulation only needs mass accuracy, but this stronger analytical output
also passes review.

This independently closes the signed-curvature dependency for the hybrid
construction. It does not establish a general-purpose integration theorem
for arbitrary nonmonotone curvature; the hybrid handles that case by its
separate rational splitting argument.

## Supporting exact computation and scope

Inspected and reran `code/quadratic_rank/check_convex_polynomial_hybrid.py`.
It passed 70 exact expansion/rounding checks, 14 greedy-versus-optimal grid
comparisons using 2,040 exact chord decisions, and 11 global-index checks
including a local count of `2^40`.

The checker's chord decision uses square-free factors and Sturm counts
of odd-multiplicity roots. Since its decision polynomial is negative at
both interval endpoints, it becomes positive somewhere exactly when an
odd-multiplicity interior root changes its sign. This is a valid independent
predicate, including equality cases with even-multiplicity contact.
The examples include signed coefficients, nonmonotone nonnegative curvature,
and interior curvature zeros. These checks do not implement the general
certified quadrature routine or construct the full Boolean circuit; those
claims are supported by the proofs reviewed above.

The result is restricted to dense rational univariate convex polynomials
and positive rational tolerance. Checking the convexity promise is itself
a polynomial univariate sign decision. Affine polynomials are handled
exactly. Sparse huge degrees and multivariate nonseparable functions are
outside the statement. No proof correction was required by this review.

## Checked separable consequence

The hybrid also supplies the scalar cell estimate needed by the reviewed
[separable packing argument](review-positive-polynomial-linear-shape-precision-second.md).
At local tolerance `tau`, its actual cell count is at most `486N_tau`
in either branch: the small branch uses at most `9N_tau`, and the fallback
has the stronger strict bound above. Thus its declared index capacity
satisfies `2^L<=972N_tau<=5832P`, since a maximal Jensen packing at
tolerance `tau` gives `N_tau<=6P` by the three-way chord refinement.

Consequently the same polynomial construction extends to arbitrary dense
convex polynomial separable summands, using at most `p_conv+16r` binaries
for scalar sums and `p_conv+13r` for independent outputs. The respective
constants follow from `6*5832=34992<65536` and `5832<8192` using the
already reviewed radius-`r` product code or full product packing. Local
tolerances are `epsilon/r` for sums and `epsilon_i` for independent outputs.
The whole-graph and error proofs are unchanged. This checked consequence
was sent to the author; it requires no coefficient signs, monotone curvature,
or new integration primitive beyond the present hybrid theorem.

The author's final Section 5, which now states and proves these two
separable bounds explicitly, was reread and independently passes review.
It also correctly handles `r=0` by returning the exact affine graph.
