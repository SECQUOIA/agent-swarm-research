# Adversarial review of recovery on a bounded mixed polytope

Date: 2026-10-02. Scope: the proposed exact recovery lemma for arbitrary
optimal sets of rational quadratic programs on bounded mixed polytopes,
and its use after a supplied-growth approximation. This is an independent
mathematical review, supported by a second reviewer and targeted exact
examples. No literature-priority claim is made.

## Finding

The recovery argument is sound. In particular, the final stationarity
linear program cannot introduce a nonoptimal objective value once its
selected face is proved to contain an optimum. Its multipliers must be
unrestricted. Feasibility and exact objective comparison at the end do
not independently certify the supplied global growth assumption.

The review checked the complete written
[mixed-polytope recovery theorem](../new-direction/proximal-polytope-recovery.md),
including its explicit constants and its integration with the auxiliary
proximal grid. No substantive gap was found. A second reviewer
independently confirmed the recovery algebra and arithmetic thresholds.

## Why redundant constraints do not invalidate the height argument

Use the Hessian convention
\(F(x)=\tfrac12x^TAx+b^Tx+c\). Clear a common denominator \(D\)
from the objective and constraints, and write \(\bar A,\bar M\)
for the resulting integer matrices. Let

\[
 C=\max(1,\|\bar A\|_{\max},\|\bar M\|_{\max}),\quad
 Z_0=(nC)^n,\quad B_0=nCZ_0,\quad H=(nB_0)^n.
\]

At a nearest optimizer \(s\), use an independent row basis \(E\)
of its active inequality rows together with the fixed-integer unit rows.
An integer basis \(Z\) for \(\ker E\) can be constructed by
choosing pivot columns and using an adjugate. Each entry is a determinant
of a matrix whose entries have magnitude at most \(C\), so the
bound \(Z_0\) is valid. Rank zero gives the usual unit basis; full
rank gives no kernel columns.

The stationary polytope uses
\(Z^T(\bar A x+\bar b)=0\), rather than unrestricted multiplier
variables. Its coefficient magnitudes are at most \(B_0\), and
its right-hand sides are integers, including the fixed integer tuple.
It is nonempty and bounded, possibly lower-dimensional. Every vertex has
a common coordinate denominator at most \(H\). Arbitrary integer
right-hand-side magnitudes affect numerator size, but not this determinant
bound on denominators. Original bounded-polytope height bounds control
the integer tuple's encoding length.

This elimination matters. Keeping redundant rows and then asserting that
the lifted multiplier polyhedron has a vertex would be invalid: redundant
rows can leave multiplier lineality. The proof avoids that step. The
final recovery LP may safely retain redundant rows because it uses only
linear feasibility and no vertex assertion in multiplier space.

## Simultaneous snapping is justified

Let \(m\) be the number of inequalities, \(q=\max(1,m)\),
\(\tau=1/(4qH)\), and \(\delta=\tau/(2nC)\). A feasible
point \(y\) within \(\delta\) of the optimal set agrees with a
nearest optimizer \(s\) in every integer coordinate, since
\(\delta<1\). Select each inequality whose nonnegative scaled
slack at \(y\) is at most \(\tau\).

The row norm bound \(\|\bar M_i\|_2\le nC\) ensures every
inequality active at \(s\) is selected. A selected inequality has
slack at \(s\) at most \(3\tau/2\). Sum the slacks of all
extra selected inequalities over the stationary polytope associated with
\(s\)'s original face. That sum is nonnegative, has integer
coefficients, and is at most \(3/(8H)<1/H\) at \(s\).
Its minimum occurs at a vertex. A positive vertex value would be at
least \(1/H\), so the minimum is zero. This proves simultaneous
feasibility of all extra snaps, not merely their separate feasibility.

All points of the original stationary polytope are global optimizers:
they share the face equalities and their gradients annihilate its tangent
space. The quadratic difference identity therefore makes their values
equal to \(F(s)\). The zero-slack vertex is consequently an optimum
on the selected face.

## Every feasible final-LP solution has the correct objective

Let \(K\) collect selected inequality rows and fixed-integer unit
rows. The final LP requires the original inequalities, the selected
equalities, the fixed integer values, and

\[
 \bar A x+\bar b\in\operatorname{rowspan}(K).
\]

