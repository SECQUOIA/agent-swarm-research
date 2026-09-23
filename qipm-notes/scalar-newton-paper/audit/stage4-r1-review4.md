# Stage 4, round 1 — independent review 4

## Verdict

No major scientific issue found in this integration stage. One minor build-dependency issue should be corrected. This review covers the new abstract, introduction and comparison table, barrier conventions, conclusion, bibliography integration, README, build rules, and submission archive. It does not replace the requested final review of the complete manuscript. I did not consult other reviewers' reports or edit manuscript sources.

## Finding

1. **Minor — declare the compiled bibliography as a required build artifact.** `Makefile:5–9` generates `main.bbl` as an undeclared side effect of the `main.pdf` rule, whereas `package` depends only on `main.pdf` and the packaging script requires both files. Consequently, if the PDF is current but `main.bbl` is missing, `make package` fails with `FileNotFoundError: Build the manuscript before packaging: main.bbl`; ordinary `make` does not repair this state. I reproduced this in a temporary extraction of the submitted archive after a successful forced build, deleting only its temporary `main.bbl`. Declare both artifacts in the dependency graph, or make the package target explicitly ensure/rebuild a missing bibliography. Keep the current documented forced-rebuild option. This is a minor robustness defect; the delivered archive currently includes a valid bibliography and builds successfully.

## Scientific and presentation checks

- The abstract and introductory summaries distinguish separate lower-bound families from simultaneous products. They do not claim that the full statistical and exponential lower factors multiply. The table further identifies population/promise restrictions and the oracle-preserving inner-family hypothesis.
- The block-access comparison is properly separated from exact coherent sparse entries. The table states the relevant normalization and parameter ranges, excludes state-preparation cost from the displayed block-call count, and leaves the general sparse quantum gap explicit.
- The clock summary and table caption correctly distinguish the two-public-form reduction from a lower bound for an algorithm accepting an arbitrary supplied form.
- The structured-system summary preserves the important interface and probability distinctions: sampled source columns, a fixed approximate solution, reusable setup, and bounded-cost draws with flags. It does not silently promise exact samples from the true solution or dimension-independent cost without the listed spectral/access conditions.
- The new barrier conventions define the restricted Hessian and local norms, separate central and analytic centers, and use the correct predictor squared-decrement scaling. The introduction explicitly limits the interpretation of Newton decrement to local progress/centrality under the stated objective and barrier.
- The contribution claim is qualified and enumerates specific statements. It expressly excludes priority claims for the established polynomial, Forrelation, scalar optimization, cone algebra, and recycling ingredients. The prior-work discussion explains the different input and output contracts rather than comparing rates without their assumptions.
- Current primary arXiv records support the newly introduced Edenhofer–Hasegawa–Le Gall spectral-sum reference, Le Gall's approximate-SQ robustness reference, and Zhao et al.'s adjacent streaming/data-model reference. The later literature-audit entry correctly gives Edenhofer et al. v3 as 12 August 2026; its earlier 10 August entry concerns the prior search state and does not create an incorrect manuscript citation.
- The conclusion summarizes the proved comparisons and explicitly retains unmatched general parameter regimes. It does not promise a complete end-to-end interior-point speedup.

## Artifact verification

- The ZIP passes its integrity check and contains 24 files. Every archived file matched the corresponding current file at review time; no audit files, absolute paths, or parent-directory traversal paths are included.
- Extracted the archive into a fresh temporary directory and ran `conda run -n qipm --live-stream make -B`. It succeeded and generated the 59-page PDF (651875 bytes), with no warnings, undefined references/citations, or overfull/underfull boxes in the final log.
- The README accurately specifies the qipm environment, dependencies, fixed-seed diagnostic scope, packaging contents, and author/venue metadata still to be supplied. Its statement that no external repository file is needed to build is supported by the independent archive build.
- The missing-bibliography experiment above was confined to the temporary extraction; no manuscript or submission files were changed.
