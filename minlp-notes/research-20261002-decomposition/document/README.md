# Decomposition-aware global optimization: integrated report

Read [main.pdf](main.pdf) for the mathematical account and implementation
results. The [coverage map](COVERAGE.md) distinguishes proofs in the report,
imported companion proofs, implemented behavior, diagnostic evidence and
unresolved targets. The title page supplies no author or publication date.

Sections 2–5 give the corrected-grid, min-marginal, filtering-history,
conditioning and exact-output arguments. They now include finite exact
recovery for arbitrary nonunique rational box QPs, while keeping the
stronger point-growth running-time theorem separate. Section 6 develops the
restricted extensions, including curvature cancellation across changing
convex responses and union-state filtering for nonunique TU problems.

Section 7 preserves the **74 first-release runs** and their original source
snapshots as historical evidence. Section 8 covers the completed
implementations and separately saved new experiments. Section 9 records
what those results establish and the remaining research limits. The report
makes no publication-priority or broad competitive-performance claim.

The source is [main.tex](main.tex), with [extensions.tex](extensions.tex),
[computation.tex](computation.tex), [completion.tex](completion.tex),
[evidence.tex](evidence.tex), and [references.bib](references.bib). References
come from the continuation's [primary-source audit](../literature/source-ledger.md).
The [continuation index](../README.md) and
[implementation completion index](../completion/README.md) link the full
proofs, source code, reviews, reproduction commands and raw evidence.

Build only this report, from this directory:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The generated PDF is retained. TeX auxiliary files are ignored locally.
The document uses ordinary TeX Live packages and BibTeX; no shell escape is
needed. This command does not run research experiments or any other
paper's checks.

The [core mathematical review](reviews/core-review.md) checks the original
proof chain. The [completion review](reviews/completion-review.md) checks
the added proofs, implementation claims and evidence against the saved
artifacts. Both are research-agent reviews, not journal peer review.
[VERIFICATION.md](VERIFICATION.md) records the report-only build, link and
rendering checks actually performed.

Computational tables are summaries, including incomplete runs. Full
per-run data, source hashes, certificates, timing boundaries and resource
limits remain in the linked experiment directories. Exact certificate
acceptance, theoretical complexity and measured usefulness are stated
separately. No project-wide verification or CI status/log inspection was
performed for this report.
