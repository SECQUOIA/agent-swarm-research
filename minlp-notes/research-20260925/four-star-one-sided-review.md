# Independent review of the one-sided star exactness argument

Reviewed on 2026-09-25 against
[four-star-analytic.md](four-star-analytic.md). The proposed result is
correct. It is a direct application of the corrected SPN theorem for the
five-vertex book graph. It does not settle arbitrary four-variable box
stars, and no novelty claim is justified by this review.

## Precise one-sided statement

Let

\[
q(t,y)=a t^2+b t+c+
\sum_{i=1}^{m}\bigl(d_i y_i^2+(e_i+f_i t)y_i\bigr),
\qquad 0\leq t\leq1,\quad y\in\mathbb R_+^m,
\]

where \(m\leq3\), and suppose its infimum \(\lambda\) is finite.
Use the moment matrix

\[
Y=\begin{pmatrix}1&\mu^T\\\mu&X\end{pmatrix}\succeq0
\]

for \((t,y)\), together with

\[
X_{tt}\leq\mu_t,\qquad
0\leq X_{ti}\leq\mu_i\quad(1\leq i\leq m),\qquad
X_{ij}\geq0\quad(1\leq i<j\leq m).
\tag{1}
\]

Then minimizing the linearized objective over these moments gives exactly
\(\lambda\). The constraints \(0\leq\mu_t\leq1\) and
\(\mu_i\geq0\) may be included explicitly, but follow from PSD and (1).
For example, \(\mu_t^2\leq X_{tt}\leq\mu_t\), and
\(0\leq X_{ti}\leq\mu_i\).

The constraints in (1) are the needed products of the valid linear
inequalities \(t\geq0\), \(1-t\geq0\), and \(y_i\geq0\).
In particular, the last family concerns nonedges of the star. The proof
below does not permit dropping it.

## Certificate proof, with the boundary and support issues checked

Introduce two nonnegative hub variables \(r,s\), and define the polynomial

\[
\begin{aligned}
Q(r,s,y)={}&a s^2+b s(r+s)+(c-\lambda)(r+s)^2\\
&+\sum_{i=1}^{m}\bigl(d_i y_i^2+e_i(r+s)y_i+f_i s y_i\bigr).
\end{aligned}
\tag{2}
\]

When \(r+s>0\), this is

\[
(r+s)^2\left[
q\left(\frac{s}{r+s},\frac{y}{r+s}\right)-\lambda
\right]\geq0.
\]

At \(r=s=0\), continuity of the polynomial (2) gives nonnegativity as
well. This is a genuine limit of nonnegative arguments, for example
\((r,s,y)=(\varepsilon,0,y)\) as \(\varepsilon\downarrow0\).
No boundedness of \(y/(r+s)\) is needed: the lower bound \(\lambda\)
holds on the entire nonnegative leaf orthant.

Thus the symmetric coefficient matrix \(A\) of \(Q\) is copositive.
Its only possible off-diagonal nonzero entries join the hubs to each
other or a hub to a leaf. Its support is therefore contained in the book
graph \(T_{m+2}\).

