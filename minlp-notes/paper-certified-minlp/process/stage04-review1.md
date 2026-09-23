# Stage 4 independent review 1

Reviewed the completed Stage 4 experimental section, generated tables, primary/V2/V3 protocols and compact records, analysis/catalog code, source repair diff, and packaging validation evidence. Particular attention was given to complete denominators, exact comparison arithmetic, timing meanings and source-version separation. No other reviewer report was read, and no numerical generation, full proof replay or bulk archive hash pass was performed. Only this review file was written.

## Verdict

**No major issues found. One minor specification clarification should be addressed.** Independently recomputed experimental counts, exact reference metrics, proof statistics, phase aggregates and merged catalog agree with the manuscript. The repairs retain the original outcomes and make the version-dependent acceptance difference explicit.

## Finding

### R1-1 — Minor: specify the separate solver-objective flag criterion

Location: `sections/06-experiments.tex:123–126`, the sentence reporting 18 flagged saved-solver pairs.

The preceding library-reference metric normalizes by `max(1, |r|)`, but the 18-pair diagnostic uses `max(1, |B|)` and a one-sided excess. Calling this only the “recorded 10^-6 relative scale” leaves the standalone description ambiguous. The baseline model-status restriction is also omitted there.

Evidence: `certify/summarize.py` includes baseline records with model status in `{1,2,8}` and flags exactly

`s * (B - r_solver) > 10^-6 * max(1, |B|)`.

I independently applied that rule to the saved baseline objective files and reproduced 18 pairs. Thus this is a specification issue, not a wrong count.

Correction: give that explicit inequality and identify the included baseline-status codes (or their documented names). Keep the existing warning that these are investigation candidates. This also distinguishes the diagnostic from the library-reference metric without altering any experiment or table.

## Independent data verification

### Cohorts and outcomes

- Parsed `cohort-selection.csv`: 299 unique selected names, 289 marked attempted, and ten exclusions. The latter comprise seven recorded load errors and three unsuccessful curvature screens. The attempted set equals the frozen primary `names.txt` population.
- Independently checked both historical and primary replay record indices cover exactly `0,...,288` and have 289 distinct instance names.
- Historical replay: **188 verified, 92 rejected, nine missing**. Among records whose old checker/external flags were both `OK`, 188 remain verified and 81 are rejected. Eleven other rejected records have historical `crash` status. Thus 81 revoked acceptance labels and 92 total rejections are correctly distinguished.
- Primary production: **198 verified, 67 producer errors, eight rejected, four hard timeouts, twelve worker errors**. All 67 producer errors contain an uncertified-model admission diagnostic. Primary replay: **203 verified, 19 rejected, 67 missing**. Its accepted records include all 198 successful productions, all four timeout survivors and one worker-error survivor. Replay acceptance is not incorrectly counted as a producer return.
- Independently grouped the nineteen primary rejection reports: thirteen domination failures, two non-rational `+infinity` tokens, two incompatible-direction combinations, one unsplit-disjunction failure, and one post-proof report conversion failure.
- The V2 planned twelve-name set equals both the original worker-error set and the twelve regenerated names. Its saved generation and replay each contain twelve verified outcomes. V3 records two verified targets for one model, not two additional models.
- Matched the V3 primary `tls12` proof SHA against the original rejected primary record: these are the same proof bytes. The V3 success is therefore a reporting-boundary recovery, not an unreported new optimization run.

### Exact reference comparisons

I recomputed each comparison directly from the saved rational bound and the metadata decimal string, using decimal integer ratios and FLINT rationals rather than the paper's summary function. This reproduced:

| Cohort | Verified comparisons | `0 <= d <= 10^-4` | `0 <= d <= 10^-2` | `d < 0` |
|---|---:|---:|---:|---:|
| Historical | 188 | 52 | 81 | 23 |
| Primary | 203 | 46 | 80 | 25 |

