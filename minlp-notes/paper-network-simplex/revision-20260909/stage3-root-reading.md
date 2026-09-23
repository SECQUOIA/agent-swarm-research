# Root Stage 3 reading and independent reproduction

The root reviewed the developing computational narrative and package builder
while the stage author prepared the submission files. This is separate from
the five independent frozen-stage reviews that follow author completion.

The distinction between a numerical solver result and an exact checked cut or
decomposition remains explicit. The explanation of fixed-weight independent
network objectives and the component-hull meaning of the aggregate-budget
control is retained. Canonical measurements remain unchanged; fresh results
are written separately, and table regeneration uses the canonical records.

Two small author-stage prose suggestions were sent before completion: omit a
counterfactual runtime statement whose supporting older measurements are not
in the standalone package, and name flat-chain inverse bases by their three
observed labels rather than ambiguous graph-rank terminology. The author owns
and reports the final edits. Neither changes mathematical content.

The builder selects explicit source inputs and runnable dependencies. The
supplement preserves the relative layout needed by the unreduced comparator
and rank-recovery imports. Each ZIP contains a payload checksum list; the
outer manifest also hashes inputs and final artifacts. Fixed timestamps and
suppressed variable PDF metadata support byte reproducibility for a fixed
toolchain. Cross-version byte stability is not claimed.

## Independent complete study rerun

The root copied accepted Stage 2 executable files into an isolated temporary
root, kept the original relative code/reference layout, and ran:

```sh
PYTHONPATH=code python -m network_simplex_benchmarks.paper_stage06 --output paper-network-simplex/verification/stage06-benchmarks.json
python paper-network-simplex/verification/stage06-tables.py
```

Both returned zero. The default grid contained sixteen flat, three many-label
membership, and three optimization cases, with one warmup and five rotated
measurements per case. The table generator accepted the full record. A recursive
comparison with canonical data examined 5,754 non-timing scalar leaves: inputs,
objective vectors, weights, side rows, statuses, counts, dimensions, and audit
outcomes matched (absolute tolerance 1e-7 for numeric comparisons). Environment,
timing, derived summaries, cold calls, and the historical update record were
excluded; the table generator independently checks the fresh timing summaries.
No new performance ordering is claimed. The original data were not modified.

Evidence is in stage3-root-evidence/full-study.json, full-study.log,
full-study-validation.json, and full-study-tables/. This rerun checks the complete
study logic; the author's tests of actual extracted archives separately check
that packaging includes the necessary dependencies.

## Rendered-page check

The root inspected all fifty pages in five contact sheets and checked the title
and computational tables/reproduction pages at higher resolution. No clipped
equation, illegible table, misplaced figure, missing reference, or blank unintended
page was found. The final bibliography occupies part of the last page normally.
The contact sheets and PDF hash are recorded in stage3-root-evidence/. This
layout check complements, and does not replace, the mathematical source audit.
