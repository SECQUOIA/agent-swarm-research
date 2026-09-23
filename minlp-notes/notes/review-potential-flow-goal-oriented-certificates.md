# Independent review of conservation-aware goal certificates

Date: 2026-09-06. Reviewer: `review_goal_bounds`, separate from the author.

**Outcome:** the two certificate formulas, their stated scope, and the current
implementation pass this independent mathematical and computational review. No
correctness defect was found. This conclusion concerns the deterministic flow
problem supplied to the verifier. It does not independently certify a mapping
from an original uncertainty problem to that deterministic problem.

Reviewed:

- [Mathematical note](potential-flow-goal-oriented-certificates.md).
- [Producer and verifier](../code/potential_flow_mpd/goal_flow_certificate.py).
- The imported rational energy and Bregman interval verification conditions.

The review adds a separate, standard-library-only
[check script](../code/potential_flow_mpd/check_goal_flow_certificate_review.py).
It does not modify the author's implementation.

## Mathematical checks

For the support certificate, maximizing
`s*t - lambda*c*abs(t)^3/3` gives the stationary magnitude
`sqrt(abs(s)/(lambda*c))`. Substitution gives
`(2/3)*sqrt(abs(s)^3/(lambda*c))`, with the coefficient selected by the sign of
`s`. Thus both the factor `2/3` and the single power of `lambda` inside the
denominator are correct. Conservation contributes `v^T b` with the implemented
incidence convention. The witness is an upper bound for every conserved flow
in the energy sublevel, not only the physical flow.

At multiplier zero the conjugate is finite exactly for zero residual. The
resulting goal is a cut functional and is fixed by conservation. Negative
goals use the same calculation, so upper certificates for `w` and `-w` give
two-sided bounds. The note's strict energy slack hypothesis suffices for the
stated relative Slater argument. For a nonconstant goal, a dual solution with
zero multiplier cannot be finite. Rational approximation and upward root
enclosures establish the claimed completeness, without establishing an
efficient general certificate producer.

For the Hessian certificate, the physical gradient is a node-potential
difference even on a disconnected graph. Therefore its product with a
conserved flow error vanishes. Taylor's integral formula on the certified
edge intervals gives

\[
 \tfrac12\sum_e h_e(y_e-x_e^*)^2
 \le E(y)-E(x^*)\le g.
\]

Weighted Cauchy–Schwarz then yields exactly `radius^2 >= 2*g*factor`.
The curvature coefficient on a negative interval is `-2*c_minus*upper`, as
implemented. The asymmetric energy is twice continuously differentiable at
zero, with zero second derivative there; no missing differentiability
assumption is needed.

When a curvature is zero, the corresponding dual goal residual must vanish.
The constrained Laplacian system has the correct blocks and right side.
Its consistency is equivalent to the goal annihilating every circulation on
the zero-curvature subgraph. Redundant equality constraints and component
gauges make the matrix singular without making a valid problem inconsistent.
The rational elimination handles these cases. A nonoptimal feasible potential
also gives a valid bound; optimality of the producer's potential is correctly
excluded from the verifier's trust boundary.

For one circulation direction `z`, a separate scalar calculation gives the
optimal quadratic factor

\[
 C_*=(w^Tz)^2/(z^THz).
\]

The independent test checks this identity against the produced factor for
positive, negative, and partially zero physical flows. For strictly positive
curvature the effective-resistance formula in the note follows by expanding
the quadratic projection objective. Its zero value on bridges is correct.

The zero-gap bypass is valid: strict convexity gives `x*=y`, regardless of
whether the Hessian controls the goal. A positive-gap failure of the Hessian
producer on a zero-curvature circulation is a documented limitation of that
method, not a failure of the support method or proof of physical ambiguity.

For the long-path example, direct expansion gives energy gap
`2*L*epsilon^2`. The conserved energy sublevel has target coordinate
`[1-epsilon,1+epsilon]`. As curvature tends to two, its circulation denominator
is `4*L`, so the Hessian radius tends to `epsilon`. The asymptotic improvement
factor `sqrt(2*L)` is correct in the stated limit: first small epsilon at fixed
L, with epsilon chosen small enough as L increases. This does not imply a
uniform improvement for a fixed epsilon and arbitrary L.

## Exact checks and trust boundary

The checker reconstructs three known physical solutions directly from
rational potentials and edge laws. It uses an independent energy expression
and samples the one-dimensional conserved energy sublevel. It also exercises
parallel edges, disconnected components, an isolated node, independent
component gauges, a zero-flow bridge with positive energy gap elsewhere,
redundant zero-edge constraints, and zero-gap noncut goals.

