# Regular recourse multipliers restore inverse-square sparse rates

Date: 2026-09-28. Completed theorem and scope statement.
The [prior-work audit](active-region-prior.md) distinguishes this hierarchy
result from established parametric QP sensitivity and polynomial recourse
approximation. Publication priority is not established.

## Main point

Affine recourse can force the sparse hierarchy to converge only as
`Theta(1/r)`. That obstruction is not caused by affine feasibility alone.
This note proves an inverse-square bound when the part of the optimal
multiplier that acts on the shared variables has sufficient regularity.
Private variables still appear only through degree two. The hierarchy is
exactly the one in [affine recourse rounding](affine-recourse-kernel-upper.md):
no KKT equations, active-set enumeration, or multiplier variables are added
to its SDP.

There are two useful regularity conditions. In several shared dimensions,
a weighted absolute Chebyshev coefficient bound suffices. For one shared
dimension, Lipschitz continuity suffices, including continuous
piecewise-affine policies from nondegenerate parametric QPs. A
coordinatewise version of this second condition also permits arbitrarily
coupled multivariate polynomial master objectives. The conditions concern
projected multipliers, not the full multiplier vector.

The proof uses KKT inequalities to charge the discrepancy between source
and output shared coordinates. Integrating the discrepancy against the
kernel produces a polynomial commutator. Regularity makes its cost second
order, and explicit preordering degree bounds make that estimate valid for
nonrepresentable pseudomoments. A uniform approximation argument alone
would not justify the last step.

## 1. Model and the unchanged hierarchy

Use the model, constants, and hierarchy (6)--(9) of
[the affine recourse note](affine-recourse-kernel-upper.md). For clarity,
the data are a junction tree of shared bags `S_b`, private continuous
vectors `y_b`, and

\[
 P_b(u)=\{y\in[-1,1]^{p_b}:A_by\le a_b+B_bu\},\qquad
 f_b(u,y)=c_b(u)+q_b(u)^Ty+y^TQ_b(u)y.
\tag{1}
\]

Every fiber is nonempty. The coefficients of `f_b` are polynomial in the
shared coordinates, and `Q_b(u)` is positive semidefinite throughout the
shared box. Write `k_b=|S_b|`, `s=max(1,max_b k_b)`,
`f_b=z^TH_b(u)z`, `z=(1,y^T)^T`, and

\[
 H_b(u)=\sum_\alpha H_{b\alpha}T_\alpha(u),\qquad
 \mathcal A=\sum_{b,\alpha}\|H_{b\alpha}\|_{1,\mathrm{entry}}
                                \sum_i\alpha_i^2,
 \quad d=\max_{b,\alpha:H_{b\alpha}\ne0}|\alpha|.
\tag{2}
\]

Take `d=0` for a zero objective. The local functionals are defined on
shared degree at most `2r` and private degree at most two, normalized,
and agree on separator polynomials through degree `2r`. With
`w_I=prod_(i in I)(1-u_i^2)`, their positivity conditions are

\[
 \begin{split}
 L_b(w_I[q_0(u)+q(u)^Ty]^2)&\ge0,
                        &&\deg q_i\le r-|I|,\\
 L_b(w_Iq(u)^2[a_b+B_bu-A_by]_j)&\ge0,
                        &&\deg q\le r-|I|-1,\\
 L_b(w_Iq(u)^2(1-y_j^2))&\ge0,
                        &&\deg q\le r-|I|.
 \end{split}
\tag{3}
\]

The affine private bounds `1+y_j` and `1-y_j` may be added to the second
line without changing feasible functionals. Indeed,
`1+-y_j=((1+-y_j)^2+(1-y_j^2))/2`, and the first and third lines already
imply their positivity with at least the required degree allowance.

Include these bounds in a single system