[Shaked-Monderer's corrigendum, Theorem 1](https://arxiv.org/html/1712.05115)
proves that \(T_5\), the graph of three triangles sharing a common edge,
is SPN. In other words, every copositive matrix having that graph admits
a decomposition \(A=P+N\), with \(P\succeq0\) and \(N\geq0\)
entrywise. The corrected theorem is sufficient here; the superseded
claim for arbitrary book graphs is unnecessary.

To account explicitly for missing edges and \(m<3\), pad with zero
rows and columns to order five. Add \(\varepsilon>0\) to all missing
book edges and their symmetric positions. This preserves copositivity
and gives the exact graph \(T_5\), so the perturbed matrix is SPN.
The SPN cone is closed: in any convergent sequence
\(A_k=P_k+N_k\), its diagonal bounds
\(0\leq(P_k)_{ii}\leq(A_k)_{ii}\) bound all entries of \(P_k\) by
PSD; a convergent subsequence gives the limiting decomposition. Taking
\(\varepsilon\downarrow0\) and then a principal submatrix proves
the desired SPN decomposition for \(A\).

Now set

\[
z=(1,t,y),\qquad w=(1-t,t,y)=Bz.
\]

For every relaxation point, the moment matrix of \(w\) is
\(W=BYB^T\succeq0\). Every entry of \(W\) is nonnegative:

- Diagonal entries are nonnegative by PSD.
- The hub cross entry is \(\mu_t-X_{tt}\geq0\).
- The hub–leaf entries are \(X_{ti}\geq0\) and
  \(\mu_i-X_{ti}\geq0\).
- The leaf–leaf entries are \(X_{ij}\geq0\).

Consequently

\[
\mathcal L_Y(q-\lambda)
=A\mathbin\bullet W
=P\mathbin\bullet W+N\mathbin\bullet W\geq0.
\]

The first term is nonnegative by self-duality of the PSD cone, and the
second by entrywise nonnegativity. Every actual point generates feasible
moments, so the reverse inequality for the infimum follows as usual.
This proves exactness directly. It invokes neither strong conic duality
nor existence of an optimal relaxed moment matrix.

Although \(A\) has book support, the matrices \(P\) and \(N\) need
not preserve that support. Their leaf–leaf entries can cancel in the
sum. This is why the nonedge constraints in (1) remain relevant.

## Finiteness and attainment

The argument above only needs a finite infimum. In this particular
class, a finite infimum is also attained. Indeed, finiteness forces
\(d_i\geq0\). If \(d_i=0\), it further forces
\(e_i+f_i t\geq0\) throughout the center interval, so \(y_i=0\)
is always a minimizing choice. If \(d_i>0\), a minimizing choice is

\[
y_i(t)=\max\left\{0,-\frac{e_i+f_i t}{2d_i}\right\}.
\]

These choices are uniformly bounded and continuous on \([0,1]\).
The reduced objective is continuous there and attains its minimum.
An actual minimizer therefore also produces an optimal rank-one point
of the relaxation. This conclusion is about existence of a rank-one
optimum, not about ranks of all optimal moment matrices.

## Passage to the finite box

Suppose \(d_i>0\) and put

\[
h_i(t)=-\frac{e_i+f_i t}{2d_i}.
\]

For each leaf, assume either \(\max h_i\leq1\) or \(\min h_i\geq0\),
where the extrema are taken on \([0,1]\). Both tests are checked at
the two endpoints because \(h_i\) is affine.

In the first case, releasing the upper bound leaves the minimizing
response \(\max\{0,h_i(t)\}\) inside \([0,1]\). In the second
case, use the complemented coordinate \(v_i=1-y_i\); its unconstrained
response is \(1-h_i(t)\leq1\), and the same argument applies.
The root coefficients may change under complementation, but the star
support and positive leaf curvatures do not.

Thus the simultaneous bound release preserves the minimum for every
fixed center value. The full finite-box SDP–RLT is invariant under the
chosen complementations and is contained in the one-sided relaxation.
The preceding certificate proves its lower bound equals the box minimum.
The coefficient test is sufficient, not necessary: it excludes exactly
those affine responses with \(\min h_i<0\) and \(\max h_i>1\).
Equality at either endpoint presents no problem.

More generally, the certificate applies whenever a chosen set of leaf
orientations makes bound release preserve the global minimum. The
positive-curvature coefficient test is an easily checked way to ensure
the stronger pointwise property; it is not an additional assumption of
that more general proposition.

## Limits and significance

The example in the analytic note,

\[
t^2+y^2-4ty+t+y=(t-y)^2+t(1-y)+y(1-t),
\]

is a decisive check against overextending the result. Its box minimum is
zero and its SDP–RLT certificate is explicit. Yet its value is
\(-1/4\) at both \((1,3/2)\) and \((0,-1/2)\). Each possible
orientation releases a bound that permits one of those points.
Therefore even an exact two-variable instance need not satisfy the
bound-release premise.

The separate five-variable star obstruction has four nonnegative leaves
and a bounded center; its displayed minimizing responses never need
their chosen leaf upper bounds. It rules out extending this one-sided
theorem to arbitrary four-leaf stars. Together these facts identify a
sharp universal threshold for this one-sided domain. They do not
establish a sharp threshold for fully bounded stars.

The one-sided theorem supplies a checkable sufficient condition for
standard SDP–RLT exactness on some four-variable stars. Its reusable
idea is the conversion of a bounded scalar into two nonnegative hubs.
The substantial graph-theoretic input is already known. This review
does not establish that the optimization corollary is new, does not
give a new SPN theorem, and does not show improved solver performance.
The unrestricted four-variable star remains outside the proved scope.

## Verification record

The review independently expanded the homogenized polynomial, checked
each transformed moment entry, verified the finite-box response test,
and read the corrected source theorem and its proof. No computational
claim depends on numerical optimization. No automated test was needed
for these exact algebraic arguments, and no project-wide verification
or CI inspection was run. Formal proof verification and an exhaustive
literature search were not performed.
