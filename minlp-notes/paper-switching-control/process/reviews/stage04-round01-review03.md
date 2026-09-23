# Independent review 03: stage 04, round 01

**Assessment:** No major or minor issue found. The arbitrary-grid formula, the all-N floor-history realization theorem, the five-/six-/seven-cell results, and the continuous consequences are sound. The primary-source correction is accurately scoped. I recommend accepting this stage.

## Scope and materials

I read `sections/08-finite-grid-one-switch.tex` and `sections/09-three-mode-floor-chambers.tex` in full, together with the required earlier definitions, endpoint monotonicity, grid domination, one-switch error identity, compactness, and integral-prefix-flow argument. I inspected all manuscript renderings on pages 32–40, the new verification programs, the compressed `minimax.py` implementation, stage README/runner/summary, and the source record. All **95 snapshot hashes** match.

I independently reconstructed the relevant mathematical checks rather than relying on the bundled logs. I also inspected the final published Sager–Zeile PDF directly on pages 610–612. Its SHA-256 digest matches the source record: `f4dfdfdc761de38dafeea5dd9eafb5bbf3c637a39dc7ee2ff1432a9803996770`.

I did not read other stage-4 reports or root/author assessments, confer with reviewers, delegate, or edit manuscript/snapshot files. All reviewer artifacts are in `verification/reviewer03/stage04-round01/`. The build and log-writing verification runner were executed only in a relocated copy under that directory.

## Findings

No correction requested. Later-stage algorithms, experiments, full literature synthesis, introduction, and abstract work are intentionally outside this review's acceptance scope.

## Mathematical assessment

### Arbitrary-grid LP families and complete coverage

**Locators:** section 08, `thm:finite-one`, `eq:grid-LP`.

The final-mode dominance reduction is correct for fixed initial mode and switch time: replacing the final mode by the largest terminal mass outside the initial mode reduces the final deficit and replaces a potentially larger omitted mass by a smaller one. Thus the listed orders cover the competing optimum, including constants through endpoint switch times.

Every feasible endpoint LP has monotone coordinates and the correct total increments, so interpolation produces an admissible relaxed control. When times coincide, coordinate monotonicity and zero total increment force identical states. The two cutoff intervals and the monotonicity of the initial deficit obstruct all relevant grid switch positions. The all-initial-modes family covers every dominating order; in the two-large-modes family, omitting either large mode already gives the required error. No unneeded mass-threshold restriction is imposed on the first family.

For the converse, E<F and E>T/3 correctly force positive first-eligible indices and at most two masses above E. The two cases m_2<=E and m_2>E provide exactly the displayed failure constraints. Averaging modes 3,...,n preserves each required constraint. Compactness and a fixed-family/index subsequence justify closing the inequalities at E=F. The explicit F=T/3 construction covers that boundary, including c=N and n=3.

### Elimination, symmetrization, and reconstruction

**Locators:** section 08, `eq:grid-H`, `eq:grid-M-interval`, `eq:grid-xy-reconstruct`, and `eq:grid-admissible`.

The two-large-modes family has the correct bounds E<=(T+B)/4 and E<=(T-Q)/2. Only the cell meeting T/3 can improve on T/3; equality at a grid endpoint does not create an additional larger value. The explicit H-witness has the right cumulative sums, ordered terminal masses, nonnegative rates, and cutoff inequalities. It attains H even when the last phase is empty.

When the remaining contribution is needed, averaging all modes except the largest preserves each averaged initial deficit. The averaged terminal mass cannot exceed the old second-largest mass, so the new eligible final cutoff moves only later. The initial deficit of mode 1 is nondecreasing, preserving its obstruction. This is the necessary justification for using only one distinguished mode in the remaining formula.

The scalar state inequalities in x,y,M are equivalent to monotonicity of both the distinguished coordinate and the repeated coordinate. The printed interval for M contains the constraints needed for an actual state reconstruction. The formulas for x and y give x<=A, x<=y<=M, y-x<=B-A, and B-y<=T-M, as well as both failure constraints. The eight lower-versus-upper comparisons reduce to the two automatic comparisons, the separate admissibility inequality, and the listed lower/upper error endpoints. Hence no omitted compatibility condition is hidden in the formula.

