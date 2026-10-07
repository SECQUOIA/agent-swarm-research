# Stage 2 corrections after round 1

Date: 2026-09-05. Status: all accepted findings implemented and checked; ready for the coordinator to freeze the corrected draft and request a fresh complete review round.

The correction pass read `process/stage02-round01-adjudication.md`, the cited reviewer 11, 02, and 13 reports, the canonical smaller-member refinement, the author's coverage ledger, and the affected proofs and checkers. No subagents were used. No snapshot, literature file, or other paper folder was modified.

## Exact finite coverage: R11-01

`sections/appendix-cubic-certificates.tex`, Table `tab:two-level-small`, now supplies all smaller two-level certificates:

| m | Affine minorant of A binom(C,2)+(5m/4) binom(A,2) | Attaining counts | vex | cav=T | T/H |
| --- | --- | --- | --- | --- | --- |
| 4 | 9A+4C-19 | (2,3) | 11 | 27 | 27/16 |
| 8 | 47A+20C-188 | (4,6) | 120 | 252 | 21/11 |
| 12 | (231/2)A+48C-684 | (6,9) | 441 | 891 | 99/50 |

The proof takes expectations of the affine minorants under any law with the required means. Choosing uniform subsets of the fixed attaining sizes in each group realizes every singleton mean and achieves the bound. The common upper envelope and termwise gap follow from the support counts and monomial envelopes, giving positive hull gaps and the displayed exact ratios. The correction pass independently executed every count inequality with rational arithmetic; the results agree with the coordinator's `verification/two-level-small-refinement.json`.

`thm:cubic-two-level` and its proof now give the completed threshold: among positive multiples of four in the specified family, T/H>2 if and only if m>=16. The exact ratios for m=4,8,12 are below two, the preserved m=16 certificate gives 135/67>2, and the existing lower bound is increasing in m and equals 4617/2300>2 at m=20. This proof makes no claim about minimum dimension over other families or parameterizations.

The printed checker and `verification/check_stage02_finite.py` were extended identically. They preserve all earlier checks and add the 25+81+169 small-member count inequalities, zero minimum slack, attaining values, singleton means, common upper/termwise values, exact ratios, and the threshold comparisons at m=16 and m=20. No floating-point optimization is used.

## Wording, notation, and discoverability

- S02R01-R02-01: changed “contributes less than” to “contributes at most” for the first integral interval in the arbitrary-partition proof. The subsequent geometric sum is still strictly below two.
- R13-M1: defined the positive part of the base-two logarithm for positive arguments before its first use. The separate convention at zero failure-count quantile is preserved.
- Added the explicit analytic m=36 specialization after the proof of `eq:cubic-analytic-finite`: dropping the slack gives 16985/8436>2. The existing stronger positive-slack theorem is unchanged; its value at m=36 is 42462500/21081891, as checked exactly by the symbolic script.

## Printed checker layout: R13-M2

The executable appears in two unbroken `verbatim` blocks inside minipages, separated at the top-level transition from data/function definitions to verification loops. Page 31 holds the new table, explanatory paragraph, imports, data, and function; page 32 holds all loops and final assertions/output. The bibliography begins on page 33. This removes the orphaned import and final success line without reducing code size or changing the executable.

The text explicitly instructs readers to concatenate both blocks. `verification/build_and_check.py` extracts all blocks in order, compares the resulting text byte-for-byte with the executable, records the comparison, and fails on mismatch. Frozen historical reviewer scripts were preserved; scripts that replay the revised printed checker must extract both blocks.

## Validation and preserved scope

- `python verification/check_stage02_finite.py`: passed all original three-group certificates (343+729+274625 states), all 289 original m=16 two-level states, and all 275 new smaller-member states, together with exact primal/dual and envelope checks.
- `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python verification/check_stage02_symbolic.py`: passed the original Bernstein and scalar identity checks, both exact m=36 evaluations, and the positive derivative of the lower bound for positive m. Output: `verification/stage02-symbolic.json`.
- Replayed the concatenated code extracted from the actual revised appendix and verified exact equality with the supplied executable.
- `python verification/build_and_check.py`: clean 33-page compilation, zero warnings, no duplicate labels, and matching printed/executable code. Output: `verification/build-report.json`.
- Visually inspected PDF pages 20, 22, 23, 26, and 30–33. All changed statements, the table, and both complete checker blocks are legible and within the page boundaries. Page renderings are in `verification/stage02-corrections-pages/`.
- Compared the accepted Stage 1 foundations, finite-signing appendix, and macros byte-for-byte with `process/snapshots/stage01-accepted`. Compared the main file, macros, bibliography, and universal-positive section with `process/snapshots/stage02-round01`. All are unchanged. The only modified manuscript sources are the cubic/equal-means section and the two Stage 2 appendices.

`verification/stage02-corrections-validation.json` records the source preservation checks, printed-checker replay, exact/symbolic results, build metadata, and visual inspection. `process/stage-02-author.md` has an appended correction coverage addendum. The historical author record and reviews remain evidence of their respective drafts; this correction record does not replace the required new independent review round.
