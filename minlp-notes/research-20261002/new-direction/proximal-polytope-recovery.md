# Exact mixed-polytope QP with an arbitrary optimal set

Date: 2026-10-02. Status: derivation passed a
[fresh independent review](../reviews/polytope-recovery-review.md) and
targeted exact-rational checks. This combines the supplied-growth proximal
algorithm, fixed-domain Fenchel recourse, and a new general-polytope
recovery argument. No publication-priority or practical-performance claim
is made.

## 1. Result and the required promise

Let

\[
 \mathcal P=\{x\in\mathbb R^n:Mx\le d\},\qquad
 X=\mathcal P\cap(\mathbb Z^m\times\mathbb R^{n-m}),
 \qquad F(x)=\tfrac12x^TAx+b^Tx+c,
\]

where all data are rational, \(A\) is symmetric, \(\mathcal P\) is
bounded, and \(X\) is nonempty. Lower-dimensional polytopes and redundant
inequalities are allowed. The empty case can first be detected by the exact
convex-MIQP feasibility oracle. Put

\[
 f^*=\min_XF,\qquad S=\operatorname*{argmin}_X F.
\]

The compact set \(S\) may contain any number of discrete components and
continuous optimal faces. Supply a **valid rational** \(g_0>0\) with

\[
 F(x)-f^*\ge g_0\operatorname{dist}(x,S)^2
       \quad\text{for every }x\in X.                     \tag{1}
\]

Let \(k=n_-(A)\) and
\(\nu=\max\{0,-\lambda_{\min}(A)\}\). Under this promise, an exact
rational optimizer and exact value can be returned in

\[
 f\bigl(m,k,\max\{1,\nu/g_0\}\bigr)(I+1)^C            \tag{2}
\]

bit operations, for an absolute polynomial exponent. Here \(I\) includes
the supplied growth bound. Neither uniqueness nor finite optimal coordinate
projections are assumed. Approximation with an additive gap \(2^{-q}\)
has the corresponding bound with \(I+q+1\) in place of \(I+1\).
For \(k=0\), the existing exact convex-MIQP oracle suffices without (1).

The bound and global intervals **depend on the supplied promise**. The
algorithm does not verify (1), and a small reported interval is not a valid
stopping rule for an untrusted growth guess. This differs materially from
the [unique-projection theorem](negative-inertia-miqp.md), whose global
lower bounds are sound independently of its growth constant.

The new recovery lemma below applies to any rational quadratic on a bounded
mixed polytope. Negative inertia is used to obtain the sufficiently accurate
feasible point efficiently, not in the recovery proof.

Existence of some positive set-growth constant is classical in this setting.
[Luo and Sturm, Theorem 3.3](../../literature/papers/luo2000-error-bounds-for-quadratic-systems/paper.md)
(author manuscript pp. 11–12) proves a global square-root error bound for
the zero set of any quadratic on a polytope. Apply it to `F-f*` to obtain
growth toward the full optimal set on a continuous bounded polytope.
For the mixed case, boundedness leaves finitely many feasible integer
assignments. Apply the theorem on each globally optimal continuous slice.
Every other slice has a positive objective gap; dividing that gap by the
squared diameter bounds its growth toward the global optimal set. The
minimum of these finitely many positive constants gives some valid bound
in (1). This argument neither computes a useful bound nor validates a
supplied guess. The contribution here is the conditioned algorithm and
exact recovery, not qualitative existence of set growth.

## 2. Explicit arithmetic and slack thresholds

Assume \(n\ge1\); the zero-variable case is immediate. Let \(q_M\)
be the number of input inequalities and \(Q=\max\{1,q_M\}\).
Choose a positive integer common denominator \(D\) of all entries of
\(A,b,c,M,d\), and write

\[
 \bar A=DA,\quad\bar b=Db,\quad\bar M=DM,\quad\bar d=Dd.
\]

These matrices and vectors are integral. No row independence or row
normalization is required. Set

\[
 \begin{aligned}
 C_0&=\max\{1,\max_{ij}|\bar A_{ij}|,
                    \max_{ij}|\bar M_{ij}|\},\\
 R_0&=nC_0,\qquad Z_0=(nC_0)^n,\\
 C_1&=nC_0Z_0=(nC_0)^{n+1},\qquad H=(nC_1)^n,\\
 V&=2DH^2,\qquad
 \tau=\frac1{4QH},\qquad
 \delta=\frac\tau{2R_0}=\frac1{8QHR_0}.
 \end{aligned}                                                     \tag{3}
\]

