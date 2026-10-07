# Independent mathematical audit: spatial certificates, propagation, and RLCTs

Date: 2026-10-05. Scope: the spatial-constrained, spatial-face-exact, cutoff-propagation, and RLCT notes identified in `BRIEF.md`, their independent reviews and revisions, and the relevant closeout statements. This report contains mathematical review and local proof repairs. I did not search the literature, rerun experiments, run project-wide checks, inspect CI, or edit the source notes.

## Decision for the manuscript

The central mathematical program is viable. A complete paper can prove a strong chain from a specified relaxation gap to certificate complexity, from constraint error bounds to bisection complexity, and from analytic sublevel asymptotics to exact polynomial and logarithmic rates. The strongest general characterization in the assigned sources is the unconstrained `C^{1,1}` box-face integral theorem. The constrained covering characterization has a logarithmic comparison loss. The McCormick results are separate lower bounds and separations; they do not constitute a general characterization.

Two integration corrections are required before using the results: the source families use different meanings of `N_opt`, and the closed-frame tightening lemma is false as stated. Both have clean repairs below. A smaller defect concerns repeated root nodes in the flat-sum propagation formula. The local extension from affine to nonlinear exactly kept constraints can be proved under `C^2` and combined LICQ for the original compatible exact/relaxed model; a full proof is given below.

**Correction after fresh review (2026-10-05).** The nonlinear constraint-gap extension in Section 5 requires LICQ for a compatible description of the original exact set `P_ex`, the unchanged original relaxed constraints defining `v`, and KKT multipliers for that same exact/relaxed assignment. Its earlier sentence permitting a redundant formulation to be replaced by an arbitrary LICQ description was unsafe and has been removed. The exact-ball/reverse-sphere example below shows why a LICQ description of the feasible set alone is insufficient. Also, node counts in the event argument include virtual probe partitions if probing supplies the stopping bound; actual tree-node counts alone need separate restrictions. The deduplicated successful-source cover has a fresh count `K_eval`, not the original terminal-owner count `K_F`.

Existing independent reviews checked substantial mathematics, but their repeated approval of the closed-frame lemma does not cure its boundary defect. Existing numerical evidence should remain labelled as evidence from the recorded computations, with exact-arithmetic replays distinguished from floating-point counts.

## 1. A safe theorem spine

Use the following order and scope.

1. **Certificate and event accounting.** Define rectangular test boxes with owned subsets, define cover and tree benchmarks separately, and count node processing, relaxation evaluations, probing evaluations, reduction rounds, propagation phases, and propagation rounds separately. Include the ownership lemma in Section 2 of this report.
2. **Quadratic-gap lower bounds.** Under the bound gap on feasible points, prove the vertex covering bound and the arcsine integral bound. Under the pointwise gap, transfer them to same-relaxation reductions through owned subsets. State the coordinate-multiplicity condition for curved strata.
3. **Constrained bisection and covering characterization.** Under second-order relaxation error, a local constraint error bound, and a Lipschitz objective, prove localization at each scale. Compare the resulting level sum with the running supremum of near-optimal covering numbers. Under quadratic growth, derive half the box dimension of the optimal set as the exponent. Under explicit stratified density and quadratic-doubling hypotheses, derive an integral characterization.
4. **Constraint-gap lower bounds.** State the inner-tube hypothesis and the exclusion of exact original-constraint propagation. Prove outward-descent transfer, then the logarithmic lower bound at a KKT minimizer with a positive-dimensional active stratum and a nonzero multiplier for a relaxed constraint. Either retain the affine-exact-constraint hypothesis or use the nonlinear extension proved in Section 5 below, with LICQ and multipliers for a description preserving the original exact/relaxed assignment and violation function.
5. **Unconstrained box-face characterization and RLCTs.** Under `C^{1,1}`, a positive uniform lower quadratic gap, and a vertex-vanishing upper gap, prove the characterization by all positive-dimensional faces. The analytic corollary uses the three integral regimes, including the extra logarithm at equality. Interior minimizers, or nonnegativity beyond the root box, permit the full-dimensional integral alone.
6. **Face-exact relaxations.** Prove the exact McCormick formulas, zero-face/vertex-cover geometry, matching-slice lower bounds, transversality and flat-centroid lower bounds, and the fractional-vertex-cover exponent. Include the two-box aligned certificate and the higher-dimensional counterexamples. Keep branching-rule separations under their exact quantified rule models.
7. **Cutoff propagation.** Define the objective-DAG hull-consistency bound with closed cutoffs and strict emptiness. Prove the greatest-fixed-point and witness lemmas. Distinguish exact local propagation, CND transfer, ND1 face-layer bounds, and round cost. Do not promote the bounded-round conjecture or a universal representation dichotomy to a theorem.

All comparison constants may depend on the stated instance parameters. Several upper constants are exponential in the dimension. These are tolerance-asymptotic statements for a fixed instance, not dimension-free approximation guarantees or practical runtime predictions.

## 2. Benchmarks, boundaries, tightening, and work

### 2.1 Different source definitions of `N_opt`

The constrained note defines `N_opt` as the least number of boxes in an arbitrary interior-disjoint rectangular partition of the root box. The face-exact note defines it as the least number of leaves of a guillotine tree. These quantities need not be identified without proof.

Safe notation is:

- `N_cov`: the least size of an arbitrary valid rectangular cover;
- `N_rect`: the least size of an interior-disjoint rectangular partition certificate;
- `N_tree`: the least number of leaves of an admissible axis-parallel split tree.

Then `N_cov <= N_rect <= N_tree`. Every lower bound proved by bounding the contribution of one valid box holds for all three. A dyadic tree gives an upper bound for `N_tree`, and hence for all three. Therefore a two-sided rate obtained from a cover lower bound and a tree upper bound holds for each benchmark, even though the finite values are different. Exact identities such as the tilted-stratum ceiling bound concern the explicitly constructed tree benchmark; use the correct symbol.

For a complete finite binary tree, total tree nodes equal `2L-1`; for a complete `b`-ary tree, nodes equal `1+b(L-1)/(b-1)`. These formulas do not count probing solves, repeated relaxation solves, reduction rounds, or propagation rounds. A finite rectangular partition can be refined to a grid and represented by a split tree, but the refinement may increase the number of boxes; this is not an equality of benchmarks.

An upper bound using the incumbent `UBD=f*` measures ideal certification cost after an optimal incumbent is available. It does not include the cost of discovering that incumbent. Lower bounds remain valid for every feasible incumbent with `UBD>=f*`, because pruning at `LB>=UBD-eps` implies `LB>=f*-eps`.

### 2.2 A counterexample to the closed-frame lemma

The constrained note, Lemma 2.1, and face-exact note, Lemma 1.2, assert that closed feasibility-reduction pieces contain no feasible points. This is false.

Take `X0=[-1,1] x [0,1]`, `F={0} x [0,1]`, and `f=0`. Set `R_B=F∩B` and `f_B=f-alpha q_B` on `R_B`, so the pointwise lower gap holds. Exact propagation replaces the root by `B'={0} x [0,1]`. The closed frame pieces `[-1,0] x [0,1]` and `[0,1] x [0,1]` both contain every point of `F`. At `(0,1/2)`, their `q` equals `1/4`, so neither is alpha-valid when `eps<alpha/4`. They also falsify the asserted feasible-piece count that omits all feasibility-reduction rounds.

