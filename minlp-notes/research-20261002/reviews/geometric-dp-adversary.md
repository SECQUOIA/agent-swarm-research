# Adversarial review of the geometric-grid certificate

Date: 2026-10-02. Scope: the proposed formulation and
`geometric-dp/independent-derivation.md`. This is a mathematical review,
not a literature or novelty audit.

The central argument survives this review. The corrected-grid minimum is
a valid lower bound, the stated contraction constants are valid, and the
purely integer problem has a finite exact certificate under the stated
growth assumption. No counterexample was found to those claims with their
full assumptions. The main qualifications concern the meaning of the
curvature assumption, unknown growth constants, dynamic-programming cost
accounting, and exact arithmetic.

## 1. The lower bound and constants check out

Write the growth constant as \(\mu\) and the current center as \(z\).
Assume

\[
F(x)-f^*\ge\mu\|x-x^*\|^2
\]

on the mixed product domain, with one fixed optimizer \(x^*\).
For each coordinate, independently round a feasible point to adjacent
grid endpoints with its mean preserved. For a rounded interval of length
\(\ell\), both endpoints carry a penalty of at least \(L\ell^2/8\).
Its rounding variance is at most \(\ell^2/4\). A unit integer interval
contains no omitted feasible point and needs no penalty.

Consequently the expected penalty pays for the entire rounding error.
For any exact corrected-grid minimizer \(y\),

\[
Q=F(y)-D(y)\le f^*\le F(y),\qquad F(y)-f^*\le D(y).
\]

The certificate itself does not require quadratic growth, a known
optimizer, or a first-order condition at the optimizer.

The adjacent-interval estimate gives

\[
D(y)\le\frac L4\left(nh^2+\theta^2\|y-z\|^2\right).
\]

Setting \(E=\|y-x^*\|^2\), \(E_{\rm old}=\|z-x^*\|^2\), and using
\(\|y-z\|^2\le2E+2E_{\rm old}\), one obtains

\[
(\mu-L\theta^2/2)E
\le Lnh^2/4+(L\theta^2/2)E_{\rm old}.
\]

Thus \(\theta^2\le\mu/(8L)\) implies exactly

\[
E\le\frac{4L}{15\mu}nh^2+\frac1{15}E_{\rm old}.
\]

Halving \(h\) gives the invariant \(E_j\le Bnh_j^2\), with
\(B=\max\{1,4L/(11\mu)\}\). The additional restriction
\(\theta\le1/2\) ensures \(B\theta^2\le1/4\), and hence
\(D(y_j)\le(7L/8)nh_j^2\). The stage-zero initialization in the
independent derivation is sufficient. These bounds hold for every
corrected-grid minimizer, including ties.

## 2. Diagonal curvature is sufficient, but needs the right proof

The independent derivation assumes a full Taylor upper bound, supplied
there by a Lipschitz gradient. The weaker proposed assumption
\(\partial_{ii}F\le L\) is also sufficient. Its proof must use
successive independent coordinate rounding and the one-dimensional
interpolation inequality

\[
\mathbb E F(\ldots,Y_i,\ldots)
\le F(\ldots,x_i,\ldots)+(L/2)\operatorname{Var}(Y_i).
\]

Sum this inequality while conditioning on the coordinates already
rounded. An upper bound on diagonal second derivatives alone does not
imply the full-vector Taylor upper bound: \(F(x_1,x_2)=M x_1x_2\)
has zero diagonal curvature and arbitrarily large mixed curvature.
Independence is what makes the coordinate proof work.

The bound must hold along the real coordinate intervals used for integer
rounding, or be replaced by a valid discrete interpolation inequality.
Checking derivatives only at mixed feasible points is insufficient. For
example, on \(\{0,1,2\}\), let

\[
F(x)=(x-1)^2-\sin^2(\pi x).
\]

Its integer values are \((1,0,1)\), so growth holds with \(\mu=1\).
At every integer, \(F''=2-2\pi^2<1\). Nevertheless the grid
\(\{0,2\}\) with \(L=1\) has corrected minimum \(1/2>f^*=0\).
A derivative bound on the full real box is a simple sufficient
assumption. A bound on every real coordinate fiber through mixed feasible
points also suffices.

## 3. Integer grids and exact termination are valid

Integer interval bounds must first be replaced by
\([\lceil a_i\rceil,\lfloor b_i\rfloor]\). Clipping to raw noninteger
bounds would create infeasible nodes. Empty intervals indicate an empty
domain; singleton coordinates can be eliminated. The independent
derivation already assumes integral bounds and removes singletons.

