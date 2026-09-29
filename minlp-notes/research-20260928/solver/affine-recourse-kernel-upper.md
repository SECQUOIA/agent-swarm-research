# Kernel rounding with affine private recourse

Date: 2026-09-28. An extension of
[partial-kernel-rounding.md](partial-kernel-rounding.md).
This note proves an upper bound. An upper bound alone does not establish
that its exponent is sharp or that the result is new in the literature.

## 1. Result and its meaning

Large private convex quadratic blocks can have feasible polytopes that
depend affinely on the shared variables. Complete recourse on the shared
box and a fixed constraint matrix make the conditional-mean rounding
repairable. The resulting anisotropic moment hierarchy has error
`O(r^-1)`. Its private degree remains two; its SDP dimension exponent in
`r` depends only on the number of shared variables in a bag.

The mechanism is precise. Smoothing produces a private mean feasible at
a conditional mean of the **source** shared variables. The generated
shared variables are different. A Hoffman error bound repairs the private
mean at the generated point. The kernel bounds the expected movement by
`O(r^-1)`. Objective smoothing itself still costs only `O(r^-2)`.

This could supply controlled global lower relaxations for nonconvex
polynomial master decisions coupled to large continuous convex QPs. The
result gives finite SDP dimensions and an exact-arithmetic grid/QP
comparison. It does not give a numerical running-time or bit-complexity
guarantee. Private integer variables are outside this argument.

## 2. Model, constants, and finite relaxation

Let shared bags `S_b` form a finite junction tree with running intersection
and cover `{1,...,n}`. Put `k_b=|S_b|`, `s=max(1,max_b k_b)`, and let `t`
be the number of bags. Bag `b` has a private vector `y_b` of dimension
`p_b`; private vectors in different bags are disjoint. Its feasible set is

\[
 P_b(u)=\{y\in[-1,1]^{p_b}:A_by\le a_b+B_bu\},
 \qquad u\in[-1,1]^{S_b}.                                      \tag{1}
\]

All coefficients are real. Assume **complete recourse**:
`P_b(u)` is nonempty for every shared box point `u`, for every bag.
Equalities may be included as two inequalities. Neither strict feasibility
nor a full-dimensional fiber is assumed. The number of rows of `A_b` is
`J_b`. Shared variables have no further constraints.

The objective is

\[
 f(u,y)=\sum_b f_b(u_{S_b},y_b),\qquad
 f_b(u,y)=c_b(u)+q_b(u)^Ty+y^TQ_b(u)y,                         \tag{2}
\]

where the coefficients are polynomial in `u`, `Q_b` is symmetric, and
`Q_b(u)\succeq0` on the entire shared box. Let `z=(1,y^T)^T` and write

\[
 f_b(u,y)=z^TH_b(u)z,\quad
 H_b(u)=\begin{pmatrix}c_b(u)&q_b(u)^T/2\\q_b(u)/2&Q_b(u)\end{pmatrix}
       =\sum_\alpha H_{b\alpha}T_\alpha(u).
\]

Define

\[
 d=\max_{b,\alpha:H_{b\alpha}\ne0}|\alpha|,\qquad
 \mathcal A=\sum_{b,\alpha}\|H_{b\alpha}\|_{1,\mathrm{entry}}
                              \sum_{i\in S_b}\alpha_i^2.       \tag{3}
\]

Take `d=0` for the zero objective. The entrywise matrix norm counts both
off-diagonal entries. For Euclidean norms choose a Hoffman constant `h_b^H`
for the fixed matrix `C_b=[A_b;I;-I]`: for every consistent right-hand side
`e` and every `y`,

\[
 \operatorname{dist}(y,\{v:C_bv\le e\})
 \le h_b^H\|(C_by-e)_+\|_2.                                 \tag{4}
\]

Such a finite constant depends on `C_b`, not on `e`. This is a classical
Hoffman bound, not a new assumption about a particular active set. Put

\[
 \Lambda_b=\max_{u\in[-1,1]^{S_b},\ y\in[-1,1]^{p_b}}
                  \|q_b(u)+2Q_b(u)y\|_2,\quad
 \Gamma_b=\Lambda_bh_b^H\|B_b\|_2,\quad
 \mathcal R=\sum_b\Gamma_b\sqrt{k_b}.                        \tag{5}
\]

