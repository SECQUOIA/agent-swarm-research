# Independent review of constrained sparse kernel rounding

Date: 2026-09-28. This review checks the supplied proofs, including the
ordinary-kernel transport sharpening. It does not establish novelty or
independently audit every cited theorem. The separate
[prior comparison](general-constraints-prior.md) addresses that task.

**Conclusion:** no mathematical defect was found in the full box-preordering
theorem or the ordinary-module theorem. The transport argument
does improve the ordinary-module squared-violation estimate from
`O(log^3(R)/R^2)` to `O(log^2(R)/R^2)`. With the stated global geometric
bound, the resulting objective rate is `O((log(R)/R)^alpha)`. The proof
uses the existing degree reserve `R >= wD + 2d` and does not require
products of ordinary box generators.

## Full box-preordering proof

The degree reserve is sufficient for each distinct positivity claim. The
kernel certificate has degree at most `2(R-d)`. Multiplying by `g`, or
by the square of a linear combination of `1,g`, gives degree at most
`2R-d` or `2R`, respectively. The supplied additional localizers are
exactly what proves `L(K_b g) >= 0`; ordinary constraint localizers alone
would not suffice for this kernel.

For `h=L(K_b)`, conditional Cauchy--Schwarz gives
`(-g(y))_+^2 h <= L(K_b(g(x)-g(y))^2)`. If `h=0`, the right side is
nonnegative and the displayed inequality still holds. Thus no conditional
division or representing-measure assumption is hidden here.

The integrated residual has degree at most `2 deg g <= R`, so its
Chebyshev coefficient norm can be used with the available bound
`|L(T_beta)| <= 1`. The weighted product inequality

`A(pq) <= C(p) A(q) + A(p) C(q)`

is valid: in a tensor Chebyshev product, the average squared frequency in
coordinate `i` is `alpha_i^2+beta_i^2`. It follows that the residual norm
is at most `12 C(g) A(g)/(2m^2+1)`. Exact consistency of the normalized
kernel laws makes this a bound on the same global law used for the
objective estimate.

The finite-net repair argument gives measurable approximate projections
onto compact `K`. Jensen's inequality applies because `alpha/2` lies in
`(0,1/2]`. Taking a weak limit retains support in `K` and the objective
inequality. This proves existence; it supplies no efficient global
projection algorithm.

## Ordinary-kernel second moment

Write `F_s` for the normalized-circle Fejer density with Fourier
coefficients `a_k=(1-|k|/s)_+`. For `x=cos(theta)`, `y=cos(phi)`,

\[
 S_s(x,y)=\tfrac12\{F_s(\theta-\phi)+F_s(\theta+\phi)\}.
\]

The elementary inequalities `(u+v)^2/4 <= (u^2+v^2)/2` and
`(cos(theta)-cos(phi))^2 <= 2(1-cos(theta-phi))`, together with the
corresponding inequality using `theta+phi`, imply

\[
 J_s(x):=\int (x-y)^2 S_s(x,y)^2\,d\mu(y)
 \le \int_{\mathbb T}2(1-\cos t)F_s(t)^2\,dt
 ={2\over s}.
\]

Here circle measure is normalized. The arcsine integral equals a full
circle integral of its even-in-`phi` integrand. The final equality is
`2(sum_k a_k^2 - sum_k a_k a_(k-1))=2/s`; equivalently, the sum of squared
adjacent differences of the triangular coefficient sequence is `2/s`.
This confirms both the normalization and the factor two.

The normalization polynomial satisfies `0 <= p_(s,N) <= 2/C_s` on the
interval. Therefore

\[
 j(x)=p_{s,N}(x)J_s(x),\qquad
 0\le j(x)\le c_s:={4\over sC_s}\le {6\over s^2}.
\]

Moreover, `j` is globally SOS: `J_s` is an integral of squares, and `p`
is globally SOS for even `N`. Its degree is at most `D+2`. The univariate
interval representation theorem therefore places `c_s-j` in the ordinary
interval module with degree at most `D+2`. Pointwise nonnegativity of `j`
alone would not justify the later product argument; global SOS does.

## The polynomial difference certificate

Fix an output point `y` in the bag cube. For
`g=sum_alpha c_alpha T_alpha`, set

\[
 A_i=\sum_\alpha |c_\alpha|\alpha_i^2,\qquad A=\sum_i A_i.
\]

The following polynomial has an ordinary box-module representation of
degree at most `2 deg g`:

\[
 A\sum_i A_i(x_i-y_i)^2-(g(x)-g(y))^2. \tag{1}
\]

To verify this assertion without mistaking pointwise positivity for
module membership, telescope each tensor difference in coordinate order.
For a nonzero coefficient and `k=alpha_i>0`, put

\[
 a_{\alpha i}=|c_\alpha|k^2,\qquad
 r_{\alpha i}(x)=\operatorname{sign}(c_\alpha)
 {T_k(x_i)-T_k(y_i)\over k^2(x_i-y_i)}
 \prod_{j<i}T_{\alpha_j}(x_j)
 \prod_{j>i}T_{\alpha_j}(y_j).
\]

