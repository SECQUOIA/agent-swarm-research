# Joint continuous-resistance and weighted-potential optimization on cacti

Date: 2026-09-06. Status: passed two independent full mathematical reviews; a focused open-literature comparison found no matching combined theorem. This result supplies the missing resistance-elimination step for the [fixed-dimensional nomination-family investigation](../notes/potential-flow-reopened-weighted-investigation.md) and composes it with the separately reviewed nomination-face theorem for unrestricted balanced boxes at fixed objective support. Internal review and a bounded source search do not establish external peer review or exhaustive priority clearance.

## Theorem

Fix `d`. Let `G` be a connected cactus with quadratic passive laws `A^T pi=beta_e x_e|x_e|`, independent positive rational resistance intervals `[L_e,U_e]`, nominations `b=b0+Hz` on a nonempty compact rational polytope `P` in `R^d`, and a rational objective `c^T pi` with `sum c=0`. Assume the nomination family is balanced. For positive rational epsilon, joint maximization and minimization over nominations and resistances have certified rational optimum intervals of width at most epsilon and rational epsilon-optimal original parameter scenarios in time polynomial in the input bit length and `max(0,log(1/epsilon))`, for fixed `d`.

The number and length of cycles and the support of `c` are unrestricted. Resistances are continuous and independent; operating constraints and discrete resistance choices are excluded from this main theorem. This is an accuracy-bit complexity result, not an assertion that a complete exact optimizer has been implemented. Section 6 composes the separately reviewed fixed-support nomination-face theorem with this theorem. Section 7 adds local arc capacities to the fixed-dimensional model with algebraic feasible output.

Take `0<epsilon<=1`; for larger tolerances run with `min(epsilon,1)`.

## 1. Weighted objective separates by blocks at fixed nominations

Choose a spanning tree, orient each cactus cycle consistently, and write its edge flows as `x_e=q+ell_e(z)`, with rational affine `ell_e`. Bridges have affine flow. Expressing normalized potentials along the spanning tree gives

```
c^T pi = sum_e w_e beta_e x_e|x_e|,
```

where the rational weights `w_e` are fixed by `c` and the tree, with zero weight on chords. After reversing an edge orientation, reverse the corresponding objective weight. Every cycle has its own scalar circulation and resistance coordinates; its sole compatibility equation is `sum_e beta_e x_e|x_e|=0`. Thus, for fixed `z`, the joint maximum is the sum of independent local cycle maxima and bridge maxima. The resulting edge drops integrate to a global potential because they satisfy all fundamental-cycle equations.

A rational polynomial-bit bound `M` on total positive nominations bounds every physical edge flow. Take a rational box for `P`; a sufficiently large constant bound `|q|<=R` follows from `q=x_e-ell_e(z)`. If the particular-flow convention makes a chord's offset zero, `R=M` suffices. These artificial bounds contain every physical state and make each local feasible set compact.

## 2. Eliminate all cycle resistances using a one-equality linear program

On a closed sign cell for the affine flows, put `f_e(z,q)=s_e(q+ell_e(z))^2`, where `s_e` is the chosen sign. At zero either sign is valid. For fixed `(z,q)`, the local problem is

```
maximize sum_e w_e f_e beta_e
subject to sum_e f_e beta_e=0,   L_e<=beta_e<=U_e.
```

For a scalar multiplier `lambda`, nonzero reduced costs `(w_e-lambda)f_e` select the maximizing resistance endpoint. Set `lambda` equal to any distinct edge weight `w_j`. Let `T={e:w_e=lambda}`. For `e` outside `T`, choose the upper endpoint when `(w_e-lambda)s_e>0` and the lower endpoint otherwise; at a zero flow either choice gives the same contribution. Denote these fixed endpoints by `hat beta_e`. Define

```
S = sum_(e outside T) hat beta_e f_e,
lo_T = sum_(e in T) min(L_e f_e,U_e f_e),
hi_T = sum_(e in T) max(L_e f_e,U_e f_e).
```

The min and max endpoints are determined by the sign cell. This threshold branch is feasible exactly when

