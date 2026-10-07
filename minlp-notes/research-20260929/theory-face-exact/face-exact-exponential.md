# Exponential lower bounds for single-tree spatial branch-and-bound with termwise McCormick relaxations on a path

Date: 2026-09-29. Workstream "Theory B" of the
[program](../PROGRAM.md). Status: reviewed
([`../reviews/face-exact-review.md`](../reviews/face-exact-review.md)) and
revised (Section 13 lists every change). The revision was rechecked
([`../reviews/face-exact-recheck.md`](../reviews/face-exact-recheck.md)); the
recheck's small fixes are applied (Section 13, item 5).
Proofs are complete unless a step is marked otherwise. Computations are
floating-point illustrations, not certified counts. Scripts and logs are in
this directory (Section 12).

## Summary

**Question.** Face-exact relaxations (McCormick envelopes of bilinear terms,
per-factor convex envelopes, secants of concave univariate terms) have a gap
that vanishes on box faces. The repository's exponential lower bounds
(constrained note, Theorem 3.1) need a gap of at least `alpha q_B` at every
point, so they do not apply. Does single-tree spatial branch-and-bound still
need exponentially many leaves in `n` on a path-structured problem (treewidth
1) with a unique nondegenerate interior minimizer?

**Answer: yes for termwise McCormick relaxations, and this is a statement
about the relaxation class.** The results hold for every single-tree
certificate: any branching rule, split points, node order, valid incumbent,
pruning by inherited bounds, and same-relaxation bound tightening. With bound
tightening, the counted quantity is leaves plus `2n` per tightening round
(Lemma 1.2), not leaves alone.

1. **Theorem 1 (termwise McCormick).** Take the path family
   `f(x) = sum_i g_i(x_i) + sum_{i<n} b_i x_i x_{i+1}` with `|b_i| = b` and
   `g_i'' <= D` near the minimizer. Every certificate has at least

   ```
   (1 + 1/S)^n exp(-lambda (1 + eps/(b r^2))),   S = sqrt(1 + D/(2b)),   lambda = (1+S)/(2 S^2),
   ```

   members (leaves plus tightening pieces) when `D/(2b) <= 1.99`. Here `r` is
   the radius of a cube around the minimizer inside the root box.
   - For the family of PROGRAM.md (`D = 2`, `b = 0.8`) this is
     `(5/3)^n exp(-(5/9)(1 + 1.25 eps/r^2))`: at least `0.57 (5/3)^n` for
     `eps <= 10^-4` and `r >= 1/2`.
   - There is no `log(1/eps)` factor. The tolerance enters only through
     `exp(-lambda eps/(b r^2))`.
   - The bound holds for every relaxation whose gap is at least the termwise
     McCormick gap: exact, secant or outer-approximated univariate terms,
     level-1 RLT (which equals McCormick here).
   - It does not use uniqueness, nondegeneracy or nonconvexity of `f`. It
     holds for the convex member `kappa = 0`, a strictly convex QP.

   So Theorem 1 says that the termwise relaxation class forces exponentially
   many leaves. It is not a statement about single-tree search as such
   (Section 9).
2. **Theorem 2 (per-factor convex envelopes, for the PROGRAM factorization).**
   With factors `f_i = g_i(x_i) + b x_i x_{i+1}`, the per-factor envelope
   forces `c 1.20^n` leaves (base 1.205; the tables use the slightly
   conservative 1.2021). This depends on the factorization. Suppose the
   Hessian of `f` is positive definite at `x*` and the `g_i` are `C^2` near
   `x*`. Split each `g_i` between its two neighbouring factors, following a
   decomposition of the Hessian into positive definite `2x2` blocks
   (Griewank–Toint 1984). Then every factor is convex near `x*`, and the
   mechanism disappears there (Section 9.2).
3. **Mechanism.** The rigorous mechanism is a product-form volume argument
   (candidate (b) of the task, made precise).
   - At the center of `C ∩ R`, where `R` is a cube around the minimizer, the
     McCormick gap is at least `b sum_i w_i w_{i+1}/4`.
   - The center lies within `r - w_i/2` of `x*` in coordinate `i`, so `m`
     there is at most a quadratic in these numbers.
   - Validity couples the two, and the coupling forces
     `vol(C ∩ R) <= 0.6^n vol(R)` up to a constant (Lemma 2.1, Theorem 1).

   The other candidates:
   - *(a) Vertex covers at `x*`.* True as a statement about boxes that contain
     `x*`, but it gives no lower bound by itself, because a cube of half-side
     `sqrt(eps/(b(n-1)))` centered at `x*` is valid (Proposition 5.1). The
     correct `eps -> 0` picture is Proposition 5.2: of the `2^n` orthant boxes
     at `x*`, exactly two are exactly valid, and every orthant with a sign
     change along the path loses `b^2 W^2/(4D)` at scale `W`.
   - *(c) The nonconvex outer region.* Not needed. The bound holds for
     arbitrarily small cubes around `x*`. In a bisection run at `n = 8`, 82%
     of the leaves meet the cube `x* + [-0.3, 0.3]^n`, and `f` is convex on
     the larger cube `|x|_inf < 0.577`.
4. **A `log(1/eps)` factor** is proved only with a weak exponential base:
   `c sqrt(n) 1.072^n log(1/(n eps))`, from the matching-slice theorem of the
   face-exact note (Proposition 5.3; it needs the McCormick chord gap itself,
   not only (M_b)). Whether `c^n log(1/eps)` holds with the base of
   Theorem 1 is open (Conjecture 5.4).
5. **Upper bound.** The uniform `2^n`-ary dyadic refinement uses at most
   `C^n O(log(n/eps))` leaves with `C ≈ 17` (`kappa = 0`) or `20`
   (`kappa = 0.1`). Widest-side binary bisection uses at most as many
   (Proposition 5.5). So the minimal certificate size is `exp(Theta(n))` at
   fixed `eps`, not super-exponential.
6. **Per-factor alphaBB (Section 6).** On this family the repository's
   Theorem 3.1 (in its anisotropic form) gives base `0.78 < 1` with the exact
   per-factor `alpha` (`kappa = 0`) and `1.03` with the root-box `alpha`
   (`kappa = 0.1`). So it gives no, or almost no, exponential growth here.
   The center-volume argument gives `1.33^n` and `1.52^n` for these two
   values of `alpha`, and exponential growth for every `alpha > 0`.
7. **Computations (Section 7).**
   - *Toy branch-and-bound.* With exact termwise relaxations and certified
     node bounds, it grows by 2.7–3.1 per added variable under every rule
     tried, except one rule that stalls. Per-factor alphaBB, a different
     relaxation, grows by 2.4–2.9. The count behaves like `A_n + B_n log(1/eps)`,
     with both terms exponential in `n`.
   - *Certified bounds.* The first version pruned on HiGHS QP values, which
     can be up to `1.5e-4` too high. That made the `kappa = 0`, `c = 0` counts
     at `eps <= 1e-5` too small and produced a spurious "slope falls at small
     `eps`". Corrected.
   - *SCIP.* Default SCIP 10 is outside the theorem's relaxation class: its
     minor separator adds PSD cuts on `2x2` principal minors.
     - With that separator off, SCIP grows by 2.9–3.5 per variable, in the
       toy's range.
     - With it on (default), SCIP grows by 2.1–2.3 per variable and solves the
       convex variant at the root for small `n`.
   - *Minimal certificates.* Exact minimal grid-restricted certificates
     (upper bounds on the minimum) have 4, 10 and 32 leaves at `eps = 10^-2`
     for `n = 2, 3, 4`, and 4, 8 and 12 at `n = 2` for
     `eps = 10^-2, 10^-4, 10^-6`. That is 2.5–4.5 times fewer than bisection.
     - Theorem 1's bound is below every termwise toy count and every grid
       count, by factors of about 2.5–2200.
     - SCIP's default counts can be below it, because they are outside the
       model.

