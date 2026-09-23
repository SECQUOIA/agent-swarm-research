# Independent check of the diagonal follower dimension boundary

Date: 2026-09-05. Verdict: PASS as an attributed supporting argument.

Reviewed [the construction](bilevel-diagonal-leader-dimension-boundary.md)
independently. This review concerns mathematical correctness and parameter
accounting; the linked source audit establishes the prior-result overlap.

The alternating capped-ramp sum has slopes alternating between two and
minus two on the half-grid, starts at zero, and therefore equals twice
the distance to the nearest label. The mixed-radix argument lies in
`[0,n^2-1]`, and the second interpolation identity is the standard telescoping
piecewise-linear interpolation of the zero-one table. Its Lipschitz constant
is at most one.

Rounding to labels gives `|s-s_rounded|<=nD`. In a no-clique instance some
rounded pair has table value one, including repeated labels. Its contribution
alone proves the objective bound `2nD+2 max(0,1-nD)>=2`. Every other contribution
is nonnegative. A clique attains zero at an exact rational grid point. Thus
the continuous-domain gap is valid without relying on integrality enforcement
or stationary-point arguments.

Each ramp is exactly the unique minimizer of its scalar strictly convex box
quadratic. Taking their sum gives Hessian identity. The `n` copies in the
triangle term correctly convert `2d` to `2nd`; pair ramp coefficients are
twice table differences, and a fixed-one follower supplies each constant.
The follower count is `O(k^2 n^2)`, its affine forms involve at most two
leaders, and all coefficient magnitudes and encodings are polynomial.

The final coefficient normalization is also exact: the positive ranges of
both `h` and `h-1` are bounded by `R=2n^2`, so their ReLUs equal `R` times
the corresponding scaled capped ramps on the leader domain. Their difference
equals the original capped ramp. Duplicating `R` copies keeps upper
coefficients bounded and gives `O(k^2 n^4)` followers. Scaling only one capped
ramp would fail, and the note correctly avoids that step.

The dimension parameter remains `k`. Polynomial growth of the remaining input
preserves the stated clique-based W[1] and ETH implications. Guessing clipping
regimes leaves a rational linear feasibility system, providing the ordinary
NP membership assertion. The single-leader-coordinate dependence special
case is separable under the stated product-domain and no-coupling assumptions.

No correction was needed. The result is explicitly identified as already
covered by the cited primary neural-network hardness theorem; it is not a
new hardness claim.
