# Independent review of exact SOCP witness recovery

Date: 2026-09-27; coefficient-sensitive review: 2026-09-28.
Status: the complete saved
[recovery proof](socp-exact-witness-recovery.md) passes this independent
review, conditional on its stated theorem inputs and coefficient-sensitive
refinement. No substantive
mathematical gap was found. This review does not establish novelty or
reprove those input theorems.

## Scope and algebraic selection

The reviewer read the entire recovery draft and checked its use of the
[SOCP decision theorem](socp-hessian-span-frontier.md), the bounded-value
and optimal-point statements in the
[nonconvex certificate theorem](nonconvex-hessian-span-frontier.md), and
the [common-field construction](constructive-common-field-recovery.md).
The local [recognition audit](algebraic-recognition-source-review.md)
was consulted for the recognition input model and minimal-polynomial
height bound; this review did not repeat its primary-source inspection.

The boxed feasible set is compact and convex. Its minimum squared-norm
point exists and is unique, including for lower-dimensional sets. The
nonconvex optimizer theorem supplies some algebraic optimizer with bounded
joint degree and coordinate heights. Uniqueness identifies that optimizer
with the one point approximated throughout the recovery algorithm. This is
the essential connection between the existence theorem and the algorithm.

The joint-degree bound comes from the optimizer theorem. Multiplying
individual coordinate degrees would not establish the claimed bound.
Squaring the rational cone maps increases input length by a fixed
polynomial factor and requires their affine sign conditions. Neither the
sign conditions nor box rows increase the constraint Hessian span. The
objective Hessian is excluded by the optimizer theorem as stated.

## Exact rational queries and approximation

For a fixed rational threshold \(r\ge0\),

\[
 \|(2x,r-1)\|_2\le r+1
 \quad\Longleftrightarrow\quad \|x\|_2^2\le r.
\]

The right side of the cone inequality is positive. The squared residual is
\(4\|x\|_2^2-4r\), with Hessian \(8I\). Therefore every query
has squared-Hessian span at most \(h+1\), and all query data are rational.

With \(n\ge1\) and \(R\ge1\), the initial upper norm threshold
\(nR^2\) is positive and feasible. The initial lower threshold zero
need only be a lower bound; it need not be infeasible. Thus zero optimal
norm causes no exception. Bisection preserves an enclosing interval and a
feasible upper endpoint. At termination every point under the retained
norm cap has objective gap at most \(\tau^2/16\).

For the minimum-norm point \(x^*\), convexity gives

\[
 \langle x^*,y-x^*\rangle\ge0,
 \qquad
 \|y-x^*\|_2^2\le\|y\|_2^2-\|x^*\|_2^2.
\]

Every feasible point under that cap is consequently within Euclidean
distance \(\tau/4\) of the same \(x^*\). Coordinate bisection
retains the cap and the entire current box. If its closed lower half is
infeasible, its closed upper half remains feasible because their union is
the current box. This argument permits boundary-only feasibility.
Zero-width coordinate intervals already meet the stopping condition.

For the final midpoint \(c\), some feasible point in the final box gives
\(|c_j-x_j^*|\le3\tau/4<\tau\). This is the coordinatewise
approximation the common-field theorem needs. The draft correctly makes
no claim that \(c\) itself is feasible or that its Euclidean error is
less than \(\tau\).

The number of norm bisections is \(O(\log(nR^2)+p)\), and the
coordinate bisections require \(O(n(\log(2R)+p))\) steps when
\(\tau=2^{-p}\). Their endpoints are dyadic interpolations of rational
endpoints. Hence query counts, endpoint bit lengths, and total query input
lengths are polynomial in \(N+p\). Calling the boxed decision theorem
at span at most \(h+1\) gives \((N+p)^{O(h+2)}\) time.

## Common-field recovery and verification

