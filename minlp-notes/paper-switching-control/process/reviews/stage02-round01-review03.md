# Independent review 03: stage 02, round 01

**Assessment:** No major or minor defect identified. The analytic reductions, the computational proof boundary, and the strengthened three-mode counterexample are sound as presented. I recommend acceptance of this stage. This is an independent stage review, not a claim that external peer review or later-stage work is complete.

## Scope and materials

I read all new manuscript text in the immutable `process/snapshots/stage02-round01` snapshot:

- `sections/03-heavy-and-reach.tex`: heavy-mode construction, first-repeat reordering, exact one-sided reduction, and analytic two-/three-block reach bounds.
- `sections/04-four-block-certificates.tex`: weighted pair inequality, printed event LP, exhaustive symmetry classification, quotient construction, symbolic stabilization, dual identities, and analytic passage to four blocks.
- `sections/05-small-budget-minimax.tex`: minimax consequences, equal masses, transitions/asymptotics, and all three structural counterexamples.

I checked the necessary stage-1 definitions and endpoint/compactness/uniform-input results. I inspected the complete `verify_general_four_block.py` implementation and its certificate data, the manifests, reference README, manuscript README, and the stage-2 runner, symbolic-quotient test, and new-results test. I did not treat prior reviews, author approval, or solver discovery output as proof. I did not consult other reviewers, spawn agents, or edit manuscript sources. Own verification artifacts are confined to `verification/reviewer03/stage02-round01/`.

All **35 snapshot hashes** and **12 provenance hashes** pass. The previous stage's external-dependency defect is resolved: the primary checker and its data are bundled together and execute from the frozen snapshot without importing live repository implementations. I ran individual checkers with output directed to my own directory; I did not run the log-writing stage runner against the immutable snapshot.

## Findings

No requested correction. In particular:

- A necessary-condition LP may contain nonphysical allocations and omit chronological constraints. Here that is valid because every actual control maps into it and the certificates prove a lower bound throughout the larger feasible set. No converse or exact relaxation claim is made.
- The ten symbolic certificates do not rest on numerical interpolation. The manuscript proves affine count dependence, and I independently verified the polynomial identities using **direct symbolic counts**, avoiding the author's n=9,10 reconstruction entirely.
- The n=k=3 proposition genuinely rules out repeated schedules. It is not an inference from the failure of six distinct-word compositions.
- The abstract, literature synthesis, and arbitrary-budget results are intentionally assigned to later stages and are not defects of this stage.

## Mathematical assessment

### Heavy-mode construction and one-sided reduction

`thm:heavy`, `lem:prefix-repeat`, and `lem:first-repeat` have the necessary hypotheses. The network's chain flow at prefix j is exactly the cumulative selected count. Integer lower/upper capacities and supplies give integral solutions; maximizing the heavy mode's final flow forces at least two occurrences. Merely having two occurrences would not save a switch, and the separate prefix-reordering argument correctly supplies adjacency.

In the first-repeat lemma, the prefix contains one twice-used mode and all other selected modes once. Error at its final endpoint provides every mass bound used subsequently. Choosing the latest level-one deadline works with flat allocations, including the equality case at the prefix end. The sorted deadline argument has the right strictness: missing a true deadline forces allocation strictly above one, while the double-block mode contributes at least one after its deadline. The terminal count vector is preserved, so the unchanged suffix remains feasible. Scaling and extension to `(s+2)E` preserve heaviness and do not increase the switch count after restriction.

The exact reduction uses the universal heavy-mode theorem only when a mass is strictly above E. Otherwise positive discrepancy is bounded by the terminal mass independently of the selected schedule, while compactness supplies a one-sided minimizer. The lower-bound witness needs k+1 distinct modes, exactly explaining k<n.

### Analytic two- and three-block reach

`eq:reach-definition` and `eq:reach-boundary` correctly use latest feasible endpoints. A one-sided discrepancy for an unused selected mode is largest at its block end; later activity in other modes cannot increase that discrepancy. Monotonicity of each reach map justifies greedy latest endpoints **for a fixed distinct word**. No repeated-word optimality is assumed.

