# Stage 1, round 1: root assessment

All five requested independent reports were received and read. They inspected
the frozen `stage01-round01` source (manifest digest
`2230f1e9da9d015278c6bbf424d04167961f6c7911646ca287e899b9ccae36de`).
No reviewer found a major defect; the root agrees. The stage is not accepted
until the following minor corrections are made and checked.

## Accepted corrections

| ID | Reports | Root decision and required change |
| --- | --- | --- |
| S1-1 | R01-1, R03-1 | Valid minor scope defect. Restrict the blanket infeasibility/attainment promise to exact algorithms. Approximation algorithms must retain their theorem-specific original-infeasibility, relaxed-output, and empty-inner-surrogate guarantees. |
| S1-2 | R01-2, R02-02, R03-2 | Valid minor precision defect. State algebraic output bounds in `(L,delta)` and derive polynomial-in-`L` output only under the degree-encoding condition. The nearby correct runtime convention does not remove the need to qualify the output sentence. |
| S1-3 | R02-01, R05-01 | Valid minor attribution ambiguity. Attach `optimistic` directly to the classical fixed-follower-variable positive claim. The later warning about pessimistic conventions is not sufficiently explicit. |
| S1-4 | R05-02 | Valid minor model omission. Declare `c_b(x)` to be a rational polynomial vector, and state once that every polynomial datum in the model is supplied explicitly with rational coefficients. |
| S1-5 | R03-3 | Valid minor inventory omission. Assign the zero-local-curvature and negative-local-curvature 3SAT examples explicitly to stage 5, preserving their different upper-row restrictions and elementary attribution. |

The mathematical constructions are not invalidated by these issues: the
correct guarantees are already present in the intended source statements and
surrounding text. These are specification, attribution, and coverage refinements,
not repairs to a failed proof. No mandatory repeat five-reviewer round is
triggered by this minor-only round.

## Optional suggestions and rejected concerns

R02's suggestion to distinguish logarithmic-accuracy resource allocation from
Vigneron's inverse-relative-error scheme is useful and will be included as a
short clarification in the same correction. It does not change a claim or add
a proof dependency. R05's optional concrete opening example belongs to stage 7's
planned synthesis and is not an unresolved defect in this stage.

R04 reported no defects. This does not override the more specific, justified
findings above. The root's earlier suspected Ketkov--Prokopyev theorem-number
error was independently withdrawn after inspecting the original theorem; see
`stage01-root-reading.md`. No corresponding source change is authorized or needed.

## Evidence and process

All five reviewers checked the source snapshot and performed isolated builds;
their final logs were clean. Root independently read the foundations, checked
all 14 canonical result files were mapped, checked label uniqueness, and visually
inspected a rendered mathematical page. The substantive inventory includes the
note-only path, inverse, and algorithm developments. These checks do not approve
later proofs merely because they have been assigned.

Reviewer04 disclosed an accidental initial build at the manuscript root, then
completed an isolated build. No source changed; the isolated result is the
relevant verification evidence. Reviewer independence was maintained.

A correction agent distinct from the author and five reviewers will implement
S1-1 through S1-5 and the short accepted exposition clarification. Root will
inspect the changes, verify the build and close the stage before assigning stage 2.

## Acceptance

The separate correction agent completed all changes in `stage01-corrections.md`.
Root read that record, inspected the full foundations and coverage diffs, and
checked the final clean six-page build log. S1-1 through S1-5 and the accepted
literature clarification are closed. No new defect was introduced by the local
changes. Stage 1 is accepted; its corrected source is frozen as
`process/snapshots/stage01-accepted`. No major issue occurred, so no additional
five-reviewer round is required by the user's process.
