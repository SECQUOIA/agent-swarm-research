# Ambient dimension cannot be removed from the current grid-count surrogate

Date: 2026-10-02. Status: complete proof with independent reviews of the
component arguments and the combined note. No novelty claim.

The dimension loss in the
[ambient-noise cell-closure theorem](smoothed-ambient-cell-closure.md)
cannot be removed by a dimension-free estimate of the same local or
near-optimal grid-node counts. Actual rational QPs with `k` negative
eigenvalues, perfectly conditioned supplied factors, fixed projected
coordinate widths, and fixed noise and curvature scales have expected
counts growing as powers of the ambient dimension with exponent
proportional to `k`.

This is a limitation of the counting argument, not a lower bound on the
work of exact cell closure. A solver can close a quadratic region before
visiting the many nodes counted below. The examples also have growing
ambient diameter, so they do not rule out a bound parameterized by that
diameter instead of the projected widths.

## 1. The fiber-volume factor is exactly sharp

Let `n=m^2`, and take the rational row

\[
 T=m^{-1}(1,\ldots,1),\qquad TT^T=1.
\]

For independent continuous `gamma_j` uniform on `[-sigma,sigma]`, write

\[
 d=T\gamma=m\bar\gamma,\qquad
 r=\gamma-\bar\gamma\mathbf1.
\]

Conditional on the residual `r`, the coefficient `d` is uniform on the
fiber

\[
 J(r)=m[-\sigma-\min_jr_j,\ \sigma-\max_jr_j].
\]

Its midpoint is `c(r)=-m(min r+max r)/2`. Let `I(r)` be the interval
of length `L` centered there. Then

\[
 \boxed{
 \Pr\{d\in I(r)\}
 =1-\left(1-\frac{L}{2\sigma m}\right)^n,
 \quad 0\le L\le2\sigma m.}
\tag{1}
\]

Indeed, `d-c(r)=m(min gamma+max gamma)/2`. Rescale to independent
uniform variables on `[0,1]`, with minimum `A` and maximum `B`, and
put `q=L/(2sigma m)`. For `n>=2`, their joint density gives

\[
 \Pr\{|A+B-1|\le q\}
 =n(n-1)\int_0^1s^{n-2}\min\{q,1-s\}\,ds
 =1-(1-q)^n.
\]

The `n=1` case is immediate. Thus

\[
 \lim_{L\downarrow0}\frac{\Pr\{d\in I(r)\}}L
 =\frac{\sqrt n}{2\sigma}.
\tag{2}
\]

This exactly attains the ambient theorem's sum of absolute minors and
its `sqrt(n)` bound. At `L=sigma/m`, the probability tends to
`1-exp(-1/2)`, although `L/sigma` tends to zero. At the same time,
`Var(d)=sigma^2/3` is independent of `n`. A dimension-free covariance
does not justify dimension-free anti-concentration for intervals allowed
to depend on the residual.

For `N=k m^2`, use `k` disjoint blocks of this construction. Their rows
satisfy `TT^T=I_k`, and independence gives the product of (1). The
ratio of the resulting probability to `prod_i[L_i/(2sigma)]` tends to

\[
 m^k=(N/k)^{k/2}.
\tag{3}
\]

The complementary-minor sum is exactly `m^k`: a nonzero minor chooses
one coordinate from each block. Thus perfect factor conditioning alone
cannot improve this probability lemma to a dimension-free bound.
The [separate fiber review](../reviews/ambient-fiber-volume-sharpness.md)
contains the full derivation and its targeted checks.

## 2. Actual QPs with fixed projected widths

The next construction shows that the obstruction is not confined to
arbitrary measurable interval choices. Let `m>=256` be even and set
`n=m^2`. Choose a rational unit vector `u` with `n/2` entries `+1/m`
and `n/2` entries `-1/m`, the last two entries both positive. Let
`B_+` and `B_-` be its positive and negative index sets among the
first `n-2` coordinates. Put

\[
 q=e_{n-1}-e_n,\qquad c=3/4,\qquad \epsilon=m^{-3},
 \qquad T=u^T.
\]

Use either `alpha=1` or `alpha=m`, and define

\[
 P=\alpha[uu^T+c(uq^T+qu^T)+qq^T],\qquad
 A=P-\alpha uu^T.
\tag{4}
\]

