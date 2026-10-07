# Independent review of closure under full ambient noise

Date: 2026-10-02. Scope: the complete
[ambient-noise extension](../new-direction/smoothed-ambient-cell-closure.md),
including the added volume, section-complexity, finite-grid, and exceptional
hyperplane arguments. The underlying algebraic closure algorithm was
[reviewed separately](smoothed-exact-cell-closure-review.md).
No substantive gap was found in the completed extension. This review
does not establish publication priority.

## Conclusion and runtime distinction

The dependence among the transformed factor coefficients is handled
correctly. The proof does not condition on a residual perturbation and
then invoke independent factor noise. It instead integrates the ambient
cube directly, and later transfers local-event probabilities to the finite
ambient product grid by a uniform section bound.

The result returns an exact optimum for every draw from the specified,
base-chosen rational product law on the original linear coefficients.
Expected work is polynomial at each fixed negative rank under the stated
numerical bounds. The displayed count contains powers of the ambient
dimension with rank-dependent exponents. The note correctly does not
claim the dimension-free FPT dependence of the aligned-noise theorem.

## The projection-volume calculation is valid

Write \(\gamma=S(d,\eta)\), with the first columns of \(S\)
equal to \(T^T\), and its remaining columns spanning \(\ker T\).
Fix a subset \(Q\) of \(t\) factor coordinates. For each fixed
value of the other transformed coordinates, the required \(d_Q\)
fiber has volume at most the product of the prescribed interval lengths.
This remains true when the intervals depend arbitrarily on the residual
coordinate \(\eta\). No assumption about a rectangular conditional
distribution is needed.

The other-coordinate integration domain is contained in the corresponding
projection of \(S^{-1}[-\sigma,\sigma]^n\). Its zonotope volume
is the sum of the absolute maximal minors times \((2\sigma)^{n-t}\).
Multiplying by the transformed density introduces \(|\det S|\).
Jacobi's complementary-minor identity cancels this factor and leaves

\[
 \sum_{|K|=t}|\det((T^T)_{K,Q})|.
\]

Cauchy--Schwarz and Cauchy--Binet bound this sum by
\(\sqrt{\binom nt}\sqrt{\det(T_QT_Q^T)}\le n^{t/2}\).
The operator-norm assumption on \(T\) justifies the last inequality.
Empty subsets and zero-dimensional projections use determinant and volume
one, so the endpoint cases also agree with the formula. Rescaling or
changing the residual basis does not introduce a hidden conditioning
factor.

For the local grid event, the neighboring inequalities restrict factor
coordinate \(d_i\) to an interval depending only on the residual.
All other factor coordinates cancel. The upper-curvature bound controls
its length uniformly in that residual. Applying the volume lemma to the
interior-coordinate subset and summing over the deterministic grid gives
the stated effective density \(\sqrt n/(2\sigma)\). This bounds
the necessary local event directly; it does not analyze a noise-dependent
global optimizer.

## The exceptional hyperplanes remain fixed in ambient space

For each active KKT basis, the optimizer is affine jointly in auxiliary
parameter and residual noise. Its derivative with respect to the auxiliary
parameter depends only on the base KKT matrix and \(\alpha T^T\).
The critical-region normals in that parameter and the quadratic-piece
Hessian are therefore independent of residual noise. Only their offsets
change, and those offsets are affine in the residual.

An exceptional factor hyperplane consequently has an equation
\(u^Td+v^Tr+c=0\) with fixed coefficients and \(\|u\|=1\).
Substituting the original-noise decomposition gives ambient normal
\(L=D^Tu+\Pi^Tv\). The exact identity \(TL=u\) implies
\(\|L\|\ge1\), since \(\|T\|\le1\). A factor tube of
width \(\tau\) is thus contained in an ambient Euclidean tube of
width at most \(\tau\). Large residual-offset coefficients cannot
make the ambient normal disappear or enlarge the required tube.

The argument also covers singular piece Hessians and lower-dimensional
critical regions, using the algebraic gradient identity from the earlier
closure review. A critical-region row with zero auxiliary normal cannot
be violated elsewhere in a cell while holding at its queried corner;
such rows introduce no extra exception.

The base-only curvature bound correctly uses the KKT response to the
auxiliary parameter. It does not clear denominators involving the sampled
linear coefficient. Therefore the hyperplane count, curvature bound, and
terminal level are fixed before the noise precision is chosen.