What remains open: the right base (2.7–3.5 per variable for termwise
relaxations in the data; the grid optima, which are upper bounds, grow by
2.5–3.2 per variable at `eps = 10^-2`), a
`log(1/eps)` factor with a good base, and whether per-factor envelopes with a
split factorization need exponentially many leaves outside the region where
the split factors are convex (Section 9.3). The program's separation must fix the relaxation class on both
sides.

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
  Lemma 2.1(c)). Termwise cuts inherited from ancestors are dominated by, or
  allowed in, this relaxation. Ancestor McCormick cuts are dominated because
  `vex_A <= vex_C` on `C ⊆ A`, and inherited univariate cuts are valid
  underestimators of `g_i`. Level-1 RLT for these terms is McCormick plus
  secants and tangents, so it satisfies (M_b). Cuts on aggregated
  expressions (for example on `sum t_i`) and PSD or SDP cuts are not
  covered.
- **(M^+)** The stronger hypothesis "the gap is at least the sum of the
  exact termwise McCormick gaps", `Gamma_C >= sum_i Gamma^McC_{C,i}`. It
  holds for the same termwise relaxations. Proposition 5.3 needs it, because
  it uses the McCormick chord gap along concave directions, which (M_b) does
  not bound.
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

Not covered:
- objective-cutoff propagation (interval FBBT of `f <= UBD`);
- cutting planes stronger than the termwise envelopes, in particular PSD cuts
  on principal minors of `xx^T` (SCIP's minor separator) and SDP relaxations
  (Section 9.1). Level-1 RLT is covered, as noted above;
- branching on lifted variables;
- relaxations of the aggregated sum `sum_i f_i` (convexity detection on the
  whole function, alphaBB with a box-dependent `alpha` of the whole
  function);
- incumbents accepted within a feasibility tolerance (then `f*` means the
  optimum of the tolerance-relaxed problem).

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
`mu`, improves these by 3.1% at `n = 2`, 1.7% at `n = 4` and less than 1%
for `n >= 8`.

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
  uniform `|b_e| = b`, the same computation gives
  `theta^(-n) exp(-2 lambda eps''/Delta)` with `rho = D/(Delta b)`. There is
  no boundary term.
- *A ceiling on the base.* At an interior minimizer with `g_i'' <= D`, the
  Hessian `diag(g_i''(x*_i)) + B` is PSD, hence so is `D I + B`. On a path
  this forces `rho >= cos(pi/(n+1))`, so the base `1 + 1/S` is at most
  `1 + 1/sqrt(1 + cos(pi/(n+1)))`, which tends to `1 + 1/sqrt 2 = 1.707`. The
  PROGRAM value 5/3 is close to this ceiling (observation of the review).
- *Where the constant is lost: in the covering step, not in the witness.*
  - The per-box step is nearly exhausted. The review's adversarial search
    found a valid box with volume fraction `0.582^n` at `n = 8` (review,
    Section 1.5), and our greedy search found `0.547^n` (Section 7.2).
  - So any lower bound that uses only the largest single-box volume is at most
    75.5 at `n = 8`, whatever witnesses it uses. Theorem 1 gives 34.2, and
    the exact supremum `nu` of Lemma 2.1 gives 37.9 (review): Lemma 3.1 loses
    about 10%.
  - The observed counts (`10^4` or more at `n = 8`) are far larger because
    large valid boxes cannot tile `R`. A better base must come from an
    argument about covering.
  - In particular, a bound of the form `c 2^n` (Conjecture 5.4) cannot come
    from a per-box volume argument while valid boxes with volume fraction
    above `2^-n` exist.

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

For `D = 2`, `b = 0.8`:
- The optimal parameters are `sigma = 0.400` and `mu = 1.165`. They give the
  per-variable base `exp(-Psi_J) = 1.2050` (`chordal_checks.py`; the review
  found the same).
- The value 1.2021 used in `bounds.log` and in the tables was optimized at
  `n = 200` including the `mu b sigma/n` term. It is slightly conservative.
- Per-`n` values (optimized per `n`): 1.5 at `n = 4`, 4.5 at `n = 10`, 28.7 at
  `n = 20` (`bounds.log`).
- The supremum over `s` is evaluated in floating point on a grid of
  `4 * 10^5` points with local refinement. This evaluation, not the
  inequality chain, is the only non-symbolic step.

**Theorem 2 depends on the factorization.** (E_D) puts all of `g_i` into
the factor that contains `x_i x_{i+1}`. That is how PROGRAM.md writes the
model, and it is what a modeling system sees. But the same `f` can be
factored as `f_i = s_i g_i(x_i) + b x_i x_{i+1} + t_{i+1} g_{i+1}(x_{i+1})`
with `s_i + t_i = 1`.
- With a split that follows the chordal decomposition of the Hessian, every
  factor is convex near `x*`, and the per-factor envelopes are exact there.
  For `kappa = 0` they are exact everywhere, and the root is pruned
  (Section 9.2).
- So "the strongest factorable relaxation" (PROGRAM.md) is the strongest only
  for a given factorization.
- Theorem 1 has no such dependence. McCormick relaxes the product alone under
  every split of the `g_i`.

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
interior, and (Q_D) holds on `R = x* + [-r, r]^n`. Consider an orthant box
with vertex `x*`, `C = x* + prod_i sigma_i [0, W_i] ⊆ X0` with `W_i <= r`, and
`sigma in {-1, 1}^n`. Call edge `i`
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

**Proposition 5.3 (matching slices).** Assume (M^+) and (Q_D) on `R`. Let
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
- That theorem's proof uses `Gamma_C >= sum over matched terms of their
  chord gaps` along `v_r` (face-exact Lemma 2.4). This is a property of the
  McCormick gap itself, so it holds under (M^+). It does not follow from
  (M_b): the chord product `min(delta_i^-, delta_j^+) min(delta_i^+, delta_j^-)`
  and `d_i d_j` are not comparable.
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
bound (integral restricted to the ellipsoid, hence conservative) is 4.0 at
`n = 4`, 8.2 at `n = 10` and 20.6 at `n = 20`. The full-cube integral gives
4.29 at `n = 4` (review). At `n = 10` it
grows from 3.1 (`eps = 10^-2`) to 18.7 (`10^-8`) (`bounds.log`). So the log
factor is proved, but with a weak base.

**Conjecture 5.4.** For the PROGRAM family (`b = 0.8`, `kappa in [0, 0.1]`)
there are constants `c, c' > 0` with `N_cert(eps) >= c 2^n` and
`N_cert(eps) >= c' beta^n log(1/eps)` for some `beta > 1.072`, for all
`eps <= eps_0`.

Evidence, and its limits:
- The minimal grid-restricted certificates of Section 7.6 have 4, 10 and 32
  leaves at `eps = 10^-2` for `n = 2, 3, 4`, and 4, 8 and 12 leaves at
  `n = 2` for `eps = 10^-2, 10^-4, 10^-6`. The last sequence is linear in
  `log(1/eps)`. But these are *upper* bounds on `N_cert`, so they are weak
  evidence for a lower bound.
- Only 2 of the `2^n` orthant boxes at `x*` are exactly valid
  (Proposition 5.2).
- The toy branch-and-bound's `log(1/eps)` coefficient `B_n` grows by about 3
  per variable (Section 7.5).
- SCIP with its minor separator off grows by 2.9–3.5 per variable
  (Section 7.4).
- The `2^n` half cannot be proved by a per-box volume argument. Valid boxes
  with volume fraction above `2^-n` exist (Remark in Section 3).

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
`b = 0.8` and 19.9 for `kappa = 0.1` (`logs/upper_bound.log`).

**Binary bisection is no worse.** Widest-side binary bisection at midpoints
(ties to the lowest index), with the same pruning test, has at most as many
leaves as the dyadic scheme. The argument is from the review; we checked it.
1. Validity is monotone under inclusion, because `Gamma_{C'} <= Gamma_C` on
   `C' ⊆ C`.
2. A binary leaf `L` lies between a dyadic cube `Q` of some level `j`
   (`L ⊆ Q`) and a level-`(j+1)` subcube.
3. If `L = Q`, the dyadic parent of `Q` was not pruned (it is a strict
   binary ancestor of `L`), so `Q` is a dyadic leaf.
4. Otherwise `Q` was split in the binary tree, so `Q` is invalid and is split
   in the dyadic tree too. Choose a level-`(j+1)` cube `Q' ⊆ L`: it is valid
   by step 1 and is a dyadic leaf.
5. Distinct binary leaves give distinct dyadic leaves, because leaves have
   disjoint interiors.

So `0.57 (5/3)^n <= N_cert(10^-4) <= 20^n O(log(n/eps))`, and the growth seen
with practical rules (Section 7) is about `2.1^n`–`3.5^n`.

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
(`logs/abb_bases.log`). The table uses the anisotropic form of Theorem 3.1,
with `prod_i alpha_i^(1/2)` and `alpha_f` at the two end variables. The
repository states Theorem 3.1 with one `alpha`. The anisotropic form follows
by the same proof, with AM–GM applied to `sum_i alpha_i a_i` as in step 4 of
face-exact Theorem 3.4.

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
  by 2.39 per variable. McCormick needs 69,632 and grows by 2.94. So being
  exact on faces does not make McCormick cheaper here. Near an interior
  minimizer, the size of the gap at box centers matters more.

## 7. Computations

All counts are floating-point illustrations.
- *Our branch-and-bound (`bb_path.py`).* The incumbent is fixed at `f*`,
  computed by multi-start L-BFGS-B. The tree does not depend on node order.
  Every run also checked that no relaxation solution had `f < f* - 10^-9`;
  all were "ok".
- *Certified node bounds (revision after review).*
  - A box is pruned iff a *certified* lower bound is at least
    `f* - eps - 10^-12`. The `10^-12` absorbs rounding at exact ties.
  - So pruned boxes are valid at `eps + 10^-12` up to rounding. In the
    recheck's exact-arithmetic reruns, no node bound fell in that band
    (recheck, Sections 1–2).
  - For `mc` and `mcx` the certified bound is the separable dual function of
    the McCormick relaxation at multipliers `lambda in [0,1]^(n-1)`, valid
    for every `lambda` by weak duality. For alphaBB it is the Frank–Wolfe
    bound at the solver's point.
  - When `f* - eps` lies between this bound and the relaxation value at a
    feasible point, the bound is refined by dual ascent (L-BFGS-B). For
    `mc`, if that fails, the multipliers are taken from an interior-point
    solve (Clarabel). In the final runs, no node whose solver value was
    above the threshold remained undecided.
  - Nodes that stay undecided while the solver value is also below the
    threshold are branched. The counter does not record them. This can only
    inflate counts. The recheck's exact branch-and-bound found no flipped
    decision on the instances it tried (`kappa = 0` and seed 0,
    `n = 2..5`).
  - HiGHS's objective value is used only for branching decisions.
  - The first version pruned on HiGHS's QP value, which can be up to `1.5e-4`
    too high (review, Section 5.2). All counts below are from the certified
    reruns: `logs/bb_runs_v2.log`, and for `mc` with `kappa = 0.1`
    `logs/bb_runs_v3_mc.log`, which overrides it. First-version logs are in
    `logs/v1/`.
  - The v2 runs of `mc` with `kappa = 0.1` computed the feasible-point value
    with the true quartic instead of the node's secant. That affected only
    when refinement was triggered and the diagnostic counters, not the
    validity of pruning. Those runs were redone with the corrected code (v3),
    together with the Clarabel fallback. At most a few leaves per run
    changed (for example 15,719 -> 15,717 for `viol`, `n = 8`).
- *Relaxations.*
  - `mc`: `x^2` exact, secant of `-kappa x^4`, McCormick. A convex QP solved by
    HiGHS, with Clarabel as fallback.
  - `mcx`: `g_i` exact (Kelley cuts to violation `1e-10`) and McCormick, an LP.
  - `abb`: per-factor alphaBB with `kappa = 0`, a QP.
  - `abbU`, `abbS`: per-factor alphaBB with an exact box-dependent `alpha`,
    for the PROGRAM factorization (`U`) or the balanced split (`S`,
    Section 9.2). Any `kappa`; solved by L-BFGS-B over the box, with the
    Frank–Wolfe bound.

  For `kappa = 0`, `mc = mcx`: the counts agree (320 and 962 leaves at
  `n = 4, 5`, `logs/bb_runs_v2.log`).
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
- Theorem 2: 1.205 (1.202 in the table columns, conservative);
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

### 7.3 Leaf counts, `eps = 10^-4` (`make_tables.py`, `logs/tables.md`)

Leaves of our branch-and-bound with certified bounds. The last column is the
geometric-mean growth factor per added variable over the last four steps of
`n`.

| relaxation, rule, instance | n=2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | growth |
|---|---|---|---|---|---|---|---|---|---|---|
| `mc` bisect, `kappa=0`, `c=0` | 24 | 100 | 320 | 962 | 2780 | 7976 | 23552 | 69632 | 206612 | 2.94 |
| `mc` bisect, seed 0 | 20 | 80 | 249 | 738 | 2254 | 7121 | 21001 | 64518 | 198363 | 3.06 |
| `mc` oracle, seed 0 | 31 | 111 | 335 | 954 | 2594 | 7174 | 20296 | 57637 | 164804 | 2.82 |
| `mc` viol, seed 0 | 16 | 67 | 206 | 700 | 1941 | 8350 | 15717 | 50493 | 130035 | 2.86 |
| `mc` vw, seed 0 | 19 | 66 | 189 | 587 | 1766 | 5791 | 15756 | 47043 | | 2.99 |
| `mcx` bisect, seed 0 | 17 | 77 | 241 | 648 | 1988 | 6229 | 18032 | 54788 | | 3.03 |
| `mcx` oracle, seed 0 | 24 | 101 | 316 | 904 | 2405 | 6483 | 18012 | 49771 | | 2.72 |
| `mcx` vw, seed 0 | 16 | 61 | 182 | 499 | 1474 | 4503 | 11976 | 35908 | | 2.91 |
| `mcx` vw, seed 1 | 16 | 58 | 173 | 560 | 1711 | 4822 | 14954 | 40860 | | 2.92 |
| `mcx` vw, `c=0` | 20 | 65 | 228 | 664 | 1780 | 5064 | 13994 | 39297 | | 2.77 |
| `abb` bisect, `kappa=0`, `c=0` | 32 | 114 | 316 | 804 | 1992 | 4828 | 11532 | 27314 | 64740 | 2.39 |
| `abb` viol, `kappa=0`, `c=0` | 16 | 46 | 142 | 456 | 1338 | 3930 | 11406 | 32254 | 95198 | 2.90 |
| `abbU` bisect, `c=0` (PROGRAM factorization) | 34 | 114 | 318 | 824 | 2094 | 5284 | 13352 | | | 2.55 |
| `abbS` bisect, `c=0` (balanced split) | 1 | 24 | 64 | 162 | 404 | 1000 | 2476 | | | 2.49 |
| Theorem 1 lower bound | 1.6 | 2.7 | 4.4 | 7.4 | 12.3 | 20.5 | 34.2 | 56.9 | 94.9 | 1.67 |

"Seed 0" and "seed 1" are the PROGRAM instances with `kappa = 0.1`. The
`abbU`/`abbS` rows use `kappa = 0.1`.

- **Growth.** Every termwise rule grows by 2.7–3.1 per variable on every
  instance. The alphaBB relaxations (a different class) grow by 2.4–2.9.
- **Effect of certified bounds.**
  - At `eps = 10^-4` the counts change by at most 0.8% against the first
    version.
  - They change most on `kappa = 0`, `c = 0`: 23,552 against 23,488 at
    `n = 8`.
  - On seed 0, the rules `oracle`, `viol` and `vw` gained 1–73 leaves.
  - At smaller `eps` the changes are large (Section 7.5).
- **The `viol` rule stalls with exact relaxations.** It needs 390–448 leaves
  at `n = 3` with `mcx`. With `mc` at `kappa = 0` it needs 42,009 leaves at
  `n = 4` with certified bounds (38,394 in the first version). The runs at
  larger `n` were stopped by hand in the first version and are not repeated.
  The `vw` rule, which differs only in variable selection and split point,
  behaves normally.
- **The `oracle` rule** (splitting at `x*`) changes the count by between
  +55% (`n = 2`) and -17% (`n = 10`) on seed 0. Placing faces through `x*`
  does not remove the exponential growth, in line with Proposition 5.2: only
  the two unfrustrated orthants become exact.
- **Split factorization.**
  - For `kappa = 0`, per-factor alphaBB with the balanced split needs 1 leaf
    at every `n`, because the relaxation equals `f`. It is logged at
    `n = 8`.
  - For `kappa = 0.1` it needs about 5 times fewer leaves than the PROGRAM
    factorization, but grows at the same rate.
  - These counts are upper bounds on the split-envelope counts
    (Section 9.3), not lower bounds.

### 7.4 SCIP (`scip_runs.py`, `logs/scip_runs.log`, `logs/scip_noprop_*.log`, `logs/scip_nominor_*.log`)

SCIP 10 through PySCIPOpt 6.2.1, one thread, the same model as
`scratch/probe3.py`, `absgap = 1e-4`. The table gives nodes, not leaves.
"Minor off" means `separating/minor/freq = -1` (default 10).

| n | `kappa=0.1`, `c=0` | same, minor off | seed 0 (PROGRAM) | seed 0, minor off | seed 0, presolve and propagation off | `kappa=0`, `c=0` | same, minor off | `kappa=0`, seed 0 |
|---|---|---|---|---|---|---|---|---|
| 2 | 1 | | 1 | | | | | |
| 3 | 7 | | | | | | | |
| 4 | 81 | 134 | 217 | 529 | 232 | 1 | 21 | 1 |
| 5 | 411 | | | | | | | |
| 6 | 1116 | 1841 | 1055 | 4367 | 1273 | | | |
| 7 | 2701 | | | | | | | |
| 8 | 6410 | 19781 | 4447 | 36081 | 8069 | 21 | 14011 | 30 |
| 9 | 11449 | | | | | | | |
| 10 | >26236 (300 s) | | 28954 (PROGRAM) | | | | | |
| 12 | >87839 (300 s) | | | | | 5619 | | 1271 |
| 16 | | | | | | >34478 (60 s) | | >38181 (60 s) |

- **The minor separator puts default SCIP outside (M_b).**
  - With it off, SCIP grows by about 2.9 per variable on seed 0 (`n = 4 -> 8`)
    and about 3.5 on `kappa = 0.1`, `c = 0`, which is the range of the toy
    branch-and-bound.
  - With it on (default), SCIP grows by about 2.3 (`c = 0`, `n = 5 -> 9`) and
    2.1 (seed 0, `n = 4 -> 8`; 2.2–2.3 over `n = 4..10` in the PROGRAM
    table). The PROGRAM's "factor 2–3 per two added variables" understates
    its own table, whose factors per two variables are 3.1–8.4.
  - The minor separator also explains the root solves of the convex variant
    (1 node at `n = 4`, 21 at `n = 8`; 21 and 14,011 with it off). The
    PROGRAM reports root solves up to `n = 5`.
  - Section 9.1 explains why PSD cuts on clique minors are exact for the
    convex variant.
  - The review reported the same minor-off counts, and we reproduced them
    (`logs/scip_nominor_*.log`).
- **Tolerance.**
  - On seed 0, the counts are identical for absolute gaps `10^-4`, `10^-5`
    and `10^-6` (217, 1055, 4447), with or without propagation. They drop
    only at `10^-2`–`10^-3` (74 and 181 at `n = 4`).
  - `limits/absgap` is a global stopping criterion. Nodes are cut off when
    their bound reaches the primal bound, with no `absgap` slack (SCIP's
    documented behaviour; we did not read the source).
  - SCIP's incumbents lie below the true `f*` because the feasibility
    tolerance lets `t_i` sit about `10^-6` below its expression. The gap is
    2.5e-6 at `n = 4` and 3.5e-6 at `n = 6` with default settings (2.3e-6 and
    3.6e-6 without propagation). So SCIP's effective per-node tolerance is
    about `10^-6` whatever gap is requested, and its trees close with
    `dual = primal`.
  - Its counts are best compared with ours at `eps = 10^-6`. There default
    SCIP uses 2.5–8 times fewer nodes than our `vw` rule (539, 4501, 37,429
    nodes at `n = 4, 6, 8`, against 217, 1055, 4447). With the minor
    separator off it is within 4% of `vw` (529, 4367, 36,081).

### 7.5 Dependence on `eps` (leaves)

Columns are `eps = 10^-2, 10^-3, 10^-4, 10^-5, 10^-6`. All counts use
certified bounds.

| relaxation, rule, instance | n | `10^-2` | `10^-3` | `10^-4` | `10^-5` | `10^-6` |
|---|---|---|---|---|---|---|
| `mcx` bisect, seed 0 | 4 | 113 | 159 | 241 | 313 | 359 |
| | 6 | 875 | 1443 | 1988 | 2564 | 3130 |
| | 8 | 8290 | 13337 | 18032 | 23418 | 28024 |
| `mcx` vw, seed 0 | 4 | 86 | 136 | 182 | 231 | 270 |
| | 6 | 704 | 1121 | 1474 | 1850 | 2251 |
| | 8 | 5707 | 8966 | 11976 | 15200 | 18715 |
| `mc` bisect, `kappa=0`, `c=0` | 4 | 132 | 232 | 320 | 422 | 522 |
| | 6 | 1122 | 1954 | 2780 | 3636 | 4474 |
| | 8 | 9508 | 16534 | 23552 | 30474 | 37500 |
| `mc` viol, seed 0 | 8 | 6820 | 10626 | 15717 | 26771 | 36220 |
| SCIP nodes, seed 0 | 8 | 2831 | 4447 | 4447 | 4447 | 4447 |

- **Linear in `log(1/eps)`.** Counts grow linearly in `log10(1/eps)` on every
  instance. The slope `B_n` per decade is:
  - bisection, seed 0: about 60, 560 and 5000 at `n = 4, 6, 8`;
  - `vw`: 46, 390 and 3250;
  - bisection on `kappa = 0`, `c = 0` (`x* = 0` on the dyadic grid): 100,
    840 and 7000, nearly constant in `eps` (increments 7026, 7018, 6922, 7026
    at `n = 8`).

  So `N ≈ A_n + B_n log(1/eps)`, with `B_n` growing by about 3 per variable.
- **Correction.** The first version reported that on `kappa = 0`, `c = 0`
  "the slope falls at small `eps`" (29,282 leaves at `n = 8`,
  `eps = 10^-6`). That was an artifact of HiGHS values that were too high.
  The certified count is 37,500, as the review found with an independent
  solver.
- **Secant relaxation.** The secant relaxation (`mc`, `kappa = 0.1`) adds
  refinement toward `x*` in every coordinate. The secant gap of
  `-kappa t^4` is linear near a vertex.

### 7.6 Minimal grid-restricted certificates (`grid_dp.py`, `logs/grid_dp_n*_*.log`)

Exact minimum over guillotine partitions whose split points lie on the grid
`{0, ±2^-k : 0 <= k <= K}`, for `kappa = 0`, `c = 0` and exact McCormick,
with certified bounds. This is an upper bound on `N_cert`. Bisection and
`vw` counts are from `logs/bb_runs_v2.log`.

| n | `eps` | K | grid-optimal leaves | bisection leaves | `vw` leaves | Theorem 1 | Prop. 5.3 |
|---|---|---|---|---|---|---|---|
| 2 | `10^-2` | 4 | 4 | 10 | 10 | 1.58 | 1.61 |
| 2 | `10^-4` | 7 | 8 | 24 | 20 | 1.59 | 2.80 |
| 2 | `10^-6` | 10 | 12 | 38 | 30 | 1.59 | 4.00 |
| 3 | `10^-2` | 4 | 10 | 40 | 30 | 2.64 | 1.61 |
| 3 | `10^-3` | 5 | 16 | 72 | 48 | 2.65 | 2.20 |
| 4 | `10^-2` | 3 | 32 | 132 | 102 | 4.40 | 1.98 |

- **Corrections.** The first version reported 10 and 32 for `n = 2`,
  `eps = 10^-6`. The certified values are 12 and 38, as the review found.
- **A tie at `n = 2`, `eps = 10^-2`.** 4 is the exact optimum under the
  definition `LB >= f* - eps`.
  - 56 grid boxes, such as `[-1/4, 1/4] x [-1, 0]`, have bound exactly
    `-eps` (recheck, exact rational DP).
  - Without the tie tolerance, floating-point rounding puts them `1.7e-18`
    below `-eps` and gives 5. That is also the optimum under a strict
    inequality.
  - At `10^-4` and `10^-6` no grid box has bound exactly `-eps`, and the exact
    optima 8 and 12 agree with ours.
- **Growth in `eps`.** At `n = 2` the sequence 4, 8, 12 is linear in
  `log(1/eps)`.
- **Shape of the optimum.** For `n = 2`, `eps = 10^-4` the optimal
  certificate has 8 leaves:
  - two slabs `|x_1| >= 1/4` that span all of `x_2`;
  - four boxes with `1/64 <= |x_1| <= 1/4`, split in `x_2` at `±1/16`;
  - two thin boxes `|x_1| <= 1/64`, split at `x_2 = 0`.

  So it is not orthant-based. It is multi-scale in the coordinate `x_1`. At
  `eps = 10^-6` the same pattern has one more scale.

### 7.7 Where the leaves are (`analyze_leaves.py`, `logs/leaves_*.log`)

`mcx`, bisection, `kappa = 0.1`, `c = 0`. Leaves counted by sup-distance from
`x* = 0`. The rerun with certified bounds gave identical counts:

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

- **Default SCIP is outside the theorem's relaxation class.** SCIP 10
  separates PSD cuts on `2x2` principal minors by default
  (`separating/minor/freq = 10`). These cuts see curvature spread over
  several terms, which termwise relaxations cannot (Section 9.1).
  - They explain the root solves of the convex variant: with the minor
    separator off, `kappa = 0`, `c = 0` needs 21 nodes at `n = 4` and 14,011
    at `n = 8`, against 1 and 21 with it on.
  - They also explain most of SCIP's lower growth: 529, 4367 and 36,081
    nodes on seed 0 at `n = 4, 6, 8` with the separator off, against 217,
    1055 and 4447 with it on (Section 7.4).
- **With the minor separator off, SCIP's growth is in the range of the toy
  branch-and-bound** (2.9 per variable on seed 0 and 3.5 on `kappa = 0.1`,
  `c = 0`, against 2.7–3.1). This is consistent with the product-volume
  mechanism of Theorem 1. It is not a proof about SCIP: we did not check that
  SCIP's remaining components satisfy (M_b), and SCIP also uses propagation
  with the objective cutoff.
- **The observed rates are higher than the proved one** (2.7–3.5 against
  5/3). The review showed that the per-box step is nearly exhausted
  (Remark in Section 3), so the difference lies in the covering step. It is
  not a second mechanism, but this is not proved.
- **Default SCIP still grows by 2.1–2.3 per variable.** It applies minor cuts
  only at some depths and only as outer approximations of the PSD condition.
  This note does not explain that remaining growth.
- **Dependence on `eps`.** In the toy runs, `log(1/eps)` terms with
  exponential coefficients are visible from `10^-2` to `10^-6` (Section 7.5).
  They are consistent with the frustrated-orthant structure
  (Proposition 5.2) and with Conjecture 5.4. SCIP's counts do not change for
  `absgap` from `10^-4` to `10^-6`, for the following reason.
  - `limits/absgap` is a global stopping criterion. Nodes are cut off when
    their bound reaches the primal bound, with no `absgap` slack. This is
    SCIP's documented behaviour; neither we nor the review read its source.
  - SCIP's incumbents lie a few `10^-6` below `f*` (feasibility tolerance), so
    its effective per-node tolerance is about `10^-6`.
- **Neither vertex covers (a) nor the outer region (c) drive the toy counts**
  (Sections 5.1 and 5.3).

## 9. Significance: a statement about the relaxation class

### 9.1 Theorem 1 concerns termwise relaxations; clique-wise PSD cuts escape it

Theorem 1 holds for `kappa = 0`, where `f` is a strictly convex QP. What it
measures is that a termwise relaxation cannot see curvature spread over
several terms: `x_i^2` in one term, `b x_i x_{i+1}` in another. Relaxations
that see the aggregated curvature near `x*` avoid it. The relevant structure
is the chordal decomposition of the Hessian.

**Lemma 9.1 (chordal split of a path Hessian).** Let
`H = diag(d) + B` be tridiagonal with off-diagonal entries `b_i`. Define the
pivots `p_1 = d_1` and `p_{i+1} = d_{i+1} - b_i^2/p_i`. If `H` is positive
definite, all pivots are positive, and

```
H = sum_{i<n} E_i' [[p_i, b_i], [b_i, b_i^2/p_i]] E_i + p_n e_n e_n',
```

where `E_i` selects coordinates `i, i+1`. Each `2x2` block is PSD. To get
positive definite blocks, decompose `H - delta I`, which is still positive
definite for small `delta > 0`, and distribute `delta I` over the blocks'
diagonals.

*Proof.* The pivots are those of Gaussian elimination (the `LDL'`
factorization), which are positive iff `H` is positive definite. The
diagonal of the sum at `i` is `b_{i-1}^2/p_{i-1} + p_i = d_i`, and the
off-diagonal entries are `b_i`. Each block has determinant 0 and positive
trace. □

This is the path case of a known theorem: a PSD matrix with chordal
sparsity is a sum of PSD matrices supported on the maximal cliques. It was
first proved by Griewank and Toint (1984, Theorem 4), then by Agler, Helton,
McCullough and Rodman (1988, Theorem 2.3). See Vandenberghe and Andersen
(2015), Theorem 9.2 and Section 12.1. Griewank and Toint were motivated by
exactly the question of Section 9.2: shifting quadratic terms among element
functions so that each element function becomes locally convex. For `H = 2I + 0.8A` the pivots decrease from 2
to 1.6, and the balanced blocks `[[1, 0.8], [0.8, 1]]` (eigenvalues 0.2 and
1.8) also work (`chordal_checks.py`).

**Consequence A: clique-wise PSD cuts are exact for the convex variant.**
Take a lifted relaxation with variables `X_ii` (for `x_i^2`) and
`X_{i,i+1}` (for the products). Impose, for each edge `c = {i, i+1}`, that
`[[1, x_c'], [x_c, X_c]]` is PSD, where `X_c` is the `2x2` block of `X`.
For `kappa = 0` the objective is `<H/2, X> + c'x`. By Lemma 9.1,
`<H, X> = sum_c <H_c, X_c> >= sum_c <H_c, x_c x_c'> = x'Hx`. The term
`p_n e_n e_n'` uses `X_nn >= x_n^2`, which the last block implies. So the
relaxation bound equals `min f` on every box, and one leaf suffices.
- *Numerical check.* On the root box, the clique-PSD bound equals `f*` to
  `1e-9` for `n = 6, 8` with `c = 0` and seed 0 (`logs/chordal_checks.log`).
- *SCIP.* SCIP's minor separator derives cuts from such PSD conditions on
  `2x2` principal minors (per `sepa_minor.h` of SCIP 10.0.3, read by the
  recheck). It adds eigenvector cuts that are violated by at least `1e-4`,
  at some nodes (frequency 10), not the full constraint. That is consistent
  with the data of Section 7.4: root solves at small `n`, and much smaller
  counts at larger `n`.

### 9.2 Theorem 2 depends on the factorization

**Consequence B: a split factorization removes the local mechanism for
per-factor envelopes.** This is Griewank and Toint's (1984) local
convexification, applied to our factors. Assume the Hessian of `f` is
positive definite at `x*` and the `g_i` are `C^2` near `x*_i`.
1. Split each `g_i` in proportion to Lemma 9.1, with positive definite
   blocks: `f_i = s_i g_i(x_i) + b_i x_i x_{i+1} + t_{i+1} g_{i+1}(x_{i+1})`,
   where `s_i g_i''(x*_i)` and `t_{i+1} g_{i+1}''(x*_{i+1})` are the block
   diagonals. The part `p_n` of `g_n` goes to the last factor.
2. Each factor Hessian is then positive definite at `x*`. By continuity it is
   positive definite on a cube `U = x* + [-r_0, r_0]^n`. PSD blocks, such as
   the determinant-0 blocks of Lemma 9.1, would give convexity at `x*` only.
3. A convex function is its own convex envelope. So on every box inside `U`
   the per-factor envelope relaxation is exact, and `U` is certified by one
   box.
4. The mechanism of Theorem 2 near `x*` disappears.

Examples (`logs/chordal_checks.log`):
- For `kappa = 0` with the balanced split (end factors take all of `g_1` and
  `g_n`), every factor is convex everywhere. So `N_cert(eps) = 1` for every
  `eps >= 0`.
- For the PROGRAM family (`kappa = 0.1`), with the balanced split, the
  largest centred cube on which every factor is convex is
  `|x|_inf <= 1/sqrt(3) ≈ 0.577`. For the end factors it is 0.851. It
  coincides with the convexity cube of `f` (Lemma 1.1(c)). The set where a
  factor is convex is not a cube: the interior factor is convex at
  `(0.77, 0)`, for example. On the full square an interior factor has
  smallest Hessian eigenvalue -0.40.

Theorem 1 is not affected by the split, because McCormick relaxes the
product alone.

### 9.3 What remains globally

*Update (root, 2026-09-30):* the later
[robust-lower-bound note](../theory-robust-lb/robust-lower-bound.md)
shows that this family with `c = 0` is solved at the root by a fixed
balanced split with exact envelopes (its Proposition 2.1), and proves a
qualitative split-robust exponential lower bound on a different, gadget-based
family (its Theorem 4.3). The discussion below predates that note.

- **For per-factor envelopes with a split.**
  - If `f` is nonconvex on `X0` (`kappa = 0.1`, `n >= 3`), every split
    leaves some factor nonconvex somewhere, because a sum of convex factors is
    convex. So some boxes have a positive envelope gap.
  - With the balanced split, only boxes that reach outside
    `|x|_inf <= 1/sqrt(3)` have a gap. Such a box has points where
    `m >= (1 - kappa - b)|x|^2 >= 0.033`, and its gap need not be small near
    `x*`.
  - Our lower-bound argument needs a cube around `x*` on which every box has
    a gap of order `b w_i w_{i+1}` at its center. Here boxes inside the convex
    cube have no gap, so the argument gives nothing. We have no lower bound
    for the split factorization.
  - Numerical proxy: per-factor alphaBB with an exact box-dependent `alpha`.
    It is exact where the factors are convex, and its gap dominates the
    per-factor envelope gap of the same factorization. So with bisection and
    `UBD = f*` its tree contains the envelope tree, and its leaf count is an
    upper bound for the envelope count. Leaves for `kappa = 0.1`, `c = 0`,
    `eps = 10^-4`, bisection:

    | n | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
    |---|---|---|---|---|---|---|---|
    | PROGRAM factorization (`abbU`) | 34 | 114 | 318 | 824 | 2094 | 5284 | 13352 |
    | balanced split (`abbS`) | 1 | 24 | 64 | 162 | 404 | 1000 | 2476 |

    - The split removes a factor of about 5, but the proxy's count still
      grows by about 2.5 per variable.
    - This is an *upper* bound on the split-envelope count with bisection.
      It shows that split envelopes need at most, for example, 2476 leaves
      at `n = 8`. It is no evidence that they need exponentially many.
    - Every leaf of the split run has a side of length at least 1
      (`logs/leaves_abbS.log`), so it reaches outside the convex cube. That
      is automatic under widest-side bisection of `[-1,1]^n`, not a finding.
    - Whether exact per-factor envelopes with a split need exponentially many
      leaves is open.
- **For clique-wise PSD relaxations with `kappa = 0.1`.** Near `x*` the
  remaining gap is the secant gap of `-kappa x_i^4`. That gap is of alphaBB
  type with coefficient about `6 kappa x_i^2`, which vanishes at `x* = 0`.
  Our results give no exponential bound there. Default SCIP still grows by
  2.1–2.3 per variable, which this note does not explain.

### 9.4 Relation to the literature

The program's literature audit
([`../literature/decomposition-bb-prior.md`](../literature/decomposition-bb-prior.md),
claim C1) rates the single-tree lower bound "partially known". The review
checked the same sources and ran no new search.

- **Cluster problem.**
  - Du and Kearfott (1994) give upper bounds on the number of boxes left near
    a nondegenerate minimizer.
  - Neumaier (2004, Section 15) gives a heuristic count exponential in `n`
    even for second-order bounds.
  - Wechsung, Schaber and Barton (2014) estimate that exponential growth in
    `n` is avoided only if the second-order prefactor satisfies
    `K <= 9 lambda_1/4`; alphaBB has `K <= alpha n/4`.
  - Kannan and Barton (2017) treat the constrained case.

  These are estimates for specific box sizes and schemes, and they ignore
  sparsity. Termwise McCormick has prefactor `sum_E |b|/4`, which grows like
  `n` even on a path (face-exact Lemma 2.5). Theorem 1 is a rigorous version
  of the cluster prediction for this class, valid for every certificate and
  at treewidth 1. The audit and the review found no prior rigorous statement
  of this form.
- **The technique.** Covering by volume is standard (the repository's
  Theorem 3.1). The center-of-box witness is that of face-exact
  Proposition 3.10. The new part is the combination: the summed edge gap,
  with `m` bounded at the witness's own position.
- **MILP.** Rigorous exponential lower bounds for LP-based branch-and-bound
  at bounded treewidth exist (Basu, Conforti, Di Summa and Jiang 2023;
  Dey and Shah 2022; Cheng and Basu 2026, as listed in the audit). They use
  instances with many optimal solutions. Here the minimizer is unique and
  nondegenerate, and the bound comes from the relaxation gap.
- **Chordal structure.**
  - Griewank and Toint, "On the existence of convex decompositions of
    partially separable functions", *Math. Programming* 28 (1984) 25–49.
    Their Theorem 4 gives the decomposition of Lemma 9.1, and they construct
    the local convexification of Consequence B.
  - Agler, Helton, McCullough and Rodman, *Linear Algebra Appl.* 107 (1988)
    101–149, Theorem 2.3.
  - Vandenberghe and Andersen, *Foundations and Trends in Optimization* 1(4)
    (2015), Theorem 9.2 and Section 12.1.
  - The sparse SDP and SOS relaxations of Waki, Kim, Kojima and Muramatsu
    (*SIAM J. Optim.* 17, 2006) exploit the same clique structure.
  - The recheck verified these references.

### 9.5 Consequence for the program

A separation between single-tree and decomposition-aware branch-and-bound
must fix the relaxation class on both sides. Theorem 1 separates the
termwise class from a decomposition method only if that method's child
minorants are also built from termwise relaxations. Otherwise the comparison
measures relaxation strength, not search structure. Section 9.1 shows that
clique-wise PSD cuts alone already remove the local mechanism for the convex
variant.

## 10. Status

| Item | Content | Status |
|---|---|---|
| Lemma 1.1 | properties of the family (`c = 0`) | proved |
| Lemma 1.2 | runs give certified covers; the count is leaves plus `2n` per tightening round | proved (restates repository lemmas) |
| Lemma 2.1 | center-volume lemma | proved; checked by the review, including an adversarial box search |
| Lemma 3.1 | one-variable inequality, `rho <= 1.99055` | proved; `S_max` computed numerically; checked on a grid |
| Theorem 1 | termwise McCormick (M_b): `(1 + 1/S)^n e^(-lambda(1+eps''))`; `>= 0.57 (5/3)^n` for PROGRAM | proved; review confirmed |
| Theorem 1(b) | every `rho`: `exp((n-1-eps'')/(rho+2))` | proved |
| Lemma 4.1 | chord bound for per-factor envelopes | proved; checked numerically |
| Theorem 2 | per-factor envelopes, PROGRAM factorization: `c 1.20^n` (base 1.205) | proved; base from a floating-point 1-D maximization; depends on the factorization (Section 9.2) |
| Proposition 5.1 | vertex covers at `x*`; a small valid cube | proved |
| Proposition 5.2 | 2 exact orthants; frustrated orthants cost `b^2 W^2/(4D)` (`W_i <= r`) | proved; attained numerically |
| Proposition 5.3 | `log(1/eps)` factor with base 1.072, under (M^+) | proved (application of face-exact Theorem 3.4); integral by quadrature |
| Conjecture 5.4 | `N_cert >= c 2^n` and `c' beta^n log(1/eps)` | conjecture; the `2^n` half is out of reach of per-box volume arguments |
| Proposition 5.5 | dyadic refinement `<= 20^n O(log(n/eps))`; binary bisection no worse | proved |
| Proposition 6.1 | per-factor alphaBB center-volume, base 1.33–1.52 | proved; base numerical |
| Lemma 9.1 | chordal split of a positive definite path Hessian into PSD `2x2` blocks | proved (Griewank–Toint 1984, Theorem 4, path case) |
| Consequence A | clique-wise PSD relaxation exact for `kappa = 0` | proved; checked numerically; consistent with SCIP's minor-separator effect |
| Consequence B | a split factorization (positive definite blocks) removes Theorem 2's mechanism near `x*` | proved (Griewank–Toint's local convexification) |
| Split envelopes, globally | exponential outside the region where the split factors are convex? | open; the alphaBB proxy, an upper bound on the envelope count, grows by about 2.5 per variable |
| Other graphs | `rho = D/(Delta b)` for `Delta`-regular graphs | sketched |
| Route to `theta'^(-n) log(1/eps)` | frustrated boxes are single-scale | sketched |
| Section 7 counts | toy branch-and-bound with certified node bounds | recomputed after review |
| Default SCIP satisfies (M_b) | (first version) | withdrawn: its minor separator is outside the class |

