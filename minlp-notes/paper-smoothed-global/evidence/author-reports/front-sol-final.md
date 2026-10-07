# Final front matter, model, and boundary author response

Date: 2026-10-05. Author: Sol, completing the interrupted Opus revision under
the authorized provider fallback. Ownership is limited to Sections 0, 1, 2,
9 and 10, Appendix G, and this report. All six scientific files are complete.
This is an author handoff, not independent approval of the integrated paper.

I read the original brief, notation, inventory and architecture, the complete
live integration contract and decisions, front-r1, all root model,
introduction and integration-scope reports, the complete frozen boundary
review, the Opus editorial interim and root disposition, the universal-law
report, the preliminary literature account, and the partial Opus mathematical
record. The partial mathematical record has no final verdict and was not
treated as approval. I also read `quadratic-sol-final.md` and
`recourse-sol-final.md` and `sparse-sol-final.md`, and checked their stated
interfaces against the live statements used by the introduction table. I
then read the updated literature-preliminary companion subsection after the
root relayed its verified contracts; the final prose incorporates those
contracts. Remaining bibliography identities and metadata are listed below.

## Responses in the actual text

Locations name this handoff version; labels remain the primary locators.

| Finding | Final location and resolution |
| --- | --- |
| Uniform law and logarithmic native-label format | `02-model.tex:174`, `prop:model:uniform`, cites `cor:count:universal-law` and `app:count:universal` instead of duplicating their proof. The proof explicitly bounds `log(s+1)` and logarithms of base format/degree multipliers, separately from added-bit coefficient height and `B poly_d(I+b+q)` work. `P,A,D` are positive integer-valued envelopes. |
| Gaussian support and uniformization qualifications | `prop:model:uniform` retains the support/box/cap recomputation and the supplied `k<=K` flow/TU budget. Its following paragraph preserves geometric and oracle qualifications and the iterated-squaring width example. Strong-field `q_i` and beta are recomputed, rather than asserted monotone. |
| Output fixing and feasibility | `02-model.tex:304`, `def:model:outputs`, includes sound singleton-hull continuous fixing separately from original-bound fixing. Charted outputs retain exact algebraic lifts; the evaluation paragraph handles point patches directly. The domain paragraph expressly assumes nonemptiness or an explicit feasibility branch. |
| Common-root output and fallback size | The algebraic item lists one root for every continuous optimizer coordinate and its value, with native labels explicit. `02-model.tex:370` states fallback length/refinement `B poly_d(I+b+q)`. Component values remain a symbolic sum; unrelated exact sum comparisons are not promised. |
| Rational quadratic output scope | `01-introduction.tex:201` restricts rational QP output to rational box/polyhedral classes. Its graph/domain table row says charted or implicit. The model states why an implicit graph can lack any fully rational feasible point. |
| Common invariant and count qualifications | `sec:intro:mechanism` gives valid curvature bounds and noise comparisons as the common invariant. Fixed residual feasibility is the direct recourse premise; charts and order transport supply proved replacements. The count paragraph charges certified evaluation error and limits the direct independence product to the appropriate box/core/aligned arguments, with directional/transport and ambient volume variants explicit. |
| Turing and noise-coordinate distinctions | `sec:model:noise` says bounded worst-case random bits force finite support, while countably supported rational laws can be Turing-sampled. `10-discussion.tex:5` assigns independence to the perturbation coordinates, including independent xi with correlated original aligned coefficients. The grid symbol is uniformly `U_{sigma,M}`. |
| Original-objective accuracy | `02-model.tex:470` defines `W_noise` for ambient/core coordinate widths and aligned row widths and retains row-specific scale sums. It treats `W_noise=0` separately. For Gaussian-like noise it uses exactly `(b+20)sigma`, a nonnegative least dyadic exponent satisfying an effective polynomial envelope, `R=max(1,W_noise/epsilon)`, positive logarithms and `1/sigma<=R poly(I0+log R+1)`. The work substitution retains all numerical factors. Introduction and discussion restrict arbitrary-accuracy calibration to routes valid at every positive scale; strong fields keep only their available regret bound. |
| B10 proof ownership | `09-boundaries.tex:296`, `prop:lim:conditional`, is now a short corollary of the substantive `prop:sp:conditional` and `eq:sp:conditional`. It retains its old result and item labels. The duplicated conditional-recourse proof is removed. The sparse author owns the feasible-upper/certified-error/retention proof. |
| Width barrier scope and P2 moment qualification | Introduction, boundary discussion and `sec:disc:open` say certified conditional values are one sufficient interface for this search, not necessary for every width-FPT algorithm. The discussion explains that a linear small-growth tail leaves a cutoff factor `K^(1-1/r)` for generic inverse-growth powers `r>1`; it makes no algorithmic impossibility claim. The front companion paragraph now gives the verified weighted versus point-growth ratios, the actual f(p,t) formula and input exponent 5, sharp filtered-uniform versus graded counts, and the rETH restriction to the product-time model. It does not claim a matching p/2 lower bound or a smoothed lower bound. |
| Square Root Sum versus PosSLP structure | `tab:lim:summary`, the introduction's boundary paragraph, `thm:lim:posslp`, and its discussion restrict treewidth two and bounded coefficient magnitudes to Square Root Sum part (a). Part (b) has neither restriction. The reviewed direct six-lemma proof remains intact. |
| Positive amplifier modulus | `G-boundaries.tex:211`, `lem:lim:amplifier`, now expressly assumes `mu_0>0`. Its reviewed constants and proof are retained. |
| DK construction and worked threshold gap | `rem:lim:dk` says binary penalties `x_i(1-x_i)` plus residual squares, retaining the explicit A=2^r, items A and A+2, target A+1 witness and gap `2^(-2r-4)`. `prop:lim:threshold` retains delta>=0 and its narrow threshold-reading scope. The exact source locator is a Luna dependency. |
| P1: complete arithmetic overlap and degree distinction | `sec:intro:prior`, `sec:lim:points`, the paragraph after `thm:lim:posslp`, and `G-boundaries.tex:179` attribute all three point-obstruction parts, including noisy-core (c), to the exact-arithmetic companion. They include its positive residual-convex cubic point theorem and supplied-convexifier theorem at the cubic/polytope or fixed-degree/global-convexity scope. The updated introduction also describes its canonical selector and common per-draw Omega factor for all q; these already appear in that companion. Finite patch-plus-proof output is distinguished from its Cauchy-name interface without claiming a new time bound from format alone. They identify degree four as the general obstruction and a modulus as sufficient rather than necessary. |
| Convexifier versus direct numerical scale | `sec:lim:rank` retains the rank-at-most-k Schur convexifier caveat, distinguishes the merely convex rank-separation family, and compares sufficient scale `M+M^2/mu` with the direct count's original `L/sigma`. The recourse final report supplies the concrete two-variable example. |
| P3: indicator-only noise | `sec:intro:prior` names the sparse-indicator companion, its independent grid noise only on binary indicator penalties, exact every-draw fixed-width result, and numerical-dependence obstruction. It distinguishes this from ambient-coordinate smoothing and arbitrary affine feasibility. |
| P4: FPT numerical parameters | The abstract, table caption/rows, model parameter subsection, introduction explanations and discussion make FPT joint in structure and the displayed numerical ratios, or in structure for fixed bounded ratios. They explicitly say a polynomially growing ratio gives `I^{O(k)}`, rather than structure-only FPT. |
| P5: applications | Discussion applies uncertain-cost interpretations only to the actual constructed law and hypotheses. The two-stage example permits core-dependent residual costs with fixed residual feasibility; it excludes general second-stage constraint coupling. |
| P5: strong-field scale | Introduction cites `eq:int:sf-regime`; discussion discloses conservative `c_d=2^{10000D}` and contrasts quadratic continuous weight a_i=3. No practical impossibility or speedup is inferred. Lattice and component routes are consistently distinguished from rare-fallback routes. |
| Final separable-class distinction | The introduction body and two table rows now distinguish rational-breakpoint convex piecewise-quadratic unaries in `thm:qp:sep/sep-gauss` from the fixed-degree piecewise-polynomial unaries allowed by pure-integer `thm:int:lowrank`. No rational continuous polynomial output is inferred from the lattice extension. |
| X16 integration | The recourse final report and live `cor:int:grid` now contain the deterministic core-grid error `kL/(8m^2)` plus oracle error, with proof in Appendix F. This bridge is no longer missing; it requires no duplicate front theorem. |

