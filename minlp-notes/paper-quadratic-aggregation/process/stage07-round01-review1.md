# Stage 7 independent review 1

Reviewer scope: scientific synthesis, especially the new two-point proof for every r >= 2, the abstract/introduction, and consistency with the stated formal coverage. Read the stage 7 author report; main.tex; Sections 00, 01, 05, 06, 09, and 10; the statements and opening proofs in Sections 07 and 08; and the actual portable `Formal/InfiniteAggregation/HullCore.lean` construction. No manuscript edits were made.

## Verdict

**No major or minor issues identified in the reviewed scope.** The new strict hull proof is complete, and the synthesis accurately separates certificate existence, exact description cardinality, and approximation. This verdict is a substantive review of the specified scope, not a claim to have independently replayed every formal module or rechecked all earlier-stage proofs.

## Mathematical checks

1. In the new proof of Theorem `thm:ball-hulls`, p and q are strictly positive, so a and b and every displayed denominator are well-defined. A unit vector perpendicular to b*u-a*v exists for r=2 as well as higher dimensions, including when that vector vanishes. The perpendicularity identity gives both u.e=a*gamma and v.e=b*gamma. Thus all three expansions use the same scalar 2*gamma*t+t^2. The assumed hull inequality supplies k strictly between max(0,(1/2-h)/(ab)) and 1. Its positivity makes the two roots nonzero with opposite signs. At both roots the squared norms remain strictly below one and the inner product is strictly above one half. The stated positive weights sum to one and cancel t exactly. This proves actual membership in the ordinary convex hull, without a closure argument or use of the BDS full-hull theorem. The mathematical construction agrees with the inspected Lean interface and proof.

2. Necessity is not circular: the good-cone proposition precedes the hull formula and proves convex validity directly. Its coordinate multipliers give positive p and q, and the point-dependent multiplier (q,p,2*sqrt(pq)) belongs to the previously established cone. Its value is exactly 2*sqrt(pq)*(1/2-h-sqrt(pq)).

3. The subsequent all-good intersection proof remains valid with the new ordering. The displayed decomposition of a multiplier handles lambda_3=0 separately and otherwise has positive diagonal weights and a nonempty interval for tau. The strict scalar infimum is attained when p,q>0. The separate dense countable weak family uses continuity and endpoint infima, so it does not imply the false analogous strict claim.

4. The finite lifts follow from the Schur complement. The closure proof mixes with a positive definite lift at scalar 1/2 and uses openness of positive definiteness to adjust that scalar when needed. This avoids assuming projection preserves closedness. Compactness of T_r justifies closing its convex hull in the subsequent equality.

5. The arbitrary-quadratic cardinality proof treats strict and weak descriptions differently for a valid reason. A nonzero restricted quadratic has finitely many zeros on the compact analytic quartic arc: the nonsquare rational function and primitive irreducible quartic argument supply the needed nonidentity. Strict validity at the planar origin rules out an identically zero restriction. At a strict boundary point continuity gives nonpositivity for every row, and exclusion forces equality in one row. In the finite weak case simultaneous strict slack would include an infeasible neighborhood. These arguments support exactly the original-variable conjunction claims made in the introduction and abstract, with no implication against the finite lifted descriptions.

## Synthesis and literature checks

The abstract's proper-hull certificate, sharp Gram threshold, four-variable example, cardinality distinctions, and strict PDLC transfer match the theorem statements. The introduction distinguishes signed PDLC coefficients from nonnegative aggregation multipliers, and good aggregations from globally convex ones. The dimensional qualifiers and ordinary/closed hull distinctions are retained. The approximation claim is about the specified good-aggregation cone, with dimension-independent constants; the paper does not claim an unprecedented inverse-square exponent or an optimization-iteration lower bound.

Independently reopened the primary versioned sources:

- [Blekherman--Dey--Sun, arXiv:2210.01722v2](https://arxiv.org/html/2210.01722v2), with the local PDF text as a second view. Conjectures 3.1, 3.2, and 3.3 match the introduction's respective affirmative, negative, and affirmative resolutions. The version qualification is necessary and present.
- [Blekherman--Dunbar, arXiv:2405.18282v1](https://arxiv.org/html/2405.18282v1). The synthesis credits the existing four-bound and describes the contribution as its transfer to unrestricted strict systems. It does not claim invention of the number four or priority over the acknowledged dissertation statement.

The novelty paragraph uses a qualified knowledge claim, and nearby text specifically credits antecedents in fidelity, quadratic matrix programming, infinite aggregation, and approximation. The current main formal overview expressly distinguishes the stronger paper lower constant from the formal one, the smaller paper SDP test from the formal signed-coordinate test, and the nonformal results from verified results. Its description of the r>=2 two-point proof agrees with the actual formal source inspected here.

No additional mathematical development or correction is requested by this review.
