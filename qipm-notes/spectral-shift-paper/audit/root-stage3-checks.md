# Root independent LP checks

Before reading the Stage 3 draft, I checked the source construction directly.
The q vectors are orthonormal; q_+ is strictly positive, so a nonzero kernel
direction has both signs and cuts out a bounded nontrivial feasible segment
through the strictly positive center. The component of the all-ones vector
in span(v0,k) is proportional to k, not q_- when cos(theta) is nonzero,
so the objective is nonconstant on the feasible line. Eliminating the
predictor equations yields H_t dy=A_t*1 with the displayed positive sign.

A qipm NumPy check at rho=2, delta in {1e-2,1e-4,1e-6}, and t at both
interval endpoints confirmed AA*=H, the predictor solution, and unitarity
of the explicit factor Halmos completion to <1e-13. The endpoint trace
distance was 0.169101978726 throughout, agreeing with
(sqrt(2)-1)/sqrt(6). The factor-oracle norm gap divided by sqrt(delta)
was 0.417266057, 0.414243743, 0.414213864, approaching sqrt(2)-1.
These are diagnostics, not proof certificates.

The standard amplitude-estimation bound gives a relative-t estimate at
O(1/delta) queries for success probability t^2, or O(1/sqrt(delta)) for
success probability t. Clipping to the known interval cannot increase its
absolute error. The state angle arctan(sqrt(delta/t)) has derivative of
magnitude at most 1/(2t), so O(delta) scalar error gives a fixed trace
error uniformly. Constant repetition suffices for a fixed failure budget.

The author correctly found that public fixed eigenspaces permit zero-query
coarse compilation, unlike the general unknown-support c=1 problem. This
exception must appear in the formal transfer theorem. The matrix-only
compiler can still use the scalar trigonometric lower proof for every
positive-index tier: its known high block is constant in the hidden angle.
An additional RHS-preparation oracle is allowed for the state problem but
is not silently added to that compiler theorem.

Exact sparse values reveal t immediately, even from H_12=(1-t)/2. Thus
these analog-oracle bounds are not sparse-value input lower bounds.