These commands both pass:

```sh
python code/potential_flow_mpd/check_goal_flow_certificate_review.py
python -O code/potential_flow_mpd/check_goal_flow_certificate_review.py
```

Each run checks nine asymmetric/zero-edge goal cases, 732 conserved sublevel
samples, and 161 rejected malformed witnesses, plus the structural cases above.
Rejections include incorrect bounds, negative multipliers or radii, negative
or insufficient root enclosures, truncated potentials, nonrational scalar
witnesses, invalid Bregman intervals, false factor identities, uncontrolled
zero-curvature goals, and a corrupted base energy gap. All review checks use
explicit exceptions and remain active with `-O`.

The verifiers recheck feasibility and the supplied energy witness where
needed. They do not trust termination status, floating-point residuals, or
the producer's optimality. Upward-root generation contains assertions in a
preexisting helper, but accepted certificates independently verify the root
inequalities with explicit checks. Invalid generation inputs can fail with
ordinary Python exceptions; the interface does not promise a uniform
exception type for every malformed container. This is an API limitation,
not acceptance of an invalid mathematical witness.

The saved six-edge demonstration was independently rerun under optimized
Python:

```sh
python -O code/potential_flow_mpd/goal_flow_certificate.py --certificate code/potential_flow_mpd/envelope_certificate_example.json
```

The reported maximum width drops from `2.89362482e-6` for separate Bregman
intervals to `9.44682415e-7` for the Laplacian certificates. The six displayed
width pairs agree with the author's note. This checks a small concrete
instance, not scalability or actual numerical error.

## Publication scope

The note appropriately identifies convex duality, gap-based error control,
and weighted electrical projection as established ingredients. This review
does not establish literature novelty. The useful package is the explicit
exact witness, singular/zero-curvature treatment, and demonstrable improvement
from conservation. A generic conic producer for support witnesses and a
large-network sparse implementation are not presently supplied. Their absence
does not leave a gap in the stated certificate theorems, but practical runtime
claims should stay within the implemented demonstrations.

An important retained distinction is that the support sublevel contains
nonphysical conserved flows. Physical Bregman intervals cannot automatically
be imposed on that whole set. Intersecting bounds independently proved for
the physical solution is valid.

## Follow-up: integration in the original-instance pipeline

The optional `goal_bounds` integration in
[certified_envelope.py](../code/potential_flow_mpd/certified_envelope.py) was
reviewed after the standalone certificate code. The verifier reconstructs the
edge goal from the original target index; it does not accept a supplied goal
vector. It checks each Hessian witness against the correct recomputed envelope
or scenario coefficients and corresponding base certificate. Intersections
are centered at that certificate's feasible target flow, and empty
intersections are rejected. Malformed supplied witnesses are rejected rather
than silently ignored. The producer omits a witness only for the documented
zero-curvature circulation obstruction. Absence or explicit null means the
original Bregman-only bound remains in effect.

The independent checker now includes this integration. A rational physical
triangle fixture has strictly narrower optimum and scenario intervals after
the verified intersections, and both retain the known physical target value.
Ten malformed integrated witnesses are rejected, including a valid cut-goal
witness incorrectly offered for an edge goal. Null fallback and a positive-gap
zero-curvature obstruction are checked separately.

Both complete commands pass without site packages:

```sh
python -S code/potential_flow_mpd/check_goal_flow_certificate_review.py
python -S -O code/potential_flow_mpd/check_goal_flow_certificate_review.py
```

The producer was subsequently changed to construct witnesses in normalized
units and lift them back exactly. For flow scale B and coefficient scale C,
the correct transformations are intervals and radius times B, unchanged goal
potentials, and factor divided by CB. Two additional exact checks apply
flow/coefficient rescalings `(10^-30,10^40)` and `(10^15,10^-20)` and confirm
the claimed exact covariance.

That change initially bypassed the documented obstruction fallback when
`b=0` but the supplied feasible flow had a positive energy gap. The independent
test caught it. The author corrected it by using normalization supply one for
zero loads and keeping the common fallback path. Both complete commands above
pass after the correction. This was a producer behavior defect, not acceptance
of an unsound certificate; the ordinary solver already produced an exact
zero-gap witness for zero loads.

No integration issue remains from this review. This adds review of the
optional Hessian component; the graph recognition and uncertainty-to-envelope
mapping have a separate independent pipeline review.
