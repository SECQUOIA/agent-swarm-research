# Affine recourse can reduce the sparse certificate rate to inverse order

Date: 2026-09-28. Research result with an independent
[proof review](affine-recourse-proof-review.md) and
[prior-work and significance audit](affine-recourse-prior.md).
Publication priority is not established.

## Main point

The fixed-private-domain assumption in
[partial kernel rounding](partial-kernel-rounding.md) has quantitative
content. Allowing a private feasible polytope to depend affinely on a shared
coordinate can force a sparse full-preordering hierarchy to converge only
as `Theta(1/r)`. This happens with three continuous variables, two bags of
size two, a quadratic objective, and linear private programs. The example
does not show a difficulty intrinsic to optimizing this problem: merging
the two bags gives an exact degree-three preordering certificate.

The obstruction already holds when each local relaxation is replaced by
an actual probability measure. It is the limited polynomial information
passed across the separator. Convexity of every private subproblem does
not remove it. This is a precise boundary on extending the inverse-square
theorem to general affine recourse; it is not a lower bound on MINLP
algorithms or on all formulations of this problem.

## 1. A two-bag problem and its hierarchy

Consider

\[
 \min f(x,y,z)=-xy+z,
 \qquad -1\le x,y\le1,\quad 0\le z\le1,
 \qquad z-y\ge0,\ z+y\ge0.                         \tag{1}
\]

The bags are `B_1={x,y}` and `B_2={y,z}`, with separator `{y}`.
The local feasible sets have generating lists

\[
 G_1=(1-x^2,1-y^2),\qquad
 G_2=(1-y^2,z,1-z,z-y,z+y).                         \tag{2}
\]

For each list, its degree-`2r` full preordering consists of sums
`sum_I sigma_I prod_{i in I} g_i`, where `I` ranges over subsets of the
list, each `sigma_I` is a sum of squares, and every summand has degree at
most `2r`. Let `T_{b,r}` denote this cone.

The moment relaxation has linear functionals `L_b` on bag polynomials of
degree at most `2r`, normalized by `L_b(1)=1`, nonnegative on `T_{b,r}`,
and satisfying `L_1(y^j)=L_2(y^j)` for `0<=j<=2r`. Define

\[
 \rho_r=\inf\{-L_1(xy)+L_2(z): (L_1,L_2)
                  \text{ satisfy these conditions}\}.          \tag{3}
\]

The sparse certificate bound is

\[
 \lambda_r=\sup\{\lambda:
                 f-\lambda\in T_{1,r}+T_{2,r}\}.                \tag{4}
\]

Weak duality gives `lambda_r<=rho_r<=f*=0`. Indeed, each fixed `y`
has private minima `min_x(-xy)=-|y|` and `min_z z=|y|`, so the
global optimum is zero. Both private subproblems are linear programs.
No strong SDP duality or attainment assertion is needed below.

**Theorem 1.** For every integer `r>=2`,

\[
 \frac{1}{9\pi(r+1)}
 \le -\rho_r\le -\lambda_r
 \le \frac{2\sqrt6}{\sqrt{2r^2+1}}
 \le\frac{2\sqrt3}{r}.                               \tag{5}
\]

In particular, both sparse gaps have exact order `Theta(1/r)`, and neither
hierarchy is finitely exact. The constants in (5) are not sharp.

## 2. Exact local measures and best uniform approximation

Write

\[
 E_n=\inf_{p\in\mathbb R[y]_{\le n}}
                  \max_{-1\le y\le1}\bigl||y|-p(y)\bigr|.       \tag{6}
\]

Replace the moment functionals by actual probability measures on their
respective local feasible sets, and require only equal separator moments
through degree `n`. Call this optimum `eta_n`.

**Proposition 2.** For every integer `n>=0`,

\[
                         \eta_n=-2E_n.                         \tag{7}
\]

To prove this, let `alpha,beta` be the separator marginals of the two
local measures. Conditional minimization bounds the objective below by
`-int |y| d alpha + int |y| d beta`. This bound is attained by lifting
`alpha` to `x=sign(y)` and `beta` to `z=|y|`; take `sign(0)=0`.
Thus the negative of `eta_n` is the greatest difference in expectations
of `|y|` between probability measures agreeing on polynomials of degree
at most `n`. For any such measures and any polynomial `p` of that degree,

\[
 \left|\int |y|\,d(\alpha-\beta)\right|
 \le2\|\,|y|-p\,\|_\infty.
\]

