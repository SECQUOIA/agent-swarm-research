# Positivity-preserving convex extraction cannot remove large diagonal curvature

Date: 2026-10-02. Status: direct construction, targeted exact checks, and a
[fresh independent review](../reviews/psd-extraction-curvature-obstruction-review.md)
finding no substantive gap. No priority claim is made.

A natural route to the [sparse negative-curvature target](negative-curvature-sparse.md)
would subtract a globally nonnegative convex quadratic, certify the
remaining copositive quadratic with the diagonal-curvature grid, and
add the extracted part back. The following fixed-dimensional family
rules out a uniform curvature reduction of that kind. It even permits
extracting an additional entrywise nonnegative quadratic.

The family has a unique optimum at the origin, a fixed orthant growth
margin, fixed interaction width, and bounded negative curvature.
Nevertheless, every copositive remainder after such extraction has an
arbitrarily large positive diagonal. This is a limitation of that
preprocessing strategy, not optimization hardness or a lower bound for
methods that retain convex recourse, change coordinates, or use other
certificate families.

## 1. The family and its true conditioning

Let `C_5` be the five-cycle, put

\[
 H=\boldsymbol 1\boldsymbol 1^T-2\operatorname{Adj}(C_5),\quad
 D=\operatorname{diag}(d,1,1,1,1),\quad
 \epsilon=1/100,\quad A_d=DHD+\epsilon I,
 \tag{1}
\]

where `d>=1` is an integer. Define `Q_d(x)=x^T A_d x` on the
nonnegative orthant or on `[0,1]^5`. The interaction graph is `K_5`,
so a single bag of size five suffices. Input length is `O(log(d+1))`.

The [Horn calculation](box-preordering-growth-obstruction.md) proves
`u^T H u>=0` for every `u>=0`. Briefly, after normalizing `sum u_i=1`,
the cycle edge sum is at most `1/4`: a maximizer of minimum support
can move mass between any nonadjacent positive pair without decreasing
the objective, so its support is a clique of size at most two. Hence

\[
 Q_d(x)\ge\epsilon\|x\|_2^2\qquad(x\ge0).
 \tag{2}
\]

Let indices be cyclic and define five nonnegative vectors

\[
 z_i=D^{-1}(e_i+e_{i+1}),\qquad i=1,\ldots,5.
 \tag{3}
\]

They belong to the unit box and satisfy

\[
 z_i^T DHD z_i=0,\qquad
 Q_d(z_i)=\epsilon\|z_i\|_2^2.
 \tag{4}
\]

Thus the best growth constant on either domain is exactly
`g=epsilon`, and the unique minimizer is zero.

To bound negative curvature, write `x=(x_1,y)` and
`h=(-1,1,1,-1)^T`. If `H_0` is the lower four-by-four principal
submatrix of `H`, completing the first square gives

\[
 Q_d(x)=(d x_1+h^T y)^2+y^T S y+\epsilon\|x\|_2^2,
 \quad
 S=H_0-hh^T=
 \begin{pmatrix}
 0&0&2&0\\
 0&0&-2&2\\
 2&-2&0&0\\
 0&2&0&0
 \end{pmatrix}.
 \tag{5}
\]

The maximum absolute row sum of the symmetric matrix `S` is four,
so `S>=-4I`. Consequently `A_d>=-4I`. In the Hessian convention
used by the sparse target,

\[
 \nu_d=\max\{0,-\lambda_{\min}(\nabla^2Q_d)\}
       =2\max\{0,-\lambda_{\min}(A_d)\}\le8,
 \qquad \nu_d/g\le800.
 \tag{6}
\]

These matrices are nonconvex. For example, take
`y=(0,1,1,0)` and `x_1=-2/d` in the ambient space. Equation (5)
gives quadratic value `-4+epsilon(2+4/d^2)<0`.
This direction is used only to show ambient negative curvature;
it need not belong to the feasible orthant.

## 2. Every copositive remainder retains a large diagonal

Allow an arbitrary decomposition

\[
                  A_d=P+N+R,                                \tag{7}
\]

where `P` is positive semidefinite, `N` is symmetric and entrywise
nonnegative, and `R` is copositive. No sparsity or rationality restriction
is imposed on these matrices. In particular, the claim applies to dense
real PSD extraction and therefore also to rational sparse extraction.

It suffices to prove the bound when `N=0`. Indeed, replace the split by

