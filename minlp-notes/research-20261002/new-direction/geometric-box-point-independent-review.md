# Independent review of the proposed-point geometric certificate

Date: 2026-10-02. Reviewed the complete
[signed box-point draft](geometric-box-point-certificate.md) and its
[homogeneous predecessor](geometric-copositive-certificate.md). No external
literature search or index edit was made.

**Verdict.** No substantive gap was found in the continuous-box theorem.
The radial inequality, sign-preserving rounding, positive-margin discovery,
width-preserving dynamic program, and rational encoding are sound. The
factor-sixteen statement concerns the specified side-normalized metric.
It is not a mixed-integer discovery guarantee or a bound in physical
Euclidean conditioning without a side-width loss.

## 1. Certificate soundness

The preliminary first-order conditions imply `c_v'd(z)>=0` throughout
the allowed signed box. Since `d(rz)=r d(z)` for positive `r`,

```
f(rz)-r^2 f(z)=r(1-r)c_v'd(z)>=0             (0<=r<=1).
```

This direction is the one needed to extend a lower bound on the normalized
shell inward. It also proves that the infimum defining the normalized
growth modulus is attained on that shell. If the proposed point is the
unique global minimizer, continuity and compactness make its shell ratio
strictly positive. No supplied growth premise is used in the certificate.

Every available sign must pass the first-order check. A failure supplies
the stated rational descent point. A nonpositive one-coordinate endpoint
increment supplies a different point with no larger objective, which
disproves unique global minimality. A zero increment need not disprove
global minimality, and the draft correctly keeps that distinction.

Independent rounding never crosses zero. On the chosen sign side each
displacement coordinate is linear in its normalized coordinate. Therefore
both the linear expectation and every off-diagonal quadratic expectation
are exact. The remaining diagonal variance is bounded above by `L/2`
even when a quadratic diagonal is negative. The subtraction of
`sigma||z||^2` and the second unary correction give exactly the displayed
`sigma/n` residual. A coordinate with magnitude one remains fixed, so
every rounding outcome obeys the shell constraint. This proves the finite
DP lower bound without presuming that the candidate is optimal.

The signed transformed function need not be globally coordinate-semiconcave
across zero. For example, `d1^2+d2^2+d1*d2` with first-coordinate side
widths one and two has a derivative jump from one to two at zero when
the second displacement is one. This does not affect the argument: the
bound is on fixed-sign quadratic branches, and zero is a grid node. The
final draft explicitly states this limitation.

## 2. Discovery, normalization, and arithmetic

When every available endpoint increment is positive, its minimum `M`
is positive and bounds the normalized growth modulus from above. Thus
`L=2max{M,max A_ii(w_i^s)^2}` is positive and satisfies `L>=2g`,
including linear objectives. The proof does not require positive diagonal
curvature. The sufficient threshold `sigma<=g/4`, quartering of `sigma`
between trials, and initial value `L/32` establish the factor-sixteen
discovery bound. A positive root quantity additionally gives
`g>=sigma+b_delta/n>sigma`.

Available signs become coordinate states, not separate global orthants.
Each objective term retains its original variable support. The OR flag
must record endpoint attainment by variables owned in the subtree; the
draft uses this ownership rule and sequential two-state child convolutions.
This establishes the claimed state count without an occurrence or
high-degree factor. Rational side widths and translated coefficients
increase encoding length polynomially; the common grid denominator and
term-once message sums prevent depth-dependent denominator products.

For a nonnegative physical growth modulus, the comparison

```
w_min^2 g_E <= g <= w_max^2 g_E
```

is correct. Its positivity qualification matters: the displayed ordering
is not valid for arbitrary negative-margin candidates. This was raised
during review and made explicit by the author. The resulting positive
certificate gives a physical margin at least `sigma/w_max^2`.

The distortion can be arbitrarily large even for a trivial convex problem:
`F(x)=x^2`, candidate zero, and box `[-epsilon,1]` have physical margin
one, but normalized margin `epsilon^2` and scale `L=2`. Thus the new
parameter must not be described as intrinsic Euclidean conditioning.
For a strictly interior unique quadratic optimum, direct positive-definite
matrix testing is already simpler, as the draft acknowledges.

The endpoint-increment term in `L` can also worsen conditioning independently
of side-width distortion. On the unit box, at candidate zero, take

```
F(x,y)=H[x(1-y)+y(1-x)]+epsilon(x^2+y^2),     H,epsilon>0.
```

The bracket is nonnegative, and `(1,1)` attains the exact growth ratio
`g=epsilon`. The original summed diagonal curvature is `2epsilon`, but
the endpoint-based scale in this theorem is `2(H+epsilon)`. Hence even
at a unit-box corner its conditioning can be arbitrarily worse than the
original diagonal-curvature/growth ratio. The factor-sixteen discovery
claim remains correct for its stated scale. An alternative that keeps
the original curvature should accept a returned margin bounded below by
`min{L/32,g/12}`, rather than insist on a constant fraction of `g` when
`g` can greatly exceed the curvature. The separate physical-shell draft
is pursuing that formulation.

## 3. What this adds to existing conditioned optimization

The direct shell certificate is useful as a small, explicit proof object:
its verifier needs rational finite-state DP and the rounding theorem,
without an optimization accuracy target or rational-value isolation.
It also reports a quantitative margin close to the best normalized one.

It does not establish a new conditioned solvability class beyond the
earlier [pruned coordinate-grid theorem](pruned-coordinate-grid.md). In
principle, given a candidate and a trial physical margin `gamma`, one can
apply that exact optimizer to

```
F(x)-F(v)-gamma||x-v||^2.
```

If `0<gamma<g_E`, this auxiliary quadratic has the same unique optimizer
and positive growth `g_E-gamma`; its exact minimum zero independently
certifies the proposed margin. Suitable trial budgets handle an unknown
valid margin. The present construction avoids that general exact-recovery
machinery and obtains its direct arithmetic grid count. Neither finding
the candidate nor deciding every nonunique or incorrect candidate is
claimed. The earlier preordering obstruction is compatible with this
different certificate family.

## 4. Targeted checks performed

An inline Python `fractions.Fraction` diagnostic checked three fixtures:
an asymmetric convex signed box, a nonoptimal KKT corner with negative
curvature and positive axis endpoint increments, and a purely linear
objective. At `delta=1/2` it computed the corrected normalized-grid minimum
by enumeration and verified the claimed certificate and radial inequality
at 69 rational points. It also checked the exact diagonal-variance identity
over 163 independent rounding atoms.

The incorrect KKT fixture produced a negative certificate quantity, as it
must. The linear fixture gave `sigma=1/16` and `b_delta=13/16`, confirming
that the endpoint-increment scale handles zero curvature. These finite
checks complement the proof and do not establish the general complexity
bound. The author's sparse-DP diagnostic is separate; no project-wide
verification or CI inspection was performed here.