For \(H=\max(h,1)\), every unclipped outward step satisfies
\(\Delta\ge(H+\theta t)/3\). Hence a side of length \(R\) uses at most

\[
1+\frac{\log(1+\theta R/H)}{\log(1+\theta/3)}
\]

intervals. The additive one pays for a final clipped step. The displayed
ceiling version in the independent derivation is conservative and valid.
The proof must not apply the full-step lower bound to the clipped step.

For a purely integer domain, \(Bnh_j^2<1\) forces \(y_j=x^*\) by
lattice separation. One further stage again returns \(x^*\). Since its
center is now \(x^*\) and \(h<1\), every adjacent first interval has
length one, so \(D(x^*)=0\). This is an exact lower-and-upper-bound
certificate, not merely identification of a likely optimizer.

Logarithmic dependence on large domain lengths is therefore justified
for fixed width and fixed curvature-to-growth ratio in the stated oracle
model. This does not guarantee that every individual instance avoids a
full coordinate grid: small domains or poor constants may give one.

## 4. Unknown growth constants require an explicit parameter search

Refining \(h\) with an unsafe fixed \(\theta\) can fail forever,
even with a unique integer minimizer. Take

\[
X=\{0,\ldots,9\},\quad F(x)=x^2/100,\quad L=8,\quad
\theta=1/2,\quad 0<h<1/2.
\]

Here \(\mu=1/100\) and \(L\) is a valid, loose curvature bound.
Center zero gives grid \([0,1,2,3,4,6,9]\), whose unique corrected
minimizer is six with penalty nine. Center six gives
\([0,2,3,4,5,6,7,8,9]\), whose unique corrected minimizer is zero
with penalty four. The method cycles \(0\to6\to0\) while \(h\)
tends to zero.

The proposed halving search over \(\theta\) fixes this problem. For a
positive tolerance, run each attempt through the certificate horizon
derived from \((7L/8)nh_J^2\le\varepsilon\). Restarting with
\(h_0=s\) gives the required initialization from any feasible center.
Accept only a computed certificate. A trial eventually has safe
\(\theta\); earlier failed trials do not invalidate its certificate.
For exponent \(w+1\ge1\), their geometrically increasing work is
bounded by a constant times the final trial's work.

For exact pure-integer optimization, a positive-tolerance horizon alone
does not state a complete stopping algorithm. A sufficient horizon for
each trial is: refine to \(nh_j^2\le\theta^2\), then run one more
stage, accepting only \(D=0\). On a safe trial,

\[
B\le\max\{1,1/(22\theta^2)\}\le1/(4\theta^2),
\]

so the first of those stages has \(E_j\le1/4<1\), and the next has
a zero certificate. This uses
\(O(1+\log_+(s\sqrt n/\theta))\) stages. Halving \(\theta\) until
success preserves a bound of the same order as the successful trial.

## 5. Cost and scope qualifications

The shared coordinate grids and unary penalties preserve the supplied
factorization. Each unary penalty must be assigned exactly once.
Ordinary tree dynamic programming works with arbitrary branching.

The final uniform bound \(O(Nq^{w+1})\) per stage is valid. The
intermediate claim that usual table computation costs simply
\(O(\sum_t\prod_{i\in V_t}|G_i|)\) needs a convention or further
argument when a bag has many children. Direct message addition gives
the safe explicit bound

\[
O\left(\sum_t(1+\deg_{\rm children}(t))
                 \prod_{i\in V_t}|G_i|\right)
\le O(Nq^{w+1}).
\]

The independent derivation explicitly makes a bag objective evaluation
one oracle operation. Without that convention, the number and cost of
factor evaluations must also appear. Finding a decomposition and proving
valid curvature or growth bounds are separate costs.

The assumptions requiring emphasis are:

- Growth is relative to one fixed optimizer. The conventional bound by
  distance to the entire optimizer set does not supply the contraction
  argument given here.
- The domain is a product. Coupled constraints can make endpoint
  rounding infeasible; this is not a theorem for general constrained
  MINLP.
- Exact finite minimization and evaluation are assumed. An
  \(\eta\)-optimal corrected-grid answer gives a gap bound
  \(D(y)+\eta\), so \(D(y)=0\) alone ceases to be an exact
  certificate. A bit-complexity claim requires an objective
  representation and certified arithmetic analysis.
