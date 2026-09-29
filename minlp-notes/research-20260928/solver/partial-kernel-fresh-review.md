# Fresh adversarial review of partial-kernel rounding

Date: 2026-09-28. Reviewer: `partial_kernel_fresh_review`, independent of
the author. Reviewed [partial-kernel-rounding.md](partial-kernel-rounding.md)
and the kernel construction in [sparse-kernel-rounding.md](sparse-kernel-rounding.md).
A separately delegated reviewer checked the finite-grid consequence.

The theorem and finite-grid consequence pass this review under their stated
assumptions. I found no substantive proof gap. This is independent mathematical
review plus targeted exact checks, not formal verification or a novelty
determination. The main restrictions are substantial: private variables are
continuous, belong to fixed separate polytopes, and enter a pointwise convex
quadratic objective. Shared-dependent feasible sets are not covered.

## 1. Rectangular degrees and SDP dimensions

The functional's domain is genuinely rectangular: shared total degree at
most `2r`, and private total degree at most two. A product of two affine
private expressions remains in that domain regardless of the number of
private variables. For a shared generator set `I`, the square basis degree
`r-|I|` gives complete shared degree at most `2r` in all three localizers.
Thus using that same basis degree in the affine and redundant quadratic
private localizers is correct. Private degree does not consume the shared
degree budget.

For `k` shared and `p` private variables, the matrix basis in (7) has
`(p+1) binom(r-|I|+k,k)` elements. The affine and redundant quadratic
localizers use `binom(r-|I|+k,k)` elements. The entire rectangular domain
has `binom(p+2,2) binom(2r+k,k)` monomials. These formulas also cover
`p=0` and `k=0`. They establish polynomial dependence on `p` at fixed
shared width; the required accuracy order still depends on the coefficient
budget, which can grow with `p`.

The tensor kernel representation needs square degree at most
`k(m-1)-|I|`. Since `m-1=floor(r/s)` and `k<=s`, this is at most
`r-|I|`. Multiplying those scalar squares by a constant affine expression
in the private vector uses exactly (7), with no missing private-degree
allowance. The full shared preordering is used here.

## 2. Mixed moments and the role of the quadratic bounds

For `|alpha|<=r`, the Chebyshev telescoping identity places
`1-T_alpha^2` in the allowed shared quadratic module. Therefore
`0<=L(T_alpha^2)<=1`. The quadratic private localizer supplies

\[
0\le L(T_\alpha^2 y_i^2)\le L(T_\alpha^2)\le1.
\]

The lower inequality comes from (7); the upper one comes from (9).
Both are needed in the stated Cauchy--Schwarz argument. The PSD form on
shared-degree-`r`, private-affine polynomials then gives

\[
|L(T_\alpha z_i z_j)|^2
\le L(T_\alpha^2 z_i^2)L(z_j^2)\le1,
\]

including either zero index. This verifies (14) without a representing
measure. Requiring `r>=d` is sufficient; merely requiring the objective
to belong to the degree-`2r` domain would not justify this proof.

The simple counterexample with `L(y)=0` and arbitrary `L(y^2)=R` correctly
shows that affine private localizers alone do not give this bound. The
stronger counterexample added during review establishes all-order
unboundedness for one fixed instance; Section 8 independently checks that
addition. It does not imply failure for every special instance class.

## 3. Conditional matrices and zero density

For fixed output `v`, apply (7) to every shared kernel square and an
arbitrary constant affine form in `y`. Summing proves `M(v)>=0`.
For an affine inequality `g(y)=beta_0+beta^T y`, (8) gives

\[
\beta_0 h(v)+\beta^T\ell(v)=L(K(u,v)g(y))\ge0.
\]

Dividing by positive `h(v)` proves every inequality defining `P`.
Paired inequalities impose equalities as well, so lower-dimensional
polytopes create no feasibility gap in this step.

The same kernel expansion with (9) gives `Y_ii(v)<=h(v)`.
PSD gives all diagonal entries nonnegative. If `h(v)=0`, every diagonal
entry of `M(v)` is zero; PSD implies every off-diagonal entry is zero
through `|M_ij|^2<=M_ii M_jj`. Thus `M(v)=0` as asserted.

On `h>0`, the conditional mean is a ratio of polynomial functions. On the
closed zero set, it is assigned one fixed feasible point. This is a Borel
measurable feasible function. No selection theorem for optimizing private
variables is needed for the probability-law theorem.

## 4. Convexity, objective comparison, and gluing