## 11. Limitations and open problems

- **Model.**
  - Theorem 1 covers relaxations whose gap dominates termwise McCormick.
    Theorem 2 covers per-factor envelopes of the PROGRAM factorization.
  - Not covered, and able to remove the local mechanism:
    - PSD cuts on clique minors (Consequence A);
    - a split factorization for per-factor envelopes (Consequence B);
    - convexity detection on the aggregated sum;
    - objective-cutoff propagation.
  - A solver that recognizes that `f` is convex on `|x|_inf < 0.577` could
    prune every box inside that cube exactly. Theorem 1 still applies to the
    rest. Take `R = X0` (`x* = 0`) and discount the convex cube, whose volume
    fraction is `0.577^n`: the bound becomes `(1 - 0.577^n) 0.57 (5/3)^n`.
    This assumes the aggregated relaxation certifies only boxes inside the
    cube.
  - Branching on lifted variables is not covered, and neither are bounds
    taken from children unless the children are counted as leaves.
- **Constant.** The proved base 5/3 is below the observed 2.7–3.5 of
  termwise relaxations. The loss is in the covering step (Section 3).
- **Split factorizations.** Whether per-factor envelopes with a split
  factorization need exponentially many leaves outside the region where the
  split factors are convex is open.
- **Other graphs.** For general graphs only a sketch is given. The relation
  to treewidth is one-directional: the bound holds at treewidth 1, which is
  the point for the program. We did not look for matching lower bounds for
  decomposition-aware methods.
