# Independent review of nonlinear exact constraints and boundary ownership

Date: 2026-10-05. Reviewer: GPT Sol. Scope: the local nonlinear exact-constraint repair and owned-set accounting in `AUDIT-SPATIAL.md`, compared with the spatial-constrained source. This is a mathematical review, not a literature review. I read `AGENTS.md` and `BRIEF.md`. I did not rerun experiments, inspect CI, run project-wide checks, add literature sources, or edit another file.

## Verdict

The nonlinear constraint-preserving construction is correct. It extends the source's Lemma 5.5 and Theorem 5.7 from affine exactly kept constraints to a compatible finite `C^2` constraint description satisfying LICQ. It gives both the local covering transfer and the logarithmic lower bound on a positive-dimensional active stratum. Neither strict complementarity nor SOSC is needed for this lower bound. The uniformity in the tolerance, including the inverse maps, graph Hessians, area Jacobians, and coordinate multiplicities, can be proved with `C^2` data alone.

The rectangular ownership repair is also correct. It preserves retained boundaries, handles dimension-collapsing reductions, and transfers the covering, arcsine, matching-slice, and flat-centroid lower bounds. A closed slab containing feasible points on its boundary need not be valid there; its owned subset is the object that must satisfy the inequality.

Three integrations require explicit statements. First, LICQ must hold in a description compatible with the original exact set and relaxed violation function. An arbitrary replacement description of the feasible set is insufficient. Second, tube witnesses are generally infeasible, so their argument uses all terminal owners and the owned tube dichotomy, not only the feasible-owner count. Third, node counts must include virtual probe partitions when their child bounds supply a certificate. An actual search-node count alone can omit arbitrarily much probing work. The deduplicated evaluation cover also needs its own count; it is not the number of the original terminal owners.

I reinspected the revised audit after the author addressed these points. Its compatible-description requirement, all-owner tube lemma, augmented event count, and separate evaluation covers now resolve the substantive issues. I approve the repaired local theorem and boundary transfer within that scope. The complete statements and proofs below can be used independently of the audit's presentation.

## Locators and issues

The audit locators in this section refer to the version first reviewed, before the parallel clarification edits. The source locators are unchanged.

| Location | Finding | Required statement or repair |
| --- | --- | --- |
| Audit Section 5, line 261; source Lemma 5.5, lines 1063–1071; source Theorem 5.7, lines 1136–1147 | The exact/relaxed partition is essential. The instruction to replace redundant constraints by an LICQ description could be read too broadly. | Require a local finite `C^2` description of the unchanged exact set, together with the original relaxed functions defining `v`; use LICQ and KKT multipliers for that same tuple. |
| Audit Section 5, lines 265–281 | The IFT equations and preservation argument are correct. | No change to the construction is needed. The proof below supplies the derivative identity and uniform constants explicitly. |
| Audit Section 5, lines 293–305; source Proposition 5.6 and Theorem 5.7, lines 1110–1209 | The shifted geometry is correct, but the common projection ball and the Jacobian relative to the original stratum should be quantified. | Use the fixed projection ball, inverse-map bounds, and relative area factor proved below. A subset of the larger graph inherits its two-point inequality; it need not itself have a convex projection domain. |
| Audit Section 5, line 307; source Theorem 5.7, lines 1195–1209 | The logarithm follows for curved and flat strata. A vanishing Lagrangian Hessian must not cause division by zero in an explicit prefactor. | Choose any positive quadratic upper constant, increasing it to at least one. If the objective is constant on the stratum, the integral is even larger. |
| Audit Section 2.3, lines 57–85; source Lemma 2.1, lines 357–415 | The ownership construction repairs the false closed-frame assertion. | Retain boundaries in the continuation, require validity only on an owner, and record emptying reductions as terminal events. |
| Audit Section 2.3, line 91; source flat-stratum Theorem 3.6, lines 555–584 | The centroid argument remains valid for half-open rectangular owners. | Use the closure of the convex intersection for widths and centroid integration; its relative boundary has zero volume, and its centroid belongs to the original intersection. A proof is below. |
| Audit Section 2.3, lines 69–85, and Section 5, lines 287–305; source Lemma 2.1(c), lines 373–412 | Feasible-owner accounting alone does not establish the tube transfer for a run. | State the dichotomy on `A_e ∩ P_ex`, keep all owners, and exclude original-feasibility reductions. |
| Audit Section 2.4, lines 97–103; source Lemma 2.1 and remarks, lines 361–364 and 424–428 | Virtual probe children need accounting; a source cover may have fewer members than the original owner partition. | Use augmented event nodes for node statements and a fresh `K_eval` for the source cover. Charge each relevant reduction round to a distinct counted evaluation. |

