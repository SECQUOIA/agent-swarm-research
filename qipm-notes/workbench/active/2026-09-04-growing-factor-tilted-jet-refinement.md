# Removing the \(r^r\) overhead from multivariate tilted jets

Status: Core theorem and arbitrary-coefficient exponential-rank lower bound
independently audited
Started: 2026-09-04
Paper status: Not incorporated
Confidence: High on the mesh tradeoff, source-query ledger, and stated
oracle-model lower bounds

## Result

Let \(X\in[-1,1]^r\) and

\[
 f(z)=\mathbb E[e^{\langle z,X\rangle}],
 \qquad z\in[-K,K]^r.
 \tag{1}
\]

As in the
[fixed-factor compiler](2026-09-04-fixed-factor-multivariate-tilted-jet-compiler.md),
the exact dual width of this coordinatewise sector is

\[
 B=rK.
 \tag{2}
\]

The earlier construction used coordinate mesh \(1/r\) so every Taylor
chart had constant \(\ell_1\) radius.  That choice introduced
\((Cr)^r\) in the center sum.  It is unnecessary: a chart may have
\(\ell_1\) radius \(\Theta(r)\), provided its Taylor order is increased.

For \(0<\epsilon\leq1/2\) and \(0<\alpha<1/2\), there is, with failure
probability at most \(\alpha\), a positive-atom compiler with the same
uniform relative certificate and output support

\[
 R\leq {r+d\choose r},\qquad
 d=O(B+\log(1/\epsilon)),
 \tag{3}
\]

but with quantum source-query complexity

\[
 \widetilde O\left({C_0^r e^{rK}\over\epsilon}\right)
 \tag{4}
\]

for a numerical constant \(C_0>1\), whenever \(K\) is at least a fixed
positive numerical constant.  Thus the factor \(r^r\) is removed.

There is also a sharper small-box form.  If \(0<K\leq a_0\), for a fixed
constant \(a_0\), one can use a single chart and obtain

\[
 \widetilde O\left(
 {e^{rK+Cr\sqrt K}\over\epsilon}\right)
 \tag{5}
\]

queries.  In particular, when \(K=\Theta(1/r)\), the bound is
\(\widetilde O(e^{O(\sqrt r)}/\epsilon)\), not \(C_0^r/\epsilon\).

A complementary measured-source compiler is stronger in this shrinking-box
regime.  With \(B=rK\), its dimension-free empirical-process arm uses

\[
 O\left({e^{4B}B^2\over\epsilon^2}
 [1+\log(1/\alpha)]\right)
\]

source preparations and full-vector-value queries.  It delivers the same
uniform certificate, and its empirical measure can be delivered directly
on at most the sample-count number of atoms.  Consequently, when
\(K=\Theta(1/r)\), both its source-query count and its scenario-induced
positive-atom/cone count have no dimension-dependent factor.

This dimension-free cone statement cannot be improved to a constant
independent of accuracy.  At width \(B\), a Rademacher source in factor
dimension \(r=\Theta(B^2/\epsilon)\) forces every positive atomic uniform
approximation to use \(\Omega(B^2/\epsilon)\) atoms.  In fact, the exact
tradeoff below applies even to signed exponential sums with arbitrary real
nodes and coefficients.  At fixed \(B\), its optimized leading lower is
\((1-o(1))B^2/(16\epsilon)\).  This holds in the nontrivial accuracy regime
stated below.  At fixed \(B>0\), a coherent dimension-free
\(\widetilde O(1/\epsilon)\)-query compiler, if found, would therefore also
have the optimal positive-output size.

More generally, the proof gives an explicit mesh tradeoff rather than only
(4)--(5).  This result leaves open whether the remaining \(C_0^r\) in the
coherent \(1/\epsilon\) large-box bound can be removed by a nonlocal basis or
a genuinely simultaneous quantum estimator.  In the small-box regime, the
dimension dependence is gone, but the empirical arm has the classical
\(1/\epsilon^2\) accuracy law.

## Mesh tradeoff

For a coordinate chart radius \(a\in(0,K]\), take a one-dimensional center
set \({\cal C}_{K,a}\subset[-K,K]\) of spacing \(2a\), adjusted at the
endpoints, and its \(r\)-fold tensor product.  Define

\[
 H(K,a):=\sum_{c\in{\cal C}_{K,a}}e^{|c|}.
 \tag{6}
\]

The elementary geometric-series estimate is

\[
 H(K,a)\leq
 1+{C e^K\over1-e^{-2a}}.
 \tag{7}
\]

When \(K\leq a\), use the single center zero instead, so \(H(K,K)=1\).
Every point in the parameter cube is within coordinate distance \(a\) of a
center; hence its local displacement \(t\) obeys

\[
 \|t\|_\infty\leq a,\qquad
 \|t\|_1\leq\sigma:=ra.
 \tag{8}
\]