```
S+lo_T<=0<=S+hi_T.                              (1)
```

Both are rational quadratic inequalities in `(z,q)`. On that domain the exact optimal objective is the quadratic polynomial

```
Q_lambda(z,q)=sum_(e outside T)(w_e-lambda)hat beta_e f_e.  (2)
```

Indeed, the tied coordinates can supply every value in `[lo_T,hi_T]`; equality of the aggregate then subtracts the entire `lambda` term from the objective. Every chosen coordinate maximizes its reduced-cost term, so this feasible profile attains the Lagrangian upper bound.

Conversely, whenever the LP is feasible, some threshold branch attains its optimum. Its convex piecewise-linear dual function is

```
D(lambda)=sum_e max_(L_e<=beta<=U_e) (w_e-lambda)f_e beta.
```

All breakpoints are among the finitely many weights of edges with `f_e!=0`. A dual minimum exists: outside the extreme breakpoints the function is affine, and feasibility prevents it from decreasing without bound. A minimum in an unbounded flat tail also reaches its boundary breakpoint. Consequently a minimum occurs at an edge weight unless all `f_e` vanish. In that exceptional case every threshold branch is feasible and has value zero. Box-LP strong duality now gives (1) and (2) for at least one threshold. Multiple tied weights cause no exponential enumeration because their whole interval of aggregate contributions is retained.

The affine flow hyperplanes have polynomially many realizable sign cells in fixed dimension `d+1`. Each cell and each distinct weight generate one threshold domain. Taking closures adds only valid physical states, since the signed law agrees at zero. Their union represents every local optimum.

## 3. Reduce each circulation optimization to polynomially many explicit candidates

On one closed threshold domain, maximize its quadratic `Q(z,q)` over `|q|<=R`, the sign inequalities, and (1). For fixed `z` this is a compact one-dimensional semialgebraic set. A maximum occurs at one of the following:

1. A boundary point where a nonconstant-in-`q` domain polynomial vanishes. Include the artificial bounds `q=+-R` among these boundaries.
2. A stationary point `partial Q/partial q=0`, when the coefficient of `q^2` in Q is nonzero.
3. A stratum on which Q is independent of q and the domain is nonempty.

All domain polynomials have form

```
a q^2+b(z)q+c(z),
```

with rational constant `a`, affine `b`, and quadratic `c`. Linear sign constraints are included. If `a!=0`, enumerate both roots `q=(-b+-sqrt(Delta))/(2a)`, `Delta=b^2-4ac`; substitution into Q gives

```
P(z)+L(z)sqrt(Delta(z)),                         (3)
```

with rational quadratic P and affine L. The sign in (3) is absorbed into L. Unlike a direct optimization with variable resistance inside the original quadratic root, the denominators here are fixed nonzero rational constants.

If `a=0`, on `b(z)!=0` the boundary point is `q=-c(z)/b(z)` and Q becomes a bounded-degree rational function with denominator `b(z)^2`. On `a=b(z)=0` that polynomial either imposes no q boundary or makes the domain infeasible; it supplies no candidate, and the other boundary/stationary/flat cases still cover every maximum. No division by a vanishing coefficient occurs. The stationary candidate is rational affine, since the q-quadratic coefficient of Q is constant. If that coefficient is zero, add the stratum where the affine q-linear coefficient is zero, and project domain nonemptiness; Q there is its q-independent polynomial part.

The exact z-domain of each candidate is obtained by eliminating one q from its defining root equation, a branch-selector inequality when needed, and all original domain inequalities. For the plus root of a quadratic with leading coefficient a the selector is `2aq+b>=0`; for the minus root it is `2aq+b<=0`. At a double root both are harmless. Rational candidates impose `b!=0`. Fixed-dimensional elimination of bounded-degree rational polynomials produces polynomial-size domain descriptions with polynomial coefficient encoding. A flat candidate uses only existential domain nonemptiness and needs no explicit q formula.

There are polynomially many candidates over all cycles. A candidate is always a feasible local value. The maximum of their values on their valid domains is exactly the local optimum. The local circulation itself need not be unique after resistance optimization.

