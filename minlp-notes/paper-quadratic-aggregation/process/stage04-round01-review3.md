# Stage 4, round 1: independent review 3

Date: 2026-09-22. Scope: both new sections, the infinite-aggregation
checker and README, bibliography, coverage, author/literature records,
source snapshot, and the stated primary-source/novelty comparisons.
I did not read other current reviewer reports, edit source, or review
the deliberately deferred accuracy, PDLC, or formal-integration stages.

## Verdict

**Accept stage 4. No major or minor mathematical, scientific, or
presentational correction is required on this review.** The sharp Gram
threshold, indispensable strict-ray construction, both hull formulas,
and arbitrary-quadratic finite-description obstruction are proved.
The priority language is narrow and qualified; classical matrix
ingredients and prior convexification results are credited.

One external source changed concurrently after the author's snapshot;
the manuscript files did not. This is recorded under checks below and
does not alter this review verdict or certify the new formal material.

## Mathematical audit

### Full Gram map and exact hyperplane image

The factorization of every Gram fiber as `G^(1/2) Q`, with orthonormal
rows of Q, handles singular G correctly: zero rows in an eigenbasis
are completed only in Q, so the original X is preserved. The rectangular
SVD reduces the linear functional to a weighted sum of diagonal entries
bounded by one. The displayed maximizing factor attains the nuclear-norm
value, and negation attains its negative.

The interval-attainment argument is valid over the reals. For even k,
pair rotations connect the maximizing trace to its negative. For odd
`k>=3`, the fixed least-singular-value axis gives endpoint `2 s_k-M<=0`;
continuity obtains every nonnegative intermediate trace, and negation
obtains every nonpositive one. This does not incorrectly assume that
the two components of the orthogonal group are connected to one another.
The scalar sphere case `k=1,r>=2`, zero fibers, and vanishing singular
values are covered. The excluded interval case `k=r=1` is correctly
handled separately in the HHC theorem.

The squared-fidelity proof is also correct. Frobenius Cauchy–Schwarz
gives the product-of-traces lower bound for each positive definite Z.
The proposed Z satisfies `ZGZ=H` for positive definite inputs and
attains equality. Regularizing **both** inputs and then using positivity
and continuity supplies equality for singular inputs without assuming
an optimizer exists there. Separate concavity follows from an infimum
of linear functions; the proof never squares a concavity inequality.

Combining the exact fiber interval with `t=sqrt(T)` proves both
directions of the hyperplane-image formula, including `B=0`, `beta=0`,
singular matrices, and zero traces. Concavity makes the displayed
hypograph convex. For `r<k`, the rank-`r` obstruction on `t=0` proves
necessity. At `k=r=1`, hyperplanes are lines and images are rays, so
HHC holds despite failure of the general image formula. The corollary
uses only a linear output transformation and correctly disallows
unrestricted mixed `tX` terms. Its threshold is explicitly sharp for
the full map, not for every smaller collection of outputs.

### Good cone, indispensable rays, and closed finite-family obstruction

For the three-row ball system, the leading two-by-two block's negative
eigenvalue repeats at least twice when `r>=2`, excluding it from the
good class by the homogeneous inertia condition. If that block is PSD,
the scalar block is strictly negative for every nonzero nonnegative
multiplier; convexity also gives strict validity on the ordinary hull.
This proves the complete good-cone characterization, not only an
inclusion.

The Gram witnesses are positive definite uniformly on the specified
parameter interval and hence are realizable in two coordinates. The
AM–GM equality conditions identify exactly one active good ray at each
witness. An omitted ray's witness strictly satisfies **every** other
good ray, so the uncountability conclusion holds for arbitrary proposed
families, not merely finite ones. Distinct parameters give distinct rays.

For the closed hull, the proof correctly perturbs off the boundary
witness. A sufficiently small decrease in its cross entry preserves
Gram positivity and the finite family's strict slacks but makes the
omitted valid aggregate positive. This supplies a point outside the
closed hull, avoiding the invalid use of the original boundary point
as a closed-hull counterexample.

