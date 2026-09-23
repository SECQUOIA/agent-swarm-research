# Stage 3 first-round adjudication

The coordinator read all five independent reports and inspected the complete
approximation section and appendix. The ten-file source freeze was unchanged
through the review. No reviewer identified a major issue; the coordinator
agrees. The normalization, exact ranges, signed profiles, growing-rank
represented-matroid argument, feasibility counters and bit-complexity proofs
survived independent reconstruction and exact finite checks.

Accepted minor findings:

1. Reviewers 1 and 4: explicitly restrict the focused predecessor reduction to
   scalar observations **and one parameter**, with cardinality only and
   1 <= k <= n. Distinguish infeasible cardinality, empty, and zero-signal cases.
   This clarifies the intended scope; it does not change the main theorem.
2. Reviewer 1: replace “published theorem” with “stated theorem” because the
   inspected and cited Mahalanabis source is the arXiv preprint.

Reviewers 2, 3 and 5 requested no corrections. No finding is rejected or left
unresolved. A separate correction author will address both accepted items.
No second five-reviewer round is required by the protocol because there are
no major findings. Acceptance remains conditional on coordinator verification
of the corrections and a clean build.

The coordinator also independently checked the minimum-gap counter against
exact selected-covariance calculations across 216 constraint families in
`verification/stage03-root/check_cooldown.py`. This and the reviewers' finite
checks supplement the proofs; they are not formal verification or performance
benchmarks. Stage 3 acceptance does not establish completion of later stages.

Final disposition: both corrections were verified in the actual source. Only
the intended appendix changed from the review freeze. The correction author's
clean 36-page build was inspected. Stage 3 is accepted; its source snapshot is
`process/snapshots/stage03-accepted/`.
