# Stage 5 primary-agent audit and development

## Initial source reading

Read the complete sharp-transfer result and reopened proof, and the fixed-budget algorithm result. The transfer proof's support condition is essential: select an original occurrence at a positive-measure time inside each assigned grid cell. The times strictly increase, so the original block indices cannot decrease. Deleting intervening blocks and merging equal labels cannot increase the switch count. Uniform cell widths are what permit the unit-supply integral prefix network; arbitrary nonuniform multicomponent transfer is not justified by that proof. The binary discrepancy interval argument separately works on nonuniform grids.

The sharpness input fixes N=n+1, s=n-1, uniform rates in the first cell and pure final mode afterward. The exact grid optimum is1-1/n; the continuous cycle competitor has error(n-1)/n² and uses exactly the allowed switches after its last block merges with the tail. Their gap is at least(1-1/n)², approaching one. The n4 instance exceeds a half-cell gap. This corrects the source's instance-level heuristic argument, not a proved theorem or automatically a difference between two outer maxima.

The accepted cell-averaging lemma resolves the older note's warning about different adversarial classes. For the grid maximizer A*, which exists, the strict instance transfer gives F_grid=OPT_grid(A*)<OPT_cont(A*)+h<=F_cont+h. The reverse comparison F_cont<=F_grid is the accepted averaging argument. One must select a maximizer to retain strictness; simply taking suprema of strict inequalities is insufficient.

## Certified coarsening

For exact piecewise-constant rational input on a fine partition, integrate its actual rates over a uniform coarse grid of M cells rather than assuming the grids align. A merge of the two ordered partitions computes the coarse cumulative array in O(n(N+M)) rational operations. Cell averaging preserves the exact full discrepancy of every coarse word, so the returned exact coarse minimizer has actual input error U, not just an estimate of that error.

Transfer gives the certified interval (U-h,U] intersected with [0,infinity), where h=T/M. If a code interface clamps the lower bound to0, it is strict exactly when U-h>=0, including equality; when the raw lower is negative, the clamped0 is non-strict. Choosing M=ceil(1/epsilon) gives an additive epsilon*T schedule and certificate. This is an additive approximation scheme, not a relative FPTAS. The joint budget/accuracy dependence is separated from polynomial input dependence; for fixed budget the grid-size exponent is constant.

If a represented input differs from the true cumulative input by at most eta, the interval becomes (U-h-eta,U+eta] intersected with [0,infinity), and the returned schedule's true error is at most U+eta. Its width is at most h+2eta. Direct evaluation on available exact original data can sharpen that upper endpoint. The same bracket certifies a fine-grid optimum only when every coarse switching boundary is an admissible fine-grid boundary. With nonaligned coarse grids, the output remains continuously feasible but need not be fine-grid feasible. A dwell-constrained DP result must not be given this unrestricted transfer certificate because projection can shorten runs.

## Continuous word/time-cell LP formulation

For piecewise-affine cumulative input, fix k=s+1 nominal blocks, a word, and a nondecreasing list of input cells containing the k-1 switching times. At each schedule endpoint, cumulative input is affine in its selected cell and cumulative integer service is linear in the switching times. The two discrepancy inequalities per mode and endpoint, time ordering, and cell bounds are linear. Integer-block monotonicity makes these endpoint inequalities sufficient even if a block crosses input knots.

There are at most n^k words and binomial(N+k-2,k-1) input-cell choices. Unlike the grid DP, continuous k must not be capped at N. Adding0<=E<=T makes each feasible LP compact without changing its optimum. Enumerating all k-tuples of active rows among O(nk) constraints, solving each independent linear system exactly, and checking feasibility is a complete rational method. Degenerate or lower-dimensional feasible polytopes still have vertices with k independent active normals in ambient space. This gives polynomial bit complexity for every fixed k without relying on a floating-point LP oracle. Its role is a small-instance exact benchmark; established switch-time enumeration must be credited and the grid DP has better dependence on the number of modes.

Full manuscript and code review, authorship handoff, and five independent reviews remain pending.

## Handoff audit and independent computation

Read both complete new manuscript sections, the exact coarsener, the full continuous LP implementation, the independent checker, and the source record. The LP discrepancy signs correctly distinguish full and one-sided objectives; k is not capped by input-cell count. Switch endpoints, repeated modes, zero-length blocks, and active-constraint degeneracy are handled consistently. Independently generated 27 rational piecewise-constant inputs over n=2,3,4 and N=1,2,3. A separate exact one-switch solver enumerated ordered mode pairs, solved the increasing/decreasing crossing in each input cell, and compared against the new complete rational LP solver. All 27 optima agree.

The final draft incorporates the suggested sharper non-strict half-width certificates for binary inputs or one switch, and the odd-grid dwell counterexample. Their scope is correct. The implementation deliberately returns the general strict-width certificate, clearly documented. The flow transfer, coarsening, perturbation, and clipping arguments check out independently.

Direct primary-source browsing confirmed Bestehorn–Kirches Corollary 2.7 (uniform supported rounding) and Zeile Section 6.4.3 (prior switching-time enumeration). The author separately records exact final-source locators and PDF hashes for both half-mesh passages.

The 122-file immutable snapshot stage05-round01 has been dispatched to five independent reviewers. Their findings remain pending.

A second independent cross-check solved eight rational one-switch continuous instances on one- and two-cell input partitions for two and three modes, then formed 32 coarse certificates over M=1,2,3,5, including nonaligned grids. Every exact continuous optimum lies inside the returned strict-width certificate and the stronger non-strict half-width interval.