\[
 C_by\le e_b+D_bu,
 \qquad C_b=\begin{bmatrix}A_b\\ I\\-I\end{bmatrix},\quad
 e_b=\begin{bmatrix}a_b\\\mathbf1\\\mathbf1\end{bmatrix},\quad
 D_b=\begin{bmatrix}B_b\\0\\0\end{bmatrix}.
\tag{4}
\]

For each shared point `u`, let `F_b(u)=min_(y in P_b(u)) f_b(u,y)`.
Assume a choice of an optimal KKT pair `(y_b^*(u),lambda_b(u))` with

\[
 \lambda_b(u)\ge0,\quad
 q_b(u)+2Q_b(u)y_b^*(u)+C_b^T\lambda_b(u)=0,\quad
 \lambda_b(u)^T(e_b+D_bu-C_by_b^*(u))=0.
\tag{5}
\]

The existence of some finite multiplier at each point follows from the
normal-cone formula for a polyhedron and convex differentiable optimality.
The substantive assumption below is that one can choose these multipliers
so that their projection

\[
                 a_b^{\mathrm{dual}}(u)=D_b^T\lambda_b(u)
\tag{6}
\]

has the stated regularity on the closed shared box. Neither boundedness
nor continuity of the full multiplier vector is required: only the
projection enters the proof. In particular, a continuous projection need
not assert continuity of every active-constraint multiplier.

Set, for `r>=max(s+1,d)`,

\[
 m=\lfloor(r-1)/s\rfloor+1=\lceil r/s\rceil\ge2,
 \quad D_m=2m^2+1,\quad
 V_m=\frac{3(4m-3)}{2m(2m^2+1)}<\frac6{D_m}.
\tag{7}
\]

## 2. Two regularity theorems

**Theorem 1: weighted Chebyshev regularity.** Suppose every component of
(6) has a uniformly absolutely convergent tensor Chebyshev expansion

\[
 a_{bi}^{\mathrm{dual}}(u)=\sum_\alpha a_{bi\alpha}T_\alpha(u),
 \qquad
 \mathcal M=\sum_{b,i,\alpha}|a_{bi\alpha}|
                              \max(1,2\alpha_i)<\infty.
\tag{8}
\]

Every feasible moment collection admits a globally feasible probability
law `nu` with

\[
 \int f\,d\nu\le\sum_bL_b(f_b)
                         +\frac{3(\mathcal A+\mathcal M)}{D_m}.
\tag{9}
\]

Consequently, with `rho_r=inf sum_b L_b(f_b)`,

\[
 0\le f^*-\rho_r
       \le\frac{3(\mathcal A+\mathcal M)}{D_m}
       \le\frac{3s^2(\mathcal A+\mathcal M)}{2r^2}.
\tag{10}
\]

Condition (8) is a directional weighted absolute coefficient condition.
It holds for polynomial projections and for analytic projections with
geometrically decaying tensor coefficients. Mere multivariate Lipschitz
continuity is not asserted to imply it.

**Theorem 2: coordinatewise regularity.** Instead, suppose

\[
 a_{bi}^{\mathrm{dual}}(u)=\phi_{bi}(u_i),\qquad
 \|\phi_{bi}\|_\infty\le M_{bi},\quad
 |\phi_{bi}(v)-\phi_{bi}(w)|\le H_{bi}|v-w|^\beta,
 \quad 0<\beta\le1.
\tag{11}
\]

Then the right side of (9) can be replaced by

\[
 \sum_bL_b(f_b)+\frac{3\mathcal A}{D_m}
       +\sum_{b,i}\left\{\frac{3M_{bi}}{D_m}
                    +H_{bi}V_m^{(1+\beta)/2}\right\}.
\tag{12}
\]

In particular, Lipschitz projections (`beta=1`) give `O(r^-2)`; a
coordinatewise Hölder exponent `beta` gives `O(r^-(1+beta))`. These are
upper bounds. No sharpness assertion is made for intermediate exponents.
When `k_b=1`, coordinatewise dependence is automatic. For larger bags it
is a real restriction on (6), not on the polynomial master term `c_b(u)`.