### Open and closed hulls and lifted descriptions

The application of BDS's open aggregation theorem has the required
dimension `n=2r>=4`, nonemptiness, properness, and proved HHC. The
explicit decomposition generates the whole multiplier cone from its
coordinate and curved extreme rays. Strict positivity of p and q
makes the minimizing parameter finite and attained, so the strict
scalar hull formula follows without exchanging an unattained infimum
with a strict inequality.

The Schur complement gives exactly the displayed strict and nonstrict
lift projections, with correct scalar endpoint conditions. The closed
projection is proved closed through its continuous explicit formula,
not through an unsupported general fact about SDP projections. Mixing
with the positive definite lifted origin and, if necessary, increasing
the scalar slightly proves density of the ordinary hull. Compactness
of the original closed set then yields its ordinary convex-hull equality.

The countable-dense argument is confined to nonstrict inequalities and
treats zero p or q by endpoint limits. The supplementary direct
two-point construction requires `r>=3`, which is clearly distinguished
from the HHC-based `r=2` proof. Its covariance converse has the right
strict variance inequalities and Cauchy–Schwarz direction.

### No finite arbitrary quadratic conjunction

The planar restriction reduces the relevant boundary to the specified
quartic arc strictly inside both ball bounds. The rational radicand
has simple zeros and poles, so it cannot be a square in `R(x)`.
The division-in-y argument and primitive-polynomial Gauss lemma
correctly prohibit a nonzero degree-at-most-two polynomial from
vanishing on an arc. Real analyticity on a neighborhood of a compact
interval then gives only finitely many intersection points.

For a strict description, an identically zero restriction is impossible
because the planar origin is feasible; continuity from the feasible
side makes every boundary value nonpositive, and some value must be
zero. For a nonstrict description, identically zero restrictions may
be discarded; otherwise strict negativity of every remaining value
would admit an infeasible planar neighborhood. Both cases therefore
require an impossible finite cover of the arc by finite zero sets.
The statement concerns conjunctions in original variables and explicitly
does not exclude the finite lifted SDP descriptions proved earlier.

## Primary-source and novelty audit

- **Uhlmann (2000).** Independently opened the
  [published author PDF](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf).
  Printed pp.408–410 state separate concavity of transition probability,
  allow positive operators without trace normalization, and give the
  product-of-traces infimum in equation (14). At partial-fidelity index
  zero, the operator pair has full rank and the two factors are inverses.
  The manuscript's attribution is precise. Its real proof independently
  establishes the real specialization and singular boundary case.
