# Representability and sparse-graph proof audit

Scope: `sections/06-representability.tex`, `sections/07-graphs.tex`, and
`appendices/C-representability.tex`. The proofs were reconstructed from the
September and October notes and their existing reviews. No optimization
experiments, sampling experiments, timing experiments, project-wide checks,
or CI checks were run for this work.

## Conclusions

The sharp four-variable nonrepresentability theorem survives reconstruction.
It applies to the full moment hull, its positive diagonal upward closure,
and the correctly homogenized dual cones. The simple-vertex polytope
extension and the positive-induced `K4`-minor transfer also survive. The
small-positive-component finite lift is exact, subject to its explicit
torso-width and input-decomposition qualifications. The forest reduction
to the submodular cone is a proved equivalence, not a classification.

No result in these chapters depends on the three-variable completeness
conjecture or on a proposed classification of series-parallel graphs.
The path and star cases remain open and are presented as limits of the
proved boundary. The inconclusive archived fan SOS computation and the
SPN-pattern table are omitted because they do not add a proved
classification or support a finite-lift conclusion.

Independent manuscript reviewer `/root/review_repr` found no substantive
mathematical defect in these three TeX files. The reviewer recommended
making the empty-`R` case explicit in the bag formulation; this was added
as a single empty bag with table mass one.

## Proof corrections and completed details

1. **Normalization for the unbounded positive hull.** The original notes
   refer to the dual of `{1} × H`. The manuscript instead defines the
   closed homogenized cone with all height-zero diagonal rays. A finite
   lift is homogenized first; its zero-height visible directions must lie
   in the recession cone. Explicit addition of the polyhedral diagonal
   cone then fills directions that the homogenized lift might omit.
   This avoids assuming that every visible recession direction has a
   lifted recession witness. The lemma works for any compact convex
   `K` plus polyhedral `D`.
2. **The four-variable embedding.** All five Horn coordinates are retained,
   with `u1 = 1` and the other four equal to box coordinates. The diagonal
   square coefficients are positive monomials. Lexicographic ordering of
   `Q^5` makes each evaluation coordinate a positive infinitesimal. The
   mapped evaluation is exactly `epsilon^(4e1) * eta`, not an informal
   limit or a numerical approximation.
3. **External versus own steps.** The positive-square separator, the
   Hahn coefficient-map theorem, real-closed-field transfer, and
   closed-cone duality are external inputs. The cube embedding, evaluation,
   unbounded normalization, simple-ray geometry, and graph-minor reduction
   are the manuscript's explicit arguments. BKT is not said to state the
   cube or polytope theorem itself.
4. **Simple rays.** A uniform bound using all nonincident facet slacks
   replaces the informal phrase “close to the ray.” The case `u1 = 0`
   is handled separately. The cone is considered in its linear span;
   polytopes are considered in intrinsic affine coordinates.
5. **Proper faces.** The literal statement “every face of Q4 is a shadow”
   in the notes is false because the full hull is an improper face of
   itself. The manuscript states **every proper face**. The intended
   substantive result is proved: exposed-face zero sets are finite unions
   of polytopes of dimension at most three; compact homogenized lifts give
   their finite convex hull; a finite chain of relative supporting sections
   handles nonexposed faces.
6. **Graph contraction.** The exposed squared-difference equation kills
   the contracted vertices' diagonal slack. The manuscript explicitly
   restores the merged diagonal ray after projection; it does not claim
   projection alone yields the positive diagonal hull.
7. **Mixed signed graphs.** The minor branch sets are restricted to the
   positive-induced graph. Outside negative-loop vertices and arbitrary
   additional edges are allowed. Singleton branch-set slack is retained
   in the intermediate image and then completed by adding the other rays.
8. **Small-component lift.** The proof reconstructs the joint binary law
   from separator-consistent bag tables, conditions the continuous
   component simplex lifts on boundary states, handles zero-probability
   states, and proves reverse inclusion. The complexity statement uses
   the completed-boundary torso and a supplied tree decomposition. It does
   not infer a torso-width bound from original graph treewidth, claim
   efficient computation of an optimal decomposition, or count every
   coefficient in the linear maps as constant cost.

## External source contracts verified by the Luna literature agent

All primary-source and novelty research was delegated to
`/root/literature` using GPT Luna with maximum reasoning. This writer did
not browse or inspect primary literature. The literature agent verified
the published BKT paper and reported these contracts:

- `BodirskyKummerThom2024`, Lemma 2.3, printed p. 4: unital base-field-linear
  completely positive self-maps preserve LMI formulas of every finite
  size over the base field. The manuscript also gives the direct witness
  proof for spectrahedral shadows.
- Section 2, printed p. 5: a Hahn field over a real closed coefficient field
  and a divisible ordered abelian value group is real closed. Lexicographic
  `Q^5` satisfies the hypotheses.
- Theorem 2.13, printed pp. 7–8: positive-definite coefficient multipliers
  on Hahn series are completely positive, with base-field linearity.
- Remark 3.2, printed p. 9: membership in the group-ring SOS cone is
  equivalent to polynomial SOS after some common integer-power
  substitution.
- Example 3.4, printed pp. 9–10: the Horn form fails SOS after every power
  substitution. Applying this to the even-power nonnegative polynomial
  `h(z1^2,...,z5^2)` supplies the manuscript's group-ring witness.
- Theorem 3.7, printed p. 11: a group-ring non-SOS polynomial has, over a
  real closed extension, a linear separator strictly positive on every
  nonzero square and negative on the polynomial. Normalizing the separator
  yields the positive-definite `f` with the required negative Horn sum.
- Remark 3.17, printed p. 14: closed convex cones and their duals have
  equivalent spectrahedral-shadow status.

The canonical keys for the other source inputs are `Diananda1962`,
`MaxfieldMinc1962`, `AnstreicherBurer2010`, `BurerDong2013`, and
`Khajavirad2026SparseBoxQP`. The literature agent owns bibliography and
novelty adjudication. The mathematical chapters make no unconditional
priority claims and attribute the low-dimensional construction to prior
work.

## Targeted check actually run

A single inline Python exact-integer check evaluated the 25 exponent
identities

`2ei + 2ej + exponent(ui(xi)) + exponent(uj(xi)) = 4e1`

and checked the leading sign of each of the four infinitesimal box
coordinates. It exited zero and printed:

`PASS: all 25 Hahn evaluation exponents; all four box infinitesimals; all four square-coefficient exponents.`

The check used only integer tuples and Python's standard library, with no
solver, external source, or previously archived experiment. An `rg` scan
for stale citation keys, the corrected sum-index typo, and unfinished
placeholders in the three scoped TeX files returned no matches. Full
manuscript compilation and integration checks belong to the root task.