The top-two and top-three first-reach sums are derived at their respective ordered first-reach times with the correct inequality direction. I checked the coefficients in `eq:first-reach-pair` and `eq:first-reach-triple`; their required signs match n>=3 and n>=4. The excluded-pair inequality follows by summing all other modes and comparing the excluded allocation at M_i and M. A maximizing pair remains available outside its two modes, which makes the aggregate argument work. The final sum is strict because failure at L means L itself is infeasible. This treats equality and flat portions correctly. The construction's pair/final reach evaluation counts and O(n^2) comparison bound are consistent with the described scans.

### Actual input to the printed four-block LP

I checked each family `eq:event-mass` through `eq:event-equal-P` directly against the objective and actual reaches. At event v, every permitted ordered pair (j,k) has reach no greater than t_v, so uncappedness and monotonicity give `R_j-t_v+A_k(t_v) <= -1`. Exclusion inclusion gives the allocation ordering; retaining the selected maximizing pair makes the corresponding event exactly M. No needed inequality is reversed.

The objective counts each Q exclusion inside S twice and each crossing exclusion once. Its normalization `(n-1)^2 H_S - 3n^2 sum_{i!=z} R_i` and lower bound `3n^2(n-1)` agree exactly with the strong weighted-pair statement after scaling by E. Choosing a smallest first reach supplies `sum_{i!=z} R_i >= nE`, giving the weaker form used later.

### Exhaustive types, averaging, and symbolic topology

The three intersection sizes of the maximizing pair with S give the three pair representatives. Within each type, the positions of z are exactly the nonempty membership classes relative to S and the pair: three, four, and three possibilities, with the outside representative absent for n=5 in the final type. Thus there are nine n=5 cases and ten thereafter.

The permutation action on modes outside K preserves the entire printed system and objective; convex averaging proves equality of infima without needing an optimum or boundedness. The orbit identifier retains the distinction between allocation to an interchangeable index excluded by its event and allocation to another interchangeable index. That distinction is essential and is present in both manuscript and checker.

In every representative from the printed table, K is an initial segment of at most six labels. Three additional labels realize every possible equality pattern in a pair-constraint row; allocation-order rows need at most two. Therefore n=9 already realizes every row pattern. Increasing n only repeats existing patterns and does not change the first-occurrence ordering. Mass equations have bulk coefficients n-|K| or n-|K|-1, and objective multiplicities are constant or n-|K|. This supports the claimed stable inequality matrix and affine mass/count reconstruction. Independently reconstructed quotient dimensions agree with the stated ranges 57–162 variables, 151–826 inequalities, and 10–19 equalities.

### Exact identities and four-block conclusion

The finite dual multiplier sign is correct for a minimization lower bound under Ax<=b: Y<=0 gives Y^T Ax>=Y^T b. All coefficient residuals vanish, so no omitted nonnegative-variable slack multiplier is needed. For polynomial data, D=(n-1)^2 D0 and positivity of D beyond 23 imply positivity of D0; the shifted coefficient signs establish Y<=0 throughout that interval. The finite cases cover 5–22 and polynomial cases every integer n>=23 without a gap.

The analytic four-block argument uses the certified inequality only on the mode set of a maximizing triple. A maximizing triple remains available in every exclusion outside that set. The aggregate coefficient of G is positive for n>=5, allowing G>=B3 to be substituted in the required direction. The identity n(B2+E)=(n-1)B3 gives the displayed aggregate bound. The final uncapped reach failures again produce strict inequalities, contradicting L<=B4. No full-error conclusion is obtained prematurely from one-sided bounds.

### Minimax consequences and counterexamples

The one-sided uniform lower recurrence permits repeated modes, since a mode's occupation at its current block end is at least the current block length. The full minimax and equal-terminal-mass results correctly combine this with the heavy-mode reduction and the separate T/n positive bound. I checked the stated plateau ranges, asymptotic coefficients, and equal-mass strict-improvement ranges against their rational formulas; the bundled exact arithmetic check also passes.

For `prop:three-mode-failure`, the tabulated increments are nonnegative, sum to time increments, and have slopes at most 3/4. Hence all H_i are strictly increasing, and the asserted knot substitutions identify unique first, pair, and distinct-triple reaches. The terminal masses sum to 57/8 and modes 0 and 1 both exceed two. For any schedule using at most two modes, the terminal one-sided inequalities imply omitted mass <= number of used modes, so omitting either 0 or 1 is impossible. The only possible support is {0,1}.