## A compatible description is necessary

Let the unchanged original relaxed constraints be `g_j <= 0` and `h_k = 0`, so their violation function remains

`v(x) = max(0, max_j g_j(x), max_k |h_k(x)|)`.

Near the point under study, require `P_ex` to equal the set defined by finitely many exact `C^2` equalities and inequalities. Include the root box inequalities as exact constraints. LICQ applies to the gradients of all equalities and active inequalities in this combined exact/relaxed tuple, and the KKT multipliers come from the same tuple. A different exact description can be used if it describes the same local exact set and preserves these hypotheses. Merely describing the same feasible set does not suffice.

For a counterexample to careless re-description, take, in dimension at least two,

`X0 = [-2,2]^n`, `P_ex = {x : |x|^2 <= 1}`, `g(x) = 1 - |x|^2 <= 0`, and `f(x) = -x_1`.

The feasible set is the unit sphere, the optimum is `f* = -1`, and the active stratum at `e_1` has dimension `n-1`. The exact-ball gradient and the relaxed reverse-sphere gradient are dependent. KKT multipliers `mu_exact=3/2` and `mu_relaxed=1` satisfy stationarity and give the relaxed inequality a positive multiplier, but LICQ fails for the actual tuple. Replacing the feasible set by a sphere equality supplies a LICQ description of that set with multiplier `1/2`; it does not preserve the exact/relaxed geometry.

Indeed, for any `beta > 0`, set

`R_B = B ∩ P_ex` and `f_B = f`.

This is a convex relaxation with a linear objective and satisfies the tube hypothesis `(T_{0,beta})`. Every point of `P_ex` has objective at least `-1`, and the root contains `e_1`, so the root bound is exactly `f*`. One box certifies every positive tolerance. There is no point of `P_ex` with objective below `f*`, hence no outward-descent witness. The compatible-description requirement excludes this instance correctly. The audit uses `f=-x_1^2` for the same geometry; its counterexample is valid in the stated abstract relaxation model as well.

## Independent nonlinear extension

### Statement

Let `z*` be a global minimizer. Suppose the compatible combined constraint tuple above is finite and `C^2` on an open neighborhood of `z*`, satisfies LICQ, and has KKT multipliers. Suppose at least one active relaxed inequality has a positive multiplier, or at least one relaxed equality has a nonzero multiplier. Let the manifold on which all active inequalities and all equalities in this tuple hold at their values at `z*` have dimension `d >= 1`.

There are a fixed relatively open stratum patch `S` containing `z*`, constants `A, j_*, M_* > 0`, and `eps_0 > 0`, such that for every `0 < eps <= eps_0` there is an injective `C^2` map `Z_eps : S -> X0 ∩ P_ex` with

`f(Z_eps(y)) < f* - eps`, `v(Z_eps(y)) <= A(m(y)+eps)`, and `J_{Z_eps}(y) >= j_*`.

Its image has coordinate multiplicity at most `M_*`, uniformly in `eps`. Consequently every finite rectangular owned certificate covering the image and satisfying the tube dichotomy with `beta > 0` obeys

`K >= c integral_S (m(y)+eps)^(-d/2) dH^d(y) >= c' log(1/eps)`

for sufficiently small positive `eps`. The constants depend on the fixed instance and local descriptions. The same construction gives the local near-optimal covering transfer.

### Constraint-preserving curves

Form the matrix of gradients of all equalities and active inequalities at `z*`. LICQ gives full row rank. Choose a right-hand-side vector that is zero on every exact constraint and every other active constraint, is one on one relaxed inequality with positive multiplier, or is the sign of the multiplier on one relaxed equality with nonzero multiplier. Solve for a vector and normalize it to obtain a unit vector `e_0`. KKT gives

`grad f(z*) · e_0 = -sigma < 0`.

