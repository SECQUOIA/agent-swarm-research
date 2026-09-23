# Independent review: posterior Bregman flow intervals

Date: 2026-09-05. Verdict: **PASS**, conditional on the independently
verified base energy certificate and, for robust scenario recovery,
the independently correct uncertainty-envelope mapping.

Reviewed [the mathematical note](potential-flow-envelope-bregman-certificates.md)
and [the implementation](../code/potential_flow_mpd/envelope_bregman_bounds.py).
This is a certificate refinement using established convex analysis;
no separate novelty claim is established by the review.

## Reverse divergence and rational boundary certificates

Write `g=E'` edgewise. Since `g(x*)=A^T pi*` and `A(y-x*)=0`,
the stationarity term `sum g_e(x*_e)(y_e-x*_e)` vanishes exactly.
Thus the displayed sum of reverse Bregman divergences equals the
actual primal energy gap and is at most the certified gap `delta`.
Each summand is nonnegative by convexity.

For fixed `y`, direct differentiation gives
`dD(y,z)/dz=g'(z)(z-y)=2 c^sign(z)|z|(z-y)`. Its isolated zero
at `z=0` does not prevent strict decrease on `z<y` or strict increase
on `z>y`. The function grows without bound at both ends. Hence the
sublevel set `D<=delta` is an interval, and the two outward tests
`D(y,L)>=delta`, `D(y,U)>=delta`, together with `L<=y<=U`, enclose
that interval. Equality is safe: an exact boundary point may be used.
The claim uses this orientation of the divergence; replacing it by
the other Bregman orientation without rechecking monotonicity would
not be justified.

At `delta=0`, strict convexity forces `x*=y`, so returning singleton
intervals is correct. The verifier also accepts any wider interval
containing `y` at zero gap, which is valid.

The previous scalar inequality `D(y,z)>=beta_L|y-z|^3/6`, together
with the verified common-radius inequality, puts `y±eta` outside
the sublevel set. Every bisection iteration retains the outward
endpoint satisfying `D>=delta` and an inward endpoint satisfying
`D<delta`. After `k` steps the boundary bracket has width at most
`eta/2^k`; rational arithmetic has polynomial bit complexity in the
input size and requested precision. This isolates the boundary to
arbitrary accuracy. It does not remove the intrinsic interval width
caused by a fixed positive energy gap.

## Conditional recovery of an original resistance scenario

Let `h_e` be the law of the original scenario chosen from the sign of
`y`, and let `x'` be its physical state. If its coefficient differs
from the envelope coefficient at `x*`, the signs used for selection
disagree. The certified interval then bounds the magnitude of `x*`
on that opposite side by the stated `a_e`. Accordingly
`|h_e(x*_e)-g_e(x*_e)|<=(Ubeta_e-Lbeta_e)a_e^2=r_e`.

For completeness, put `d=x'-x*`. Both states satisfy the same
conservation equation, so `Ad=0`. Both physical law vectors are
potential gradients. Summing against `d` and using scalar strong
monotonicity of the original quadratic law gives

```
(beta_L/2) sum_e |d_e|^3
 <= sum_e (h_e(x'_e)-h_e(x*_e)) d_e
 = sum_e (g_e(x*_e)-h_e(x*_e)) d_e
 <= ||d||_infinity sum_e r_e.
```

If `d!=0`, division and `sum |d_e|^3>=||d||_infinity^3` give exactly
`||d||_infinity^2<=2 sum r_e/beta_L`; for `d=0` it is immediate.
No unproved quantitative circulation decomposition is required.
This certifies the target-edge **flow** loss relative to its envelope
optimum. It is not directly a pressure-objective loss bound.

If every `a_e=0`, all selected original laws agree with the envelope
laws at `x*`, including edges with `x*_e=0`. Uniqueness of the original
physical state therefore makes this scenario exactly optimal for the
target flow. Strictly sign-resolved intervals suffice but are not
necessary: an interval touching zero on the consistent side also
has `a_e=0`. This posterior statement does not promise a universal
polynomial precision bound for exact scenario recovery.

## Implementation and independent checks

The new verifier uses unconditional `require` calls. Its documented
precondition is that the base certificate was checked independently;
it is not a replacement for conservation, conjugate-root, or energy-gap
verification. The public file path checks the base certificate before
refining its intervals. Positive rational coefficients, dimensions,
rational endpoints, ordering, gap type/sign, and both outward tests
are checked. Malformed data cannot become accepted merely because
Python assertions are disabled.

The independent checker
[check_envelope_bregman_review.py](../code/potential_flow_mpd/check_envelope_bregman_review.py)
passed in both normal and `python -O` modes. In each mode it checked:

- 50 exact known physical states, including asymmetric laws, conserved
  cycle perturbations across positive, negative, and zero approximate
  edge flows, a nonzero exact state with zero gap, and the zero state;
- 339 rejected malformed bounds or coefficients, including endpoints
  placed at the approximate flow when the gap is positive, reversed
  endpoints, nonrational data, dimension mismatch, and a zero-gap
  interval missing the physical state;
- 60 exact pairs of conserved physical states satisfying the residual
  recovery inequality above.

The checks also verified exact divergence decomposition, containment
of the known physical state, pressure-drop containment, and the
outward/inward boundary-bracket invariant after bisection. No floating
point tolerance was used for these checks.

Running the supplied example in optimized mode verified all six
intervals and rejected its deliberate undersized interval. Its largest
certified flow width is below `2.894e-6`, compared with the prior
common width below `3.405e-4`; its largest certified edge-pressure
width is below `3.961e-6`. These are conservative summaries of exact
interval bounds, not empirical errors against a numerical solution.

Finally, monotonicity of each scalar law makes `[g(L),g(U)]` a valid
edge-drop enclosure. Signed summation along a path, or along a fixed
spanning-tree representation of a zero-sum weighted objective, remains
valid even when edge errors are dependent. This certifies a deterministic
objective. The JSON still does not authenticate an original uncertainty
set, target, or graph-dependent envelope construction.
