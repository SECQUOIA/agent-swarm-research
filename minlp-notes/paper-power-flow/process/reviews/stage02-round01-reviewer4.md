# Stage 2, round 1 — independent reviewer 4

**Verdict: PASS. No required major or minor correction identified.**

I reviewed the frozen stage-2 manuscript, especially `sections/03-ac.tex`, the abstract, bibliography, README, coverage map, and `checks/check_ac_exact.py`. I checked dependencies against the accepted resistive argument. I did not read any other stage-2 reviewer report and did not edit the manuscript. The conclusions below concern the written results, not a classification of every possible physical or approximate variant.

## Mathematical audit

1. **AC signs and magnitude encoding are correct.** With `A=r_i^2-H_ij`, complex power from a line is `(g-ib)(A-iD)`, whose real and imaginary parts are `gA-bD` and `-bA-gD`. The shunt contribution is `(h-it)r_i^2`. These give exactly the displayed rectangular equations. The strictly positive rational lower bounds on `r_i` make `r_i` the positive magnitude and exclude zero phasors.

2. **Negative cosine limits cause no squaring problem.** The condition `H_ij >= c_ij r_i r_j` with positive `r_i,r_j` is equivalent to the principal angular bound for all `c_ij` in `(-1,1]`. The case `c=1` forces equal directions. The excluded endpoint `c=-1` is exactly where antipodal directions would make the selected principal arc nonunique. The input encodes rational cosines, so no transcendental coefficient is hidden in the ETR formula.

3. **The crossing rule works beyond pi/2.** With endpoint arguments in `[0,2pi)`, `f_j<0<=f_i` implies `a=alpha_i-alpha_j` lies in `(-2pi,0)`. On that interval, the positive determinant condition holds exactly for `a<-pi`. Thus the first case is precisely the positive wrap; reversal proves the negative case. At positive-ray endpoints, the closed-upper/open-lower convention counts arrivals and departures with the correct sign. Negative-ray endpoints are not accidentally counted because the determinant has the opposite sign. Coincident directions give zero. The proof is independent of radii and excludes only antipodal directions, so it remains valid for all the stated negative cosine inputs.

4. **Cycle signs and the lift criterion are sound.** The orientation is consistently `j -> i`, with `D_ij=Im(U_i conjugate(U_j))`. Summing `delta_ij=alpha_i-alpha_j+2pi k_ij` along a directed cycle cancels the alpha terms with the manuscript's epsilon convention. For the converse lift, assigning an actual argument at each forest root and integrating principal differences along tree edges yields angles representing the original phasors. The fundamental-cycle equations then force the proper difference on each chord. Disconnected graphs and isolated buses are handled componentwise. No global unwrapped-angle variable with irrational coefficients is required.

5. **The ETR size claim is valid.** There are three real bus variables and one real crossing variable per edge. The disjunction defining a crossing variable has constant size and forces one of `-1,0,1` exactly, without integer quantification. A forest has `|E|-|N|+kappa` chords, each fundamental cycle has at most `|N|` edges, and explicitly listing all such sums remains polynomial in graph encoding length. Rational coefficient bit lengths also remain polynomial after denominator clearing. Strict comparisons and their negations are permitted by the ETR convention established in stage 1.

6. **The equal-angle lemma validly extends the earlier bound to all real line differences below pi.** Pairing bus contributions in `-sum theta_i Q_i` gives positive weights times `t sin t`. This is positive for every nonzero `t` with `|t|<pi`, irrespective of cosine sign. Zero reactive injections therefore force zero line differences. The real-lift hypothesis is essential and explicitly stated. The unit-line example at difference pi correctly shows sharpness at the excluded endpoint.

7. **All hardness transfers are valid.** Adding zero susceptances/shunts/reactive injections and fixed cosine zero to the stage-1 network preserves its graph, bounds, and feasibility. For angle boxes, the two inequalities imply `e>=|f|`; the positive magnitude lower bound rules out `e=0`, supplying an actual angle in `[-pi/4,pi/4]`. The reference at zero then forces every equal-angle component to have `f=0` and `e=v`. The reference is chosen separately for each component, including isolated vertices.

