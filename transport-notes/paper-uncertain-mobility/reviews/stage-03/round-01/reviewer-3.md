# Independent review: Stage 03, round 01, reviewer 3

Reviewer: `/root/paper_reviewer_3`. Date: 2026-09-07.

Reviewed snapshot: `13abd3fbd62d1a6faf46617e4f678ed14ac22bacb42b8ff161f0ee27d67f0b00`.

I reviewed all of `sections/03-predetermined.tex`, the author handoff, and its dependencies on the accepted scalar-form, transfer, and localization statements. I did not consult other reviews or coordinator checks, delegate review work, or edit manuscript sources. The checks below are independent derivations and adversarial proof checks; no numerical approximation to the new variational constant was used as evidence.

## Unrestricted lower bounds and symmetry

The quotient supremum proves convexity for every positive q: numerator powers are fixed nonnegative constants for each test and the reciprocal affine energy to power q is convex. Reflection and half-period translation are ensemble symmetries, and group averaging is therefore valid even below q=1.

For the sliding bump, the averaged derivative penalty is of order `m/(r ell)` and the reaction penalty of order `r^2 ell^3`. Balancing them gives `ell=(m/r^3)^(1/4)`, and the moment after offset integration is `r^(2-5q/4)m^(-q/4)`. Jensen applies to the negative power for all q>0. The m=0 case can be obtained by sending the bump width to zero. This argument controls arbitrary concentrated mass through Fubini; it does not evaluate D at a root. The disjoint shells and fixed fold bump give the stated order lower bounds without imposing a regularity scale on competitors.

## Sharp tangent certificate and counting factors

I checked the paired test normalization at lines 207–221. Its source is `2 I z`, its frozen derivative energy is `2 T z`, and its reaction energy is `2 U z+o(z)`. Thus the reference quotient is `2 j_psi z`. The tangent to the negative energy power gives exactly the bracket `1+qT/Q_psi - q integral D|h_c'|^2/(2Q_psi z)+o(1)`. The error comes only from the known reaction, so it is independent of the competing D, including unbounded spikes.

The root density is `|sin r|/4`. A scalar offset average becomes half the corresponding integral over both root branches, whereas the paired derivative penalty becomes a full sum over branches. This distinction gives the factor `2^(q-3)` in the reference mean and the same factor in the derivative kernel after its explicit prefactor is included.

For the moving kernel, the derivative amplitude squared and the root-position Jacobian together give `M^(-5/4)d_E^(-5/4)a^(-3/4)`. Multiplication by `z^(q-1)` gives `M^(-1-q/4)d_E^(-1-q/4)a^(-3q/4)`. The chosen reference density makes its product with the root density equal to `Z_E^(1+q/4)/4`. Integrating the profile derivative squared gives T. This independently reproduces the exact kernel coefficient needed to cancel the `qT/Q_psi` term.

The supremum bound is valid at arc boundaries: extending the reference coefficients slightly beyond the retained arc allows the same local change of variables, while truncation discards only a nonnegative kernel. The bound therefore remains valid if a competitor places its entire budget at, or just outside, an arc edge. No pointwise convergence of D is needed. Taking compact oscillator tests approaching the harmonic quotient gives the claimed sharp lower coefficient.

## Graded upper bounds and the critical joint limit

With mobility `a_R(r+R)^(-alpha)`, the separated-root response is `a_R^(-1/4)r^(-3/2+alpha/4)`. The reciprocal-potential complement divided by this response is bounded by `(R/r)^((6+alpha)/4)`, and the core scale is `R^(-3)`. The normalization yields the three stated relations between a_R, R, and M.

The integrated root exponent simplifies to `(8-5q)/(q+4)` after adding one for the radial integral. For the sharp subcritical fields, the normalized qth moment has fold exponent `gamma_q=(6-alpha_q)q/8=7q/[2(q+4)]`, which is less than one exactly below 8/5. The core and rootless contributions satisfy that same envelope; hence dominated convergence also covers the interval 4/3 through 8/5 where the undesigned envelope would fail.

For the critical lower bound, the worst relative support size is `[M/(Z_E M^(7b))]^(1/4)`. It tends to zero for fixed b<1/7, controlling potential Taylor errors, coefficient variation, and the moving-kernel Jacobian. The four one-sided approaches to the folds give `Z_E=4b log(1/M)+O(1)`. Relative kernel errors remain small when this normalization diverges, since the cancellation is performed before the limit in b. This gives `(2C0)^(8/5)(4/7)^(7/5)/8` on sending b to 1/7.

For the critical upper bound, `R=(M/L)^(1/7)`, `a_R~(7/4)R^7`, and the retained minimum root distance is RL. The oscillator width divided by the root distance is at most of order `L^(-7/4)`. The chosen relative interval length `L^(-1/2)` therefore gives expanding oscillator intervals of order `L^(5/4)`, and the complementary response has relative order `L^(-5/4)`. The retained harmonic equivalent is uniform. The remaining root annuli cost only `a_R^(-2/5) log L`; the core and rootless sides cost `a_R^(-2/5)`. These are negligible compared with the retained term `a_R^(-2/5) log(1/R)`. Its coefficient agrees exactly with the lower certificate after substituting the budget normalization.