Let `E` collect the active exact constraints, including active root box coordinates. All exact equalities belong to `E`. Its derivative has full row rank. Choose a constant right inverse `R` satisfying `E'(z*) R = I`. If `E` is empty, omit the correction below. Define

`H(y,t,xi) = E(y+t e_0+R xi)-E(y)`.

The derivative in `xi` at `(z*,0,0)` equals the identity. The `C^2` implicit function theorem gives a `C^2` solution `xi(y,t)` on an open product neighborhood. Since `H(y,0,0)=0`, local uniqueness gives `xi(y,0)=0` for every `y` in a smaller neighborhood. Put

`Z(y,t) = y+t e_0+R xi(y,t)`.

Then `E(Z(y,t))=E(y)` and `Z(y,0)=y`. Differentiating the equation at `(z*,0)` gives

`E'(z*) [e_0+R xi_t(z*,0)] = 0`.

Because `E'(z*)e_0=0` and `E'(z*)R=I`, this implies `xi_t(z*,0)=0` and `Z_t(z*,0)=e_0`. In addition, `Z_y(y,0)=I` for all nearby `y`, directly from `Z(y,0)=y`.

Shrink to a product neighborhood with compact closure. Continuity and the strict negative objective derivative give constants `mu > 0`, `t_0 > 0`, and `C >= 0` such that, for feasible `y` in a fixed neighborhood and `0 <= t <= t_0`,

`|Z_t(y,t)| <= 2`,

`f(Z(y,t)) <= f(y)-mu t+C t^2`.

For example, take `mu = sigma/4`, shrink so the derivative at time zero is at most `-2mu`, and bound the second time derivative of `f composed with Z`. Since all relaxed functions have bounded first derivatives on the chosen neighborhood and `|Z(y,t)-y| <= 2t`, feasibility of `y` implies

`v(Z(y,t)) <= c t`

for a fixed positive `c`. An active exact inequality preserves its feasible level at `y`; an exact equality preserves zero. Active root bounds preserve the relevant coordinate. Every inactive exact inequality and every inactive root bound has a uniform positive slack on a smaller neighborhood and retains it for small `t`. Thus `Z(y,t)` belongs to `X0 ∩ P_ex`.

This proves the needed curve version of outward descent. It does not claim a common straight ray for nonlinear exact constraints.

### Covering transfer and strict inequalities

Write `a = eta+eps > 0`. For `y` in the local near-optimal set with `m(y) <= eta`, choose `t = 3a/mu`. Require

`a <= mu t_0/3` and, when `C > 0`, `a <= mu^2/(9C)`.

Then

`f(Z(y,t)) <= f*+eta-3a+a = f*-eps-a < f*-eps`,

`v(Z(y,t)) <= 3c a/mu`, and `|Z(y,t)-y| <= 6a/mu`.

If the shifted point belongs to an owner with test box `C_e`, the tube dichotomy and `alpha >= 0` force

`beta q_{C_e}(Z(y,t)) < v(Z(y,t)) <= 3c a/mu`.

The nearest-endpoint inequality gives a vertex within sup-norm distance `r = sqrt(3c a/(mu beta))`. If also `a <= c mu/(12beta)`, the displacement `6a/mu` is at most `r`. Thus the original near-optimal points are covered by at most `2^n K` cubes of radius `2r`. Equivalently,

`K >= 2^(-n) N_inf(Y, 2 sqrt(a/alpha_eff))`, with `alpha_eff = mu beta/(12c)`.

The displacement bound requires a smaller admissible tolerance than the unit-speed straight-ray proof; the effective covering coefficient above can be retained.

### Uniform shifted geometry

LICQ gives an active-stratum graph `y(x)=z*+x+phi(x)` on a ball in its tangent space `T`, where `phi` is `C^2`, `phi(0)=0`, and `Dphi(0)=0`. Shrink so all inactive inequalities have slack; then this graph is feasible. Put `m_t(x)=m(y(x))`. Since `z*` minimizes on the graph, `m_t(0)=0` and `Dm_t(0)=0`.

Define

`W_eps(x) = Z(y(x), 3(m_t(x)+eps)/mu)` and `Psi_eps(x) = pi_T(W_eps(x)-z*)`.

