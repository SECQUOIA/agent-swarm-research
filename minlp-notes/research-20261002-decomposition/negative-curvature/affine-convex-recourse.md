# Certified removal of stiff convex recourse

Date: 2026-10-02. Status: a scoped reduction and algorithm, with exact
diagnostic checks and independent review recorded below. The general sparse
negative-curvature problem remains open.

The useful positive result is the following: **large convex blocks can be
removed exactly before sparse global search when their optimal response has
a globally valid affine certificate.** The retained variables need not be
few, and the number of negative eigenvalues need not be bounded. The
certificate includes bound-active and singular convex blocks. Its validity
does not rely on growth or on numerical conditioning.

For a supplied partition into private blocks, whether such an affine
response exists can itself be decided in polynomial time, including
singular blocks. Section 5 gives the recognition procedure. The partition
and residual decomposition remain structural inputs.

The reduction is classical parametric-QP elimination. The implication for
the existing filtered-grid algorithm is stated explicitly because it removes
arbitrarily large positive curvature from a verifiable class of sparse
problems. It is not a new general Schur-complement theorem or a resolution
of the unrestricted negative-curvature target.

## 1. Model and the certificate

Retain a vector `z` in a rational product box `Z`. For each block `t`, let
`z_t=E_t z` select its attachment coordinates, and let its private variables
`y_t` lie in a rational product box `Y_t=[l_t,u_t]`. The private blocks are
disjoint. They have no mutual interactions except through `z`. Write

\[
 F(z,y)=q_0(z)+\sum_t f_t(y_t,z_t),\qquad
 f_t(y,z)=\tfrac12y^TC_ty+y^TD_tz+c_t^Ty
          +\tfrac12z^TA_tz+d_t^Tz+e_t.                 \tag{1}
\]

All matrices and vectors are rational; `C_t` and `A_t` are symmetric.
Assume `C_t` is positive semidefinite. The full Hessian of `F` need not be.
Fixed coordinates may be substituted first. The size of each private block
may grow with the input, and its positive curvature may be arbitrarily large.

An affine certificate for a block consists of

\[
 \bar y(z)=a+Bz,\qquad
 \ell(z)=r+Rz,\qquad u(z)=s+Sz,                       \tag{2}
\]

where `ell` and `u` are multipliers for the lower and upper bounds,
respectively. In this section `u(z)` denotes a multiplier, while the fixed
upper-bound vector is written `u_t`. Require, for every `z` in the attachment
box,

\[
 \begin{split}
 l_t\le\bar y(z)\le u_t,\quad \ell(z)\ge0,\quad u(z)\ge0,\\
 C_t\bar y(z)+D_tz+c_t=\ell(z)-u(z),\\
 \ell_i(z)(\bar y_i(z)-l_{t,i})=0,\qquad
 u_i(z)(u_{t,i}-\bar y_i(z))=0.                       \tag{3}
 \end{split}
\]

These conditions are checked in polynomial rational bit time. The range
of an affine form on a box is obtained by choosing each endpoint according
to the coefficient sign. Stationarity is an affine coefficient identity.
Complementarity is a quadratic coefficient identity after substituting
fixed attachment coordinates. A polynomial vanishing on a nondegenerate
box vanishes identically, so coefficient checks suffice. Exact rational
positive-semidefiniteness tests check `C_t`. Strict complementarity,
invertibility of `C_t`, and interiority of the response are not required.

This certificate is stronger than checking KKT conditions at a center or at
sampled parameters. Feasibility and signs must hold on the whole attachment
box. Failure of a candidate certificate says nothing about solvability of
the original problem.

## 2. Exact elimination identity

Define `q_t(z)=f_t(bar y(z),z)`. For every feasible `y,z`, expansion and
(3) give the identity

\[
 \begin{split}
 f_t(y,z)-q_t(z)
  ={}&\tfrac12(y-\bar y(z))^TC_t(y-\bar y(z))\\
    &+\ell(z)^T(y-l_t)+u(z)^T(u_t-y)\ \ge0.          \tag{4}
 \end{split}
\]

To verify it, the quadratic expansion has linear term
`(ell-u)'(y-bar y)`. Complementarity replaces this term by the two
displayed bound-slack products. Every term on the right is nonnegative.
Equality holds at the feasible response `bar y(z)`. Thus

