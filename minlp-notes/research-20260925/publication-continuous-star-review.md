# Publication readiness review: continuous quadratic stars

Reviewed on 2026-09-25. This is a fresh, scope-bounded audit of
[the sparse-hull investigation](disjunctive-exploration.md),
[the five-variable star certificate](star-hull-proof-exploration.md),
[its transfer review](star-copositive-transfer-review.md),
[the four-variable star reductions](four-star-analytic.md), and
[the one-sided-domain review](four-star-one-sided-review.md).
No new research direction was pursued.

The accepted mathematical statements are ready to use as supporting
results, examples, or limitations in a potential publication. No unresolved
proof defect was found. They should not be presented as a standalone major
original contribution: the decisive matrix obstruction and the main
exactness inputs are prior work, and priority for the particular star
specialization has not been established. The unrestricted four-variable
box star remains unresolved in this work.

## Disposition of the claims

| Claim | Audit result | Publication treatment |
| --- | --- | --- |
| Two exact edge moment hulls can disagree globally on a three-vertex path | The two local laws and the separating quadratic are correct. The gap is exactly `1/128`. | Use as a small explanatory example. Do not claim discovery of the general failure of local moment gluing. |
| Full dense SDP–RLT is exact after projection for forests on at most three vertices | Correct consequence of Burer–Natarajan–Willemsen, using variable complements and support functions. | Attribute the substantive exactness theorem. |
| A fixed finite family of linear cuts cannot repair the basic SDP uniformly on the four-vertex path | The quoted Zhang–Wang construction retains path support through its diagonal and linear perturbations. | Attribute the lower bound. Keep the quantifiers over cuts and objectives in that order. |
| Five-variable stars can have a strict full SDP–RLT gap, with positive squares and submodular interactions | The explicit rational certificate is correct; its true minimum is zero and its relaxed value is `-9337/250000`. | Retain the exact example and credit Drury's matrix. The particular box specialization has qualified priority. |
| Every connected interaction graph on at least five vertices admits such a gap | The spanning-tree dichotomy, deterministic padding, and small negative edge perturbation are correct. | Present as a corollary of the cited path gap and the star specialization, without priority or complexity claims. |
| A binary-center face is exact for the retained star moments; a nonpositive center square coefficient implies exactness | The conditional distribution construction, including degenerate probabilities, is complete. | Use as a structural supporting lemma, with novelty unclaimed. |
| One bounded center and at most three nonnegative leaves admit exact SDP–RLT when the infimum is finite | The book-graph homogenization and corrected `T5` SPN theorem prove this directly. | Attribute the graph theorem. Nonedge nonnegativity constraints are essential to the stated argument. |
| Suitable leaf orientations permit an exactness certificate for some four-variable box stars | Correct when releasing the chosen upper bounds preserves the minimum. The endpoint response test is sufficient. | Keep the bound-release premise. This is not a solution of the arbitrary four-variable case. |

## Independent proof audit

The five-variable calculation does not rely on numerical copositivity.
Differentiating each leaf term gives its clipped affine minimizing response.
Every response stays below four on the center interval, so the displayed
five-piece scalar reduction is valid. The two square pieces, the signs of
the three remaining pieces, and the exhibited zero prove the true optimum.
The rational moment matrix is positive definite and all box product
inequalities have strictly positive slack. Thus the gap survives small
perturbations and does not arise from an SDP solver tolerance.

The general transfer uses separation from the closed cone
`PSD + entrywise nonnegative`. The closedness argument is valid because the
nonnegative summand bounds the PSD diagonal, which then bounds the whole
PSD matrix. Perturbing the separating moment matrix by a small positive
multiple of `I + ee^T` makes it strictly positive and positive definite
without losing the negative objective. A sufficiently large common box
bound supplies all remaining RLT inequalities. This proves a gap even if
the dehomogenized polynomial has no zero. The explicit example separately
supplies a zero and therefore has true minimum zero.

For the connected-graph corollary, a spanning tree either contains a
four-vertex path or is a star with at least four leaves. Extra variables
fixed deterministically to zero preserve the full dense moment constraints.
Adding a coefficient `-delta` on each of `r` missing graph edges decreases
the true objective by at most `r*delta`, while it cannot increase the
old relaxed witness value. Taking `r*delta` below the original gap proves
the asserted exact support and strict gap. The rational Zhang–Wang
Appendix A witness is a directly checked choice for the path case.

The binary-center construction preserves the first moments, every
individual square, and every center–leaf product. It deliberately does
not preserve the unused leaf–leaf moments. This is sufficient for star
objectives and for the stated projection, but not for equality of full
moment hulls. Increasing only the center square moment to its first
moment preserves PSD and RLT. This proves the pointwise rounding bound
and the uniform bound `max(a,0)/4` on a unit center interval.

