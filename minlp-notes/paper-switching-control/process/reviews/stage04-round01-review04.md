# Independent review 04: stage 4, round 1

**Verdict: no major issues. One valid minor issue requires correction before acceptance.**

I reviewed the immutable `process/snapshots/stage04-round01` version of Sections 8 and 9 in full, their relevant definitions and dependencies, the new verification material, and selected rendered pages. The arbitrary-grid formula and the three-mode grid results have sound proof contracts. In particular, the seven-cell result is an exact grid value; the manuscript correctly leaves a gap between the continuous lower and upper bounds. The one issue concerns how the exact grid result is related to a published conjecture, rather than its proof.

## Finding requiring correction

### R04-1 — Minor: distinguish the published equality conjecture from its upper-bound consequence

**Locator:** `sections/09-three-mode-floor-chambers.tex:281–284`, rendered manuscript p. 40, immediately after the proof of the exact seven-cell value.

The manuscript says that the value `4/3` is below the published conjectured upper bound `3/2`, “so it is not a counterexample to that conjecture.” The first comparison is correct, but the conclusion does not describe the published statement accurately. Sager–Zeile's **Conjecture 1, equation (7.6)** states an equality for the worst-case grid value. At three modes, seven uniform cells, and three switches, its second branch is `3/2`. Thus the proved exact value `4/3` contradicts that equality, while satisfying the associated upper-bound inequality. The parameters satisfy the conjecture's stated range.

**Suggested correction:** Say that this value satisfies the proposed upper bound `3/2` at these parameters, but refutes the equality asserted in Conjecture 1. Preserve the distinction from the separate correction to Corollary 5. No mathematical result or verification artifact needs changing.