Continuity does not fix this example: a whole feasible stratum lies in the retained boundary, and no discarded feasible sequence approaches it. The same issue can arise at a retained boundary of a same-relaxation reduction. Use ownership rather than treating the closures as valid everywhere.

### 2.3 Complete ownership repair

At every point in the computation, attach to the current closed test box `B` a Borel owned region `A⊆B`. Initially `A=X0`. Make owners rectangular with open or closed endpoint choices when a centroid proof will be used.

At a split at coordinate value `s`, give the lower child `A∩{x_i<=s}` and the upper child `A∩{x_i>s}`. Both are convex rectangular owners. At a reduction to a nonempty closed box `B'⊆B`, carry `A∩B'`, including its retained boundary, forward. Assign the discarded part by its first coordinate outside `B'`. More precisely, for each `i`, define

`A_i^- = A ∩ {x_j∈[l'_j,u'_j] for j<i} ∩ {x_i<l'_i}`,

`A_i^+ = A ∩ {x_j∈[l'_j,u'_j] for j<i} ∩ {x_i>u'_i}`.

Use as closed test boxes the usual slabs

`C_i^- = product_{j<i}[l'_j,u'_j] x [l_i,l'_i] x product_{j>i}[l_j,u_j]`,

and the corresponding upper slabs. Each owner lies in its test box, all are convex rectangular sets, they are pairwise disjoint, and their union is `A\B'`. Empty owners are discarded. This construction remains valid when some or all retained widths are zero. An emptying reduction is recorded as one terminal event with parent test box `B`, rather than a frame around an undefined empty box.

The terminal owners partition `X0`. For feasible-objective lower bounds, discard owners containing no feasible point. For a feasibility reduction, every discarded owner has empty intersection with `F`; retained-boundary points continue through the tree.

Suppose the pointwise lower gap holds. If a feasible point `y` belongs to a same-relaxation discarded owner, it was removed because `f_B(y)>UBD-eps>=f*-eps`; it cannot have been removed for `y∉R_B`. Since `C⊆B`,

`f(y)-alpha q_C(y) >= f(y)-alpha q_B(y) >= f_B(y) > f*-eps`.

Thus validity holds on the owned feasible subset. At a terminal bound event, if the bound comes from a box `D⊇B`, the bound gap gives the same result because `q_C<=q_D` on `C`. Infeasible relaxed leaves own no feasible point. Feasibility reductions require no pointwise test at the discarded owners.

Consequently there are closed test boxes `C_e` and convex rectangular owners `A_e⊆C_e` covering `F` such that

`m(y)+eps >= alpha q_{C_e}(y)` for `y∈A_e∩F`,

with the event bound

`K_F <= L + 2n R_rel`.

Here `L` counts terminal events in the certificate event tree and `R_rel` counts same-relaxation reduction rounds. If a stopping bound is a minimum over probe-child bounds, insert that probe partition, and recursively insert any further probe partitions on which those bounds rely, as virtual events: use the raw successful child tests, not a fictitious raw test at their parent. Thus `L` can exceed the actual search tree's leaf count. Feasibility rounds contribute zero feasible owners. No assertion is made that the closed test boxes themselves are valid on all their boundary points.

**Why covering and integration constants survive.** For a near-optimal set `S`, every point of `S∩A_e` is within `sqrt((eps+eta)/alpha)` of a vertex of `C_e`. Thus its owned contribution is covered by at most `2^n` cubes of the original side length. For the arcsine proof,

`integral_{S∩A_e}(m+eps)^(-d/2) <= alpha^(-d/2) integral_{S∩C_e∩A_e}q_{C_e}^(-d/2)`.

The coordinate-area proof is stated for a Borel subset of a box and gives exactly the original per-box bound. Owners partition `S`, so summing is legitimate even when a positive-measure feasible stratum lies on a shared closed face. For matching slices one integrates over the owned subset and bounds it by the full rectangular slice. For the flat McCormick centroid theorem, `S` is convex and each rectangular owner is convex, so `S∩A_e` is convex. If it has positive relative volume, its centroid lies in its relative interior and therefore in the owner. Its coordinate widths are distances between supporting hyperplanes of that set, and the original centroid estimate applies. This last point would fail for arbitrary nonconvex Borel ownership; rectangular owners are necessary for this transfer.

**Degenerate tests.** A retained box that collapses dimensions must be admitted in the node model and evaluated in its affine hull, with `q_B` summing only nonzero-width factors. No new operation type is needed. A positive-dimensional stratum contained in a degenerate box can still have an arcsine bound in its free coordinates. More generally, if a chosen coordinate projection uses a zero-width coordinate, its intersection has zero `d`-measure on the part where that projection is nonsingular. Ignore such measure-zero terms; every positive-measure projected part uses nondegenerate coordinate intervals. Singleton tests contribute at most the trivial counting lower bound. If the formal tree model insists on positive-width boxes, either disallow dimension-collapsing reductions or treat them as new lower-dimensional subproblems explicitly; do not silently discard the surviving feasible stratum.

**Owned tube dichotomy.** The terminal owners before feasible-point filtering partition all of `X0`. Let `K_all` count them, including owners with no feasible point. Assume the original inner-tube condition `(T_{alpha,beta})`, forbid original-feasibility reductions `(R-inf)`, and retain only same-relaxation reductions, admissible splits, and raw or expanded-probe bound/infeasibility pruning. Then every owned pair `(C,A)` satisfies, for every `z∈A∩P_ex`,

`v(z)>beta q_C(z)` or `f(z)-alpha q_C(z)>=f*-eps`.

To prove this, suppose `v(z)<=beta q_C(z)`. At a raw successful bound event with source box `B⊇C`, `q_C<=q_B` implies that `z` lies in the inner tube of `B`. Condition (T) gives `z∈R_B` and `f_B(z)<=f(z)-alpha q_B(z)<=f(z)-alpha q_C(z)`. The successful bound then gives the second alternative. If `R_B` is empty, this inner-tube assumption is impossible, so the first alternative holds. At a discarded same-relaxation owner in a reduction from `B`, the same implication gives `z∈R_B`; the removal predicate therefore forces `f_B(z)>UBD-eps>=f*-eps`, again giving the second alternative. Probe-derived successful bounds are expanded into their raw successful child events before this argument. This proves the dichotomy with the repaired boundaries, without claiming it on unowned retained faces of closed slabs.

The count is `K_all<=L+2nR_rel` under this no-(R-inf) model. Tube lower bounds, including shifted infeasible-stratum integrals, apply to `K_all`, not `K_F`: their witnesses lie in `X0∩P_ex` and can be infeasible. Exact original-constraint propagation would discard such witnesses without the dichotomy and is therefore excluded substantively, not just for counting convenience.

### 2.4 Safe operation-cost statements

Let `T_aug` count processed nodes of the augmented certificate event tree, including virtual probe partitions used by stopping bounds, and let `T_real` count actual search tree nodes. Then `K_F<=T_aug+2nR_rel`. Under a bound of `r` relevant rounds per augmented event node, `K_F<=(1+2nr)T_aug`. This is enough for every lower bound and the bisection comparison. If no stopping bound uses a probe partition, `T_aug=T_real` for this purpose. Otherwise actual node count alone is not justified by this accounting; probe evaluations must enter a separate evaluation/event cost or be charged under an explicit bound. Without a per-node round bound, the statement is about event work `T_aug+R_rel`, not node count alone.

