# Referee report: tree-structured nonconvexity with dense linear coupling rows

Date: 2026-09-30. Note under review:
[`../theory-coupling/coupling.md`](../theory-coupling/coupling.md) (scripts
and logs alongside). Context read: `SYNTHESIS.md`; the decomposition note
[D] (Definition 1.2, Lemmas 1.3–1.5, 3.1, 3.2, Theorem 3.4 with its full
proof, Corollary 2.1, Lemma 2.2); the consistency note [K] (Theorem 1.1);
the waterno2 and open-instances reports, at the passages the note cites.
Independent checks are in [`coupling-review-checks/`](coupling-review-checks/)
(scripts `c1`–`c10`, logs in `logs/`). I did not edit the note and did not
commit anything.

## Verdict summary

| # | Claim | Verdict |
|---|---|---|
| 1 | Prop. 1.1: rows that define aggregate variables leave the single-tree lower bound unchanged | **correct**; one side remark is false as worded (fix F1) |
| 2a | Thm. 2.1: coupling dual = local consistency + `k` moments, `k+1` atoms, no Slater | **correct** (classical in substance) |
| 2b | Thm. 2.2: at most `k` fractional components at extreme points | **correct**; confirmed on 420 further LPs (branching trees, width 2, inequalities, generic vertices) |
| 2c | Cor. 2.3 gap bound; Ex. 2.4 gap `c n/4` with one row, width 1 | **correct**; Example 2.4 confirmed by independent code |
| 3 | Thm. 3.1: under (LQG), size of [D, Thm 3.4], independent of `k` | **correct, with small fixes** (F2, F3) |
| 4 | Thm. 4.5: partial-sum certificates, depth factor | **correct, with small fixes** (F2, F4, F5); reuse of [D] is legitimate; nothing breaks the proof |
| 5 | Thm. 5.1: `C(n+1,(n+1)/2)` leaves vs `O(n^2)` DP | **correct in its model**; (c) also holds in the box-certificate model (new check); fixes on scope and prior art (F6–F8) |
| 6 | Prop. 5.2 `exp(Omega(k)) log(1/eps)`; Prop. 5.3 NP-hardness and ETH | **correct**; one conclusion is overstated ("conditioning must enter", F9); prior art missing (F8) |
| 7 | Census: 17.7% vs 14.6% | **numbers reproduce**; interpretation needs fixes (F10–F13) |
| 8 | Novelty | **overstated in three places** (F7, F8, F14) |

No claim is false. The fixes below are scope, labeling and literature
corrections, plus three census caveats that change the headline numbers
slightly.

## 1. Proposition 1.1 (single-tree lower bound with aggregate rows)

**Verdict: correct.** I checked the proof step by step. For every `x in X0`,
the point `(x, Ax)` is feasible and lies in some leaf `B = B_x x B_y`. The
alphaBB gap depends only on `B_x`, and `y` carries no cost. So
`m(x) + eps >= sum_j alpha_j a_j^{B_x}(x)` holds for that leaf. The
integrand inequality sums over all leaves whose `x`-projection contains `x`.
Several leaves may share a projection; each is counted once, and each leaf's
integral is bounded as in [C, Thm 3.1]. The proof only needs the leaves to
cover the feasible set, not all of `X0 x Y`. The result is the observation
that the feasible set projects onto `X0`; it is correct and close to
trivial.

**F1 (false side remark).** Section 1, first bullet: "When a row can be
solved for `k` variables that enter the objective convexly (as `y` above),
... the bound is unchanged." In the proposition, `y` has **zero** cost. With
a convex cost `g(y)` the argument runs on `F_n(x) + g(Ax)`: the minimizer
can move (if `g` has linear terms), and `H` becomes `H + A^T ∇²g A`. This
rank-`k` update lowers the bound by the factor
`det(I + H^{-1/2} A^T ∇²g A H^{-1/2})^{-1/2}`. The exponential base in `n`
survives for fixed `k`, but the bound is not "unchanged". Restrict the
remark to cost-free aggregates, or state the determinant factor. The Summary
item 1 should also say "cost-free aggregate variables".

