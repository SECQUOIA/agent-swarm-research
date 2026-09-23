# R2 author report: scientific experimental organization and delivery

Author: `/root/s1_author`. Scope: prose organization, current documentation, and
standalone paper delivery after accepted R1. No new experiments, replay, tests,
Lean builds, numerical/source-code changes, or large archive reads were needed
or performed. Root owns adjudication and the five independent reviews.

## Scientific structure

Section 6 now answers three questions in order:

1. **Capability (6.1):** what checkable bounds the uniform protocol provides and
   how strong they are relative to explicitly unverified references. The main
   result is 203/289 accepted replay artifacts, distinguished from 198 accepted
   producer returns. Exact primal completion examples and the descriptive
   catalogue make the stronger and broader claims precise.
2. **Failure mechanisms (6.2):** what a rejection or objective disagreement
   actually establishes. Invalid external-accepted discrete steps lead the
   exact audits; historical counts, sufficient nonlinear-test failures, and
   returned-point/source audits are then classified by their witnesses.
3. **Costs and practical limits (6.3):** generation versus checking time,
   accepted versus all-record sums, concurrency, storage, and memory dependence.
   The condensed memory account includes per-derivation index arrays as well
   as live sparse rows, master/input/rational sizes, and the absence of a
   peak-memory conclusion from machine capacity.

Appendix A remains the portable reproduction guide. New Appendix B preserves
full frozen protocols, generated production/phase accounting, historical
checking costs, and separate V1/V2/V3 representation repairs. Its summaries
are described as derived from frozen records, not as a revision narrative.
The main section gives scientific answers and synthesis before the supporting
accounting; chronological repair detail no longer determines its order.

## Old-to-new content map

| Previous Section 6 material | Current location and treatment |
|---|---|
| Opening three questions | Rewritten around capability, failure mechanisms, and costs, with answers stated immediately |
| Population, source interpretation and 299-to-289 exclusions | 6.1, all facts retained |
| Historical/new generation and replay protocols, candidate selection, hardware/versions/threads/hashes | Appendix B.1; key uniform limits summarized in 6.1 and cost interpretation in 6.3 |
| Historical 269 labels, 81 revocations, 188/92/9 results | 6.2, tied to the effect of enforcing the checking obligations; Table 4 remains in 6.1 |
| Historical sizes, derivations and all timing definitions | Appendix B.2 in full; storage implications selected in 6.3 |
| Generated uniform outcome/timing paragraph and phase table | Unchanged inputs in Appendix B.2; principal capability/cost results selected in 6.1/6.3 |
| Exact signed reference metric and thresholds | 6.1; fresh 46/80/25 counts explicitly interpreted without claiming optimality |
| Historical 52/81/23 reference counts and rounding qualification | 6.1, retained |
| Solver-objective flag criterion and 18 flags | 6.2 before original-variable audits, with statuses and investigation-only qualification retained |
| Twelve historical discrete-step audits | 6.2, retained exact residual range, directions, evidence references, and local-only conclusion |
| Three new external-accepted/internal-rejected steps | 6.2 leads the exact inference discussion; all antecedent/direction/gapped-disjunction qualifications retained |
| risk2bpb sufficient-intercept rejection and three targeted regression cases | 6.2 under conservative nonlinear failures; no implication of globally false cut or false reference |
| Twelve normalization failures, V2 regeneration, tls12 reporting boundary, V3 checks | Appendix B.3, all outcomes and generated repair text retained; scientific representation lesson summarized in 6.2 |
| clay0204m and risk2bpb returned-point/primal/source audits | 6.2, full quantitative rows, printed uncertainty, model sizes, statuses, formula semantics and limitations retained |
| Representative quadratic optimum, 11 cuts/39 derivations, 161 tests | 6.1 as positive capability/primal completion, with test/formal boundary retained |
| Catalogue: 222 models from 405 accepted records | Unchanged generated input in 6.1, with explicit separate-protocol context and Appendix B.3 link |
| Core/bulk contents, generator/checker separation and redactions | 6.3 plus existing Appendix A commands; archive data unchanged |

## Precise integration edits