For the reverse inequality, Hahn--Banach applied to the distance from
`|y|` to the finite-dimensional subspace `R[y]_{<=n}` gives a norm-one
linear functional annihilating that subspace and taking value `E_n` on
`|y|`. By the Riesz representation theorem it is a signed measure `sigma`
of total variation one. Its total mass is zero because constants belong
to the subspace. Its positive and negative parts therefore each have mass
one-half. Take `alpha=2 sigma_+`, `beta=2 sigma_-`. This attains `2E_n`.
The standard functional-analytic duality is included to fix the factor
two; it is not claimed as new.

Every feasible pair of such measures for `n=2r` is feasible for (3), so

\[
                        \rho_r\le-2E_{2r}.                      \tag{8}
\]

The lower bound consequently cannot be removed by strengthening only
the local positivity tests while retaining finite-degree separator
matching.

## 3. An elementary inverse-degree lower bound

**Lemma 3.** For `n>=0`,

\[
                    E_n\ge\frac1{9\pi(n+2)}.                   \tag{9}
\]

Let `N` be the even integer with `n+1<=N<=n+2`. With circle integrals
normalized by `d theta/(2 pi)`, define the Fejer kernel

\[
 F_N(t)=1+2\sum_{j=1}^{N-1}(1-j/N)\cos(jt),\qquad
 Q_N(\theta)=-\cos(2N(\theta-\pi/2))F_N(\theta-\pi/2).
                                                               \tag{10}
\]

The Fejer kernel is nonnegative and has integral one. Hence
`int |Q_N|<=1`. Every Fourier frequency of `Q_N` is at least `N+1>n`,
so `int p(cos theta) Q_N(theta)=0` for every polynomial `p` of degree
at most `n`.

The cosine Fourier coefficients in
`|cos theta|=c_0+sum_{k>=1}c_k cos(k theta)` are zero for odd `k`, and

\[
 c_k=-\frac{4\cos(k\pi/2)}{\pi(k^2-1)}
                     \quad\text{for even }k\ge2.               \tag{11}
\]

Integrating directly over the two half-circles proves (11). Therefore

\[
 \int |\cos\theta|\cos(k(\theta-\pi/2))
                     \frac{d\theta}{2\pi}
       =-\frac{2}{\pi(k^2-1)}
                 \quad\text{for even }k\ge2.                  \tag{12}
\]

Expand (10) by the cosine product identity. The even-frequency terms
have positive weights after the signs in (12) cancel. Those weights sum
to

\[
 1+2\sum_{\substack{1\le j<N\\j\text{ even}}}(1-j/N)=N/2.
                                                               \tag{13}
\]

Their frequencies are less than `3N`, so

\[
 \int |\cos\theta|Q_N(\theta)\frac{d\theta}{2\pi}
 \ge \frac2{9\pi N^2}\frac N2
 =\frac1{9\pi N}\ge\frac1{9\pi(n+2)}.                         \tag{14}
\]

Subtract `p(cos theta)` inside the integral and use `int |Q_N|<=1`.
Taking the infimum over `p` proves (9). Equations (8)--(9) give the
leftmost bound in (5). Classical approximation theory gives much sharper
information on `E_n`; this elementary bound is sufficient here.

## 4. A matching sparse preordering certificate

Use the normalized nonnegative kernel `K_m(y,t)` and circle density
`J_m` constructed in [the scalar kernel note](sparse-kernel-rounding.md),
Section 3. The kernel has polynomial degree `2m-2` in each argument,
preserves constants, and its first Chebyshev multiplier satisfies

\[
                 1-g_1=3/(2m^2+1).                            \tag{15}
\]

Let `mu` be normalized arcsine measure and set

\[
 s_m(y)=\int K_m(y,t)\operatorname{sign}(t)\,d\mu(t),\qquad
 \delta_m=2\sqrt{6/(2m^2+1)},\qquad
 p_m(y)=ys_m(y)+\delta_m.                              \tag{16}
\]

Positivity and normalization give `|s_m|<=1`. Symmetry makes `s_m` odd,
so its degree is at most `2m-3`, and `deg p_m<=2m-2`.

For a fixed `y=cos theta`, the kernel distribution of `t` can be sampled
as `t=cos(theta+T)`, where `T` has circle density `J_m`. This follows
from the symmetrized-kernel formula in the scalar note. Since

\[
 |\cos(\theta+T)-\cos\theta|^2
               \le2(1-\cos T),
\]