No substantive reviewed ambient-count, direct Square Root Sum, PosSLP,
regularization, sparse-width, affine-hardness or boundary-flow construction
was replaced. The new author work repairs statements, attribution and shared
interfaces; it does not substitute numerical diagnostics for their proofs.

## Targeted checks actually run

1. Scoped reads/searches and analytical checks of the corrected contracts,
   Gaussian calibration, format-versus-height distinction, degree/output
   scopes and cited live theorem interfaces.
2. An inline `python3 -` check restricted validation to the six assigned TeX
   files: final newlines, trailing whitespace, control characters,
   environment nesting, paired display delimiters, 92 unique local labels,
   all references used by these files against the live dependency labels,
   positive amplifier modulus, projected calibration expression, shared
   universal-law citation and removal of `BasuLerario2023`. Passed. The
   dependency scan did not validate unrelated chapters.
3. A six-file scratch harness at `/tmp/sgfront-sol-final-check` contains only
   the assigned files and external-label stubs, using the current preamble
   and macros. Nine required build passes ran
   `pdflatex -interaction=nonstopmode -halt-on-error main.tex` in that
   directory: initial reference resolution and subsequent changed-table
   validation/resolution, followed by two passes after the final verified
   companion-prose integration. The last pass produced a 39-page PDF with no TeX
   errors, unresolved cross-references, overfull boxes, oversized floats,
   font warnings or rerun warning. The first table was 19 pt too tall;
   the required piecewise-quadratic qualification later made it 3.3 pt too
   tall. Compact caption/row text repaired both without reducing fonts or
   deleting mathematical scopes. Expected undefined-citation warnings
   remain because the harness deliberately has no bibliography.
