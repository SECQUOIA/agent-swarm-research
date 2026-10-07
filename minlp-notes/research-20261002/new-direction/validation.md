# Validation and scope

Date: 2026-10-02.

The main candidate theorem is in
[screening-percolation.md](screening-percolation.md). The independent
mathematical review is in [influence-review.md](influence-review.md).
The reviewer subsequently checked the main note and its graph-specific
extension read-only. No proof error was reported. Clarifications from that
review were applied: input length covers all rational data; threshold ties
are retained to preserve every optimizer; the checker covers negative
penalties with an active zero coordinate; graph certificates use rational
probability upper bounds and a fixed moment parameter greater than two.

The final targeted command was:

    python3 -B research-20261002/new-direction/check_screening.py

It passed 70 rational optimization instances, 5,080 exact principal-support
optimizer bounds, 320 screened coordinates, and objective comparisons
against complete enumeration. Two random instances had several retained
components. Additional exact checks cover threshold-tie retention, negative
penalties with a selected zero coordinate, a branching-process
supersolution, moment divergence above the stated threshold, a heterogeneous
four-cycle certificate against all 16 retention outcomes, and the
fixed-active-center Schur-complement obstruction.

An earlier checker run failed because its illustrative divergence fixture
expected a generating-function iterate to exceed 1,000 after nine levels;
the value was approximately 248.37. Direct inspection showed that the tenth
iterate exceeds 5,095, and the fixture was corrected to use ten levels.
This changed a finite diagnostic threshold, not the theorem or algorithm.

The finite checks do not prove asymptotic expected complexity or novelty.
The proof supplies the complexity claim. External literature assessment was
requested from the parent team's literature agent; no external search or
knowledge-base ingestion was performed in this workstream. No project-wide
checks or CI inspection were run.

The result remains a modest supporting direction. It establishes exact
optimization under a sparse independent candidate set, including graphs of
unbounded treewidth. It does not establish efficient exact optimization for
centered high-disorder penalties with a substantial always-active
background. That harder question remains open in this workstream.
