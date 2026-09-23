# Stage 3 independent review — reviewer 2

## Decision

**No major issues identified.** One minor terminology correction is requested. The results and proofs within this stage are mathematically coherent, including the fractional leading constants and the equal-degree counterexample.

I reviewed all three new sections, the bibliography additions, and the author notes. I did not read other Stage 3 reports. I checked the relevant local Drusvyatskiy–Wolkowicz primary text and the existing claim-level source audit. I also ran the retained Stage 3 verification script successfully; that run supplements the analytical checks below and is not a substitute for them.

## MINOR 1 — distinguish the path parameter from the barrier parameter

Location: `sections/07-fractional-sdp.tex`, Theorem “Four reduced-Hessian scales,” immediately before the displayed formula for `q` and `mu`.

The text says “its barrier parameter satisfies” but the quantity being solved for is `mu`, the central-path parameter. The self-concordant barrier parameter is `nu` (three for the ambient canonical log-det barrier). This terminology is inconsistent with the setup and is particularly confusing in a paper comparing different barriers and different path parameterizations.

Fix: replace “its barrier parameter satisfies” by “the corresponding central-path parameter satisfies.” No formula changes are needed.

## Analytical verification

### Error bounds and the regime dictionary

The distance bound gives the stated diameter upper bound by projecting both chord endpoints to the compact optimal set. The objective-normal lower bound follows from a feasible point with gap exactly `g`. At a singleton optimum this yields an upper conditioning rate; the manuscript correctly requires attained diameter growth for a matching rate. The polytope proof establishes linear shrinkage without imposing vertex nondegeneracy. The positive-dimensional face and curved singleton implications are valid consequences of the general law.

For the two-by-two example, the tangent coordinate Gram matrix is `2I`. Dividing the scalar second derivatives by two gives exactly the displayed eigenvalues. The ratio is asymptotic to `1/(2g)`. No ambient-versus-reduced normalization is lost.

### Uniform simplex family

The diameter comparison has absolute constants: the displayed feasible edge chord has length `sqrt(2) min(g/theta,1)`, and the distance of every sublevel point from `e1` is at most the same bound. The triangle inequality supplies a uniform diameter upper bound. The objective range and projected objective norm remain uniformly controlled, so the all-barrier plateau estimate follows with exactly the stated parameter dependence. The common attained gap interval is justified by the earlier analytic-center bound and does not hide a threshold depending on the objective perturbation.

For fixed positive `theta`, the limiting coordinate quadratic form is `diag(theta^2,1)` against Gram matrix `[[2,1],[1,2]]`. Its characteristic equation is

`3 lambda^2 - 2(1+theta^2)lambda + theta^2 = 0`.

This gives the displayed roots and condition ratio. Their product and limiting large root give `theta^2 kappa -> 4/3`. The manuscript properly separates this iterated limit from its uniform joint gap estimate.

### Unique LP optimum and degeneracy

The endpoint convergence is explicitly invoked as a classical theorem with attribution, and the new section proves the exact consequence it needs. Complementarity gives the scaled-Hessian identity. Uniqueness makes `A_B` full column rank: a supported null direction admits both feasible signs, and dual optimality makes both directions objective-neutral. Hence restriction to the inactive coordinates is injective on the equality nullspace, which proves positive definiteness of the limiting compression even when `|B|<m`.

The dual-face analytic-center formula is well posed. Strict primal feasibility bounds all optimal slack coordinates; full row rank controls the corresponding multiplier. Strict complementarity supplies a point with all `N`-slacks positive. The negative log Hessian is positive definite on the equality tangent, giving uniqueness, including the zero-dimensional case. Every displayed extreme-eigenvalue bound follows from the same Loewner sandwich, and the condition lower bound is allowed to be below one without becoming false.

The compact four-variable example is consistent: the proposed primal point satisfies both equalities, the given negative multiplier is strictly dual feasible, and the objective has unique minimizer `e3`. The one-variable dual center equation and root are correct. The explicit basis lies in `ker A` and has the stated Gram matrix; generalized eigenvalues are the appropriate metric-preserving calculation. The reproduced values agree with the text. The unbounded example solves the central equations exactly, has compact positive objective sublevels, and correctly yields `diag(1,M^2)` in its orthonormal tangent basis.

