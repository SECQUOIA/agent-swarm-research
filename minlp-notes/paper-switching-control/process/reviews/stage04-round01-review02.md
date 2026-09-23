# Stage 4, round 1: independent review 02

## Verdict

**No major issue found. No valid minor correction identified.** The arbitrary-grid formula, all-length strict floor-history characterization, and exact five-, six-, and seven-cell results are supported by the manuscript's arguments and independent exact checks. The continuous consequences and published-source correction have the stated scope.

## Scope and files

Reviewed all of frozen `sections/08-finite-grid-one-switch.tex` and `sections/09-three-mode-floor-chambers.tex`, the relevant schedule/endpoint/compactness/minimax dependencies in sections 01–02, and the cited full-versus-one-sided distinctions. Inspected manuscript pages 32–40 and the relevant stage 4 checker interfaces and mathematical row constructions. Verified all 95 snapshot manifest hashes.

I did not read other current reviews or root/author assessments, confer with other reviewers, delegate, or change the manuscript or snapshot. All extra artifacts are under `verification/reviewer02/stage04-round01/`. The manuscript build and log-writing verification runner were executed on a relocated copy there.

## Mathematical review

### Arbitrary-grid one-switch formula

At `08-finite-grid-one-switch.tex:46–107`, the largest eligible final mass dominates every other final choice for a fixed initial mode and switch time: the last deficit and largest omitted mass cannot increase. Constants remain covered by endpoint switches. Both closed LP families are valid lower-bound witnesses. In particular, the all-initial-modes family need not impose `m_2<=E`; every feasible point already obstructs the relevant schedules.

The coverage argument correctly works with thresholds `T/3<E<F`, avoiding unjustified strict inequalities at a maximizing threshold. A zero first-eligible index would produce a constant schedule of error at most `E`, so the chosen indices are positive. At most two masses exceed `E`. The appropriate obstruction inequalities survive averaging modes 3 through n, and the finite family/compactness limit passes to a closed LP. The separate construction for `F=T/3` has the correct conserved sums and remains feasible at `a=b`, for `n=3`, and at endpoint equalities.

At `:109–127`, the two-large-modes elimination uses the monotonicity of the second mode's initial deficit to bound its allocation at the later cutoff. The two scalar bounds produce `H`. The proposed two-type witness conserves cumulative and terminal allocation, has nonnegative increments, and satisfies both cutoff conditions, including an empty final phase. Its other terminal masses do not exceed the two distinguished masses because `E>=T/3`.

At `:129–177`, averaging all modes other than the largest preserves initial obstructions, while reducing the possible final mass shifts its cutoff weakly later. This is sufficient for coverage even though the later relaxed family contains additional feasible cases. The subsequent one-distinguished-mode elimination is reversible. Its four lower and two upper mass endpoints, the independent feasibility inequality, and the two separate error inequalities yield exactly the displayed `L_ab`, `U_ab`, and admissibility test. The explicit `x,y` reconstruction satisfies both monotone cumulative chains, including `a=b`, `b=N`, and zero-length phases. It therefore constructs an actual relaxed control rather than only an algebraic LP point.

At `:178–181`, each candidate uses a fixed-depth rational expression in original grid endpoints and n. There are `O(N^2)` candidates, rational bit lengths remain polynomial, and comparisons can be exact. The statement explicitly promises a compressed two-component-type output; it does not incorrectly claim logarithmic-in-n cost for expanding n component functions. The assumptions exclude zero cell widths and the singular n=2 denominators. The N=1 formula gives the correct no-switch value `(n-1)T/n`.

### Unit-grid consequences

At `:185–239`, all residue branches have valid parameter ranges, including N=2 with an empty pure block and the separately treated N=1 case. The upper construction separates two masses above threshold from the remaining cases correctly; its use of k=0 selects an endpoint switch and remains valid. The lower controls force an error of at least the stated value for either an omitted large mass or a switch on either side of the cutoff. The corrections to N/3 are exactly 0, 1/6, and 1/12.

At `:241–285`, the five-mode/nine-cell example has the stated rates, masses, lower obstruction and independent upper guarantee. The uniform instance and three-mode minimax values used for comparison are the appropriate values on that same grid. The nonuniform counterexample specifically concerns an incomplete elimination rule; the text does not discard the admissibility inequalities when stating the final formula.