## The finite-grid transfer handles degeneracies

Along any line in one original noise coordinate, a fixed auxiliary query
has at most \(2^m\) active-basis critical intervals. They are intervals
because feasibility and multiplier conditions are affine on the line.
They cover the line because every convex optimum admits the nonsingular
basis extraction already proved. Overlapping valid formulas agree, so
their endpoints suffice to partition the line into quadratic pieces.
There is no need to count arbitrary crossings of unrelated candidate
quadratics.

A local event uses at most \(2k+1\) such queries. On each common
open piece, it is a conjunction of at most \(2k\) quadratic weak
inequalities. There are at most \(4k\) roots to consider. Identically
zero comparisons add none. Counting the resulting intervals, isolated
root points, and critical-interval endpoints gives the conservative
\(C_{\rm sec}\) stated in the note. Degenerate singleton critical
regions and repeated roots fit within this count.

For a union of at most \(C_{\rm sec}\) intervals or isolated
points, equally spaced endpoint-grid probability differs from uniform
interval probability by at most \(2C_{\rm sec}/N\). Replacing
one ambient coordinate distribution at a time proves the tensor-grid
bound \(2nC_{\rm sec}/N\). It is important that the section bound
holds for every fixed value of the other coordinates, including their
mixed discrete/continuous values during this replacement. The written
argument establishes that uniformity.

Summing over all deterministic grid vertices through the base-chosen
terminal level is valid even though the algorithm visits only an adaptive
subset. The choice of \(N\) makes the total additional expectation
at most one. Its logarithm, rather than \(N\), is the sampling and
encoding cost; \(\log N=O(kJ+\log C_{\rm sec}+\operatorname{poly}(I))\)
has polynomial base-input length. No full fine-grid enumeration is part
of the algorithm.

The separate ambient hyperplane bound includes its \(1/N\) atom term
and makes the probability of the same-draw fallback at most \(1/B\).
The fallback cost \(B\operatorname{poly}(I+\log N)\) therefore
contributes polynomial expected work. No exact rational-recovery precision
depending on the sampled denominator enters the construction.

## Normalization and numerical widths

The added normalized-factor bound is valid. With orthonormal Jacobi
columns \(B\) and exact range projector \(R\), the existing
residual estimate gives \(\|(I-R)B\|\le1/8\). Thus

\[
 TT^T=B^TRB
     =I-B^T(I-R)B\succeq(63/64)I.
\]

Together with \(\|T\|\le1\), this implies the stated safe
bound \(\|(TT^T)^{-1}T\|\le2\). The fixed rational auxiliary
widths are consequently at most
\(\operatorname{diam}(X)+4\sigma\sqrt n/\alpha\).
The explicit normalized count still contains powers of \(n\)
depending on \(k\); this is a real limitation of this estimate,
not hidden factor conditioning. The separate
[interface review](smoothed-ambient-interface-review.md) checks the same
normalization and arithmetic conclusions.

## Targeted verification

The command
`python research-20261002/new-direction/check_ambient_noise_review.py`
passed exact SymPy checks of the new ingredients:

- 84 complementary-minor identities for oblique rational factors in
  ambient dimensions two, three, and four, with residual bases rescaled
  by factors of 1,000 and \(1/1{,}000\); the Cauchy--Binet and
  determinant-sum bounds were also checked.
- 14 ambient-normal pullback identities and lower norm bounds, including
  nonzero residual offsets.
- 27 exact local-event line sections for a two-variable convex recourse
  model, with 81 finite-grid discrepancy checks at grid sizes 8, 32,
  and 128. Each grid membership was compared with the symbolic section
  obtained from its quadratic inequalities; the probability bound used
  the section's actual component count.
- 27 exact polygon-area probabilities for obliquely transformed noise
  with residual-dependent interval locations, checked against the fiber
  volume bound.

These diagnostics check the added geometry and finite-noise steps; they
do not claim an implementation or performance test of the full ambient
solver. The reused closure and fallback have their separate targeted
checks. The scoped command
`git diff --check -- research-20261002/reviews/smoothed-ambient-cell-closure-review.md research-20261002/new-direction/check_ambient_noise_review.py`
passed, as did an inline `python - <<'PY'` check of whitespace,
mathematical delimiters, and local references. No project-wide checks,
CI inspection, or external search were performed.
