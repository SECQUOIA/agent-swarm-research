# Publication assessment of the quadratic hull results

Date: 25 September 2026. Scope: the completed three-variable cut family,
its exact relaxation gap, and the supporting sparse-hull results from this
research batch. This is a research and verification assessment, not a manuscript.

## Verdict and proposed contribution

The main mathematical package is ready to support a focused theoretical
submission. Its strongest claim is an explicit, exactly certified negative
answer to the three-positive-variable question for a specified recent
relaxation, followed by a valid parameter family and an exact small SDP
formulation enforcing that family. Independent proof review found no unresolved
gap in these claims. The contribution has a clear comparison with published
and publicly available formulations, rather than resting on numerical evidence.

The appropriate scope is **a missing family of quadratic inequalities and its
compact enforcement**, not a new general method for solving three-variable
box quadratic programs. Exact formulations and complete separation for that
whole hull were already known. The literature audit supports a candidate
original contribution relative to the specified relaxations; it does not
certify priority against every equivalent formulation. Practical superiority,
a complete hull description, and minimality of the new lift are not claimed.

Two supporting structural results can accompany the main package if they help
the eventual presentation: an exact construction when each connected positive
component has at most three vertices, and absence of any finite SDP lift when
the positive-induced graph contains a `K_5` minor. Their established ingredients
and their narrower originality claims must remain visible.

## Claims that can be stated

