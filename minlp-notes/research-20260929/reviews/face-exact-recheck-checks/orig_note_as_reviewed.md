# Exponential lower bounds for single-tree spatial branch-and-bound with face-exact relaxations on a path

Date: 2026-09-29. Workstream "Theory B" of the
[program](../PROGRAM.md). Status: first draft, not reviewed. Proofs are
complete unless a step is marked otherwise. Computations are floating-point
illustrations, not certified counts. Scripts and logs are in this directory
(Section 11).

## Summary

**Question.** Face-exact relaxations (McCormick envelopes of bilinear terms,
per-factor convex envelopes, secants of concave univariate terms) have a gap
that vanishes on box faces. The repository's exponential lower bounds
(constrained note, Theorem 3.1) need a gap of at least `alpha q_B` at every
point, so they do not apply. Does single-tree spatial branch-and-bound still
need exponentially many leaves in `n` on a path-structured problem (treewidth
1) with a unique nondegenerate interior minimizer?

**Answer: yes.** The main results, all for every single-tree certificate
(any branching rule, split points, node order, valid incumbent, pruning by
inherited bounds, same-relaxation bound tightening):

1. **Theorem 1 (termwise McCormick).** On the path family
   `f(x) = sum_i g_i(x_i) + sum_{i<n} b_i x_i x_{i+1}` with `|b_i| = b` and
   `g_i'' <= D` near the minimizer, every certificate has at least

   ```
   (1 + 1/S)^n exp(-lambda (1 + eps/(b r^2))),   S = sqrt(1 + D/(2b)),   lambda = (1+S)/(2 S^2),
   ```

   leaves when `D/(2b) <= 1.99`. Here `r` is the radius of a cube around the
   minimizer inside the root box. For the family of PROGRAM.md (`D = 2`,
   `b = 0.8`) this is `(5/3)^n exp(-(5/9)(1 + 1.25 eps/r^2))`, that is at
   least `0.57 (5/3)^n` leaves for `eps <= 10^-4` and `r >= 1/2`. There is no
   `log(1/eps)` factor. The tolerance enters only through
   `exp(-lambda eps/(b r^2))`, so no smallness condition on `eps` is needed. The bound
   holds for every relaxation whose gap is at least the termwise McCormick gap:
   exact, secant or outer-approximated univariate terms, inherited cuts. It
   does not use uniqueness, nondegeneracy or nonconvexity of `f`: it also holds
   for the convex member `kappa = 0` of the family.
2. **Theorem 2 (per-factor convex envelopes).** With the factorization
   `f_i = g_i(x_i) + b x_i x_{i+1}`, the per-factor envelope still forces
   `c 1.20^n` leaves (base evaluated numerically from a one-dimensional
   maximization).
3. **Mechanism.** The rigorous mechanism is a product-form volume argument
   (candidate (b) of the task, made precise). At the center of `C ∩ R`, where
   `R` is a cube around the minimizer, the McCormick gap is at least
   `b sum_i w_i w_{i+1}/4`. The center lies within `r - w_i/2` of `x*` in
   coordinate `i`, so `m` there is at most a quadratic in these numbers.
   Validity couples the two, and the coupling forces `vol(C ∩ R) <= 0.6^n vol(R)` up to a constant
   (Lemma 2.1, Theorem 1). Candidate (a) (vertex covers at `x*`) is true as a
   statement about boxes that contain `x*`, but it gives no lower bound by
   itself, because a cube of half-side `sqrt(eps/(b(n-1)))` centered at `x*`
   is valid (Proposition 5.1). The correct `eps -> 0` picture is
   Proposition 5.2: of the `2^n` orthant boxes at `x*`, exactly two are
   exactly valid, and every orthant with a sign change along the path costs
   `b^2 W^2/(4D)` at scale `W`. Candidate (c) (the nonconvex outer region) is
   not needed. The bound holds for arbitrarily small cubes around `x*`. In a
   bisection run at `n = 8`, 82% of the leaves meet the cube
   `x* + [-0.3, 0.3]^n`, and `f` is convex on the larger cube
   `|x|_inf < 0.577`.
4. **A `log(1/eps)` factor** is proved only with a weak exponential base:
   `c sqrt(n) 1.072^n log(1/(n eps))`, from the matching-slice theorem of the
   face-exact note (Proposition 5.3). Whether `c^n log(1/eps)` holds with the
   base of Theorem 1 is open (Conjecture 5.4).
5. **Upper bound.** Uniform bisection uses at most
   `C^n log(n/eps)` leaves with `C ≈ 17` (`kappa = 0`) or `20`
   (`kappa = 0.1`) (Proposition 5.5). So the minimal certificate size is
   `exp(Theta(n))` at fixed `eps`, not super-exponential.
6. **Per-factor alphaBB (Section 6).** On this family the repository's
   Theorem 3.1 gives base `0.78 < 1` with the exact per-factor `alpha`
   (`kappa = 0`) and `1.03` with the root-box `alpha` (`kappa = 0.1`). So it
   gives no, or almost no, exponential growth here. The PROGRAM's statement
   that it "already gives an `exp(Omega(n))` single-tree lower bound on chains"
   needs its condition `alpha > ~0.29 lambda_geo(H)` (in the convention
   `m ≈ y'Hy/2`), which this family does not meet. The center-volume argument
   gives `1.33^n` and `1.52^n` for these two values of `alpha`. It gives
   exponential growth for every `alpha > 0`.
7. **Computations.** A toy branch-and-bound with exact node relaxations grows
   by 2.7–3.1 per added variable under every rule tried, except one rule that
   stalls (Section 7.3). Its count behaves like
   `A_n + B_n log(1/eps)` with both terms exponential in `n`. SCIP 10 grows by
   about 2.1–2.3 per variable. Its counts are identical for absolute gaps
   `10^-4`, `10^-5` and `10^-6`. The likely reason is that SCIP's incumbents
   lie a few `10^-6` below `f*` (feasibility tolerance), so its effective
   tolerance is about `10^-6` whatever gap is requested. Exact minimal
   grid-restricted certificates for `n = 2, 3, 4` have 2.5–4.5 times fewer
   leaves than bisection trees (4, 10, 32 leaves at `eps = 10^-2`).
   All counts are above Theorem 1's bound, which is below them by factors of
   about 10–2000.

Also found: the PROGRAM's claim that the convex variant (`kappa = 0`) is solved
at the root holds only for `n <= 4`. SCIP needs 21–30 nodes at `n = 8`,
1271–5619 at `n = 12`, and exceeds 60 s at `n = 16` (Section 7.4).

What remains open: the right base (the data suggest about 2 per variable,
Conjecture 5.4), a `log(1/eps)` factor with a good base, relaxations outside
the factorable class (RLT, SDP, aggregated convexity detection), and
objective-cutoff propagation.

## 1. Setting

### 1.1 The path family

- Root box `X0 = prod_i [L_i, U_i]`, `n >= 2`.
- Objective `f(x) = sum_{i=1}^n g_i(x_i) + sum_{i=1}^{n-1} b_i x_i x_{i+1}`,
  with `g_i` continuous and `|b_i| = b > 0` for all `i`. The signs of the
  `b_i` are arbitrary. The interaction graph is the path `1 - 2 - ... - n`.
- `f* = min_{X0} f`, `x*` a global minimizer, `m = f - f*`.
- For a box `C = prod [l_i, u_i]` and `y in C`: `d_i^C(y) = min(y_i - l_i, u_i - y_i)`.
- **(Q_D)** on the cube `R = x* + [-r, r]^n ⊆ X0`:
  `m(x* + y) <= (D/2) |y|^2 + sum_{i<n} b_i y_i y_{i+1}` for all `y in [-r, r]^n`.

  Sufficient condition: `x*` is interior and each `g_i` is `C^2` with
  `g_i'' <= D` on `[x*_i - r, x*_i + r]`. Proof: `grad f(x*) = 0`, the
  bilinear part equals its second-order Taylor expansion, and
  `g_i(x*_i + t) - g_i(x*_i) - g_i'(x*_i) t <= D t^2/2`.

**The explicit family.** `g_i(t) = t^2 - kappa t^4 + c_i t`, `X0 = [-1,1]^n`,
`b_i = b`. PROGRAM.md uses `kappa = 0.1`, `b = 0.8`, and `c = 0` or
`c ~ U(-0.3, 0.3)` (seeds 0 and 1). Here `g_i'' = 2 - 12 kappa t^2 <= 2`, so
`D = 2`.

**Lemma 1.1 (the family with `c = 0`).** Let `kappa in [0, 1/6]` and
`kappa + b < 1`.