All have polynomial binary length. In particular,
\(\|\bar M_i\|_2\le R_0\) for every row, and \(\delta<1\).
The numerical heights are not enumerated. Right-hand sides and linear
objective coefficients affect numerator sizes, but need not enter the
coefficient determinant bound \(H\).

At a feasible point \(y\in X\), select exactly the rows

\[
 J(y)=\{i:0\le\bar d_i-\bar M_i y\le\tau\}.            \tag{4}
\]

Fix the integer coordinates to \(z=y_{1:m}\), and impose the selected
rows as equalities. Solve the following **linear feasibility problem**:

\[
 \begin{aligned}
 \bar Mx&\le\bar d,& x_{1:m}&=z,&
 \bar M_{J(y)}x&=\bar d_{J(y)},\\
 \bar Ax+\bar b
   &=\bar M_{J(y)}^T\lambda+E_m^T\mu.
 \end{aligned}                                                     \tag{5}
\]

Here \(E_mx=x_{1:m}\), and \(\lambda,\mu\) are **unrestricted**
real multipliers. Equation (5) expresses stationarity along the selected
face's affine hull. It is not a KKT system requiring nonnegative multipliers.
The original mixed constraints are satisfied because all integer coordinates
are fixed to the known integer tuple \(z\).

**Recovery lemma.** If \(\operatorname{dist}(y,S)\le\delta\),
then (5) is feasible, and every feasible \(x\) in (5) is a global
optimizer. A rational solution can be obtained in polynomial bit time.

## 3. A bounded stationary polytope for analysis

Choose a nearest optimizer \(s\in S\). Since \(\delta<1\), its
integer tuple equals \(z\). Let \(J_0\) be all inequality rows active
at \(s\). From these rows and the integer-fixing unit rows, choose a
linearly independent row basis \(E\). Its right-hand side \(e\) is
integral: entries come from \(\bar d\) and \(z\). All its
coefficients have magnitude at most \(C_0\).
Because the full equation set is consistent at \(s\), \(Ex=e\)
implies every original active equality and every integer-fixing equality,
including those omitted from the independent basis.

Write \(r=\operatorname{rank}(E)\). There is an integer matrix \(Z\)
whose columns form a basis of \(\ker E\), with entries bounded by
\(Z_0\). To see this, choose an invertible \(r\)-column submatrix
\(E_K\). For each nonpivot column, use its replaced-column determinants
to form the usual null vector, with free entry \(\det E_K\).
Every entry is bounded by \(r!C_0^r\le(nC_0)^n\). When \(r=0\),
take \(Z=I\); when \(r=n\), there are no columns or stationarity
equations.

Every direction in \(\ker E\) admits both signs of sufficiently small
feasible displacement from \(s\) in its continuous slice: active rows
are preserved, while the finitely many inactive rows have positive slacks.
First-order optimality therefore gives
\(Z^T(\bar As+\bar b)=0\). Define the analysis-only polytope

\[
 P_s=\{x:\bar Mx\le\bar d,\ Ex=e,
                  Z^T(\bar Ax+\bar b)=0\}.              \tag{6}
\]

It is nonempty and bounded. It is an \(x\)-space polytope; no assertion
about vertices of an unbounded multiplier lift is used. Redundant active
rows have already been removed from the basis \(E\).

Every point in \(P_s\) is optimal. For \(x\in P_s\), the vector
\(v=x-s\) lies in \(\ker E\). Both stationary gradients are
orthogonal to that kernel, so

\[
 (As+b)^Tv=0,\qquad v^TAv=0,
 \qquad F(x)-F(s)=(As+b)^Tv+\tfrac12v^TAv=0.             \tag{7}
\]

This argument needs neither a nonsingular Hessian nor isolated optima.

Every defining row of (6) has integer coefficients of magnitude at most
\(C_1\): for a stationarity row use
\(|(Z^T\bar A)_{ij}|\le nZ_0C_0\). Its right-hand side is also
integer. A vertex of this nonempty bounded polytope is determined by
\(n\) independent equality or active-inequality rows, including in the
lower-dimensional case. Their nonzero determinant has magnitude at most
\(n!C_1^n\le H\). Thus every such vertex has one common coordinate
denominator at most \(H\).

This also proves a global height bound: choosing any optimizer \(s\)
and then any vertex of \(P_s\) gives a rational global optimizer with
common denominator at most \(H\). Substitution into \(F\) shows that
the reduced denominator of \(f^*\) is at most \(V=2DH^2\).