At tensor center \(z_j\), use the normalized tilt

\[
 W_j(x)=e^{\langle z_j,x\rangle-\|z_j\|_1},\qquad
 b_j=\mathbb E[W_j(X)]\geq e^{-2\|z_j\|_1}.
 \tag{9}
\]

The inverse-square-root tilted masses sum as

\[
 \sum_j b_j^{-1/2}
 \leq\sum_j e^{\|z_j\|_1}
 =H(K,a)^r.
 \tag{10}
\]

This identity includes the covering number; no extra factor equal to the
number of centers is needed.

## Local jets with growing radius

For a multi-index \(\nu\), put

\[
 c_\nu={a^{|\nu|}\over\nu!},\qquad
 S_{r,m}(a)=\sum_{|\nu|\leq m}\sqrt{c_\nu}.
 \tag{11}
\]

Writing

\[
 s(a):=\sum_{q=0}^{\infty}{a^{q/2}\over\sqrt{q!}},
 \tag{12}
\]

the tensor majorant gives

\[
 S_{r,m}(a)\leq s(a)^r.
 \tag{13}
\]

Because the local MGF can fall by \(e^{-\sigma}\) relative to its value at
the chart center, use the confidence allocation

\[
 \xi_\nu=
 \min\left\{1,\,
 {c\epsilon e^{-\sigma}\over
  S_{r,m}(a)\sqrt{c_\nu}}\right\}.
 \tag{14}
\]

The tilted signed feature
\(\mathbb E[W_j(X)X^\nu]\) is estimated to additive accuracy
\(\Theta(b_j\xi_\nu)\).  Distribution-sensitive amplitude estimation costs
\(O((\xi_\nu\sqrt{b_j})^{-1})\), and

\[
 \sum_{\nu:\xi_\nu<1}{1\over\xi_\nu}
 \leq {e^\sigma S_{r,m}(a)^2\over c\epsilon}
 \leq {e^{ra}s(a)^{2r}\over c\epsilon}.
 \tag{15}
\]

As before, the rounded source histogram is feasible in the tilted-feature
confidence LP.  Any feasible histogram has feature discrepancy
\(O(b_j\xi_\nu)\), including the trivial inactive-feature bound supplied by
the accurately estimated zeroth feature.  For
\(\|t\|_\infty\leq a\), the summed multi-index contribution satisfies

\[
 \sum_{|\nu|\leq m}{|t^\nu|\over\nu!}
 O(b_j\xi_\nu)
 \leq O(\epsilon e^{-\sigma}b_j).
 \tag{15a}
\]

Indeed, the active features contribute at most
\(c\epsilon e^{-\sigma}b_j\); for an inactive feature, the defining
inequality \(\xi_\nu=1\) bounds \(c_\nu\) by
\((c\epsilon e^{-\sigma}/S_{r,m}(a))\sqrt{c_\nu}\), giving the same bound
after summation.  The local MGF is at least \(e^{-\sigma}b_j\).

The two Taylor remainders contribute relative error at most

\[
 C e^{2\sigma}{\sigma^{m+1}\over(m+1)!}.
 \tag{16}
\]

Thus it suffices to take

\[
 m=O\bigl(1+ra+\log(1/\epsilon)\bigr).
 \tag{17}
\]

This is the central trade: increasing the chart radius removes centers, and
only increases the temporary Taylor degree.  It does not change the final
degree \(d\) or support in (3), because post hoc compression still uses a
global total-degree Taylor polynomial on dual width \(B=rK\).

Combining (10), (13), and (15) gives the general query bound

\[
 Q(a)=\widetilde O\left(
 {e^{ra}s(a)^{2r}H(K,a)^r\over\epsilon}
 \right).
 \tag{18}
\]

For \(K\geq a_0\), choose any fixed numerical \(a_0\in(0,1)\).
Equations (7) and (18) give

\[
 Q(a_0)
 \leq\widetilde O\left(
 {[
 e^{a_0}s(a_0)^2C/(1-e^{-2a_0})
 ]^r e^{rK}\over\epsilon}\right),
 \tag{19}
\]

which is (4).

For \(K<a_0\), take the single center zero and \(a=K\).  The elementary
bound

\[
 \log s(K)\leq C\sqrt K
 \qquad(0<K\leq a_0)
 \tag{20}
\]

follows by separating the \(q=0,1\) terms and bounding the remaining
factorial series.  Equations (18) and (20) give (5).

The public slope rounding and final moment compression are unchanged:
coordinate spacing \(h=\Theta(\epsilon/(rK))\), public grid size

\[
 O((1+rK/\epsilon)^r),
 \tag{21}
\]

and at most \(\binom{r+d}{r}\) delivered atoms.  The temporary confidence
LP now has

