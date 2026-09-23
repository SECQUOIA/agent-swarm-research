# Sharper rational edge-flow intervals from the energy certificate

Date: 2026-09-05. Status: verified support refinement; independent mathematical and checker audit passed. This is an application of the established Bregman divergence of a convex energy, not a standalone novelty claim.

Formal verification follow-up (2026-09-20): [Lean topic 16](../formal/topics/16-potential-flow-certificates/COVERAGE.md) proves the deterministic Bregman intervals, rational bisection accuracy, pressure-objective enclosures, and scenario-recovery bounds conditional on the stated coefficient and selection hypotheses. It reuses [topic 03](../formal/topics/03-potential-flow/COVERAGE.md) for the energy certificate. The original uncertainty-to-envelope mapping, Python implementation and bit-complexity claims remain outside these proofs.

Use the deterministic asymmetric-quadratic energy, rational conserved flow `y`, and certified energy gap `delta` from the [rational certificate result](potential-flow-envelope-rational-certificates.md). Let `x*` be the exact physical flow.

## 1. Each edge has its own certified interval

For one edge, define the reverse Bregman term

```
D_e(y,z)=E_e(y)-E_e(z)-g_e(z)(y-z).
```

Physical stationarity and exact conservation give

```
E(y)-E(x*)=sum_e D_e(y_e,x*_e)<=delta.
```

Every summand is nonnegative by convexity, so each is at most `delta`. For fixed `y`, the function `z->D_e(y,z)` is continuous, strictly decreasing for `z<y`, and strictly increasing for `z>y`. For the asymmetric quadratic law, away from zero,

```
partial D_e(y,z)/partial z = 2 c_e^sign(z) |z| (z-y).
```

The derivative can vanish at zero without destroying strict monotonicity on either side of `y`. Therefore rational endpoints `L_e<=y_e<=U_e` satisfying

```
D_e(y_e,L_e)>=delta,
D_e(y_e,U_e)>=delta
```

certify `x*_e in [L_e,U_e]`. At `delta=0`, use `L_e=U_e=y_e` directly.

These bounds are verified by exact rational cubic arithmetic. Starting from the already certified common radius `eta`, its stronger scalar inequality `D_e(y,z)>=beta_L|y-z|^3/6` shows that `y_e-eta,y_e+eta` are valid outer endpoints. Bisection on each side, keeping an outside point with `D>=delta`, locates each interval boundary to any rational dyadic accuracy in polynomial bit time; the compatible interval itself need not become arbitrarily narrow at a fixed energy gap. This is univariate monotone root isolation and does not require solving the physical system again.

Away from a zero flow, the Bregman term grows quadratically in the displacement, so this interval can be much narrower than the uniform cube-root energy radius. Near zero, the cubic behavior remains correctly represented.

## 2. Certifying the original endpoint scenario more tightly

Suppose this deterministic instance has independently been established as the appropriate quadratic envelope for a target edge, with original interval endpoints `Lbeta_e,Ubeta_e`. Select resistances from the sign of `y` and the envelope rule. Define

```
a_e=max(0,-L_e)  if y_e>=0,
a_e=max(0, U_e)  if y_e<0.
```

Whenever this endpoint choice disagrees with a choice realizing the envelope at `x*_e`, the true flow magnitude is at most `a_e`. The constitutive residual at `x*` is therefore bounded by

```
r_e=(Ubeta_e-Lbeta_e) a_e^2.
```

Let `x'` be the physical flow in the selected original scenario. The same circulation and strong-monotonicity argument as in the reviewed recovery proof yields

```
||x'-x*||_infinity^2 <= (2/beta_L) sum_e r_e.
```

An upward rational square-root enclosure gives a certified target-edge flow suboptimality bound for the original scenario. This improves the earlier uniform estimate by using only intervals that allow a mistaken flow sign. If all intervals certify a consistent sign, every `a_e` is zero and the original selected resistance scenario attains the exact envelope optimum, even though the physical state and its objective value may remain irrational.

No universal polynomial-time exact scenario recovery is asserted: if a relevant envelope flow is exactly zero or extremely small, these posterior intervals may not establish a strict sign at a prescribed precision. The result certifies what the supplied numerical approximation actually resolves.

The scalar interval verifier concerns the deterministic energy instance. As with the base certificate, the original uncertainty interpretation requires a separately verified graph/target/envelope mapping.

The later [original-instance certificate pipeline](../notes/potential-flow-certified-envelope-pipeline.md) implements and independently verifies that mapping. Its [conservation-aware goal certificates](../notes/potential-flow-goal-oriented-certificates.md) can further tighten a target interval without another physical-flow solve. The base certificate and Bregman formats retain their deterministic-instance scope.

## Prototype and achieved intervals

[`envelope_bregman_bounds.py`](../code/potential_flow_mpd/envelope_bregman_bounds.py) uses only the Python standard library and the base rational verifier. On the [saved exact energy certificate](../code/potential_flow_mpd/envelope_certificate_example.json), it verified six rational edge intervals whose maximum width is less than `2.9e-6`, compared with the earlier uniform width about `3.41e-4`. All six intervals exclude zero. The maximum certified envelope edge-pressure interval width is less than `4.0e-6`. These are certified enclosures, not comparisons against a numerical reference state.

The certificate interpretation remains conditional on the independently checked deterministic envelope mapping. Given that mapping, all six resolved signs would certify an exactly optimal original endpoint scenario. The saved JSON alone does not encode or verify the original uncertainty data.

The prototype rejects a deliberately undersized Bregman interval, including when executed with `python -O`. All interval validation uses unconditional checks. Run

```
python -O code/potential_flow_mpd/envelope_bregman_bounds.py code/potential_flow_mpd/envelope_certificate_example.json
```

The bounds are stored and checked as exact fractions inside the program. Printed decimal widths are rounded summaries; the slightly larger decimal bounds stated above are conservative.

## Other deterministic pressure objectives

The same verified flow intervals give each edge a pressure-drop interval `[g_e(L_e),g_e(U_e)]`. Summing these intervals with the appropriate orientation signs along any fixed path yields a rational enclosure of its terminal potential difference. More generally, express a zero-sum weighted potential objective along a fixed spanning tree as `sum_e w_e g_e(x_e)` and apply signed interval arithmetic to the edge-drop intervals. This certifies that deterministic physical objective even on a non-series-parallel graph. It does not supply an uncertainty-envelope theorem for such an objective; the graph-dependent robust reduction remains separate.

## Independent verification

The [independent full audit](../notes/review-potential-flow-envelope-bregman-certificates.md) passed. Its separate [checker](../code/potential_flow_mpd/check_envelope_bregman_review.py) passed 50 signed and zero-gap physical states, 339 malformed-bound rejections, and 60 exact residual inequalities under both normal and optimized Python. The audit checked divergence decomposition, boundary directions, outward bisection, conditional original-scenario flow recovery, and the deterministic-versus-uncertainty scope.