\[
 q_t(z)=\min_{y\in Y_t} f_t(y,z),\qquad
 q(z):=q_0(z)+\sum_t q_t(E_tz),\qquad
 \min F=\min_{z\in Z}q(z).                           \tag{5}
\]

The reduced Hessian contributed by a block is exactly

\[
 A_t+B_t^TC_tB_t+B_t^TD_t+D_t^TB_t.                 \tag{6}
\]

No large positive term is approximated or dropped. Its cancellation in
(6) is rational algebra certified by (4). An optimizer `z*` lifts by (2)
to an optimizer of `F`. This proves exact partial minimization even when
the conditional minimizer is nonunique.

The nonnegativity of the removed expression is relative to its moving
affine response. It need not be a homogeneous PSD quadratic about the
original origin. Therefore (4) does not contradict the existing
[copositive residual obstruction](../../research-20261002/new-direction/psd-extraction-curvature-obstruction.md).

## 3. Width, growth, and exact output

Suppose every scope of `q_0`, and every attachment set selected by `E_t`,
fits in a bag of a supplied tree decomposition on the retained variables.
Let `p` be its largest bag size. Assign each reduced factor `q_t` to its
containing bag. Formula (6) then introduces no edge outside these bags.
The relevant width is this verified **residual** width. Eliminating an
arbitrary block of a low-width original graph can create a large clique;
original width alone is insufficient.

Suppose the original problem has a unique optimizer `(z*,y*)` and

\[
 F(z,y)-F^*\ge g\big(\|z-z^*\|^2+\|y-y^*\|^2\big),
 \qquad g>0.                                       \tag{7}
\]

Since every reduced optimizer lifts to an original optimizer, `q` has
unique optimizer `z*`, and `y_t*=a_t+B_tE_tz*`. Evaluating (7) on the
affine response gives the stronger reduced growth bound

\[
 q(z)-F^*\ge g(z-z^*)^TM(z-z^*),\qquad
 M=I+\sum_t E_t^TB_t^TB_tE_t\succeq I.             \tag{8}
\]

This has no variable-occurrence penalty: every private coordinate is
counted once, and shared retained coordinates are already counted in `I`.
In particular, ordinary Euclidean growth with constant `g` transfers.

Let `H_red` be the assembled reduced Hessian. If its diagonal entries
are all nonpositive, independent endpoint rounding and finite-state tree
DP solve (5) exactly with two states per retained coordinate, without
growth or uniqueness. Otherwise put

\[
 L_{\rm red}=\max_i (H_{\rm red})_{ii}>0,\qquad
 \kappa_{\rm red}=\max\{1,L_{\rm red}/g\}.          \tag{9}
\]

**Reduction theorem.** The validated block certificates, the rational
original input, and the residual tree decomposition admit an exact
algorithm in

\[
 f(p,\kappa_{\rm red})(I+1)^C                      \tag{10}
\]

bit operations, where `I` includes the supplied certificate and decomposition
encoding lengths and `C` is absolute. A rational feasible point with a
certified additive gap at most `2^-q` requires
`f_1(p,kappa_red)(I+q+1)^C_1`. The algorithm needs neither `g` nor
`kappa_red` as input. It returns the expanded rational original vector.

**Proof.** Compute (6), assign factors as above, and apply the
[reviewed filtered-grid theorem](../../research-20261002/new-direction/pruned-coordinate-grid.md)
to the rational box quadratic `q`. Its hypotheses are precisely the
verified bag scopes, (8), and (9). The solver's certified filtering and
unknown-growth trial caps apply unchanged. Rational matrix multiplication
and summation produce a reduced encoding length polynomial in `I`; exact
cancellation causes no numerical precision issue. Its exact rational
reconstruction returns `z*`, and (2) returns all private coordinates in
polynomial additional bit time. If there are no retained variables,
evaluate the one feasible affine response and stop. The case of no
private blocks is the original filtered-grid theorem. This proves all
claimed bounds. □

The final certificate combines the residual solver's filtering-history
certificate with identities (3)--(4). Given a reduced certified lower
bound `L`, (4) proves `F>=q>=L` throughout the original box. Every residual
incumbent lifts to a feasible original point with exactly the same value.
Thus certificate validity is independent of (7), as is its checking. Growth
is used only in the runtime bound. A floating-point active-set guess alone
is not such a certificate.