## 2. Coupling dual, tree Shapley–Folkman, per-bag failure

**Theorem 2.1: correct.** The proof uses Sion's theorem on
`P(X0) x R^k`, with `P(X0)` weak*-compact and `phi` affine and continuous in
`nu`. It then uses Dirac minimizers, Vorob'ev gluing on the tree
(running intersection makes edge consistency sufficient) and Carathéodory on
a face of dimension at most `k` of `conv{(F(x), Ax)}`. Each step checks. The
face step also covers the case where the hull has empty interior. "No
Slater" is right because the primal side is compact; attainment of the
multiplier is not claimed. This is classical in substance (Aubin–Ekeland;
Udell–Boyd, Appendix A). On a path it is the known fact that the Lagrangian
dual of a resource-constrained shortest path mixes at most `k+1` paths
(Handler–Zang 1980; from memory). Minor: "nonempty" in Theorem 2.2 needs
`K ≠ ∅`.

**Theorem 2.2: correct.** Steps checked:
- the perturbed component measure `(1-s) rho + s rho^E` is a probability
  measure for `s in [-p/(1-p), 1]`;
- it is absolutely continuous with respect to `rho`, so every separator
  marginal that leaves the component stays the same Dirac measure;
- the directions live on disjoint sets of bags, so they are independent;
- when `q > k`, a kernel element gives a two-sided perturbation inside `K`.

Empty separators are Dirac trivially. The component count genuinely
refines "`k+1` atoms": two atoms can differ in many places separated by
agreeing separators. That configuration is not extreme, and the theorem
explains why.

- *Independent check* (`c4_tree_sf.py`, 420 LPs). The author's script covers
  paths with optimal vertices only. Mine adds random tree decompositions
  with up to 3 children per bag, separators of size 2, bags with 2 new
  variables (width 2), `<=` rows (counting active rows), and random
  objectives, so the basic solutions are generic extreme points of `K`.
  Violations: 0. The bound is attained in every setting. All 9 bags can be
  fractional while there are at most `k` components.

**Corollary 2.3: correct.** Jensen's inequality on each glued component and
the exact values on deterministic bags give the equality and the bound. The
mean point needs a convex box domain, as the note says.

**Example 2.4: correct.** The penalty chain is
`F(x) = sum_i c x_i(1-x_i) + M sum_i (x_i - x_{i+1})^2` on `[0,1]^n` with
the row `sum_i x_i = n/2`. Checked by hand:
- `D = 0`, because `F >= 0` and the half–half mix of all zeros and all ones
  is consistent and meets the row;
- `|x_i - 1/2| <= Delta`, because the mean `1/2` lies between the minimum
  and the maximum;
- Cauchy–Schwarz along the path gives `sum (x_i - x_{i+1})^2 >= Delta^2/(n-1)`;
- `rho(a_t) <= c/2`, because `vex(g + h) >= vex g + h` for convex `h`.

The unique optimal measure is that half–half mix, one component covering
the whole path. Independent checks (`c3_penalty_chain.py`):
- *Optimum by exact-row grid DP.* A DP over `(x_i, partial sum)` gives
  `OPT = c n/4` at `M = c n(n-1)` for `n = 6, 10, 16`, and `0.75` at `M = 1`
  (agrees with the note). At `M = 10` the DP gives the grid upper bound
  2.475, consistent with the note's SLSQP value 2.47284.
- *Per-bag nonconvexity.* A convex-hull envelope gives `rho = 0.5000` for
  the two-term bag and `0.2500` for one-term bags.
- *Threshold on `M`.* `M >= c n(n-1)` is sufficient but conservative. The
  empirical threshold for `OPT = c n/4` is 3.74, 10.9 and 26.7 at
  `n = 6, 10, 16`. This is within 7% of the second-order threshold
  `c/(2 - 2cos(pi/n)) ≈ c n^2/pi^2`, so the example works with `M` about
  `pi^2` times smaller.
- *Optional strengthening.* Splitting each `c x_i(1-x_i)` evenly between the
  two bags that contain `x_i` gives `max rho = c/4` and a gap of
  `n · max rho`.

