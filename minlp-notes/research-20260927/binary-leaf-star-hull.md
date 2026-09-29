# An exact SDP–RLT projection for a continuous center and binary leaves

Research date: 2026-09-27. Status: proved below, independently reviewed,
and supported by targeted exact checks. The literature comparison is
preliminary; priority is not established.

## Result and meaning

Let

\[
H_m=\operatorname{conv}\{(t,t^2,y,ty):
 t\in[0,1],\ y\in\{0,1\}^m\}.
\]

The products \(ty\) are componentwise. Introduce first moments
\(\mu=(\mu_t,\mu_1,\ldots,\mu_m)\) and a symmetric matrix \(X\).
Let \(S_m\) be the full unit-box SDP–RLT region:

\[
Y=\begin{pmatrix}1&\mu^T\\\mu&X\end{pmatrix}\succeq0,
\quad 0\leq\mu\leq1,
\quad
\max(0,\mu_i+\mu_j-1)\leq X_{ij}\leq\min(\mu_i,\mu_j)
\]

for every pair, including the diagonal. Impose the binary-leaf
equalities \(X_{ii}=\mu_i\) for \(i=1,\ldots,m\).

**Theorem 1.** For every finite \(m\), the projection of this face of
\(S_m\) onto
\((\mu_t,X_{tt},\mu_1,\ldots,\mu_m,X_{t1},\ldots,X_{tm})\)
equals \(H_m\).

The full region \(S_m\) has the same projection, so the binary-leaf
equalities are optional. To see this directly, increase each leaf
diagonal \(X_{ii}\) to \(\mu_i\). This adds a nonnegative diagonal
matrix to \(Y\), preserving PSD and all RLT constraints without
changing any retained coordinate.

There is no assertion that the auxiliary leaf–leaf moments can also be
matched by a distribution. They are auxiliary variables in the stated
semidefinite representation.

The key optimization statement is stronger than needed for this
projection.

**Theorem 2.** The full SDP–RLT relaxation is exact for every star
quadratic on \([0,1]^{m+1}\) whose leaf square coefficients are
nonpositive. The number of leaves, center square coefficient, linear
coefficients, and center–leaf interaction signs are unrestricted.

This settles a dimension-independent subclass of the star question,
not the case of arbitrarily curved leaves. In particular it does not
settle the unrestricted four-variable star considered in the
[earlier investigation](../research-20260925/four-star-analytic.md).

**Proposition 3 (upper RLT suffices for submodular stars).** Suppose the
objective in Theorem 2 already has nonpositive center–leaf interaction
coefficients. Its relaxation remains exact after dropping all lower RLT
inequalities. Precisely, it suffices to impose

\[
Y\succeq0,\qquad 0\leq\mu\leq1,\qquad
X_{ij}\leq\mu_i,\quad X_{ij}\leq\mu_j
\]

for every pair, including the diagonal. This proposition concerns the
specified submodular objectives. The arbitrary-sign objective theorem
and the moment-hull theorem above retain full RLT.
The [forest extension](binary-separator-forest-hull.md) glues these exact
star projections across binary vertices; its separate review status is
recorded there.

## A standard submodular rounding fact

Let

\[
r(y)=\rho+\sum_i\ell_i y_i-\sum_{i<j}h_{ij}y_i y_j,
\qquad h_{ij}\geq0.
\]

For first moments \(u\in[0,1]^m\) and any products
\(Z_{ij}\leq\min(u_i,u_j)\), its linearized value satisfies

\[
\rho+\ell^Tu-\sum_{i<j}h_{ij}Z_{ij}
\ \geq\ \mathbb E[r(B)]
\ \geq\ \min_{y\in\{0,1\}^m}r(y),
\]

where \(B_i=\mathbf1\{U\leq u_i\}\) for a single uniform random
variable \(U\in[0,1]\). Indeed,
\(\mathbb E[B_i]=u_i\) and
\(\mathbb E[B_iB_j]=\min(u_i,u_j)\). The distribution has at most
\(m+1\) distinct outcomes.

This is the established exactness of McCormick linearization for
quadratic submodular binary minimization, supplied here with its short
proof. It is not a claimed contribution.

## Reductions that retain valid relaxation bounds

