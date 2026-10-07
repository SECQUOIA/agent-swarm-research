# Independent composition review of Gaussian mixed-integer cell closure

Date: 2026-10-02. Verdict: **PASS**. The completed
[Gaussian MIQP manuscript](../new-direction/smoothed-gaussian-miqp.md)
has no substantive gap in the reviewed composition. This is a mathematical
review, not a priority claim or a production-solver validation.

The reviewer authored the Gaussian continuous ingredient but did not
author this mixed-integer extension. This review freshly read the actual
composition, the complete
[mixed gap-certificate theorem](../new-direction/smoothed-miqp-cell-closure.md),
and the [integer-label isolation proof](../new-direction/integer-label-isolation.md).
It does not infer correctness merely because both ingredients had earlier
reviews. The exact convex-MIQP interface was also checked against the
locally ingested primary statement of
[Del Pia, Theorem 3](../../literature/papers/pia2025-convex-quadratic-sets-and-the/fulltext.md).

## Exact gap certification survives the composition

For the returned integer tuple, the union of the \(2p\) exclusion
inequalities is exactly the set of different integer tuples. Minimizing
over those exclusions gives the true best-other-label gap, including zero
at ties and infinity if no other tuple is feasible. This needs exact
convex-MIQP values and feasible witnesses; approximate primal values do
not supply the certificate.

For each label, subtracting the common quadratic in the auxiliary variable
leaves an infimum of affine functions with slopes \(-\alpha Tx\).
Every label's increment along a displacement lies in the same interval
of scalar slopes. Therefore the difference between two increments is
bounded by that interval's width, namely
\(\alpha\operatorname{diam}(T\mathcal P)\|a-v\|\), with no
missing factor of two. The prescribed corner-gap threshold dominates
this change throughout the cell. Combined with a covering fixed-label
critical region, it proves whole-cell equality with the label's quadratic
formula. Equality in the gap threshold is safe because a competing label
may tie without changing the certified value or witness.

The scalar label-isolation proof applies to the original objective, not
to the adaptively selected auxiliary corner. If its gap certificate
fails at a near-optimal corner, square completion gives two distinct
original feasible labels within the displayed
\(C_{\rm gap}h\) of the original optimum. If neither is globally
best, the global best label and one of these labels still provide the
required two-label event. No union over grid points is needed here.

## Gaussian approximation and label isolation

Condition on all original coefficients except integer coefficient
\(\gamma_i\), even if the conditioned coefficients already have
the finite law. Each nonempty group with coordinate value \(t\) has
objective \(a_t+t\gamma_i\). Compact mixed feasibility and continuity
give attained group minima. The intercepts are fixed under this
conditioning, although they can depend arbitrarily on all the other
coefficients and on optimized continuous variables.

The lower envelope has at most \(U_i-L_i\) breakpoints. A near-winning
different group puts \(\gamma_i\) within \(\varepsilon\) of a
breakpoint. The Gaussian probability of that interval is at most
\(\varepsilon/\sigma\). Scalar Kolmogorov error \(\delta\)
adds at most \(2\delta\), including closed endpoints and singleton
intervals. Thus conditioning, union over breakpoints, and union over the
integer coordinates prove exactly

\[
 \Pr\{\text{two near-optimal original labels}\}
 \le G(\varepsilon/\sigma+2\delta).
\]

There is no extra ambient-coordinate factor in this conditional estimate.
The finite product law preserves the required independence in the
original coordinates. Zero-gap ties at atoms are controlled by the
Kolmogorov term, rather than excluded by a genericity assumption.

The continuous-slice hyperplane event uses a different argument. Gaussian
projection controls each tube, and full product-law replacement adds
\(2n\delta\) per hyperplane. Adding the two event types yields the
manuscript's \(2(nK+G)\delta\) term. The distinction between the
two transfers is correct.

## Nonsmooth recourse does not break the weighted count

The mixed envelope is the infimum of its feasible-witness quadratics.
Every attaining witness supplies a global quadratic upper model, so
coordinate upper curvature and the deterministic location constraint
needed by the Gaussian weighted count remain valid. The witness's image
lies in \(T\mathcal P\). One does not need a derivative of the mixed
envelope or a favorable choice among tied witnesses.

For fixed residual noise, the local neighboring inequalities restrict
the factor coefficients to intervals whose endpoints depend on that
residual alone. A witness selected from the residual recourse can be
chosen without the factor noise. Gaussian factor/residual independence
therefore applies exactly as in the continuous proof. The true finite
law need not retain that transformed independence: its local-event
probabilities are transferred from the Gaussian proxy by their uniform
axis-section bound.