### All-N floor-history realization

At `09-three-mode-floor-chambers.tex:8–79`, nonintegral three-coordinate prefixes force the two fractional-sum states, and floor increments are coordinatewise zero or one. This yields the displayed four transition types. The node offsets enumerate precisely the three integer prefix counts allowed by error below one.

The new sufficiency argument is complete for arbitrary finite N. Each listed transition has an incoming and outgoing edge at every node, with the stated active labels. Every node therefore belongs to a complete path. Averaging all complete paths gives a simplex-valued relaxed control; each coordinate at every prefix attains both bounding integers among those paths, making the averaged coordinate strictly intermediate. Thus every generated history is a realizable strict chamber. No temporal compatibility constraint is missing. The recurrence counts histories, while the nine-entry switch recursion tracks the last active label separately from the count-node index. These roles are not conflated.

### Five and six cells; continuous two-switch boundary

At `:94–146`, the finite chamber enumeration is accompanied by a complete combinatorial generation rule and a separate full-word/floor-array check. The perturbation argument covers every integral-boundary profile: the auxiliary constant control has nonintegral coordinates at all relevant prefixes, and only finitely many parameters are forbidden for each nonconstant affine coordinate. Continuity of the minimum over finitely many grid words then gives an error bound of one. The suggested prime-denominator control extends this argument to arbitrary finite N.

The pure five-cell word forces every integer word of error below one to match its prefix counts exactly and hence use all its switches. This is a grid lower witness; it is not illicitly used as a continuous lower witness.

At `:148–174`, the continuous upper bound follows from grid domination for arbitrary measurable input. The alternative continuous lower witness `01201` has terminal masses `(2,2,1)`. Error below one forces all three modes to be selected and hence each to be used once under three blocks. For every possible final mode, its necessary early starting deadline contradicts its terminal service constraint. The matching word with switching times 2 and 4 has error exactly one. Thus `F_{3,2}(T)=T/5` is a full-error conclusion and does not conflict with the separate one-sided k=n obstruction.

At `:176–188`, the six-cell chamber distribution gives the claimed three-switch upper bound, and the alternating pure lower word forces five switches below error one. The same boundary/density argument applies.

### Exact seven-cell value and continuous three-switch band

At `:190–229`, every prefix coordinate of the explicit instance has fractional part 1/3 or 2/3. An integer outside its floor/ceiling pair therefore incurs at least 4/3. The displayed chamber minimum of four switches proves the lower bound under three allowed switches; the word `0011022` attains 4/3.

At `:233–280`, the six exceptional floor histories are identified as an exact orbit under mode permutations, rather than merely by equal cardinality. Each of the three repair words violates exactly one prefix-coordinate floor bound, and its counts there are zero. Its discrepancy is thus bounded by the corresponding actual cumulative allocation or one. Monotonicity and conservation imply that the three exceptional allocations sum to at most four, so at least one repair has error at most 4/3. This proves the universal upper bound in every exceptional chamber. Density and continuity cover boundaries, and endpoint averaging covers measurable inputs. The exact seven-cell statement follows.

At `:281–304`, the seven-cell value is correctly compared with the conjectured 3/2 bound and is not presented as a counterexample to it. The continuous upper bound uses the stronger six-cell transfer, not the seven-cell value. The pure word `0120011` proves the continuous lower bound: modes 0 and 1 each require separated early and late activations, since joining those occurrences would accumulate an error change greater than 2E over their inactive relaxed intervals. Mode 2 requires an additional activation. Thus fewer than five blocks cannot achieve error below one. The interval `T/7<=F_{3,3}(T)<=T/6` is expressly left as an interval.

### Published lower-bound correction

At `:306–326`, the article's Corollary 5 is transcribed accurately with its displayed parameter restrictions. The five-cell instance lies in that range and contradicts the claimed `8 Delta/7` lower bound with an exact value of `Delta`. Allowing the grid to vary while retaining horizon `5 Delta`, five cells, and maximum width `Delta` cannot avoid the contradiction because all five widths must then equal `Delta`.

