# Stage 2, round 1 — independent review 5

## Verdict and findings

**No major or minor defects found.** I recommend accepting this stage. The two compression constructions, forest-complement corollary, individual-coordinate completion result, and recovery claims are justified within their stated scope. The new fixed-arc preprocessing lemma is also correct.

Enumerated findings: **none**. I did not manufacture presentation preferences as required corrections.

## Mathematical checks actually performed

1. **Fixed arcs, Lemma 4.1.** Verified the affine bijection at graph points and its compatibility with convexification. For the affine-hull assertion, nonconstancy of each remaining coordinate supplies a feasible point strictly inside that coordinate's two bounds; averaging over coordinates gives simultaneous strictness. The empty remaining-coordinate set is handled explicitly. No extra equalities can remain beyond balances after this preprocessing, because all other constraints are coordinate bounds.
2. **Path suppression.** Checked arbitrary arc orientations, degree-two vertices whose total graph degree is larger due to other blocks, rank-one cycles, original loops, and parallel edges. It is the block circulation deviation that is constant with a sign along a path, so nonzero original balances are correctly absorbed in the reference vector. The reduced-core degree bound gives the stated `3r-3` edge count for rank at least two. Chord rows prove boundedness of the cycle-coordinate domain even on lower-dimensional feasible sets.
3. **Cycle-coordinate hull, Theorem 4.2.** Checked that each explicit state has the correct scaled path bounds and every original observation is retained. The eliminated merged deviation is a circulation because both its aggregate and explicit summands are circulations. Its residual bounds are essential and are retained. The coefficient and row counts are correct; retaining one representative original flow per residual row avoids coefficient accumulation on flow variables.
4. **Unit-minor elimination, Lemma 4.3.** Checked the incidence-minor argument, tree-column replacement determinant formula, identity chord rows, row replacement formula for `W`, and bordered determinant formula for `R`. The zero-dimensional pivot case and full-pivot case agree with the formulas. The proof establishes the required entries in `{0,+1,-1}` without assuming the final extended formulation itself is totally unimodular.
5. **Observation-sensitive hull, Theorem 4.4.** The substitution is reversible for every feasible extension. Selected observations use distinct product variables; nonselected observations, including duplicate observations on a path, do not silently disappear. Different labels have disjoint product columns, so collecting the residual rows does not defeat the unit coefficient conclusion. The kernel of restriction to observed arcs is exactly the circulation space on the unobserved subgraph, giving the stated nullity. Isolated vertices, loops, and parallel edges are correctly reflected in the rank formula.
6. **Sizes and normalization.** Recomputed the row and nonzero counts. The latter correctly accounts for dense reconstructed path expressions and observation rows when rank grows. The paper distinguishes unit coefficients under the displayed rational scaling from primitive integer normalization; its claims therefore do not contradict later coefficient-growth directions. Polynomial encoding length is justified by reference-flow sums, selected interval endpoints, and unit-minor reconstruction.
7. **Forest complements and completion, Corollary 4.5 and Proposition 4.6.** Checked the zero-kernel equivalence, necessity of at least the nullity many additional scalar coordinates, and sufficiency of adding unobserved nonforest edges. Reclassifying the extra products as auxiliary variables is legitimate because linear projection commutes with convexification. The additional observations do not create new locally observed labels, and their number is absorbed in the earlier row count. The ambient-space and zero-weight limitations are explicit and correct.
8. **Recovery.** Pivot reconstruction, expansion along signed paths, recovery of the merged block deviation, and proportional refinement give a valid global decomposition. The stated exactness appropriately requires rational feasible extension data; a numerical LP solution alone is not advertised as an exact certificate.
9. **K4 worked example.** Recomputed all three state-deviation equations from the incidence equations. The four path average has the listed arc flows. All three supplied products obey their independent McCormick constraints, while the reconstructed nonnegativity constraint is violated by exactly `1/10`. This is a clear small example of the structural benefit and does not overclaim that the single cut describes the hull.

## Independent exact executable check

I wrote a separate symbolic check in `verification/reviewer5/stage02-round01/check_k4.py`; it does not import the manuscript author's implementation. It constructs the oriented K4 fundamental-cycle matrix and checks:

- all 64 observation subsets;
- 181 choices of independent observed rows and nonsingular pivot columns;
- 1,086 exact row checks of the unit `W` and `R` conclusions;
- the unobserved-incidence nullity identity for every observation subset;
- the worked example's McCormick feasibility and exact `1/10` violation using rational arithmetic.

The check passed. Its output is retained in `check_k4.json`. These finite checks supplement, rather than replace, the general proofs.

## Source coverage and dependency check

Compared the stage with the substantive statements in `notes/network-simplex-reopened-compressed-hull.md` and `notes/network-simplex-observed-rank-elimination.md`. The compressed variable and row bounds, observation-rank refinement, unit coefficients, forest criterion, individual-coordinate interpretation, and relevant limitations are all represented. The paper improves self-containment by proving the unit-minor lemma and explicitly giving the final reconstructed inequalities and recovery steps.

The reduced-RLT precursor is credited at the relevant reconstruction discussion; the narrower claimed contribution is the observation-complement criterion and sparse exact-hull consequence. The corrected Stage 1 passage now explicitly acknowledges the equality-flow overlap with Khademnia–Davarnia, resolving the issue from my earlier review. I found no newly introduced contradiction with the accepted foundations.

## Build and presentation

Built a private snapshot copy under `verification/reviewer5/stage02-round01/build/` with the documented `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` command. The final PDF has 13 pages. The final LaTeX log has no warning, undefined-reference, undefined-citation, or overfull/underfull-box entries. The first-pass missing-bibliography notice resolved during the normal BibTeX/LaTeX build sequence.

Visually inspected rendered pages 9 and 11, covering the determinant proof, observed-rank notation, forest corollary, and completion proposition. The displays and text fit within the margins and were legible. The source exposition identifies its assumptions before each reduction and explains the distinction between the local merged state and the global residual state through the accepted dependency.

## Limitations and independence

This review concerns the frozen Stage 2 snapshot and its foundational dependencies, not unprovided future sections, future benchmarks, or a definitive literature-priority search. I did not independently verify every publisher metadata field. I did not read current-round reports, coordinate findings with other reviewers, spawn agents, change manuscript sources, or build inside the frozen snapshot.
