# Stage 4, round 1: independent reviewer 5

Verdict: no major integration, mathematical-summary, or attribution issues
found. Two minor bibliography issues remain. I reviewed the abstract,
introduction/table, model additions, conclusion, bibliography and rendered
`main.bbl`, source map, author report, README, Makefile, package script and
submission archive. I did not edit the manuscript or consult other reviews.

## Numbered findings

1. **Minor — render the full-version identifiers actually needed by the
   theorem citations.** `plainnat` does not print the `eprint` fields in
   `bibliography.bib`. Consequently, the rendered CGJ reference
   (`main.bbl:123–131`) links only to its 14-page ICALP publication, while
   the introduction and Section 6 invoke Theorem 33 of the full version.
   The rendered Apers–Gribling reference (`main.bbl:42–47`) says “arXiv
   version 3” but gives no identifier or arXiv URL. Montanaro–Shao has the
   same bibliography problem (`main.bbl:270–277`), although Section 4 does
   give its identifier in prose. **Fix:** add explicit versioned arXiv URLs
   or identifiers in a field rendered by `plainnat`, retaining publication
   metadata. Relevant locators are CGJ `1804.01973v2`, Apers–Gribling
   `2311.03215v3`, and Montanaro–Shao `2311.06999v3`. Also say “Theorem 33
   in the full version” in the introductory CGJ citation for consistency.
   This is a source-locatability issue, not a dispute about the theorem used.

2. **Minor — complete two available journal metadata records.**
   `bibliography.bib`, keys `AaronsonAmbainis2018` and `ApersGribling2026`,
   omit volume, issue and page range, which also makes the rendered
   bibliography incomplete. The primary SIAM records give, respectively,
   *SIAM Journal on Computing* **47**(3), 982–1038 (2018), and **55**(1),
   93–134 (2026). Add those fields and regenerate the bibliography/PDF/ZIP.
   Primary evidence:
   [Aaronson–Ambainis](https://epubs.siam.org/doi/abs/10.1137/15M1050902?journalCode=smjcat)
   and [Apers–Gribling](https://epubs.siam.org/doi/10.1137/25M1736098).

Major findings: none. No other minor findings.

## Summary-to-theorem checks

- The abstract's classical upper has the correct `kappa epsilon^-2`
  statistical multiplier and square-root-condition polynomial degree. It
  does not multiply the two separate lower families.
- All six table rows match the stated theorems. The caption carries the
  parameter-selected dimensions, population restrictions, two-form clock
  reduction, oracle-preserving composition hypothesis and separate state
  preparation cost. The sparse quantum gap remains explicitly unmatched.
- The introduction's simultaneous `epsilon^-2 s^{Omega(sqrt(kappa))}`
  example and restricted high-accuracy `kappa^2` product agree with Section
  5. It does not claim that the statistical and complete approximation
  factors of the generic upper are simultaneously necessary.
- The plain block-encoding claim charges the system block and correctly
  excludes exact-entry access. Its three-dimensional lower family and the
  attributed variable-time upper are compatible with the table.
- The optimization summaries preserve the distinction between ordinary
  value, selected coordinate, decrement and full feasible-vector output.
  The affine-slice barrier and hidden equality-elimination caveat agree with
  Section 7. The trajectory/endpoint summaries do not claim a generic
  iteration-by-iteration information lower bound.
- The structured summary accurately describes the sparse full-rank base,
  source-vector access, fixed approximate vector, flagged capped sampling,
  spectral assumptions and separately charged geometric-mean acquisition.
  Profile and latent-width full-output comparisons are not described as
  weak-output lower bounds.
- The added barrier, local norm, central point and predictor definitions
  are consistent with the conventions in Sections 7–10, including
  equality restriction and the difference from augmented-KKT conditioning.
- The conclusion adds no stronger theorem than the body. It leaves the
  unmatched parameter regimes open and preserves the limitations on input
  acquisition, iteration reuse and outer residual contracts.

## Literature and novelty audit

The novelty paragraph is qualified and identifies precise statements,
while expressly declining priority for the established ingredients. The
related-work section covers the important nearby scalar, matrix-function,
sampling, optimization, state-output and structured-solver comparators.
No inspected comparison transfers a result between incompatible interfaces.

I independently checked the current primary records and relevant full-text
locators for the new/current comparisons:

- [Edenhofer–Hasegawa–Le Gall, v3](https://arxiv.org/html/2509.20183v3)
  is dated 12 August 2026. Theorem 3.1 and Section 3.3 concern sparse
  polynomial spectral-sum estimation, including reciprocal traces, as the
  introduction states. Their prior polynomial method is not claimed here
  as new.
- [Zhao et al., primary PDF](https://arxiv.org/pdf/2604.07639)
  and [current record](https://arxiv.org/abs/2604.07639) identify the April
  2026 version and listed authors. Task F.1 is a normalized solution
  quadratic observable, and its input is a data-generation process. The
  nearby lower bounds restrict classical space; the present introduction
  explicitly does not import those restrictions or lower bounds.
- [Le Gall, current record](https://arxiv.org/abs/2304.04932)
  supports the robustness comparator. Section 3's new attribution does not
  relabel its elementary sufficient transfer as a general first robustness
  result.
- [Cifuentes et al., current preprint](https://arxiv.org/abs/2410.13937)
  supports the matrix-element/local-measurement classification description.
  The [APS recent-publications listing](https://journals.aps.org/prxquantum/recent?page=4)
  confirms *PRX Quantum* 7, 020364, published 18 June 2026. The direct DOI
  fetch was unavailable in this review; the publication metadata is also
  corroborated by that primary publisher listing.
- Current primary records confirm [Grønlund–Larsen v5](https://arxiv.org/abs/2411.02087),
  [Montanaro–Shao v3](https://arxiv.org/abs/2311.06999),
  [CGJ v2](https://arxiv.org/abs/1804.01973), and the
  [Apers–Gribling publication](https://epubs.siam.org/doi/10.1137/25M1736098).

The source map retains explicit exclusions for neighboring geometry and
other output-contract programs. Stage 4 does not relabel these exclusions
as completed proofs or incorporate obsolete claims by implication. Earlier
reviewed corrections to transformed-column access and temporal reuse are
reflected in the integration.

## Standalone and reproducibility checks

- The archive contains 24 files, passes its ZIP CRC check, and contains no
  audit paths. Every archived file matched its current repository counterpart
  byte for byte at the time of review.
- I independently extracted the archive into a fresh temporary directory
  and ran `conda run -n qipm --live-stream make -B`. It succeeded, producing
  a 59-page PDF with no warnings, undefined references/citations, or
  overfull/underfull boxes in its final log.
- `make check PYTHON=/home/sgusev/miniconda3/envs/qipm/bin/python` passed all
  five diagnostic scripts.
- README and Makefile commands match the delivered layout. The package
  includes its bibliography and `main.bbl`, diagnostics, and build
  instructions. The README correctly separates diagnostics from proofs and
  internal reviews from external peer review, and does not invent authorship.

Regenerate the package after the bibliography corrections. The separate
whole-manuscript review remains necessary; this report assesses Stage 4's
integration and deliverables rather than replacing that review.