The preceding Corollary 4 attainment argument does restrict N to the specified congruence family. The manuscript does not infer that the source supplies attainment at every N. It keeps the correction to Corollary 5 separate from Proposition 4's continuous lower bounds and from the previously discussed Conjecture 1 counterexamples.

## Fresh independent computations

### Full-grid LP families with exact certification

`verification/reviewer02/stage04-round01/grid_lp.py` imports no repository mathematical code. It independently assembles the two LP families using **all n mode coordinates at every grid endpoint**, without the three-component or three-phase compression. It separately implements the printed closed formula and its extremizer reconstruction.

For 30 grids with n=3,4,6 and N=1 through 5, including uniform and deterministic nonuniform rational grids, it evaluates every family and cutoff pair. SciPy only proposes solutions. Every feasible LP's primal variables and inequality dual multipliers are reconstructed as exact fractions; primal feasibility, multiplier signs, nonnegative dual residual, and equality of primal/dual values are checked exactly. For an infeasible family, an independently formed minimum-common-violation LP supplies a strictly positive exact dual lower bound, proving infeasibility.

The results are **82 exact feasible primal/dual certificates** and **338 exact infeasibility certificates**, covering all 420 programs in those grids. The maximum equals the closed formula in every case. The compressed extremizer reconstructed independently from the formula has that exact discrepancy under direct enumeration of all one-switch grid schedules, including constants and endpoint switches.

The same script checks all three-mode residue values through N=40, and directly evaluates the reconstructed witnesses through N=15. Results are in `grid-lp.log`. The numerical solver is a discovery aid only; none of these accepted LP values relies on a floating-point feasibility tolerance.

### Floor histories by full-word bitsets

`floors.py` uses **neither the transition graph nor its switch-count dynamic program**. It enumerates all 2,187 seven-cell words and forms exact bitsets for their integer prefix counts. At each prefix it tries every nonnegative floor triple with the two possible sums. A candidate history survives precisely when the remaining full words attain both bounding values in every coordinate at every prefix. This is the exact convex-average/prefix-flow characterization, implemented independently of the three-state recurrence.

It reproduces the total history counts `1,4,18,84,396,1872,8856` and the complete distributions:

- Five cells: `{0:3, 1:138, 2:255}`.
- Six cells: `{0:3, 1:255, 2:1377, 3:237}`.
- Seven cells: `{0:3, 1:414, 2:4542, 3:3891, 4:6}`.

It verifies equality of the six exceptional histories with the printed permutation orbit, checks every repair word's unique violated coordinate, directly computes the instance optimum 4/3 over all three-switch words, and confirms exactly 104 chamber words. Results are in `floors.log`.

## Source verification, portability, and presentation

Downloaded the final [Sager–Zeile article](https://doi.org/10.1007/s10589-020-00244-5) from the publisher and independently inspected printed pages 610–612. Its SHA-256 is `f4dfdfdc761de38dafeea5dd9eafb5bbf3c637a39dc7ee2ff1432a9803996770`, matching the recorded primary-source artifact. Corollary 4, Corollary 5, and Proposition 4 support the locators and distinctions described above. The continuous lower-bound construction on printed page 612 gives `0120011` at the stated seven-unit horizon. Source download and text are in this review's verification directory.

A clean build of the relocated frozen manuscript succeeds and produces 40 pages, with no unresolved references or overfull-box warnings in the final log. Pages 32–40 are readable and the displayed formulas/tables are not clipped. The relocated stage 4 runner passes all four exact checkers and validates the 25 bundled original-artifact hashes. Logs are `build.log` and `portable-checks.log`; `manifest.log` records all 95 matching frozen hashes. No log-writing runner or build was executed inside the immutable snapshot.

## Limitations

The sampled LP comparisons supplement the analytic all-grid elimination proof; they are not a proof by enumeration over all rational grids. The full-word floor enumeration is exhaustive through seven cells, while the all-N realization claim relies on the audited analytic path-averaging argument. No global exact continuous three-switch value is claimed beyond the proved interval. Comprehensive literature novelty, later algorithms, and final manuscript synthesis are intentionally outside this stage's scope.
