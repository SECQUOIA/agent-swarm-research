# KKT charts and exact representation for stable nonlinear dynamics

Date: 2026-10-02. This review concerns the model in
[the nonlinear dynamics note](../new-direction/nonlinear-dynamics.md)
and its [rational approximation extension](../new-direction/nonlinear-dynamics-bit.md).
It does not make a novelty claim or use a literature search.

Global box invariance makes the propagated state bounds redundant. Keeping
an active redundant state bound prevents the linear independence constraint
qualification, or LICQ, regardless of objective noise. Removing those bounds
gives a uniformly conditioned constraint chart. This resolves the constraint
geometry, but a positive definite tangent Hessian does not give a polynomial
bound on the degree or expanded encoding of an exact optimizer. A sparse
implicit KKT representation remains possible; an exact closure theorem must
specify what operations it supports.

## The free variables give a uniform constraint chart

Write the dynamics as

\[
q_t=s_{t+1}-\phi_t(s_t,u_t)=0,\qquad t=0,\ldots,T-1.
\]

Assume nondegenerate compact state and control intervals, global box
invariance, and the derivative bounds
\(|\partial_s\phi_t|\le a<1\), \(|\partial_u\phi_t|\le b\).
The primitive variables are \(z=(s_0,u_0,\ldots,u_{T-1})\); the dependent
variables are \(y=(s_1,\ldots,s_T)\). Forward simulation defines the graph
\((z,\Phi(z))\) over the entire primitive box.

At a feasible point write the equality Jacobian as \([E\ R]\), with the
columns ordered as \((z,y)\). The matrix \(R\) is lower bidiagonal with
unit diagonal and subdiagonal entries \(-\partial_s\phi_t\). Thus

\[
\|R^{-1}\|_2\le\frac1{1-a},\qquad
\|E\|_2\le\sqrt{a^2+b^2}.
\tag{1}
\]

For the second bound, different rows of \(E\) have disjoint supports:
each uses its own control, and only row zero also uses \(s_0\).
Consequently the graph chart satisfies

\[
\|D(z,\Phi(z))\|_2
\le C_{\rm graph}:=
\sqrt{1+\frac{a^2+b^2}{(1-a)^2}}.
\tag{2}
\]

Delete the propagated state inequalities, retaining only the primitive
box. This leaves exactly the same feasible set. Let \(C\) be the matrix
of any active primitive coordinate bounds, using signed unit rows. Its
rows are distinct because the intervals are nondegenerate, so
\(CC^T=I\). The active constraint Jacobian is

\[
J=\begin{bmatrix}E&R\\C&0\end{bmatrix}.
\]

For any right-hand side \((r,\eta)\), choose

\[
\delta z=C^T\eta,\qquad
\delta y=R^{-1}(r-EC^T\eta).
\]

This is a right inverse with norm at most

\[
K=\sqrt{1+\frac{1+a^2+b^2}{(1-a)^2}}.
\tag{3}
\]

Indeed,
\(\|\delta z\|^2+\|\delta y\|^2
\le\|\eta\|^2+(\|r\|+\sqrt{a^2+b^2}\|\eta\|)^2/(1-a)^2\).
Hence \(J\) has full row rank and its smallest singular value is at least
\(1/K\), uniformly in the horizon. LICQ in this formulation requires no
objective genericity or noise assumption.

Forward repair also has a uniform bound. If an ambient point \(x\) lies in
the prescribed boxes and \(\widehat x\) is its forward repair with the same
primitive coordinates, then

\[
\|\widehat x-x\|_2\le\frac{\|q(x)\|_2}{1-a},\qquad
\|\widehat x-x\|_\infty\le\frac{\|q(x)\|_\infty}{1-a}.
\tag{4}
\]

These follow from the scalar recurrence
\(|\widehat s_{t+1}-s_{t+1}|\le
a|\widehat s_t-s_t|+|q_t(x)|\).
This map is a retraction onto the feasible graph, not an assertion about
Euclidean nearest-point projection.

## Active redundant state bounds always defeat LICQ

In the original formulation, LICQ holds at a feasible point if and only
if every propagated state \(s_t\), \(t\ge1\), is strictly inside its
prescribed interval.

For necessity, eliminate the equalities. A propagated state inequality
becomes a smooth function \(h(z)\le0\) valid throughout the primitive box.
If \(h(z)=0\), then \(z\) maximizes \(h\) over that box. Its derivative
vanishes in every interior coordinate. At a lower endpoint its derivative
is nonpositive, and at an upper endpoint it is nonnegative. Thus
\(\nabla h(z)\) is a nonnegative combination of the active primitive-box
outward normals. If no primitive bound is active, this says
\(\nabla h(z)=0\). Lifting the relation to the original variables gives
a linear dependence among that state-bound row, the primitive-bound rows,
and the equality rows. Sufficiency follows from (3).

