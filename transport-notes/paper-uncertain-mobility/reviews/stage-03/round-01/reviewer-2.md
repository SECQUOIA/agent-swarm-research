# Independent review: stage 03, round 01, reviewer 2

Reviewed snapshot: `13abd3fbd62d1a6faf46617e4f678ed14ac22bacb42b8ff161f0ee27d67f0b00`. Date: 2026-09-07. Independently recomputed every file hash in the manifest; all matched. Read the complete Stage 3 section, its handoff, accepted Sections 1–2 prerequisites, notation, bibliography, and relevant claim/plan entries. No other reviewer report or coordinator-check file was read. No source edits, delegation, or shared-output build was performed.

## Verdict

**No major or minor issue found; accept Stage 03.** In particular, the newly proposed sharp supercritical equivalent has a genuine arbitrary-competitor lower bound and exact-budget recovery argument. Its value is not merely specified by dimensional scaling. This review does not certify later stages or the final literature novelty assessment.

## Checks of the lower-order and critical results

1. **Positive-moment convexity.** The quotient raised to q is a supremum of negative powers of affine nonnegative energies. Those functions are convex for every q>0, not only q≥1. Tests with zero numerator contribute zero under the established quotient convention. Reflection and π translation act on the ensemble as stated, so averaging over the four transformations is legitimate.

2. **Arbitrary-competitor shell bound.** Averaging the derivative cost over a root interval of length comparable to r gives `C m/(r ell)`. The reaction cost is `C r² ell³`. At `ell=κ(m/r³)^(1/4)`, the quotient has size `m^(-1/4)r^(-5/4)`. Raising to q and including parameter probability of order r² produces `r^(2-5q/4)m^(-q/4)`. The m=0 limiting-width argument is valid. Disjoint shells give the critical logarithmic order, and the single fold bump at radius M^(1/7) gives the supercritical lower order for every field.

3. **Graded upper bounds.** On a root neighborhood the frozen mobility is comparable to `a_R r^(-α)` and curvature to r², hence the harmonic response is `a_R^(-1/4)r^(-3/2+α/4)`. Its ratio to the complementary reciprocal response is sufficient precisely because `a_R/r^(6+α)` is bounded. The core scaling has mobility R⁶, rate R⁴, and response R⁻³. The rootless bound follows independently of mobility. The normalization regimes in the text match the integrability of `(r+R)^(-α)`.

4. **Sharp tangent certificate and root factors.** For the paired test, source is `2 I z_c`, reference energy is `2Qψ z_c`, and reaction energy is `2U z_c+o(z_c)`. The tangent to the negative power therefore has exactly the displayed constant `1+qT/Qψ` and derivative penalty. The root intensity is `|sin r|/4`; expected paired scalar values require dividing the root integral by two, whereas the derivative penalty sums the two disjoint root derivatives and requires no such division. This gives `Kψ,E=2^(q-3)jψ^q Z_E^(1+q/4)` and the matching kernel coefficient `(qT/Qψ)Kψ,E`. The cancellation after integration against D uses only its mass, so concentration and fine structure are covered.

5. **Kernel uniformity.** Changing root location to the local test coordinate gives the derivative factor `M^(-5/4)d_E^(-5/4)a^(-3/4)`. Multiplication by `z_c^(q-1)` and the root density leaves `M^(-1-q/4)Z_E^(1+q/4)/4`. Coefficient and Jacobian errors are uniform on fixed arcs; nonnegative endpoint truncation can only decrease the kernel upper bound. On the critical moving arcs the same errors are controlled by ell/r, which tends uniformly to zero for b<1/7. This addresses arbitrary concentrated competitors near the arc endpoints.

6. **Subcritical upper coefficient.** The proposed envelope exponent is `q(6-α_q)/8=7q/[2(q+4)]<1`. It bounds root, core, and rootless regions after multiplication by M^(q/4). Consequently the exact limiting shape may be used in dominated convergence even for 4/3≤q<8/5. For q<2/3 the negative grading exponent causes no difficulty because every finite-M trial is still strictly positive and its fixed-root limit is smooth and positive.