Here `||B_b||_2` is the operator norm. Compactness makes `Lambda_b` finite;
it is a Lipschitz constant in the private vector on its box. A simple
explicit bound is
`Lambda_b <= sum_alpha ||q_balpha||_2 +
2 sqrt(p_b) sum_alpha ||Q_balpha||_2`.
Zero-dimensional and empty shared blocks have their natural empty-vector
interpretations and make no repair contribution.

For an integer `r>=max(s+1,d)` define local functionals on

\[
 L_b:\mathbb R[u_{S_b}]_{\le2r}\otimes
                    \mathbb R[y_b]_{\le2}\longrightarrow\mathbb R.
                                                                    \tag{6}
\]

They satisfy `L_b(1)=1` and separator agreement for shared polynomials of
total degree at most `2r`. With `w_I=prod_{i in I}(1-u_i^2)`, impose

\[
 L_b\bigl(w_I[q_0(u)+q(u)^Ty]^2\bigr)\ge0,
                  \qquad \deg q_i\le r-|I|;                    \tag{7}
\]

\[
 L_b\bigl(w_Iq(u)^2[a_b+B_bu-A_by]_j\bigr)\ge0,
                  \qquad \deg q\le r-|I|-1;                    \tag{8}
\]

\[
 L_b\bigl(w_Iq(u)^2(1-y_i^2)\bigr)\ge0,
                  \qquad \deg q\le r-|I|.                      \tag{9}
\]

Conditions with negative degree allowance are absent. The conservative
degree allowance in (8) works for all affine rows. When a row has no shared
dependence, its degree allowance can be increased to `r-|I|` without
changing the proof. The redundant bounds (9) are essential; the fixed
polytope note gives an all-order unboundedness example when they are omitted.

Let `rho_r` be the infimum of `sum_b L_b(f_b)` and `f*` the original
minimum. Evaluations at feasible points satisfy (6)--(9), so `rho_r<=f*`.
The matrix in (7) has
`(p_b+1) binom(r-|I|+k_b,k_b)` rows; those in (8) and (9) have respectively
`binom(r-|I|-1+k_b,k_b)` and `binom(r-|I|+k_b,k_b)` rows when present.
There are `2^k_b` shared preordering weights. At most
`binom(p_b+2,2) binom(2r+k_b,k_b)` local moments are needed. These are
polynomial dimension bounds in `p_b,J_b,r` at fixed `s`, with no assertion
that the conditioning constants in (3)--(5) are independent of dimension.

## 3. Quantitative theorem

Set

\[
 m=\lfloor(r-1)/s\rfloor+1\ge2,\quad D_m=2m^2+1,\quad
 V_m=\frac{3(4m-3)}{2m(2m^2+1)}<\frac6{D_m}.                \tag{10}
\]

**Theorem.** Every feasible collection `(L_b)` admits a globally feasible
probability law `nu` such that

\[
 \int f\,d\nu\le\sum_bL_b(f_b)
                   +\frac{3\mathcal A}{D_m}
                   +\sqrt{V_m}\,\mathcal R.                  \tag{11}
\]

Consequently,

\[
 0\le f^*-\rho_r\le\frac{3\mathcal A}{D_m}
                         +\sqrt{V_m}\,\mathcal R
 \le\frac{3s^2\mathcal A}{2r^2}
                         +\frac{\sqrt3s\mathcal R}{r}         \tag{12}
\]

because `m=ceil(r/s)>=r/s`. Some feasible point has objective at most (11).
When all `B_b=0`, repair disappears, recovering a second-order bound
(with the unused one-degree reserve removable as in the companion note).

The exponent is sharp for this hierarchy. In the
[affine-recourse boundary example](affine-recourse-rate-boundary.md), take
the shared coordinate `u=y` and private coordinates `x` and `z` in the
two bags. Its actual local measures satisfy every condition (6)--(9),
and agree on shared moments through degree `2r`. Therefore they give
`f*-rho_r>=1/[9 pi(r+1)]` for this rectangular hierarchy as well. The
present upper bound proves matching order `Theta(1/r)`. This argument
uses the actual-measure witnesses, not a comparison between the different
finite cones. The [combined prior audit](affine-recourse-upper-prior.md)
checks this transfer and compares the theorem with existing recourse work.

### 3.1. Degree reserve and conditional source means

Use the squared-Fejer kernel `K_m` from
[sparse-kernel-rounding.md](sparse-kernel-rounding.md), with normalized
arcsine measure `mu` and multipliers `g_j`. It has degree `2(m-1)` in each
argument, integrates to one, and satisfies

