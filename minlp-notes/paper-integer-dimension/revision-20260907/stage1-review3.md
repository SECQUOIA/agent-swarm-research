# Stage 1 independent review 3

Reviewed the frozen introduction and bibliography in `reviews/revision-stage1-round1/source`, their changes relative to Git HEAD, and the author and literature reports `revision-20260907/stage1-author.md` and `stage1-literature.md`. No other reviewer report was consulted. No manuscript changes were made.

## Assessment

No major issue identified in the stage 1 changes. The introduction now states a precise approximation model, distinguishes minimum integer count from explicit rational description length, explains the importance of the joint quadratic invariant, and limits its explicit priority assertion to the stated quadratic characterization. The scalar and vector contribution descriptions correspond to their theorem statements. The attribution of chord estimates, adaptive approximation, shared SOS2 encodings, and logarithmic formulation tools is substantially clearer than before.

I checked the quoted scalar chord lemma and its proof, the dense scalar compiler statement, the box/facet curvature-rank theorem and proof, the finite covariance and rational construction statements, the quadratic precision statement, and the stated separation and hardness results to assess the introduction's scope. This is a framing and prior-work review, not a completed verification of all technical proofs in those later sections.

## Valid minor finding

### M1. Complete the LinA comparison in the overlapping convex setting and identify the unit of oracle complexity

Locator: `sections/00-introduction.tex:241–246` in the frozen source.

The statement that LinA's general corridor model permits discontinuous PWL functions is true. However, this comparison immediately follows discussion of convex scalar functions and the convex-corridor routine, where LinA explicitly gives a continuous solution. Remark 3 says that the greedy algorithm solves the continuous version for convex corridors. Omitting this qualification can leave the reader with an inaccurate impression that continuity separates the present convex scalar result from LinA. The substantive distinction here is comparison against arbitrary convex integer lifts and compilation of an implicit partition with polynomial total rational encoding.

The same passage calls the routine's oracle complexity logarithmic without saying that this is the cost of computing one maximal linear segment. Algorithm 2 and the paragraph preceding it give that bound for the maximal-segment subproblem; an explicit complete partition still has to generate its segments. State “per maximal segment” so this paragraph supports, rather than blurs, the existence/oracle/bit-complexity distinction developed elsewhere.

Evidence independently read and checked against the original PDF:

- `[[codsi2025-lina-a-faster-approach-to]] p.10`: Remark 3, printed page 274, gives continuity in the convex-corridor case.
- `[[codsi2025-lina-a-faster-approach-to]] p.12`: Algorithm 2 and preceding paragraph, printed page 276, give the oracle bound for a maximal linear piece.
- `[[codsi2025-lina-a-faster-approach-to]] p.6`: Table 1 includes approximation, overestimation, and underestimation corridors, so bands for continuous convex functions are within the relevant prior approximation setting.
- Publisher metadata and abstract were independently checked at https://link.springer.com/article/10.1007/s12532-024-00274-8.

Suggested repair: say that LinA computes successive maximal segments, with logarithmic precision-dependent oracle cost per maximal segment, and that its general model permits discontinuities while the convex-corridor solution is continuous. Then state the arbitrary-lift comparison and compact rational compilation as the additional developments here. No mathematical change is needed.

## Literature cross-checks supporting acceptance

- Read `[[rebennack2015-continuous-piecewise-linear-delta-approximations]] p.1–2`: the source explicitly studies minimal breakpoint systems for continuous approximation and shifted under/overestimation. Introduction lines 237–239 fairly describe that contribution without claiming optimized knots as new.
- Read `[[griffiths2018-adaptive-sampling-for-convex-regression]] p.3–5`: Lemma 2.1 is the asserted factor-two secant/midpoint estimate; the subsequent local modulus and endpoint treatment concern approximation/sampling complexity. The introduction and scalar opening preserve the difference from arbitrary-lift minimum dimension. The source authors match the manuscript's Simchowitz et al. entry despite the local package slug beginning with Griffiths.
- Read `[[lyu2026-building-formulations-for-piecewise-linear]] p.6–8`: Section 3 and Proposition 1 merge all breakpoints and use one SOS2 constraint for several same-input outputs. The manuscript fairly credits this and claims the curvature-rank comparison and compact implicit access separately. Primary arXiv metadata was checked at https://arxiv.org/abs/2304.14542.
- The introduction explicitly says that the two-bit scalar result permits real coefficients and unrestricted continuous size; the separate eleven-bit claim specifies dense rational polynomial input and total encoding length. Likewise, it does not transfer the sparse binary-exponent claim for positive separable polynomials to the general dense vector compiler.
- The finite covariance benchmark's coefficient/output uniformity and the quadratic asymptotic law's fixed-instance constants match the displayed theorem statements. The nc-rank priority sentence is qualified and identifies the precise new connection, not a new invariant or algorithm.

## Optional preferences

None needed for acceptance of this stage. Address M1 before proceeding; no five-reviewer repeat is required on the basis of this review alone because it identifies no major issue.
