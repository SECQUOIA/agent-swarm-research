# Exact certificates for convex quadratic optimization at fixed Hessian span

Date: 2026-09-27. Status: certificate corollary with a complete proof;
[independent adversarial review](algebraic-certificate-proof-review.md)
found no mathematical gap after two wording corrections. A
[prior-art audit](algebraic-certificate-prior.md) identifies the classical
certificate mechanisms; publication priority for the parameter-sensitive
encoding remains unestablished. This note does not claim a new
alternative theorem, a new facial-reduction principle, or a new complexity
class inclusion.

The exact optimization results in this directory initially describe an
optimizer by separate coordinate polynomials and root intervals. This note
gives an independently checkable certificate of feasibility and optimality
in one real number field. A sequence of at most `h` curved facial reductions
handles failure of Slater's condition, where `h` is the span dimension of
the native constraint Hessians. Every multiplier stays in the field of the
selected primal optimizer. A separate positive-aggregate certificate handles
infeasibility.

The mechanisms are classical. The addition is an explicit connection
between their algebraic encoding size and the Hessian-span parameter,
together with a verifier that does not have to repeat quantifier elimination
or an optimization algorithm. These certificates concern continuous convex
quadratic programs. Applying one on an integer slice certifies that slice;
it does not certify global mixed-integer optimality.

## 1. Statement

Write the rational input as

\[
 F=\{x\in P:q_i(x)\le0\ (i=1,\ldots,m)\},\qquad
 P=\{x:Ax\le b\},\qquad
 q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
\]

with every \(Q_i\succeq0\). Equalities are encoded by their two opposite
inequalities. Let \(N\ge2\) be the explicit binary input length and

\[
 h=\dim_{\mathbb Q}\operatorname{span}\{Q_1,\ldots,Q_m\}.
\]

Write
\[
 \mathcal B(n,h)=\max_{0\le s\le\min(h,n)}2^s\binom ns.
\]

The objective \(q_0\) is rational and convex, but its Hessian need not
belong to this span and does not enter `h`.

**Certificate theorem.** If \(F\ne\varnothing\) and the objective has
a finite optimum, let \(x^*\) be its unique minimum-norm optimizer. There
is a certificate of its feasibility and global optimality with the following
properties.

1. All primal coordinates, multipliers, and facial equations belong to the
   single real number field
   \[
   K=\mathbb Q(x_1^*,\ldots,x_n^*),\qquad
   D=[K:\mathbb Q]\le\mathcal B(n,h).              \tag{1}
   \]
2. At most `h` curved exposing combinations are followed by one final KKT
   certificate. Each exposing combination uses at most \(n+1\) nonzero
   native and polyhedral multipliers in total. The final KKT certificate
   uses at most \(n\) in total.
3. A primitive integer polynomial for a generator of `K`, a rational interval
   selecting its intended real root, and rational polynomial expressions
   for every field element have total encoding length \(N^{O(h+1)}\).
   A deterministic verifier runs in time polynomial in this encoding length
   and the input length.

If `F` is nonempty, the same field representation of its canonical feasible
point alone is a feasibility certificate with (1). If `F` is empty, there is
an infeasibility certificate of length \(N^{O(h+1)}\). When `P` is
nonempty it can be chosen in a real field of degree at most

\[
                         \mathcal B(n+1,h),         \tag{2}
\]

using one positive convex quadratic aggregate and at most \(n+1\)
nonzero multipliers. When `P` is empty, a rational linear Farkas certificate
suffices.

These are certificate-size and verification statements. The constructive
conversion of the existing optimizer output into the one-field format is
[treated separately](constructive-common-field-recovery.md). A polynomial
construction of all facial multipliers is not proved in this note.
No certificate of unboundedness is asserted here, and
no rational feasible-point or rational-multiplier promise is imposed.

The field degree and coordinate-height inputs to this theorem are the
[ordered-perturbation optimizer theorem](ordered-perturbation-optimizer.md)
and its [sharper degree refinement](multihomogeneous-span-degree.md).
The height argument below uses the common-field encoding lemma in
[the quantitative Hölder note](hessian-span-holder-height-review.md).
The geometric reduction is related to that in
[the qualitative Hölder proof](hessian-span-holder-geometry.md), but its
certificate form admits a useful simplification: all native tangents can
be added at the start.