Both maps are jointly `C^2` in `(x,eps)`, using the open product neighborhood supplied by the IFT. At `(0,0)`, the time derivative term is multiplied by `Dm_t(0)=0`, while `Z_y(z*,0)=I`. Therefore `D_x Psi_0(0)=I`.

On a fixed closed ball `B_r ⊆ T`, contained in the open coordinate domain, and a small compact parameter interval `0 <= eps <= eps_0`, arrange

`||D_x Psi_eps-I|| <= 1/2` and `|Psi_eps(0)| <= r/8`.

The mean-value formula along segments yields

`|Psi_eps(x)-Psi_eps(x')| >= |x-x'|/2`.

Thus each map is injective and its determinant in absolute value is at least `2^(-d)`. Every image contains the same ball `V=B_{r/4}(0)`: for `u in V`, the map `x -> u-[Psi_eps(x)-x]` is a contraction of the closed ball `B_r` into itself, because its norm is at most `r/4+r/8+r/2 < r`. Its unique fixed point solves `Psi_eps(x)=u`.

The inverse maps on `V` have first derivative bounded by two. Their second derivatives satisfy the differentiated inverse formula

`D^2 Psi_eps^(-1) = -(D Psi_eps)^(-1) D^2 Psi_eps[D Psi_eps^(-1),D Psi_eps^(-1)]`,

so they have a uniform second-derivative bound. It follows that the normal graph functions

`phi_eps'(u) = pi_(T-perp)(W_eps(Psi_eps^(-1)(u))-z*)`

are `C^2` on the common convex ball `V` with a uniform Hessian bound `K_2`. Each larger graph has the two-point inequality

`dist(z-y,T_y S_eps') <= (K_2/2)|z-y|^2`.

Use `tau=1/(1+K_2)` as a uniform positive two-point constant. Restrict the original patch to a still smaller fixed ball in `x`, small enough that its shifted projections lie in `V` and its shifted image diameter is uniformly less than `2tau/(1+sqrt(binomial(n,d)))`. This is possible because `D_x W_eps` is uniformly bounded. The coordinate-fibre argument of source Lemma 4.2 now gives

`M(Z_eps(S)) <= binomial(n,d)`

for every small `eps`, including when the original stratum is flat. Translation invariance, which the affine proof uses, is unnecessary here.

Let `B_phi = (1+sup ||Dphi||^2)^(d/2)`. The output area factor is at least the determinant of its tangential projection, whereas the input graph area factor is at most `B_phi`. Hence the Jacobian relative to stratum measure satisfies

`J_{Z_eps} >= 2^(-d)/B_phi =: j_* > 0`.

Shrink the patch and `eps_0` one last time so the time parameter is at most `t_0` and the quadratic remainder is at most `m(y)+eps` throughout. The covering calculation with `a=m(y)+eps` gives the stated strict objective inequality and `A=3c/mu`.

### Area formula and the logarithm

For a point of the shifted image in owner `A_e`, the dichotomy gives `beta q_{C_e}(Z_eps(y)) < A(m(y)+eps)`. Use the injective area formula on the preimage of this owner and the lower Jacobian bound. Source Lemma 4.1 applies directly to the Borel subset `A_e` of the test box. With

`C_(n,d) = (pi^2/d)^(d/2) sqrt(binomial(n,d))`,

each owner contributes at most

`(A/beta)^(d/2) C_(n,d) binomial(n,d)/j_*`

to the integral of `(m+eps)^(-d/2)`. The owner preimages partition the patch when the owners form a partition; a cover would also suffice for this upper estimate after summation. Thus

`K >= (beta/A)^(d/2) j_* integral_S (m+eps)^(-d/2) dH^d / [C_(n,d) binomial(n,d)]`.

On the active stratum every constraint term in the KKT Lagrangian vanishes, so `m=L-f*` there and `grad L(z*)=0`. Equivalently, `Dm_t(0)=0` already gives the needed conclusion by Taylor's theorem in graph coordinates. Choose a positive constant `M >= 1` with `m_t(x) <= M|x|^2` on a ball `B_s` in the patch. Its graph area factor is at least one. Therefore

`integral_S (m+eps)^(-d/2) dH^d >= d omega_d integral_0^s r^(d-1) (M r^2+eps)^(-d/2) dr`.

