# Manuscript process

The active September 9 revision prepares a standalone anonymous submission of
*Sparse convex hulls for network flows coupled to a simplex*. It includes renewed
literature positioning, mathematical verification, computational reproducibility,
and delivery. Other manuscript folders are outside scope. Author and affiliation
fields are intentionally empty; no external submission is authorized.

## Required review protocol

Each stage has one author. After the author finishes, five agents independently
review the frozen changes. The root evaluates every finding. A different agent
corrects every accepted finding, including minor ones. Any accepted major finding
requires another complete five-reviewer round after correction. All accepted
minor findings must be resolved before the next stage. The complete manuscript
then undergoes the same review and correction process.

No stage is accepted on an author's assertion alone. Earlier material is reopened
if a later stage exposes a problem. Claims distinguish arithmetic complexity from
bit complexity, exact certificates from numerical checks, coefficient magnitude
from encoding length, and constructive formulation size from extension complexity.
Internal acceptance does not mean external peer review or establish priority.

## Active revision

1. Literature, contribution hierarchy, and significance: accepted after five
   independent reviews and separate correction of accepted minor findings.
2. Mathematical audit and development: accepted after five independent reviews
   with no required corrections.
3. Standalone exposition, computational reproducibility, and delivery: prepared
   for five independent frozen-stage reviews.
4. Whole-manuscript review: pending Stage 3 acceptance.

The authoritative current status is [revision-20260909/STATUS.md](revision-20260909/STATUS.md).
Author reports, independent reviews, adjudications, accepted snapshots, and private
validation evidence are retained under `revision-20260909/`. The
[delivery directory](delivery/README.md) contains the current anonymous PDF,
standalone source and supplement archives, deterministic builder, and manifests.
Package creation does not itself close a review stage.

## Historical development

The September 7 development had eight stages: foundations; compression;
structural oracles; bounded rank; coefficient obstructions and flat chains;
computation; final exposition; and whole-manuscript review. It completed nine
five-reviewer rounds, including a repeated computational review after a major
baseline-control correction. The 45 reports and their corrections remain in
`process/` and `verification/`.

The historical [final summary](process/final-summary.md) and
[whole-manuscript assessment](process/assessments/stage08-accepted.md) describe
that version. Their acceptance and source/evidence manifests are preserved
unchanged. They do not serve as acceptance records for the active revision.