A concrete example shows that bounded objective noise cannot fix this.
Take all state and control intervals to be \([0,1]\), and set

\[
\phi_t(s,u)=\frac{s+s^2+u+u^2}{4}.
\]

This map is invariant and satisfies
\(0<\partial_s\phi_t\le3/4\). For \(\sigma>0\), minimize

\[
F_\gamma(x)=\sum_j(2\sigma+\gamma_j)x_j,
\qquad \gamma_j\in[-\sigma,\sigma].
\]

The unique global optimum is the zero trajectory for every noise draw.
There are \(2T+1\) active lower bounds and \(T\) equality rows in an
ambient space of dimension \(2T+1\). The active Jacobian has row
deficiency exactly \(T\). Its full active-set KKT matrix is singular
for every objective Hessian.

This example permits strictly positive bound multipliers: take equality
multipliers zero and bound multipliers \(2\sigma+\gamma_j\).
It also satisfies MFCQ: choose positive primitive directions and propagate
\(\delta s_{t+1}=(\delta s_t+\delta u_t)/4\).
The obstruction here is specifically the redundant-row failure of LICQ.

## Finite noise retains strict complementarity exceptions

Fix any prescribed rational noise grid with \(M\) atoms and one vector
of atoms \(\zeta\). At horizon one, use the same dynamics and the base
objective

\[
F(x)=s_0^2+u_0^2-\zeta^Tx.
\]

On the draw \(\gamma=\zeta\), the optimum is zero. If
\(\lambda_{s_0},\lambda_u,\lambda_{s_1}\ge0\) are lower-bound
multipliers, reduced stationarity gives

\[
0=\lambda_{s_0}+\lambda_{s_1}/4,
\qquad
0=\lambda_u+\lambda_{s_1}/4.
\]

All three multipliers vanish. After deleting the redundant propagated
state bound, the two remaining multipliers still vanish. The exceptional
draw has probability \(M^{-3}\) under iid uniform noise on that grid.
If the grid contains zero, the same example works with the fixed base
objective \(s_0^2+u_0^2\) and \(\zeta=0\).

This rules out an unconditional claim that finite-grid noise guarantees
strict complementarity on every draw. It does not rule out controlling
the probability of exceptions through a base-dependent grid choice and
an always-correct fallback.

## Uniform positive curvature allows exponential algebraic degree

For \(T\ge2\), let \(d=2^T\) and consider

\[
s_{t+1}=s_t^2/3,\qquad s_t\in[0,1],\qquad u_t\in[-1,1],
\]

with objective

\[
F=\frac{s_0^2}{2}-\frac{s_0}{3}+s_T
  +\frac12\sum_{t=0}^{T-1}u_t^2.
\tag{5}
\]

The controls are unused by this allowed dynamics example. The dynamics
have contraction constant \(2/3\), degree two, curvature \(2/3\), and
input length \(O(T)\). Forward simulation gives

\[
s_T=\frac{s_0^d}{3^{d-1}}.
\]

The reduced objective has Hessian at least the identity everywhere on the
primitive box. Its unique minimizer has every control equal to zero and
\(s_0\in(0,1/3)\), determined by

\[
P_T(s_0):=d s_0^{d-1}+3^{d-1}s_0-3^{d-2}=0.
\tag{6}
\]

All state and control bounds are inactive there. The reduced Hessian is
also bounded above by \(5I/3\): its only nonconstant entry is
\(1+d(d-1)s_0^{d-2}/3^{d-1}\), and
\(d(d-1)/3^{d-1}\le2/3\) for these powers of two.
Thus neither constraint degeneracy nor small curvature causes the exact
representation issue.

The polynomial \(P_T\) is irreducible over \(\mathbb Q\). Here is a
direct valuation proof. Put \(n=d-1\), and let \(v\) denote the
3-adic valuation of a root in an algebraic closure of \(\mathbb Q_3\),
normalized by \(v_3(3)=1\). The valuations of the three terms in (6) are

\[
nv,\qquad n+v,\qquad n-1,
\]

because \(d\) is a power of two. If \(v\le0\), the leading term has
uniquely smallest valuation, which prevents their sum from being zero.
If \(v>0\), the linear term has valuation greater than \(n-1\), so
cancellation requires \(nv=n-1\). Every root therefore has valuation
\((n-1)/n\).

For a rational factor of degree \(k\), the ratio of its constant and
leading coefficients has integer 3-adic valuation. Factoring over the
algebraic closure shows that valuation is \(k(n-1)/n\). Since
\(\gcd(n,n-1)=1\), this requires \(n\mid k\). No proper factor exists.

The exact optimizer consequently has algebraic degree \(2^T-1\).
An explicit minimal polynomial has exponentially many coefficient bits,
even in a sparse encoding: the two displayed powers of three already
have that size. The optimum value also has degree \(2^T-1\). Stationarity
gives

