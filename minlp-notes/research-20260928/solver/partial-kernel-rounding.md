# Kernel rounding with large private convex quadratic blocks

Date: 2026-09-28. Structural extension with independent adversarial reviews.
The theorem uses the explicit positive kernel from
[sparse-kernel-rounding.md](sparse-kernel-rounding.md). Priority is not
established. The private blocks below are continuous, not integer.

## Contribution and intended capability

The kernel need only smooth variables that link local optimization blocks.
Each block may also contain an arbitrarily large private vector constrained
to a fixed bounded polytope, provided its objective is convex quadratic in
that vector. Matrix moments retain the private vector only through degree
two. Conditional means recover feasible private decisions without smoothing
them. The convergence bound remains of order `r^-2`; the dimension exponent
in the SDP size depends on the number of smoothed coordinates per bag,
not on the private block dimension.

This extends the box-only theorem to fixed local polyhedral constraints and
large convex quadratic blocks. It does not require an SOS representation of
the coefficient matrix's positivity. Positivity on the whole shared box is
an assumption, and verifying it can itself be difficult. The formulation is
useful when this property follows from the application's structure.

The possible solver capability is a polynomial-size dependence on the
number of private continuous variables at fixed shared width and accuracy
parameters. This is a statement about the dimensions of finite SDPs, not a
numerical running-time guarantee. Constants can grow with objective
coefficients and private dimension. The
[prior-work comparison](partial-kernel-prior.md) places this as a structural
consequence of the sparse kernel theorem. Partial lifting, fixed degree in
convex variables, matrix pseudomoment Jensen inequalities, and quadratic
matrix-kernel rates are established ideas. The candidate addition is their
quantitative compatibility with this sparse hierarchy and fixed private
polyhedral feasibility.

## 1. Problem and moment relaxation

Let `T` be a finite tree with `t` nodes indexed by `b`. Let `S_b` be subsets covering a
shared index set `{1,...,n}` and satisfying running intersection. Put
`k_b=|S_b|` and `s=max(1,max_b k_b)`. For each bag introduce a distinct
private vector `y_b` of dimension `p_b>=0` and a nonempty bounded rational
polytope

\[
 P_b=\{y\in\mathbb R^{p_b}:g_{bj}(y)\ge0,\ j=1,\ldots,J_b\}
       \subseteq[-1,1]^{p_b},                              \tag{1}
\]

where every `g_bj` is affine. Equalities may be represented by two
inequalities. A bounded rational polytope can be placed in this box by a
rational affine coordinate scaling, with the change reflected in the
objective coefficients. Private variables are disjoint across bags;
shared variables `u` range freely over `[-1,1]^n`. There are no additional
constraints involving both `u` and `y`.

Consider

\[
 f(u,y)=\sum_b f_b(u_{S_b},y_b),\qquad
 f_b(u,y)=c_b(u)+a_b(u)^Ty+y^TQ_b(u)y,                    \tag{2}
\]

where the coefficients are polynomials in `u`, `Q_b(u)` is symmetric, and

\[
 Q_b(u)\succeq0\quad\hbox{for every }u\in[-1,1]^{S_b}.   \tag{3}
\]

Write `z=(1,y^T)^T`, so that `f_b=z^T H_b(u)z` with

\[
 H_b(u)=\begin{pmatrix}c_b(u)&a_b(u)^T/2\\
                       a_b(u)/2&Q_b(u)\end{pmatrix}
       =\sum_\alpha H_{b\alpha}T_\alpha(u).              \tag{4}
\]

The whole matrix `H_b` need not be positive semidefinite. Define

\[
 d=\max_{b,\alpha:H_{b\alpha}\ne0}|\alpha|,\qquad
 A=\sum_{b,\alpha}\|H_{b\alpha}\|_{1,\mathrm{entry}}
                              \sum_{i\in S_b}\alpha_i^2. \tag{5}
\]

The entrywise norm in (5) counts both symmetric off-diagonal entries. In
terms of (2), it is the sum of absolute coefficients of `c`, of each
component of `a`, and of all ordered entries of `Q`. Empty multi-indices
contribute zero. Take `d=0` when the objective is zero.

For an integer `r>=max(s,d)`, a local functional is defined on the
rectangular polynomial space