The approximation oracle returns rational coordinates of polynomial
encoding length and approximates one fixed tuple at every requested
precision. It therefore satisfies the common-field theorem's full input
model, including the selected real embedding. Its joint-degree and
coordinate-height bounds are both \(N^{O(h+1)}\).

Using only total input length, that theorem's polynomially many recognition
calls request precision polynomial in these bounds. Substitution into the decision-oracle cost
gives supplied-box time \(N^{O((h+1)^2)}\). Its algebraic arithmetic
and output encoding have polynomial overhead, leaving output degree and
length \(N^{O(h+1)}\). These remain valid fallback bounds. The sharper
accounting reviewed below separates coefficient bits from structural size.
The proof does not confuse output size with the cost of acquiring sufficient
precision.

Exact checking must include original affine inequalities and equalities,
all supplied or derived box inequalities, and both \(q_i\le0\) and
\(c_i^Tx+d_i\ge0\) for each cone. The draft explicitly checks the
cone signs, box inequalities, and affine equalities. The explicit wording
for boxes and equalities was added after review and the saved change was
checked. These rows were already part of the feasible system.
The common-field note provides polynomial-time sign
determination without trusting an asserted irreducibility label.
The draft correctly distinguishes verifying feasibility from verifying
minimum-norm optimality.

## Removing the box and integer fibers

The small-point radius \(R_0\) supplies a feasible point \(y\) with
\(\|y\|_\infty\le R_0\) whenever the original set is nonempty.
Its intersection with the Euclidean ball of radius \(\|y\|_2\)
is compact, proving global minimum-norm attainment. Convexity again gives
uniqueness, and

\[
 \|x^*\|_\infty\le\|x^*\|_2
 \le\sqrt nR_0\le nR_0.
\]

Thus the enlarged box contains the global minimum-norm point, as required
by the statement. Merely containing some feasible point would not prove
that claim. The zero-dimensional case is separately handled by rational
comparisons.

The coarse enlarged input length is \(M=N^{O(h+1)}\). Substituting \(M\)
into the supplied-box bounds correctly gives output degree and length
\(N^{O((h+1)^2)}\), and runtime \(N^{O((h+1)^3)}\).
These fallback derivations remain valid independently of the refinement
below.
The integer-fiber consequence is limited to recovering a continuous point
after an integer assignment has been found. Bounded integer coordinates
justify the uniform polynomial substitution overhead. No algorithm for
unrestricted integer dimension is introduced.

The example with \(\|(1,1)\|_2\le x\) and
\(\|(x,x)\|_2\le2\) has the unique feasible point \(\sqrt2\).
Its two scalar Hessians span dimension one, so it correctly demonstrates
the need for algebraic output even at \(h=1\).

## Coefficient-sensitive refinement

