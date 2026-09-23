# Stage 3 independent review 5

Reviewed Sections 6 and 7 in full, their dependencies in Sections 1 and 5,
the Stage 3 source inventory and author reports, and targeted original
workbench notes. The author reports were used to locate claims, not as
evidence for their proofs. No manuscript files were changed.

## Verdict

No major mathematical error or gap found in the asserted Stage 3 theorems.
The open bounded narrow-cap interval and the unknown intrinsic optimum of
general norm-tree domains are honestly delimited classification questions;
neither is a missing premise in a theorem currently asserted.

There is a substantive source-coverage omission, described below. The root
has assessed it and selected explicit routing to Stage 4A. Thus it is a
minor Stage 3 routing correction, not a major issue in this stage's
asserted mathematics. The current ledger should not call that source fully
incorporated. All four findings below are minor corrections with this
accepted routing; there are no major issues requiring mathematical revision.

## Findings requiring disposition

1. **Coverage: the heterogeneous constant-nullity theorem is missing.**
   `fiberwise-nullity-selection-free-rigidity.md`, Sections 5 and 6, contains
   two developments not covered by the single-ball remark at
   `06-restricted-barriers.tex:318`. For a compact full preimage of the
   simultaneous extreme stratum, all symmetric factors of dimension at
   most d, total tangent dimension n=L(d-2), and constant total nullity L,
   the source tangent-dimension multiset must consist of L copies of d-2.
   This has no global C1-selection assumption. The source also gives a
   corollary replacing constant nullity by a standard-parameter upper bound
   together with accessibility of **every** boundary tuple by regular
   contact sheets. Stage 2's globally smooth results do not subsume these
   hypotheses. The author disposition at lines 88–89 currently omits them.
   Concrete fix: add the product theorem and accessibility corollary, or
   explicitly route them to the Stage 4 general-dictionary topology author
   and change the Stage 3 completion ledger accordingly. This is a material
   completeness issue for the final paper, not a counterexample to the
   existing theorems. A formal all-EJA product statement should retain the
   compactness and all-fiber-point hypotheses.

2. **Minor coverage: escaping primal selections are not represented.**
   `arbitrary-affine-psd-ball-barrier-cap.md`, Section 5, gives a strictly
   feasible exact disk lift with no locally bounded primal selection at
   one boundary point. With delta=1-x1 its three blocks are
   `[[1+x1,x2],[x2,delta]]`, `[[delta,x2],[x2,u]]`, and
   `[[delta,u],[u,z-1]]`. Along the circle approaching (1,0), every feasible
   completion has u>=2-delta and z>=1+(2-delta)^2/delta. This is independent
   of the compact rotated-perspective counterexample: it explains why
   compact projected bodies and relative Slater do not justify compact
   primal choices. Add a short example or an explicit later-stage route.
   The recession theorem already handles these lifts correctly, so this
   omission does not affect its validity.

3. **Minor prior-work attribution for the conic facet bound.**
   The intrinsic norm-tree proof correctly gives the homogeneous lower
   bound L+1. The source note identifies the general polyhedral-cone
   extra-unit bound as Hildebrand, Theorem 6.1, but the manuscript presently
   cites only NN's polytope bound. Add a sentence attributing the conic
   facet principle to Hildebrand while identifying the tree polysection as
   the application. I independently checked the original paper's Section 6:
   [primary preprint](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf).
   The journal DOI is 10.1007/s10107-012-0576-1. The proof here is valid;
   this is a literature-positioning correction, not a need to replace it.

4. **Minor source-disposition wording for the local H3(R) pencil.**
   The Stage 3 audit says its local-versus-global caution is incorporated,
   but Section 5 supplies the stronger finite-affine-gluing exclusion
   without stating the local counterexample. It is reasonable to omit a
   superseded proof-route counterexample, but say that explicitly in the
   source map rather than imply that its example appears. Alternatively,
   one short remark can display the pencil with determinant
   `(1-x3)(1-||x||^2)` and explain that local constant rank does not yield
   global constant rank. The stronger global proof itself is sound.

The root accepted inclusion of both explicit examples in findings 2 and 4
and explicit Stage 4A routing of finding 1. Finding 3 remains a recommended
minor attribution correction for the root's assessment and the separate
correction author.

## Mathematical checks supporting the verdict

- Boundary orders are proved at every feasible tuple after face reduction.
  The recession argument supplies the necessary scaled first and second
  derivative limits, including the vanishing mixed term; an O(1) function
  remainder is not silently differentiated.
- The one-channel contradiction uses parameter below two. Compact normalized
  full certificate fibers, their convexity, and the whole-slice identity
  justify singleton rays and the injective primitive-ray map. In sequential
  compression, using images of original fibers preserves compactness and
  the genuine cylinder identities needed for the same argument.
- The bounded homogenization height in the face-codimension lemma is
  positive on nonzero cone points. The codimension inequality and
  `(q-1)(B+1)<qB+1` give exactly the claimed wide-cap range. The endpoint
  argument forcing singleton compact fibers is valid because an endpoint
  remaining in the relative interior of the same cone face would extend
  the affine chord.
- In the range-collapse proposition, a full-rank positive average spans
  the full certificate range. The stratum curvature argument yields
  codimension at least B. Outside the collapse set, compactness and
  singleton primal fibers give local stability of generic labels. Passing
  to the complement of the semialgebraic closure is justified, and its
  connectedness when B>=2 yields the fixed-label conclusion. This does not
  extend the kernel map across collapsed fibers, and the manuscript does
  not claim it does.
- The incidence fiber is the whole Cartesian product of primal and genuine
  certificate fibers, because every such pair is complementary. Thus the
  Vietoris–Begle application is appropriate, with the stated limited use.
- For the root-incidence law, the root-leaf test direction has zero second
  derivative of the Lorentz determinant, so the displayed Hessian formula
  is correct. In the all-internal case the child Dikin bounds and Schur
  complement comparison have the right direction. The bound on Z implies
  the claimed Schur lower bound. Both limits establish sharpness.
- The tree polysection has L free beta coordinates, meets the interior,
  and has exactly L independent active facets at beta=0. The homogeneous
  extension explicitly retains its homogeneity hypothesis. No optimality
  among arbitrary root-fixed barriers is claimed.
- The bounded-fiber projection lemma proves local uniform boundedness
  using a vertical recession direction, rather than assuming it. This
  ensures both minimizer existence and barrier divergence at projected
  finite boundary points. The third derivative formula follows from
  stationarity and Hessian orthogonality. I independently checked
  [Chares, Theorem 5.2.1](https://perso.uclouvain.be/francois.glineur/files/theses/Chares-PhD-thesis-2007.pdf),
  which is an appropriate attribution for the classical calculus.
- Grouped box sections and bounded-fiber column packing correctly bound
  every barrier, including coupled barriers. Column packing does not rely
  on orthogonal columns and remains valid when b exceeds p. The repeated
  block example correctly distinguishes standard determinant multiplicity
  from intrinsic barrier complexity.

## Integration notes

The full paper must eventually explain the existing central-path-paper
overlap in the manuscript itself, especially the root-incidence formula
and grouped/packed constructions. The current author report identifies
this accurately, and the source map assigns the final novelty synthesis
to Stage 5. I do not treat the unfinished introductory synthesis as a
Stage 3 mathematical defect. The current LaTeX log has no undefined
references or citations, bad-box warnings, or other warning lines.
