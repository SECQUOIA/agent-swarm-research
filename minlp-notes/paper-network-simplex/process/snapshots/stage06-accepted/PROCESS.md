# Manuscript process

The user requested a comprehensive LaTeX paper on sparse network–simplex hulls,
with renewed development and verification while writing. Work began 2026-09-07.
Other manuscript folders and unrelated working-tree changes are outside scope.

## Required review protocol

Each stage has one author. After the author finishes, five agents independently
review the frozen changes. The root evaluates every finding. A different agent
corrects all valid findings, including minor ones. Any accepted major finding
requires another complete five-reviewer round after correction. All accepted
minor findings must be resolved before the next stage. The complete manuscript
then undergoes the same review and correction process.

Review reports, root assessments, correction records, snapshots, and verification
artifacts are retained under `process/` and `verification/`. Internal acceptance
does not mean external peer review or establish literature priority.

## Sequential stages

1. Foundations, notation, literature positioning, and compilable paper skeleton.
2. General-graph compression, observation rank, forest complements, and recovery.
3. Explicit cycle/theta/parallel-path hulls and complete constructive separators.
4. Bounded cycle rank: finite support libraries, coefficient bounds, sharp K4.
5. General universality, sparse series–parallel coefficient growth, and the
   fixed-state flat-chain theorem; integrate the positive and negative boundaries.
6. Implementations, strengthened fair computational comparisons, reproducibility,
   and application interpretation.
7. Final exposition: introduction, abstract, connections, completeness audit,
   conclusion, bibliography, and publication presentation.
8. Five independent reviews of the entire manuscript, with required correction
   and repeat rounds.

Stage boundaries may be refined only with the same author/review protocol.
No stage is accepted on an author's assertion alone. Earlier material is
reopened if a later stage exposes a problem. Claims must distinguish arithmetic
complexity from bit complexity, numerical checks from exact certificates, and
coefficient magnitude from coefficient encoding length.

## Status

Stage 1: accepted after five reviews and correction of three minor findings.
Stage 2: accepted after five reviews with no required corrections.
Stage 3: accepted after five reviews with no required corrections.
Stage 4: accepted after five reviews and correction of three minor findings.
Stage 5: accepted after five reviews and correction of one minor finding.
Stage 6: accepted after two five-reviewer rounds, correction of one major
baseline-control issue and all five distinct minor findings.
Stage 7: in progress. Stage 8: not started.
