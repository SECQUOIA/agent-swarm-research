# Independent review of joint weighted cactus optimization

Date: 2026-09-06. Reviewer: independent `review_weighted` agent. Reviewed source: [joint continuous-resistance and weighted-potential optimization](potential-flow-reopened-joint-weighted.md).

**Verdict: pass for the fixed-dimensional affine-nomination theorem, its composition with the reviewed fixed-support nomination-face lemma, and the local-capacity corollary.** I audited the new resistance elimination and recovery argument separately; this conclusion is not inherited from the earlier fixed-law review. Accuracy should be stated as rational `0<epsilon<=1`, replacing larger tolerances by one. This is an internal mathematical review, not a novelty determination or implementation benchmark.

## What is new in the proof obligation

The earlier square-root compiler alone cannot handle the original quadratic cycle root with variable leading coefficient and arbitrarily many resistance variables. The present argument correctly eliminates the resistance variables first. On each cycle sign region, a one-equality box LP reduces the problem to finitely many scalar-circulation quadratic optimization problems whose quadratic leading coefficients are rational constants. Their candidate values fit the previous compiler.

This is a substantive reduction. A generic appeal to fixed-dimensional optimization of the original problem would not work because the original resistance dimension is unbounded.

## Conditional separation and physical feasibility

Cactus cycles are edge-disjoint. Once nominations are fixed, each circulation changes only its own cycle flows. A spanning-tree potential reconstruction writes the weighted objective as a sum of local weighted drops with fixed rational weights. Loop equalities make these drops globally integrable, and conservation already holds in the affine-flow representation. Thus independently chosen locally feasible cycle states and bridge resistances combine into a physical network state. There is no unrepresented compatibility condition between cycles.

Every physical edge flow is bounded by total positive nomination, uniformly over the positive resistance box. The artificial rational circulation bounds therefore preserve all feasible original states and make the scalar local domains compact. This compactness matters for the candidate-completeness proof, including a q-independent objective.

## Threshold LP, ties, and zero flows

An equivalent LP uses signed drops `y_e=beta_e f_e`, with bounds

```
min(L_e f_e,U_e f_e) <= y_e <= max(L_e f_e,U_e f_e),
sum_e y_e=0,
objective = sum_e w_e y_e.
```

This makes the threshold rule transparent. For a multiplier equal to an edge weight, every larger-weight drop takes its upper bound and every smaller-weight drop takes its lower bound. The tied drops need only supply one prescribed aggregate. A sum of closed intervals fills the interval between the sums of their endpoints, so the two stated quadratic inequalities are necessary and sufficient. Eliminating the tied aggregate yields precisely the stated quadratic objective `sum_(outside T)(w_e-lambda) hat_beta_e f_e`.

Every feasible threshold branch attains the same LP optimum at a fixed `(z,q)`, because it reaches a Lagrangian upper bound. Every feasible LP has such a threshold: its finite convex piecewise-linear dual achieves a minimum at a breakpoint, including the endpoint of a flat unbounded tail. If all `f_e` vanish, all drops and objective contributions are zero and every threshold is feasible. Zero-flow edges outside the tied set need no special endpoint enumeration; their contribution vanishes whichever endpoint is selected.

Equal weights can occur on arbitrarily many edges. Aggregating their whole contribution interval handles this degeneracy without an exponential choice of tied endpoints. Fixed resistances `L_e=U_e` cause no additional difficulty.

## Completeness of the local candidate list

At fixed `z`, a threshold domain is a nonempty compact subset of the q interval defined by finitely many univariate degree-at-most-two inequalities. A maximizer of its quadratic objective is a feasible-set boundary point or an interior stationary point, unless the objective is constant in q. Every boundary point is a zero of an active domain polynomial that is not identically zero as a polynomial in q at that parameter. Artificial interval endpoints are included among these polynomials.

Each domain polynomial has a constant rational q-quadratic coefficient, an affine q-linear coefficient, and a quadratic constant term. Both quadratic roots must be included, and the draft does so. The selector `2aq+b>=0` selects the plus-square-root formula for either sign of `a`; the opposite inequality selects the minus formula. The selector would be wrong if interpreted as a physical monotonicity condition here, but the draft uses it only to label roots.

If the quadratic coefficient is zero and the linear coefficient vanishes at the parameter, that polynomial has no isolated q boundary. Other active polynomials, the stationary case, or the flat case still cover the maximum. The rational candidate explicitly excludes a zero linear denominator. If the objective has zero quadratic coefficient, only the stratum with zero q-linear coefficient needs a flat candidate. Its value is the q-independent quadratic part, and projecting domain nonemptiness gives the exact domain of validity.

These observations also cover isolated feasible q points, repeated roots, lower-dimensional sign strata, and a domain that changes the number of connected components with z. No genericity or positive separation hypothesis is required.

