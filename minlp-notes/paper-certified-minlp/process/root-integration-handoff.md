# Coordinator notes for Stage 5, after Stage 4 acceptance

Do not begin Stage 5 before Stage 4's author/five-reviewer/correction cycle closes.

- Complete the abstract, contribution statement, discussion/conclusion,
  reproduction appendix and source delivery. Use unconditional section inputs;
  the final build must fail if a required section is absent. The PDF at the paper
  root currently predates the finished work and must be replaced by the final
  complete build. Use an anonymous review version rather than inventing author
  names or affiliations.
- Integrate `root-literature-followup.md`: Jansson, Messine–Trombettoni and QIBEX
  provide important rigorous-bounding precedents; describe established support
  minimization as such. Clarify Baes's number-of-points bound, not bit complexity.
  The references should credit direct sources without unsupported priority.
- Preserve all accepted mathematical distinctions: loaded-tree exact semantics,
  original domains, sufficient support correction, pointwise bound transfer,
  true original-model primal witnesses, complete restricted VIPR replay, and the
  limited Lean coverage. Improve flow and remove repeated defensive passages
  while retaining material assumptions and limitations.
- Make the architecture easy to understand. A small reproducible vector diagram
  of proposal/artifact/checking/transfer interfaces may help. Keep the final
  manuscript focused enough to read as a journal paper, with proofs available in
  the paper itself and large instance data in the supplement.
- Update all counts from Stage 4's final generated evidence. Distinguish the
  289-case historical replay, primary uniform generation, separate execution of
  the same checker, and any targeted integer-conversion repair cohort. Do not
  combine their denominators or infer causal speed/coverage superiority.
- Python's 4300-digit conversion limit was discovered in producer fraction
  normalization during the primary run. Stage 4 is preserving that frozen run,
  then repairing the producer and rerunning every affected case separately.
  The final paper and packages must identify each producer version; the
  mathematical checker is not changed by that repair. Use final test counts.
  A second occurrence was then found after complete successful proof arithmetic:
  conversion of tls12's 4326-digit bound in the driver's reporting layer. Stage 4
  is preserving its first two frozen cohorts and separately repairing exact
  rational text parsing/formatting at reporting boundaries. Distinguish these
  executable versions and targeted replays; do not silently replace the primary
  campaign's original verdicts with the final software's verdicts. The mathematical
  inference rules remain unchanged. Consult the final Stage 4 evidence rather
  than the provisional counts in this handoff.
- Give portable reproduction instructions for the small core, bulk proof
  archive, and Lean sources. No source instructions should require private paths
  or absent research notes. Keep solver generation dependencies separate from
  the five checker dependencies. Exact tool versions and hash manifests are the
  provenance; do not fabricate a public DOI or claim an upload occurred.
- Package complete LaTeX sources and the focused Lean sources (including pins,
  audit scripts and coverage), excluding `.lake/`, duplicate build trees, user
  literature PDFs and huge raw artifacts. Experimental core/bulk archives are
  separate deliverables. Preserve compact audit/review records in the repo.
- Update the current claim-to-evidence map and literature-review evidence with
  the completed formalization, final software/tests, campaigns and packages.
  Keep dated stage reports as historical records; remove provisional wording
  from current documentation and the manuscript.

Stage 5 still requires five independent reviews after authoring, a different
correction agent for every valid issue, and repeated five-review rounds after
any major finding. Stage 6 then applies the same process to the whole manuscript
and integrated artifact, before final delivery.

Stage 4 author completion facts (subject to its review/correction cycle):
- Current full draft builds cleanly as 28 pages at build/stage04-clean/main.pdf.
- All 161 targeted software tests pass, including from the extracted package.
- Historical 188/92/9 and primary V1 203/19/67 replay outcomes stay frozen.
  V2's twelve regenerated cases all verify in production and separate replay.
  V3 verifies two saved tls12 proofs that passed mathematical checking but had
  failed post-proof reporting. Current V3 is expected to replay the primary
  artifacts as 204/18/67; this is explicitly distinguished from the original run.
- The descriptive catalogue selects 222 model-identical bounds from 405 accepted
  records. Selected origins are 162 historical, 51 primary and nine V2. It is not
  a uniform-run success rate or a comparative performance experiment.
- The small core is approximately 6.46 MB, and the bulk archive is 30,664,561,063
  bytes compressed. Full readback checked 5,207 entries and 93,713,729,595 regular
  bytes. Core extraction reproduced four complete bundles, source/primal audits,
  fifteen failed-step audits, all thirteen generated table/catalog outputs, and
  the tests without licensed solver dependencies. Read supplement/archives.json
  for final hashes: documentation corrections may rebuild the small core.