- (a) `m(x) = f(x) >= (1 - kappa - b) |x|^2` on `X0`. So `x* = 0` is the
  unique global minimizer, `f* = 0`, and the Hessian `2I + bA` (`A` the path
  adjacency matrix) has smallest eigenvalue `2 - 2b cos(pi/(n+1)) > 0`.
- (b) (Q_2) holds with `r = 1`.
- (c) Each `g_i` is convex on `[-1, 1]`. `f` is convex on the cube
  `|x|_inf < sqrt((1-b)/(6 kappa))` (0.577 for the PROGRAM values) and, when
  `b > 1 - 6 kappa`, nonconvex on `X0` for all `n` with
  `cos(pi/(n+1)) > (1 - 6 kappa)/b` (all `n >= 3` for the PROGRAM values).

*Proof.* (a) `x_i^2 - kappa x_i^4 >= (1 - kappa) x_i^2` on `[-1,1]`, and
`b |sum x_i x_{i+1}| <= (b/2) sum (x_i^2 + x_{i+1}^2) <= b |x|^2`. The
eigenvalues of `2I + bA` are `2 + 2b cos(k pi/(n+1))`. (b) is the sufficient
condition above. (c) The Hessian is `diag(2 - 12 kappa x_i^2) + bA`. It is
positive definite when `2 - 12 kappa x_i^2 > 2b` for all `i`, and at
`x = (1, ..., 1)` its smallest eigenvalue is
`2 - 12 kappa - 2b cos(pi/(n+1))`. □

For `c != 0` we compute `x*` numerically. For the PROGRAM seeds it is
interior with `|x*|_inf <= 0.47` for `n <= 10`, so (Q_2) holds with
`r = 1 - |x*|_inf >= 0.53`.

### 1.2 Relaxations and gap hypotheses

A node relaxation on a box `C ⊆ X0` is a convex `f_C <= f` on `C`. Its bound is
`LB(C) = min_C f_C`, and its gap is `Gamma_C = f - f_C >= 0`.

- **(M_b)** For every box `C` and `y in C`:
  `Gamma_C(y) >= b sum_{i<n} d_i^C(y) d_{i+1}^C(y)`.

  This holds for the termwise relaxation "McCormick envelope of each
  `b_i x_i x_{i+1}` plus any valid convex underestimator of each `g_i`". The
  univariate part may be exact (if convex), a secant of a concave part, an
  alphaBB term or outer-approximation cuts. The gap is the sum of the
  univariate gaps (`>= 0`) and the McCormick gaps, and the McCormick gap of
  `b_i x_i x_{i+1}` is at least `|b_i| d_i d_{i+1}` (face-exact note,
  Lemma 2.1(c)). (M_b) also holds for any relaxation that lies pointwise
  below such a relaxation, for example cuts inherited from ancestors.
- **(E_D)** Per-factor convex envelopes. Factors `f_i(x_i, x_{i+1}) =
  h_i(x_i) + b_i x_i x_{i+1}` for `i < n` and `f_n = h_n(x_n)`, with
  `h_i'' <= D`. The relaxation satisfies `f_C <= sum_i vex_C f_i`, where
  `vex_C f_i` is the convex envelope of `f_i` over the projection of `C`.
  This is the strongest factorable relaxation for this factorization.
- **(A_alpha)** alphaBB type: `Gamma_C(y) >= sum_i alpha_i (y_i - l_i)(u_i - y_i)`.

### 1.3 Certificates

**Definition.** A finite family `P` of boxes is a *certified cover* of a set
`R ⊆ X0` at tolerance `eps >= 0` if it covers `R` and every `C in P` has a
*certifying box* `A ⊇ C` with `f_A(y) >= f* - eps` for all `y in C`.
`N_cert(eps)` is the least size of a certified cover of `X0`.

**Lemma 1.2.** Consider any branch-and-bound run that terminates at tolerance
`eps`. It may use any axis-parallel splits, any node order, any incumbents
`UBD >= f*`, pruning by the node's own or an inherited bound, and rounds of
same-relaxation bound tightening (OBBT or reduced-cost tightening computed
from `f_B` with cutoff `UBD` or `UBD - eps`). Record children, not the parent,
when a parent's bound is the minimum of its children's bounds (strong
branching). Then the leaves, together with the per-round frame pieces of the
tightening rounds, form a certified cover of `X0`. Hence the number of leaves
plus `2n` times the number of tightening rounds is at least `N_cert(eps)`.

*Proof.* This is Lemma 2.1 of the constrained note and Lemma 1.2 of the
face-exact note, restated. A leaf `C` pruned by `LB(A) >= UBD - eps`, with
`A = C` or an ancestor, has `f_A >= LB(A) >= f* - eps` on `A ⊇ C`. A piece
`S` removed from `B_k` in one round consists of points `y` with
`f_{B_k}(y) > UBD - eps >= f* - eps`, and `S ⊆ B_k`. There are no constraints,
so no box is pruned as infeasible. □

If `P` is certified and `A` certifies `C`, then for `y in C`,
`Gamma_A(y) = f(y) - f_A(y) <= m(y) + eps`. Since `C ⊆ A` implies
`d^A >= d^C`, hypothesis (M_b) gives

```
(V)   b sum_{i<n} d_i^C(y) d_{i+1}^C(y) <= m(y) + eps     for every C in P and y in C.
```

Not covered: objective-cutoff propagation (interval FBBT of `f <= UBD`),
cutting planes stronger than the envelopes (RLT, SDP), branching on lifted
variables, relaxations of the aggregated sum `sum_i f_i` (convexity detection
on the whole function, alphaBB with a box-dependent `alpha` of the whole
function), and incumbents accepted within a feasibility tolerance (then `f*`
means the optimum of the tolerance-relaxed problem).

## 2. The center-volume lemma

**Lemma 2.1.** Let `R = x* + [-r, r]^n ⊆ X0` and let `P` be a certified cover
of `R`. Suppose that:

- for every box `A` and `y in A`, `Gamma_A(y) >= L(d^A(y))`, where
  `L : [0, inf)^n -> R` is nondecreasing in each argument;
- `m(x* + y) <= U(|y_1|, ..., |y_n|)` for `y in [-r, r]^n`, where `U` is
  nondecreasing in each argument.

Say that `s in [0,1]^n` is *admissible* if `L(r(1 - s)) <= U(r s) + eps`, and
let `nu = sup {prod_i (1 - s_i) : s admissible}`. Then every `C in P`
satisfies `vol(C ∩ R) <= nu vol(R)`, and hence `|P| >= 1/nu`.

*Proof.*
1. Let `C in P` with `vol(C ∩ R) > 0`, and write
   `C ∩ R = prod_i [z_i - h_i, z_i + h_i]`. Put `s_i = 1 - h_i/r in [0, 1)`.
2. The center `z` lies in `C`, and `d_i^C(z) >= h_i = r(1 - s_i)`, because
   `C ∩ R ⊆ C`.
3. Since `C ∩ R ⊆ R`, `|z_i - x*_i| <= r - h_i = r s_i`.
4. Let `A` certify `C`. Then
   `L(r(1-s)) <= L(d^A(z)) <= Gamma_A(z) <= m(z) + eps <= U(r s) + eps`.
   So `s` is admissible, and `vol(C ∩ R)/vol(R) = prod_i (1 - s_i) <= nu`.
5. `P` covers `R`, so `1 <= sum_{C in P} vol(C ∩ R)/vol(R) <= |P| nu`. □

**How this differs from Proposition 3.10 of the face-exact note.** That
proposition uses the same witness (the center of `C ∩ R`), but with two
weaker inputs: the gap of one edge at a time, and the uniform bound
`m <= eta = sup_R m`. Near an isolated minimizer `eta` is about
`lambda_max n r^2/2`, which is larger than every edge gap. So its bound is
`O(1)` there. Lemma 2.1 uses the gap summed over all edges and the bound on
`m` at the witness's own position. Both are needed for growth in `n`:
- the summed gap grows like `n` for boxes of fixed shape;
- a witness far from `x*`, where `m` is large, is the center of a box that
  must be narrow, because the box fits inside `R`.

## 3. Termwise McCormick: Theorem 1

Put `rho = D/(2b)`, `S = sqrt(1 + rho)`, `theta = S/(1+S)`,
`lambda = (1+S)/(2 S^2)`. Let `S_max ≈ 1.72932` be the root of
`(1+S)/(2S^2) = log(1 + 1/S)`, and `rho_max = S_max^2 - 1 ≈ 1.99055`.

