# Second independent audit of fixed-support weighted tree optimization

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-fixed-support-weighted-tree.md) proves an exact rational algorithm with running time `N^{O(p)}` for fixed objective support, arbitrary finite rational nomination boxes intersected with balance, and independent interval or finite resistance choices. The proof covers zero flows and degenerate nomination domains. This is a correctness audit, not an independent novelty determination.

## 1. Objective reduction and contraction

On an oriented tree, the incidence map is a bijection from edge flows to balanced nominations. Consequently both `Aw=c` and `Ax=b` have unique solutions, and

```
c^T pi=sum_e w_e beta_e x_e|x_e|.
```

Every retained edge flow and weight is a signed sum on an edge cut. Contracting edges with zero weight preserves these cut sums exactly when nominations and objective coefficients are summed over each contracted cluster. Thus it preserves the weighted objective and the retained flows. This argument does not identify the original potentials inside a cluster; those potentials generally differ, and will be reconstructed on the original tree afterward.

The image of an independent product of closed real intervals under summation is the full summed interval. Hence cluster aggregation is exact for the complete feasible nomination set, including shifted boxes, singleton coordinates, and boxes whose balanced intersection has empty relative interior in the balance hyperplane. A rational aggregate value can be disaggregated by starting at all lower bounds and distributing its residual through the available upper-minus-lower capacities. This uses only rational arithmetic. Resistances on zero-weight edges have no objective effect and do not affect tree flows.

If the retained tree has an edge, it has at least two leaves. Each leaf has nonzero aggregated objective coefficient, because its incident weight is nonzero. Therefore there are at most `p` leaves and at most `p-2` vertices of degree at least three. Marking these branching vertices and all nonzero objective vertices gives at most `2p-2` marks and at most `2p-3` intervening paths. An internal unmarked vertex has degree two and coefficient zero, which makes the consistently oriented cut weight constant and nonzero along its path. The zero-objective case, including support below two under `sum c=0`, is handled directly before these bounds are used.

## 2. Complete nomination-face family

For fixed positive resistances, the perturbed weighted objective is

```
F_rho(b)=sum_e w_e beta_e (x_e|x_e|+rho*x_e),
```

where `x` is linear in `b`. For balanced perturbations `delta b=A delta x`, define `h` by

```
A^T h=(w_e beta_e(2|x_e|+rho))_e.
```

This system always has a solution on a tree, unique modulo constants, and gives `delta F_rho=h^T delta b`. The displayed gradient differences in the candidate therefore have the correct sign. They are strictly monotone along every suppressed path, including at zero physical flow, because `rho>0` and all resistances are positive.

At a constrained maximizer, differentiability implies that `h` belongs to the normal cone of the box intersected with balance. The normal cone formula for a polyhedron supplies a common balance multiplier `lambda` and the asserted endpoint rules. It needs no strict feasibility assumption. Coordinates with equal lower and upper bounds may be assigned either endpoint status without changing their value. Along a strictly monotone path, at most one internal gradient can equal `lambda`; coordinates before and after that possible equality are fixed to the prescribed opposite endpoint types.

For a path with `k` internal coordinates, `k` possible free-coordinate placements and `k+1` cuts suffice. When a gradient equals `lambda` but its coordinate is already at an endpoint, the corresponding free-coordinate face still contains the nomination. If no gradient equals `lambda`, a cut face contains it. Marked coordinates can independently be designated lower, upper, or free. It is harmless that many enumerated combinations cannot arise from a common multiplier: they add feasible faces but do not omit the one containing a smoothed maximizer.

For `M` marked vertices and `P` paths, the face count is bounded by

```
3^M product_paths (2k_path+1)
    <=3^(2p-2) (2n+1)^(2p-3).
```

Each face has at most `M+P<=4p-5` free coordinates before balance. Imposing balance and any further forced equalities can only lower the dimension.

For fixed resistances, bounded nomination boxes imply bounded tree flows, so `F_rho` converges uniformly to `F_0`. The face family is finite and independent of `rho`. From smoothed maximizers as `rho` tends to zero, select a subsequence in one fixed face and then a convergent subsequence in the compact nomination domain. The face is closed; uniform convergence makes the limit a global maximizer of `F_0`. This argument establishes existence of an optimal nomination in the family, rather than claiming that every unperturbed maximizer has a strict threshold pattern.

