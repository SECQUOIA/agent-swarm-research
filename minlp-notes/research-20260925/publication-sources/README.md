# Retained primary sources

The [source manifest](source-manifest.json) records primary artifacts used in
the September 25 research and publication-readiness reviews. It identifies
versions, public source URLs, repository paths, SHA256 digests, file sizes,
provenance, and known retrieval dates. Paths in the manifest are relative to
the repository root. Existing literature and penalty-source artifacts are
referenced without another copy.

Every newly retained PDF passed a PDF-header check and `pdftotext -layout`.
The manifest's file paths, sizes, and hashes were checked directly. These
checks establish artifact integrity and text extraction, not correctness of
the papers or their mathematical use. The research review notes document
the mathematical comparisons separately. Null inspection or retrieval
timestamps mean that exact time was not recorded; the retention timestamp
does not replace it.

Two source-identity details matter for reproduction:

- The Anstreicher–Puges HTML previously inspected at
  `https://arxiv.org/html/2501.09150v1` displays a manuscript date of August 24,
  2026. The PDF downloaded from the corresponding pinned v1 URL displays
  January 17, 2025. Both artifacts are retained. Cite the artifact and checked
  formulas; do not infer their equivalence or chronology from the URL alone.
  The later [priority audit](../publication-quadratic-priority-audit.md)
  checks equations (14)–(16) and Lemmas 4–5 across these copies and the
  current Optimization Online manuscript and reports agreement.
- The Basu–Roy source is the final author manuscript dated June 5, 2010. Its
  formulas supersede the 2009 draft. The Basu quantifier-elimination source
  is the exact author-survey PDF used by the review, whose bytes differ from
  the repository's arXiv copy.

Other apparent manuscript or template-date anomalies are recorded per source
in the manifest. The Sun–Wang–Li-Jost–Fei article is retained as complete
primary HTML because the PMC PDF endpoint returned a non-PDF response.