| Claim | Exact assumptions and conclusion | Contribution and proof location |
|---|---|---|
| Strict three-variable gap | The full disjoint-support affine-SOS cone has a dual moment system of 27 maximal localizing matrices, without a degree cutoff. A quadratic with three positive square coefficients has cube minimum zero, while a rational moment point satisfying all 27 matrices strictly evaluates it to `-1/40`. | Direct negative answer for the source's explicit system; [counterexample](three-positive-disjoint-counterexample.md). |
| Stronger comparator gap | The same point satisfies PSD, off-diagonal RLT, triangle inequalities, diagonal caps, and all inspected Anstreicher–Puges SOC constraints under permutations and complements. | Exact separation from that strengthened system, hence also from its ETRI1/2/3 consequences. This concerns the inspected source formulas, not every possible later or differently defined triangle strengthening. |
| Valid parameter family | For `h` real and `d_1,d_2,d_3,k >= 0`, the displayed quadratic family is nonnegative on the cube. Positive diagonal slack preserves validity. | A polynomial identity establishes the whole parameter domain, including its boundary; [family note](three-positive-family-sdp.md). |
| Exposed rays and certificate exclusion | With all parameters positive, `h < min(d_1,d_2)` and `d_1+d_2-h+k < d_3`, the five contacts expose precisely the ray of that quadratic in the cone of cube-nonnegative quadratics. Every such member is outside the disjoint cone. | Geometric structure and a general exclusion argument; [counterexample, final theorem](three-positive-disjoint-counterexample.md#every-member-of-the-family-generates-an-exposed-extreme-ray). Scaling all parameters scales the polynomial quadratically, so these are not five independent dimensions of rays. |
| Exact family enforcement | All inequalities in the broader valid family are equivalent to one affine `5 x 5` PSD block and six nonnegative scalar auxiliaries. | The parameter quadratic reduces to order-four copositivity, a classical PSD-plus-nonnegative cone. The novel item under assessment is this family's representation, not the cone identity. |
| Exact sparse component construction | If every component of the positive-induced graph has at most three vertices, the joint moment hull with signed diagonal slack has a finite SDP lift. The displayed size bound uses a **supplied torso decomposition**, including its actual width. | Combination of classical simplex CP/DNN formulations, Bernoulli rounding, and finite binary marginal gluing; [Proposition 1](three-positive-exploration.md#3-exact-lifts-for-components-with-at-most-three-positive-vertices). |
| Sparse obstruction to every finite SDP lift | A `K_5` minor entirely within the positive-induced graph prevents a finite SDP lift of the joint hull. Extra vertices, edges, and negative loops are allowed. | Explicit section and projection onto a compact base of `CP_5`, using the known nonrepresentability theorem; [Theorem 3](three-positive-exploration.md#4-an-obstruction-to-every-finite-sdp-lift). |

The five-variable Horn witness remains a checked supporting example. It is
superseded by the three-variable witness as a variable-count obstruction to
this relaxation, and the Horn form itself is classical. It should not be
presented as a separate main novelty claim.

## Adversarial proof audit

The fresh [family proof audit](publication-quadratic-proof-audit.md) checks
the polynomial identities, unrestricted `h`, zero parameters, exact cone
decomposition, zero-diagonal normalization, all strict contact assumptions,
the zero scale in the exposed-ray proof, and both source comparisons. It
also distinguishes the baseline constraints carefully: the disjoint matrices
imply PSD, off-diagonal RLT, and ordinary triangle inequalities, but do not
imply diagonal upper bounds. The displayed point satisfies those bounds
separately.

The family SDP is a lift with auxiliaries. Six nonnegative variables suffice;
there is no six-variable lower bound. Setting its auxiliary matrix to zero
would already exclude the genuine cube point `(1/2,1/2,0)`. The separation SDP
decides family violation mathematically, but extracting an individual cut
from an arbitrary matrix solution needs a completely positive decomposition
or an additional vector search. No claim about exact polynomial-time SDP
decision in the bit model is used.

For the structural claims, this assessment independently rechecked the
following points against the full proofs and the primary external theorems:

- Bernoulli rounding of vertices without positive loops preserves every
  recorded product. A negative-loop diagonal is recovered by downward slack.
  Consistent bag tables produce a finite joint distribution; zero-mass states
  produce zero simplex blocks. Hence ordinary finite convex hulls suffice.
- The component formulation uses only quadratic component moments. It does
  not also provide an exact cubic coordinate. Its size bound counts variables,
  affine constraints, and bounded-order blocks; encoding every nonzero
  coefficient can introduce incidence factors. The original graph's width
  does not replace the actual torso width.
- The minor obstruction's first affine section equates branch coordinates
  and kills slack on nonsingleton branches. Its second section imposes the
  simplex equation and kills the remaining singleton slack. This section
  projects exactly onto the compact normalized `CP_5` base.
- Homogenizing a lift of that compact base introduces no nonzero visible
  zero-mass direction: such a direction would make the base unbounded.
  The result therefore concerns arbitrary finite SDP lifts, without a size
  restriction. It does not concern only one chosen relaxation.

No new proof correction was required. Editorial corrections now avoid an
unsupported minimal-lift-size implication, identify the older Horn result
as superseded for the three-variable question, and remove construction-agent
narrative from the main counterexample.

## Prior results that constrain the novelty claim

The [fresh priority audit](publication-quadratic-priority-audit.md) records
current versions, relevant sections, searches for equivalent inequalities,
and source comparisons. The earlier
[family priority review](three-positive-family-priority-review.md) contains
additional comparisons with Burer–Letchford and Lambert. The following
external results are central rather than optional background:

| Primary source inspected | What is already established | What remains in the present package |
|---|---|---|
| [Anstreicher–Burer, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf), full triangulated-polytope construction | An exact DNN lift of the full quadratic moment hull in dimension at most three. The displayed cube triangulation has six tetrahedra; five are also possible. | A selective family block and strict comparisons with other relaxations, without a new full-hull tractability claim. |
| [Burer–Dong, Section 5.3, Corollaries 3–4](https://optimization-online.org/wp-content/uploads/2010/05/2621.pdf) | Complete separation for the homogeneous three-variable box moment cone, and a recursive extension to four variables. | A compact explicit representation of the selected family, not the first separation method for the full hull. Separation does not itself imply a single finite SDP lift. |
| [Khajavirad, Section 3, equation (17)](https://arxiv.org/html/2601.18545v2#S3) | The precise disjoint moment system and its explicit three-positive-loop question. | A rational point feasible for that system and a valid inequality it violates. The source's later degree-index convention is unnecessary to this comparison. |
| [Anstreicher–Puges, Section 4, equations (14)–(16)](https://arxiv.org/html/2501.09150v1#S4) | A trilinear extension and SOC strengthenings implying ETRI1/2/3. | The same strict rational separation, with every switch and permutation checked. Intersecting with the new family is a strict strengthening; the isolated family block need not dominate the existing system. |
| [Bodirsky–Kummer–Thom, Remark 3.17 and Corollary 3.18](https://content.ems.press/assets/public/full-texts/serials/jems/no-issue/14297974/online-first/10.4171-jems-1509-online-first.pdf) | Nonrepresentability of copositive cones of order at least five, and equivalence under closed-cone duality. | A reduction of the stated signed box joint hull to the `CP_5` obstruction along positive graph minors. The deep arbitrary-lift impossibility theorem is an external input. |
| [Nishijima, Sections 3–4](https://arxiv.org/html/2602.23725v1) | Related nonrepresentability over symmetric cones, using sections, and exposed Horn transformations. | The box graph reduction has a different domain. Section-transfer arguments and exposed copositive rays are established methods. |

Source artifacts with the same apparent arXiv version label need not have
the same displayed manuscript date. In particular, the inspected
Anstreicher–Puges HTML and the pinned v1 PDF have different dates. The
[retained source manifest](publication-sources/source-manifest.json) and fresh
audit identify the actual formulas used; the comparison does not assume those
artifacts are identical. The current Optimization Online and author copies
of Khajavirad retain the same three-positive-loop question. The current
Anstreicher–Puges Optimization Online and arXiv PDFs have the same inspected
formulas (14)–(16) and Lemmas 4–5. The publication audit found no advertised
later version that supersedes either comparison.

The dedicated graph audit searched combinations of box/hypercube quadratic
hulls, positive loops, `K_5` minors, completely positive completion,
spectrahedral shadows, and sparse copositive graphs. This assessment repeated
targeted searches for `quadratic K5 minor spectrahedral`, `box Bodirsky Kummer
quadratic`, and `completely positive minor semidefinite representability`.
No exact graph theorem was identified in those searches. This is limited
priority evidence, not a proof that none exists. In particular, SPN graph
results address equality with a particular PSD-plus-nonnegative cone and
must not be confused with the absence of every finite SDP lift.

## Reproduction and verification scope

The fresh family reviewer ran and passed:

```sh
python research-20260925/checks/three_positive_gap_certificate.py
python research-20260925/verify_three_positive_family_review.py
python research-20260925/verify_three_positive_disjoint_review.py
```

These check the 27 strictly positive definite localizing matrices, all 24
and 48 switched SOC instances, the symbolic family and moment identities,
and independent rational edge and zero calculations. The key values are
`-1/40` for the cut, `2831/4000000` for the first SOC slack minimum, and
`124813/12500000` for the second. The review also derives RLT and triangle
validity from the eight nonnegative cube atom weights and checks the separate
diagonal caps exactly.

This assessment independently ran and passed:

```sh
python research-20260925/verify_cp5_face.py
python research-20260925/verify_horn_disjoint_review.py
python research-20260925/checks/three_positive_horn_certificate.py
```

The first checks the exposing identity, a CP normalization example, and the
Petersen-to-`K_5` contraction. The other two independently check all 243 Horn
localizing matrices and the exact objective `-1/2000000000000`; one also
checks every limiting matrix after subtracting `I/100` and the perturbation
bound. These computations corroborate algebra and finite examples. They
do not prove the external CP/DNN or nonrepresentability theorems, the general
gluing argument, or novelty. This quadratic package has no Lean coverage.
No project-wide checks or CI inspection were performed.

## Remaining questions are extensions, not hidden assumptions

The completed claims require neither a classification of all nonnegative
cube quadratics nor a proof that all symmetry copies of this family are
complete. Both remain worthwhile extensions. Likewise, the structural results
leave the four-positive-variable case and other positive graphs without a
`K_5` minor open in this package; no converse is asserted.

For a computational publication, an additional experiment would be needed
to compare selected family blocks, individual cut generation, and the exact
tetrahedral formulation on larger sparse instances. A single orientation
uses one PSD block, but up to 24 orientations can cost more than the exact
six-block comparator. No present theorem implies a runtime or total-size
advantage. These experiments are unnecessary for the narrower theoretical
claims above and have not been silently assumed.

Potential publication remains subject to external peer review and a final
date-specific priority check when a submission is prepared. The research
package is ready on its stated mathematical scope; it is not a claim of
journal acceptance, a completed paper, or exhaustive novelty certainty.