## 3. Theorem 3.1 (exact Lagrangian: coupling costs nothing)

**Verdict: correct, with small fixes.** Checked:
- (a) the slopes are unchanged, because `R_s ∩ S_t = ∅` for `s in sub(t)`;
- (b) the linear terms cancel in the Taylor brackets of [D, (3.1)], since
  `z^t` and `x_{V_t}` differ only on `S_t`;
- (c) Young's inequality with weight `c_L/16` and
  `4 delta^2 ||A||^2/c_L <= eps/8`;
- (d) the collected coefficient `1 - 7/16 - 1/16 = 1/2` and the additive
  error `7/8 eps`.

The reuse of [D, Thm 3.4] with a reference point that is not the minimizer
of the tree objective `F + mû^T(Ax - b)` is legitimate. In [D], `x*` enters
only as the shell centre (`|x̂ - x*|_inf <= h`), as the base point of the
slopes `lambda_t(x*)` in Lemma 3.2 (which holds for any `x°`), and in
`|∇a_t(x) - ∇a_t(x*)| <= M_a r_t`. None of these uses optimality.

- **F2 (labeling).** Theorem 3.1 step 3 and Theorem 4.5 step 1 say "steps
  1–5 of [D, Thm 3.4] ... give `E <= (7/8) c̃ X^2 + (3/4) eps`." In [D] that
  bound is assembled in **step 6**, using (T2), (T3) and `h <= h_0`; (QG)
  enters only in the last sentence of step 6. Say "steps 1–6 of [D,
  Thm 3.4] up to the final use of (QG)". Section 10 item 2 asks the referee
  to check this: **no step of [D] before that sentence uses (QG) or the
  optimality of `x*`.**
- **F3 (lnts).** "lnts is this case" (Summary item 3, Section 7.2) should
  say "consistent with this case". (LQG) was not verified for lnts. The
  global variable `h` lies in every separator and is outside the theorem.
  The lnts certificate was a closed-form Lagrangian, not a decomposition
  certificate, so Theorem 3.1 was not needed there.

## 4. Theorem 4.5 (partial-sum certificates)

**Verdict: correct, with small fixes.** I rederived every inequality.

- *Lifted model.* `Sigma_t` equals `A_t X0_{R_t} + sum_u Sigma_u` (the
  interval hull of a Minkowski sum over disjoint variables), so
  `zeta_t(z) in Sigma_t` and the cells cover all child-side values. Lemma
  4.3 holds by the induction of [D, Lemma 1.3]: take a minimizer `x` of
  `Phi_t(s, sigma)` and `z = (x_{V_t}, (sigma_u(x))_u)`. The (LC) programs
  stay convex because `zeta_t` is affine.
- *Lemma 4.4.* The induction
  `zeta_t(z^t) = sigma_t(x) + sum_{u in sub(t), u ≠ t} delta_u` is right,
  and with `eta_t = -mû` the drift enters `g` only through
  `rho|r + sum delta|^2`. The first-order cancellation is exact.
- *x-part.* Leaves and cells are products of `x` and `sigma` boxes, and
  product boxes meet iff each factor meets. So the `x`-parts of a
  configuration satisfy exactly [D]'s configuration conditions, and [D]'s
  analysis applies verbatim with `c̃ = c_g/8`. The partial sums depend only
  on `x_{R_t}`, which is exact at the consistent point, so `x`-drift and
  `sigma`-drift do not interact. Column assignment to top bags is what makes
  this work.
- *Step 4.* `e_t <= 4h_sigma + theta_sigma(s_t + sum_{siblings}(s_u + e_u))`
  is valid; the note uses a sum where a max would do.
  `sum_t s_t <= Y + dE` holds because each node has at most `d` proper
  ancestors, and the sibling sum is at most `Delta(Y + dE + E)`. So
  `E(1 - theta_sigma((1+Delta)d + Delta)) <= 4h_sigma|T| + theta_sigma(1+Delta)Y`,
  and (T4) gives the factor 2.
