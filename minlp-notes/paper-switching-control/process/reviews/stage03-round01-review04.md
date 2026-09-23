# Stage 3, round 1: independent review 04

**Major-issue verdict: no major issue found.** The new mathematical results are supported by their proofs. The stronger equal-mass claim is valid for every input in its stated band. The chronological certificate establishes exactly the restricted relaxation result claimed; it does not establish the unresolved five-block reach theorem. I found one minor documentation inconsistency concerning advertised build logs.

## Scope

I read all of `sections/06-general-budgets.tex` and `sections/07-predecessors-and-frontier.tex` in the frozen `paper-switching-control/process/snapshots/stage03-round01/`, and revisited their relevant dependencies: measurable cumulative controls, endpoint monotonicity, distinct reach maps, uniform lower recurrence, universal heavy rounding, and the established two-, three-, and four-block seeds. I inspected the new verification README, `check_new_results.py`, `check_chronological.py`, the row builder and witness checker in `verification/reference/general_reach_research.py`, and the independent event verification in `check_seeded_review.py`. All 71 frozen manifest hashes match. I inspected the supplied final-page rendering.

No other review report was consulted. I did not edit the manuscript, frozen snapshot, or literature, or spawn agents. The planned literature synthesis and later topic sections were not treated as omissions.

## Finding

### R04-01 — Minor: the verification README advertises build logs absent from the frozen package

Locator: `verification/stage03/README.md:52–55` in the frozen snapshot.

The README says `build.log` and `final-build.log` record the initial and final builds. Neither file is present in the frozen `verification/stage03/` directory or its manifest. The neighboring `manuscript.txt` and images are present. This does not affect the mathematical or certificate verification, but a reader following the supplement's evidence description cannot inspect the advertised logs.

Correction: include the logs in the reviewable supplement, or qualify the description to say they are working-directory build outputs not included in frozen snapshots. Reproduction instructions and the proof dependencies need no change.

## Mathematical and scientific assessment

### Mode removal and general coefficients

Locator: `sections/06-general-budgets.tex`, Lemma `lem:mode-removal` and its proof.

The completion of the retained rates preserves the simplex constraint and measurability. The prefix's original one-sided error is bounded using the removed mode's terminal mass, while the appended removed mode has a monotone discrepancy ending at exactly `E`. The returned schedule uses distinct modes.

I checked both signs of the selection rule. For `C>=1/(n-1)`, choosing maximum mass supplies the correct direction in the affine mass inequality; the nonconstant branch gives positive `E'`. For `C<1/(n-1)`, minimum mass supplies the reversed selection direction and `E>T/[n(n-1)]` ensures `E'>0`. The constant-mode branch is impossible there. At equality, either selection is valid. None of these steps assumes piecewise-constant rates or an unstated lower bound on the seed coefficient.

The transformed recurrence and telescoping product yield the displayed elementary coefficient, including the zero-transform case. The one-sided, equal-mass, and unrestricted bounds use the correct input classes and switch/block indexing. The plateau factorization gives a sufficient interval rather than an asserted maximal one. The two asymptotic expansions and their first-order minimax consequence follow by squeezing; no exact general second-order minimax coefficient is claimed.

### Exact seeds and their consequences

Locator: `sections/06-general-budgets.tex`, subsection `subsec:seeded`.

The general transformed seed remains in `(-1,1)` throughout propagation, so denominators and coefficients stay positive. The negative seed values are retained, requiring the minimum-mass branch rather than a clipped formula. The strict four-block improvement follows from the positive seed gap and the strictly increasing transfer map. The text correctly notes that strict one-sided improvement may leave a full-error plateau unchanged.

The two negative-transform diagonals, the `(n,k)=(16,5)` plateau extension, the integer plateau test, and the seeded series have consistent algebra and parameter ranges. The result continues to disclose its four-block certificate dependency. Its second-order gap is explicitly a bound, not an exact asymptotic coefficient for the unresolved minimax. References to the later-in-this-stage light-input corollary are not circular: that corollary has a separate construction.

### All-light construction and the new equal-mass instance identity

Locator: `sections/07-predecessors-and-frontier.tex`, Lemma `lem:all-light` and Corollary `cor:light-boundaries`.

At the selected next endpoint, previously used modes have allocation at most `(j-1)E`; averaging over unused modes provides the required new mode. The recurrence identity and the capped endpoint have the correct inequality direction. The new mode's endpoint one-sided bound extends throughout its block, prior modes' one-sided errors cannot increase, and all positive errors are bounded by the mass hypothesis.

For `n<=k`, the heavy case always occurs at threshold `T/(k+1)` and yields only the upper bound claimed. For `k<n<=2k`, the all-light reach condition gives the matching upper bound, and the `k+1`-pure-mode input gives equality. The `k=1,n=2` endpoint is included correctly.

Most importantly, the equal-mass conclusion is genuinely an **instance identity**, not merely a worst-case identity. Setting `E=T/n` makes the reach condition exactly `(n-k)^2<=k`. Every competing schedule with at most `k<n` blocks omits a mode, whose terminal mass is `T/n` for every input in this class. Thus the upper and lower bounds apply to each input separately. The stated fixed-deficit examples follow immediately, with no claim of necessity outside the band.