## Projection, approximation, and ordering complexity

There are polynomially many realized flow-sign cells in fixed dimension `d+1`. Each has at most one threshold branch per distinct edge weight, polynomially many boundary-root candidates, one stationary candidate, and a flat candidate when applicable. All local projections eliminate one q while retaining only the fixed parameter dimension. Their degrees and rational coefficient sizes satisfy the standard fixed-dimensional elimination bounds checked in [the earlier independent review](review-potential-flow-reopened-weighted.md).

Substitution of a quadratic candidate into the local quadratic objective gives one polynomial plus an affine multiplier times a square root of a quadratic polynomial. The nonzero quadratic denominator is a fixed rational constant. Linear candidates instead give bounded-degree rational functions with explicit nonzero denominator domains. Thus the established rational square-root panel construction applies without needing a lower bound on a variable reciprocal.

The further pairwise comparison step is sound. There are polynomially many rational surrogate pieces per cycle, hence polynomially many pairs. Rational comparison numerators and denominator signs form polynomial-size input to a common decomposition in fixed `d`. Candidate eligibility and surrogate ordering then remain constant on each stratum. This replaces exact comparisons of algebraic candidate values by comparisons of rational surrogates with certified uniform error. It also avoids enumerating a Cartesian product of choices across cycles.

Dense coefficient expansion remains polynomial because the parameter dimension is fixed. Surrogate degrees grow polynomially with requested precision. Clearing or multiplying denominators adds their degrees rather than multiplying degrees exponentially, and the number of monomials in fixed dimension is polynomial in the resulting degree. Coefficient bit lengths grow polynomially under these products and sums.

For a fixed parameter, perturbing each candidate value by at most eta perturbs its cycle maximum by at most eta. Selecting the candidate that maximizes the surrogate can lose at most `2 eta` relative to the true best candidate. Both facts are needed: the first certifies the global value interval, and the second certifies the recovered original scenario. With total local surrogate error `E<=epsilon/16`, global surrogate optimization error `xi`, and final rounding loss `r`, the recovered true scenario loses at most `2E+xi+r`. The proposed budgets can therefore be made explicit, for example `xi<=epsilon/4` and `r<=epsilon/4`, leaving loss below epsilon.

## Algebraic recovery without a common field

The global algebraic sample has only fixed-dimensional parameter coordinates, so it has a polynomial-size joint algebraic representation. Each selected nonflat circulation adjoins a root of degree at most two to that parameter field. A flat branch is a univariate bounded-degree semialgebraic sampling problem over that field and also has polynomial representation complexity. There is no reason to form the compositum of the different cycles' root fields.

For the selected threshold, greedy filling of the tied contribution intervals recovers exact balance and leaves at most one tied resistance strictly inside its interval. Dividing a recovered contribution by its nonzero `f_e` is valid local algebraic arithmetic; when `f_e=0`, an interval endpoint is used instead. Even a very small nonzero algebraic divisor has polynomially describable inverse because its local degree and coefficient encoding are polynomial. Exact sign tests and coordinate isolation can be performed separately in each cycle's field.

The recovered coordinates combine into a feasible original scenario at the common parameter sample. Independent coordinate isolation then supports rational rounding inside every original resistance interval and rational LP rounding of parameters inside the original polytope. The rounded physical flows are recomputed implicitly by the original network; they need not preserve any chosen candidate chart or circulation value.

## Continuity estimates for rational rounding

A conservative resistance Hölder bound, independent of the sharper linear estimate used in the final draft, is also sufficient and correct. Energy monotonicity gives

```
(beta_L/2) sum_e |h_e|^3 <= delta M^2 sum_e |h_e|,
```

where `h=x'-x`. Since `sum|h_e|<=m||h||_infinity`, the claimed square-root bound follows. The induced pressure bound follows by applying the `2M` Lipschitz estimate for `x|x|` on each edge of a path. Squaring a rational target accuracy still costs only a linear factor in accuracy bits, so this weaker modulus does not threaten polynomial bit complexity.

I also checked the newer linear resistance-flow estimate in [the operating-constraints note](potential-flow-reopened-operating-constraints.md). Orienting the difference circulation positively yields a directed cycle through a maximum-flow edge whose other edges have difference at least `||h||_infinity/m`. Otherwise a reachable-set cut contradicts circulation balance. On this cycle, the scalar inequality `f(x+h)-f(x)>=h|x|/2` holds through sign changes, and summing constitutive differences proves `||h||_infinity<=2mM delta/beta_L`. Its associated linear pressure bound can replace the conservative modulus without changing the algorithm or its scope.

