# Stage 4B second independent review 2

Reviewer: `/root/stage4b_round2_review2`.

## Scope and decision

I personally read every line of the five new sections, 09a through 09e,
and the revised assessment and correction record. I also read the
joint-cover theorem and proper-phase-domain lemma in 08a, which are the
main dependencies of the revised global argument. I did not read the
other second-round review reports and did not delegate this review.

**No major or minor issue identified.** The changes correctly strengthen
the sharing bounds, and the strengthened statements are consistent with
the other results in this stage. No manuscript correction is requested.

## Verification of the substantive revision

The common-annihilator argument in 09b and 09e is valid. At a simultaneous
contact, fixing one active, nonzero dual vector gives a nonnegative
function of all primal source variables with value zero. Its first
derivative vanishes in every primal tangent direction. Consequently the
primal ray and all rank-detecting derivative spaces lie in the same
hyperplane. The cross-contact derivative identities make their sum direct:
pairing a proposed dependence with the derivative of dual row a kills
the primal ray and every other source's selected space, and is injective
on the selected space for row a. This proves

    1 + sum_a t_i^a <= m_i - 1.

The argument requires neither second derivatives nor positivity or
symmetry of the individual mixed matrices. It applies to the rectangular
spectral mixed pairing even though that full pairing has a kernel.
Vanishing primal or dual factors cannot be active, since two-sided
derivatives of pointed-cone-valued maps vanish at the vertex.

For the product-ball premium, the aggregate dual maps are C1 maps into
the dual cones and give exactly the joint kernel stated in 09b. Both
source manifolds are the compact connected product of k p-spheres;
their contact map is the identity, and the independent mixed pairing
is the nondegenerate product metric. Thus the hypotheses of the 08a
joint-cover theorem hold when R = kp. As p >= 2, the multiset conclusion
is applicable and forces k capacities equal to p. The strict cap
c < p excludes equality. The resulting integer improvement R >= kp+1
is justified and does not assume that the individual maps split by source.

The separate face-weighted budgets also remain valid. In the capacity
argument, activity is open, the loci with exactly the minimum capacity
are closed, and their finitely many exact-label pieces are compact.
The normalized dual maps are defined on neighborhoods of the projected
pieces, since a corresponding nearby nonzero primal contact factor
forces their dual factors to remain on the nonzero boundary. The
derivative injection follows from the full mixed identity and radial
annihilation. The proper-phase-domain lemma then supplies the required
vanishing of each source top class. The analogous minimum-count
argument is needed only when c divides p, exactly as the proof states.

The arithmetic combination is correct: the face budgets imply
R >= ceil(k tau/f) and L >= ceil(k h/f), the aggregate argument implies
R >= K, and R <= cL gives the additional count ceiling. Therefore the
displayed R_*, L_*, dimension lower bound, and ambient barrier lower
bound follow together. At f = 1 they give R_* = k tau and L_* = kh,
including both the strict-cap and direct-cone cases. The Lorentz
construction therefore still supplies the stated exact ray-exposed
frontier. The text appropriately asserts no corresponding exact
frontier for general f > 1.

In 09e, summing the revised local bound gives the stated undivided
capacity inequality. Combining this with the independent incidence
budget yields precisely the two factor-count ceilings shown there.
No global spectral topological premium is inferred from this local
argument.

## Checks of the remaining sections

- **09a:** The whole-row affine-function ranks, contact-cylinder face
  ranks, and shared-homogenization exposed-face calculation agree. The
  minimum-dimension rigidity proof handles affine output and free-variable
  reduction; its slack-factorization proof obtains both cone inclusions.
  The connected-extreme-set gap is distinguished correctly from the
  stronger normalized-product-base bound. The recession-level criterion
  uses closedness, line-freeness, and compact projection in the required
  places. The simple-vertex barrier transfer and the escaping-fiber
  obstruction have the stated limited scope.
- **09b:** Summing the face inequalities gives the displayed shared-block
  tradeoff. The shared-square cone has the claimed face dimensions and
  function ranks. Its completion-barrier parameter and the grouped
  scalar ledger are consistent with 09e and with the whole-row comparison.
- **09c:** The two-equation minimal-face criterion gives exactly the
  one- and two-block extreme points described. The classical, spin, and
  Albert height constructions provide the paths needed for connectivity,
  including the disconnected real rank-two zero set. Frame-diagonal
  sections give the orthant and simplex lower bounds, and the restricted
  gradient-norm calculation gives the claimed upper bounds. Essentiality,
  strict-cap dimension attainment, and the alternate moment construction
  are consistent. I also independently checked the derivatives in the
  failed-cancellation example: they are 13/4 and 25 as stated.
- **09d:** The local curved patches have the stated positive Hessians;
  the tree and added-zero-coordinate constructions have full Slater
  faces and the asserted counts. The global theorem uses independent
  primal/polar C1 charts, so coordinate-zero regularity does not invalidate
  its mixed pairing. The Young factors are dual feasible and give genuine
  affine-slice certificates. The two-dimensional exception separates the
  nonsmooth-ray count from the Lorentz zero-curvature obstruction. The
  generalized power-cone section has the required dimension and strictly
  positive second fundamental form. The revised integer cap conventions
  are explicit and consistent.
- **09e:** The spectral rank count includes the imaginary scalar channel
  over complex and quaternionic fields. Whole-row contact codimensions
  and shared cone faces agree with the remaining contraction rectangle.
  The ambient shared-spectral lower certificate applies to arbitrary
  barriers, and the restricted gradient norm gives the slice parameter.
  The completion cone is closed, its maximum-determinant barrier and
  diagonal-section lower bound agree, and the clique-separator and
  block-star formulas have the correct dimensions and parameters. The
  rank-one star certificate is independent of the phase representation.
  The equality of the reduced Hessians and KKT systems is stated only
  after the specified eliminations and common retained coordinates.

I checked the existing final LaTeX and bibliography logs; neither contains
warnings, unresolved references/citations, duplicate-label warnings, or
overfull/underfull boxes. I did not rebuild or edit the manuscript. This
review found no new literature question requiring another external search;
the revisions under review are proved internally and preserve the
explicitly qualified attribution of the classical constructions.
