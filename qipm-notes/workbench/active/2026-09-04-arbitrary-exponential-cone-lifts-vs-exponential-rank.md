# Why exponential-feature rank does not lower-bound arbitrary exponential-cone lifts

Status: Proved; independently audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the explicit lifts and rank separations; exact-lift
corollary inherits the independently audited curvature-capacity theorem

## Result

The signed exponential-rank lower bound for the product-cosh MGF does not
extend syntactically from direct positive mixtures to arbitrary
exponential-cone lifts.  Auxiliary variables can compose log-sum-exp with an
outer exponential, and elimination can increase exponential-feature rank
without bound.

There are three precise conclusions.

1. A one-dimensional bounded-slope MGF can have exact signed exponential
   rank \(m+1\) while its epigraph has a lift using only three exponential
   cones and one linear inequality.
2. The Rademacher product-cosh MGF used in the signed-rank lower has exact
   signed rank \(2^r\), but its epigraph has an exact lift using
   \(2r+1\) exponential cones and \(r\) linear inequalities.
3. A different argument still gives a useful arbitrary-lift theorem in the
   exact setting: every exact lift of that product-cosh epigraph by
   \(K_{\exp}^R\) and arbitrary nonnegative-ray factors has
   \(R\geq r-1\).  This follows from curvature capacity, not exponential
   rank, and is matched within a constant factor by the explicit lift.

The exact conclusion is not robust under uniform vertical approximation
without further restrictions.  On a compact parameter cube, a finite
piecewise-linear tangent envelope gives a uniform relative epigraph bracket
using no exponential cones at all if linear inequalities are uncharged.
Thus an approximate arbitrary-lift lower must charge the polyhedral part or
impose additional regularity.  The direct positive-mixture lower remains
valid and useful precisely because that output contract excludes these
compositions.

## Exponential-cone convention

Write

\[
 K_{\exp}=\operatorname{cl}\left\{
 (a,b,c):b>0,\ c\geq b e^{a/b}\right\}.
 \tag{1}
\]

In particular,

\[
 (a,1,c)\in K_{\exp}\quad\Longleftrightarrow\quad c\geq e^a.
 \tag{2}
\]

Linear equations and auxiliary variables are free in the cone count.  A
displayed scalar linear inequality can either be kept as part of the
polyhedral formulation or represented by one nonnegative-ray factor.  The
distinction is stated whenever it matters.

## A fixed-cone-count MGF with unbounded exponential rank

Let \(B_1,\ldots,B_m\) be independent
\(\operatorname{Bernoulli}(1/2)\) variables and

\[
 X_m={1\over m}\sum_{k=1}^m B_k\in[0,1].
 \tag{3}
\]

Its MGF is

\[
 F_m(z)=\mathbb E e^{zX_m}
 =\left({1+e^{z/m}\over2}\right)^m
 =2^{-m}\sum_{k=0}^m{m\choose k}e^{kz/m}.
 \tag{4}
\]

### Proposition 1

On every nonempty open real interval, the exact signed exponential rank of
\(F_m\) is \(m+1\), even when the competing exponent nodes are arbitrary
real numbers.  Nevertheless,
\(\operatorname{epi}F_m\) has an exact lift with three copies of
\(K_{\exp}\), one scalar linear inequality, and \(O(1)\) auxiliary
variables:

\[
\begin{aligned}
 (z/m-s,1,u)&\in K_{\exp},\\
 (-s,1,v)&\in K_{\exp},\\
 u+v&\leq2,\\
 (ms,1,t)&\in K_{\exp}.
\end{aligned}
\tag{5}
\]

All affine coefficients in (5) are rational and have
\(O(\log m)\)-bit descriptions.

#### Proof

The first three constraints in (5) are feasible exactly when

\[
 e^{z/m-s}+e^{-s}\leq2,
\]

or equivalently

\[
 s\geq\log\left({1+e^{z/m}\over2}\right).
\tag{6}
\]

The last cone gives \(t\geq e^{ms}\).  Minimizing the feasible right side
over \(s\) proves that the projection is exactly
\(t\geq F_m(z)\).

For the rank statement, combine duplicate nodes in any proposed finite
signed exponential representation.  Distinct real exponentials are
linearly independent on every open interval: their Wronskian is a
nonzero Vandermonde factor, or equivalently repeated differentiation at one
point gives an invertible Vandermonde system.  Equation (4) has the
\(m+1\) distinct nodes \(0,1/m,\ldots,1\), all with nonzero coefficients.
Uniqueness therefore forces at least \(m+1\) terms. \(\square\)

Proposition 1 rules out any bound on exact signed exponential rank that is a
function only of the number of exponential-cone factors, even within
bounded-slope probability MGFs and even with a fixed linear epigraph
readout.  It uses no hidden or high-precision coefficients: the largest
coefficient magnitude is \(m\), with only \(O(\log m)\) encoding length.

## The product-cosh source has exponential rank but a linear cone lift

Let

