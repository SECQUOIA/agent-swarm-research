# Stage 4, round 1: independent review 05

Verdict: **accept this stage; no major issues found and no valid minor issues identified.**

## Scope and independence

I read `sections/08-finite-grid-one-switch.tex` and `sections/09-three-mode-floor-chambers.tex` in full in the immutable `process/snapshots/stage04-round01` snapshot. I checked their endpoint-error, compactness, scaling, grid-domination, and one-switch-formula dependencies as needed, read the new checker implementations and documentation, and inspected manuscript pages 32–40. I did not read another current review or an author/root assessment, communicate with another reviewer, delegate work, or edit the manuscript or snapshot.

All generated artifacts are confined to `verification/reviewer05/stage04-round01/`. The snapshot's 95 recorded file hashes still match.

## Mathematical audit

### Arbitrary-grid formula

Locator: Theorem 11.1, equations (92)–(100), in `08-finite-grid-one-switch.tex`.

I checked the dominance reduction to a largest available final mode. The two closed LP families correctly obstruct all admissible schedules, including constants. Their converse coverage uses strict thresholds below the attained minimax and then a bounded subsequence; the separate `F=T/3` construction fills the remaining boundary case. The all-initial-modes family correctly does not require `m_2<=E` as an additional feasibility constraint.

The two-large-modes family's elimination gives both necessary upper bounds, and the displayed two-phase witness attains their minimum. Its inequalities remain valid if the first crossing endpoint equals `T/3`, if it is the final endpoint, or if a component type has zero terminal mass.

For the other contribution, averaging all modes except the largest preserves the required initial obstructions and moves the other final-mode cutoff weakly later. I checked both directions of the scalar endpoint elimination. In particular, the reconstruction of `x,y` supplies nonnegative increments for both component types, including coincident phases `a=b` and `b=N`. Comparing the four lower and two upper bounds on `M` gives exactly the retained feasibility condition and the stated lower/upper intervals for `E`; the omitted comparisons really are automatic. Thus the closed formula has neither a lost constraint nor an unsupported converse.

The arithmetic-operation and bit-complexity claims apply to the compressed maximizer. Every candidate has fixed algebraic depth in original rational endpoints and `n`, and only `O(N^2)` candidates are compared. Writing all components would introduce a dependence on `n`, and the manuscript explicitly separates that output cost.

### Unit-grid consequences

Locator: Corollary 11.2 and Example 11.3.

The residue proof handles `N=2` through `k=0`, all displayed inequalities have the required signs, and the `N=1` case is treated separately. The upper constructions omit only masses at most the chosen threshold. The mixed-cell lower witnesses obstruct both orders and constant schedules, including empty pure blocks. The corrections relative to `N/3` are correct.

I checked the five-mode nine-cell rates, terminal masses, lower obstruction, and independent upper proof. Its error `17/5` exceeds the two stated restricted-family values. The nonuniform-grid warning is limited to the specified incomplete simplification; the complete formula retains the missing cutoff and feasibility conditions.

### Floor histories and small-grid theorems

Locator: Proposition 12.1 through Theorem 12.6 in `09-three-mode-floor-chambers.tex`.

The all-`N` realization proof is complete. Every transition graph has an incoming and outgoing edge at each node; every node therefore lies on a complete path. Averaging complete integer paths gives a simplex-valued control, and every prefix coordinate lies strictly between its specified floor and ceiling because both count values occur. This establishes existence for every listed history without presupposing feasibility of the floors. The count-node index is distinguished from the active-mode label, and the switch-count recursion uses the latter correctly.

The floor-history totals and minimum-switch distributions for five, six, and seven cells are correct. The perturbation argument reaches all boundary profiles, with an explicit nonintegral target for arbitrary `N`; continuity over the finite schedule class gives the non-strict error bound. The alternative five-cell coverage argument via integral prefix flows is valid in both directions.

