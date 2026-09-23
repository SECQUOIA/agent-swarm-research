# Stage 2, round 1: primary-agent adjudication

The primary agent read all five independent reports and all new manuscript sections. All five reviewers found no major mathematical issue. All five ultimately requested no correction; reviewer 01 initially reported, then withdrew, a heading-margin issue after checking the actual PDF coordinates. Independent checks include exact all-cell primal/dual optimization, independent Fourier–Motzkin elimination, exact reordering enumeration, direct control-to-event embeddings, and an independently reconstructed symbolic certificate argument. These strengthen the written proof audit without substituting finite tests for universal proofs.

## Findings

1. **Root finding, valid minor:** the quotient-size sentence in `04-four-block-certificates.tex` must specify n>=9. The quoted inequality range 151–826 holds for the stabilized symbolic topology; n=5 can have 148 rows. This is descriptive scope, not an error in the certificate or coverage proof. Correct it.
2. **Reviewer 01 M1, not substantiated in the frozen PDF:** the primary agent viewed the actual frozen page-18 rendering and extracted text bounding boxes from the frozen `main.pdf`. The heading's final word ends at x=513.074727 pt, within the ordinary body-text extent x=513.502290 pt. The supplied rendering likewise fits. Thus the reported overrun is not accepted as an existing layout defect; reviewer 01 independently confirmed these coordinates, withdrew M1, and amended the report. The initial pixel estimate was unsupported. A shorter heading is still a reasonable editorial choice during the substantive revision below.

No valid major criticism was identified. All accepted stage 1 mathematics remains unaffected.

## Additional development requiring a fresh review

Reviewer 02 independently established the exact one-sided instance optimum 18673/18396 for the three-mode example, using exact primal and dual certificates for all 972 word/time cells. The primary agent then derived a short analytic proof, independently confirmed by reviewer 02. We will develop it now, before accepting stage 2, instead of leaving only a weaker strict lower claim.

Let delta=E-1 and delta*=277/18396. Since all allocation slopes are <=3/4, each inverse reach is 4-Lipschitz in its right-hand side. Relative to threshold one, first reaches increase by at most 4delta and pair reaches by at most 20delta. Every distinct triple originally ends at t*=971/146. Its last complement has slope 2/3 on the uniform extension, hence its reach is at most t*+(63/2)delta. This is below L=57/8 for 0<=delta<delta*. Word 021 attains L at delta*: its first and second inverse roots remain in slope-1/4 complement intervals, giving endpoints 8341/4599 and 17639/4599 exactly, followed by the uniform suffix.

Repeated words remain impossible at E*=1+delta*. Terminal support still forces {0,1}, since both masses exceed 2E*. The first pair endpoint is at most M2+20delta*, and the global allocation slope <=3/4 bounds middle service by M2-Rp+16delta*. The necessary terminal service bound drops by only delta*. The old gaps minus17delta* are 2923/4599 and 4372/4599, both positive. Feasibility is monotone in E, so exclusion at E* excludes lower thresholds too. For distinct words the sensitivity proof is scoped to 1<=E<=E*; threshold one already excludes smaller E. This yields the exact instance optimum analytically, with a matching schedule.

A different correction agent will independently derive this argument, revise the proposition and verification, and fix the valid minor count scope. Because the mathematical statement is substantially strengthened, the revised stage will receive another five independent reviews even though the first round found no major criticism. No stage acceptance is recorded yet.