A relaxation-evaluation statement can also be made safely. Suppose each relevant reduction round uses at least one separately counted relaxation evaluation, and every successful terminal bound can be expanded into counted successful raw source evaluations, including the probe-child evaluations if the bound is the minimum of their bounds. Every inherited successful raw bound can be represented by its source box; that box is globally alpha-valid on its feasible points. Use each distinct successful source box only once. Together with owned discarded slabs these form a new covering certificate for `F`, possibly overlapping. Let `K_eval` be its size; it is not the size `K_F` of the terminal-owner partition. Every feasible point either was discarded into a valid slab owner or survives into a region covered by one successful raw source box. Hence

`K_eval <= S_success + 2nR_rel <= (2n+1)S`

when each round is charged to a distinct counted solve and `S` includes all probing evaluations. Apply covering and per-test integral lower bounds to this new cover to infer a lower bound on `S`; do not assert that deduplication reduces the original terminal-owner count. For centroid arguments, use `S_stratum∩C` at a globally valid source box and `S_stratum∩A` at a rectangular discarded owner; both are convex when the stratum piece is convex. Arbitrarily many uncharged reductions or an oracle that computes a child partition bound for free are outside this solve-cost claim. A pointwise gap is required for discarded same-relaxation owners; the weaker bound gap suffices for successful source boxes and no-tightening certificates.

For tube lower bounds, exact original-feasibility propagation remains excluded: it can discard the superoptimal infeasible points that carry the proof. The ownership repair does not remove this substantive exclusion.

For evaluation-cost tube claims, keep every successful raw source box, including sources proving relaxed infeasibility, and every same-relaxation discarded owner. This gives a fresh cover of `X0∩P_ex` on which the tube dichotomy holds, of size `K_eval_all<=S_success+2nR_rel`. Under the same distinct-solve charging condition, `K_eval_all<=(2n+1)S`. This is the tube analogue of `K_eval`; it does not permit filtering by intersection with `F`.

For hybrid cutoff runs, use `K <= L+2n(R_rel+P)` on feasible owners, with `P` propagation phases and `L` again counting the augmented certificate terminal events; count additional feasibility events only if a bound specifically uses infeasible owned witnesses. Consecutive objective-only propagation runs may count as one phase under the inheritance-chain invariant in the revised cutoff note. A bounded phase count per augmented event node gives a lower bound on that event-node count. A claim about actual search nodes requires that probe stopping partitions be absent or their cost be separately charged. Unbounded propagation rounds inside one phase are still real work and are not controlled by that node lower bound.

## 3. Quadratic gap, geometry, and constrained bisection

### 3.1 Lower bounds and their quantifiers

Assume `alpha>0` and, for every admissible box and every feasible point in it,

`LB(B) <= f(y)-alpha q_B(y)`.

A valid test at tolerance `eps` satisfies `m+eps>=alpha q_B` on its feasible points or owners. Hence for every `eta>=0`,

`K >= 2^(-n) N_inf(E(eta), 2 sqrt((eps+eta)/alpha))`.

The proof uses `q_B>=d_i^2` separately in every coordinate; it does not require convexity of the feasible set, disjointness of test boxes, regularity of `f`, or a particular split rule. It is a certificate lower bound, not a claim that a solver can compute the benchmark.

For `F=X0`, AM–GM gives `q_B^(-n/2)<=n^(-n/2) product_i a_i^(-1/2)`. Each one-dimensional integral is `pi`, so

`K >= (alpha n/pi^2)^(n/2) integral_{X0}(m+eps)^(-n/2)`.

For a `d`-dimensional embedded `C^1` stratum `S⊆F`, choose the lexicographically first dominant `d`-coordinate projection at each point. Cauchy–Binet gives its tangential Jacobian at least `binom(n,d)^(-1/2)`. The area formula with coordinate-fibre multiplicity, followed by the same arcsine integral in those `d` coordinates, gives

`integral_{S∩B∩A}q_B^(-d/2) <= (pi^2/d)^(d/2) binom(n,d)^(1/2) sum_I M^I(S;B∩A)`.

Thus finite coordinate multiplicity is a real hypothesis. A positive two-point constant controls it on sufficiently small pieces and, on a bounded root box, globally. Curvature bounds alone do not: parallel flat components, or an embedded infinite spiral of bounded curvature, can accumulate unbounded length. Do not substitute curvature for reach or coordinate multiplicity.

On root faces the fixed factors vanish and one obtains the sharper constant `(alpha d/pi^2)^(d/2)` directly. This distinction matters for the later facewise RLCT theorem.

### 3.2 Localization upper bound

Assume `R_B⊆B∩P_ex`, valid relaxations, and for `z∈R_B`,

`f_B(z)>=f(z)-tau w(B)^2`, `v(z)<=tau w(B)^2`.

Assume also `dist_2(z,F)<=kappa v(z)` whenever `z∈X0∩P_ex` and `v(z)<=v0`, and that `f` is `L`-Lipschitz on `X0`. Put `Lambda=tau(1+L kappa)`. A nonpruned dyadic cube `D` of side `s` has a relaxed witness `z` with `f_D(z)<f*-eps`. For sufficiently small `s`, a nearest feasible point `y` satisfies

`dist_inf(y,D)<=kappa tau s^2<=s`,

`0<=m(y)<Lambda s^2-eps`.

Thus `eps<Lambda s^2`, and at most `5^n` nonpruned cubes can be charged to each grid cube meeting that feasible sublevel set. Coarse levels contribute a finite constant independent of `eps`; every nonpruned cube has `2^n` processed children. This proves the level sum upper bound without lower-gap assumptions.

The error bound is about distance to the full feasible set, with box and exactly kept constraints included. LICQ or MFCQ asserted only at global minimizers does not automatically supply the global error bound used here. One may assume the bound directly or give a separate compactness argument from local bounds at every feasible point. Relaxed witnesses need not be feasible; omitting this error-bound step would invalidate the constrained upper bound.

### 3.3 The covering characterization

Define

`Phi_alpha(eps)=sup_{eta>=0}N_inf(E(eta),2sqrt((eps+eta)/alpha))`.

The lower bound applies for every `eta` and therefore to the supremum. At each upper-bound scale, set `eta=Lambda s^2-eps` and refine the covering cubes by a constant scale ratio. This gives

`c Phi_alpha(eps) <= N_cov <= N_rect <= N_tree <= T_bis <= C0+C J_eps Phi_alpha(eps)`,

where `J_eps=O(1+log(1/eps))` for small positive `eps`. The same comparison with any owned valid event certificate bounds bisection by `C0+C J_eps K_F`.

The running supremum is essential for instance-uniform constants. Within a factor `2^n`, it equals

`sup_{eta>=eps} N_inf(E(eta),2sqrt(eta/alpha))`.

The source's oscillatory family with `K` separated near-optimal wells and uniform Hessian and relaxation constants gives `N_tree>=K/2`, while the single-scale covering of `E(eps)` remains bounded at `eps=0.2K^(-2)`. The factor `log(1/eps)` is then `O(log K)` and cannot absorb `K`. This argument is correct and should remain explicit.