Cauchy--Schwarz and (15) imply

\[
 \int |t-y|K_m(y,t)\,d\mu(t)
               \le\sqrt{2(1-g_1)}
               =\sqrt{6/(2m^2+1)}.                            \tag{17}
\]

Pointwise, `0<=|y|-y sign(t)<=2|t-y|`; thus

\[
              0\le |y|-ys_m(y)\le\delta_m.                    \tag{18}
\]

In particular, `p_m(y)>=|y|`. The following identity separates the
objective using a polynomial solely on the separator:

\[
 f+\delta_m
 =\underbrace{p_m(y)-xy}_{A_m(x,y)}
  +\underbrace{z-p_m(y)+\delta_m}_{B_m(y,z)}.                  \tag{19}
\]

For the first bag,

\[
 A_m=\frac{1+x}{2}(p_m-y)+\frac{1-x}{2}(p_m+y).                 \tag{20}
\]

Each `p_m +/- y` is nonnegative on `[-1,1]` and has degree at most
`2m-2`. The univariate interval positivity theorem represents it as
`sigma_0+(1-y^2)sigma_1` with each displayed term of degree at most
`2m-2`. Also

\[
 \frac{1\mathbin{\pm}x}{2}
       =\frac{(1\mathbin{\pm}x)^2}{4}
                             +\frac{1-x^2}{4}.                \tag{21}
\]

Products of sums of squares are sums of squares. Expanding (20)--(21)
therefore gives `A_m in T_{1,m}`, with degree at most `2m`.

For the second bag,

\[
 B_m=z-ys_m
 =\frac{1+s_m}{2}(z-y)+\frac{1-s_m}{2}(z+y).           \tag{22}
\]

The polynomials `(1 +/- s_m)/2` are nonnegative on the interval. Pad
their degree bound to the even number `2m-2` and use the same univariate
representation. Multiplication by `z-y` or `z+y` produces allowed
preordering products, involving at most the generators `1-y^2` and one
of `z-y,z+y`, of degree at most `2m-1`. Hence `B_m in T_{2,m}`.
Taking `m=r` in (19) proves `lambda_r>=-delta_r`, and finishes the
proof of Theorem 1. This is a full-preordering statement: the products
`(1-y^2)(z +/- y)` are explicitly used.

## 5. What the obstruction means for a solver

The same polynomial has the global certificate

\[
 f=\frac{(1+x)^2}{4}(z-y)
   +\frac{(1-x)^2}{4}(z+y)
   +\frac12(1-x^2)z.                                         \tag{23}
\]

Every term belongs to the dense preordering for the union of (2), with
degree at most three. Thus merging the two bags makes order two exact.
The obstruction is specifically to maintaining the original two-bag
decomposition and polynomial separator information.

There is also no exact decomposition `f=a(x,y)+b(y,z)` with polynomial
`a,b` nonnegative on their local feasible sets. Comparing the polynomial
identity forces `a=-xy+p(y)`, `b=z-p(y)` for a polynomial `p`. Local
nonnegativity then forces both `p(y)>=|y|` and `p(y)<=|y|` on the
interval, which is impossible for a polynomial. This gives a qualitative
explanation of infinite nonexactness; (5) strengthens it to a sharp
exponent.

A split at the active-set change `y=0` also gives an exact certificate
of degree at most three in each branch while retaining the original bags.
On `y>=0`, add the valid local generator `y` and write
`f=(z-y)+y(1-x)`. On `y<=0`, add `-y` and write
`f=(z+y)+(-y)(1+x)`. Formula (21) represents the last factor in each
branch; the resulting terms have degree at most three. Thus two branch
certificates at order two remove a gap that otherwise decays only as
`Theta(1/r)`. This is a proved property of this instance, not a generic
branch-selection algorithm.

Another response is to include the additional shared function `|y|` in
separator communication. Exact agreement on `int |y|` eliminates the
local-measure gap immediately. Its implementation may require a new
representation or a larger bag, and a general recourse value function
can have many active regions. These observations motivate active-region
branching or selective bag merging, but their practical value has not
been tested.

The example has no integer variables. It is a subclass obstruction for
sparse continuous polynomial relaxations used in MINLP, not a theorem
about private integer averaging. It proves that a universal inverse-square
extension to affine shared-dependent private constraints is false. It
does not prove a universal inverse-order upper rate for all such problems.

## 6. Closest prior results and significance