## 2. A certificate format that needs no affine-hull test

The certificate first supplies the point \(x^*\) in one field, and the
verifier checks every original primal constraint. Define

\[
 \ell_i(x)=q_i(x^*)+\nabla q_i(x^*)^T(x-x^*),\qquad
 P_0=P\cap\{x:\ell_i(x)\le0\text{ for every }i\}.   \tag{3}
\]

Convexity gives \(q_i(x)\ge\ell_i(x)\) everywhere. Consequently
\(F\subseteq P_0\), and adding these tangents does not remove any
original feasible point. All original quadratics are retained. Tangent
validity needs no calculation of the affine hull of `P` or of `F`.

Suppose the current polyhedron is \(P_j=\{x:A_jx\le b_j\}\).
One exposing record consists of vectors \(\lambda\ge0\) and
\(\mu\ge0\) satisfying

\[
 \sum_i\lambda_i=1,\qquad
 \lambda_iq_i(x^*)=0,\qquad
 \mu_r((A_jx^*)_r-(b_j)_r)=0,                       \tag{4}
\]
\[
 \sum_i\lambda_i\nabla q_i(x^*)+A_j^T\mu=0.       \tag{5}
\]

Define, from these supplied data,

\[
 g_j=\sum_i\lambda_iq_i,\qquad
 H_j=\sum_i\lambda_iQ_i,\qquad
 v_j=\nabla g_j(x^*).
\]

The next polyhedron is exactly

\[
 P_{j+1}=P_j\cap
 \{x:H_j(x-x^*)=0,\ v_j^T(x-x^*)=0\}.             \tag{6}
\]

As before, store these equations as opposite inequalities. The coefficients
of (6) can be supplied explicitly and checked against their defining
identities. The verifier need not determine whether this record reduces
the affine dimension or the Hessian span. Those properties establish the
existence of a short certificate; they are unnecessary for its soundness.
The set in (6) is a polyhedral minimizer section, not necessarily a face
of \(P_j\): minimizing \(x^2\) over \(\mathbb R\) gives \(\{0\}\).
The facial-reduction terminology refers to the constraint reduction and its
usual conic interpretation, not to a claim that every section is a
polyhedral face.

Indeed, for \(d=x-x^*\) and \(x\in P_j\), (4)--(5) give

\[
 g_j(x)=\tfrac12d^TH_jd+v_j^Td,
 \qquad
 v_j^Td=\sum_r\mu_r((b_j)_r-(A_jx)_r)\ge0.        \tag{7}
\]

Both terms in (7) are nonnegative. If also \(x\in F\), the
nonnegative combination of native inequalities gives \(g_j(x)\le0\).
Both terms therefore vanish. Since \(H_j\succeq0\),
\(d^TH_jd=0\) implies \(H_jd=0\). Thus

\[
                  F\subseteq P_j\Longrightarrow F\subseteq P_{j+1}.
                                                               \tag{8}
\]

In particular, every record preserves all original feasible points.
Complementarity with the native rows in (4) matters: stationarity and
normalization alone would not imply \(g_j(x^*)=0\).

## 3. The final optimality record

After the exposing records, let the final polyhedron be
\(P_t=\{x:A_tx\le b_t\}\). Supply \(\lambda\ge0\) and
\(\mu\ge0\) satisfying

\[
 \nabla q_0(x^*)+\sum_i\lambda_i\nabla q_i(x^*)
                                  +A_t^T\mu=0,     \tag{9}
\]
\[
 \lambda_iq_i(x^*)=0,\qquad
 \mu_r((A_tx^*)_r-(b_t)_r)=0.                       \tag{10}
\]

There is no normalization of `lambda` in this last record. Let
\(\theta=q_0(x^*)\) and \(H=Q_0+\sum_i\lambda_iQ_i\succeq0\).
An exact quadratic identity is

