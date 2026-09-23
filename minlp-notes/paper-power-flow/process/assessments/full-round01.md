# Root assessment: whole-manuscript review, round 1

Read all five complete independent reports. Every reviewer rechecked the
entire manuscript and finds no major mathematical or scientific issue.
Reviewer 1 has no required finding. Reviewers 2–5 independently identify
the same minor composition omission, which root also noticed and accepts.
No reviewer finds a missing in-scope development or required new research.

## Accepted minor: connected principal transfer of the trivial source

The zero-variable arithmetic source maps to a one-bus connected RPF point.
The principal-window transfer requires n>=2 and its general isolated-bus
padding would lose connectedness if imported literally into the structural
AC corollary. Hardness is unaffected, but the uniform composition needs an
explicit trivial-case image.

Correct the proof of cor:structural-ac: every construction starting with a
named arithmetic variable already has at least two buses after connection
and subdivision, so apply the principal transfer without padding there.
For the zero-variable source, use two voltage-1 buses with zero active and
reactive injections joined by one unit-conductance edge, with c_2=3/4.
This connected simple planar bipartite graph has degree one and infinite
girth, preserves the singleton magnitude set, and uses permitted interval
data. Qualify the graph-unchanged statement for this explicit exception.
The ordinary reduction, RPF empty-source convention, real-angle and box
transfers, and checker code need no change.

## Whole-paper judgment and verification

Root independently audited the complete proof sequence, repaired arithmetic,
source scopes, eight analytic examples, numerical estimates, and package.
All four exact suites were freshly rerun by root with exit zero; logs are
verification/root/full-*.log. The reviewers also supplied distinct whole-
graph lift, boundary, symbolic reversal, and interval-range checks. All
frozen inputs remain unchanged during review. Clean 28-page builds and
visual inspections support the presentation. Source/worktree coverage is
complete and primary-source version qualifications are explicit.

Assign a different agent to correct the accepted minor and rebuild. Because
no major issue was found in this full-paper round, the user's process does
not require another five-reviewer round. Root must verify the correction
and final build before marking the whole manuscript complete. No accepted
finding may remain unresolved.