The joint resistance step is also valid: choose an attained joint optimum `(b*,beta*)`, freeze `beta*`, and apply the preceding argument. Its replacement nomination on an enumerated face cannot improve beyond the joint optimum and achieves that value at `beta*`. No uniform perturbation argument over a nonconvex finite resistance set is needed. Compactness of either the finite sets or the closed bounded intervals supplies the initial joint optimum.

## 3. Endpoint elimination and sign cells

For each nomination, tree flows are independent of resistance. The objective is separately linear in each resistance, so selecting the largest allowed value when `w_e x_e|x_e|>=0` and the smallest otherwise is exact. Both extrema are feasible members of an interval or an explicitly listed finite set. Consequently no enumeration of all resistance corners is needed.

On each nomination face, flow coordinates are affine rational functions of at most `4p-5` variables. Hyperplanes where retained flows vanish partition its feasible polytope into `N^{O(p)}` sign cells. It suffices to keep closures of full-dimensional cells relative to the polytope's actual affine hull: every feasible point is a limit of such cells. Identically zero flow functions are excluded from the arrangement; a zero-dimensional feasible set is evaluated directly. This treatment is necessary for singleton balanced domains and faces collapsed by balance, and is explicitly included in the candidate.

Within a sign cell, both the sign of `x_e|x_e|` and the optimal resistance endpoint are fixed, making the objective rational quadratic. Shared boundaries cause no discrepancy because contributions from vanishing flows are zero. The feasible sign cells remain bounded rational polyhedra.

## 4. Exact rational quadratic optimization

The stationary-system enumeration is correct even when the quadratic is indefinite or singular. A global maximizer `z*` lies in the relative interior of its minimal polyhedral face. Its gradient is orthogonal to the direction space of that face. A basis of active inequality normals therefore gives a subset `I` of at most the ambient dimension such that

```
Az*<=d,  A_I z*=d_I,  Qz*+g=A_I^T mu*.
```

The algorithm enumerates this subset. It does not need multiplier signs, negative semidefiniteness checks, or a claim that every stationary point is a maximum. Every feasible solution returned is a point of the original polytope, so its value cannot exceed the global optimum.

More importantly, an arbitrary feasible solution of the same system as `z*` attains the same objective. If `(z,mu)` and `(z',mu')` solve one fixed system and `v=z'-z`, then

```
A_I v=0,  Qv=A_I^T(mu'-mu),
v^T Qv=0,  v^T(Qz+g)=0,
q(z')-q(z)=v^T(Qz+g)+(1/2)v^T Qv=0.
```

This is the key step justifying rational optimizer recovery from linear feasibility, including a continuum of stationary solutions. Rational linear feasibility has a polynomial-bit rational solution whenever feasible; unboundedness in the multiplier variables does not invalidate that statement. Thus one arbitrary feasible solution per stationary system suffices for an exact global maximum comparison.

## 5. Complexity, recovery, and evidence

The nomination-face count has exponent `O(p)`. In dimension `d=O(p)`, both the arrangement cell count and the number of active-normal subsets have exponent `O(d)`. Multiplying these counts adds their exponents and still gives `N^{O(p)}`; there is no hidden exponent exponential in `p`. Each resulting linear system has `O(p)` variables and polynomially many inequalities. Rational cut summation, affine-hull computation, Gaussian elimination, and coefficient substitution have polynomial-bit data for fixed `p`. This establishes the stated fixed-support polynomial bound, without asserting a bound of the form `f(p)N^C`.

The winning nomination disaggregates rationally. Endpoint resistance choices are rational allowed values. Original flows are rational cut sums, and original potentials are rational sums of quadratic edge drops after one reference potential is fixed. These operations retain polynomial binary output length. Replacing `c` by `-c` proves the minimum statement with unchanged support.

No additional flow or pressure constraints may be inserted into this argument: they would generally destroy the simple nomination-face normal cone or the resistance elimination. No cycle may be introduced while retaining the tree flow-independence argument. The candidate states these limits correctly.

The proof was audited independently of the numerical checks. I reran `fixed_support_weighted_tree_checks.py` using the project Python environment: 3,119 feasible stationary candidates over five tree cases, 30 exact rational contraction checks, and four quadratic controls passed. The supplied stationary checks use floating-point systems and therefore support the formulas without implementing the claimed exact bit algorithm.
