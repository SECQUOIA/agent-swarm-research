# One-step robust Newton-output hardness for the parallel-path LP

Date: 2026-09-02

## Result

The robust parallel-path LP admits an input-independent, strictly positive,
exactly centered primal--dual initialization from which one standard
infeasible-start Newton correction, with centering target
\(\widehat\mu=\mu_0/2\), lands exactly on a parity-hard feasible central
point. Consequently:

- preparing the exact Newton-direction amplitude state is
  \(\Omega(N)=\Omega(\sqrt P)\) coefficient-query hard; and
- the existing constant-\(\ell_2\)-residual theorem becomes a robust
  approximate Newton-update lower bound.

The construction changes no LP row, column, coefficient, or oracle. It only
chooses a fixed initialization.

## The robust LP

Use the LP (R2)--(R3) from
2026-09-02-parity-amplified-primal-state-lower-bound.md. There are
\[
 P=33N^2-1
\]
tree vertices and \(4P\) nonnegative variables
\((u_j,v_j,h_j,t_j)\). Write
\[
 d_j=u_j-v_j,\qquad q_j=u_j+v_j.
\]
The equality system is
\[
 D_a d=e_r,\qquad D_1h=e_r,\qquad q+t-2h=0,
\tag{1}
\]
where \(D_a\) is the pinned labelled-tree incidence matrix and \(D_1\) is
its unsigned version. The objective coefficients are
\[
 c_u=c_v=2,\qquad c_h=c_t=1.
\]
Every row and column has at most four nonzeros. A coherent sparse LP query
uses at most one query to the hidden-sign oracle, despite the repeated paths.

## A rational central point

On the feasible affine space, every central pair has the same
\(q\in(1,2)\), and the scalar first-order condition is
\[
 1-\mu\left(\frac{2q}{q^2-1}-\frac1{2-q}\right)=0.
\tag{2}
\]
Choose
\[
 q_1=\frac43,\qquad
 \mu_1=\frac{14}{27}.
\tag{3}
\]
Let \(\tau_j\) be the root-to-\(j\) sign product. The primal central point is
\[
 (u_j^1,v_j^1)
 =
 \begin{cases}
 (7/6,1/6),&\tau_j=+1,\\
 (1/6,7/6),&\tau_j=-1,
 \end{cases}
 \qquad
 h_j^1=1,\qquad t_j^1=\frac23.
\tag{4}
\]
Its slack is fixed by complementarity:
\[
 (s_{u,j}^1,s_{v,j}^1)
 =
 \begin{cases}
 (4/9,28/9),&\tau_j=+1,\\
 (28/9,4/9),&\tau_j=-1,
 \end{cases}
\]
\[
 s_{h,j}^1=\frac{14}{27},\qquad
 s_{t,j}^1=\frac79.
\tag{5}
\]
Strict feasibility and the central KKT equations give the associated unique
dual multiplier \(y^1\).

## Input-independent centered initialization

Set \(y^0=0\), and at every vertex take
\[
 u_j^0=v_j^0=\frac89,\qquad
 h_j^0=\frac{16}{3},\qquad
 t_j^0=\frac{32}{9},
\tag{6}
\]
\[
 s_{u,j}^0=s_{v,j}^0=\frac{64}{27},\qquad
 s_{h,j}^0=\frac{32}{81},\qquad
 s_{t,j}^0=\frac{16}{27}.
\tag{7}
\]
This point is independent of every hidden sign, strictly positive, and
exactly centered at
\[
 X^0s^0=\mu_0\mathbf1,\qquad
 \mu_0=\frac{512}{243}.
\tag{8}
\]
It is deliberately primal and dual infeasible. Standard infeasible-start
Newton equations allow both residuals.

Take the usual centering target
\[
 \widehat\mu=\frac{\mu_0}{2}=\frac{256}{243}.
\tag{9}
\]

### Theorem 1 (one exact Newton correction)

At the initialization (6)--(8), the unique primal--dual Newton correction
with target (9) is
\[
 (\Delta x,\Delta y,\Delta s)
 =(x^1-x^0,y^1-y^0,s^1-s^0).
\tag{10}
\]
Thus a full step lands exactly on the feasible central point
\((x^1,y^1,s^1)\) at \(\mu_1=14/27\).