The reviewer read the new Section 6 and checked its use of
[the coefficient-sensitive algebraic bounds](nonconvex-finite-infimum.md#8-separate-structural-size-from-coefficient-bit-length)
and their [independent review](nonconvex-finite-infimum-review.md#6-the-coefficient-sensitive-refinement-is-valid).
Let \(S\ge2\) bound structural size and \(\tau_0\ge1\) bound
input rational numerator and denominator bit lengths. Structural size
counts coefficient positions, rows, variables, cone coordinates, and index
lengths. Expanding the quadratic rows changes it only by a fixed polynomial
factor. The relevant bounds are

\[
 D\le S^{O(h+1)},\qquad H\le(\tau_0+1)S^{O(h+1)}.
\]

The cited coefficient refinement explicitly covers feasible-point
coordinates. The recovery note also explains its application to bounded
optimal-point coordinates: changing the perturbation objective preserves
the same bounded-size affine determinants and finite-quotient norm bounds.
The squared-norm objective adds only fixed-bit coefficients and polynomial
structural overhead. Thus the same joint-degree and coordinate-height
accounting applies to the unique point being recovered.

For every accuracy request, the algorithm starts again from the original
supplied box. This matters because a previous approximation's final box
can exclude \(x^*\). Within each request, it stores only the current two
coordinate endpoints and one current norm threshold. Replacing endpoints
preserves accumulated restrictions without retaining redundant history rows.
Consequently the native SOCP query has

\[
 S_q\le S^{O(1)},\qquad
 \tau_q\le(\tau_0+p+1)S^{O(1)},\qquad h_q\le h+1,
\]

with \(S_q\) independent of requested accuracy \(p\). Rational
endpoint arithmetic and the number of queries have absolute polynomial
exponents in \(S,\tau_0,p\).

The query's infeasibility gap is obtained from its quadratic epigraph
system before the LP lift is built. The coefficient-sensitive value bound
gives tolerance bit length
\((\tau_q+1)S_q^{O(h+1)}\). The explicit rational cone construction
and exact LP solution have absolute polynomial exponents in their input
and output encoding lengths. Hence one query costs
\((\tau_q+1)^{O(1)}S_q^{O(h+1)}\), and the full approximation costs

\[
 T_{\mathrm{approx}}(p)
       \le(\tau_0+p+1)^{O(1)}S^{O(h+1)}.
\]

The LP does gain variables and rows as accuracy increases. Those variables
are used only by the LP algorithm; they do not become structural input to
another algebraic certificate theorem. Confusing the native SOCP structure
with this internal lift would invalidate the argument for the sharper bound.

The common-field construction uses absolute polynomial call counts,
precision, and arithmetic overhead in \(n,D,H\). In particular its
primitive search has \(O(nD^2)\) candidates, followed by at most
\(n(D+1)\) interpolation sample recognitions. Candidate linear forms
are computed rationally from approximations of the original tuple; they
are not new SOCP constraints. Thus its maximum requested precision and
overhead are bounded by
\((\tau_0+1)^{O(1)}S^{O(h+1)}\). Substituting into
\(T_{\mathrm{approx}}\) and multiplying by the call count preserve
that form, since all powers applied to coefficient lengths are absolute
constants. This proves the stronger supplied-box runtime and output bound.

Without an input box, use the coefficient-sensitive radius

\[
 \widehat R_0
       =2^{\lceil(\tau_0+1)S^{C(h+1)}\rceil}
\]

for a sufficiently large effective absolute \(C\), and box coordinates
by \(n\widehat R_0\). This replaces the numerical coarse radius used
in the fallback proof; the coarse radius need not itself have the sharper
bit-length bound. The same geometric argument proves that this new box
contains the global minimum-norm point. It adds only \(2n\) affine
rows, and its coefficient bound is
\(\tau_B\le(\tau_0+1)S^{O(h+1)}\). Substituting \(\tau_B\)
into the boxed bounds again preserves
\((\tau_0+1)^{O(1)}S^{O(h+1)}\). The joint-field degree remains
\(S^{O(h+1)}\), since structural size does not grow with radius bits.

Finally \(S\le N^{O(1)}\) and \(\tau_0\le N\). Thus both
running time and output length are \(N^{O(h+1)}\), with or without
a supplied box. This conclusion follows from the algorithmic cost
accounting above, not from the certificate-size refinement alone. No
substantive gap was found in this stronger bound. The reviewer requested
explicit replacement of the coarse radius and checked the saved revision,
along with the per-call restart and external linear-form calculations.

## Verification record

An additional independent narrow review checked the norm-cone identity,
the feasible bisection invariant, the fixed-point error, rational endpoint
sizes, and the query exponent. It found no further gap and independently
confirmed that the final error guarantee is coordinatewise.
The same reviewer separately checked the stronger composition, including
replacement of query endpoints, restart of each approximation call, and
the separation between native SOCP structure and internal LP size.

No implementation of the recovery algorithm was run. Targeted inline
`python -` document checks of this review passed for local links, math
delimiters, trailing whitespace, control characters, and final newline.
The checks were repeated after the coefficient-sensitive revision.
No project-wide
verification or CI inspection was performed.
