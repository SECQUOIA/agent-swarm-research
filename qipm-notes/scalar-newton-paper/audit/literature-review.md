# Literature review and attribution ledger

Review started 2026-09-22. This is an internal source and search record; the
manuscript bibliography is standalone. Original sources control corrupted
extractions and local metadata. No search establishes priority by absence.

## Core comparisons checked

| Source | Primary evidence | Attribution boundary |
| --- | --- | --- |
| Gharibian and Le Gall, SICOMP 52(4), 2023, arXiv:2111.09079v5 | Local full text, Definitions 2.2–2.4 and Theorem 4.1 with its sampling-estimator proof; current arXiv metadata checked online | Sparse polynomial local evaluation and coordinate importance sampling are prior work. Relative positive inverse forms and their parameter-sensitive variance/lower-bound comparison require separate statements. |
| Montanaro and Shao, STOC 2024, arXiv:2311.06999v3 | Local full text, Theorems 1.5–1.10 and weighted clock construction; current arXiv abstract/version checked online | Approximate-degree query bounds, sparse matrix-function entry hardness, and Forrelation clocks are prior work. SPD affine shift, full-SQ simulation, positive relative outputs, and optimization realization must each be justified. |
| Grønlund and Larsen, arXiv:2411.02087v5 | Current arXiv and authors' Aarhus PDF; local source package | Exponential separation for sparse linear-system solution output is prior work. A scalar optimizer/decrement transfer is a distinct claim and must retain the input and accuracy contracts. |
| Chakraborty, Gilyén and Jeffery, ICALP 2019, arXiv:1804.01973 | Local full text, negative-power and variable-time norm-estimation results; current arXiv metadata | The inverse-square-root norm-estimation upper bound is a specialization of their theorem, not a new quantum primitive. |
| Gilyén, Su, Low and Wiebe, STOC 2019, arXiv:1806.01838 | Local source; current arXiv metadata | Block encodings, bounded polynomial transformations, and inverse-power implementation are prior work. |
| Li, Sra and Jegelka, ICML 2016, PMLR 48, pp. 1766–1775 | Primary PMLR publication page and local source | Matrix-inverse-form estimation and quadrature are established. Distinguish matrix-vector-product access from local sparse and vector SQ access. |
| Andoni, Krauthgamer and Pogrow, ITCS 2019 | Local primary-source package | Sublinear linear-system algorithms are prior work; compare structural assumptions and local output, not merely the phrase dimension independent. |
| Cifuentes, Wang, Silva, Berta and Aolita, arXiv:2410.13937v2 | Current arXiv and local source | Matrix-element and local-measurement complexity with sparse/Pauli access provides an existing classification. The present relative SPD observable has a different output normalization. |

## Metadata correction

The local Gharibian–Le Gall bibliography title ends in “Gradient Estimation
and Faster Matrix Inversion.” That is not the title of arXiv:2111.09079.
The manuscript uses the verified title “Dequantizing the Quantum Singular
Value Transformation: Hardness and Applications to Quantum Chemistry and the
Quantum PCP Conjecture.” Existing literature files were left untouched.

## Online search record

Queries included “inverse quadratic forms quantum relative estimation sparse,”
“Newton decrement sampling quantum,” “sparse quadratic forms sample quantum
complexity,” and broader 2025–2026 sparse-SQ/relative-form queries. Exact-phrase
searches were sparse and noisy; they are not affirmative evidence of novelty.
Primary arXiv records were opened for 2311.06999, 2411.02087, 2111.09079,
2410.13937, 1804.01973, and 1806.01838. The PMLR article page for Li–Sra–Jegelka
was also checked.

A recent numerical comparator was located: Bizas, Mitrouli and Turek,
“Efficient estimates for matrix-inverse quadratic forms,” Applied Numerical
Mathematics 208 (2025), 76–91, doi:10.1016/j.apnum.2024.01.013. Its primary
publisher text describes matrix-vector-product-based analytic and heuristic
estimates, including backward-error analysis. This is relevant numerical
context, not evidence of a sparse-SQ query-complexity collision. An open copy
is available on the University of Athens course site.

