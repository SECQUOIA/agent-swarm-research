# Second independent audit of maximum dissipation over a resistance polytope

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-global-energy-maximization.md) has the stated exact second-order cone formulation and polynomial-bit additive algorithm returning an exactly admissible rational resistance profile on arbitrary connected graphs. Its relative-interior argument covers lower-dimensional resistance polytopes. The appended rational certificate for global design quality is also valid. No exact SOCP threshold-decision or general rational-optimum claim is needed or implied.

## 1. Physical energy and conjugate duality

For fixed positive beta, the primitive energy is differentiable, strictly convex, and coercive on the nonempty affine conservation space. Its unique minimizer is the physical flow. Its gradient is `beta_e x_e |x_e|`. Equality-constrained stationarity places this gradient in the range of the incidence transpose, giving a potential vector, unique modulo a constant on the connected graph.

The scalar conjugate calculation is correct. At a drop d, maximizing `d x-beta |x|^3/3` gives signed optimizer `sign(d)sqrt(|d|/beta)` and value `(2/3)|d|^(3/2)/sqrt(beta)`. Zero d gives zero optimizer and zero conjugate. The physical potential attains equality in every Fenchel inequality, so it gives an attained dual optimum and proves strong duality directly. No inequality-constraint Slater condition on the flow space is being assumed.

The incidence identity at the physical state gives

```
b^T pi=sum_e x_e (A^T pi)_e=sum_e beta_e |x_e|^3=3V(beta).
```

Thus the factor of three is correct throughout. The conjugate is a convex perspective of `|d|^(3/2)` in `(d,beta)`, so the dual objective is jointly concave. Maximization over beta and the dual potentials can be combined without a minimax interchange: both are maximizations, and for each fixed beta the attained inner value is V(beta).

Maximum attainment over P follows, for example, from continuity of V. The uniform physical-flow bound gives `|V(beta)-V(beta')|<=(B^3/3)||beta-beta'||_1` by evaluating each energy at the other's minimizer. Compactness of P then gives an optimizing profile.

## 2. Exact cone projection, including zero cases

With all of z, u, t nonnegative and beta positive, the two inequalities are rotated second-order cones. They have rational ordinary SOC representations; for example `z^2<=tu` is equivalent to `||(2z,t-u)||_2<=t+u`. No irrational coefficient is required.

If z is positive, combining the two inequalities gives `z^4<=t^2 u^2<=beta z t^2`, hence `z^3<=beta t^2`. Conversely this last inequality with z positive forces t positive, and the rational expression `u=z^2/t` satisfies both cone inequalities. If z is zero, u zero works for every t nonnegative. If t is zero, the inequalities force z and u both zero. These are all boundary cases.

Since z bounds the absolute potential drop, eliminating z and u yields exactly `t>=sqrt(|d|^3/beta)`. For the reverse direction select `z=|d|` and the preceding u. The lifted formulation is therefore exact, rather than only a relaxation.

At a physical state, the proposed values

```
z=beta |x|^2, u=beta |x|, t=beta |x|^3
```

satisfy both cone inequalities at equality and give the exact conjugate. They also handle x zero. Hence the optimal conic value is precisely the maximum V, and its triple is maximum dissipation.

## 3. Bounds and relative-interior construction

Positive physical flows form an acyclic orientation because their potential drops are positive. Path decomposition bounds their magnitudes by total positive nomination and hence by B. Along a path from the fixed reference vertex, each absolute drop is at most `beta_U B^2` and the path has at most m edges. This proves the displayed physical-potential bound. The z, u, t bounds follow from their exact physical formulas. These arguments do not require a cactus, bounded cycle rank, or a special orientation of the input graph.

Set `r=min(1,beta_L)/2`. It is positive and rational. At the proposed artificial interior point, `tu-z^2=1` and `beta z-u^2>=beta_L-r^2>0`. If `beta_L<=1`, then `r^2=beta_L^2/4<beta_L`; if `beta_L>=1`, then `r^2=1/4<beta_L`. Also z strictly exceeds either signed drop at pi zero, and z, u, t are positive. Enlarging upper coordinate bounds beyond both a physical optimizer and this interior point, and adding one to the potential bound, preserves an optimizer while making this point strict in the added bounds. All quantities have polynomial rational encoding even if beta_L or the nominations are very small.

A relative-interior beta point is obtained with rational LPs. For each defining inequality, maximize its slack over P. Zero optimum means it is an equality throughout P. Every other inequality has a rational positive-slack witness of polynomial bit length. Averaging all such witnesses gives positive slack for every non-universal inequality simultaneously. Each resulting positive rational slack has a polynomial-bit lower bound; no facet enumeration is needed.

The universally tight rows define the affine hull. Gaussian elimination gives polynomial-bit rational coordinates on it. One can choose the free coordinates as a subset of the original beta coordinates, so their explicit beta bounds immediately bound them; a general rational injective parametrization also has a polynomial-bit rational left inverse. A singleton P leaves no free beta coordinates and causes no failure.

After this elimination and removal of the fixed reference potential, all remaining defining inequalities are strict at the displayed rational point. The transformed inequalities have degree at most two and polynomial-bit coefficients. On a rational unit neighborhood of the center, explicit coefficient bounds bound their gradients. Dividing each positive slack by a suitable gradient bound, and taking a positive rational minimum smaller than one, gives a computable inner radius of polynomial bit length. This justifies the claimed full-dimensional ball in the reduced space without assuming numerical conditioning of P. Coordinate bounds and the rational transformation give an outer radius with polynomial encoding too.