**Lemma 3.1 (one-variable inequality).** If `0 < rho <= rho_max`, then for all
`s in [0, 1)`

```
log(1 - s) <= log(theta) - lambda (rho s^2 + 2 s - 1).
```

*Proof.* Let `k(s) = log(1-s) + lambda (rho s^2 + 2s)` and
`s0 = 1/(1+S)`, so `1 - s0 = theta` and `rho s0 + 1 = S`.
1. `k'(s) = -1/(1-s) + 2 lambda (rho s + 1)`. At `s0`,
   `k'(s0) = -(1+S)/S + 2 lambda S = 0`.
2. `rho s0^2 + 2 s0 = s0 (rho s0 + 2) = s0 (S + 1) = 1`. So
   `k(s0) = log theta + lambda`, and the claim is `k(s) <= k(s0)`.
3. `k''(s) = -1/(1-s)^2 + 2 lambda rho` is decreasing. If `2 lambda rho <= 1`,
   `k` is concave and `s0` is its maximizer. Otherwise `k` is convex on
   `[0, s1]` and concave on `[s1, 1)`, where `(1 - s1)^2 = 1/(2 lambda rho)`.
4. `k''(s0) <= 0` iff `1/theta^2 >= 2 lambda rho`. Since
   `2 lambda rho = (1+S)^2 (S-1)/S^2` and `1/theta^2 = (1+S)^2/S^2`, this holds
   iff `S <= 2`, which is true because `S <= S_max`. So `s0 >= s1`, and `s0`
   maximizes `k` on `[s1, 1)`.
5. On `[0, s1]`, `k` is convex, so its maximum there is `k(0) = 0` or
   `k(s1) <= k(s0)`. And `k(0) <= k(s0)` iff `lambda >= log(1 + 1/S)`.
6. `F(S) = (1+S)/(2S^2) - log(1 + 1/S)` has
   `F'(S) = (S^2 - 3S - 2)/(2 S^3 (S+1)) < 0` on `[1, 3.5]` and `F(1) > 0`. So
   `F >= 0` exactly on `[1, S_max]`. □

**Theorem 1.** Assume the path setting, (Q_D) on `R = x* + [-r, r]^n ⊆ X0`,
and (M_b). Let `eps'' = eps/(b r^2)`.

(a) If `rho = D/(2b) <= rho_max`, every certified cover `P` of `R` at
tolerance `eps` satisfies

```
|P| >= theta^(-n) exp(-lambda (1 + eps'')) = (1 + 1/S)^n exp(-lambda (1 + eps'')).
```

(b) For every `rho > 0` and every `mu > 0`,
`|P| >= exp(-n Psi_rho(mu) - mu (1 + eps''))`, where
`Psi_rho(mu) = sup_{s in [0,1)} [log(1-s) + mu (rho s^2 + 2s - 1)]`. In
particular `Psi_rho(mu) <= -mu` for `mu <= 1/(rho + 2)`, so
`|P| >= exp((n - 1 - eps'')/(rho + 2))` for every `rho`.

By Lemma 1.2 the bounds apply to the leaves (plus tightening pieces) of every
branch-and-bound run with such relaxations.

*Proof.*
1. Apply Lemma 2.1 with `L(d) = b sum_{i<n} d_i d_{i+1}` (hypothesis (M_b))
   and `U(t) = (D/2) sum t_i^2 + b sum_{i<n} t_i t_{i+1}`. By (Q_D),
   `m(x* + y) <= U(|y|)`, since `b_i y_i y_{i+1} <= b |y_i| |y_{i+1}|`.
2. Admissibility of `s` reads
   `b r^2 sum_{i<n} (1-s_i)(1-s_{i+1}) <= r^2 [(D/2) sum s_i^2 + b sum_{i<n} s_i s_{i+1}] + eps`.
3. Use `(1-s_i)(1-s_{i+1}) - s_i s_{i+1} = 1 - s_i - s_{i+1}` and divide by
   `b r^2`: `sum_{i<n} (1 - s_i - s_{i+1}) <= rho sum_i s_i^2 + eps''`.
4. Each index lies in at most two edges, so
   `n - 1 <= sum_i (rho s_i^2 + 2 s_i) + eps''`.
5. (a) Sum Lemma 3.1 over `i`:
   `sum_i log(1 - s_i) <= n log theta - lambda (sum_i (rho s_i^2 + 2 s_i) - n)
   <= n log theta + lambda (1 + eps'')`. So `nu <= theta^n e^(lambda(1+eps''))`.
6. (b) For `mu > 0`, adding `mu` times the nonnegative quantity
   `sum_i (rho s_i^2 + 2 s_i) + eps'' - (n - 1)` gives
   `sum_i log(1-s_i) <= n Psi_rho(mu) + mu (1 + eps'')`. For
   `mu (rho + 2) <= 1`: `log(1-s) <= -s` and `rho s^2 + 2s - 1 <= (rho+2)s - 1`,
   so the bracket is at most `-s + mu (rho+2) s - mu <= -mu`. □

**Corollary 1.3 (the PROGRAM family).** Take `g_i(t) = t^2 - kappa t^4 + c_i t`
on `[-1,1]^n` with `kappa in [0, 1/6]`, `b in [0.503, 1)`, and any relaxation
satisfying (M_b). Suppose the global minimizer `x*` is interior, and let
`r = 1 - |x*|_inf`. Then `D = 2`, `rho = 1/b <= rho_max`, and every certified
cover has at least `(1 + 1/S)^n exp(-lambda(1 + eps/(b r^2)))` members. For
`b = 0.8`: `S = 3/2`, `theta = 3/5`, `lambda = 5/9`, and

```
N_cert(eps) >= (5/3)^n exp(-(5/9)(1 + 1.25 eps/r^2)).
```

With `c = 0` and `kappa + b < 1`, `x* = 0` is the unique, nondegenerate global
minimizer and `r = 1` (Lemma 1.1). The bound is then `>= 0.574 (5/3)^n` for
`eps <= 10^-4`: 4.4 leaves at `n = 4`, 95 at `n = 10`, 2034 at `n = 16`, and
15700 at `n = 20` (`bounds.log`). The Lagrangian form (b), optimized over
`mu`, improves these by less than 1%.

**Remarks.**

- *What the proof uses.* One point per box (the center of `C ∩ R`) and an
  upper quadratic model of `m` on one cube. It does not use uniqueness,
  nondegeneracy or nonconvexity. It holds for `kappa = 0`, where `f` is a
  convex quadratic and the exponential cost is purely an artifact of the
  termwise relaxation.
- *Scale.* The bound depends on `r` only through `eps/(b r^2)`. So the cube
  `x* + [-r, r]^n` with `r = sqrt(eps/b)` already needs
  `(5/3)^n e^(-10/9) >= 0.33 (5/3)^n` boxes, while the cube of half-side
  `sqrt(eps/(b (n-1)))` is covered by one valid box (Proposition 5.1). The
  cost appears at the scale `sqrt(eps/b)` and persists at every larger scale.
- *Tolerance.* The bound stays exponential for `eps` up to a constant times
  `b r^2 n`. It is not an `eps -> 0` statement.
- *Near-optimal local minimizers.* If `x*` is only a local minimizer with
  `f(x*) <= f* + eta`, then (Q_D) holds for `m` with an extra `+ eta`, and the
  theorem holds with `eps` replaced by `eps + eta`.
- *Other graphs (sketch).* The proof uses the path only in step 4 (degree
  at most 2, `n - 1` edges). For a `Delta`-regular interaction graph with
  uniform `|b_e| = b` the same computation gives Theorem 1 with
  `rho = D/(Delta b)`.
- *Where the constant is lost.* The center is not the worst point of a box.
  Boxes grown greedily until they become invalid reach volume fractions of
  `0.55^n`–`0.65^n` (checks.py, Section 7.2), against `0.6^n e^lambda`
  allowed by the proof. Adding witnesses that move the center toward `x*`
  does not improve the base (a scratch computation found 0.61 against 0.62
  for `n = 16`). Improving it needs witnesses that exploit the sign of
  `b y_i y_{i+1}`, which the uniform model `U` ignores.

## 4. Per-factor convex envelopes: Theorem 2

**Lemma 4.1 (chord bound for a factor).** Let `phi(u, v) = h(u) + beta u v` on
a rectangle `A`, with `beta != 0`, `h in C^2` and `h'' <= D`. Let `p in A`
have distances `d_1, d_2` to the sides of `A` in `u` and `v`. Then

```
phi(p) - vex_A(phi)(p) >= psi(d_1, d_2) := max_{sigma in [0,1]} max(0, |beta| sigma d_1 d_2 - D sigma^2 d_1^2/2).
```