Under global quadratic growth `m>=c_g dist_inf(.,M)^2`, each near-optimal sublevel lies in a tube of radius `O(s)` around `M`. Hence the upper level counts are bounded by a constant times `N_j(M)`. Summing to `s≈sqrt(eps)` proves the exponent `dim_box(M)/2` when that dimension exists; for finite `M` it gives only `O(log(1/eps))`. The quadratic-growth hypothesis is necessary for this inference. Degenerate analytic minima can have an isolated optimal set and a positive polynomial exponent, so the unqualified closeout phrase “the exponent is half the dimension of the optimal set” is too broad.

For the stratified integral upper bound, the source's assumptions (R1) parabolic proximity, (R2) quadratic doubling along strata, and (R3) positive lower density are sufficient. Maximal separated witnesses supply disjoint stratum balls of mass at least `theta s^d`; all those balls lie in a sublevel of order `s^2`. Tonelli and the geometric sum give the claimed integrals. Finite zero-dimensional strata add an `O(log(1/eps))` term unless a stronger argument removes it. State (R) rather than treating arbitrary stratifications as automatically regular.

### 3.4 KKT and sharp minima

The finite nondegenerate KKT package is correct with its stated LICQ, strict complementarity, SOSC, local feasible-description hypotheses, and the independent relaxation/error-bound assumptions. Positive-dimensional active strata give the logarithm by an upper quadratic bound on `m` along the stratum; SOSC supplies the upper complexity through quadratic growth. These are different uses of second-order information.

When the active stratum has dimension zero, strict complementarity makes feasible directional growth linear. The source proof should handle the case with no active inequalities separately: if `n` independent equalities alone fix the point, the feasible set is locally a singleton, so local sharp growth is vacuous and uniqueness plus compactness gives global sharp growth. The source's `mu_min=min_{j∈A}mu_j` is undefined in that case. With active inequalities, its estimate is valid. A bounded exact certificate requires the vertex-vanishing upper error; a width-squared error that remains positive at the minimizer does not suffice.

The logarithmic lower bound for dyadic bisection at an off-grid sharp minimizer requires the middle-part recurrence condition. Being nondyadic alone is insufficient; sparse binary expansions defeat the asserted uniform lower rate. The source corrections already acknowledge this.

## 4. Box faces and analytic asymptotics

### 4.1 Complete generic-constant proof of the face characterization

Let `X0` be a cube, `m>=0` on it, and let `grad m` be `M`-Lipschitz there. Increase `M` to a positive value if needed. Assume a bound lower gap `alpha q_B` and a pointwise vertex-vanishing upper error `alpha' q_B`, with `alpha,alpha'>0`. Then

`N_cov(eps) ≍ N_rect(eps) ≍ N_tree(eps) ≍ T_bis(eps) ≍ 1+sum_{F:dim F>=1} I_F(eps)`

for sufficiently small positive `eps`, with instance-dependent constants and `I_F=integral_F(m+eps)^(-dim F/2)`.

The lower bound is the root-face arcsine bound, maximized over the finitely many faces, together with `N_cov>=1`. It remains to prove the tree upper bound without quadratic doubling.

At side length `s<=s0/2`, a nonpruned dyadic cube has a witness `y` with `m(y)+eps<C s^2`. Move each coordinate at distance less than `s` from a root endpoint to that endpoint, producing `y'` on a face `F`. To control a moved derivative, take an admissible length-`s` step away from that endpoint. Nonnegativity and the descent lemma imply

`sigma ∂_i m(y) <= m(y)/s+Ms/2`.

Each moved coordinate costs at most `m(y)+Ms^2` after including the quadratic remainder. The unmodified coordinates have length-`s` room in both directions. The two corresponding derivative tests give `|∂_i m(y')|<=m(y')/s+Ms/2`. Therefore a full relative cube of radius `s` in `F`, centered at `y'`, is contained in `E(C' s^2)` for a constant depending only on `n,alpha',M`.

For each positive-dimensional face choose maximal witnesses separated by more than `s` in sup norm. Their relative cubes of radius `s/2` are disjoint, have measure `s^d`, and lie in `F∩E(C's^2)`. Every original nonpruned cube lies within `O(s)` of one chosen witness, so at most a dimension-dependent number of grid cubes is charged to each. Summing scales and using Tonelli gives

`sum_j s_j^(-d) H^d(F∩{m+eps<=C''s_j^2}) <= C I_F(eps)`.

Vertices need separate treatment. A nonoptimal vertex `v` can be charged only when `m(v)<=C's^2`, so it contributes finitely many levels independently of `eps`. At an optimal vertex use inward coordinates `t_i>=0`, and let `g>=0` be the smallest inward edge derivative. The lower descent estimate and `q_D<=s|t|_1` show that its corner cube is pruned when `s<=g/(alpha'+M/2)`. Independently, no cube can remain open below `s≈sqrt(eps)`. Thus its charge is at most a constant plus

`log_+(s0/max(g/M,sqrt(eps)))`.

On an edge attaining derivative `g`, Taylor gives `m(v+te)<=gt+Mt^2/2`. For `t>=max(g/M,sqrt(eps))`, this is at most `3Mt^2/2` and `eps<=t^2`. Therefore the edge integral bounds the same logarithm below. This absorbs all optimal-vertex charges into edge integrals. Using `log_+` avoids the source's harmless negative intermediate-count bound for very large `g`. Coarse levels, nonoptimal vertices, and fixed additive terms form `C0`. This completes the upper proof and shows why a vertex adds no unaccounted logarithm.

This theorem is unconstrained. For constrained feasible sets, root faces do not describe curved active strata, and the projection step need not stay feasible. Do not apply the face characterization to arbitrary constrained problems.

### 4.2 Integral asymptotics with exact logarithmic regimes

For a positive-dimensional compact face `F`, let analytic `h=m|_F` be nonnegative, nonzero, and have a zero. Suppose its sublevel volume is

`V_h(t) ~ c_V t^lambda (log(1/t))^(theta-1)`.

The analytic input supplies positive rational `lambda` and positive integer `theta` under the intrinsic full-dimensional box/semianalytic hypotheses. With `c_Z=c_V Gamma(1+lambda)`, the identity

`I_a(eps)=1/Gamma(a) integral_0^infinity s^(a-1)e^(-eps s) Z(s) ds`

gives:

- `a>lambda`: `I_a ~ c_Z Gamma(a-lambda)/Gamma(a) eps^(lambda-a)(log(1/eps))^(theta-1)`;
- `a=lambda`: `I_a ~ c_Z/[theta Gamma(a)] (log(1/eps))^theta`;
- `a<lambda`: `I_a` increases to the finite value `integral h^(-a)`.

For the first case, substitute `u=eps s`, apply the asymptotic uniformly away from zero, and dominate the logarithmic factor with an integrable power perturbation. For equality, the range `1<<s<<1/eps` contributes `integral ds (log s)^(theta-1)/s=(log(1/eps))^theta/theta`; the ranges below a fixed threshold and above `1/eps` are lower order. For `a<lambda`, the tail `s^(a-1-lambda)(log s)^(theta-1)` is integrable and monotone convergence applies. These arguments verify the constants, not merely the exponents.

