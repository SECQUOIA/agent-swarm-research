# Independent audit: diagonal PSD quadratics with linear dimension overhead

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**PASS.** I independently reviewed [the diagonal PSD trace-allocation candidate](diagonal-psd-quadratic-linear-dimension-precision.md). The finite characterization and the explicit polynomial rational construction are correct as stated for nonnegative diagonal Hessians in the original cube axes. The final bound `p_out<=p_conv+5r+1` follows from the displayed constants. No correction was needed.

## Domain and covariance lower bound

Subtracting the complete affine part from each output is an invertible affine change of visible coordinates and preserves the integer count. The remaining functions depend only on the `r` active axes. Restricting inactive coordinates to zero gives one direction of the minimum-count equality; reintroducing them as independent continuous cube coordinates gives the other. This proves the exact active-cube reduction, rather than assuming that affine directions can always be dropped without specifying the formulation map. The case `r=0` has an exact LP.

For every same-parity pair, the midpoint identity gives `0<=q_j(x-y)<=4 epsilon_j`. Positivity of the diagonal Hessians is essential here. For independent uniformly distributed points on a compact positive-volume support, the expected coordinate squared difference is `2 Sigma_ii`. Hence the expectation of `q_j(X-Y)` is exactly `sum_i h_ji Sigma_ii`, with no missing factor of two. Dividing diagonal variances by four gives a feasible trace allocation; the cap follows from `Sigma_ii<=1/4`.

Hadamard's inequality and the covariance-volume bound yield the stated support volume at most `2^r omega_r(r+2)^(r/2) sqrt(D_tr)`. Taking closures of parity supports, as in the reviewed general argument, preserves the pair inequality and makes the volume argument legitimate for arbitrary convex lifts. Zero-volume supports cannot cover the cube by finitely many parity classes. Thus the unrestricted-integer lower bound has precisely the displayed constant `A_r^tr`.

The elementary Gaussian volume estimate is sufficient to prove `A_r^tr<4r`. Indeed, integrating `exp(-(r/2)||x||^2)` over all of Euclidean space and comparing with its minimum over the unit ball gives `omega_r<=(2pi e/r)^(r/2)`. The resulting bracket `2pi e(1+2/r)` is at most `6pi e<64` for every `r>=1`, proving the strict bound.

## Original-axis grid upper bound

The depths `L_i=ceil(.5 log2(1/p_i))` are nonnegative and give residual width at most `sqrt(p_i)`. Exact prefix products plus the residual square triangle contain every exact graph point and have residual square error at most one quarter of the squared cell width. Consequently each output has absolute error at most `sum_i h_ji p_i/8<=epsilon_j/8`. Shared square variables suffice for all outputs; there are no cross terms to approximate.

Summing the depth bounds gives at most `Phi_tr+r` binaries at an optimal allocation. The established exact prefix construction uses no additional integer coordinates and has polynomial size. The original-axis condition is substantive: this proof does not apply to an arbitrary orthogonal simultaneous diagonalization whose transformed cube is oblique. The note correctly states that limitation.

## Explicit allocation algorithm

A feasible common allocation `delta=2^(-b)` yields an optimal product at least `delta^r`. Since every coordinate is at most one, every optimal coordinate is at least `delta^r`. Thus its natural logarithms lie in the proposed box `[-R,0]^r` with `R=rb+1`.

The function `F(u)=-sum_i u_i+r h(u)` is convex, and the repair `p_i=exp(u_i-h(u))` gives an exactly feasible allocation whose negative log product is `F(u)`. The minimum on the box is therefore the required constrained optimum. Every nonzero row log-sum-exp branch has a probability-vector gradient; together with the coordinate and zero branches this gives the global Lipschitz bound `sqrt(r)+r<=2r`.

The candidate's inexact scheme has the correct constants. The diameter bound `D_bar=rR` dominates the actual diameter `sqrt(r)R`. Approximate branch selection costs at most `2r tau`; full-gradient error costs at most `D_bar nu`, totaling `1/32`. With the stated step size and step count, the initial-distance and gradient-square terms are each at most `1/32`. The mean objective gap is therefore at most `3/32`. Selecting the best estimate with error `1/64` adds at most `1/32`, giving the claimed `1/8` gap. The approximate gradient norm is bounded by `3r`. Exact rational clipping adds no projection error.

The row lower bound `exp(-R)sum_i h_ji` makes logarithms and normalized gradients polynomially conditioned in the required bit sense. Input magnitudes and the number of terms give polynomial upper bounds on the corresponding encoding lengths. Polynomially many rational updates preserve polynomial bit length; the approximate gradients can be chosen dyadic to fixed sufficient polynomial precision. Scalar exponential and logarithm evaluation on these ranges uses the previously reviewed elementary routines.

The rational `q_i` with logarithmic error at most `1/(32r^2)` can be obtained using relative exponential approximation. Its exact rational scaling by `kappa` enforces every allocation inequality and every cap. The negative log product equals `F(log q)`. Global Lipschitz continuity bounds its increase over `F(u)` by `sqrt(r)/(16r)<=1/16`, comfortably inside the claimed final loss of one. Thus the constructed product is at least `exp(-1)D_tr`.

The resulting grid uses at most `Phi_tr+r+1/(2ln2)` binaries. Combining `Phi_tr<=p_conv+A_r^tr`, `A_r^tr<4r`, and `1/(2ln2)<1` gives the advertised bound. Grid depths are decided by exact rational comparisons, and all input, affine-output, prefix, and residual coefficients have polynomial rational encoding.

## Interpretation

The trace benchmark differs materially from the Frobenius-energy benchmark. Its linear overhead does not contradict the diagonal PSD example with a larger dimension-dependent gap for the latter benchmark. The new proof uses positivity to turn midpoint control into a first-moment trace inequality and the original box axes to avoid a rotated-domain covering loss. This audit certifies those deductions; it does not independently establish novelty relative to all literature.
