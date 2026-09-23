# Independent review 03: stage 03, round 01

**Assessment:** No major mathematical issue found. One minor reproducibility issue concerns the ordering of rows addressed by the new chamber certificate. The general bounds, equal-mass instance band, necessary-event analysis, and single-chamber optimum are otherwise sound within their stated scopes.

## Scope and materials

I read all of `sections/06-general-budgets.tex` and `sections/07-predecessors-and-frontier.tex` in the immutable `process/snapshots/stage03-round01` snapshot, including their necessary earlier heavy-mode, uniform-input, exact-seed, and latest-reach dependencies. I inspected the complete new chronological checker, saved chamber data, historical event builder and witness, new-results checker, runner, verification README, and manifests. I independently rebuilt the new certificate system from the displayed equations and checked both the old witness and new primal/dual data.

I did not read another stage-3 review, communicate with another reviewer, use subagents, or modify manuscript/snapshot files. All reviewer code/results are under `verification/reviewer03/stage03-round01/`. All **71 snapshot hashes** and **19 bundled-origin hashes** match. Unchanged earlier certificate families were not rerun without a new reason.

## Finding

### R03-S3-01 — Minor: certificate row indices depend on unspecified set iteration

**Locators:** `verification/reference/general_reach_research.py:83`, `:89`, `:92`, `:102`, and `:107`; its use by `verification/stage03/check_chronological.py` when applying `inequality_dual`; the generic Python 3 portability statement in `verification/stage03/README.md`.

The new rational dual is addressed by row number, but the builder produces those row numbers through iteration over `frozenset` objects (`modes`, `available`, and `available - {i}`). Python does not specify their traversal order. The current CPython execution yields the expected order, and the certificate passes. The certificate's indexing nevertheless has an unstated interpreter/order dependency beyond the explicit event permutation and tie rule documented in the manuscript.

I tested the dependency without changing the mathematics: reversing only the `for i in available` traversal preserves the complete row multiset, variable coordinates, equality rows, and objective, but the unchanged indexed dual then has 67 negative residual coordinates, with minimum `-461877/104750`. This is recorded by `order_probe.py` and `order-probe-results.json`. It is a controlled alternative-order probe, **not** a claim that the provided checker fails on the current interpreter.

Use explicit sorted iteration everywhere traversal defines certificate row order, or give the chamber checker an equivalent deterministic row builder. The current certificate already passes my independently written builder using sorted integer tuples, so no mathematical change or new dual discovery is required. If the historical reference copy must remain byte-identical, a deterministic manuscript-local builder can preserve that provenance policy. At minimum, document/pin the implementation dependency, though deterministic ordering is the simpler robust outcome.

This is a minor portability issue, not an incorrect theorem: the printed system and the exact certificate check have been independently verified below.

## Mathematical assessment

### Mode removal and general coefficients

`lem:mode-removal` correctly separates maximum-mass and minimum-mass choices according to the sign of `1/(n-1)-C`. The constant-mode branch controls the entire one-sided discrepancy because t-A_q(t) is nondecreasing. In the nonconstant branch, the proof establishes both positive prefix length and positive residual budget before invoking the lower-dimensional construction. The completed rates are measurable and simplex-valued, and their discrepancy relative to the original input is bounded by the terminal removed mass. Appending the unused mode preserves distinctness. The argument is valid for C below the reciprocal mode count; clipping the transformed seed is unnecessary.

The fractional-linear transform, telescoping product, elementary coefficient, plateau factorization, and first-order asymptotic matching are algebraically correct. The mode-removal lemma gives an upper coefficient, not an exact minimax claim. The elementary coefficient's use for equal masses is justified by C>=1/n. The full minimax bounds use the proved heavy-mode reduction in its spare-mode range and the omitted-mode witness for the plateau.

`thm:seeded` retains the sign of the seed transform, keeps all denominators positive, and propagates a distinct-mode schedule. Its seed range implies m>=ell+1, as required by the exact seed theorems. The strict four-block improvement follows from the displayed seed gap and strict monotonicity of the transfer. The plateau integer test clears only positive denominators. The claims at (n,k)=(16,5), the two negative-transform diagonals, and the seed-dependent series have the stated scope. In particular, the second-order gap is not presented as an exact minimax expansion.

