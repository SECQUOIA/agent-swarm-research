# Stage 4 first-round adjudication

The coordinator read all five complete independent reports and the main
section and supporting appendix. All twelve frozen source hashes remained
unchanged through the review. No reviewer identified a major issue; the
coordinator agrees. The main certificate, split-family, robust and separator
proofs withstood the reviews and independently formulated finite exact checks.

All findings are accepted and consolidated into two minor corrections:

1. Reviewers 2 and 5: define the continuous relaxation explicitly by
   `conv{1_S:S in F} subseteq Z subseteq [0,1]^n`, with compactness and
   convexity. The cube condition supplies the proven concavity domain and
   nonnegative virtual variances; containing the indicators alone is not
   sufficient. Preserve the distinction between a cube query and a query
   feasible for the relaxation.
2. Reviewers 1 and 5: distinguish the arbitrary real witnesses allowed by
   the theorem from the rational witnesses required by the checker. Choose
   rational symmetric SPD references, verified exactly, and a certified
   rational upper enclosure `delta_hat` with `delta <= delta_hat < 1`.
   Use this enclosure in all rational scores, including scenarios. Rational
   model data alone do not make square-root locality constants rational.
   Explain validity under enlargement, how to obtain the enclosure, and
   refinement/increased memory/rejection if it is not below one. State the
   analogous rational representation choices for the remaining witnesses.

Reviewers 3 and 4 request no corrections. No finding is rejected or left
unresolved. The additional nested-sensor-bound source noted by reviewer 5
uses a different construction; the existing qualified Markov-anchor claim
remains appropriate and must retain its narrow scope during synthesis.

A separate correction author will make both changes, followed by coordinator
inspection and a clean build. Neither clarification changes the intended
mathematics. The protocol does not require a second five-reviewer round
because no major issue was accepted. Acceptance is conditional on verification
of both corrections.

The coordinator's separate script also passed 160 exact elimination identities,
40 mixture orderings, and 120 arbitrary-nuisance supports. These and the
reviewers' independent checks supplement the proofs; they are not formal
verification, external peer review, or performance benchmarks. Later empirical
and integration stages remain required.

Final disposition: the coordinator verified the explicit cube containment,
rational witnesses, upper error enclosures, and scenario convention in the
actual corrected source. Only the two intended Stage 4 source files changed
from the freeze. The forced 51-page build is clean. Stage 4 is accepted and
its twelve-file source snapshot is `process/snapshots/stage04-accepted/`.
