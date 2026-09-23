# Stage 5 author record

The sole author completed the assigned Stage 5 draft and independently
checked its mathematical arguments. This is an author record for the next
15 full-stage reviews, not a review verdict or stage acceptance. No author
subagents or reviewers were delegated. The draft includes the order-one
refinement after fresh verification; it was not assumed from its proposal.

## Files and dependencies

New manuscript files:

- `sections/13-xor-quadratic-hulls.tex` (printed Section 16, `sec:xor-quadratic`).
- `sections/14-monomial-reformulations.tex` (printed Section 17, `sec:monomial-reformulation`).
- `sections/15-finite-certificates-affine.tex` (printed Section 18, `sec:xor-upper-affine`).

`main.tex` includes these files before the appendices. Four primary-source
entries were appended to the paper-local `references.bib`. Existing
mathematical sections, appendices, and `macros.tex` were not changed. A byte
comparison with `process/snapshots/stage04-accepted` verified all 18 earlier
mathematics/macro files unchanged. No snapshot, literature package, canonical
repository source, or other paper folder was edited.

The author read `review-protocol.md`, `scope-proposal.md`, the complete
Stage 5 assignment and candidate, the complete three canonical sources,
and their linked correction audits. Earlier internal PASS labels were not
used as evidence. Shared mathematical dependencies checked directly were
`01-foundations.tex` (vertex-law and certified-cover conventions),
`11-coordinate-domains-lifts.tex` (the exact local oracle and scope of the
coordinatewise interpolation proof), and `12-relative-blocks-cuts.tex`
(the clique escape and decomposition limitations). The new proofs use
signed Boolean variables and explicitly define their own moment oracle.
The root's primary-source record was read as a locator guide; the new
source audit was performed directly.

Canonical and correction files read, relative to the repository root:

- `results/spatial-bb-quadratic-cut-exponential-lower-bound.md`.
- `results/spatial-bb-monomial-lift-exponential-lower-bound.md`.
- `notes/spatial-bb-affine-branching-barrier.md`.
- `notes/review-spatial-bb-beyond-clique.md`.
- `notes/review-spatial-bb-beyond-clique-second.md`.
- `notes/review-spatial-bb-bounded-monomial-lift.md`.
- `notes/review-spatial-bb-affine-branching-barrier.md`.

## Source-to-label coverage

| Source and required content | Manuscript labels |
| --- | --- |
| Quadratic-cut source: signed 3XOR multiset, three distinct coordinates, normalized objective and Boolean/continuous optimum | `eq:xor-objective`, `eq:xor-vertex-min` |
| General degree-4r transfer, original r>=2, deterministic substitution and marginalization, repeated slack products, affected costs, arbitrary cover and witness count | `thm:xor-transfer`, `eq:xor-source-assumptions`, `eq:xor-indicator-square`, `eq:xor-node-cost`, `eq:xor-transfer-count` |
| Exact quadratic hull of full coordinate domain, linear-only use of coupled quadratic inequalities; arbitrary nonclosed coordinate sets and all local valid polynomials/equalities | `eq:xor-moment-hull`, `eq:xor-node-preorder`, `eq:xor-node-local-equality`, `eq:xor-node-quadratic`, `eq:xor-local-endpoints`, `thm:xor-transfer` |
| Signed moment realization, including the constant vector's signed class | `lem:signed-moment-law` |
| Schoenebeck's classical input, direct signed closure and Gram construction, width versus degree, delta=gamma=1/4 at density8 | `lem:xor-width-moments`, `eq:xor-character-gram`; following source-parameter paragraph |
| Elementary random-sign tail and assignment union bound, occurrence deletion, event intersection, every sufficiently large n, retained7n<=m<=8n, OPT>=1/8 | `thm:xor-family`, `eq:xor-family-parameters`, `eq:xor-deletion` |
| Original linear-order regime and absolute1/16/relative1/2 exponent7n/1024 | `thm:xor-family`, `eq:xor-family-count` |
| Gradient and Hessian normalization | `prop:xor-sensitivity`, `eq:xor-sensitivity` |
| Monomial-lift source: retained originals, signed nonempty squarefree supports<=D, arbitrary repeated/overlapping supports and arbitrary finite N; exact available-degree objective pullback | `eq:signed-monomial-map`, `eq:lift-objective-pullback` |
| All available graph identities and multiplier constraints, full lifted coordinate hull rather than feasible-graph hull | `eq:lift-all-identities`, `eq:lift-box-hull` |
| Degree-4rD source, all signed character moments, full lifted preordering, exact Boolean quadratic realization that may leave graph, local equalities and nonclosed coordinate sets | `thm:monomial-transfer`, `eq:lift-node-functional`, `eq:lift-degree-accounting` |
| Substitution cost and parity-rank witness count, basis-row support union rather than number of restricted lifted coordinates | `eq:lift-restricted-supports`, `eq:lift-cost-restriction`, `eq:parity-rank-support`, `eq:monomial-transfer-count` |
| Pair-plus-clause formulation, linear objective,2m quadratic equalities, N=n+2m<=17n, exponent7n/3072, linear order | `cor:xor-quadratic-formulation`, `eq:xor-factorable-formulation`, `eq:quadratic-formulation-count` |
| D versus region count only within4rD<=an, D=Omega(n/log n) for polynomial count in original n, dimension distinction, no unsupported extension of Stage4 interpolation | `cor:degree-regions`, `eq:degree-region-tradeoff`; final paragraph of Section 17 |
| Canonical distinct order-two Bernstein upper proof, full eight-corner identity, M=ceil(3/epsilon),48^n, cubic identity transferring to lifted linear objective | `prop:xor-bernstein-upper`, `eq:xor-grid-corner-bound`, `eq:xor-bernstein-identity`, `eq:bernstein-graph-transfer` |
| Order-one candidate: lower transfer at r>=1,rD>=2, source width 4rD, D=3 formulation requiring12r<=an, order1 allowed | `thm:monomial-transfer`, `cor:xor-quadratic-formulation` |
| Order-one candidate:48^n upper bound using only full-box degree-two distribution and graph equations on moments; explicit quadratic certificate | `prop:xor-order-one-upper`, `eq:order-one-graph-moments`, `eq:order-one-corner-estimate`, `eq:order-one-quadratic-cut`, `eq:order-one-cut-identity` |
| Affine note: preserved uniform moments rejected by a balanced halfspace with at least half the witness mass; normalized affine coordinate cut | `prop:affine-quadratic-obstruction` |
| Affine note: every substitution satisfying the order-r halfspace localizers fixes at least min(r-1,ceil(n/2)) originals; exact negative localizer and order1 boundary | `prop:affine-substitution-obstruction`, `eq:affine-substitution-count` |
| Method obstruction only, perfect-satisfiability refutation gives normalized1/m, continuous subdivisions differ from integer-negation disjunctions; disjunctive SOS and Stabbing Planes comparison | `subsec:xor-literature-boundary`; paragraphs after both affine propositions |