This row-space membership is a linear equality system with unrestricted
multipliers. The constructed optimum \(s'\) satisfies it because
the original active row space is contained in the selected row space.
For any other feasible solution \(x\), put \(v=x-s'\). Then
\(Kv=0\), and both gradients lie in the row space of \(K\).
Hence

\[
 v^T\nabla F(s')=0,\qquad
 v^TAv=v^T(\nabla F(x)-\nabla F(s'))=0.
\]

The exact quadratic expansion gives \(F(x)=F(s')=F^*\). No
positive-definiteness, multiplier-sign, or isolated-optimum assumption is
needed for this final identity. The recovery LP itself contains no free
integer decision: all integer coordinates were fixed from \(y\).

A stationary-polytope vertex also gives the optimum-value denominator
bound \(V=2DH^2\). The factor two matches the Hessian convention.
An approximation with objective gap at most \(g_0\delta^2\)
therefore supplies the required distance under the valid supplied growth
bound \(g_0\). Additional accuracy below \(1/(4V^2)\) safely
isolates the rational optimum value.

## The auxiliary proximal-grid integration is valid

The reviewed spectral decomposition has
\(A=P-\alpha T^TT\), \(P\succeq0\), and
\(\|T\|_2\le1\). Exact convex mixed-integer recourse evaluates

\[
 W(a)=\min_{x\in X}\left[F(x)+\frac\alpha2\|a-Tx\|^2\right]
\]

at rational auxiliary nodes, with an attaining original mixed-feasible
witness. The identity and upper coordinate curvature remain valid when
the feasible domain is mixed. The auxiliary optimal set is \(TS\),
and set-distance growth transfers by

\[
 \operatorname{dist}(a,TS)
 \le\|a-Tx\|+\operatorname{dist}(x,S),\qquad
 g_W=\frac{g_0\alpha}{2g_0+\alpha}.
\]

Thus the existing proximal theorem applies to the continuous auxiliary
box, using \(W\) as one factor in a single bag of size at most the
negative inertia. It does not need a finite set of auxiliary optimizers.
Most importantly, its returned original witness obeys
\(F(y)-F^*\le W(a)-F^*\le\varepsilon\). Original full-space
growth then gives the distance needed by the recovery lemma. A projected
growth bound alone would not supply that conclusion; the written theorem
correctly requires full set-distance growth.

The bit argument also survives the nonquadratic value function. Auxiliary
centers are previous auxiliary grid points, so their rational coordinate
heights have the established dyadic control. Each rational node produces
a convex-MIQP instance of that bounded encoding length. Its exact oracle
returns rational values and witnesses with the claimed FPT cost. The
single-bag search compares these values and explicit corrections; it does
not accumulate unrelated oracle denominators into a long sum or treat
\(W\) as a quadratic polynomial. The original bounded polytope also
bounds the size of the integer tuple used in the final LP.

The guarantee remains conditional on the supplied valid \(g_0\).
The proximal search restricts its auxiliary domain using this promise.
Exact inner optimization and the final face LP do not independently prove
that an excluded region contains no better point. The written theorem
states this limitation correctly and does not offer an unknown-growth
stopping rule.

## Targeted examples

The command
`python research-20261002/new-direction/check_polytope_recovery_review.py`
passed eight exact SymPy cases. It checked thirteen vertices of the
original stationary polytopes, ten vertices of the selected recovery
polytopes, and four extra facet snaps. It also checked objective equality
at the average of all recovery vertices in each case.

The cases covered redundant nonzero rows and identically tight zero rows,
a flat diagonal segment, an extra coupled-facet snap, a lower-dimensional
affine feasible set, disconnected optimal edges, fixed integer assignments
with extra snaps, coupled mixed constraints with rational data, and a
Hessian indefinite in the ambient space but convex along the feasible
affine hull. The checks verified the stated distance threshold, vertex
denominator bound, positive slack gap, joint zero-slack feasibility, and
the recovered objective.

The first temporary-checker run exposed a zero-row matrix construction
with the wrong number of columns; correcting its empty-basis shape made
the final run pass. This was a checker implementation error. The
diagnostic enumerates vertices only for these small cases; the proposed
algorithm uses polynomial-time rational linear feasibility.

The scoped command
`git diff --check -- research-20261002/reviews/polytope-recovery-review.md research-20261002/new-direction/check_polytope_recovery_review.py`
passed. An inline `python - <<'PY'` check of whitespace, paired
mathematical delimiters, and local links also passed.

No project-wide checks, CI inspection, or external search were performed.