For `h≡0`, the integral is exactly `H^d(F)eps^(-d/2)`; for `h>0` on the compact face it is bounded. Apply the preceding result with `a=d/2` to each face. The governing asymptotic is the maximum over positive-dimensional faces of the resulting rates, with a baseline `1`. In particular equality `lambda_F=d/2` carries `log^theta`, not `log^(theta-1)`. Finitely many faces allow sums and maxima to be compared by fixed constants.

The four-dimensional example `m=x(1-x)+y^4+z^4+w^4` on `[0,0.9]x[-0.4,0.5]^3` is a correct substantive boundary counterexample. The full-box RLCT is `(7/4,1)`, giving only exponent `1/4`, while the `x=0` face has RLCT `(3/4,1)` in dimension three and gives exponent `3/4`. The maximum-face theorem gives that larger rate in both directions.

### 4.3 Interior and external-nonnegativity simplifications

When all minimizers are interior, proper root faces have `m` bounded away from zero and contribute only constants. At an interior minimizer, Taylor gives `m<=C|h|^2`, so `lambda<=n/2`. If the Hessian has a null vector, analyticity gives `m(w+sv)<=C(|w|^2+|s|^3)`; the corresponding sublevel box has volume of order `t^((n-1)/2+1/3)`, forcing `lambda<n/2`. Thus equality holds exactly when all minimizers are nondegenerate. Compactness then makes their number finite, the Laplace expansion gives `theta=1`, and the node rate is logarithmic. This proof is correct.

More generally, if `m>=0` on a fixed neighborhood of the root box and the gradient is Lipschitz there, the nonnegative descent inequality supplies `|grad m|<=sqrt(2Mm)` on low sublevels. Around each low-valued face point, an inward full-dimensional cube of side `sqrt(t)` lies in `E(Ct)`. Packing such points gives

`V_{X0}(Ct) >= c t^((n-d)/2) V_F(t)`.

Inserting this estimate in the layer-cake formula bounds every face integral by a constant plus a constant times the full integral. Hence the full integral suffices. A merely thin unspecified extension on which nonnegativity is not assumed does not justify quadratic doubling or this dominance statement.

### 4.4 Newton and learning-coefficient claims

The safe Newton statement is a local RLCT bound by the reciprocal Newton distance, with equality under the precise nondegeneracy/positive compact-face condition verified by the literature agent. At a boundary zero, arbitrary analytic coordinate changes alter the local integration domain. The orthant argument works in coordinates that preserve a union of coordinate orthants: square the function, compare with the sum of squares of Newton monomials, and use that the even monomial sum has the same poles on each orthant as on the full symmetric cube. Do not use a full-neighborhood Newton equality automatically on a one-sided domain.

The existing remark that a critical face with `lambda=d/2,theta>=2` might never govern the maximum is explicitly incomplete. The facewise theorem already covers such a face and does not need that conjecture. Leave the stronger non-governance claim open.

For reduced-rank regression with true rank zero, the transfer from the learning coefficient to node rate is mathematically sound once the supplied coefficient is correctly sourced. Positive definite data covariance changes the loss only by bounded multiplicative constants. Homogeneity `K(tA,tB)=t^4K(A,B)` makes the RLCT independent of the radius of any ball about the origin; sandwiching any compact box containing an origin neighborhood between balls identifies the box-restricted RLCT. Since the loss is globally nonnegative, the full-integral corollary applies. This audit did not independently establish the cited Aoyagi–Watanabe coefficient formula; retain it as external analytic input.

The scalar noisy toy `(ab-delta)^2` has a uniformly bounded Hessian on a fixed box, is globally nonnegative, and its integral is

`eps^(-1/2) [pi log(1/max(delta^2,eps))+O(1)]`.

For `|a|` above a constant times `max(delta,sqrt(eps))`, integrating in `b` gives `pi/(|a|sqrt(eps))+O(a^(-2))`. The small-`a` region contributes `O(eps^(-1/2))`, by splitting additionally at `|a|≈delta` when `delta>sqrt(eps)`. Integrating both signs of `a` gives the displayed coefficient and proves the logarithm freezes below the noise scale. For a fixed positive scaling factor `S`, replace `eps` by `eps/S`; constants change. The general noisy regression two-regime claim remains a conjecture: uniform empirical-process control, the noisy fiber's geometry, and boundary intersections have not been proved.

## 5. Completing the nonlinear exactly kept constraint extension

The source deliberately keeps the affine-exact-constraint hypothesis in its formal KKT tube theorem and only sketches the nonlinear case. The following proof resolves the local gap while retaining a clear scope.

Let `z*` be a global KKT minimizer for the original relaxation model. Require a finite `C^2` local description of the original exactly kept set `P_ex`, together with the original relaxed inequalities `g_j` and equalities `h_k` defining the unchanged violation function `v`, such that the gradients of all active inequalities and equalities in this combined tuple satisfy LICQ. Include active box bounds. Require KKT multipliers for this same tuple and the same classification into exactly kept and relaxed constraints. In particular, a different LICQ description of `F` alone is not a substitute. If no such compatible tuple exists, this theorem does not apply; the proof provides no license to remove redundant constraints, convert a relaxed inequality into an equality, or change which restrictions are kept exactly.

Let `E(x)` collect the active exactly kept equalities and active exactly kept inequalities from that compatible tuple, including active box coordinates, with their values at `z*` subtracted if necessary. Inactive exactly kept inequalities have strict slack near `z*`. Assume at least one original active relaxed inequality has a positive multiplier, or one original relaxed equality has a nonzero multiplier.

**Why compatibility matters.** Take `P_ex={x∈R^2: x_1^2+x_2^2<=1}`, the relaxed inequality `1-x_1^2-x_2^2<=0`, and `f=-x_1^2`. The feasible set is the unit circle, with minimizers `(±1,0)` and `f*=-1`. Its equality description `x_1^2+x_2^2=1` is LICQ, but the original active exact and relaxed gradients are opposite and fail combined LICQ. Every point of the original exact ball has `f>=-1`, so no superoptimal point `f<f*-eps` exists inside `P_ex`. An outward-descent tube proof based only on the equality description would therefore be false. The compatible combined-tuple requirement excludes this example.

LICQ supplies a vector `e0` with derivative zero along every exactly kept active constraint and every other active constraint not used for outward descent, derivative `1` along the chosen relaxed inequalities, and derivative equal to the equality multiplier's sign along chosen relaxed equalities. Normalize it. KKT then gives `grad f(z*)·e0<0`.

Let `R` be a right inverse of `E'(z*)`; when `E` is empty omit the correction. Consider

`H(y,t,xi)=E(y+t e0+R xi)-E(y)`.

At `(z*,0,0)`, the derivative with respect to `xi` is the identity. The implicit function theorem gives a `C^2` function `xi(y,t)` on a product neighborhood of `(z*,0)`, satisfying `H=0` and `xi(y,0)=0`. Define

`Z(y,t)=y+t e0+R xi(y,t)`.

Then `E(Z(y,t))=E(y)`, `Z(y,0)=y`, and `Z_t(z*,0)=e0`, because `E'(z*)e0=0`. After shrinking the neighborhoods, `|Z_t|<=2` and `grad f(y)·Z_t(y,0)<=-2mu` for some `mu>0`. Bounded second derivatives of `f∘Z` give uniformly

`f(Z(y,t))<=f(y)-mu t+C t^2`.