The cases a=b, b=N, N=1, and an empty set of admissible pairs are treated correctly. The closed formula uses a constant number of rational operations per pair and a constant-size component-type representation; its bit complexity is polynomial in the full grid encoding and log n. Expanding every mode's function would require linear output size in n, which is explicitly distinguished from the compressed complexity claim. The supplied implementation agrees with the printed rational formulas and uses no LP solver.

### Unit-grid residues and examples

**Locators:** section 08, `cor:three-unit-one`, `ex:five-nine`, and the nonuniform example.

The three-mode residues have the correct parameter ranges. The N=1 exception is necessary; N=2 is covered by k=0 in the 3k+2 branch. The upper proof's mass cases and cutoff choices work at equality and at a zero switch time. The explicit lower witnesses have the stated masses and initial deficits, including empty pure blocks when k=0. Their excesses above N/3 are 0, 1/6, and 1/12, respectively.

The five-mode nine-cell example has the correct cumulative allocations, masses, and cutoff obstructions; its independent upper argument covers both mass cases. The value 17/5 exceeds both comparison families as claimed. The nonuniform example demonstrates that the omitted feasibility conditions matter, and the complete formula yields the stated exact value.

### All-N floor-history realization

**Locators:** section 09, `prop:floor-automaton`, `eq:floor-transitions`, and `eq:floor-edge`.

For nonintegral three-mode prefix coordinates, the fractional-part sum is exactly 1 or 2. The possible integer count vectors are precisely the three displayed offsets. A cell's coordinate allocation lies in [0,1], so floor increments are binary; their sum gives exactly the four listed transition types.

I checked the explicit edge descriptions, including the asymmetric 1-to-1 and 2-to-2 cases and both arms of the 2-to-1 case. Every node has an incoming and outgoing edge at each permitted transition. Therefore every node at every layer belongs to a complete path, since all initial nodes are available and there is no final restriction. Averaging all complete integer paths is an admissible cellwise relaxed control. At each coordinate and prefix it includes both floor and ceiling counts with positive weight, so the average is strictly interior. This proves realizability for arbitrary N, not merely for the enumerated horizons.

The graph-word correspondence holds throughout the entire strict chamber: floor/ceiling membership is exactly the condition for integer discrepancy below one. Endpoint monotonicity then extends prefix control to the original continuous-in-cell objective. The cost recursion has the correct free initial activation and switch increment. The 2-by-2 history-count matrix has the correct transition multiplicities.

### Five and six cells; boundary passage

**Locators:** section 09, `thm:five-cells` and `cor:six-cells`.

The enumerations have complete mathematical coverage because all realizable histories were characterized first. The five-cell minimum-switch distribution is (3,138,255), and the six-cell distribution is (3,255,1377,237). I reproduced these with a complete-word method independent of the nine-state cost recursion.

The alternative 14,400-array test has a valid strict-feasibility criterion. Integral prefix-flow decomposition proves necessity of attaining both floor and ceiling among feasible integer words; averaging those words proves sufficiency. It is not merely a coincidental numerical agreement with the transition enumeration.

Perturbing toward the specified rational constant control avoids all integral prefix coordinates along a sequence tending to zero. The finite minimum over admissible integer words is continuous, so strict bounds pass to weak bounds at boundary inputs. The general prime-p construction also has nonintegral coordinates at every prefix up to N. The alternating pure lower witnesses force their entire integer word whenever the error is below one. Scaling and averaging cover the claimed cell widths and measurable inputs.

### Exact seven-cell value

**Locators:** section 09, `prop:seven-cell-instance`, `thm:seven-cells`, and `eq:seven-bad-floor`.

For the lower instance, every coordinate is one-third or two-thirds away from an integer. Leaving the floor/ceiling pair therefore incurs at least 4/3 error. Its chamber requires four switches; independently enumerating all 2,187 words gives exactly 104 chamber words and the same minimum. The printed three-switch witness has error exactly 4/3.

The complete seven-cell distribution is (3,414,4542,3891,6). The six exceptional histories equal the full mode-permutation orbit of the printed history, not merely a six-element set with a matching count. Each repair word has at most three switches and exactly the asserted single floor/ceiling violation: coordinate i at time i+2, with count zero. Every other coordinate/prefix error is below one throughout the strict chamber. Monotonicity and conservation bound the sum A_0(2)+A_1(3)+A_2(4) by four, so one repair word always has discrepancy at most 4/3. Generic perturbation covers boundaries. This is a complete upper proof matched by the explicit lower instance.