The private dimension dependence in both results is exactly that of (3):
the largest PSD block has `(p_b+1) binom(r+k_b,k_b)` rows, and the moment
count is at most `binom(p_b+2,2) binom(2r+k_b,k_b)`. Constants in (2),
(8), or (11) can grow with the private dimension and data. These are SDP
dimension and relaxation-gap bounds, not numerical time bounds.

## 3. Proof: a KKT inequality and a polynomial commutator

Use the positive squared-Fejer kernel `K_m` and arcsine probability
measure `mu` from [the kernel theorem](sparse-kernel-rounding.md).
Its Chebyshev multipliers are `g_j`, with `g_0=1`, `g_j=0` for
`j>2m-2`, `0<=g_j<=1`, and `1-g_1=3/D_m`. Put
`K_b(x,v)=prod_(i in S_b) K_m(x_i,v_i)` and define the smoothing operator

\[
          (\mathcal K_b a)(x)=\int K_b(x,v)a(v)\,d\mu^{S_b}(v).
\tag{13}
\]

Suppress the bag index. The degree reserve in (7) allows the conditional
matrix and source means from the affine recourse note:

\[
 h(v)=L(K_b),\quad U(v)=L(K_bx),\quad
 \ell(v)=L(K_by),\quad Y(v)=L(K_byy^T),\quad
 M(v)=\begin{bmatrix}h&\ell^T\\\ell&Y\end{bmatrix}\succeq0.
\tag{14}
\]

For `h(v)>0`, `ubar=U/h` lies in the shared box and
`ybar=ell/h` lies in `P(ubar)`. If `h=0`, then `U=ell=Y=0`.
All these statements follow directly from (3), including the redundant
private square bounds; they do not require a representing measure.

At a fixed output `v`, (5) and private convexity imply for every `y`

\[
 f(v,y)\ge F(v)+\lambda(v)^T[e+Dv-Cy].
\tag{15}
\]

Indeed, subtracting the right side leaves
`(y-y^*(v))^T Q(v)(y-y^*(v))`. Since
`e+D ubar-C ybar>=0` and `lambda(v)>=0`, (15) and the Schur-complement
Jensen inequality give

\[
 h(v)F(v)\le \langle H(v),M(v)\rangle
                   +a^{\mathrm{dual}}(v)^T[U(v)-v h(v)].
\tag{16}
\]

At `h=0` all terms vanish. Integrating the correction term produces

\[
 \begin{split}
 \int a^{\mathrm{dual}}(v)^T[U-vh]\,d\mu(v)&=L(R),\\
 R(x)&=\sum_i\{x_i\mathcal K_b(a_i^{\mathrm{dual}})(x)
                         -\mathcal K_b(v_i a_i^{\mathrm{dual}})(x)\}.
 \end{split}
\tag{17}
\]

The coefficient functions being integrated are bounded under either
theorem, so exchanging integration and the finite-dimensional functional
is valid. Although `a` need not be polynomial, `R` is polynomial. Every
frequency in its tensor Chebyshev expansion has degree at most `2m-2` in
each coordinate except possibly one coordinate of degree at most `2m-1`.
Its total degree is at most `2k_b(m-1)+1<=2r-1`.

The matrix-cost estimate already proved in the affine recourse note is

\[
 \int\langle H_b(v),M_b(v)\rangle\,d\mu(v)
 \le L_b(f_b)+\frac3{D_m}
        \sum_\alpha\|H_{b\alpha}\|_{1,\mathrm{entry}}
                                     \sum_i\alpha_i^2.
\tag{18}
\]

It remains to bound `L(R)` inside the actual truncated cone.

### 3.1. A degree bound for tensor Chebyshev moments

