# Independent review of algebraic-coefficient span precision

Date: 2026-09-27. Status: independent mathematical audit completed; no
unresolved proof gap found in the saved direct number-field argument in
[the precision note](algebraic-coefficient-span-precision.md).

The argument supports a terminal margin, and hence a Hölder constant,
with exponent linear in the Hessian-span dimension. The essential change
is to perform the finite-quotient elimination over the common number field
and estimate its coefficient vector at every place. The field degree and
input coefficient heights are then not raised to an exponent depending
on the Hessian span.

## Field and affine restriction

Write \(D=[K:\mathbb Q]\), let \(B\ge1\) bound the absolute
logarithmic Weil heights of the input coefficients, and let \(S\ge2\)
bound the number of variables, rows, and explicitly listed coefficients.
All convexity assertions concern the selected real embedding of \(K\).

The active affine restriction works over \(K\). The active set is selected
at an optimizer, but its defining coefficients do not use the optimizer's
coordinates. Hessian dependencies are computed over \(K\); their rank
over \(K\) equals their rank over \(\mathbb R\). The added equations
\(q_i-\sum_j c_{ij}q_j=0\) vanish at that optimizer because the retained
rows are active. A free-coordinate chart is then obtained by linear algebra
over \(K\).

Only a fixed number of linear-algebra and substitution stages is needed.
Cramer's rule bounds every new coefficient height by
\(S^C(B+1)\), for an absolute constant \(C\). There are polynomially
many such coefficients. In particular, this step introduces neither a
field extension nor a factor \(B^{O(h)}\).

On the chart, the retained constraints span at most \(h\) dimensions as
whole polynomials. Minimal nonnegative support for the regularized KKT
gradient therefore has size \(s\le\min(h,d)\), with independent
gradient columns. Positive definiteness of the regularized Lagrangian
Hessian makes the selected multiplier root nonsingular. The construction
in [the explicit separation proof](explicit-span-separation.md) consequently
applies over \(K\).

The draft uses the two ordered perturbations in
[the optimizer proof](ordered-perturbation-optimizer.md). First add
\(\varepsilon\|x_0+Vu\|^2\), using the original-coordinate norm.
For each fixed \(\varepsilon>0\), relaxing the retained rows by
\(\delta>0\) gives an inner sequence in a fixed coercive sublevel
set. As \(\delta\downarrow0\), uniqueness gives the exact regularized
optimizer. Those exact optimizers satisfy
\(\|x_\varepsilon\|\le\|x^*\|\), so their outer limit as
\(\varepsilon\downarrow0\) is the minimum-norm optimizer. This
argument works over the selected embedding without a right-hand-side
continuity theorem. No auxiliary ball constraint or ball multiplier is
needed.

## Coefficient height through the quotient

For the multiplier polynomials \(G_1,\ldots,G_s,A,B\), let their
multiplier degree be at most \(a\). Set

\[
 \ell=(a+1)^s,\qquad T=a(s+1).
\]

At each archimedean place \(v\), let \(C_v\ge1\) be the maximum
of their coefficient \(\ell_1\)-norms. At each nonarchimedean place,
use the maximum coefficient absolute value and one. With normalized local
weights, put

\[
 E=\frac1D\sum_v n_v\log C_v.
\]

The reduction rule
\(\lambda_i^{a+1}=-G_i/\beta\) has branch depth at most \(T\).
After multiplication by \(\beta^T\), every multiplication-matrix
entry has local coefficient norm at most \(C_v^{T+1}\). The determinant

\[
 H=\det(w\widetilde M_A-\widetilde M_B-\zeta\beta^T I_\ell)
\]

therefore has archimedean coefficient norm at most
\(\ell!3^\ell C_v^{\ell(T+1)}\), and nonarchimedean coefficient
norm at most \(C_v^{\ell(T+1)}\). Thus its affine joint coefficient
height is at most

\[
 W=\ell(T+1)E+\log(\ell!)+\ell\log3.                \tag{1}
\]

This is one bound on the whole coefficient vector. It does not sum the
heights of all determinant terms separately. Its normalization is unchanged
in a larger number field, so no normal-closure degree enters.

For the KKT expressions, the common input coefficient vector has height at
most the sum of the individual input heights. Include the fixed scalars
\(2,1/2\), the regularizer Hessian \(2V^TV\), and its linear vector
\(2V^Tx_0\) in that vector. The universal KKT formulas then have input
degree at most \(2d+3\) and logarithmic coefficient norm polynomial
in \(S\). The coordinate numerator
\((x_{0j}\Delta+(Vp)_j)\Delta\) satisfies the same bound.
Consequently \(E\le S^C(B+1)\), after adjusting the absolute
constant \(C\) for the affine chart. With \(a=2d\), equation (1)
gives

\[
 W\le (B+1)S^{O(h+1)}.                              \tag{2}
\]

In particular, the exponent of \(B+1\) is independent of \(h\).

## Nonzero extraction and root bounds