The maximum historical negative normalized magnitude is approximately `5.833656876857371e-10`, below the stated `6e-10`. Every accepted historical and primary record has a usable metadata comparison, so the displayed threshold denominators have no silently missing reference subset. The manuscript correctly treats these as reference differences, not certified optimality gaps.

### Proof size, derivations and time

Recomputed directly from accepted record fields:

| Quantity | Historical | Primary |
|---|---:|---:|
| Accepted derivations | 29,903,993 | 11,749,855 |
| Accepted proof bytes | 38,826,726,525 | 14,233,742,052 |
| Sum accepted checker seconds | 7,987.953599 | 2,791.064419 |
| Median accepted checker seconds | 16.679065 | 5.173456 |
| Maximum accepted checker seconds | 463.845461 | 221.484185 |
| Sum all-record checker seconds | 8,234.349309 | 2,953.981639 |

Historical median and maximum accepted proof sizes are respectively 74,469,242 and 2,163,285,624 bytes, as stated.

Independently summed the primary event files. They contain 358 completed SCIP calls totaling 7,401.356837 seconds; 358 completed proof-completion calls totaling 371.306651; 477 completed external checks totaling 1,290.663279; and 202 internal-proof starts with 201 ends totaling 1,583.153191 completed-call seconds. These reproduce the phase table. The single interrupted internal call is not silently assigned a completion time.

The protocol freezes precede their corresponding starts. The primary replay selection was fixed during generation and before replay, which agrees with the manuscript rather than claiming it preceded generation. The wrapper's outer process-group cap, per-search budgets, maximum fallback count and event timing agree with the description. Proof-completion threading and shared-machine contention are disclosed. Worker sums, process-call durations, full-check durations and campaign elapsed times are not conflated. Historical replay's extra external corroboration is stated, so its checker times are not presented as directly comparable internal-kernel timings.

### Strongest-bound catalog

Using the four saved verified-record collections, I independently grouped by instance, required identical model SHA and objective sense, compared exact normalized lower bounds, and retained the first record on exact ties in the documented cohort order. I then compared every selected value, source cohort and proof hash with the saved catalog.

Result: **405 verified candidate records, 222 distinct models**, with selected records from **162 historical, 51 primary and nine producer-repair** entries. Every catalog choice matched. Reporting-repair candidates are included in comparisons but do not become the strongest selected bound for their model. The manuscript accurately calls this a descriptive union, not the success rate of the uniform budget or 405 distinct models.

## Repairs, audits and reproducibility evidence

The V2/V3 changes shown in the saved diff concern rational text normalization, exact report input/output and optional floating display. I independently matched current hashes for `exact_model.py`, `convexity.py`, `safecut.py` and `vipr.py` against frozen V1. The driver's shown changes occur after proof validation and in serialization; the model/cut/master logic is unchanged. This supports the distinction between representation failures and mathematical proof-rule repairs.

The local failed-step discussion is correctly qualified: an invalid supplied combination or disjunction does not prove a false final bound, and a failed sufficient nonlinear intercept test does not establish global cut invalidity. The returned-point section's printed-coordinate error allowances are consistent with the displayed coefficients: `(1+1+51)*0.00005=0.00265` and `(1+1+86)*0.00005=0.0044`. Its source-formula comparison is explicitly narrower than verification of the historical solver's in-memory model.

Independently hashed the small core archive; its SHA matches the published index. Inspected the final extracted-manifest log, four-bundle/source/primal/local-proof audit log, 161-test log, and thirteen-file byte-identical table-regeneration report. Inspected the saved complete bulk readback report covering 5,207 members and 93,713,729,595 regular-file bytes. These are author execution evidence; this review did not repeat that expensive readback or all numerical/proof work. The restriction is intentional and does not turn those logs into an independent full rerun.

## Remaining stage boundary

Missing final abstract/discussion integration is not treated as a Stage 4 defect. Preserve the versioned-count and reference-feasibility distinctions when integrating the final manuscript. After the minor diagnostic-definition clarification, this review identifies no major issue requiring another Stage 4 review cycle.