The [independent literature audit](affine-recourse-prior.md) records
sources, assumptions, conclusions, and search limits. A close prior is
[Nie, Qu, Tang, and Zhang, Example 6.7](https://arxiv.org/html/2406.06882v2):
two bags on three variables already give failure of finite sparse
exactness with a dense degree-four SOS certificate. Their private convex
quadratic minima force a rational, nonpolynomial separator. Thus the
qualitative sparse/dense separation and its separator explanation are
established; the candidate addition here is the sharp inverse-order rate
under affine LP recourse.

The exact moment-matching duality (7) is explicitly stated in
[Han, Jiao, and Weissman, Lemma 25](https://proceedings.mlr.press/v75/han18b/han18b.pdf).
[Bernstein's classical absolute-value approximation theorem](https://history-of-approximation-theory.com/fpapers/acta37.pdf)
gives a positive limit `beta=lim_(r->infinity) 2r E_(2r)`. Therefore the
ideal local-measure gap is asymptotic to `beta/r`. This does not identify
the leading constant of either finite SDP gap in (5). Neither the duality
nor the inverse-degree approximation of the absolute value is new.

Polynomial separator approximation also has direct precedents in
[Fix and Agarwal's continuous graphical models](https://www.cs.cornell.edu/~afix/Papers/ECCV14.pdf)
and [Korda, Magron, and Rios-Zertuche's sparse hierarchy rates](https://d-nb.info/1330825241/34).
The former gives approximation bounds for polynomial and piecewise
polynomial messages with Lipschitz potentials on product domains. The
latter constructs positive bag polynomials by approximating separator
value functions and proves general sparse convergence rates. The inspected
statements do not establish this fixed-instance matching lower rate.
Jackson kernels and univariate interval positivity are also established
ingredients.

The strongest defensible claim is a focused quantitative boundary theorem:
finite polynomial separator matching alone can impose inverse-order
convergence even when all local measures are exact, and the stated sparse
preordering attains that exponent. It does not by itself establish a
substantial general advance in MINLP solving. Detecting such obstructions,
selecting a useful richer separator representation, and balancing its cost
against bag merging remain necessary for a general solver method. No
identical theorem was located in the inspected sources, but that negative
search result does not establish novelty.

## 7. Verification and open questions

The [independent proof review](affine-recourse-proof-review.md) checked
all main arguments and found no proof gap. It identified the unnecessary
second additive `delta_m` in the initial certificate. Removing it halves
the upper constant. Both the author and reviewer independently checked the
corrected identity and degree bounds. The review also checked the two
sign-branch certificates.

The targeted script
[check_affine_recourse_rate.py](check_affine_recourse_rate.py) passed with
results in [affine-recourse-verification.json](affine-recourse-verification.json).
It checked six symbolic polynomial identities; exact rational Fourier
frequency and correlation estimates for `n=0,...,80`; exact kernel
normalization, the first multiplier, and parity for seven orders from two
through 64; and numerical kernel bounds on 20,001 points per order.
Finite-grid minimax LPs for degrees 2, 4, 8, 16, and 32 produced matching
numerical probability measures with maximum Chebyshev moment residual
below `8e-15`. Their values of `n E_n` increased from approximately
`0.25` to `0.2800`, consistent with inverse-degree decay.

The rational and symbolic checks are exact for the finite cases tested.
The sampled inequalities and LPs are numerical diagnostics, not rigorous
uniform bounds. None of these computations proves the arbitrary-order
theorem, mechanically checks the functional-analytic representation
theorems, or verifies interval-SOS certificates at every order. No Lean
proof was attempted; the main verification is the direct proof with an
independent adversarial review.

Commands actually run for the final version were
`python research-20260928/solver/check_affine_recourse_rate.py` (exit 0;
JSON output also saved using shell redirection) and
`git diff --check -- research-20260928/solver/affine-recourse-rate-boundary.md research-20260928/solver/check_affine_recourse_rate.py`
(exit 0; a tracked-diff whitespace check). Source and instruction reads
used `rg`, `cat`, and `sed`. No project-wide verification or CI inspection
was run.

Three useful open questions remain. First, can the exact leading constant
of the finite SDP gap be related to Bernstein's constant? Second, which
regularity and geometry assumptions on shared-dependent private feasible
sets restore a faster convergence rate? Third, can a solver detect a
small set of active-region boundaries or nonlinear separator statistics
that removes this obstruction without unnecessarily increasing bag size?
The example's exact cancellation of opposite private value functions
also leaves robustness to perturbations and isolated minimizers open.
