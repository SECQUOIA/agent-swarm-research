# Independent review 04: stage 6, round 1

**Verdict: no major issues and no valid minor issues identified. Accept this authoring/integration stage and proceed to the separate full-manuscript proof review.**

I reviewed the immutable `stage06-round01` draft: abstract, introduction, computations, discussion, the new classical small-mode consequence, relocation of the higher-reach material, bibliography, figures/tables, verification scripts, README, and the allowed coverage map and inventory. I consulted accepted proofs where needed to check the scope of the new statements. I did not read other current reviews or author/root assessments, confer with reviewers, delegate, or edit the manuscript or snapshot.

## Mathematical scope and integration

**Headline formula and abstract (`main.tex`; `00-introduction.tex:25–102`).** The formula retains the correct range `0 <= s <= 3`, `n >= s+2`. I checked the no-switch case, the uniform one-sided term, and the distinction between the supported plateau witness and the all-mode uniform witness. The transition mode counts 5, 8, and 12 agree with exact rational comparisons. The figure displays only the stated integer-mode ranges and distinguishes the full minimax from the geometric one-sided term. The asymptotic expansion has the necessary fixed-block-count qualification. The heavy reduction, spare-mode hypothesis, exact three-mode boundary value, unresolved three-switch boundary band, and one-chamber scope of the higher-reach certificate are described consistently with the accepted results.

The introduction and abstract separate supplied-input optimization, minimax values, and discretization error. They do not promote the sharp instance-transfer coefficient to a sharp difference of minimax values. Algorithmic arithmetic costs retain their fixed-budget qualifications; no unsupported general efficiency or nonlinear-control guarantee is added.

**Preservation of accepted mathematics.** I compared the new source directly with `stage05-accepted`. Files 01–06 and 08–11 are byte-for-byte unchanged. The higher-reach text removed from file 07 is preserved verbatim in file 14, apart from surrounding whitespace, and is now placed after `\appendix`. The remaining change to file 07 is the explicitly attributed classical bound. Its movement changes neither the relaxation's feasible set nor the certificate claim. The unresolved weighted premise and the distinction between interpolated event allocations and actual inverse-reach events remain explicit.

**New classical consequence (`07-predecessors-and-frontier.tex`, `eq:classical-small-mode`).** The source states an unrestricted-grid CIA bound `(2n-3)/(2n-2)` times the largest cell width for all grid lengths. Its separate condition `N >= n-1` concerns tightness, not validity. Applying the bound to the averages on `k` equal cells produces at most `k-1` switches and preserves discrepancy for the original measurable input. Hence the new hard-budget upper bound is valid for every stated `n,k`. I independently simplified its comparison with `T/(k+1)`: it improves that bound precisely when `k > 2n-3`. This supports the stated sufficient-large-budget comparison. No hard-budget tightness is inferred from the source.

**Uniform continuous comparison (`12-computations.tex:103–119`).** The direct lower proof is valid: a schedule omitting a mode has error at least `1/3`; otherwise three blocks use all three labels once. The last mode's starting and terminal discrepancies give `max(v/3,2/3-v) >= 1/6`. The displayed schedule with switches at `1/4` and `1/2` attains `1/6`. This correctly supplies a proof outside the earlier theorem's `k<n` hypothesis.

**Discussion and coverage.** The discussion accurately separates complete theorems from substantial open questions. It does not imply that the nonphysical event assignment refutes a reach theorem or that one ordered chamber settles all chronological orders. Its constrained-coarsening discussion agrees with the dwell obstruction. The coverage map accounts for the substantive repository result families, including retained input-dependent predecessors, strengthened counterexamples, specialized results subsumed by later theorems, and archived verification artifacts. I found no unsupported omission or promoted conjecture in the new synthesis. This integration audit does not replace the separately planned full-proof review.

## Independent public-data reconstruction

I downloaded the CSV at the exact pinned commit to my own verification directory and independently verified its SHA-256:

`1ed44f0906dfe71654a2f263d354ee0046ae6211baa1ddfd4b5945293c900883`.

My `independent_public.py` imports no manuscript algorithm or checker. It parses the decimals as rationals, performs normalization and largest-remainder quantization independently, and then uses integer cumulative masses in units of `10^-9` for grid calculations.

The reconstruction confirmed:

- 12,000 cells of width `1/1000`, horizon 12, and three nonnegative rates per row;
- the exact archived maximum normalization and quantization errors, and the printed strict bounds on both;
- every integrated mass in all three archived coarse grids, reconstructed directly from the source;
- all six continuous ordered-pair crossings, with each candidate evaluated independently at every original input knot and its switch;
- the continuous optimum and attaining time `4721469/2500000 = 1.8885876`, with zero-based mode order `(1,2)`, corresponding to manuscript modes two and three;
- the fine-grid optimum `1889/1000`, found by an independent scan of all pairs and all internal boundaries, and the exact gap `1031/2500000 < 1/2000`.

The crossing argument used in the manuscript (`12-computations.tex:36–50`) is complete: the increasing and decreasing terms cross, their maximum is minimized there, and the omitted-mass term is constant. Constant schedules cannot improve on all crossing candidates, since they are endpoint choices of the same pair families. The verification code handles these endpoints.

I additionally enumerated actual runs, requiring adjacent labels to differ and including all shorter schedules, on **all three public switching grids and all four budgets**. This provides an independent check even for the 48-cell entries, beyond the manuscript's stated independent enumeration on 12 and 24 cells. The 12 comparisons covered **470,454 candidate schedules**, with safe early pruning by attained prefix discrepancy. Every optimum matched the archive. Every archived schedule was also checked against all 12,000 original input endpoints.