## New supercritical measure argument

The singular-mass removal is valid for the stated one-dimensional smooth-test convention. For any fixed compact smooth test, flattening its derivative on a neighborhood of a compact set carrying almost all relevant singular mass changes its primitive uniformly by a quantity tending to zero. The correction of the total derivative integral is also small. Absolute continuity of the Lebesgue integral controls the derivative energy against d on the shrinking neighborhood; the remaining singular mass and the small correction control the singular energy. The reaction potential is bounded on the common support, so source and reaction convergence follow. This proves equality of the two responses, rather than merely one inequality.

For each compact test, vague measure convergence gives continuity of the derivative integral. The supremum is lower semicontinuous, and its nonnegative qth power can be integrated by Fatou. Positivity of the infimum follows from a fixed bump with uniformly bounded energy for total measure mass at most one. For finiteness, a graded density with `1<alpha<min(2,6-8/q)` has positive-parameter response exponent `-(6-alpha)/8` and negative-parameter exponent `-3/2`, whose qth powers are integrable. This interval of permissible alpha is nonempty for every q>8/5.

The mass transformation `d_m(x)=m^(6/7)d(x/m^(1/7))` has mass m and gives response `m^(-3/7)J_(mu/m^(2/7))(d)`. The integrated cost therefore scales as `m^(-(3q-2)/7)`. These facts do also prove attainment of the unit-mass density infimum: a vague limit of a minimizing sequence has cost at most S_q, while any loss of absolutely continuous mass would force a strictly larger cost by the positive mass-scaling law. This rules out both escape and singular mass at the minimizer. The argument does not imply uniqueness or regularity, and neither is asserted.

## Natural endpoints and recovery for unbounded densities

The graded positive lower bound gives a genuine H1 bound on each fixed interval despite possible arbitrarily large values of d. Smooth derivative approximation in L2(d dx) is available for this finite absolutely continuous measure; the local lower bound makes derivative integrals continuous, so the stated integral correction preserves endpoint constraints. The anchored primitives converge uniformly and therefore also in the reaction and source terms.

The Neumann compactness argument has the necessary whole-line completion check. Locally the energy controls `integral v^2` by a constant times `|x|^(-4)` and `integral |v'|^2` by a constant times `|x|^alpha`. The one-dimensional pointwise estimate consequently gives the two powers displayed in the manuscript. In particular the limit is bounded for the chosen alpha<2. A remote cutoff then costs at most a constant times `R^(-2)||v||_infinity^2 integral_annulus d`, which vanishes; the original weighted derivative and potential tails vanish as well. Thus the limit is admissible in the minimal smooth energy completion, and artificial Neumann endpoints cannot lower the limiting value. The argument permits the metric weights used by the recovery construction.

For the arbitrary-design lower localization, I independently checked the scaling with `ell=(M/b0^2)^(1/7)` and test amplitude `b0^(-2)ell^(-4)`. The common response factor is `b0^(-2)ell^(-3)`. Offset integration gives the coefficient `b0^((3-8q)/7)/4` before the two-fold mass allocation. Minimizing the sum of the two negative mass powers with total mass at most one gives equal masses 1/2 and the exact coefficient `2^((11q-12)/7)S_q`. Compact tests suffice for each liminf, and Fatou on bounded parameter windows followed by expansion does not interchange an optimizer with a limit.

For recovery, adding a positive graded background and applying the inverse mass scaling restores unit mass at a cost factor at most `(1+varepsilon)^beta_q`. The exact sine coordinate has bounded metric between one and sqrt(2). Mobility chosen proportional to this metric cancels it in the derivative energy; the source and potential retain the metric and meet the Neumann lemma's hypotheses. The mass converges to the intended mass by dominated convergence against the integrable local density. Final normalization is multiplicative by `1+o(1)` and changes all responses by uniformly comparable factors tending to one.

The recovery envelope covers both the expanding scaled fold window and offsets a fixed distance from it. On the regular-root portion, `mu` is of order `ell^(-2)`, and both sides of the asserted bound scale as `ell^((6-alpha)/4)`; on the rootless portion the reciprocal potential gives the required bound. Its qth power is integrable by the chosen alpha. Thus moment convergence follows from a global dominated-convergence argument, rather than a compact-parameter limit alone.

## Interpretation, dependencies, and verdict

The full-bulk transfer is an application of the accepted same-budget theorem and its logarithmic growth condition. The manuscript distinguishes measures used for scalar compactness from stochastic mobility coefficients. It distinguishes achieving the correct order from attaining the sharp coefficient, and the half-uniform counterexample correctly limits the former concentration claim. For a sharply minimizing sequence, strict mass allocation in the lower bound does force full limiting mass split equally between the folds.

No major or minor issue identified in this stage. I recommend acceptance subject to the coordinator's assessment of all five independent reports. In particular, the new supercritical equivalent and the existence claim for its local variational minimizer withstand the independent checks above. No numerical value, unique profile, or publication novelty of S_q has been certified by this review. The stage was authored before the independent review round, as required; final adjudication remains with the coordinator.