\[
 O\left(
 (1+K/a)^r {r+m\choose r}
 \right)
 \tag{22}
\]

rows.  With constant \(a=a_0\), this is
\((1+K)^r\binom{r+O(r+\log(1/\epsilon))}{r}\), so the improvement in source
queries does not remove the exponential classical postprocessing cost when
\(r\) grows.

## Lower bound and what is not resolved

The opposite-corner source from the fixed-factor note still gives

\[
 Q_{\rm quantum}=\Omega(e^{rK}/\epsilon),\qquad
 Q_{\rm classical}=\Omega(e^{2rK}/\epsilon^2)
 \tag{23}
\]

in the hidden weighted state-preparation and i.i.d. sampling models,
respectively.  It changes all \(r\) coordinates and evaluates the MGF at
the opposite cube corner, so \(rK\) is the correct exponent for the
coordinatewise sector.

Together, (4) and (23) locate the growing-\(r\) quantum frontier between
\(e^{rK}/\epsilon\) and \(C_0^r e^{rK}/\epsilon\).  In particular, the old
\(r^r\) gap was algorithmic rather than information-theoretic.  No
information-theoretic lower bound forcing \(C^r\) was found.

There is a limited method-specific obstruction.  For tensor charts with
fixed coordinate radius \(a\), the proof cost per coordinate contains

\[
 \chi(a):=
 e^a s(a)^2(1-e^{-2a})^{-1}>1.
 \tag{24}
\]

Therefore optimizing \(a\) inside this independent-feature,
tensor-cover proof can change the numerical base but cannot eliminate an
exponential-in-\(r\) prefactor.  This is not a lower bound against
non-tensor covers, correlated confidence regions, or simultaneous quantum
estimation.

For shrinking boxes \(K=\Theta(1/r)\), the single-chart bound (5) and (23)
leave a larger subexponential gap: that upper is
\(e^{O(\sqrt r)}/\epsilon\), while the opposite-corner lower is only
\(\Omega(1/\epsilon)\). The empirical construction below removes the
dimension-dependent exponential from this regime.

## Empirical fallback removes the small-box exponential

Audit status: Independently checked for the net and Rademacher arms,
including the oracle contract, high-probability uniform certificate, and
the direct-empirical versus post hoc moment-compression support minimum.

There is a simple complementary construction which is better when
\(B=rK\) is small.  Measure independent preparations of the weighted source
and, for every measured source index, query and round its full \(r\)-vector;
then form the empirical distribution \(\widehat\mu_n\).  Thus one sample
costs one state preparation and one full-vector-value query under the oracle
contract of this note.  A coordinate-value oracle would instead introduce
an additional factor \(r\).  For a fixed \(z\), the normalized
variable

\[
 Z_z=e^{\langle z,Y\rangle-B}\in[0,1]
 \tag{24a}
\]

has mean at least \(e^{-2B}\).  Multiplicative Chernoff bounds therefore
give relative-\(\eta\) accuracy at a fixed point using
\[
 O(e^{2B}\eta^{-2}\log(1/\delta))
\]
samples.

Take an \(\ell_\infty\) net of \([-K,K]^r\) with coordinate covering radius
\[
 s={\epsilon\over Cr}.
\]
It has
\[
 M\leq\left(1+{CKr\over\epsilon}\right)^r
 \tag{24b}
\]
points.  For every positive measure on \([-1,1]^r\), each coordinate of the
gradient of its log MGF is a tilted mean in \([-1,1]\).  Hence the
log-ratio of two such MGFs is \(2\)-Lipschitz in \(\ell_1\).  A union bound
over the net, followed by interpolation over distance at most \(rs\),
proves a uniform relative certificate.  Take the fixed-net relative error
\(\eta=\Theta(\epsilon)\) and choose \(C\) so that the net error and
\(2rs\) together consume only a fixed fraction of \(\epsilon\).  The same
empirical samples are reused at every net point, so the net size enters only
through the confidence logarithm.  The resulting sample count is

\[
 Q_{\rm emp}=
 O\left(
 {e^{2B}\over\epsilon^2}
 \left[
 r\log\left(1+{CKr\over\epsilon}\right)
 +\log{1\over\alpha}
 \right]\right)
 \tag{24c}
\]

classical samples.  A quantum algorithm can obtain those samples by
measuring one coherent source preparation and making the full-vector query
described above per sample.  Public rounding with
\(h=\Theta(\epsilon/B)\) for \(B>0\), capped at the slope-cube diameter,
costs only another relative \(e^{\pm Bh}\) factor.  The case \(B=0\) needs
neither rounding nor sampling.

The net is unnecessary when the dual width \(B\) is small.  A second,
dimension-free empirical-process bound follows directly from the geometry
of the parameter cube.  Put \(F_z(y)=e^{\langle z,y\rangle}\) and