## 4. Compile the maximum of local candidates before summing

Use the elementary rational piecewise-polynomial square-root approximation from the fixed-law investigation on every radical in (3). All quadratic-root denominators are constant, so bounding `|L(z)|` on the rational box for P gives polynomial-bit uniform error budgets. Choose individual tolerances so the sum of local value errors is at most `epsilon/16`. Rational candidates remain exact, with explicit nonzero denominator domains.

For each candidate and every eligible square-root panel, retain the rational surrogate formula and its domain. Collect all exact candidate-domain polynomials, panel-boundary polynomials, bridge flow-sign hyperplanes, and P's inequalities. Also collect rational comparison numerators between every pair of surrogate pieces belonging to the same cycle, together with the denominators needed to determine signs. There are polynomially many such pieces and pairs. Their degrees and encoding lengths are polynomial in the input and accuracy bits.

Decompose P into a common sign-invariant semialgebraic partition in fixed dimension. On each cell, candidate eligibility and pairwise surrogate comparisons are constant. Choose a maximizing eligible surrogate for each cycle. Such a candidate exists because every resistance box admits a physical state for every balanced nomination. For bridges choose the resistance endpoint maximizing the weighted drop, with the choice determined by its flow sign and fixed weight. The sum of the selected local surrogates is one rational function on that cell.

If every local candidate is approximated within eta, the maximum over them is approximated within eta as well; no separation between competing values is needed. The true value of the candidate selected by maximizing the surrogate can fall below the true local optimum by at most `2 eta`, since both the maximizing true candidate and the selected candidate incur approximation error. Allocate the error budget to include this second loss when returning a scenario. Consequently the summed rational surrogate uniformly approximates the true joint optimum conditional on z. This avoids exact comparisons of radical sums and avoids enumerating combinations of cycle choices.

Optimize the rational surrogate cell by cell by fixed-dimensional real quantifier elimination and rational threshold bisection. Denominators have explicit nonzero conditions; open cells may use a supremum and a near-maximizing algebraic sample. The physical objective is uniformly bounded and each surrogate has the proved uniform error, so no unbounded supremum is introduced by a denominator approaching zero. The partition includes all lower-dimensional boundaries. This yields a rational interval for the true joint optimum and a polynomial-size algebraic parameter sample whose actual selected candidate scenario is within the requested intermediate error budget.

## 5. Recover original resistances and rational parameters

For each selected local candidate at the algebraic z sample, recover its q by its defining degree-at-most-two equation. In a flat branch recover any feasible q by one-dimensional real-algebraic sampling. For its selected threshold, the non-tied resistances already equal rational endpoints. The tied ones solve the one-row box LP `sum_T beta_e f_e=-S`. Starting at the lower contribution of every tied interval and filling the required residual in a fixed edge order gives a feasible solution with at most one resistance away from an endpoint. Edges with zero f need no division and can use L_e.

Each cycle is processed separately over the algebraic z sample and its own bounded-degree local q extension. It is unnecessary to form a common field containing all cycle roots. Each recovered coordinate has a polynomial-size algebraic description, so certified coordinate isolation to any polynomial number of bits is available. These independent coordinates together form a physical scenario, because every cycle equation and the global conservation equations hold.

Round the shared z sample by rational linear programming inside P intersected with a fine rational isolating box. Round each resistance inside its original rational interval. No semialgebraic candidate-domain membership must be preserved: the rounded original parameters induce their own unique physical network state.

To control objective loss, apply the nomination continuity estimate from the fixed-law investigation uniformly over `beta<=beta_U` and the reviewed resistance perturbation estimate from the [rational-witness and perturbation result](../results/potential-flow-capacity-rational-witness-boundary.md). For fixed nominations with total positive nomination bounded by M, resistance perturbation `||beta'-beta||_infinity<=delta` implies

```
||x'-x||_infinity <= 2m M delta/beta_L,
|c^T(pi'-pi)| <= ||c||_1(n-1) M^2 delta
    (1+4m beta_U/beta_L).
```

