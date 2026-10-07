# Significance update: sharp growth tails and expected exact QP work

Update: the [frontier reassessment](frontier-significance.md) includes
the later Gaussian-like ambient QP and MIQP FPT theorems, sparse mixed and
anisotropic separable closure, pure-integer quartics, and the deterministic
orthant certificate. It supersedes this note's
headline ranking; the \(k\le2\) theorem below remains a useful special bound.

Date: 2026-10-02. This addendum updates
[the program assessment](current-significance.md) and
[the earlier perturbation assessment](smoothed-growth-significance.md).
It reads the completed proximal-tail and expected-work proofs, their
independent reviews, and the separate approximate cell-count draft.
The literature comparisons below use the existing literature agents'
source checks and a targeted local read of Kelner and Nikolova's theorem
and perturbation definitions. This assessment did not start another
search or ingestion workstream.

The program now has a stronger algorithmic conclusion than high-probability
optimization under a random growth promise. For a bounded rational
polytope QP with at most two negative Hessian eigenvalues, one explicit
finite rational draw of independent noise in every linear coefficient
can be solved exactly, on every realization, with expected bit work

\[
 \operatorname{poly}(I)
 \left(1+\frac{\nu\sum_iw_i}{\sigma}\right).
\tag{1}
\]

Here \(w_i\) are the feasible coordinate widths, \(\nu\) is the
magnitude of the most negative Hessian eigenvalue, and \(\sigma\)
is the noise half-width. The
[expected-work theorem](../new-direction/expected-smoothed-qp.md)
passed this author's
[fresh actual-file review](expected-smoothed-qp-adversary.md), with a
separate challenge of the precision and conditioning exponents.

This is the strongest completed algorithmic milestone in the current
program, judged by the removal of an input conditioning promise and the
strength of its output and probability guarantees. It moves the
negative-inertia branch ahead as the natural headline for the smoothed
analysis. The pruned-grid theorem remains the distinct mixed-integer
contribution; the new expected theorem does not cover its full domain.
This ranking concerns the mathematical conclusions, not established
publication priority or practical solver performance.

## What changed

The [proximal theorem](../new-direction/proximal-growth-tail.md) proves
the sharp bound

\[
 \Pr\{g_*<\varepsilon\}
 \le2\varepsilon\sum_i\phi_iw_i
\tag{2}
\]

for every continuous objective on a nonempty compact feasible set under
independent linear noise with density bounds \(\phi_i\). Its constant
is attained already in one dimension. There is no logarithmic loss from
summing coordinate maximal slopes. For rational QPs, a polynomial-bit
grid gives the same linear tail plus an explicit residual, uniformly
over every growth threshold on the same distribution.

The proof controls the actual bad-growth event through a proximal map.
Bad coefficients map into a null nondifferentiability set; the area
formula bounds their indicator by the divergence of a bounded monotone
displacement. Integrating its coordinate variations gives (2). This
is a sharper and more geometric statement than the earlier response-sum
certificate. Its ingredients remain classical convex analysis and
geometric measure theory. The exact result needs source comparison;
its elementary ingredients neither establish nor refute publication
priority.

The expected algorithmic conclusion requires a separate step. The
conditioned spectral algorithm's numerical exponent is \(k/2\).
For \(k=1\), the inverse-growth tail is integrable at this exponent.
For \(k=2\), it is at the logarithmic threshold. Interleaving with
exact face enumeration caps the work there. A sufficiently fine
rational grid makes the mass of ties and other zero-growth draws small
enough to pay for their fallback work. Sampling precision enters
ordinary polynomial arithmetic, and no resampling changes the instance.

The sharpness improvement is not logically necessary for this polynomial
tractability conclusion. The earlier dimension-dependent linear growth
tail, with a polynomial factor in dimension, could also be integrated
against this fallback. The decisive algorithmic addition is identifying
the actual \(k/2\) exponent and combining it with a finite-bit exact
fallback without a precision circularity. The proximal theorem provides
the strongest quantitative input and a clean general result of its own.

## Why this is a real expected-work result

Every draw from the specified finite distribution is solved exactly,
including multiple-optimum draws. The expectation includes all of them.
The algorithm never asks for a favorable growth event, reports failure
because a work budget expired, or redraws the objective until an easy
sample appears. The noise distribution is fixed by the base instance
and its prescribed scale; it does not depend on a requested approximation
tolerance.

Finite precision is essential to the exact Turing statement. A draw has
polynomial bit length, the output is an exact rational point and value,
and convex subproblems and fallback enumeration have charged bit costs.
This is stronger than a statement about real-arithmetic oracle calls.

