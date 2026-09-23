# S3 independent review — reviewer 3

Verdict: one minor statement-scope clarification; no major finding. The intended results and their proofs pass this review.

Reviewed `complexity/sections/05-boundaries.tex` in full, with the needed existence, flow-bound, block-aggregation, Lipschitz, cactus SRS, and exact bounded-block-rank dependencies in Sections 1–3. This review did not consult other S3 reviews, author reports, root development notes, or author verification scripts. No manuscript or shared build files were changed.

## Finding

### R3-1 — designate the queried probe and its orientation in the SRS equivalence statement

Severity: minor. Location: `complexity/sections/05-boundaries.tex:687–690`; compare the converse at lines 717–725.

The restricted-family sentence describes a graph consisting of a cactus branch, terminal bridges, and a probe edge, but does not explicitly require that the queried arc be the probe oriented from the unit source to the unit sink. Its converse uses precisely that requirement: it identifies the target flow with a number strictly between zero and one and transforms `x >= c` into the lower cactus-pressure comparison `R >= beta(c/(1-c))^2`.

Describing only the graph family leaves the sentence open to a broader reading that allows an arbitrary queried arc, or a probe oriented in the opposite direction. The displayed reduction does not prove that broader statement. This is a scope ambiguity, not a defect in the intended equivalence.

Repair: replace the last sentence of the theorem by language such as: “On the restricted family consisting of a two-terminal cactus branch with two terminal bridges in parallel with one probe edge, weak lower comparison of the probe flow, oriented from the unit source to the unit sink, is polynomial-time many-one equivalent to SRS.”

## Universal characterization audit

No finding in the proof at lines 590–672.

- The theta formulas satisfy conservation and both potential equations. At resistances `23/108`, `1`, and `71/12`, the cross flows are respectively `3/2`, `1`, and `1/2`. The outer reverse pressures are `-49/24`, `-2`, and `-49/24`.
- Adding `(1,0)` makes exactly K4. The sign of its flow and the direction of its feedback follow from the decreasing probe-pressure map. The bound `96/sqrt(10^8) < 1/96` is correct. The endpoint pressure lies below `-65/32`, whereas the interior pressure exceeds `-2`; their advantage exceeds `1/32`. Rationalization gives the stated strict target-flow advantage `g = 1/1280000`.
- The minor-to-subdivision argument is valid for K4 because each minor branch set has at most three required attachments. Pruning to a connecting tree and taking its median produces disjoint subdivided K4 branches. The subdivision lies in a single block.
- Series subdivision preserves the state with zero internal nominations. Dividing the uncertain path into a fixed positive total `theta_L/2` and one uncertain edge preserves positive resistance endpoints and leaves only one uncertain edge. The length-one case is treated separately.
- Every edge outside the subdivision is restored, including chords between subdivision vertices and edges through extra vertices. The proposed comparison flow is conservation-feasible on the full graph even though it need not satisfy its potential equations; feasibility is all the energy comparison needs. Its energy is `(10+theta)/3 < 6` for all three scenarios.
- The energy bound implies `|x_e| <= (18/R)^(1/3)` for each added edge. The total positive nomination is seven, so all physical edges are bounded by seven. Restricting to the subdivision gives a valid passive state for the balanced induced nomination `b' = A_H x_H`; it does not require the original subdivision nominations to remain unchanged.
- The induced-nomination estimates are valid: `||b'-b||_1 <= 2m(18/R)^(1/3)`, and the containing coordinate box has absolute sum at most `14m`. Applying the general-graph Lipschitz lemma along the actual target edge cancels its possibly subdivided resistance and gives the displayed `112m^2(18/R)^(1/3)` bound on squared flow error.
- The stated integer `R = 18(2000m^2/g^2)^3` has polynomial bit length. Since `112/2000 < 1/16`, each of the three restored target flows changes by less than `g/4`; the interior advantage remains greater than `g/2`. Thus both separate monotonicity and finite-set versus interval-hull equality fail on the full original graph. No edge deletion is hidden in the conclusion.

## Probe-cactus arithmetic audit

Apart from R3-1, no finding at lines 681–736.

The earlier cactus encoder yields integer resistances and a positive integer threshold after its preprocessing and scaling. Adding two unit terminal bridges and a probe of resistance `H+2` preserves simplicity and maximum degree three. The resulting graph is series-parallel; adding the probe merges the cactus chain into a block whose rank grows with the input. The identity `(D+2)(1-x)^2 = (H+2)x^2` gives exactly `x >= 1/2` iff `D >= H`, including equality.