Together with the nomination bound, this gives a polynomial-bit rational choice of rounding widths with total objective loss below the remaining epsilon budget. If M is zero the objective is identically zero. Because only P and independent resistance intervals constrain the original parameters, rational rounding preserves exact feasibility. Apply the same construction to `-c` for minimization.

## 6. Full balanced nomination boxes at fixed objective support

The independently reviewed [weighted nomination-face reduction](../notes/potential-flow-reopened-weighted-face-reduction.md) is independent of resistance values. Fix a support bound p and let the original nominations range over an arbitrary nonempty rational box intersected with balance. Its objective-preserving pruning and zero-block contractions yield a reduced cactus, and its finite graph-only face family has polynomial size with `O(p)` free nomination coordinates on each face.

Choose a global joint maximizer and hold its resistance profile fixed. The structural theorem supplies an equally good nomination on one of those faces. Thus the same face family contains a joint maximizer when all surviving resistance intervals remain variable. Apply the main theorem to each face with `d=O(p)`, compare its certified additive values, and retain a candidate with the required overall error. Rationally disaggregate reduced nominations and choose any rational allowed resistance on contracted or pruned blocks. Their objective coefficients vanish in the precise translation sense established by the structural proof, so this lifting preserves the objective. This proves polynomial accuracy-bit joint weighted optimization, certified rational optimum intervals, and rational epsilon-optimal original nomination/resistance scenarios for fixed p and unbounded total cactus cycle rank.

This composition has no operating filters. The fixed-dimensional affine-family theorem permits arbitrary objective support; the unrestricted balanced-box corollary fixes the objective support instead. Neither statement asserts exact equality-sensitive threshold decisions for the objective.

## 7. Local arc capacities: algebraic feasible output and qualified rational recovery

In the fixed-dimensional affine-family theorem, rational lower and upper edge-flow bounds add affine inequalities in `(z,q)` on a cycle and in z on a bridge. These preserve every local LP and boundary-candidate degree bound. The local candidate domains now also encode feasibility. A common z-cell is globally feasible exactly when each cycle has an eligible candidate and every bridge capacity holds. Consequently feasibility can be decided exactly, and when feasible the constrained optimum has certified additive rational value intervals and polynomial-size **algebraic** epsilon-optimal original z and resistance output. No full-box fixed-support composition is claimed here: its pruning and face arguments require unfiltered nomination boxes.

Tight capacity filters can force irrational nomination parameters even with fixed resistances, as the four-edge cactus example in the fixed-law investigation shows. Therefore unconditional rational exact-feasible output is not claimed. For practical rational output, take a supplied positive rational common slack sigma, and optimize with each signed capacity interval tightened by sigma at each end. Assume this tightened feasible set is nonempty. If z and resistance rounding change nominations by `Delta_b` in one-norm and resistances by at most delta in infinity norm, the combined flow change is at most

```
Delta_b/2 + 2m M delta/beta_L.
```

Choose polynomial-bit rounding widths so this is at most `sigma/2`, while the objective loss remains within its epsilon budget. The returned rational parameters are exactly feasible for the original capacities and epsilon-optimal **relative to the tightened optimum**. No relation between the tightened and original optima is asserted without an additional margin assumption. Cross-cycle potential constraints and globally correlated resistances are outside this corollary.

## 8. Fixed rational nominations: exact rational optimizing resistance profiles

For fixed rational nominations, arbitrary rational weighted potential objectives, independent positive rational resistance intervals, and optional rational signed arc capacities on a cactus, feasibility can be decided and, whenever feasible, an **exactly optimizing rational resistance profile** can be computed in polynomial bit time. No bound on objective support or cycle count is needed. Each local optimum value has algebraic degree at most two over the rationals; the global optimum may be retained as a sum of local algebraic values. A polynomial-size single algebraic-field representation or exact rational-threshold comparison of that global sum is not claimed.

To prove the strengthened output statement, set `d=0` in the local construction. All offsets, objective coefficients, sign endpoints, capacity endpoints, and artificial q bounds are rational. A stationary circulation of a nonflat quadratic objective is therefore rational. A boundary circulation arising from a flow-sign, capacity, or artificial-bound constraint is also rational. At every rational feasible q, all f coefficients are rational and the one-row tied-resistance LP recovers rational resistances of polynomial bit length.

