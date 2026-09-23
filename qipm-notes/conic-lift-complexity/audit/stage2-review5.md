# Independent Stage 2 review 5

Reviewed `sections/03-products.tex`, `04-global-regularity.tex`, and
`05-support-orbits.tex`, their dependencies in Sections 1–2, the bibliography,
and the Stage 2 source dispositions. I did not consult other reviewer reports
or modify the manuscript.

## Assessment

**No major mathematical issue found.** The central statements have the right
quantifiers and the reconstructed proofs support them. The minor corrections
below should be made before closing this stage.

## Minor corrections

1. **State that dimension/capacity caps are integers.** In
   `04-global-regularity.tex:87`, replace “Fix c >= 1” by “Fix an integer
   c >= 1.” Make the same convention explicit for the dimension cap in
   `05-support-orbits.tex:349` and `:392` (and the cap used in the
   everywhere-differentiable proposition). These are discrete dimensions;
   the stated exact formulas are false if the cap is interpreted as an
   arbitrary real number. For example, c = 3/2 allows only Q3, while the
   formula for a single source with p = 3 would give three factors instead
   of the required four. This is an assumption clarification, not a gap
   in the intended integer-cap result.

2. **Exclude the zero denominator in the private-curvature statement.** In
   `03-products.tex:101–102`, specify an integer R >= 2. The surrounding
   dictionary setup makes the intended scope evident, but this separately
   stated theorem introduces B = delta(R - 1) and then divides by B.
   With only R = 1 factors the assumed full-row factorization cannot exist,
   but the displayed quotient should still have a defined domain.

3. **Correct one source-disposition overstatement.** The entry
   `audit/source-map.md:358` marks
   `joint-saturated-block-covering-rigidity` as subsumed by the Stage 2
   theorems. Its source theorem is about arbitrary proper cones and
   arbitrary compact contact manifolds P,D with a nondegenerate contact
   pairing; the normalized cone-base maps yield a covering by a product of
   spheres. Stage 2 proves the Lorentz version and a distinct symmetric-cone
   support-orbit result. It does not yet prove that general proper-cone
   theorem. Mark the entry partially included, with its general theorem
   deferred to Stage 4 alongside `saturated-block-submersion-rigidity`.
   This is a coverage-accounting correction; it does not require adding
   future-stage material now.

## Substantive proof checks

- The support-join identity uses orthogonality of positive elements and
  idempotent complements, so it does not silently rely on associative
  matrix multiplication. Sequential compression retains original-slice
  pure-row certificates; the text correctly asserts existence of selected
  high-rank aggregates, not a lower bound on every aggregate-objective
  certificate fiber.
- In the private-curvature argument, two-sided positivity eliminates the
  kernel-to-kernel derivative blocks. Cylindrical complementarity
  annihilates the other sources' support spaces, leaving the stated
  private quotient. The independently chosen complements are indeed
  jointly independent. The one-factor column-packing construction and
  its genuine rank-one row certificates check directly.
- Lorentz phase forms are positive semidefinite, and pointwise
  no-sharing does not imply a fixed assignment of labels. The proof
  correctly handles this by finitely many compact exact-label pieces,
  disjoint neighborhoods for each source, and a relative cup-product
  contradiction. All uses of a simply connected source occur at sphere
  dimension at least two.
- The two-ball joint-kernel construction has the correct normalization:
  the stereographic squared-distance identity and Q3 pairing each contain
  a factor one half. Its 2s - 1 count is correctly separated from the 2s
  full-labelled-row count. The norm-tree certificates telescope on the
  entire affine slice, including free internal primal variables.
- The global support-orbit theorem does not differentiate the polar
  contact correspondence. Its independent tangent spaces pair
  nondegenerately, and saturation gives constant complementary ranks.
  The support differential therefore yields an actual finite covering.
  The real Grassmannian homotopy argument, the complex/quaternionic
  intermediate homotopy, and the Cayley-plane middle cohomology give
  the stated classification.
- The real PSD3 exclusion is sound. A finite ray-positivity pattern
  eliminates all ray terms on U x U; an open projective rank-one sheet
  spans the symmetric matrices. Finite C1 affine selections glue because
  two distinct affine restrictions can share their tangent first jet at
  at most one sphere point. Finally, a nonnegative affine scalar function
  on a sphere cannot have two distinct zeros unless it is identically
  zero. This proves the kernel-map injectivity contradiction without a
  hidden determinant classification.
- I specifically checked the new **uniform all-EJA selected-rank
  frontier**. Under a putative saturated bound, every nonzero dual factor
  must have rank one, capacity exactly B, and complementary primal rank
  r - 1; all ray and unused dual factors vanish identically. The target
  primitive-orbit product cannot be covered by a sphere when there is
  more than one positive-dimensional factor. A lone real projective
  target is excluded by the affine-kernel lemma for every matrix order,
  not merely order three. The only surviving case is the matching spin
  factor. The fixed-tail Peirce construction attains the formula,
  including at zero coordinate groups and in the Albert algebra.
- In the smooth product theorem a proper face strictly lowers its
  parent's per-rank capacity, including Albert's rank-two faces (eight
  versus sixteen). Thus sequential compression cannot create a new
  spin exception at capacity B. The integer adaptive capacity envelope
  is a valid upper envelope obtained by balancing a concave quadratic;
  it is correctly described as a lower-bound tool, not an exact frontier.
- Resource statements consistently distinguish ambient dimension/rank
  from the parameter of a restricted barrier. The text makes no
  unsupported inference to a Newton-system or iteration lower bound.

## Literature and build

I independently checked the publisher abstract of Saint Raymond's
*Local inversion for differentiable functions and the Darboux property*,
Mathematika 49 (2002), 141–158,
https://doi.org/10.1112/S0025579300016132. It explicitly extends finite-
dimensional local inversion to everywhere differentiable functions with
nonvanishing Jacobian; the manuscript uses precisely that hypothesis.
The invocation is not the invalid assertion that differentiability and an
invertible derivative at only one point suffice.

Classical Jordan algebra and topology are identified as such. Stage 2
does not make an unqualified priority claim for its new formulas. The
introduction's present novelty discussion is limited to Stage 1; expanding
it to reflect the eventual full paper belongs to the already planned final
integration, rather than being a Stage 2 defect.

`make -C conic-lift-complexity` succeeded with the PDF already up to date.
The mathematical assessment above comes from checking proofs, not from
the successful build.
