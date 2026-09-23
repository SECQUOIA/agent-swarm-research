# Stage 3, round 1: independent review 02

## Verdict

**No major issue found.** One valid minor prose correction is identified below. All audited mathematical claims, including the instance-level equal-mass identity, negative seed transforms, and the single-chamber certificate, are supported within their stated ranges.

## Scope and files

Reviewed all of `sections/06-general-budgets.tex` and `sections/07-predecessors-and-frontier.tex` in the immutable `process/snapshots/stage03-round01` tree. Revisited the needed definitions, attainment, endpoint monotonicity, uniform lower recurrence, heavy-mode reduction, and distinct reach seed results in sections 01–05. Also reviewed the expanded exact three-mode instance proof in section 05, which now gives the value independently found in my earlier stage review. Inspected the stage 3 rendered contact sheets/pages 21–32, the verification README, the chamber checker, the original event-relaxation row builder, and the chamber certificate's interface. All 71 frozen file hashes match.

I did not consult other reviewers or their reports, spawn agents, or change manuscript content. Extra scripts and outputs are confined to `verification/reviewer02/stage03-round01/`. The mathematical proof review and fresh checks below were performed independently of the author's success logs.

## Finding

### Minor R02-01: Remove internal review-process language from the article

**Locator:** `sections/07-predecessors-and-frontier.tex:68–70`.

The phrase “the accepted small-budget theorems already cover them” refers to the project's internal review state. A journal reader has no reason to interpret “accepted” in that sense, and the text should identify the mathematical result instead.

**Correction:** Replace this with an explicit reference to `Theorem~\ref{thm:small-full}` or “the preceding small-budget theorems.” No mathematical change is required.

## Mathematical assessment

### Mode removal and every branch contract

At `06-general-budgets.tex:9–78`, the lower-dimensional hypothesis is a guarantee over every positive horizon and every input, so it applies to the completed prefix on `[0,L]`. The completed rates remain measurable and simplex-valued. Appending the removed mode preserves distinctness, and the one-sided discrepancy of each previously used mode cannot grow afterward.

The sign identity correctly determines the mass choice. If `C>=1/(n-1)`, selecting a largest terminal mass makes the affine bound nonincreasing in the removed mass; the nonconstant branch gives `a<T-E<=(n-1)E`, hence `E'>0`. If `C<1/(n-1)`, selecting a smallest mass reverses the necessary monotonic comparison. Here `E>T/[n(n-1)]`, `E<T/n`, and `a<=T/n` prove positivity of `E'` and rule out the constant branch. At equality both mass choices satisfy the contract. The constant branch is proved using its actual one-sided discrepancy and requires no omitted-mode full-error bound. The subsequent full-error claims invoke the heavy-mode theorem or a mass qualification explicitly, so they do not confuse the signs.

At `:80–120`, the fractional-linear transform, its inverse, and the factor `(j-2)/j` are correct. The elementary seed at two modes is handled despite its zero transform. Negative transformed seeds remain in `(-1,0)` under propagation and yield positive coefficients below `1/n`; no clipping is necessary.

### Elementary and seeded coefficients

At `:122–211`, the lower bounds use uniform input but allow repeated-mode competitors. Equal-mass and unrestricted classes are distinguished correctly. The elementary plateau factorization has a positive denominator throughout its stated range, and the interval is expressly sufficient rather than maximal. The asymptotic squeeze is valid because the uniform term eventually exceeds the omitted-mode threshold and `1/n`.

At `:215–265`, the general seed formula follows from the telescoping transform. It includes `n=m`, and its coefficient and denominator remain positive for either sign of the seed transform. The exact seeds are applied only when `m>=ell+1`, as required. The derivative of the transfer map is strictly positive for every step, so strict improvement over the elementary four-block seed survives propagation. This strict comparison is carefully limited to the one-sided coefficients; plateau maxima may agree.