`psi` is nondecreasing in both arguments and `psi(t a, t c) = t^2 psi(a, c)`.

*Proof.*
1. Fix `sigma in [0,1]` and `v = (sigma d_1, -sign(beta) d_2)`. The points
   `p ± v` lie in `A`.
2. `q(lambda) = phi(p + lambda v)` has
   `q'' = h'' sigma^2 d_1^2 - 2 |beta| sigma d_1 d_2 <= -2 k0` with
   `k0 = |beta| sigma d_1 d_2 - D sigma^2 d_1^2/2`.
3. `q(lambda) + k0 lambda^2` is concave on `[-1, 1]`, so
   `q(0) >= (q(1) + q(-1))/2 + k0`.
4. `vex_A(phi)(p) <= (phi(p+v) + phi(p-v))/2 <= phi(p) - k0`.
5. Monotonicity: in terms of the displacement `sigma d_1`, the maximization
   is over `[0, d_1]`, a set that grows with `d_1`. Monotonicity in `d_2` is
   clear. □

A floating-point check on 400 random boxes and points, with the exact envelope
of `x^2 + 0.8 x y` (PSD + RLT hull, exact in two variables by
Anstreicher–Burer 2010), found `gap - psi >= 3.4e-7`. The ratio `gap/psi`
ranged over `[1.001, 70]`. The envelope gap was a median 0.54 of the McCormick
gap (`logs/checks.log`).

**Theorem 2.** Assume the path setting, (Q_D) on `R`, and (E_D) with
`|b_i| = b`. For every `sigma in [0, 1]` and `mu > 0`, every certified cover
of `R` satisfies

```
|P| >= exp(-n Psi_J(sigma, mu) - mu (b sigma + eps/r^2)),
Psi_J(sigma, mu) = sup_{s in [0,1)} [log(1-s) + mu (phi_sigma(s) - b sigma)],
phi_sigma(s) = 2 b sigma s + (b (1 - sigma) + D/2) s^2 + (D sigma^2/2) (1 - s)^2.
```

*Proof.*
1. By Lemma 4.1, `Gamma_A(y) >= sum_{i<n} psi(d_i^A(y), d_{i+1}^A(y))`, a
   nondecreasing function of `d^A`. Apply Lemma 2.1 with this `L` and the `U`
   of Theorem 1.
2. With `psi(a, c) >= b sigma a c - (D sigma^2/2) a^2` and 2-homogeneity,
   admissibility implies
   `sum_{i<n} [b sigma (1-s_i)(1-s_{i+1}) - (D sigma^2/2)(1-s_i)^2]
   <= (D/2) sum s_i^2 + b sum s_i s_{i+1} + eps/r^2`.
3. Expand `(1-s_i)(1-s_{i+1}) = 1 - s_i - s_{i+1} + s_i s_{i+1}`. Bound
   `s_i s_{i+1} <= (s_i^2 + s_{i+1}^2)/2`, and use degree at most 2. This
   gives `b sigma (n-1) <= sum_i phi_sigma(s_i) + eps/r^2`.
4. Finish with a Lagrange multiplier `mu` as in Theorem 1(b). □

For `D = 2`, `b = 0.8`, the best parameters found on a grid are
`sigma = 0.40` and `mu = 1.16`. They give `exp(-Psi_J) = 1.2021`, so
`|P| >= c 1.20^n`: 1.5 at `n = 4`, 4.5 at `n = 10`, 28.7 at `n = 20`
(`bounds.log`). The supremum over `s` is evaluated in floating point on a grid
of `4 * 10^5` points with local refinement. This evaluation, not the
inequality chain, is the only non-symbolic step.

## 5. The other candidate mechanisms

### 5.1 Vertex covers at the minimizer (candidate (a))

**Proposition 5.1.** Assume (M_b).

(a) If a certified box `C` contains `x*`, then
`K_C = {i : d_i^C(x*) <= sqrt(eps/b)}` is a vertex cover of the path. So `x*`
lies within `sqrt(eps/b)` of faces of `C` whose fixed coordinates form a
vertex cover, which has at least `floor(n/2)` elements.

(b) For the explicit family with the McCormick-plus-exact-`g` relaxation, the
cube `x* + [-s, s]^n` with `s = sqrt(eps/(b (n-1)))` is valid.

*Proof.* (a) (V) at `y = x*`, where `m = 0`, gives
`b sum d_i d_{i+1} <= eps`. So each edge has an endpoint with
`d <= sqrt(eps/b)`. (b) The McCormick gap of an edge is at most
`b w_i w_j/4 = b s^2` (face-exact Lemma 2.1(d)), so
`Gamma <= b (n-1) s^2 = eps <= m + eps`. □

So (a) is a true statement about the boxes that contain `x*`. It forces about
`2^(n/2)` such boxes only when every box near `x*` is much larger than
`sqrt(eps/b)`. Nothing forces that, by (b). As a lower-bound mechanism,
candidate (a) needs a scale-free replacement, and Theorem 1 is that
replacement (its base `5/3` exceeds `2^(1/2)`). The `eps -> 0` structure at
`x*` is also different from "vertex covers". The fixed coordinates must be
all of them, and the orthant matters:

**Proposition 5.2 (orthant boxes).** Assume the `g_i` are convex, the
relaxation is exact on them (`f_C = sum g_i + sum McCormick`), `x*` is
interior, and (Q_D) holds. Consider an orthant box with vertex `x*`,
`C = x* + prod_i sigma_i [0, W_i] ⊆ X0`, `sigma in {-1, 1}^n`. Call edge `i`
*frustrated* if `sigma_i sigma_{i+1} b_i < 0`.

(a) If no edge is frustrated, then `LB(C) = f*`, so `C` is valid for every
`eps >= 0`. For a connected path exactly two sign vectors qualify.

(b) If edge `j` is frustrated and `b <= 2D`, then
`LB(C) <= f* - b^2 W_j^2 W_{j+1}^2 / (2 D (W_j^2 + W_{j+1}^2))`. For
`W_j = W_{j+1} = W` this is `f* - b^2 W^2/(4D)`.

*Proof.* McCormick envelopes commute with translations: adding an affine
function to `b x_i x_j` adds it to the envelope. With `grad f(x*) = 0`, this
gives
`f_C(x* + y) - f* = G(y) + sum_i vex_C(b_i y_i y_{i+1})`, where
`G(y) = sum_i [g_i(x*_i + y_i) - g_i(x*_i) - g_i'(x*_i) y_i]`. `G` is
nonnegative (convexity) and at most `(D/2)|y|^2`.

- (a) Write `u_i = sigma_i y_i in [0, W_i]`. An unfrustrated term is
  `|b_i| u_i u_{i+1}`, and its McCormick underestimator from the lower bounds
  `(0, 0)` is `0`. So `f_C >= f*`, and `f_C(x*) = f*`.
- (b) Take `y` supported on `{j, j+1}` with `u_j = tau W_j` and
  `u_{j+1} = tau W_{j+1}`. The neighbouring edges have one coordinate on a
  face of `C`, where McCormick is exact, so they contribute 0.
  - The frustrated term is `-|b| u_j u_{j+1}`. Its convex envelope is
    `-|b| min(W_{j+1} u_j, W_j u_{j+1}) = -|b| tau W_j W_{j+1}`.
  - So `f_C - f* <= (D/2) tau^2 (W_j^2 + W_{j+1}^2) - |b| tau W_j W_{j+1}`.
  - Minimize over `tau`. The minimizer satisfies `tau <= |b|/(2D)`, which is
    at most 1 when `b <= 2D` (true for the family). So it is admissible.
  □

Numerically (`checks.py`, `kappa = 0`, `n = 3, 4, 6`, `W = 1, 0.5`), all
unfrustrated orthant boxes have `LB = 0` exactly, and every box with one
frustrated edge has `LB = -b^2 W^2/(4D)` (`-0.08` for `W = 1`), so (b) is
attained. More frustrated edges give lower bounds down to `-0.667`.

**Consequence.** For `eps < b^2 W^2/(4D)`, only 2 of the `2^n` orthants at
`x*` can be covered at scale `W` by one box with vertex `x*`. The others need
boxes that do not have `x*` as a vertex at that scale. Such boxes are
constrained by the concave directions `e_i - sign(b_i) e_{i+1}`, which carry
alphaBB-type chord gaps (face-exact Lemma 2.4). This is where `log(1/eps)`
terms come from. There is no finite exact certificate
(face-exact Corollary 3.5 gives at least
`(1/pi) sqrt(b/M) log(1/eps) - O(1)` leaves).