For a quadratic polynomial \(p\), write \(L_Y(p)\) for its linearized
evaluation at the moments. PSD gives \(L_Y(\ell^2)\geq0\) for every
affine \(\ell\). Full RLT gives
\(L_Y(uv)\geq0\) for all products of box literals. Consequently,
if

\[
q=\widetilde q+R,
\]

where \(R\) is a nonnegative combination of literal products,
\(q\) and \(\widetilde q\) have the same box minimum \(v\), and
\(L_Y(\widetilde q)\geq v\) for every feasible relaxation point,
then \(L_Y(q)\geq v\) as well. Variable elimination uses the
corresponding principal submatrix of \(Y\).

A leaf term with coefficient \(d_i\leq0\) has the identity

\[
d_i y_i^2=d_i y_i+(-d_i)y_i(1-y_i).
\]

Replacing it by \(d_i y_i\) changes neither minimum: both the original
concave univariate leaf term and its affine replacement attain their
minimum at a leaf endpoint for fixed other variables, and they agree
there. The remainder is a valid diagonal RLT product.

After making these replacements, complement each leaf as needed to
write the remaining objective as

\[
q(t,y)=a t^2+b t+c+\sum_i(e_i y_i-k_i t y_i),\qquad k_i\geq0. \tag{1}
\]

Complementation acts by an invertible affine congruence on the moment
matrix and permutes box literals, so it preserves PSD and full RLT.

If \(a\leq0\), replace \(a t^2\) by \(a t\) in the same way.
The result is a submodular multilinear polynomial in \(t,y\). The
rounding fact proves exactness directly. Hence assume \(a>0\).

Leaves with a response of fixed sign can be eliminated. If \(e_i\leq0\),
set \(y_i=1\), updating \(b,c\). The difference from that substitution is

\[
(-e_i)(1-y_i)+k_i t(1-y_i)\geq0.
\]

If \(e_i\geq k_i\), set \(y_i=0\); the difference is

\[
(e_i-k_i)y_i+k_i(1-t)y_i\geq0.
\]

Each difference has nonnegative relaxation evaluation, and the
substitution preserves the true minimum. This also handles \(k_i=0\).
Individual literals have nonnegative evaluation from \(0\leq\mu\leq1\).
Every remaining leaf satisfies

\[
0<e_i<k_i. \tag{2}
\]

Empty sums are allowed. In that case the endpoint branches below or
the final square argument reduce to a univariate quadratic.

## Removing the lower-end clipping of the center response

Write \(K=\sum_i k_i\), \(E=\sum_i e_i\), and let \(v\) be the
minimum of (1). Eliminating its affine leaves gives

\[
F(t)=a t^2+b t+c-\sum_i(k_i t-e_i)_+,
\qquad v=\min_{0\leq t\leq1}F(t). \tag{3}
\]

In particular \(v\leq F(0)=c\). If \(b\leq0\), leave the polynomial
unchanged for this step. Suppose \(b>0\).

If \(b\geq K-E\), the minimum is \(c\), with the direct certificate

\[
q-c=a t^2+(b-K+E)t+
\sum_i\bigl[(k_i-e_i)t(1-y_i)+e_i(1-t)y_i\bigr]. \tag{4}
\]

All coefficients are nonnegative and \(t=0,y=0\) attains equality.
This completes the proof in this branch.

Otherwise \(0<b<K-E\). Define

\[
G(\tau)=\sum_i(k_i-e_i/\tau)_+,\qquad 0<\tau\leq1.
\]

The function is continuous, is zero for sufficiently small positive
\(\tau\), and is strictly increasing wherever it is positive.
Since \(G(1)=K-E>b\), there is a unique \(\tau\in(0,1)\) such that
\(G(\tau)=b\). Put

\[
\lambda_i=(k_i-e_i/\tau)_+,
\quad k_i'=k_i-\lambda_i=\min(k_i,e_i/\tau),
\quad
q'=q-\sum_i\lambda_i t(1-y_i). \tag{5}
\]

Then \(\sum_i\lambda_i=b\), so the coefficient of \(t\) in \(q'\)
is zero, and \(0<e_i<k_i'\). The reduced objective of \(q'\) is

\[
F'(t)=a t^2+c-\sum_i(k_i't-e_i)_+.
\]