The mixed section bound correctly includes pairwise intersections of
different labels' quadratic pieces. Fixed-label regions alone would be
insufficient because different labels' values need not agree on overlaps.
The bound \(R^2\) has polynomial logarithm even when integer ranges
are large. Degenerate regions and isolated equality events are covered
by the generous component count and one-sided CDF limits.

## Support and precision remain fixed before sampling

For \(R_s=2^t\), the auxiliary width is at most a base constant times
\(1+R_s\). The gap constant is affine in that width, and the combined
failure coefficient is consequently also at most linear in \(R_s\).
The product \(sC_{\rm bad}\) is at most quadratic in \(R_s\).
The final manuscript makes this exact: both factors are at most
\(2^t\) times their values at \(t=0\), so

\[
 J(t)\le J(0)+2t.
\]

Here \(J(0)\) is polynomially bounded in the base encoding length,
not merely an exponentially large number with short encoding. The same
holds for the additive precision bound \(A_1\): all original LP
ranges and coefficient bounds have polynomial bit length, and only
their logarithms enter these additive constants.

Hence the required sampler precision grows only linearly in \(kt\),
up to logarithms. The support loop terminates with polynomially bounded
\(t,J,b\). The actual scalar sampler operates on radius \(b+20\),
not on the possibly larger trial support \(2^t\), so its bounded
polynomial sampling-time guarantee remains applicable. Sampling starts
only after the loop terminates. The sampled denominators are absent
from the response-Hessian bound and all prior cutoff choices.

At the selected cutoff the geometric/gap contribution is at most
\(1/(4B)\), and the finite-law contribution is at most \(1/(4B)\).
Their sum is at most \(1/(2B)\). The same-draw fallback costs
\(B\operatorname{poly}(I+b)\), so its expected contribution is
polynomial, without rejecting or resampling an exceptional atom.

## Parameter and arithmetic scope

The expected local count contains the original projection widths, not
the enlarged auxiliary widths. Under the normalized frame these widths
are at most \(\operatorname{diam}(\mathcal P)\), and
\(\alpha<4\nu\). Ambient dimension enters polynomial bit budgets
and logarithmic probability precision, not a numerical factor raised
to \(k\) in the count. The stated FPT parameter scope
\((p,k,1+\nu\operatorname{diam}(\mathcal P)/\sigma)\) is therefore
supported. The diameter is that of the continuous relaxation as stated.

Exact convex-MIQP optimization contributes \(f(p)\) times a polynomial
with an absolute exponent. Integer coordinates lie in the original
bounded LP ranges, so their heights are polynomial independently of that
oracle's running-time factor. Fixing its returned tuple and polishing the
continuous convex slice provides uniformly polynomial-height values,
witnesses, and critical formulas for subsequent work. The \(2p\)
additional gap queries introduce no new integer parameter.

The result concerns the specifically chosen finite Gaussian-like product
law and the perturbed objective. It is not an exact-real Gaussian input
algorithm, an arbitrary-precision-law assertion, or an unperturbed
worst-case optimization guarantee. These limitations are stated in the
manuscript.

## Distinct targeted checks

The reviewer ran

```sh
python research-20261002/new-direction/check_gaussian_miqp_review.py
```

The [diagnostic](../new-direction/check_gaussian_miqp_review.py) enumerates
a 33-atom dyadic Gaussian-like law and computes label gaps and event
probabilities exactly as rational numbers. It passed five complete-law
fixtures, 3,333 draws, 84 tied draws, and 20 isolation bounds. Fixtures
include missing labels, a nonproduct label set, ties, and a continuous
quadratic variable optimized separately for each integer label. Both CDF
limits at every atom were checked against a high-precision Gaussian CDF;
the probability bound uses a deliberately loose analytic Kolmogorov
bound for the small law.

These checks specifically exercise the new scalar Gaussian-isolation
transfer, including residual-dependent optimized intercepts. They do not
duplicate the existing cell-closure tests, implement the general oracle,
or enumerate the theorem's much finer sampler. The author separately
ran [the support-budget diagnostic](../new-direction/check_gaussian_miqp_budget.py):
six synthetic rational-bound fixtures and 63 exact trials passed,
including a case attaining \(J(t)=J(0)+2t\), a 1,000-bit curvature
bound, and large integer ranges. This review reread and approved the
final sharpened loop proof; it did not duplicate that diagnostic run.

Scoped checks of this review passed: six local links, trailing whitespace,
and paired mathematical delimiters. No project-wide checks, CI inspection,
or external literature search were performed for this review.