### 5.2 A `log(1/eps)` factor

**Proposition 5.3 (matching slices).** Assume (M_b) and (Q_D) on `R`. Let
`k = floor(n/2)` and `M = 2(D - b) I_k - b A_k`, where `A_k` is the path
adjacency matrix on `k` vertices, and suppose `D > 2b`. Then

```
N_cert(eps) >= (k b/pi^2)^(k/2) integral_{[-r,r]^k} (t'Mt/2 + eps)^(-k/2) dt.
```

For fixed `n` the right side grows like `log(1/eps)`. For large `k` it is
about `sqrt(k/pi) (4 e b/(pi lambda_geo))^(k/2) log(r sqrt(lambda_min(M)/(2 k eps)))`,
where `lambda_geo = (D - b) + sqrt((D-b)^2 - b^2)` is the geometric mean of
the spectrum of `M` as `k -> inf`.

*Proof.* This is Theorem 3.4 of the face-exact note, with the matching
`{1,2}, {3,4}, ...`, base point `z = x*` and directions
`v_r = e_{2r-1} - sign(b_{2r-1}) e_{2r}`.
- That theorem's proof uses only `Gamma_C >= sum over matched terms of their
  chord gaps`, so it holds under (M_b).
- On the slice, (Q_D) gives the quadratic form
  `m(x* + V t) <= (D - b)|t|^2 + b sum_r e_r t_r t_{r+1}` with signs
  `e_r = -sign(b_{2r}) sign(b_{2r-1})`. Within a pair the product is
  `-|b| t_r^2`; between pairs it is `e_r b t_r t_{r+1}`.
- A change of signs `t_r -> s_r t_r` with suitable `s_r in {-1, 1}` turns all
  `e_r` into `-1`. It preserves the cube and Lebesgue measure. So the integral
  equals the one with `t'Mt/2`. (Replacing the cross terms by
  `b |t_r t_{r+1}|` would lose this equality.)
- The asymptotic form restricts the integral to the ellipsoid
  `{t'Mt <= lambda_min(M) r^2}`, which lies in the cube, and uses
  `integral_0^U u^(k-1) (1+u^2)^(-k/2) du >= e^(-1/2) log(U/sqrt(k))`. □

For `D = 2`, `b = 0.8`: `lambda_geo = 2.094`, and the base is
`(4 e b/(pi lambda_geo))^(1/4) = 1.072` per variable. At `eps = 10^-4` the
bound is 4.0 at `n = 4`, 8.2 at `n = 10` and 20.6 at `n = 20`. At `n = 10` it
grows from 3.1 (`eps = 10^-2`) to 18.7 (`10^-8`) (`bounds.log`). So the log
factor is proved, but with a weak base.

**Conjecture 5.4.** For the PROGRAM family (`b = 0.8`, `kappa in [0, 0.1]`)
there are constants `c, c' > 0` with `N_cert(eps) >= c 2^n` and
`N_cert(eps) >= c' beta^n log(1/eps)` for some `beta > 1.072`, for all
`eps <= eps_0`.

Evidence:
- the minimal grid-restricted certificates of Section 7.6. At `eps = 10^-2`
  they have 4, 10 and 32 leaves for `n = 2, 3, 4`, at or above `2^n`. At
  `n = 2` they have 4, 8 and 10 leaves for `eps = 10^-2, 10^-4, 10^-6`;
- the exact validity of only 2 of the `2^n` orthants (Proposition 5.2);
- SCIP's base of 2.1–2.3 per variable;
- the `log(1/eps)` coefficient `B_n` of our runs, which itself grows by about
  3 per variable (Section 7.5).

*Sketch of a route to the log factor (not proved).*
1. Take two cubes `x* + [-r, r]^n` and `x* + [-r', r']^n` with `r' << r/n`.
   Suppose a box meets both in volume fractions of order `theta^n`.
2. Then `x*` must lie within about `r'` of a vertex of the box. Otherwise, at
   the center of the smaller intersection, some edge has gap of order
   `b r r'`, while `m` there is of order `n r'^2`.
3. By Proposition 5.2(b), the orthant at that vertex must be unfrustrated.
   Boxes of this kind cover at most about `2 * 2^-n` of each cube.
4. So the remaining boxes are essentially single-scale, and summing Lemma 2.1
   over dyadic scales would give about `theta'^(-n) log(1/eps)/log n`.

Making steps 2 and 4 quantitative is not done.

### 5.3 The nonconvex outer region (candidate (c))

This candidate is not needed.
- Theorem 1 holds for arbitrarily small cubes around `x*` (as long as
  `eps <~ b r^2`) and for the convex case `kappa = 0`.
- In our runs, 82% of the leaves (bisection, `n = 8`, `eps = 10^-4`) meet
  the cube `x* + [-0.3, 0.3]^n`, and 46% meet `x* + [-0.1, 0.1]^n`. `f` is
  convex on the cube `|x|_inf < 0.577` (Section 7.7).

### 5.4 Upper bound: the growth is exponential, not faster

**Proposition 5.5.** Take the explicit family with `c = 0`,
`kappa in [0, 1/6]`, `kappa + b < 1`, and the relaxation
"McCormick + exact `g_i`". Consider the uniform `2^n`-ary dyadic refinement of
`[-1,1]^n` with `UBD = f*`. Let `mu0 = 1 - kappa - b` and
`tau = b(n-1)/4`. Then it has at most

```
1 + (2^n - 1) J V_n (sqrt(tau/mu0) + sqrt(n))^n
```

leaves, where `V_n = pi^(n/2)/Gamma(n/2 + 1)` and `J` is the number of levels
`j >= 0` with `tau 4^(1-j) > eps`. (For the secant relaxation of `-kappa t^4`,
add `1.5 kappa n` to `tau`.)

*Proof.*
1. A level-`j` cube `D` has side `s = 2^(1-j)`, and
   `sup_D Gamma_D <= b (n-1) s^2/4` (face-exact Lemma 2.1(d)).
2. If `D` is split, some `y in D` has `m(y) < Gamma_D(y) - eps <= tau s^2 - eps`.
   So `tau s^2 > eps`.
3. By Lemma 1.1(a), `|y| < s sqrt(tau/mu0)`. So `D` lies in the ball of radius
   `s (sqrt(tau/mu0) + sqrt(n))`.
4. Level-`j` cubes are disjoint, so at most `V_n (sqrt(tau/mu0) + sqrt n)^n`
   of them are split.
5. Each split adds `2^n - 1` leaves. □

With `V_n <= (2 pi e/n)^(n/2)`, the per-variable factor is at most
`2 sqrt(2 pi e) (1 + sqrt(b/(4 mu0)))`. This is 16.5 for `kappa = 0`,
`b = 0.8` and 19.9 for `kappa = 0.1` (`logs/upper_bound.log`). Binary
widest-side bisection changes the count by at most a factor `2^n`
(face-exact Theorem 5.1). So
`0.57 (5/3)^n <= N_cert(10^-4) <= 20^n O(log(n/eps))`, and the true growth
(Section 7) is about `2.1^n`–`3^n` for practical rules.

## 6. Comparison with per-factor alphaBB

Per-factor alphaBB relaxes `f_i = h_i(x_i) + b x_i x_{i+1}` by
`f_i - alpha_i [a_i(x_i) + a_{i+1}(x_{i+1})]`, with
`a_i = (x_i - l_i)(u_i - x_i)` and
`alpha_i >= max(0, -lambda_min(hess f_i)/2)` on the node box. For
`h'' in [h_lo, 2]`, the exact value is `(sqrt(h''^2 + 4 b^2) - h'')/4`:
- at least `alpha_f = 0.1403` on every box (`h'' = 2`, the `kappa = 0` value);
- `0.2472` on the root box when `kappa = 0.1` (`h'' = 0.8` at `|x| = 1`).

Interior variables lie in two factors, so the gap satisfies (A_alpha) with
`alpha_i = 2 alpha_f` (and `alpha_f` at the two ends).

**Proposition 6.1 (center-volume for alphaBB-type gaps).** Under (Q_D) and
(A_alpha), for every `mu > 0`,
`|P| >= exp(-sum_i Psi_i(mu) - mu eps/r^2)`, where
`Psi_i(mu) = sup_{s in [0,1)} [log(1-s) + mu ((D/2 + b) s^2 - alpha_i (1-s)^2)]`.
For every `alpha_i >= alpha > 0` the base is larger than 1.

