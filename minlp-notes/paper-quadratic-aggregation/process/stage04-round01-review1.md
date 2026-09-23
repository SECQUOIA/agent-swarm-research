# Stage 4, round 1: independent review 1

Verdict: accept stage 4. No major or minor issue identified in the reviewed
mathematics, supporting exact checks, or stage-specific source positioning.
This verdict does not cover the deferred quantitative, PDLC, or formal-
integration stages.

## Major findings

None.

## Minor findings

None.

## Gram-map proof audit

**Singular Gram factors.** The representation X=G^(1/2)Q with QQ^T=I is
valid also for singular G: zero-eigenvalue rows of a factor must be zero,
and the normalized positive-eigenvalue rows can be completed orthonormally
because r>=k. No invertibility of G is silently used. The rectangular SVD
and the diagonal-entry upper bound give exactly the stated maximum.

**Real trace interval.** The disconnectedness of O(k) causes no omitted
case. For even k, paired rotations join I and -I and give the full trace
interval. For odd k>=3, leaving the smallest singular-value axis fixed
gives endpoint 2s_k-M<=0, so continuity supplies [0,M]; negating factors
supplies [-M,0]. This argument includes repeated or zero singular values.
For k=1,r>=2 the sphere argument works, including B=0; G=0 gives a
singleton. The exceptional k=r=1 case is correctly excluded from the
interval/image formula, but retained in the HHC theorem because each
domain hyperplane is a line with a ray image.

**Squared fidelity.** Frobenius Cauchy–Schwarz has the correct order of
the factors and yields the claimed lower bound on the infimum. For
positive-definite G,H, the proposed Z satisfies ZGZ=H and both traces equal
tr(K). For singular arguments, regularizing *both* matrices gives a valid
positive-definite Z_epsilon; the two original traces are nonnegative and
individually bounded above by their regularized counterparts. Continuity
then proves the reverse inequality. Separate concavity follows directly
from an infimum of linear functions; it does not rely on squaring a
concave function.

**Exact image and threshold.** The trace interval permits the precise
target -beta*sqrt(T), so both necessity and actual attainment in the
hyperplane are proved. The beta=0 and B=0 cases are included correctly.
The resulting hypograph is convex. For r<k the two exhibited rank-limited
Gram matrices are attainable, while their midpoint has rank r+1, proving
necessity. The repeated-block corollary is a linear-image consequence and
does not overstate the threshold for smaller output collections or permit
unproved mixed tX terms. The k=2 simplification follows from the two
eigenvalues of G^(1/2)HG^(1/2).

## Infinite aggregation and hull audit

- The k=2 Gram construction gives HHC for every r>=2. A negative leading
  2x2 eigenvalue repeats at least twice and violates the good-inertia
  condition. Conversely the PSD leading block has a strictly negative
  scalar block for every nonzero feasible multiplier, and convexity gives
  strict validity on the ordinary hull. Thus the entire good cone, not
  only a subfamily, has been identified.
- Each G_tau is genuinely positive definite, with the displayed uniform
  lower bound. The aggregate slack identity and both equality conditions
  force exactly the claimed positive ray. This proves indispensability even
  if every other ray is retained. For the nonstrict finite-family claim,
  perturbing the Gram off-diagonal decreases the inner product and raises
  the omitted aggregate by 2 eta; finitely many strict margins and positive
  definiteness survive. The resulting witness is outside the *closed*
  hull, so the argument does not misuse a boundary point of the open hull.
- The BDS full-description theorem is applied with n=2r>=4, strict
  nonemptiness, properness, and the already proved HHC. The generating-ray
  decomposition of K is valid, including the lambda3=0 case. Minimizing
  tau*p+q/tau for positive p,q yields the strict hull formula with the
  correct strict inequality.
- Schur complementation gives both finite lifts exactly. The scalar
  interval has the stated intersection condition. Closedness of the
  nonstrict projection is established by its explicit formula, not by a
  general projection claim. Mixing with M(0,0,1/2) gives positive
  definiteness; when its scalar is exactly 1/2 it can be increased slightly
  without losing it. This proves density of the strict hull. Compactness
  of T_r makes conv(T_r) closed and proves the remaining hull equality.
