# Stage 2 adjudication and acceptance

The author completed the mathematics audit before the stage2-round1 freeze.
Five reviewers independently examined that frozen development; the root read
all five complete reports and assessed their arguments and evidence. The root
also read the author audit and exact source diff and independently examined the
sensitive proofs, as recorded in stage2-root-reading.md.

## Findings and disposition

| Report | Major findings | Minor findings | Root disposition |
|---|---:|---:|---|
| stage2-review1.md | 0 | 0 | Accept the argument and evidence within stated limits. |
| stage2-review2.md | 0 | 0 | Accept; especially the unimodular multiplier and encoding arguments. |
| stage2-review3.md | 0 | 0 | Accept; coordinate-section invariance and actual-cell universality checked. |
| stage2-review4.md | 0 | 0 | Accept; the classification and both coefficient repairs cover all cases. |
| stage2-review5.md | 0 | 0 | Accept; exact certificates are distinguished from numerical statuses. |

Reviewer 3's F0 and reviewer 4's numbered no-defect entries record affirmative
checks, not unresolved findings. No reviewer requested an optional edit.
There is therefore no correction assignment or repeated mathematics round.

The root agrees that the expanded three-label proof is complete: the support
bound, minimality, and positive weighted covers exclude every additional case.
The sole doubled circuit weight does not contain products, and the two separate
flow-balance repairs are necessary for the full flow/product coefficient claim.
The compact recovery vector wording resolves a scalar/vector ambiguity without
altering the algorithm. The remaining results preserve the carefully qualified
scope of the accepted contribution statements.

Independent rational computations test distinct parts of these arguments:
cycle restriction and Schur minors, block refinement with an infeasible reference,
primal versus dual supports and degenerate recovery, actual Fibonacci facets,
all exceptional three-label repairs, and returned certificates against original
flow/simplex generators. These finite checks supplement the proof reading;
no sample count is treated as a proof of an asymptotic result. The imported
transportation universality theorem was checked in its primary source, without
claiming that its full reduction was reimplemented.

All 86 frozen file hashes and all corresponding active files matched at root
acceptance. Private 50-page builds have clean diagnostics. Production code and
canonical benchmark data have not changed in this stage. No identified major
or minor mathematical issue remains. Stage 2 is accepted; Stage 3 may begin.
This internal acceptance is not external peer review or a guarantee of priority.
