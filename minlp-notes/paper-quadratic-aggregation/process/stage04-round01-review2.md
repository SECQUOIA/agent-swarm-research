# Stage 4, round 1, independent review 2

Verdict: **pass; no major or minor correction requested**.

I reviewed both complete stage 4 sections, the exact-check script and README,
bibliography additions, author report, stage 4 literature audit, snapshot,
and updated coverage destinations. I did not read another current review,
edit manuscript source, or treat future stages as present obligations.

## Gram-map proof

The sharp threshold and its exceptions are proved correctly.

- Singular Gram factors have the stated row-orthonormal extension when
  `r>=k`. The rectangular SVD proves the maximum trace value with actual
  attainment. For even `k`, pair rotations reach the negative maximum;
  for odd `k>=3`, their endpoint is nonpositive and negating the factors
  supplies the other half of the interval. The scalar sphere case and
  `k=r=1` exception are handled separately. This avoids silently assuming
  the orthogonal group is connected.
- The Frobenius Cauchy–Schwarz estimate uses correctly ordered matrix
  factors. In the positive definite case, the constructed `Z` satisfies
  `ZGZ=H` and gives equality. Regularizing **both** PSD arguments, followed
  by continuity of matrix square roots, proves the boundary case without
  asserting attainment of the infimum there. The infimum consists of
  functions linear in `G`, so separate concavity follows directly.
- The exact hyperplane image follows from the full attained trace interval,
  including zero coefficients and singular matrices. Its convexity follows
  from the proved concavity. The exceptional scalar square map is HHC but
  has the narrower equality image described in the manuscript.
- For `r<k`, the explicit `t=0` midpoint has rank `r+1`, establishing
  necessity for the full Gram map. Linear output maps give the repeated
  block corollary; neither arbitrary mixed terms nor necessity for every
  smaller output family is incorrectly inferred.

## Good multipliers and infinite necessity

The good-multiplier classification uses both actual homogeneous inertia and
strict hull validity. A negative eigenvalue in the leading two-by-two block
repeats at least twice because `r>=2`; hence no such multiplier is good.
Conversely a nonzero multiplier in the PSD cone has a strictly negative
constant block, exactly one negative homogeneous eigenvalue, and a convex
aggregate strictly negative on every finite convex combination of strict
feasible points. This establishes the exact class, not just a sufficient
subfamily.

For each witness parameter, the Gram matrix is genuinely positive definite
and realizable already in two dimensions. Equality in its aggregate value
forces equality in both the weighted AM–GM inequality and the cone bound,
and thus precisely one positive multiplier ray. Therefore the witness
satisfies **every** other good strict inequality, even if uncountably many
others are retained. This proves the asserted indispensability rather than
only ruling out one chosen discretization.

For nonstrict finite descriptions, the manuscript correctly moves outside
the closed hull: decreasing the off-diagonal Gram entry preserves positive
definiteness and the finite selected slacks, while increasing the omitted
aggregate to `2 eta>0`. The original boundary witness alone would not prove
that statement. The proof works for arbitrary finite good families, including
interior or coordinate multipliers.

## Hulls, lifts, and countability

- The BDS theorem is used only after checking its dimension, strict
  nonemptiness, properness, and HHC hypotheses. The good cone's decomposition
  into coordinate rays and positive-parameter rank-one rays is exact.
- For positive `p,q`, the minimum over the parameter is attained, giving
  the strict inequality in the ordinary hull formula. For nonnegative
  `p,q`, the same infimum includes the zero-coordinate endpoint cases.
  Continuity in the positive parameter proves that a countable dense
  family suffices for the closed nonstrict description. It is not applied
  incorrectly to strict inequalities at the indispensable parameters.
- The Schur complement of the identity block gives exactly the stated
  interval for the scalar lift. Strict positivity is possible precisely
  when the upper endpoint exceeds `1/2`; the closed counterpart allows
  zero slack and singularity.
