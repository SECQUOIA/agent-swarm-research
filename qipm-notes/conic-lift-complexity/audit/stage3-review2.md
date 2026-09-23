# Stage 3 independent review 2

Reviewed `sections/06-restricted-barriers.tex` and
`sections/07-concrete-barriers.tex`, with the genuine-certificate,
semialgebraic-selection, and mixed-Peirce results in Section 1 checked as
dependencies. The main focus was the bounded-lift rigidity and exceptional
fiber arguments. No manuscript changes were made.

## Conclusion

**No major issue found.** The wide-cap theorem and the fixed-generic-label
refinement have complete arguments under their stated contextual cap
hypotheses. The explicitly excluded narrow-cap classification and intrinsic
norm-tree optimality problems are not gaps in the asserted results. Three
minor changes below would improve precision and notation.

## Independently reconstructed checks

1. **Compact homogenization and face budget.** Boundedness gives
   `T intersect K = {0}`. A negative-height cone point would combine with
   the Slater point to give a nonzero height-zero cone point; pointedness
   excludes cancellation. Thus the homogenized slice is exactly the cone
   over the original bounded slice. At a lifted boundary point, two-sided
   directions in its minimal-face span project into the line of the target
   Lorentz extreme ray. Counting the projection kernel then gives
   `codim E_X >= s`. This works with affine, rather than initially linear,
   output maps, because they homogenize with the height coordinate.

2. **The wide-cap numerical threshold.** In the Hermitian case the displayed
   face codimension is correct for real, complex, and quaternionic matrices.
   The bound `(B+1) nullity` also holds for Lorentz vertices and optional
   rays. The strict inequality needed for nullity `q-1` is equivalent to
   `q < B+2`, precisely the integer hypothesis `B >= q-1`. Hence every point
   of every boundary fiber has nullity `q`; this is stronger than a statement
   about only one selected point.

3. **Singleton fibers.** A nontrivial compact affine fiber has a maximal chord
   through a relative-interior point. Within its minimal cone face, a finite
   endpoint must leave the relative interior, because otherwise that same
   affine direction remains feasible for a longer segment. It therefore
   loses rank. This proves the primal singleton claim under constant nullity.
   The dual singleton argument on the generic set is the same argument with
   the rank inequality reversed: its maximal rank is `q`, but every member
   already has rank `q`. Slater normalization provides the needed dual
   compactness.

4. **Generic saturation and topology.** Equality in the mixed-Peirce chain
   forces `q_i=1`, cap-attaining order or dimension, primal corank one, and
   no inactive singular blocks. Constant total nullity lets a generic label
   pattern persist to limits and prevents two distinct patterns from having
   intersecting closures. Kernel/support lines determine the same product
   face. A genuine certificate annihilating that face distinguishes the
   projected sphere point, giving the claimed injection. Invariance of
   domain then contradicts intermediate mod-two cohomology of a product of
   `q >= 2` projective spaces or spheres. No factor-count assumption enters.

5. **Certificate collapse and its dimension.** A finite positive average of
   certificate tuples realizes the sum of their ranges, simultaneously in
   all blocks. Complementarity bounds this total rank by `q`. On a smooth
   stratum of `Z`, independent differentiation of the sphere slack supplies
   the positive definite induced tangent metric, while the certificate rank
   bound supplies at most `B(q-1)` channels. Semialgebraic closure preserves
   this dimension bound.

6. **The new fixed-label claim.** Outside `Z`, the averaged rank-`q`
   certificate forces all primal tuples to have nullity `q`, so the primal
   fiber is unique. Compactness then forces every nearby sequence of generic
   primal tuples to approach this unique point. Its inactive blocks are
   positive definite, so nearby generic tuples cannot acquire another
   active label. This proves local constancy at every point outside `Z`,
   including nongeneric points. The complement of the semialgebraic closure
   of `Z` is connected when `B >= 2`; all nonempty open generic pattern
   regions meet it. The conclusion follows. The Lorentz replacement by
   the smallest support face of the full certificate fiber preserves each
   step. The proof correctly excludes `B=1` from the connected-complement
   conclusion.

7. **Incidence topology.** The incidence space is closed and bounded, its
   projection is a continuous surjection of compact metrizable spaces, and
   each fiber is the product of two nonempty compact convex sets. Thus the
   acyclic-fiber cohomology theorem applies. I checked the standard theorem
   formulation against Andrew McLennan, *A Geometric Vietoris-Begle
   Theorem*, Section 4, https://arxiv.org/html/1909.11347. The manuscript
   correctly stops at a cohomology isomorphism and does not invent a global
   extension or degree for the generic kernel map.

8. **Other Section 6 checks.** Boundary determinant order is correctly
   quantified over every completion. The recession argument controls scaled
   first and second derivatives, including the mixed derivative, rather
   than relying on a value-level remainder. One-channel rigidity uses
   `nu < 2`, which is sufficient for integer nullity at most one. The
   sequential product argument works with compressed whole certificate
   fibers and retains their compactness, convexity, closed graph, and
   nonzero genuine row identity. The rotated example correctly separates
   minimum primal nullity, maximum certificate rank, and standard parameter.

9. **Section 7 scan.** The root-leverage identity, the root-leaf limiting
   direction, and the all-internal-root Schur bound are consistent. The
   polyhedral section really has `L` independent active facets at the stated
   vertex. Grouped box sections supply the arbitrary-barrier lower bound.
   In bounded-fiber projection, closed convexity and bounded fibers imply
   bounded inverse images of bounded projected sets through the recession
   argument given; this justifies attainment and boundary divergence of the
   partial minimum. Column packing does not require orthogonal columns or
   `b <= p`. Its shear calculation and product-of-balls projection support
   the asserted parameter `b` over all three associative fields.

## Minor findings and precise fixes

1. **Restate the cap in the collapse proposition.** At Section 6, lines
   339–340 of the reviewed version, “a bounded Hermitian lift in the divisible
   case” inherits a fixed field, maximum order `R`, and `B=a(R-1)` from the
   preceding theorem. Restate these in the proposition's opening sentence.
   Without that context, `B` and “full-order” are under-specified. The
   Lorentz paragraph should likewise identify `B=d-2` for its dimension cap.
   This is a statement-clarity fix, not a failure of the proof.

2. **Qualify the classification status locally.** At Section 6, lines
   326–327, change “the only unsettled single-ball cases” to “the single-ball
   cases not resolved by the preceding results.” The exact interval and
   range are proved, but the former wording can be read as a literature-wide
   assertion that no other result settles any such case. No such priority or
   exhaustive literature assertion is needed here.

3. **Use bilinear Hessian notation.** At Section 7, line 381, replace
   `D^2F[(H,K)]^2` by `D^2F[(H,K),(H,K)]`. The current notation looks like
   the square of a second derivative rather than its evaluation on a
   repeated direction. The numerical expression itself is correct.

## Scope of this conclusion

This is a correctness review of the Stage 3 changes, not a certification of
literature-wide originality. The manuscript's explicit distinctions between
standard and arbitrary barriers, selected and selection-free results, and
proved and unresolved parameter ranges are necessary and should be retained.
