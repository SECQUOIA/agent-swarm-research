# Sparse-SOS knowledge-base intake receipt

This receipt records the supplied-source intake and final package states. The source-lane theorem comparison is in [`literature-lanes/`](literature-lanes/); the paper aggregate literature audit is maintained separately.

## Outcomes for all 29 supplied works

The 29 distinct works comprise 10 recourse sources, 13 sparse-hierarchy sources, and 6 standards sources. All 29 were accepted into the KB. Twenty-one packages are read; eight remain metadata-only and unread. Kahl was first created as metadata-only after an HTML fetch, then promoted from the verified author PDF; the promotion is not an additional work. Tran–Toh's preprint and journal article are one work represented by one KB package.

| Batch | Current citation key(s) | KB slug | Final package state |
|---|---|---|---|
| Recourse | `baotic2016-gradient-value-function` | `baotic2016-gradient-of-the-value-function` | Created; open full text; read |
| Recourse | `kahl2005-globally-optimal-estimates` | `kahl2005-globally-optimal-estimates-for-geometric` | Created metadata-only after HTML fetch; promoted from supplied author PDF; read |
| Recourse | `lasserre2009-convexity-sdp` | `lasserre2009-convexity-in-semialgebraic-geometry-and` | Created; open full text; read |
| Recourse | `lasserre2010-joint-marginal` | `lasserre2010-a-joint-marginal-approach-to` | Created; open full text; read |
| Recourse | `miller2025-sparse-matrix` | `miller2026-sparse-polynomial-matrix-optimization` | Created; open full text; read |
| Recourse | `pena2018-hoffman-constants` | `pena2018-an-algorithm-to-compute-the` | Created; open full text; read |
| Recourse | `piazzon2018-chebyshev-grids` | `piazzon2018-a-note-on-total-degree` | Created; open full text; read |
| Recourse | `qu2024-correlatively-sparse-lagrange` | `qu2024-a-correlatively-sparse-lagrange-multiplier` | Created; open full text; read |
| Recourse | `zhang2025-wasserstein-moment` | `zhang2025-moment-relaxations-for-data-driven` | Created; open full text; read |
| Recourse | `zhong2024-two-stage-polynomial` | `zhong2024-towards-global-solutions-for-nonconvex` | Created; open full text; read |
| Sparse hierarchy | `baldi2024-putinar-hypercube` | `baldi2024-degree-bounds-for-putinar-s` | Created; open full text; read |
| Sparse hierarchy | `catala2024-singular-measures` | `catala2024-approximation-and-interpolation-of-singular` | Created; HTML-only import; metadata-only/unread in KB; primary HTML read in source lane |
| Sparse hierarchy | `dklerk2017-improved-upper-bounds` | `klerk2017-improved-convergence-rates-for-lasserre` | Created; open full text; read |
| Sparse hierarchy | `gamertsfelder2025-countable-gmp` | `gamertsfelder2025-the-effective-countable-generalized-moment` | Created; open full text; read |
| Sparse hierarchy | `gribling2026-squared-kernels` | `gribling2026-squared-polynomial-approximation-kernels-for` | Created; open full text; read |
| Sparse hierarchy | `grimm2007-structured-sparsity` | `grimm2007-a-note-on-the-representation` | Created; open full text; read |
| Sparse hierarchy | `han2018-local-moment-matching` | `han2018-local-moment-matching-a-unified` | Created; open full text; read |
| Sparse hierarchy | `korda2025-convergence-rates-sparsity` | `korda2025-convergence-rates-for-sums-of` | Created; open full text; read |
| Sparse hierarchy | `laurent2023-effective-schmudgen` | `laurent2023-an-effective-version-of-schmudgen` | Created; landing-page HTML only; metadata-only/unread in KB; open CWI text read in source lane |
| Sparse hierarchy | `magron2025slides-lorentz` | `magron2025-sparse-polynomial-optimization-applications-solution` | Created; HTML-only fetch; metadata-only/unread in KB; retained author PDF read in source lane |
| Sparse hierarchy | `magron2026slides-tenors` | `magron2026-non-linear-moment-problems-theory` | Created; HTML-only fetch; metadata-only/unread in KB; retained author PDF read in source lane |
| Sparse hierarchy | `nie2026-sparse-tightness` | `nie2026-a-characterization-for-tightness-of` | Created; HTML-only import; metadata-only/unread in KB; primary publisher HTML read in source lane |
| Sparse hierarchy | `tran2026-truncated-moment-sequences` | `tran2026-on-the-convergence-rates-of` | Created; arXiv v1 preprint open and read; 2026 journal full text unavailable |
| Standards | `bental2001-lectures-modern-convex` | `tal2001-lectures-on-modern-convex-optimization` | Created from supplied original; read |
| Standards | `heijmans2026-degree-bounds` | `kuryatnikova2026-degree-bounds-for-positivstellensatze-of` | Created from supplied arXiv v2 original; read |
| Standards | `powers2000-univariate-interval` | `powers2000-polynomials-that-are-positive-on` | Created from supplied author PDF; read visually at relevant page; text extraction garbled |
| Standards | `kallenberg2002-foundations` | `kallenberg2002-foundations-of-modern-probability` | Created metadata-only; full text paywalled; unread |
| Standards | `rudin1987-real-complex-analysis` | `rudin1987-real-and-complex-analysis` | Created metadata-only; no lawful full text located; unread |
| Standards | `vorobev1962-consistent-families` | `ev1962-consistent-families-of-measures-and` | Created metadata plus publisher abstract; article full text unavailable; unread |