## Required final positioning

Do not claim a first classical inverse-form estimator, first sparse
dequantization, first exponential matrix-function separation, or a new
variable-time inverse-power quantum algorithm. State precisely the access,
relative-error, positivity, and LP/SOCP transfer refinements. Distinguish
proved joint bounds from separately sharp factors and conditional composition.
The search must be supplemented by theorem-level checks in each author/review
stage and the final introduction must reflect the corrected results.

## Additional primary-source checks during Stage 2

- Alase, Nerem, Bagherimehrab, Høyer and Sanders, *Tight Bound for Estimating
  Expectation Values from a System of Linear Equations*, Physical Review
  Research 4, 023237 (2022), DOI 10.1103/PhysRevResearch.4.023237,
  [arXiv:2111.10485](https://arxiv.org/abs/2111.10485). Local full text and
  current primary metadata checked. Their tight observable-block-encoding
  query bound concerns additive estimation of a quadratic observable of a
  linear-system solution. Its queried observable and error normalization
  differ from the relative inverse-form/H-oracle bound here. This comparator
  must appear in the final related-work discussion.
- Edenhofer, Hasegawa and Le Gall, *Dequantization and Hardness of Spectral
  Sum Estimation*, [arXiv:2509.20183v2](https://arxiv.org/html/2509.20183v2),
  revised 10 August 2026. Checked primary HTML, Theorem 3.1 and Sections
  1.3 and 3.3. Their spectral-trace algorithms use the same established
  sparse polynomial evaluation principle, with reciprocal applications.
  The present paper must not claim that principle or its square-root
  conditioning degree as a first result. Its arbitrary-vector relative
  estimator, variance factor, access-preserving reductions, and composition
  statements need their own narrow positioning.
- Cifuentes et al. now has a journal version: *Quantum Computational
  Complexity of Matrix Functions*, PRX Quantum 7, 020364 (18 June 2026),
  [DOI 10.1103/g5x4-jcsz](https://doi.org/10.1103/g5x4-jcsz).
  Final bibliography should cite this publication, retaining the arXiv
  identifier where version-specific theorem locators are used.

Primary sources located for subsequent stages (the author still needs to
check the exact theorem used): Buhrman–Newman–Röhrig–de Wolf,
[*Robust Polynomials and Quantum Algorithms*](https://homepages.cwi.nl/~rdewolf/publ/qc/robust_journal.pdf),
arXiv:quant-ph/0309220, supplies collective recovery of Boolean outputs;
Roy–Xiao's [author manuscript](https://www.microsoft.com/en-us/research/wp-content/uploads/2018/01/powercones-5a71024933c4b.pdf)
and DOI 10.1007/s11590-021-01748-7 supply the generalized-power barrier;
Chen–Goulart, [arXiv:2305.12275](https://arxiv.org/abs/2305.12275),
explicitly exploit existing sparse and low-rank nonsymmetric-cone Hessian
structure. None of these established primitives should be claimed as new.

## Stage 3a theorem-level checks

- CGJ full-version Theorem 33 was checked against the original PDF: for
  c=1/2 its q=max(1,c) parameter is one, the matrix cost is ακ, and the
  state-preparation term is √κ. The norm-estimation theorem, rather than
  merely inverse-state preparation, is the cited upper primitive.
- Bansal–Sinha Theorem 1.3 and Corollary 1.4 use the positive high promise
  Φ≥2^(-5k) and the low promise |Φ|≤2^(-5k-1). The manuscript now states
  this exact source promise. Its magnitude-output lower conclusions hold
  by restriction to that promise, rather than attributing an unstated
  absolute-high theorem to the source.
- Alase et al. Theorem II.19 and IV.13 provide the tight observable-block
  expectation complexity for a supplied normalized state. Their full
  linear-system task has additional system conditioning costs; these are
  not suppressed in an alleged joint frontier. Section 6 states the
  narrower and accurate comparison.
- Apers–Gribling arXiv:2311.03215v3, Lemma 8.5, explicitly proves an Ω(n)
  full-SQ classical LP value lower bound. The manuscript cites it and
  disclaims priority for optimization SQ hardness. The construction here
  is positioned through its joint K/s/accuracy accounting, public norm
  tilt, and precise scalar/decrement interfaces.
- Motlagh–Wiebe, PRX Quantum 5, 020368 (2024), has a unit-circle boundedness
  condition in its generalized signal-processing characterization. The
  Laurent Bernstein argument retains that domain and does not mistake
  removal of parity restrictions for removal of boundedness.

Primary arXiv metadata pages 2111.10485, 2008.07003, 2308.01501, and
2311.03215 were opened on 2026-09-22. The corresponding verified DOI entries,
and the Quantum 5, 427 (2021) SOCP-output comparator, are now in the paper's
bibliography. The global minimal SOC-lift theorem is deliberately excluded
as a separate repository program; the elementary norm-tree construction is
proved here without claiming it is new or globally optimal.

Further current-version checks: Apers–Gribling
[arXiv:2311.03215v3](https://arxiv.org/html/2311.03215v3), revised 30 January
2026, Lemma 8.5 already proves a classical full-SQ lower bound for an LP's
ordinary optimal value; Theorem 8.4 gives other oracle value lower bounds.
The new paper therefore cannot claim the first scalar LP value lower bound.
Mori et al., [arXiv:2601.16697v2](https://arxiv.org/html/2601.16697v2),
revised 24 August 2026, is now Quantum Science and Technology 11, 035063,
DOI 10.1088/2058-9565/ae89e0. Its Theorem 1 concerns sparse linear-system
state preparation at error at most 1/11; its main sparsity result has
constant state error. Neither is a scalar inverse-form theorem.

## Further synthesis checks for Stages 3c and 4

Primary arXiv records checked on 2026-09-22:

- Chia, Gilyen, Li, Lin, Tang and Wang,
  [arXiv:1910.06151v4](https://arxiv.org/abs/1910.06151), revised July 2023,
  gives the established low-rank SQ matrix-arithmetic framework. The
  journal version is JACM 69(5), Article 33, 72 pages (2022), DOI
  10.1145/3549524, verified against the final publication deposited by MIT.
  Cite this when discussing the structured-cone sampler;
  dimension-free SQ inner-product and mixture techniques are not new.
  The manuscript's sparse full-rank base plus few structured corrections
  has a different parameterization from a globally low-rank matrix.
- Le Gall, [arXiv:2304.04932v2](https://arxiv.org/abs/2304.04932), final
  journal version revised December 2024, explicitly treats approximate
  length-squared sampling in total variation for both sparse and low-rank
  dequantization. Cite as prior robustness work; the elementary coupling
  transfer in Section 3 is not a general first robustness theorem.
- Chia, Lin and Wang, [arXiv:1811.04852](https://arxiv.org/abs/1811.04852),
  and Gilyen--Lloyd--Tang, arXiv:1811.04909, already sample solutions of
  low-rank linear systems under SQ access. The claimed distinction must
  remain the stated sparse/structured parameters, not solution sampling
  itself. Use the consolidated framework as the main comparator unless
  a more specific theorem comparison calls for these antecedents.

These checks supplement the existing scalar, trace-estimation, and
optimization prior-art comparisons; they do not certify novelty by absence.

The trajectory-stage search also checked newer direct-product literature:
Ben-David--Blais, [arXiv:2512.08268](https://arxiv.org/abs/2512.08268)
(FOCS 2025), treats all success parameters and list-decoding variants;
Blanc--Koch--Strassle--Tan,
[arXiv:2405.16340](https://arxiv.org/abs/2405.16340) (CCC 2024), treats
strong distributional expected-query direct sums. These are relevant
background for the broader theory, but neither primary abstract supplies
an optimization/Newton construction, and the manuscript needs only the
older constant-error direct-sum and strong-XOR ingredients. No priority
is claimed for a general direct-sum theorem. The explicit random-target
proof is retained for its formulation-oracle accounting, not as a new
query-complexity result.

An additional current search found Zhao et al.,
[Exponential quantum advantage in processing massive classical data,
arXiv:2604.07639](https://arxiv.org/pdf/2604.07639) (April 2026).
The primary paper's Task F.1 estimates a normalized solution-state
quadratic observable, and Sections E.5/F use Forrelation circuit embeddings
for classical streaming-space and sample lower bounds. Its access model
is a data-generation process with explicit space restrictions and, in
the dynamic version, refreshing data. This differs from unrestricted-storage
static SQ query complexity and the positive inverse form studied here.
It is relevant adjacent scalar-readout/streaming prior work, not evidence
for importing its space lower bound into this manuscript. Stage 4 should
decide whether a brief comparison is useful; do not claim the first
Forrelation-based scalar linear-system separation.

## Lead checks during Stage 3c

The primary Dagstuhl version of Fürer, Hoppen and Trevisan, *Fast Gaussian
Elimination for Low Treewidth Matrices*, ESA 2025, LIPIcs 351, 116:1--15,
DOI 10.4230/LIPIcs.ESA.2025.116, was checked directly. Theorem 1 uses the
row--column bipartite graph and a supplied decomposition of width k and
size O(k(m+n)). Its O(k^2(m+n)) field-operation bound allows exact pivot
cancellations. The linear-system consequence is applicable after doubling
the symmetric graph's bags. It is not a floating-point stability theorem.

Targeted online queries for eccentricity-profile SOCP preconditioning,
sparse-plus-low-rank Newton sampling, and power-cone inverse sampling did
not identify a direct matching statement. Search results were sparse and
noisy, so this is only a search record, not evidence of priority. Established
SQ products and mixture sampling, Lorentz rank-two algebra, and sparse
elimination must retain their prior-work attribution.

Metadata follow-up for the synthesis stage: Lin's 2013 JMAA article is
402(1),127--132 (publisher verified). Le Gall's robustness article is
Computational Complexity 34, Article 2 (2025), DOI
10.1007/s00037-024-00262-3. Its March 2025 correction,
DOI 10.1007/s00037-025-00265-8, concerns open-access licensing, not a
mathematical correction (correction text checked). Edenhofer--Hasegawa--Le
Gall's current arXiv version is v3, 12 August 2026; the change from v2 adds
an author contribution statement. The theorem-level check above used v2.

## Stage 4 integration and metadata

Integrated the checked comparisons into Section 1 and retained theorem-level
attribution in the technical sections. Updated Cifuentes et al. to PRX
Quantum 7,020364 (2026), DOI 10.1103/g5x4-jcsz; supplied Lin's volume,
issue, and page range. Added Edenhofer--Hasegawa--Le Gall, current
arXiv:2509.20183v3, Le Gall's Computational Complexity 34,Article 2 (2025),
and Zhao et al., arXiv:2604.07639. The last is a brief adjacent-model
comparison, not an imported streaming-space bound. The licensing-only
correction is not cited as a mathematical correction.

Stage4 author reopened primary arXiv records for 2509.20183, 2304.04932,
and 2604.07639 on 2026-09-22 to verify authors, titles, and versions. The
Cifuentes DOI landing request failed in this tool; its publication metadata
uses the earlier primary-source check recorded above. Montanaro--Shao's
bibliography now identifies arXiv version 3, matching the theorem locators.
The newer spectral-sum and robust-SQ comparisons are phrased narrowly and
claim no priority for their existing primitives.