The Schur complement gives `Y/h-(ell/h)(ell/h)^T>=0`.
Since `Q(v)>=0`, its trace product with that matrix is nonnegative.
This is exactly the inequality needed for conditional averaging; neither
`H(v)>=0` nor an SOS certificate for `Q` is required. The zero-density
case follows from the preceding matrix calculation.

Integrating the matrix surrogate uses only finite polynomial sums. The
kernel eigenvalue identity damps each shared Chebyshev coefficient by
`prod_i g_{alpha_i}`. Zero multipliers above the kernel support cause no
problem. Their associated mixed moments are still defined and bounded
because `|alpha|<=d<=r`. The entrywise matrix norm correctly counts both
off-diagonal coefficients: the two copies of `a_i/2` sum to `|a_i|`.
The stated coefficient budget and one-sided error bound follow.

Shared marginalization removes normalized kernel factors. The residual
separator polynomial has shared total degree at most `2r`, so adjacent
moment agreement implies equality of complete separator distributions.
Running intersection then permits the standard conditional-distribution
gluing on the shared variables. Defining each distinct private vector as
its bag's conditional-mean function preserves all required local laws.
No agreement of private moments across bags is needed because no private
variable occurs in another bag.

The assembled law is feasible for the original product domain, which
gives the bound on `rho_r` by taking an infimum over feasible functionals.
It does not require SDP attainment, strict feasibility, or strong duality.
The distinction between a feasible moment objective and a certified lower
bound remains essential and is stated correctly in the draft.

## 5. Finite grid and extraction

For `N=m+floor(d_infty/2)`, the difference

\[
(2N-1)-\bigl(2(m-1)+d_\infty\bigr)
\]

is one for even `d_infty` and zero for odd `d_infty`. Thus tensor
Gauss--Chebyshev quadrature integrates the matrix surrogate exactly.
It also integrates the density and each removed kernel factor exactly.
The finite nonnegative masses therefore normalize and have matching
separator marginals.

At a zero-density node, both the surrogate and `h(v)F_b(v)` vanish.
At a positive-density node, minimizing over `P_b` can only improve the
conditional-mean value. Finite tree gluing consequently gives the claimed
comparison of the optimal grid cost with each feasible moment objective.

Let `t` denote the number of bags. Even with arbitrary tree degrees,
dynamic programming uses at most a constant times