- *Steps 5–7.* `Y <= (d+1) alpha_A X`, since each `u` lies in at most
  `d+1` subtrees. The Young constants (`c_g/32`, `c_g/64`, `8/c_g`,
  `16/c_g`) check. The collected coefficient is `12/64 < 1/4` and the
  additive error is `15/16 < 1`.
- *Constants.* `K/c_g <= kappa^2 (1 + M_F/c_g)^2` holds. `nu_A` is invariant
  under scaling of `A`. The bound
  `alpha_A <= sqrt(|T|) max_t ||A_t||_{2->inf}` follows from Cauchy–Schwarz
  over the disjoint sets `R_t`.

**Role of `d`.** Depth enters twice, both through uniform-ratio shells
around `sigma*`:
1. solving the drift recursion, `theta_sigma((1+Delta)d + Delta) <= 1/2`,
   because a partial sum inherits all drifts below it;
2. the accumulation `Y <= (d+1) alpha_A X`, which is tight within a factor 2
   for a row of ones on a path with `x - x*` along the row.

The note is right to call its necessity open. Its "fake feasibility"
heuristic (drifts summing to about `-r`) is plausible, but I did not verify
it either.

**Anything missing?** Nothing that breaks the proof. Small items:
- **F4.** Lemma 3.1 requires the shell centre to lie in the box: state
  `sigmâ_t in Sigma_t` (possible, since `sigma_t(x*) in Sigma_t`).
- **F5.** The one-line forms drop factors. Section 8 item 3 and the
  Summary write `(C d sqrt(k) nu_A cond^2)^{k Delta_1}`; the proof gives
  `((1+Delta)(d+1)(sqrt(k) nu_A cond^2 + 1))^{k Delta_1}`, so the
  `(1+Delta)^{k Delta}` factor is hidden in "C". The shallow-tree form
  `exp(O(w + k Delta log(k log n)))` drops `(nu_A cond^2)^{k Delta}`. Both
  should be written out or stated as "for bounded `Delta` and bounded
  conditioning".

Proposition 4.6 is also correct:
- (a): the `H`-orthogonal splitting, Sylvester's law giving positive index
  `k - p` on the complement, and Finsler's lemma;
- (b): immediate;
- (c): with `eta_t = 0` the root penalty has zero slope at `x*`, so only the
  second-order drift term remains; the multiplier tolerance still involves
  `||A||`, not `||RA||`.

Vavasis (1992) is prior art in spirit for (c) and should be cited (F8).

## 5. Theorem 5.1 (Jeroslow-type lower bound)

**The model** as stated in (b):
- *Branching:* spatial B&B on `[0,1]^n`, any variable and any split point
  at every node, any node order, any incumbent `UBD >= OPT`.
- *Node bound:* at most `D(B)`, the box Lagrangian dual. For separable
  blocks and one row, `D(B)` is the termwise-envelope (chord) continuous
  knapsack.
- *Excluded:* bound tightening and cuts.

**Verdict: correct in this model.**
- *Step 1.* `0 < n/2 - a` because `a <= |z| <= m`, and
  `n/2 - a < |z'| - a <= |P|`. Off `P`, each `y_i in {0,1}` is an endpoint
  of `B_i`, where the envelope equals `f = 0`.
- *Step 2.* A low subcube holds at most its top point of weight `m` and a
  high subcube at most its bottom point of weight `m+1`.
- *Step 3.* This gives an injection from the `C(n,m) + C(n,m+1)` points into
  the leaves. Leaves closed by infeasibility are included, because the
  constructed point is feasible.

Independent checks:
- `c1_jeroslow.py`:
  - the chord-knapsack bound equals `max_mu L_B(mu)`, computed by exact
    breakpoint search, on 3000 random boxes (maximum difference 4.4e-16);
  - my own depth-first B&B with 4 branching rules gives exactly
    `C(n+1,(n+1)/2)` leaves for `n = 3..13` with 3 deterministic rules, and
    more with random splits.
