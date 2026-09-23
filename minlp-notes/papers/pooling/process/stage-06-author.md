# Stage 6 author audit

Author: /root/stage06_author. Date: 2026-09-05.
Scope: introduction/abstract, final substantive section, append-only bibliography,
all 23 stage-6 inventory rows. No later-stage work or review agents were started.
Sections 1–5 and main.tex were preserved.

## Contribution and proof map

- Introduction gives the central structural question, ranks algebraic/certificate,
  hardness/structural, and exact-contract contributions, and compares selected
  boundaries with objective, capacity, contract and arithmetic hypotheses.
  It is unnumbered so sections and theorem numbering remain stable.
- s6:certificate proves the full telescoping identity, endpoint vertex
  characterization, distinct terminal values, and tangent exposure. This supplies
  a self-contained shadow direction for all physical developments.
- s6:path-realization proves both directions of the physical descending-quality
  path mapping.
- s6:price-response proves ordinary-price telescoping, one varying terminal price,
  two-quality reset relays, supply/demand duplication, and uniform exact penalty
  removing every positive flow lower bound in the LINEAR family. The primary
  direction is d_j=3s_j^2, with physical coefficients 3s_j, prices at most three
  before penalties, and M=3N^N+1. The original Gärtner direction c_j=epsilon^(3(n-j))
  is retained explicitly, with its narrower interval and M=2N^N+1.
- s6:response-size proves state-message interval count and total polynomial degree
  lower bound for quantifier-free graph/epigraph descriptions. The following
  recurrence proves linear-operation pointwise evaluation. No circuit,
  extended-formulation or optimization lower bound is inferred.
- s6:ports proves closure of two-variable inequalities under coordinate projection
  and the three-coordinate simplex obstruction, with global-row and linear-image
  qualifications.
- s6:vertex-forcing proves every original interface balance, the active pool
  quality, the single nonlinear clean-flow bound, the complete economic identity,
  and all optimal flows. s6:local gives exact negative edge derivatives and the
  tangent-cone/local remainder argument. s6:integer-lift gives both parity lower
  and finite binary-lift upper bounds. s6:lp-hull proves both hull containments
  and physical feasibility of each LP vertex, so optimizer recovery is explicit.
- s6:alphabet-geometry transfers the interface to the relay path, correctly placing
  nonzero economic coefficients on equal-flow reset duplicates, and proves the
  arbitrary strictly-growing-supply extension. The explicit nonlinear contracts
  stay. The deleted pool-throughput lower-bound counterexample stays.
- s6:slab-hardness proves the abstract SUBSET SUM reduction, nonempty compact
  promise, rational endpoint NP certificate, and fixed-local-coefficient padding.
  The extra dense slab has TWO bounds. This remains abstract; it is not a
  degree-two physical pooling reduction.
- s6:rank-theorem proves fixed-interaction-rank decomposition, zonotope enumeration
  including degeneracy and corner witnesses, slice-vertex edge coverage, harmless
  nonedge candidates, global common-total search including zero, exact radical
  comparison and physical matrix recovery. s6:rank-one-cost proves the four
  continuous-knapsack envelope specialization. s6:oracle proves the direct
  fixed-attribute physical pool Lagrangian cost identity; the primal quality
  constraints must be dualized and no duality-gap statement is made.
- s6:parametric gives the full rank-one matrix-parameter two-LP reformulation,
  signal-zero semantics, rational reconstruction and scope limits. It compares
  the independent-column positive-product rank-two construction to the inspected
  preprint and to the already developed source. It also proves the convex
  singleton-leaf Square-Root Sum arithmetic reduction.
- s6:related describes all 13 adjacent canonical inventory results, with exact
  titles and explicitly unpublished research-note citations. It includes the
  correlation-face atom/selection argument, precise approximate metrics/constants,
  general matrix cost versus physical additive economics, and common-factor,
  anchor, network-simplex and power-flow scope. Unrelated standalone conic,
  common-factor and power-flow proofs are not reproduced.