In the orthonormal basis `(u,q/sqrt(2))`, the nonzero blocks are

\[
 P=\alpha\begin{pmatrix}1&c\sqrt2\\c\sqrt2&2\end{pmatrix},
 \qquad
 A=\alpha\begin{pmatrix}0&c\sqrt2\\c\sqrt2&2\end{pmatrix}.
\tag{5}
\]

Consequently `P` is positive semidefinite, `ker P subset ker T`, and
`TT^T=1`. There is exactly one negative eigenvalue of `A`, of magnitude

\[
 \nu=\alpha(\sqrt{17/8}-1),\qquad \alpha<4\nu.
\tag{6}
\]

Thus neither poor factor conditioning nor an oversized correction
relative to negative curvature causes the result.

Use the rational polytope

\[
 \begin{split}
 x_i&\ge0 &&(1\le i\le n-2),\\
 \sum_{i=1}^{n-2}x_i&=4m,\\
 x_{n-1}+x_n&=0,\\
 |x_{n-1}-x_n|&\le\epsilon.
 \end{split}
\tag{7}
\]

It has `O(n)` inequalities after replacing equalities by pairs. All
coefficients have polynomial encoding length. With `y=Tx` and
`z=q^Tx`, its feasible image is exactly
`[-4,4] x [-epsilon,epsilon]`, and

\[
 F(x)=\tfrac12x^TAx=\alpha(cyz+z^2/2).
\tag{8}
\]

The Hessian in feasible `(y,z)` coordinates has negative determinant,
so the objective is genuinely nonconvex on this polytope. The projected
width is exactly eight. The thin `z`-interval is an explicit feature
of the example.

## 3. A constant-probability event makes the recourse nearly flat

First let all original noise coordinates be independently continuous
uniform on `[-1,1]`. Decompose

\[
 d=u^T\gamma,\qquad r=\gamma-ud,
\]

and let `V_gamma(a)=W_r(a)+da` be the ambient theorem's auxiliary
objective. At fixed `(y,z)`, minimizing `r^T x` over the active simplex
coordinates gives

\[
 L_r+C_r y+t z,
 \qquad
 C_r=\frac m2\left(\min_{B_+}r_i-\min_{B_-}r_i\right),
 \qquad t=(\gamma_{n-1}-\gamma_n)/2\in[-1,1],
\tag{9}
\]

where `L_r` is independent of `(y,z,a)`. Define

\[
 S=\frac m2\left(\min_{B_+}\gamma_i-
                       \min_{B_-}\gamma_i\right).
\]

The signed factor gives the exact cancellation `C_r=S-d`. Hence

\[
 W_r(a)=L_r+
 \min_{|y|\le4,\ |z|\le\epsilon}
 \left[\alpha(cyz+z^2/2)+C_r y+t z
       +\frac\alpha2(a-y)^2\right].
\tag{10}
\]

This is an actual convex QP in `(y,z)`, with positive definite Hessian.
Whenever `y` is not at an endpoint, its stationarity and the envelope
gradient give

\[
 y=a-C_r/\alpha-cz,
 \qquad V_\gamma'(a)=S+\alpha c z.
\tag{11}
\]

Consider

\[
 E=\left\{
 \min_{B_+}\gamma_i\le-1+4/n,\quad
 \min_{B_-}\gamma_i\le-1+4/n,\quad |d|\le2
 \right\}.
\tag{12}
\]

The first two events are independent, and `Var(d)=1/3`. Since
`|B_+|=n/2-2>=15n/32`, a union bound with Chebyshev's inequality gives

\[
 \Pr(E)\ge(1-e^{-15/16})(1-e^{-1})-1/12>1/4.
\tag{13}
\]

No independence between the group minima and `d` is assumed.
On `E`, `|S|<=2/m` and `|C_r|<=2+2/m`. For every `|a|<=3/2`
and feasible `z`, the candidate `a-C_r/alpha-cz` lies strictly in
`(-4,4)`. Thus (11) applies throughout that interval and

\[
 |V_\gamma'(a)|<3/m.
\tag{14}
\]

The nearly flat behavior comes from the two minima of many original
coefficients, not from independent factor noise.

## 4. Lower bounds on local and globally near-optimal counts

The fixed auxiliary domain prescribed by the ambient theorem is

\[
 A_{\rm aux}=[-4-m/\alpha,\ 4+m/\alpha],\qquad
 w=8+2m/\alpha.
\tag{15}
\]

