# Independent review: Stage 05, round 01, reviewer 1

Reviewer: `/root/paper_reviewer_1`. Date: 2026-09-07.

Snapshot: `b10b05d41199399897fdd9cc7cc6eab8d0fe2ae90e96c6ff4fa8d7d2ef68b42c`. All fifteen manifest hashes matched. I read the entire new section, the applicable accepted form/transfer, quadratic localization and predetermined-design prerequisites, the handoff, notation and claims, and the new cited source. I did not read other reports or coordinator-checks, coordinate conclusions, delegate, or modify manuscript sources.

## Verdict

**No major issue found. Two minor precision corrections are requested below.** The local global certificate and its equality case establish the stated unique scalar optimizer. The compact-wall result uses actual competitor masses and supports the claimed allocation. The explicit degenerate trials have a valid minimal closed realization and the stated fixed-profile flux/remainder behavior. The oracle mean proof supplies a measurable policy with uniform integrable bounds and does not assume an expectation–infimum interchange.

The two corrections concern endpoint-domain terminology and the distinction between operator scale and integrated energy scale; neither changes the results or constants.

## Independent checks

### 1. Exact whole-line placement, source interpretation, and uniqueness

I independently expanded `p(y)=y-3y^3+2y^4`, obtaining `int_0^1 p=3/20` and `p'(y)+y^2(9-8y)=1`. Thus the mass is `3aR^5/80` and the flux on the positive half-support is `-Rp(x/R)`. Near zero that flux is `-x+O(x^3)`, on either side; at all three junctions it has no jump. The cusp in h and the jumps in its slope at the outer support edges therefore introduce no distributional delta term.

The dimensionless interior source integral is 10, the interior reaction coefficient is 38/5, the exterior source and reaction coefficients are each 2, and the derivative coefficient is 12/5. These give the total identities 12, 48/5, and 12/5 printed in the section. They also check the direct square completion on each support used later.

The whole-line source is handled correctly as an energy-dual source. The explicit h has a square-integrable derivative on compact intervals and an inverse-square tail. Cutoff and corner mollification approximate it in the relevant weighted energy and source integral. For the proposed bounded D*, this gives the exact inverse response without applying an L2 inverse to the constant source.

For an arbitrary integrable competing D, the same approximants can have derivative uniformly bounded by `b_*+o(1)` and convergent almost everywhere to h'. The cutoff derivative in the distant inverse-square tail is O(`L^(-3)`). Dominated convergence against the fixed measure `D dx` therefore justifies using h in the lower certificate even when D is unbounded, concentrated, or not assigned an operator realization. The source and reaction terms are independent of the competitor and converge as well. The mass identity gives `m b_*^2=12/(5aR)`, so the final lower value is exactly `12/(aR)`.

The uniqueness proof also checks. Equality forces the derivative-bound inequality to be saturated D-almost everywhere. Since the derivative magnitude is strictly smaller than b_* outside the support, D must vanish there almost everywhere. The approximated test h+t phi is admissible for every compact smooth phi, so equality gives the weak equation for D. Its flux `D h'` is locally integrable and has locally integrable distributional derivative, hence has an absolutely continuous local representative. Its exterior value is zero. Since h' is a nonzero constant on each open half-support, integration from either outer edge determines D uniquely and recovers the polynomial. No trace constraint at the cusp is needed in this scalar argument. Differentiating the value with respect to m gives `-64/(a^2R^6)=-b_*^2`, as stated.

### 2. Compact-wall lower and upper bounds

The continuous-rate hypothesis is enough for the fixed local two-sided quadratic comparisons. With actual local masses b_j, the global certificate can be cut off in a fixed neighborhood because for small total M the cutoff acts only on the inverse-square tail. Its source/reaction error is bounded independently of b_j, while the central derivative bound grows as `b_j^(-3/5)` and eventually dominates all cutoff slopes uniformly for `b_j<=M`. Mollification preserves the requisite Lipschitz bound. Disjoint supports let the certificates be added. The auxiliary-budget test in a zero-mass neighborhood correctly gives an infinite response rather than requiring a positive local allocation in advance.

Minimizing `sum w_j b_j^(-1/5)` over total mass at most M uses all mass and gives `b_j proportional to w_j^(5/6)`. With `w_j=Cpl a_j^(-4/5)`, this is the stated curvature power `a_j^(-2/3)`. Strict convexity gives the allocation minimum.