\[
 q_0(x)-\theta
 =\tfrac12(x-x^*)^TH(x-x^*)-\sum_i\lambda_iq_i(x)
                  +\sum_r\mu_r((b_t)_r-(A_tx)_r).  \tag{11}
\]

Equations (9)--(10) prove (11) by expansion. Every term on its right is
nonnegative for \(x\in F\subseteq P_t\). Thus the feasible point
\(x^*\) is globally optimal. This is the complete soundness proof.
The verifier does not check a constraint qualification, minimality of the
point's norm, or completeness of the exposing sequence. A valid final
identity already certifies what is needed.

## 4. Why at most `h` exposures suffice in one field

For existence, use the actual canonical optimizer as \(x^*\). At a
current polyhedron \(P_j\), let `I` contain exactly those native rows
whose Hessians are nonzero after restriction to the direction space of
\(\operatorname{aff}P_j\). Every other native row agrees with its
tangent in (3) throughout \(P_j\), by the quadratic Taylor identity.
It is therefore already enforced by the polyhedron.

If the rows indexed by `I` have a common strictly feasible point in
\(P_j\), they satisfy relative Slater. A strict point can be moved
slightly towards any point of \(\operatorname{ri}P_j\) while preserving
strictness, which supplies the usual relative-interior version of the
condition. Convex KKT then gives (9)--(10), with zero native multipliers
outside `I`. If `I` is empty, polyhedral first-order optimality gives the
same conclusion directly.

Otherwise the convex alternative supplies a normalized nonnegative
combination of the rows in `I` with

\[
                       g(x)=\sum_{i\in I}\lambda_iq_i(x)\ge0
                       \quad(x\in P_j).            \tag{12}
\]

Because \(x^*\in F\), it minimizes `g` with value zero. Consequently
positive native weights are supported only on rows active at \(x^*\),
and polyhedral first-order optimality gives (5) with active polyhedral
normals. These are linear equations in the multipliers over
\(K=\mathbb Q(x^*)\), together with nonnegativity and the normalization
in (4). Restrict the variables to the native active rows in `I` and the
polyhedral active rows. A feasible solution of minimum positive support has
linearly independent columns in this linear system. It has at most
\(n+1\) positive entries, and a nonsingular subsystem expresses them
by Cramer's rule over `K`.

Replacing the original real multipliers by this basic solution preserves
all of (4)--(5). The restricted Hessian
\(H_j=\sum_{i\in I}\lambda_iQ_i\) is nonzero: it is a normalized
positive combination of nonzero positive semidefinite restricted Hessians.
Every direction of the new affine hull in (6) lies in its kernel. Therefore
the dimension of the restricted native Hessian span falls by at least one.
There can be at most `h` such curved records.

At the terminal KKT system, restrict multiplier variables to active rows.
The same minimum-support argument applies to its `n` stationarity equations,
with no normalization equation. It gives at most `n` positive multipliers,
again in `K`. Encoding equality rows as opposite inequalities avoids any
separate issue with unrestricted-sign multipliers.

All arguments take place in the original coordinates. There is no sequence
of unrelated algebraic exposing points and no successive extension of the
number field. The unknown affine hull is used only in this existence
argument, not in the certificate format or its verifier.

## 5. Encoding size and verification

By the ordered-perturbation theorem, the field degree satisfies (1), and
every coordinate of \(x^*\) has absolute logarithmic height at most
\(B_*=N^{O(h+1)}\). The same bound holds for every original tangent
coefficient and gradient evaluated at \(x^*\).

For completeness, the needed elementary height estimates are

\[
 H(uv)\le H(u)+H(v),\quad H(u^{-1})=H(u),\quad
 H(u+v)\le H(u)+H(v)+\log2,
\]

and, for an \(r\times r\) matrix with entry heights at most `B`,

\[
                  H(\det M)\le r^3B+\log(r!).      \tag{13}
\]

The determinant bound follows by applying the triangle inequality at each
archimedean place, the ultrametric inequality at the other places, and the
definition of absolute height. It avoids an exponential sum of separate
heights for determinant terms. These estimates are expanded in the
quantitative Hölder note.