## Proof and degree audit

The unlifted proof fixes restricted originals to the selected witness and
uses the untouched marginal. Positivity does not assume that this event
has positive pseudo-probability. An indicator I made from a product of
slacks has degree at most the sum a of generator degrees. For a multiplier
of degree d, a+2d<=2r implies deg(IP)<=a+d<=2r. Thus the square uses at
most degree 4r. Arbitrary local polynomials reduce to their nonnegative
endpoint interpolation; each nonconstant factor costs at least one original
generator degree. Local equalities reduce to zero. A genuine Boolean
quadratic law is marginalized and fixed to realize every cross moment.

The lifted proof repeats this calculation with literal pullback: each
factor costs at most D and deg(IP)<=D(a+d)<=2rD. Parity indicators remain
idempotent with dependent, repeated, or inconsistent supports. Every
multiplied graph identity vanishes as a real polynomial under pullback
within degree 2rD. For the quadratic law, lifted linear squares pull back
to degree D, and all degree-two entries are signed original characters of
degree at most2D. The signed-class construction fixes the constant class
to one; a restricted coordinate has endpoint mean and therefore is fixed
almost surely. This distribution may leave the nonlinear graph.

All changed clause costs are in [0,1]: the source has enough degree to
apply positivity to squares of characters of degree at most3. In the
lifted theorem, the sufficient integer condition is rD>=2, so2rD>=4>=3.
No positivity, identity, rank, or realization step requires r>=2. The
written lifted objective still must have degree <=2r with exact polynomial
pullback. Thus r=1 is allowed for D=3 and linear Phi, with source
requirement 12<=an. The original cubic objective still requires r>=2.
The candidate was verified independently and fully developed, while the
order-two Bernstein proof remains separate.

The count uses the support union C of restricted lifted coordinates. A
basis of the restricted binary row matrix has the same support union,
so |C|<=D rank. Its consistent affine fiber has size2^(n-rank). This
justifies arbitrarily many auxiliaries and repeated supports; counting
restricted lifted coordinates without rank would fail.

For the order-one upper certificate, the full-box distribution supplies
only moments through degree two. The two graph equations hold on those
moments. The per-clause estimate is h+2h=3h for its product coordinate,
or3h/2 for its cost. The additional explicit quadratic identity makes the
same proof a linear use of a valid quadratic box cut. It assumes neither
pointwise graph equations for the realizing law nor any hidden cubic
moment at order one. The canonical Bernstein proof instead uses cubic
bound products and the cubic identity with multiplier x_k at order two.

The event intersection is existential for every sufficiently large n,
not just a subsequence. The two source/random-sign events fail with o(1)
probability, while the elementary deletion event fails with probability
less than 1/8. No independence of these events or occurrence counts is
assumed. The retained functional works at all allowed smaller orders.

## Direct primary-source checks and attribution

`verification/stage05-primary-sources.json` records original paths, URLs,
SHA-256 digests, and locators. The original PDFs and their renders remain
outside the paper directory or in the existing literature package. The
literature collection was read according to its AGENTS.md and not edited.
Open arXiv abstract pages were checked for version metadata; originals
were used to verify the comparisons. No download required bypassing an
access control. These targeted source checks do not establish priority.

