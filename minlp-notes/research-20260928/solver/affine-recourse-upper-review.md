# Independent review of affine recourse kernel rounding

Date: 2026-09-28. This review first derives the proposed result independently
from the existing [partial kernel theorem](partial-kernel-rounding.md) and
[scalar kernel construction](sparse-kernel-rounding.md). It checks the
mathematical transport and feasibility arguments. It makes no novelty or
publication-priority claim.

After that derivation, the complete
[affine recourse draft](affine-recourse-kernel-upper.md) was read and
checked against it. The written theorem agrees with the independent
derivation. No substantive gap was found in its assumptions, finite SDP
dimensions, degree accounting, transport bound, projection construction,
gluing, or grid consequence. This is evidence from a mathematical review,
not formal proof certification.

The proposed assumptions support an inverse-order rounding bound. The
degree reserve is sufficient, the conditioned source shared vector stays
in its box, and a uniform Hoffman bound supplies a measurable feasible
repair. The explicit kernel also permits a slightly sharper transport
constant than the convenient bound `6/(2m^2+1)`.

## 1. Assumptions used in this review

The shared bags form a junction tree. For a bag with shared vector `u`
of dimension `k` and private vector `y` of dimension `p`, the feasible
private set is

\[
 P(u)=\{y\in[-1,1]^p:Ay\le b+Bu\},\qquad u\in[-1,1]^k.
\]

The matrices `A,B` and vector `b` are fixed; `P(u)` is nonempty for
every shared box point. The objective is
`f(u,y)=c(u)+a(u)^T y+y^T Q(u)y`, with polynomial coefficient data and
`Q(u)` positive semidefinite throughout the shared box. Private variables
belong to only one bag.

The rectangular local functional has shared degree at most `2r` and
private degree at most two. It has the partial theorem's matrix moment
positivity and redundant quadratic private localizers. For each affine
recourse row `g(u,y)=b_j+B_j u-A_j y`, impose

\[
 L(w_I q^2g)\ge0,\qquad \deg q\le r-|I|-1,
 \quad w_I=\prod_{i\in I}(1-u_i^2).
\]

This is a conservative uniform bound for all recourse rows, including
those whose shared coefficients happen to vanish. All moment agreements
on shared separators remain the same as in the partial theorem.

Set `s=max(1,max_b k_b)`, assume `r>=max(s+1,d)`, and choose

\[
 m=\lfloor(r-1)/s\rfloor+1\ge2.
\]

Here `d` is the maximum total shared degree of an objective coefficient.
These conditions leave one square degree beyond each bag kernel.

## 2. The degree reserve is sufficient

For fixed target `v`, write the product kernel as

\[
 K(u,v)=\sum_I w_I(u)\sum_\ell q_{I\ell}(u)^2,
 \qquad\deg q_{I\ell}\le k(m-1)-|I|\le r-1-|I|.
\]

The kernel may therefore be multiplied by a recourse row under the
specified affine localizers. It may also be multiplied by the square of
any affine shared polynomial under scalar moment positivity. In
particular, the required expressions `L(Ku_i)`, `L(Ku_i^2)`, and
`L(K(u_i-v_i)^2)` are defined and controlled.

Multiplying the kernel by `1-u_i^2` stays in the shared preordering within
degree `2r`. If `i` was absent from `I`, add it. If it was already present,
absorb the resulting factor `(1-u_i^2)^2` into the square and remove `i`
from the generator subset. In the latter case the square degree increases
by two, but the generator subset loses one element; the same total degree
bound follows. Repeated generators are therefore not a missing constraint.

Without the reserve, a kernel of shared degree exactly `2r` does not even
permit defining `L(Ku_i)` within the original functional's domain. A
proof that simply retains the old kernel order is invalid at such orders.

## 3. The conditioned source is feasible at its own shared mean

Let

\[
 h(v)=L(K(u,v)),\quad n_i(v)=L(K(u,v)u_i),\quad
 \ell(v)=L(K(u,v)y).
\]

For `h(v)>0` put `ubar=n/h` and `ybar=ell/h`. Scalar kernel moment
positivity gives

\[
 n_i^2\le h L(Ku_i^2),\qquad
 0\le L(Ku_i^2)\le h.
\]

The upper bound follows from the repeated-generator argument above.
Thus `|ubar_i|<=1`. The private moment matrix and private quadratic
localizers likewise give `|ybar_j|<=1`. Applying the recourse localizers
to the kernel yields

\[
 b+B\overline u-A\overline y\ge0.
\]

Consequently `ybar in P(ubar)`. This uses the constraints' joint
affineness, not a representing measure for the pseudoexpectation.