### Dimension-free limit and analytic predecessors

Locator: `sections/07-predecessors-and-frontier.tex`, Proposition `prop:dimension-free` through Lemma `lem:third-mass` and its discussion.

The finite-mode upper bound is strictly below `T/k` in both regimes, while uniform input approaches that value as the mode count tends to infinity. The direct coarse-slot network explanation gives the same leading estimate; it is not used to bypass finite-mode analysis.

The certificate-free four-block coefficient is the analytic three-block seed propagated once. The minimum-mass branch at `n=5` is necessary and is explicitly used. Its plateau calculation and comparison with the exact certificate-based coefficient are correct. The superseded two-switch coefficient `V_n` is larger than the exact one-sided coefficient; the resulting full upper bound is therefore indeed subsumed. No superseded estimate is mistakenly presented as the final sharp answer.

The third-largest-mass lemma gives additional instance information: after a two-block prefix of length `T-m_(3)-E`, an unused member of the three largest modes can be appended. The stated condition is exactly what makes that prefix reachable. The nonpositive-prefix-length case is also handled, and the mass hypothesis bounds the other discrepancy sign. I checked the eight-mode example and independently constructed schedules for profiles with its specified masses; its guarantee is strictly below the unrestricted minimax coefficient.

### Exclusion identity and unresolved reach question

Locator: `sections/07-predecessors-and-frontier.tex:208–278`.

The generalized exclusion inequalities follow by appending an unused final mode and applying the uncapped boundary identities. A maximizing word survives exclusions outside its supporting set. The global coefficient is positive for `n>=k+1`; substituting the two stated premises gives the required aggregate lower bound and terminal contradiction.

For five blocks, the preceding four-block reach premise is already available in the uncapped situation. The missing weighted three-block premise is identified correctly, including the distinction between a maximizing four-mode set and an arbitrary four-element set. The manuscript does not use this missing premise in any proved result.

### Nonphysical event data and the chronological chamber

Locator: `sections/07-predecessors-and-frontier.tex:282–end`; `verification/stage03/check_chronological.py`.

I compared the listed necessary constraints to the bundled row constructor. The event sizes, counts, root constraints, endpoint inequalities, inclusion inequalities, fixed global maximizing pair/triple, and objective agree. The witness's allocation decrease between two increasing event times is an actual obstruction to interpolation by a cumulative control. The witness therefore disproves an implication of the relaxed inequalities, not a reach theorem. The possible absence of a maximizing four-word supported on `S` is separately disclosed.

The interpolation lemma is correct, including equal-time events and addition of the origin. Its conclusion is limited to interpolation of allocations; it does not enforce inverse-root or maximum-composition identities.

The new chamber order is reproducibly defined from the witness. Adjacent coordinate inequalities imply all chronological allocation comparisons by transitivity, and conservation orders the times. They do not fix the old numerical times. The certificate includes nonnegative residual multipliers through the condition `c-A^T y-Q^T z>=0`; together with `x>=0` and `y<=0`, this gives the claimed lower bound with the correct signs. The matching uniform-event point is feasible in this chamber and attains the objective. The exact value `13104/125` is consequently justified.

The stated scope is scientifically accurate: one chronological permutation, one specified global maximizing pattern, one mode count, and a relaxation which still need not encode actual reach identities. The general higher-block question remains open, with no unsupported extrapolation from the chamber calculation.

## Verification performed

Fresh checks and logs are under `paper-switching-control/verification/reviewer04/stage03-round01/`.

My `independent_checks.py` imports no manuscript verifier. It passed:

- 71 frozen manifest hashes;
- 192 nonconstant equal-mass profiles constructed as rational convex combinations of permutation profiles, including pure profiles, with independent light schedules reaching the full horizon and error exactly `T/n`; parameter cases include the new deficit-three regime;
- 100 independently constructed recursive schedules from the analytic three-block seed, exercising the minimum-mass, maximum-mass, and constant-mode branches, and checking errors directly at all relevant knots and block endpoints;
- 30 independent schedules for the third-largest-mass example, preserving its terminal masses under time-dependent perturbations.

I reran the frozen `check_new_results.py` and `check_chronological.py`; both passed. Their logs cover 12,170 seed-coefficient cases, 1,344 branch-contract cases, 314 formal-series checks, predecessor identities and plateau tests, additional rational constructions, the 3660-row original witness, and the complete 4038-row strengthened primal/dual certificate. The chamber log confirms 239 ordered-coordinate violations in the old witness, maximum decrease `224/645`, 254 nonzero dual rows, and exact optimum `13104/125`.

## Limitations

Finite construction tests supplement the analytic proofs over measurable controls; they do not replace them. I inspected the chronological row specification, checker, and exact dual argument but did not write a second complete certificate verifier. I did not rerun the unchanged four-block certificates, claim a global solution of the higher-block reach question, or conduct a new priority search. The sole requested correction is documentation of build-log availability, not a mathematical defect.