\[
 D_n:=\sup_{z\in[-K,K]^r}|(\widehat\mu_n-\overline\mu)F_z|.
\]

The empirical process is unchanged if the constant one is subtracted.
Thus symmetrization applied to \(F_z-1\), followed by the contraction
lemma for \(u\mapsto e^u-1\) on \([-B,B]\), gives

\[
 \mathbb E D_n
 \leq {C e^B\over n}\,
 \mathbb E_\sigma\sup_{\|z\|_\infty\leq K}
 \left|\sum_{i=1}^n\sigma_i\langle z,Y_i\rangle\right|
 \leq {C e^B B\over\sqrt n}.
 \tag{24c-1}
\]

The last inequality uses
\(K\mathbb E_\sigma\|\sum_i\sigma_iY_i\|_1
\leq Kr\sqrt n=B\sqrt n\).  Changing one sample changes \(D_n\) by at
most

\[
 {e^B-e^{-B}\over n}\leq {2Be^B\over n}.
\]

McDiarmid's inequality and \(\overline f(z)\geq e^{-B}\) therefore imply
the simultaneous relative certificate with

\[
 Q_{\rm rad}=O\left(
 {e^{4B}B^2\over\epsilon^2}
 \left[1+\log{1\over\alpha}\right]
 \right).
 \tag{24c-2}
\]

This bound has a worse sector exponent than (24c), but it has no explicit
dimension or covering-number factor.  It is strongest precisely in the
shrinking-box regime.  For \(B=0\), the MGF is identically one and no
samples are needed; otherwise the displayed bound may harmlessly be
replaced by its maximum with one.

The rounded empirical measure itself is already a valid classical positive
atomic compiler, with exactly the same uniform certificate and at most the
chosen sample-count number of atoms.  It may therefore be delivered
directly.  If that count exceeds the moment dimension, match all of its
ordinary moments through total degree
\[
 d=O(B+\log(1/\epsilon))
\]
and apply Caratheodory--Tchakaloff compression.  The same two-remainder
argument as before leaves at most \(\binom{r+d}{r}\) positive atoms and
consumes only a reserved fraction of the uniform error budget.  Explicitly,
matching the constant moment preserves total mass one, and matching every
monomial of total degree at most \(d\) makes the scalar Taylor polynomials
of \(e^{\langle z,y\rangle}\) agree.  Hence, uniformly on the cube,
\[
 |g_\psi(z)-\widehat f_n(z)|
 \leq 2e^B{B^{d+1}\over(d+1)!}.
\]
Choosing \(d\) so that the right side is at most
\(c\epsilon e^{-B}\leq c\epsilon\overline f(z)\) requires only
\(d=O(B+\log(1/\epsilon))\).  The moment-space dimension, including the
constant, is \(\binom{r+d}{r}\), which is also the Tchakaloff support bound.
Thus, if \(n_{\rm emp}\) is the ceiling of the smaller of the sample bounds
in (24c) and (24c-2), the empirical compiler has

\[
 R_{\rm emp}\leq
 \min\left\{n_{\rm emp},{r+d\choose r}\right\}.
 \tag{24c-3}
\]

Combining the coherent tilted-jet method, empirical fallback, and an
indexed full read gives the independently audited hybrid upper

\[
 \widetilde O\left(
 \min\left\{
 N,\,
 {C_0^r e^B\over\epsilon},\,
 {e^{2B}\over\epsilon^2}
 \left[r\log\left(1+{rK\over\epsilon}\right)
 +\log{1\over\alpha}\right],\,
 {e^{4B}B^2\over\epsilon^2}
 \left[1+\log{1\over\alpha}\right]
 \right\}\right).
 \tag{24d}
\]

The \(N\) arm requires indexed weight-and-vector access; the empirical arms
require measurable preparations plus full-vector-value access.  In particular, for
\(K=\Theta(1/r)\) and constant \(\epsilon,\alpha\), the dimension-free arm
of (24d), and its support in (24c-3), are both \(O(1)\), rather than
\(e^{O(\sqrt r)}\).
Consequently neither the old \(r^r\) nor the single-chart
\(e^{O(\sqrt r)}\) overhead is information-theoretically necessary in that
regime.  For fixed \(B\), the remaining accuracy gap is the usual one
between the coherent lower \(\Omega(1/\epsilon)\) and this measured-source
fallback's \(O(1/\epsilon^2)\).  Equation (24c) retains a uniform-class
dimension factor but has the better sector exponent when \(B\) grows.
The \(O(1)\) claims concern source queries and atom/cone count, not total
output size: each atom contains \(r\) coordinates, so merely reading and
writing the returned atoms costs \(\Omega(rR_{\rm emp})\).  Neither
empirical arm needs to evaluate its proof net or perform moment compression:
direct empirical delivery takes \(O(n_{\rm emp}r)\) vector processing, in
addition to oracle costs.  If compression is chosen because
\(\binom{r+d}{r}<n_{\rm emp}\), then it instead processes that many moment
features.  The net in (24b) enters the sample bound only through its
confidence logarithm.

