# Adversarial review: summing optimizer-response slopes

Date: 2026-10-02. This separate review checks the actual
[summed-response draft](../new-direction/summed-response-growth.md), including
its continuous and rational-grid constants, linear example, and inverse-growth
moments. The reviewer independently derived the grid completion before reading
the completed draft. The earlier response and component arguments were checked
against [the preceding note](../new-direction/smoothed-linear-growth.md).
This is a mathematical review, not a literature-priority assessment.

The claimed improvement is valid. Finite anchored slopes in every coordinate
imply uniqueness. Applying the scalar comparison with every positive
\(K_i>Z_i\), then letting \(K_i\downarrow Z_i\), gives

\[
(x_i-x_i^*)^2\le4Z_i[F_c(x)-F_c(x^*)].
\]

This includes zero slopes without division. Summation gives the asserted
growth certificate \(1/(4\sum_iZ_i)\). If the sum vanishes, the domain is a
singleton; removing constant coordinates handles this exception. No
independence among the slopes is needed.

For continuous perturbations, the conditional weak bound gives
\(\Pr(Z_i>s)\le\min\{1,a_i/s\}\). With \(A=\sum_i a_i\) and
\(T=2A/\rho\), the event that any slope exceeds \(T\) has probability
at most \(\rho/2\). Since \(T>a_i\), tail integration and the entropy
bound give

\[
\mathbb E\sum_i\min\{Z_i,T\}
\le A[1+\log(T/A)-\sum_i(a_i/A)\log(a_i/A)]
\le A[1+\log(2n/\rho)].
\]

Markov's inequality costs another \(\rho/2\), proving the stated
continuous constant. Independence of the sampled coefficients is used in
the conditional density argument; it is not transferred to the slopes.

The rational-grid calculation also passes. The response-piece bounds are
deterministic and uniform over the other coefficients. With
\(\beta_i=4B_i^2/M_i\) and \(M_i\ge16nB_i^2/\rho\), their sum
\(\beta\) is at most \(\rho/4\). Choosing \(T=4A/\rho\) gives

\[
\Pr(\max_iZ_i>T)\le A/T+\beta\le\rho/2,
\qquad
\mathbb E\sum_i\min\{Z_i,T\}
\le A[2+\log(4n/\rho)].
\]

The added expectation term is \(\beta T\le A\); retaining it accounts
for grid atoms, including infinite slopes at ties. Markov and the maximum
event yield precisely
\(g\ge\rho/[8A(2+\log(4n/\rho))]\). Under common half-width
\(\sigma\), substituting \(A=3\sum_iw_i/\sigma\) gives equation (3).
The union event excludes infinite slopes before invoking uniqueness.

Choosing the least sufficient powers of two preserves polynomial sampling
bits and rational coefficient encoding for the three stated face counts.
Doubling the earlier sufficient grid bound adds one bit per coordinate.
The proposed ceiling of the binary logarithm is a valid rational replacement
for the natural logarithm, since its argument exceeds one. The solver
conclusions remain conditional on the earlier solver theorems and their
numerical parameter assumptions; this review does not repeat those proofs.

The linear example is correct almost surely. Each coordinate displacement
lies in \([0,2]\), so \(d_i\ge d_i^2/2\); moving only a coordinate of
least absolute coefficient to the opposite endpoint attains equality.
Therefore \(g_*=(1/2)\min_i|b_i|\). Its distribution and quantile in
equations (16)--(17) follow directly. The lower quantile bound uses the
concavity of \((1-\rho)^{1/n}\); the upper uses
\(1-e^{-z}\le z\). Thus this family requires dimension scale
\(\sigma/n\), and scale \(\sigma\rho/n\) for small failure probability.
It does not require a logarithmic loss in every possible theorem.

The anchored slope of this endpoint response is exactly \(2/|b_i|\).
For \(Y=U^{-1}\), with \(U\) uniform on \([0,1]\),
\(\mathbb E\min(Y,T)=1+\log T\) and
\(\mathbb E\min(Y,T)^2=2T-1\) for \(T\ge1\). At
\(T=n\log n\), the probability of any truncation is at most
\(1/\log n\), while the variance of the truncated sum divided by
\((n\log n)^2\) is at most \(2/\log n\). Its normalized mean tends
to one. Chebyshev therefore proves equation (18), so this particular
summed-slope certificate does lose a logarithm on the example.

The inverse-growth moment claims also pass. In the continuous example the
minimum coefficient has positive density at zero, which makes moments of
order at least one infinite. On an even grid, a single reciprocal coefficient
has moments proportional to

\[
\sigma^{-a}M^{a-1}\sum_{j=1}^{M/2}(2j-1)^{-a}.
\]

The sum grows logarithmically for \(a=1\) and stays bounded above and below
by positive constants for fixed \(a>1\). For fixed \(n\), the moment of
the maximum reciprocal coefficient lies between the single-coordinate
moment and \(n\) times that moment. This proves both stated orders for
\(g_*^{-a}\).

One wording clarification was requested: the statement that finite grids
remove the divergence applies to this linear example with an even grid.
It must not be read as a claim for general rational-grid QPs, which can
retain tie atoms. The draft otherwise correctly separates failures of an
inverse-growth moment argument from lower bounds on actual algorithmic work.
The example itself is easy to solve by selecting endpoints.

No substantive mathematical gap was found. This review used direct analytic
checks and targeted document reads. No executable optimization test,
project-wide verification, CI inspection, or external literature search was
performed. A targeted Python document check verified trailing whitespace,
paired math delimiters, and local Markdown links in this review.
