# Stage 4 correction after round 1

Addressed the sole valid minor finding, R04-1, after reading the primary
adjudication and reviewer 04's source comparison. This is a prose and
source-interpretation correction; no theorem, proof, mathematical value,
verification code, or certificate was changed.

## Exact scope

In `sections/09-three-mode-floor-chambers.tex`, the paragraph after the
seven-cell theorem now states that the exact value `4/3` satisfies the
proposed upper bound `3/2` but refutes the equality asserted in Sager and
Zeile's Conjecture 1. The citation identifies equation (7.6), p.615.

The concluding description of the separate Corollary 5 correction now
refers to the “counterexamples to Conjecture 1” without restricting that
phrase to the earlier many-mode examples. The Corollary 5 lower-bound
correction itself remains unchanged and explicitly separate. The accepted
Section 2 discussion, which correctly says its examples fail even as an
upper bound, was left unchanged.

Updated `verification/stage04/source-record.md` with the equality/upper-bound
distinction, exact source locator, and substitution at three modes, seven
unit cells, and three switches. The nearby verification README makes no
contrary claim and needed no change.

## Source and build validation

Independently read the final [publisher HTML, Conjecture 1, equation (7.6)](https://link.springer.com/article/10.1007/s10589-020-00244-5),
which states an equality. Also retrieved the final publisher PDF in memory
and extracted the corresponding statement on its printed p.615. Its
6,214,094 bytes have SHA-256
`f4dfdfdc761de38dafeea5dd9eafb5bbf3c637a39dc7ee2ff1432a9803996770`,
matching the existing source record. The parameter restrictions hold, and
the second branch evaluates to `7/(2*3+4-3)+1/2=3/2`. The publisher PDF was
not added to the repository.

Clean build command:

```sh
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -cd paper-switching-control/main.tex
```

The build passed, yielding 41 pages. The final LaTeX log has no warnings,
undefined references, or overfull/underfull boxes. Inspected the extracted
paragraph and rendered page 40; the corrected statement, precise citation,
and separate Corollary 5 discussion are readable and fit the text area.
Build evidence is `verification/stage04/corrections-build.log`; the render
is `verification/stage04/corrections-page40.png`.

`git diff --check -- paper-switching-control` passed. All 95 frozen stage 4
round 1 file hashes still match. All other manuscript sections and all
frozen verification code are unchanged; integrity results are in
`verification/stage04/corrections-integrity.log`. No frozen snapshot,
reviewer report, original research source, or accepted earlier section was
edited. No mathematical tests were rerun for this prose-only change.

All assigned work is complete. No stage acceptance or new snapshot was
created by the correction agent. Ready for the primary agent's inspection.

## Final layout correction after primary inspection

The primary agent identified that the longer source citation left the final
two bibliography lines alone on page 41. Shortened the following scope
paragraph to: “The exact continuous three-switch value remains undetermined;
transferring the seven-cell bound gives only $4T/21$.” This preserves its
mathematical qualifications while removing repetition. The new equality
versus upper-bound distinction and its precise source citation remain intact.
No spacing override, theorem change, or code change was introduced.

Rebuilt successfully. The final manuscript has **40 pages**, with the complete
bibliographic entry together on page 40. Inspected the extracted final page
and its updated render, `verification/stage04/corrections-page40.png`; the
paragraphs and full bibliography fit cleanly. The final LaTeX log has no
warnings, undefined references, or overfull/underfull boxes. Build log:
`verification/stage04/corrections-layout-build.log`. This final 40-page build
supersedes the initially reported 41-page build above.
