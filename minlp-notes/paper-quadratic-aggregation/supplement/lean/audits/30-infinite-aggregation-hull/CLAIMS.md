# Topic 30 frozen claims

Status: complete. These obligations were fixed from the
source inventory, independently of proof convenience.
The [coverage map](COVERAGE.md) links all eight to proved declarations,
the independent reviews record semantic review, and the
verification record records the targeted checks.

For every integer `r≥2`, write `x=(u,v)∈R^r×R^r`,
`S={x : u·u<1 ∧ v·v<1 ∧ 1/2<u·v}`, and
`T={x : u·u≤1 ∧ v·v≤1 ∧ 1/2≤u·v}`. Set
`p=1-u·u`, `q=1-v·v`, and `d=u·v`. All inner products are Euclidean.
Let `H=convexHull ℝ S` and `C=closure H`. Good multipliers use the
source-level predicate already verified in topic 29.

| ID | Required conclusion |
|---|---|
| H01 | Define the original weak system, the strict formula `p>0 ∧ q>0 ∧ d+sqrt(p*q)>1/2`, the weak formula `p≥0 ∧ q≥0 ∧ d+sqrt(p*q)≥1/2`, and the actual affine symmetric lift `L(x,sigma)=[[1,sigma,uᵀ],[sigma,1,vᵀ],[u,v,I_r]]`. Prove agreement of any reindexed or block representation with these formulas and the existing strict system and aggregate. |
| H02 | Prove the exact ordinary-hull formula `H={x : p>0 ∧ q>0 ∧ d+sqrt(p*q)>1/2}` for every `r≥2`, including `r=2`. Both inclusions must concern the actual ordinary convex hull of `S`. Any decomposition, extreme-point argument, or general theorem needed for sufficiency must be proved or imported as an already proved theorem; a new BDS theorem premise is not acceptable. |
| H03 | Prove the exact strict SDP representation `H={x : ∃sigma>1/2, L(x,sigma) is positive definite}`. Establish the required Schur-complement or equivalent block-quadratic argument for the actual matrix, including the exact strict inequalities. |
| H04 | Prove that the weak formula is exactly `{x : ∃sigma≥1/2, L(x,sigma) is positive semidefinite}`. Include singular cases `p=0` or `q=0` and both signs of `sigma-d`; a determinant condition without diagonal conditions is insufficient. |
| H05 | Prove `C={x : p≥0 ∧ q≥0 ∧ d+sqrt(p*q)≥1/2}` and hence the closed SDP representation. Derive the closure equality, including approximation of every weak-feasible point by strict-hull points; do not assume that replacing strict inequalities by weak ones always commutes with closure. |
| H06 | Prove `convexHull ℝ T=C`. Establish the compactness/closedness or an equivalent argument needed for the reverse inclusion; merely showing `S⊆T⊆C` is insufficient. |
| H07 | Prove `H={x : ∀lambda, Good(lambda) → aggregate(lambda,x)<0}`. Use the actual spectral and hull-containment good-multiplier predicate. For sufficiency include coordinate rays and every positive ray `(tau,1/tau,2)`, and justify attainment of the minimizing parameter when the strict diagonal slacks are positive, or give an equivalent complete cone argument. |
| H08 | Prove `C={x : ∀lambda, Good(lambda) → aggregate(lambda,x)≤0}`. Handle zero diagonal slacks and limiting positive-ray parameters; the strict-intersection result alone does not establish this weak-intersection result. |

No quantitative approximation, coefficient-size, single-objective,
arbitrary-quadratic impossibility, countable closed-family sufficiency,
or general Gram-map conclusion is frozen here. A general hull theorem may
be a proved dependency, but proving a conditional version without
discharging its hypotheses does not satisfy H02–H08.