\[
 f_r(z)=\prod_{i=1}^r\cosh z_i
 =2^{-r}\sum_{x\in\{-1,1\}^r}e^{\langle z,x\rangle}.
\tag{7}
\]

For every coordinate introduce \(s_i,u_i,v_i\) and impose

\[
\begin{aligned}
 (z_i-s_i,1,u_i)&\in K_{\exp},\\
 (-z_i-s_i,1,v_i)&\in K_{\exp},\\
 u_i+v_i&\leq2.
\end{aligned}
\qquad i\in[r],
\tag{8}
\]

together with

\[
 \left(\sum_{i=1}^rs_i,1,t\right)\in K_{\exp}.
\tag{9}
\]

### Proposition 2

Equations (8)--(9) project exactly to
\(\operatorname{epi}f_r\).  They use \(2r+1\) exponential-cone factors and
\(r\) linear inequalities.  In contrast, the exact signed exponential rank
of \(f_r\) on every nonempty open subset of \(\mathbb R^r\) is \(2^r\).

#### Proof

For each \(i\), (8) is feasible exactly when

\[
 2e^{-s_i}\cosh z_i\leq2,
\]

so it is equivalent after projection to
\(s_i\geq\log\cosh z_i\).  Equation (9) gives
\(t\geq\exp(\sum_i s_i)\).  Minimization over the \(s_i\)'s proves the
epigraph identity.

For exact rank, move any proposed signed representation to the same side as
(7), combine equal exponent vectors, and use linear independence of
multivariate exponentials.  One quick reduction chooses a direction not
orthogonal to any difference of the finitely many exponent vectors and
restricts the analytic identity to a line segment in the open set.  The
resulting univariate exponentials have distinct exponents and are linearly
independent.  Hence every one of the \(2^r\) cube-corner nodes in (7) must
occur. \(\square\)

This is a direct counterexample to the hoped-for elimination principle.
The boundary value of a fixed linear readout of an affine
\(K_{\exp}^{2r+1}\) lift need not be an exponential sum with
\(O(r)\), or even polynomially many, terms.  Proposition 1 shows that no
finite bound depending only on the cone count exists.

## What survives for arbitrary exact lifts

The failure of the rank transfer does not make the exact arbitrary-lift
question vacuous.  The local curvature-capacity theorem supplies a
different lower bound.

### Proposition 3

Fix \(r\geq2\) and \(K>0\).  Suppose the epigraph of \(f_r\) on
\([-K,K]^r\) has an exact lift over

\[
 K_{\exp}^R\times\mathbb R_+^P
\tag{10}
\]

with arbitrary affine slices, projections, and free auxiliary variables.
Then

\[
 \boxed{R\geq r-1.}
\tag{11}
\]

The exact product-barrier theorem moreover implies that every
self-concordant barrier, even a nonhomogeneous barrier coupling all factors,
on the full ambient product in (10) has

\[
 \nu_{\rm ambient}\geq3R+P\geq3(r-1)+P.
 \tag{11a}
\]

The standard separable barrier attains \(3R+P\).  This barrier statement
concerns the full ambient product, not a projected feasible image or all
possible IPM formulations.

#### Proof

Choose

\[
 1<c<\cosh K
\]

and form the compact sublevel body

\[
 C_c=\{z\in\mathbb R^r:f_r(z)\leq c\}.
\tag{12}
\]

If any \(|z_i|\geq K\), then \(f_r(z)\geq\cosh K>c\).
Thus \(C_c\) lies in the interior of the parameter cube, and slicing the
claimed epigraph lift at \(t=c\) gives an exact lift of \(C_c\) over the
same cone product.  Continuity makes \(C_c\) closed, while
\(f_r(z)\geq\cosh(\|z\|_\infty)\) makes it bounded.

The body is full-dimensional and contains zero in its interior.  Moreover,

\[
 \nabla^2 f_r
 =f_r\left[
 \operatorname{diag}(\operatorname{sech}^2 z_i)
 +(\tanh z)(\tanh z)^T\right]\succ0.
\tag{13}
\]

On the level \(f_r=c>1\), the gradient is nonzero, so the second fundamental
form is positive definite on every tangent space.  The independently
audited universal curvature-capacity theorem applies.  A
three-dimensional exponential cone has curvature capacity at most one,
while one-dimensional ray factors have capacity zero.  Therefore
\(r-1\leq R\), proving (11).  One-dimensional orthant factors contribute
zero curvature capacity, but they do contribute one unit each to the exact
ambient barrier parameter.  The independently audited exact mixed-product
barrier theorem therefore gives (11a). \(\square\)

Together with Proposition 2, this pins the exact exponential-cone factor
complexity of the product-cosh epigraph to

\[
 r-1\leq R_{\rm exact}\leq2r+1.
\tag{14}
\]

This is the valid arbitrary-lift consequence.  It is independent of the
signed-rank proof and currently applies only to exact representation.

## Why the uniform approximate theorem does not follow