The only possible irrational boundary circulations come from the two aggregate feasibility quadratics `S+lo_T=0` or `S+hi_T=0`. At the first boundary, the tied aggregate must equal its minimum possible contribution; every tied edge with nonzero f must therefore take the corresponding minimizing resistance endpoint. At the second boundary all nonzero tied contributions take their maximizing endpoints. Zero-f edges can use either rational endpoint. The non-tied resistances already are rational endpoints. Thus this case also yields a rational original resistance profile, even though the induced physical circulation is irrational. When both aggregate bounds coincide, either endpoint construction is valid.

If the local objective is flat in q, choose a boundary of its nonempty compact feasible q-set instead of an arbitrary semialgebraic sample. At least one nonconstant domain polynomial is active there, because the artificial q bounds ensure boundedness. This returns to the same rational-q or aggregate-boundary classification. Degenerate identically-zero domain polynomials do not supply a boundary and are omitted as in Section 3.

There are polynomially many candidates on each cycle, all with rational or quadratic-algebraic objective values. Comparing two such values uses a field of degree at most four, or ordinary constant-degree root isolation; therefore a local exact winner can be selected in polynomial bit time. Every recovered rational resistance coordinate has polynomial encoding length, since it is an endpoint or is obtained by rational arithmetic from a stationary or rational-boundary q and the one-row LP. On bridges, feasibility is checked directly and an objective-maximizing rational resistance endpoint is chosen. The independently chosen local exact winners integrate into a global physical state and a rational exact optimizing resistance profile. Replace c by -c for minimization.

This corollary is more directly implementable than the varying-nomination theorem: its algorithm needs only sorting, rational arithmetic, quadratic roots, and exact comparisons of pairs of constant-degree algebraic numbers. It does not require parameter-space quantifier elimination. The existing single-cycle capacity linearization and cactus rational feasibility result are prior ingredients; the claim here adds arbitrary weighted-objective exact optimization and its rational optimizing resistance witness.

### A weighted optimum can require an interior resistance

Consider an oriented four-edge cycle with nominations `b=(0,0,3,-3)`, using incidence with outgoing flow positive. Its flows are `x=(q,q,q+3,q)`. Let the resistance intervals be

```
beta_1 in[1,4], beta_2 in[1,3], beta_3 in[1,4], beta_4 in[1,5],
```

and take `c=(2,-3,-2,3)`. The edge-drop representation has weights `w=(2,-1,-3,0)`, since c is their incidence. Every physical circulation lies strictly between -3 and 0. On this sign interval, the LP dual threshold `lambda=-1` gives the uniform upper bound

```
c^T pi <= -4q^2-2(q+3)^2 = -6(q+1)^2-12 <= -12.
```

The bound is attained at `q=-1` and `beta=(1,2,1,1)`: the original signed edge drops are `(-1,-2,4,-1)`, their cycle sum is zero, and their weighted sum is -12. Equality in the upper bound forces `q=-1`. The strictly nonzero reduced costs at that point force `beta_1=beta_3=beta_4=1`, and the original cycle equality then forces `beta_2=2`. Thus the maximizing resistance profile is unique and has an interior second coordinate. No resistance-box corner attains the optimum.

This exact example explains the need for the circulation-stationary and tied-resistance recovery cases. An endpoint-only search, although sufficient for some prescribed-arc envelope problems under their assumptions, does not solve arbitrary weighted potential optimization. The example was proposed during the first independent review and checked separately by the investigating and coordinating agents.

## Boundaries and literature comparison

The resistance LP elimination uses continuity of each interval. It does not extend to discrete sets: tied contributions then need not fill an interval, and the existing one-cycle weighted hardness already rules out that unrestricted extension.

The local-capacity corollary uses fixed-dimensional nominations and algebraic feasible output. Cross-cycle resistance correlations destroy the separability used in Section 1.