The source vector `ubar(v)` is only used locally to prove feasibility and
bound repair distance. It does not need to agree between overlapping bags.
The target vector `v` is the shared variable whose scalar bag laws are
glued, and those laws have exactly consistent separator marginals.

## 4. Exact integrated square displacement

Cauchy--Schwarz for the kernel-weighted scalar moment form gives

\[
 h(v)(\overline u_i(v)-v_i)^2
 \le L(K(u,v)(u_i-v_i)^2).                         \tag{1}
\]

Normalization removes all other coordinate kernels upon integration.
The first two Chebyshev multiplier identities give

\[
 \int L(K(u,v)(u_i-v_i)^2)\,d\mu^k(v)
 =\frac{1-g_2}{2}+(1-2g_1+g_2)L(u_i^2).           \tag{2}
\]

For the squared-Fejer kernel of the scalar note,

\[
 a_0=\frac{m(2m^2+1)}3,\quad a_0-a_1=m,\quad a_0-a_2=4m-3.
\]

For the last identity use
`a0-a2=(1/2) sum_j (b_j-b_(j-2))^2`. The nonzero differences comprise
one `1`, `m-1` copies of `2`, `m-1` copies of `-2`, and one `-1`.
Therefore (2) equals

\[
 \frac{4m-3}{2a_0}+\frac{3-2m}{a_0}L(u_i^2).
\]

Because `m>=2` and `L(u_i^2)>=0`, define

\[
 C_m=\frac{4m-3}{2a_0}
     =\frac6{2m^2+1}-\frac9{2m(2m^2+1)}
     <\frac6{2m^2+1}.                              \tag{3}
\]

Equations (1)--(3) imply

\[
 \int h(v)\|\overline u(v)-v\|_2^2\,d\mu^k(v)\le kC_m.
                                                               \tag{4}
\]

This constant is sharp for (4): the actual source evaluation functional
at `u=0` has `ubar(v)=0` and density `K(0,v)`; each coordinate's second
target moment is exactly `(1-g2)/2=C_m`. This is only sharpness of the
transport estimate. It makes no claim of sharpness for the final objective
error or its dependence on recourse data.

The simpler bound `k*6/(2m^2+1)` remains valid. It can be proved using
only `0<=1-g2<=4(1-g1)` and `0<=L(u_i^2)<=1`, without computing `a2`.

## 5. Uniform Hoffman repair and continuity

Stack the private box inequalities with `Ay<=b+Bu` to obtain a fixed
matrix `C=[A;I;-I]`. A Euclidean Hoffman constant `H(C)` is uniform over
all right-hand sides for which the polyhedron is nonempty. For `ybar`
in the box, the added box-row residuals vanish. Since `ybar in P(ubar)`,

\[
 \operatorname{dist}(\overline y,P(v))
 \le H(C)\|(A\overline y-b-Bv)_+\|_2
 \le H(C)\|B\|_2\|\overline u-v\|_2.              \tag{5}
\]

The positivity operation here is componentwise. The last inequality is
valid because the residual is componentwise bounded above by
`B(ubar-v)`, then taking the positive part and Euclidean norm cannot
increase the norm of that vector.

For completeness, the projection used in (5) is measurable without a
Slater or full-dimensionality assumption. Applying (5) to arbitrary
points of `P(u)` and reversing `u,v` gives

\[
 d_H(P(u),P(v))\le H(C)\|B\|_2\|u-v\|_2.
\]

Here `d_H` is Hausdorff distance. Let `u_n -> u`, `y_n -> y`, and let
`p_n` be the unique Euclidean projection of `y_n` onto `P(u_n)`.
Compactness gives convergent subsequences of `p_n`, and the closed graph
places every limit in `P(u)`. For every `z in P(u)`, the Hausdorff bound
supplies `z_n in P(u_n)` tending to `z`. Minimality gives
`||p_n-y_n||<=||z_n-y_n||`, so every subsequential limit minimizes distance
to `y` on `P(u)`. Convexity gives uniqueness; hence all `p_n` converge to
that projection. The projection is jointly continuous in `(u,y)`.

The functions `ubar,ybar` are continuous where the polynomial density
`h` is positive. On its zero set choose `yhat(v)` as the projection of
zero onto `P(v)`. This yields a measurable feasible private decision
everywhere, and the choice on the zero-density set has no effect on the
integrals.