The quotient is the polynomial divided difference, also defined at
`x_i=y_i`. The derivative bound `|T_k'| <= k^2` gives its absolute value
at most one on the interval. Every other nonconstant factor is a
univariate Chebyshev polynomial bounded by one, and the final factors are
constants of absolute value at most one.

Each univariate factor `r_j` thus has an interval certificate for
`1-r_j^2` of degree at most twice its degree. The telescoping identity
for `1-prod_j r_j^2` multiplies these certificates only by squares.
Consequently `1-r_(alpha i)^2` has an ordinary box-module certificate
of degree at most `2(|alpha|-1)`.

Index these records by `ell`, write `t_ell=x_i-y_i`, and use
`g(x)-g(y)=sum_ell a_ell t_ell r_ell`. The exact identity

\[
\begin{split}
 A\sum_\ell a_\ell t_\ell^2
 -\left(\sum_\ell a_\ell t_\ell r_\ell\right)^2
 ={}& A\sum_\ell a_\ell t_\ell^2(1-r_\ell^2)\\
 &+\sum_{\ell<k}a_\ell a_k
                  (t_\ell r_\ell-t_k r_k)^2
\end{split}
\]

proves (1), including its degree bound. Constant `g` has `A=0` and
zero difference, so it needs no special positivity assumption.

Multiplication by the globally SOS product kernel `Q_b` preserves this
ordinary module. Its degree is at most `vD+2d`, where `v` is the bag
size. Apply `L_b` to this certificate for each fixed `y`, then integrate
the resulting scalar inequality. This order avoids assuming a measurable
selection of interval SOS representations.

## Product masses, violations, and the rate

The mass factors `n_i` are globally SOS and satisfy `0 <= n_i <= 1` on
the interval. The companion ordinary-kernel proof gives module
certificates for `1-prod_(k != i) n_k`. Hence

\[
 c_s-j_i\prod_{k\ne i}n_k
 =(c_s-j_i)\prod_{k\ne i}n_k
       +c_s\left(1-\prod_{k\ne i}n_k\right)
\]

is in the ordinary module with degree at most `vD+2`. Applying the
normalized functional bounds `L_b(j_i prod_(k != i)n_k)` by `c_s`.
Together with (1), this proves

\[
 \int L_b\bigl(Q_b(x,y)(g(x)-g(y))^2\bigr)\,d\mu_b(y)
 \le c_s A(g)^2.
\]

The conditional positivity argument remains valid with the ordinary
constraint localizers because `Q_b` is globally SOS. Division by the bag
mass `Z_b >= a^v` gives the normalized bag bound
`c_s A(g)^2/a^v`.

The tree coupling from the companion note preserves every normalized
bag law before the replacement on its bad event. This single coupling
therefore controls the objective and all constraint violations at once.
Replacing its bad tuples increases expected squared violation by at most
`G_2 epsilon_T`, since violations are nonnegative and their sum is at
most `G_2` on the box. The valid sharpened quantity is

\[
 U_{s,N}=\sum_{b,j}{c_s A(g_{bj})^2\over a^{|B_b|}}
                  +G_2\varepsilon_T.
\]

For the stated even `N` of order `3 log_2 s`, fixed tree, and
`s` of order `R/log R`, this is `O(log^2(R)/R^2)`. The unchanged
objective error `O(log^3(R)/R^2)` is smaller than
`(log(R)/R)^alpha` for every fixed `0<alpha<=1`. Global feasible repair
therefore gives the announced sharpened rate. The constants still
depend on the geometric bound, generators, and finite tree. There is no
uniform-in-tree-size conclusion.

## Limitations retained

The ordinary theorem proves a primal moment bound. Empty interior can
prevent the box-only Slater proof from applying to the constrained
problem, so an attained SOS dual at the exact stated error is not proved
here. A global distance bound cannot be replaced by unrelated local
distance bounds. The repair step does not justify efficient extraction
or an integer-feasible extension. The alpha-one lower example only
shows a sharp polynomial exponent for the full class; it does not prove
that the ordinary logarithm is necessary.

## Targeted verification

Commands actually run for this review:

```text
python3 -B research-20260928/solver/check_general_constraints_transport_review.py
python3 -B research-20260928/solver/check_general_constraints_review.py
```

Both passed. The new independent checker verifies 63 exact Fejer
autocorrelation constants; eight kernel degree, mass, and product
identities; 200 rational samples of their interval bounds; and 24 exact
multivariate divided-difference and weighted-square identities. The
earlier checker verifies 4,368 basis products, 120 signed product bounds,
480 Jackson residual bounds, 16 ordinary residual/tensor cases, 79 exact
Fejer displacement constants, 18 normalized displacement bounds, and 81
simultaneous objective/violation coupling cases.

The finite checks do not prove the interval inequalities at untested
points, the statements at arbitrary degree, or positivity for arbitrary
pseudomoments. Those claims rest on the proofs above and the standard
univariate interval SOS theorem. No Lean proof, project-wide test, or CI
inspection was performed for this review.