For the seven-cell result I checked the supplied fractional cumulative vectors, the implication from error below `4/3` to floor/ceiling compatibility, and the need for four switches inside the witness chamber. The six exceptional histories are exactly a full relabeling orbit. Each repair word has three switches and exactly its stated exceptional coordinate. Conservation and monotonicity bound the sum of the three exceptional allocations by four, proving the uniform `4/3` upper bound on this entire chamber. The matching instance proves sharpness. The pure five- and six-cell lower witnesses correctly force their original words whenever discrepancy is below one.

### Continuous consequences and source correction

Locators: Corollary 12.3, equation (113), and Section 12.4.

The direct `01201` lower witness proves `F_{3,2}(T)>=T/5` against continuous switching times: any hypothetical smaller-error schedule must use all three modes once, and the last mode has incompatible initial and terminal timing requirements. The proposed attaining schedule has error one on horizon five. The grid upper bound transfers in the correct direction.

For `F_{3,3}`, the `0120011` argument forces two activations each of modes 0 and 1 and at least one of mode 2 under error below one. A single activation spanning each mode's required early and late occurrences would change discrepancy by more than `2E` on its inactive interval. Thus the stated lower bound is valid; the six-cell upper bound yields `T/6`. The manuscript correctly leaves the continuous value undetermined between `T/7` and `T/6`, rather than transferring the grid lower bound.

I independently read the final published Sager–Zeile PDF at printed pages 610–612, using a local copy whose SHA-256 matches the recorded publisher-file hash. The attainment congruence in Corollary 4, the absence of that condition in Corollary 5, and the separate continuous Proposition 4 match the manuscript's descriptions. The five-cell contradiction satisfies the published parameter restrictions, including the alternative reading that permits varying a grid of fixed horizon and maximum width. The paper does not confuse this correction with the continuous lower bounds or the separate conjecture counterexamples.

## Independent verification beyond the supplied checks

I wrote two new programs without importing project implementation code.

1. `independent_floor_words.py` enumerates all integer words and represents prefix compatibility by bit masks. It independently generates monotone binary floor increments and intersects the full-word masks, without using the manuscript's nine-entry switch recursion. For **396, 1,872, and 8,856 histories**, respectively, it reproduces all printed switch distributions. For every prefix coordinate of every history it additionally verifies that both allowed integer counts occur on complete compatible words, independently checking strict realizability. It confirms equality of the six exceptional-history set with the printed permutation orbit. Results are in `independent-floor.log`.

2. `independent_grid_lp.py` assembles the two LP families directly in **all original modes and all cell-allocation variables**, without endpoint compression or elimination. Across **18 rational grids and 320 LPs**, including one-cell grids, irregular grids, the nine-cell example, and the displayed nonuniform counterexample, their optima agree with an independently implemented closed formula. These LP comparisons use SciPy/HiGHS and are numerical corroboration. Separately, the program reconstructs each winning compressed extremizer and exhaustively evaluates the original absolute discrepancy of every one-switch schedule using exact rational arithmetic. All reconstructed values agree exactly. Results are in `independent-grid-lp.log`.

The mathematical formula and elimination do not depend on the numerical LP checks. The all-`N` realization theorem rests on its graph/averaging proof, while finite coverage is independently checked by word enumeration.

## Build, layout, and portability

I copied the snapshot to the assigned verification directory, removed its supplied PDF and bibliography output, and performed a fresh LaTeX/BibTeX build. The 40-page build succeeds with no final LaTeX warnings, unresolved references, overfull boxes, or underfull boxes. I rendered and visually inspected pages 32–40: the formula, closed LPs, elimination, floor-transition tables, switch matrices, repair argument, and source correction are readable and consistently referenced.

All four documented standard-library stage 4 checks pass from the relocated copy, including integrity checks for the 25 bundled originals. The runner's output files remain outside the frozen snapshot. The documentation accurately separates exact verification from optional numerical LP audits and identifies the finite computations used by the small-grid proofs.

## Limitations

This review does not repeat all unchanged earlier certificate families or constitute a new literature-priority search. The independent LP comparisons are numerical; the independent extremizer and floor-word checks are exact. The all-`N` floor characterization was checked analytically, not by finite enumeration alone. Later algorithms, experiments, full bibliography, and integrated introduction/abstract remain outside this stage as instructed.