- `c2_min_tree.py`: the **exact minimum** number of leaves over all trees
  whose split points lie on a grid equals `C(n+1,(n+1)/2)`:
  - `n = 3` with grids of step 1/10 and 1/12;
  - `n = 5` with split points {1/4, 1/2, 3/4} and {1/3, 1/2, 2/3};
  - `n = 7` with split point {1/2}.
- *FBBT (outside the model).* Propagating the row before bounding changed no
  count, neither in `c1` nor in the exact minima of `c2`. The proof's step 1
  genuinely fails under FBBT: tightening can move `P`-coordinates off
  `[0,1]`. So extending the theorem to bound tightening is open, but these
  small cases suggest it holds.

**Part (c): correct, and it holds in the note's certificate model.** The DP
claim ("`O(n^2)` pieces") is an exact symbolic DP, while Table 6.2 compares
it with B&B leaves. I built a lifted partial-sum certificate in the model of
Section 4.2 (`c8_lifted_jn.py`, `c8b_validity.py`): cells of side 1/2 on
the partial sums with chord minorants, and leaves aligned with the child
cells.
- It proves `l_r = c/4 = OPT` **exactly**, with about `3 n^2` boxes:
  1,802 boxes at `n = 25` (versus `C(26,13) = 10,400,600` leaves) and 4,922
  at `n = 41`.
- Every minorant equals the true value function `c phi` at the cell
  endpoints and is continuous across cells, so the strict (CM) holds.
- With cells of side 1 the root bound is 0: the same bound as the
  Lagrangian dual, so no progress.

**Recommend adding this**, because it puts both sides of Table 6.2 in one
model.

- **F6 (scope).** Summary item 6 and Section 4.5 omit "no bound tightening".
  Add it, together with the FBBT evidence above.
- **F7 (novelty).** The count is not new in itself. For Jeroslow's binary
  instance (`max x_1`, `2 sum x_i = n`, variable fixing), a node is a leaf
  iff `m+1` ones or `m+1` zeros are fixed. So **every** such tree has
  exactly `C(n+1,(n+1)/2)` leaves, a lattice-path count (`c9_jeroslow_binary.py`
  confirms it for `n <= 25`); Jeroslow's stated bound is `2^{(n+1)/2}`.
  What Theorem 5.1 adds is the transfer to continuous spatial branching with
  arbitrary split points and Lagrangian/envelope node bounds. Say so, and
  compare with Dey–Shah (ORL 2022), an exponential B&B lower bound on
  instances that a DP solves in polynomial time (the same message for MILP),
  and with Dey–Dubey–Molinaro (MP 2023). Both are in `literature/papers`.
- **F8 (prior art for (c) and Prop. 5.3(a)).** Vavasis (Math. Prog. 1992,
  Section 3; local copy) gives exactly this partial-sum DP for separable
  concave quadratic knapsacks, with piecewise concave quadratic value
  functions (his Theorem 4). His Theorem 2 gives running time
  `O([n(n+1)/sqrt(eps)]^t)`, where `t` is the number of negative
  eigenvalues, which is directly relevant to "the exponent counts bad
  directions" (Prop. 4.6, Prop. 5.2). NP-hardness of the concave quadratic
  knapsack is Sahni (1974); Moré–Vavasis (1991) characterize its local
  minima (one fractional coordinate).

## 6. Propositions 5.2 and 5.3

**Proposition 5.2: correct.** Checked:
- the decomposition `|x|^2 = |x_⊥|^2 + |s|^2/gamma^2`, with
  `lambda = 1/gamma^2 - beta = 0.8 m`;
- the growth constant `min(1/2, lambda gamma^2/2)`;
- the Hessian `diag(I_m, -beta I_k)`;
- `D < OPT` by Prop. 2.6(c); the dual optimum is attained, since `0` is
  interior to the set of residuals;
- the integral bound: the change of variables, `R/sqrt(eps) = sqrt(lambda'/(8k^2 eps))`,
  `T^2 >= 1.25 lambda' >= m >= k`, and the Stirling form;
- part (c): Lemma 2.2's proof only needs a map `s -> (x(s), s)` into
  feasible points, which exists here.