\[
 0\le g_j\le1,\qquad 1-g_j\le3j^2/D_m.
\]

For a bag set `K_b(u,v)=prod_{i in S_b}K_m(u_i,v_i)` and suppress `b`
temporarily. At every fixed output `v`, its shared preordering certificate
has terms `w_I p(u)^2` with

\[
 \deg p\le k_b(m-1)-|I|\le r-1-|I|.                         \tag{13}
\]

Multiplying by the square of any affine form in `(u,y)` remains allowed
by (7): every resulting coefficient of `1,y_1,...,y_p` has shared degree
at most `r-|I|`. Thus `F_v(a)=L(K_b(u,v)a(u,y))` has a positive
semidefinite moment matrix on `1,u_1,...,u_k,y_1,...,y_p`.
All products used here have shared degree at most `2r` and private degree
at most two. Define

\[
 h(v)=L(K_b),\quad U(v)=L(K_bu),\quad
 \ell(v)=L(K_by),\quad Y(v)=L(K_byy^T).                       \tag{14}
\]

In addition to positivity, (9) gives `0<=Y_ii(v)<=h(v)`. We also have

\[
 0\le L(K_bu_i^2)\le h(v).                                 \tag{15}
\]

Here the upper bound needs the reserve in (13). To verify it directly,
multiply a certificate term `w_I p^2` by `(1-u_i^2)`. If `i notin I`,
use weight `w_(I union {i})` and the same square. If `i in I`, use weight
`w_(I without {i})` and square `[(1-u_i^2)p]^2`. The square-degree bounds
are respectively `r-|I|-1` and `r-|I|+1`, precisely the allowances for
those new weights in (7). Therefore `L(K_b(1-u_i^2))>=0`.

When `h(v)>0`, put `ubar(v)=U(v)/h(v)` and `ybar(v)=ell(v)/h(v)`.
Cauchy--Schwarz and (15) show `ubar(v) in [-1,1]^k`; the analogous
private bounds show `ybar(v) in [-1,1]^p`. Applying (8) to the kernel
certificate, permitted by (13), gives

\[
 a_b+B_b\overline u(v)-A_b\overline y(v)\ge0,
 \qquad \overline y(v)\in P_b(\overline u(v)).                \tag{16}
\]

This proves feasibility at the conditional **source mean** `ubar(v)`.
It does not claim that this mean equals the output `v`.

When `h(v)=0`, every diagonal of the conditional moment matrix is zero
by (9) and (15); positive semidefiniteness makes that whole matrix zero.
In particular, `U=ell=Y=0` there. This handles all later zero-density
expressions without dividing by zero. Define `ubar(v)=0` and `ybar(v)=0`
there; (16) is asserted only when `h(v)>0`.

### 3.2. Repair and measurability

For positive density let

\[
 \widehat y_b(v)=\operatorname{proj}_{P_b(v)}\overline y_b(v).
                                                                    \tag{17}
\]

The Euclidean projection is unique because the fiber is nonempty, compact,
and convex. At the source-feasible mean, box residuals vanish, and (16)
implies componentwise

\[
 (A_b\overline y-a_b-B_bv)_+
       \le[B_b(\overline u-v)]_+.
\]

The fixed-matrix Hoffman bound therefore gives

\[
 \|\widehat y_b(v)-\overline y_b(v)\|_2
 \le h_b^H\|B_b\|_2\|\overline u_b(v)-v\|_2.                 \tag{18}
\]

The projection map `(v,z) -> proj_(P_b(v))(z)` is continuous. Indeed (4)
applied in both directions gives
`d_H(P_b(v),P_b(w)) <= h_b^H ||B_b||_2 ||v-w||_2`.
For any convergent sequence `(v_j,z_j)`, compactness bounds its projections;
every limit point is feasible at the limit parameter. Approximate each
fixed limit-fiber comparison point by points of `P_b(v_j)` using this
Hausdorff bound. Passing to the projection-minimality inequalities shows
that every limit point is the unique projection at the limit. This proves
continuity, including at lower-dimensional fibers.

The functions in (14) are polynomial in `v`. On `{h>0}` their ratios are
continuous. Define `yhat_b(v)=proj_(P_b(v))(0)` on `{h=0}`. This gives a
Borel measurable, everywhere feasible private decision. Complete recourse
is used at every output point, including this zero-density definition.