For the upper bound, zero flux permits direct square completion on each actual support with free endpoint values. The support contributes `10/(a_-R)`, and the reciprocal rate on its neighboring exterior contributes at most `2/(a_-R)+O_eta(1)`. A fixed positive-potential remainder is bounded. The common multiplicative curvature adjustment `(1-eta)` does not change the allocation proportions. Taking M to zero first and then eta to zero proves the equivalent while retaining the distinction between a relative asymptotic and an additive bounded error. The comparison to uniform diffusion is also justified by the potential-ordering proof, not an unwarranted application of a C2 theorem statement to arbitrary continuous k.

### 3. Closed realization, zero-capacity endpoints, and physical correction

For the explicit coefficients, the positive set is a finite union of half-intervals with continuous positive D in their interiors; D is zero on the exterior. An energy-Cauchy sequence converging to zero in L2 has weighted derivative limit zero on every compact positive subinterval by the local positive floor. It has zero weighted derivative on the zero set, and the remaining finitely many endpoints have measure zero. This proves closability.

I checked both transition costs. For an outer quadratic zero, a unit transition over width epsilon has weighted derivative cost proportional to epsilon. For the central linear zero, the normalized logarithmic transition has derivative of order `1/(x |log epsilon|)` over `(epsilon^2,epsilon)`, and hence cost of order `1/|log epsilon|`. L2 and bounded-reaction costs vanish with the shrinking intervals. These constructions remove a matching condition between neighboring components. General finite-energy functions need not have finite endpoint traces; this is the terminology correction R1-01 below.

Coercivity at fixed M is valid. Away from the centers the reaction is bounded below on the relevant fixed sets. On a half-support near its center, an interior anchor and weighted Cauchy–Schwarz with `D(x)` comparable to |x| give the bound by `1+|log x|`, whose integral is finite. Thus the source inverse belongs to the minimal L2 form domain for every fixed positive M. The constants may depend on M, as the text permits.

Using the componentwise minimal form, positive-part comparison with h_- is legitimate: its quadratic reaction is below k, its source is one, and its flux is zero at the endpoints. The reaction-plus-derivative energy of the positive part forces `h<=h_-`. On the D=0 exterior the inverse is multiplication by 1/k. The maximum of `y^2(9-8y)` is 27/16 at y=3/4. Thus kh is uniformly bounded on the shrinking supports and exactly one outside them. Their total length is O_eta(`M^(1/5)`), yielding L2 error O_eta(`M^(1/10)`). This argument only concerns fixed separated profiles; it does not imply a uniform fold-offset estimate.

The load difference in the bulk Schur formula therefore tends to zero in the bulk energy dual. Dropping the nonnegative penalty gives the upper limiting remainder. For a fixed smooth bulk trial, its trace has bounded tangential derivative and is admissible for each explicit bounded D. The penalty is at most M times that derivative bound squared. Such smooth tests are dense in the mean-zero bulk energy space, giving the lower limiting remainder. This proves convergence to R0 without requiring extra trace regularity of the maximizing bulk field.

### 4. The measurable oracle policy and all its regimes

For the separated regime, `a=t(2-t)>=t` gives `z=M/a^(7/2)<=L^(-7/2)`. The displayed ratio `R/delta=2(40/3)^(1/5) z^(1/10)(1-eta)^(-1/5)` is correct. A sufficiently large fixed L makes the profile supports lie well inside their comparison neighborhoods and keeps the two neighborhoods disjoint. Taylor's lower bound gives `k>=a x^2(1-eta/4)^2>=a(1-eta)x^2`, so the chosen b is valid uniformly.

The reciprocal-potential estimate separates the immediate root tails, each of order `1/(aR)`, from the fold-scale complement, of order `a^(-3/2)`. The latter is absorbed because R is at most a fixed small multiple of sqrt(a). At a fixed simple-root offset, the shrinking comparison radius has order `M^(1/10)`, so its outside error is smaller than `M^(-1/5)`; b/a tends to one. Combining two interior contributions and their neighboring inverse-square tails gives `2^(6/5) Cpl a^(-4/5) M^(-1/5)`, agreeing with the compact-wall lower bound.