For the one-sided theorem, the homogeneous variables are
`(r,s,y) >= 0`, with `t=s/(r+s)`. Continuity handles the boundary
`r=s=0`; nonnegativity at positive `r+s` uses the full nonnegative leaf
orthant. The resulting matrix has book support. The corrected `T5`
theorem also covers missing edges and fewer leaves by padding, positive
edge perturbation, and closedness of the SPN cone. After substituting
`r=1-t`, `s=t`, PSD controls the square part and full product
nonnegativity controls the entrywise nonnegative part. An SPN
decomposition need not preserve book support, so dropping the
leaf–leaf product constraints would invalidate this proof.

## Primary sources checked in this pass

- [Burer–Natarajan–Willemsen, arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3),
  Theorem 1 and Example 4: the current version establishes submodular
  exactness through dimension three and contains a four-dimensional
  path counterexample. The earlier all-dimensional conjecture is obsolete.
  The forest projection argument is an immediate application of this
  exactness result, not a new proof of it.
- [Zhang–Wang, arXiv:2609.03617v1](https://arxiv.org/html/2609.03617v1),
  Proposition 1, Lemma 2, Theorem 2, and Appendices A–B: the base polynomial
  has only path interactions; the finite-cut perturbation leaves its
  off-diagonal support unchanged. The rational Appendix A point satisfies
  full RLT, including diagonal bounds. The source supplies the finite-cut
  lower bound; the repository only specializes its sparsity statement.
- [Qiu–Yıldırım, Journal of Global Optimization 90 (2024), 293–322](https://link.springer.com/article/10.1007/s10898-024-01407-y),
  Lemmas 18–19 and Proposition 20, also available in the
  [local literature copy](../literature/papers/qiu2024-on-exact-and-inexact-rlt/fulltext.md):
  their optimality conditions yield the homogeneous copositive/SPN
  equivalence used in the comparison. At the origin, complementarity
  forces their upper-bound multiplier `r`, lower-product multiplier `W`,
  and scalar PSD block `beta` to zero. PSD then forces `h=0`, and with
  `c=0`, stationarity and nonnegativity force `s=Y=0`. Their matrix equation
  becomes `Q=Z+H`, with `Z>=0` and `H` PSD. The converse is immediate.
  This checks the claimed specialization, rather than attributing it as
  the literal wording of their proposition.
- [Shaked-Monderer's corrigendum, arXiv:1712.05115](https://arxiv.org/html/1712.05115),
  Theorem 1: the corrected result proves `T5` is SPN. The earlier claim
  about every book graph is not an available theorem.
- [Drury's primary supporting page](https://www.math.mcgill.ca/drury/research/spn/index.html),
  Section 4: its integer matrix agrees entry for entry with the repository
  matrix. The matrix obstruction is prior work, independently of the
  repository's exact finite-box certificate.
- [Khajavirad, arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2),
  Lemma 4: the decomposition result requires no positive loops on the
  overlap and concerns the source's one-sided square hull. It does not
  assert the full equality-moment gluing disproved by the local example.
- [Gabl, arXiv:2509.19348v1](https://arxiv.org/html/2509.19348v1),
  Theorems 9–10: this nearby result uses set-completely-positive arrowhead
  completion. Its scalar-leaf form imposes local affine equalities and
  their quadratic moment equalities, bounded shared moments, and a
  rank-one extreme-point condition. It does not assert arbitrary box-star
  gluing from common first and second moments. This comparison addresses
  an alternative terminology under which an equivalent theorem might
  otherwise be missed.

Additional web queries covered `star SDP-RLT quadratic`,
`box T_6 SPN`, `star copositive box quadratic`, `arrowhead box semidefinite
quadratic exact`, `Drury SDP-RLT`, and `set-completely positive arrowhead`.
No checked source from this bounded search stated the same five-variable
box certificate. That outcome is not evidence that the specialization is
new. The safe publication decision is to retain its explicit attribution
and make no priority claim.

## Reproducibility and limits

The following targeted commands were rerun in this audit with Python
3.13.11 and SymPy 1.14.0:

```text
python research-20260925/check_star_counterexample.py
python research-20260925/check_star_independent_review.py
python research-20260925/verify_disjunctive_review.py
```

All passed. The first uses standard-library rational arithmetic. The
second reads only the literal matrices from the first and independently
uses SymPy for all 63 nonempty principal minors, RLT, scalar elimination,
affine transformation, and inertia. The third checks the local moments
and exact rational certificates from the cited path construction.
Manual review supplies the general cone, graph, and probability-law
arguments. No Lean verification, project-wide verification, or CI
inspection was performed for this topic. Numerical discovery searches
were not rerun and are not part of the proof.

No mathematical blocker remains for publishing the accepted statements
with this scope and attribution. A standalone paper claiming a new star
exactness boundary would have two genuine blockers: the fully bounded
four-variable star is unresolved, and priority for the five-variable box
specialization remains unestablished. Neither should be hidden by calling
the investigation complete. They are excluded from the accepted result
package, and resolving them is not needed to use the verified supporting
material. Solver improvements, stronger conic-formulation impossibility,
and general optimization hardness have not been established here.
