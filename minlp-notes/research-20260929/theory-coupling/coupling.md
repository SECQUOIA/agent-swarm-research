# Tree-structured nonconvexity with dense linear coupling rows

Date: 2026-09-30. Workstream "theory-coupling" of the September 29
program. Status: **reviewed, revised and rechecked** (review:
[`../reviews/coupling-review.md`](../reviews/coupling-review.md), checks in
`../reviews/coupling-review-checks/`; no false claim found; the revision is
listed in Section 11). A recheck of that revision
([`../reviews/coupling-recheck.md`](../reviews/coupling-recheck.md)) found
no false claim and raised minor wording, labelling and provenance items
M1–M8; the root applied M1–M7 in the text on 2026-09-30 (Section 11.1,
not rechecked). Proofs are complete unless a step is
marked "sketch" or "not proved". Computations are floating-point
illustrations, not certified values. Scripts and logs are in this directory
(Section 9).

Cited notes:

- [D] decomposition note,
  [`../theory-decomposition/decomposition-certificates.md`](../theory-decomposition/decomposition-certificates.md)
  (Definition 1.2, Lemmas 1.3–1.5, Lemma 2.2, Corollary 2.1, Lemma 3.1,
  Lemma 3.2, Theorem 3.4, Observation 4.2);
- [C] constrained node-complexity note (Theorem 3.1), as cited in [D];
- [K] consistency note,
  [`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
  (Theorem 1.1; reviewed, rechecked and confirmed, see its header);
- [W] waterno2 report,
  [`../open-instances-wave2/waterno2/report.md`](../open-instances-wave2/waterno2/report.md);
- [O] open-instances report (lnts, Section 3),
  [`../open-instances/open-instances-report.md`](../open-instances/open-instances-report.md);
- [S] scouting report on duality gaps,
  [`../../research-20260928b/scouting/decomposition-duality-gaps.md`](../../research-20260928b/scouting/decomposition-duality-gaps.md);
- census, [`../treewidth-census/census-report.md`](../treewidth-census/census-report.md).

Notation clash: [D] writes `k` for the largest number of bags that contain
one variable. Here `k` is the number of coupling rows, and [D]'s parameter
is written `k_T`.

## Summary

**Question.** Many nonconvex MINLPs have a nonlinear interaction graph of
small treewidth `w` but also `k` dense linear rows (budgets, balances,
horizon totals) that couple everything. What do such rows do to single-tree
lower bounds, to decomposition certificates, and to the choice between
dualizing the rows (Route L) and adding partial-sum variables (Route P)?

**Answers.**

1. **Single-tree lower bounds persist** (Proposition 1.1, close to
   trivial). Rows that define cost-free aggregate variables leave the
   exponential lower bound of [D, Corollary 2.1] unchanged; a convex cost
   on the aggregates changes the prefactor by a factor at least
   `(1 + ||A||^2 sup||∇²g||/lambda_min(H))^{-k/2}`, polynomial in `n` for
   rows with bounded entries (the factor is exact when the minimizer stays
   at 0), but, for fixed `k`, not the exponential base. Rows are the whole difficulty in Theorem 5.1.
2. **The coupling dual is the tree's local-consistency relaxation plus `k`
   moment conditions** (Theorem 2.1, no Slater condition). **Tree
   Shapley–Folkman** (Theorem 2.2): an extreme optimal solution has at most
   `k` *fractional components*, maximal subtrees of bags joined by
   fractional separators. The gap is at most the sum of the components'
   nonconvexities (Corollary 2.3), which reduces to the classical
   `k max rho` bound when separators are pinned. **Per-bag nonconvexity
   does not control the gap on trees**: with one row, width 1 and smooth
   data the gap is `c n/4`, `n/2` times the largest per-bag nonconvexity
   (Example 2.4).
3. **When the Lagrangian is exact, coupling costs nothing.** Under
   quadratic growth of the Lagrangian (LQG), [D, Theorem 3.4] applies to the
   Lagrangian with the same constants (`c_g` replaced by `c_L/2`): size `O(|T| C^{w+1} log(|T|/eps))`,
   independent of `k` and of the density of the rows, with second-order
   multiplier tolerance (Theorem 3.1). lnts is consistent with this case.
4. **With a gap, partial sums work, at a price** (Theorem 4.5). An exact
   augmented Lagrangian (Lemma 4.1) made local by partial sums, with slopes
   `-mû` on the partial-sum separators, gives certificates of size
   `2|T| (4/theta_x)^{w+1} Gamma_sigma^{k Delta_1} log^2`, where
   `Gamma_sigma = 16 (1+Delta)(d+1) max(1, 64 sqrt(k) nu_A (1 + M_F/c_g)^2)`,
   `d` is the depth of the decomposition and `nu_A` a scale-invariant
   row-conditioning number. First-order partial-sum drift cancels exactly;
   the depth factor comes from second-order drift that accumulates over all
   bags. So the target `poly(n) exp(O(w+k)) log(1/eps)` is met up to the
   factor `Gamma_sigma^{k Delta_1}`: `n^{O(k)}` on paths, and
   `exp(O(k Delta log(k log n)))` on shallow trees with bounded `Delta` and
   bounded conditioning. Whether the depth factor is necessary is open.
5. **The exponent counts bad directions, not rows** (Propositions 2.5, 4.6).
   Under second-order sufficiency the Lagrangian Hessian has `p <= k`
   nonpositive directions; a single negative one forces a duality gap;
   lifting `p` row combinations suffices locally, and no exact quadratic
   augmentation with fewer rows exists.
6. **Shapley–Folkman bounds the gap, not the certificate** (Theorem 5.1).
   With `w = 0`, `k = 1` and gap `c/4 = k rho_max`, every spatial B&B
   without bound tightening whose node bound is at most the Lagrangian dual
   needs `C(n+1, (n+1)/2)` leaves (attained in computations up to
   `n = 13`; FBBT on the row changed no count), while a lifted partial-sum
   certificate in the model of Section 4 is exact with `3n^2 - 3n + 2`
   boxes. The count equals the exact tree size of Jeroslow's binary
   instance and the DP is Vavasis's (1992); the contribution is the
   transfer to continuous spatial branching with Lagrangian bounds. For
   relative accuracy the Lagrangian alone suffices when the cost grows with
   `n`; for absolute accuracy it does not.
7. **Exponential dependence on `k` is necessary**: `exp(Omega(k)) log(1/eps)`
   leaves at a unique nondegenerate minimizer with `w = 0` for single trees
   with alphaBB or with exact envelope (Lagrangian) node bounds, and for
   root-closing lifted certificates (Proposition 5.2, base about 2.45 per
   row with alphaBB). NP-hardness at `k = 1` and, under ETH, no
   `2^{o(k log k)}(n + s0)^{o(k)} polylog(1/eps)` algorithm (Proposition
   5.3). So some dependence beyond `poly(n, s0) 2^{O(k)}` must enter: on
   `k log k`, on `(n + s0)^{Omega(k)}`, or on conditioning. These are
   running-time statements; they do not bound certificate size.
8. **Practice.** waterno2's horizon row is not the bottleneck of the
   wave-2 certificate (its bins gained +0.0005 on waterno2_06); that gap
   sits in the 3-dimensional level separators. The horizon-only Lagrangian
   at its best multiplier was not computed. lnts is three dense rows with
   an exact Lagrangian and a global variable handled by monotonicity.
   **Census**: dualizing at most 8 **linear** rows brings 17.2–17.4% of the
   582 large nonconvex MINLPLib instances to width `<= 12` (16.3–17.0% with
   linear equality rows only; 17.7% if nonlinear rows may be dualized),
   against 14.8% with none. The gap between nonlinear width and
   factor-incidence width comes mostly from wide linear structure: in the
   gap class, 121 instances keep a median width of 71 after 64 removed rows.
   22 small-`w` instances have `1 <= k <= 16` linear rows, 17 of them open.

**Status of the main claims.**

| Item | Content | Status |
|---|---|---|
| Proposition 1.1 | single-tree lower bound unchanged by rows through cost-free defined variables | proved, close to trivial; convex costs change the prefactor by a factor at least `(1 + \|\|A\|\|^2 sup\|\|∇²g\|\|/lambda_min(H))^{-k/2}`, polynomial in `n` for rows with bounded entries (corrected); face-exact transfer not checked |
| Theorem 2.1 | coupling dual = local consistency + `k` moments; `k+1` atoms | proved; classical in substance |
| Theorem 2.2 | at most `k` fractional components at extreme optima | proved; checked on 360 LPs, and on 420 more by the review |
| Corollary 2.3 | gap `<=` sum of component nonconvexities; per-bag when separators are pinned | proved |
| Example 2.4 | one row, gap `c n/4 >= (n/2) max rho` | proved; checked numerically |
| Proposition 2.5 | at most `k` bad directions under SOSC | proved (classical) |
| Proposition 2.6 | LQG characterization; a negative direction forces a gap | proved (attainment hypothesis dropped in (c)) |
| Theorem 3.1 | LQG: size of [D, Thm 3.4], independent of `k` | proved (relies on [D], steps 1–6 up to the final use of (QG)); lnts only consistent with it |
| Lemma 4.1, Corollary 4.2 | global quadratic deficit; exact augmented Lagrangian | proved (classical in substance) |
| Lemmas 4.3, 4.4 | lifted certificates: validity, configuration identity | proved |
| Theorem 4.5 | partial-sum certificate size under (QG) | proved; reuses steps 1–6 of [D, Thm 3.4] up to the final use of (QG); checked by the review; no general certificate computed |
| Proposition 4.6 | only `p` row combinations need lifting | (a), (b) proved; (c) proved under a global hypothesis |
| Theorem 5.1 | `C(n+1,(n+1)/2)` leaves with Lagrangian node bounds (no bound tightening); exact DP; exact lifted certificate with `3n^2 - 3n + 2` boxes | proved; bound attained for `n <= 13`; FBBT changed no count; count and DP known (Jeroslow, Vavasis) |
| Proposition 5.2 | `exp(Omega(k)) log(1/eps)` at a nondegenerate minimizer, `w = 0` | proved for single trees (alphaBB; envelope/Lagrangian node bounds for `m >= 8`) and root-closing lifted certificates |
| Proposition 5.3 | NP-hardness (`k = 1`, Sahni 1974 in substance); ETH bound in `k` | proved by reduction (KPW statement from the abstract); excludes `poly(n, s0) 2^{O(k)}`; does not exclude conditioning-free bounds in general |
| Section 7.3 | census of coupling rows | computed (heuristic); linear rows only: 17.2–17.4% at `k <= 8` (16.3–17.0% linear equalities) vs 14.8% at `k = 0` |
| necessity of the depth factor; adaptive algorithm; general lifted lower bound | — | open |

## 0. Setting

- `X0 = prod_i [L_i, U_i]`, a box in `R^n`.
- `F(x) = sum_{t in T} a_t(x_{V_t})`, where `(T, {V_t})` is a rooted tree
  decomposition of the hypergraph of the **nonlinear** factors, of width
  `w`. Notation as in [D, Section 1.1]: `S_t = V_t ∩ V_{p(t)}`,
  `R_t = V_t \ S_t`, `sub(t)`, `W_t`, `Delta` (largest number of children),
  `k_T` (largest number of bags containing one variable), and `d` (depth:
  the largest number of edges from a node to the root).
- `k` **coupling rows** `A x = b`, `A in R^{k x n}`, with no sparsity
  assumption. Inequality rows are treated in remarks.
- The problem is

  ```
  (P)   OPT = min { F(x) : A x = b, x in X0 }.
  ```

- **Column assignment.** A variable `i` lies in `R_t` for exactly one bag,
  `t = top(i)`, the root of the subtree `T_i`. Write `A_t` for the columns
  of `A` indexed by `R_t`. Then `A x = sum_t A_t x_{R_t}`, and each column
  of `A` is used once.
- **Coupling Lagrangian.** For `mu in R^k`,

  ```
  L(mu) = min_{x in X0} F(x) + mu^T (A x - b),     D = sup_mu L(mu) <= OPT.
  ```

  `L(mu)` is again a tree problem on the same decomposition, with bag
  functions `a_t + mu^T A_t x_{R_t}`. The added terms are linear, so they do
  not change bag Hessians, Lipschitz constants of gradients, or width.
- **Row crossing number.** For an edge `e = (t, p(t))`, `k_e` is the number
  of rows whose support meets both `W_t \ S_t` and its complement. Dense
  rows have `k_e = k` on every edge. A partial-sum reformulation needs `k_e`
  extra state coordinates at edge `e` (Section 6).

Two routes are compared:

- **Route L (Lagrangian).** Dualize the `k` rows; handle the tree problem by
  a decomposition certificate [D]; close any remaining duality gap by
  branching.
- **Route P (partial sums).** Add partial-sum variables for the rows, which
  turns each row into a chain of local equations and raises the width by
  `O(k)`; then use a decomposition certificate on the lifted problem.

## 1. Single-tree lower bounds persist (item 1)

The single-tree lower bounds of [D] and of the face-exact note are proved on
box-constrained path problems. Dense rows cannot remove them. The simplest
way to see this is the common modelling form in which a dense row defines
an aggregate variable (a budget use, a total flow, a horizon total).

**Proposition 1.1 (transfer).** Let `F_n` be the path family of [D,
Section 2.1] on `[-1,1]^n` (`b = 0.8`, `kappa <= 1/6`), with alphaBB
relaxations of the bilinear factors and the unary factors kept exact. Add
`k` aggregate variables `y_j in [l_j, u_j]` with `[l_j, u_j]` containing
`a_j^T [-1,1]^n` (interval hull), `k` rows `a_j^T x - y_j = 0` with arbitrary
dense `a_j`, and no cost on `y`. Then every single-tree certificate at
tolerance `eps` (leaves are boxes in `(x, y)`; each leaf bound minimizes the
termwise relaxation subject to the `k` rows) has at least the bound of
[D, Corollary 2.1], that is
`0.068 sqrt(n) (2e/pi)^{n/2} log(0.2/(n eps))` leaves for `eps <= 0.2/n`.

*Proof.* The minimizer is `x* = 0`, `y* = 0`, unique, `f* = 0`, and the rows
do not restrict `x`. For every `x in X0` the point `(x, A x)` is feasible,
so it lies in some leaf `B = B_x x B_y`. Validity gives
`f* - eps <= LB(B) <= F_n(x) - sum_c alpha_c q_{(B_x)_c}(x)`, because the
relaxation has no gap in `y` and the rows hold at `(x, Ax)`. So
`m(x) + eps >= sum_j alpha_j a_j^{B_x}(x)` with the weights of [D,
Section 2.1], at this particular `x`. Hence
`(m(x) + eps)^{-n/2} <= sum_{B : x in B_x} (sum_j alpha_j a_j^{B_x}(x))^{-n/2}`,
because the right side contains the term of the leaf holding `(x, Ax)` and
all terms are nonnegative. Integrating over `X0` and bounding each leaf's
integral by AM–GM and the arcsine integral, as in the proof of
[C, Theorem 3.1], gives the same inequality as there. The computation of
[D, Corollary 2.1] then applies unchanged. □

The proposition only says that the feasible set projects onto `X0`; it is
close to trivial.

*What the rows do.*

- They can only add constraints to leaf relaxations. With **cost-free**
  aggregate variables (as `y` above) the bound is unchanged. With a convex
  cost `g(y)` the same argument runs on `F_n(x) + g(A x)`: the minimizer can
  move (if `g` has linear terms), and the quadratic upper bound `H` becomes
  `H + A^T ∇²g A` (if `∇²g` is bounded above). This rank-`k` update lowers
  the bound by the factor
  `det(I + H^{-1/2} A^T ∇²g A H^{-1/2})^{-1/2}`, at least
  `(1 + ||A||^2 sup||∇²g||/lambda_min(H))^{-k/2}`. The factor is exact when
  the minimizer stays at 0; if it moves, `r_in` and hence the `J_n` term also
  change, and Corollary 2.1 then needs the new minimizer to be interior with
  zero gradient. For rows with entries of order one the factor is not a
  constant: for one row of ones and `g(y) = y^2/2` it is about
  `1.9/sqrt(n)` (coupling recheck, M2). So the exponential base in
  `n` survives for fixed `k`, but the bound is not unchanged. (Corrected
  after review; the first version said "unchanged" for convex costs.)
- For exact rows on the nonconvex variables themselves, the covering
  argument would run on the `(n-k)`-dimensional slice. It is not carried out
  here; the expected effect is `n -> n - k` in the exponent.
- The face-exact bound (`0.57 (5/3)^n`, McCormick) uses the centre of a
  leaf's intersection with a cube, which need not satisfy the rows. Its
  transfer is **not checked**.
- For the decomposition side the rows are the obstacle: a row touching all
  bags joins every bag to every other, and [D]'s certificates do not apply
  until the rows are dualized (Route L) or lifted (Route P).

Theorem 5.1 below gives a different single-tree lower bound in which the
rows are the whole difficulty: with `w = 0` and one row, B&B with the exact
Lagrangian node bound and no bound tightening needs `C(n+1, (n+1)/2)`
leaves.

## 2. The coupling Lagrangian on a tree

### 2.1 Measure form

**Theorem 2.1 (coupling dual as a local-consistency relaxation).** Let
`X0` be compact and each `a_t` continuous. Then

```
D = min { sum_t ∫ a_t dmu_t :  (mu_t) locally consistent,  sum_t ∫ A_t z_{R_t} dmu_t(z) = b },
```

where `(mu_t)` ranges over families of probability measures `mu_t` on
`X0_{V_t}` whose marginals on `S_t` agree for every edge. The minimum is
attained (`D = +inf` if the set is empty). Equivalently,
`D = min { ∫ F dnu : nu in P(X0), ∫ A x dnu = b }`, and an optimal `nu`
with at most `k + 1` atoms exists. No Slater condition is needed.

*Proof.*

1. Put `phi(nu, mu) = ∫ F dnu + mu^T (∫ A x dnu - b)` on
   `P(X0) x R^k`. `P(X0)` is convex and weak*-compact, `phi` is affine and
   weak*-continuous in `nu` (the integrands are continuous on a compact
   set) and linear in `mu`. Sion's theorem gives
   `sup_mu min_nu phi = min_nu sup_mu phi`.
2. For fixed `mu`, a linear functional on `P(X0)` is minimized at a Dirac
   measure, so `min_nu phi(nu, mu) = L(mu)`. For fixed `nu`,
   `sup_mu phi(nu, mu)` is `∫ F dnu` if `∫ A x dnu = b` and `+inf`
   otherwise. This gives the global-measure form.
3. The bag marginals of a global measure are locally consistent.
   Conversely, locally consistent bag measures glue into a global measure
   with these bag marginals (Vorob'ev 1962; [D, Observation 4.2]). Both
   `∫ F dnu = sum_t ∫ a_t dmu_t` and `∫ A x dnu = sum_t ∫ A_t z_{R_t} dmu_t`
   depend only on bag marginals.
4. *Atoms.* The point `(D, b)` lies in `conv {(F(x), A x) : x in X0}`, a
   compact convex set in `R^{k+1}`, and on its boundary, because
   `(D - delta, b)` is not in it for `delta > 0`. A boundary point of a
   compact convex set lies in a proper face, of dimension at most `k`, and
   by Carathéodory it is a convex combination of at most `k + 1` extreme
   points of that face. Extreme points of the hull are images of points of
   `X0`. □

So dualizing `k` rows of a tree-structured problem gives exactly the tree
problem's exact local-consistency relaxation plus `k` linear moment
conditions. The duality gap is the price of letting at most `k + 1`
tree-feasible points be mixed.

The theorem is classical in substance: the Lagrangian dual of `k` linear
rows equals the convexified (measure) problem, and optimal mixtures need at
most `k + 1` points (Aubin–Ekeland 1976; Udell–Boyd 2016, Appendix A). On a
path it is the known fact that the Lagrangian dual of a
resource-constrained shortest path mixes at most `k + 1` paths
(Handler–Zang 1980; from memory, per the review). The only tree-specific
ingredient is gluing (step 3).

### 2.2 A Shapley–Folkman theorem on trees

For a locally consistent family `mu = (mu_t)`, call bag `t`
**deterministic** if `mu_t` is a Dirac measure and **fractional** otherwise.
The **fractional graph** `Gamma(mu)` has the fractional bags as vertices
and joins `t` and `p(t)` when both are fractional and the `S_t`-marginal is
not a Dirac measure. Its connected components are the **fractional
components**. Each is a subtree of `T`.

**Theorem 2.2 (tree Shapley–Folkman).** Let
`K = {mu locally consistent : sum_t ∫ A_t z_{R_t} dmu_t = b}`. Every
extreme point of `K` has at most `k` fractional components. If `K` is
nonempty, the optimal set of Theorem 2.1 is a nonempty compact convex face
of `K`, so it has
extreme points (Krein–Milman), and each has at most `k` fractional
components. With inequality rows, `k` counts the rows active at the point.

*Proof.* Let `mu` be extreme in `K` with fractional components
`C_1, ..., C_q`.

1. *Glue each component.* `C_j` is a subtree, so its bag measures glue into
   a measure `rho_j` on `X0_{W_j}`, `W_j = union_{t in C_j} V_t`. Every edge
   leaving `C_j` has a Dirac separator marginal: either the other bag is
   deterministic, or the edge is not in `Gamma(mu)`.
2. *Split it.* Pick `t_j in C_j` and a Borel set `E` with
   `0 < mu_{t_j}(E) < 1` (it exists because `mu_{t_j}` is not a Dirac
   measure on a compact metric space). Let `E'` be the set of points of
   `X0_{W_j}` whose `V_{t_j}`-part lies in `E`, `p = rho_j(E')`, and
   `rho_j^E = rho_j(· | E')`. For `|s|` small, `rho_j + s (rho_j^E - rho_j)`
   is a probability measure (for `s < 0` this needs `|s| <= p/(1-p)`), with
   support inside `supp rho_j`.
3. *Consistency is kept.* Replace the bag measures of `C_j` by the bag
   marginals of this measure and keep all other bags. Edges inside `C_j`
   are consistent because the marginals come from one measure. Edges
   leaving `C_j` are consistent because the support did not grow, so the
   separator marginal is still the same Dirac measure.
4. *Independent directions.* Let `Dir_j` be the resulting change of the bag
   marginals (a signed measure on the bags of `C_j`). It is nonzero,
   because the marginal of `t_j` changes: `mu_{t_j}(·|E)` gives `E` mass 1,
   not `mu_{t_j}(E)`. The `Dir_j` live on disjoint sets of bags, so they are
   linearly independent, and each can be applied with its own small
   coefficient.
5. *Count.* The `k` linear maps `nu -> sum_t ∫ A_t z_{R_t} dnu_t` send the
   `q` directions into `R^k`. If `q > k`, some nonzero combination
   `sum_j c_j Dir_j` is in their kernel. Then `mu ± s sum_j c_j Dir_j` lies
   in `K` for small `s > 0` (step 3 and convexity), so `mu` is the midpoint
   of two distinct points of `K`, which contradicts extremality.
6. *Inequalities.* Rows inactive at `mu` stay satisfied under small
   perturbations; only active rows enter step 5. □

For a forest of single bags (no separators) this is the Shapley–Folkman
statement in the form of Udell–Boyd: at most `k` blocks are not extreme at
an extreme optimal point. On a tree, **fractional bags can form long
chains**: a component is a set of bags whose separators are themselves
fractional. Section 2.3 shows that this is where the tree changes the
answer.

A finite-domain check (`tree_sf_lp.py`, Section 9.3): on 360 random path
problems (widths 1, grids of 3–4 values, `k = 1, 2, 3`), the LP over locally
consistent bag marginals with the `k` moment rows, solved by dual simplex,
always returned at most `k` fractional components, and exactly `k` in the
worst case of every setting. With a stiff pairwise penalty the largest
component covered on average 4.8–6.0 of the 7 bags.

### 2.3 The gap bound, and why per-bag nonconvexity does not control it

For a function `g` on a box `Y`, let `rho(g) = sup_Y (g - vex_Y g)`
(nonconvexity), and for a set `C` of bags let `a_C = sum_{t in C} a_t` on
`X0_{W_C}`.

**Corollary 2.3 (gap bound).** Let `mu` be an extreme optimal point of
Theorem 2.1 with fractional components `C_1, ..., C_q`, `q <= k`, and let
`x̄` be its mean (`x̄_i = ∫ z_i dmu_t` for any `t` containing `i`; this is
well defined by consistency). Then `x̄` is feasible for (P) and

```
OPT - D  <=  F(x̄) - D  =  sum_{j <= q} [ a_{C_j}(x̄_{W_j}) - ∫ a_{C_j} drho_j ]  <=  sum_{j <= q} rho(a_{C_j}).
```

If every separator marginal of `mu` is a Dirac measure (for example, when
the separator variables have been fixed by branching, or are integers fixed
in the current node), the components are single bags and

```
OPT - D  <=  sum of the k largest rho(a_t).
```

*Proof.* `x̄ in X0` by convexity, and `A x̄ = sum_t A_t x̄_{R_t} = sum_t ∫ A_t z_{R_t} dmu_t = b`.
A deterministic bag has `a_t(x̄_{V_t}) = ∫ a_t dmu_t`. For a component,
`∫ a_{C_j} drho_j >= vex a_{C_j}(x̄_{W_j})` by Jensen, since `x̄_{W_j}` is
the mean of `rho_j`. Bags outside the components are deterministic, and
bags are in at most one component, so the terms add up. □

This recovers the classical bounds (Aubin–Ekeland `min(k+1, n) max rho`;
Udell–Boyd, sum of the `min(m~, n)` largest) when the tree has no
separators. With separators it is honest but weak: `rho(a_C)` is the
nonconvexity of a **whole component**, which can be as large as the
problem.

**Example 2.4 (penalty chain: one row, gap `n/2` times the largest
per-bag nonconvexity).** Let `n >= 2`, `x in [0,1]^n`, bags `{x_i, x_{i+1}}`,

```
F(x) = sum_i c x_i (1 - x_i) + M sum_i (x_i - x_{i+1})^2,     one row  sum_i x_i = n/2.
```

Assign `c x_i (1 - x_i)` to one bag containing `x_i` (one bag receives two
such terms). A bag function is a sum of at most two concave quadratics in
different variables plus a convex function, and the envelope of a sum
dominates the sum of envelopes, so `rho(a_t) <= c/2` for every bag (and
`<= c/4` for all but one). Then:

- `D = 0`. `F >= 0` on the box, and mixing `x = 0` and `x = 1` with weights
  `1/2` gives a locally consistent family with value 0 that satisfies the
  row.
- `OPT = c n/4` when `M >= c n (n-1)`. Proof: for feasible `x` let
  `Delta = max x - min x`. The mean is `1/2`, so `|x_i - 1/2| <= Delta` and
  `sum_i x_i(1 - x_i) = n/4 - sum_i (x_i - 1/2)^2 >= n/4 - n Delta^2`. Along
  the path, `sum_i (x_i - x_{i+1})^2 >= Delta^2/(n-1)` (Cauchy–Schwarz on
  the path between the extreme entries). So
  `F >= c n/4 - c n Delta^2 + M Delta^2/(n-1) >= c n/4`, with equality at
  `x = (1/2, ..., 1/2)`.

So `OPT - D = c n/4 >= (n/2) max_t rho(a_t)` with `k = 1`. The extreme optimal
point is the half–half mixture of the two constant configurations: a
single fractional component covering the whole path, with
`rho(a_C) = c n/4`. With a soft penalty the gap saturates at a wall cost of
order `sqrt(M c)`: multistart SLSQP gives `OPT = 0.75` for `M = 1` and
`2.4728` for `M = 10` at `n = 10, 16`, and exactly `c n/4` for
`M = c n (n-1)` at `n = 6, 10, 16`; a grid DP of `max_mu L(mu)` gives `0`
throughout (`penalty_chain.py`, Section 9.2). The condition
`M >= c n(n-1)` is sufficient but conservative: the review's exact-row grid
DP finds the threshold for `OPT = c n/4` within 7% of the second-order
value `c/(2 - 2 cos(pi/n)) ≈ c n^2/pi^2` for `n = 6, 10, 16`. (Below that
value the uniform point is not even a local minimizer: on the slice
`sum d_i = 0` the Hessian is `-2c I + 2M L`, with `L` the path Laplacian,
whose smallest eigenvalue on the slice is `2 - 2 cos(pi/n)`; this agrees
with the SLSQP value 2.4728 < 2.5 at `n = 10`, `M = 10 < 10.2`.)

*Consequences.*

- No bound of the form `gap <= f(k) max_t rho(a_t)` holds on trees, even
  for `k = 1`, width 1, and smooth data. The tree transmits nonconvexity
  through its separators, and one row lets the relaxation mix two
  **global** configurations.
- This is the counterpart of the scouting result [S, Section 3A]: there,
  many rows on a path-shaped block–row incidence give gaps linear in the
  number of rows; here, one row on a path of tightly coupled bags gives a
  gap linear in the number of bags.
- The gap is controlled once separators are pinned: with Dirac separator
  marginals, Corollary 2.3 gives the per-bag Shapley–Folkman bound. In a
  decomposition certificate, separator cells play this role
  approximately; Section 4 makes this quantitative in the partial-sum
  model.

### 2.4 Local Shapley–Folkman: bad directions of the Lagrangian

**Proposition 2.5 (inertia).** Let `x* in int X0` be a local minimizer of
(P) with `A` of full row rank and `∇²F(x*) ≻ 0` on `ker A` (second-order
sufficient condition). Then `∇²F(x*)` has at most `k` eigenvalues `<= 0`.
For separable `F` this means that at most `k` blocks have nonpositive
curvature at `x*`.

*Proof.* If `k + 1` eigenvalues were `<= 0`, their eigenspace `E` would
meet `ker A` (`dim E + dim ker A = n + 1`) in some `d != 0` with
`d^T ∇²F(x*) d <= 0`, contradicting the hypothesis. □

Call `p(x*)`, the number of eigenvalues `<= 0`, the number of **bad
directions**. It counts the directions in which the Lagrangian
`F + mu*^T (A x - b)` fails to be locally convex. It is at most `k`, and it
can be much smaller.

**Proposition 2.6 (when the coupling Lagrangian is exact).** Say that
**(LQG)** holds with constant `c_L > 0` if

```
F(x) + mu*^T (A x - b) - OPT >= c_L |x - x*|^2   for all x in X0.
```

(a) (LQG) implies `D = OPT`, that `x*` is the unique minimizer of (P), and
that `x*` is the unique minimizer of the Lagrangian at `mu*`.
(b) Conversely, if `D = OPT` is attained at `mu*`, `x* in int X0` is the
unique minimizer of `F + mu*^T(A x - b)` on `X0`, and `∇²F(x*) ≻ 0`, then
(LQG) holds for some `c_L > 0`. Conversely (LQG) forces
`∇²F(x*) ⪰ 2 c_L I` when `F` is `C^2`, so it requires `p(x*) = 0`.

(c) If a global minimizer `x*` of (P) lies in `int X0`, `A` has full row
rank, and `∇²F(x*)` has a negative eigenvalue, then `D < OPT`.

*Proof.* (a) `L(mu*) = min_{X0}(F + mu*^T(Ax - b)) = OPT` by (LQG) with
equality only at `x*`; and `D <= OPT`. (b) `∇(F + mu*^T A x)(x*) = 0`, so by
Taylor's theorem the function exceeds `OPT + (lambda_min/4)|x - x*|^2` on a
ball `|x - x*| <= r`; outside the ball it exceeds `OPT + delta` for some
`delta > 0` by uniqueness and compactness; take
`c_L = min(lambda_min/4, delta/diam(X0)^2)`. (c) The dual optimum is
attained: `A` maps a ball around the interior point `x*` onto a
neighbourhood of `b = A x*`, so `L(mu) <= max_{X0} F - r |mu|` for some
`r > 0`, and the concave function `L` has bounded superlevel sets. If
`D = OPT = L(mu)`, then
`x*` minimizes `F + mu^T(A x - b)` over `X0` (its value there is
`F(x*) = OPT`). As `x*` is interior, `∇F(x*) + A^T mu = 0`, so `mu` is the
unique KKT multiplier, and the second-order necessary condition
`∇²F(x*) ⪰ 0` fails. □

So under the second-order sufficient condition the Lagrangian is exact
(with a nondegenerate minimizer) only if there are no bad directions, and a
single negative direction already forces a duality gap.

### 2.5 Absolute versus relative accuracy

- *Separable problems, or pinned separators.* Corollary 2.3 gives
  `OPT - D <= k max_t rho(a_t)`, independent of `n`. If the optimal value
  grows with the number of bags (each bag contributes a cost of order one),
  the **relative** gap is `O(k/n)`: the Lagrangian alone certifies relative
  accuracy `eps_rel` as soon as `n >~ k rho_max/(eps_rel · average bag cost)`.
  This is the classical message of Aubin–Ekeland and Bertsekas et al.
- The **absolute** gap `k rho_max` does not shrink with `n`. Closing it by
  branching can cost `2^Omega(n)` nodes even when `k = 1` and the bags are
  single variables (Theorem 5.1): Shapley–Folkman bounds the gap, not the
  certificate.
- *Trees.* Even the relative statement fails: in Example 2.4 the relative
  gap is 100% for every `n`.
- Dey–Xu (2026) prove `OPT(b + E 1) - E <= D(b) <= OPT(b)`, with `E -> 0`
  for smooth blocks under their conditions. This is a statement with a
  perturbed right-hand side. The parity structure of Theorem 5.1 shows why
  a perturbed right-hand side hides exactly the global sensitivity that an
  absolute certificate must pay for (compare the parity chain of [S,
  Proposition L4]). Whether their hypotheses hold on our examples was not
  checked.

## 3. When the coupling Lagrangian is exact, coupling costs nothing

Write `A_r` for the relaxation constant called `A` in [D] (the largest
number of relaxed-factor coordinates in a bag), to avoid a clash with the
row matrix.

**Theorem 3.1.** Assume (LQG) with `(x*, mu*, c_L)`, (L^{1,1}) with `M_a`
and (U^q_{alpha'}) for the bag functions `a_t` [D, Section 1.2]. Let
`mû in R^k` with `|mû - mu*|_2 <= delta`. Build the certificate of
[D, Theorem 3.4] for the bag functions `ã_t = a_t + mû^T A_t z_{R_t}` (the
constant `-mû^T b` added at the root), with `c_g` replaced by `c_L/2` in
(T2), (T3), `Q` and `h_0`, and slopes
`lambda_t = ∇_{S_t} (sum_{s in sub(t)} a_s)(x̂)` (the linear terms do not
contribute to them). Then its root bound satisfies
`OPT >= L(mû) >= l_r` (validity), and `l_r >= OPT - eps` if

```
delta ||A||_2 <= sqrt(eps c_L/32).
```

Its size is `2|T| (4/theta)^{w+1} (log2(s0/h) + 2)`, with `theta` as in
[D, Theorem 3.4] for `c_L/2`. The bound does not depend on `k`, on the
density of `A`, or on its norm (except through the multiplier tolerance).

*Proof.*

1. *Slopes.* For `s in sub(t)`, `R_s ∩ S_t = ∅`: a variable of `S_t` lies
   in the parent bag, so its top bag is outside `sub(t)`. Hence the linear
   terms `mû^T A_s z_{R_s}` do not depend on separator coordinates of
   `S_t`, and the slopes of [D, Lemma 3.2] for `ã` equal those for `a`.
   Linear terms also cancel in the Taylor remainders of [D, (3.1)] and do
   not change `M_a` or the relaxation errors.
2. *Identity.* For a configuration with consistent point `x`, [D, (3.1)]
   gives `Phi = sum_t ã_t(x_{V_t}) - mû^T b + (brackets) = F(x) + mû^T (A x - b) + (brackets)`,
   using `sum_t A_t x_{R_t} = A x`.
3. *Error terms.* Steps 1–6 of the proof of [D, Theorem 3.4], up to the
   final use of (QG) in the last sentence of step 6, never use (QG) or the
   optimality of `x*` (`x*` enters only as the shell centre, as the base
   point of the slopes, and in `|∇a_t(x) - ∇a_t(x*)| <= M_a r_t`). Run with
   the parameter `c̃ = c_L/2`, they give
   `Phi - E_rel >= F(x) + mû^T(Ax - b) - E` with
   `E <= (7/8) c̃ X^2 + (3/4) eps`, `X = |x - x*|_2`; this bound is assembled
   in step 6 of [D] from (T2), (T3) and `h <= h_0`.
4. *Margin.* `F(x) + mû^T(Ax - b) = [F(x) + mu*^T(Ax - b)] + (mû - mu*)^T A (x - x*) >= OPT + c_L X^2 - delta ||A||_2 X`
   by (LQG) and `A x* = b`. Young's inequality gives
   `delta ||A|| X <= (c_L/16) X^2 + 4 delta^2 ||A||^2/c_L <= (c_L/16) X^2 + eps/8`
   under the stated condition.
5. *Collect.* `Phi - E_rel >= OPT + (1 - 7/16 - 1/16) c_L X^2 - (7/8) eps >= OPT - eps`
   for every configuration, so `l_r >= OPT - eps` by [D, Lemma 1.5].
6. *Size.* As in [D, Theorem 3.4]. □

*Remarks.*

- Multiplier errors are second order: `delta = O(sqrt(eps))` suffices, as
  for the copy multipliers in [D, Remark 3.5]. A local solve that returns
  KKT multipliers gives them.
- lnts ([O, Section 3]) is consistent with this regime, but Theorem 3.1
  was not needed there and (LQG) was not verified: the lnts certificate is
  a closed-form Lagrangian, not a decomposition certificate, and its global
  variable `h` lies outside the theorem. After eliminating the linear state
  recursion for fixed `h`, three dense rows couple single-control blocks
  (`w = 0`). Only the upper boundary of each block's image
  `{(cos th, sin th)}` matters, and it is the graph of the concave function
  `sqrt(1 - s^2)`, so the convexified problem is exact and the Lagrangian
  certificate had no gap. The global variable `h`, which lies in every
  separator, was handled by monotonicity instead of branching
  (Section 7.2).

## 4. Certificates with a duality gap: partial sums

### 4.1 A quadratic deficit lemma and the exact augmented Lagrangian

Hypotheses for this section:

- **(H1)** `x* in int X0` is the unique minimizer of (P), with constrained
  quadratic growth `F(x) - OPT >= c_g |x - x*|^2` for all `x in X0` with
  `A x = b`.
- **(H2)** `A` has full row rank, and `kappa` is a Hoffman constant of the
  feasible polytope: `dist(x, P_b) <= kappa |A x - b|_2` for all `x in X0`,
  where `P_b = {x in X0 : A x = b}`.
- **(H3)** `∇F` is `M_F`-Lipschitz on `X0`; the bag functions satisfy
  (L^{1,1}) with `M_a` and the relaxations satisfy (U^q_{alpha'}).

Let `mu*` be the KKT multiplier: `∇F(x*) + A^T mu* = 0`.

**Lemma 4.1 (quadratic deficit).** For all `x in X0`,

```
F(x) + mu*^T (A x - b) - OPT  >=  (c_g/4) |x - x*|^2 - K |A x - b|^2,
K = kappa^2 ( M_F^2/(2 c_g) + M_F/2 + c_g/2 ).
```

*Proof.* Let `G = F + mu*^T(A · - b)` and let `x'` be a nearest point of
`P_b` to `x`, so `|x - x'| <= kappa |r|`, `r = A x - b`. Then
`G(x') = F(x') >= OPT + c_g |x' - x*|^2`, `∇G(x*) = 0`, and `∇G` is
`M_F`-Lipschitz. Hence
`G(x) >= G(x') - |∇G(x')| |x - x'| - (M_F/2)|x - x'|^2` with
`|∇G(x')| <= M_F |x' - x*|`, and Young's inequality gives
`G(x) - OPT >= (c_g/2)|x' - x*|^2 - (M_F^2/(2c_g) + M_F/2)|x - x'|^2`.
Finally `(c_g/2)|x' - x*|^2 >= (c_g/4)|x - x*|^2 - (c_g/2)|x - x'|^2`. □

**Corollary 4.2 (exact augmented Lagrangian).** For `rho >= K`,
`G_rho(x) = F(x) + mu*^T(A x - b) + rho |A x - b|^2` satisfies
`G_rho(x) - OPT >= (c_g/4)|x - x*|^2` on all of `X0`. So dropping the rows
and adding the augmentation is an exact relaxation with quadratic growth on
the box.

Both facts are classical in substance (exact augmented Lagrangians under
second-order sufficiency, Hestenes, Powell, Rockafellar 1974); the global
form with a Hoffman constant is written out here because the constants
enter the certificate size. The term `rho |A x - b|^2` couples all
variables. Partial sums make it local.

### 4.2 The lifted problem and lifted certificates

For `t in T` let `sigma_t(x) = sum_{u in sub(t)} A_u x_{R_u} in R^k` (the
subtree's contribution to the rows) and let `Sigma_t` be the interval hull
of `sigma_t(X0)`.

- **Lifted bag.** The variables of bag `t` are
  `z = (x_{V_t}, (zeta_u)_{u in ch(t)})` in
  `Z_t = X0_{V_t} x prod_{u in ch(t)} Sigma_u`. Its own partial sum is the
  affine function `zeta_t(z) = A_t x_{R_t} + sum_{u in ch(t)} zeta_u`.
- **Lifted separator** of `t != r`: `Y_t = X0_{S_t} x Sigma_t`, with value
  `(z_{S_t}, zeta_t(z))` on the child side and the coordinates
  `(z_{S_t}, zeta_t)` on the parent side.
- **Value functions.**
  `Phi_t(s, sigma) = min { sum_{u in sub(t)} a_u : x in X0_{W_t}, x_{S_t} = s, sigma_t(x) = sigma }`.
- **Root term.** `g(sigma) = mû^T (sigma - b) + rho |sigma - b|^2`, convex
  and kept exact. The root value is
  `min_{x in X0} F(x) + mû^T(A x - b) + rho |A x - b|^2 <= OPT`, for every
  `mû` and `rho >= 0`. The root may instead impose `zeta_r(z) = b` as a
  linear constraint; validity (Lemma 4.3) is unchanged, and the
  configurations of Lemma 4.4 then have `A x - b + sum_t delta_t = 0`, a
  special case of the analysis.

A **lifted certificate** is a decomposition certificate [D, Definition 1.2]
for this lifted tree problem: cells on `Y_t` with affine minorants
`l(s, sigma) = lambda^T s + eta^T sigma + beta`, leaves covering `Z_t`,
child bounds, and conditions (CM), (LC), where the bag's own separator
value is `(z_{S_t}, zeta_t(z))`. (LC) for one pair (leaf, cell) is still one
convex program, because `zeta_t` is affine.

**Lemma 4.3 (validity and unfolding).** A lifted certificate satisfies
`l_r <= OPT`. With one slope pair `(lambda_t, eta_t)` per separator and
maximal `beta` as in [D, Lemma 1.5],

```
l_r = min over configurations of  sum_t sum_{c at t} f_{c,B_t}(z^t)
      + sum_{t != r} [ lambda_t^T (z^{p(t)}_{S_t} - z^t_{S_t}) + eta_t^T (zeta^{p(t)}_t - zeta_t(z^t)) ]  + g(zeta_r(z^r)),
```

where a configuration picks a leaf `B_t` and a point `z^t in B_t` for every
bag and a cell `D_t` for every `t != r` containing `(z^t_{S_t}, zeta_t(z^t))`
and meeting the projection of `B_{p(t)}`, and `zeta^{p(t)}_t` is the
coordinate `zeta_t` of `z^{p(t)}`.

*Proof.* The proofs of [D, Lemmas 1.3 and 1.5] only evaluate functions at
points of the bag domains and use `f_{c,B} <= f_c` and (CM); the affine map
`zeta_t` is exact. At a minimizer of the recursion the partial sums are the
true subtree sums, which lie in `Sigma_t`. □

**Lemma 4.4 (configuration identity).** Take `eta_t = -mû` for every
`t != r`, exact factors, and a configuration with consistent point `x`
(`x_i = z^{top(i)}_i`) and **partial-sum drifts**
`delta_t = zeta^{p(t)}_t - zeta_t(z^t) in R^k`. Then
`zeta_r(z^r) = A x + sum_{t != r} delta_t`, and

```
Phi = F(x) + mû^T (A x - b) + rho |A x - b + sum_t delta_t|^2
      + sum_t [ a_t(z^t) - a_t(x_{V_t}) - ∇a_t(x*)^T (z^t - x_{V_t}) ]
      + sum_{t != r} (lambda_t - lambda_t(x*))^T (z^{p(t)}_{S_t} - z^t_{S_t}),
```

with `lambda_t(x*)` the slopes of [D, Lemma 3.2].

*Proof.* For `i in R_t`, `top(i) = t`, so `z^t_i = x_i` and
`A_t z^t_{R_t} = A_t x_{R_t}`. By induction from the leaves of `T`,
`zeta_t(z^t) = A_t x_{R_t} + sum_{u in ch(t)} (zeta_u(z^u) + delta_u) = sigma_t(x) + sum_{u in sub(t), u != t} delta_u`,
which at the root is the first claim. The `eta` terms add up to
`-mû^T sum_t delta_t`, and `g(zeta_r) = mû^T(A x + sum delta - b) + rho |...|^2`;
the drift terms cancel in the linear part. The `lambda` terms and
`sum_t a_t(z^t)` are handled by [D, Lemma 3.2] exactly as in [D, (3.1)]. □

The linear part of the drift cancels for **any** `mû`: first-order errors
of the partial-sum copies are removed by the slopes `-mû`, just as the
slopes `lambda_t` remove those of the separator copies. What remains is the
second-order term `rho (|r + sum delta|^2 - |r|^2) >= -2 rho |r| |sum delta|`,
`r = A(x - x*)`. It is harmful when the drifts add up coherently: a
configuration with `sum delta ≈ -r` "fakes" feasibility and removes the
augmentation, which brings back the Lagrangian dip of Lemma 4.1.

### 4.3 Size under quadratic growth

Leaves and cells are products of two shell partitions [D, Lemma 3.1]: one
in the `x`-coordinates (centre `x̂`, ratio `theta_x`, smallest width `h_x`)
and one in the partial-sum coordinates (centre `sigmâ`, ratio
`theta_sigma`, smallest width `h_sigma`). Put `Delta_1 = max(Delta, 1)` and

```
alpha_A = max_{|v|_2 = 1} sum_t |A_t v_{R_t}|_inf   (<= sqrt(|T|) max_t ||A_t||_{2->inf}).
```

**Theorem 4.5 (partial-sum certificates).** Assume (H1)–(H3) and let
`rho >= K`. Suppose:

- the `x`-part satisfies the hypotheses (T1)–(T3) and `h_x <= h_0` of
  [D, Theorem 3.4] with `c_g` replaced by `c_g/8`, with centre
  `|x̂ - x*|_inf <= h_x` and slopes `lambda_t` of error `nu`;
- `sigmâ_t in Sigma_t` (the shell centre must lie in the box, [D,
  Lemma 3.1]; possible since `sigma_t(x*) in Sigma_t`),
  `|sigmâ_t - sigma_t(x*)|_inf <= h_sigma`, and
  `h_sigma <= sqrt(eps c_g) / (128 rho ||A||_2 sqrt(k) |T|)`;
- **(T4)** `theta_sigma` is a power of `1/2`, `theta_sigma ((1 + Delta) d + Delta) <= 1/2`, and
  `128 rho ||A||_2 sqrt(k) (1 + Delta)(d + 1) alpha_A theta_sigma <= c_g`;
- `eta_t = -mû` with `|mû - mu*|_2 <= sqrt(eps c_g)/(16 ||A||_2)`.

Then the lifted certificate proves `l_r >= OPT - eps`, and its size is at
most

```
2 |T| (4/theta_x)^{w+1} (4/theta_sigma)^{k Delta_1} (J_x + 1)(J_sigma + 1),
J_x = ceil(log2(s0/h_x)),  J_sigma = ceil(log2(s_sigma/h_sigma)),
```

with `s_sigma` the largest side of the boxes `Sigma_t`.

*Proof.* Fix a configuration, its consistent point `x`, `X = |x - x*|_2`,
`r = A(x - x*)`.

1. *Split the value.* By Lemma 4.4 and (U^q),
   `Phi - E_rel >= G_rho(x) + (mû - mu*)^T r - E_x - 2 rho |r|_2 |sum_t delta_t|_2`,
   where `E_x` collects the Taylor brackets, the slope error and the
   relaxation error. The `x`-parts of leaves and cells are shell members in
   `x` only, so their widths depend only on `x`-distances, and steps 1–6 of
   the proof of [D, Theorem 3.4] up to the final use of (QG) (see
   Theorem 3.1, step 3), run with parameter `c̃ = c_g/8`, give
   `E_x <= (7/64) c_g X^2 + (3/4) eps`.
2. *Margin.* `G_rho(x) >= OPT + (c_g/4) X^2` (Corollary 4.2).
3. *Multiplier error.* `|(mû - mu*)^T r| <= (c_g/64) X^2 + 16 |mû - mu*|^2 ||A||^2/c_g <= (c_g/64) X^2 + eps/16`.
4. *Drift recursion.* Write `e_t = |delta_t|_inf`,
   `s_t = |zeta_t(z^t) - sigma_t(x*)|_inf`, `E = sum_{t != r} e_t`. A
   partial-sum shell member containing a point `zeta` has width at most
   `2 h_sigma + theta_sigma |zeta - sigma*|_inf` ([D, Lemma 3.1] and the
   centre error). The cell `D_t` contains `zeta_t(z^t)`; the parent's leaf
   is one shell member over all its children's partial sums and contains
   `(zeta^{p}_u)_{u in ch(p)}`, with `|zeta^p_u - sigma*_u| <= s_u + e_u`; the
   two boxes intersect. Hence
   `e_t <= 4 h_sigma + theta_sigma ( s_t + sum_{u in ch(p(t))} (s_u + e_u) )`.
   By Lemma 4.4, `s_t <= y_t + sum_{u in sub(t), u != t} e_u` with
   `y_t = |sigma_t(x) - sigma_t(x*)|_inf`. A node has at most `d` proper
   ancestors and at most `Delta` siblings (itself included), so summing,
   `E <= 4 h_sigma |T| + theta_sigma (1 + Delta)(Y + d E) + theta_sigma Delta E`,
   `Y = sum_t y_t`. By (T4), `E <= 8 h_sigma |T| + 2 theta_sigma (1 + Delta) Y`.
5. *Accumulation.* `y_t <= sum_{u in sub(t)} |A_u (x - x*)_{R_u}|_inf`, and
   each `u` lies in at most `d + 1` subtrees, so
   `Y <= (d + 1) alpha_A X`. Hence
   `|sum_t delta_t|_2 <= sqrt(k) E <= sqrt(k) (8 h_sigma |T| + 2 theta_sigma (1+Delta)(d+1) alpha_A X)`.
6. *Drift term.* With `|r| <= ||A||_2 X`,
   `2 rho |r| |sum delta| <= 4 rho ||A|| sqrt(k) (1+Delta)(d+1) alpha_A theta_sigma X^2 + 16 rho ||A|| sqrt(k) |T| h_sigma X`.
   The first term is at most `(c_g/32) X^2` by (T4). By Young's inequality
   the second is at most `(c_g/32) X^2 + 8 (16 rho ||A|| sqrt(k) |T| h_sigma)^2/c_g <= (c_g/32) X^2 + eps/8`
   by the choice of `h_sigma`.
7. *Collect.* The coefficient of `X^2` in the errors is at most
   `(7/64 + 1/64 + 4/64) c_g < c_g/4`, and the additive errors sum to
   `(3/4 + 1/16 + 1/8) eps < eps`. So `Phi - E_rel >= OPT - eps` for every
   configuration, and `l_r >= OPT - eps` by Lemma 4.3.
8. *Size.* A bag has at most `(J_x + 1)(4/theta_x)^{|V_t|}` `x`-shell
   members and `(J_sigma + 1)(4/theta_sigma)^{k |ch(t)|}` partial-sum shell
   members; a separator has `(J_x + 1)(4/theta_x)^{|S_t|}(J_sigma + 1)(4/theta_sigma)^k`
   cells. Sum over `t`. □

**Reading the constants.** With `rho = K` from Lemma 4.1,
`rho ||A||_2 alpha_A / c_g <= nu_A (1 + M_F/c_g)^2` with
`nu_A = kappa^2 ||A||_2 alpha_A`. Since `(1+Delta) d + Delta <= (1+Delta)(d+1)`,
(T4) holds for the largest power of `1/2` below
`[2 (1+Delta)(d+1) max(1, 64 sqrt(k) nu_A (1 + M_F/c_g)^2)]^{-1}`, so

```
4/theta_sigma <= Gamma_sigma := 16 (1 + Delta)(d + 1) max(1, 64 sqrt(k) nu_A (1 + M_F/c_g)^2),
size <= 2 |T| (4/theta_x)^{w+1} Gamma_sigma^{k Delta_1} (J_x + 1)(J_sigma + 1).
```

`nu_A` is invariant under scaling of `A`. For "spread" rows (entries of
similar size, `||A||_2 ≈ sigma_min(A) ≈ 1/kappa`, so that
`||A_t||_{2->inf} ≈ ||A||_2 sqrt(|R_t|/n)`), `nu_A = O(sqrt(|T|(w+1)/n)) = O(sqrt(w+1))`.
The Hoffman constant of a box intersected with an affine space can be much
larger than `1/sigma_min(A)` when the affine space passes near a corner; this
was not analysed. Then:

- **Paths** (`Delta = 1`, `k_T = 2`, `d = |T| - 1`):
  `size <= 2 |T| C_x^{w+1} (32 |T| max(1, 64 sqrt(k) nu_A (1 + M_F/c_g)^2))^{k} (J_x + 1)(J_sigma + 1)`,
  with `C_x = 4/theta_x` the base of [D, Theorem 3.4]. For fixed `k` and
  bounded conditioning this is polynomial in `n` of degree about `k + 1`,
  times `log^2(|T|/eps)`.
- **Trees of depth `d = O(log |T|)`** with bounded `Delta` and `k_T`:
  `size <= 2 |T| C_x^{w+1} (16 (1+Delta)(d+1) max(1, 64 sqrt(k) nu_A (1 + M_F/c_g)^2))^{k Delta_1} (J_x + 1)(J_sigma + 1)`.
  For bounded `Delta` and bounded `nu_A (1 + M_F/c_g)^2` this is
  `exp(O(w + k Delta log(k log n)))` times `|T| log^2(|T|/eps)`; in general
  the factor `((1+Delta) nu_A (1 + M_F/c_g)^2)^{k Delta}` must be kept.
- Rebalancing a decomposition to depth `O(log n)` (Bodlaender–Hagerup
  1998: width `3w + 2`) is **not free** here: it raises `k_T` to
  `O(log n)`, and the base of [D, Theorem 3.4] grows with `k_T` through
  `D_k = sum_{j < k_T} Delta^j`. So the logarithmic-depth bound applies only
  to decompositions that are shallow to begin with (for example
  tree-shaped networks of bounded degree).

So the target form `poly(n) exp(O(w + k)) log(1/eps)` is reached with the
extra factor `Gamma_sigma^{k Delta_1}` (which contains
`((1+Delta)(d+1) sqrt(k) nu_A cond^2)^{k Delta_1}`, `cond = 1 + M_F/c_g`)
and a second logarithm. Two of these factors have identifiable sources:

- the depth `d` comes from **drift accumulation** (step 4): the
  partial-sum copies of all bags drift within their cells, and the drifts
  add up at the root. Uniform-ratio shells then need `theta_sigma ~ 1/d`.
  For a single row of ones on a path and `x - x*` parallel to the row, the
  cell widths allow drifts summing to about `theta_sigma n |r|/2`, which
  suggests that the requirement is real for shell certificates (a heuristic
  count; no minimizing configuration was computed). Whether **every**
  certificate in the model
  needs `d^{Omega(k)}` cells is open; it would be the analogue of the
  tolerance-splitting factor `n^{Theta(w)}` of [D, Proposition 2.4];
- `cond^2 = (1 + M_F/c_g)^2` and `nu_A` come from Lemma 4.1: the
  augmentation weight must pay for the Lagrangian dip, whose size is set by
  the conditioning of the constrained problem. Proposition 5.3 shows that
  some conditioning dependence is unavoidable.

The second logarithm comes from using two independent shell partitions. A
single shell partition in rescaled coordinates would remove it but lets
`x`-distances widen partial-sum cells; this was not worked out.

### 4.4 Only the bad directions need to be lifted

**Proposition 4.6.** Assume the second-order sufficient condition at
`x* in int X0` (`H = ∇²F(x*) ≻ 0` on `ker A`, `A` full row rank), and let
`p` be the number of eigenvalues of `H` that are `<= 0` (`p <= k` by
Proposition 2.5).

(a) There is `R in R^{p x k}` of rank `p` with `H ≻ 0` on `ker(R A)`, and
then `H + rho (RA)^T (RA) ≻ 0` for all large `rho` (Finsler's lemma).
(b) No matrix `M` with fewer than `p` rows has `H ≻ 0` on `ker M`.
(c) If the partially augmented Lagrangian
`G_{R,rho}(x) = F(x) + mu*^T(A x - b) + rho |R(A x - b)|^2` satisfies
`G_{R,rho} - OPT >= c_P |x - x*|^2` on `X0` ("partial LQG"), then
Theorem 4.5 holds with the `p` rows `R A` lifted (partial sums of `R A x`,
slopes `eta_t = 0`, root term `rho |sigma - R b|^2`), the linear terms
`mû^T A_t x_{R_t}` put directly into the bags,
`c_g/4` replaced by `c_P`, `(A, k)` replaced by `(R A, p)` in (T4) and
`h_sigma`, and the exponent `k Delta_1` replaced by `p Delta_1`. For `p = 0`
this is Theorem 3.1.

*Proof.* (a) `U_0 = ker A` is `H`-positive definite, so
`R^n = U_0 ⊕ U_0^{[⊥]}` with `U_0^{[⊥]} = {v : v^T H u = 0 for all u in U_0}`,
and `H` is block diagonal in this splitting. By Sylvester's law of
inertia, the quadratic form of `H` restricted to `U_0^{[⊥]}` has positive
index `(n - p) - dim U_0 = k - p`; let `U_1` be a subspace of
`U_0^{[⊥]}` of that dimension on which it is positive definite. `U = U_0 ⊕ U_1` is `H`-positive definite, has dimension
`n - p`, and contains `ker A`, so `U = ker M` for some `M` with `p` rows in
the row space of `A`, that is `M = R A`. Finsler's lemma gives the second
claim. (b) `ker M` would be an `H`-positive-definite subspace of dimension
greater than `n - p`, the number of positive eigenvalues. (c) With `eta_t = 0`, the
proof of Lemma 4.4 gives
`Phi = F(x) + mû^T(A x - b) + rho |R(A x - b) + sum_t delta_t|^2 + (brackets)`:
the linear terms kept in the bags are exact at the consistent point
because columns are assigned to top bags, and the penalty has zero slope
at `x*`. Steps 1–8 of Theorem 4.5 then apply with
the margin `c_P X^2` in place of Corollary 4.2. □

So the exponent of the coupling part counts the **bad directions of the
Lagrangian**, not the rows: `p = 0` gives Theorem 3.1, and in general only
`p <= k` combinations of rows need partial sums. Parts (a) and (b) are local;
the global hypothesis in (c) must be checked or assumed. The construction
of `R` uses the classical fact that positive subspaces extend to maximal
ones; the proposition is likely known in the exact-penalty literature in
some form (not searched).

### 4.5 Localized branching: what Shapley–Folkman gives and what it does not

Route L would close the gap by spatial branching restricted to the few
places Theorem 2.2 marks as fractional. Two facts delimit this.

- *Nonconvexity confined to few bags.* If every `a_t` outside a set `Q` of
  bags is convex on its box, a node relaxation that replaces each `a_t`,
  `t in Q`, by its envelope on the node box is a convex program with linear
  rows, so its Lagrangian dual is exact, and branching only on the
  variables of `Q` converges (Dür–Horst 1997; reduced-space convergence
  orders in Kannan 2018, Chapter 6). The count is exponential in the
  dimension of the branched space, `|Q| (w+1)`, not in `k`.
  Proposition 2.5 bounds the number of bags with negative curvature **at
  `x*`** by `k`, but it says nothing about nonconvexity elsewhere in the
  box.
- *In general, no.* Theorem 5.1: with `w = 0`, `k = 1` and one fractional
  block at every dual optimum, every B&B tree with the exact Lagrangian
  node bound and no bound tightening has at least `C(n+1, (n+1)/2)` leaves
  (FBBT on the row changed no count in the computations of Section 9.1). The Shapley–Folkman
  count limits the fractional part of **one** relaxation solution. The
  fractional block moves from node to node, and the tree must exclude every
  parity pattern.

So SF-localized branching has a guarantee only under extra structure (few
nonconvex bags, or partial LQG with lifting as in Proposition 4.6).

## 5. Lower bounds (item 4)

### 5.1 Shapley–Folkman bounds the gap, not the certificate

**Theorem 5.1 (Jeroslow-type instance, `w = 0`, `k = 1`).** Let `n` be odd,
`m = (n-1)/2`, `c > 0`, and

```
(J_n)   min  sum_i c y_i (1 - y_i)   s.t.  sum_i y_i = n/2,   y in [0,1]^n.
```

(a) `OPT = c/4` and `D = 0`. Every extreme optimal point of Theorem 2.1 has
exactly one fractional block, so the Shapley–Folkman bound
`k max_i rho(f_i) = c/4` is attained.

(b) Consider any spatial B&B tree on `[0,1]^n` (any branching variable and
split point at every node, any node order, any incumbent value
`UBD >= OPT`, no bound tightening) whose node bound on a box `B` is at most
the coupling-Lagrangian dual on `B`,

```
D(B) = min { sum_i vex_{B_i}(c y (1-y))(y_i) : sum_i y_i = n/2, y in B },
```

and which proves tolerance `eps < c/4`. It has at least

```
C(n, m) + C(n, m+1) = C(n+1, (n+1)/2) >= 2^{n+1}/sqrt(2(n+1))
```

leaves.

(c) The partial-sum value functions are explicit:
`U_t(s) = min { sum_{i<=t} c y_i(1-y_i) : sum_{i<=t} y_i = s, y in [0,1]^t } = c phi(s)`
with `phi(s) = frac(s)(1 - frac(s))`, `s in [0, t]`. So a DP over one
partial sum certifies `OPT = U_n(n/2) = c/4` with `t` concave quadratic
pieces at stage `t` (one per interval `[j, j+1]`), `O(n^2)` pieces in all,
each recursion step being a one-dimensional check. (This is Vavasis's exact
DP for separable concave quadratic knapsacks, 1992, Theorem 4.)

(d) *The same model on both sides.* In the lifted-certificate model of
Section 4.2 (path of bags `t = 1..n`, bag `t` holding `(zeta_{t-1}, y_t)`,
`zeta_t = zeta_{t-1} + y_t`, the root imposing `zeta_n = n/2`), take
partial-sum cells of side `1/2`, the `y`-pieces `[0, 1/2]` and `[1/2, 1]`,
bag leaves equal to (child cell) x (`y`-piece), envelope (chord)
relaxations of `c y(1-y)` on the pieces, and on every cell the minorant
`(c/2) dist(zeta, Z)`. This is a valid certificate with root bound
`l_r = c/4 = OPT` exactly, and its size is `3n^2 - 3n + 2`. With cells of
side 1 the same construction gives `l_r = 0`, the Lagrangian dual.

*Proof.* (a) The objective is concave, so its minimum over the polytope
`{y in [0,1]^n : sum y = n/2}` is attained at a vertex. Vertices have at
most one fractional coordinate, and since `n` is odd exactly one, equal to
`1/2`: value `c/4`. The envelope of `c y(1-y)` on `[0,1]` is 0, so `D = 0`
(Udell–Boyd, Appendix A, or Theorem 2.1). At an extreme optimal point of
Theorem 2.1 all but one block are Dirac measures (Theorem 2.2), zero cost
forces supports in `{0,1}`, and a sum of `n/2` forces one non-Dirac block.

(b) *Step 1.* Let a leaf `B` contain binary points `z`, `z'` with
`|z| <= m` and `|z'| >= m + 1`. Let `P = {i : z_i != z'_i}`; then
`B_i = [0,1]` for `i in P`. Keep `y_i = z_i` off `P` and choose
`y_P in [0,1]^P` with `sum y = n/2`: this is possible because the sum of
the agreeing part is `a = |z ∧ z'|` and `0 < n/2 - a <= |z'| - a <= |P|`.
At `y`, every envelope term vanishes: on `P` because `vex_{[0,1]} = 0`, off
`P` because `y_i in {0,1}` is an endpoint of `B_i ⊂ [0,1]`, where the
envelope equals the function. So the node bound is at most
`D(B) <= 0 < c/4 - eps <= UBD - eps`, and `B` is neither pruned nor
infeasible, which is impossible for a leaf.
*Step 2.* The binary points of a box `B ⊂ [0,1]^n` form a subcube: the
coordinates with `B_i = [0,1]` are free, those whose interval contains one
of `0, 1` are fixed. By step 1 the subcube of a leaf is all "low"
(weights `<= m`) or all "high" (`>= m+1`). A low subcube contains at most
one point of weight `m` (its top) and none of weight `m + 1`; a high one at
most one point of weight `m + 1` (its bottom) and none of weight `m`.
*Step 3.* The leaves cover `[0,1]^n`, so each of the
`C(n, m) + C(n, m+1)` binary points of weight `m` or `m + 1` lies in some
leaf, and no leaf holds two of them. The last inequality is the central
binomial bound `C(2j, j) >= 4^j/sqrt(4j)` with `2j = n + 1`.

(c) The same vertex argument on `{y in [0,1]^t : sum y = s}`: a vertex has
`floor(s)` ones and at most one fractional coordinate, equal to
`frac(s)`.

(d) Let `dist(u) = dist(u, Z)`. The chord of `c y(1-y)` on `[0, 1/2]` is
`(c/2) y` and on `[1/2, 1]` it is `(c/2)(1 - y)`: in both cases
`(c/2) dist(y)`. The function `(c/2) dist` is affine on every cell of side
`1/2`, so it is an admissible cell minorant, and all minorants are pieces of
one continuous function, so (CM) holds for every cell that meets a leaf's
projection. (LC) at bag `t` reads
`(c/2) dist(y) + (c/2) dist(zeta_{t-1}) >= (c/2) dist(zeta_{t-1} + y)`,
which is the subadditivity of `dist(·, Z)`. At the root every point with
`zeta_n = n/2` has relaxed value at least `(c/2) dist(n/2) = c/4`. The
cells of stage `t` cover `[0, t]` (`2t` cells) and the leaves cover the bag
boxes (`2` at `t = 1`, `4(t-1)` for `t >= 2`), so for `n >= 2` the size is
`2 + 2 + sum_{t=2}^{n-1} (4(t-1) + 2t) + 4(n-1) = 3n^2 - 3n + 2` (at `n = 1`
the closed form 2 is right and the itemized sum is not). With cells
of side 1 the chords of `c phi` on `[j, j+1]` vanish, so every minorant is
at most 0. □

*Remarks.*

- **Tightness.** A best-first B&B with the exact node bound (a continuous
  knapsack over chords) and either bisection or splitting at the relaxation
  point used exactly `C(n+1, (n+1)/2)` leaves for `n = 3, ..., 13` and
  `eps = 0.05, 0.01` (`jeroslow_bb.py`; 6, 20, 70, 252, 924, 3432 leaves).
  The review found the same counts with three further deterministic rules,
  and the exact minimum over all trees with split points on small grids
  (`n = 3, 5, 7`) equal to the bound.
- **Bound tightening.** The proof of (b) fails under FBBT: propagating the
  row can move the constructed point's free coordinates off `[0,1]`. But
  FBBT on the row, applied at every node, changed no leaf count in
  `jeroslow_bb.py` (both rules, `n <= 13`) nor in the review's exact
  minima. Extending (b) to bound tightening is open.
- **Prior art.** The count itself is not new. In Jeroslow's binary
  instance (`max x_1` s.t. `2 sum x_i = n`, `x` binary, LP bounds,
  branching by fixing), a node is infeasible exactly when `m + 1` ones or
  `m + 1` zeros are fixed, and no incumbent exists, so **every** tree has
  exactly `2 sum_{j<=m} C(m+j, j) = C(n+1, (n+1)/2)` leaves (a lattice-path
  count; Jeroslow 1974 states `2^{(n+1)/2}`). What (b) adds is the transfer
  to continuous spatial branching with arbitrary split points and
  Lagrangian/envelope node bounds. The message "exponential B&B on
  instances that a DP solves in polynomial time" is known for MILP:
  Dey–Shah (ORL 2022; lot-sizing, general split disjunctions,
  `2^{n/2 - 1}` leaves, `O(n log n)` DP) and Dey–Dubey–Molinaro (Math.
  Prog. 2023). The DP in (c) is Vavasis (1992); NP-hardness of the concave
  quadratic knapsack is Sahni (1974), and Moré–Vavasis (1991) show that its
  local minimizers have at most one fractional coordinate (from memory,
  per the review).
- **Both sides in one model.** (b) and (d) are statements in comparable
  models: spatial B&B leaves versus the boxes of a lifted certificate.
  `3n^2 - 3n + 2` exceeds `C(n+1, (n+1)/2)` for `3 <= n <= 7` (they are equal
  at `n = 1`) and is smaller from
  `n = 9` on (218 against 252); at `n = 25` it is 1,802 against
  10,400,600 (`jn_lifted_cert.py`, exact rational arithmetic, and the
  review's independent construction). The certificate uses a piecewise
  affine price `(c/2) dist(zeta, Z)` on the partial sum, which no single
  multiplier can express.
- **What is covered.** Any node bound not above the Lagrangian dual:
  termwise envelopes with the row, alphaBB, and in particular
  Shapley–Folkman-localized branching (branching only on the fractional
  block of the current relaxation solution). Not covered: bound tightening
  (FBBT on the row can cut the constructed point's box), cuts that exploit
  parity, and reformulations such as partial sums, which is exactly what
  (c) uses.
- **A unique minimizer does not help.** Adding `tau_i y_i` with generic
  `sum_i |tau_i| < (c/4 - eps)/2` makes the minimizer unique and keeps the
  bound (the constructed point has relaxed value at most `sum |tau_i|`, and
  `OPT >= c/4 - sum |tau_i|`). Other parity patterns are within
  `2 sum |tau_i|` in value at distance at least 1, so any quadratic-growth
  constant is at most `2 sum |tau_i|`: such instances are badly
  conditioned, consistent with the conditioning factors of Section 4.3.
- **Absolute versus relative accuracy.** The absolute gap `c/4` is
  `k rho_max`, as Shapley–Folkman predicts, but closing it costs
  `2^Omega(n)` leaves in this model. If every block also carries a
  constant cost 1, then `OPT = n + c/4`, the root's relative gap is
  `c/(4n + c) = O(1/n)`, and no branching is needed for relative accuracy
  of that order, while the leaf bound of (b) is unchanged for every
  absolute tolerance `eps < c/4`.

### 5.2 Exponential dependence on `k` at a nondegenerate minimizer

**Proposition 5.2.** Let `m >= k` be a power of 2, `H_m` a Hadamard matrix,
`gamma = 1/(2 sqrt m)`, and `a_j = gamma H_m[j,:]/sqrt(m)` for
`j = 1..k` (orthogonal dense rows, `|a_j|_2 = gamma`, `|a_j|_1 = 1/2`). On
`x in [-1,1]^m`, `s in [-1,1]^k` consider

```
min  sum_i x_i^2/2 + sum_j h(s_j)   s.t.  s_j = a_j^T x  (j = 1..k),     h(s) = -beta s^2/2 + s^4,
```

with `beta = 0.8/gamma^2 = 3.2 m`. All nonlinear terms are unary, so the
nonlinear primal graph has no edges (`w = 0`), and there are `k` dense
rows. Relax each `h` on a box by alphaBB with `alpha = beta/2` (valid since
`h'' >= -beta`) and keep the convex terms exact. Then:

(a) `(x*, s*) = (0, 0)` is the unique minimizer, nondegenerate, with
quadratic growth on the feasible set; the Hessian of the objective has
exactly `k` negative eigenvalues, so `p = k` bad directions and `D < OPT`
(Proposition 2.6(c); the dual optimum is attained because `0` is an
interior point of the set of row residuals `{s - A x}` over the box), and
by Proposition 4.6(b) every exact augmentation must see `k` row
combinations.

(b) Every single-tree certificate at tolerance `eps <= 0.1/k^2` (leaves are
boxes in `(x, s)`; leaf bounds minimize the relaxation subject to the rows)
has at least

```
N >= 2 (2k/pi)^{k/2} (alpha/lambda')^{k/2} Gamma(k/2)^{-1} J_k( sqrt(lambda'/(8 k^2 eps)) )
  = (1 + o(1)) sqrt(k/pi) (4 e alpha/(pi lambda'))^{k/2} (1/2) log(1/eps),
```

leaves, where `lambda' = 1/gamma^2 - beta + 1/(2k^2)` and `J_k` is as in
[D, Corollary 2.1]. Here `alpha/lambda' >= 1.729` for `m >= 4` and tends to
2, so the base is at least `sqrt(4e · 1.729/pi) ≈ 2.45` per row.

(c) The same bound holds for the leaves of one bag of any lifted
certificate in which that bag contains all `s_j` and carries all `k` terms
`h(s_j)` (for example the root of the partial-sum decomposition, where all
rows close).

*Proof.* (a) With `A A^T = gamma^2 I`, `min{|x|^2/2 : A x = s} = |s|^2/(2 gamma^2)`,
attained at `x(s) = A^T s/gamma^2`. So on the feasible set the objective is
`|x_⊥|^2/2 + psi(s)` with `x_⊥` the part of `x` in `ker A` and
`psi(s) = sum_j (lambda s_j^2/2 + s_j^4)`, `lambda = 1/gamma^2 - beta = 0.8 m > 0`.
This is at least `min(1/2, lambda gamma^2/2) |x|^2`, using
`|x|^2 = |x_⊥|^2 + |s|^2/gamma^2`. The Hessian in `(x, s)` at 0 is
`diag(I_m, -beta I_k)`.
(b) Let `r_k = 1/(2k)` and `S_0 = [-r_k, r_k]^k`. For `s in S_0`,
`|x_i(s)| <= |s|_1/(gamma sqrt m) <= 1`, so `(x(s), s)` is feasible and in
the box; its objective value is `psi(s)`. The leaf containing it has bound
`>= f* - eps` and, since the relaxation is exact in `x` and has gap
`alpha q_{B}` in `s`, `psi(s) + eps >= alpha sum_j a_j^{B}(s_j)`. As in
[C, Theorem 3.1], integrating `(psi + eps)^{-k/2}` over `S_0` and using the
arcsine integral on each leaf gives
`N >= (k alpha/pi^2)^{k/2} ∫_{S_0} (psi(s) + eps)^{-k/2} ds`. On `S_0`,
`s_j^4 <= r_k^2 s_j^2`, so `psi(s) <= (lambda'/2)|s|^2`; restrict to the
Euclidean ball of radius `r_k` and use polar coordinates as in
[D, Corollary 2.1]. The condition on `eps` makes the argument of `J_k` at
least `sqrt(k)`, where `J_k(T) >= (e^{-1/2}/2) log(T^2/k)`. Numbers:
`alpha/lambda' = 1.6 m/(0.8 m + 1/(2k^2)) >= 6.4/3.7 = 1.7297` for `m >= 4`.
(c) The chain inequality [D, Lemma 1.4] holds for lifted certificates at
feasible points (all copies equal), so the bag lemma [D, Lemma 2.2] applies
to that bag with `K = {s_1, ..., s_k}` and the points `(x(s), s)`. □

**Extension to Lagrangian node bounds.** For `m >= 4`,
`h'' = -beta + 12 s^2 <= -(beta - 12) < 0` on `[-1, 1]`, so `h` is concave
there and its convex envelope on a box `[l, u]` is the chord, with gap
`h - chord >= ((beta - 12)/2)(s - l)(u - s)` (the difference has second
derivative at most `-(beta - 12)` and vanishes at both ends). The proof of
(b) therefore holds for termwise envelope relaxations with
`alpha' = (beta - 12)/2 = 1.6 m - 6` in place of `alpha`. For this
separable instance, envelope node bounds with the rows are exactly the
node-wise coupling-Lagrangian duals (Theorem 2.1 with single-variable
blocks), that is, Route L's node bounds. The base
`sqrt(4 e alpha'/(pi lambda'))` is below 1 at `m = 4` (0.61–0.65), between
1.85 and 1.92 at `m = 8`, between 2.26 and 2.30 at `m = 16`, and tends to
`sqrt(8e/pi) = 2.63` (range over `1 <= k <= m`; computed from the closed
form, and 1.91, 2.30 in the review). So `exp(Omega(k))` also holds for
Route L's node bounds once `m >= 8`.

The instance is "a nonconvex function of `k` aggregates": `k` dense rows
create an effective nonconvex block of dimension `k`, and the single-tree
cost is exponential in `k` exactly as [D, Proposition 2.3] is exponential in
`w`. It matches the exponent `p Delta_1` of Proposition 4.6 in form. Not
covered: lifted decompositions that attach the `s_j` to different bags; a
lower bound on partial-sum cells for those is open.

### 5.3 Complexity: what must enter a bound

**Proposition 5.3.** Let `w = 0` (all nonlinear terms unary) and absolute
accuracy `eps`.

(a) *One row.* For integers `a_1, ..., a_n, B > 0`, the instance
`min sum_i c y_i(1 - y_i)` s.t. `sum_i a_i y_i = B`, `y in [0,1]^n`, has
`OPT = 0` if some subset of the `a_i` sums to `B`, and
`OPT >= c/(2(sum_i a_i + 1))` otherwise. So computing `OPT` to accuracy
`eps` with `log(1/eps)` polynomial in the input size is NP-hard already for
`k = 1`.

Model of computation: a Turing machine that queries objective values at
rational points to a requested number of bits. `sin^2(pi y)` at rational
`y` can be computed to `p` bits in time polynomial in `p`, so (b) covers
algorithms that such a machine can simulate; it does not cover exact
real-RAM algorithms as such.

(b) *`k` rows.* Assume the Exponential Time Hypothesis. Knop, Pilipczuk
and Wrochna (STACS 2019; arXiv 1811.01296) show that ILP feasibility
`{A z = b, z in Z^l, z >= 0}` with `A in {0,1}^{k x l}` cannot be solved in
time `2^{o(k log k)} (l + ||b||_inf)^{o(k)}`. The instance
`min sum_i c sin^2(pi y_i)` s.t. `A y = b`, `y in [0, ||b||_inf]^l` (columns
of `A` nonzero) has `OPT = 0` iff the ILP is feasible, and
`OPT >= 4c/(l + 1)^2` otherwise. Hence no algorithm computes `OPT` of
`w = 0` instances with `k` dense rows to absolute accuracy `eps` in time
`2^{o(k log k)} (n + s0)^{o(k)} polylog(1/eps)`; in particular not in time
`poly(n, s0) 2^{O(k)} polylog(1/eps)` with a polynomial independent of the
instance.

*Proof.* (a) If every `y_i` were within `delta = 1/(sum a_i + 1)` of
`{0, 1}`, rounding would give a binary `z` with
`|sum a_i z_i - B| <= delta sum a_i < 1`, hence an exact subset sum. So some
`y_i(1 - y_i) >= delta(1 - delta) >= delta/2`. (b) If every `y_i` were
within `delta = 1/(l+1)` of an integer `z_i`, then `z >= 0` and
`|A(y - z)|_inf <= l delta < 1`, so `A z = b` with `z` integral. Otherwise
some `sin^2(pi y_i) >= sin^2(pi delta) >= 4 delta^2`. Integer solutions
satisfy `z_i <= ||b||_inf` because columns are nonzero and nonnegative. The
running-time class `poly(n, s0) 2^{O(k)}` lies inside
`2^{o(k log k)}(n + s0)^{o(k)}` as `k -> infinity`. □

*What this means for the upper bounds.* Proposition 5.3 does **not** show
that conditioning must enter. It excludes running times
`poly(n, s0) 2^{O(k)} polylog(1/eps)`, but it allows `(n + s0)^{O(k)}`
(Papadimitriou-type pseudo-polynomial DP) and `2^{O(k log k)}`-type bounds
(Eisenbrand–Weismantel). So a correct bound must depend on something
beyond `poly(n, s0) 2^{O(k)}`: on `k log k`, on the scale
`(n + s0)^{Omega(k)}`, or on conditioning. Theorem 4.5's size contains
`Gamma_sigma^{k Delta_1}`: its dependence on `k` is already
`exp(O(k log k))`, and it depends on the depth and on conditioning. The
hard instances of Proposition 5.3 have no quadratic growth (many or nearly
degenerate optima), so they do not contradict it. Two caveats: ETH bounds concern running time,
not certificate size (small certificates for hard instances are not
excluded by this argument); and our certificates are built around a known
`x*`, so their size bounds say nothing about the cost of finding them.
Unconditional certificate-size lower bounds are Theorem 5.1 (model:
Lagrangian node bounds, `2^Omega(n)`) and Proposition 5.2 (termwise
relaxations, `exp(Omega(k)) log(1/eps)` at a nondegenerate minimizer).

## 6. Comparing the two routes (item 3)

### 6.1 Width accounting for partial sums

In the lifted problem of Section 4.2, bag `t` holds `x_{V_t}` and the
partial sums of its children; its own partial sum is an affine function of
these. So the lifted width is at most `w + k Delta_1`, and `w + k` on a
path. Two refinements:

- Only rows that cross an edge need a partial sum there: the lifted width
  is at most `w + max_t sum_{u in ch(t)} k_{e(u)}` with the row crossing
  numbers `k_e` of Section 0. For dense rows this is `k Delta_1`.
- The census's factor-incidence graph (rows as hub nodes joined to their
  variables and terms) is the elimination-based version of this lifting,
  so Route P's width is what the census's first column measures. Removing
  a set `R` of row nodes lowers treewidth by at most `|R|`:
  `tw(G) <= tw(G - R) + |R|`. So Route L with the rows `R` dualized works on
  a graph of **treewidth** at least `tw(G) - |R|`: a large treewidth can
  only be removed by dualizing at least that many rows. This applies to
  true treewidth, not to the min-degree upper bounds of the census, which
  can move non-monotonically.

### 6.2 Which route is better

| regime | Route L (dualize, then branch) | Route P (partial sums) | better |
|---|---|---|---|
| (LQG): no bad directions, `p = 0` | Theorem 3.1: `\|T\| C^{w+1} log(\|T\|/eps)`, independent of `k` | Theorem 4.5: extra `Gamma_sigma^{k Delta_1}` and a second log | L |
| `0 < p < k` bad directions, partial LQG | dual alone has a gap (Proposition 2.6(c)) | lift only `p` row combinations (Proposition 4.6): exponent `p Delta_1` | hybrid |
| duality gap, unique minimizer with (QG), no LQG information | no general guarantee; SF-localized branching can be exponential (Theorem 5.1 shows this for degenerate instances) | Theorem 4.5 | P |
| near-integer or degenerate structure, small integer coefficients | `>= C(n+1, (n+1)/2)` leaves (Theorem 5.1) | exact lifted box certificate with `3n^2 - 3n + 2` boxes (Theorem 5.1(d)); smaller from `n = 9` on | P |
| large integer coefficients (subset sum) | NP-hard for absolute accuracy (Proposition 5.3) | pseudo-polynomial in the coefficient range | P, pseudo-polynomially |
| relative accuracy, many bags, separators pinned (or separable blocks) | Lagrangian alone: relative gap `<= k rho_max/\|OPT\|` (Corollary 2.3) | unnecessary | L |
| tightly coupled tree with a gap (Example 2.4) | relative gap up to 100% with `k = 1` | exact with one extra coordinate | P |
| rows sparse across separators (`k_e` small) | still dualizes all `k` rows | width grows by `k_e` only | P |

Rules of thumb that follow:

1. First dualize and test. The number of bad directions `p` of the
   Lagrangian Hessian at the local solution is computable from the local
   solve (inertia of `∇²F(x̂)`, Proposition 2.5). If `p = 0`, the coupling
   rows cost nothing beyond a multiplier (Theorem 3.1).
2. If `p > 0`, lift `p` combinations `R A` of the rows (Proposition 4.6)
   rather than all `k`, and keep the rest in the Lagrangian.
3. Use partial sums along a shallow decomposition when possible: the drift
   factor grows with the depth `d` (Theorem 4.5).
4. Do not expect Shapley–Folkman-localized branching to close absolute
   gaps on near-integer structure (Theorem 5.1).

### 6.3 Rows and global variables

A dense coupling row and a global variable (a variable present in every bag,
such as lnts's time step `h`) are dual obstacles. A global variable raises
the width by one; it can be branched on (one dimension, as a first-stage
variable) or, as in lnts, handled by monotonicity. A dense row raises the
factor-incidence width by one; it can be dualized (one multiplier) or lifted
(one partial-sum chain). Dualizing a row and branching on a global variable
are the two sides of the same Lagrangian/Benders pairing, and both fail in
the same way when the value function in the global coordinate is
nonconvex: the Lagrangian then needs lifting, and branching needs
refinement.

## 7. Practical certificates and the census (item 5)

### 7.1 waterno2: the horizon row is not the bottleneck of the wave-2 certificate

Structure [W, Section 2]: `T` periods of 166 variables, linked by 3 tank
levels per transition (separators of dimension 3), plus **one** horizon row
`sum_t q_t >= c` with one variable per period (`k = 1`). The census gives
factor-incidence width 9 with the horizon row and 7 after dropping the
objective-defining rows; the horizon row is the densest remaining row
(degree `T`), and removing it is not needed to reach width 12.

The wave-2 certificate dualized the level links **and** the horizon row, so
its blocks are the periods and it has `3(T-1) + 1` rows. In the language of
this note:

- Classical Shapley–Folkman then allows `min(3(T-1) + 1, T) = T`
  fractional periods, that is, all of them, which matches the diagnosis of
  [W, Section 7, item 6]: the period
  solutions jump to extreme start levels, and the gap (5–11%) comes from
  the level links.
- Keeping the links in the tree and dualizing only the horizon row
  (Route L with `k = 1`) leaves at most one fractional component
  (Theorem 2.2), but that component may span all periods, as in
  Example 2.4, because tank levels couple consecutive periods tightly. The
  only available estimate ([W], `horizon_only.py`, `T = 3`, one multiplier
  `mu = 194.26`, SCIP with a time limit) found a point (feasible to SCIP's
  tolerance) of the horizon-dualized problem with value 113.29 below the optimum 115.00, so at
  that multiplier this Lagrangian leaves a gap of at least 1.5%. The best
  multiplier was not computed.
- Route P for the horizon row adds one partial-sum coordinate to each
  3-dimensional level separator. The coarse version was tried: a DP over
  bins of the horizon variable gained +0.0005 [W, Section 7, item 3]. This is
  what the theory predicts when the gap sits in the separators (the gain
  was measured on waterno2_06): the horizon row contributes at most one
  fractional component, and the level
  cells are what must be refined ([D, Theorem 3.4]; the report's DP over
  level boxes raised waterno2_03 from 74.07 to 75.38 before it became too
  expensive).

So the dense row is not the bottleneck of the wave-2 certificate; its
difficulty is the 3-dimensional separator with nonconvex, head-dependent
period value functions, the regime of [D] and [K]. Whether the horizon
row alone leaves a gap at its best multiplier is not known (the estimate
above shows at least 1.5% at one multiplier).

### 7.2 lnts: three rows, a global variable, and an exact Lagrangian

Structure [O, Section 3]: controls `th_0..th_N`, states, and one global time
step `h` that lies in every separator (census width 11–12). For fixed `h`
the dynamics are linear, and eliminating the states leaves **three dense
rows** in the single-control blocks (`w = 0`): `sum w cos th = A(h)`,
`sum w sin th = 0`, `sum c sin th = B(h)`. The certificate is the coupling
Lagrangian of these three rows with multipliers `(mu, nu)` and per-block
closed-form maxima.

- It has no duality gap: the convexified problem
  `max sum w_j sqrt(1 - s_j^2)` is exact because the upper boundary of each
  block's image is concave. This is consistent with Theorem 3.1's regime,
  with `k = 3`, but the theorem was not needed (the Lagrangian has
  closed-form block maxima) and (LQG) was not verified.
- The global variable `h` is not dualized or branched: monotonicity of
  `A(h)` and `B(h)` replaces branching on it (Section 6.3).
- The census sees lnts at width 11–12 with no dense row to remove; the
  small-`k` structure appears only after the linear state elimination, which
  the graph heuristics do not perform.

### 7.3 Census: how many instances have small `w` and small `k`?

**Heuristic** (`census_k.py`, `census_k2.py`, `census_k3.py`,
`census_k_rows.py`, `census_k_analyze.py`). The graph is the census's
factor-incidence graph (variables, row hubs, nonlinear-term nodes), with
the same min-degree width upper bound.

1. *Free rows.* The objective row and objective-defining rows (a row that is
   the only constraint containing a variable with a linear objective
   coefficient) are removed at no cost: any DP sums their terms, so they
   are not coupling rows. The min-degree bound is not monotone under row
   removal (dropping free rows raised it in 44 instances, per the review),
   so the starting width is `min(w_full, w_free)`.
2. *Coupling rows*, two greedy rules. **Densest first:** remove the `r`
   rows of largest degree, `r in {1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64}`.
   **Bag-targeted:** repeatedly remove the row hub of largest degree in the
   bag where the width is attained, up to 64 rows or 240 s; it stops early
   when that bag contains no row hub. A removed row's nonlinear terms stay
   as factors (dualizing a row does not remove its terms).
3. `k` is the smallest number of removed rows after which the width bound
   is at most 12, minimized over the two rules; "not reached" means more
   than 64 rows, an early stop, or a time limit.
4. *Rows the theory covers.* Sections 3–4 treat linear equality rows;
   linear inequalities are covered through slack variables; nonlinear rows
   are not covered. `census_k3.py` reruns both rules with only linear rows,
   or only linear equality rows, eligible (on the 99 instances where the
   unrestricted rules reached width 12 with 1–64 rows; the others keep
   their status). `census_k_rows.py` classifies the rows that the
   unrestricted bag rule removed.

**Results** (`logs/census_k_summary.log`; 582 nonconvex instances with at
least 100 nonlinear variables, as in the census; percentages of the class
size; 581 of 582 processed, the remaining one, acopf_caseactivsg70k_qcqp
with nonlinear width 255, counts as "not reached").

All rows eligible:

| class | size | `k = 0` | `k <= 2` | `k <= 4` | `k <= 8` | `k <= 16` | `k <= 32` | `k <= 64` |
|---|---|---|---|---|---|---|---|---|
| all | 582 | 86 (14.8%) | 88 (15.1%) | 97 (16.7%) | 103 (17.7%) | 110 (18.9%) | 153 (26.3%) | 184 (31.6%) |
| nonlinear width `<= 12` | 365 | 78 (21.4%) | 80 (21.9%) | 89 (24.4%) | 95 (26.0%) | 101 (27.7%) | 144 (39.5%) | 173 (47.4%) |
| gap class: nonlinear `<= 12`, factor-incidence `> 12` | 294 | 7 (2.4%) | 9 (3.1%) | 18 (6.1%) | 24 (8.2%) | 30 (10.2%) | 73 (24.8%) | 102 (34.7%) |
| open (MINLPLib gap `> 1e-4`) | 362 | 59 (16.3%) | 61 (16.9%) | 68 (18.8%) | 74 (20.4%) | 78 (21.5%) | 93 (25.7%) | 103 (28.5%) |

Only the rows the theory covers (class "all", 582 instances; rerun with
restricted eligibility):

| eligible rows | `k = 0` | `k <= 2` | `k <= 4` | `k <= 8` | `k <= 16` | `k <= 32` | `k <= 64` |
|---|---|---|---|---|---|---|---|
| linear rows | 86 (14.8%) | 88 (15.1%) | 96 (16.5%) | 101 (17.4%) | 108 (18.6%) | 142 (24.4%) | 164 (28.2%) |
| linear equality rows | 86 (14.8%) | 87 (14.9%) | 94 (16.2%) | 99 (17.0%) | 104 (17.9%) | 117 (20.1%) | 131 (22.5%) |

Findings.

- **Small `w` plus small `k` adds little.** With at most 8 dualized rows,
  17.7% of the large nonconvex instances reach width 12 if any row may be
  dualized, against 14.8% with none. Restricted to the rows the theory
  covers, the share at `k <= 8` is 17.2–17.4% (linear rows) and 16.3–17.0%
  (linear equality rows). The lower values classify the rows removed by the
  unrestricted bag rule (the review's method; with the old baseline of 85
  it gives 17.0% and 16.2%); the upper values rerun the rules with only
  those rows eligible. So the coupling theory of Sections 2–4 extends the
  reach of decomposition certificates by about two percentage points
  (1.5–2.6) at `k <= 8`.
- **The census gap is not caused by a few dense rows.** In the gap class
  (294 instances; 290 with a starting width) the median width after
  dropping free rows is 49.5 (quartiles 31, 108). The bag-targeted rule
  ended as follows:
  - reached width 12 in 82 instances, after a median of 28 rows;
  - hit the 64-row cap in 121, with median width only lowered from 99 to 71;
  - stopped early in 77 because the widest bag contained no row hub
    (median 15 rows removed, width 40 to 30);
  - hit the time cap in 10;
  - (4 further instances had no starting width within the time limit.)

  The overall median of 43.5 removed rows reported in the first version
  mostly reflects the cap and the early stops, and the stop rule can
  overestimate `k` when rows eliminated earlier cause the width. The
  conclusion stands on the 121 capped instances, which keep a median width
  of 71 after 64 rows: the width comes from the linear structure itself
  (network balances, assignment and facility constraints), not from a few
  dense rows. The rows the bag rule removed have median degree 14
  (quartiles 9, 31). Such instances need other tools: dualizing many rows
  (where Shapley–Folkman gives weak absolute bounds [S]) or
  structure-specific decompositions.
- **Candidates.** With any rows eligible, 25 instances had
  `1 <= k <= 16`. casctanks is dropped: its width is 11 with all rows, and
  its apparent `k = 2` came from the non-monotone bound after dropping free
  rows. Of the other 24, 19 are open. In the bag rule's selection, 13 use
  only linear equality rows, 7 also use linear inequality rows, and 4 use
  nonlinear rows (kall_ellipsoids_tc03c, powerflow0030r, tln12,
  wastepaper6; all open). With only linear rows eligible, powerflow0030r
  still reaches width 12 with 3 rows, while kall_ellipsoids_tc03c (24
  rows), tln12 (36) and wastepaper6 (not reached) do not.
  kall_ellipsoids_tc03c also has nonlinear width 14 > 12, so it is not a
  small-`w` instance. Restricting to linear rows and nonlinear width at most
  12 leaves 22 candidates with `1 <= k <= 16` (17 open; powerflow0057r
  enters with `k = 14`), and 18 with linear equality rows only (14 open).
  The open ones are water networks (waternd_fossiron,
  waternd_fosspoly0/1, waternd_modena, waternd_pescara, waterno1_03/04/06,
  waterful2), facility location (sfacloc1_3_90, sfacloc1_4_95), power flow
  and transmission switching (powerflow0030p/r, powerflow0057r,
  transswitch0030p/r) and ann_cumene_tanh. They are the natural targets for
  Route L or P certificates.
- **The program's families** (waterno2, lnts, camshape, rocket, catmix,
  chain, dtoc5, optcdeg2, lukvle10, kriging_peaks) all have `k = 0`: their
  width is at most 12 with every row present. kriging_peaks has one row of
  degree `n + 1`, and waterno2 its horizon row of degree `T`, but neither
  raises the width above 12.

Caveats: widths are upper bounds; the greedy rules can overestimate `k`;
dense rows that appear only after eliminating defined variables (lnts) are
not detected; the free-row rule is syntactic; the restricted reruns cover
only the 99 instances where the unrestricted rules succeeded within 64
rows.

## 8. Literature and what is new (item 6)

Sources marked "local" were read in `literature/papers` (full text or read
notes); "from memory" means not re-read for this note; "abstract" means
only the abstract or listing was checked. An unsuccessful search does not
establish novelty.

**Shapley–Folkman duality-gap bounds (separable blocks).**

- Starr (1969) and Aubin–Ekeland (MOR 1976), from memory: gap at most
  `min(m+1, n) max_i rho_i` for `m` linking rows and `n` blocks.
- Bertsekas, Lauer, Sandell, Posbergh (IEEE TAC 1983), from memory: the
  relative gap of unit commitment tends to zero with the number of units;
  Bertsekas, *Convex Optimization Theory* (2009), Section 5.7, from memory.
- Udell–Boyd (COAP 2016), local: the sum of the `min(m~, n)` largest
  `rho_i`, `m~` = equalities plus active inequalities; tight; extreme points
  of the convexified optimal set achieve it, interior optima can be
  arbitrarily bad.
- Kerdreux–Colin–d'Aspremont (MOR 2023), local: stable and approximate
  bounds; only active constraints matter.
- Dubois-Taine–d'Aspremont (MP 2025), local: constructive Frank–Wolfe with
  Shapley–Folkman steps. Bi–Tang (SIOPT 2020), per [S].
- Dey–Xu (arXiv 2601.19003, 2026), local:
  `OPT(b + E 1) - E <= D(b) <= OPT(b)` with `E` the Hausdorff nonconvexity
  of the Minkowski sum; `E -> 0` for smooth blocks under pointedness and a
  projection-factor condition. A perturbed right-hand side, not an absolute
  gap.
- Integer counterparts: Cslovjecsek et al. (SODA 2021; per [S]) — at most
  `r` non-integral blocks and proximity `(r Delta G)^{O(r)}`; Murota–Tamura
  (DAM 2024).

Relation: Theorem 2.2 and Corollary 2.3 reduce to these when the tree has
no separators. With separators, the unit is the fractional component, and
Example 2.4 shows that no bound in terms of per-bag nonconvexity holds.
[S, Section 3A] showed the dual phenomenon for many rows (gap governed by a
weighted matching number of the block–row incidence graph).

**Lagrangian decomposition with coupling constraints in (MI)NLP.**

- Dür–Horst (JOTA 1997), abstract: the Lagrangian gap vanishes under
  partitioning; partitioning only nonconvex variables suffices for partly
  convex problems.
- Nowak (2005, LaGO; DECOGO 2018), per the repository's audit: block
  splitting with copy constraints, Lagrangian bounds, one full-space tree.
- Karuppiah–Grossmann (JOGO 2008), Cao–Zavala (JOGO 2019), Kannan (thesis
  2018, Chapter 6: convergence orders of reduced-space schemes),
  Li–Grossmann (JOGO 2019), Robertson–Cheng–Scott (JOGO 2025), MUSE-BB
  (JOGO 2025): two-stage decomposition B&B, convergence without complexity
  bounds (per the repository's audit).
- Cifuentes–Dey–Xu (IPCO 2025), per [S]: redundant constraints make
  decomposable Lagrangian duals exact, including over tree decompositions of
  sparse MIPs.
- Vujanic et al. (Automatica 2016), per [S]: primal recovery with tightened
  coupling rows; a row-local rank refinement.

**Nested decomposition.** Zhang–Sun (Math. Prog. 2022), per the audit:
`T (1 + 2 L D T/eps)^{d_s}` iterations for multistage nonconvex problems
with state dimension `d_s`, and an algorithm-specific lower bound
`(D L T/(4 eps))^{d_s}`. A coupling row over all stages (a horizon budget)
adds one state per row, so their bound becomes
`T (1 + 2 L D T/eps)^{d_s + k}`. Theorem 4.5 is the instance-dependent
counterpart under quadratic growth: on a path of `T` stages it replaces
`eps^{-(d_s + k)}` by `log^2(1/eps)` and keeps a factor `(C T)^k` from
drift accumulation. Both bounds are polynomial in `T` with degree growing
with `k`.

**Concave knapsacks and B&B lower bounds on DP-easy instances.**

- Vavasis (Math. Prog. 1992), local: an exact DP for separable concave
  quadratic knapsacks whose value functions are continuous piecewise
  concave quadratics (Theorem 4) — the DP of Theorem 5.1(c) — and, for
  indefinite QPs over polytopes, `O([n(n+1)/sqrt(eps)]^t)` convex QPs with
  `t` the number of negative eigenvalues (Theorem 2, relative accuracy).
  The latter is the closest prior result to "the exponent counts bad
  directions" (Propositions 4.6 and 5.2).
- Sahni (1974), NP-hardness of the concave quadratic knapsack;
  Moré–Vavasis (1991), its local minimizers have at most one fractional
  coordinate (both from memory, per the review).
- Jeroslow (Math. Prog. 1974), from memory: LP-based B&B needs
  `2^{(n+1)/2}` nodes on `max x_1` s.t. `2 sum x_i = n`; in fact every
  variable-fixing tree has exactly `C(n+1, (n+1)/2)` leaves (Theorem 5.1,
  remarks).
- Dey–Shah (ORL 2022), local: every general split-disjunction B&B tree for
  a lot-sizing family has at least `2^{n/2 - 1}` leaves, while a DP solves
  it in `O(n log n)`; Dey–Dubey–Molinaro (Math. Prog. 2023), local: lower
  bounds for general B&B trees. Theorem 5.1 is the spatial, Lagrangian-bound
  counterpart of this message.
- Handler–Zang (1980), from memory, per the review: the Lagrangian dual of
  a resource-constrained shortest path mixes at most `k + 1` paths.
- Papadimitriou (1981) pseudo-polynomial ILP with few rows, from memory.

**Other ingredients.** Vorob'ev (1962) gluing; the local polytope on trees
(graphical models); Knop–Pilipczuk–
Wrochna (STACS 2019, arXiv 1811.01296; abstract checked);
Eisenbrand–Weismantel (2018) `(m Delta)^{O(m)}` algorithms, from memory;
exact augmented Lagrangians (Hestenes 1969, Powell 1969, Rockafellar 1974)
and Finsler's lemma (1937), from memory; Bodlaender–Hagerup (SIAM J.
Comput. 1998) for balanced decompositions, from memory; low-rank nonconvex
structures (Konno–Thach–Tuy 1997), from memory, for problems whose
nonconvexity is a function of a few aggregates, as in Proposition 5.2.

**What is new here (to the extent checked).** Theorem 2.1 is classical in
substance and is not claimed.

1. *Tree Shapley–Folkman* (Theorem 2.2): at most `k` fractional
   components, and the counterexample to per-bag control (Example 2.4). The
   argument is elementary and close to classical facts about faces of the
   marginal polytope; the statement in this form and its consequence for
   tree-structured MINLP were not found.
2. *Coupling costs nothing under (LQG)* (Theorem 3.1), with second-order
   multiplier tolerance. A corollary of [D, Theorem 3.4].
3. *Partial-sum certificates* (Theorem 4.5): exact cancellation of
   first-order partial-sum drift by the slopes `-mû`, a size bound of
   `2|T| C_x^{w+1} Gamma_sigma^{k Delta_1} (J_x+1)(J_sigma+1)` with
   `Gamma_sigma = 16(1+Delta)(d+1) max(1, 64 sqrt(k) nu_A cond^2)`, and the
   identification of drift accumulation as the source of the depth factor.
   No instance-dependent complexity bound for coupled tree problems was
   found.
4. *The exponent counts bad directions* (Proposition 4.6): only
   `p <= k` row combinations need lifting. The pieces (inertia, Finsler,
   maximal positive subspaces) are classical, and Vavasis (1992,
   Theorem 2) already has complexity exponential only in the number of
   negative eigenvalues, for indefinite QP with relative accuracy. The
   certificate-size version with lifting of `p` row combinations is
   distinct.
5. *Continuous Jeroslow bound* (Theorem 5.1(b)): the count
   `C(n+1, (n+1)/2)` is the exact tree size of Jeroslow's binary instance,
   and the DP of (c) is Vavasis's. The contribution is the transfer to
   spatial B&B with arbitrary split points and Lagrangian/envelope node
   bounds, and (d), which puts both sides in one certificate model. It
   makes precise that Shapley–Folkman controls the gap but not the
   certificate; Dey–Shah give the same message for MILP.
6. *`exp(Omega(k))` at a nondegenerate minimizer with `w = 0`*
   (Proposition 5.2): [D, Proposition 2.3]'s mechanism in aggregate
   coordinates, including Lagrangian node bounds.
7. Proposition 5.3 is known in substance (subset sum, Sahni 1974;
   Knop–Pilipczuk–Wrochna); the reduction to smooth `w = 0` MINLP is
   routine.
8. The census of coupling rows (Section 7.3) is new data.

## 9. Numerical checks and commands

All commands were run from `research-20260929/theory-coupling/` with
Python 3.13, NumPy 2.5.1 and SciPy 1.18.0 (HiGHS). They are targeted checks
of this note only; no project-wide verification was run and no CI results
were consulted. Floating-point illustrations, not certified values.

### 9.1 Jeroslow-type instance (Theorem 5.1)

`python3 jeroslow_bb.py` → `logs/jeroslow_bb.log`. Best-first spatial B&B,
exact node bound (continuous knapsack over chords, equal to the Lagrangian
dual on the box), incumbent `c/4`, `c = 1`.

| n | lower bound `C(n+1,(n+1)/2)` | leaves, bisection | leaves, split at relaxation point | same two rules with FBBT on the row |
|---|---|---|---|---|
| 3 | 6 | 6 | 6 | 6, 6 |
| 5 | 20 | 20 | 20 | 20, 20 |
| 7 | 70 | 70 | 70 | 70, 70 |
| 9 | 252 | 252 | 252 | 252, 252 |
| 11 | 924 | 924 | 924 | 924, 924 |
| 13 | 3432 | 3432 | 3432 | 3432, 3432 |

Identical for `eps = 0.05` and `0.01`. FBBT (propagation of the row to a
fixpoint at every child node) is outside the model of Theorem 5.1(b) and
changed no count.

`python3 jn_lifted_cert.py` → `logs/jn_lifted_cert.log` (Theorem 5.1(d),
exact rational arithmetic, independent of the review's code):

| n | cells of side 1: `l_r`, size | cells of side 1/2: `l_r`, size | `3n^2 - 3n + 2` | `C(n+1,(n+1)/2)` |
|---|---|---|---|---|
| 5 | 0, 21 | 1/4, 62 | 62 | 20 |
| 9 | 0, 73 | 1/4, 218 | 218 | 252 |
| 13 | 0, 157 | 1/4, 470 | 470 | 3432 |
| 25 | 0, 601 | 1/4, 1802 | 1802 | 10400600 |
| 41 | 0, 1641 | 1/4, 4922 | 4922 | 538257874440 |

### 9.2 Penalty chain (Example 2.4)

`python3 penalty_chain.py` → `logs/penalty_chain.log`. `c = 1`.

| n | M | OPT (multistart SLSQP) | `c n/4` | `max_mu L(mu)` (grid DP) |
|---|---|---|---|---|
| 6 | 1 | 0.750000 | 1.5 | 0 |
| 6 | 10 | 1.500000 | 1.5 | 0 |
| 6 | 30 = `n(n-1)` | 1.500000 | 1.5 | 0 |
| 10 | 1 | 0.750000 | 2.5 | 0 |
| 10 | 10 | 2.472840 | 2.5 | 0 |
| 10 | 90 | 2.500000 | 2.5 | 0 |
| 16 | 1 | 0.750000 | 4.0 | 0 |
| 16 | 10 | 2.472840 | 4.0 | 0 |
| 16 | 240 | 4.000000 | 4.0 | 0 |

The gap equals `c n/4` once `M >= c n(n-1)` (proved) and saturates at a
wall cost that grows with `M` otherwise (observed).

### 9.3 Tree Shapley–Folkman on finite domains (Theorem 2.2)

`python3 tree_sf_lp.py` → `logs/tree_sf_lp.log`. Path problems with bags
`{x_i, x_{i+1}}`, grids of `d` values, random normal bag costs (plus a
penalty `20 (x_i - x_{i+1})^2` in the "stiff" rows), `k` random dense rows;
"mid": `b` is the image of the midpoint of two random configurations;
"feas": `b` is the image of one configuration. LP over locally consistent
bag marginals with the `k` moment rows, dual simplex (basic solution); 30
trials per row; OPT by enumeration.

| mode | n | d | k | penalty | max #components | trials with > k | mean largest component (bags, of n-1) | mean OPT - D (finite cases) |
|---|---|---|---|---|---|---|---|---|
| mid | 8 | 3 | 1 | 0 | 1 | 0 | 2.60 | 5.95 (1 case) |
| mid | 8 | 3 | 2 | 0 | 2 | 0 | 4.20 | 7.53 (1) |
| mid | 8 | 3 | 3 | 0 | 3 | 0 | 4.73 | – |
| mid | 7 | 4 | 2 | 0 | 2 | 0 | 3.93 | – |
| mid | 8 | 3 | 1 | 20 | 1 | 0 | 5.43 | – |
| mid | 8 | 3 | 2 | 20 | 2 | 0 | 6.03 | – |
| feas | 8 | 3 | 1 | 0 | 1 | 0 | 2.63 | 7.40 (30) |
| feas | 8 | 3 | 2 | 0 | 2 | 0 | 3.47 | 6.17 (30) |
| feas | 8 | 3 | 3 | 0 | 3 | 0 | 3.80 | 4.54 (30) |
| feas | 7 | 4 | 2 | 0 | 2 | 0 | 3.83 | 7.33 (30) |
| feas | 8 | 3 | 1 | 20 | 1 | 0 | 4.83 | 39.97 (30) |
| feas | 8 | 3 | 2 | 20 | 2 | 0 | 5.27 | 38.04 (30) |

The component bound holds in all 360 trials and is attained. The gaps are
large because the domains are finite grids: with generic real rows the only
integer-feasible point is the one that defined `b`, so these are
exact-feasibility gaps, which Corollary 2.3 (box domains, mean point) does
not cover. The stiff penalty makes components longer, as Example 2.4
predicts.

### 9.4 Census of coupling rows (Section 7.3)

`python3 census_k.py logs/census_k.jsonl 16`,
`python3 census_k2.py logs/census_k2.jsonl 14`,
`python3 census_k3.py logs/census_k3.jsonl 16`, `python3 census_k_rows.py`,
`python3 census_k_analyze.py` → `logs/census_k_summary.log`. Every line of
the summary log is printed by `census_k_analyze.py` (in the first version
three lines had been appended by an unsaved inline script; the review
flagged this).

| Command | Log | Result |
|---|---|---|
| `python3 jeroslow_bb.py` | `logs/jeroslow_bb.log` | leaves equal `C(n+1,(n+1)/2)` for `n <= 13`, with and without FBBT |
| `python3 jn_lifted_cert.py` | `logs/jn_lifted_cert.log` | exact `l_r = c/4` with `3n^2 - 3n + 2` boxes (side 1/2); `l_r = 0` with side 1 |
| `python3 penalty_chain.py` | `logs/penalty_chain.log` | `OPT = c n/4`, `D = 0` for `M = c n(n-1)` |
| `python3 tree_sf_lp.py` | `logs/tree_sf_lp.log` | at most `k` fractional components in 360/360 trials |
| `python3 census_k.py logs/census_k.jsonl 16` | `logs/census_k.jsonl` | densest-first heuristic, see Section 7.3 |
| `python3 census_k2.py logs/census_k2.jsonl 14` | `logs/census_k2.jsonl` | bag-targeted heuristic, see Section 7.3 |
| `python3 census_k3.py logs/census_k3.jsonl 16` | `logs/census_k3.jsonl` | reruns with only linear (equality) rows eligible, 99 instances |
| `python3 census_k_rows.py` | `logs/census_k_rows.log` | row classes of the bag rule's selection: 13 linear-equality, 7 with inequalities, 5 with nonlinear rows (of 25); shares at `k <= 8` by classification: 16.3% (linear equality), 17.2% (linear) |
| `python3 census_k_analyze.py` | `logs/census_k_summary.log` | tables of Section 7.3, stop reasons, restricted shares |

Not computed: a general certificate of Section 4 under quadratic growth
(only the exact `J_n` certificate of Theorem 5.1(d)), and any check of the
drift-accumulation mechanism.

## 10. Limitations and open problems

1. **Review.** One independent review
   ([`../reviews/coupling-review.md`](../reviews/coupling-review.md)) found
   no false claim; its fixes are made (Section 11) but not rechecked. The
   numerical checks are floating-point illustrations, except the exact
   rational computation of Theorem 5.1(d).
2. **Theorem 4.5 reuses [D, Theorem 3.4].** Its proof cites steps 1–6 of
   [D, Theorem 3.4] up to the final use of (QG) with a changed parameter
   rather than repeating them. The review checked that no step before that
   sentence uses (QG) or the optimality of `x*`. No certificate of
   Section 4 was computed under quadratic growth (only the exact `J_n`
   certificate), so neither the size bound nor the drift mechanism has been
   observed numerically.
3. **Depth factor.** Whether `d^{Omega(k)}` partial-sum cells are necessary
   (a "drift-splitting" analogue of [D, Proposition 2.4]) is open. On paths
   Theorem 4.5 gives `n^{O(k)}`, not `poly(n) exp(O(k))`. Rebalancing to
   logarithmic depth increases `k_T`, which hurts the `x`-part of [D].
4. **Knowledge of `x*`.** As in [D], the certificates are centred at a point
   within `h` of `x*`; an adaptive algorithm with a size guarantee is open.
   Proposition 4.6(c) also needs a global hypothesis (partial LQG) that no
   algorithm here verifies.
5. **Conditioning.** The bounds depend on `(1 + M_F/c_g)^2`, the Hoffman
   constant `kappa` (through `nu_A`), and `c_g` is a global constant that a
   second near-optimal local minimizer makes tiny ([D, Section 6, item 4]).
   Proposition 5.3 shows only that algorithms need some dependence beyond
   `poly(n, s0) 2^{O(k)}` (on `k log k`, on `(n + s0)^{Omega(k)}`, or on
   conditioning); whether conditioning itself must enter, for algorithms or
   for certificates, is open.
6. **Integer and nonconvex domains.** Theorem 2.2 holds for any compact bag
   domains, but Corollary 2.3 needs box domains (the mean point must be
   feasible). For integer blocks with exact feasibility, gaps can be global
   (the parity chain of [S]; the "feas" rows of Section 9.3).
7. **Lower bounds.** Theorem 5.1 covers B&B without bound tightening
   (FBBT changed no count in the computations, but the proof does not
   extend);
   Proposition 5.2 covers single trees and lifted certificates in which one
   bag carries all nonconvex aggregate terms. A lower bound on partial-sum
   cells for general lifted decompositions is open. The transfer of the
   face-exact single-tree bound to problems with rows (Section 1) was not
   checked.
8. **Census.** Widths are min-degree upper bounds; the two row-selection
   heuristics are greedy and may overestimate `k`; rows that become dense only
   after eliminating defined variables (lnts) are not detected; the
   objective-defining rule is syntactic.
9. **Inequality rows** are covered in Section 2 (active rows count); Section
   4 assumes equalities, which slack variables in one bag provide.

Open questions, in the order I would attack them:

- A lower bound for partial-sum certificates on a path with one dense row
  and a Lagrangian gap: is `n^{Omega(1)}` per shell level necessary?
- An adaptive Route L/P hybrid: compute the inertia `p` at a local
  solution, lift `p` row combinations, and certify; with a complexity bound
  that does not assume knowledge of `x*`.
- A quantitative tree Shapley–Folkman bound that uses separator stiffness
  (Example 2.4 suggests a wall-energy quantity) instead of whole-component
  nonconvexity.
- Coupling rows in the certification campaign: which open MINLPLib
  instances in the "small `w`, small `k`" class of Section 7.3 have a
  Lagrangian gap, and whether lifting `p` combinations closes it.

## 11. Revision after review

The review ([`../reviews/coupling-review.md`](../reviews/coupling-review.md),
checks in `../reviews/coupling-review-checks/`) found no false claim. Changes,
each checked here as stated:

1. **Proposition 1.1 (F1).** The side remark "unchanged for convex costs on
   the aggregates" was false; replaced by the determinant factor
   `det(I + H^{-1/2} A^T ∇²g A H^{-1/2})^{-1/2}` (checked from the
   Corollary 2.1 formula, whose bound contains `(det H)^{-1/2}`). Noted that
   the proposition is close to trivial; Summary item 1 says "cost-free".
2. **Theorem 2.1** is called classical in substance (Aubin–Ekeland;
   Udell–Boyd, Appendix A; Handler–Zang for constrained shortest paths).
   Theorem 2.2 now says "if `K` is nonempty". Proposition 2.6(c) no longer
   assumes attainment of the dual optimum (proved: `b` is interior to
   `A X0`, so `L` is coercive).
3. **Theorems 3.1 and 4.5 (F2–F5).** They cite steps 1–6 of [D, Theorem 3.4]
   up to the final use of (QG), where the error bound is assembled; "lnts is
   this case" became "consistent with this case", with the reasons; the
   centre condition `sigmâ_t in Sigma_t` was added; the one-line size forms
   now carry `Gamma_sigma^{k Delta_1}` with
   `Gamma_sigma = 16(1+Delta)(d+1) max(1, 64 sqrt(k) nu_A (1 + M_F/c_g)^2)`
   (derived from (T4): `(1+Delta)d + Delta <= (1+Delta)(d+1)` and
   `rho ||A|| alpha_A/c_g <= nu_A (1 + M_F/c_g)^2`, plus a factor 2 for
   rounding to a power of 1/2). Section 4.2 now allows the root to impose
   the rows exactly.
4. **Theorem 5.1 (F6–F8).** Added "no bound tightening" to the Summary and
   Section 4.5, with the FBBT evidence (rerun here: `jeroslow_bb.py` now
   applies FBBT on the row at every node and gets the same counts for
   `n <= 13`; the review's exact minima over small split grids also agree).
   Added prior art: the count is the exact tree size of Jeroslow's binary
   instance (lattice-path identity `2 sum_{j<=m} C(m+j, j) = C(n+1, (n+1)/2)`,
   checked), the DP of (c) is Vavasis (1992), NP-hardness is Sahni (1974),
   and Dey–Shah (2022) and Dey–Dubey–Molinaro (2023) are the MILP analogues.
   New part (d): an exact lifted certificate with `3n^2 - 3n + 2` boxes,
   proved by subadditivity of `dist(·, Z)` and checked in exact arithmetic
   (`jn_lifted_cert.py`; sizes 62, 218, 470, 1,802, 4,922 for
   `n = 5, 9, 13, 25, 41`, matching the review's 1,802 at `n = 25`).
5. **Propositions 5.2 and 5.3 (F9).** "Conditioning must enter" was
   overstated: ETH excludes `poly(n, s0) 2^{O(k)}` but allows
   `(n + s0)^{O(k)}` and `2^{O(k log k)}`-type bounds; corrected in the
   Summary, Section 5.3 and Section 10, with the time-versus-certificate
   caveat in the Summary and the model of computation stated. Proposition
   5.2 now also covers envelope (Lagrangian) node bounds for `m >= 8`
   (proved from `h'' <= -(beta - 12)`; bases recomputed: 1.85–1.92 at
   `m = 8`, 2.26–2.30 at `m = 16`).
6. **Census (F10–F13).**
   - The baseline is `min(w_full, w_free)`, so casctanks moves to `k = 0`
     and the `k = 0` share is 14.8%.
   - Shares for linear rows (17.2–17.4% at `k <= 8`) and for linear
     equality rows (16.3–17.0%) were added, from new reruns with
     restricted eligibility (`census_k3.py`) and from a classification of
     the rows removed (`census_k_rows.py`, which reproduces the review's
     13 / 7 / 5).
   - The candidates are restated: 22 small-`w` instances with
     `1 <= k <= 16` linear rows, 17 open; kall_ellipsoids_tc03c is flagged
     (nonlinear width 14).
   - The "median 43.5 rows" statistic is explained by the stop reasons
     (82 reached, 121 capped at 64 rows, 77 early stops, 10 time caps).
   - Every summary-log line is now printed by `census_k_analyze.py`.
   - Section 6.1 now says that the lower bound on the number of dualized
     rows holds for true treewidth only.
7. **Smaller changes.** waterno2's horizon row is "not the bottleneck of
   the wave-2 certificate" rather than "harmless" (the +0.0005 gain was on
   waterno2_06); Example 2.4 records the review's sharper threshold
   `M ≈ c n^2/pi^2` with a derivation of the second-order value; the
   literature section cites Vavasis's negative-eigenvalue complexity as the
   closest prior result to Proposition 4.6.

Commands run for the revision (from this directory; targeted checks only,
no project-wide verification, no CI): `python3 jeroslow_bb.py`,
`python3 jn_lifted_cert.py`, `python3 census_k3.py logs/census_k3.jsonl 16`,
`python3 census_k_rows.py`, `python3 census_k_analyze.py`; and, from
`../reviews/coupling-review-checks/`, a rerun of the review's
`c1_jeroslow.py` and `c2_min_tree.py` (outputs identical to the review's
logs; not saved in the repository).

### 11.1 Root edits after the recheck (2026-09-30)

The recheck ([`../reviews/coupling-recheck.md`](../reviews/coupling-recheck.md))
found no false claim and suggested minor edits M1–M8. Each was checked
against the recheck's derivation before the text was changed. No theorem or
headline number changes.

1. **M1, M2 (Proposition 1.1).** Summary item 1 and the status table now say
   that a convex cost changes the prefactor by a factor at least
   `(1 + ||A||^2 sup||∇²g||/lambda_min(H))^{-k/2}`, polynomial in `n` for
   rows with bounded entries, instead of "changes the constant". The remark
   after the proposition says that the factor is exact when the minimizer
   stays at 0, what changes if it moves, and gives the recheck's
   `1.9/sqrt(n)` example.
2. **M3 (Proposition 2.6(c)).** `x*` is now a global minimizer of (P); the
   proof uses `F(x*) = OPT`.
3. **M4 (Section 6.2 table).** The lifted certificate is Theorem 5.1(d), not
   (c). The docstring of `jn_lifted_cert.py` still says "(c)"; scripts were
   not edited in this root pass.
4. **M5, M6.** "0.61–0.65" at `m = 4`; `alpha/lambda' >= 1.729`
   (`6.4/3.7 = 1.7297`); "exceeds for `3 <= n <= 7`"; the itemized count
   holds for `n >= 2`.
5. **M7 (Proposition 5.3).** The model of computation is now a Turing
   machine with a bit-precision evaluation oracle, as the recheck suggested;
   the status-table cell reads "does not exclude conditioning-free bounds in
   general".
6. **Not applied: M8.** The open counts 17 and 14 and the list of 17 open
   candidates are still not printed by `census_k_analyze.py`; the recheck
   reproduced them with its own code (`r1_census_recount.py`). Changing the
   script was outside this root pass.
7. **Header and citations.** The header cites the recheck; the [K] citation
   no longer says "under revision".
8. **Table rendering (closing audit, 2026-09-30).** In the status table
   (Summary) and the Section 6.2 table, the `|` characters inside code
   spans (`||A||`, `||∇²g||`, `|T|`, `|OPT|`) split the rows into extra
   cells in GitHub-flavoured Markdown. They are now escaped as `\|`. The
   text is unchanged.
