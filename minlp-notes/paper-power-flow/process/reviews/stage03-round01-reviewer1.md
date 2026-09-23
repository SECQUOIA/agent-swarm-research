# Stage 3, round 1 — independent reviewer 1

**Verdict: major revision required. One major mathematical issue and one minor description issue.**

Reviewed the entire frozen stage-3 manuscript at `paper-power-flow/process/snapshots/stage03-round01`, its new checker, bibliography, abstract, and accepted dependencies. I did not read other reviewers' reports. Every snapshot hash matches. Structural, residual, separation-scale, certificate, and reactive-stability arguments pass my audit. The unrestricted rational-universality theorem is false, despite faithfully repeating the assertion of its cited preprint. The algebraic-degree theorem can survive after its source dependency is repaired.

## Required findings

### R1-3-1 — Major: rational universality must distinguish basic closed sets from arbitrary compact semialgebraic sets

**Locations:** `sections/05-algebraic.tex:11–35`, especially the statement at lines 13–16 and source invocation at lines 20–22. The same unsupported source theorem is invoked for the singleton/coordinate argument at lines 53–61. Update the abstract, coverage map, and later summaries wherever they depend on the unrestricted interpretation.

**Counterexample and reason.** Let

`S = { (x,y)∈[-1,1]² : x≥0 or y≥0 }`.

This is compact and defined over the rationals. It cannot be rationally equivalent, in the manuscript's sense of rational functions with denominators nonzero on their domains, to any basic closed set. Every resistive feasible voltage set is basic closed: all its defining constraints are weak polynomial inequalities.

Here is a self-contained local obstruction. Suppose `S` were rationally equivalent to a basic closed target `T`, via `F` and inverse `G`. Both `F` and `G∘F` are defined on an open neighborhood `V` of the origin, because their denominators are nonzero at the relevant points. On this neighborhood,

`S∩V = {x∈V : F(x)∈T and G(F(x))=x}`.

The reverse inclusion follows because `G` maps `T` into `S`. Clear rational denominators by positive squares and replace equalities by two weak inequalities. This makes `S` locally a finite conjunction `p_1≥0,…,p_h≥0` of polynomial inequalities.

But a neighborhood of the origin containing three quadrants and excluding the open lower-left quadrant is not such a conjunction. For each nonzero `p_j` with `p_j(0)=0`, let `h_j` be its lowest-degree nonzero homogeneous term. Nonnegativity of `p_j` on the three included open quadrants forces nonnegativity of `h_j` there. Its degree cannot be odd: the upper-left and lower-right quadrants are negatives of each other, so odd degree would force `h_j` to vanish on an open quadrant and thus identically. Its degree is therefore even. Consequently it is also nonnegative on the fourth quadrant, by negation symmetry. Choose a ray in the lower-left quadrant avoiding the zero sets of the finitely many nonzero `h_j`. Every such leading term is strictly positive on that ray. For sufficiently small positive radius all the `p_j` are positive there; constraints with positive constant term also hold, and identically zero constraints impose nothing. This contradicts the excluded quadrant.

There is a stronger global boundary, which root proposed during our exchange and I independently checked: compact rational equivalence to a basic closed set preserves basic closedness. For rational `F:S→T` and inverse `G`, retain all forward denominator polynomials and the uncancelled numerator polynomials obtained when inverse denominators are composed with `F`. These polynomials are nonzero on compact `S`, so their absolute values have a common positive rational lower bound `δ`. The conditions consisting of their squared lower bounds, `F(x)∈T`, and `G(F(x))=x` define exactly `S`; after positive denominator clearing they are a finite weak polynomial conjunction. This proves that the corrected basic-closed scope is sharp.

**Why the citation does not resolve this.** I inspected *Dynamic Toolbox for ETRINV*, Theorem 1 on p.3, Definition 5 on p.4, and the actual proof of Lemma A on pp.5–7, including the original PDF's equations. The theorem does print the broad claim, but its purported rational extension through disjunctions fails. For example, its step (3), followed by disjunction elimination, replaces `x≥0 or y≥0` by

`(x-u)(y-v)=0, u≥0, v≥0`.

