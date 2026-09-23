# Stage 4 independent adversarial review 5

## Verdict

**No major issues found.** One minor wording correction would make the artifact-content claim exact. The experimental outcomes are carefully separated by population, source version, production/replay stage, and artifact selection. The data inspected support the manuscript's numbers and the merged bound catalogue. I found no invalid inference from reference proximity or from a locally rejected proof to a false final bound.

## Evidence and independent checks

Read Section 6 and its generated tables, the Stage 4 author report, supplement README, frozen generation protocol and replay-selection policy, analysis and catalogue scripts, repair-summary script, new proof-step summary, historical first-failure data, rational-text implementation and related tests, and the reporting call sites. Inspected the small core archive's member list and independently computed its SHA-256. I did not read peer reports, replay the large corpus, regenerate experiments, or repeat the full bulk readback.

Independent compact-record calculations reproduced:

- Historical: 289 records, 188 verified / 92 rejected / 9 missing, accepted proof bytes 38,826,726,525.
- Primary replay: 289 records, 203 verified / 19 rejected / 67 missing, accepted proof bytes 14,233,742,052.
- Producer-repair replay: twelve records, all verified. Reporting-repair replay: two records, both verified.
- Catalogue: 405 candidate accepted records, 222 distinct model names, with 162 selections from historical, 51 primary, and nine producer-repair records. Every catalogue selection equals the maximum exact signed-normalized bound among its candidates, all of which share its model SHA and objective sense. The union of verified names across the four supplied cohorts is exactly 222.
- The eleven positive historical right-hand-side excesses range from about 1.54749e-12 to 1.93196e-10, agreeing with the rounded paper range.
- Core archive SHA-256 is `031a8a47f296d7fd8f484d3ad695c9476a8f316498a8ef5f2d5ecd03d7b287a6`, agreeing with the index and report. Its campaign-model directory contains exactly 289 Python model files.

## Valid minor correction

1. **Minor — specify which models and dependency material are in the core.** At `sections/06-experiments.tex:238–240`, “pinned checking dependencies, all loaded models” is imprecise. The core provides the dependency specifications and the 289 campaign model files; the earlier selection description also mentions three models that loaded but failed the previous curvature screen. Replace this fragment with “pinned dependency specifications, all 289 campaign models.” This matches the supplement README and archive contents without implying inclusion of the three excluded loaded models or bundled installed dependency binaries. No additional model or dependency packaging is needed for the advertised replay scope.

## Scientific and interface assessment

The historical 269 labels, 81 revoked labels, 92 total rejections, and nine missing records refer to compatible but different subsets, and the text explains them. New generation outcomes add to 289 and are not conflated with the separate replay verdicts. The four timeout survivors and one worker-error survivor explain the primary difference between 198 accepted production returns and 203 accepted replay records. Deterministic completed-proof selection is explicit and does not optimize bound quality. The selection policy was recorded before replay, while generation was in progress; the paper accurately claims that timing rather than falsely claiming it was in the original pre-generation freeze.

The three source versions and repair cohorts are explicit. The twelve regenerated producer failures are not silently substituted into the primary cohort. The two later reporting replays concern exact rational representation after successful mathematical checks, and the paper distinguishes an additional accepted primary bundle from a rerun of the uniform experiment. The catalogue uses verified evidence, model identity and objective sense rather than a library reference to choose bounds; its 222-model union is not described as a uniform-budget success rate.

The rational-text changes preserve exact fractions and decimal-string meaning through FLINT and Decimal conversion. Their uses are at report/normalization boundaries, with the proof and nonlinear rules unchanged. The optional floating representation does not replace the exact result. The distributed tests exercise long positive/negative fractions, decimal reference strings, both objective senses and unavailable floating displays; this is a suitable boundary repair and is not claimed as a new mathematical certification rule.

The signed reference metric has the correct sense normalization for both minimization and maximization. Negative differences and near-reference counts are clearly distinguished from certified gaps. The small negative historical discrepancies are not used as solver-error evidence. The returned-point audits have stronger premises and retain their appropriate limits: original bounds/rows, robustness to printed precision, common source interpretation, no claim to reconstruct historical solver memory, and no unobserved internal-cause attribution.

The historical arithmetic extracts and three new inference descriptions establish violations of the admitted local inference rules. The text correctly avoids claiming that every arithmetic mismatch proves the final numerical bound false. In particular, the gapped branches leave integer activity 65 outside the stated disjunction, while other uncited master information could still exclude it; this is properly treated as failure of the supplied standalone justification.

The time measures have explicit boundaries, concurrency is disclosed, external corroboration differs between historical and primary replay, and the proof-completion thread default is not concealed behind the one-thread search settings. The archive and reproduction claims are scoped to core versus bulk, checker versus producer, frozen versus portable wrappers, and original versus redacted logs. Full bulk and fresh-core execution validation are covered by the author and designated execution reviewer; this review does not independently duplicate them.

Stage 5 integration and publication-wide wording remain separate work. No Stage 4 result reviewed here invalidates the paper or requires mathematical repair before proceeding.