### Paired SDP geometry and facial reduction

Trace normalization gives compactness and the displayed strict point works for both sets. At zero objective, PSD zero-row implications force the unique rank-one optimum. The principal-minor inequalities give the claimed upper diameter rates. For the signed lower witnesses, I obtain

`det X = g^(3/2)(a/2 - 1/4)`

with positive leading minors. The Frobenius distance between the two signs is exactly `g^(1/4)`. The restricted witness is feasible and supplies the square-root lower distance.

For both optimality systems, the trace multiplier vanishes in a first-step exposing combination. PSD and the zero first diagonal then force the coefficients of `J12` and `J13` to vanish, and the zero third diagonal forces the `J23` coefficient to vanish. The only nonzero first-step certificate is therefore a positive multiple of `E22`. The two stated reductions are admissible and reach the rank-one face; one step cannot. Adding the block-zero equations thus preserves degree two for the explicitly stated `S_+^3` formulation. The manuscript correctly distinguishes this degree from degree zero of the strictly feasible original systems and does not claim formulation invariance.

The same zero-row calculation with the objective coefficient fixed to one yields the sole optimal dual slack `E22`. Therefore strict complementarity fails, although adding a positive identity to that slack yields strict dual feasibility. This is consistent with all hypotheses used for the canonical path.

The error-bound application uses only the residual in the added objective equality and a fixed affine-system right inverse. The degree-based bound is an upper estimate. Comparing the two proved diameters legitimately demonstrates that degree alone does not determine the conditioning exponent.

### Exact center and spectral constants

Sign conjugation removes both off-block coordinates at the canonical center. Differentiating `-log b-log q` gives `q+bq_b=0` and `1/mu=q_g/q`; the chosen positive quadratic root and positive denominator give a genuine central point for small positive gap.

The asymptotic relations give `b~sqrt(mu/2)`, `q~mu`, and `a->1`. In the off-block subspace the Frobenius factor two cancels the factor two in the log-det second derivative. The operator is therefore `A2^(-1)/b`, with the stated constants `sqrt(2)` at powers one-half and three-halves.

In the other subspace I independently obtain the Gram matrix `[[4,1],[1,2]]` and the displayed coordinate Hessian. Its scaled entries tend to `6`, `-sqrt(2)`, and `1` with their respective powers of `mu`. The nonzero eigenvalue of the limiting normalized rank-one operator is `(G^-1)22=4/7`. The generalized determinant product is asymptotic to `(4/7)mu^-3`, so the smaller eigenvalue constant is exactly one. These calculations establish all four constants and their eventual ordering. They also give the restricted pair directly, without an interlacing assumption.

Finally, converting `mu~2g/3` yields the condition constants `3sqrt(3)/7` on the full set and `6/7` on the restricted set. The same-gap Loewner comparison transfers orders to any fixed barrier while leaving the canonical leading constants explicitly barrier-specific.

## Prior work and scientific framing

The local Drusvyatskiy–Wolkowicz Example 4.5.2 gives the nested system `X22=0`, `X(k+1,k+1)=X(1,k)` and its sharp fractional error geometry; Section 4.7 attributes that example and the singularity-degree error theorem to Sturm. This supports the manuscript's classical-construction attribution. The LP endpoint statement is likewise marked as a classical corollary. The discussion distinguishes the reduced primal Hessian from the older SDP Schur-matrix analysis.

The qualified novelty sentence is narrowly about the explicitly computed constants for this trace-normalized construction and their all-barrier transfer. It does not claim the first fractional SDP example, first spectral clustering analysis, or a complete facial classification. I found no unsupported broader priority claim in this stage. The final introduction should retain these exact boundaries.

After the terminology fix, no additional correction cycle is required on the basis of this review. The deferred solver and numerical sections are not prerequisites for the proved Stage 3 results.
