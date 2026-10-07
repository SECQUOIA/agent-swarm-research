# Independent review of the combined ambient grid-count obstruction

Date: 2026-10-02. Reviewed
[the complete combined note](../new-direction/ambient-local-count-barrier.md),
including its finite-noise argument and FPT conclusion.

**Verdict: no mathematical blocker found.** The construction proves lower
bounds for the stated complete-grid local and near-optimal node counts.
It does not prove a lower bound for the exact cell-closure algorithm.

## 1. Factor geometry and the actual QP

The rational all-ones factor gives the stated conditional fiber and its
midpoint. Integrating the joint minimum/maximum density yields the exact
continuous probability in equation (1). Its first derivative at zero
matches the complementary-minor coefficient. Disjoint blocks give the
factor \((N/k)^{k/2}\), with \(TT^T=I_k\).

For the actual QP, \(u\) is unit, \(q\) has norm \(\sqrt2\), and
\(u^Tq=0\). The displayed \(2\times2\) blocks therefore correctly
represent \(P\) and \(A\). The block for \(P\) is positive definite,
and \(A\) has exactly one negative eigenvalue of magnitude
\(\alpha(\sqrt{17/8}-1)\). The nullspace inclusion and the bound
\(\alpha<4\nu\) follow. These statements remain valid for both
\(\alpha=1\) and \(\alpha=m\).

The linear constraints give the full rectangle in \((y,z)\), with
projected width eight. Its objective has an indefinite Hessian on that
rectangle, so the negative curvature is present on the feasible set.
The interval \(|z|\le m^{-3}\) is small but nonzero and needs only
\(O(\log m)\) rational bits.

Minimizing over each active simplex gives the coefficients in equation
(9). The two signs of \(u\) imply \(C_r=S-d\) exactly. The reduced
recourse QP has positive definite Hessian
\(\alpha\left(\begin{smallmatrix}1&c\\c&1\end{smallmatrix}\right)\).
Consequently the envelope derivative is well-defined even when there
are ties between simplex coordinates. Whenever the \(y\)-constraint
is inactive, its derivative is \(S+\alpha c z\), as claimed.

## 2. Events, grids, and product counts

The event \(E\) bounds \(|S|\) by \(2/m\), \(|d|\) by two, and
\(|C_r|\) by \(2+2/m\). For all \(|a|\le3/2\), every feasible \(z\)
gives a \(y\)-stationary point in \((-4,4)\). Thus the derivative
bound holds throughout the interval containing the central nodes and
their neighbors. At the fine level, \(h\ge16/(\alpha m)\) makes the
allowed error \(\alpha h^2/4\) larger than the derivative bound
times \(h\). The lower bound on the number of central nodes is valid
even when the grid is not centered at zero.

The global near-optimal argument uses a different, coarser level.
Completing the square leaves \(G\) plus a nonnegative quadratic.
For \(|a|\le1\), the feasible trial point \(y=a+d/\alpha,z=0\)
has value at most \(6/m\), whereas every feasible \(G\) is at least
\(-8/m-3/m^2-1/m^3\). This proves the gap below \(15/m\).
The prescribed auxiliary box contains \(a=y-d/\alpha\) for every
feasible \(y\), so minimizing over that box removes the quadratic
exactly; no larger auxiliary domain is being used silently.

At the coarser level, \(2B\ge16/m\). The assumption \(m\ge256\)
also ensures at least \(\sqrt{\alpha m}/16\) central nodes.
The resulting expectation lower bound is therefore valid.

For \(k\) independent blocks, all widths and steps coincide.
The product event has probability above \(4^{-k}\). At the fine
level the multidimensional local tolerance is at least the scalar
tolerance. At the coarser level both the gap and the correction add
over blocks, giving \(15k/m<2B\). Equations (23)--(24) follow with
the stated constants.

These two arguments use different grid levels. The proof does not
mistakenly treat all fine-level local nodes as globally near-optimal.

## 3. Exact finite-grid constants

For the endpoint-inclusive noise grid, a coordinate lower-tail
probability is at least \(2/n-1/M_{\rm noise}\). If
\(M_{\rm noise}\ge64n\), this is at least \(19/(10n)\).
The active group sizes give failure exponents \(57/64\) and \(19/20\).
The groups are independent; independence from \(d\) is not used.

The variance identity

\[
 \operatorname{Var}(d)=
 \frac{M_{\rm noise}+1}{3(M_{\rm noise}-1)}
\]

uses independence of the original coordinates and \(\|u\|=1\).
It is at most \(3/8\) whenever \(M_{\rm noise}\ge17\), so the
Chebyshev subtraction \(3/32\) is valid. The asserted numerical
inequalities can be certified with positive rational Taylor sums:

\[
 \begin{split}
 e^{57/64}
 &>\sum_{j=0}^5\frac{(57/64)^j}{j!}
   =\frac{104619383539}{42949672960}>\frac{12}{5},\\
 e^{19/20}
 &>\sum_{j=0}^5\frac{(19/20)^j}{j!}
   =\frac{992460199}{384000000}>\frac52.
 \end{split}
\]

Consequently the probability lower bound is strictly greater than

\[
 \left(1-\frac5{12}\right)\left(1-\frac25\right)
 -\frac3{32}=\frac{41}{160}>\frac14.
\]

The sampling grid prescribed by the ambient theorem satisfies the
needed threshold. Its section bound has \(C_{\rm sec}\ge70\) for
positive factor dimension, and \(Q_{\rm all}\ge1\). With total ambient
dimension \(N\), that theorem chooses
\(M_{\rm noise}\ge2N C_{\rm sec}Q_{\rm all}\ge140N\ge64n\).
Thus the finite-law obstruction applies to that specified sampling law,
not merely to an unrelated continuous approximation.

The exact fiber probability in section 1 is appropriately retained as
a continuous-noise identity; the note does not assert it for atomic noise.

## 4. FPT meaning and algorithmic scope

With \(\alpha=1\), all the stated intrinsic parameters are fixed per
coordinate, while \(k\) remains the parameter. The lower bounds rule
out \(f(k,R)N^C\) for either count with an absolute exponent \(C\):
fix \(k>4C\) for the global count and send \(m\) to infinity.
The local-count lower bound is stronger.

The rational-input version is also correct. An explicit dense encoding
of this family has size \(I=O(N^2\log N)\), with an absolute degree
independent of \(k\). Thus any proposed bound \(f(k,R)I^C\) is
contradicted by fixing \(k>8C\) and then sending \(m\) to infinity.
The logarithm cannot compensate for the resulting positive power of \(N\).
If the projected diameter is included in \(R\), its value \(8\sqrt{k}\)
can be absorbed into the function of \(k\); it does not depend on \(m\).

The note correctly states both important limits. The ambient diameter
grows like \(m\) already in a single block, so this example does not
exclude a diameter-dependent bound. More importantly, a large complete
grid count does not force the exact solver to inspect that grid. The
few reduced quadratic pieces may close early. No retained-cell,
unresolved-cell, runtime, bit-complexity, or hardness lower bound follows.

## 5. Verification performed for this review

This was a fresh full-file analytic audit. A targeted exact-rational
Python calculation checked the two fifth-order Taylor sums and the
identity \(7/20-3/32=41/160>1/4\); it passed. The earlier component
checks were not rerun. Their results remain recorded in the
[fiber review](ambient-fiber-volume-sharpness.md) and
[construction review](ambient-local-count-barrier.md).
Scoped link and whitespace checks of this review passed.

No external search, project-wide verification, or CI inspection was
performed. The combined note's pending-review status can now be updated
to cite this completed audit.
