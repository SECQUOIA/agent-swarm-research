# Stage 2, round 1: independent review 02

## Verdict and findings

**No major issue found. No valid minor correction identified.** The stage is suitable for acceptance on the scope reviewed. The new repeated-mode counterexample is supported by its analytic proof and by a stronger independent exact optimization described below. The four-block theorem is appropriately identified as computer-assisted; its analytic implications do not overstate what the certificates prove.

## Files and review scope

Reviewed the immutable `process/snapshots/stage02-round01` manuscript, especially all of `sections/03-heavy-and-reach.tex`, `sections/04-four-block-certificates.tex`, and `sections/05-small-budget-minimax.tex`. Rechecked the relevant stage 1 foundations, schedule class, endpoint lemma, attainment, uniform-input lower recurrence, and the changes to sections 01 and 02. Read the certificate checker `verification/reference/verify_general_four_block.py` against the displayed event relaxation and certificate identities, and read the supplement/README instructions. All 35 snapshot manifest hashes match.

Inspected the rendered new manuscript pages 9–20. The two stage 1 minor clarifications from my earlier review have been made. I did not read other reviewers' reports, consult other reviewers, spawn agents, or change manuscript files. I do not regard future abstract/literature synthesis or future general-budget sections as omissions from this stage.

## Analytic audit

### Heavy modes and one-sided reduction

- At `03-heavy-and-reach.tex:19–48`, the network has integer capacities and supplies, a feasible fractional assignment, and a bounded objective. Maximizing the heavy-mode terminal flow yields an integer optimum of at least two. The endpoint lemma legitimately extends the prefix error to measurable controls between unit boundaries.
- At `:50–103`, the first repeated prefix contains precisely one twice-used mode and otherwise distinct modes. The deadline definition uses the latest point of the allocation sublevel set, so equality and flat allocations are handled. The selected double interval brackets the deadline. The before/after deadline counting arguments are valid even at the endpoints and at tied deadlines. The revised prefix preserves the occupation multiset, which is the necessary condition for retaining the original suffix's discrepancies.
- At `:105–113`, extension to `(s+2)E`, scaling, and restriction preserve the heavy condition and do not increase the switch count. In particular `s=0` yields two adjacent identical slots, hence zero switches. There is no covert assumption `s<n`.
- At `:120–139`, the upper bound divides inputs according to a *strictly* heavy mass, leaving all equal-threshold masses in the case where positive discrepancy is automatic. Full-error domination of one-sided error gives the stated lower bound after taking minima and suprema. The omitted-mode input uses the separately stated assumption `k<n`. Repeated modes remain permitted in both optimizations.

### Reach and certificate foundations

- At `03-heavy-and-reach.tex:145–174`, feasible reach sets contain their start time; their latest endpoints give both equality at an uncapped endpoint and strict failure at the horizon. These facts remain correct when `H_i` has flat parts. An unused mode's service error is controlled at the block end, and earlier selected modes' one-sided errors cannot increase after their service ends.
- At `:176–209`, the largest/second-largest reach inequalities have the correct directions. Both uses of uncapped endpoint equality are valid under the assumed failure of all pairs. The coefficient of `x-y` is positive for the full stated range `n>=3`.
- At `:211–277`, the exclusion maxima are nonempty for `n>=4`. The estimates at the third-largest first reach, the excluded-pair inequality, and the summation over a maximizing pair correctly account for the two exceptional exclusions. The coefficient used to substitute the global pair lower bound is positive at `n=4` and thereafter. The final strict summed inequality contradicts `L<=B_3` without an equality-case gap.
- At `04-four-block-certificates.tex:59–118`, every displayed event row is a necessary consequence of the actual pair maxima, cumulative monotonicity, or allocation conservation. Reverse orders only apply when the chosen maximizing pair survives exclusion. Missing chronological constraints enlarge the feasible set, which is legitimate for this lower-bound certificate; no reconstruction of a control from an arbitrary LP point is claimed.
- At `:120–199`, the three positions of the maximizing pair relative to `S` and the distinguished-mode orbits cover all cases, including the absent tenth case at `n=5`. Averaging preserves feasibility and objective without assuming an optimizer. The orbit identifiers retain coincidence of interchangeable labels; in particular an excluded interchangeable mode and another interchangeable mode are not conflated. The stated maximum of three interchangeable indices per inequality row and at most six special labels supports stabilization at `n>=9`. The affine mass multiplicities and factored objective multiplicities justify reconstruction from dimensions 9 and 10.
- At `:201–256`, multiplier signs are correct for the `Ax<=b` convention. Zero coordinate residual proves the bound without requiring nonnegativity residual multipliers or dual optimality. The finite case count is correct. Positivity of the shifted denominator polynomial and nonpositivity of shifted inequality multipliers establish valid certificates for all integer `n>=23`; this is more than evaluation at sample dimensions.
- At `:260–300`, the analytic passage from weighted pairs to excluded triple reaches preserves all distinctness requirements. A maximizing triple remains available outside exactly its three labels. The substitution coefficient is positive at `n=5`, and the recurrence identity makes the bound exactly `nB_3`. Latest endpoints justify the final strict contradiction.

### Minimax values, refinements, and counterexamples