Every such schedule with at most three blocks has the form p,q,p allowing zero lengths. Its first endpoint is bounded by R_p; monotonicity controls the second endpoint by M_2. The middle block length is at most A_q(M_2)+1=M_2-R_p, while the final first-mode occupation gives the contradictory lower bound. Both printed gaps are arithmetically correct. This is a direct repeated-schedule argument, not a greedy claim about a repeated word. Compactness converts failure at error one into a strict optimum greater than one. The separate uniform construction and recurrence give uniform optimum exactly one even at k=n=3.

Both fixed-slot adjacent-pair counterexamples have consistent column sums, terminal masses, contradiction arithmetic, and feasible witness words. Their stated scope is fixed unit slots, and the final paragraph correctly refrains from claiming that they disprove every possible largest-heavy-mode strengthening.

## Checks actually performed

All completed checks passed. Main artifacts: `independent.py`, `results.json`, and `results.log` in this reviewer's directory.

1. **49 independent event-system reconstructions:** all admissible printed types at n=5,6,9,12,23. I rebuilt full event constraints and projected them onto independently defined orbit labels. The reconstruction uses different event order and a separate same/other classification for bulk allocation variables. The resulting complete inequality/equality row sets and objective match the bundled quotient exactly after coordinate conversion. This checks the printed equations against the checker, not just one against itself.
2. **179 exact finite dual identities:** all finite certificate entries satisfy the signs, coordinate equalities, and bound using integer arithmetic. The bundled main checker independently confirms case identifiers and exhaustive case coverage.
3. **10 symbolic certificates with direct counts:** I rebuilt symbolic mass rows as sums over individually labeled indices plus `(n-|K|)` bulk copies, or one excluded bulk copy plus `(n-|K|-1)` other copies. I rebuilt objective multiplicities directly from the event orbit, then checked every polynomial coordinate identity, bound, denominator factorization, and shifted sign using SymPy. This does not call `symbolic_program` or infer coefficients from n=9,10.
4. **Direct control-to-relaxation checks:** `control_embedding.py`, `control-embedding-results.json`, and `control-embedding.log` cover 48 rational controls, n=5,...,10, twenty cells each. Half use pure cell controls, contributing 480 cells with flat H_i. For every three-element S, exact latest first/pair reaches satisfy **2,828,640 printed pair constraints** plus the mass/order/equality constraints. All **22,552 strong weighted inequalities** over the resulting choices of S and distinguished z pass with exact fractions.
5. **972 independent word/time-cell LPs for n=k=3:** every one of the 27 three-letter words and every chronological pair of affine switching-time cells. Variables are u,v,E; constraints directly impose each coordinate's negative discrepancy at u,v,L. This includes repetitions and zero block lengths. The minimum over all cases is approximately **1.0150576212220048**, attained numerically by a distinct word (0,2,1). This corroborates strict failure at one; it is not presented as a new exact optimum theorem.
6. **Bundled exact checks run directly:** `verify_general_four_block.py` passes all 179 finite and ten polynomial cases; `check_new_results.py` passes all 972 rational feasibility cells, arithmetic consequences, and exhaustive fixed-slot counterexamples. The retained `verify_n4.py` and `verify_n5_weighted_pairs.py` pass their special-case certificates. The heavy-mode construction and independent audit programs were also run; individual logs are in the reviewer directory.
7. Both snapshot and provenance hash manifests pass in full.

## Limitations

The finite rational samples do not replace the proofs for arbitrary measurable controls. The independent n=3 optimization uses floating-point HiGHS and is corroborating evidence only; the manuscript's direct contradiction proof and the bundled exact rational feasibility audit establish the asserted strict failure. My independent symbolic audit uses SymPy, whereas the bundled primary checker uses only standard-library integer polynomial operations. I did not independently regenerate the discovery optimization or certificate search, neither of which is a premise of the proof. I did not rebuild or visually inspect every page of the PDF, and I did not conduct a new literature/priority search. Those limitations do not affect the examined mathematical statements.
