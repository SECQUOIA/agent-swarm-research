# Stage 4, round 1 — independent reviewer 3

## Verdict

**PASS subject to three minor clarifications. No major issue found.** The integrated introduction, literature comparisons, conclusion, and verification appendix accurately position the accepted mathematical results. I verified the 22 frozen-input hashes, read the stage-4 author scope report, and did not consult another stage-4 review. No manuscript sources were edited.

## Required minor corrections

1. **Say that the prescribed girth is a lower bound.** `main.tex:21` and `README.md:5–6` say “any prescribed fixed girth.” The theorem proves girth at least a prescribed constant; it does not prescribe an exact girth (which could not be an odd number in a bipartite graph). Use “girth at least any prescribed fixed constant” or “any prescribed fixed lower bound on girth.” The introduction and actual theorem already make the correct lower-bound statement.
2. **State the Python minimum.** `README.md:30` says to run the suites “with Python 3.” `checks/check_resistive_exact.py:27` evaluates the annotation `str | None`, requiring Python 3.10 or newer. The developments suite imports this module. Specify “Python 3.10 or newer” in the README so the reproducibility requirements are complete. No code compatibility layer is needed.
3. **Use absolute principal angle in the check count.** In `appendices/verification.tex`, the AC paragraph describes “768 whose principal angle exceeds pi/2.” The checker counts `dot(a,b)<0`, including both positive and negative oriented principal differences. Write “768 whose absolute principal angle exceeds pi/2,” or describe short-arc length instead. The count itself is correct.

## Integration and source checks

- The rational-universality summaries now retain “defined over Q,” and the distinction from arbitrary compact semialgebraic topology is consistent throughout. The introduction does not revive the rejected general rational-universality claim.
- The three AC input conventions are distinguished, including real bus-angle consistency, principal-angle winding, and reference-fixed boxes. The size-dependent cosine data are explicitly separated from the fixed-data resistive construction. The conclusion does not claim symmetric-tolerance hardness or exact NP membership.
- The introduction states independent voltage/injection singleton bounds and does not conflate the model with conventional load-only feasibility, the linear DC approximation, or lossless fixed-magnitude AC models.
- [Gan–Low's primary abstract](https://authors.library.caltech.edu/records/zf7qf-8jb24) confirms the conditional SOCP exactness statements involving voltage upper bounds and injection lower bounds. The manuscript attributes sufficient conditions rather than unconditional exactness.
- I checked Jeeninga–De Persis–van der Schaft in the repository: the model fixes source voltages, allows constant-power demands at variable-voltage load buses without the manuscript's full operational intervals, and Theorem 3.22 gives both exact-feasibility and interior alternatives. The introduction correctly preserves both claims, distinguishes the demand set from the voltage set, and does not infer an exact polynomial-time Turing algorithm.
- The archived Lehmann–Grastien–Van Hentenryck proof fixes unit magnitudes and reduces to a star. The Bienstock–Verma full text uses lossless lines with unconstrained reactive power. Both comparisons are accurate. The separate version-specific Bienstock–Verma entry supports the Section 1.3 locator without assigning that numbering to the journal article.
- The repository's Bienstock–Muñoz Theorem 7 and Corollary 8 use scaled feasibility/optimality tolerance, as the introduction states. This is properly separated from exact decision and from the manuscript's particular gap-promise certificate result.
- I downloaded and read [Lavaei–Low's primary Appendix B, Case 2](https://smart.caltech.edu/papers/zeroduality.pdf). Its real-admittance/zero-reactive connection supports the narrow attribution. The manuscript does not adopt the source's unrestricted discrete-phase conclusion; it proves its own real-lift result and describes the winding obstruction. The cited sine-coupling connection was independently verified in stage 2 and remains unchanged.
- The remaining source-dependent mathematical statements and locators remain those accepted in the prior corrected stage. A hash comparison confirms that, among accepted sections/checkers/appendices/macros, only section 06 changed, by its version-specific bibliography key.

## Verification appendix and packaging

All eight listed source systems match the legacy script. I independently checked their equations and interval consequences: six have the stated unique positive bounded solution, and the two contradictions are valid. The two irrational outcomes have the correct square-root formulas. The unique-network-extension conclusion follows from the accepted bijection.

The four historical AC sizes and the bound on the sum of squared imaginary voltages agree with the repository's result and audit records. They are correctly described as historical solver reports; the manuscript does not say the solver was rerun or promote floating point upper bounds to exact certificates.

The four paper-local suites' counts agree with the unchanged programs and the independent runs recorded in my previous stages. I separately reran the legacy winding checker in this review: **360 scaled pairs, 4,136 cycles, 256 nonzero windings**, all passing. The verification appendix distinguishes finite sample coverage from quantified proofs and explicitly excludes inference of planarity, universality, or spectral theorems from sampling.

The coverage map accounts for corrected historical claims and duplicated worktree sources rather than presenting them as additional theorems. README commands and paths match the package, subject to the Python-version clarification above. Ignoring generated builds and diagnostic images does not exclude manuscript sources, checker code, or review reports.

A separate `latexmk` build succeeds in `verification/reviewer3/stage04-round01/build/`, with no final warnings or overfull/underfull reports. I rendered and inspected page 27: the eight-example table, equations, exact outcomes, and historical-evidence paragraph fit without clipping and are readable. Build output, extracted manuscript layout, rendered page, and the downloaded primary-source PDF/text are retained in my verification directory.

## Optional suggestions

None required for this stage. The planned separate whole-manuscript review remains the appropriate final integration check.
