# Stage 5 adjudication

All five independent integration reviews are complete, with no major findings.
Reviews 1, 2, 3 and 5 give clean verdicts. Their checks cover theorem/claim
consistency, primary literature, complete source extraction and clean build,
stale-auxiliary recovery, deterministic packaging and artifact provenance.

The coordinator accepts both minor findings from review 4:

1. Define outer approximation (OA) on first introduction, and expand special
   ordered set (SOS) at its first use in the implementation contract. This
   distinguishes the latter from sums-of-squares terminology in the literature.
2. Make the campaign table's reference metric understandable from its caption
   or an explicit definition cross-reference, since the table can float before
   the metric's prose definition. State that reference counts concern verified
   bounds. Keep the table generator and distributed copies consistent.

A separate correction agent must make these clarity changes, regenerate the
affected small artifacts/indexes and source archive, update exact size/hash
references where needed, and validate a clean source build and table agreement.
The mathematical proof/checker sources, experiment records, formal sources and
large bulk archive remain unchanged. No new numerical generation, large replay
or bulk readback is warranted. No major issue requires another five-reviewer
Stage 5 round; Stage 6 remains a separate mandatory whole-manuscript review
after these corrections are accepted.

## Acceptance

The coordinator inspected the correction report, the acronym expansions and
the regenerated caption/definition link. Both valid findings are resolved.
The correction agent verified unchanged numerical outputs, all 3,793 extracted
core entries and a clean 32-page extracted-source build matching delivery. The
coordinator independently checked current core/source sizes and SHA-256 digests,
and bulk size against the preserved index. Stage 5 is accepted.