- At `05-small-budget-minimax.tex:7–75`, reach upper bounds are applied at the exact target threshold. The uniform-input lower recurrence is valid for every competitor, including repetitions and fewer than the nominal number of blocks. The equal-terminal-mass upper bound controls each sign separately and the uniform lower example belongs to the restricted class. The regime `n>=k+1` is stated throughout and is not extended to `k=n`.
- At `:77–118`, the listed equal-mass improvements and plateau transitions have the correct ranges. Both shifted sign polynomials and both asymptotic expansions were independently checked with symbolic algebra. The large-mode expressions are expansions of the full minimax because the relevant branch eventually dominates.
- At `:131–223`, the rational knots form an admissible cumulative allocation, with every coordinate slope at most `3/4`; thus the `H_i` are strictly increasing. Substitution at the printed knots verifies the first and pair reaches and all six distinct triples' common final reach. The uniform comparison uses a recurrence valid even at `k=n`, without applying a theorem restricted to `k<n`.
- The repeated-mode argument at `:183–215` is complete: terminal constraints eliminate every active set except `{0,1}` among schedules using at most two modes. Both orders `p,q,p`, allowing zero blocks, cover every schedule on that set with at most three blocks. The middle-service estimate `v-u<=A_q(M_2)+1=M_2-R_p` is valid because the middle mode is unused before `u`, `v<=M_2`, and allocation is nondecreasing. The two terminal lower bounds contradict it by exactly the stated positive rational gaps. Attainment is essential and correctly cited when concluding `OPT^-_3(A)>1` from infeasibility at one.
- At `:231–279`, both adjacent-pair examples concern the fixed unit-slot problem and are accurately confined to that setting. They do not claim that continuous schedules have the same restriction or that every choice of a largest heavy mode fails. Their terminal and prefix contradictions have the correct signs.

## Fresh independent checks

All new checks and outputs are under `verification/reviewer02/stage02-round01/`.

### Exact optimum of the three-mode counterexample

`independent_checks.py` constructs the piecewise-affine input directly from the printed knots and enumerates all 27 words in `{0,1,2}^3`. For each word it enumerates all 36 chronologically ordered pairs of closed switching-time segments, including coincident times. In each cell the original endpoint one-sided error conditions give a linear program in the two switch times and the error.

SciPy proposes an active basis; it is **not** trusted as a correctness oracle. Exact rational elimination reconstructs the primal solution and nonnegative dual multipliers. The program verifies every primal inequality, every dual sign, the dual coordinate identity, and equality of primal and dual objectives. Thus all 972 cell optima have exact lower and upper certificates, including degenerate cells. The union covers every schedule with at most three blocks, since zero-length blocks and repeated labels are explicitly included.

The independently established instance value is

`OPT^-_3(A) = 18673/18396 = 1.0150576212220048...`.

An optimal word is `021`, with switching times

`u = 8341/4599`, `v = 17639/4599`.

This is the only word in the enumeration attaining that minimum; uniqueness of the switching times is not claimed. The result is stronger than the manuscript's `>1` assertion and is reported as verification evidence, not a requested addition to this stage's theorem. Exact cell certificates are stored in `n3-exact-cell-certificates.json`; all word minima are in `n3-word-minima.json`. The main log is `checks.log`.

### Heavy rounding and algebra

The same independent program exhaustively checks all 1,296 three-mode/four-cell profiles whose cell rates are simplex-half points. Every profile has a heavy mode, and direct enumeration finds a full-error-one unit-slot word with an adjacent repetition. This check implements neither the flow nor the deadline reordering, so it supplies independent evidence for the observable conclusion.

The program also uses SymPy to expand the two shifted plateau polynomials and the two rational minimax expressions around inverse mode count zero. All displayed coefficients agree exactly. SciPy and SymPy are dependencies of this reviewer's extra checks only; they are not dependencies added to the manuscript's proof checker.

### Direct reach checks on actual controls

`reach_checks.py` builds fresh deterministic rational profiles for `n=5,6,10,30`, evaluates latest reach maps from the actual cumulative allocations, and directly forms pair-exclusion maxima. It checks 16,650 instances of the **strong** weighted-pair inequality, allowing every distinguished mode and multiple choices of the three-element set. The thresholds include `1/2`, `1`, and `2`. It also constructs the maximum distinct three- and four-block reaches using a mode-subset dynamic program for `n=5,6,10`, checking the analytic/certified reach constants. All pass; results are in `reach.log`.

### Published checker and artifact integrity

Reran the frozen all-dimension exact certificate checker as an additional check. It verifies all 179 finite and all 10 polynomial certificates. Output is retained in `certificates.log`. `manifest.log` records the 35 matching frozen hashes. These reruns supplement the direct manuscript audit and fresh checks above.

## Limitations

The new finite control searches do not prove the universal measurable-input statements; those rely on the audited analytic proofs and exact certificate reduction. I read the all-dimension checker and its mathematical construction, but did not implement a wholly independent second version of every quotient coefficient and polynomial certificate identity. No new external literature search was performed because source novelty and comprehensive literature positioning are explicitly deferred to the later synthesis stage. The exact instance value above should receive its own manuscript review if it is later promoted from verification evidence to a stated result.
