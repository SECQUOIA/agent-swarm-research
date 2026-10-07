# Focused review of the ambient-noise normalization and arithmetic interface

Date: 2026-10-02. Scope: the normalization, fixed auxiliary domain,
critical-piece arithmetic, and bit-complexity interface in
[the ambient-noise extension](../new-direction/smoothed-ambient-cell-closure.md).
This is not the independent review of its volume lemma or scalar-section
discrepancy argument. No publication-priority claim is made.

The reviewed interface has no substantive gap. The normalized rational
factor has a uniform lower singular-value bound, so ambient noise does not
introduce hidden factor conditioning. The curvature bound and refinement
cutoff can be fixed without the sampled coefficient denominators. The
result remains a fixed-rank polynomial bound with explicit powers of the
ambient dimension, rather than a dimension-free FPT bound.

## 1. The normalized factor is uniformly well-conditioned

Use the notation of
[the rational normalization proof](../new-direction/spectral-normalization.md).
Its selected rational Jacobi columns form a matrix \(B\) with
\(B^TB=I_k\). Let \(R\) be the exact orthogonal projector onto
\(\operatorname{range}(A)\), and let \(\Pi_-\) be the negative
spectral projector. The constructed correction is \(U=RB\), and
\(T=U^T\). For each selected column \(q_j\), the proof gives

\[
 \|(I-\Pi_-)q_j\|\le2e/\mu,
 \qquad e=\mu^2/(16n\beta),\quad\beta\ge\mu.
\]

Because \(\operatorname{range}(\Pi_-)\subseteq
\operatorname{range}(R)\),

\[
 \|(I-R)B\|_2^2\le\|(I-R)B\|_F^2
 \le4ke^2/\mu^2\le\frac{k}{64n^2}\le\frac1{64}.
\]

Therefore

\[
 TT^T=B^TRB=I_k-B^T(I-R)B\succeq\frac{63}{64}I_k.
\]

This proves full row rank and, in particular,
\(\sigma_{\min}(T)\ge1/2\), without adding an input hypothesis.
The upper bound \(\|T\|_2\le1\) follows from orthogonal projection.
The same construction makes the residual positive definite on
\(\operatorname{range}(A)\), with kernel \(\ker A\), on which
\(T\) vanishes. Thus the smooth-envelope kernel hypothesis also holds.
The branch \(k=0\) is handled separately by convex optimization.

## 2. The auxiliary box is rational and fixed before sampling

Set \(D=(TT^T)^{-1}T\) and \(E=I-T^TD\). Then

\[
 DT^T=I_k,\qquad ET^T=0,\qquad \|D\|_2\le2.
\]

For every ambient cube draw \(\gamma\in[-\sigma,\sigma]^n\),
\(d=D\gamma\) satisfies \(\|d\|_2\le2\sigma\sqrt n\).
More precisely, the rational bounds
\(s_i=\sigma\sum_j|D_{ij}|\) satisfy
\(|d_i|\le s_i\le2\sigma\sqrt n\). Thus the written box
\([\ell_i-s_i/\alpha,u_i+s_i/\alpha]\) contains
\(Tx-d/\alpha\) for every feasible \(x\) and every draw.
Its endpoints are base-only LP values and rational matrix expressions.
A simpler uniform rational enlargement
\(2\sigma\lceil\sqrt n\rceil/\alpha\) would also be valid.

The decomposition \(\gamma=T^Td+r\), \(r=E\gamma\), is exact.
Square completion therefore gives the equality between the global
auxiliary minimum and the original perturbed minimum minus
\(\|d\|^2/(2\alpha)\). This equality holds on all auxiliary space
and on the fixed box. The full-space gradient upper-model argument may
consequently use a trial point outside that box.

## 3. Piece curvature does not depend on sampled denominators

For an independent active-row basis \(J\), let

\[
 K_J=\begin{pmatrix}P&M_J^T\\M_J&0\end{pmatrix}.
\]

Its response to the auxiliary variable is

\[
 \binom{X_J}{\Lambda_J}=K_J^{-1}
                     \binom{\alpha T^T}{0}.
\]

Clear a common denominator from \(P,M,\alpha T^T\), and let
\(C\ge1\) bound the magnitudes of those scaled integer entries.
Cramer's rule bounds each entry of \(X_J\) by
\(U=(2n)!C^{2n}\). The piece Hessian is
\(H_J=\alpha(I-TX_J)\), so
\(\|H_J\|_2\le\alpha(1+nkU)\). Neither the sampled residual
\(r\), its denominator, nor the linear objective coefficient is used
in this response bound.

The intercept does depend on \(b+r\) and the constraint right-hand
side. It is affine in \(r\), with base-only rational coefficients.
Consequently the defining critical-region rows, piece gradients, and
fixed-region boundary images have residual-dependent affine offsets and
base-only normals. After substituting \(d=D\gamma\), \(r=E\gamma\),
their equations are affine in the original noise with coefficients fixed
before sampling.

There is no disappearing-normal exception in this substitution. A factor
hyperplane with unit factor normal \(u\) has equation
\(u^Td+v^Tr+c=0\). Its ambient normal is
\(w=D^Tu+E^Tv\), and \(Tw=u\). Hence \(\|w\|_2\ge1\).
A factor tube of width \(\tau\) lies within an ambient Euclidean tube
of width at most \(\tau\), even if the intercept dependence on the
residual has large coefficients.

## 4. Arithmetic and parameter dependence

The fixed widths and curvature bound have polynomial binary length, so
the cutoff \(J\) is polynomial in the base input length. The finite-grid
choice has

\[
 \log N=O(kJ+\log C_{\rm sec}+\log(J+1)+\log(n+1)
             +\log(KB)).
\]

All terms are polynomial in the base encoding length; \(k\le n\)
is itself bounded by that length. Sampling, transformed residuals, query
coordinates, exact convex-QP inputs, active-face LPs, and local quadratic
face solves therefore retain polynomial bit lengths. Their polynomial
exponents do not depend on the negative rank. The explicit number of local
face choices contributes a separate factor \(3^k\).

For the normalized factor,
\(w_i\le\operatorname{diam}(X)+4\sigma\sqrt n/\alpha\).
With \(\alpha<4\nu\), the displayed expected-count factor is bounded
by

\[
 \left[2+(1+2k)
       \left(2n+\frac{2\nu\sqrt n\operatorname{diam}(X)}{\sigma}\right)
 \right]^k.
\]

This includes a power of \(n\) depending on \(k\). It establishes
polynomial expected work for each fixed rank under the stated numerical
bounds, but this estimate alone is not FPT in rank and a dimension-free
curvature/noise ratio. The draft states this distinction correctly.

## 5. Targeted check and scope

An inline `python - <<'PY'` exact SymPy check formed a rational orthogonal
three-dimensional frame from two rational rotations, projected its first
two columns onto a two-dimensional range, and checked the displayed Gram
and pseudoinverse bounds. It also checked nine exact affine-hyperplane
pullback identities, including residual offsets with rational coefficients,
and verified \(\|w\|^2\ge1\). The command passed. This is a small
identity diagnostic, not a run of the complete spectral normalization or
ambient-noise solver.

The complementary-minor volume estimate and finite-grid section count
are outside this focused review. Their correctness must be established by
the separate full review. The landed additions of the response-only Cramer
formula and normalized-factor corollary were reread and passed.

The scoped command
`git diff --check -- research-20261002/reviews/smoothed-ambient-interface-review.md`
passed, as did an inline Python check of whitespace, mathematical
delimiters, and local links. No project-wide checks, CI inspection, or
external search were performed.