*Proof.* Lemma 2.1 with `L(d) = sum alpha_i d_i^2` (since `a_i >= d_i^2`) and
`U(t) = (D/2 + b) sum t_i^2` (using `b t_i t_{i+1} <= b (t_i^2 + t_{i+1}^2)/2`).
Admissibility reads `sum_i [(D/2 + b) s_i^2 - alpha_i (1-s_i)^2] + eps/r^2 >= 0`;
add `mu` times it and take the supremum in each `s_i`. For the base: put
`K = D/2 + b`. If `mu K <= 1/2` and `mu alpha_i <= 1/4`, then (using
`log(1-s) <= -s` and `s^2 <= s`) the bracket is at most
`-s/2 - mu alpha_i (1-s)^2`, whose derivative is negative, so
`Psi_i(mu) <= -mu alpha_i` and `|P| >= exp(mu (sum_i alpha_i - eps/r^2))`. □

| per-factor `alpha_f` | center-volume base (Prop. 6.1) | repository Theorem 3.1 base | Theorem 3.1 bound at `n = 10`, `eps = 10^-4` |
|---|---|---|---|
| 0.1403 (exact, `kappa = 0`) | 1.334 | 0.779 | 0.18 |
| 0.2472 (root box, `kappa = 0.1`) | 1.516 | 1.034 | 3.0 |

The Theorem 3.1 base is `sqrt(4 e alpha_eff/(pi lambda_geo(H)))` with
`alpha_eff = 2 alpha_f` and `lambda_geo(H) = 1.6` for `H = 2I + 0.8A`
(`logs/abb_bases.log`).

**Why the two relaxations behave differently.**

- *Theorem 3.1 applies to alphaBB, not to McCormick.* Its key step bounds
  `integral_C q_C^(-n/2)` by a constant independent of `C`. That constant is
  scale-free, so the bound adds up over dyadic scales and produces the
  `log(1/eps)` factor. For McCormick the per-box integral of
  `Gamma^(-n/2)` diverges on faces whose fixed coordinates form a vertex
  cover (face-exact Lemma 3.1). The unfrustrated orthant boxes show why no
  such bound can hold: they are valid at every scale at once.
- *The integral bound needs a large `alpha`.* Its exponential base exceeds 1
  only if `alpha_eff > pi lambda_geo/(4e) ≈ 0.29 lambda_geo`. This is the
  PROGRAM's "0.58 times the Hessian scale" in the convention `m ≈ gamma |y|^2`.
  With the exact per-factor `alpha` this family fails the condition. The
  PROGRAM's claim that Theorem 3.1 "already gives" exponential bounds on
  chains holds only for coarser (larger) `alpha`.
- *The center-volume argument uses only the gap at box centers.* There the
  McCormick gap `b w_i w_j/4` per edge is larger than the alphaBB gap
  `alpha_f (w_i^2 + w_j^2)/4` per factor (`b = 0.8` against
  `2 alpha_f = 0.28`). So McCormick gets the larger single-scale base
  (`5/3` against `1.33`). The `log(1/eps)` factor comes directly from
  Theorem 3.1 only for alphaBB, and there with a base above 1 only when
  `alpha` is large.
- *Numerically the smaller gap wins* (Section 7.3). With `kappa = 0`, `c = 0`
  and bisection, per-factor alphaBB needs 27,314 leaves at `n = 9` and grows
  by 2.39 per variable. McCormick needs 69,390 and grows by 2.93. So being
  exact on faces does not make McCormick cheaper here. Near an interior
  minimizer, the size of the gap at box centers matters more.

## 7. Computations

All counts are floating-point illustrations.
- *Our branch-and-bound (`bb_path.py`).* The incumbent is fixed at `f*`,
  computed by multi-start L-BFGS-B. A box is pruned iff `LB >= f* - eps`, so
  the tree does not depend on node order. Every run also checked that no
  relaxation solution had `f < f* - 10^-9`; all were "ok".
- *Relaxations.*
  - `mc`: `x^2` exact, secant of `-kappa x^4`, McCormick. A convex QP solved by
    HiGHS, with Clarabel as fallback.
  - `mcx`: `g_i` exact (Kelley cuts to violation `1e-10`) and McCormick, an LP.
  - `abb`: per-factor alphaBB with `kappa = 0`, a QP.

  For `kappa = 0`, `mc = mcx`: the counts agree, for example 962 leaves at
  `n = 5`.
- *Rules.*
  - `bisect`: widest variable, midpoint.
  - `oracle`: widest variable whose interval contains `x*_i`, split at
    `x*_i`; otherwise bisect.
  - `vw`: widest variable among those in a violated term, split at
    `0.75 * midpoint + 0.25 * relaxation point`, clamped to the middle 60%.
  - `viol`: largest summed violation, split at the relaxation point, clamped.

### 7.1 Bounds (`bounds.py`, `bounds.log`)

`eps = 10^-4`, `r = 1`, `D = 2`, `b = 0.8`. All columns are lower bounds on
the number of leaves.

| n | Thm 1 closed form | Thm 1 Lagrangian | Thm 2 (envelopes) | Prop 6.1 (alphaBB, `alpha_f = 0.14`) | repo Thm 3.1 (alphaBB) | Prop 5.3 (slice) |
|---|---|---|---|---|---|---|
| 2 | 1.59 | 1.64 | 1.10 | 1.39 | 0.85 | 2.80 |
| 4 | 4.43 | 4.50 | 1.53 | 2.38 | 0.62 | 4.05 |
| 6 | 12.3 | 12.4 | 2.18 | 4.24 | 0.42 | 5.29 |
| 8 | 34.2 | 34.5 | 3.13 | 7.54 | 0.28 | 6.66 |
| 10 | 94.9 | 95.6 | 4.50 | 13.4 | 0.18 | 8.22 |
| 12 | 264 | 265 | 6.51 | 23.9 | 0.11 | 10.0 |
| 16 | 2034 | 2043 | 13.7 | 75.5 | 0.045 | 14.5 |
| 20 | 15692 | 15748 | 28.7 | 239 | 0.018 | 20.6 |

Asymptotic bases per variable:
- Theorem 1: 1.667;
- Theorem 2: 1.202;
- Proposition 6.1: 1.334;
- Proposition 5.3: 1.072 (times `log(1/eps)`);
- repository Theorem 3.1: 0.779.

At `n = 10` Theorem 1 gives 88.5 at `eps = 0.1` and 94.9 for all
`eps <= 10^-4`.

### 7.2 Lemma checks (`checks.py`, `logs/checks.log`)

- *Center inequality.* It holds on all 190 valid boxes produced by random
  greedy growth (`kappa = 0.1` and `0`, `n = 3, 5, 8`). The largest slack
  `lhs - rhs` is `-0.085`.
- *Largest grown valid boxes.* Their volume fraction to the power `1/n` is:
  - for `kappa = 0`: 0.655 (`n = 3`), 0.595 (`n = 5`) and 0.547 (`n = 8`);
  - for `kappa = 0.1` (secant): 0.572, 0.546 and 0.533.

  These are all within what Theorem 1 allows (0.72, 0.67, 0.64) and above the
  orthant value 0.5.
- *Orthant boxes and envelope chord bound.* These match Propositions 5.2 and
  Lemma 4.1 (numbers in Sections 4 and 5.1).
- *Lemma 3.1* (`python3 checks.py lemma31`, `logs/checks_lemma31.log`).
  - On a grid of `2 * 10^6` values of `s` and 400 values of
    `rho in [0.001, 1.9905]`, the largest value of `lhs - rhs` is
    `1.3e-16`, which is rounding.
  - At `rho = 2.0` and `2.2`, just above `rho_max`, it is `+4e-4` and
    `+8e-3`, so the condition `rho <= rho_max` is needed for the closed
    form.

### 7.3 Leaf counts, `eps = 10^-4` (`summarize.py`, `logs/summary.log`)

Leaves of our branch-and-bound. The last column is the geometric-mean growth
factor per added variable over the last five available sizes.

