# Sources for the encoding upper bounds

The manuscript uses the following primary results. Repository paths below
are relative to the repository root. The proofs of the cited general
algebraic theorems were inspected for their applied statements and height
clauses, not independently reproved.

| Primary source inspected | Location and use |
| --- | --- |
| Basu and Roy, *Bounding the radii of balls meeting every connected component of semi-algebraic sets*, final author manuscript June 5, 2010; J. Symbolic Computation 45(12), 1270–1279 | Theorems 3–4, printed p.5, and the proof on pp.12–14. Applies to weak sign conditions. The paper uses only basic closed systems and finite unions. The proof's factorial-bit term on p.12 is retained in the asymptotic majorant. Degree two gives logarithmic radius `(tau + log(S+1) + 1) 2^{O(d)}`. |
| Basu, *Algorithms in Real Algebraic Geometry: A Survey*, September 4, 2014 author version | Theorem 2.27, printed p.16. For quantifier block sizes 1 and h+2 and one free variable, the output degree and integer coefficient bitsize give `L^{O(k+1)}`. The output-height clause, not merely arithmetic operation complexity, is needed. |
| Grigoriev and Pasechnik, *Polynomial-time computing over quadratic maps I: sampling in real algebraic sets*, arXiv:cs/0403008v3 | Theorem 1.2, printed p.3, gives sampling degree and coefficient-bit bounds for fixed quadratic-map dimension. Theorem 1.5 on p.4 states an optimization extension and defers its proof. The manuscript cites only the proved sampling result as prior algebraic machinery and does not rely on Theorem 1.5. |
| Kamminga and Rudolph, arXiv:2411.03096v2 | Sections 6.3–7.2, especially equations (98), (101), Theorem 7.2 and its coefficient bounds; §8.5, Corollary 8.14 and equation (115), printed p.44, apply the framework to few-constraint QCQP. The bounded OptGP hypothesis is retained in the comparison. The manuscript's affine-face reduction and bounding ball explain its relation to this precedent. |

The first, second and fourth sources were read from the existing local
primary texts and PDFs under `research-20260925/publication-sources/`.
The Grigoriev–Pasechnik version was downloaded from
<https://arxiv.org/pdf/cs/0403008v3> into this folder's ignored
`evidence/sources/` and extracted with `pdftotext -layout`. Its author names,
version and journal reference were also checked on the arXiv primary record.
The Basu–Roy primary PDF and the Kamminga–Rudolph version page were opened
online to verify the retained sources. No repository literature files were
modified.

Kamminga–Rudolph's inspected PDF is headed *The Pure-State Consistency of
Local Density Matrices Problem: In PSPACE and Complete for a Class between
QMA and QMA(2)*, while its current arXiv version record uses *On the
Complexity of Pure-State Consistency of Local Density Matrices*. The
bibliography preserves the inspected PDF title and identifies v2 and its
April 8, 2025 posting, so the section locators are unambiguous.

The proof handles all needed degeneracies directly. Refined Slater yields
feasible-slice KKT certificates; active-gradient sparsification avoids putting
all row multipliers into the general radius dimension. No Slater condition
is used for an infeasible slice. In the fixed-count argument, deleting
inactive affine rows uses convexity, the added ball makes the reduced problem
compact, strict regularization gives invertible stationarity, and the
quantified limit permits multipliers to diverge. Rational affine-normal
inverses bound reconstructed real multipliers without asserting that those
multipliers or optimal values are rational.

The conservative-output corollary is a deduction added to this manuscript
development from the uniform encoding bounds and monotonicity. This does
not claim that conservative printing is globally new: Gu–Ahmed–Dey
Theorem 11 and Lefebvre–Schmidt Theorem 15 already cover encoding and
polynomial-time output for linear native constraints; the latter manuscript
explicitly notes the convex-MIQP extension. The extension here concerns
fixed positive nonlinear count or fixed continuous dimension. Finding an unknown active
face is unnecessary for that deduction: hardcode a universal exponent
constant and print a power of two larger than every promised input's
sufficient bound. No numerical constant was tuned, no calibration algorithm
was implemented, and no practical numerical-size bound is claimed.

## Primary artifacts

SHA-256 hashes identify the PDF versions actually inspected:

| Source URL | Local PDF | SHA-256 |
| --- | --- | --- |
| <https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf> | `research-20260925/publication-sources/basu-roy-2010-final.pdf` | `4bfd74a9e664cca71644ee97f17813cdcd6043fbd8467cdfb7e03bdee85518e6` |
| <https://www.math.purdue.edu/~sbasu/raag_survey2011_final-sep4-2014.pdf> | `research-20260925/publication-sources/basu-2014-author-survey.pdf` | `4d32f328179a354e8ad19b5fd07233581f8d0408ed39fc2a175d7461f9b949e4` |
| <https://arxiv.org/pdf/2411.03096v2> | `research-20260925/publication-sources/kamminga-rudolph-2411.03096v2.pdf` | `ec683f1d5840a42f17ba6b82c857f06b2b528af010c58da5bed8dbd4ab45a20a` |
| <https://arxiv.org/pdf/cs/0403008v3> | `paper-exact-penalties/evidence/sources/grigoriev-pasechnik-v3.pdf` | `3cc798595c32b0f2c2343c3d2c34113bf9aabe7d663d56015f221e4eb0253e44` |

The new PDF and extracted text remain local and are ignored by this folder's
`.gitignore`; existing repository primary artifacts were only read.

## Final source refinements

The block-elimination step now cites Basu, Pollack and Roy, *Algorithms in
Real Algebraic Geometry*, second edition, Springer, 2006, Theorem 14.16,
directly alongside Basu's survey Theorem 2.27. The lead inspected the
original book's rendered PDF pages 559–561 (the theorem on pages 560–561),
including both polynomial degree and coefficient bitsize conclusions; its
text extraction is garbled. The retained PDF is
`literature/papers/basu2006-algorithms-in-real-algebraic-geometry/original.pdf`,
SHA-256 `01ab763368db41c0760c60ee41760f9f23b4d0cb3edfa9ad41628d5f38c5e70c`.
Author URL: <https://www.math.purdue.edu/~sbasu/bpr-posted1.pdf>;
DOI: <https://doi.org/10.1007/3-540-33099-2>.
The manuscript uses asymptotic constants and has not numerically evaluated
them. Their existence suffices for the conservative-output corollary.

Kamminga–Rudolph's bibliography now includes the official ITCS 2026
publication: LIPIcs 362, 83:1–83:23, published January 23, 2026,
<https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2026.83>.
The lead checked this publisher record. Every mathematical section locator
continues to refer to the inspected full arXiv v2, not the proceedings
pagination.