### 3.3. Integrated displacement

Conditional Cauchy--Schwarz yields, for positive density,

\[
 h(v)\|\overline u(v)-v\|_2^2
 \le\sum_{i\in S_b}L(K_b(u,v)(u_i-v_i)^2).                  \tag{19}
\]

Both sides vanish at zero density if the left side is defined to be zero.
Let `a_0=m(2m^2+1)/3` be the kernel normalizer. Its coefficients satisfy

\[
 1-g_1=m/a_0,\qquad 1-g_2=(4m-3)/a_0.                      \tag{20}
\]

For the second identity, the triangular coefficients
`b_j=(m-|j|)_+` obey
`a_0-a_2=(1/2)sum_j(b_j-b_(j-2))^2=4m-3`.
Integrate the right side of (19). Kernel normalization removes the other
coordinates, while `u_i=T_1(u_i)` and `u_i^2=(1+T_2(u_i))/2` give

\[
 \int L(K_b(u,v)(u_i-v_i)^2)\,d\mu^{S_b}(v)
 =\frac{1-g_2}{2}+(1-2g_1+g_2)L(u_i^2)
 =\frac{4m-3}{2a_0}+\frac{3-2m}{a_0}L(u_i^2)
 \le V_m.                                                   \tag{21}
\]

The final step uses `m>=2` and `L(u_i^2)>=0`. Consequently

\[
 \int h_b(v)\|\overline u_b(v)-v\|_2^2\,d\mu^{S_b}(v)
 \le k_bV_m,\qquad
 \int h_b(v)\|\overline u_b(v)-v\|_2\,d\mu^{S_b}(v)
 \le\sqrt{k_bV_m}.                                         \tag{22}
\]

The last inequality uses `int h_b=1`. No representing measure for the
input functional is used. The constant `V_m` is sharp for this intermediate
transport bound: evaluation at source `u=0` makes (19) and (21) equalities.
This observation does not prove sharpness of (11) or of its rate for SDP
gaps.

### 3.4. Convex objective and global gluing

The conditional private matrix
`M_b(v)=[[h,ell^T],[ell,Y]]` is positive semidefinite. For positive density
its Schur complement and `Q_b(v)\succeq0` give

\[
 h_b(v)f_b(v,\overline y_b(v))
 \le \langle H_b(v),M_b(v)\rangle.                         \tag{23}
\]

At zero density the matrix vanishes, so both sides are zero. Lipschitz
continuity in the private box, (18), and (22) then give

\[
 \int h_b(v)f_b(v,\widehat y_b(v))\,d\mu^{S_b}(v)
 \le\int\langle H_b(v),M_b(v)\rangle\,d\mu^{S_b}(v)
                                  +\Gamma_b\sqrt{k_bV_m}.  \tag{24}
\]

The mixed-moment argument in the fixed-polytope note uses only (7),(9):
`|L_b(T_alpha z_i z_j)|<=1` for `|alpha|<=r`. Briefly, the shared
Chebyshev identity bounds `L_b(T_alpha^2)<=1`; (9) bounds
`L_b(T_alpha^2 y_i^2)<=1`; Cauchy--Schwarz in (7) bounds the cross moments.
Expand `H_b` and integrate the kernel using its Chebyshev multipliers.
Since `r>=d`, this gives

\[
 \int\langle H_b(v),M_b(v)\rangle\,d\mu^{S_b}(v)
 \le L_b(f_b)+\frac3{D_m}\sum_\alpha
       \|H_{b\alpha}\|_{1,\mathrm{entry}}\sum_i\alpha_i^2.    \tag{25}
\]

The normalized shared laws `h_b dmu^{S_b}` have matching separator
marginals: integrating out a coordinate removes its common kernel factor,
and the remaining separator polynomial lies in the agreed degree space.
Running intersection glues these laws to a global shared law. Assign
`y_b=yhat_b(u_(S_b))` for every bag. Measurability and (17) make this a
globally feasible law with the desired bag distributions. Sum (24)--(25)
to prove (11). The original feasible set is nonempty and compact and `f`
is continuous, so `f*<=int f dnu` and a point with no larger objective
exists. Taking the infimum over moment points proves (12), without SDP
attainment or strong duality.

## 4. Finite-grid consequence

Let `d_infty` be the largest individual shared degree in the Chebyshev
expansion of `H_b`, taking zero for constant coefficients. Set

