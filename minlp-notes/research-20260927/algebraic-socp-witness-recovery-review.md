# Review of exact SOCP witnesses over one real number field

Date: 2026-09-28. Scope: the proposed algorithm in
[algebraic-socp-witness-recovery.md](algebraic-socp-witness-recovery.md),
using the exact feasibility theorem in
[algebraic-threshold-misocp.md](algebraic-threshold-misocp.md).
Status: the complete manuscript, its recovery reduction, and its field
accounting have been checked. No unresolved mathematical gap was found. The reviewer independently suggested the unknown-box
canonical-point proof, also proposed by the separate field reviewer.
That arithmetic argument is therefore checked by independent
reconstructions, not by a reviewer with no involvement in its formulation.

## 1. The field-degree issue

The input contains one dense irreducible polynomial, an isolator selecting
its real root \(\alpha\), and explicit coefficient vectors over
\(K=\mathbb Q(\alpha)\). Its degree \(D\) counts toward input
length. The algorithm must retain this input model: separately encoded
algebraic coefficients can have a compositum of exponential degree.

A common algebraic certificate is required for the canonical point. Bounds
on the degree of each coordinate over \(K\) would not suffice. The
nonconvex elimination proof instead uses one common convergent minimizing
sequence and one fixed chart and active support. Any rational linear form
in the coordinate limit can be substituted as its output, with the same
relative-degree bound \(L\). The coordinate limits are first shown to
be algebraic. A rational linear combination can generate their joint
extension over \(K\): differences between two distinct \(K\)-embeddings
exclude only finitely many choices from a separating family of rational
linear forms. Applying the output degree bound to such a form gives

\[
 [K(x^*):K]\le L,
 \qquad [K(x^*):\mathbb Q]\le DL.
\]

No factor \(D\) is multiplied once per coordinate, no normal closure
is needed, and no product of individual coordinate degrees is taken.

For the canonical point, a direct existence proof can keep the unknown
box out of all height estimates. In lifted coordinates choose a box
strictly containing the lift of the global minimum-norm point. Minimize
the original squared norm plus a generic vanishing perturbation, subject
to outward quadratic bands and the box. Comparison with that one point
and compactness make every limit feasible with no larger norm. Convexity
makes the original point unique; the lifted quadratic coordinates are
then fixed as well. Every artificial box row is consequently inactive
for all sufficiently small perturbations. Its endpoints do not enter the
eventual KKT chart. This supplies a direct original-input encoding bound,
rather than feeding a previously computed large box back into that bound.

The finite-quotient argument over \(K\) controls joint coefficient norms
at every place. Coefficient extraction preserves them. A nonzero
annihilator over \(K\) of degree \(L\) and coefficient height \(W\)
gives rational degree at most \(DL\) and integer minimal-polynomial
coefficient bits bounded by \(DL(W+O(1))\). The other embeddings need
not preserve optimization; they enter only these coefficient estimates.
The argument uses the purely algebraic lemma from
[the field-precision note](algebraic-coefficient-span-precision.md),
not its convex-quadratic theorem applied to indefinite squared SOC rows.

## 2. The approximation oracle does not enlarge the input field

The original feasible set is closed and convex. When nonempty, its
Euclidean norm has a unique global minimizer. A direct coordinate
annihilator bound for this point supplies a computable rational box by
Cauchy's root bound.

Alternatively, a box meeting the feasible set can be enlarged by a factor
of \(n\) to contain this minimizer. That enlargement cannot simply be
omitted: the affine set \(2x+y=3\) meets \([-1,1]^2\) at \((1,1)\),
but its minimum-norm point is \((6/5,3/5)\). The direct canonical-point
radius avoids this issue.

For rational \(r\ge0\), the norm sublevel has the exact rational
cone representation

\[
 \|(2x,r-1)\|_2\le r+1.
\]

Its squared residual is \(4\|x\|^2-4r\), with Hessian \(8I\).
It adds at most one direction to the Hessian span over \(K\). Affine
coordinate bounds add none. All oracle calls therefore use the original
field \(K\), rational new coefficients, and span at most \(h+1\).
The growing input field degree is never replaced by the degree of an
intermediate optimizer or value.

Norm bisection keeps a feasible rational upper threshold
\(u\le\nu+\eta^2/16\), where \(\nu=\|x^*\|^2\). The
projection inequality gives

\[
 \|y-x^*\|^2\le\|y\|^2-\nu\le\eta^2/16
\]

for every feasible point in that slice. Coordinate bisection preserves
some feasible point in the slice, including at boundaries of closed
halves. Once every interval has width at most \(\eta\), its midpoint
has coordinate error at most \(3\eta/4\). The midpoint need not
itself be feasible.

Only current endpoints are stored, and the coordinate search restarts
from the original box for every requested accuracy. An earlier retained
box can exclude \(x^*\), even though it contains nearby feasible points;
reusing it would invalidate an arbitrary-precision oracle.