- The proof of closed-hull equality uses the explicit closed formula,
  not an assumed closed projection. Mixing with `M(0,0,1/2)` yields a
  positive definite lift, and when its scalar remains at the endpoint
  it can be increased slightly without losing definiteness. Compactness
  of the original closed feasible set then justifies `D_r=conv(T_r)`.
- The direct midpoint construction is correctly limited to `r>=3`.
  Its covariance converse has strict variance inequalities and remains
  valid when either variance is zero. The `r=2` proof legitimately uses
  the earlier HHC result and BDS theorem instead.

## Arbitrary finite quadratic descriptions

The stronger original-variable obstruction is sound. The restricted
sections have the claimed quartic boundary arc inside the ball bounds.
The rational radicand has simple zeros and poles and therefore is not a
square in `R(x)`. Division in `R(x)[y]`, followed by primitivity and
Gauss's lemma, rules out an identically vanishing nonzero quadratic on
that arc. Analyticity on a neighborhood of the compact interval then
makes every such quadratic's zero set on the arc finite.

For a strict description, no plane restriction can vanish identically
because the planar origin is feasible. Continuity puts every restricted
polynomial at most zero on the boundary, where at least one must vanish.
For a nonstrict description, identically zero restrictions can be removed;
the remaining conjunction must still have a zero at every boundary point
or would include a neighborhood outside the hull. Both cases contradict
finite coverage of the infinite arc. The statement is correctly limited
to conjunctions in original variables and does not exclude the proved
finite semidefinite lifts.

## Literature and reproducibility checks

- Re-read the BDS v2 conjecture and hull theorem checked in earlier stages.
  The new example resolves precisely the HHC/good-aggregation question.
- Read the DMS published extraction's Proposition 2.8 and independently
  checked the displayed earlier example: its hyperplane midpoint is
  impossible, and its cited multiplier family has two negative leading
  eigenvalues. The manuscript accurately distinguishes this antecedent
  rather than claiming first infinite aggregation necessity in general.
- Opened [Uhlmann's published author PDF](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf),
  checking equation (14) and the zero-index specialization. The classical
  product-of-traces identity is credited appropriately.
- Read Beck 2009 Theorems 3.1 and 3.4 in the downloaded primary extraction.
  The real count and definiteness qualifications match the discussion;
  arbitrary hyperplane restriction need not preserve QMP structure.
- Independently opened [Wang–Kılınç-Karzan v2](https://arxiv.org/html/2403.04752v2),
  including Assumption 1 and Section 4.1. Its replication threshold is
  at least the number of constraints. Zero objective and the positive
  sum of the two ball matrices give the claimed prior closed-hull
  consequence for `r>=3`; the versioned locator is correct.
- Opened [Brun–Sun–Watson v1](https://arxiv.org/html/2603.18473v1) as an
  additional primary comparison. The manuscript's hypograph versus
  fixed-level qualification prevents an unsupported inference from
  convexification followed by slicing.
- The homogeneous PDLC obstruction, repeated determinant factor and
  common projective zero witness were checked algebraically. They
  accurately delimit applicability of the cited finiteness results.
  The explicit resolution priority sentence is narrowly qualified;
  no new fidelity inequality or general SDP principle is claimed.
- Ran `python3 paper-quadratic-aggregation/supplement/check_infinite_aggregation.py`:
  passed with 2,601 exact ray identities and six finite-family outside
  witnesses. Read the rational calculations and actual DMS midpoint
  reconstruction. These finite checks were not substituted for the
  universal proofs above.
- Scanned the current main LaTeX and BibTeX logs for warnings, undefined
  references, and overfull/underfull boxes: no matches. No build rerun,
  broad tests, CI inspection, formal rerun, or subagent was used.

This verdict accepts stage 4 only; quantitative approximation, later PDLC
results, formal integration, and final synthesis still require their
assigned stages.