- s6:open distinguishes unbounded attachment parameter cells from dense pool
  aggregates, gives the failed helper-pool substitution, identifies which later
  exact-contract algorithms remove each obstacle, and closes the older
  unrestricted one-pool/one-quality threshold question using section 3.

## Source inspection and attribution

Literature archive read-only. No downloaded paper is packaged with the manuscript.
Primary web passages were read through the browser; source images are only under
/tmp/pooling-paper-sources/stage06-author. Initial rendering with the scientific
Python environment failed because PyMuPDF is absent; pdftoppm succeeded.

- Gärtner, Helbling, Ota, Takahashi, arXiv:1308.2495v1 (2013), Section 4,
  local extracted pages 6–9. Original PDF page 8 was rendered and visually checked:
  Definition 11 has the cubic-exponent direction and the signed even-power
  exposing parameter. The author manuscript is explicitly cited as a preprint.
  The mathematical exposure phenomenon is established prior work. Our tangent
  certificate is a self-contained alternative used to prove physical extensions.
- Lubin, Vielma, Zadik, Mixed-Integer Convex Representability, published
  Mathematics of Operations Research 47(1), 720–749 (2022), DOI
  10.1287/moor.2021.1146. The inspected local source is arXiv:1706.05135v3:
  Section 4.2, Definition 4.2 and Lemma 4.1, extracted pages 11–12.
  The finite midpoint integer-dimension principle is explicitly credited.
  Browser publisher DOI fetch returned Internal Error; local source package
  and author-associated metadata corroborate the publication. No final-journal
  page locator is inferred from the preprint.
- Punnen, Sripratak, Karapetyan, Discrete Applied Mathematics 193, 1–10 (2015),
  DOI 10.1016/j.dam.2015.04.004. Inspected local open manuscript
  arXiv:1212.3736v3, Sections 3.2–3.3, extracted pages 9–16: bounded-variable
  LP bases, perturbation, fixed-rank and rank-one algorithms. Our scope
  comparison is shared variable total and division by that total; no novelty
  claimed for projected-box/low-rank optimization methods.
- Hladík, Černý, Rada, Optimization Letters 15(6), 2331–2341 (2021),
  DOI 10.1007/s11590-021-01711-6. Inspected the author's publication page
  and abstract, which explicitly state fixed-rank arbitrary quadratic box
  optimization through zonotope face enumeration. Only that broad method
  is attributed; no uninspected internal theorem details are used.
- Boveroux, Carvalho, Lodi, Louveaux, On the Complexity of Linear Programs
  with Parametric Constraint Matrices: inspected 17-page author PDF from
  ORBi /2268/345162. Section 3.1 PDF pages 5–7 contains the fixed-one and
  second-factor columns; Section 3.3 PDF pages 10–11 contains the
  one-nonzero-column discussion. The two-LP proof here is self-contained.
  The PDF has no visible date and the landing-page browser fetch failed,
  so the entry says undated author preprint consulted September 5, 2026.
  It is not attributed an inferred publication year or journal.
- Grothey, McKinnon, arXiv:2002.10899v1 (2020), Section 3, PDF pages 9–10:
  two nutrient coordinates, seven inputs, six products and three mixing bins,
  symmetric optima and further local solutions. The final section cites the
  scoped three-pool/two-quality prior geometric example without reproducing
  its reported numerical local-solution counts or claiming exhaustive priority.
- Pardalos–Vavasis (1991) is credited only for established broad rank-one
  concave quadratic hardness. The path/slab proof is supplied in full.
- Root inspected Fawzi–Parrilo arXiv:1311.2571v1, Theorem 1, including
  fixed-block constants and the linear-size SOC-to-order-two-block conversion.
  The bibliography retains preprint metadata.
- Root inspected Lee–Raghavendra–Steurer's author-hosted full manuscript,
  Theorem 3.8 equation (3.11), Theorem 5.3 and exact 2/13 exponent.
  It is cited as that full manuscript without invented journal metadata.