### Continuous consequences and source correction

**Locators:** section 09, `cor:three-two-continuous`, `eq:three-three-band`, and `eq:source-cor5`.

The continuous upper bounds T/5 and T/6 use the proved grid domination in the correct direction. For the T=5 lower witness 01201, error below one requires all three modes and hence exactly one block per mode. An unserved final mode forces its start before its first unit-mass time, while its terminal error forces that start strictly later than the displayed lower cutoff. These conditions are incompatible. The printed attaining word verifies error one.

For the T=7 witness 0120011, error below one forces early service of all three modes and later service of mode 0 in (3,5) and mode 1 in (5,7). A single spanning block of either mode would cause an error change exceeding 2E over its intervening inactive relaxed interval. Thus those two modes each need two activations, and mode 2 needs its own activation: at least five blocks. This proves the lower bound for three switches. The manuscript correctly leaves a band for F_{3,3}; it does not infer a continuous exact value from the seven-cell grid theorem.

The final published source on pp.610–612 confirms the printed statements. Corollary 4's attainment calculation uses the stated congruence class of N; Corollary 5 states its many-mode lower bound without that restriction. The five-cell exact value contradicts Corollary 5 as written, and fixing total horizon, cell count, and maximum cell width cannot remove that particular counterexample. Proposition 4 is a separate continuous lower bound and supplies the stated T/5 and T/7 instances. The manuscript attributes those existing lower bounds and does not claim a new general replacement for the incorrect finite-grid statement.

## Checks actually performed

1. **Independent complete-word floor audit:** `floor_independent.py` uses bitsets of all 3^N words and intersections of their prefix floor/ceiling compatibility sets. It does not import author code or use the nine-entry switch-cost DP. It reproduces all **11,124 histories** at N=5,6,7 and their exact switch distributions. For every history, every coordinate at every prefix attains both its floor and ceiling among full feasible words, independently checking strict realization. It verifies the exceptional orbit, all three repair words, the 104 chamber words, and the original-objective optimum 4/3. Results: `floor-results.json` and `floor-results.log`.
2. **Independent full-mode/full-cell LPs:** `grid_independent.py` retains every original mode and every cell allocation, with no component averaging in its LP variables. It solves **1,246 LPs** from both obstruction families across **65 unit/nonuniform rational grids**, n=3,...,8 and up to six cells. The maximum always agrees with the closed formula. These LP solves are numerical corroboration only.
3. **Exact original-objective witnesses:** The same independent program separately implements the printed closed formula and reconstructs its two-type extremizer using exact fractions. It enumerates every initial/final mode and every grid switch boundary, including constants, and verifies that the original maximum absolute discrepancy has the stated optimum. Both extremizer types occur in the tested grids (12 H cases and 53 U cases). It additionally checks every n=3 residue through N=30 and the two named nonuniform/many-mode examples. Results: `grid-results.json` and `grid-results.log`.
4. **Relocated bundled verification:** The stage-4 runner passes all four standard-library checks and all **25 bundled-original hashes**. Its checks cover 172 exact formula witnesses, all floor distributions through seven cells, the alternative exhaustive 14,400-array/243-word five-cell audit, and the printed lower/repair witnesses. Logs and regenerated summary are under `relocated/verification/stage04/`, with top-level output in `bundled-run.log`.
5. **Relocated build:** `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completes successfully and produces a 40-page manuscript. The final TeX log has no undefined references, warnings, or overfull/underfull diagnostics. I inspected all frozen renderings of pp.32–40. Build log: `build.log`.
6. **Primary source:** I checked the publisher PDF's hash and extracted/read pp.610–612 directly. The local extraction is `source-610-612.txt`.
7. All 95 immutable snapshot hashes pass.

## Limitations

Finite grid examples and floating-point LP comparisons supplement the analytic minimax proof; they do not prove it over arbitrary inputs or rational grids. The exact small-grid enumerations are computational proof dependencies, whose coverage and boundary arguments were separately reviewed above. I did not run the optional historical LP/MILP suite because I independently assembled the relevant LPs. I did not perform a new broad novelty search, extend the unresolved continuous three-switch band, or review intentionally pending stages. No claim of external peer review or eventual journal acceptance is made.