Combining resistance continuity with the earlier graph-independent nomination Lipschitz bound controls simultaneous rounding. All constants are uniform on the compact input boxes and have polynomial rational encoding. Zero total nomination gives identically zero physical flows and objective. Exact feasibility after rounding follows because the theorem imposes only the original rational parameter polytope and independent resistance intervals; it does not impose operating constraints.

## Composition with fixed-support nomination faces

The [weighted nomination-face lemma](potential-flow-reopened-weighted-face-reduction.md) has a separate independent review. For its composition here, the essential fact is that its finite family of rational faces is independent of resistance values.

The joint maximum exists on the compact nomination and resistance set. Fix the resistance vector of one joint maximizer. The face lemma supplies a nomination on an enumerated face with objective at least as large for those fixed resistances. That nomination and resistance vector remain a joint maximizer. On a cactus with fixed objective-support bound, each enumerated face has a fixed number of free coordinates and is exactly the affine-polytope input form of the joint theorem. Maximizing the certified intervals over the polynomially many faces, and selecting a witness with a controlled interval-selection loss, proves the fixed-support joint result.

The support-free pruning and zero-adjoint-block contractions also preserve this joint conclusion: one can choose arbitrary admissible rational resistances in removed blocks when lifting the rounded reduced scenario. Their objective contributions vanish under the corresponding potential translations. Nomination disaggregation is rational and respects the original boxes. For minima, apply the face construction and optimization to `-c`.

This composition does not preserve scenario-filtering capacities or potential bounds. It gives no result for discrete resistance sets, cross-cycle correlations, or general bounded-rank blocks beyond cacti.

## Local-capacity corollary

The added signed arc-capacity bounds are affine in each local `(z,q)` representation. They therefore preserve the one-equality resistance LP, quadratic candidate degree, and fixed-dimensional projection. Compactness ensures a local maximizing candidate exists whenever the local capacity-filtered problem is feasible. Thus exact feasibility can be decided by intersecting projected eligible-candidate domains, even though the objective value itself is approximated. Bridge capacities are imposed directly. The algebraic output and bounded local field arguments remain valid.

The supplied-slack recovery claim also passes. First vary nominations at fixed resistance, then resistances at the new nomination. The uniform bounds give total edge-flow change at most `||Delta b||_1/2+2mM delta/beta_L`. Rounding the parameters inside P and resistance boxes sufficiently finely therefore preserves the original capacities after optimization over the nonempty tightened-capacity problem. The objective guarantee is correctly relative to that tightened optimum. Arbitrarily tight capacities need not admit rational parameters, and the draft explicitly declines unconditional rational recovery. The unrestricted-box face composition is correctly excluded from this corollary.

## Independent exact checks

I wrote [an independent exact checker](../code/potential_flow_mpd/check_reopened_joint_weighted_review.py), comparing threshold/tie aggregation against exhaustive vertex enumeration of the original one-equality box LP. Running `python code/potential_flow_mpd/check_reopened_joint_weighted_review.py` passed all 203 instances: 74 feasible and 129 infeasible. Cases include all-zero flows, zero individual flows, equal weights, fixed resistance coordinates, and feasible tie groups of size four.

For every feasible threshold, the checker also verifies the recovered resistance bounds, exact cycle equality, equality of the recovered original objective and the eliminated formula, and at most one nonendpoint tied resistance. Exhaustive vertex search is an independent finite LP solution method; it does not reuse the threshold dual argument.

These checks target the new resistance-elimination mechanism. The global candidate-completeness and algebraic-complexity conclusions rest on the proof audit above, not on a numerical claim that the complete optimizer has been implemented.

## Addendum: exact rational optimizer at fixed rational nominations

The later Section 8 corollary also **passes independent review**, including optional rational signed arc capacities. This is stronger than rounding a near-optimizer and needs the separate endpoint classification given there.

When nominations are fixed rational numbers, every flow offset is rational. Nonflat stationary q candidates are rational because the objective polynomial has rational coefficients and degree at most two. Sign, capacity, and artificial-box boundary candidates are rational as well. At any such feasible q, the threshold LP has rational data and its greedy tied-coordinate recovery is rational with polynomial bit length.

An irrational candidate can therefore only be a root of an aggregate-feasibility quadratic. When `S+lo_T=0`, each tied contribution must attain its lower interval endpoint, because their sum is at its minimum. When `S+hi_T=0`, every tied contribution attains its upper endpoint. Thus the resistance coordinates are rational box endpoints even though the physical circulation is irrational. In fact no flow is zero at an irrational q when every offset is rational. The note's provision for zero-flow edges is harmless and makes the endpoint rule cover rational cases too.

For a flat objective, the separate instruction to select a feasible-domain boundary is essential and valid. A nonempty compact subset of the real line has a boundary, and an active nonconstant domain polynomial defines it. This returns to the preceding classification. Arbitrarily sampling a flat domain would only guarantee an algebraic witness; the stated boundary choice proves the stronger rational claim.