- **Theorem 2's constant** relies on a floating-point maximization over one
  variable. A symbolic proof like Lemma 3.1 should be possible but was not
  done.
- **Computations** are floating point.
  - Node bounds are certified by weak duality up to rounding. Pruned boxes
    are valid at `eps + 1e-12` (Section 7). The recheck's exact rational
    branch-and-bound reproduced the counts it tried.
  - The toy branch-and-bound is not SCIP.
  - The grid DP restricts split points. It gives an upper bound on `N_cert`,
    not `N_cert` itself.
  - Only two random seeds were used.
  - Runs not cited in the note were not repeated with certified bounds.
    Their first-version logs are in `logs/v1/`.
- **Literature.** See Section 9.4 and the program's audit (claim C1). The
  recheck verified the chordal-decomposition references.

## 12. Files and commands

All commands are run from this directory. Targeted runs only; no
project-wide checks. Set `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` for
parallel runs (the certified bounds use numpy and scipy).

| File | Purpose |
|---|---|
| `bounds.py` | evaluates Theorems 1, 2, Propositions 5.3, 6.1 and repository Theorem 3.1; `python3 bounds.py > bounds.log`; `python3 bounds.py upper > logs/upper_bound.log` (Proposition 5.5) |
| `checks.py` | orthant boxes, envelope chord bound, center inequality on grown boxes; `python3 checks.py > logs/checks.log`; Lemma 3.1: `python3 checks.py lemma31 > logs/checks_lemma31.log` |
| `chordal_checks.py` | Theorem 2 base, chordal split, split-factor convexity, clique-PSD exactness; `python3 chordal_checks.py > logs/chordal_checks.log` |
| `bb_path.py` | toy branch-and-bound with certified node bounds (`certified`, `relax_split`); `python3 bb_path.py rel rule kappa cmode eps n...` |
| `jobs_v2.txt`, `run_jobs_v2.sh` | the runs cited in the note, with certified bounds; log `logs/bb_runs_v2.log`; also `python3 bb_path.py mc bisect 0.0 zero 1e-6 2 3 4 5 > logs/bb_runs_v2_k0_eps1e-6.log` |
| `jobs_v3.txt`, `run_jobs_v3.sh` | the `mc`, `kappa = 0.1` runs with the final code; log `logs/bb_runs_v3_mc.log` (overrides v2); spot checks in `logs/bb_runs_v2_check.log` |
| `make_tables.py` | Section 7 tables from the certified logs; `python3 make_tables.py > logs/tables.md` |
| `run_grid_v2.sh`, `grid_dp.py` | grid-restricted minimal certificates with certified bounds; logs `logs/grid_dp_n{n}_{eps}.log` |
| `scip_runs.py`, `scip_jobs.txt`, `run_scip.sh` | SCIP runs; `logs/scip_runs.log`; `... noprop > logs/scip_noprop_EPS.log`; `python3 scip_runs.py KAPPA CMODE 1e-4 600 n... nominor > logs/scip_nominor_*.log` |
| `analyze_leaves.py` | leaf locations; `logs/leaves_a.log` (`mcx bisect 0.1 zero 1e-4 6 8`), `logs/leaves_c.log` (`... 1e-6 6`), `logs/leaves_abbS.log` (`abbS bisect 0.1 zero 1e-4 6 8`) |
| `summarize.py` | tables of Section 7; `python3 summarize.py > logs/summary.log` |
| `logs/v1/`, `jobs.txt`, `jobs2.txt`, `jobs3.txt`, `run_jobs.sh`, `run_jobs2.sh`, `run_jobs3.sh` | first-version runs (HiGHS values used for pruning), kept for reference |