| relaxation, rule, instance | n=2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | growth |
|---|---|---|---|---|---|---|---|---|---|---|
| `mc` bisect, `kappa=0`, `c=0` | 24 | 100 | 320 | 962 | 2778 | 7962 | 23488 | 69390 | 205714 | 2.93 |
| `mc` bisect, seed 0 | 20 | 80 | 249 | 738 | 2254 | 7121 | 21001 | 64518 | 198363 | 3.06 |
| `mc` oracle, seed 0 | 31 | 111 | 335 | 954 | 2594 | 7172 | 20279 | 57637 | 164774 | 2.82 |
| `mc` viol, seed 0 | 16 | 67 | 206 | 693 | 1940 | 8349 | 15715 | 50481 | 129962 | 2.86 |
| `mc` vw, seed 0 | 19 | 66 | 189 | 587 | 1761 | 5745 | 15727 | 46989 | | 2.99 |
| `mcx` bisect, seed 0 | 17 | 77 | 241 | 648 | 1988 | 6229 | 18032 | 54788 | | 3.03 |
| `mcx` oracle, seed 0 | 24 | 101 | 316 | 904 | 2405 | 6483 | 18012 | 49771 | | 2.72 |
| `mcx` vw, seed 0 | 16 | 61 | 182 | 499 | 1474 | 4503 | 11976 | 35908 | | 2.91 |
| `mcx` vw, seed 1 | 16 | 58 | 173 | 560 | 1711 | 4822 | 14954 | 40860 | | 2.92 |
| `mcx` vw, `c=0` | 20 | 65 | 228 | 664 | 1780 | 5064 | 13994 | 39297 | | 2.77 |
| `abb` bisect, `kappa=0`, `c=0` | 32 | 114 | 316 | 804 | 1992 | 4828 | 11532 | 27314 | 64740 | 2.39 |
| `abb` viol, `kappa=0`, `c=0` | 16 | 46 | 142 | 456 | 1338 | 3930 | 11406 | 32254 | 95198 | 2.90 |
| Theorem 1 lower bound | 1.6 | 2.7 | 4.4 | 7.4 | 12.3 | 20.5 | 34.2 | 56.9 | 94.9 | 1.67 |

"Seed 0" and "seed 1" are the PROGRAM instances with `kappa = 0.1`; the full
set of runs (all seeds and rules) is in `logs/summary.log`.

- Every rule grows by 2.7–3.1 per variable on every instance. The exception
  is per-factor alphaBB with bisection (2.39).
- The `viol` rule stalls with exact relaxations. It needs 390–448 leaves at
  `n = 3`, and at `n >= 4` it did not finish within a few minutes. With
  `kappa = 0` it needed 38,394 leaves at `n = 4` and 178,991 at `n = 5`. We
  stopped those runs by hand. The `vw` rule, which differs only in variable
  selection and split point, behaves normally.
- The `oracle` rule (splitting at `x*`) changes the count by between +55%
  (`n = 2`) and -18% (`n = 10`). Placing faces
  through `x*` does not remove the exponential growth, in line with
  Proposition 5.2: only the two unfrustrated orthants become exact.

### 7.4 SCIP (`scip_runs.py`, `logs/scip_runs.log`, `logs/scip_noprop_*.log`)

SCIP 10 through PySCIPOpt 6.2.1, one thread, the same model as
`scratch/probe3.py`. The table gives nodes, not leaves.

| n | `kappa=0.1`, `c=0` | seed 0 (PROGRAM) | seed 0, presolve and propagation off | `kappa=0`, `c=0` | `kappa=0`, seed 0 |
|---|---|---|---|---|---|
| 2 | 1 | 1 | | | |
| 3 | 7 | | | | |
| 4 | 81 | 217 | 232 | 1 | 1 |
| 5 | 411 | | | | |
| 6 | 1116 | 1055 | 1273 | | |
| 7 | 2701 | | | | |
| 8 | 6410 | 4447 | 8069 | 21 | 30 |
| 9 | 11449 | | | | |
| 10 | >26236 (300 s) | 28954 | | | |
| 12 | >87839 (300 s) | | | 5619 | 1271 |
| 16 | | | | >34478 (60 s) | >38181 (60 s) |

- *Growth.* From `n = 5` to `n = 9` on `c = 0`, SCIP grows by about 2.3 per
  variable, and by about 2.1 on seed 0 between `n = 4` and `n = 8` (2.2–2.3
  over `n = 4..10` in the PROGRAM table). The
  PROGRAM's "factor 2–3 per two added variables" understates its own table:
  the factors per two variables there are 3.1–8.4, about 2.2 per variable.
- *Tolerance.* On seed 0, SCIP's node counts are identical for absolute gaps
  `10^-4`, `10^-5` and `10^-6` (217, 1055, 4447), with or without propagation.
  They drop only at `10^-2`–`10^-3` (74 and 181 at `n = 4`). SCIP's primal
  values lie below the true `f*` by `2.3e-6` (`n = 4`) and `3.6e-6`
  (`n = 6`), because the feasibility tolerance lets `t_i` sit about `10^-6`
  below its expression. So its effective tolerance is about `10^-6` whatever
  gap is requested, and its trees close with `dual = primal`. Its counts are
  best compared with ours at `eps = 10^-6`. There SCIP uses 2.5–8 times
  fewer nodes than our best rule (`vw`: 539, 4501, 37429 nodes at
  `n = 4, 6, 8`, against 217, 1055, 4447).
- *The convex variant.* PROGRAM says `kappa = 0` "was solved at the root".
  That holds for `n = 4` only. SCIP needs 21–30 nodes at `n = 8`, 1271–5619 at
  `n = 12`, and more than 34,000 in 60 s at `n = 16`. This fits Theorem 1,
  which does not depend on convexity. SCIP's relaxation is stronger than
  termwise McCormick at small `n` (1 node at `n = 4`, against Theorem 1's
  4.4 leaves). We did not identify which component does this.

### 7.5 Dependence on `eps` (leaves)

Columns are `eps = 10^-2, 10^-3, 10^-4, 10^-5, 10^-6`.

| relaxation, rule, instance | n | `10^-2` | `10^-3` | `10^-4` | `10^-5` | `10^-6` |
|---|---|---|---|---|---|---|
| `mcx` bisect, seed 0 | 4 | 113 | 159 | 241 | 313 | 359 |
| | 6 | 875 | 1443 | 1988 | 2564 | 3130 |
| | 8 | 8290 | 13337 | 18032 | 23418 | 28024 |
| `mcx` vw, seed 0 | 4 | 86 | 136 | 182 | 231 | 270 |
| | 6 | 704 | 1121 | 1474 | 1850 | 2251 |
| | 8 | 5707 | 8966 | 11976 | 15200 | 18715 |
| `mc` bisect, `kappa=0`, `c=0` | 4 | 132 | 232 | 320 | 400 | 448 |
| | 6 | 1122 | 1954 | 2778 | 3378 | 3654 |
| | 8 | 9511 | 16534 | 23488 | 27888 | 29282 |
| `mc` viol, seed 0 | 8 | 6820 | 10623 | 15715 | 26767 | 36217 |
| SCIP nodes, seed 0 | 8 | 2831 | 4447 | 4447 | 4447 | 4447 |

- With `x*` off the dyadic grid (seed 0, exact `g`), counts grow linearly in
  `log10(1/eps)`. The slope `B_n` is about 60, 560 and 5000 per decade for
  bisection at `n = 4, 6, 8`, and 46, 390 and 3250 for `vw`. So
  `N ≈ A_n + B_n log(1/eps)`, with `B_n` growing by about 3 per variable.
- With `x* = 0` on the dyadic grid (`kappa = 0`, bisection) the slope falls at
  small `eps` (29282 against 27888 leaves at `n = 8`). Bisection splits
  exactly at `x*`, and the unfrustrated orthants become exact.
- The secant relaxation (`mc`, `kappa = 0.1`) adds refinement toward `x*` in
  every coordinate. The secant gap of `-kappa t^4` is linear near a vertex.

### 7.6 Minimal grid-restricted certificates (`grid_dp.py`, `logs/grid_dp*.log`)

Exact minimum over guillotine partitions whose split points lie on the grid
`{0, ±2^-k : 0 <= k <= K}`, for `kappa = 0`, `c = 0` and exact McCormick. This
is an upper bound on `N_cert`.

| n | `eps` | K | grid-optimal leaves | bisection leaves | `vw` leaves | Theorem 1 | Prop. 5.3 |
|---|---|---|---|---|---|---|---|
| 2 | `10^-2` | 4 | 4 | 10 | 10 | 1.58 | 1.61 |
| 2 | `10^-4` | 7 | 8 | 24 | 20 | 1.59 | 2.80 |
| 2 | `10^-6` | 10 | 10 | 32 | | 1.59 | 4.00 |
| 3 | `10^-2` | 4 | 10 | 40 | 30 | 2.64 | 1.61 |
| 3 | `10^-3` | 5 | 16 | 72 | 48 | 2.65 | 2.20 |
| 4 | `10^-2` | 3 | 32 | 132 | 102 | 4.40 | 1.98 |