- **Rotation extrema.** Independently inspected the institutional
  [Ramachandran–Shu–Wang PDF](https://ir.cwi.nl/pub/35175/35175.pdf),
  Lemma 1, printed p.1460. It gives the determinant-corrected SO(n)
  singular-value formula and credits Farrell and coauthors. The paper
  cites it only as classical context and supplies its own full interval
  argument, so no SO/O or connectedness distinction is lost.
- **Beck.** Read the existing primary Beck2009 extraction at Theorems
  3.1 and 3.4. Over the real field the stated counts, row-dimension
  qualification, and signed PD combination match the manuscript.
  These are global quadratic-matrix image statements and do not
  directly give the present every-hyperplane full-Gram formula.
  A fresh open of the Beck2007 author PDF failed in the web tool;
  I do not claim a fresh reading of that article. Its use here is
  the modest historical attribution of quadratic matrix programming,
  consistent with Beck2009 and WKK's primary references.
- **BDS Conjecture 3.1.** Read the exact conjecture and Theorem 2.9
  in the available arXiv-v2 primary text. The construction meets
  the conjecture's HHC/good-aggregation conjunction. All numbered
  locators refer to the explicitly identified preprint version.
- **DMS.** Read the local published primary extraction, Proposition
  2.8 and §7.4, including its closed two-variable system and displayed
  multiplier family. The manuscript's HHC-failure midpoint is correct.
  The leading diagonal `(a-1,-a)` gives two negative homogeneous
  eigenvalues by restriction, so those multipliers are outside the
  good class in this manuscript. This is a meaningful distinction
  from prior infinite necessity, rather than a broad priority claim.
- **Wang–Kılınç-Karzan.** Independently opened
  [arXiv v2 §4.1](https://arxiv.org/html/2403.04752v2#S4.SS1)
  and Assumption 1. The replication count is at least the number
  of constraints, and a nonnegative PD quadratic combination is
  required. Zero objective, three constraints, and `A1+A2=I` meet
  the hypotheses for this closed system when `r>=3`. The manuscript
  correctly obtains a feasible-set hull from the zero-objective
  epigraph and separates preprint theorem content from journal
  metadata. It makes no new-general-SDP-exactness claim.
- **Brun–Sun–Watson.** Independently inspected
  [§3.2.1 and Corollary 1](https://arxiv.org/html/2603.18473v1#S3.SS2.SSS1).
  They concern the inner-product hypograph over two balls in dimension
  at least two. The manuscript accurately says that taking a level
  after convexification alone does not prove the fixed-level hull.
  No claim of novelty follows merely from that distinction.
- **Dey–Han–Wang.** Independently read the
  [published definition and Theorem 2](https://link.springer.com/article/10.1007/s10898-026-01607-8).
  Its signed boxed equality aggregation is followed by convexification
  of each aggregate before intersection. The manuscript's distinction
  from directly intersecting good quadratic sublevel sets is correct.
- **Blekherman–Dunbar.** Read the available primary preprint at Theorems
  1.3–1.4. The latter retains homogeneous PDLC and its stated
  regularity/infinity conditions; the former uses empty common
  projective variety and a smooth spectral curve. The manuscript
  proves lack of PDLC, a repeated determinant factor, and an actual
  common projective zero. Thus these finiteness results do not
  contradict the construction. I did not independently obtain the
  journal eprint; the manuscript honestly uses inspected preprint
  numbering and separate publication metadata.

I also ran bounded searches for the exact HHC/Conjecture 3.1 phrase,
Gram/hyperplane/fidelity convexity, and Blekherman/infinite aggregations
with recent years. They revealed no verified earlier resolution; much
of the Gram/fidelity search was irrelevant quantum-kernel literature.
That search outcome is not a priority proof. The paper's qualified
explicit-conjecture-resolution claim and its refusal to claim the
classical fidelity or generic SDP principles as new are appropriate.

## Targeted checks and concurrent source movement

- `python3 paper-quadratic-aggregation/supplement/check_infinite_aggregation.py`
  from the repository root: PASS, with 2,601 exact ray identities,
  six finite-family outside witnesses, and the additional algebra.
  I inspected the checker and its README; they use rational arithmetic
  and do not represent sampling as proof of infinite or geometric claims.
- Compared all 22 SHA-256 entries in `stage04-author-snapshot.json`.
  **21 match.** The only mismatch is the external canonical result
  `results/infinite-quadratic-aggregation-hhc.md`, which now records
  concurrent formal packages 29/30 and their bounded scopes. The
  stage-4 manuscript, checker, bibliography, and author records remain
  unchanged at their reviewed hashes. This movement was reported to
  the coordinator; it does not confer formal verification on this review.
- Searched the current main LaTeX and BibTeX logs for warnings,
  undefined references, and overfull/underfull boxes: no matches.
  I did not rerun LaTeX or visually inspect the PDF.
- Reviewed coverage's authored stage-4 destinations. They expressly
  supersede the historical `r>=3k/r>=6` thresholds and include the
  stronger nonstrict arbitrary-quadratic obstruction. Later accuracy,
  four-bound, formal packaging, and synthesis obligations are separate.
- The first source-read attempt used the wrong guessed filename
  `05-gram-completion.tex`; I then read the actual
  `05-gram-hyperplanes.tex`. The failed read made no modification.
- No project-wide checks, CI inspection, solver benchmark, formal
  verification rerun, or subagent was used. Only this report was written.