7. **Critical coefficient.** The lower cutoff integral is `4b log(1/M)+O(1)`, and taking b→1/7 after the small-budget limit gives the stated lower constant. In the upper trial, `Z_R∼(4/7)log(1/M)`, and on retained roots `J∼2C0 a_R^(-1/4)(1-c²)^(-5/8)`. The four one-sided fold approaches give the integral factor in the manuscript. The omitted annuli cost only `a_R^(-2/5)log log(1/M)`, and the core/rootless pieces cost `a_R^(-2/5)`. These are smaller than the retained logarithm. Thus the critical coefficient `(2C0)^(8/5)(4/7)^(7/5)/8` is justified.

Symbolic simplification independently confirmed the shell exponent, subcritical domination exponent, and the positivity of the admissible supercritical tail range: `6-8/q-α_q=4(5q-8)/[q(q+4)]`.

## Detailed audit of the new supercritical development

### Singular measures and attainment

The singular-mass removal proof is valid for the specified smooth-test functional. For a fixed compact test, inner regularity gives compact subsets of a null carrier that miss arbitrarily little of the relevant singular mass. Their open neighborhoods can have arbitrarily small Lebesgue measure and arbitrarily small integral of the absolutely continuous density. Flattening the derivative there removes the singular derivative cost. The correction coefficient is O(|U_n|), so a fixed smooth integral-one correction changes both the absolutely continuous and singular energies by quantities tending to zero. The corrected primitive has compact support and converges uniformly to the original test. Source and polynomial reaction terms therefore converge as well. This proves the reverse inequality without assigning a process to a singular measure.

For vague convergence, each compact-test expression is continuous in the measure. Its supremum is lower semicontinuous, and Fatou gives the integrated moment result. The response is lower semicontinuous, hence Borel, in μ as well. The fixed bump supplies a positive lower bound on a compact μ interval uniformly over mass at most one. A graded density with `1<α<min(2,6-8/q)` supplies a finite integrated cost. Thus the positivity used in the mass argument is established independently of existence.

The exact mass transformation `d_m(x)=m^(6/7)d(x/m^(1/7))` scales response by m^(-3/7) and parameter integration by m^(2/7). It therefore gives `S_q(m)=m^(-(3q-2)/7)S_q`. This strict decrease rules out both escaped mass and singular mass in a minimizing sequence: vague lower semicontinuity gives a limit cost at most S_q, while an absolutely continuous limiting mass m<1 would give a cost strictly greater than S_q. Hence the added attainment assertion for a unit-mass L¹ density follows. No uniqueness or regularity is inferred.