## A sharp measure-first obstruction, not an output obstruction

The \(1/\epsilon^2\) dependence of the empirical arms is unavoidable for
any compiler whose only source access consists of independent computational-
basis measurements of fresh prepared source states, followed by arbitrary
processing which makes no further coherent source queries.
This remains true even if the subsequent classical algorithm reweights,
compresses, or outputs atoms that were not observed.
Here the primitive returns only the measured source label from the canonical
weighted preparation; an unspecified unitary completion or retained quantum
workspace is not part of this measure-first model.

Fix a numerical width \(B_0>0\), put \(K=B_0/r\), and let the source be
supported on the opposite corners

\[
 x^+=\mathbf 1,\qquad x^-=-\mathbf 1,
\]

with \(\Pr[X=x^+]=p\).  At \(z^*=K\mathbf1\),

\[
 f_p(z^*)=e^{-B_0}+(e^{B_0}-e^{-B_0})p.
 \tag{24e}
\]

For sufficiently small \(\epsilon\), take
\(p_\pm=1/2\pm c_0\epsilon\), where

\[
 c_0>{1\over2}\coth B_0
\]

is fixed and \(\epsilon\leq1/(2c_0)\).  Indeed,
\(f_{p_\pm}(z^*)=\cosh B_0\pm2c_0\epsilon\sinh B_0\), so this strict
inequality makes the relative-\(\epsilon\) intervals around
\(f_{p_-}(z^*)\) and \(f_{p_+}(z^*)\) disjoint.  A successful uniform
compiler therefore distinguishes the two promises simply by evaluating its
classical output at \(z^*\).

If every preparation is measured, its entire information about the promise
is one Bernoulli sample.  Since

\[
 D_{\rm KL}(\operatorname{Ber}(p_-)\|\operatorname{Ber}(p_+))
 \leq C\epsilon^2,
\]

the Bretagnolle--Huber testing bound gives
\(2\alpha\geq\tfrac12\exp(-qC\epsilon^2)\).  Combining it with the
ordinary constant-error two-point lower bound proves, uniformly for
\(0<\alpha<1/4\),

\[
 q=\Omega\left({1\over\epsilon^2}\log{1\over\alpha}\right)
 \tag{24f}
\]

for failure probability at most \(\alpha<1/4\).  Thus (24c-2) is optimal
in its accuracy and confidence dependence at fixed nonzero \(B_0\) within
the whole measure-first class, not merely for the literal empirical mean.

Crucially, (24f) is not caused by the requirement of a classical positive
output.  Under coherent access to the preparation unitary and its inverse,
standard amplitude estimation estimates \(p\) to additive
\(O_{B_0}(\epsilon)\) using
\(O(\epsilon^{-1}\log(1/\alpha))\) queries.  After clipping
\(\widetilde p\) to \([0,1]\), which cannot increase its error, it outputs
the classical
positive measure

\[
 \widetilde p\,\delta_{x^+}+(1-\widetilde p)\delta_{x^-}.
\]

For every \(z\) in the cube, its absolute MGF error is at most
\(2\sinh(B_0)|\widetilde p-p|\), while \(f_p(z)\geq e^{-B_0}\), so the
measure has the required uniform relative certificate.  Conversely, the
usual two-amplitude lower bound gives \(\Omega(1/\epsilon)\) coherent
queries at constant failure probability on this same family.

Therefore neither positivity, classical output, nor dimension forces the
empirical \(1/\epsilon^2\) law.  What remains open is a coherent compiler
which, for bounded \(B\), achieves a dimension-free
\(\widetilde O_B(1/\epsilon)\) query bound for arbitrary sources while still
extracting a positive classical atomic measure.  For variable \(B\), the
corresponding target must include at least the known \(e^B/\epsilon\)
opposite-corner lower bound.  Any
impossibility proof must use a genuinely many-direction family rather than
the two-corner source.

## Exponential-feature rank has a linear accuracy floor

There is nevertheless a genuine classical exponential-feature output
obstruction at bounded width.  It is linear, rather than quadratic, in
\(1/\epsilon\), and the span argument does not require positive
coefficients.

Fix \(B>0\), an integer \(r\geq B\), and set

\[
 K={B\over r},
 \tag{24g}
\]

and let \(\mu\) be the uniform law on \(\{-1,1\}^r\).  Suppose an arbitrary
real exponential sum

\[
 g(z)=\sum_{j=1}^R\theta_j e^{\langle z,y_j\rangle},
 \qquad \theta_j\in\mathbb R,\quad y_j\in\mathbb R^r,
\]