The fold patch has exactly mass M and a fixed rescaled half-length B. With `r=M^(1/7)`, its differential operator scales as r fourth and its integrated quadratic form for an unamplified rescaled test scales as r fifth. Uniform Neumann coercivity follows by the stated constant-mode contradiction because no limiting quadratic-square potential vanishes identically. The integrated response is consequently of order r inverse-cubed. A fixed scaled margin beyond both possible roots bounds the outside reciprocal integral by the same order. The wording of the intermediate energy scale should be corrected as R1-02 below, but the response calculation itself is right.

In the rootless regime, the reciprocal-rate integral has order `|t|^(-3/2)`. The policy branches are Borel into L1: root positions, widths, and amplitudes vary continuously within the separated branch; translated/dilated compact continuous profiles are L1 continuous; fold-patch and uniform branches are Borel, with explicit assignments at thresholds and folds. All branches have exactly the per-realization budget.

### 5. Oracle averaging and constants

The stated integrable envelope follows in the central window from `M^(1/5-3/7)=M^(-8/35)` and `|t|<=L M^(2/7)`. On the rootless side, after dividing by `|t|^(-4/5)`, the remaining factor is `M^(1/5)|t|^(-7/10)`, uniformly bounded for `|t|>=L M^(2/7)`. Thus dominated convergence applies to the explicit policy on the entire offset interval.

For the converse, a sequence of Borel policies within one of the finite policy infimum exists by definition. The fixed-offset compact-wall theorem bounds every coefficient in that sequence. Fatou over `|c|<1` then proves the sharp lower mean without measurable selection of pointwise minimizers. This is sufficient to justify the stated policy optimum.

I recalculated the constants independently at 40-digit precision:

- `Cpl = 6.222823736019888609084577`.
- `Kobs = 22.40462823074913829298219`.
- `Kobs/K1 = 1.218565792934687373063461`.

The oracle/blind budget exponent is `1/4-1/5=1/20`. The fold layer contributes `M^(2/7) M^(-3/7)=M^(-1/7)`, lower order than the leading mean. All physical leading-value statements follow from the accepted same-budget transfer under fixed bulk diffusivity and nonzero mean velocity.

## Minor corrections

### R1-01 — Avoid asserting endpoint traces for the degenerate form domain

- **Severity:** minor mathematical terminology/clarification.
- **Location:** `sections/05-exact-observation.tex`, lines 252–255, particularly “permits independent traces of the half-supports and exterior.”
- **Reason:** Finite-energy elements need not possess finite endpoint traces. Near a linear zero, a cutoff of `v(x)=log(log(1/x))` has finite L2, reaction, and `int x|v'|^2` energy but diverges at the endpoint. The exterior domain where D=0 is L2 and has no general endpoint trace either. The correct conclusion from the transition construction is absence of a matching condition, or a direct decomposition into component form domains.
- **Remedy:** Replace the trace wording with a statement that the minimal closed form allows independent component restrictions with no endpoint matching condition. Briefly note that the displayed transitions first localize bounded form functions and that truncation extends this to arbitrary form-domain elements. This is the domain fact needed for the following positive-part comparison; no claim that traces exist is necessary.

### R1-02 — Distinguish operator and integrated form scaling in the fold patch

- **Severity:** minor.
- **Location:** `sections/05-exact-observation.tex`, lines 411–412: “The derivative energy has the same scale r^4.”
- **Reason:** With `D=r^6/(2B)` and `s-s0=rx`, the diffusion operator scales as r fourth, but the integrated derivative energy of an unamplified test is `r^5/(2B) int |v'|^2 dx`; the reaction energy likewise has factor r fifth. The final response scale r inverse-cubed is correct.
- **Remedy:** Say “the diffusion operator has the same scale r^4” or explicitly write the common r fifth factor in the rescaled integrated form and the r factor in its source. Retain the existing correct response conclusion.

## Source check and boundaries

I inspected the [institutional Alexandersen–Sigmund accepted manuscript](https://findresearcher.sdu.dk/ws/portalfiles/portal/191660127/ITherm2021_revised.pdf). Its metadata match the new reference, and its constant-temperature-gradient optimization precedent supports the limited attribution made here. The present section does not claim that the general gradient-saturation method is new. Broader novelty assessment remains assigned to the final literature stage.

No frozen build artifact was changed. This review found no mathematical reason to reopen a prior accepted result or to require a major-revision round on its own.

**Recommended disposition:** accept after the separate fixer addresses the two minor points and the coordinator verifies them. **No major issue found.**
