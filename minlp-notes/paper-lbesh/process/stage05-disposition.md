# Final whole-manuscript review disposition

All five independent final reports are complete. Reviewers 1, 4 and 5 request no further correction; reviewers 2 and 3 each identify one minor issue. Every reviewer finds the manuscript scientifically complete in its stated computational and methodological scope, with no major mathematical, empirical or originality defect. The lead independently checked the two findings against the frozen tables and timer implementation and accepts both.

## Accepted corrections

1. **PAR10 scope (reviewer 2).** The first results paragraph follows a statement about all four matched configurations with an explanation that applies only to the two single-tree pairs. Limit the much larger PAR10 differences to those single-tree comparisons, where ECP has one or two additional failures. The multi-tree pairs have equal held-out accepted counts (30/30 and 29/29); their PAR10 differences reflect timing, not additional failures. The tables and numerical ratios are already correct.
2. **Recorded separation-time definition (reviewer 3).** `time_cuts` accumulates elapsed time inside completed `_esh_cuts` calls. This includes row checks, radial searches when used, and linearization/coefficient work. It excludes initial tangents, NLP-solution tangents, the outer normalization/transformation work and installation of cuts in the master/callback. Define this precise scope in the algorithm and compact-data documentation, and consistently use a term such as “recorded row-separation time per run” in the abstract, introduction, results/caption, conclusion and other affected prose. Align the generated table label and figure title. Preserve the warnings about overlapping timers and the absence of a per-cut comparison. The 5.5–6.6 ratios are correct for this recorded field; neither their values nor the frozen field/schema/data should change.

As part of the same telemetry-definition correction, the lead's source inspection adds one short clarification: `lp_iters` counts iterations of the initial LP separation phase, not internal simplex/barrier iterations or all node LP solves. State this in the algorithm's LP-phase paragraph and compact-data documentation. No counter, table value or formula changes.

Both are minor description/quantifier corrections. They do not change a theorem, data value, accepted outcome, experimental cohort or central conditional wall-time conclusion. No new algorithm development, benchmark campaign or full witness audit is needed. A five-reviewer repeat is not required because no valid issue is major. A separate correction agent will close both findings, regenerate the changed presentation, rebuild and refresh packages/checksums, and verify unchanged numerical outputs and frozen research evidence. The lead will inspect those corrections before final acceptance.

## Administrative closeout to follow verification

Once both corrections pass, update the delivered coverage/README status to the completed five-stage process, without implying external journal peer review or guaranteed acceptance. Keep the full author/reviewer/disposition records in the repository. Record the final delivery identifiers and targeted verification actually performed. No new scientific claims may be introduced during this closeout.

## Lead acceptance — 19 September 2026

Accepted the separate correction author's final changes after inspecting the corrected PAR10 passage, timer and LP-counter definitions, abstract, result captions and delivered status. All accepted findings are closed. These corrections preserve the mathematical results, frozen observations and numerical table entries. No accepted major issue remains, so no repeated five-reviewer round is required by the agreed process.

The lead independently verified all 68 final fingerprints, all 62 source-archive payloads against both their manifest and current source, equality of embedded and external manifests, equality of main and submission PDFs, all three delivery checksums, and five retained review reports for each of the five stages. See `final-lead-checks.json` and `final-acceptance.md`. This closeout changes only process records; the frozen manuscript and packages are unchanged.
