# Independent review 03: stage 02, round 02

**Assessment:** No major or minor issue found. The new exact instance optimum is proved analytically, with correct treatment of capped inverses and repeated schedules. I recommend accepting the revised stage.

## Scope and change audit

I compared the immutable `stage02-round02` snapshot against `stage02-round01`, then read the complete revised Proposition `prop:three-mode-failure`, its surrounding conclusions, and all mathematical dependencies needed for its proof. I also examined the change in `sections/04-four-block-certificates.tex`, the updated `verification/stage02/check_new_results.py`, and the README descriptions. I inspected the rendered correction pages 18 and 20. I did not read other round-2 reports, discuss findings with other reviewers, use subagents, or edit manuscript/snapshot files.

All **40 snapshot hashes** match. The general four-block checker and certificate data are byte-identical to round 1. Its mathematical reduction is unchanged except that the quoted quotient-size range is now explicitly restricted to n>=9; that qualification is correct. I did not unnecessarily rerun those unchanged certificates. The new proposition depends on the existing definition of one-sided error, endpoint monotonicity, distinct-word reach monotonicity, and scaling; those dependencies remain applicable at n=k=3. It does not invoke the spare-mode minimax theorem outside its range.

## Findings

None. The following points were checked explicitly and do not require correction.

### Capped-inverse sensitivity

**Locator:** `sections/05-small-budget-minimax.tex:194`, through line 215.

The knot slopes and uniform suffix imply `H_i(t)-H_i(u) >= (t-u)/4` globally, including intervals crossing knots. The inverse is well-defined for all y>=0 because H_i(0)=0, and strict increase gives the claimed root identity whenever the inverse is below L. If two inverse values are strictly ordered, the lower is uncapped; the upper may be capped, but its H-value is still at most its argument. Thus the 4-Lipschitz proof is valid at the cap and at y=0 as well as in segment interiors.

Increasing E from 1 to 1+delta perturbs the first reach by at most 4 delta. A pair's second inverse argument increases by at most 5 delta, giving the printed 20 delta bound. Each threshold-one ordered pair has the same baseline M_i when its omitted mode is i. The last-mode threshold at L is exactly `M_i+1+21 delta_*`. Therefore every distinct triple fails when delta<delta_*. This is a uniform analytic bound over the entire interval, not an extrapolation from three sampled thresholds in the checker.

The alternative last-reach bound also follows: the threshold-one final inverse value is t_*, its argument cannot decrease as E increases, and on the uniform suffix its slope is 3/2 until the cap. Multiplying the 21 delta argument bound by 3/2 gives `(63/2) delta`.

### Exact attaining schedule

**Locator:** `sections/05-small-budget-minimax.tex:217`, equations `eq:n3-exact-optimum` and `eq:n3-optimal-times`.

The first slope-1/4 interval for H_0 begins at R_0, and the relevant slope-1/4 interval for H_2 begins at M_1. The printed u_* and v_* lie inside those intervals. Exact substitution gives

- `H_0(u_*)=E_*`,
- `H_2(v_*)=u_*+E_*`,
- `H_1(L)=v_*+E_*`.

These are precisely the three active-mode block-end constraints for word (0,2,1). Other modes have nonpositive occupation-minus-allocation before selection, and their discrepancy cannot increase after their block. Endpoint monotonicity therefore proves the schedule's full one-sided error is E_*. The interval locations, rational times, error fraction, and suffix-length relation all check exactly.

### Repeated schedules and shorter words

**Locator:** `sections/05-small-budget-minimax.tex:231`, through line 273.

Both m_0 and m_1 exceed 2E_*. Terminal mass conservation forces any schedule using at most two modes at error E_* to use both 0 and 1. This correctly eliminates every other support, including single-mode schedules. Every remaining word with at most three blocks can be represented as p,q,p with zero-length blocks permitted.

The first two block constraints use the fact that q is unused before its middle block; they do not claim that a greedy method solves the repeated word. They bound v by `M_2+20 delta_*`. The bound is below L. Monotonicity and the global 3/4 allocation slope bound give
`A_q(v) <= A_q(M_2)+15 delta_*`, even when v happens to be less than M_2. Adding the error threshold gives the printed 16 delta_* service increase. Meanwhile the terminal requirement loses only delta_*. The two margins are exactly 2923/4599 and 4372/4599, both positive.

Hence repeated schedules are infeasible even at E_* and therefore below it. The distinct argument excludes [1,E_*), while infeasibility at one excludes every lower threshold. Together with the attaining word, this proves the exact instance optimum over **all** at-most-three-block schedules.

### Minimax implication and computational claims

**Locator:** `sections/05-small-budget-minimax.tex:283` and updated README.

Dividing E_* by L gives `37346/262143`, strictly exceeding `8/57`. Scaling establishes a minimax lower bound for every T, and the manuscript explicitly does not identify this coefficient with the unknown exact minimax. The uniform comparison uses a matching explicit schedule and the block-end recurrence, which remains valid for repeated modes when n=k.

The updated checker checks the arithmetic premises, representative sensitivity values, and exact attaining error, while its exhaustive polygon test remains a threshold-one test. Both the manuscript and README accurately distinguish those tasks. They do not present the finite sensitivity samples as proof over a continuum.

## Independent verification performed

Own artifacts are in `verification/reviewer03/stage02-round02/`.

1. **Fresh exact lower-bound certificates for all 972 word/time cells.** `check_exact.py` formulates the original one-sided objective for every word in `{0,1,2}^3` and every chronological pair of the eight affine switching-time cells. The variables are u,v,E. Constraints include cell bounds, u<=v, E>=0, and all three coordinates' occupation-minus-allocation at u,v,L. Repeated modes and zero-length blocks are included.

   HiGHS is used only to select a candidate dual support. I then solve the corresponding multiplier equations with exact rational linear algebra, check every multiplier's sign, verify `A^T y=(0,0,1)` exactly, and verify the exact dual lower bound is at least 18673/18396. **All 972 certificates pass.** No numerical objective, tolerance, or solver status establishes this lower bound. The exact certificate multipliers and bounds are saved in `exact-duals.json`.

   These certificates independently corroborate the analytic proof using the original objective rather than its sensitivity bounds. The minimum exact bound among the cells is 18673/18396.

2. **Exact direct witness evaluation.** The same independent program evaluates W-A on the union of all input knots and the two printed switch times. Its maximum is exactly 18673/18396; each active block-end discrepancy equals that value. No author reach-evaluation function is imported.

3. **Exact sensitivity and support arithmetic.** The independent program checks the knot slopes, terminal masses, delta_*, suffix identity, matching segment locations, final thresholds, scaled coefficient, support exclusions, and both repeated-word contradiction margins using rational arithmetic.

4. **Updated bundled checker.** I ran `verification/stage02/check_new_results.py` from the frozen snapshot with its output redirected to `bundled-check.log` in my own directory. It passes the revised exact-instance checks, all 972 threshold-one rational feasibility cells, and the retained identity/counterexample checks.

5. **Integrity.** All 40 snapshot file hashes pass, and the unchanged principal four-block computational dependencies match the prior snapshot byte for byte. The independently generated results are recorded in `results.json` and `results.log`.

## Limitations

I did not rerun the unchanged general certificate family or rebuild the PDF. I inspected only two of the newly rendered correction pages. My independent exact LP certificates use SciPy to discover supports and SymPy to solve rational equations; all accepted lower bounds are subsequently verified exactly, and the manuscript itself does not depend on these reviewer artifacts. I did not perform a new literature search or attempt to determine the unknown exact value of G^-_{3,3}; neither is needed to validate this instance theorem.