- **Schoenebeck, author full version.** Read the source's random-CSP
  definition, Theorems 11–12, all of Lemma 13's signed-character construction
  and product-consistency argument, and the appendix width argument
  (printed 17–19). The surrounding main text was read for conventions and
  context. Visually checked printed 7,8,10,11. Theorem 11 supplies a positive
  constant width at fixed density; Theorem 12's simultaneous gap statement
  and Lemma 13's half-width conversion agree with our parameters. Our
  `lem:xor-width-moments` directly proves the closure equivalence, sign
  consistency, and Gram positivity for arbitrary square polynomials.
  Moments through width w are defined directly by the derived-sign/zero
  rule, so odd top-degree moments do not rely on splitting into two
  floor(w/2)-degree factors. Required 4r and 4rD are even in any case.
  The source prints a norm-zero sentence immediately after displaying its
  constant vector as (1,0,...,0); this is a typographical error, not the
  normalized construction used here. Its illustrative gamma=1/2 at k=3
  is avoided: gamma=1/4 gives denominator1/4. The source's character
  construction is attributed as classical, rather than presented as a
  new SOS lower bound. No unrelated corollary of the source is imported.
- **Ahmadi–Dash–Hua–Stellato, arXiv 2605.28674v1.** Read abstract,
  contribution statements, Definitions 1–2, main fixed-degree theorem
  statement, relevant simplicial construction discussion, Section 6's
  region/oracle definitions and termination statements, and closing scope
  discussion. Visually checked original printed 32, including Algorithm 2,
  its preceding positive-tolerance termination statement, and the opening
  simplex formulation. The manuscript compares these inspected statements;
  it does not claim a lower bound on their simplicial algorithms or audit
  every theorem of that paper.
- **Beame et al., arXiv 1710.03219v3.** Read abstract and introduction
  through its result statements. Visually checked PDF 3–4, printed 2–3:
  the integer-negation rule and Theorem 1's quasipolynomial Tseitin bound.
  The citation uses the inspected 2023 version and records its 2018
  preliminary conference version. The manuscript makes no polynomial-size
  claim or direct continuous-cover inference.
- **Fleming et al., arXiv 2102.05019v2.** Read abstract and introduction
  through Theorems1.1–1.4. Visually checked PDF 5, printed 4, for the exact
  CNF-encoding scope of Theorem 1.3 and coefficient-restricted SP* scope
  of Theorem 1.4. The manuscript does not transfer either result to its
  constant-gap continuous objective.

The earlier Coniglio/Jarre comparison belongs to the accepted preceding
sections. No stronger comparison or claim of exhaustive literature access
is introduced in Stage 5.

## Exact verification and build

Author checker:

```
/home/sgusev/miniconda3/envs/minlp-notes/bin/python verification/check_stage05_author.py
```

The run completed successfully. `verification/check_stage05_author.json`
records its script digest and these exact checks:

- All 16,384 families of supports of size at most3 on 4 originals, checking
  basis support union, rank bound, every consistent signed fiber by full
  Boolean enumeration, and duplicated rows.
- All 1,296 signed class allocations/orientations for 4 coordinates, with
  a deterministic constant class and two independent free classes,
  checking every augmented first/second moment exactly.
- A six-variable inconsistent parity instance whose width 3 closure has
  directly defined signed cubic moments and identity degree-one Gram
  matrix, while width 4 derives contradiction. This tests the odd-width
  convention; it is not evidence for asymptotic width.
- Formal symbolic Bernstein interpolation (after multiplying by h^3),
  cubic graph transfer, order-one quadratic cut identity, and an overlapping
  repeated parity-indicator square identity.
- 324 exact negative halfspace localizer evaluations over dimensions 1–9,
  plus first/second moments and halfspace witness mass including parity
  boundaries and the vacuous order-one lower condition.
- Exact arithmetic for the deletion bound, both lower exponents, the
  lifted-dimension exponent, and upper grid base 48.

Separately, the coordinator's `verification/check_order_one_upper.py/json`
checks 3,375 chosen boxes and 216,000 quadratic vertex cases, with 250
LP-selected distributions reconstructed exactly. Of those, 242 have support
outside the graph and 226 give values below the true node graph optimum.
These are distinctly the coordinator's checks, inspected as supplemental
evidence and not rerun as an author claim. The universal proof and author's
formal identity verification are independent of these numerical selections.
Finite checks do not prove the asymptotic source theorem or replace any
universal manuscript proof.

Build command:

```
python verification/build_and_check.py
```

The final run returned compile exit 0, no warnings, no duplicate labels,
no unresolved references/citations, and an unchanged printed Stage 2 checker.
The PDF has 91 pages. Author visually inspected manuscript pages 65,66,68,
70,71,73,74,75, covering the new oracle, source-degree conversion, both
lifted moment and rank arguments, the two upper proofs, and affine scope.
No clipping or layout defect was found. `verification/build-report.json`
contains exact input and PDF digests and the complete build metadata.
The source record and coverage ledger are process artifacts; they introduce
no extra manuscript claims.