\[
 L_b:\mathbb R[u_{S_b}]_{\le2r}\otimes
                   \mathbb R[y_b]_{\le2}\longrightarrow\mathbb R.
                                                                  \tag{6}
\]

For `I subseteq S_b`, put `w_I(u)=prod_{i in I}(1-u_i^2)`. Impose
`L_b(1)=1` and the following conditions whenever the displayed polynomial
has shared degree at most `2r`:

\[
 L_b\!\left(w_I(u)[q_0(u)+q(u)^Ty]^2\right)\ge0,
 \quad \deg q_i\le r-|I|;                               \tag{7}
\]

\[
 L_b(w_I q(u)^2 g_{bj}(y))\ge0,
 \quad \deg q\le r-|I|;                                 \tag{8}
\]

\[
 L_b(w_I q(u)^2(1-y_i^2))\ge0,
 \quad \deg q\le r-|I|.                                 \tag{9}
\]

Here (7) uses vector-valued coefficients and (8)--(9) use scalar `q`.
Terms with a negative degree allowance are absent. Conditions (9) are
valid redundant quadratic bounds; they are essential for the proof below.
Finally adjacent bags agree on every polynomial solely in their shared
separator variables of total degree at most `2r`.

Let `rho_r` be the infimum of `sum_b L_b(f_b)` over these constraints and
let `f*` be the minimum of (2) on `[-1,1]^n x product_b P_b`. Every feasible
point supplies feasible evaluation functionals, so `rho_r<=f*`.

All these conditions are finite SDP constraints. The matrix for (7) has
size

\[
 (p_b+1){r-|I|+k_b\choose k_b};                          \tag{10}
\]

those for each constraint in (8) or (9) have size
`binom(r-|I|+k_b,k_b)`. There are `2^{k_b}` choices of `I`. The number of
local moment variables is at most

\[
 {p_b+2\choose2}{2r+k_b\choose k_b}.                     \tag{11}
\]

Thus the SDP dimensions are polynomial in `p_b,J_b,r` for fixed `s`, with
`r`-exponents depending only on `s`. The constants include `2^s`. This is
an anisotropic degree restriction: private degree stays two at all orders.

## 2. The rounding theorem

**Theorem.** Under (1)--(3), set `m=floor(r/s)+1`. Every feasible collection
`(L_b)` admits a feasible global probability law `nu` such that

\[
 \int f\,d\nu\le\sum_bL_b(f_b)+{3A\over2m^2+1}.          \tag{12}
\]

Consequently,

\[
 0\le f^*-\rho_r\le {3A\over2m^2+1}
                       \le{3s^2A\over2r^2}.             \tag{13}
\]

In particular, there is a feasible point attaining the upper bound in
(12). No absolute-value bound on the difference in (12) is claimed:
conditional averaging can strictly improve the private convex cost.
If all coefficients are constant in the shared coordinates, `A=0`, and
this relaxation is exact at every allowed order.

### Bounded mixed moments

For `|alpha|<=r` and `0<=i,j<=p_b`, with `z_0=1`,

\[
 |L_b(T_\alpha(u)z_i z_j)|\le1.                         \tag{14}
\]

For clarity suppress `b`. The scalar shared-box positivity in (7), applied
to the standard telescoping Chebyshev identity, gives

\[
 L(T_\alpha^2)\le1.
\]

Indeed `1-T_k(u)^2=(1-u^2)U_{k-1}(u)^2`, and telescoping the tensor product
represents `1-T_alpha^2` as a sum of shared box generators times squares,
each of shared degree at most `2|alpha|`. Condition (9), with `I` empty and
`q=T_alpha`, gives

\[
 0\le L(T_\alpha^2 y_i^2)\le L(T_\alpha^2)\le1.
\]

Condition (7) with `I` empty defines a positive semidefinite bilinear form
on polynomials of shared degree at most `r` and private degree at most
one. Cauchy--Schwarz for `T_alpha z_i` and `z_j` now gives (14), including
indices zero. This proof uses no representing measure for `L`.

### Positive conditional matrices

Use the common univariate kernel `K_m` from the companion theorem, with
nonnegative Chebyshev multipliers `g_k<=1` and

\[
 1-g_k\le{3k^2\over2m^2+1},\qquad
 \int K_m(u,v)\,d\mu(v)=1,                              \tag{15}
\]

where `mu` is normalized arcsine measure. Define