\[
\sum_b(1+\#\mathrm{children}(b))N^{k_b}
\le(2t-1)N^s
\]

arithmetic/comparison operations after the local tables exist. A minor
notation improvement is to define `t` explicitly in the theorem note.
Private QP minima exist on every nonempty compact polytope, including
singular Hessians and lower-dimensional polytopes. Exact oracle access is
an adequate stated model; the theorem does not establish reliable floating
point extraction or polynomial bit complexity.

## 6. A direct grid bound limits the significance claim

The grid's second-order approximation rate itself does not require the
SDP. The delegated review supplied the following argument, which I checked
independently. Write `u_i=cos(theta_i)` and use the full circular angular
lattice with spacing `Delta=pi/N` and points
`(2j-1)pi/(2N)`. Its cosines are the `N` grid nodes. For each `theta_i`,
choose the two neighboring angular points with barycentric probabilities,
and round different coordinates independently. Linear interpolation and
the bound on the second derivative of `cos(k theta)` give

\[
|\mathbb E\cos(k\Theta_i)-\cos(k\theta_i)|
\le\frac{k^2\Delta^2}{8}.
\]

This remains valid near angles zero and pi: neighboring lattice points
may lie outside `[0,pi]`, but their cosines are still grid nodes. Product
telescoping gives

\[
|\mathbb E T_\alpha(V)-T_\alpha(u)|
\le\frac{\pi^2}{8N^2}\sum_i\alpha_i^2.
\]

Freeze an original global minimizer's private vectors. Since `|z_i|<=1`,
its coefficient `z_b^T H_{b alpha}z_b` has absolute value at most the
entrywise norm used in `A`. Optimizing the private vectors again at each
rounded shared point can only improve the cost. Therefore

\[
0\le\min_{u\text{ on the grid}}\sum_bF_b(u_{S_b})-f^*
\le\frac{\pi^2A}{8N^2}.
\]

This elementary argument even dispenses with private convexity; convexity
makes the table problems convex QPs. It does not compare the grid with a
finite SDP objective or provide that SDP's convergence certificate.
Accordingly, the draft's emphasis on the anisotropic SDP comparison is
appropriate. No novelty claim about this direct argument or the main
theorem follows from the review.

## 7. Targeted exact checks and their limits

Ran:

```text
python research-20260928/solver/check_partial_kernel_review.py
```

Result: all checks passed. The script uses exact SymPy arithmetic and
verifies all localizing matrices for one order-one rectangular example
with one shared and two private variables. The private polytope is the
segment `y1+y2=1` inside `[-1,1]^2`. Its moment functional satisfies
every relaxation constraint but has
`L((y1+y2-1)^2)=1`, so it cannot have a representing measure on that
polytope. This tests a relevant case beyond feasible-point averaging.

For this functional, the script verifies the conditional affine equality,
normalization, objective damping, a positive symbolic conditional-convexity
gap, and exact grid quadrature. A separate one-atom construction verifies
that a vanishing kernel density gives a zero conditional matrix. Integer
enumeration checks 1,807 kernel-certificate degree cases, including empty
bags, and checks both quadrature parities.

After the stronger negative propositions were added, I reran the same
command successfully with exact checks of the Motzkin coefficient
eliminations and the nonconvex triangle's moment matrix and objective.

These checks establish exact identities and finite-instance feasibility.
They do not establish the general theorem, the interval positivity theorem,
all possible tree gluings, novelty, or numerical conditioning. No Lean
formalization, project-wide verification, or CI inspection was performed.

## 8. Independent recheck of the stronger negative propositions

During review the author added a proposition that omitting (9) makes
the relaxation unbounded below for the fixed objective

\[
f(x,y)=q(x)y^2,\qquad
q(x)=x_1^4x_2^2+x_1^2x_2^4+x_3^6-3x_1^2x_2^2x_3^2.
\]

I independently checked the argument before reading the companion proof
review, then checked the revised theorem note and that review. The
proposition passes.

First, AM--GM makes `q>=0` everywhere, so the original objective is
convex quadratic in its scalar private variable and has optimum zero.
Every shared box weight has value one at the origin. Consequently the
lowest nonzero homogeneous part of a box-preordering representation is
a nonzero sum of squares of the lowest homogeneous parts of its square
polynomials. A representation of this homogeneous sextic would therefore
make `q` an SOS of cubics. The coefficient eliminations in the draft are
valid: the vanishing pure sixth powers remove `x_1^3,x_2^3`; the four
listed vanishing mixed monomials then remove `x_1^2x_3,x_2^2x_3,
x_1x_3^2,x_2x_3^2`. The negative `x_1^2x_2^2x_3^2` coefficient becomes
impossible. This argument excludes every finite preordering degree.

The finite-order cone's closedness needs care because arbitrary linear
images of PSD cones need not be closed. Here the stated integral argument
does supply the missing fact. For each fixed order and each weight, the
integrated weighted monomial Gram matrix is positive definite: the weight
is positive throughout the open cube. A bounded sequence of polynomial
integrals therefore bounds the traces of all its PSD Gram matrices
separately. Since there are finitely many matrices of fixed sizes, a
subsequence converges and represents the polynomial limit.

Closed-cone separation now supplies `lambda(C_r)>=0` and
`lambda(q)<0`. At the asserted orders `r>=6`, both `1` and `q` belong
to the order-`r` square basis. Cauchy--Schwarz gives

\[
0<\lambda(q)^2\le\lambda(1)\lambda(q^2),
\]

so `lambda(1)>0` and normalization is legitimate. The displayed
functional `L_R(a+by+cy^2)=a(0)+R lambda(c)` then has a block diagonal
PSD square form. Both affine private localizers ignore its unrestricted
second-moment block, while `L_R(f)=R lambda(q)` tends to minus infinity.
All degrees match the rectangular domain. The separating functional may
depend on `r`; the polynomial optimization instance remains fixed.

The added nonconvex example also passes. On the triangle
`y>=0, y_1+y_2<=1`, the true minimum of `-(y_1+y_2)^2` is `-1`.
The proposed moment matrix has mean `(1/2,1/2)` and covariance

\[
\begin{pmatrix}3/4&3/4\\3/4&3/4\end{pmatrix}\succeq0.
\]

Its mean satisfies the affine constraints, both private quadratic bounds
are tight, and its relaxation objective is `-4`. With no shared
coordinates, every allowed order has the same private matrix constraints
and `A=0`. This disproves the theorem without private convexity, rather
than only showing failure of the chosen conditional-mean rounding rule.