`c5_prop52.py` confirms `|a_j|_2 = gamma`, `|a_j|_1 = 1/2`,
`A A^T = gamma^2 I`, `max |x_i(s)| = 1.000` on `S_0` (tight), and
`alpha/lambda' = 1.730` at `m = 4, k = 1` (base 2.447), tending to 2 (base
2.63).

*Strengthening worth adding.* For `m >= 4`, `h'' <= -(beta - 12) < 0` on
`[-1,1]`. So the convex envelope (chord) of `h` on any box has gap at least
`((beta - 12)/2) q_B`, and the bound extends to envelope node bounds. For
this separable instance those are exactly Route L's Lagrangian node bounds.
The base with `alpha' = (beta-12)/2` is 1.91 at `m = 8`, 2.30 at `m = 16`,
and tends to 2.63. So `exp(Omega(k))` also holds for Route L, not only for
alphaBB.

**Proposition 5.3: correct.**
- (a): the rounding argument with `delta = 1/(sum a + 1)`.
- (b): the reduction. The integer bound `z_i <= ||b||_inf` uses nonnegative
  columns; `|A(y - z)|_inf <= l delta < 1`; and `sin(pi delta) >= 2 delta`.
- I checked the KPW statement on arXiv 1811.01296: for `A in {0,1}^{k x l}`,
  no `2^{o(k log k)}(l + ||b||_inf)^{o(k)}` algorithm exists under ETH. It
  matches the note.

Caveats:
- State the computational model. Exact evaluation of `sin^2` is not a
  Turing-machine operation; an oracle or real-RAM model is implicit.
- **F9 (overstated conclusion).** "Conditioning must enter any such bound"
  (Summary item 7; Section 5.3) does not follow. ETH excludes
  `poly(n, s0) 2^{O(k)} polylog(1/eps)`, but it allows running times
  `(n + s0)^{O(k)}` (Papadimitriou) or `2^{O(k log k)}`-type bounds
  (Eisenbrand–Weismantel). The correct conclusion: some dependence beyond
  `poly(n, s0) 2^{O(k)}` must enter, on `k log k`, on the scale `s0^{Omega(k)}`,
  or on conditioning. The note's own caveat, that ETH bounds running time
  and not certificate size, should also appear in the Summary.

## 7. Census (Section 7.3)

**Reproduction.**
- `c10_census_recount.py` recomputes every table entry from the author's
  JSONL files with my own code, including 83 → 85 and "25 candidates, 19
  open". All match.
