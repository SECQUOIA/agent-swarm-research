# Expected exact MIQP under independent rational Gaussian-like noise

Date: 2026-10-02. Status: composition passed a
[separate independent review](../reviews/smoothed-gaussian-miqp-review.md)
and targeted checks. No publication-priority claim is made.

Combining the reviewed integer-gap closure certificate with the reviewed
Gaussian-weighted local count removes the ambient dimension power from
the mixed-integer theorem. The resulting algorithm has expected FPT bit
work in integer dimension, negative inertia, and a curvature/noise ratio.
It solves every sampled instance exactly; its finite noise law is chosen
before sampling, and the fallback uses the same draw.

## 1. Statement and reused interfaces

Use a nonempty bounded rational mixed polytope

\[
 X=\{x\in\mathbb R^n:Mx\le b_X\}
       \cap(\mathbb Z^p\times\mathbb R^{n-p}),
 \qquad F(x)=\tfrac12x^TAx+b^Tx+c_0.
\]

Write \(\mathcal P=\{x:Mx\le b_X\}\), with \(q\) inequalities.
Suppose rational data satisfy

\[
 P=A+\alpha T^TT\succeq0,\quad
 \ker P\subseteq\ker T,\quad
 cI_k\preceq TT^T\preceq I_k,
 \quad 1/2\le c\le1,\quad\alpha>0.                     \tag{1}
\]

Here \(1\le k\le n\); the convex case uses the exact convex-MIQP
oracle directly. Fix rational \(\sigma>0\), included in the base input
length \(I\).

There is a deterministically computed finite rational scalar law
\(\mathcal L\), sampled in bounded polynomial time, such that independent
\(\gamma_i\sim\mathcal L\) give an always-correct exact algorithm
for \(F_\gamma=F+\gamma^Tx\), with expected bit work

\[
 f(p)C_0^k(1+H_G)(I+1)^{C_1},                            \tag{2}
\]

where the polynomial exponent is absolute. Put
\(\ell_i=\min_{\mathcal P}(Tx)_i\),
\(u_i=\max_{\mathcal P}(Tx)_i\), and \(C_k=1+2k\). Then

\[
 H_G=\prod_{i=1}^k\left[
 2+c^{-1/2}(2C_k+4)+
 \frac{C_k\alpha(u_i-\ell_i)}{\sigma\sqrt{2\pi}}
 \right].                                               \tag{3}
\]

The reviewed rational normalization supplies (1) with
\(c=63/64\), \(k=n_-(A)\), and \(\alpha<4\nu\), where
\(\nu=\max\{0,-\lambda_{\min}(A)\}\). Thus (2) has the form

\[
 f_1\left(p,k,1+\frac{\nu\operatorname{diam}(\mathcal P)}\sigma\right)
 (I+1)^{C_1}.                                           \tag{4}
\]

No quadratic growth, uniqueness, or generic-position promise is required.
The law approximates a Gaussian; it is not an exact real Gaussian or an
arbitrary fixed coarse approximation. The target is the sampled objective.

The proof uses two independently reviewed inputs:

- [Integer-gap MIQP cell closure](smoothed-miqp-cell-closure.md), including
  the exact convex-MIQP oracle, whole-cell certificate, fixed-slice
  extraction, active-witness bound, integer-label isolation, and exact
  fallback.
- [Gaussian-weighted cell closure](smoothed-gaussian-cell-closure.md),
  including the local probability count, bounded finite rational sampler,
  and Kolmogorov-distance transfer. Its weighted count requires an active
  upper model, not differentiability of the full value function.

## 2. Why the weighted count applies to mixed recourse

Set \(D=(TT^T)^{-1}T\), \(E=I-T^TD\), \(d=D\gamma\), and
\(r=E\gamma\). Under the Gaussian proxy
\(\gamma\sim N(0,\sigma^2I_n)\), the vectors \(d,r\) are independent,
with \(\operatorname{Cov}(d)=\sigma^2(TT^T)^{-1}\). Define

\[
 W_r(a)=\min_{x\in X}
 [F(x)+r^Tx+\tfrac\alpha2\|a-Tx\|^2],
 \qquad V_\gamma(a)=W_r(a)+d^Ta.
\]

The mixed envelope can be nonsmooth. Nevertheless every attaining
witness \(x_v\) supplies, for all \(z\in\mathbb R^k\),

\[
 W_r(z)\le W_r(v)+\alpha(v-Tx_v)^T(z-v)
                         +\tfrac\alpha2\|z-v\|^2.       \tag{5}
\]

This is precisely the model used in the weighted count. At a deterministic
grid node, the local neighboring comparisons restrict each interior
factor coefficient to an interval of length at most
\(C_k\alpha h_i\). Equation (5) further places its allowed values in

\[
 \alpha[\ell_i-v_i,u_i-v_i]
       +[-C_k\alpha h_i/2,C_k\alpha h_i/2].
\]

Conditioning on \(r\), the Gaussian factor density majorant and weighted
lattice sum from the cited theorem therefore give