The Tran citation key is the one present in the current manuscript citation request. The source lane also retains a second provisional key alias for the same work; it does not identify a second source or package.

## Source contracts and limits

- **Interval SOS conversion:** Powers–Reznick, p. 4681 (author PDF p. 5), gives the nonnegative even- and odd-degree interval forms with degree-preserving bounds; the forms include polynomials with zeros. The page was visually checked because the PDF's text extraction is garbled.
- **Finite SDP dual attainment and separation:** Ben-Tal–Nemirovski, Theorems 2.4.1–2.4.2, printed pp. 57–58 (PDF pp. 72–73), supports the stated primal-Slater/finite-lower-bound dual-solvability premise and finite-dimensional separation under the book's hypotheses.
- **Positive lift and degree substitution:** Heijmans-Kuryatnikova–Vera–Zuluaga, arXiv:2605.15821v2, Theorem 2, pp. 8–9, and §3, supplies the cited lift and fixed-generator substitution relation. The displayed logarithmic composition is an inference for the dense lifted formulation; the sparse rates are proved separately in the manuscript.
- **Partial PMI lifting:** Kahl–Henrion, §2.2, p. 3 of the correct LAAS author PDF, limits linearization to selected nonlinear variables and says this partial method does not generally ensure asymptotic convergence; rank one on the selected moment matrix certifies the particular solution.

The three standards sources still lacking full text are **two books** (Kallenberg 2002; Rudin 1987) and **one article** (Vorob'ev 1962). Tran–Toh is a separate version-specific gap: the cited journal version was not retrieved, while the same work's arXiv:2507.00572v1 preprint is locally read. Do not transfer preprint locators to the journal version.

## Archives, check, and stopping record

Archived input records are preserved at:

- [`literature/runs/2026-10-06-sparse-sos-supplied-sources/`](../../literature/runs/2026-10-06-sparse-sos-supplied-sources/): recourse round 1, kernel round 2, and the explicitly provisional incomplete round 3.
- [`literature/runs/2026-10-06-sparse-sos-standards-supplied/`](../../literature/runs/2026-10-06-sparse-sos-standards-supplied/): standards round 1 and Kahl promotion round 2.

The supplied round directories compare identical to their archived copies; the promoted Kahl PDF is also byte-identical to the retained original. The candidate intake was bounded to the supplied sources; no new discovery round was opened. Stopping reason: all supplied sources were processed, the missing full texts were recorded with their actual access states, and no additional discovery was requested.

Earlier sparse search artifacts are preserved at [`literature-discovery/earlier-raw-round-1/`](literature-discovery/earlier-raw-round-1/) (four raw lane files) and [`literature-discovery/earlier-api-captures/`](literature-discovery/earlier-api-captures/) (eleven API responses), with original paths, byte sizes, and hashes in [`earlier-artifact-manifest.json`](literature-discovery/earlier-artifact-manifest.json). These are incomplete search artifacts, not a complete `$lit` run archive: the lane files have no candidate, decision, result, or run-account files, and the API captures have no round lane or candidate/result records. They are separate from the completed supplied-source rounds above; this supplied-source receipt does not claim discovery saturation.

After the latest package-note edits, the direct check completed on 2026-10-06 at 05:59 UTC, exit code 0:

```text
WARNING: unread packages: 197
WARNING: andretta2008-topicos-em-otimizacao-com-restricoes: possible preview or excerpt (1 pages for type thesis)
WARNING: huang2011-operative-planning-of-water-supply: possible preview or excerpt (1 pages for type thesis)
WARNING: kaminetz2025-everything-is-vecchia-unifying-column: possible preview or excerpt (25 pages for type thesis)
KB_CHECK=ok
UNREAD=197
READ_UNCITED=770
```

The preview warnings are three existing unrelated KB warnings. The Peyrl–Parrilo record and generated reference now correctly identify first author **Helfried Peyrl**.