The relaxed constraint derivatives and second derivatives are bounded, so for feasible `y`,

`v(Z(y,t))<=c t`.

Exactly kept active inequalities retain the value `E(y)<=0`, exactly kept equalities retain zero, and active box coordinates retain their values. Inactive exact constraints and box inequalities retain their uniform slack for sufficiently small `t`. Thus `Z(y,t)∈X0∩P_ex`, while `|Z(y,t)-y|<=2t`.

For a covering lower bound on `E(eta)` near `z*`, take `t=3(eta+eps)/mu`, small enough that `Ct^2<=eta+eps`. Then

`f(Z(y,t))<f*-eps`, `v(Z(y,t))<=3c(eta+eps)/mu`.

If a test owner satisfies the tube dichotomy and contains `Z(y,t)`, the superoptimal objective value forces

`beta q_C(Z(y,t))<v(Z(y,t))<=A(eta+eps)`.

The shifted point is within `sqrt(A(eta+eps)/beta)` of a vertex in every coordinate. Since `|Z-y|<=O(eta+eps)`, the original point lies within a constant times `sqrt(eta+eps)` of that vertex for small tolerances. This proves the covering transfer with changed fixed constants. A straight ray is unnecessary.

For the logarithmic integral, let the active feasible stratum have dimension `d>=1` and write a small piece as the `C^2` graph `y(x)=z*+x+phi(x)` over its tangent space `T`, with `phi(0)=Dphi(0)=0`. Let `mt(x)=m(y(x))`. Since `z*` minimizes along this stratum, `mt(0)=Dmt(0)=0`. Define

`Z_eps(y)=Z(y,3(m(y)+eps)/mu)`.

This map is `C^2` jointly in graph coordinates and `eps`. At `(x,eps)=(0,0)`, its tangent derivative is the identity on `T`: `Z_y(y,0)=I`, while the time derivative is multiplied by `Dmt(0)=0`. The tangential projection `Psi_eps(x)=pi_T(Z_eps(y(x))-z*)` therefore has derivative `I` at that point. Shrink to a fixed coordinate ball and a compact interval `0<=eps<=eps0` so that `||D_x Psi_eps-I||<=1/2`. The maps are uniformly injective, with Jacobian at least `2^(-d)`, and their images contain a common smaller ball. By the parameter version of the inverse function theorem, the inverse maps and the normal graph functions are `C^2` with uniform derivative bounds on that common ball.

Choose a still smaller fixed stratum piece whose projected images all lie inside this common ball. Each `Z_eps(S)` lies in a larger graph over a convex ball with uniformly bounded Hessian. The graph two-point inequality then gives a uniform positive two-point constant. On a sufficiently small piece this yields a uniform finite coordinate multiplicity. The full map has a uniform positive area Jacobian because its tangential projection does. Uniform descent and violation estimates give

`f(Z_eps(y))<f*-eps`, `v(Z_eps(y))<=A(m(y)+eps)`.

The owned tube lemma in Section 2.3 supplies the dichotomy for every shifted image point of an admissible run; all terminal owners, including infeasible ones, cover the image. The shift-map area formula and the arcsine lemma therefore imply

`K_all >= c integral_S(m(y)+eps)^(-d/2)dH^d(y)`.

On the active stratum of the compatible combined tuple, `m=L-f*` for its KKT Lagrangian, and `grad L(z*)=0`. Thus `m(y)<=C|y-z*|^2`. The graph has `d`-measure at least `c r^d` in each sufficiently small radius-`r` neighborhood. Integrating radial shells from `sqrt(eps)` to a fixed small radius gives `c log(1/eps)`. Therefore the tube logarithmic lower bound extends to nonlinear exactly kept `C^2` constraints under combined LICQ for the compatible original model and its nonzero-relaxed-multiplier hypothesis. This is a local proof; it does not resolve the separate open question about what exact original-constraint interval propagation can do to curved strata.

## 6. Face-exact audit and transferable claims

The main McCormick formulas and proofs rederive correctly. For an edge `ij`, the gap is `|c_ij|` times the minimum of the appropriate two endpoint-distance products. It is at least `|c_ij|d_i d_j` and at most `|c_ij|(a_i+a_j)/2`. All edge gaps are nonnegative, so their sum vanishes precisely when the fixed coordinates cover every graph edge. Joint-envelope bounds are generally weaker than sums of termwise gaps; use only the proved mixed-partial maximum or chord bounds for joint envelopes.

The matching integral uses disjoint pairs to factor the per-box integral. Its exact factor `2 Gamma(1-sigma)^2/Gamma(3-2sigma)` for `sigma<1` is correct, and it diverges at `sigma>=1`. Optimizing `sigma` below one gives the `log^(2k)` lower loss. The kink example shows that some logarithmic loss is necessary in this general class, but it does not settle the necessity under quadratic doubling or the optimal loss for matchings. Do not state a sharp general integral characterization.

Matching concave directions give genuine quadratic chord gaps and the usual arcsine bound in the matching coordinates. A smooth interior minimizer with an active edge therefore forces at least logarithmically many tests. The feasible chord must actually lie in `F`; an edge in the objective alone does not supply such a chord under arbitrary constraints.

For flat near-optimal sets, the centroid theorem with `tau(V,G)>0` is correct. Graph transversality implies this condition but is stronger in dimension at least two. For curved compact strata, injectivity of every vertex-cover projection on tangent spaces, plus a finite atlas, gives the required projection-slab measure bound. Under that condition, the near-optimal stratum forces `eps^(-p/2)` tests. These statements extend through convex rectangular owners as described above.

The fractional vertex-cover exponent is also correct. The maximum volume of a valid intersection rectangle is the multiplicative-width optimization `w_i w_j<=rho^2`; logarithms turn it into the fractional vertex-cover LP. Half-integral optimal solutions yield matching anisotropic grid constructions. This is an exact exponent for the specified near-optimal box model, not an exponent determined by the optimal set alone.

The two-dimensional aligned full-segment theorem is correct: convexity forces the transverse directional derivatives to be affine along the segment, and nonnegativity supplies exactly the McCormick endpoint-product inequalities on the two boxes. It extends to the stated independent star-center cover condition. That structural condition concerns the pair `(G,K)`, not merely the graph being a star forest. The path example fixing both leaves fails it and has order `1/eps`. The aligned three-dimensional quadratic example costs order `eps^(-1/2)` even though its optimal segment has `tau=0`. The curved row-slice example gives only a lower bound `Omega(1/(eps log(1/eps)))`; its exact complexity and a matching upper bound are not known.

### 6.1 A complete repair of one-sided concave-ray divergence

Face-exact Proposition 4.6(b) asserts divergence from a one-sided feasible concave ray. Its written proof establishes nonexistence of an exact certificate. Because Proposition 4.6(a) is restricted to `F=X0`, invoking it would not prove divergence for a general polyhedral feasible set. Divergence nevertheless follows directly and can be included with this proof.

Suppose `y(t)=y*+tv` is feasible for `0<=t<=t0`, `c_ij v_i v_j<0`, and `liminf_{t↓0}m(y(t))/t=0`. Put `kappa=|c_ij v_i v_j|`. If valid covers of at most `N` boxes existed along `eps_l↓0`, intersect each box with the ray and obtain at most `N` closed intervals in `[0,t0]` covering that interval. Empty intersections can be padded by points. Pass to a subsequence with all endpoints convergent. The limit intervals still cover `[0,t0]`.