satisfies the uniform relative-\(\epsilon\) MGF certificate on
\([-K,K]^r\), where \(0<\epsilon<1\).  Define
\(L_\epsilon=\log((1+\epsilon)/(1-\epsilon))\), discard any zero
coefficients, and put
\(d=\dim\operatorname{span}\{y_1,\ldots,y_R\}\).  Then

\[
 \boxed{
 d\geq r-{L_\epsilon\over\log\cosh(B/r)},\qquad
 d>r-{3r^2\over B^2}L_\epsilon,\qquad R\geq d.}
 \tag{24h}
\]

To prove this, let
\(E=\operatorname{span}\{y_1,\ldots,y_R\}^{\perp}\), whose dimension is
\(m=r-d\).  The sharp combinatorial form of Vaaler's cube-
section theorem gives a probability measure \(P\) on
\(E\cap[-1,1]^r\) such that

\[
 \int u\otimes u\,dP(u)\succeq I_E.
\]

Taking traces shows that some \(u\in E\cap[-1,1]^r\) has
\(\|u\|_2^2\geq m\).  Put \(z=Bu/r\).  Since \(r\geq B\), one has
\(K=B/r\leq1\).  Thus \(z\in[-K,K]^r\) and every exponent vanishes, so

\[
 g(z)=\sum_j\theta_j=g(0).
 \tag{24i}
\]

In contrast, independence under \(\mu\) gives

\[
 \log f_\mu(z)=\sum_{k=1}^r\log\cosh(z_k)
 \geq \|u\|_2^2\log\cosh(B/r)
 \geq (r-d)\log\cosh(B/r).
 \tag{24j}
\]

Here \(t\mapsto\log\cosh(t)/t^2\) is decreasing for \(t>0\): the
numerator controlling its derivative is
\(t\tanh t-2\log\cosh t\), whose derivative is negative because
\(t<\sinh t\cosh t\).  Hence
\(\log\cosh((B/r)u_k)\geq u_k^2\log\cosh(B/r)\).
Also \(\log\cosh t>t^2/3\) for \(0<|t|\leq1\).

The certificate at zero and at \(z\), together with (24i), imply

\[
 f_\mu(z)\leq{1+\epsilon\over1-\epsilon}.
\]

Comparing logarithms with (24j) proves the first inequality in (24h).
If \(d<r\), then \(u\ne0\), so the strict quadratic bound gives the second
inequality; if \(d=r\), that inequality is immediate.  Finally,
\(R\geq d\).  Notice that neither
positivity nor a bound on \(y_j\) entered the proof; the certificate itself
makes \(g(0)>0\).  Only the evaluation point—not an approximating node—must
lie in the certified parameter cube.  The theorem grants exact arbitrary
real coefficients and nodes, so it applies to every positive, finite-bit,
or source-cube-restricted subclass, but does not impose a coefficient-bit
bound.

Optimizing the quadratic inequality in (24h) already gives a useful fully
explicit bound.  If
\(B^2/(6L_\epsilon)\geq B+1\), choose the integer
\(r=\lfloor B^2/(6L_\epsilon)\rfloor\).  Completing the square gives

\[
 R>{B^2\over12L_\epsilon}-{3L_\epsilon\over B^2}.
 \tag{24j-1}
\]

The exact \(\log\cosh\) inequality is asymptotically sharper.  For fixed
\(B>0\) and \(\epsilon\downarrow0\), choose instead
\(r=\lfloor B^2/(4L_\epsilon)\rfloor\).  Then \(r\geq B\),
\(B/r=(4L_\epsilon/B)(1+o(1))\), and
\(\log\cosh t=(t^2/2)(1+o(1))\).  The first inequality in (24h) yields

\[
 R\geq d\geq(1-o(1)){B^2\over8L_\epsilon}
   =(1-o(1)){B^2\over16\epsilon}.
 \tag{24j-2}
\]

Thus any general bounded-width compiler using a classical exponential sum,
even a signed one with arbitrary real nodes, needs
\(\Omega(B^2/\epsilon)\) terms in the worst case.  The open dimension-free
coherent target
\(\widetilde O(e^B\operatorname{poly}(B)/\epsilon)\) would therefore be
optimal simultaneously in accuracy dependence and absence of an extra
factor-rank cost, up to logarithms and \(B\)-dependence.  The empirical
compiler's \(O(1/\epsilon^2)\) direct support is not output-optimal;
optional moment compression does not close this particular gap at growing
\(r\).

### Conic and barrier corollary

In the reusable direct positive-mixture ECP, each retained atom is
represented by one local three-dimensional exponential-cone factor before
aggregation.  Equation (24h) therefore forces

\[
 R_{\exp}\geq(1-o(1)){B^2\over16\epsilon}
 \tag{24k}
\]