Run notes:
- First version: the second batch (`run_jobs2.sh`) stopped early. Our manual
  `pkill` of the stalled `viol` runs also terminated `xargs`, and the missing
  runs were rerun in batch 3. The stalled `viol` runs with `mcx`, and with
  `mc` at `kappa = 0`, were stopped by hand. They are not repeated in
  `jobs_v2.txt` beyond `n = 3` and `n = 5` respectively.
- Revision: the first launch of `run_jobs_v2.sh` oversubscribed the shared
  machine through multithreaded BLAS. It was stopped and restarted with
  single-threaded BLAS and 14 workers. The job `mc viol 0.0 zero 1e-4 5` was
  stopped after 19 minutes; it is not cited.

## 13. Revision after review

The review ([`../reviews/face-exact-review.md`](../reviews/face-exact-review.md))
confirmed the proofs of Theorems 1 and 2 and of the propositions. It found
two wrong computational interpretations and several smaller issues. Every
item below was checked by us before the text was changed.

1. **Node bounds of `bb_path.py`.**
   - *Finding.* HiGHS's QP solver sometimes returned values up to `1.5e-4`
     above the exact bound on `kappa = 0`, `c = 0`. The McCormick auxiliaries
     were not tight: the counter `solver-too-high` in the new logs records
     returned values above the relaxation value at the returned point.
   - *Fix.* Pruning now uses a lower bound valid by weak duality
     (`bb_path.certified`): the separable dual function of the McCormick
     relaxation for `mc` and `mcx`, and a Frank–Wolfe bound for alphaBB. It
     is refined by dual ascent when the threshold lies between it and the
     value at a feasible point, with a Clarabel fallback, and uses a tie
     tolerance of `1e-12`.
   - *Two bugs of our own, found while rerunning.* The feasible-point value
     for `mc` with `kappa > 0` first used the true quartic instead of the
     secant, and dual ascent occasionally stalled on very thin boxes. Neither
     could make pruning invalid. Both were fixed, and the affected runs were
     redone (v3).
   - *Rerun.* Every run cited in the note was repeated. The corrected counts
     match the review's independent Clarabel bound (for example 38, 162, 522
     and 1562 leaves at `eps = 1e-6`, `n = 2..5`,
     `logs/bb_runs_v2_k0_eps1e-6.log`). The claim that "the slope
     falls at small `eps`" was an artifact and is removed (Section 7.5). The
     grid optimum at `n = 2`, `eps = 1e-6` is 12, not 10.
   - *A tie.* At `n = 2`, `eps = 1e-2`, 4 is the exact optimum under
     `LB >= f* - eps`. 56 grid boxes have bound exactly `-eps`. Rounding
     without the tie tolerance gives 5, which is also the optimum under a
     strict inequality (see item 5).
   - *Elsewhere.* At `eps = 1e-4` all cited counts changed by at most 0.8%.
     On seed 0 the rules `oracle`, `viol` and `vw` gained 1–73 leaves. The
     `mcx`, `kappa = 0` runs requested by the review are now logged (320 and
     962 leaves at `n = 4, 5`).