### Proof

The primal and dual Newton equations hold because the endpoint is feasible:
\[
 A\Delta x=b-Ax^0,
\qquad
 A^\top\Delta y+\Delta s=c-A^\top y^0-s^0.
\tag{11}
\]
It remains only to check linearized complementarity. Directly from
(4)--(7), every coordinate satisfies the same cross identity
\[
 s_i^0x_i^1+x_i^0s_i^1=\frac{256}{81}.
\tag{12}
\]
For example, on the two members of a signed pair,
\[
 \frac{64}{27}\frac76+\frac89\frac49
 =
 \frac{64}{27}\frac16+\frac89\frac{28}{9}
 =\frac{256}{81}.
\]
For the \(h\) and \(t\) coordinates,
\[
 \frac{32}{81}\cdot1+\frac{16}{3}\frac{14}{27}
 =
 \frac{16}{27}\frac23+\frac{32}{9}\frac79
 =\frac{256}{81}.
\]
Therefore
\[
\begin{aligned}
 S^0\Delta x+X^0\Delta s
 &=\frac{256}{81}\mathbf1-2\mu_0\mathbf1\\
 &=-\frac{256}{243}\mathbf1
  =(\widehat\mu-\mu_0)\mathbf1,
\end{aligned}
\tag{13}
\]
which is exactly the complementarity Newton equation.

Finally, \(A\) has full row rank and \(X^0,S^0\) are positive diagonal.
Eliminating \(\Delta s\) gives an SPD normal matrix
\[
 A(S^0)^{-1}X^0A^\top,
\]
so the Newton correction is unique. \(\square\)

The full step remains strictly positive. Although its linearized target is
\(\widehat\mu=\mu_0/2\), the quadratic products at the endpoint equal
\(\mu_1\):
\[
 \frac76\frac49
 =\frac16\frac{28}{9}
 =1\cdot\frac{14}{27}
 =\frac23\frac79
 =\frac{14}{27}.
\]

## Exact Newton-direction state is parity-hard

The direction components at every vertex are
\[
 (\Delta u_j,\Delta v_j)
 =
 \begin{cases}
 (5/18,-13/18),&\tau_j=+1,\\
 (-13/18,5/18),&\tau_j=-1,
 \end{cases}
\]
\[
 \Delta h_j=-\frac{13}{3},\qquad
 \Delta t_j=-\frac{26}{9}.
\tag{14}
\]
Every vertex contributes the same squared norm
\[
 \frac{25+169}{18^2}
 +\frac{169}{9}
 +\frac{676}{81}
 =\frac{499}{18}.
\tag{15}
\]

Let \(S\) be the \(16N^2\) leaves in the endpoint copy trees. On a measured
\(u_j\) coordinate with \(j\in S\), report \(-1\); on a measured \(v_j\)
coordinate report \(+1\); elsewhere report a fair sign. Conditional
correct-minus-incorrect squared mass on an output pair is
\[
 \frac{169-25}{18^2}=\frac49.
\]
The decoder bias on the ideal normalized direction state is therefore
\[
 \frac{|S|(4/9)}
      {2P(499/18)}
 =\frac4{499}\frac{|S|}{P}
 >\frac{64}{16467}>\frac1{258}.
\tag{16}
\]
Trace distance \(1/400\) leaves a fixed positive bias. A fixed number of
repetitions, independent of \(N\), computes endpoint parity with bounded
error.

### Theorem 2 (Newton-direction output lower bound)

Any coherent coefficient-query algorithm whose unconditional output state is
within trace distance \(1/400\) of
\[
 |\Delta x/\|\Delta x\|_2\rangle
\]
for the Newton correction in Theorem 1 makes
\[
 \Omega(N)=\Omega(\sqrt P)
\]
LP coefficient queries. The same holds for a heralded constant-success
branch after charging the constant repetitions.

The proof is the decoder above followed by the bounded-error quantum parity
lower bound. Each LP oracle query is simulated with one hidden-sign query.
This is a genuine Newton-direction-state theorem; no tomography or classical
coordinate output is assumed.