**Primary source:** [Sager and Zeile, *On mixed-integer optimal control with constrained total variation*, Conjecture 1, equation (7.6)](https://link.springer.com/article/10.1007/s10589-020-00244-5). I checked the published statement directly, rather than relying on the repository's description of it.

## Mathematical review

### Section 8: arbitrary grids and one switch

I checked the reduction from a fixed input to the two closed LP families, the coverage of all inputs, the elimination, and the reconstruction.

- The restriction to the largest terminal-mass alternative for the final mode is justified by the stated discrepancy formula. Endpoint switch choices include constant schedules. The cutoff definitions and the two obstruction mechanisms agree with the actual control problem.
- The two families retain conservation, coordinate monotonicity, terminal ordering, and the appropriate obstruction inequalities. Averaging the undistinguished modes preserves these constraints. Interpolation of feasible endpoint data gives admissible rates, including coincident selected endpoints and zero-length phases. The heavy-family obstruction is valid whether a candidate omits a heavy mode or uses the two heavy modes.
- Coverage uses a discrepancy level strictly below the input optimum, so the relevant cutoff inequalities have the correct direction. Finiteness and closedness of the families then justify the limiting boundary argument. The explicit baseline construction at `T/3` covers the case in which a strict super-baseline argument is unavailable.
- The second-family upper bounds yield the stated `H` term, and only the interval straddling `T/3` can improve the baseline. Its displayed witness meets the constraints at the endpoints as well as in the interior.
- In the first family, symmetrization and the resulting terminal-mass change preserve the obstruction. I checked the bounds on the remaining scalar mass variable and their pairwise comparisons against the stated lower and upper expressions. The formulas reconstructing the prefix masses satisfy both monotonicity and interval-capacity constraints. The resulting `L`, `U`, and admissibility condition agree with the full LP constraints.
- The theorem's complexity statement is appropriately about the compressed description. There are quadratically many endpoint pairs and a fixed amount of rational arithmetic per pair. The formulas do not introduce an unbounded sequence of denominator growth. Dependence on the number of modes is through its binary encoding until an expanded control is requested, whose linear output cost is explicitly acknowledged.

I also checked the unit-grid three-mode residue formula, including the exceptional one-cell case and the smallest values in the other residue classes. The upper estimates and the lower constructions have matching endpoint conventions. The five-mode, nine-cell example correctly distinguishes the arbitrary-grid value from the uniform-control and three-mode candidates. Averaging a measurable input on each cell preserves every quantity used by the grid problem.

### Section 9: floor histories and small grids

The floor-history description and its realization theorem apply to every stated cell count, not merely to the enumerated small cases. With nonintegral prefix coordinates, the sum of their fractional parts is one or two. This gives exactly the two three-node count sets. Coordinate increments and the change in that sum give the four listed transition types.

The realization argument is sufficient: each allowed node has an incoming and outgoing edge whenever that neighboring layer exists, so each layer node belongs to a complete path. Averaging the integer allocations of all complete paths gives admissible cell rates. At each prefix, all three nodes occur, so every coordinate lies strictly inside its required unit interval. This proves realizability of every combinatorially admitted history without an unproved numerical feasibility assumption.

The dynamic-programming state includes the active mode and consequently counts switches, with the initial activation free. I checked the transition logic against actual count-vector evolution. The history totals and switch distributions agree with a fresh implementation described below.

For five cells, the generic upper bound and the treatment of boundary profiles are valid. The perturbation argument can avoid integral prefixes, and the finite minimum over words is continuous. The alternating pure input proves the matching integer lower bound. The continuous identity `F_{3,2}(T)=T/5` follows from grid domination and the separate pure-input witness. Its lower proof properly forces all three modes to be used and then uses the last activation's start time to obtain a contradiction below unit error.

For six cells, the enumerated maximum of three switches and the alternating pure lower witness give the claimed exact grid value.

For seven cells, I checked both the lower instance and the global upper bound. On the displayed lower instance, departing from a floor/ceiling count set costs at least `4/3`; the minimum-switch count inside those sets is four. The supplied three-switch word attains `4/3`. The six exceptional histories form the claimed permutation orbit. Each of the three repair words has precisely the advertised possible violation. Monotonicity and conservation give

`A_0(2) + A_1(3) + A_2(4) <= A_0(4) + A_1(4) + A_2(4) = 4`,

which supplies a repair word with error at most `4/3`. Perturbation and continuity extend this to boundary inputs. Thus the exact seven-cell value is established for all inputs, not just for the displayed exceptional example.

The continuous consequence `T/7 <= F_{3,3}(T) <= T/6` is stated with the correct scope. The six-cell grid gives the upper bound. The direct lower witness forces two distinct activation blocks each for modes zero and one and a block for mode two; its zero-rate gaps exclude joining the relevant early and late occurrences when the error is below one. This rules out four blocks. The manuscript does not claim that the seven-cell grid value determines the continuous minimax value.

### Published lower-bound correction

I checked the publisher PDF on pp. 610–612. Corollary 4's sharpness construction uses its stated congruence class. Corollary 5, p. 611, states the higher-mode lower bound without that restriction; the five-cell result contradicts its value `8/7`. Proposition 4, p. 612, equation (7.4), gives the separate continuous lower bound used here. The manuscript correctly separates those statements. The equality/upper-bound distinction in R04-1 is the only source-scope correction found.

## Independent verification and reproducibility

All generated files and log-writing runs were confined to `verification/reviewer04/stage04-round01/`. I verified all 95 snapshot manifest entries, copied the snapshot to `relocated/`, and ran the supplied stage-4 checks and LaTeX build only in that copy.

The supplied runner passed `check_finite_formula.py`, `check_floor_chambers.py`, `small_grid_boundary.py`, and `check_small_grid_review.py`; all 25 original artifact hashes matched. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeded on the relocated source. I found no unresolved-reference, undefined-command, or overfull warning in the final build log.

I wrote `independent_checks.py` without importing the manuscript verifiers. It generates admissible floor histories directly and computes minimum switches using actual count vectors and the last active mode. It reproduced:

| Cells | Minimum 0 | Minimum 1 | Minimum 2 | Minimum 3 | Minimum 4 | Total histories |
|---|---:|---:|---:|---:|---:|---:|
| 5 | 3 | 138 | 255 | 0 | 0 | 396 |
| 6 | 3 | 255 | 1377 | 237 | 0 | 1872 |
| 7 | 3 | 414 | 4542 | 3891 | 6 | 8856 |

It also reproduced the six-history orbit and checked the three repair properties directly.

For the arbitrary-grid formula I independently built the full-coordinate LP families, with separate prefix and terminal variables for every mode. These checks use twelve uniform or randomly generated rational grids across `(n,N)=(3,1),(3,2),(3,5),(4,4),(5,5),(7,4)`. Every maximum agreed with an independently coded closed formula. For every feasible optimum, rationalized primal and dual solutions passed exact feasibility, sign, residual, and objective-equality checks: 30 exact rational optimality certificates in total. The remaining 186 LP cases were reported infeasible numerically; I do not count those statuses as exact infeasibility proofs. The mathematical elimination and coverage arguments supply the general proof.

I retrieved the publisher PDF independently. Its SHA-256 matched the recorded `f4dfdfdc761de38dafeea5dd9eafb5bbf3c637a39dc7ee2ff1432a9803996770`. The extracted pages used for the published lower bounds are saved as `source-pages610-612.txt`.

Useful artifacts are `integrity.log`, `runner.log`, `relocated-build.log`, `independent_checks.py`, and `independent-checks.log` in the assigned verification folder.

## Limitations and final assessment

This review covers the new stage-4 material and dependencies needed to assess it. I did not repeat every accepted certificate from earlier stages or conduct a new global novelty search. I checked selected rendered pages rather than performing a separate typographic audit of every page. Numerical infeasibility results are corroboration only, as distinguished above. The pending algorithm, full bibliography, introduction, abstract, and experiment stages are outside this review's scope.

There is no remaining major mathematical or scientific-development issue identified in this stage. Correct R04-1 before acceptance; the theorem statements and proofs can otherwise proceed to the next stage.