In particular, the three-switch values are:

| Allowed cells | Independently verified exact optimum |
|---:|---:|
| 12 | `1067507/1250000 = 0.8540056` |
| 24 | `2631679/5000000 = 0.5263358` |
| 48 | `10526709/20000000 = 0.52633545` |

Thus the observation about the much smaller improvement from 24 to 48 cells is accurate. The same grid is used across budgets in each table row; no comparison silently changes the feasible budget.

## Certificates, computations, and figures

**Certificate table (`12-computations.tex:78–101`).** All coarse grids divide the fine grid, so every coarse schedule is fine-grid feasible. The intervals therefore enclose both the continuous and fine-grid optima. I checked all printed endpoints and the strictness flags directly from the independently verified coarse values. In particular, the 12-cell, three-switch lower endpoint is clipped to zero and correctly closed; positive general lower endpoints remain open. The instructions for the normalized decimal source use the *unclipped* lower endpoint before applying perturbation and clipping, so they preserve the correct endpoint convention. The manuscript explicitly distinguishes the normalized source from the unnormalized columns.

The conservative cumulative perturbation bound follows from the verified strict componentwise rate bound over the fixed horizon. I did not independently reconstruct the very large exact fraction recording the maximum actual cumulative perturbation; it is unnecessary for the printed conservative certificate and is checked by the source-reproduction script.

**Uniform figure.** I independently reduced every displayed uniform three-mode grid problem to two distinct boundaries. Any repeated-label word omits a mode and costs at least `1/3`, while all displayed distinct-word optima are smaller. Direct integer endpoint formulas then reproduced all nine plotted values, including `M=4: 1/6`, `M=5: 1/5`, and `M=9: 5/27`. The nonnested-grid qualification is necessary and correctly stated. Both figures identify their discrete cases, relevant input, and objective; their connecting lines are not presented as continuous-grid laws.

**Timings (`12-computations.tex:131–190`).** I checked every stored CPU and wall median against its three samples: 26 timing records matched exactly. The generated table values and timing macros passed the supplied exact text check. The archive identifies the machine and Python environment, and the code's timer boundaries match the described input preparation, solver validation, and post-solve verification scope. Comparisons use the same input, objective, grid, and switch budget. The manuscript does not assert superiority to established external solvers, and it does not treat the timing table as proof of asymptotic complexity. Past hardware utilization and elapsed measurements cannot be independently recreated; their descriptive status is made explicit.

## Literature verification

I read the literature-folder instructions and checked the relevant primary passages. The source comparisons are appropriately limited and do not assert exhaustive priority.

- The publisher abstract of [Sager–Jung–Kirches (2011)](https://link.springer.com/article/10.1007/s00186-011-0355-4) supports attribution of the switch-constrained NLP/MILP decomposition and tailored branch-and-bound method.
- I checked Knuth's local primary manuscript, pp. 1–3, including its integer-flow partial-sum construction. The introduction uses it as general historical context, without identifying its problem with the hard-budget minimax problem.
- I checked [Zeile–Robuschi–Sager, Corollary 1, p. 669](https://link.springer.com/article/10.1007/s10107-020-01533-x) in both publisher HTML and the original rendered PDF. The constant and the separate tightness restriction match the new consequence.
- The primary publisher preview for [Abbasi-Esfeden et al. (2025)](https://www.sciencedirect.com/science/article/abs/pii/S0959152425001507) explicitly states the loss of optimal substructure and the absence of a general global-optimality guarantee. This supports the introduction's methodological comparison. Direct page opening failed, but the indexed primary preview supplied the complete introduction; I did not retrieve or audit the full algorithmic paper.
- The local primary texts support the cited tight SUR setting, compactness/convergence context, and adaptive SCARP refinement. The adaptive citation is explicitly to the inspected preprint. The regularity-qualified state-error interpretation agrees with Zeile–Weber–Sager, Theorem 1 and Corollary 1, pp. 8–9.

The source claims already reviewed in stages 4 and 5 are unchanged. The introduction preserves the distinction among a false conjectured equality, a failed upper-bound claim, a failed lower-bound claim, and the separate half-mesh instance argument.

## Portable verification and limitations

All **161 snapshot manifest hashes** matched before the audit and again afterward. I ran the entire `verification/run_all.py` suite offline in a relocated copy; every proof, integrity, algorithm, and archived-experiment suite passed. I ran `latexmk -C` followed by a clean PDF build in that copy. The build succeeded with 56 pages, and its final log had no undefined-reference or overfull warning. The clean PDF's extracted text matches the frozen PDF exactly. I inspected introductory renderings and clean-build computation/table pages; I did not conduct a separate pixel-by-pixel audit of every page.

Artifacts are confined to `verification/reviewer04/stage06-round01/`, including `independent_public.py`, `independent-public.log`, `uniform-independent.log`, `preservation.log`, `integrity.log`, `offline-runner.log`, and `clean-build.log`. A mistaken initial working-directory command failed before running a checker; its error log was moved into this directory, and the correctly relocated run subsequently passed. No source or snapshot file was changed.

I independently reconstructed the fine source and all reported public exact values rather than rerunning the complete timed `experiments.py` experiment. The offline runner covered its documented archived-data scope. I did not repeat all accepted mathematical proofs or perform an exhaustive new literature search; those limits do not reveal an unresolved claim in this stage.

**Final recommendation: accept stage 6 round 1; no corrections requested.**