If the current polyhedron has coefficient heights at most \(B_j\),
Cramer's rule in the basic multiplier system bounds the next multipliers
and face coefficients by

\[
                 N^{O(1)}(B_j+B_*+1).              \tag{14}
\]

There are at most `h` such arithmetic rounds. Absolute heights, rather
than repeatedly expanded power-basis coefficients, are tracked throughout
these rounds; there is no factor of the field degree at each round.
Thus every certificate
element has height \(N^{O(h+1)}\). The polyhedral row count is bounded
by the original count plus `m` tangents and \(2h(n+1)\) facial rows.

Choose a primitive generator \(\alpha\) as a short integer linear
combination of the coordinates, as in
[the witness-recovery argument](algebraic-witness-recovery.md). Its height
and minimal-polynomial coefficient bit lengths are \(N^{O(h+1)}\).
Each certificate element \(\beta\in K\) has a unique expression

\[
                   \beta=\sum_{r=0}^{D-1}c_r\alpha^r,
                   \qquad c_r\in\mathbb Q.        \tag{15}
\]

The common-field encoding lemma applies Cramer's rule to the Vandermonde
system over all embeddings of `K`. Absolute height is independent of the
chosen ambient number field, so use of a normal closure does not introduce
its possibly large degree. It gives

\[
 H(c_r)\le D^{O(1)}(H(\alpha)+H(\beta)+1).
\]

For rational \(c_r\), this bounds numerator and denominator bit lengths.
An isolating interval for the intended real root has polynomial bit length
in the generator polynomial's degree and coefficient bits. Together these
bounds prove the claimed total length.

The verifier performs rational polynomial arithmetic modulo the generator
polynomial and exact sign determination at its isolated real root. It
checks original primal feasibility, the definitions of all tangents and
face coefficients, multiplier signs, all identities (4)--(6), and the
final stationarity and complementarity equations. Input positive
semidefiniteness can also be checked by exact rational linear algebra.
Univariate root counting and sign determination have polynomial bit cost
in the degrees and coefficient lengths. If desired, the verifier may
accept a squarefree defining polynomial instead of checking its
irreducibility: requiring the displayed identities to vanish modulo that
polynomial is still sound at its selected root. The certificates constructed
above use the primitive minimal polynomial.

Supplying each face's coefficients explicitly and checking their local
defining identities keeps all verification calculations polynomial in the
stated certificate length. No multivariate real-root selection problem is
hidden in the format. In contrast, unrelated coordinate isolators alone
would not justify this verification claim.

## 6. Infeasibility needs only one positive aggregate

If the rational polyhedron `P` is empty, linear Farkas multipliers give a
rational certificate of polynomial bit length. Suppose `P` is nonempty and
the native system is infeasible. Necessarily \(m>0\). Consider

\[
        \alpha=\min_{x\in P}\max_iq_i(x)
        =\min\{t:x\in P,\ q_i(x)-t\le0\text{ for all }i\}.   \tag{16}
\]

All values of the maximum are positive, so its infimum is nonnegative and
finite. Classical attainment for convex quadratic inequality systems
applies to the epigraph problem. It therefore has an optimizer and
\(\alpha>0\); otherwise an attained value zero would give a feasible
point of the original system.

Choose its canonical optimizer \((\bar x,\alpha)\). The native
epigraph Hessians are \(\operatorname{diag}(Q_i,0)\), whose span still
has dimension `h`. The ordered-perturbation theorem in dimension \(n+1\)
gives the degree bound (2) and heights \(N^{O(h+1)}\).

The epigraph constraints have a common strict point relative to `P`: choose
any \(x\in\operatorname{ri}P\) and then take `t` sufficiently large. Consequently
ordinary convex KKT gives

