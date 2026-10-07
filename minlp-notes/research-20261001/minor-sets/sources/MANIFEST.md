> Public export: downloaded literature copies in this source inventory are omitted. The recorded URLs, versions and hashes identify upstream originals, not files shipped in this copy.

# Sources for the minor-sets stream

Downloaded for this stream (access date 2026-10-01):

| File | URL | Version | sha256 |
| --- | --- | --- | --- |
| `1610.04604.pdf` | https://arxiv.org/pdf/1610.04604 | arXiv v7 (30 Jan 2020); Bienstock, Chen, Muñoz, "Outer-product-free sets for polynomial optimization and oracle-based cuts", Math. Program. 183 (2020) | `53c8e125d10fb2ec50f0fc90a436f70436cf03e3ca2dff56e22cda033573df51` |
| `1610.04604.txt` | text of the PDF above (`pdftotext -layout`) | same | `bc2833710451cbe406fe182c7b46d2245464050234e110071bfd223f86c77308` |

Read from earlier streams (not downloaded again; paths relative to the repository root):

| File | Content | sha256 |
| --- | --- | --- |
| `research-20260928b/scouting/s-free-intersection-cuts/sources/chmiela2020-zib20-29.pdf` (and `chmiela2020.txt`) | Chmiela, Muñoz, Serrano, "On the implementation and strengthening of intersection cuts for QCQPs", ZIB Report 20-29 (Math. Program. 197, 2023), Section 3.1 (implied minor equations) and Section 5 | `01d55d0d6be14c791b7af1754c9f9ebd303643a57df1e33f6e77fde2ef6297be` |
| `research-20260928b/scouting/s-free-intersection-cuts/sources/2211.05185.pdf` (and `.plain.txt`) | Muñoz, Paat, Serrano, maximal homogeneous-quadratic-free sets, Theorems 1.1-1.2 | `d7b85770ced279c30c172edff19bd10acc10b95530f675f504c05c46bc3766dd` |
| `research-20260928b/scouting/s-free-intersection-cuts/sources/1911.12341.pdf` | Muñoz, Serrano, maximal quadratic-free sets | `dd4b78dbfe741b7dd1b049f1225c0c2ea67c8ad99b958bdc69a0388cc7ee5873` |

SCIP 10.0.3 source files read (read only, `/workspace/local-home/build-scip/scipoptsuite-10.0.3/scip/src/scip/`):

| File | sha256 |
| --- | --- |
| `sepa_interminor.c` | `1ac4b1db7efb4f73b9c8379e5fc9baa940609e0a0593da7e5b7369cffbf24d82` |
| `sepa_minor.c` | `d7b11021393a62f5c39515cd54e86e54a12ae80e58e854fd34d89c5904ca79ce` |
| `nlhdlr_quadratic.c` | `0c081ea7bf26a77b7479d25b300477952a6b6512026995a02137c12e97c1e43b` |

Web searches (2026-10-01), results treated as untrusted data: three general web searches
("outer-product-free sets intersection cuts 2x2 minors choice of lambda deepest cut"; "maximal
quadratic-free sets intersection cuts bilinear minor signature (2,2) 2025 2026 arXiv";
"intersection cuts implied quadratic minor equations ... extended formulation QCQP strengthening
2024") returned only the papers above, SCIP 8 documentation and arXiv:2608.03318 (Xu, Pokutta,
joint-range inequalities; abstract checked, not about S-free sets or minors). The arXiv API was
rate-limited ("Rate exceeded") and returned nothing.