Its deterministic dyadic grid has step `h=w 2^-j` and correction
`B=alpha h^2/8`. Choose a level with

\[
 16/(\alpha m)\le h\le32/(\alpha m).
\tag{16}
\]

Such a level exists. Every grid node `v in [-1,1]` and its neighbors
lie in `[-3/2,3/2]`. On `E`, (14) implies

\[
 V_\gamma(v)\le V_\gamma(v\pm h)+\alpha h^2/4.
\tag{17}
\]

These are exactly the ambient theorem's local neighboring comparisons,
whose tolerance is `2B`. There are at least `alpha m/32` central
nodes, so

\[
 \boxed{\mathbb E\#\{v:E_v\}\ge\alpha m/128.}
\tag{18}
\]

With `alpha=1`, this is `Omega(sqrt(n))` at fixed projected width,
negative curvature, and noise scale. With `alpha=m`, the auxiliary
width itself is the fixed value ten, but the count is `Omega(n)`.
In the latter version, omitting the volume lemma's `sqrt(n)` factor
would predict only `O(1+alpha w)=O(sqrt(n))`. Thus that extra factor
cannot simply be deleted, even for actual convex-QP recourse.

A coarser level gives a lower bound on globally near-optimal nodes.
Completing the square in (10), up to an additive constant, gives

\[
 V_\gamma(a)=
 \min_{|y|\le4,\ |z|\le\epsilon}
 \left[G(y,z)+\frac\alpha2(a-y+d/\alpha)^2\right],
 \qquad
 G(y,z)=\alpha(cyz+z^2/2)+Sy+tz.
\tag{19}
\]

On `E`, for each `|a|<=1`, choose `(y,z)=(a+d/alpha,0)`.
This is feasible and has `G(y,0)<=6/m`. Every feasible point has
`G(y,z)>=-8/m-3/m^2-1/m^3`. Minimizing also over `a` removes the
square, so

\[
 V_\gamma(a)-\min V_\gamma<15/m\qquad(|a|\le1).
\tag{20}
\]

Choose a deterministic level satisfying

\[
 8/\sqrt{\alpha m}\le h\le16/\sqrt{\alpha m}.
\tag{21}
\]

Now `2B>=16/m`. At least `sqrt(alpha m)/16` central nodes are
globally `2B`-near-optimal on `E`. Hence

\[
 \boxed{
 \mathbb E N_{2B}\ge\sqrt{\alpha m}/64.}
\tag{22}
\]

In particular, even the complete-grid global near-optimal count grows
as `Omega(n^(1/4))` when `alpha=1` and all per-coordinate projected
width and curvature-to-noise parameters are fixed.

## 5. Products rule out an FPT bound for these surrogates

Take `k` independent copies with common `m,alpha`. Their ambient
dimension is `N=k m^2`, the Hessian has exactly `k` negative
eigenvalues, and the supplied disjoint factor rows satisfy `TT^T=I_k`.
Every projected coordinate width is eight. The constraints and rational
encodings remain polynomial in `N`.

The block events have joint probability greater than `4^-k`.
At the local level (16), every Cartesian product of central nodes
satisfies the `k`-dimensional local comparisons: their tolerance
`2B=alpha k h^2/4` is at least the scalar tolerance. At the coarser
level (21), the sum of the block gaps is below `15k/m<2B`.
Consequently,

\[
 \mathbb E\#\{v:E_v\}\ge(\alpha m/128)^k,
 \qquad
 \mathbb E N_{2B}\ge(\sqrt{\alpha m}/64)^k.
\tag{23}
\]

For `alpha=1`, these bounds become

\[
 \boxed{
 128^{-k}(N/k)^{k/2},\qquad
 64^{-k}(N/k)^{k/4}.}
\tag{24}
\]

Therefore neither full-grid count admits an upper bound
`f(k,R) N^C` with absolute exponent `C` when `R` records only the
fixed projected coordinate widths, factor conditioning, and
curvature-to-noise ratios. The conclusion also holds with a polynomial
in rational input length instead of `N`: a dense representation of this
family has `I=O(N^2 log N)`. Given a proposed bound `f(k,R) I^C`,
fix `k>8C` and let `m` grow. The near-optimal count in (24) then
exceeds that bound; the local count grows still faster.

The ambient diameter is different. Already one block has diameter
`Theta(m)` because its active simplex has total mass `4m`.
Thus (24) does not contradict a bound parameterized by the full ambient
diameter divided by the noise scale. The projected diameter is only
`8 sqrt(k)`, independent of `m`.

## 6. The same obstruction holds for sufficiently fine rational noise

The exact fiber identity (1) was a continuous-noise identity. The actual
QP count construction has a separate direct finite-law argument.
Let each original coefficient be independently uniform on an
endpoint-inclusive `M_noise`-point grid in `[-1,1]`, with
`M_noise>=64n` for the block dimension `n=m^2`.

A single coordinate is at most `-1+4/n` with probability at least

\[
 2/n-1/M_{\rm noise}\ge19/(10n).
\]

The two group-minimum events therefore have joint probability at least
`(1-exp(-57/64))(1-exp(-19/20))`. Also

\[
 \operatorname{Var}(d)
 =\frac{M_{\rm noise}+1}{3(M_{\rm noise}-1)}\le3/8,
\]

so Chebyshev's contribution is at most `3/32`. Hence

\[
 \Pr(E)\ge
 (1-e^{-57/64})(1-e^{-19/20})-3/32>1/4.
\tag{25}
\]

For example, `exp(57/64)>12/5` and `exp(19/20)>5/2` make the
right side greater than `7/20-3/32=41/160>1/4`.
All deterministic conclusions above then apply unchanged, including the
independent-block bounds (23)--(24). The fixed sampling grid prescribed
by the ambient closure theorem is finer than this threshold: its section
constant is at least 70 and its grid-count factor is at least one, so
its sampling rule gives at least `140N>=64n` noise points.

## 7. What an algorithmic improvement would still need

There are three different counts here: local-comparison nodes, globally
near-optimal nodes of the complete deterministic grid, and retained
unresolved cells actually visited by the exact algorithm. Only the first
two have been lower-bounded. They are the surrogates used to upper-bound
the third in the current proof; a large surrogate does not force a large
actual search.

For this example, the original noise selects one minimum coordinate in
each simplex group, and the remaining recourse depends only on `(y,z)`.
Its small number of quadratic pieces may be easy to extract and close.
An FPT theorem based on algebraic closure, stronger global pruning, or
another factorization or search representation remains possible. The
example uses an admissible supplied rational factor, without asserting
that a particular spectral-normalization implementation returns it.
An improvement would need to use
more than a dimension-free replacement for these full-grid counts.

Likewise, the covariance of the projected uniform-cube noise does not
control its residual-conditioned concentration. A different noise law
with independence between orthogonal projections can avoid that specific
obstruction; the separate
[Gaussian-noise analysis](smoothed-gaussian-cell-closure.md) uses this
distinction. No conclusion about that law follows from this example.
The present result supplies neither a solver lower bound nor a hardness
claim for ambient-noise quadratic optimization.

## 8. Verification status

The exact fiber probability and minor sums were independently derived
and checked in the [fiber review](../reviews/ambient-fiber-volume-sharpness.md).
The actual-QP construction and its product bounds were developed and
independently checked in the
[construction review](../reviews/ambient-local-count-barrier.md).
The [completed combined review](../reviews/ambient-local-count-combined-review.md)
then checked this full note, including the finite-grid constants,
input-length conclusion, and scope, and found no mathematical blocker.

The targeted commands actually run were

```text
python research-20261002/new-direction/check_ambient_fiber_sharpness.py
python research-20261002/new-direction/check_ambient_local_qp_barrier.py
```

The fiber checker passed 160 exact range integrals, 96 discrete
endpoint/enumeration comparisons, 36 finite-grid discrepancy checks,
and 22 disjoint-block minor sums. The actual-QP checker passed 12
rational noise fixtures satisfying `E`, 144 exact derivative identities,
286 local comparisons, and 84 global-gap checks. It covers both choices
of `alpha` and all three possibilities for the thin coordinate: lower
bound, interior, and upper bound. Its independent minimizations check
the reduced convex QP on a rectangle and the nonconvex original
objective, which is affine in `y` for fixed `z`.

These finite exact-rational checks support the formulas and inequalities;
they do not prove the probability estimate by sampling or benchmark the
full closure algorithm. No literature search, project-wide verification,
or CI inspection was performed in this workstream.
