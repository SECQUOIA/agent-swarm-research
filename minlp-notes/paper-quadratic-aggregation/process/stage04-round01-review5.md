# Stage 4, round 1: independent review 5

Verdict: pass. No major or minor correction required in the stage 4
mathematics or its stated scope. One external-source fingerprint changed
after the author snapshot; this is recorded below as provenance information,
not a claim that the paper sources changed or that the proofs failed.

## Mathematical review

Read both complete new sections and checked their interdependence. The
Gram theorem supplies HHC independently of the BDS hull theorem; the good
cone is derived directly before the latter theorem is used. There is no
circular use of the hull formula to establish HHC or indispensable rays.

### Gram fibers and sharp HHC

The Gram-factor parameterization handles singular G by orthonormal extension
of only the positive-eigenvalue rows. The rectangular SVD yields the correct
trace maximum and explicit maximizing factor. The interval argument is valid
over the real field despite disconnected orthogonal groups: for odd k >= 3
the pair-rotation path reaches 2s_k-M <= 0, while negation fills the other
half. Even k and k = 1, r >= 2 have the stated direct rotation paths.
The scalar exception k = r = 1 is correctly excluded from the exact image
formula but included in HHC.

The product-of-traces fidelity infimum has a valid Cauchy–Schwarz lower
bound, positive-definite equality case, and regularization argument for
singular G,H. The proof uses separate concavity obtained from an infimum
of linear functions, not the invalid rule of squaring a concave function.
The resulting hypograph formula is convex, including B = 0, beta = 0,
and singular Gram matrices. For r < k the explicit rank-increasing midpoint
on t = 0 proves necessity. The repeated-block corollary is a linear-image
consequence and does not extend to unproved mixed terms.

### Good rays and ordinary/closed hulls

Replication excludes any negative leading-block eigenvalue from goodness
when r >= 2. A nonzero PSD leading block has a strictly negative scalar block
and a globally convex aggregate strictly valid on the ordinary hull. This
proves both directions of the exact cone description.

The ray witnesses have uniformly positive definite realizable Gram matrices.
The two AM–GM equalities force precisely the designated positive ray;
coordinate rays and all other good rays have strict slack. Consequently the
uncountability quantifier holds even for arbitrary infinite descriptions.
For the closed hull, decreasing the off-diagonal Gram entry preserves a
finite family's strict slack while violating the omitted aggregate, giving
the required point outside the closed hull rather than merely on its boundary.

The cone-generation calculation has positive denominators whenever lambda3
is positive. For strict p,q the ray infimum is attained, so the strict hull
formula follows with the correct strict inequality. The BDS invocation
checks n = 2r >= 4, HHC, nonemptiness, and properness. Schur complements
give both lift formulas. The closure proof uses an explicit closed scalar
description, not assumed closedness of an SDP projection. Mixing with the
lifted origin and adjusting sigma when needed gives density. Compactness of
T_r then justifies conv(T_r) = closure(C_r). The dense-countable description
is correctly restricted to nonstrict inequalities and handles p = 0 or q = 0
through endpoint infima. The alternate midpoint proof is explicitly limited
to r >= 3, while covariance gives the necessary condition generally.

### Arbitrary quadratics and spectral comparisons

The perpendicular plane exists for r >= 2 and its section has the stated
quartic boundary arc. The rational radicand has simple real zeros and poles,
so it cannot be a square in R(x). Its degree-two minimal polynomial in y,
primitive numerator, and Gauss's lemma exclude a nonzero quadratic vanishing
identically on an arc. Analyticity on a neighborhood of the compact interval
then makes each quadratic's arc intersection finite. Continuity and the
existence of both feasible and infeasible nearby planar points force a finite
description to cover the arc by those zero sets. Identically zero restrictions
are correctly impossible in the strict case and discarded in the nonstrict
case. Thus the extension to arbitrary quadratic conjunctions is proved;
no Boolean-description or lifted-formulation impossibility is implied.

The DMS hyperplane midpoint and two negative leading eigenvalues are correct.
The new example's signed homogeneous PDLC conditions are incompatible;
its repeated spectral determinant and projective witness are exact. The
comparison distinguishes these hypotheses from positive definiteness of
A1+A2 and does not claim to refute an applicable finiteness theorem.

## Literature, coverage, and reproducibility

Read the author report, dedicated literature record, consolidated coverage,
bibliographic additions, script, README, and snapshot. Independently opened
the [primary Uhlmann PDF](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf):
pp.408–410 explicitly give separate concavity, permit matrices without trace
normalization, and give the product infimum at partial-fidelity index zero.
The manuscript's attribution is accurate. Read the primary local Beck 2009
extraction at Theorems 3.1 and 3.4; its dimensions and definiteness assumptions
agree with the summary. Rechecked BDS v2 Conjecture 3.1, which is exactly the
HHC/finite-good-aggregation question resolved here. Other source comparisons
have explicit version/access records and appropriately bounded claims. This
review does not establish exhaustive priority by a new search.

The final stage-4 coverage replaces the earlier weaker replication thresholds
and contains all stage-4 developments in the current canonical source headings.
Quantitative accuracy, objective-specific exactness, later PDLC results, and
formal integration remain explicitly assigned to later stages. They are not
current missing work. The exact scripts' finite checks are not represented
as proofs of HHC, irreducibility, infinite quantifiers, or novelty.

## Checks actually run

- Ran `python3 paper-quadratic-aggregation/supplement/check_infinite_aggregation.py`:
  PASS, 2,601 exact ray identities and six finite-family outside witnesses,
  plus the documented ancillary checks.
- Ran an independent SymPy heredoc deriving the arbitrary two-parameter
  ray-slack identity and checking the quartic numerator identity and
  coprimality of its coefficients. All passed. This supplemented direct
  proof reading; it was not used as a substitute for real irreducibility.
- Checked all 22 snapshot entries by SHA-256. All paper files and primary
  PDFs match. The sole mismatch is the concurrently edited external file
  `results/infinite-quadratic-aggregation-hhc.md`. Inspected its current
  section inventory and verification record: stage-4 content remains mapped,
  and subsequent formal-package scope is separately reported. Preserve the
  historical snapshot; refresh source provenance during final integration.
- Inspected saved main LaTeX and BibTeX logs: the main PDF reports 25 pages;
  no Warning, Overfull, Underfull, or undefined matches. Did not rerun LaTeX.
- One initial read used an incorrect guessed section filename and failed
  before any file edit; the subsequent reads covered the actual sections.

No project-wide checks, CI inspection, Lean reruns, manuscript edits, or
subagents were used. Did not read other current reviewer reports.