For an interval `[a_l,b_l]` from a cover box and `a<t<b` in its nondegenerate limit, the ray chord and the concave-edge bound give

`m(y(t))+eps_l >= kappa(t-a_l)(b_l-t)`.

Letting `l→infinity` gives the same inequality with `eps=0` and endpoints `a,b`; continuity extends it to the endpoints. Finitely many limit intervals covering `[0,t0]` imply that one has left endpoint zero and positive right endpoint `b`: take a sequence of positive points tending to zero and a repeated covering index. Consequently

`m(y(t))/t >= kappa(b-t)` for `0<t<b`,

contradicting the liminf hypothesis. Thus even `N_cov(eps)→infinity` under arbitrary covers, with constraints allowed. This repairs the omitted limiting step without assuming continuity of the full feasible-set intersections of boxes.

### 6.2 Rule quantifiers and count corrections

- The kink family has a certificate of at most two leaves for every tolerance, and exactly two only below the root's negative-bound magnitude. Replace repeated claims `N_opt=2 for all eps` by `N_tree<=2`, or by equality for sufficiently small `eps`.
- The oblivious-rule theorem gives an expected lower bound for every fixed tolerance; its resulting bad instance may depend on that tolerance. This defeats a uniform coefficient/dimension-only competitive constant. It does not by itself prove one fixed bad instance with a polynomial lower rate for all small tolerances under an arbitrary oblivious tree.
- Unclamped relaxation-point splitting gives three nodes on the kink under the stated coordinate/tie rule. A fixed clamp changes the symbolic dynamics. Polynomial lower rate on the Cantor set is proved for the periodic point `a=1/6` and similar orbits bounded away from endpoints, not uniformly for every survivor.
- Fixed midpoint weights and box-dependent weights are different rules. The countable-exception proof applies to fixed weights. The source correctly leaves the SCIP-dependent-weight extension open.
- The min-child strong-branching example is valid under its exact point rule and exact score. Probe evaluations must be counted separately from committed tree nodes if work comparisons are made. A successful min-child parent bound requires accounting for the tested child boxes in certificate arguments.
- Claims of generic polynomial growth for a fixed-weight widest-side rule outside the explicitly proved examples should remain numerical. Product-score competitiveness remains open.

## 7. Propagation audit and exact scope

### 7.1 Fixed points and strict cutoffs

On a finite objective DAG with continuous operations on the compact forward domains and constants fixed at their values, exact elementary hull revises are monotone, deflationary, and continuous along decreasing compact boxes. The hull of all common fixed boxes is a common fixed box and is greatest. A fair exact schedule converges to it: every elementary constraint is revised infinitely often, and continuity passes its equality to the limit. If the limit is empty, compactness implies some finite iterate is empty. Fair forward and backward partial steps have the same conclusion when their common fixed points are the exact hull-consistent boxes. These proofs are sound.

With `pi_D(C)=min{c:Z*(C,c)≠empty}`, nonempty-cutoff thresholds are closed. Hence emptiness occurs at `c<pi_D(C)`, not at equality. Likewise a point is removed exactly when `pi_D(C,y)>c` in the ideal limit. Relaxation pruning has the weak comparison `LB>=f*-eps`; propagation of the closed cutoff has a strict comparison. Preserve this difference.

Propagators that treat repeated variables globally, shaving, auxiliary-variable OBBT, auxiliary branching, and objective-plus-original-constraint revises do not automatically preserve the objective-only `Z*` witnesses. The constraint counterexample already recorded in the recheck shows why separate original-feasibility reductions and objective-only propagation phases are required. A different bound could be defined on an augmented constraint DAG, but the current witness and loss theorems do not prove results for it.

The revised inheritance-chain proof is sound: take the minimum cutoff over every inherited phase feeding the current phase, not just the current phase's cutoffs. Its greatest fixed box lies in each inherited final box by monotonicity and remains in restarted forward boxes because any hull-consistent box is contained in the forward box of its own variable projection. Thus consecutive objective runs can be merged for event accounting. Use owned points outside the final retained box; closed frame boundaries need not satisfy the pointwise propagation test.

### 7.2 Repeated root nodes: necessary correction

The flat-sum formula requires that root terms be distinct node coordinates. The general witness remark states this explicitly, but setting (FS) also permits several `p_j` to be the same direct base variable, and then the fixed-point formula can be false.

Let the elementary root equation use the same node `x` three times in `f=x+x-x=x`, on `C=[-1,1]`. The true root constraint is `w=x`, so `pi_D(C,0)=0`. The endpoint formula on `U'=[-1,0]` gives minima `-1,-1,0`, widths `1,1,1`, and `Phi(U')=-1`. It would incorrectly predict `pi_D(C,0)<=-1`. Its witness treats three root coordinates independently, although they are one coordinate.

Safe hypothesis: each root child term is a distinct node, with signed coefficients handled consistently; repeated references to a direct variable are combined first, or placed behind distinct operation nodes when that is the chosen representation. A variable shared below distinct unary term nodes is allowed. The endpoint-minimum formula and its proof then hold exactly as written. The representation is part of the model, so adding copies is not an innocuous claim that the original DAG behaves identically.

The witness lemma for a sum of distinct root nodes over arbitrary DAGs is sound: give each non-root node its exact range over `U'`. Every interval endpoint is attained by some original point and therefore extends within its own elementary constraint. The root treats distinct coordinates independently. Single-use terms are needed only to identify the forward interval minima with exact term minima, not for this general witness construction.

### 7.3 Exactness and lower-bound transfer

One-sidedness is a sufficient criterion, not a necessary characterization of every exact representation. Local exactness on boxes meeting a neighborhood of the optimal set yields an epsilon-independent ideal node count: sufficiently small near-optimal boxes are certified exactly, while compactness and forward convergence certify boxes outside that neighborhood after a finite fixed refinement. This counts an ideal fixed-point bound; actual schedules can require unboundedly many rounds as `eps→0`.

The representation transformation `f*+abs(f-f*)` equals `f` on the whole root domain only when `f>=f*` there. The no-representation-free-lower-bound proposition is therefore safe for the unconstrained setting, or as a function agreeing with `f` only on the feasible set if the model explicitly permits that. It is not a literal representation of an objective that drops below its constrained optimum at infeasible points.

The CND first-order witness and transfer proof are correct. Coordinatewise term-derivative cancellation with a uniform positive no-dominance margin gives a loss at least `D0 delta/2` along a sufficiently short centered segment. If propagation removes the point at cutoff `f*-eps`, each nearest-face distance is at most `2(m+eps)/D0`. Since `q_C<=w(C)sum_i d_i`, this yields a quadratic-gap validity bound with `alpha_F=D0/(2ns0)`. Transfer every covering or arcsine lower bound through the owned hybrid events with `alpha_eff=min(alpha,alpha_F)`.