2. **SCIP.**
   - *Finding.* Default SCIP is outside (M_b): its minor separator adds PSD
     cuts. Rerun: with `separating/minor/freq = -1` we get 21 and 14,011
     nodes (`kappa = 0`, `n = 4, 8`), 529, 4367 and 36,081 (seed 0), and 134,
     1841 and 19,781 (`kappa = 0.1`, `c = 0`), as the review reported.
   - *Fix.* Removed: "SCIP should satisfy (M_b)" and "this fits Theorem 1".
     Added: Section 8 (rewritten) and Section 9.1, which explains the effect
     through the chordal decomposition. The explanation of the tolerance
     effect now says that `absgap` is a global stopping criterion.
3. **Summary and wording.**
   - The Summary counts leaves plus `2n` per tightening round.
   - Theorem 2 base 1.205 (1.2021 labelled conservative).
   - Proposition 5.3 now assumes (M^+).
   - Proposition 5.5 gives the monotonicity argument for binary bisection.
   - Proposition 5.2 assumes `W_i <= r`.
   - "Less than 1%" in Corollary 1.3 is corrected.
   - The "Other graphs" remark uses `2 eps''/Delta`.
   - Inherited cuts are dominated by the termwise relaxation, not "pointwise
     below" it.
   - Level-1 RLT is covered by (M_b).
   - The anisotropic form of Theorem 3.1 is stated.
   - The oracle rule's range is corrected to +55% to -17% on seed 0.
   - The claim "all counts above the bound by 10–2000" is corrected.
   - The remark on where the constant is lost now places the loss in the
     covering step.
   - The evidence for Conjecture 5.4 is recalibrated.
