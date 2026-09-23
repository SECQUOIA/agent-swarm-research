# Independent review 01 — stage03-round01

**Verdict: no major or minor issues identified.** The new equal-mass result is valid as an instance identity for every input in its stated band. The general exclusion argument is explicitly conditional, and the chronological result proves only the specified chamber optimum.

## Scope

Read both complete new files, `sections/06-general-budgets.tex` and `sections/07-predecessors-and-frontier.tex`, and checked the accepted dependencies needed for them: heavy-mode rounding, the one-sided reduction, endpoint monotonicity, distinct-mode reach maps and their uncapped boundary identities, exact seeds, and scaling. Read the new stage checkers, the complete original event-relaxation builder and its witness verifier, and the chronological certificate checker. Inspected the stage verification README and a rendered new manuscript page.

No other stage-3 review was read. No manuscript or snapshot was edited, and no subagent was used. Executed the chronological checker only from a relocated copy beneath `verification/reviewer01/stage03-round01/`.

## Analytic audit

### Mode removal and arbitrary budgets

- **Lemma `lem:mode-removal`, lines 9–78:** The constant-mode branch directly bounds the negative discrepancy by `T-a`. In the maximum-mass branch, `E>=T/n` and the exclusion of the constant branch give strict positivity of `E-a/(n-1)`. The coefficient comparison is in the correct monotonic direction when `a>=T/n`. In the minimum-mass branch, `T/[n(n-1)]<E<T/n` and `a<=T/n` give positivity, and the same comparison reverses its monotonicity correctly. The constant branch is impossible there. At equality of the seed coefficient with `1/(n-1)`, both selections work; the proof separately covers the minimum-mass positivity and the maximum-mass constant boundary.
- The completed rates are a measurable simplex input on the positive prefix horizon. Bounding the completion discrepancy by the original removed mode's terminal mass is valid even though its mass on the prefix can be smaller. Appending the previously excluded mode controls its maximum negative discrepancy at the horizon and can only improve that sign for the others. Distinctness and the block count are preserved.
- The fractional-linear transform, its telescoping product, and inversion give the elementary coefficient on every stated spare-mode budget, including `k=1` and the zero-transform seed at two modes. Denominators are positive. The lower recurrence remains valid for repeated modes and the uniform schedule attains its one-sided coefficient. The positive-sign mass bound and heavy-mode reduction give the advertised unrestricted and equal-mass bounds.
- Checked the elementary plateau factorization, its endpoints, the `k=1` exception, the dimension-free strict bound, and the first-order asymptotic sandwich. None of these arguments assumes an unproved higher-block reach formula.

### Seed propagation and predecessors

The general seed formula permits a negative transformed seed and keeps its coefficient positive. The exact seed is used only in its established range `m>=ell+1`. Strict comparison with the elementary bound follows from the positive seed difference and strictly increasing transfer map. The equal-mass diagonal statements and the `(16,5)` plateau consequence have the right switch/block indexing. The integer plateau test clears a positive denominator and is correctly described as a sufficient criterion for the actual minimax. The second-order formulas describe gaps between bounds, not a determined minimax coefficient.

The analytic four-block predecessor is the correct one-step transfer of the analytic three-block seed. Its minimum-mass branch at five modes is necessary and explicitly included. The plateau and gap factorizations are correct. The third-largest-mass sufficient condition appends a mode unused by the pair schedule and bounds both signs. Its numerical example has terminal masses summing to one and improves the unrestricted guarantee without implying a new minimax value. The historical `V_n` expression is correctly presented as superseded, with a positive denominator in its stated range.

### All-light induction and the new instance identity

- **Lemma `lem:all-light`, lines 11–43:** The deterministic target times increase strictly below the mode count. Before step `j`, the allocations of the `j-1` previously selected modes are bounded by `(j-1)E` even at the next proposed endpoint. Averaging over the unused modes gives the stated bound. The algebraic target-time identity converts it into the required endpoint service inequality, including when the endpoint is capped by `T`. The selected mode is unused beforehand; earlier modes receive no further service. These facts bound the negative sign, while terminal masses independently bound the positive sign. Thus the induction reaches the precise displayed prefix with at most the permitted number of distinct blocks.
- **Corollary `cor:light-boundaries`, lines 45–80:** For `n<=k`, the average mass is strictly above the heavy threshold and no lower equality is claimed. For `k<n<=2k`, the all-light reach inequality is equivalent to the displayed dimension condition and matches the omitted-mode lower witness. For equal terminal masses, setting `E=T/n` gives exactly `k>=(n-k)^2`. Every input in that band admits an upper-bound schedule. Every competing schedule with at most `k<n` blocks omits a mode and therefore has error at least `T/n`, independently of temporal profile. This proves the claimed **instance** identity, rather than merely a worst-case equality. The boundary cases `k=1,n=2`, `n=k+1`, and the stated deficit diagonals are included correctly.

