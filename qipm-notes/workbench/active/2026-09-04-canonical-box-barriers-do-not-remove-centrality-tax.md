# Universal and entropic box barriers do not remove the separable centrality tax

Status: Proved and independently hostile-audited  
Started: 2026-09-04  
Paper status: Not incorporated  
Confidence: High on the identities and consequences; no theorem for arbitrary coupled barriers

## Result

Let
\[
                         K=(-1,1)^r .
\]
The universal barrier and the entropic barrier of \(K\) both split,
up to additive constants, into sums of identical one-dimensional
barriers:
\[
 U_K(x)=\text{const}-\sum_{i=1}^r\log(1-x_i^2),          \tag{1}
\]
\[
 E_K(x)=\text{const}+\sum_{i=1}^r e(x_i),                \tag{2}
\]
where \(e\) is the one-dimensional entropic barrier of \((-1,1)\).
Both have the optimal self-concordant barrier parameter \(r\).

Consequently neither canonical optimal barrier removes the sharp
centrality tax proved in
[A sharp separable centrality tax in Hessian metric](2026-09-04-sharp-separable-centrality-tax.md).
For either barrier,
\[
 \sup_{w>0,\ s_0<s_1}
 {L_{\rm cen}[s_0,s_1]\over
 d_F(x(s_0),x(s_1))}
 =
 \Gamma_r,\qquad
 \Gamma_r^2=\sum_{j=1}^r(\sqrt j-\sqrt{j-1})^2
            ={1\over4}\log r+O(1).                       \tag{3}
\]
The supremum is approached with increasingly separated positive objective
weights.  The companion discrete theorem therefore also applies: for
the certified sparse-box instances constructed there, central-neighborhood
following takes \(\Omega(r\log r)\) bounded rounds, while an explicit
noncentral Hessian-geodesic chord sequence takes
\(O(r\sqrt{\log r})\) rounds.

Equations (1)--(3) rule out the universal and entropic barriers as a
coupled-barrier escape.  They do **not** prove that every custom
\(\nu=O(r)\) barrier on the box has a growing tax.

## 1. Exact universal-barrier factorization

Use the convex-body definition
\[
                  U_K(x)=\log\operatorname {vol}((K-x)^\circ).
                                                               \tag{4}
\]
For \(y\) in the orthant with sign vector
\(\sigma\in\{-1,1\}^r\), the support function of \(K-x\) is
\[
 h_{K-x}(y)
   =\sum_{i=1}^r |y_i|-x_i y_i
   =\sum_{i=1}^r(1-\sigma_i x_i)|y_i|.                   \tag{5}
\]
The part of the polar in this orthant is therefore a coordinate simplex
of volume
\[
                 {1\over r!}\prod_{i=1}^r{1\over1-\sigma_i x_i}.
                                                               \tag{6}
\]
Summing over the orthants and factorizing the sign sum gives
\[
\begin{aligned}
 \operatorname {vol}((K-x)^\circ)
 &= {1\over r!}\sum_{\sigma}
       \prod_i{1\over1-\sigma_i x_i}\\
 &= {1\over r!}\prod_i
       \left({1\over1-x_i}+{1\over1+x_i}\right)\\
 &= {2^r\over r!}\prod_i{1\over1-x_i^2}.                 \tag{7}
\end{aligned}
\]
Taking logarithms proves (1).