\[
 K_b(u,v)=\prod_{i\in S_b}K_m(u_i,v_i),\qquad
 M_b(v)=L_b(K_b(u,v)zz^T)
       =\begin{pmatrix}h_b(v)&\ell_b(v)^T\\
                         \ell_b(v)&Y_b(v)\end{pmatrix}. \tag{16}
\]

For fixed `v`, the kernel has a shared preordering representation whose
square terms have degree at most `k_b(m-1)-|I|<=r-|I|`. Multiplying each
square by an arbitrary constant affine form in `y` and applying (7) shows
`M_b(v) succeq 0`. Applying (8) term by term gives

\[
 g_{bj}(\ell_b(v)/h_b(v))\ge0\quad\hbox{when }h_b(v)>0.  \tag{17}
\]

Applying (9) similarly gives `0<=Y_b(v)_{ii}<=h_b(v)`. Hence if `h_b(v)=0`,
all diagonal entries of the positive semidefinite matrix `M_b(v)` vanish,
so `M_b(v)=0`.

Normalization in (15) gives `int h_b dmu^{S_b}=1`. For positive density
define `ybar_b(v)=ell_b(v)/h_b(v)`, and for zero density choose any fixed
point of `P_b`. This is measurable and belongs to `P_b` by (17). Let the
local law sample `v` with density `h_b` relative to `mu^{S_b}` and set its
private vector to `ybar_b(v)`.

The shared marginals of adjacent local laws match exactly. Integrating
out a shared coordinate removes its normalized kernel factor. The
remaining separator density depends only on the corresponding separator
moments, on which the functionals agree. Running intersection therefore
glues the shared bag laws to a global shared law. Each private vector is
then the measurable function `ybar_b(u_{S_b})`. This gives a feasible
global law with precisely the required local distributions.

### Convexity and the objective estimate

For `h=h_b(v)>0`, positive semidefiniteness of `M_b(v)` yields

\[
 Y_b(v)/h-\overline y_b(v)\overline y_b(v)^T\succeq0.
\]

Since `Q_b(v) succeq0`,

\[
 h_b(v)f_b(v,\overline y_b(v))
 \le c_b(v)h_b(v)+a_b(v)^T\ell_b(v)
                         +\operatorname{tr}(Q_b(v)Y_b(v))
 =\sum_{i,j}H_b(v)_{ij}M_b(v)_{ij}.                     \tag{18}
\]

For `h=0`, both sides are zero by `M_b(v)=0`. Integrating (18), expanding
(4), and using the Chebyshev eigenvalue property of `K_m` gives

\[
 \int f_b\,d\nu_b
 \le\sum_{\alpha,i,j}(H_{b\alpha})_{ij}
       \left(\prod_{k\in S_b}g_{\alpha_k}\right)
                            L_b(T_\alpha z_i z_j).       \tag{19}
\]

The absolute difference between the right side and `L_b(f_b)` is at most

\[
 {3\over2m^2+1}\sum_\alpha\|H_{b\alpha}\|_{1,\mathrm{entry}}
                                      \sum_k\alpha_k^2
\]

by (14)--(15) and `1-prod g<=sum(1-g)`. Summing proves (12). Taking the
infimum over feasible functionals proves (13). Compactness and continuity
of the original feasible set imply the stated point-existence conclusion.

## 3. Why the private quadratic bounds are needed

Affine private localizers do not control second moments. With no shared
variables, `P=[-1,1]`, and `L(1)=1,L(y)=0,L(y^2)=R`, the matrix moment
condition and both affine inequalities hold for every `R>=0`. Thus
`|L(y^2)|<=1` is false under (7)--(8) alone.