## 4. Simultaneous snapping and recovery

Every true active row is selected. Indeed, for \(i\in J_0\),

\[
 0\le\bar d_i-\bar M_i y
       \le R_0\|y-s\|\le R_0\delta=\tau/2.
\]

Extra rows in \(J(y)\setminus J_0\) can be close without being active
at \(s\). Define the nonnegative linear functional on \(P_s\)

\[
 q_s(x)=\sum_{i\in J(y)\setminus J_0}
                           (\bar d_i-\bar M_ix).
\]

Each extra row has slack at \(s\) at most
\(\tau+R_0\delta=3\tau/2\). Hence

\[
 0\le q_s(s)\le\frac{3Q\tau}{2}
                   =\frac3{8H}<\frac1H.                 \tag{8}
\]

The functional has integer coefficients and constant term. It attains its
minimum over \(P_s\) at a vertex. If that minimum were positive, the
common denominator bound above would make it at least \(1/H\),
contradicting (8). Therefore its minimum is zero. Nonnegative individual
slacks then give an optimizer \(s'\in P_s\) satisfying **all**
selected equalities simultaneously.

The normal space spanned by \(E\) is contained in the span of the
selected rows and integer-fixing rows. Thus \(s'\) satisfies (5),
establishing feasibility. For any other solution \(x\), put \(v=x-s'\).
The equality constraints make \(v\) orthogonal to that selected normal
space. Both gradients belong to the same space, so their difference
\(Av\) does too. Therefore
\((As'+b)^Tv=v^TAv=0\), and the quadratic expansion gives
\(F(x)=F(s')=f^*\).

Zero or duplicate rows do not affect this argument. Constant positive
integer slacks cannot be accidentally selected since \(\tau<1\);
identically zero rows merely add redundant equalities. The final LP may
retain all redundant rows and have nonunique multipliers. Only the
analysis height argument used an independent basis. General rational
linear feasibility supplies a polynomial-height rational solution even
if the multiplier variables have lineality.

## 5. Obtaining the nearby point without choosing an optimal component

For \(k>0\), use the reviewed
[rational spectral normalization](spectral-normalization.md) to construct

\[
 A=P-\alpha T^TT,\quad P\succeq0,\quad\|T\|_2\le1,
 \quad T\in\mathbb Q^{k\times n},\quad
 2\nu\le\alpha<4\nu.
\]

The exact convex-MIQP oracle from the
[mixed Fenchel theorem](negative-inertia-miqp.md) evaluates

\[
 W(a)=\min_{x\in X}\left[F(x)+\tfrac\alpha2\|a-Tx\|^2\right]
\]

and returns an attaining original mixed-feasible witness \(x_a\).
It has upper coordinate curvature \(L_W=\alpha\), even though it
need not be quadratic or differentiable. Its optimal set is exactly
\(S_W=TS\), which is compact and may be arbitrary.

For every \(a,x\),
\(\operatorname{dist}(a,TS)\le\|a-Tx\|+
\operatorname{dist}(x,S)\). The same scalar-square calculation as in
the pointwise Fenchel theorem transfers (1) to

\[
 W(a)-f^*\ge g_W\operatorname{dist}(a,TS)^2,\qquad
 g_W=\frac{g_0\alpha}{2g_0+\alpha},\qquad
 \kappa_W=\frac\alpha{g_W}=2+\frac\alpha{g_0}
                       <2+\frac{4\nu}{g_0}.              \tag{9}
\]

Bound each coordinate of \(Tx\) by rational LP over \(\mathcal P\),
and work on their product box. Constant ranges can be removed. If every
range is constant, one inner solve is already exact. Otherwise apply
[the proximal growth-grid theorem](proximal-growth-grid.md) to \(W\)
on this continuous auxiliary box, with the supplied valid \(g_W\).
Treat \(W\) as one factor in one bag of size at most \(k\); no
factorization of the value function is needed.

That algorithm returns an auxiliary point \(a\) and a promise-valid
interval \([\ell,W(a)]\) of any requested width \(\varepsilon\).
The associated witness \(y=x_a\) satisfies

\[
 \ell\le f^*\le F(y)\le W(a),\qquad
 \operatorname{dist}(y,S)^2\le\frac{\varepsilon}{g_0}.    \tag{10}
\]

Thus full-distance growth supplies a nearby point in the **original**
space, even when the auxiliary minimizers have a continuum of projections.
A projected-distance bound alone would not justify the original-space
recovery lemma.

Choose a dyadic \(\varepsilon\) satisfying

\[
 \varepsilon\le\min\{1,g_0\delta^2,1/(4V^2)\}.          \tag{11}
\]

Then (10) meets the recovery threshold. Reconstruct the unique rational of
denominator at most \(V\) in \([\ell,F(y)]\), obtaining \(\hat f\).
It equals \(f^*\) under the promise. Form (4), solve (5), and return a
rational solution only after checking original inequalities, integer
coordinates, and \(F(\hat x)=\hat f\). Under (1), feasibility and
equality are guaranteed. These final checks do not independently prove
that the supplied growth bound is valid.

## 6. Bit complexity and certification limits

The coordinate-denominator argument in the proximal theorem does not use
quadraticity of the objective. Its auxiliary centers are previous grid
points, and its fixed dyadic grading ratio and successive dyadic base
widths give a common grid-coordinate denominator whose bit length is
polynomial in input length, stage, and the parameter-dependent grid bound.

The value function \(W\) itself is not a rational quadratic. Its values
are instead computed by the exact convex-MIQP oracle on rational data of
that bounded length. Fixing an oracle-returned integer tuple and solving
its continuous convex slice, if needed, gives rational values and witnesses
of polynomial height in the node input. On the single auxiliary bag, the
algorithm compares these values plus the explicit unary corrections and
proximity term. It does not multiply denominators across a sequence of
oracle calls or form a large piecewise representation of \(W\).

There are only \(f(k,\kappa_W)\) grid values to inspect per stage, and
each exact inner call costs \(f_0(m)\) times a polynomial of absolute
degree in its rational input length. The accuracy (11) has
\(\log(1/\varepsilon)=\operatorname{poly}(I)\), with the supplied
rational \(g_0\) included. The proximal iteration count is polynomial
in this length and the original rational auxiliary-box scale. This proves
(2) and its approximation version.

For the final LP, only the selected row indices and the integer tuple are
taken from the approximate witness. Its large continuous denominators are
not inserted into the LP coefficients. Boundedness of the original
rational polytope bounds the integer tuple's encoding length uniformly.
All coefficients in (5) consequently have polynomial length in the
original input. A polynomial-height rational optimizer is returned.

The exact mixed oracle's global optimality is supplied by its existing
FPT algorithm, not by continuous KKT conditions. Separately, the global
interval from the proximal search uses (1) to keep an optimizer inside
each fresh restricted auxiliary box. Its finite grid calculations, face
stationarity LP, and final objective equality do not turn the result into
a growth-independent certificate. No unknown-growth restart or safe
stopping test for an invalid growth guess is claimed.

## Verification status

The [independent review](../reviews/polytope-recovery-review.md) found no
gap in the projected stationary polytope, integer null-basis height,
simultaneous slack snapping, unrestricted multipliers, or the integration
with a nonquadratic Fenchel value oracle. A second reviewer independently
checked the recovery algebra and thresholds.

The reviewer ran
`python research-20261002/new-direction/check_polytope_recovery_review.py`.
Its [exact recovery checker](check_polytope_recovery_review.py) passed
eight cases, checking thirteen stationary-polytope vertices, ten recovery
vertices, and four extra facet snaps. The cases include redundant and
zero rows, lower-dimensional feasible sets, disconnected optimal faces,
integer assignments, rational coupled constraints, and negative curvature
normal to the feasible affine hull. This small diagnostic enumerates
vertices; the proposed algorithm uses rational linear feasibility.

The command
`python research-20261002/new-direction/check_proximal_polytope_fenchel.py`
also passed. This [end-to-end diagnostic](check_proximal_polytope_fenchel.py)
uses one binary variable, three continuous variables, a coupled equality,
and redundant inequalities. Its optimum set consists of two disjoint
continuous segments. It checks the Fenchel identity, set-growth transfer,
optimizer containment, promise intervals, proximal contraction, and the
original-space recovery threshold at every stage. At the explicit height
threshold (616 accuracy bits), it completed 310 stages and 6,416 exact
recourse calls, with at most 21 grid nodes, and recovered the exact
optimizer \((0,1/3,2/3,0)\). Its two-mode recourse oracle and final
face solution are explicit formulas for this fixture, not implementations
of the general convex-MIQP oracle or rational LP algorithm.

Scoped whitespace, paired mathematical-delimiter, and local-link checks
passed for this note and the new diagnostic. No external search,
project-wide verification, or CI inspection was performed.
