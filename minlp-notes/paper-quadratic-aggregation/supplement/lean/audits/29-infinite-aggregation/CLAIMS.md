# Topic 29 frozen claims

Status: complete. These obligations were fixed from the
source inventory, independently of proof convenience.
The [coverage map](COVERAGE.md) links all 12 to proved declarations; the
verification record records the completed checks.

For an integer `r≥2`, write `x=(u,v)∈R^r×R^r`,
`f(x)=(u·u-1,v·v-1,1/2-u·v)`, and `S={x : ∀i, f_i(x)<0}`.
Inner products are Euclidean sums. A good multiplier is a nonzero
nonnegative triple `lambda` whose actual homogeneous aggregate matrix has
at most one negative eigenvalue, counted with multiplicity, and whose
strict aggregation contains the ordinary convex hull of `S`.
Set `K={lambda≥0 : lambda_3²≤4 lambda_1 lambda_2}` and
`rho(tau)=(tau,1/tau,2)` for `tau∈[1,2]`.

| ID | Required conclusion |
|---|---|
| I01 | Define the actual strict three-inequality system, its homogeneous quadratic map, original and homogeneous aggregation, and ordinary convex hull. Prove agreement between any pair-vector, matrix, or reindexed representation and these Euclidean formulas. Define good multipliers using the original spectral and hull-containment conditions. |
| I02 | Prove `S` is nonempty and bounded for every `r≥2`, and its ordinary convex hull is proper. A concrete strict witness is `u=v=sqrt(3/4)e_1`. Bounds must concern the actual feasible points; no hull formula is assumed. |
| I03 | Prove actual HHC: every linear homogeneous hyperplane has a convex image under `(u·u-t²,v·v-t²,t²/2-u·v)` for every `r≥2`, including `r=2`. Derive any Gram realization, hyperplane feasibility, range, or concavity facts used; none may be supplied as a new headline premise. A proved equivalent route to HHC is acceptable. |
| I04 | Prove that the homogeneous aggregate matrix, up to coordinate permutation, has repeated block `B_lambda=[[lambda_1,-lambda_3/2],[-lambda_3/2,lambda_2]]` with `r` copies and scalar block `lambda_3/2-lambda_1-lambda_2`. Relate any chosen inertia representation to the count of negative eigenvalues of this actual symmetric matrix. |
| I05 | For nonzero nonnegative multipliers, prove `B_lambda` is PSD exactly when `lambda_3²≤4 lambda_1 lambda_2`. Outside this cone, the actual homogeneous matrix has at least two negative eigenvalues because `r≥2`. Inside it, its scalar block is strictly negative and it has exactly one negative eigenvalue. The multiplicity and degenerate boundary cases must be handled. |
| I06 | Prove the exact classification `Good(lambda) ↔ lambda∈K ∧ lambda≠0`. For the forward direction discharge the spectral obstruction; for the reverse direction prove convexity of the aggregate and strict negativity on the ordinary convex hull, not merely on `S`. Do not assume a general good-aggregation hull theorem. |
| I07 | For every `tau∈[1,2]`, construct actual vectors in `R^r` with Gram matrix `[[1-(1/10)/tau,2/5],[2/5,1-(1/10)tau]]`. Prove the necessary strict positivity/realizability including endpoints, and `f(x_tau)=(1/10)(-1/tau,-tau,1)`. A Gram matrix without actual vector realization is insufficient. |
| I08 | For every nonzero good multiplier, prove `f_lambda(x_tau)≤0`, with equality exactly when `lambda=a rho(tau)` for some `a>0`. Prove `rho(tau)` is good, `x_tau` is outside the ordinary hull, and every good multiplier on another positive ray is strictly satisfied there. |
| I09 | For any family of good multipliers whose strict aggregation intersection equals the ordinary convex hull, prove that for every `tau∈[1,2]` some family member is a positive multiple of `rho(tau)`. The hypothesis must be the actual set equality, not an assumed witness-selection condition. |
| I10 | Prove distinct parameters in `[1,2]` give distinct positive rays and deduce that every exact strict good-aggregation description contains uncountably many distinct rays. In particular no finite or countable such family describes the ordinary hull. A conclusion only about repeated indices is insufficient. |
| I11 | Given an arbitrary finite family of good multipliers, choose an omitted `rho(tau)` and construct an actual perturbed Gram witness by decreasing the off-diagonal `2/5` by a sufficiently small positive `eta`. Prove the Gram matrix remains realizable, every selected aggregation remains strictly negative, and the omitted aggregation is strictly positive. An equivalent explicit finite-family witness construction is acceptable. |
| I12 | Prove that every good aggregation is nonpositive on `closure(convexHull S)`, and use I11 to show that no finite intersection of their weak inequalities equals that closed hull. Keep the strict ordinary-hull and weak closed-hull statements distinct. Do not assume that a weak intersection is the closure of the corresponding strict intersection. |

The package excludes the exact hull formula; proving existence of an exact
strict good-aggregation representation via the full BDS hull theorem;
countable dense-family sufficiency for the closed hull; equality with the
hull of the original weak system; the finite SDP lift; impossibility of
arbitrary quadratic descriptions; approximation rates and bit bounds;
single-objective results; the general sharp Gram-map theorem; and novelty
or conjecture-priority claims. None of these exclusions weakens I01–I12.
