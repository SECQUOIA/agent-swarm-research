# Stage 6, round 1: independent review 5

Verdict: mathematical pass, with one minor wording correction. No major
issue identified. The transfer, low-dimensional scope, strictness argument,
sharpness proof, and oriented closure formula are justified.

## Minor correction

- `sections/08-four-aggregation.tex:309`: change “is strict feasible” to
  “is strictly feasible.” The displayed point has the correct strict
  residuals; this is grammar only.

## External input and dimension audit

Read the entire section, its author/literature records, current coverage,
supplement/checker, bibliography addition, and snapshot. Independently read
the local primary BD preprint at its standing independent-matrix setup,
Theorem 1.4, Proposition 8.7, and the final proof combining Propositions
8.6, 8.7, and 8.10. Its proof explicitly separates n=1,2 from n>=3, so the
manuscript does not infer the all-positive-dimension scope from an omitted
restriction. Its regularity, PDLC, interior, and no-points-at-infinity
assumptions are preserved. The relevant good/permissible multipliers have
at most one negative homogeneous eigenvalue. Compactness in the application
also makes the distinction between hull and closed hull harmless there.

The manuscript distinguishes the regular nonstrict external theorem from
its own strict transfer, acknowledges Dunbar's stronger theorem statement,
and does not rest novelty on first removing the infinity assumption. I
checked the saved dissertation extraction at Theorem 5.0.5; its stated scope
supports that acknowledgement. The record is candid about access and damaged
glyphs and does not turn its proof-dependency concern into an unsupported
published-error claim. This review did not perform an exhaustive new priority
search or independently verify every antecedent proof.

## Transfer proof review

- The three chosen perturbation matrices are positive definite and independent
  already when n+1=2. Their leading blocks are positive definite. A cubic
  coordinate minor with nonzero leading coefficient gives only finitely many
  exceptional dependence parameters even for an originally dependent triple.
- Properness rules out a common strict negative leading direction without
  requiring HHC. Therefore a nonzero direction cannot satisfy all perturbed
  leading inequalities nonstrictly. Normalizing an unbounded sequence in the
  perturbed closed set would give exactly such a direction, proving boundedness.
  Strict feasibility and signed PDLC both persist for small positive epsilon.
- The countable-base regular-level lemma is correct. For a bad level, a basic
  neighborhood of a point attaining that level has precisely that value as
  its infimum. The ratio maximum is continuous because all perturbation
  denominators are positive. Selecting levels -epsilon outside the countable
  exceptional set has the correct sign and can be combined with the finite
  dependence exception set along a decreasing sequence tending to zero.
- The resulting closed inward set equals the closure of its strict set and
  of its interior. Every fixed finite original feasible subset eventually
  belongs to the inward strict set. No original boundedness or regularity is
  assumed in this argument.
- Strictification correctly deletes all globally nonpositive polynomials
  before taking interiors. A quadratic with zero at a local nonpositive
  interior point has a global maximum zero by its exact Taylor formula, so
  every retained sublevel has the stated strict interior. Finite intersections
  and the nonempty open convex hull justify the set equality. Boundedness
  ensures at least one retained inequality.
- After duplication, compactness gives one common subsequence for all four
  simplex multipliers. Strict negativity at the fixed feasible point keeps
  each limiting matrix nonzero with exactly one negative eigenvalue; no
  negative-eigenvalue disappearance is possible. The perturbation norm tends
  to zero uniformly over normalized multipliers.
- A further common eigenvector subsequence is independent of the eventual
  choice of an original feasible point. Eventual inclusion and goodness of
  the perturbed inequalities force all those points into the same oriented
  negative component. The limiting scalar product cannot vanish, since the
  limiting quadratic remains strictly negative at each original feasible
  point and is PSD on the negative eigenvector's orthogonal complement.
  Convexity of that component therefore preserves strict validity on every
  finite convex combination, including singular and rank-one limits.
- For the reverse inclusion, finitely many positive strict margins at a fixed
  point survive matrix convergence. Its inclusion in a sufficiently late
  inward hull yields membership in the original ordinary hull. No interchange
  of arbitrary intersections and closures is used.

## Dependent triples, sharpness, and closure

The optional two-generator reduction is valid: evaluation at a strict feasible
lift is strictly negative on every nonzero generator combination, making the
finite cone pointed. Its normalized slice in a span of dimension at most two
is a compact point or segment, with endpoints on original generator rays.
The selected original inequalities and all original rows imply one another
strictly through nonzero nonnegative combinations. The attributed two-bound
then transfers its multipliers and inertia without changing the system.

The four-necessary example has the stated signed PDLC identity and strict
point. Each displayed ray is good, using the negative-s component where
needed. For n>=3, a negative coefficient of rho would give at least two
negative eigenvalues, so every good multiplier belongs to the displayed
four-ray cone. The explicit interval for the decomposition coefficient is
nonempty, and all coefficients are nonnegative. Each witness has zero only
on its designated ray and strict negativity on the other three; this proves
indispensability even against arbitrary good multiplier choices. The upper
bound then proves exactness of these four. No sharpness at n=1,2 is asserted.

The SOC corollary absorbs the magnitude of the negative eigenvalue into its
oriented vector and correctly keeps that orientation. Convex mixing with a
common strict feasible point proves the closed conic intersection is exactly
the closure. The half-ball counterexample with a redundant negative-definite
row satisfies homogeneous PDLC and has the extra isolated weak point e1.
It verifies both warnings: naive weak quadratic replacement and the hull of
the original weak system can differ from the closure of the strict hull.

## Targeted checks actually run

- `python3 paper-quadratic-aggregation/supplement/check_four_aggregation.py`:
  PASS for the PDLC identity, strict point, exact radical/rational slack
  vectors, and cone-decomposition coefficient identity.
- Independent SymPy heredoc recomputed the PDLC identity and all four witness
  slack/sign vectors from the original rows. It also verified positive
  definiteness and a nonzero independence minor of the three perturbation
  matrices in the smallest n+1=2 dimension. All passed.
- SHA-256 compared all 18 entries in the author snapshot: no mismatches.
- Inspected dedicated saved LaTeX/BibTeX logs: 36 pages, with no Warning,
  Overfull, Underfull, or undefined matches. Did not rerun LaTeX.

Finite algebraic checks are not substituted for the universal transfer proof
or the credited external theorem. No manuscript edits, other current review
reads, coordination, subagents, global verification, CI inspection, or formal
reruns were used.