\[
 P'=P+\operatorname{diag}(N),\qquad
 R'=R+N-\operatorname{diag}(N).
\]

Here `diag(N)` denotes the diagonal matrix formed from the diagonal of
`N`. Then `P'` is PSD, `R'` is copositive, `A_d=P'+R'`, and `R'`
has the same diagonal as `R`. Thus a bound for PSD-only extraction
also proves the full claim (7). In the following calculation use
`A_d=P+R` with `P` PSD and `R` copositive.

Both summands are nonnegative on every `z_i`. Equation (4) gives

\[
       z_i^T Pz_i\le\epsilon\|z_i\|_2^2.
 \tag{8}
\]

The five rays satisfy the exact identity

\[
 e_1=\frac d2(z_1-z_2+z_3-z_4+z_5),\qquad
       \sum_i\|z_i\|_2^2=8+2/d^2.
 \tag{9}
\]

Apply the triangle inequality and then Cauchy--Schwarz to the
vectors `P^{1/2} z_i`. This square root is an analysis device,
not part of a rational certificate. Equations (8)--(9) imply

\[
 \begin{aligned}
 P_{11}
  &\le\frac{5d^2}{4}\sum_i z_i^T Pz_i\\
  &\le\frac{5\epsilon d^2}{4}(8+2/d^2)
   =10\epsilon d^2+\frac52\epsilon.
 \end{aligned}                                                \tag{10}
\]

Since `(A_d)_{11}=d^2+epsilon`, subtraction gives

\[
 \begin{aligned}
 R_{11}
 &\ge(1-10\epsilon)d^2-\frac32\epsilon\\
 &\ge\frac{177}{200}d^2
  \ge\frac78 d^2.
 \end{aligned}                                                \tag{11}
\]

These inequalities require only copositivity of the remainder, not a
strict residual margin. Thus they also cover a decomposition that uses
up all of the original growth margin.

## 3. Consequence for a diagonal-curvature reduction

Suppose in addition the remainder is strictly copositive, and let
`g_R` be its best Euclidean orthant growth constant. On the orthant,
`x^T R x<=Q_d(x)` because both extracted terms are nonnegative.
Evaluating this inequality at any ray in (3) gives

\[
                  0<g_R\le\epsilon.
 \tag{12}
\]

The upper coordinate curvature `L_R=2 max_i R_ii` therefore satisfies

\[
              L_R/g_R\ge175d^2.                             \tag{13}
\]

If `g_R=0`, a strict-margin grid theorem cannot be applied
to that remainder at all.

The original parameters `p=5` and `nu_d/g<=800` stay bounded, while
the residual diagonal-curvature ratio necessarily diverges. In
particular, there is no uniform bound of the form
`C(p, upper_bound_on_nu/g)` for that residual ratio, even with arbitrary
dense real choices of the extracted PSD and nonnegative matrices.

This rules out the following specific reduction: subtract an easy
nonnegative quadratic, obtain a separately copositive residual of
controlled diagonal curvature in the original coordinates, and invoke
the [geometric copositivity certificate](geometric-copositive-certificate.md)
with its `L_R/g_R` complexity bound. It does not prove that a grid
must take its general worst-case complexity, or that a different
certificate must be large. The specific shared-grid rule nevertheless
has the following direct resolution lower bound.

**Corollary for that grid rule.** Apply the homogeneous certificate of
[geometric-copositive-certificate.md](geometric-copositive-certificate.md)
to any copositive remainder `R` from (7), using its prescribed common
curvature `L_R`, `eta=delta/5`, and `sigma=L_R delta^2/8`. The normalized
grid always contains `e_2`. Also
`R_22<= (A_d)_22=101/100`, because both extracted diagonal entries
are nonnegative. Its acceptance quantity consequently obeys

\[
 b_\delta
 =\min_y[y^T R y-2\sigma\|y\|^2]-\sigma/5
 \le\frac{101}{100}-\frac{11}{5}\sigma.
\]

Any accepted trial therefore has `sigma<101/220<1/2`. Since
`L_R>=7d^2/4` by (11), this forces

\[
                    \delta^{-1}>\frac{\sqrt7}{4}d>d/2.
\]

