# Stage 1 independent review — reviewer 3

## Decision

No major issues found in this inventory-and-planning stage. The scaffold makes no unreviewed theorem claims. The proposed scope covers the substantive conditioning developments in original Sections 3–4, the later degenerate-LP endpoint correction, and the formulation/coordinate limitations. Excluding full oracle-complexity and path-length packages is justified by the chosen mathematical object.

The strengthened all-barrier theorem is a promising central contribution, conditional on the Stage 2 proofs and qualified literature positioning. It should supersede the weaker canonical-only rate-optimality narrative if established. Neither the classical containment tools nor the unique degenerate LP limiting-Hessian corollary should be promoted as novel.

## MINOR 1 — distinguish the face tangent from a finite-gap spectral subspace

Location: `development/scope-and-literature.md`, inventory row “LP two spectral clusters” (line 31).

“Identify the weak subspace with the tangent space of the optimal face” is ambiguous and can be read as an exact equality for the weak spectral eigenspace at positive gap. What is exactly equal to the face tangent, in reduced coordinates, is `ker(P_N Z)`, the kernel of the leading hard block. The low-eigenvalue invariant subspace of the full Hessian need only approach that kernel. Original Section 4 splits `H_mu=H_mu,N+H_mu,B`; the bounded second term generally couples the two fixed subspaces. The later proposed projector-angle refinement already recognizes this distinction for arbitrary barriers, but the inventory wording should also preserve it for the canonical barrier.

Action: replace the instruction with “identify the kernel of the leading hard block with the face tangent; establish convergence/angle bounds for the low-eigenvalue spectral subspace.” This is a precision correction to the plan, not a finding that the intended projector theorem is false.

## MINOR 2 — make equal-gap parameter domains explicit

Location: central proposed contribution (line 11), and Stage 2 setup obligations.

An arbitrary fixed barrier need not have a positive-parameter central point at every feasible objective gap. With the convention `x_F(t)=argmin(F+t c)`, `t>0`, the gap decreases from the barrier analytic-center gap to zero. Different barriers have different starting gaps. An equal-gap comparison therefore needs the common interval of attained central gaps, or an explicitly sufficiently small tail. The asymptotic Theta law is naturally a tail statement, but this domain is not yet recorded alongside the proposed finite-gap Loewner comparison.

Action: add a short Stage 2 obligation to establish central-path existence, strict monotonicity of its primal gap, and its range; formulate pairwise comparisons on the common attained gap interval. Under compactness, a nonconstant objective, and a positive definite restricted Hessian, differentiation gives `d g_F(t)/dt = -c_V^T H_F(t)^{-1}c_V < 0`, so this appears straightforward.

## Independent primary-source check and novelty boundary

I inspected Xiong–Freund's author-posted July 15, 2024 primary PDF, Section 5.1, Fact 5.2 and Remark 5.1 (printed pages 32–33):

<https://optimization-online.org/wp-content/uploads/2024/06/arXiv_0715.pdf>

Fact 5.2 explicitly gives the central-gap sublevel outer ellipsoid with radius `theta_F+2 sqrt(theta_F)`. Remark 5.1 uses its diameter and the inner ellipsoid radius to bound primal–dual level-set geometry by extreme Hessian eigenvalues. This confirms the inventory's characterization of direct prior overlap. These statements use the primal–dual feasible set and gap, whereas the proposed theorem uses a reduced primal Hessian and primal objective gap. They do not explicitly state the proposed equal-primal-gap cross-barrier Loewner comparison or its two-sided diameter/gap law. However, the elementary geometric closeness of the arguments means the final paper should call its novelty a precise consequence/refinement of standard containment and existing geometric analysis, not a newly discovered general connection between sublevel geometry and Hessians.

I also inspected the original conditioning/spectral setup and the active degenerate-LP note. The note's identity `mu^2 H_red(mu)=W^T Diag(s(mu)^2)W` and uniqueness argument make its relationship to classical endpoint convergence transparent. Treating it as a useful classical corollary is the right originality boundary.

The proposed difference-body route has no obvious mathematical obstruction at this planning stage: the objective-decreasing half of a Dikin ellipsoid can be used to obtain a difference-body inner inclusion; asymmetric containment supplies the outer inclusion. The authors must still check all constants, closed/open set boundaries, and the homothety argument in Stage 2. This observation is not a substitute for the requested theorem review.