\[
 N=m+\lfloor\max(d_\infty,2)/2\rfloor,\qquad
 \xi_j=\cos((2j-1)\pi/(2N)),\quad 1\le j\le N.                \tag{26}
\]

This quadrature order integrates both the polynomial matrix expression in
(23), of individual degree at most `2m-2+d_infty`, and each displacement
polynomial on the right of (19), of individual degree at most `2m`.
The latter requirement is why `N>=m+1` is retained even for a constant or
linear shared objective.

The nonnegative masses `N^(-k_b)h_b(xi)` normalize and have matching
separator marginals. Apply pointwise (19),(23),(18) at their nodes and
then finite-sum Cauchy--Schwarz. Exact quadrature reproduces (21),(25).
At each node minimize the feasible convex QP

\[
 F_b(v)=\min_{y\in P_b(v)} f_b(v,y).
\]

Replacing `yhat_b` by a QP minimizer can only improve the node cost. Thus

\[
 \min_{u\in\{\xi_1,\ldots,\xi_N\}^n}\sum_bF_b(u_{S_b})
 \le\sum_bL_b(f_b)+3\mathcal A/D_m+\sqrt{V_m}\mathcal R.       \tag{27}
\]

After `sum_b N^(k_b)` local QPs have been solved, junction-tree dynamic
programming takes `O(tN^s)` arithmetic/comparison operations to recover
an optimal grid assignment. This excludes QP table construction and
numerical certification. The algebraic nodes and real coefficients are
treated in an exact-arithmetic or oracle model.

Grid optimization itself is established, and a related first-order grid
approximation follows directly by smoothing a true optimizer and repairing
its private vectors. The additional content of (27) is its comparison
with every feasible point of this fixed-private-degree SDP hierarchy.

## 5. Limits, literature, and verification

Complete recourse is substantive: smoothing can place positive mass at
every part of the shared box, and an empty target fiber has no repair.
The fixed matrix in (1) is also substantive. A matrix depending on `u`
would make the recourse inequalities bilinear in `(u,y)`; (16) would no
longer follow by taking means. More general feasibility repair would need
separate assumptions and a separate proof.

For example, `P(u)={y in [-1,1]:uy=0}` has complete recourse, but its fiber
is `[-1,1]` at `u=0` and `{0}` at every other `u`. Its Hausdorff variation
is one across arbitrarily close shared points. Thus complete recourse alone
does not extend this proof to a shared-dependent constraint matrix.

The constants can be large for nearly incompatible linear constraints.
The theorem neither assumes a common interior feasible point nor provides
an efficiently computable sharp Hoffman constant. It includes all shared
box-preordering products, not just a quadratic module. The private variables
must be continuous, local to one bag, and convex quadratic in the objective.
Positive semidefiniteness of `Q_b` on the full shared box is an assumption;
the theorem supplies no generic efficient test for it.

The [fixed-private-polytope prior audit](partial-kernel-prior.md) covers the
kernel, pseudomoment Jensen, and partial-degree ingredients. The repair
ingredient is classical: [Hoffman (1952)](https://upload.wikimedia.org/wikipedia/commons/0/07/On_approximate_solutions_of_systems_of_linear_inequalities_%28IA_jresv49n4p263%29.pdf)
proves linear inequality error bounds; [Peña, Vera, and Zuluaga (2018),
Introduction (1) and Proposition 1](https://arxiv.org/html/1804.08418v1)
explicitly state the fixed-matrix bound uniformly over all consistent
right-hand sides. Their work also treats bounds that exploit already
satisfied box constraints. These sources were opened and inspected for the
specific fact (4); they do not establish novelty of the combined hierarchy
result. In particular, Hoffman repair after relaxation rounding is itself
prior work. A [broader comparison](affine-recourse-upper-prior.md) with
affine-recourse, sparse moment, and parametric convex optimization results
is complete. It identifies close prior mechanisms and qualifies the
combined hierarchy contribution; publication priority remains unestablished.

The [targeted verification record](affine-recourse-upper-verification.md)
reports exact checks of nonrepresentable moment feasibility, conditional
source feasibility, repair, transport, and quadrature. The
[independent adversarial review](affine-recourse-upper-review.md) found no
substantive gap in the finished proof and checked the corrected details
independently. These provide evidence about the written theorem, not a
formal certification of all its claims. No project-wide verification or
CI inspection is part of this topic.