Uniform relative approximation alone does not preserve boundary curvature.
The obstruction is elementary and applies to any positive smooth convex
function on a compact domain.

### Proposition 4

Let \(D\subset\mathbb R^r\) be a compact polytope, and let
\(f>0\) be convex and \(C^2\) on a neighborhood of \(D\).  For every
\(0<\epsilon<1\), there is a finite piecewise-linear convex function \(p\)
such that

\[
 (1-\epsilon)f(z)\leq p(z)\leq f(z)
 \qquad(z\in D).
\tag{15}
\]

Its epigraph on \(D\) has a formulation using the fixed linear description
of \(D\), finitely many additional scalar linear inequalities, and no
exponential-cone factor.

#### Proof

Put

\[
 m_f=\min_D f>0,\qquad
 L_f=\sup_D\|\nabla^2f\|_{\rm op}<\infty.
\]

Take a finite Euclidean \(\delta\)-net \(\mathcal N\) of \(D\), with
\(\delta^2\leq2\epsilon m_f/L_f\) when \(L_f>0\), and define the maximum of
supporting tangents

\[
 p(z)=\max_{x\in\mathcal N}
 \{f(x)+\langle\nabla f(x),z-x\rangle\}.
\tag{16}
\]

Convexity gives \(p\leq f\).  For a net point \(x\) within \(\delta\) of
\(z\), Taylor's theorem gives

\[
 f(z)-p(z)\leq {L_f\over2}\|z-x\|^2
 \leq\epsilon m_f\leq\epsilon f(z),
\]

which proves (15).  The epigraph of (16) is the intersection of the finitely
many halfspaces
\[
 t\geq f(x)+\langle\nabla f(x),z-x\rangle,
 \qquad x\in\mathcal N.
\]
If \(L_f=0\), the function is affine on \(D\) and one tangent is exact.
\(\square\)

Applied to \(f_r\) on the compiler cube, Proposition 4 preserves the
uniform multiplicative epigraph bracket.  More explicitly, (15) gives

\[
 \operatorname{epi}\!\left({p\over1-\epsilon}\right)
 \subseteq \operatorname{epi}(f)
 \subseteq \operatorname{epi}(p)
 \quad\text{on }D.
\tag{17}
\]

The approximation destroys the smooth curved boundary used by Proposition
3.  If scalar inequalities are uncharged, it even has
\(R_{\exp}=0\).  If they are represented by nonnegative-ray factors, their
potentially large number contributes to formulation size and barrier
parameter.  Thus no contradiction with curvature capacity occurs.

An arbitrary approximate-lift theorem would need at least one additional
contract, for example:

- charge all polyhedral as well as exponential-cone factors;
- require a contact-regular smooth factorization with quantitative
  curvature control; or
- retain the direct positive-mixture semantics.

Without such a contract, the signed exponential-rank theorem cannot be
promoted to an arbitrary-ECP or general-IPM iteration lower bound.

## Literature screen

The conic-lift framework is standard; see
[Gouveia--Parrilo--Thomas](https://doi.org/10.1287/moor.1120.0575).
The log-sum-exp and outer-exponential constructions used in
(5) and (8)--(9) are standard exponential-cone modeling operations; see the
[MOSEK Modeling Cookbook](https://docs.mosek.com/modeling-cookbook/expo.html).
The exact curvature lower in Proposition 3 is a direct corollary of the
independently audited
[universal curvature-capacity theorem](2026-09-04-universal-cone-curvature-capacity.md).
Its ambient-barrier corollary uses the independently audited
[exact exponential-product barrier
theorem](2026-09-04-exponential-product-exact-barrier-parameter.md).

A targeted search on 2026-09-04 found general work on conic lifts,
approximate cone factorizations, and exponential-cone modeling, but no
statement combining the fixed-three-cone binomial-MGF rank separation, the
product-cosh exact factor-count sandwich (14), and the explicit
piecewise-linear obstruction to a relative-approximation transfer.  The
modeling ingredients are standard; the useful result here is the sharp
boundary between the signed-feature theorem, arbitrary exact lifts, and
unrestricted approximate formulations.  Priority remains subject to expert
review.

## Independent audit scope

The audit checked the exact projections in (5) and (8)--(9), including the
normalization by two; the \(m+1\) and \(2^r\) rank claims against arbitrary
real nodes and signed coefficients; and the generic-line reduction for
multivariate exponential independence.  It verified that the level
\(1<c<\cosh K\) is closed, bounded, and strictly inside the compiler cube,
and that (13) supplies full positive curvature.  Hence the audited
curvature-capacity theorem gives \(R\geq r-1\), with orthant rays
contributing zero curvature capacity.

The audit separately checked the exact mixed-product barrier theorem:
orthant rays contribute one barrier unit even though they carry no
curvature, so the full ambient optimum is \(3R+P\).  Finally, it checked the
tangent-net error and both inclusions in (17).  The polyhedral obstruction
counts linear inequalities as free only in the explicitly stated model; it
does not claim a small total formulation or barrier parameter.
