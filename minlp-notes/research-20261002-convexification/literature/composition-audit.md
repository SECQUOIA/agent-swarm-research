# Composite and univariate convexification: primary-source audit

Checked on 2026-10-02. This audit covers five closely related sources. It is
a bounded claim comparison, not an exhaustive novelty determination. The
full-text result passages below were inspected. The 2021 and 2022 PDFs were
cached locally; their URLs and hashes are recorded in the tracked
[source manifest](sources/MANIFEST.md).

## He and Tawarmalani (2021)

Taotao He and Mohit Tawarmalani, *A new framework to relax composite
functions in nonlinear programs*, Mathematical Programming 190, 427–466
(2021). DOI: [10.1007/s10107-020-01541-x](https://doi.org/10.1007/s10107-020-01541-x).
Published online July 13, 2020; use 2021 for the journal volume.

The authors exploit estimators and bounds on inner functions, convexify over
a polytope `P`, and reduce separation to a simpler set `Q`. Crucially,
Section 5 treats a vector of outer functions. Theorem 6 transfers a
polynomial separation oracle for the simultaneous graph hull over `Q` to
one over `P`; the oracle remains an input to that result. Section 5.2
extends the construction to facet generation. [Publisher PDF](https://link.springer.com/content/pdf/10.1007/s10107-020-01541-x.pdf),
printed pp. 457–461, especially p. 458; PDF pp. 31–35.

**Boundary:** simultaneous graph convexification and oracle-based reduction
are established precedents. A concrete polynomial support oracle may add
implementation or certified-numerics value, but should not claim to
introduce simultaneous composite convexification.

## He and Tawarmalani (2022)

Taotao He and Mohit Tawarmalani, *Tractable Relaxations of Composite
Functions*, Mathematics of Operations Research 47(2), 1110–1140 (2022).
DOI: [10.1287/moor.2021.1162](https://doi.org/10.1287/moor.2021.1162).
Published online October 1, 2021.

For a concave-extendable outer function that is supermodular on the
relevant vertices, Theorem 2 gives facet generation in `O(dn log d)`
operations. Section 3.3 addresses simultaneous hypographs. Theorem 4 gives
equality between simultaneous and intersected individual hulls when the
envelopes share a triangulation. Corollary 7 specializes this to the
supermodular class and gives `O(kappa dn log d)` facet generation.
[Author manuscript](https://par.nsf.gov/servlets/purl/10382117), manuscript
pp. 14 and 20–21. Its pagination differs from the published article.

**Boundary:** simultaneous separation and a structural criterion for when
individual hypograph hulls suffice are prior results. These hypotheses do
not automatically hold for an arbitrary polynomial vector graph. The
distinction between graph hulls and one-sided hypograph hulls must remain
explicit.

## He and Tawarmalani (2024)

Taotao He and Mohit Tawarmalani, *MIP Relaxations in Factorable Programming*,
SIAM Journal on Optimization 34(3), 2856–2882 (2024). DOI:
[10.1137/22M1515537](https://doi.org/10.1137/22M1515537).
Preprint: [arXiv:2310.07168v3](https://arxiv.org/html/2310.07168v3).

Theorem 5 gives an ideal discretization formulation under a
concave-extendability condition; Remark 6 treats graphs. Theorem 9 connects
the construction to inner-function estimators. Section 7.2, Proposition 28,
extends it to vectors of composite functions and explicitly explains why
intersecting individual hulls can fail. The same section recalls the
supermodular exception from the 2022 paper. Remark 11 and Corollary 29
also explicitly formulate vector graph relaxations with shared variables.
These locators refer to the checked arXiv version; published numbering
may differ.

**Boundary:** shared discretization, vector composite relaxations, and
ideal formulations are established topics. A new block implementation
should specify its supported domains, separation costs, and certificate
contract, then compare against applicable existing formulations.

## Zhu, He and Tawarmalani (2026)

Haisheng Zhu, Taotao He and Mohit Tawarmalani, *Axis-Aligned Relaxations for
Mixed-Integer Nonlinear Programming*, [arXiv:2603.18458v1](https://arxiv.org/html/2603.18458v1),
March 2026.

Section 3.1, Theorem 7, identifies simultaneous multilinear graph hulls
over bounded axis-aligned regions from corner values. Section 3.2,
Algorithm 3 and Theorem 8, constructs convergent polyhedral relaxations
for multilinear compositions over bounded domains defined by Lipschitz
inequalities. Thus coupled feasible-domain approximation and simultaneous
factorable graph convergence already have direct precedents.

The implementation uses geometric hulls and voxelization. Section 5.2
reports 619 MINLPLib root-bound experiments; the discussion following
Table 5 leaves memoization and selective refinement for future work.
These are root-relaxation results, not proof of faster complete solves.

**Boundary:** broad claims of a first general block-convexification or
convergence framework are unsafe. Direct polynomial support minimization
with exact rational cut checking is a different mechanism requiring its
own comparison; stronger solver performance requires complete-solve tests.

## Li and coauthors (2026)

Tianwei Li, Daniel Ovalle, Barnabas Poczos, Carl Laird, Ignacio Grossmann
and Javier Pena, *Efficient Convexification of Kolmogorov-Arnold Networks
with Polynomial Functional Forms Via a Continuous Graham Scan Approach*,
[arXiv:2604.03871v1](https://arxiv.org/html/2604.03871v1), April 2026.

Section 3, Algorithm 5 and Theorem 11 construct the convex envelope of a
univariate polynomial from convex intervals and bitangents. The stated
envelope construction is exact mathematically. Section 2.1 assumes
relative-error arithmetic, excepting catastrophic cancellation; Algorithm
4 and Theorem 7 approximate bitangents to prescribed precision. Section 4,
equation (18), relaxes polynomial KANs using componentwise envelopes.

**Boundary:** exact scalar polynomial-envelope construction is already
studied. A separate checker proving validity of the final rational cut
coefficients is a stronger implementation contract than an assumed
relative-precision arithmetic model. Vector support cuts retain
dependencies across outputs that equation (18) relaxes componentwise;
this observation does not establish priority for vector hull methods.

## Version check

The primary arXiv submission histories were checked on 2026-10-02. The
latest listed versions are:

| Paper | Latest listed version | Submission date (UTC) |
| --- | --- | --- |
| [He and Tawarmalani](https://arxiv.org/abs/2310.07168) | v3 | 2024-06-15 |
| [Zhu, He and Tawarmalani](https://arxiv.org/abs/2603.18458) | v1 | 2026-03-19 |
| [Li and coauthors](https://arxiv.org/abs/2604.03871) | v1 | 2026-04-04 |

The 2024 paper was initially inspected as v2 and then rechecked in v3:
Theorem 5, Remarks 6 and 11, Theorem 9, Proposition 28, and Corollary 29
support the comparison above. The version update does not change its
conclusion.

## Consequences for this repository

The sentence in
[the earlier shared-variable audit](../../notes/shared-variable-terms-literature.md)
Section 2.4 saying that the 2021/2022 abstracts do not mention several
outer functions is incorrect. Both explicitly discuss vector extensions.
The result passages above establish that this is substantive overlap,
not merely wording in an abstract.

The defensible research focus is the implemented contract: recognizing
supported blocks, generating useful cuts within a controlled budget,
checking the exact coefficients and domain, and measuring complete-solver
benefit. These are proposed contributions to demonstrate, not established
novelty claims.

None of the five source comparisons establishes priority for Bernstein
support bounds or rational cut certificates. Those mechanisms need the
separate Bernstein, polynomial optimization, and validated-computation
audit. A text search that fails to find a technique is insufficient
evidence that it is new.

Verification performed: downloaded and extracted the two saved PDFs with
`pdftotext -layout`; inspected the cited result passages; checked the
remaining three papers in their linked arXiv full texts; checked DOI
metadata on publisher pages. No project-wide checks or CI inspection were
performed.