Under ND1 alone, only the minimum face distance is localized. The isolated-minimum integral theorem correctly decomposes propagated points into face layers of thickness `O(m+eps)`. The small-gradient condition compares `m` at a layer point and its face projection. Quadratic growth then makes the residual `(n-1)`-dimensional integral uniformly finite, while the full `n`-dimensional node integral is logarithmic. This result requires `n>=2`, as stated in the source context. For a compact curve with all unit-tangent coordinates bounded away from zero, every coordinate is monotone along each connected arc, so its measure in each face slab is controlled. The relaxation contribution is `O(sqrt(eps))` and propagation contribution `O(eps)`, retaining the `eps^(-1/2)` lower rate. Do not infer a general positive-dimensional ND1 theorem: for dimension at least three the recorded argument only gives an `eps^(-1)` lower bound.

The closeout phrase that cutoff propagation escapes the bounds “only through one-sided expression graphs” is unsupported. The proved statements are sufficient exactness under one-sided/local-exactness conditions and sufficient persistence under CND or specified ND1 hypotheses. They leave representations and dimensions outside those classes unresolved.

### 7.4 Round cost

The expanded-quadratic HC4 recurrence and the arctangent potential prove `Omega(eps^(-1/2))` rounds for the specified schedule. They do not prove this for every equivalent expression, every schedule, or every fair contractor. The lifted `u-2u^2`, `u=t^2`, recurrence proves `O(log log(1/eps))` rounds under its initial-range assumption. The corresponding rate for a different monomial representation was not proved in the source and should not be inferred.

The cancellation-based round-count rule and the bounded-round lower-rate conjecture remain unproved. The numerical “observed Theta” phrasing should be written as an observed scaling trend. A one-node ideal propagation certificate can be more expensive in rounds than a logarithmic-node relaxation tree; no practical speedup follows from the node count alone.

## 8. Higher-order claims and scope limits

The order-`k` covering theorem is sound under its explicit vertex-distance lower gap and width-`k` upper error. State `k>=1` for the source's factor-`2^n` running-supremum comparison, since its proof uses `ceil(2^(1/k))=2`; for `0<k<1` the covering constant must change. The result is about a sharp lower-gap model, not every order-`k` Taylor enclosure.

With interior minimizers and `C^{1,1}` regularity, sublevels are fat at scale `sqrt(eta)`. For `1<=k<=2`, the search scale `eta^(1/k)` is no larger, and the source's volume lower bound and integral upper bound produce the analytic exponent `n/k-lambda` when `lambda<n/k`. With only the vertex-distance lower gap, no integral lower bound is proved for `k<2`; the analytic regular-variation evaluation is what makes the volume lower bound match the integral upper bound. At `k=2,lambda=n/2`, the logarithmic rate needs the stronger quadratic arcsine gap, not merely the volume bound.

For `k>2`, the same RLCT need not give the same exponent. The strip `y^2` and isolated quartic `x^4+y^4` examples demonstrate this directly. Their covering exponents, combined with the dyadic upper bound, determine polynomial exponents even when a logarithmic comparison loss remains. The Morse–Bott order-`k` proof for `k>=2` is complete after its tube-count argument: the tube radius is `O(s^(k/2))<=O(s)`, the number of grid boxes is `O(s^(-p))`, and the geometric sum gives `eps^(-p/k)`. For isolated growth `m≈sum_i|t_i|^(q_i)`, the covering exponent is `sum_i(1/k-1/q_i)_+`; this is invariant under a locally bi-Lipschitz coordinate change, with fixed metric constants.

## 9. Corrections and unresolved claims to track in the claim map

Required corrections:

1. Split arbitrary-cover, arbitrary-partition, and guillotine-tree benchmarks.
2. Replace closed-piece validity by owned-region validity, with retained boundaries carried forward.
3. State reduction/phase versus actual-node, augmented-event-node, and solve cost explicitly; count probing tests and use a fresh `K_eval` for a deduplicated source cover.
4. Permit degenerate retained boxes or exclude dimension collapse explicitly.
5. Require distinct root term nodes for the flat-sum formula.
6. Restrict the absolute-value representation construction to nonnegativity on the represented domain.
7. Use `N_tree<=2` for the kink at arbitrary tolerance; equality needs a small-tolerance condition.
8. Handle the empty-active-inequality case in the zero-dimensional KKT proof; for tube transfer require combined LICQ and multipliers for a description preserving the original exact set, relaxed violation, and exact/relaxed assignment.
9. Use the exact facewise logarithmic RLCT regimes, and keep external analytic coefficients attributed.
10. Do not state the half-box-dimension exponent without quadratic growth.
11. Qualify oblivious-rule bad-instance quantifiers and preserve the restricted Cantor polynomial-rate claim.
12. Keep strict propagation cutoff comparisons distinct from weak relaxation pruning.

Local additions now justified by complete arguments in this report:

- nonlinear-exact-constraint KKT tube transfer and logarithmic lower bound for a compatible original exact/relaxed model satisfying combined LICQ;
- divergence of bounded-tolerance covers on a one-sided feasible concave ray, with constraints;
- boundary-safe transfer of covering, stratified integral, matching-slice, and convex flat-centroid lower bounds through reductions.

Claims that should remain open or conditional:

- a general face-exact complexity characterization;
- a matching upper bound for the curved row-slice example;
- uniform polylogarithmic competitiveness of a local branching rule;
- removal of the product-integral logarithmic loss under quadratic doubling;
- whether critical face RLCT logarithms can govern the maximum in all analytic boundary cases;
- bounded-round propagation exponents in the exact case;
- ND1-only propagation effects on optimal sets of dimension at least three;
- exact original-constraint propagation on curved active strata;
- generic noisy regression two-regime asymptotics;
- general constrained bounded-count/exact-certificate equivalence beyond the special concave-ray result.

## 10. Source and verification record

Primary mathematical text inspected:

- `research-20260928b/bb-complexity/spatial-constrained/instance-dependent-node-complexity.md`: definitions, event lemma, lower bounds, tube/KKT proofs, localization, covering and stratified characterizations, regular rates, first-order package, revisions.
- `research-20260928b/bb-complexity/spatial-face-exact/face-exact-node-complexity.md`: model, gap lemmas, product and slice integrals, flat and curved lower bounds, fractional covers, exact aligned certificates, counterexamples, branching rules, and revisions.
- `research-20260928b/bb-complexity/cutoff-propagation/cutoff-propagation.md`: fixed-point model, hybrid inheritance proof, endpoint formula, witness and loss bounds, CND/ND1 transfer, round-cost statements, and revisions.
- `research-20260929/rlct/rlct-node-complexity.md`: analytic input and constants, face projection and vertex accounting, facewise characterization, learning-coefficient and noisy-toy transfer, higher-order package, and revisions.

Reviews inspected include the spatial-constrained review and recheck, face-exact review and recheck, cutoff review and recheck, RLCT review and both rechecks, the relevant closing audits, and both closeouts. These are secondary verification evidence; the proof repairs above are independently derived.

Commands actually run were read-only targeted inspections: `cat AGENTS.md paper-bb-complexity/evidence/BRIEF.md`; `rg --files` in the assigned topic/review directories; `wc -l` on the four assigned notes; `rg -n` for theorem, revision, and closeout locations; and `sed -n`/`cat` for the identified proof and review sections. No computation script or experiment was run. One broad file listing was truncated; subsequent inspections were restricted to Markdown review files and the assigned topic notes. The only write was this report, via `apply_patch`.

No CI result is asserted. This audit establishes mathematical arguments and scope corrections; external analytic theorems and coefficient tables still require the literature agent's source verification and the manuscript's own citations.