4. `pdftotext -f 4 -l 7 -layout main.pdf table.txt` inspected the results
   table and adjacent mechanism prose in the scratch PDF; the complete
   table fits on its own page.
5. `git diff --check -- paper-smoothed-global/sections/00-abstract.tex
   paper-smoothed-global/sections/01-introduction.tex
   paper-smoothed-global/sections/02-model.tex
   paper-smoothed-global/sections/09-boundaries.tex
   paper-smoothed-global/sections/10-discussion.tex
   paper-smoothed-global/appendices/G-boundaries.tex` passed.

These are targeted author checks, not CI checks or project-wide verification.
No CI status/log, literature search, experiment, saved proof diagnostic,
historical edit, commit, publication or delegation was performed. No other
author's scientific file was edited.

## Citation requests and remaining reconciliation

The literature owner must finish identities and theorem scopes; the
preliminary account is evidence for the new citations, not final citation
closure. The front files use these newly incorporated verified-preliminary
comparators:

- `soltanalian2026-random-parameter-noise-does-not`: negative exact ReLU
  verification boundary for independent clipped Gaussian parameter noise
  rounded to finite dyadic grids, uniformly over adversarial bases.
- `khajavirad2026-a-polynomial-time-solvable-class`: deterministic exact
  sparse-box class, with the rational-bit quadratic versus algebraic-RAM
  higher-degree distinction.
- `ari2026-curvature-batching-for-integer-and`,
  `ari2026-bounded-integer-quadratic-programming-through`, and
  `wei2026-integer-quadratic-programming-in-fixed`: the separate mixed,
  bounded pure-integer and fixed-integer-dimension deterministic comparisons.
- `pia2026-rational-jacobi-rotations-and-the`: approximation, not exact
  indefinite MIQP optimization.
- `tndel2003-an-algorithm-for-multi-parametric`: established critical-region
  machinery without a polynomial region-count claim.
- `mulmuley1987-matching-is-as-easy-as` and
  `beier2022-the-smoothed-number-of-pareto`: discrete isolation/Pareto
  precedents, distinguished from continuous global growth and atomic-grid
  transfer.
- `basu2021-hausdorff-approximations-and-volume-of`: the read primary source;
  the provisional/unread-journal `BasuLerario2023` is removed here.

All inherited exact-convex-QP, GLS, Renegar, algebraic, genericity,
Hochbaum--Shanthikumar, Allender et al., and treewidth-hardness citations
still require the root/Luna final bibliography audit. In particular,
`pardalos1991-quadratic-programming-with-one` was explicitly unresolved by
preliminary literature intake; the opening hardness claim must not be
counted verified until Luna resolves it or the root narrows it.

Exact remaining reconciliation:

1. All three other final author reports have been read. The B10 front
   corollary imports the final sparse error allowance eta_j<=a e_j, its
   feasible returned-completion witnesses, and its count with unchanged
   labels. Quadratic and recourse output/precision interfaces match the
   introductory table.
2. The updated Luna evidence verifies the mathematical companion scopes now
   incorporated in the introduction and discussion: cubic selector and
   common per-draw factor for all q, convexifier degree/domain distinction,
   weighted versus point-growth parameters, the actual graded-grid work
   formula, sharp filtered-uniform count, the restricted rETH product model,
   and indicator-only grid noise with its numerical obstruction. Companion
   authorship/version metadata and final bibliography entries remain with
   the root/Luna audit; they are not asserted closed by this author.
3. The root must complete bibliography, integrated layout and independent
   review of these live edits. The frozen r1 boundary review alone does not
   approve them. The root is separately reconciling the sparse comparison
   with the same final verified companion contracts.

## Final source hashes

| File | SHA-256 |
| --- | --- |
| `sections/00-abstract.tex` | `2b1dd7bfef41dd05d68d527afcba9c1526ce5b4ca243d96d926f63b2236bfbc2` |
| `sections/01-introduction.tex` | `c3b27472e13d0c6a94d1cb6693d264d6ac0f6137c7e64d039bc613eb3d35ba56` |
| `sections/02-model.tex` | `0a9267cd7a893497d212e5ccb0fbb6433b6428c4784793dd9fc79ec4f4e38a63` |
| `sections/09-boundaries.tex` | `1acb7217806f6e53e27a653e9ca36df3adfa3d37cc25a428b45c4770cb8e7bf8` |
| `sections/10-discussion.tex` | `d1e176dc2598a40d80d9bc6e13773cd634a713cd6f8e236d5b6e992ebfc49c56` |
| `appendices/G-boundaries.tex` | `163333352717c3b090f62924f8a8b90eea63cf7c4fc50bf1da0dafd4556f1553` |