on the bounded-width growing-factor family above.  The
[exact exponential-product barrier theorem](2026-09-04-exponential-product-exact-barrier-parameter.md)
shows that the optimal parameter of the full ambient product
\(K_{\exp}^{R_{\exp}}\) is exactly \(3R_{\exp}\), even among arbitrary
coupled standard self-concordant barriers.  Hence every such barrier
satisfies

\[
 \nu_{\rm ambient}\geq3R_{\exp}
 \geq(3-o(1)){B^2\over16\epsilon}.
 \tag{24l}
\]

The standard separable exponential-cone barrier attains
\(3R_{\exp}\).  Thus coupling factors cannot improve this ambient barrier
parameter at all.

This corollary is restricted to reusable, one-cone-per-atom positive-
mixture ECPs and to barriers defined on their full ambient cone product.  It
does not lower-bound arbitrary exponential-cone extended formulations, a
barrier only on a projected feasible image, or the iteration complexity of
all interior-point algorithms.

## Optimization consequence

For the \(r\)-factor entropic-risk program in the fixed-factor note, the
same inner/outer exponential-cone programs and error

\[
 {\gamma V_{\max}\over\beta}\log{U_*\over L_*}
\]

remain valid.  At additive target \(\tau\) and \(K\geq a_0\), the improved
source-query count is

\[
 \widetilde O\left(
 C_0^r e^{rK}
 \max\left\{1,{\gamma V_{\max}\over\beta\tau}\right\}
 \right),
 \tag{25}
\]

while the delivered cone count and barrier parameter remain

\[
 R\leq {r+d\choose r},\qquad
 d=O\left(rK+
 \log_+{\gamma V_{\max}\over\beta\tau}\right),\qquad
 \nu\leq\nu_0+3R+O(1).
 \tag{26}
\]

For any \(B=rK\), the dimension-free empirical arm instead gives the
end-to-end source bound

\[
 O\left(
 e^{4B}B^2
 \max\left\{1,
 {\gamma^2V_{\max}^2\over\beta^2\tau^2}\right\}
 \left[1+\log{1\over\alpha}\right]
 \right)
 \tag{27}
\]

under measurable source preparations and full-vector-value access.  Thus,
when \(B=O(1)\) and the risk accuracy/confidence parameters are fixed, even
the certified multivariate entropic-risk ECP has no factor-rank dependence
in its source-query or scenario-induced exponential-cone count.  Indeed,
direct empirical delivery gives

\[
 R_{\rm emp}\leq \min\left\{\lceil Q_{\rm risk,rad}\rceil,
 {r+d\choose r}\right\},\qquad
 \nu\leq\nu_0+3R_{\rm emp}+O(1).
 \tag{28}
\]

Here \(Q_{\rm risk,rad}\) denotes the right side of (27).

The base barrier \(\nu_0\), the \(r\) coordinates stored in every atom, and
the linear-algebra cost may still depend on \(r\).  Splitting each dense
factor inner product through a balanced sum tree gives \(O(rR_{\rm emp})\)
linear-lift size without adding cone-barrier parameter.  Thus the empirical
arm changes both source compilation and the scenario-induced cone count,
while the coherent arm changes only source compilation relative to (26).

## Literature screen