- `c6_census_sample.py` reruns both heuristics (the author's code) on 16
  instances, including waterno2_03 and kriging_peaks. `k_heur`, `k_bag` and
  the full width traces are identical to the logs (16/16).

**Issues.**
- **F10 (rows outside the theory).** The heuristics remove any row: linear
  or nonlinear, equality or inequality, with or without integer variables.
  Sections 3–4 cover linear equality rows; slacks handle linear
  inequalities. Classifying the rows removed by the bag rule
  (`c7_candidate_rows.py`):
  - Of the 25 candidates, 13 use only linear equalities, 7 include linear
    inequalities, and 5 include **nonlinear** rows: casctanks,
    kall_ellipsoids_tc03c, powerflow0030r, tln12, wastepaper6 (all 4 rows
    nonlinear). Four of these five are among the 19 open instances.
  - Of the 18 instances gained at `k <= 8`, only 9 use linear equalities
    only, and 14 use linear rows only. The headline "17.7%" becomes 16.2%
    (linear equalities) or 17.0% (linear rows).
  - kall_ellipsoids_tc03c has nonlinear width 14 > 12, so it is not a
    "small `w`" instance. It reaches width 12 only because dualizing its
    nonlinear rows splits their terms into separate factors.
- **F11 (non-monotone width bound).** Dropping "free" rows raised the
  min-degree bound in 44 instances. casctanks has width 11 with all rows but
  15 after dropping free rows, so its "`k = 2`" is spurious (it is a
  `k = 0` instance). Take the minimum of the two bounds. The effect: `k = 0`
  becomes 86 (14.8%), and 24 candidates remain, of which 19 are open.
- **F12 (the "median 43.5 rows" statistic is capped).** In the gap class
  (290 instances with a width), the bag rule:
  - reached width 12 in 82 (median 28 rows removed);
  - hit the 64-row cap in 121 (median width 99 → 71);
  - stopped in 77 because the width-attaining bag had no row hub (median
    15 rows removed, width 40 → 30);
  - hit the time cap in 10;
  - had a width timeout in 4 (these have no starting width and are excluded
    from the 290).

  So the median of 43.5 mostly reflects the caps and the early stops. The
  qualitative conclusion is still supported: 121 instances keep median width
  71 after 64 rows. Report the breakdown, and note that the rule's stop
  condition overestimates `k` when earlier-eliminated rows cause the width.
- **F13 (reproducibility).** The last three lines of
  `logs/census_k_summary.log` (gap-class median 49.5, "bag rule: rows
  removed median 43.5 ...", "removed-row degree median 14") are not printed
  by `census_k_analyze.py`, and no script in the repository prints them.
  Add the code; `c10_census_recount.py` reproduces the numbers. Also,
  Section 6.1's "a large census width can only be removed by dualizing at
  least that many rows" applies to true treewidth, not to a min-degree upper
  bound.

## 8. Novelty

- *Theorem 2.1:* classical in substance, as the note's table says. The
  constrained-shortest-path mixture result on paths should be mentioned.
- *Theorem 2.2 and Example 2.4:* I found no identical statement. The
  statement is elementary, and it refines the known "`k+1` atoms" in a
  useful way. The note's hedged claim is fair.
- *Theorem 3.1:* a corollary of [D], as stated.
- *Theorem 4.5:* no prior instance-dependent size bound for coupled tree
  problems is known to me. The exact first-order cancellation by
  `eta_t = -mû` is a clean observation.
- **F14 (Prop. 4.6).** "The consequence for certificate size appears new":
  add Vavasis (1992) Theorem 2, where the complexity is exponential only in
  the number of negative eigenvalues, as the closest prior result. The
  certificate-size version with lifting of `p` row combinations is still
  distinct.
- *Theorem 5.1:* see F7. The count equals the exact tree size of Jeroslow's
  binary instance. The continuous, arbitrary-split, Lagrangian-bound model
  is the contribution. Part (c) is Vavasis's DP (F8).
- *Propositions 5.2 and 5.3:* 5.2 is [D, Prop. 2.3]'s mechanism in
  aggregate coordinates, as stated. 5.3(a) is Sahni (1974) in substance.
- *Shapley–Folkman sources.* Udell–Boyd (Theorem 1, `min(m̃, n)` largest,
  extreme points) and Dey–Xu (Theorem 3, shifted right-hand side) are
  described accurately; I checked both against the local full texts.
  Kerdreux et al., Bertsekas and Aubin–Ekeland are cited from memory and
  consistent with my recollection.

## Other items checked

- *Prop. 2.5 and 2.6: correct.* In 2.6(c), attainment of the dual optimum
  is automatic when `x* in int X0` and `A` has full row rank, because `b` is
  then interior to `A X0`; that hypothesis can be dropped.
- *Lemma 4.1 and Cor. 4.2: correct.* The proof uses the Euclidean
  projection onto `P_b`, the Lipschitz gradient on the segment inside the
  convex box, and the constant `K` as stated.
- *Section 7.1 (waterno2).* The +0.0005 gain from horizon bins was on
  waterno2_06 ([W] line 355). The SCIP incumbent 113.29 at `mu = 194.26`
  (`logs/horizon_only_34.log`) is an upper bound on `L(mu)`, so "a gap of at
  least 1.5% at that multiplier" is right. Given that, "the horizon row is
  harmless" (Summary item 8) is too strong. It is "not the bottleneck of the
  wave-2 certificate"; the horizon-only Lagrangian at its best multiplier
  was not computed.
- *Tables of Section 9:* they match the author's logs (Jeroslow, penalty
  chain, tree SF LP, census).

## Required and recommended fixes (priority order)

1. F9: replace "conditioning must enter" with the correct ETH consequence,
   and carry the time-versus-certificate caveat into the Summary.
2. F10–F13: census. Classify removed rows (linear/nonlinear,
   equality/inequality) and report headline shares for linear rows; use
   `min(w_full, w_free)`; report the bag-rule stop reasons; add the code for
   the last log lines; drop kall_ellipsoids_tc03c from the "small `w`" list
   or flag it.
3. F7, F8, F14: literature. Jeroslow's exact count; Dey–Shah and
   Dey–Dubey–Molinaro; Vavasis (1992) for the DP and the
   negative-eigenvalue complexity; Sahni (1974) and Moré–Vavasis (1991).
4. F6: add "no bound tightening" to Summary item 6, with the FBBT evidence.
5. Add the exact lifted box certificate for `J_n` (about `3 n^2` boxes) to
   Theorem 5.1(c) and Table 6.2.
6. F1: correct the convex-cost remark after Prop. 1.1.
7. F2–F5: labeling of the [D] steps, `sigmâ_t in Sigma_t`, the full
   constants in the one-line size forms, and "lnts is consistent with"
   instead of "lnts is".
8. Optional: Prop. 5.2 extends to envelope (Route L) node bounds; Example
   2.4 works with `M ≈ c n^2/pi^2`, and with the split assignment the gap
   is `n · max rho`.

## Commands run

All from `research-20260929/reviews/coupling-review-checks/` unless noted,
with Python 3.13.11, NumPy 2.5.1 and SciPy 1.18.0. These are targeted checks
of this note only. No project-wide verification was run and no CI status or
logs were consulted.

| Command | Log | Result |
|---|---|---|
| `python3 c1_jeroslow.py` | `logs/c1_jeroslow.log` | chord bound = box Lagrangian dual (4.4e-16); leaves `>= C(n+1,(n+1)/2)`, equal for 3 deterministic rules, `n <= 13`; FBBT changes nothing |
| `python3 c2_min_tree.py` | `logs/c2_min_tree.log` | exact minimum over split grids = 6, 6, 20, 20, 70 (`n = 3, 3, 5, 5, 7`), with and without FBBT |
| `python3 c3_penalty_chain.py` | `logs/c3_penalty_chain.log` | `OPT = c n/4` at `M = c n(n-1)`; `rho` = 0.5 / 0.25; `M` threshold about `c/(2 - 2cos(pi/n))` |
| `python3 c4_tree_sf.py` (after replacing a `None` objective with zeros) | `logs/c4_tree_sf.log` | 0 violations in 420 LPs; bound attained |
| `python3 c5_prop52.py` | `logs/c5_prop52.log` | constants confirmed; envelope bases 1.91 (`m = 8`), 2.30 (`m = 16`) |
| `python3 c6_census_sample.py` | `logs/c6_census_sample.log` | 16/16 identical to the author's logs; row classes |
| `python3 c7_candidate_rows.py` | `logs/c7_candidate_rows.log` | 13 linear-equality, 7 with inequalities, 5 with nonlinear rows |
| `python3 c8_lifted_jn.py`; inline `certificate(n, N)` loop | `logs/c8_lifted_jn.log`, `logs/c8_lifted_jn_exact.log` | exact `l_r = c/4` with about `3 n^2` boxes (`h = 1/2`) up to `n = 41`; `h = 1` gives 0 |
| `python3 c8b_validity.py` | `logs/c8b_validity.log` | minorants equal the value function at endpoints; no jumps |
| `python3 c9_jeroslow_binary.py` | `logs/c9_jeroslow_binary.log` | Jeroslow binary tree leaves = `C(n+1,(n+1)/2)`, `n <= 25` |
| `python3 c10_census_recount.py` | `logs/c10_census_recount.log` | all table entries reproduce; bag-rule stop reasons |
| inline Python in `theory-coupling/` (width consistency) | `logs/c11_width_consistency.log` | 44 instances where dropping free rows raised the bound; casctanks 11 → 15 |
| WebFetch arXiv 1811.01296 | — | KPW statement confirmed |
