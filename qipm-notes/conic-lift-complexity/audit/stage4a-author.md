# Stage 4A author report

Stage status: authored and integrated; ready for the mandatory five independent reviews.

## Structure and verification

The stage develops the deferred global topology and support-rigidity material.
Three bounded author helpers independently reconstruct general-cone topology,
all-EJA product-orbit classification, and restricted kernel obstructions. The
stage author independently develops the compact full-fiber theorem, checks the
integrated proofs, and owns manuscript integration and bibliography.

`08d-full-fibers.tex` proves the mandatory heterogeneous product theorem from
`fiberwise-nullity-selection-free-rigidity`, including its accessibility
corollary. Constant total nullity is used on every boundary-fiber tuple, not
only a selected sheet. The proof checks connectedness of the compact full
preimage, constant individual ranks, support descent through a compact quotient,
the exact EJA capacity equality, injectivity using genuine full rows, and the
cohomology indecomposable multiset. The single-ball statement is its strict-cap
corollary. This covers all of that source, whose earlier single-ball restricted
barrier discussion alone did not cover its Sections 5–6.

## Literature check by stage author

The primary HTML of Aubrun–La Piana–Müller-Hermes,
*Factorization through Lorentz cones*, arXiv:2606.27825v1 (26 June 2026), was
inspected, specifically the definition in Section 1 and Theorem 1. Its self-pair
classification quantifies over every positive linear map. It is not the same
statement as capacity equality for one globally regular nonlinear full-slack
factorization. The complete author metadata and arXiv identifier are included
under `ALM2026Lorentz`.

## Validation

The completed integrated build passes in the qipm environment and produces
a 55-page draft. The final log contains no undefined references or citations,
no warnings, and no overfull boxes. Build output is in `stage4a-build.log`.
The first three new sections retain the central global results; abstract
splitting/individual submersions and restricted kernels form appendices.
All mathematical author fragments were independently read and checked by the
stage author before integration. These checks do not replace the required
five independent formal reviews.

## Source dispositions

- `global-smooth-saturation-topology`: the general compact-contact covering
  theorem includes the exact globally regular cone conclusion; its independent
  abstract tangent-splitting, Euler, clutching, and frame implications are
  retained in the topology appendix. The prior symmetric single-sphere
  support-orbit part is subsumed by Section 5 and the new product theorem.
- `rank-two-curvature-summand-topology`: the rank-one/rank-two frame budget
  is included in the abstract splitting proposition. Its numerical cone
  consequences are subsumed by the stronger joint-covering theorem under
  actual globally regular factorization hypotheses.
- `steenrod-effective-curvature-capacity`: subset-sum restriction,
  Radon–Hurwitz effective cap, near-full summand, exceptional dimensions,
  and unstable clutching condition retained. The proof supplies the classical
  plane-field implication directly; it does not assert that the original
  plane field itself is trivial.
- `saturated-factor-submersion-obstruction`: normalized-base submersion
  mechanism proved in the general covering theorem and applied separately
  to one everywhere saturated channel in the topology appendix.
- `saturated-block-submersion-rigidity`: independent reconstruction subsumed
  by the same complete argument. The primal and polar charts remain
  independent, and no derivative of supporting polarity is assumed.
- `joint-saturated-block-covering-rigidity`: verified and included for
  arbitrary compact contact manifolds, not just convex-body spheres. The
  product capacity multiset is retained without an unjustified product
  splitting assertion.
- `sphere-submersion-curvature-gap`: strict sphere gap and exact general-cone
  smooth ball resources follow from the stronger joint theorem. The
  individual Hopf dimension obstruction remains in the topology appendix.
- `product-sphere-submersion-dimension-rigidity`: verified and retained as
  the necessary alternatives r=q or q=2r−1 with even r. The proof handles
  r=2 directly by a Sullivan fiber model; no sufficiency for the other
  candidate dimensions or sphere-total-space theorem on a product is claimed.
