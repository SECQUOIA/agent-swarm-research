# Independent review: expected exact integer optimization with low-rank noise

Date: 2026-10-02. This review checks the actual
[integer theorem](../new-direction/smoothed-integer-low-rank.md), the
underlying [expected-cell argument](../new-direction/smoothed-semiconcave-cells.md),
and its [completed review](smoothed-semiconcave-cells-review.md).
Independent delegated checks examined the denominator closure, oracle
bit cost, and deterministic baselines.

The theorem passes. The same finite noise law supports the expected
cell bound and exact termination for every draw. No growth, uniqueness,
or fallback assumption is needed. The critical facts are that original
feasible points are integer vectors and that the sampling coordinates
share one denominator \(M-1\). No substantive mathematical gap was
found in the written model, constants, or bit bound.

## Exact recourse and the fixed noise-independent domain

For each rational auxiliary vector \(a\), the recourse objective
separates into convex univariate quartics minus linear terms. Convexity
on the original real interval makes its integer forward differences
nondecreasing. The stated first-nonnegative-difference search returns
an exact minimizer, including endpoint and tie cases. Its two neighbor
conditions certify optimality on the entire integer interval.

Binary search needs logarithmically many comparisons in the interval
cardinality. Fixed-degree polynomial evaluation, rational comparison,
and the sums involving \(T^Ta\) have polynomial bit cost. Large
binary-encoded integer ranges are not enumerated. The resulting witness
is an original feasible integer point with input-bounded coordinate
length. General coupled integer feasibility is not hidden in this oracle.

The enlarged auxiliary box is fixed before drawing \(d\). Its endpoints
come from exact row ranges of the integer box and the support bounds
\(\sigma_i/\alpha\). Constant or dependent rows do not invalidate the
construction. The \(r=0\) case is correctly separated.

The square-completion identity has the correct signs:

\[
 W(a)+d^Ta=
 \min_x\left[F_d(x)+\frac{\alpha}{2}
       \|a-Tx+d/\alpha\|^2\right]
       -\frac{\|d\|^2}{2\alpha}.
\]

It places every joint optimum at \(a=Tx-d/\alpha\), inside the
fixed box. It also transfers an auxiliary lower/upper interval to an
original feasible witness without increasing its gap. The recourse
function \(W\) is fixed independently of the sampled noise, as required
by the direct counting argument.

## The sampling and stopping precisions close without circularity

Interpret the listed coefficients of \(g_j\) as its ordinary polynomial
coefficients. With \(Q\) the product of all base rational denominators,
each unary value at an integer vector has denominator dividing \(Q\).
The term \(\alpha\|Tx\|^2/2\) has denominator dividing \(2Q^3\).
The noise term has denominator dividing \(Q^2(M-1)\). Hence

\[
 D_0=2Q^3,\qquad
 F_d(x)\in\frac{1}{D_0(M-1)}\mathbb Z
\]

for every feasible integer point. This includes constant coefficients
and the factor \(1/2\). A factored or shifted quartic can first be
expanded in polynomial time, since its degree is fixed.

The base-only choice

\[
 M=2^J\ge\max\{2,r\alpha s^2D_0\}
\]

has two simultaneous effects. First, every terminal subdivision count
obeys \(m_{iJ}\le M\), since \(w_i\le s\). Second,

\[
 B_J\le\frac{r\alpha s^2}{8M^2}
       \le\frac{1}{8D_0M}
       <\frac{1}{D_0(M-1)}.
\]

The original feasible incumbent has gap at most \(B_J\). Its value
and the optimum are both on the same original objective lattice, so a
gap below one lattice spacing forces equality. The output is therefore
exact for every sample, including samples with many optimizers.

The auxiliary function and square-completion shift can have denominators
involving \(M^2\) or \((M-1)^2\). This is harmless: they certify a
real inequality for the original gap, and the same additive shift
cancels in that gap. The proof uses no auxiliary-value lattice. Charging
the auxiliary denominator to original exact recovery would create an
unnecessary precision obstruction.

The explanation is not an appeal to arbitrarily fine refinement under a
fixed coarse distribution. This algorithm stops at the predetermined
level \(J\), exactly where the same distribution still controls the
finite-noise atom term. It closes the limitation identified in the
earlier expected-cell review for this pure-integer model.

## Expected work and bit costs

For a deterministic level-grid node, near-optimality forces each
interior noise coefficient into an interval determined by the base
function and neighboring nodes. Other noise coefficients cancel. Thus
the probabilities multiply before summing over the whole grid; there
is no independence assumption about adaptively retained cells.

The nested equal subdivisions, rather than clipped terminal intervals,
give \(h_j/2<h_{ij}\le h_j\) whenever a coordinate is refined. This
justifies the coefficient-interval bound
\((1+2r)\alpha h_{ij}\). Unrefined coordinates have no interior
nodes and introduce no inverse small-width term.