The leading coefficient of \(H\) in \(\zeta\) is
\((-\beta^T)^\ell\), so \(H\ne0\). Extract its first nonzero
coefficient successively in \(\zeta\), \(\beta\), \(\delta\),
and \(\varepsilon\), in that order. This gives a nonzero
\(P\in K[w]\) of degree at most \(\ell\).

The selected nonsingular multiplier root supplies a local real branch for
each fixed regularization-parameter pair. Its value factor is coprime to
\(\zeta\) because \(A\ne0\). The factor argument in the explicit
separation proof therefore survives the first extraction, including when
specialization raises the order of vanishing in \(\zeta\). Taking
\(\beta\to0\) preserves an equation on every selected parameter pair.
The two ordered limits, first \(\delta\to0\) and then
\(\varepsilon\to0\), show \(P(\theta)=0\).
Unbounded multipliers do not affect those
ordered limits. No convexity assertion is made at another embedding.

Each extraction selects a subvector of coefficients and cannot increase
the affine joint height. Hence \(P\) has affine joint height at most
\(W\). Its projective coefficient height is also at most \(W\).
The root-degree and root-height bounds are

\[
 [\mathbb Q(\theta):\mathbb Q]\le D\ell,
 \qquad h_{\rm W}(\theta)\le W+\log2.              \tag{3}
\]

The height inequality follows by applying the ordinary Cauchy bound at
archimedean places and its ultrametric version at nonarchimedean places,
then summing with normalized weights in \(K(\theta)\).

For the selected nonzero value, one can avoid the extra factor \(\ell\)
that combining both bounds in (3) would introduce. Remove powers of \(w\)
from \(P\), and write its nonzero constant coefficient as \(p_0\).
Every ratio \(p_i/p_0\) has height at most the projective coefficient
height, hence at most \(W\), and belongs to \(K\). Therefore

\[
 |\theta|^{-1}
 \le2\max_i\max(1,|p_i/p_0|)
 \le2e^{DW},
 \qquad -\log|\theta|\le DW+\log2.                 \tag{4}
\]

Zero coefficients and repeated roots cause no problem. A nonzero constant
polynomial cannot annihilate \(\theta\). The case \(s=0\) has
\(\ell=1\); a zero-dimensional chart is handled directly by evaluating
the objective at its \(K\)-rational point.

The same estimates apply to every optimizer coordinate, using its
original-coordinate numerator. Fixing one nested multiplier support before
choosing the numerator also bounds the degree of every \(K\)-linear
combination of the coordinates by \(\ell\). A primitive linear
combination exists because the coordinate extension is finite and separable.
Thus their joint field has degree at most \(\ell\) over \(K\).
The objective value belongs to that field. This argument does not infer a
joint degree bound from the separate coordinate degrees.

## Terminal margin and Hölder constant

For a nonempty bounded polyhedron \(P\) and at least one remaining
quadratic row, a common strict point gives

\[
 \theta=\min_{x\in P}\max_i q_i(x)<0.
\]

Compactness gives attainment. Its epigraph program has objective \(t\)
and constraints \(q_i(x)-t\le0\). Appending \(t\) does not change
the constraint Hessian-span dimension. The epigraph is allowed to be
unbounded above; attainment of its finite minimum is sufficient for the
preceding proof. Taking \(\sigma=\min(1,-\theta)\) gives

\[
 \log(1/\sigma)\le D(B+1)S^{O(h+1)}.               \tag{5}
\]

No rational box for \(t\), primitive generator, or embedding-selection
variable is needed. If no rows remain, the terminal margin is unused.

In [the Hölder height proof](hessian-span-holder-height-review.md), the
number of scalar coefficients is polynomial in the original input size
\(N\), and both \(D\) and \(B\) are \(N^{O(h+1)}\).
Substitution into (5) gives \(\log(1/\sigma)\le N^{O(h+1)}\).
The other constants in that proof already have logarithms bounded by
\(N^{O(h+1)}\); the polynomially many affine and curved steps do not
increase the exponent to a quadratic function of \(h\). This supports
\(\log\max(1,C)\le N^{O(h+1)}\) with the same Hölder exponent
\(2^{-h}\).

## Verification scope

This review checks the mathematical coefficient growth, multiplier count,
field preservation, nonzero extraction, root bounds, and terminal-margin
application, including the complete saved precision draft and the ordered
optimizer proof. It depends on the earlier active-restriction,
finite-quotient, ordered-optimizer, and common-field witness arguments as
stated in the linked notes. It is not a new audit of their historical
priority or a formal proof in a theorem prover. Review prompted explicit
inclusion of the regularizer Hessian and linear vector in the local input
norm; that saved clarification was reread and passes the displayed
\(2d+3\) exponent bound.

Targeted verification run: an inline `python` check read only this review,
checking final newline, trailing whitespace, control characters, paired
inline/display math delimiters, and existence of its relative Markdown
link targets. All checks passed. These are document-integrity checks,
not mathematical tests. No project-wide verification or CI inspection was
performed.
