# Independent final referee 4 evidence

Reviewed frozen `final-round1` candidate on 2026-09-09. No frozen source was edited. All imports, generated reports, and the LaTeX build used the private archive extractions in this directory. No other referee reports or adjudications were read. The review brief and permitted literature audit/source evidence were inspected.

Actual checks:

- Both extracted payload manifests: 19 source files and 39 supplement files passed SHA-256 verification.
- `latex-source/`: documented latexmk command succeeded; final `main.log` contains no warnings, overfull boxes, or underfull boxes. `main.pdf` is 50 pages, 613974 bytes, SHA-256 `21d09299cee1b7f9c6deece832a29aa6d96bb3402bcefdf9ca8e1c7d8aaff816`, identical to the submitted PDF. Initial-pass unresolved references in the combined build log resolved normally.
- `principal-tests.log`: all 23 documented principal tests passed.
- `fibonacci-facets.log`: supplied check passed q=3,4. LP proposes a normal; exact checks establish all-vertex validity, affine dimension, codimension-one support face, ratios 2 and 3, and simple-graph path lifts.
- `repairs.log`: supplied check passed 512 negative-two and 27 positive-two endpoint patterns, 1617 repair choices, and the four-label local witness/rejection checks.
- `own_fibonacci.py` / `.json`: independently written exact SymPy reconstruction from the manuscript, with no production-code import. q=3 through 15, 327 feasible rational witnesses and 310 points rejected by the necessary weighted inequality. Checked D and complement K invertibility, balancing identities, observation count, full a/b/bypass state bounds and aggregate equalities. Largest tested ratio 610. The finite grid includes both boundary and strictly feasible perturbations. This is a finite proof check, not a replacement for the all-q argument.
- `tables.log` / `post-tables-manifest.log`: documented table generator passed; every original payload hash still matched after regeneration.
- Local environment: Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0, SymPy 1.14.0.

Primary sources personally inspected:

1. De Loera–Onn, author-hosted published PDF: https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf (also downloaded here as `transportation.pdf`). Theorem 1.1 and its coordinate-erasing definition, pp. 807–808; Section 3.3 first-layer injection and margin construction, p. 816; polynomial size estimate, p. 818. The source proves the exact coordinate retention and polynomial encoding needed by the transfer.
2. Khademnia–Davarnia, published advance article: https://par.nsf.gov/servlets/purl/10546393 (`predecessor.pdf`, stripped-layout text `predecessor.txt`). Theorem 1, Section 3 balance signs, Example 2, Theorems 2 and 3. Browser retrieval failed, direct Python HTTPS download succeeded. The printed claims credited in the submission agree with these passages.
3. Almoghrabi–Skutella–Warode, publisher full text: https://link.springer.com/article/10.1007/s10107-026-02392-8, Theorem 1 and Remark 1. The distinction between total-flow and full commodity-vector decomposition is explicit.
4. Existing primary full-text extractions in `../literature/`: Davarnia dissertation Proposition 2.6, pp. 28–29; Liberti–Pantelides Theorem 3.1 and the subsequent McCormick warning, pp. 7–9; Kis–Horváth Section 5.9 Proposition 22 and equations (30)–(31). The manuscript's corresponding attributions are accurate.

Limits: no rerun of the full five-repetition timing protocol, no general transportation universal-generator implementation, no exhaustive priority search, and no line-by-line audit of every production module. Complete manuscript proofs were reviewed directly. Supplement programs above were actually executed, rather than their pre-existing reports being counted as new evidence.