\[
 \sum_{v\in G_j}\Pr_{\rm Gauss}(E_v)\le H_G             \tag{6}
\]

on every fixed auxiliary box and every refinement level. The count is
independent of that box's enlargement. Neither convexity of the mixed
feasible set nor smoothness of \(W_r\) is used here.

## 3. Two failure events under a finite Gaussian approximation

Use the base constants from the mixed theorem. Integer coordinate LP
bounds \(L_i,U_i\) give

\[
 Z=\prod_{i=1}^p(U_i-L_i+1),\quad G=\sum_{i=1}^p(U_i-L_i),
 \quad R=Z2^q,\quad B=\max\{2,R\},\quad K=R(q+n+1),
\]

with \(Z=1,G=0\) when \(p=0\). Define

\[
 C_{\rm sec}=[2(2k+1)R^2+1](8k+2),\quad
 C_T=\max\{1,\sum_i(u_i-\ell_i)\},\quad
 \Lambda=\alpha k C_T.
\]

Let \(H_0\) be the mixed theorem's base-only Hessian-response bound,
computed without any sampled coefficients. Its logarithm and those of
all the preceding constants are polynomial in \(I\).

Suppose each coordinate of a finite product law has Kolmogorov distance
at most \(\delta\) from \(N(0,\sigma^2)\). For a fixed ambient
hyperplane, a Euclidean tube of width \(\tau\) has Gaussian probability
at most \(2\tau/(\sigma\sqrt{2\pi})\le\tau/\sigma\).
Each coordinate-axis section is an interval, so product-measure replacement
gives probability at most

\[
 \tau/\sigma+2n\delta.                                  \tag{7}
\]

The fixed-slice critical-region failure is covered by \(K\) such tubes,
with \(\tau=\sqrt k(\alpha+H_0)h\), exactly as in the mixed theorem.

The integer-label isolation event has a different, sharper transfer.
Condition on every coefficient except one integer coefficient. There
are at most \(U_i-L_i\) relevant lower-envelope breakpoints. A
\(2\varepsilon\)-length interval has scalar Gaussian probability at
most \(2\varepsilon/(\sigma\sqrt{2\pi})\), and changing that one
coordinate's law adds at most \(2\delta\). The conditional estimate
is uniform in all the other coefficients, even when their laws are finite.
Thus

\[
 \Pr\{\text{two original labels lie within }\varepsilon
                      \text{ of the optimum}\}
 \le G(\varepsilon/\sigma+2\delta).                     \tag{8}
\]

No factor \(n\) is needed in (8); it is a conditional one-coordinate
estimate followed by the integer-coordinate union. Ties at atoms remain
included in its Kolmogorov term.

If the fixed auxiliary box has largest width \(s\), put

\[
 C_{\rm gap}=k\alpha s/4+\Lambda,\qquad
 C_{\rm bad}=Kk(\alpha+H_0)+G C_{\rm gap}.               \tag{9}
\]

A retained unresolved cell at nominal mesh \(h\) fails either its
fixed-slice region certificate or its best-other-label gap certificate.
The latter implies two original labels within \(C_{\rm gap}h\) of
the optimum. Combining (7)--(9), with \(\sqrt k\le k\), bounds
the probability of any unresolved retained cell by

\[
 C_{\rm bad}h/\sigma+2(nK+G)\delta.                     \tag{10}
\]

This is a statement about the entire search, not a union over its visited
cells.

## 4. A noncircular support and precision budget

The reviewed rational Gaussian sampler takes an integer accuracy
\(b\ge1\), uses bounded polynomial time and polynomially many fair
bits, and returns a rational scalar whose law has Kolmogorov error at
most \(2^{-b}\) from the standard Gaussian and support in
\([-b-20,b+20]\). Scaling by \(\sigma\) preserves these properties
with noise scale \(\sigma\).

For a trial support multiplier \(R_s=2^t\), compute

\[
 s_i=R_s\sigma\|D_i\|_1,\qquad
 A_{R_s}=\prod_i[\ell_i-s_i/\alpha,u_i+s_i/\alpha],
 \qquad s=\max_i(u_i-\ell_i+2s_i/\alpha).
\]

Use this \(s\) in (9), and choose the least integer \(J\ge0\) with

\[
 s2^{-J}\le\frac{\sigma}{4B C_{\rm bad}},
 \qquad Q_{\rm all}=(J+1)(2^J+1)^k.                     \tag{11}
\]

Choose the least positive integer \(b\) with

\[
 2^b\ge\max\{8B(nK+G),\ 2nC_{\rm sec}Q_{\rm all}\}.    \tag{12}
\]

Starting with \(t=0\), increase \(t\) until \(2^t\ge b+20\).
Fix the first successful \(R_s,J,b\), then independently sample all
original coefficients with the reviewed finite sampler of accuracy \(b\).
All random choices occur after this deterministic calculation.