8. **The positive-width reactive corollary is exact but correctly delimited.** Pure resistance and absent shunts make the sum of reactive injections zero by edgewise cancellation for arbitrary phasors. A common weak sign consequently forces every injection to zero. Replacing all zero intervals by `[0,1]` preserves the feasible set in each transfer. The text correctly says this is not a symmetric-tolerance robustness theorem.

9. **Counterexamples have legitimate rational inputs.** The n-cycle has zero reactive injections and strictly positive equal active injections, with principal winding one. For arbitrary fixed rational `c<1`, taking a sufficiently long cycle and rational bounds strictly surrounding its common positive power gives rational data even when the actual power is irrational. This is an existence statement, so density of the rationals suffices; no unstated polynomial-time selection procedure is being used as a reduction. The explicit 4-cycle has entirely rational phasors and singleton power 2. Its corresponding unit-voltage resistive problem has power zero at every bus and is infeasible.

10. **Shrinking positive principal windows preserve polynomial complexity.** The concavity inequality `sin(t/2)>=t/pi` gives the stated bound `gamma_n<=pi/(sqrt(2)n)` for `c_n=1-1/n^2`. Every cycle budget is then strictly below `2pi`. Its principal difference sum is an integral multiple of `2pi`, hence zero; the real-lift and equal-angle arguments apply. Padding by isolated free buses to ensure `n>=2` preserves feasibility and the finite alphabet. The denominator `n^2` has `O(log n)` bits. The corollary explicitly distinguishes this varying cosine from the other fixed numerical data and does not silently claim a fixed positive principal-window classification.

## Source and writing assessment

The oscillator citation supports the specific background statement made here. I independently opened the primary [arXiv version](https://arxiv.org/html/1208.0045v1), verified the weighted sine equilibrium in equation (1), and checked its discussion of cohesive phases. The manuscript does not import a global uniqueness claim from that paper: its zero-reactive real-lift result has the self-contained energy proof audited above. The source identity and DOI agree with the [arXiv record](https://arxiv.org/abs/1208.0045).

The abstract correctly describes the actual scope. The exposition separates real line limits, principal differences, and bus-angle boxes sufficiently clearly, and it preserves the important distinction between exact balance and small numerical residuals. I found no unsupported claim requiring a source correction in this stage. The broader literature comparison and future stage-3 results are not silently asserted here.

## Verification performed

All artifacts below are in repository-relative `paper-power-flow/verification/reviewer4/stage02-round01/`.

- `ac-exact.log`: the frozen checker passed 2,112 scaled short-arc pairs, including 768 arcs longer than pi/2; 14,784 rational-cosine checks; 177,168 cycles compared with a rotated ray, including 59,640 with nonzero winding; and 648 independently expanded complex-power cases. Its rational four-cycle, antisymmetric reactive sum, antipodal exclusion, and size-dependent cosine regressions passed. The coverage-map counts agree with the actual output.
- `boundary_check.py` and `boundary-check.log`: I added reviewer-owned exact checks at near-axis and near-antipodal rational directions with perturbation `10^-100` and radii between `10^-100` and `10^100`. All 396 admissible cases agree with the independent chord/ray crossing computation and reversal identity. This tests strict boundaries and scale independence beyond the manuscript checker's fixed sample.
- `build.log` and `build/`: independently compiled the frozen manuscript with `latexmk -pdf -interaction=nonstopmode -halt-on-error` into my own output directory. The final ten-page PDF compiled without warnings, undefined references/citations, or overfull/underfull boxes. `manuscript-layout.txt` contains the extracted final PDF text.
- `manifest-check.log`: all twelve frozen input hashes agree with `manifest.json`.

These computations are finite regression evidence; the mathematical conclusions rely on the audited proofs.

## Required corrections and optional future work

No required correction. No optional extension is needed to complete this stage. In particular, fixed positive principal windows, symmetric reactive tolerances, and broader physical restrictions are separate research questions rather than gaps in the proved theorems.

Artifact packaging note: the review artifacts were relocated byte-for-byte from the repository-root `verification/reviewer4/` directory into `paper-power-flow/verification/reviewer4/`. Historical command and build logs retain their actual original paths.