The cited uniform Hoffman result appears in
[Peña, Vera and Zuluaga, Proposition 1 and Introduction (1)](https://arxiv.org/html/1905.02894).
Their relative version, Introduction (2), also allows the reference
polyhedron to be the fixed private box. This can sharpen the constant;
the stacked-matrix formulation already suffices. This source was opened
and checked during this review.

## 6. Objective error follows without a new convexity assumption

Let

\[
 G=\max_{v\in[-1,1]^k,\,y\in[-1,1]^p}
           \|a(v)+2Q(v)y\|_2.
\]

Both `ybar` and its projection `yhat` lie in the private box. The segment
between them is in that box, so the mean-value bound and (5) give

\[
 f(v,\widehat y)\le f(v,\overline y)
                 +G H(C)\|B\|_2\|\overline u-v\|_2.
\]

Weighted Cauchy--Schwarz and (4), using `int h=1`, bound the integrated
repair cost by `G H(C)||B||_2 sqrt(k C_m)`. The pre-repair value
`f(v,ybar)` is bounded by the partial theorem's matrix expression because
`Q(v)` is positive semidefinite. Feasibility of `ybar` at `v` is not
required for that matrix Jensen inequality.

Thus, if `A_obj` is the objective Chebyshev coefficient budget from the
partial theorem, the total error is bounded by

\[
 \frac{3A_{\mathrm{obj}}}{2m^2+1}
 +\sum_b G_b H(C_b)\|B_b\|_2\sqrt{k_b C_m}.
\]

With fixed problem data this is `O(1/r)`, reducing to the second-order
coefficient term when every recourse matrix `B_b` vanishes. Large Hoffman
or objective-gradient constants can erase a practical advantage. No
running-time, bit-complexity, or dimension-independent conditioning claim
follows from this estimate.

## 7. Finite-grid reserve and limitations

If a finite quadrature version is included, the quadrature must integrate
the displacement expression in (1), whose individual target degree can
be `2m`. Consequently `N>=m+1` Gauss--Chebyshev nodes are necessary for
this argument even for a constant or linear shared objective. A sufficient
choice is `N=m+floor(max(d_infty,2)/2)`. The objective matrix expression
requires degree `2(m-1)+d_infty`; the same choice covers it. No
polynomial claim about the private QP value function is needed.

Complete recourse is substantive: a positive kernel can put shared mass
where the private feasible set would otherwise be empty. The proof also
requires fixed private constraint coefficients. For example,
`P(u)={y in [-1,1]:uy=0}` has complete recourse but `P(0)=[-1,1]` and
`P(u)={0}` for every nonzero `u`. Such bilinear constraints do not admit
the uniform Hausdorff bound used here. This counterexample concerns the
proof's extension beyond affine recourse; it does not contradict the
stated fixed-matrix theorem.

## 8. Targeted computational check and its scope

Command:

```sh
python research-20260928/solver/check_affine_recourse_transport_review.py
```

The script checks the convolution identities and sharp displacement
constant with exact rational arithmetic for `m=2,...,60`. Separately,
for `m=2,...,10`, it expands the kernel and integrates its monomials using
the exact normalized arcsine moments. These checks agree with (2)--(3).
They do not prove the all-order theorem, preordering positivity, Hoffman
bounds, projection continuity, or sparse gluing. Those steps receive the
arguments above. No project-wide checks or CI inspection were performed.

## 9. Detailed draft review observations

The initial draft's strict final inequality in (12) was valid when
the objective coefficient and repair constants are not both zero. The
stated non-strict convention handles the zero case. There is a harmless
sharpening: integer `r,s` give
`m=floor((r-1)/s)+1=ceil(r/s)>=r/s`. Thus the final denominator may use
`r` in place of `r-1`:

\[
 \frac{3\mathcal A}{2m^2+1}+\sqrt{V_m}\mathcal R
 <\frac{3s^2\mathcal A}{2r^2}
                 +\frac{\sqrt3s\mathcal R}{r},
\]

when `A` and `R` are not both zero, with a non-strict inequality in
general. The current draft incorporates this sharpening with a non-strict
inequality throughout. This changes neither the proof nor its rate.

The zero-density matrix argument is valid for the full augmented matrix
on `(1,u,y)`: (15) bounds all shared diagonal entries, (9) bounds all
private diagonal entries, and positive semidefiniteness then kills every
entry. One notation clarification was suggested: explicitly assign
`ubar=ybar=0` on `{h=0}`, so the expression `h f(v,ybar)` is defined
literally everywhere. Source feasibility is asserted only when `h>0`,
and the actual feasible output on `{h=0}` remains the projection of zero.
The current draft incorporates this explicit definition.

The matrix dimensions in (7)--(9) and the total moment count use the
correct rectangular degree spaces. The finite grid includes the needed
extra quadrature order for the transport polynomial, and its dynamic
programming count separates local QP table construction. No claim of
sharp SDP-gap exponent is inferred from the sharp transport constant.