The scalar summand
\[
                         u(t)=-\log(1-t^2)               \tag{8}
\]
is a standard self-concordant barrier with gradient parameter one:
\[
 {u'(t)^2\over u''(t)}
 = {2t^2\over1+t^2}\leq1,
\]
and the ratio tends to one at either endpoint.  Product additivity gives
parameter at most \(r\), while the simple-vertex lower bound for the box
gives at least \(r\).  Thus the parameter is exactly \(r\).

## 2. Exact entropic-barrier tensorization

Let
\[
 A_K(\theta)=\log\int_K e^{\langle\theta,z\rangle}\,dz .
                                                               \tag{9}
\]
Fubini's theorem gives
\[
\begin{aligned}
 A_K(\theta)
 &=\sum_{i=1}^r a(\theta_i),\\
 a(t)
 &=\log\int_{-1}^1 e^{tz}\,dz
   =\log {2\sinh t\over t},                              \tag{10}
\end{aligned}
\]
with the continuous value \(a(0)=\log2\).  Fenchel conjugacy preserves
this Cartesian sum:
\[
 A_K^*(x)=\sum_{i=1}^r a^*(x_i).                         \tag{11}
\]
This proves (2), with \(e=a^*\).

Chewi's theorem that the entropic barrier of an \(n\)-dimensional convex
body is an \(n\)-self-concordant barrier gives parameter one for the
scalar summand and parameter at most \(r\) for (11).  The same
simple-vertex lower bound makes the box parameter exactly \(r\).
Equivalently, \(e'(x)=\theta\), where
\[
                  x=a'(\theta)=\coth\theta-{1\over\theta};
                                                               \tag{12}
\]
its gradient branch maps \((0,1)\) onto \((0,\infty)\), as required by
the scalar-product theorem.

## 3. Transfer of the sharp tax

Both (1) and (2) are products of one-dimensional standard
self-concordant barriers with gradient parameter one, analytic center
zero, and full positive gradient range.  The universal scalar theorem in
the companion note applies verbatim.  It shows that the scalar metric
velocity rises from zero to one, has integrable step tails, and that
translated copies with ordered weights approach every prefix-step
extremizer.  The sharp prefix inequality then gives exactly (3), not only
an upper bound.

The discrete sparse-box construction in that note uses only these scalar
properties.  Hence its actual-accuracy endpoint argument, arbitrary-label
clipped potential, and bounded central-neighborhood round lower bound
hold for both canonical barriers without changing constants except for
the fixed scalar profile.

## 4. Boundary of the conclusion

The calculations expose a useful structural fact: tensorization occurs
for different reasons.  The entropic log-partition integral factorizes
because the reference uniform measure is a product.  The universal polar
volume initially looks coupled because the polar of a translated product
is not a product, but its orthant simplex volumes have a sign sum which
factorizes exactly.

A custom barrier may add genuinely coupled curvature, for example through
redundant inequalities which vanish at selected vertices.  An
\(O(r)\)-parameter budget allows only \(O(r)\) ordinary logarithmic terms,
but no current argument turns that observation into a lower bound for
arbitrary self-concordant barriers.  Conversely, no explicit custom
\(O(r)\)-barrier is presently known here whose worst positive-objective
central paths have uniformly constant arc-to-distance ratio.  The
barrier-independent question is therefore left open.

## Literature boundary

Lee and Yue,
[*Universal Barrier is \(n\)-Self-Concordant*](https://arxiv.org/abs/1809.03011),
prove the dimension-\(n\) parameter bound for the universal barrier on an
arbitrary proper convex domain.  Chewi,
[*The entropic barrier is \(n\)-self-concordant*](https://arxiv.org/abs/2112.10947),
proves the exact dimension-\(n\) bound used above.  The factorization
identities (7) and (11) are elementary specializations to a product
interval.  No novelty is claimed for those identities themselves.  The
new-looking consequence is their combination with the audited sharp
centrality-tax and discrete-round constructions.

## Audit checklist

1. Verify the translated-cube polar and every orthant volume in (5)--(7).
2. Check the universal scalar parameter-one calculation and exact product
   parameter.
3. Verify log-partition and Fenchel-conjugate tensorization in (9)--(11).
4. Check that the scalar entropic barrier meets every hypothesis of the
   sharp product theorem.
5. Keep the arbitrary coupled-barrier question explicitly open.

## Independent hostile audit record

**PASS.**  The translated polar calculation is exact.  In orthant
\(\sigma\), writing \(y_i=\sigma_i u_i\) gives the simplex
\(\sum_i(1-\sigma_i x_i)u_i\leq1\), whose Jacobian-scaled volume is
\(1/[r!\prod_i(1-\sigma_i x_i)]\).  Summing all orthants gives (7), with
no missing \(2^r\), factorial, or translation factor.

The parameter claims are also exact.  For (8), direct differentiation
gives
\[
 u''(t)={2(1+t^2)\over(1-t^2)^2},\qquad
 u'''(t)={4t(3+t^2)\over(1-t^2)^3},
\]
and the standard self-concordance inequality reduces, after squaring, to
\((1-t^2)^2(t^2+2)\geq0\).  Its squared local gradient norm is the displayed
\(2t^2/(1+t^2)\), with supremum one.  Hence the product has parameter
exactly \(r\).  For the entropic barrier, Fubini and separability of Fenchel
conjugacy prove (10)--(11).  The scalar log partition is strictly convex,
\(a'\) maps \(\mathbb R\) onto \((-1,1)\), and Chewi's theorem supplies
standard self-concordance with parameter at most one.  Exactness can also
be seen directly from
\[
 a''(\theta)={1\over\theta^2}-{1\over\sinh^2\theta},\qquad
 \theta^2a''(\theta)=1-\left({\theta\over\sinh\theta}\right)^2\longrightarrow1.
\]
Thus the product gradient parameter has supremum \(r\), independently of
the simple-vertex lower bound.

Finally, along the entropic positive-objective central path
\(\theta=e^s w\), the scalar metric velocity is
\[
 v(s)=\theta\sqrt{a''(\theta)}
     =\sqrt{1-(\theta/\sinh\theta)^2}.
\]
It is increasing from zero to one; it is \(O(e^s)\) at negative infinity
and differs from one by a superexponentially integrable tail at positive
infinity.  The universal scalar profile and the general normalized-scalar
argument in the companion theorem give the same hypotheses.  Therefore
the exact supremum (3) and its discrete central-neighborhood consequence
transfer as stated.  The latter remains a geometric real-weight theorem;
it is not a finite-bit input or quantum-query lower bound.  No step of the
argument extends the conclusion to an arbitrary genuinely coupled
\(O(r)\)-parameter barrier, and the note correctly leaves that question
open.