The credited measure compactness method is consistent with [Buttazzo–Oudet–Velichkov, Proposition 4.1](https://arxiv.org/pdf/1506.00141). The manuscript supplies its own singular-mass and whole-line arguments instead of treating that bounded-domain proposition as a proof of this new limit.

### Natural endpoints for an unbounded rough density

This lemma addresses a genuine recovery issue and its proof closes it.

- On each compact interval, the graded lower bound is a strictly positive constant. It controls the ordinary derivative in L², while a positive-potential anchor controls constants.
- Smooth functions are dense in the finite weighted-derivative space even without an upper bound on d. Approximate v′ in L²(d dx); because 1/d is bounded on the compact interval, this convergence also implies ordinary L¹ convergence of derivatives. Correcting the integral with a fixed smooth bump costs a quantity tending to zero in L²(d dx). Integration then gives uniform convergence of the functions and convergence of reaction/source terms. This proves the relevant endpoint-domain identification rather than assuming it.
- For expanding intervals, local H¹ compactness and locally weak weighted derivatives identify a limiting derivative. One can test the latter against a smooth function divided by sqrt(d), which is in L² locally, to verify the distributional identification explicitly.
- The potential controls source tails by L^(-3/2), uniformly in compact μ sets and uniformly comparable source/reaction weights.
- The global cutoff step is justified even with unbounded d. On a unit interval about large x, `||v||₂²≤C|x|⁻⁴ E` and `||v′||₂²≤C|x|^α E`. The one-dimensional interpolation estimate gives the displayed bound `|v(x)|²≤C(|x|⁻⁴+|x|^(α/2-2))E`. Since α<2, v is bounded (in fact this bound decays). A cutoff derivative therefore adds at most `C R⁻²||v||∞²∫annulus d`, tending to zero. The original energy tails vanish, and the compact density argument finishes the membership in the whole-line smooth energy completion.

These points make the Neumann upper limit legitimate. Compact tests give the opposite limit; locally convergent bounded weights and converging μ are handled by the same arguments. No hidden smoothness or upper-density assumption is needed.

### Arbitrary-design fold liminf and equal allocation

With the common lower-bound scale `ell=(M/b0²)^(1/7)`, normalize each pushed-forward mobility measure by M. Their total limiting masses sum to at most one. The test amplitude `b0⁻² ell⁻⁴` makes the source, derivative, and reaction energies share factor `b0⁻² ell⁻³`; the normalized derivative coefficient is one because `M=b0² ell⁷`. Local potential convergence therefore proves the stated pointwise liminf by compact tests.

Fatou applies on each fixed μ window; these windows correspond to disjoint physical offset windows for the two folds. Expanding the μ windows after taking the lower limit covers the entire local integrated functional. The probability/Jacobian factor is

`(1/4) b0^(1-2q) ell^(2-3q)`,

which becomes `(1/4)b0^((3-8q)/7)` after multiplication by M^((3q-2)/7). Applying mass scaling to both limiting measures is valid even if they retain singular mass, since their useful absolutely continuous masses are no larger. The decreasing strictly convex function θ^(-β_q) gives equal masses 1/2. Substituting b0=1/2 gives exactly `2^((11q-12)/7)S_q`; independent symbolic simplification confirmed this exponent of two.

### Exact-coordinate recovery and global domination

Adding a small graded background and applying the exact mass scaling back to unit mass increases cost by at most `(1+varepsilon)^β_q`; it does not require continuity of the optimum under an unspecified regularization. Reflection averaging preserves its lower background and mass and cannot increase cost.

For the exact coordinate `x=2sin((s-s_j)/2)/ell`, the metric lies between one and sqrt(2). The field `Dhat=b0² ell⁶ w_ell dtilde` transforms the derivative energy exactly into the unweighted local derivative energy: its metric factor cancels the derivative Jacobian and arclength Jacobian. Source and reaction both retain the bounded weight w_ell. The cell mass is `m∫w_ell² dtilde=m[1+o(1)]` by dominated convergence. Final global normalization therefore changes every response by at most a multiplicative 1+o(1), in the appropriate direction.

At fixed μ the other physical cell has a uniformly positive potential and contributes O(1), so the rough-density natural-endpoint lemma gives the full pointwise recovery. The lower background on dtilde supplies the global comparison `D_M≥c ell^(6+α)(r+ell)^(-α)`. The resulting rescaled envelope decays as `(1+μ)^(-(6-α)/8)` on the root side and `(1+|μ|)^(-3/2)` on the rootless side. Both qth powers are integrable by the chosen α range. The manuscript also checks the regular-offset ends of the parameter halves, where μ is of order ell⁻², so this is an envelope on the entire expanding integration range, not just compact μ sets. Dominated convergence therefore proves integrated recovery with the same factor as the lower bound. The ordered limits in the near-minimizer and background parameters preserve the sharp value.

## Physical interpretation and limits

The accepted same-budget transfer applies because all three scalar values dominate logarithmic moments. The recovery fields have positive floors on the compact wall for each fixed budget, even if their local densities are rough or unbounded. They therefore belong to the physical class introduced in Stage 1. The distinction between achieving the correct order and attaining the sharp equivalent is correctly retained: wasting a fixed fraction of mass can preserve an exponent but cannot preserve the sharp constant. Equality in the lower-bound allocation argument indeed forces full, equally split limiting mass at the two rescaled folds, without implying a unique limiting density.

No currently actionable gap or correction was identified. The complete manuscript still requires the planned later-stage and final reviews, and broader primary-literature novelty comparison remains separate from this mathematical acceptance.