## Robust approximate Newton-update lower bound

Let an algorithm return a state \(\rho\) for which there is a direction
\(\widetilde{\Delta x}\) such that
\[
 \widetilde x^+=x^0+\widetilde{\Delta x}\ge0,
\]
\[
 \frac{\|A\widetilde{\Delta x}-(b-Ax^0)\|_2}{\|b\|_2}
 \le10^{-3},
\tag{17}
\]
and
\[
 D_{\rm tr}\!\left(
 \rho,
 |\widetilde x^+/\|\widetilde x^+\|_2\rangle
 \langle\widetilde x^+/\|\widetilde x^+\|_2|
 \right)
 \le\frac1{400}.
\tag{18}
\]
Equation (17) is exactly
\[
 \|A\widetilde x^+-b\|_2/\|b\|_2\le10^{-3}.
\]
The robust residual-tube theorem for (1) therefore applies without using the
dual or complementarity equations.

### Theorem 3 (robust approximate Newton-update output)

Every algorithm satisfying (17)--(18) makes
\[
 \Omega(N)=\Omega(\sqrt P)
\]
coefficient-oracle queries. This remains true if the approximate direction
also satisfies any standard dual, complementarity, neighborhood, or
objective-accuracy requirement.

This theorem is robust to a fixed global right-hand-side-relative
\(\ell_2\) primal Newton residual. It does not assert robustness to
\(\|\cdot\|_2/\sqrt{\text{number of rows}}\), nor does it assert that the
state of an arbitrary residual-accurate direction itself is hard. The
robust state is the updated original-primal point.

## Why the infeasible start is essential

An input-independent primal-feasible point cannot exist: the equations
\(D_ad=e_r\) fix \(d_j=\tau_j\), including all hidden prefix products.
The earlier observation that feasible reduced directions change \(u_j,v_j\)
equally is therefore not contradicted.

The successful initialization also uses dual infeasibility. If one fixes
\(y^0=0,s^0=c\), exact centering forces
\[
 (u^0,v^0,h^0,t^0)
 =(\mu_0/2,\mu_0/2,\mu_0,\mu_0),
\]
which happens to satisfy every cap equation. Requiring a one-step secant to
a central point then overconstrains the pair, \(h\), \(t\), and cap
coordinates. Indeed, write the endpoint pair values as
\(U=(q+1)/2,V=(q-1)/2\). Equality of the cross terms on the two swapped pair
coordinates forces
\[
 \mu_0\mu_1=4UV=q^2-1.
\]
Equality with the \(h\)-coordinate cross term forces instead
\[
 1+\mu_0\mu_1=2q.
\]
Together these give \(q=2\), outside the strictly feasible central path.
Thus this dual-feasible symmetric start admits no exact one-step secant to an
interior central point, regardless of the requested target. The rational
initialization (6)--(7) escapes
this obstruction by allowing both primal cap residuals and a dual residual,
while retaining exact positivity and complementarity centering.

## Preconditioning and oracle accounting

Theorems 2--3 are end to end and independent of the normal/KKT
representation. Any data-dependent preconditioner may move the parity
information among setup, transformed-RHS preparation, iterative application,
and recovery, but it cannot change the fixed output decoder. If these phases
make respectively
\[
 Q_{\rm set},Q_{\rm rhs},Q_{\rm solve},Q_{\rm rec}
\]
raw LP queries, then either output theorem gives
\[
 Q_{\rm set}+Q_{\rm rhs}+Q_{\rm solve}+Q_{\rm rec}
 =\Omega(N).
\tag{19}
\]
Thus a natural exact tree factor may condition the Newton system perfectly,
but applying it or recovering the original direction/update must pay the
same total query cost.

## Status and novelty

The robust residual-tube theorem and the parallel-path gadget were already
established in the companion note. The new result here is the explicit
input-independent rational initialization and the proof that one ordinary
infeasible-start Newton correction with \(\sigma=1/2\) lands exactly on its
hard central point. The direction-state decoder is also new relative to the
earlier scope statement, which only treated the final primal state.

Status: **proof complete in the fixed-pattern coefficient-query model.**