Every candidate value is rational or quadratic algebraic. Exact comparison of two candidates requires only constant-degree algebraic arithmetic, so an exact local winner can be selected in polynomial bit time. Independent local winners combine into a global optimizing rational resistance profile. This does not require evaluating or comparing the exact sum of all local optima against a rational threshold. A sum representation of the global objective is enough, and the claimed limitation concerning the global radical sum is correct.

### An exact optimum requiring an interior resistance

The following example was found during this independent audit. It shows why the stronger rational optimizer theorem cannot be reduced to testing resistance box corners.

Take a consistently oriented four-cycle with

```
x=(q,q,q+3,q),
b=(0,0,3,-3),
beta_lower=(1,1,1,1),
beta_upper=(4,3,4,5).
```

Use weighted drops `w=(2,-1,-3,0)`, equivalently the balanced potential objective `c=(2,-3,-2,3)`. Every physical circulation satisfies `-3<q<0`. The threshold multiplier `lambda=-1` yields the upper bound

```
D(q) = -3q^2 - 2(q+3)^2 - q^2
     = -6(q+1)^2 - 12
     <= -12.
```

The profile `beta=(1,2,1,1)` induces `q=-1` and reaches objective `-12`. Its flows are `(-1,-1,2,-1)`, its cycle drops are `(-1,-2,4,-1)`, and normalized potentials can be `(1,2,4,0)`.

Equality in the upper bound requires `q=-1`. All non-tied reduced costs are then nonzero, so equality also requires `beta_1=beta_3=beta_4=1`. The cycle equation forces `beta_2=2`, strictly inside `[1,3]`. Thus this is the unique optimizing resistance profile and no box corner is optimal. The claim is exact, rather than an inference from a numerical search.

The independent checker now verifies the quadratic upper-bound coefficients, exact physical witness, objective, interval membership, and threshold recovery for this example. This is a useful regression for the stationary-q branch of an exact implementation, not a separate literature-priority claim.

## Implementation audit: exact fixed-nomination block solver

I independently audited [exact_weighted_cactus.py](../code/potential_flow_mpd/exact_weighted_cactus.py). **The candidate optimization and rational recovery code pass review.** Its input contract is an already valid cactus decomposition into consistently oriented cycles with fixed offsets and objective weights, plus fixed-flow bridges. The module does not construct or validate a graph-to-block reduction; that limitation is stated explicitly and must remain visible in its documentation.

The implementation clips the circulation interval by all rational capacities, then splits it at every flow-sign change. It retains singleton intervals and the all-zero repeated-offset case. On each panel it enumerates threshold LPs, both roots of both aggregate constraints, rational panel endpoints, and the rational stationary point. Omitting an arbitrary flat-objective sample is correct because the boundary candidates already include a maximizing boundary of every nonempty compact feasible component.

Feasibility and candidate comparison use exact rational/quadratic arithmetic. Recovery selects aggregate endpoints at irrational q and performs rational greedy tie filling at rational q. Before accepting an improving candidate, the code reconstructs the original drops and rechecks every resistance interval, flow capacity, cycle equality, and weighted objective. It does not certify a surrogate or a relaxed instance in place of the original cycle.

The quadratic comparison routine is mathematically correct: it writes a difference as a one-radical number plus a signed second radical, handles equal signs directly, and compares squared magnitudes only when their signs oppose. This avoids introducing an explicit biquadratic field. The interval routine encloses the square root with integer square-root arithmetic and scales precision by the coefficient magnitude. Summing independently enclosed local values with an additional ceiling-logarithmic block-count allowance gives the promised global interval width.

I wrote [check_exact_weighted_cactus_review.py](../code/potential_flow_mpd/check_exact_weighted_cactus_review.py). Its most direct optimization test fixes a rational q using an exact arc-capacity constraint, then compares the solver with independent exhaustive vertex enumeration of the original resistance LP. All 280 max/min cases passed, with 44 feasible cases. This exercises sign and capacity boundary handling, tied weights, rational recovery, and infeasibility without reusing the solver's threshold optimization logic.

The same checker passed 1,220 arithmetic/interval cases, including equal numbers expressed with different radicands and perturbations of size `10^-90`, and seven special optimization cases. Those include the unique interior-resistance optimizer above, the irrational physical root `sqrt(10)-3` with rational fixed resistances `(1,2,2)`, an all-zero cycle, a flat objective, and mixed-cycle/bridge interval output for both objective senses. These tests use explicit exceptions and remain active under optimized Python execution.

The separate [input-schema, arithmetic, and block-orientation audit](review-potential-flow-exact-weighted-cactus-arithmetic.md) also passed. The mathematical and numerical checks here do not remove the supplied-block input requirement or establish runtime performance on large networks.
