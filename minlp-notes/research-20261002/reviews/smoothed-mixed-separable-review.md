# Independent review of separable mixed recourse closure

Date: 2026-10-02. Scope: the complete
[separable mixed closure note](../new-direction/smoothed-mixed-separable-closure.md).
No substantive gap was found in its stated product-domain result. This
review does not establish publication priority.

The integer-state certificate is global. Convexity makes forward
differences nondecreasing, and summing them proves that the two neighbor
inequalities characterize every integer minimizer, including endpoint
states and ties across long flat stretches. Binary search uses the binary
length of the integer range rather than enumeration. A piecewise-quadratic
representation does not change this fact: each needed function value is
computed from the explicit input pieces.

For continuous coordinates, positive-curvature free states and constant
knot states cover every scalar tilt. A flat interval needs no free state
because at its slope a knot is also optimal. The endpoint derivative
conditions include missing neighbors correctly. There are at most
\(2s_i+1\) states when \(s_i\ge1\) positive-length intervals are
listed. Their validity conditions are linear inequalities in the scalar
tilt, hence affine inequalities in the auxiliary parameter and residual
linear coefficient.

Because the recourse objective and domain separate, intersecting these
scalar regions certifies global optimality of the complete response on
the whole intersection. This is stronger than matching integer labels at
cell corners. The counterexample in section 7 correctly shows why that
weaker test would fail for a general coupled convex residual.

The quadratic formula and its gradient follow by direct substitution.
At a positive-curvature free coordinate, the scalar first-order equation
cancels the derivative of its response; fixed coordinates contribute only
the explicit parameter derivative. Thus the branch gradient is
\(\alpha(a-Tx_J(a,r))\), even on a lower-dimensional region.
The reciprocal-curvature bound controls the operator norm of every branch
Hessian. It has polynomial encoding length and affects only the cutoff
through logarithms.

The nonsmooth envelope presents no gap. Every optimal witness is feasible
at every auxiliary parameter, and therefore supplies a global touching
quadratic upper model. Minimizing that model bounds the norm of its active
vector by the value gap. No differentiability, unique witness, or preferred
subgradient is being assumed. This is exactly the property needed for
the unclosed-cell hyperplane argument. A constant or singular branch
Hessian is handled by its proper affine gradient image; a zero defining
row cannot be violated elsewhere in a cell containing the query.

The exact local box solve and original witness reconstruction remain
valid. On a cell contained in the extracted region, the quadratic formula
is the actual mixed value. Its minimizer maps through the affine and
constant scalar responses to a feasible mixed point. At a global auxiliary
minimum, square completion forces that witness to attain the original
sampled optimum.

The fallback count is also sufficient. Enumerate integer assignments,
choose one listed quadratic interval for every continuous coordinate,
and enumerate the faces of the resulting continuous box. A minimal
optimal face has nonsingular positive definite restricted Hessian or is
a vertex, so the usual stationary candidates include an exact optimum.
This costs the stated product of integer counts and \(3s_i\) continuous
choices times polynomial rational arithmetic. Since
\(2s_i+1\le3s_i\) for \(s_i\ge1\), the asserted \(R\le B\)
holds. Fixed or empty coordinates are removed before applying these
counts, as the model specifies.

Aligned noise leaves the scalar functions unchanged; residual ambient
noise merely changes their linear tilts. Thus it preserves separability,
state counts, the base-only Hessians, and affine region offsets. Along an
ambient-coordinate line each global critical region is an interval, and
all simultaneously valid formulas agree. The continuous-QP section-count
argument consequently applies without the pairwise lower-envelope
crossings needed by general mixed recourse. The stated full-row-rank and
norm assumptions are required for the ambient version. The note correctly
does not claim that general spectral normalization preserves its supplied
separable residual.

The result has a meaningful scope distinct from fixed-integer-dimension
convex-MIQP recourse: the number of integer coordinates here is unrestricted,
while the product-domain and separability assumptions make each oracle call
polynomial. The numerical width factors and the ambient bound's
\(n^{O(k)}\) dependence remain explicit.

An inline `python - <<'PY'` exact rational check used a convex univariate
function with two positive-curvature outer pieces and a flat middle piece.
Across seventeen rational tilts it verified 119 integer state equivalences,
seventeen continuous piece minima, and 22 active upper-model inequalities,
including multiple optimal knot witnesses. It also checked the displayed
state/fallback count. This diagnostic tests the new scalar ingredients;
it is not an implementation of the whole smoothed algorithm.

No project-wide checks, CI inspection, or external search were performed.