## 4. A checkable negative-curvature regime

Let `H` be the original full Hessian and
`nu=max(0,-lambda_min(H))`. The convex case `nu=0` needs just an exact
convex-QP solve. For `nu>0`, compute a rational bound

\[
 \nu\le\beta<2\nu                                  \tag{11}
\]

by the exact PSD halving procedure in the
[spectral normalization note](../../research-20261002/new-direction/spectral-normalization.md).
This procedure has polynomial bit complexity even when the positive
eigenvalues are much larger than `nu`.

If the reduced diagonal satisfies the verifiable inequalities

\[
 (H_{\rm red})_{ii}\le C_0\beta\quad\hbox{for all }i,\qquad C_0>0,
                                                               \tag{12}
\]

then (10) is of the requested form

\[
 f\big(p,\max\{1,2C_0\nu/g\}\big)\operatorname{poly}(I).         \tag{13}
\]

The actual algorithm computes `L_red`; it need not guess `C_0` or `g`.
For an input class with bounded `C_0`, only width and `nu/g` enter the
parameter dependence. Establishing (12) for arbitrary sparse QP is **not**
part of this theorem.

A stronger, still checkable version uses (8). Supply a positive rational
diagonal matrix `D` satisfying

\[
 M-D\succeq0,\qquad (H_{\rm red})_{ii}\le C_0\beta D_{ii}.
                                                               \tag{14}
\]

Choose dyadic `r_i>0` with `1<=r_i^2 D_ii<4`; this takes polynomial
bit time by exact comparisons with powers of four. Set `z=Rw`, with
`R=diag(r_i)`. The transformed box is still a rational product box,
the graph is unchanged, and (8) yields ordinary growth at least `g`
in `w`. The transformed upper coordinate curvature is at most
`4C_0 beta<8C_0 nu`. This gives (13) with factor eight in place of two.
Taking `D=I` always meets the first inequality and recovers the unscaled
version without its factor-four approximation loss. Finding an optimal
diagonal `D` is not needed or claimed.

For clarity, the original negative curvature does transfer as the
generalized bound

\[
 H_{\rm red}\succeq-\nu M.                         \tag{15}
\]

Indeed, the derivative of the affine lift has Gram matrix `M`, and
`H_red` is the full Hessian pulled back by this derivative. Applying
`H>=-nu I` proves (15). This controls negative curvature; it does not
imply (12) or (14), which bound *positive coordinate* curvature.

## 5. Constructing and recognizing the certificate

For a proposed bound-active set `K`, fix each `y_i`, `i in K`, at its
chosen endpoint `v_i`. Let `J` be the remaining coordinates. If
`C_JJ` is positive definite, solve

\[
 \bar y_J(z)=-C_{JJ}^{-1}(D_Jz+c_J+C_{JK}v_K),\qquad
 \bar y_K(z)=v_K.                                   \tag{16}
\]

For free coordinates use zero multipliers. For a lower-bound coordinate
use its affine gradient as the lower multiplier and zero upper multiplier;
for an upper-bound coordinate use minus its gradient as the upper
multiplier and zero lower multiplier. Exact box range tests check primal
feasibility and the required multiplier signs. If they pass, (3) follows.
If `J` is empty the linear solve is absent. Singular certificates can
instead be supplied directly through (2)--(3).

A single arbitrary central active pattern can fail to find an existing
affine selector when the private Hessian is singular. The stronger
[recognition theorem](adversary/affine-selector-recognition.md) avoids this
failure and decides existence of an affine selector in polynomial bit time.
Here is its algorithm and the reason it is complete.

Choose the strict interior midpoint `z0` of the attachment box and obtain
one exact convex-QP optimizer `yhat` there. Put `h0=Dz0+c`. The complete
central optimal set is the rational polytope

\[
 P_0=\{y\in Y:Cy=Cyhat,\quad h_0^Ty=h_0^Tyhat\}.      \tag{16a}
\]

This follows by expanding the objective about `yhat`: both its
first-order feasible displacement term and its PSD quadratic remainder
are nonnegative, so equality forces both to vanish. In particular all
central optima have the same gradient `h=Cyhat+h0`. Set
`K_l={i:h_i>0}`, `K_u={i:h_i<0}`, and `J={i:h_i=0}`.
No coordinate optimization over `P0` is needed.