At `:267–308`, the fourth-power transform is negative precisely at seed dimensions 5 and 6, yielding the two stated diagonal full-error conclusions for equal masses. The broader all-light result is correctly acknowledged. The value `C*_{16,5}=588449/3544816` lies strictly below `1/6`, while `C_{16,5}=35/208` is above it. The integer plateau test is exactly equivalent to this seeded upper coefficient being at most `1/(k+1)`, since all denominators cleared are positive. The text does not mistake that equivalence for a complete characterization of the true minimax plateau.

At `:310–344`, the formal expansions and the seed-dependent gap are correct for each `ell=1,2,3,4`, with fixed integer `k>=ell`. The case `k=ell` has identically zero gap. The result explicitly bounds an unresolved second-order term instead of claiming an exact second-order minimax expansion.

### The equal-mass instance identity and boundary regimes

At `07-predecessors-and-frontier.tex:11–43`, the all-light construction is sound even when some cumulative coordinates are flat, terminal masses equal the threshold, or the target is truncated at the horizon. The induction uses precisely timed endpoints, picks an unused mode by allocation averaging, controls that mode's negative discrepancy at the endpoint, and bounds every positive discrepancy by the terminal mass. The recurrence identity and its inequality for `u<=t_j` have the correct directions.

At `:45–80`, the consequence is indeed an **instance identity for every equal-terminal-mass input**, not merely a minimax identity. With `E=T/n` and `d=n-k`, the reaching condition is exactly `k>=d^2`. Every competing schedule with at most `k<n` blocks, including one with repetitions, omits a mode of mass `T/n`. This gives the same lower bound for each individual input and matches the constructive upper bound. The specified examples of the band (`d=2,k>=4`; `d=3,k>=9`) are correct. The `n<=k` statement is only an upper bound, as expressly stated, and the separate range `k<n<=2k` has a valid omitted-mode witness.

At `:82–106`, the finite-mode strict dimension-free bound follows from a strictly positive rational difference or the heavy boundary bound; the limiting lower coefficient gives the supremum. The supplementary prefix-flow interpretation does not interchange a pointwise strict inequality with an unjustified supremum claim.

### Analytic predecessors and structural question

At `:108–157`, the certificate-free four-block upper bound is the one-step propagation of the analytic three-block seed. Its minimum-mass branch at `n=5` and maximum-mass branch thereafter are correct. Its sign polynomial gives exactly the stated plateau range, and the comparison with the certificate-based exact coefficient is scoped correctly.

At `:159–197`, the third-largest-mass condition handles both `L<=0` and `L>0`. Two distinct prefix modes leave at least one of the three selected terminal masses available for the final block. The eight-mode example has the stated terminal sum and error coefficient. The superseded global coefficient is retained as a larger bound, without being mistaken for the sharp value.

At `:208–278`, all exclusion maxima used are nonempty under `n>=k+1`. Assuming the global `(k-1)` reach is uncapped ensures the smaller events are uncapped too. The general exclusion inequality follows by the same valid monotonicity and conservation argument as the low-budget cases. The coefficient multiplying the global maximum is positive even at the boundary `n=k+1`. The weighted inequality is stated as an additional premise, and the discussion correctly isolates its missing justification for five blocks.

At `:282–355`, the original relaxation rows are necessary under the fixed maximizers and minimum first-root labeling. Its witness violates actual chronological monotonicity between incomparable events, so it cannot represent a cumulative control. The interpolation lemma treats equal-time events correctly and proves exactly trajectory interpolation, not inverse or maximum-reach identities.

At `:357–409`, fixing the saved witness's event permutation defines one closed chamber, not all possible chronological orders. The uniform point has all pair events before triple events and is feasible in this chamber. The dual convention `Ax<=b`, `y<=0`, and nonnegative residual is correct. The resulting exact minimum is confined to this one permutation and these prescribed maximizers, as required. It does not imply the open five-block theorem.

### Expanded exact three-mode instance proof