At `x=-1/2, y=1/2`, setting `v=y` permits every `u≥0`. The projection is not one-to-one, and the proposed forward assignment `u=x` is not even feasible. Appending the box inequalities makes the source compact without fixing this failure. Thus this is an actual failure of the inherited proof, not a missing citation or a preference for more exposition. The [archived arXiv version](https://arxiv.org/html/1912.08674v1) contains the same issue.

**Required repair.** Establish rational universality for **compact basic closed semialgebraic sets** by a conjunction-only arithmetic construction. This still yields the singleton and designated-coordinate field conclusions, because an isolated real algebraic root with rational isolating endpoints is basic closed. State and prove a separate **semialgebraic-homeomorphism/topological** universality result for arbitrary compact semialgebraic sets if that breadth is retained. Do not call the latter rational equivalence.

Two possible ways to retain arbitrary topology are available, but one must be completed rather than merely asserted:

- Represent a compact semialgebraic set by a finite union of basic closed pieces and encode the resulting max/min evaluation by unique continuous auxiliary variables, obtaining a compact basic closed graph with a semialgebraic homeomorphism and coordinate-projection inverse.
- Use semialgebraic triangulation. An abstract finite simplicial complex has a rational basic closed realization in a standard simplex: nonnegative barycentric coordinates summing to one, with the product of coordinates indexed by each nonface constrained to zero. Triangulation preserves topology, not generally rational equivalence.

The source's downstream conjunction-only steps are discussed below. They retain a designated replacement coordinate of the form `εx_j+1`, so the field-degree assertion need not be weakened to a field generated jointly by all coordinates.

### R1-3-2 — Minor: state the actual incidence at the inversion bus D

**Location:** `sections/06-numerical.tex:66–67`.

The residual proof says “at D, including its two weighted x copies and one y copy.” Bus `D` has **one** complemented `x` copy with conductance two and one complemented `y` copy with conductance one. The other `x` copy is attached to `C_I`, not `D`. The displayed `ε+3δ` bound is correct; only the incidence description is wrong.

**Fix:** replace with “at D, including its x copy of weight two and its y copy of weight one,” or equivalent precise wording.

## Independent audit of the usable arithmetic-source chain

I did not assume that fixing the name of the input class repairs the cited source automatically. I read the original source's Lemmas C–G, pp.8–18, including the printed gate equations and Figures 2 and 3.

- A compact basic closed set has a conjunction of polynomial equalities and weak inequalities. For each polynomial inequality introduce its **unique polynomial value** as a variable, impose the defining equality globally, and require that variable nonnegative. All new variables are polynomial functions on a compact domain, so the extension is compact. This avoids Lemma A's problematic disjunction/strict-inequality step entirely.
- Lemma C builds constants and arithmetic circuits with unique polynomial values. Original coordinates are retained. Its inverse is coordinate projection.
- Lemma D uses one positive rational scaling `ε` and uniquely determined arithmetic constants/auxiliaries. A sufficiently small rational scale exists because the preceding solution set is compact; for an existence theorem one can choose such a scale directly rather than rely on a particular printed quantitative radius estimate. Original coordinates are recovered individually by division by `ε`.
- Lemma E shifts each scaled source coordinate to `εx+1`. Its addition and multiplication equations recover the old operations in both directions. The lower bound on the auxiliary `x+1/2` enforces a source constraint `x≥0` exactly. The other arithmetic auxiliaries are uniquely determined. There are minor source typos in its listed constant-term set: the constructed `x+3/4+Δ` has constant term `3/4+Δ`, not one of the four subsequently listed numbers. This intermediate still stays safely in `[1/2,2]` for the required small input range. A corrected proof should check actual expressions instead of repeating that list.
- Lemma F's multiplication-to-squaring diagram is algebraically sound and retains its input coordinates. With small centered inputs `x,y`, all intermediate values lie strictly inside `[1/2,2]`; the output is `(1+x)(1+y)`.
- Lemma G's reciprocal diagram is also algebraically sound. Its output is `(1+x)²`. Its finite auxiliary rational functions have nonzero denominators at `x=0` and values strictly between `1/2` and `2`, so a uniform sufficiently small rational neighborhood works. Every step is addition, inversion, or uniquely solvable rational scaling/shift, hence there is no sign-choice fiber. The printed Lemma 17 has an obvious coefficient typo (its definition of `α` repeats the denominator coefficients rather than numerator coefficients) and omits hypotheses needed for its most general displayed ratio bound. These defects are avoidable by directly checking the finite gate expressions and choosing a smaller input neighborhood; do not import the general estimate uncritically.

I wrote distinct exact Fraction diagnostics for these last two gate chains, checking 1,681 multiplication-to-squaring profiles and 41 square-to-inversion profiles, plus an explicit inactive-slack counterexample to Lemma A. These diagnostics supplement the algebra above; they do not establish a universal theorem by finite testing. The script and log are retained in my verification directory.

## Remaining theorem audit

**Section 4: PASS.** The three-equation arithmetic crossover really forces both transmitted values and its sum uniquely. Explicit `[1/2,2]` wire bounds and `[1,4]` local-sum bounds avoid confusing a bounded witness with a whole-solution-set bound. I checked the crossover and attribution against [Dobbins–Kleist–Miltzow–Rzążewski, Theorem 2.1](https://link.springer.com/article/10.1007/s00454-022-00381-0), including the exact three equations. The electrical realization with `C=9/2` gives the stated new pinned injections. Inversion solutions still have both operands in `[1/2,2]`, so the `W` bound is valid where it is needed. Cyclically ordered variable paths, duplicate strands, and three-leaf inversion trees give compatible planar embeddings even for repeated names. Connectors attach only to free-injection roots of degree at most two, preserve unique extension, and admit an exterior-face embedding. Positive internal voltages make zero-injection subdivisions exactly linear interpolation. Their effective conductances scale every old current by `1/(4L)`, and all old injection intervals receive the same factor. Even path lengths imply bipartiteness; simple cycles project to old simple cycles, giving girth at least `6L`. The graph restrictions hold simultaneously. No part of this section depends on the false general universality claim.

**Algebraic-degree conclusion: repairable, with no counterexample found.** The singleton is defined by a polynomial equality and rational isolating interval. The conjunction-only chain preserves a unique point, rational auxiliary functions, and one individually affinely recoverable coordinate. Thus each voltage lies in `Q(α)` and the designated root generates precisely that field. Planarization, connectors, and subdivision do not discard that root. Eisenstein gives the asserted every-degree examples. A one-bus rational example meets all graph conventions. AC magnitude uniqueness and reference-fixed rectangular uniqueness follow from the previously accepted exact transfers. The proof must invoke a valid conjunction-only result, as required by R1-3-1.

**Residual transfer: PASS after the minor wording correction.** The canonical extension is well-defined on the entire ordinary source box. Its only nonzero fixed-injection residuals are the source addition residuals and `|y−1/x|≤2|xy−1|`. Reverse copy errors accumulate over at most `6m` extensions. The bounds `|v_I−x|≤ε+δ`, `|v_W−h(v_I)|≤2ε`, and `|h'|≤2` give the printed coefficient `10(6m+1)`. The argument is pointwise before minimization and handles `m=0`.

**Tiny infeasible family: PASS.** Its exact recurrence is `δ_{j+1}=δ_j²/(1+δ_j)`, equivalently `d_{j+1}=d_j(d_j+1)` from `d_0=2`. All auxiliary source values stay within `[1/2,2]`. Only the final inversion bus has nonzero residual in the canonical extension, exactly `1/(d_k+1)`. The formula is nonetheless infeasible, and compactness makes the minimum positive. Variable/equation counts give the displayed bus/line bounds, and its incidence graph is connected. The rational witness itself may have exponentially many bits; the theorem does not claim otherwise. The discussion correctly identifies an accuracy-threshold limitation, not an exact-algorithm lower bound.

**Jeronimo–Perrucci–Tsigaridas application: PASS.** I checked the exact bound and hypotheses in the archived original PDF, Theorem 1 on p.2 and the dimension convention on p.3. The manuscript cites the corresponding journal numbering. The epigraph-with-cap has dimension `q=n+1≥2`, exactly `4n+2` weak polynomial inequalities, degree at most two, rational coefficients that can be independently cleared, and integer objective `t`. It is nonempty, compact, and connected because its entire top face is present. Thus it itself is the compact connected component required by the source theorem. Substituting degree two gives exponent `q4^q` and base `2^(4−q/2) Htilde 2^q`; the manuscript's logarithmic estimate is conservative and correct. Fixed data plus bounded degree make the coefficient bound constant; the dependence on `n` in `Htilde` is accounted for. The tiny family has linearly many buses, supporting the claimed matching exponential scale in `n`.

**Promised approximate certificates: PASS.** The displayed derivative bounds give a valid `4UD` sup-norm Lipschitz constant. Mesh rounding and clamping preserve arbitrary rational singleton bounds and give polynomial-length rational coordinates with residual at most `ε/2`. The same rational threshold yields soundness for promised no cases `γ_G>ε`. Empty networks and edgeless positive-dimensional boxes cause no exception. The text correctly avoids concluding exact NP membership or solving an unpromised sharp-threshold problem.

**Reactive stability: PASS.** For centered real angles, energy gives `(2/π)ℓ² s≤−θᵀq≤sqrt(s/λ₂)||q||`. This yields the angle and active discrepancy bounds with the printed constants. Replacing `2/π` by `1/2` gives rational constants two in both bounds. The all-pairs path argument gives `λ₂≥2g_min/(n−1)²`. Substituting the ordinary gadget bounds `ℓ=1/2`, `U=4`, `g_min≥1` produces exactly `256 n(n−1)² η²`. Componentwise application and isolated vertices are correctly handled. The result requires the real lift and exact voltage box and does not suppress principal winding or prove symmetric-tolerance hardness.

## Build and checker scope

The isolated `latexmk` build succeeds, with no warnings in the final LaTeX log. The development checker passes all reported crossover, inversion, connector, subdivision, perturbed-profile, tiny-family, and rational Poincaré/Lipschitz checks. I inspected its implementation: its structural checks do not purport to certify arbitrary planarization or universal topology. It explicitly says that finite checks do not replace proofs. The false universality theorem is outside what those finite checks could establish, so the successful run does not mitigate R1-3-1.

Artifacts: `paper-power-flow/verification/reviewer1/stage03-round01/` contains the hash check, isolated build, new-check output, extracted downstream primary-source pages, and independent source-gate diagnostics.