- Dense countable nonstrict ray sufficiency handles p=0 or q=0 by the
  infimum at tau endpoints. It is not transferred to strict inequalities.
  The direct midpoint construction for r>=3 preserves each original ball
  constraint and makes the original inner-product inequality strict. The
  covariance proof of necessity is valid even if a variance vanishes.

## Arbitrary-quadratic obstruction

The chosen planar sections and analytic boundary arc follow exactly from
the hull formulas. The rational function R has simple, uncancelled zeros
and poles, so it is not a rational square. Division in R(x)[y] correctly
shows that any polynomial vanishing along an arc either makes R a square
or is divisible by y^2-R. The polynomial P is primitive over R[x]; Gauss's
lemma transfers irreducibility and divisibility, contradicting the degree
bound for a nonzero quadratic. Analyticity on a neighborhood of the compact
parameter interval makes each remaining zero set finite.

For strict descriptions, the planar origin excludes identically zero
restricted polynomials, and every boundary point must make a remaining
polynomial zero. For nonstrict descriptions, identically zero restrictions
are discarded; if every remaining inequality were strict at a boundary
point, their finite conjunction would contain an infeasible neighborhood.
These arguments also cover constant polynomials and the empty remaining
family. The scope is correctly limited to finite conjunctions in the
original variables, with lifted formulations explicitly preserved.

## Literature, scope, and reproducibility

Read the new source audit, bibliography additions, and consolidated
coverage/literature integration. The exact DMS example and its displayed
multiplier family agree with the local published full text, Proposition
2.8 and Section 7.4. Its explicit HHC failure and two negative leading
eigenvalues are correctly calculated. Homogeneous PDLC fails for the new
example by the incompatible block inequalities; its determinant and
common projective zero are correct. The limited comparisons do not claim
that all infinite-aggregation phenomena are new.

Independently opened Uhlmann's author-hosted primary PDF. Pages 408–410
state separate concavity, permit unnormalized positive matrices, and give
the product-of-traces formula at partial-fidelity index zero. The
manuscript's credit and real-matrix boundary proof are appropriate:
https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf .

Independently checked Wang–Kılınç-Karzan v2 Section 4.1 and Assumption 1.
Their replication-count condition and positive-definite aggregation
assumption apply with three constraints, zero objective, and r>=3. The
manuscript correctly distinguishes that closed epigraph/hull result from
the strict fixed-level claim:
https://arxiv.org/html/2403.04752v2 .

Checked Beck 2009 Theorems 3.1 and 3.4 in the retrieved primary PDF
extraction: the stated numbers of real matrix functions, signed
definiteness and row-dimension conditions match. These are global image
results; the paper's all-hyperplane claim is presented separately. Other
new references were reviewed through the author's source/version record;
this reviewer did not repeat the entire bounded priority search. The
novelty statement is narrowly scoped and qualified.

## Checks actually run

- Read both complete new mathematical sections, author report, dedicated
  literature audit, bibliography additions, exact-check script and README,
  current main inputs and relevant coverage/literature updates.
- Primary-source `rg`/`sed` checks of Beck 2009 and DMS; web primary opens
  and targeted reads of Uhlmann and WKK v2 as described above.
- `python3 paper-quadratic-aggregation/supplement/check_infinite_aggregation.py`:
  **PASS**, including 2,601 rational ray identities and six finite-family
  outside witnesses. The script's limitation to finite evidence is clear.
- SHA-256 comparison with the 22-file author snapshot: all manuscript,
  bibliography, script, and process files match. The sole changed entry is
  the external concurrent source `results/infinite-quadratic-aggregation-hhc.md`.
  The coordinator was informed and reports that the changes document
  concurrent formal-package coverage, with no additional mathematics;
  integration is deferred to synthesis. This review accepts the unchanged
  manuscript snapshot and does not assert review of those later formal
  additions. The authored snapshot was not rewritten.
- Searched the final main LaTeX and BibTeX logs for warnings, undefined
  references, overfull and underfull boxes: no matches.

No current reviewer-report reads, manuscript edits, new subagents, Lean
reruns, project-wide verification, or CI inspection were performed.