The approximation and real-algebraic tools are established methods. The contribution proposed for a paper is the network combination: arbitrary weighted objectives, fixed-dimensional affine nominations, independent continuous resistance uncertainty, unbounded cactus cycle count, polynomial accuracy-bit complexity, and rational scenario recovery, together with the separately justified balanced-box and fixed-nomination corollaries. The one-row LP threshold reduction is elementary linear-programming duality, not a standalone novelty claim.

The [focused source comparison](../notes/potential-flow-reopened-weighted-literature.md) credits the direct predecessors. [Gotzes, Heitsch, Henrion, and Schultz (2016), Theorem 6](https://www.wias-berlin.de/people/heitsch/GHHS16_Preprint.pdf), gives piecewise quadratic-radical or rational cycle circulation along affine nomination rays and explicitly extends its methodology to node-disjoint cycles with attached trees. Local radical formulas and affine load slices are therefore established prior work. [Aßmann, Liers, Stingl, and Vera (2018)](https://arxiv.org/pdf/1808.10241) treats independent resistance intervals, robust feasibility, and single-cycle circulation restrictions expressed polyhedrally in resistance coefficients. [Vigneron's approximation framework](https://repository.kaust.edu.sa/items/263bf642-8d1d-4244-9714-7d40a0f4f70c) is a predecessor for optimization of sums of algebraic functions; its cited complexity is polynomial in inverse epsilon, whereas the present scoped theorem is polynomial in accuracy bits. The source comparison also credits joint load/friction uncertainty models and the existing internal fixed-core machinery. None of the inspected sources states the complete combined guarantee proved here. This remains a bounded priority search.

## Independent mathematical review

The [first full audit](../notes/review-potential-flow-reopened-joint-weighted.md) and [second full audit](../notes/review-potential-flow-reopened-joint-weighted-second.md) independently reviewed the resistance LP, tie aggregation, complete circulation candidate list and degenerate strata, polynomial approximation and partition complexity, algebraic scenario recovery, rational rounding, full-box face composition, and scoped capacity output. Both passed. Each separately checked the final fixed-nomination exact rational-profile corollary. Their review scripts independently enumerate original box-plane LP vertices: the first passed 203 cases, and the second passed 400 cases plus 1,000 exact quadratic-root substitution identities. These scripts do not use the author's threshold implementation.

## Reproducible local mechanism checks

[`reopened_joint_weighted_checks.py`](../code/potential_flow_mpd/reopened_joint_weighted_checks.py) compares the threshold formula and reconstructed primal scenario with exhaustive one-free-coordinate box-LP vertex enumeration in exact rational arithmetic. All 216 cases passed, including 66 feasible cases, tied weights, singleton intervals, zero individual flows, and all-zero flows. Every feasible threshold attained the same exact optimum as the independently enumerated vertices.

The script separately enumerates local circulation boundary and stationary candidates in floating-point arithmetic on 90 cycles, then compares their maximum with 15,036 physical scenarios generated by independently solving the strictly increasing original cycle equation, including all box corners and random interior resistance profiles. Maximum numerical exceedance was `1.83e-13`. This second check exercises both-root quadratic candidates and flat objectives; it is not an exact optimality certificate or an implementation of global parameter-space optimization. The checks use the standard library and explicit exceptions, so remain active under `python -O`.

## Exact fixed-nomination implementation

[`exact_weighted_cactus.py`](../code/potential_flow_mpd/exact_weighted_cactus.py) implements the fixed-nomination corollary using only the Python standard library. It accepts explicit coherent cycle offsets and objective weights, resistance intervals, local rational flow bounds, and fixed-flow bridges. It returns exact optimal rational resistances, separate quadratic circulation/objective encodings, and a certified rational interval for the total value. Both maximum and minimum are supported. The [implementation note](../notes/potential-flow-exact-weighted-cactus-solver.md) documents the input format, exact arithmetic, independent review, and the interior-resistance example.

This is a block-input solver: it does not accept or verify a full original graph-to-block mapping. It also does not implement the joint uncertain-nomination parameter-space optimizer proved above. Exact independent LP, quadratic arithmetic, orientation-invariance, capacity, and schema checks cover the implemented fixed-nomination scope.