The added label-gap event does not create a precision circle. Relative
to the trial \(t=0\), both \(s(t)\) and \(C_{\rm bad}(t)\)
are at most \(2^t\) times their initial values. Their product therefore
grows by at most \(4^t\), and the least integer cutoff obeys

\[
 J(t)\le J(0)+2t.
\]

Equation (12) then gives
\(b\le A_1+O(kt+\log(J(0)+t+1))\), where \(A_1\) and
\(J(0)\) are polynomial in the base input length. Exponential
\(2^t\) eventually exceeds this
bound after polynomially many steps, and the successful \(t,J,b\)
are polynomially bounded in \(I\). All intermediate integers also
have polynomial encoding length. The support condition ensures every
sampled draw has its auxiliary optimizer inside the fixed box.

## 5. Expected exact work

Run the reviewed mixed cell-closure algorithm through level \(J\).
It uses exact convex-MIQP values, the \(2p\) exclusion solves for the
best-other-label gap, continuous slice polishing, and certified local
quadratic closure. If unresolved cells remain, apply the exact
integer-label/continuous-face fallback to the same draw.

For local events, the mixed section bound \(C_{\rm sec}\) implies

\[
 |\Pr_{\mathcal L^{\otimes n}}(E_v)-\Pr_{\rm Gauss}(E_v)|
 \le2nC_{\rm sec}2^{-b}.
\]

Summing over all deterministic grids through \(J\), equations (6) and
(12) yield at most \((J+1)H_G+1\). Standard corner incidence, child
counts, and \(3^k\) exact local face solves turn this into the search
bound (2). Per query, the exact convex-MIQP cost contributes only the
factor \(f(p)\); continuous polishing keeps later rational heights
polynomial in the base and sampled input lengths.

For the fallback, (10)--(12) give

\[
 \Pr\{\text{fallback}\}\le\frac1{4B}+\frac1{4B}
                         =\frac1{2B}\le\frac1B.
\]

Its cost is at most \(B\operatorname{poly}(I+b)\), so its expected
contribution is polynomial. The finite sampler, grid coordinates,
recourse instances, exact witnesses, and final values all have polynomial
encoding length, with an absolute exponent. Equation (3) contains no
ambient-dimension power depending on \(k\). This proves (2)--(4).

Exact correctness does not rely on the probability estimates: every
accepted cell has a valid deterministic mixed certificate, and the
fallback is exact on every draw. The probability bounds control work
only. Exceptional samples are neither discarded nor resampled.

## 6. Verification status and limits

The two underlying theories have independent reviews. The parent
researcher also independently read this complete composition and checked
the scalar isolation transfer, combined failure budget, weighted mixed
localization, changed support-loop rate, and FPT arithmetic. The
[separate composition review](../reviews/smoothed-gaussian-miqp-review.md)
passed the actual written proof and reread the mixed gap certificate and
its exact convex-MIQP oracle interface. Its author developed the Gaussian
ingredient but did not author this mixed-integer composition.

The command
`python research-20261002/new-direction/check_gaussian_miqp_budget.py`
passed six synthetic rational-bound fixtures and 63 support-budget trials.
The [checker](check_gaussian_miqp_budget.py) verifies both \(1/(4B)\)
failure allocations, the local-event discrepancy allowance, support
containment, and the exact bound \(J(t)\le J(0)+2t\). It includes
large integer ranges, \(H_0=2^{1000}\), no integer alternatives, and
a case attaining the new \(2t\) growth rate. The support loop stopped
at exponents 8 through 13 and selected at most 4,435 accuracy bits in these
fixtures. These are arithmetic checks of the composition budget, not
MIQP instances or an end-to-end solver implementation.

The reviewer independently ran
`python research-20261002/new-direction/check_gaussian_miqp_review.py`.
That [diagnostic](check_gaussian_miqp_review.py) passed five complete-law
fixtures, 3,333 exactly enumerated draws, 84 tied draws, and twenty
isolation bounds. It uses a 33-atom dyadic Gaussian-like law, checks both
CDF limits at every atom against a high-precision Gaussian CDF, and
computes label-gap probabilities exactly. Cases include nonproduct labels
and a continuous quadratic variable optimized separately for each label.
It tests the new isolation transfer, rather than the production oracle
or the much finer law chosen by the theorem.

The [focused MIQP prior-art audit](../prior-art/smoothed-exact-miqp-prior.md)
records the established convex-MIQP oracle, parametric-QP representations,
integer isolation, and low-inertia approximation precedents. None of those
ingredients is claimed as a new mechanism here. This composition's added
conclusion is the expected FPT bound with an absolute input-polynomial
exponent under the specified independent rational Gaussian-like law. The
audit is a scoped comparison, not a publication-priority conclusion.

No project-wide verification, CI inspection, or external search was
performed for this note.

The result is for a specifically constructed finite product law on the
original coefficients. It is not an exact-real Gaussian algorithm, does
not cover every coarse Gaussian approximation, and does not recover the
unperturbed optimum. The supplied normalization and exact convex-MIQP
oracle remain essential interfaces.