### All-light construction and the exact equal-mass instance band

**Locators:** `07-predecessors-and-frontier.tex:11` and `:45`.

The deterministic times t_j are increasing. At the next target endpoint, previously selected modes hold at most (j-1)E total allocation; averaging over the unused modes yields the required one-sided block-end inequality. The algebraic recurrence for t_j is exact. Earlier selected modes receive no more service, so their one-sided error cannot increase, while terminal mass bounds control the opposite sign. Truncation at T causes no gap in the induction.

At E=T/n, the condition to reach the full horizon reduces exactly to `(n-k)^2<=k`. Every schedule with at most k<n blocks omits at least one mode, and for **every** input in the equal-terminal-mass class that omitted mass is T/n. Thus the conclusion is the exact **instance** optimum T/n for every input in the band, not merely an extremal upper/lower pairing. The general boundary statements correctly use a strict heavy mass when n<=k and make no matching lower claim there.

The dimension-free strict inequality and supremum follow from the stated finite-n bound and the uniform limit. The coarse-slot network explanation also gives strict error less than one slot length: integer cumulative counts are either exactly equal to an integer allocation or differ from a noninteger allocation by strictly less than one. The analytic four-block predecessor, its gap, and the third-largest-mass sufficient condition are valid consequences of their earlier analytic seeds. No certificate-free claim accidentally invokes the four-block certificate theorem.

### General exclusion identity

**Locator:** `07-predecessors-and-frontier.tex:216`, `lem:general-exclusion`.

All available sets are large enough to contain the required distinct words. The assumption `M^{k-1}<L` makes the appended reaches uncapped; the latest-boundary identity therefore applies. Summing allocations of all modes except i and comparing A_i at the excluded and global events gives the first inequality with the correct signs. A maximizing (k-1)-word remains available outside its support S, so those excluded maxima equal the global maximum. This gives the displayed summed inequality.

Its coefficient of `M^{k-1}` is positive: n-k+1>=2 and `(k-1)/(n-2)<=1` in the stated range. Substitution of the two additional premises, together with `n(E+B_{k-2})=(n-1)B_{k-1}`, gives exactly `sum_i M_i^{k-1}>=nB_{k-1}`. The final assumed failure is strict at L and yields the contradiction. The text correctly identifies the weighted inequality as a missing premise at k=5 and both necessary induction components as unresolved for larger k. No preceding theorem relies on those missing premises.

### Six-mode necessary relaxation and old witness

**Locator:** `07-predecessors-and-frontier.tex:280`.

The event counts are correct: 42 pair events on available sets of sizes 3–6, and 22 triple events on sizes 4–6. Together with six roots and seven variables per event, this gives 454 variables.

Each printed row is necessary for actual uncapped events **with the specified smallest root and fixed maximizing pair/triple**. In particular, an event involving i reaches at least R_i, giving its allocation lower bound; appending i supplies the pair/triple complement inequality. Available-set and block-count inclusion cannot decrease maximal reach. A retained global maximizing word gives equality of its events. These are restrictions of a fixed case, not an exhaustive reduction over all possible maximizers.

The old rational assignment satisfies all 3,660 inequalities, 64 conservation equations, and nonnegativity, while attaining 40328/387<13104/125. The stated incomparable-event example has exactly the printed time gap 184/645 and allocation drop 4/645. Hence it is not generated by an admissible cumulative allocation. The manuscript correctly draws only a failure-of-implication conclusion about the necessary relaxation; it does not claim a counterexample to five-block reach. It also notes the missing condition that S support a globally maximizing four-word.

### Interpolation and its limits

**Locator:** `07-predecessors-and-frontier.tex:330`, `lem:event-interpolation`.

The interpolation statement is correct. Equal-time events must have identical allocations; events at zero have zero allocation by nonnegativity and conservation. Ordered positive-time differences are coordinatewise nonnegative and sum to the corresponding time difference, so each interpolating slope is simplex-valued and individually at most one. An arbitrary simplex-valued continuation extends the trajectory. Conversely, any cumulative trajectory is coordinatewise monotone. The following paragraph correctly distinguishes this trajectory interpolation property from the much stronger assertion that the stored variables equal latest roots and maximum-composition reaches. The lemma is not used to bridge that missing step.

