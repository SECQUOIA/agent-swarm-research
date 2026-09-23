# Independent audit of the QCQP multiplicity resolution note

Reviewed 2026-09-04 by `review_fbbt`. The explanatory hull proof and the
strict-feasibility counterexample in
[the resolution note](qcqp-multiplicity-threshold-resolution.md) are correct.
This review does not assert novelty.

## Source scope

I independently checked [Beck (2007), Corollary 4.4, printed p.1236](https://www.tau.ac.il/~becka/14.pdf).
It requires feasibility, the positive-definite Lagrangian condition (20), and
`|I|+|E| <= r`; it gives attainment and equality of the QMP and vectorized SDP
values. Thus it covers mixed equalities and inequalities, counting each once.
Its vectorization identity matches `A_i = I_k tensor bar(A_i)` with `r=k`.

[Wang and Kılınç-Karzan, arXiv:2403.04752v2](https://arxiv.org/pdf/2403.04752v2)
states the improved hull threshold explicitly in Section 4.1, Remark 5,
printed pp.8–9. The displayed framework in this version uses inequalities.
The mixed-constraint statement is justified here by Beck and the alternative
proof, rather than by silently converting equalities into two inequalities
while retaining the original constraint count. Version-specific numbering
should be preserved; the v2 reference does not establish the numbering in v1.

## Proof audit

The signed-multiplier Lagrangian is bounded above by `q_0` on the feasible set.
Its positive-definite quadratic part therefore supplies the stated uniform
quadratic lower bound on epigraph height, without primal strict feasibility.

For the closedness argument, pad every Carathéodory representation to `N+2`
terms. After translating height, each height is nonnegative. Bounded average
height bounds every weighted height and weighted squared norm. If a weight
vanishes, Cauchy–Schwarz gives
`||lambda_j x_j|| <= sqrt(lambda_j) sqrt(lambda_j ||x_j||^2) -> 0`.
All positive limiting weights have bounded component points, and finitely many
subsequence extractions suffice. If the vanished terms leave total height
`s >= 0`, choose a surviving weight `lambda_j > 0` and increase its component
height by **`s/lambda_j`**. Upward closure then gives the required finite
representation of the limit. This is the precise meaning of absorbing the
vertical slack in the note.

For every positive `epsilon`, the perturbed objective has quadratic part
`epsilon A_0/2`; multiplying the original constraint multipliers by
`epsilon/2` preserves their signs and positive definiteness. Beck applies
with arbitrary added linear term `v^T x`. Minimizing `v^T x+epsilon t`
over the original or lifted epigraph is exactly the corresponding perturbed
QCQP or Shor value, since the positive coefficient permits minimizing over
height at its defining lower bound.

Vertical separators are handled correctly. If `v^T x >= eta` separates a
point `z=(x_z,t_z)` with margin `delta=eta-v^T x_z>0`, then its positive-height
tilt still separates whenever `epsilon(t_z+b)<delta`. Such an epsilon always
exists; if `t_z+b <= 0`, every positive epsilon works. The uniform height
bound is sufficient, and no boundedness of the feasible set is needed.
Finally, the reverse inclusion follows because the projected Shor set is
convex and contains the original epigraph. No unproved closedness of a general
spectrahedral projection is used.

## Counterexample audit

For nonzero feasible `x`, its radius satisfies `0<r<=1`, and the original
objective is at least `r(2-r)>0`. Thus zero is the unique original minimizer.
In the SDP, `tr(X)<=1` and `x<=0` give objective at least `-1`; the proposed
`x=0, X=I_k/k` attains this value. The suggested strict lifted point has
`X-xx^T=tau I_k` positive definite, strictly negative coordinates, and strictly
subunit trace. Hence it is strictly feasible also in the full block-matrix
Shor formulation. The original strict point and multiplier `2` on the ball
are valid for every `k>=1`. There are exactly `k+1` scalar inequalities, and
the common quadratic multiplicity is `k`. The gap therefore proves the
claimed sharpness at `k=m-1`, including the one-variable boundary case.