The new proof in `05-small-budget-minimax.tex:187–296` independently supports the exact value `18673/18396`. The inverse is globally 4-Lipschitz including capped endpoints; the first/pair threshold perturbations are bounded by `4 delta` and `20 delta`. The uniform suffix supplies the final factor `3/2`. The word `021` reaches equality inside the two stated slope-`1/4` intervals. Repeated-mode schedules remain excluded even at the claimed optimum because both indispensable masses exceed twice the threshold and both middle-service gaps stay positive. The scaling to `37346/262143` is correct and is expressly a lower bound on the minimax, not its exact determination.

## Fresh independent checks and artifacts

### Recursive schedules and transfer contracts

`independent_construct.py` imports no repository code. It implements exact cumulative evaluation, distinct-seed reach search, rate completion, recursive mode removal, and direct discrepancy evaluation at all switch and input breakpoints.

It constructs **792** schedules across dimensions 3–9, every spare-mode block budget in that range, and every applicable seed `ell<=4`. Profiles include uniform rates, changing pure modes, a constant pure mode, and deterministic sparse rational rates on a nonuniform three-cell partition. Every coefficient equals the closed formula; every schedule satisfies its one-sided bound, distinctness, continuity of block endpoints, and block budget. All applicable full-error mass qualifications also pass.

The tests include **176** schedules whose coefficient is below `1/n`. Across recursive levels they check **1,240** positive-prefix contracts and **136** constant-mode branches, using maximum-mass selection 764 times, minimum-mass selection 416 times, equality/maximum selection 84 times, and equality/minimum selection 112 times. Every positive-prefix case checks `L>0`, `E'>0`, and `CL<=E'` exactly.

The same program builds **84 nonuniform equal-mass profiles** from rational convex combinations of permutation matrices, including `(n,k)=(6,4),(12,9),(20,16)`. It implements the printed all-light schedule directly and obtains full error exactly `T/n` for every profile, consistent with the universal omitted-mode lower bound. Results are in `construct.log`.

### Algebra with symbolic block count

`algebra.py` verifies the transfer derivative and elementary plateau factorization symbolically. For each `ell=1,2,3,4`, it keeps `k` symbolic, cancels the exact factor of inverse mode count in the transformed rational expression, and performs coefficient division through second order. Every seed-series and gap coefficient agrees with the manuscript for symbolic `k`.

It also checks **2,926** exact rational parameter pairs through dimension 80 for strict improvement, seed-transform sign, and equivalence of the integer plateau criterion to the coefficient inequality. It checks the displayed `(16,5)` fractions and the failure of this seed test at `(17,5)`. Results are in `algebra.log`. SymPy is a dependency of this extra reviewer check only.

### Independent reconstruction of the chamber constraints

`chamber_independent.py` rebuilds event variables and every original inequality directly from the manuscript's set-based specification, using a different row order. It confirms equality of the row multisets with all **3,660** original inequalities and **64** conservation equalities, independently reconstructs the objective and the saved permutation, and appends the **378** chamber rows.

The reference builder is used only to translate the saved dual row numbers into sparse row keys. The bound is then verified against independently reconstructed row vectors: dual signs, the nonnegative coordinate residual, the exact objective `13104/125`, every primal row, and primal/dual equality all pass. This checks the single-chamber inference beyond merely rerunning the author's checker. Results are in `chamber-independent.log`.

The original exact chamber checker also passes; its separate output in `chamber.log` confirms the 239 chronological decreases, maximum drop `224/645`, 254 nonzero dual rows, and the explicit uniform primal. `manifest.log` records the 71 matching frozen hashes.

## Limitations

Finite profile tests supplement the analytic all-measurable-input proofs; they do not prove them by enumeration. The chamber's dual data are supplied artifacts, although their exact identities and the underlying row set were independently checked. No global chronological-order enumeration or proof of the open five-block reach question was attempted in this review. No external novelty search was performed; comprehensive literature synthesis and later finite-grid/algorithm material are intentionally outside this stage.