### New single-chamber certificate

**Locator:** `07-predecessors-and-frontier.tex:357`, `prop:chronological-chamber`.

The fixed event permutation is exactly the witness-time sort with original event indices breaking ties. The 378 adjacent coordinate inequalities imply all coordinate chronological comparisons along that permutation, and conservation implies the corresponding time order. Equal-time ties remain permitted; the system does not freeze the witness's numerical times. The old witness has exactly 239 ordered-coordinate decreases and maximum drop 224/645.

For the dual, y<=0 gives the required minimization lower bound from Ax<=b. The nonnegative residual can be multiplied by x>=0 without reversing the conclusion. All residual coordinates actually vanish for the provided certificate, which is stronger than necessary. The rational bound is exactly 13104/125, with 254 nonzero dual rows.

The uniform primal has the correct actual reaches: R=6/5, pair reach 66/25, and triple reach 546/125. Every pair event precedes every triple event in the chosen permutation, and equal allocations within each level satisfy every chamber cut. It meets all original rows and the objective has 24 triple-time contributions. Thus the lower bound is attained. The final scope paragraph is accurate: this solves one closed chamber only and establishes neither all permutations nor the general higher-block theorem.

## Independent checks actually performed

All mathematical checks passed. Main code and results are under this reviewer's directory.

1. **Complete independent reconstruction of the six-mode system:** `independent.py` imports no repository code. It enumerates the events using sorted tuples, reconstructs every printed inequality/equality and the objective, and addresses the saved dual using a deterministic row ordering matching the current checker. It verifies the old witness directly, all 3,660 original inequalities, 64 equalities, and nonnegativity.
2. **Exact chronology audit:** The same program recomputes the explicit permutation and tie rule, checks the named nonphysical pair, counts all 239 decreases, verifies the largest drop, and appends all 378 chamber inequalities.
3. **Exact chamber dual and independently constructed primal:** All 4,038 inequality multipliers have the correct signs; all 454 residual coordinates satisfy the required sign; the exact lower bound is 13104/125. I construct the uniform primal from its mathematical formulas and verify all rows and its objective before comparing it to the saved primal. The complete result is in `results.json` and `results.log`.
4. **Symbolic formula checks:** `formulas_light.py` verifies the transfer/sign identity, transform recurrence, derivative, plateau and dimension-free factors, elementary/uniform asymptotic coefficients, all four seed expansions, exact four-block seed gap, analytic predecessor identity/gap, all-light time recurrence, and the general exclusion aggregate substitution. These are symbolic rational identities with symbolic n and k, not merely sampled parameter checks.
5. **612 direct rational all-light constructions:** Four nonconstant cyclic profiles for each n=2,...,18, every k<n, with exactly equal terminal masses. Errors are computed directly at the union of input knots and schedule endpoints. All satisfy the full prefix error bound. **148 cases** lie in the new exact-instance band, and every one reaches the full horizon with error exactly T/n.
6. **Controlled row-order probe:** `order_probe.py` changes only available-mode traversal in a local in-memory copy, verifies that the system's complete row multiset and coordinates are unchanged, and records the indexed dual's resulting failure. This supports the minor portability finding while preserving the frozen artifacts.
7. **Bundled new checks:** Both `stage03/check_new_results.py` and `stage03/check_chronological.py` pass when run directly with logs redirected to my own directory. The former checks 12,170 coefficient cases, 1,344 branch contracts, 314 formal seed series, 75 seeded construction samples spanning all three branches, and 171 light construction samples. The latter confirms the saved witness and chamber certificate.
8. All 71 snapshot hashes and 19 original-artifact hashes pass.

## Limitations

Finite schedule examples supplement the measurable-input arguments; they do not prove the universal bounds. My symbolic checks use SymPy, while the publication checker uses standard-library exact arithmetic. I did not rebuild the PDF, visually inspect every page, rerun unchanged earlier certificate families, search for additional literature, or solve the unproved general five-block inequality. The latter remains an explicitly scoped research question and is not a premise of any accepted theorem in these sections. The portability probe demonstrates a permitted ordering dependency, not an observed failure of today's CPython execution.