The numerical factor in (1) remains material. Polynomial input encoding
does not bound its value. Noise small enough to preserve a tiny original
decision gap may destroy the useful expected bound. The result solves
the sampled objective, not the original one. Large positive curvature
affects input length and preprocessing; it does not appear as a separate
numerical multiplier in (1).

The method currently proves the result only for \(k\le2\). For larger
\(k\), integrating the same capped condition bound leaves an exponential
factor. This is a limitation of the analysis, not proof that expected
polynomial algorithms are impossible. The theorem also remains continuous:
it does not turn arbitrary mixed-integer convex recourse into a polynomial
oracle.

## Distinguish the separate direct expected-cell argument

The [direct cell-count draft](../new-direction/smoothed-semiconcave-cells.md)
is a different result and is not independently approved by this
significance assessment. It bounds expected near-optimal grid nodes using
local neighbor comparisons, rather than a global growth modulus. Its
current recourse application perturbs in the supplied low-dimensional
coordinates of \(T\). That produces original coefficient noise
\(T^Td\), which is generally correlated and supported on a proper
subspace.

| Issue | Reviewed expected exact theorem | Separate direct cell-count draft |
|---|---|---|
| Perturbation law | Independent noise in every original linear coefficient | Independent noise in auxiliary coordinates; original noise is generally correlated |
| Structural range | At most two negative Hessian eigenvalues | Any fixed auxiliary dimension in its current approximate bound |
| Output | Exact rational optimizer and value | Certified additive approximation |
| Rational sampling law | Fixed before any accuracy request | Precision chosen for the terminal approximation level |
| Main expectation argument | Growth tail, explicit \(k/2\) exponent, exact fallback | Direct expected count of near-optimal deterministic grid nodes |
| Status used here | Completed proof and fresh review | Separate review workstream |

Neither statement should be described as an extension of the other's
noise model or output guarantee without a new proof. In particular, the
direct cell count does not yet give exact recovery under one fixed finite
distribution for arbitrarily fine refinement.

## Prior-art risk and positioning

The existing literature agents identify
[Kelner and Nikolova's 2007 theorem](../../literature/papers/kelner2007-on-the-hardness-and-smoothed/fulltext.md)
as an important comparator. Sections 2.2--2.4 give expected polynomial
exact minimization for a constant-rank quasi-concave objective under a
random rotation of its objective subspace, over an integral polytope with
controlled vertex coordinates. Their rank is the dimension on which the
whole objective depends, rather than its number of negative Hessian
eigenvalues. The theorem specifies an objective oracle and a continuous
rotation distribution; it does not state the exact rational sampling and
bit-work guarantee in (1).

These are substantive model differences: a general indefinite quadratic
need not be quasi-concave or have low total rank, and independent ambient
linear noise does not rotate its Hessian eigenspaces. They justify treating
the present statement as a distinct comparison target, rather than claiming
that it dominates the earlier theorem. Expected efficient optimization
after smoothing is already an established research direction.

The spectral branch-and-bound lineage remains directly relevant.
Vavasis, Luo and coauthors, and related low-negative-inertia approximation
results supply much of the algorithmic framework. The present result
does not introduce spectral subdivision, convex quadratic recourse, or
exact active-face enumeration. A careful comparison should ask whether
their algorithms admit this same expected analysis under the present
perturbation law, rather than only compare their published worst-case
approximation rates.

For the sharp tail, the
[focused source audit](../prior-art/proximal-growth-tail-prior.md)
identifies Beier and Vöcking's quantitative discrete isolation as close
prior art. Their value-gap statement is not the same as distance-normalized
growth on arbitrary compact continuous sets. Qualitative generic growth
and local tilt stability are also established. The audit found no exact
match for the proximal trace bound, which is a scoped search result,
not a novelty certificate.

The appropriate headline is therefore a sharp quantitative growth theorem
with a finite-bit realization, and an expected exact-work consequence
for rational QPs with at most two negative directions under the specified
linear perturbations. It is a stronger theoretical capability than the
earlier high-probability conclusion. It is not yet evidence of competitive
running time, memory use, or numerical robustness against mature solvers.

## Verification scope

This assessment followed a fresh proof review and a focused independent
challenge. It used local documents and the existing literature agents'
reported comparisons. Targeted document checks cover whitespace, paired
math delimiters, and local links. No executable optimization benchmark,
project-wide verification, or CI inspection was performed.