For `r >= sqrt(eps/M)`, the last integrand is at least `(2M)^(-d/2)/r`. This supplies a positive multiple of `log(1/eps)` as `eps` tends to zero. The proof applies to curved and flat strata and also when `m` vanishes identically on the patch. It uses no SOSC.

## Boundary ownership, centroid transfer, and degenerate boxes

For a live box `B` with a rectangular owner `A ⊆ B`, use one-sided ownership at a split. At a nonempty reduction to `B'`, retain `A ∩ B'`, including all retained boundaries. For each discarded point, its first coordinate outside the closed interval of `B'` determines one lower or upper slab owner. The inequalities defining those owners are strict only in the discarded coordinate; every other interval is an intersection of intervals. Thus each owner remains rectangular, convex, and Borel. These owners are pairwise disjoint and their union is exactly `A minus B'`. Each lies in its corresponding closed test slab. The construction remains true when some retained widths are zero. An emptying reduction uses the parent test box and one terminal owner.

Induction proves that all terminal owners partition the root. A feasibility-based discarded owner has no feasible point; the closed slab can contain feasible retained-boundary points and need not satisfy an inequality there. For a same-relaxation discarded feasible point, the point belongs to the parent relaxation and was removed by the objective cutoff. The pointwise gap and `q_C <= q_B` give the required inequality on that owner. Successful terminal bounds, including inherited bounds from a containing box, use the bound gap in the same way. This proves `K_F <= L+2nR_rel` for the feasible owners; emptying reduction events are included in `L`.

For the centroid transfer, let `K=S ∩ A_e`, where `S` is a convex subset of a `p`-flat and has positive relative volume on this intersection. The bounded convex set `K` and its closure have the same volume and first moments; their difference lies in the relative boundary, which has zero `p`-dimensional volume. Their centroid lies in `ri(closure K)=ri(K) ⊆ K`. Thus the centroid is an owned point even if some endpoints are open.

The supporting-hyperplane estimate can also be proved directly. Normalize one nonconstant coordinate functional on `closure K` to have range `[0,1]`, and choose a point `v` at its maximum. For `0 <= a <= 1`, the homothetic image `a v+(1-a) closure K` lies in the region where that functional is at least `a`, and has volume `(1-a)^p vol(K)`. Integrating this tail bound shows that the centroid's functional value is at least `1/(p+1)`. Applying the same argument to the negative functional bounds its distance from the other supporting hyperplane. Therefore

`d_i^(C_e)(centroid K) >= W_i(K)/(p+1)`.

Here widths are defined by suprema and infima, so endpoint attainment in `K` is unnecessary. This proves the unchanged flat-centroid per-owner estimate. If `K` has zero relative volume, it contributes nothing. Arbitrary nonconvex owners would not support this argument.

For degenerate test boxes, the factors of `q_B` in fixed coordinates vanish automatically. A dominant `d`-coordinate projection involving such a fixed coordinate can meet the box only on a zero-`H^d`-measure part of the stratum: its Jacobian is bounded below on that part, while its projected image has zero Lebesgue measure. All positive-measure terms in the area proof therefore use nondegenerate projected intervals, each with arcsine integral `pi`. The original ambient-dimension constant still works. A singleton intersects a positive-dimensional stratum in a measure-zero set. Nodes that collapse dimensions must remain legal nodes in their affine hull, or be explicitly treated as lower-dimensional subproblems.

The owned event family need not be an ordinary cover by boxes that are valid on every feasible point in their closures. Introduce an owned-certificate class if needed; do not infer `N_cov <= K_F` from these particular boxes. The lower bounds transfer because their per-test contribution estimates hold on the owned subsets. The comparisons `N_cov <= N_rect <= N_tree` remain correct for their original classes of fully valid covers, rectangular partitions, and split trees.

## Owned tube dichotomy and work accounting

For tube arguments, assume `(T_(alpha,beta))`, `alpha >= 0`, `beta > 0`, and exclude original-feasibility reductions and other operations that can remove the superoptimal witnesses independently of the relaxation. Keep all terminal owners, including owners with no feasible point. For every test-owner pair and every `z in A_e ∩ P_ex`, the conclusion is

`v(z) > beta q_(C_e)(z)` or `f(z)-alpha q_(C_e)(z) >= f*-eps`.