The substituted trivial instances satisfy the literal restricted family: the equal two-branch triangle has effective resistance `1/2`, its terminal-bridge extension has effective resistance `5/2`, and probe resistances one and nine give yes and no at threshold `1/2`. For the converse on the designated probe, positivity gives `0 < x < 1`; consequently `c <= 0` and `c >= 1` are correctly handled, including `c = 1`. The interior-threshold transformation preserves the weak inequality. The earlier cactus reduction handles equal branch resistances, no radical terms, and nonpositive transformed SRS thresholds with fixed yes/no outputs. Neither direction evaluates square roots in the reduction. The text correctly avoids a claim about strict capacity violations, general series-parallel SRS membership, or ordinary NP-hardness.

## Remaining proof and output checks

No further finding.

- The rank-two pressure gadget, its graph degrees, fixed nominations, rational gap, and integer rescaling are correct. Scaling multiplies potentials but not flows, and the claimed absolute-error-one hardness has the stated weak-hardness limitation.
- Finite secant comparison follows directly from conservation and reciprocity. The arbitrary positive secant resistance on unchanged-flow coordinates is harmless. The target electrical current lies in `[0,1]`.
- Adjacent-terminal sign invariance applies blockwise under the stated K4-minor-free convention. The continuous envelopes remain strictly increasing and continuous; a realizing original edge law can be selected independently at the final edge flow. The argument proves attainable scalar extrema, not one simultaneous vector optimum or existential feasibility.
- The affine one-coordinate monotonicity proof covers zero parameter effects and zero derivatives. Sequential endpoint selection preserves the maximum, including jointly over a compact nomination set. The exact finite optimizer extraction uses polynomially many exact bounded-rank comparisons and permits an algebraic nomination witness.
- The cubic epigraph lift is exact, including the zero case. The additive algorithm provides explicit bounded cycle coordinates, rational function and gradient oracles, an interior near-optimal ball, and polynomial bit tolerances. Its scalar uniform convexity estimate yields the claimed cubic energy-to-flow bound. The residual analysis correctly bounds the loss caused by selecting an endpoint using an approximate flow sign. Thus it outputs both a certified rational value interval and an allowed rational endpoint scenario, without requiring exact signs of algebraic flows.
- The rank-three discrete probe reduction preserves simplicity and maximum degree three. Its pressure loss, flow gap, and resistance integrality calculations are correct. Membership guesses finite resistance indices and uses the earlier exact bounded-rank arc theorem, so it does not assume short rational physical witnesses. Weak and strict existential comparisons are separated by the reduction's gap.
- The nomination-hardness transfer preserves series-parallel structure. Its enlarged nomination box is used only for sensitivity, not to change the source uncertainty set. The yes/no margins imply the stated polynomially encoded arc gap, and no general-rank NP membership is asserted.
- Prescribed-flow interval realization is rational linear feasibility, including zero flows. The finite realization reduction is on a simple cycle in an acyclic orientation, and the capacity argument forces both positive branch flows to equal one. The separate membership claim for the fixed-nomination single-cycle capacity problem is justified. The approximation gap and the final distinction between universal containment and existential intersection are correct.

## Primary-source and isolated checks

Checked local primary full texts for Eppstein (Lemma 9), Duffin (Theorems 0 and 1 and the nonlinear discussion), Chauffoureaux–Hasler (Theorem 3 and the stated extensions), Zemanian (report Sections 4–5 and 8–9), Robinius et al. (Theorem 4.7 and its attribution), and Thürauf et al. (the robust-feasibility characterization). These support the limited comparisons made here. The unavailable Hasler–Wang comparison is expressly disclosed and no priority claim is based on it.

For Thürauf 2022, independently extracted the local original PDF to inspect equation (3), the booking/resistance definitions, Lemma 4.3, Lemma 4.17, and the unfiltered pressure subproblem. The manuscript's rational parameters and source interpretation agree.

Checked [Dadush's thesis, Theorem 2.5.9, printed p. 48](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf). Its centered-body, Lipschitz-objective formulation supports the rational weak-optimization invocation; the manuscript supplies a known cube and a tangent extension satisfying those hypotheses.

An independent Python `Fraction` calculation checked the three theta roots, their divergences and outer drops, the energy bounds for restoring edges, and the rational inequalities underlying the pressure-loss and restoration constants. All checks passed. These checks supplement the derivations above and were not used as substitutes for them.