Every central optimizer fixes `K_l,K_u` at their corresponding bounds
by KKT. Every globally affine feasible selector then fixes those
coordinates at those bounds throughout the parameter box: an affine
bounded function attaining a bound at an interior parameter is constant.
For a globally affine optimal selector, the `J` gradient must vanish
identically, because its central value is zero.
If that selected coordinate is not fixed at a bound, it is interior for
all interior parameters and stationarity applies. If it is fixed at a
bound, its affine gradient has one sign throughout the box and vanishes
at the center, so again it vanishes identically.

Thus existence of an affine selector is equivalent to the following
conditions on its coefficients: fix `K_l,K_u` at their bounds, impose
zero gradient coefficients on `J`, require global primal box membership,
and require the appropriate global gradient signs on `K_l,K_u`. These
are a polynomial-size LP. For example, writing
`Z=z0+[-rho,rho]` and `bar y=a+B(z-z0)`, the range of coordinate `i`
is exactly `a_i +/- sum_j rho_j |B_ij|`; auxiliary absolute-value
variables linearize both its range and the affine gradient sign tests.
A feasible LP point supplies rational maps and multipliers (3) of
polynomial length. Infeasibility proves that no real affine selector
exists. The recognizer uses one exact central convex QP and one LP; it
does not enumerate active sets or critical regions. A coordinate fixed
at a bound throughout `P0` but having zero central gradient can remain
in `J`: the same zero-gradient argument covers it, and global primal
feasibility supplies any needed bound restriction.

For example, `(y1+y2-z)^2` on `Y=[0,1]^2`, `Z=[0,2]` has a central
optimizer `(0,1)` whose arbitrary active pattern is misleading, but the
method finds the affine selector `(z/2,z/2)`. A clipped scalar response
crossing both bounds is correctly rejected. The linked theorem proves
every implication, includes the zero-dimensional cases, and records
targeted recognition checks.

This recognition result removes the need to supply the affine maps for
a supplied private-block partition. It does not discover a useful
partition or make all convex response maps affine. Blocks failing the
test can instead remain as exact convex value factors under the
[companion sparse oracle theorem](sparse-convex-value-factors.md). Certified
affine blocks can be removed first; the remaining factors use the direct
curvature of the resulting retained quadratic. This gives a complete
composition procedure without constructing piecewise-affine maps.

## 6. A family separating the parameters

The following family demonstrates that the reduction can remove unbounded
positive curvature while both the retained dimension and negative inertia
grow. It is an algebraic illustration, not a difficult benchmark.

For `i=1,...,m`, let `u_i,v_i,y_i` lie in `[0,1]`. Put `a=1/3`,
`eta=1/16`, `M0>=1`, and

\[
 \begin{split}
 q(u,v)={}&\sum_i\big[(u_i-a)^2-(u_i-a)v_i-v_i^2+3v_i\big]\\
 &+\eta\sum_{i=1}^{m-1}\big[(u_{i+1}-u_i)^2+(v_{i+1}-v_i)^2\big],\\
 F(u,v,y)={}&q(u,v)+M_0\sum_i(y_i-u_i)^2.             \tag{17}
 \end{split}
\]

The exact feasible response is `y_i=u_i`, with zero multipliers. Each
private block has `C=2M0`, `D=-2M0` on `u_i`, and its reduced contribution
is zero. These certificates fit at single-coordinate attachment scopes.
The residual ladder has bags `{u_i,v_i,u_(i+1),v_(i+1)}`, of size at most
four (use one size-two bag for `m=1`).

For `t_i=u_i-a`, we have `-1/3<=t_i<=2/3`, and

\[
 -t_iv_i-v_i^2+3v_i-v_i^2
   =v_i(3-t_i-2v_i)\ge0.
\]

Thus `q>=||u-a1||^2+||v||^2`, with unique optimum
`u=a1,v=0`. Also

\[
 \|u-a1\|^2+\|v\|^2+\|y-a1\|^2
 \le3\|u-a1\|^2+\|v\|^2+2\|y-u\|^2\le3F.          \tag{18}
\]

So `g=1/3` is a valid original full-vector growth constant for every
`m` and `M0>=1`.

The residual Hessian is

\[
 \begin{pmatrix}2I&-I\\-I&-2I\end{pmatrix}
    +2\eta\begin{pmatrix}L_m&0\\0&L_m\end{pmatrix},                \tag{19}
\]

