# Stage 3, round 1 — independent review 5

**Result: 0 major findings, 0 minor findings.** I found no mathematical defect or omitted substantive source development in the frozen LP section. No manuscript repair is requested from this review.

Reviewed `sections/06-lp-application.tex`, the complete `2026-09-04-sparse-lp-newton-access-separation.md` source note, `audit/stage3-author.md`, and the earlier results used by the compiler transfer. I did not read peer reports or edit the manuscript. Introduction and final packaging are outside this review.

## LP and Newton identities

The prescribed vectors form the stated orthonormal bases. The restrictions on the public gap make `0<sin(theta)<1`, and hence the displayed positive cosine and the nonconstant objective are valid. The singular values of the constraint matrix are exactly `1` and `sqrt(t)`, giving its rank, norm, normal matrix, and condition number. Its entry bound also follows directly from its operator norm.

The feasible affine line has direction `q_0`. Orthogonality to the strictly positive `q_+` forces both signs in this direction, which proves compactness and nontriviality of its intersection with the orthant. The objective derivative on the line is `cos(theta)/sqrt(3)>0`.

The central point satisfies primal feasibility, dual feasibility, positivity, and complementarity with the stated dual sign convention. Eliminating the predictor equations gives the stated positive right side in the normal equation. The identities for that right side, the dual direction, and the primal direction all check out. In particular, the hidden parameter changes only the representation of the equalities and the dual direction; the public feasible segment and primal direction are independent of it. The manuscript correctly states this limitation.

The pseudoinverse identity has the correct orientation and dimensions. The squared support overlap is `(8/9)(1+delta)`, which lies below one under `delta<1/8` and stays bounded away from zero.

## Full oracle contracts and state bounds

Both Halmos constructions are unitary on their complete stated spaces. The normal oracle reduces to the claimed two reflection blocks. The rectangular oracle reduces to two singular-vector pairs plus its specified action on the column null vector. Public identity padding adds no hidden dependence. The preparation oracle has the correct full rotation matrix and prepares precisely the normalized right side.

The contract explicitly withholds the hidden classical coefficients and the exact right-side norm. Supplying that norm would indeed reveal the parameter. All preparation queries, inverses, and controlled choices are counted, and the right-side oracle is present only in the two state-access models.

The endpoint target overlap and trace distance are correct. The hypotheses imply both `t<1/2` and `sqrt(t)<1/2`, as needed for the stated reflection-difference estimate. A fixed Hadamard basis change relates the factor reflection block to the normal reflection convention. The resulting endpoint oracle distances are `O(delta)` and `O(sqrt(delta))`; the preparation-oracle distance is `O(delta)`. Their maximum gives the stated hybrid bounds even for algorithms choosing coherently between the supplied query types. Purification, deferred measurements, and trace-distance contraction on discarded registers justify the lower bounds for the output density operators.

I independently checked the amplitude-estimation formula and its success probability against [Brassard–Høyer–Mosca–Tapp, Theorem 12](https://arxiv.org/pdf/quant-ph/0005055). Its preparation/inverse costs are counted correctly here. In the normal model the success probability is `t^2`; dividing the probability error by `t>=delta` gives the displayed parameter error with `M=O(delta^-1)`. In the factor model the probability is `t`, giving parameter error `O(delta)` with `M=O(delta^-1/2)`. Clipping to the known interval cannot increase either error.

A fixed number of median repetitions suffices because the requested output tolerance is fixed. This introduces no logarithm of the gap. The state-angle derivative is at most `1/(4 delta)` on the clipped interval, so successful estimates have trace error at most `epsilon_0/4`. All failure events are included in the mixed output and contribute at most their probability, which is at most `epsilon_0/2`. The final error is therefore below `epsilon_0`. There is no postselection or expected-query shortcut in either upper bound. These arguments establish both matching orders without relying on an unspecified generic solver bound.

## Compiler transfer and bypasses

The compiler has a separate matrix-only contract. On the canonical normal family, replacing its variable reflection by the periodic sine reflection preserves unitarity globally and agrees with the actual oracle on the promised branch. Every designated output entry retains the query-degree bound even when gates mix eigenspaces. The `u_-` entry therefore satisfies exactly the scalar hypotheses required by all transferred low-continuum lower bounds. Excluding the preparation oracle from this argument is explicit and necessary for the stated degree induction.

The polynomial upper bounds apply with the singleton high band `c=1`. This gives the matching positive fixed-accuracy tiers, their threshold equalities, and the full high-accuracy law. The conversion between relative and absolute error logarithms is uniform in the stated polynomial-or-higher-accuracy regime.

The coarse branch is correctly **zero queries**: the public contraction `(1-m_rho delta)P_-` has worst-case error exactly `G_0 delta` on this family, and a public dilation supplies the required unit-normalized block. A constant nonzero lower bound from the general unknown-projector problem would not apply here. The manuscript also avoids importing a positive-width high-band logarithmic lower bound.

The two-query factor construction is correct. The left-singular-vector formulation has output on the row space, so the column null vector does not add a spurious output eigenvalue. Independently, conjugating a free block encoding of the public complementary column projector gives the displayed compression identity and exact normalization. This establishes sufficiency of two queries; the manuscript does not claim their optimality.

The inherited intermediate-accuracy qualifications, vanishing-relative-error consequence, and exact-continuum impossibility are all transferred with the correct scope. The public-parameter comparison correctly distinguishes unknown eigenspaces from the public eigenspaces of this example.

Both digital-entry formulas reveal the hidden parameter under exact value access. Sufficient finite precision gives the advertised constant-query state approximation, with precision costs explicitly left separate. The normalization-two linear combination uses one controlled oracle call and has the claimed compressed block. These observations are consistent with the final warning against interpreting the result as an intrinsic sparse-input, LP-solving, or end-to-end QIPM lower bound.

## Source completeness and corrections

Every substantive development of the source note is represented: the exact-central sparse LP, its compact feasible segment and nonconstant objective, the Newton equation and normalized dual state, the canonical-oracle hybrid bounds including right-side preparation, the normal-versus-factor separation, the complete positive-index compiler hierarchy and high-accuracy transfer, exact factor complement construction, and digital/normalization bypasses.

The manuscript improves three points in the source without losing scope:

1. Direct amplitude estimation replaces the logarithm-suppressed factor solver upper bound and proves exact fixed-error query orders for both state models.
2. The specialized compiler's public eigenspaces give a zero-query coarse tier, correcting the source's unqualified transfer of a complete hierarchy.
3. Full oracle completions, the withheld right-side norm, and the parameter-independent primal direction make the access and task limitations explicit.

I found no remaining reliance on an unproved overlap-free solver guarantee or an unspecified completion.

## Independent numerical diagnostics

Using `/workspace/local-home/miniconda3/envs/qipm/bin/python`, I checked 135 parameter samples across `rho` values `1.01, 1.5, 2, 7, 100`, three admissible gap sizes for each ratio, and nine hidden parameters per interval. Checks covered basis orthogonality, `AA^T=H`, the normal equation, primal-direction feasibility, the complementarity predictor equation, both full oracle unitarities, right-side preparation, the projector-compression factor identity, the support overlap, endpoint state distance, the coarse approximation, and the successful-estimate angle bound.

The maximum algebraic residual was `1.33e-15`. The largest sampled successful-estimate trace error divided by its stated `epsilon_0/4` upper bound was about `0.999845`. These floating-point checks corroborate the analytic verification; they are not proof certificates. No manuscript or stored artifact was changed.