Every interval of that grid has length at most `delta`: its first
length is `delta/5`, and a positive interval has length at most
`delta` times its lower endpoint, which is at most one. Covering
`[0,1]` therefore requires at least `1+delta^{-1}>d/2` grid nodes.
The successful state count for this precise rule is thus unbounded
and can be exponential in the input length, even after an arbitrarily
chosen admissible extraction. If the remainder is not strictly
copositive, there is no accepted trial at all. This says nothing about
a coordinate-dependent mesh, a different correction, or an algorithm
that handles the convex part and the remainder jointly.

The obstruction is stronger than observing that the ordinary spectral
positive part can destroy copositivity: it quantifies over every PSD
extraction, and even every additional entrywise nonnegative extraction.
The copositivity requirement is essential. In fact (5) already gives an
unrestricted rank-one PSD extraction

\[
 P_0=(d,h)(d,h)^T,\qquad
 A_d-P_0=\operatorname{diag}(0,S)+\epsilon I.                  \tag{14}
\]

This residual has bounded norm and every diagonal entry equal to
`epsilon`, but it is not copositive: the nonnegative vector
`(0,0,1,1,0)` gives value `-4+2epsilon`. Thus the example does not
rule out bounded-curvature residuals when the convex part and residual
are optimized jointly. It specifically rules out separately certifying
both extracted and residual terms as nonnegative at the same corner.

Five-dimensional global optimization is not made hard by this family.
Exact local recourse, nonquadratic extraction, coordinate changes, and
selective certificates remain outside the claim.

There is also a concrete coordinate-change escape for this family.
Set `u=Dx`. The transformed matrix is

\[
              H+\epsilon\operatorname{diag}(d^{-2},1,1,1,1).
\]

Its coordinate curvature is at most `2(1+epsilon)`. Its limit as
`d` tends to infinity is strictly copositive: the nonnegative Horn
form plus `epsilon sum_{i>1}u_i^2` can vanish only if all those
coordinates vanish, and then the Horn form is `u_1^2`. Compactness
of the nonnegative unit sphere gives a positive margin for this
limiting form, and the finite-`d` forms have at least that margin.
An explicit bound is `epsilon/65`: writing `u=(a,y)` and
`b=||y||`, principal-submatrix copositivity and `||h||=2` give
`u^T H u>=a^2-4ab`. If `b<=a/8`, the Horn form is at least
`a^2/2>=32||u||^2/65`; otherwise the perturbation contributes
`epsilon b^2>=epsilon||u||^2/65`. The finite-`d` perturbation is
no smaller. Thus the transformed curvature/growth ratio is at most
`2(1+epsilon)65/epsilon=13130`, with a coordinate change of
`O(log(d+1))` bits. Homogeneity permits the
orthant certificate to use its usual normalized shell; no growing
transformed box must be gridded. The obstruction concerns
positivity-preserving extraction in the original coordinates, not
a scheme that combines extraction with diagonal preconditioning.

## 4. Verification

The [focused prior-art audit](../prior-art/psd-extraction-curvature-prior.md)
places the construction against the classical Horn orbit and the
minimal-zero criterion for PSD irreducibility. Those qualitative
predecessors concern the unperturbed matrix. The present calculation
quantifies permitted subtraction after the fixed positive perturbation
and its consequence for one specified grid rule. It is not a claim
that the Horn mechanism or its irreducibility is new.

An independent reviewer ran

```
python research-20261002/reviews/check_psd_extraction_dual.py
```

successfully. It checks 31 exact principal minors of `5I-ss^T`, where
`s=(1,-1,1,-1,1)`, and the symbolic rational PSD certificate

\[
 \frac{d^2}{4}Z(5I-ss^T)Z^T
       =\frac{5d^2}{4}\sum_i z_i z_i^T-e_1e_1^T\succeq0,
 \qquad Z=[z_1\ \cdots\ z_5].
\]

This supplies the universal inequality behind (10). The checker also
verifies the ray-budget and residual constants symbolically, 77 exact
axis-threshold implications for the grid corollary (including `d=2^200`),
and three actual grid interval/count checks.

A second reviewer independently checked 500 shifted Horn ray equalities,
100 signed ray identities and constant bounds, 1,000 orthant-growth
samples, and 100 explicit sign-changing-residual witnesses, using
exact rational arithmetic. These finite diagnostics are distinct from
the universal proofs. The note's author inspected the persistent
checker rather than rerunning these reviewer checks.

The independent review checked the entire written proof and the
specified-grid corollary. Scoped whitespace, equation sequence,
delimiter, and local-reference checks passed. No originality claim
is inferred from the algebra. No project-wide verification or CI
inspection was performed.