A targeted search on 2026-09-04 checked multivariate Laplace-transform
quadrature, exponential-family and Bayesian coresets, vector-valued quantum
mean estimation, simultaneous amplitude estimation, and uniform empirical
Laplace-transform approximation.  Symmetrization, contraction, and
Rademacher-complexity uniform laws used in (24c-1)--(24c-2) are standard;
see, for example, [Wainwright's notes on uniform
laws](https://www.stat.berkeley.edu/~mjwain/stat210b/Chap4_Uniform_Feb4_2015.pdf).
The coherent two-point comparison uses the standard amplitude-estimation
frontier of
[Brassard--Hoyer--Mosca--Tapp](https://arxiv.org/abs/quant-ph/0005055).
The signed exponential-rank lower bound (24h) invokes the sharp
cube-section quadratic-form
theorem of
[Ball--Prodromou](https://doi.org/10.1112/blms/bdp062); the MGF/support
consequence drawn from it here was not found in the screened scenario-
compression literature.  A follow-up search for multivariate signed
exponential-sum approximation, exponential-feature rank, product-cosh
approximation, and Laplace-transform separation rank found work on
[discretizing uniform norms of exponential
sums](https://doi.org/10.1007/s00365-022-09565-6) and broad worst-case
[ridge-function approximation
bounds](https://doi.org/10.1137/20M1356348), but no arbitrary-node signed
exponential-rank lower for the product-cosh MGF matching (24h).  This is
evidence against an immediate collision, not a priority claim.
The closest
established ingredients remain multivariate Tchakaloff compression,
[Bayesian exponential-family coresets](https://arxiv.org/abs/1906.03329),
and [near-optimal quantum multivariate mean
estimation](https://arxiv.org/abs/2111.09787).  The latter estimates a
vector mean in normed error models; applying it to the exponentially
heteroscedastic relative-confidence system here, while still extracting a
positive classical measure, does not directly remove the remaining
dimension factor.  No source found gives the mesh-radius
tradeoff (18), the removal of \(r^r\) by growing local Taylor degree, or a
positive-atom MGF compiler combining the width-sensitive empirical bound,
post hoc exact moment compression, and this query/support ledger.

The result should therefore be framed as a sharper construction, not as a
lower bound proving the remaining \(C_0^r\) necessary.  Priority remains
subject to a broader expert review.

## Independent audit scope

The audit checked the general-radius tensor cover, including endpoint
adjustment and the factorization of the weighted center sum.  It checked
the worst-case tilt mass, active and inactive feature errors in (15a), both
Taylor remainders, and the sufficient degree
\(m=O(1+ra+\log(1/\epsilon))\).  It also checked that the local degree does
not enter the delivered support after global moment compression, and that
the temporary row count (22), rather than the source-query count, retains
the full growing-dimensional classical postprocessing burden.

For (23), the audit uses the same two-corner promise as the fixed-factor
note: a Bernoulli mass of order \(e^{-2rK}\), separated by order
\(\epsilon e^{-2rK}\).  Its state-preparation angle separation is order
\(\epsilon e^{-rK}\), while its one-sample KL divergence is order
\(\epsilon^2e^{-2rK}\).  Thus the two lower bounds apply in the stated
hidden weighted-state and i.i.d. sample models.  They do not, without the
finite-population conditions in the fixed-factor note, assert the same
unsaturated laws for an indexed uniform scenario list.  No counterexample
was found to the claimed upper bounds or to the deliberately
method-specific obstruction.

For the empirical fallback, the audit also checked that no compression is
needed to transfer the certificate to the optimization problem.  The
rounded empirical law is itself a positive probability measure, so its
uniform MGF sandwich gives the same logarithmic perspective sandwich and
the same inner/outer ECP shifts as any other positive-atom compiler.
Direct delivery uses at most one atom per sample.  Tchakaloff compression
is only an optional second representation, so choosing the smaller one
proves (24c-3).  At fixed \(B,\epsilon,\alpha\), the Rademacher sample count
and the scenario-induced exponential-cone count are therefore \(O(1)\),
while storing the \(r\)-coordinate atoms and their linear coefficients
still costs \(\Omega(r)\) words.

For (24g)--(24l), the audit checked the exact Ball--Prodromou theorem on
the cube section \(E\cap[-1,1]^r\).  Its second-moment domination of
\(I_E\), after taking traces, supplies a point with squared norm at least
\(\dim E=r-d\).  Orthogonality makes every atomic exponential equal to one
at the chosen \(z\), regardless of the signs or sum of the coefficients;
the two relative certificate inequalities alone compare \(f_\mu(z)\) to
\(f_\mu(0)=1\).  The Rademacher MGF factorization and monotonicity of
\(\log\cosh t/t^2\) give the first rank inequality in (24h); the strict
bound \(\log\cosh t>t^2/3\) gives the second.  The floor computation in
(24j-1) is exact.  For fixed \(B\), optimizing the exact bound at
\(r=(1+o(1))B^2/(4L_\epsilon)\), rather than the quadratic corollary's
\(B^2/(6L_\epsilon)\), gives the sharper leading constant in (24j-2).

The theorem allows arbitrary signed coefficients and arbitrary
\(y_j\in\mathbb R^r\): the Ball--Prodromou point is controlled by the cube
section of their orthogonal complement, not by atom norms or coefficient
signs.  Negative-weight sums need not themselves have a direct convex
exponential-cone lift.  The conic consequence instead follows because the
rank lower bound applies in particular to the positive-mixture subclass;
it remains limited to the reusable one-exponential-cone-per-atom lift.
The twice-audited exact exponential-product theorem gives
\(\nu_{\rm ambient}\geq3R_{\exp}\) for every standard self-concordant
barrier, including non-logarithmically-homogeneous and coupled barriers, on
the full ambient cone product.  It does not cover arbitrary projected lifts
or all IPMs.

For (24e)--(24f), the audit checked the exact relative-interval separation
\(c_0>\tfrac12\coth B_0\), the Bernoulli KL bound, and the confidence law.
Bretagnolle--Huber supplies the \(\log(1/\alpha)\) growth for small
\(\alpha\), while the constant-error testing bound supplies the remaining
\(\alpha\in[\alpha_0,1/4)\) range.  In the coherent arm, clipping the
amplitude estimate preserves positive weights, and the
\(2e^{B_0}\sinh(B_0)|\widetilde p-p|\) relative bound is uniform on the
whole cube.  The lower therefore applies to the explicitly defined
measure-first access class, not to coherent preparations.