For a same-relaxation discarded owner, if `v(z) <= beta q_C(z)`, then `q_C(z) <= q_B(z)` puts `z` in the parent tube. The tube hypothesis gives `z in R_B`. Hence the removal predicate must be `f_B(z)>UBD-eps`, and the objective part of the tube hypothesis gives the second alternative. For a terminal successful bound from a containing source box, the same tube inclusion gives `f(z)-alpha q_C(z) >= LB(source) >= f*-eps`. For an infeasible relaxation test, the tube cannot contain a point. An emptying same-relaxation reduction uses the same reasoning on its parent box. This is the required run-transfer lemma.

Consequently the logarithmic tube lower bound is a bound on the all-owner count `K_all`, with

`K_all <= L+2nR_rel`.

The feasible-owner count `K_F` is useful for objective-gap arguments; it must not replace `K_all` in the tube argument.

Let `T_aug` count processed event-tree nodes, including virtual probe partitions whose children supply a parent bound. Then `L <= T_aug`, and

`K_all <= T_aug+2nR_rel`.

Under at most `r` relevant reduction rounds per counted node, this gives `K_all <= (1+2nr)T_aug`. Without that restriction the lower bound concerns combined node and reduction work. If actual search nodes omit the virtual probe children, no general inequality `K_all <= T_actual+2nR_rel` follows. A root can perform a large probe partition, aggregate its child bounds, and finish with one actual search node. A theorem about actual nodes must either count this probe work or prohibit it in its algorithm model.

An evaluation bound can avoid inherited-bound duplication. Gather each distinct successful source evaluation once, including every child source required by a successful minimum-of-children bound. Its source box is valid everywhere on its feasible subset under the bound gap, or satisfies the tube dichotomy under the tube hypothesis. Together with the discarded owners, these source boxes cover the witnesses that remain relevant. Use a fresh count `K_eval` for this alternative cover. If each relevant reduction round is charged to a distinct counted evaluation and all successful sources and probes are counted in `S_eval`, then

`K_eval <= S_success+2nR_rel <= (2n+1)S_eval`.

This cover can overlap, which is harmless for covering and per-box integral lower bounds. For the flat-centroid argument, each full source box has a convex intersection with the flat set, and each discarded owner remains convex. The source-cover count is not a bound on the number of the original terminal owners. Unlimited uncharged reductions or uncharged probe partitions are outside this cost statement.

## Resolution in the revised audit

I read the revised `AUDIT-SPATIAL.md` after the author incorporated the findings. The current locators are:

- Lines 273–277 require the compatible original exact/relaxed tuple and give the counterexample. This resolves the LICQ scope issue.
- Lines 97–103 prove the tube dichotomy on the owned subset, retain all terminal owners, and use `K_all`. Lines 319–323 explicitly apply that result to the shifted stratum. This resolves the infeasible-witness accounting issue.
- Lines 87 and 107 include recursively expanded virtual probe partitions and distinguish `T_aug` from actual search nodes. This resolves the probing issue.
- Lines 109–117 introduce the fresh `K_eval` and `K_eval_all` covers, explain distinct-solve charging, and retain relaxed-infeasibility sources for tube arguments. This resolves the deduplication issue.
- Lines 281–315 retain the correct `C^2` IFT and uniform-graph construction. The quantified construction in this review fills in its common-ball and relative-area details.

The revised audit contains no remaining counterexample or substantive gap in the assigned local geometry and ownership repair. Its statement on objective-owner event cost at line 107 is also valid for `K_all` under the no-original-feasibility-reduction model, by the immediately preceding all-owner count at line 103. The manuscript should state this analogue explicitly when presenting the tube complexity conclusion.

## Verification record

I inspected the mathematical statements and their proofs using targeted `rg`, `cat`, and `nl`/`sed` reads of `AGENTS.md`, `BRIEF.md`, `AUDIT-SPATIAL.md`, the spatial-constrained note, and the flat-centroid portion of the spatial-face-exact note. The first attempted spatial-face-exact filename did not exist; I located and read `face-exact-node-complexity.md`. I independently reconstructed the IFT derivative equations, the strict-descent constants, the common-ball inverse argument, the relative area Jacobian, the arcsine transfer, the logarithmic radial integral, the rectangular partition, and the centroid supporting-plane estimate. These are proof checks, not computational experiment results or CI checks.