The bounded feasible set is convex because the quadratic inequalities are conic inequalities with the required nonnegative coordinates; arbitrary quadratic sublevel sets are not being presumed convex. It is closed and bounded, hence compact, and contains the physical global optimizer.

## 4. Polynomial-bit optimization and rational scenario recovery

At rational points, membership is decided by rational linear and quadratic comparisons, so there is an exact membership oracle and therefore a weak membership oracle. The negative of the conic objective is a globally Lipschitz linear function with an explicit rational norm bound. The center and inner and outer radii supply the required convex-body representation.

I reread Dadush's Theorem 2.5.9, printed page 48, and the preceding input-length convention. It supplies a rational point inside the convex body with the stated additive objective guarantee; its time is polynomial in the lengths of the input bounds. This is the exact feasibility property needed here. [Primary thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf).

Applying the theorem with error epsilon/3 gives an exactly feasible rational conic point. The affine map sends its free coordinates to a rational beta in the original P exactly. Its conic objective is a lower bound on V(beta), because t may overestimate the conjugate but never underestimate it. Consequently

```
D(beta)=3V(beta)>=3(conic objective)>=max_P D-epsilon.
```

This step does not require the chosen potentials to be the physical potentials, or the chosen conic variables to lie on their boundary. It also does not require solving the physical state at the returned profile. The computed lower bound itself proves the desired one-sided physical guarantee.

The proof avoids general exact conic-feasibility or exact-threshold assertions. Its special feasible set has an explicitly known interior ball after affine-hull reduction, and the requested objective guarantee is additive. The returned physical state need not be rational, and an exact rational optimizing beta need not exist in all instances.

## 5. Appended exact rational global certificate

Write P as `R beta<=c`. For a rational conserved trial flow y, set `w_e=|y_e|^3/3`. Its trial energy bounds the physical primitive energy from above: `V(beta)<=beta^T w`. If rational `lambda>=0` satisfies `R^T lambda=w`, LP weak duality gives `beta^T w<=c^T lambda=U` for every beta in P. Hence U is a global upper bound on the maximum V, not just a bound for one scenario.

For a feasible rational beta0, normalized rational pi, and nonnegative rational t satisfying `beta0_e t_e^2>=|(A^T pi)_e|^3`, the same conjugate argument gives `L=b^T pi-(2/3)sum t<=V(beta0)`. Thus

```
max_P D-D(beta0)<=3(U-L).
```

All stated checks are rational, including the absolute cubes. The certificate claims sufficiency of these inequalities; it does not assume that an arbitrary trial y will give a small gap.

The triangle example is exact. Its trial half-flows conserve the unit nomination, and each coefficient w equals 1/24. The sum-resistance equality gives U=6/24=1/4. At beta0 `(3/2,3/2,3)`, the half-flows give drops `(3/8,3/8,3/4)`, agreeing with the proposed potentials. The t values sum to 3/4, and `b^T pi=3/4`, so L=1/4. The equality constraint can be represented by two inequalities with multiplier 1/24 on its upper direction and zero on its lower direction; all bound multipliers may be zero. This is a literal rational zero-gap certificate with maximum dissipation 3/4.

## 6. Exact diagnostics and scope

Added and ran [the independent checker](../code/potential_flow_mpd/global_energy_maximization_second_review.py). It passed 180 projected cone cases, 1,080 necessity controls, five strict-interior constructions including resistance bounds of size `2^-80` and `2^80`, and 84 exact complete-graph physical states with 1,008 edge conjugate/cone witnesses. Checks include zero drops, node conservation, the factor of three, and every displayed physical coordinate bound. These identities supplement the proof; the checker is not an SOCP optimizer.

Additional physical capacity or potential constraints are excluded. The mathematical dissipation equals the chosen potential difference under unit terminal nominations; if a process model uses squared pressure, it does not thereby become literal compressor power. Source priority remains a separate question because conjugacy, perspectives, and general convex optimization are established mechanisms. No correction is required.

## Addendum: exact capacity filters on a cactus

The subsequently added cactus corollary passes. The [global-correlation arc theorem](review-potential-flow-global-correlation-arc-validation-second.md) converts the specified rational physical arc capacities into rational affine inequalities in the original resistances, with exact equivalence at every profile. Fixed bridge violations and empty filtered domains are rejected. The remaining `P_cap` is a nonempty bounded rational polytope and inherits the original strictly positive resistance bounds.

Apply the conic algorithm with `P_cap` as its input polytope, recomputing its affine hull and relative-interior point. Capacity equality or additional dimension loss does not invalidate the interior-ball argument because that argument already works relative to an arbitrary input polytope. The physical flow and potential bounds are unchanged, and all new inequalities have polynomial encoding length.

The returned rational resistance profile lies exactly in `P_cap`, so its actual passive state satisfies all capacities exactly. The conic potential variables need not themselves describe that physical state; the capacity guarantee comes from the equivalent parameter inequalities. The same dual lower-bound reasoning gives dissipation within epsilon of the maximum over the filtered domain. If using the global quality certificate, its polytope matrix and right-hand side must describe `P_cap`, so the certified upper bound targets this same filtered maximum.

This is a direct composition of two reviewed proofs. The general-graph theorem remains unfiltered, and no affine-capacity characterization or potential-bound result is inferred for arbitrary graphs. No additional numerical test or correction is needed for this corollary.