- Rounding, geometric grids, and tree dynamic programming are familiar
  components. Their combination and the exact integer corollary are
  candidates for a literature audit, not established novelty from this
  review.

## 6. Targeted verification

The reviewer ran the inline command `python - <<'PY'` using exact
`fractions.Fraction` arithmetic to construct both grids in the cycling
example, enumerate their corrected objectives, and verify unique
minimizers and penalties. It returned respectively
\((y,D,F(y)-D)=(6,9,-216/25)\) and \((0,4,-4)\).
The same command checked the integer-only curvature example's values
and corrected lower bound \(1/2\). These are arithmetic checks of
counterexamples; the symbolic arguments above establish their scope.

A delegated independent checker additionally reported successful
enumeration of 108,000 integer-step inequalities and 378 one-sided
count cases. This review did not rerun that checker or the derivation
author's optimization tests. No project-wide verification or CI
inspection was performed.

## 7. Review of the main theorem and rational-table extension

The reviewer subsequently read `geometric-dp/theorem.md` in full. Its
explicit full-box coordinate-semiconcavity assumption and successive
independent-rounding proof resolve the curvature qualification above.
Its normalization of integer bounds, unique-optimizer growth assumption,
factor-counted uniform table bound, and unknown-growth positive-tolerance
algorithm are also sufficient. Lemmas 1--3, Theorem 4, and Corollaries 5--6
are mathematically valid as stated in that version. No core proof
correction is needed.

For the simplified conditioning bound, choose \(\theta\) at the largest
safe scale, or within a constant factor of it. The bound expressed directly
in \(\theta\) is valid for every permitted smaller choice, but an
arbitrarily small choice need not have the advertised dependence solely on
\(L/c\). Integer floor operations should either be included in the
arithmetic-operation convention or have their implementation cost accounted
for; this does not alter the certificate proof.

The proposed finite-table approximation extension also holds. Suppose
the assembled table objective satisfies

\[
|\widetilde F(v)-F(v)|\le\Delta
\quad\hbox{for every }v\in\prod_iG_i,
\qquad 0\le\Delta\le Lnh^2/16.
\]

A bound only on the current grid is enough. A uniform approximation on
the entire continuous box is unnecessary. Certified factor-table error
bounds whose sum is at most \(\Delta\) supply this condition.

Let \(y\) minimize \(\widetilde F-D\) exactly. Then

\[
\begin{aligned}
\mathrm{LB}&=\widetilde F(y)-D(y)-\Delta\le f^*,\\
\mathrm{UB}&=\widetilde F(y)+\Delta\ge F(y),\\
\mathrm{UB}-\mathrm{LB}&=D(y)+2\Delta.
\end{aligned}
\]

Indeed, the approximate corrected minimum is at most the true corrected
minimum plus \(\Delta\). Combining this valid gap with quadratic
growth yields

\[
(c-L\theta^2/2)E_{\rm new}
\le(3L/8)nh^2+(L\theta^2/2)E_{\rm old}.
\]

Under the same safe-parameter condition as the exact theorem, this gives
precisely

\[
E_{\rm new}\le\frac{2L}{5c}nh^2+\frac1{15}E_{\rm old}.
\]

With halved widths,
\(B=\max\{1,6L/(11c)\}\) is sufficient for
\(E_j\le Bnh_j^2\), including stage zero. If \(B>1\), then
\(B\theta^2\le3/44\); otherwise it is at most \(1/4\).
Therefore the earlier penalty estimate still gives
\(D(y_j)\le(7L/8)nh_j^2\), and adding \(2\Delta\) gives

\[
\mathrm{UB}_j-\mathrm{LB}_j\le Lnh_j^2.
\]

This extension permits finite certified factor evaluation. Rational
objective entries alone do not ensure that the corrected tables are
rational: the penalties also involve \(L\) and squared grid distances.
The simplest sufficient arithmetic assumptions are rational box bounds,
rational initial center, rational \(L>0\), and rational grid parameters.
Approximating or rounding penalties would need its own one-sided error
budget. Computational cost must include producing the certified factor
approximations.

For pure integers, the modified distance invariant can still force finite
identification of \(x^*\) when a safe growth bound and stage horizon are
available. However, with \(\Delta>0\), a zero penalty gives the numerical
gap \(2\Delta\), not zero. The approximate-value extension by itself
does not give the exact zero-gap certificate or unknown-growth exact
stopping test of the exact-oracle version. No additional computational
tests were needed for this algebraic extension.
