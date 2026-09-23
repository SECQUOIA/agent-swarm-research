# Stage 4b final corrections

All three minor repairs accepted in `completion-s4b-adjudication.md` are applied. No theorem statement, algorithmic scope, or substantive result was added.

## Changes

1. **C1: threshold dual degeneracy.** In the proof of `lem:a-wcac-threshold`, the distinct listed edge weights now partition the real line, regardless of whether they are actual breakpoints of the dual. Affinity on each interval and tail, together with the dual's lower bound, gives a minimizing listed weight. The proof explicitly includes a globally constant dual with nonzero flows. The threshold construction, recovery rule, and candidate lemma are unchanged.
2. **C2: zero-objective face output.** In the proof of `thm:a-wcac-faces`, the `c=0` branch starts at all nomination lower bounds and fills coordinates in a fixed order until balance holds. All but at most one coordinate are at endpoints. Fixing those coordinates and retaining the possible remaining interval with exact balance produces the promised rational face, with at most one unfixed coordinate and polynomial encoding length.
3. **C3: Vigneron manuscript locator.** The existing bibliography key `vigneron2014-geometric-optimization-and-sums-of` retains its journal metadata and DOI. Its URL now points to `https://antoinevigneron.github.io/manuscripts/rational.pdf`, and its note identifies the October 21, 2011 author manuscript as the version used for theorem and section locators. The section's source paragraph states that date explicitly. The date follows the lead's independent PDF verification recorded in the adjudication; this correction did not repeat that source audit.

## Checks

- Read the accepted corrections and the surrounding face and threshold proofs. For C1, the review example `f=(1,-1)`, `w=(0,1)`, `L=U=(1,1)` has constant dual value `-1`; either listed weight is covered by the revised argument. For C2, box feasibility ensures that the residual from the lower bounds is nonnegative and no greater than total interval capacity. Sequential filling therefore terminates with balance and at most one interior coordinate, including singleton and boundary cases.
- Imported `verification/build_and_check.py` and called only `build('complexity')`. This ran `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex` in `complexity`. Paper B was not built.
- Refreshed `completion-s4b-build.json` with the existing schema and all 14 Paper A input SHA-256 hashes. Independently recomputed each hash after the build and verified that all 14 match.
- The build returned zero, produced the PDF, and reported no errors, undefined references, undefined citations, duplicate labels, or overfull boxes.
- Compared source hashes before and after correction across both papers. Only `complexity/sections/07-weighted-cactus.tex` and `complexity/references.bib` changed. All other Paper A sources and all Paper B sources were preserved. No plan, coverage, or adjudication file was edited, and no commit was made.

## Limits

These are local proof and citation repairs. This correction pass did not repeat the five independent reviews, rerun the numerical regression suite, or claim that the clean build verifies the mathematical results. The existing implementation and theorem scope limitations remain unchanged. Final acceptance remains with the lead.