**Lemma 3.** If `sum_i ceil(alpha_i/2)<=r`, every functional satisfying
the scalar shared-box part of (3) obeys `|L(T_alpha)|<=1`.

For each coordinate, `1+-T_(alpha_i)` is a nonnegative polynomial on
`[-1,1]`. The interval representation theorem writes it as
`sigma_0+(1-x_i^2)sigma_1` with SOS multipliers and total degree at most
`2 ceil(alpha_i/2)`. For `z_i=T_(alpha_i)(x_i)` use

\[
 1+\epsilon\prod_{i=1}^kz_i
   =2^{1-k}\sum_{\substack{\eta\in\{-1,1\}^k\\
                            \prod_i\eta_i=\epsilon}}
                         \prod_{i=1}^k(1+\eta_i z_i),
 \qquad \epsilon\in\{-1,1\}.
\tag{19}
\]

Multiplying the univariate certificates yields the full shared-box
preordering, with total degree at most `2 sum_i ceil(alpha_i/2)<=2r`.
Thus `L(1+-T_alpha)>=0`. The empty multi-index is immediate. In
particular Lemma 3 bounds every frequency in (17), because
`sum_i ceil(alpha_i/2)<=k_b(m-1)+1<=r`.

This step is needed: the usual simpler moment bound for `|alpha|<=r`
does not cover all the commutator's frequencies.

### 3.2. Weighted Chebyshev coefficients

For all integers `j>=0`,

\[
 |g_{j+1}-g_j|\le(2j+1)(1-g_1)=\frac{3(2j+1)}{D_m}.
\tag{20}
\]

To see this, write `g_j=int cos(j theta) J_m(theta) dtheta/(2pi)` with
the nonnegative normalized circle kernel `J_m`. The identity
`cos(j theta)-cos((j+1)theta)=2 sin((2j+1)theta/2) sin(theta/2)` and
`|sin(n t)|<=n|sin t|` bound the absolute integrand by
`(2j+1)(1-cos theta)`. Integrate. The proof includes indices beyond
the multiplier support.

For a single tensor basis polynomial `T_alpha`, all factors outside
coordinate `i` contribute `prod_(j!=i) g_(alpha_j)<=1`. If
`alpha_i=k>=1`, the contribution in coordinate `i` is

\[
 \tfrac12(g_k-g_{k+1})T_{k+1}
                +\tfrac12(g_k-g_{k-1})T_{k-1}.
\tag{21}
\]

Its absolute coefficient sum is at most
`(1-g_1)[(2k+1)+(2k-1)]/2=2k(1-g_1)`. For `k=0` the expression is
`(1-g_1)T_1`, giving `1-g_1`. Uniform absolute convergence in (8)
justifies termwise integration; moreover the resulting polynomial has
finite support. Equations (20)--(21) and Lemma 3 give

\[
                  |L_b(R_b)|\le\frac3{D_m}
                    \sum_{i,\alpha}|a_{bi\alpha}|\max(1,2\alpha_i).
\tag{22}
\]

This proves the needed correction estimate for Theorem 1.

### 3.3. Scalar and coordinatewise regularity

Under (11), normalization of the other kernel factors reduces (17) to
`R(x)=sum_i R_i(x_i)`, where

\[
 R_i(x)=\int K_m(x,v)\phi_i(v)(x-v)\,d\mu(v).
\tag{23}
\]

This has degree at most `2m-1`. Add and subtract `phi_i(x)` to obtain

\[
 R_i(x)=\phi_i(x)(1-g_1)x
       +\int K_m(x,v)[\phi_i(v)-\phi_i(x)](x-v)\,d\mu(v).
\tag{24}
\]

Direct kernel integration gives the pointwise displacement estimate

\[
 \int K_m(x,v)(x-v)^2\,d\mu(v)
     =V_m+\frac{3-2m}{a_0}x^2\le V_m,
 \qquad a_0=m(2m^2+1)/3.
\tag{25}
\]