4. **Significance (new Section 9).** Theorem 1 is a statement about the
   termwise class, and it holds for a convex QP. Theorem 2 depends on the
   factorization.
   - Lemma 9.1 splits the Hessian into PSD `2x2` blocks (chordal
     decomposition). It gives two escapes: clique-wise PSD cuts are exact for
     the convex variant, and a split factorization makes per-factor
     envelopes exact near `x*`.
   - What remains globally is open. An alphaBB proxy for the split
     factorization, an upper bound on the envelope count, still grows by
     about 2.5 per variable.
   - The literature audit (C1) and the cluster-problem sources are cited.
   - The title now says "termwise McCormick".
5. **Recheck ([`../reviews/face-exact-recheck.md`](../reviews/face-exact-recheck.md)).**
   The recheck confirmed the revision. Its independent exact-rational
   branch-and-bound reproduced our counts with no flipped pruning decision.
   Small fixes, each checked before the text was changed:
   - **Tolerance.** Pruned boxes are valid at `eps + 1e-12` up to rounding.
     No exact node bound fell in that band (Section 7, Section 11).
   - **The `undecided` counter** records only nodes whose solver value was
     above the threshold. It is reworded in Section 7 and in the `bb_path.py`
     docstring.
   - **Logs and docstring.** The 1562-leaf run is now logged
     (`logs/bb_runs_v2_k0_eps1e-6.log`, rerun: 38, 162, 522, 1562). The stale
     `bb_path.py` docstring now describes the certified bound and the tie
     tolerance.
   - **The tie at `n = 2`, `eps = 1e-2`** is reworded: 4 is exact under the
     definition, 56 boxes have bound exactly `-eps`, and 5 comes from
     rounding or a strict inequality (Section 7.6).
   - **Section 9.**
     - Lemma 9.1 and Consequence B are credited to Griewank–Toint 1984
       (Theorem 4 and their local convexification), with Agler et al.
       Theorem 2.3 and Vandenberghe–Andersen Theorem 9.2 and Section 12.1.
     - "Convex exactly on the cube" became "largest centred cube on which
       every factor is convex".
     - "Near `x*`" now requires positive definite blocks, with the hypotheses
       stated. The cube radius is renamed `r_0`.
     - The claim that no leaf lies inside the cube is dropped (it is
       automatic under bisection).
     - The alphaBB proxy is labelled an upper bound on the split-envelope
       count (Sections 7.3, 9.3 and 13, and the status table).
     - SCIP's minor separator is cited from `sepa_minor.h`. "Fits" and
       "explains" are unified to "consistent with".
     - "Cited from memory" is removed.
   - **Summary.**
     - "every termwise toy count";
     - the grid optima are upper bounds that grow by 2.5–3.2 per variable,
       not evidence for a lower base;
     - "positive definite" instead of "PSD" in item 2.