- Root inspected Braun–Fiorini–Pokutta–Steurer's author-hosted full manuscript,
  Theorem 6, and verified publisher metadata: Mathematics of Operations Research
  40(3), 756–772 (2015), DOI 10.1287/moor.2014.0694. The author-version locator
  is explicit. These primary references now accompany the conic-note summaries.
- Root inspected De Loera–Onn's original: Theorem 1.1, Section 3.3,
  printed page 816, sigma(i,j,k)=((i,j),(1,k),1), verifying the first-layer
  coordinate feature. Journal metadata and DOI 10.1137/040610623 verified.
  Root found the scoped network discussion accurate.
- Companion result entries use actual note titles, year 2026, an explicit
  unpublished-research-note designation, and no invented authors or public URLs.
  The coverage inventory maps every such reference to its actual local source.

## Checks and their limits

Static checks found no missing or duplicate labels, citation keys or unmatched
environment counts in the new files. No previously passed experiment was
independently duplicated by this author.
Root owns manuscript builds, final source verification and independent tests.

Root reported fresh passing exact checks:
8190 shadow witnesses and 8178 breakpoints; 252 upper-only original-network
dual certificates; 252 fixed-alphabet original-network dual certificates;
2246 identity/tangent checks and 661 subset-sum targets; 1016 padded identities
and 661 padded targets; 2044 distinct perturbed values and 18432 negative
edge derivatives; 160 rank-one-cost comparisons (111 feasible, 49 infeasible)
and zero/singleton/irrational regressions. Root also ran the original-network
physical vertex-forcing checker: 252 endpoint extensions and 18 interior terminal
values passed. The existing exact penalty scripts use the original c direction
and M=2N^N+1. They do not separately test the new tangent direction's
M=3N^N+1; its uniform coefficient bound and repair inequality are proved
in s6:price-response.

For a distinct new concern, root created verification/check_interaction_rank_two.py:
24 rank-two instances and 104 rational total slices; 342 exact exposing
certificates, eight exact convex-combination certificates, four singleton boxes,
and two zero slices. HiGHS proposes candidates only; rational arithmetic verifies
classifications and optimum equality against independently enumerated original
margin vertices. This tests projected candidate coverage, including redundant
projected corners; it does not test the full asymptotic bound or continuous
stationary search. The general theorem proof supplies those steps.

Author checked accepted section hashes unchanged and the original bibliography
prefix unchanged at SHA-256
42325c354526840aa25926e4520974f413d6b2254209153140b8fb480a0e2c3c.
All 23 stage-6 coverage rows have concrete destinations.
No physical hardness, full classification, rational-optimum claim, uniform
local-solver bound, unrestricted convex-leaf algorithm, or zero duality gap is
inferred from an adjacent result or geometric example.

## Root feedback before freeze

Root read the full new stage and introduction and reported no mathematical
defect in that reading. The initial forced build succeeds at 90 pages.
The table had underfull justified paragraphs; the author changed its p columns
to ragged-right with arraybackslash. Root owns the final rebuilt PDF and any
remaining typesetting checks. No formal correctness or external-review claim
is inferred from these checks.

## Freeze

Author content is frozen after the above source and table corrections.
Final source hashes follow. The review snapshots and stage advancement are
owned by root.

- sections/00-introduction.tex:
  5449b1254d6eb682f3238465e01f93b5b493ebdcb068c66edb1d7d8583c928f1
- sections/06-synthesis.tex:
  3c2752d7d04769b796fed4e48cb05259fa313dcd5da006830a3e945db859867c
- bibliography.bib:
  c4a17f19fe9b4bbb80c653a722bc612209d6f1881dc35bceb94da66bb0a3a2ca
- process/coverage.md:
  695b3fe8a5cbc318fd769caaee615057d2628a74ab1f06423ba0109227adaccd