- `sections/06-experiments.tex`: scientific reorganization and synthesis above.
- `sections/09-experimental-accounting.tex`: new supporting appendix, reusing the
  existing protocol/repair prose and unchanged generated accounting inputs.
- `main.tex`: one new appendix input. Accepted R1 abstract is unchanged.
- `sections/01-introduction.tex`: only the final roadmap gains an Appendix B
  cross-reference. Accepted R1 contribution/prior-work wording is unchanged.
- `sections/08-reproducibility.tex`: generation/provenance paragraph links to
  Appendix B. Its commands, counts, version caveats, and archive sizes remain.
- `sections/07-discussion.tex`: accepted R1 conclusion unchanged.
- `README.md`: reader route through scientific results and appendices.
- Current `evidence/repository-inventory.md` and `literature-review.md`: new
  reading order and correct linkage between uniform capability, historical
  audit, and supporting repair accounting; no change to novelty attribution.
- Delivered `main.pdf`, `main.bbl`, `PAPER-SHA256SUMS`, source archive and its
  JSON index refreshed after all manuscript/current documentation edits.
  Historical reviews and source/evidence archives were not rewritten.

## Counts and qualifications preserved

A before/after inventory verifies all 32 selected table, generator, formal-source,
and archive-index files unchanged; `r2-preservation-check.json` records this.
Expanding the existing table inputs and comparing old Sections 6/8 with new
Sections 6/8/9 retains every original numerical token. That is an accounting
aid, not a semantic proof; the content map above was also checked manually.

The preserved scientific distinctions include:

- all 299 selected names and seven load/three old screen exclusions; full 289
  attempted population in historical and uniform protocols;
- 198 producer returns versus 203 primary separate-replay acceptances, with
  four timeout and one worker-error survivors, 19 rejected and 67 missing;
- historical 188/92/9, 269 old labels and 81 revocations (67 domain/curvature,
  13 cuts, one proof), plus eleven failed old crashes;
- V1/V2/V3 remain separate: twelve V2 generations/replays and two targeted V3
  proof replays are retained. Expected 204/18/67 under a fresh full V3 replay
  is explicitly not a completed additional primary experiment;
- 222-model/405-record catalogue is a matching-model union, not uniform coverage;
- reference values remain unverified; exact invalid local steps do not imply
  false final bounds; sufficient enclosure/curvature rejection need not refute
  the inequality/model; original-variable feasibility and source semantics
  remain necessary for the stronger primal conclusions;
- solver search requests, true outer wall cap, per-record replay cap, phase
  timing, sums/elapsed time, all/accepted populations, historical external
  corroboration, hashing separation, hardware/thread limits and shared-machine
  caveats all remain explicit.

## Delivery validation

`bash scripts/build-paper.sh` builds the 33-page current PDF and bibliography
from a fresh temporary source tree. Final logs have no undefined references or
citations, warnings, or overfull boxes. Pages 22 and 30 were rendered and
visually inspected to check the main results table and supporting phase/repair
layout. No layout problem was observed.

`python3 scripts/package-source.py` was run twice after the final current docs;
the repeated archive and JSON index are identical. The package contains 50
files including its manifest, occupies **479,937 bytes**, and has SHA-256
`9eb0f355af6a4af38a2586541f1c12c4fb0dcac06abe1fff66546edb90b9fb1b`.
The existing packager automatically includes the new appendix. It does not read
or rebuild the experimental core/bulk archives.

Fresh extraction:
`/tmp/certified-minlp-r2-source.zJeKUp/certified-minlp-paper`.
All 49 content files pass `sha256sum -c PAPER-SHA256SUMS`; a standard
`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` build passes
there without warnings, undefined references/citations, or overfull boxes.
Its extracted PDF text and `main.bbl` are byte-identical to the delivered
paper's text and bibliography. `r2-validation.json` records exact hashes,
archive metadata, and these checks. `r2-extracted-*.log` and `r2-current-*.log`
retain the build/manifest evidence.

No unresolved issue was found during author integration. Five independent R2
reviews are the next required gate; the author does not adjudicate that gate.