For `n = 2`, `eps = 10^-4` the optimal certificate has 8 leaves:
- two slabs `|x_1| >= 1/4` that span all of `x_2`;
- four boxes with `1/64 <= |x_1| <= 1/4`, split in `x_2` at `±1/16`;
- two thin boxes `|x_1| <= 1/64`, split at `x_2 = 0`.

So it is not orthant-based. It is multi-scale in the coordinate `x_1`.

### 7.7 Where the leaves are (`analyze_leaves.py`, `logs/leaves_*.log`)

`mcx`, bisection, `kappa = 0.1`, `c = 0`. Leaves counted by sup-distance from
`x* = 0`:

| run | `<0.01` | `[0.01,0.03)` | `[0.03,0.1)` | `[0.1,0.3)` | `[0.3,1)` | total |
|---|---|---|---|---|---|---|
| `n = 6`, `eps = 10^-4` | 86 | 264 | 918 | 1014 | 512 | 2794 |
| `n = 8`, `eps = 10^-4` | 616 | 2488 | 7848 | 8472 | 4394 | 23818 |
| `n = 6`, `eps = 10^-6` | 1450 | 504 | 1010 | 1016 | 512 | 4492 |

- Leaf sizes range from below 0.01 to the full width.
- The largest leaf has volume fraction exactly `2^-n` (an orthant-type box).
  Theorem 1 allows `0.0293` at `n = 8`.
- Going from `10^-4` to `10^-6` adds 1698 leaves at `n = 6`, 1604 of them
  within sup-distance 0.03 of `x*`.

## 8. Which mechanism explains the SCIP data

- **Growth in `n`: the product-volume mechanism near `x*` (Theorem 1).**
  - It is proved, and it does not depend on `eps`.
  - It applies to every relaxation satisfying (M_b). SCIP's node relaxation
    of this model (cuts for `x^2`, a secant for `-0.1 x^4`, McCormick for the
    products) should satisfy (M_b), but we did not verify SCIP's
    implementation.
  - SCIP also uses components outside the model: propagation with the
    objective cutoff, restarts, and whatever produces its 1-node root solve
    for `kappa = 0`, `n = 4`. So Theorem 1 is not a proof about SCIP's runs.
    It explains the trend, including the growth of the convex variant
    (Section 7.4).
- **The observed rates are higher than the proved one.** SCIP shows about
  2.1–2.3 per variable and our rules 2.7–3.1, against 5/3 proved. We attribute
  the difference to the loss in the proof (one witness per box, Remark in
  Section 3), not to a second mechanism, but this is not proved.
  Proposition 5.2 and the grid optima (Section 7.6) suggest a true base of
  about 2 or more.
- **Dependence on `eps`.** At `eps` from `10^-2` to `10^-6`, `log(1/eps)`
  terms with exponential coefficients (Section 7.5) are visible in our runs.
  They are consistent with the frustrated-orthant structure (Proposition 5.2)
  and with Conjecture 5.4. SCIP's constant counts carry no information on
  them, because its effective tolerance is fixed at about `10^-6`.
- **Neither vertex covers (a) nor the outer region (c) drive the counts**
  (Sections 5.1 and 5.3).

## 9. Status

| Item | Content | Status |
|---|---|---|
| Lemma 1.1 | properties of the family (`c = 0`) | proved |
| Lemma 1.2 | runs give certified covers | proved (restates repository lemmas) |
| Lemma 2.1 | center-volume lemma | proved |
| Lemma 3.1 | one-variable inequality, `rho <= 1.99055` | proved; `S_max` computed numerically; checked on a grid |
| Theorem 1 | termwise McCormick: `(1 + 1/S)^n e^(-lambda(1+eps''))`; `>= 0.57 (5/3)^n` for PROGRAM | proved |
| Theorem 1(b) | every `rho`: `exp((n-1-eps'')/(rho+2))` | proved |
| Lemma 4.1 | chord bound for per-factor envelopes | proved; checked numerically |
| Theorem 2 | per-factor envelopes: `c 1.20^n` | proved; base from a floating-point 1-D maximization |
| Proposition 5.1 | vertex covers at `x*`; a small valid cube | proved |
| Proposition 5.2 | 2 exact orthants; frustrated orthants cost `b^2 W^2/(4D)` | proved; attained numerically |
| Proposition 5.3 | `log(1/eps)` factor with base 1.072 | proved (application of face-exact Theorem 3.4); integral by quadrature |
| Conjecture 5.4 | `N_cert >= c 2^n` and `c' beta^n log(1/eps)` | conjecture, numerical evidence |
| Proposition 5.5 | bisection `<= 20^n O(log(n/eps))` | proved |
| Proposition 6.1 | per-factor alphaBB center-volume, base 1.33–1.52 | proved; base numerical |
| Other graphs | `rho = D/(Delta b)` for `Delta`-regular graphs | sketched |
| Route to `theta'^(-n) log(1/eps)` | frustrated boxes are single-scale | sketched |

## 10. Limitations and open problems

- **Model.**
  - The bounds cover factorable relaxations whose gap dominates termwise
    McCormick (Theorem 1) or the per-factor envelope (Theorem 2).
  - They do not cover RLT or SDP cuts, relaxations of aggregated sums, or
    objective-cutoff propagation. A solver that recognizes that `f` is convex
    on `|x|_inf < 0.577` could prune every box inside that cube exactly.
  - Theorem 1 still applies to the rest. Take `R = X0` (`x* = 0`) and discount
    the convex cube, whose volume fraction is `0.577^n`: the bound becomes
    `(1 - 0.577^n) 0.57 (5/3)^n`. That remark assumes the aggregated
    relaxation certifies only boxes inside the cube.
  - Branching on lifted variables and bounds from children (without counting
    them as leaves) are not covered.
- **Constant.** The proved base 5/3 is below the observed 2.1–3.
- **Other graphs.** For general graphs only a sketch is given. The relation
  to treewidth is one-directional: the bound holds at treewidth 1, which is
  the point for the program. We did not look for matching lower bounds for
  decomposition-aware methods.
- **Theorem 2's constant** relies on a floating-point maximization over one
  variable. A symbolic proof like Lemma 3.1 should be possible but was not
  done.
- **Computations** are floating point.
  - The toy branch-and-bound is not SCIP.
  - The grid DP restricts split points. It gives an upper bound on `N_cert`,
    not `N_cert` itself.
  - Only two random seeds were used.
- **Literature.** We did not search the literature for this bound. The
  repository notes do not contain it.

## 11. Files and commands

All commands are run from this directory. Targeted runs only; no
project-wide checks.

| File | Purpose |
|---|---|
| `bounds.py` | evaluates Theorems 1, 2, Propositions 5.3, 6.1 and repository Theorem 3.1; `python3 bounds.py > bounds.log`; `python3 bounds.py upper > logs/upper_bound.log` (Proposition 5.5) |
| `checks.py` | orthant boxes, envelope chord bound, center inequality on grown boxes; `python3 checks.py > logs/checks.log`; Lemma 3.1: `python3 checks.py lemma31 > logs/checks_lemma31.log` |
| `bb_path.py` | toy branch-and-bound; `python3 bb_path.py rel rule kappa cmode eps n...` |
| `jobs.txt`, `jobs2.txt`, `jobs3.txt`, `run_jobs*.sh` | the runs, via `xargs -P`; logs `logs/bb_runs.log`, `logs/bb_runs2.log`, `logs/bb_runs3.log` |
| `scip_runs.py`, `scip_jobs.txt`, `run_scip.sh` | SCIP runs; `logs/scip_runs.log`; `python3 scip_runs.py 0.1 seed0 EPS 300 4 6 8 noprop > logs/scip_noprop_EPS.log` |
| `analyze_leaves.py` | leaf locations; `logs/leaves_a.log` (`mcx bisect 0.1 zero 1e-4 6 8`), `logs/leaves_c.log` (`... 1e-6 6`) |
| `grid_dp.py` | grid-restricted minimal certificates; `logs/grid_dp.log`, `logs/grid_dp_n3.log`, `logs/grid_dp_n4.log` |
| `summarize.py` | tables of Section 7; `python3 summarize.py > logs/summary.log` |

Run notes:
- The second batch (`run_jobs2.sh`) stopped early. Our manual `pkill` of the
  stalled `viol` runs also terminated `xargs`. The missing runs were rerun in
  batch 3 (`jobs3.txt`).
- The stalled `viol` runs with `mcx`, and with `mc` at `kappa = 0`, were
  stopped by hand.
- A scratch exploration of extra witnesses (`/tmp/witness_explore.py`, not
  kept) is mentioned in Section 3 only as a negative result.