### General exclusion and the frontier

Under `M^{k-1}<L`, all lower-order events used by extension are uncapped. The available sets are large enough because `n>=k+1`. Appending a mode to each maximizing excluded word gives the stated coordinate bounds; summing and using allocation monotonicity gives the exclusion inequality. Outside a supporting maximizing set, that same word remains available, establishing equality of the relevant maxima. The aggregate coefficient is positive in the entire stated range. Substitution of the **additional** weighted premise and preceding reach bound yields the desired aggregate reach; the final summed failure inequality is strict by the latest-inverse convention. The text correctly distinguishes this conditional argument from a proof of its missing premise.

The failed relaxation's rows are necessary for physical uncapped events with the fixed root order and fixed maximizers. Its negative witness concerns the stronger arbitrary-set weighted inequality in the relaxation, rather than an actual control or the weaker maximizing-set premise. The explicit chronological allocation decrease makes that distinction concrete. The interpolation lemma is an exact characterization of common cumulative trajectories for the allocation events, but the text correctly notes that it does not identify those event times with inverse or maximum-composition reaches.

The strengthened chamber fixes only the permutation, not the numerical witness times. Adjacent coordinate inequalities and conservation imply all chronological comparisons in that chamber. The dual sign and nonnegative residual supply a valid lower bound on the nonnegative-variable LP. The uniform primal attains it because every pair event precedes every triple event in this specific permutation. The proposition and its following paragraphs consistently restrict the conclusion to one chamber and the fixed maximizers.

## Independent checks

All new artifacts are under `verification/reviewer01/stage03-round01/`.

1. **`check_constructions.py`:** Implemented cumulative evaluation, full direct discrepancy evaluation, greedy light rounding, and recursive mode removal independently, with exact rational arithmetic and no manuscript implementation imports. Tested 765 profile/budget cases from noncyclic balanced inputs for `n=2,...,18`. All reached the predicted prefix within the full error bound; 185 cases in the new equal-mass band reached the horizon with error exactly `T/n`. Tested 168 recursive constructions from analytic three-block seeds, covering minimum-mass, maximum-mass, and constant-mode branches. Every output used distinct modes, respected the block budget, and met its one-sided coefficient. Also checked the equality branch, including equality at the constant-mode threshold.
2. **`check_symbolic.py`:** Independently checked the transfer transform, elementary plateau factorization, dimension-free coefficient difference, all-light induction identity, all four symbolic seed transforms through cubic order, exact four-block seed difference, and analytic predecessor identities and shifted polynomials using symbolic algebra. All passed.
3. **`check_chamber_independent.py`:** Reconstructed the event LP from the manuscript's equation families, in a different order from the bundled builder. The independent multisets of all 3,660 inequalities and 64 equalities match the reference matrix exactly; the objective matches as well. Verified every original witness row, its objective `40328/387`, and the stated nonphysical time/allocation differences exactly.
4. The same script ran the relocated chronological checker after the independent matrix comparison. All 4,038 strengthened inequalities, 64 equalities, dual signs and coordinate residuals, exact lower bound `13104/125`, and matching uniform primal passed. The recomputed witness statistics are 239 chronological decreases with maximum `224/645`; there are 254 nonzero dual rows.

Finite construction tests corroborate the analytic measurable-input proofs. The chamber certificate check is exact arithmetic, and its matrix was independently compared with the mathematical row specification.

## Presentation and limitations

The new sections keep distinct the exact results, upper bounds, historical predecessors, sufficient conditions, and unresolved weighted premise. The inverse and optimization notation is consistent with the dependencies. No essential proof gap or severe readability issue was found.

I did not reassess global novelty, solve the remaining five-block problem, inspect every new PDF page visually, or rerun unchanged accepted four-block certificates. The symbolic review script uses SymPy as an independent checking aid; this is not a manuscript runtime dependency. The chamber verification uses a relocated copy and does not alter the frozen certificate.

## Required corrections

None identified.