In fact the failure can be much stronger, as discovered in the
[independent proof review](partial-kernel-proof-review.md#5-stronger-negative-result-when-private-quadratic-bounds-are-omitted).

**Proposition.** Omitting (9) can make the relaxation infimum `-infinity`
at every allowed order for one fixed nonnegative objective convex quadratic
in one private variable.

Take one bag with shared `u=(u_1,u_2,u_3)`, private `y in [-1,1]`, and

\[
 q(u)=u_1^4u_2^2+u_1^2u_2^4+u_3^6-3u_1^2u_2^2u_3^2,
 \qquad f(u,y)=q(u)y^2.
\]

Arithmetic--geometric mean gives `q>=0`, so `f*=0`. Fix any `r>=6` and
let `C_r` be the degree-`2r` shared box preordering. The homogeneous
Motzkin polynomial `q` belongs to no such cone: all box generators equal
one at the interior origin, so the first nonzero homogeneous component
of any representation of `q` would express it as a sum of squares of
cubics. It is not such a sum. Indeed the zero coefficients of `u_1^6`
and `u_2^6` eliminate the pure cubics; the zero coefficients of
`u_1^4u_3^2,u_2^4u_3^2,u_1^2u_3^4,u_2^2u_3^4` then eliminate all cubic
monomials except `u_1^2u_2,u_1u_2^2,u_3^3,u_1u_2u_3`. The coefficient
of `u_1^2u_2^2u_3^2` in a sum of their squares is nonnegative, contradicting
the coefficient `-3`.

The cone `C_r` is closed. To see this, write each weighted SOS using a
PSD Gram matrix and integrate over the cube. Every weighted monomial
moment matrix is positive definite, so bounded polynomial integrals bound
the traces of all Gram matrices; convergent subsequences provide a Gram
representation of any coefficientwise limit. Separation therefore gives
`lambda(C_r)>=0` and `lambda(q)<0`. We may normalize `lambda(1)=1`:
since `r>=6`, moment Cauchy--Schwarz on `1` and `q` implies
`lambda(q)^2<=lambda(1)lambda(q^2)`, so `lambda(1)>0`.

For every `R>=0`, define

\[
 L_R(a(u)+b(u)y+c(u)y^2)=a(0)+R\lambda(c).
\]

Its matrix positivity (7) follows from
`L_R(w_I(q_0+q_1y)^2)=w_I(0)q_0(0)^2+R lambda(w_Iq_1^2)>=0`.
Both affine constraints `1+-y>=0` satisfy (8), since their localizers
have value `w_I(0)q_0(0)^2`. Yet `L_R(f)=R lambda(q)` tends to
`-infinity`. This proves the proposition. The private bounds in (9) are
a substantive safeguard, not just a convenient step in the proof.

Convexity is also indispensable for the theorem. With no shared variables,
let `P={y>=0:y_1+y_2<=1}` and `f(y)=-(y_1+y_2)^2`. The true minimum is
`-1`. The private moment matrix

\[
 \begin{pmatrix}1&1/2&1/2\\1/2&1&1\\1/2&1&1\end{pmatrix}
\]

is positive semidefinite, its mean satisfies the three defining affine
inequalities, and both private second moments equal one. It therefore
satisfies (7)--(9), but its objective is `-4`. Here `A=0`, so removing
convexity would invalidate (13), not merely this particular rounding map.

## 4. Finite shared-grid consequence

Let `d_infty` be the largest individual shared Chebyshev degree among the
entries of (4), with zero for constant coefficients. Set

\[
 N=m+\lfloor d_\infty/2\rfloor,\qquad
 \xi_j=\cos((2j-1)\pi/(2N)),\quad 1\le j\le N.           \tag{20}
\]

At each shared grid point in a bag define the local convex-QP value

\[
 F_b(v)=\min_{y\in P_b} f_b(v,y).                        \tag{21}
\]

The minimum exists, including for singular `Q_b(v)` and lower-dimensional
`P_b`. The matrix polynomial on the right of (18) has individual degrees
at most `2(m-1)+d_infty<=2N-1`. Tensor Chebyshev quadrature integrates it
exactly. The finite probabilities `N^{-k_b}h_b(xi)` have exactly matching
separator marginals. At each positive-density node, (18) also bounds
`h_b(v)F_b(v)` by the same matrix expression. Therefore

\[
 \min_{u\in\{\xi_1,\ldots,\xi_N\}^n}\sum_b F_b(u_{S_b})
       \le\sum_bL_b(f_b)+{3A\over2m^2+1}.               \tag{22}
\]

After computing the local QP values at the `sum_b N^{k_b}` grid nodes,
junction-tree dynamic programming uses `O(t N^s)` arithmetic/comparison
work to minimize their sum. Recovering QP minimizers produces feasible
private vectors. The QP table construction cost is separate. The nodes are
algebraic, the coefficient matrices may be real, and these are mathematical
oracle/exact-arithmetic statements, not claims about rational output,
floating-point reliability, or bit complexity.

The private value functions `F_b` can be nonsmooth when active sets change.
The proof does not approximate those value functions by smooth functions;
it bounds their grid costs through the polynomial matrix expression in
(18). Discretization plus convex optimization is itself established. The
specific content of (22) is its comparison to this finite anisotropic SDP.

The same second-order objective approximation for this grid is available
without the SDP: start from a true global optimizer, keep its private
decisions fixed, and smooth its shared coordinates with the common kernel.
Quadrature and the coefficient bound give the same error for the grid
minimum. Thus a shared-dimension-only grid/QP algorithm is not a consequence
that uniquely depends on the new relaxation theorem. The distinction is
the quantitative lower-relaxation guarantee and the comparison to every
feasible collection of truncated matrix moments.

## 5. Boundaries and remaining work

- A private feasible set depending on the smoothed coordinate is outside
  the theorem. A conditional mean satisfying an averaged affine inequality
  need not satisfy its version evaluated at the new shared coordinate.
- Private variables that appear in multiple bags cannot be replaced by
  independent conditional means by this argument. They must be among the
  consistently smoothed variables or require a separate consistency theory.
- Private integer decisions are outside the conditional-mean argument.
  Exact finite-state treatment may be combined separately with the existing
  [discrete extension](mixed-discrete-extension.md), but is not asserted here.
- The positivity cone includes all shared box-preordering products. No
  corresponding ordinary-quadratic-module result follows automatically.
- A large objective coefficient budget can erase the dimensional advantage
  in an accuracy bound. The theorem makes no dimension-free conditioning
  claim and no generic MINLP complexity claim.
- Moment feasibility is different from a certified lower bound. A feasible
  SOS dual gives a lower bound, and `rho_r` is a theoretical lower bound;
  an arbitrary feasible moment objective need not be one. Lower-dimensional
  polytopes can prevent strict SDP feasibility. No dual-attainment or
  no-duality-gap assertion is needed for the rounding theorem.

The [targeted verification record](partial-kernel-verification.md) documents
exact finite matrix checks, a nonrepresentable private moment example,
objective identities, and negative examples. These computations do not
prove the theorem. No project-wide verification or CI inspection is part
of this topic. The [full independent proof review](partial-kernel-proof-review.md)
found no substantive gap in the augmented theorem or finite-grid statement.
Its stronger unboundedness proposition received a further independent
review. Review conclusions provide evidence rather than formal proof
certification.
A [fresh whole-proof review](partial-kernel-fresh-review.md) also checked
the theorem, the omitted-bound and nonconvexity counterexamples, and the
finite-grid statement; it found no substantive defect.

## 6. Closest prior results and significance

The [independent audit](partial-kernel-prior.md) records the inspected
primary sources and exact assumptions. In particular:

- [Lasserre (2009), Theorem 2.6](https://optimization-online.org/wp-content/uploads/2008/07/2025.pdf)
  proves pseudomoment Jensen for SOS-convex polynomials; the quadratic
  inequality (18) is a basic special case.
- [Guo and Wang (2025), Section 4.2](https://arxiv.org/html/2304.12628v3)
  keep the degree of SOS-convex decision variables fixed while increasing
  moment order in uncertainty variables. Their robust universal-constraint
  model differs from joint minimization with private QPs, and the inspected
  statements do not give this sparse second-order rate.
- [Fang and Fawzi (2021), Theorem 2](https://doi.org/10.1007/s10107-020-01537-7)
  give matrix-size-independent second-order SOS rates on the sphere and
  explicitly cover scalar bidegree `(2d,2)` polynomials. Neither keeping
  one block quadratic nor obtaining a matrix kernel rate is itself new.
- [Miller, Wang, and Guo, Example 5.1](https://arxiv.org/html/2411.15479v3)
  show that a generic sparse matrix hierarchy can fail despite running
  intersection and Archimedean assumptions. This theorem does not glue
  matrix-valued marginals: it glues scalar shared mass densities, with
  private matrix indices eliminated separately in each bag.

The potentially useful expansion is a quantitative sparse lower-relaxation
guarantee for arbitrarily large local convex quadratic blocks without
raising their moment degree. The grid/QP baseline already has the same
approximation exponent and can even give the lower bound `U_N-error` from
its grid optimum `U_N`. An advantage from SDP dual certificates, stronger
intermediate bounds, or integration into branch-and-bound remains a
possible application requiring further work. No publication-priority or
separate-breakthrough claim is justified by the audit.
