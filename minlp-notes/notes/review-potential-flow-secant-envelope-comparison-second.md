# Second independent audit of finite secant envelope comparison

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-secant-envelope-comparison.md) gives a valid finite comparison identity and a structural envelope theorem for continuous strictly increasing laws. It can replace the homotopy and smoothing argument in the reviewed quadratic result. It makes no computational claim for general compact parameter families.

## Exact identity

Write `delta x=y-x`, `delta pi=rho-pi`, and `R=diag(r)`. The chosen secants satisfy

```
A delta x=0,       A^T delta pi=R delta x+d
```

exactly, including coordinates where `delta x_e=0`: there the secant resistance may be any positive number. With `L=A R^-1 A^T`, the second equation implies `L delta pi=A R^-1 d`. Therefore an adjoint `Lh=e_u-e_v`, `j=R^-1 A^T h`, gives

```
delta pi_u-delta pi_v=h^T L delta pi=j^T d.
```

The target coordinate of the second equation then gives

```
r_a delta x_a=j^T d-d_a
                =sum_{e!=a} j_e d_e-(1-j_a)d_a.
```

The identities hold on arbitrary connected graphs. The graph restriction is needed only for signs independent of the positive secant resistances. The usual unit electrical flow from the tail to the head of the target has `0<j_a<=1` for a nonloop target; the weaker displayed bound `0<=j_a<=1` is sufficient. A bridge gives `j_a=1` and all other adjoint currents zero, consistently making its flow independent of laws at fixed nominations.

## Continuous laws and envelope attainment

Strict increase and `g(0)=0` imply positive values at positive arguments and negative values at negative arguments. Its primitive `F(t)=integral_0^t g(s)ds` is strictly convex and coercive: for `t>=1`, it grows at least linearly with slope `g(1)>0`, and for `t<=-1` it grows at least linearly with slope magnitude `-g(-1)>0`. Thus the finite sum of edge primitives has a unique minimizer on the nonempty affine conservation space. Differentiable convex stationarity supplies the physical potentials. No unbounded range or positive derivative of the law is needed.

Compact parameter spaces and joint continuity give continuous, attained minimum and maximum laws. Their strict increase follows from two distinct selections: choose a maximizing member at the smaller argument for the maximum envelope, and a minimizing member at the larger argument for the minimum envelope. These arguments remain valid for arbitrary compact parameter spaces; convexity of the family and parameter independence within an edge are unnecessary. Both envelopes vanish at zero and have the same coercivity property.

In the comparison from an original scenario to the proposed maximizing envelope network, `d_a<=0`. For each other edge, `sigma_e d_e>=0`, and `j_e` has the fixed sign `sigma_e`. Every term in the target identity is consequently nonnegative. Reversing the envelope choices proves the lower bound. An envelope law need not be a member of the original family. At its physical flow, however, choose independently on each edge a member matching the one required scalar law value. The envelope flow and potentials then solve the original chosen scenario exactly; uniqueness proves attainment of the entire physical state.

## Graph and nomination scope

For a target edge in a graph without a `K4` minor, all adjoint currents outside its biconnected block vanish. Within the block, its endpoints are valid two-terminal series-parallel terminals. Current signs are invariant under positive resistances, either by induction on series/parallel composition or by the classical confluence theorem. The bridge case is immediate. Eppstein's Lemma 9 explicitly permits the endpoints of any existing edge as terminals of a biconnected series-parallel graph. [Primary source](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf). Duffin's discussion of confluence and its electrical meaning supplies the classical sign comparison mechanism. [Primary source](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf).

The envelope law profile is independent of the nomination vector. The original parameter selection realizing its state may depend on that vector. Thus the same envelope network represents the pointwise extremum for every nomination, but the result does **not** promise one original scenario that attains the extremum for all nominations at once. This distinction is necessary even for a triangle: let the target law be chosen from `t` and `t^3`, and let its alternate two-edge path have total linear resistance one. For positive unit demand the cubic target law maximizes target flow; for demand four the linear target law does. The pointwise minimum target envelope handles both.

Optimization over a compact nomination set is legitimate. Physical flows of the fixed envelope network depend continuously on balanced nominations. One direct argument minimizes its strictly convex coercive energy, uses a fixed linear right inverse of the incidence matrix to perturb feasible competitors, and passes to limits of minimizers; bounded nominations give bounded comparison energies and hence bounded minimizers. Uniqueness identifies every subsequential limit. Thus target extrema on a compact nomination set are attained, and a realizing original scenario can be selected at an optimizing nomination. This reasoning does not make the nomination optimization computationally easy.

For pressure between arbitrary terminals on a cactus, the block-cut path contains all nonzero adjoint currents. Its bridges carry a fixed-direction unit flow; each cycle splits flow into its two terminal paths, both in fixed directions. All other edges carry zero. Applying `delta(pi_s-pi_t)=j^T d` with maximum laws on positive-sign edges and minimum laws on negative-sign edges proves the stated pressure corollary and its reverse. This corollary does not require the terminals to be adjacent.

## Verification and limits

The audit derived both finite identities and checked existence, continuity, strict increase, attainment, and sign scope independently. I reran `secant_comparison_checks.py` in the project Python environment: all 240 finite target-arc identities passed on series-parallel and `K4` networks, with maximum discrepancy `8.03e-15`. Compactness supplies the stated attained envelopes and original-state realization; independence is required between edges. Neither semialgebraic representation nor an envelope oracle is available for arbitrary compact families, so no new bit-time assertion follows. Novelty of the elementary secant proof device has not been established by this review.