For \(t\leq\tau\), every \(k_i't\leq e_i\); hence
\(F'(t)=a t^2+c\geq c\geq v\).
For \(t\geq\tau\), every changed leaf, with \(\lambda_i>0\), is
active in both reduced objectives. Its hinge changes by
\(\lambda_i t\). Summing gives

\[
F'(t)=F(t)-b t+\sum_i\lambda_i t=F(t)\geq v.
\]

Therefore \(\min q'\geq v\). On the box, (5) also gives \(q'\leq q\),
so \(\min q'\leq v\). The minima are equal. This proves that the
RLT subtraction is valid for the desired lower bound, including
\(t=\tau\) where the hinges vanish.

After this step, either an explicit endpoint certificate has completed
the argument, or the updated coefficients satisfy (2) and \(b\leq0\).
We now reuse their original symbols.

## Removing the upper-end clipping

If \(K-b\leq2a\), no further correction is needed. Otherwise complement
the center and every leaf:

\[
s=1-t,\qquad z_i=1-y_i.
\]

The transformed coefficients are

\[
a^{\mathrm c}=a,\quad
b^{\mathrm c}=K-2a-b>0,\quad
c^{\mathrm c}=a+b+c+E-K,\quad
e_i^{\mathrm c}=k_i-e_i,\quad k_i^{\mathrm c}=k_i. \tag{6}
\]

The transformed leaves still satisfy (2). Apply the preceding lower-end
argument. If its endpoint branch applies, (4) in the complemented
coordinates is the required certificate and the proof is complete.

Otherwise it subtracts \(\sum_i\gamma_i s(1-z_i)\), with
\(\sum_i\gamma_i=b^{\mathrm c}\) and \(0\leq\gamma_i<e_i\).
The latter follows from
\(\gamma_i=(k_i-(k_i-e_i)/\tau)_+\) with \(\tau<1\).
In the original coordinates the subtraction is
\(\sum_i\gamma_i(1-t)y_i\). It changes

\[
e_i\longmapsto e_i-\gamma_i,
\qquad k_i\longmapsto k_i-\gamma_i,
\]

leaves \(a,b,c\) unchanged, and preserves the true minimum.
In particular \(b\leq0\) still holds, and

\[
K^{\mathrm{new}}=K-b^{\mathrm c}=2a+b.
\]

Thus the final polynomial, again written as (1), has the same minimum
\(v\) and satisfies

\[
b\leq0,\qquad K-b\leq2a,\qquad k_i\geq0. \tag{7}
\]

The initial polynomial equals this final polynomial plus a nonnegative
combination of RLT products, as well as any preceding fixed-leaf and
diagonal remainders.

## Completion of the proof of exactness

For every \(y\in\{0,1\}^m\), (7) puts the unconstrained center minimizer

\[
t_y=\frac{k^Ty-b}{2a}
\]

in \([0,1]\). Consequently its eliminated binary value is

\[
c+e^Ty-\frac{(b-k^Ty)^2}{4a}\geq v.
\]

Let \(r\) be the multilinear polynomial agreeing with that expression
at binary points:

\[
r(y)=c-\frac{b^2}{4a}
+\sum_i\left(e_i+\frac{bk_i}{2a}-\frac{k_i^2}{4a}\right)y_i
-\sum_{i<j}\frac{k_i k_j}{2a}y_i y_j. \tag{8}
\]

It is submodular, and every binary value is at least \(v\). The exact
polynomial identity is

\[
q(t,y)=
a\left(t+\frac{b-k^Ty}{2a}\right)^2+r(y)
+\sum_i\frac{k_i^2}{4a}y_i(1-y_i). \tag{9}
\]

At any SDP–RLT point, the square and diagonal remainders have
nonnegative evaluation. The submodular rounding fact gives
\(L_Y(r)\geq\min_{y\in\{0,1\}^m}r(y)\geq v\).
Thus \(L_Y(q)\geq v\). Adding back every correction and eliminated
remainder preserves this lower bound. A rank-one point from a true
minimizer attains \(v\), proving Theorem 2. \(\square\)

## Why the submodular objective needs only upper RLT

Here is a separate audit proving Proposition 3. If the original
center–leaf coefficients are nonpositive, the individual leaf
complementations preceding (1) are unnecessary. All other reductions
and estimates above use only PSD, means in \([0,1]\), and upper RLT:

- Nonpositive square coefficients contribute \(y_i(1-y_i)\), or
  \(t(1-t)\) when \(a\leq0\). These have nonnegative linearized
  values by the diagonal upper bounds.
- Eliminating a fixed-sign leaf uses unary literals and
  \(t(1-y_i)\) or \((1-t)y_i\). The lower-end correction (5),
  its upper-end counterpart, and the endpoint certificate (4) use
  exactly these same types of products.
- The rounding inequality for a submodular multilinear polynomial
  uses only \(X_{ij}\leq\min(\mu_i,\mu_j)\). This covers both
  the \(a\leq0\) branch and the residual polynomial (8).
- PSD makes the affine square in (9) nonnegative. Its remaining
  diagonal terms again use only diagonal upper bounds.

The only further transformation is the simultaneous complementation
of the center and **all** remaining leaves in (6). This preserves the
weaker region. In fact, with

\[
\mu_i'=1-\mu_i,\qquad
X_{ij}'=1-\mu_i-\mu_j+X_{ij},
\]

one has \(\mu_i'-X_{ij}'=\mu_j-X_{ij}\) and
\(\mu_j'-X_{ij}'=\mu_i-X_{ij}\), including \(i=j\).
The corresponding affine congruence preserves PSD. Thus every step of
the proof remains valid under upper RLT alone. \(\square\)

Individual variable complementation does not preserve upper RLT in
general. Indeed, even the one-leaf upper-only region is too large for
the arbitrary-sign moment hull. Set

\[
\mu_t=\mu_y=\tfrac14,\qquad
X_{tt}=X_{yy}=\tfrac14,\qquad X_{ty}=-\tfrac1{16}.
\]

All upper bounds hold, including binary diagonal equalities. The Schur
complement of the constant entry is
\(\frac1{16}\left(\begin{smallmatrix}3&-2\\-2&3\end{smallmatrix}\right)\),
with positive eigenvalues \(1/16,5/16\). Hence the moment matrix is
positive definite. But the box-nonnegative objective \(ty\) has
relaxed value \(-1/16\). This explicitly separates Proposition 3
from the full-RLT hull claim.

## Proof of the moment-hull statement

Every point defining \(H_m\) has a rank-one moment lift in the stated
face, so one inclusion is immediate. Both the face and its projection
are compact: means are bounded, RLT bounds all entries of \(X\), and
the constraints are closed. The hull \(H_m\) is compact as well.

An arbitrary affine functional of the retained coordinates is the
linearization of (1) with arbitrary center coefficient and arbitrary
interaction signs. Its minimum over the continuous box equals its
minimum with binary leaves, because every leaf appears affinely.
Theorem 2 therefore gives exactness over the full SDP–RLT region and
hence over its binary-leaf face. The latter contains a rank-one
minimizer with binary leaves. Thus the projection and \(H_m\) have the
same minimum for every affine functional. Separation of compact convex
sets proves their equality. \(\square\)

## Literature comparison and limits of the contribution

The established ingredient is exact McCormick minimization of a
submodular binary quadratic. Padberg's 1989
[*The Boolean Quadric Polytope: Some Characteristics, Facets and
Relatives*](https://doi.org/10.1007/BF01589101), Section 6, Proposition 9,
covers the equivalent maximization of a multilinear quadratic with
nonnegative mixed coefficients. The local full text was inspected at
that proposition. The common-uniform proof above makes this ingredient
self-contained.

Burer, Natarajan, and Willemsen,
[*On the Semidefinite Representability of Continuous Quadratic
Submodular Minimization With Applications to Pricing and Moment
Problems*, arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3), prove
submodular exactness in at most three variables. Their Proposition 4
also gives exactness when all diagonal moment inequalities are active,
or when all pairwise upper bounds are active and at most one diagonal
inequality is inactive. Theorem 1 here has one potentially inactive
diagonal but does not assume that every pairwise upper bound is active;
it only asserts equality after projecting away leaf–leaf moments.
Proposition 3 applies in arbitrary dimension to the submodular star
subclass using the same PSD-plus-upper-RLT type of relaxation.

Qiu and Yıldırım,
[*On Exact and Inexact RLT and SDP–RLT Relaxations of Quadratic Programs
with Box Constraints*](https://arxiv.org/abs/2303.06761), provide general
algebraic exactness criteria. The local paper and its abstract were
examined for relevant structure. This note constructs certificates for
a particular structural class; it does not replace their general
criteria.

The candidate additional content is the pair of explicit threshold
corrections (5)–(6), which extend the immediate completion-of-squares
argument to arbitrary center clipping, and the resulting arbitrary-size
mixed binary star projection. Searches for combinations of
“SDP–RLT”, “one positive diagonal”, “one continuous variable”, “binary
variables”, and “convex hull” did not locate an equivalent theorem.
That search was limited and does not establish novelty. In particular,
the mixed binary moment hull, mixing-set, and common-factor covariance
literature still require a deeper comparison.

The scalar objective (3) is already easy to minimize by sorting its
breakpoints and minimizing a quadratic on each interval. The theorem
therefore does not establish new polynomial-time solvability of this
objective class. Its potential value is an exact semidefinite
representation of the retained moments and a certificate for the
existing relaxation. Such a representation could strengthen local
blocks in larger MINLP relaxations. Intersecting this hull with other
constraints does not automatically produce the hull of the constrained
problem, and no computational speedup is established here.

The proof uses dense leaf–leaf auxiliary products in (8) and the full
PSD matrix in (9). It does not show that separate three-by-three
center–leaf PSD constraints suffice. It also does not allow positive
leaf square coefficients or arbitrary interactions among leaves.

## Leaf–leaf RLT constraints cannot simply be dropped

A reviewer supplied the following exact limitation. On \([0,1]^3\),
let

\[
q=t^2-\frac t2+\frac1{16}+\frac5{64}y_1+\frac7{64}y_2
-\frac14t(y_1+y_2).
\]

Its minimum is zero, attained at \((t,y_1,y_2)=(1/4,0,0)\), as certified
by

\[
q=\left(t-\frac14-\frac{y_1+y_2}{8}\right)^2
+\frac{y_1(1-y_1)+y_2(1-y_2)}{64}
+\frac{y_2(1-y_1)}{32}.
\]

Construct a moment matrix as the Gram matrix of the vectors

\[
v_0=(1,0),\quad v_t=(3/8,1/10),\quad
v_1=(4/5,2/5),\quad v_2=(1/5,2/5).
\]

The Gram representation proves PSD. Direct rational calculation verifies
every diagonal and center–leaf RLT inequality, including the binary-leaf
diagonal equalities. Its objective is \(-3/800\). The missing leaf–leaf
upper bound fails:
\(X_{12}=8/25>1/5=\mu_2\).
Thus retaining the full PSD matrix while keeping only star-edge and
diagonal RLT constraints is insufficient, already with two leaves.

## Verification record

The parent investigator `/root/frontier_cube/four_star_route` independently
checked the two threshold corrections, endpoint identity, complement
transformation, and final square decomposition before this note was
written, and then checked the saved proof and all boundary cases.
`/root/frontier_cube` separately read the complete saved proof and checked
preprocessing equalities, empty-leaf cases, the endpoint repairs, square
identity, and projection argument without finding a defect. The fresh reviewer
`/root/frontier_cube/four_star_route/four_star_bound_bridge/binary_waterfill_review`
then checked the whole proof, boundary cases, saved note, and moment-hull
corollary. That reviewer independently developed the sparse-RLT
counterexample above and checked it with exact rational arithmetic.
The separate reviewer
`/root/frontier_cube/four_star_route/four_star_bound_bridge/binary_waterfill_review/upper_waterfill_check`
checked the upper-end correction and found no gap. These are independent
checks, not a formal proof or a priority determination.

The author and `/root/frontier_cube/four_star_route` each ran

```text
python research-20260927/check_binary_leaf_star.py
```

All checks passed. The script uses exact SymPy or rational arithmetic
for general three-leaf endpoint and square identities; seven examples
covering absent, lower, upper, double, and endpoint clipping corrections;
the empty-leaf cases; and the sparse-RLT certificate, Gram feasibility,
and negative objective. It also checks the upper-RLT transformation
under simultaneous complementation and the exact one-leaf obstruction
to an arbitrary-sign upper-only hull claim. It does not verify the universal analytic
argument, compact-convex separation, or novelty. No project-wide
verification or CI inspection was performed.

The parent investigator proposed Proposition 3, and the author then
audited it separately, step by step. Its proof enumerates the constraints
used at each step, rather than inferring the weaker claim from full-RLT
exactness.