- `sphere-submersions-balanced-real-grassmannians`: verified and retained,
  including positive-dimensional fibers, real order-five quadric exclusion,
  zero-dimensional covers, and low-order cases.
- `hermitian-product-ball-capacity-rigidity`: subsumed by the all-EJA
  product equality theorem; no-ray injectivity and fixed-field equality
  profiles retained explicitly.
- `hermitian-product-ball-active-ray-covering`: verified and included;
  keeps finite covers rather than asserting injectivity in the presence
  of scalar rays, and retains circle/fundamental-group cases.
- `real-low-order-cylinder-exclusion-product-balls`: verified and included
  with the PSD4 Hodge/ruling argument and the PSD3 row-isolation reduction
  to the fully proved one-ball affine-kernel obstruction.
- `symmetric-cone-product-ball-active-ray-saturation`: verified and included
  for every simple EJA, including Albert, scalar rays, mixed families,
  the exact cone profile and vanishing of unrelated dual rows.
- `projective-contact-q3-embedding-bound`: verified and included in the
  restricted-kernel appendix, including nowhere-zero scope, phase embedding,
  inverse Stiefel–Whitney product bound, sharp RP2 count, and explicit upper
  construction. Full-cone SOC nonrepresentability remains distinct.
- `product-q3-near-saturation-boundaries`: local/finite-sample saturation,
  partition count, functional inertia, overlapping positive block-additive
  model, and all-source-dependent channel all retained. Paired optimality
  is not extended to arbitrary common-scale sums or unrestricted factors.
- `q1-curvature-flat-residual-nullity`: verified and strengthened to actual
  column ranks on arbitrary index sets without continuity. Retains antipodal
  and squared-kernel corollaries, exact ordinary ranks, factor-count penalty,
  and standard-slice implication. The older persistent-saturation extraction
  bound b+j is subsumed by the earlier full-row theorem giving 2b, because
  j≤b; its special canonical positive splitting is retained as an example.
- `fiberwise-nullity-selection-free-rigidity`: completely included as the
  compact full-fiber constant-nullity theorem and every-tuple accessibility
  corollary, including the heterogeneous exact profile. The source's
  unresolved unconditional barrier inference is not promoted to a theorem.

Related routing clarification: `psd-support-grassmannian-submersion` is
mathematically subsumed by the earlier orbit covering and the present
individual-submersion discussion. Its concrete cap-R and real-order≤3
resource ledgers have been flagged to root for explicit final ledger
integration; this audit does not silently claim those displayed formulas
have already been written.

## Completed files and integration

- `sections/08a-general-topology.tex`: general compact-contact joint covering,
  arbitrary proper-cone smooth ball frontier, reusable proper phase-domain lemma.
- `sections/08b-product-orbits.tex`: all-EJA full-row equality classification.
- `sections/08d-full-fibers.tex`: compact full-fiber constant-nullity rigidity
  and contact accessibility.
- `sections/08e-topology-refinements.tex`: classical splitting/submersion
  refinements and their precise connection to saturated channels.
- `sections/08c-restricted-kernels.tex`: projective embeddings, local and
  restricted near-saturation constructions, strengthened Rado nullity criterion.
- `main.tex`: includes central sections followed by a single appendix marker.
  Later main sections should be inserted before that marker.
- `bibliography.bib`: eleven new, reconciled primary literature entries.

Detailed verification status and inspected primary-source locations are in
`stage4a-topology.md`, `stage4a-product-orbits.md`, and
`stage4a-restricted-kernels.md`. No workbench notes, literature packages,
existing companion manuscripts, or the pre-existing formal directory changed.

The author identified no invalidating mathematical defect. The evidence
supports precisely the stated conditional classifications and restricted-model
counts; the wider unresolved barrier brackets and unrestricted product-kernel
count are still explicitly distinguished. No universal absence-of-prior-work
claim is inferred from a targeted literature search.