For fixed \(h\), the query count, query length, and exact-feasibility
cost are polynomial in original input length, the radius bits, and the
requested precision. Internal rationalization need not preserve the
squared-Hessian span. Its gap was proved for the exact original system,
and no span theorem is applied again to the rounded system. A fixed-depth
composition of these polynomial bounds remains polynomial for fixed
\(h\). It does not by itself establish a sharp exponent linear in
\(h\), or true fixed-parameter tractability.

## 3. Absolute field recognition and verification

Append \(\alpha\) to the approximation tuple. Its approximation is
obtained from the input isolator by rational root refinement. Its height
and degree are already part of the input bounds. Apply the established
[common-field recognition procedure](constructive-common-field-recovery.md)
to \((\alpha,x^*)\), using joint absolute degree bound \(DL\), the
individual integer minimal-polynomial height bounds, and the certified
approximation oracle. All its internal linear forms are evaluated outside
the SOCP oracle. They are never appended as new algebraic conic data.

The result describes one real root \(\beta\) and polynomial expressions
for both \(\alpha\) and every coordinate. The selected embedding is
essential. For independent verification, check the input polynomial and
isolating interval on the represented \(\alpha\), map every original
coefficient through that expression, and then check every affine row,
squared cone inequality, and cone right-hand-side sign at the selected
\(\beta\). Checking the input polynomial alone would permit another
real embedding with different inequality signs. Checking squared rows
without the cone signs would not verify SOCP feasibility.

Exact substitution and univariate sign determination have polynomial
cost in the input and output lengths. This independently verifies
feasibility and embedding consistency. It does not independently certify
the minimum-norm property; that property follows from the construction.

For a mixed-integer system, the established decision theorem first returns
an integer assignment of polynomial encoding length for fixed \(k,h\).
Substitution preserves the original field and does not increase its
continuous Hessian span. Applying this continuous recovery to the fixed
fiber gives a full exact feasible point. The point is canonical within
that fiber, not necessarily among all mixed-integer feasible points.

The fractional optimal-level consequence in the final manuscript is valid.
For a known attained ratio \(\theta\), the equation
\(f-\theta d=0\) is affine over \(\mathbb Q(\theta)\). The
cone \(\|(2,d-s)\|\le d+s\) has squared residual
\(4-4ds\). Together with its sign it requires \(ds\ge1\)
and \(d+s\ge0\), hence both \(d,s>0\). Conversely, any
\(d>0\) admits \(s=1/d\). This adds one continuous Hessian
direction and produces a closed augmented conic system. The algorithm
can recover a point and discard \(s\). This does not supply an
unknown optimal value or establish its attainment.

## 4. A field extension and embedding boundary

Let \(K=\mathbb Q(\alpha)\), with \(\alpha=\sqrt2>0\). The
two cones

\[
 \|(\alpha,1)\|\le x,
 \|(x,\alpha x)\|\le3
\]

force \(x=\sqrt3\). Add the affine equation \(y=\alpha\).
The squared Hessians are scalar multiples of the same matrix, so
\(h=1\), but the output field is
\(E=\mathbb Q(\sqrt2,\sqrt3)\). Its relative degree over \(K\)
is two and its absolute degree is four. A convenient primitive element is

\[
 \beta=\sqrt2+\sqrt3,\qquad
 \beta^4-10\beta^2+1=0,
\]
\[
 \alpha=(\beta^3-9\beta)/2,
 \qquad x=(11\beta-\beta^3)/2.
\]

This example shows why recovery cannot assume the output coordinates lie
in the input field. If one recognized only \(x\), its quadratic field
would not contain the original \(\alpha\). Appending \(\alpha\)
ensures that the output can represent the original coefficients and
their selected embedding.

A targeted inline `python -` command with exact SymPy arithmetic checked
the primitive polynomial, both coordinate maps modulo that polynomial,
both cone identities, and the squared Hessians \(-2\) and \(6\).
It also checked that \(-\sqrt2\) satisfies the same input polynomial
but is excluded by the positive-root isolator. All checks passed. These
finite calculations test the field and embedding mechanism, not the
universal degree, height, or running-time bounds.

A second targeted inline `python -` check passed for this review's final
newline, trailing whitespace, control characters, paired math delimiters,
and four local links. It also verified the reciprocal-cone residual
identity by exact symbolic expansion. These are document and finite
identity checks, not a formal verification of the theorem.

## 5. Review limits

A separate nested reviewer was assigned the recovery algorithm, field
iteration, embedding verification, and precision accounting. It found no
substantive gap, conditional on the stated joint-degree and height inputs.
Its embedding and recognition argument received an additional independent
nested check. The present reviewer then read the complete saved manuscript,
including the direct canonical-point radius and the algebraic optimal-level
application; no mathematical correction was required. This review
does not supply a new prior-art search or establish publication priority.
The exact recovery is a consequence of the specific fixed-span decision
and encoding results; it is not an algorithm for arbitrary SOCP input.
No project-wide verification, CI inspection, or Lean formalization was
performed.