On the endpoint-inclusive \(M\)-point noise grid, interval probability
is at most its length divided by \(2\sigma_i\), plus \(1/M\).
The extra term after summing nodes is \((m_{ij}-1)/M\le1\)
for all \(j\le J\). This proves the stated

\[
 H_{\rm rat}=\prod_i
 \left[3+\frac{(1+2r)\alpha w_i}{2\sigma_i}\right].
\]

Counting cells incident to near-optimal corners, then children and
corners of retained cells, gives the claimed
\(2^r+8^rH_{\rm rat}J\) recourse evaluations. Equality in the
retention test is necessary and is handled correctly, so optimum cells
survive even on flat or tied draws.

The product of input denominators has polynomial bit length. Row ranges,
the enlarged box, \(D_0\), and \(J\) consequently have polynomial
encoding size; \(J\) itself is polynomial in the input length.
All grid addresses, corner coordinates, rational oracle values, and
certificates through level \(J\) have polynomial bit length. Even a
draw retaining exponentially many cells has polynomial bit cost per
processed cell. Multiplying by the expected count gives
\(8^rH_{\rm rat}P(I)\) with an absolute polynomial degree.

The numerical ratios in this expression are necessary qualifications.
Binary encoding does not make \(\alpha w_i/\sigma_i\) polynomial
in value. The theorem explicitly states this distinction. It also
correctly identifies the perturbation as independent in the supplied
factor coordinates, with generally correlated original coefficient noise.

The added normalized family also checks out. For positive integers
\(N\), taking \(X_j=\{0,\ldots,N\}\),
\(g_j(x_j)=(x_j/N)^4\), and \(T=\widetilde T/N\) makes each row
range equal the corresponding range of \(\widetilde T[0,1]^n\).
Thus the displayed expected-count factor is independent of \(N\)
when the remaining data are fixed, while denominator growth costs only
polynomially many bits in \(\log N\). For nonzero \(\widetilde T\),
the continuous polynomial extension has a negative-curvature direction
at sufficiently small interior points, so the example need not be convex.
This verifies the claimed scaling, not a hardness or baseline-separation
claim for that particular family.

## Deterministic baselines that constrain significance

The result is most informative for long binary-encoded integer intervals
where genuine interior resolution matters. Several other regimes already
have simpler deterministic exact algorithms.

For binary coordinates, each unary is affine on its two feasible values.
Project the cube to \((Tx,c^Tx)\) in dimension at most \(r+1\).
The residual objective \(t-\alpha\|z\|^2/2+d^Tz\) is concave,
so a vertex of this zonotope is optimal. For fixed \(r\), its
\(O(n^r)\) vertices can be enumerated with polynomial rational
arithmetic. The easy binary baseline therefore holds at every fixed
rank, not only at rank one.

More generally, if all labels are explicitly listed, let

\[
 P_j=\operatorname{conv}
 \{(T_{\cdot j}t,g_j(t)):t\in X_j\}.
\]

The lifted feasible hull is the Minkowski sum \(\sum_jP_j\).
Each summand is a planar polygon or a segment with at most
\(|X_j|\) vertices. The objective in the lifted coordinates remains
concave. A fixed-dimensional normal-fan arrangement gives deterministic
vertex enumeration polynomial in the total number of labels for fixed
\(r\). Every exposed sum vertex is obtained from feasible original
labels. This enumeration can be exponential in the binary encoding of
long intervals, which is the distinction preserved by the new oracle.

At rank one, coordinate reflections can make all entries of the row of
\(T\) nonnegative. The resulting cross differences are nonpositive,
so a threshold-label expansion gives an ordinary minimum-cut
formulation. Its size depends on the explicit label counts, not their
logarithms. Projection-state dynamic programming is another useful
baseline when cleared integer projected ranges are small; it likewise
has a numerical state-range dependence.

Affine unaries permit endpoint reduction regardless of interval length.
The same is true whenever every coordinate section of the full objective
is concave, for example if
\(g_j''(t)\le\alpha\|T_{\cdot j}\|^2\) throughout every interval.
Those cases reduce to the binary baseline. Merely including quartic
terms does not rule them out.

These comparisons do not prove hardness or exclude a different
deterministic polynomial-bit algorithm for the full stated class.
They identify the appropriate regime for significance and future
comparisons without claiming a new tractability consequence from easy
examples.

## Scope and verification

This is an exact expected-work theorem for a specified pure-integer
nonlinear model. General linking constraints, arbitrary mixed-integer
convex recourse, and continuous quartic coordinates are outside it.
In particular, continuous coordinates remove the original objective
lattice used above. The theorem optimizes the sampled objective and
does not claim exact recovery of the unperturbed one.

Verification used targeted local reads and independent mathematical
checks. No executable solver test, project-wide verification, external
literature search, or CI inspection was performed by this reviewer.
The author's separate test work is not counted as a command run here.
No publication-priority claim follows from this review.

A targeted inline Python document check passed trailing whitespace,
paired math delimiters, and local Markdown link targets.