For `0<beta<=1`, concavity of `t^((1+beta)/2)` and the fact that
`K_m(x,v)dmu(v)` is a probability law yield

\[
              R_i(x)\le\frac{3M_i}{D_m}
                           +H_iV_m^{(1+\beta)/2}=:\epsilon_i.
\tag{26}
\]

The polynomial `epsilon_i-R_i` is nonnegative on the interval and has
degree at most `2m-1`. Its interval certificate has degree at most
`2m<=2r`; embedding that certificate into (3) proves
`L(R_i)<=epsilon_i`. This validates the uniform bound for pseudomoments
without assuming a joint representing measure. Summing proves the
correction estimate in Theorem 2.

### 3.4. Global feasibility and completion

The shared laws `h_b dmu^(S_b)` are nonnegative, normalized, and have
matching separator marginals. Running intersection glues them to a
global shared law. Each fiber is nonempty and compact. Assign a Borel
minimizer `y_b^*(u)` to each bag to obtain a globally feasible law with
cost `sum_b int h_b F_b`.

One can justify this selection without any regularity of the chosen
KKT multipliers. The fixed-matrix Hoffman bound makes the fibers
Hausdorff-continuous. For `epsilon>0`, the unique minimizer of
`f_b(u,y)+epsilon||y||_2^2` is continuous, by compactness and strict
convexity. As `epsilon` decreases to zero, these minimizers converge
pointwise to the minimum-norm minimizer of `f_b(u,.)`; compare their
optimality inequalities with any unregularized minimizer and pass to
subsequences. The pointwise limit is Borel and is an optimal choice.

Integrate (16), use (18) and the applicable correction estimate, and sum
over bags. The original feasible set is compact, so its minimum is no
larger than the expected rounded cost. Taking the infimum over moment
points proves the claimed gap. No SDP attainment or strong duality is
needed.

## 4. Parametric QPs, active regions, and sharp limitations

For constant positive-definite `Q`, affine `q`, and affine RHS, classical
multiparametric QP theory gives piecewise-affine primal and multiplier
policies. LICQ throughout an open feasible neighborhood of the closed
master box gives continuous piecewise-affine multipliers on that box,
hence Lipschitz multipliers there. For a scalar shared parameter,
Theorem 2 therefore supplies the inverse-square bound. The open
neighborhood avoids silently extending an interior differentiability
statement to a boundary. These regularity facts are prior work; see
[the audit](active-region-prior.md) for Tøndel--Johansen--Bemporad (2003)
and Baotić (2016), exact statements, and qualifications.

For a general multivariate parameter, continuous piecewise-affine
multipliers are Lipschitz, but this note does not deduce (8) from that
fact. Oblique active-region boundaries are not covered automatically by
Theorem 2 either. The stated result is restricted to (8) or (11); it is
not a general multivariate Lipschitz-multiplier theorem.
When every bag has at most one shared coordinate, the master problem is
separable across shared coordinates: distinct coordinates meet only
through empty separators. The scalar theorem still permits many large
private blocks coupled by one common parameter, but is not a theorem
for general multivariate shared networks.

On a fixed critical region, affine primal and multiplier policies give
an exact quadratic KKT identity for eliminating each QP block. Branching
over critical regions is an established alternative. This note does not
claim that enumerating regions is new or that the hierarchy dominates
explicit multiparametric programming; there can be many regions, and no
comparison of practical effort has been established.

### A sharp regular affine-recourse example

Let `u in [-1,1]`, `x,z in [0,1]`, impose `z>=u`, and minimize

\[
                f(x,u,z)=x^2-2ux+z^2
\tag{27}
\]