\[
 \lambda_i\ge0,\quad\mu_r\ge0,\quad\sum_i\lambda_i=1,
 \quad\sum_i\lambda_i\nabla q_i(\bar x)+A^T\mu=0,             \tag{17}
\]
\[
 \bar x\in P,\quad q_i(\bar x)\le\alpha,\quad
 \lambda_i(q_i(\bar x)-\alpha)=0,\quad
 \mu_r((A\bar x)_r-b_r)=0.                         \tag{18}
\]

As before, a basic solution of the active multiplier system has at most
\(n+1\) positive entries and belongs to
\(K'=\mathbb Q(\bar x,\alpha)\), with the same height order. The
certificate consists of these data and the strict inequality
\(\alpha>0\). For every \(x\in P\), it certifies

\[
 \sum_i\lambda_iq_i(x)
 =\alpha+\tfrac12(x-\bar x)^T
                   \Bigl(\sum_i\lambda_iQ_i\Bigr)(x-\bar x)
                   +\sum_r\mu_r(b_r-(Ax)_r)
 \ge\alpha>0.                                      \tag{19}
\]

A feasible point would make the left side nonpositive, a contradiction.
The same field encoding and sign verifier as above applies. No facial
reductions are needed for this epigraph certificate.

The support count cannot be bounded in terms of `h` alone. For \(n\ge2\),
take \(P=\mathbb R^n\) and
\[
 q_i(x)=\|x-e_i\|^2-\frac{n-2}{n-1}\qquad(i=1,\ldots,n).
\]
All Hessians equal \(2I\), so \(h=1\). Their average equals
\(\|x-\mathbf1/n\|^2+(n-1)/n-(n-2)/(n-1)>0\), proving
infeasibility. Every proper subfamily is feasible: at the average of its
`s` centers, all its squared distances are \((s-1)/s\), which is at
most \((n-2)/(n-1)\). A positive aggregate must therefore use all
`n` native rows. Hessian span bounds the number of curved reductions,
not the support of every aggregate.

The [rational refinement](rational-infeasibility-certificates.md) strengthens
this infeasibility branch: the weights, stationary point, and positive
constant can all be rational with total length \(N^{O(h+1)}\).
It preserves the common rational kernel while rounding the positive weights.
The field certificate above supplies the quantitative starting point.

The positive-aggregate conclusion is already contained in
[Jeyakumar--Li's Theorem 2.5 for SOS-convex inequalities](https://web.maths.unsw.edu.au/~gyli/papers/jl-zero-sum-final-18-07-13.pdf).
It is recorded here to
make the parameter-sensitive encoding and verification statement complete,
not as a new infeasibility theorem. General semidefinite programs can lack
rational separating certificates; the linked rational conversion uses the
native PSD-quadratic structure explicitly.

## 7. Added capability and limitations

This format lets a checker verify an exact irrational optimizer and its
global continuous optimality using only one-variable algebraic arithmetic
and quadratic identities. It addresses systems with no rational feasible
point and no ordinary KKT multipliers in the original formulation. The
number of curved reductions is bounded by Hessian span, and using one
primal field prevents field-degree growth across reductions.

The exact decision and optimization algorithms already establish polynomial
time for fixed `h`. The certificate theorem does not strengthen that
complexity classification. It supplies a more transparent output contract
for independently checked exact solutions. The separate common-field
construction completes the primal output representation in polynomial time
for fixed `h`. Practical use still requires extraction of the facial
multipliers and an implementation of exact sign checking. The estimates are asymptotic and
do not predict useful numerical sizes.

The supporting mechanisms include convex alternatives, facial reduction,
polyhedral normal cones, and KKT certificates. The
[prior-art audit](algebraic-certificate-prior.md) compares these with
Ramana, Pataki, Liu--Pataki, and Klep--Schweighofer extended certificates,
and with the stronger SOS-convex alternative of Jeyakumar--Li. Those results
already establish the real-certificate mechanisms used here. Priority for
the combined field-degree, coefficient-size, and Hessian-span statement is
not established by the current source search.

Verification of this universal theorem is by complete symbolic proof review,
with a separate focused audit of the infeasibility branch. The reviews
checked exact singular-chain and identical-Hessian support examples. No
numerical experiment, Lean formalization, project-wide check, or CI
inspection is asserted.
