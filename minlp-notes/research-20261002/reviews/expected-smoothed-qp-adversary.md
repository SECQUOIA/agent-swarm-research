# Independent review: expected exact work with at most two negative directions

Date: 2026-10-02. This review reads the actual
[expected-work proof](../new-direction/expected-smoothed-qp.md), the
retained-cell and exact-recovery sections of
[the negative-inertia algorithm](../new-direction/negative-inertia-qp.md),
and the reviewed
[fixed-grid growth tail](../new-direction/proximal-growth-tail.md).
An independent child challenged the numerical exponent and precision
argument; a further focused check examined the cap and integration.

The theorem passes. No substantive gap was found in the stated expected
bit-work bound for \(k\le2\). The algorithm solves the same sampled
objective exactly on every draw, including ties. Its expected work is
bounded by

\[
 \operatorname{poly}(I)
 \left(1+\frac{\nu\sum_iw_i}{\sigma}\right).
\]

This verdict concerns the explicit fine rational sampling law in the
note. It is not a claim about arbitrary discrete perturbations or the
unmodified conditioned algorithm.

## The tail applies to one fixed distribution

The tail input is exactly the one supplied by the proximal theorem:

\[
 \Pr\{g_*<\varepsilon\}
 \le \frac{\sum_iw_i}{\sigma}\varepsilon+\beta,
 \qquad
 \beta=\frac{16n(2^m+1)^2}{M}.
\]

It holds for every positive threshold with the same grid and residual.
The component count does not depend on the threshold, coefficient
magnitudes, or sampling precision. Thus using
\(\varepsilon=\nu/t\) as \(t\) varies in the expectation integral
does not change distributions.

For \(k>0\), \(\nu>0\). With
\(Z=\max\{1,\nu/g_*\}\), including \(Z=\infty\) at zero growth,
the strict event identity gives
\(\Pr\{Z>t\}\le(\nu\sum_iw_i/\sigma)/t+\beta\) for \(t\ge1\).
The singleton case has \(Z=1\) and causes no exception. The separate
convex branch handles \(k=0\), so the proof never divides by the zero
exponent \(p=k/2\).

## The fallback is exact and its combinatorial factor is independent of precision

The active-row enumeration includes an optimizer even with a singular
ambient Hessian, a lower-dimensional polytope, or several optimizers.
Choose an optimizer on a face of smallest possible dimension. Its
tangent Hessian is positive semidefinite. A null tangent direction would
preserve the quadratic objective until reaching a smaller face, so this
Hessian is positive definite, with the zero-dimensional case allowed.

An independent basis of active input rows defines that face's affine
hull. Its KKT matrix is nonsingular: a vector in its kernel has tangent
primal component \(v\) with \(v^TAv=0\), forcing \(v=0\);
independence of the active rows then forces the multiplier component
to vanish. This subset is enumerated and recovers the chosen optimizer.

It is safe to retain other nonsingular feasible stationary candidates
without checking multiplier signs. Every retained point is feasible,
and a true optimum is among them; taking the smallest exact value is
therefore correct. Comparisons and tie selection are rational.
Determinant bounds give polynomial-length candidates even when the
linear perturbation has a large denominator.

The number of subsets is at most \(2^m\), so the fallback bound has
the form \(B P(L)\), where \(B=\max\{2,2^m\}\) and sampling precision
appears only in the polynomial factor \(P(L)\). Choosing
\(M\ge16n(2^m+1)^2B\) makes \(\beta B\le1\). Its logarithm is
polynomial in the base input size, making \(L\) polynomial too.
No assumption about a coefficient-height-independent arithmetic cost
is being made.

## The conditioning exponent survives the bit analysis

The underlying algorithm's normalization gives auxiliary dimension at
most \(k\) and conditioning less than \(2+4\nu/g_*\). Its explicit
retained-cell bound is proportional to
\((1+\sqrt{\kappa})^k\). For \(k=1,2\), child generation, corner
queries, and ordinary cell processing have constant dimension factors.
These operations contribute the numerical power \(Z^{k/2}\).

Exact value isolation and coordinate recovery require
\(\operatorname{poly}(L)+O(\log Z)\) levels. At level \(j\), rational
coordinates, transformed convex-QP inputs, and reconstruction operations
have bit length polynomial in \(L+j\). The specified polynomial-time
convex-QP algorithm therefore adds a fixed polynomial in that quantity.
Summing over levels yields

\[
 P(L)Z^{k/2}(1+\log Z)^d
\]

for an absolute \(d\), after enlarging \(P\). No additional inverse
power of growth occurs. This conclusion would not follow from counting
uncertified numerical oracle calls; the exact convex-QP bit theorem is
essential.

Without positive growth, the fast computation can take arbitrarily long,
but its accepted answers remain sound. Its lower bounds remain valid,
optimum-value isolation uses an unconditional rational height bound, and
acceptance compares an original feasible witness with that isolated
value. The fallback supplies termination where the fast proof does not.

## Capping the logarithms and integrating

Interleaving elementary bit operations of the two fixed algorithms gives
work at most a constant times the smaller completion time. This is
legitimate computational dovetailing, not an assumption that a complete
convex-QP call can finish before the fallback resumes.

For \(p=k/2>0\), the displayed inequality

\[
 \min\{B,Z^p(1+\log Z)^d\}
 \le (1+p^{-1}\log B)^d\min\{B,Z^p\}
\]

is correct in both regimes \(Z^p\le B\) and \(Z^p>B\), including
zero growth by the latter convention. Thus extremely small positive
growth cannot force an uncapped precision factor in the expected bound.

Writing \(r=\nu\sum_iw_i/\sigma\), the bounded tail integral gives

\[
 \mathbb E\min(B,Z^p)
 \le1+r\int_1^B t^{-1/p}\,dt+\beta(B-1).
\]

For \(k=1\), this is at most \(2+r\). For \(k=2\), it is at
most \(2+r\log B\). Since \(\log B=O(m+1)\), the remaining cap
factor is polynomial in the base input size. This proves the claimed
expected bit bound. In particular, the probability mass at ties is
charged to \(\beta B\), rather than discarded or resampled.

For \(k>2\) this same integration produces an exponential factor from
\(B^{1-2/k}\). That limits this proof; it is not an algorithmic
lower bound for the larger class.

## Scope and verification

The conclusion is stronger than a capped high-probability algorithm
permitted to return failure. Here every draw terminates correctly, and
the expectation includes the fallback cost. Numerical control of
\(\nu\sum_iw_i/\sigma\) is still required for polynomial expectation.
The answer optimizes the perturbed objective.

Verification used targeted reads and independent analytic challenges.
No executable optimization test, project-wide verification, external
literature search, or CI inspection was performed. Publication priority
is outside this correctness review.

A targeted inline Python document check passed trailing whitespace,
paired math delimiters, and local Markdown link targets.