where `L_m` is the path Laplacian, with eigenvalues in `[0,4]`.
Its eigenvalues are `2eta lambda +/- sqrt(5)`. It therefore has exactly
`m` negative eigenvalues, and is bounded below by `-sqrt(5) I`.
Adding the PSD penalties in (17) shows that the original `nu<=sqrt(5)`.
For every negative residual direction, lift its `y` displacement equal
to its `u` displacement. All penalties then vanish on that direction,
so the original Hessian also has an `m`-dimensional negative subspace.
The standard Schur congruence with the positive private block shows that
its negative inertia is exactly `m`.

Nevertheless, the residual maximum diagonal is at most `9/4`, so
`L_red/g<=27/4`, independent of `m` and `M0`. The original maximum
diagonal is at least `2M0`, so its coordinate-curvature ratio diverges
with `M0`. The original ratio `nu/g<=3sqrt(5)` stays bounded. To see that
(12) can also use a uniform constant, take a residual eigenvector for
eigenvalue `-sqrt(5)` in the constant path mode. Its penalty-free lift has
squared norm at most twice its residual squared norm, giving
`nu>=sqrt(5)/2`. Hence `L_red<=3 beta` for every bound (11).

The filtered residual problem has fixed width and fixed conditioning for
all these instances, while an algorithm parameterized by original
coordinate curvature or by negative inertia has no comparable uniform
parameter bound. This does not prove practical speedup. These particular
instances already have the elementary optimality proof (18).

## 7. Prior work and remaining boundary

Fixed-active-set affine responses and affine multipliers are standard
parametric quadratic programming. Theorem 2 in
[Bemporad, Morari, Dua, and Pistikopoulos (2002)](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf)
describes the affine optimizer and multipliers on a critical region for
strictly convex multiparametric QP. Our global certificate is one region
covering the attachment box; (4) directly includes PSD singular blocks.
Sparse elimination, Schur complements, and KKT certificates are also
classical. The new local implication assessed here is the combination of
validated condensation, the metric growth transfer (8), and the previously
proved filtered-grid bound. No publication-priority claim is made.

This result should not be confused with the exact forest algorithm of
[Del Pia and Khajavirad (2026)](https://arxiv.org/abs/2609.35595).
That theorem needs neither growth nor affine recourse on forests; its
more general endpoint/continuous decompositions must also be credited.
Here the reduced problem may retain an arbitrarily large continuous
nonconvex ladder or another supplied bounded-width graph, and its
conditioning remains a substantive assumption.

For the unrestricted target, a solver must still handle changing recourse
active faces, positive residual diagonals not controlled by negative
curvature, and elimination that creates large separator scopes. Current
results do not control all three simultaneously. In particular, the
[existing unique-optimum obstruction](../../research-20261002/new-direction/unique-message-growth-obstruction.md)
already gives exponential complete scalar messages on a unit box at fixed
width and `nu/g<=2`. Affine elimination avoids that representation only
on its stated certificate class; it does not invalidate the obstruction.

## 8. Targeted verification

Run the accompanying exact-arithmetic checker with

```sh
python3 -B research-20261002-decomposition/negative-curvature/check_affine_convex_recourse.py
```

It validates feasible response maps, multiplier signs and polynomial
complementarity, reduced coefficients, the identity (4), and selected
instances of (17)--(19). It also rejects maps valid only at a sample
parameter and invalid multiplier certificates. The checker is a diagnostic
for these algebraic contracts, not an implementation or performance test
of the full filtered-grid algorithm. The general claims rest on the
proofs above and the cited existing solver theorem. No project-wide
verification or CI inspection is part of this work.

The recorded run passed eight valid block certificates, 1,518 elimination
identities, five rejected invalid certificates, 1,440 family growth checks,
and 18 family matrix cases. Its companion-factor checks also passed 13,320
exact local convex-QP values and 540 corner interpolation inequalities.
The [saved JSON](check_affine_convex_recourse-results.json) was generated
by the same command with its output redirected to that file. Targeted
Python AST, whitespace, and local-link checks passed. The
[independent review](adversary/affine-convex-recourse-review.md) inspected
the proof and checker and reran the original affine checks; its recorded
scope distinguishes the later companion checks.