\[
F^*=\frac{d-2}{2d}s_0^2-\frac{d-1}{3d}s_0.
\]

Therefore \([\mathbb Q(s_0):\mathbb Q(F^*)]\le2\); this extension
degree also divides the odd number \(d-1\), so it equals one.
A zero noise draw realizes this example whenever the ambient finite grid
contains zero.

The full equality-constrained KKT system is uniformly conditioned as
well. Its equality Jacobian \(A\) obeys
\(\sigma_{\min}(A)\ge1/3\) and \(\|A\|\le5/3\).
The equality adjoints lie in \([-1,0]\), so the Lagrangian Hessian
\(H\) is diagonal and positive semidefinite with \(\|H\|\le5/3\).
It is at least one on the primitive coordinates. For a tangent state
vector,
\(\sum_t(\delta s_t)^2\le(9/5)(\delta s_0)^2\), whence
\(H|_{\ker A}\succeq(5/9)I\). These absolute bounds give a uniform
inverse bound for the saddle matrix
\(\left[\begin{smallmatrix}H&A^T\\A&0\end{smallmatrix}\right]\).

This is an obstruction to expanded exact algebraic output. It is not an
obstruction to approximation or to a succinct arithmetic-circuit or
implicit-system representation.

## What a sparse implicit KKT patch does provide

For fixed-degree local polynomial dynamics and costs, retain the original
states, controls, and equality multipliers. Fix an active set of primitive
bounds and omit the redundant propagated state inequalities. The KKT
equations then form a sparse polynomial system with \(O(T)\) variables
and equations, fixed local degree, and polynomial input length. Their
Jacobian retains the temporal sparsity. Eliminating the states is not
needed to write or evaluate this system.

At a stationary point, LICQ and a positive definite Lagrangian Hessian on
the active tangent space make that KKT Jacobian nonsingular. A proof is
short: a homogeneous KKT vector \((v,w)\) satisfies \(Jv=0\) and
\(Hv+J^Tw=0\). Pairing with \(v\) gives \(v^THv=0\), hence
\(v=0\); full row rank then gives \(w=0\).

The reduced Hessian can be evaluated without expanding compositions.
Choose the equality adjoints to cancel the dependent-state gradients.
For the graph chart \(\Psi(z)=(z,\Phi(z))\),

\[
\nabla^2(F_\gamma\circ\Psi)
=D\Psi^T\nabla_x^2\left(F_\gamma+\sum_t\mu_tq_t\right)D\Psi.
\tag{7}
\]

At stationarity the same identity applies after fixing the active primitive
coordinates. The omitted second-derivative chart term vanishes because the
dependent-state components of the adjusted gradient are zero and the
primitive coordinates of \(\Psi\) are affine. The adjoints obey the
usual stable backward recurrence, giving
\(|\mu_t|\le G/(1-a)\) when the ambient state objective derivatives
are bounded by \(G\).

A rational isolating box, the sparse equations, and a validated interval
Newton or contraction certificate can therefore define an exact algebraic
KKT point without its minimal polynomial. Active multiplier signs and
inactive primitive-bound margins can certify its active set. A uniform
positive reduced Hessian on an enclosing primitive box certifies convexity
there; together with the KKT signs, it certifies the point as that box's
unique minimizer. Positivity at one point alone certifies only a strict
local minimum. Existence, isolation, and the required sign or curvature
certificates must actually be supplied or established.

These observations leave several operations outside the present proof:
polynomial bounds on the isolating-box precision; strict-complementarity
margins on every finite draw; exact comparison of values belonging to
different implicit roots; and an always-correct global fallback with the
claimed bit bound. Interval enclosures can approximate an isolated root,
but they do not decide equality of two exact objective values by themselves.
A complete smoothed exact-closure theorem needs an explicit solution to
those tasks. Stability, LICQ, and tangent positive definiteness alone do
not provide one.

## Targeted verification

The LICQ and irreducibility arguments were checked independently by a
second agent. Two targeted shell commands ran inline Python bodies using
`python - <<'PY'`. The mathematical check used `fractions.Fraction` and
SymPy and passed:

- 92 primitive-active-set rank checks at horizons `1, 2, 3, 5`, plus the
  four original-formulation row deficiencies.
- 28 exact recurrence, first-derivative, and second-derivative checks at
  horizons `2` through `8`, using initial states `1/7, 1/3, 2/3, 1`.
- Seven rational upper-curvature bounds and coprimality checks.
- Exact polynomial irreducibility checks at horizons `2, 3, 4`, and
  three checks of the optimum-value identity modulo the stationarity
  polynomial.

The second command checked this review's local links and trailing
whitespace. All assertions passed. These finite checks support the
algebra; the general claims rely on the proofs above. No project-wide
verification or CI inspection was run.