with bags `(x,u)` and `(u,z)`. Their conditional minima are
`-h(u)` and `h(u)`, where `h(u)=max(u,0)^2`, so `f*=0`. The first bag
has fixed private feasibility and zero projected multiplier. In the
second bag, take multiplier `2 max(u,0)` on `u-z<=0` and zero on the
other rows. Its projected multiplier is `-2 max(u,0)`, which is Lipschitz
with constant two. Boundary multipliers may be chosen this way as well.
The private interval `[0,1]` is an affine scaling of the model's box.
With `x=(1+xi)/2` and `z=(1+zeta)/2`, the constants in Theorem 2 are
`A=2`, `M=2`, and `H=2`; all other projected-multiplier constants are
zero. Thus, for this scaled anisotropic hierarchy and `r>=2`,

\[
                  -\rho_r\le \frac{12}{2r^2+1}+2V_r
                            <\frac{24}{2r^2+1}<\frac{12}{r^2}.
\tag{27a}
\]

Conversely, the exact local measures from
[quadratic sharpness](quadratic-sharpness.md) lift as
`x=max(u,0)` and `z=max(u,0)` on the two bags. Their cost is
`-int h dmu_1+int h dmu_2`. Matching moments through `2r` therefore gives
the same lower bound

\[
                    -\rho_r\ge\frac{2}{27\pi(2r+2)^2}.
\tag{28}
\]

Actual measures satisfy every constraint in (3), so this lower bound
applies to the stated anisotropic hierarchy. Consequently its rate on
this fixed regular affine-recourse problem is exactly `Theta(r^-2)`.
This example extends the existing separator approximation construction;
it is not a new approximation-theoretic lower bound.

### Strict convexity is insufficient

The QP

\[
                  \min_{|u|\le z\le1} z^2+z=u^2+|u|
\tag{29}
\]

has complete recourse and a constant positive-definite Hessian. Its
primal solution `z=|u|` is Lipschitz. The projected multipliers jump at
zero, and the value has a corner there. Thus neither strict convexity,
Lipschitz primal decisions, nor complete recourse implies the multiplier
regularity used above. The companion
[inverse-order example](affine-recourse-rate-boundary.md) establishes an
actual `Theta(1/r)` sparse gap, not merely a failure of this proof.

## 5. Significance, verification, and scope

The candidate contribution is a quantitative link between recourse dual
regularity and the rate of this unchanged sparse SDP with fixed private
degree. Generic smoothness-based polynomial approximation, QP sensitivity,
sparse KKT reformulations, and asymptotic polynomial recourse approximation
are established. The proof here uses their structure to avoid increasing
the private degree and to control the commutator inside the actual
truncated preordering. The literature audit found no exact equivalent,
which does not establish novelty.

The result could justify smaller relaxation orders for regular recourse
blocks in a global nonconvex polynomial master problem. Exploiting it in a
solver requires usable bounds on (8) or (11), well-conditioned numerical
SDPs, and a certified extraction or upper-bound procedure. The theorem's
proof invokes optimal multiplier policies; the SDP does not need those
policies as inputs, but an explicit numerical error guarantee needs their
regularity constants. The bound alone does not provide an efficient way
to compute those constants or to certify regularity from arbitrary data.

The claims here require the full shared-box preordering, exact separator
moment consistency, complete affine recourse, and continuous private
variables. Ordinary quadratic modules, arbitrary multivariate Lipschitz
projections, inexact moments, and private integer decisions are outside
these theorems. No application speedup or automatic data-level regularity
test is claimed.

The [verification record](active-region-verification.md) gives the actual
targeted commands, their results, and their limits. A
[fresh adversarial review](active-region-fresh-review.md) checks the proof
separately. In particular, Lemma 3 handles commutator frequencies whose
total degree exceeds `r`; replacing it by the simpler bound restricted
to `|alpha|<=r` would leave a genuine proof gap. Finite symbolic checks
corroborate the certificate and kernel identities. They do not replace
the proofs for arbitrary orders, infinite coefficient series, or the
measurable selection argument. No Lean formalization, project-wide
verification, or CI inspection was used for this result.
