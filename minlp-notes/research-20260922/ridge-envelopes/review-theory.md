# Review of theory.md (ridge envelopes)

Date: 2026-09-22. Reviewer: independent adversarial review of
[theory.md](theory.md) as of this date, with [novelty.md](novelty.md) and
[numerical-verification.md](numerical-verification.md) as context. theory.md was
not edited. Probes: `code/review_probes.py`.

## Verdict in brief

The mathematics is sound. I found no wrong theorem and no wrong corollary
under the stated hypotheses. The issues are:

1. **Wrong word (minor).** In the concave-envelope sentence after Theorem 1,
   "the minimum of `sum_k p_k phi(t_k)` over convex majorants" should be
   "infimum". The `-sqrt` counterexample, reflected (`sigma = sqrt`, `x = 0`),
   shows that it is not always attained.
2. **Implementation caveat on cut validity (should be stated).** Validity of
   `h_{psi,pi}` on the whole box needs node values `y_k = psi(t_k)` of a
   *concave* `psi <= sigma`. A vector `y` that is only feasible for the Step 3
   program (an affine minorant on `Lambda`) gives a cut that is valid on
   `Delta_pi` but can fail elsewhere in `B` (probe P2). The concavity
   constraints must therefore hold exactly, not just to LP tolerance, when cuts
   are certified. The "certified segment by segment with univariate interval
   arithmetic" sentence omits this.
3. **Attainment in (D) is stated too weakly.** It holds whenever `p_0 > 0` and
   `p_n > 0`, that is, at every interior point of the (normalized) box, including
   points with ties. "All `p_k > 0`" excludes interior tie points for no reason.
4. **Small gaps with one-line fixes:** Step 1 versus general (non-atomic) laws;
   degenerate box coordinates `l_i = u_i` in the normalization; the sign
   sentence after Corollary 2 is vague, and mixed signs genuinely fail
   (probe P3); "linear" should be "affine" for `p^pi` and `h`; the convention
   for the "Lovász extension" when `G(emptyset) != 0`.
5. **Hypotheses.** Continuity of `sigma` can be weakened to lower
   semicontinuity with no change in the proof. Without lower semicontinuity,
   (P) = (D) fails (explicit example below).

## Claim-by-claim

### Setting and normalization — correct with fix

- Dropping `a_i = 0`: correct. Given `X_1` feasible for the reduced problem,
  `(X_1, x_2)` is feasible for the full problem with the same cost, and the
  reduced envelope composed with the projection is a convex minorant.
- Scaling and reflection: correct. The new data are `a'_i = |a_i| (u_i - l_i)`
  and the offset `b' = b + sum_{a_i>0} a_i l_i + sum_{a_i<0} a_i u_i = min_B (a^T x + b)`,
  so `I' = I - b' = [0, sum a']`.
- **Gap:** if `l_i = u_i`, the map `x_i -> l_i + (u_i - l_i) x_i` is not a
  bijection. **Fix:** also drop fixed coordinates and absorb `a_i l_i` into `b`.
  The code (`normalize`) already does this.
- Staircase data: correct. `x = sum p_k v_k`, `sum p_k = 1`, `t` strictly
  increasing, and `T_x` is the law of `a^T 1[U <= x]`. The law is independent
  of tie-breaking because tied indices get `p_k = 0`.

### Theorem 1, (P) and Step 1 — correct with a one-line fix

- Step 1 is correct. For continuous `f` on compact `B`, `conv(graph f)` is
  compact, and `conv(epi f) = conv(graph f) + R_+ e_{n+1}` is closed, so
  `vex f(x) = min{z : (x,z) in conv graph f}` with at most `n+2` atoms (`n+1`
  suffice on the lower boundary).
- **Gap:** `M_x` in Step 2 contains non-atomic laws, while Step 1 is stated for
  finitely supported ones. To conclude `vex_B f(x) = inf{int sigma dmu : mu in M_x}`
  one also needs `vex_B f(x) <= E f(X)` for every random `X` in `B` with
  `E X = x`. **Fix:** add "by Jensen's inequality for the closed convex function
  `vex_B f`, the minimum is also the infimum over all random `X`." The same
  sentence is needed for `vex_{Delta_pi}` in the localization remark, because
  `X = E[v_K | S]` need not be finitely supported.
- Attainment in (P) is correct. Laws on the compact `I` form a weakly compact
  set. `mu <=_cx T_x` is equivalent to equal means together with
  `int (s-c)_+ dmu <= int (s-c)_+ dT_x` for all `c`, which are weakly closed
  conditions. `int sigma dmu` is weakly continuous. The set is nonempty because
  it contains `T_x`.

### Step 2 — correct (and is Mao–Wang 2015, Prop. 3.2, as novelty.md says)

- (i) Supermodularity: `F(S+i) - F(S) = phi(a(S)+a_i) - phi(a(S))` is
  nondecreasing in `a(S)` by the three-slope inequality, and `a(S)` is monotone
  in `S` because `a >= 0`. This holds for every real-valued convex `phi` on
  `I`, **including `phi` convex on `I` only and discontinuous at an endpoint**.
  The interpolation bound on each Kuhn simplex and Jensen's inequality for the
  concave, continuous, piecewise-affine `L_F` need nothing more. `L_F` is
  concave on `[0,1]^n` because `L_F = F(emptyset) + Lovász(F - F(emptyset))`
  there. Conclusion: (i) is correct and proves the stronger statement for
  convex test functions on `I`.
- (ii) Strassen's theorem needs only finite first moments, which hold here
  because both laws are compactly supported. `K` is a measurable function of
  `T`, well defined a.s. because the `t_k` are distinct. `v_K` takes finitely
  many values, so `X = E[v_K | S] = sum_k P(K=k | S) v_k`. With a version of the
  conditional probabilities that is nonnegative and sums to 1 everywhere, `X`
  lies in `Delta_pi` surely, not just a.s. The identities `a^T X = S` and
  `E X = x` are correct.
- Remark (extension, not needed): if some `a_i = 0` are kept, the `t_k` can tie.
  Step 2(ii) still works if `K` is drawn given `T` among
  `{k : t_k = T}` with probabilities proportional to `p_k`. This is what makes
  the zero-coefficient case of Corollary 2 true (below).

### Step 3 — correct

- `F(lambda) = sigma(sum lambda_k t_k)` and `lambda -> sum lambda_k v_k` is an
  affine bijection onto `Delta_pi`. Correct.
- "Convex envelope = sup of affine minorants" holds at **every** point of
  `Lambda`, including the boundary, because `vex_Lambda F` is closed (proper,
  lsc; see Step 1) and a closed proper convex function equals the supremum of
  its affine minorants everywhere (Rockafellar, Thm 12.1). The affine minorants
  of `vex F` and of `F` coincide. The form `sum lambda_k y_k` is correct on
  `Lambda`.
- `psi_y` is defined and finite on all of `I` because `I = [t_0, t_n]` for
  every `pi`, and it is a maximum of a linear function over a nonempty
  polytope. It is the upper concave hull of `(t_k, y_k)` on `[t_0, t_n]`,
  concave (its hypograph is a projection of a polyhedron), `<= sigma`, and
  `psi_y(t_k) >= y_k`. The converse direction is also correct.
- Attainment when all `p_k > 0`: correct. **Stronger statement:** attainment
  holds whenever `p_0 > 0` and `p_n > 0` (equivalently `0 < x_i < 1` for all
  `i` after normalization). Proof: let `K+ = {k : p_k > 0}`. It contains `0`
  and `n`, so the upper concave hull of `(t_k, y_k)_{k in K+}` is defined on all
  of `I`. The set of `y_{K+}` whose hull lies below `sigma` is closed (an
  intersection of half-spaces). It is bounded above by `y_k <= sigma(t_k)`, and
  bounded below along maximizing sequences. The hull of an optimal `y_{K+}` is
  an optimal `psi`. The failure example needs `p_0 = 0` or `p_n = 0`, as at
  `x = 0`.
- Boundary counterexample: correct. `psi_eps(s) = -eps - s/(4 eps) <= -sqrt(s)`
  by AM–GM, so the supremum is 0. A concave `psi <= -sqrt` with `psi(0) = 0`
  would satisfy `psi(s) >= (s/A) psi(A)`, which is `O(s)` and exceeds `-sqrt(s)`
  near 0.

### Step 4, `g_psi` and the cuts `h_{psi,pi}` — correct

- `G(S) = psi(a(S))` is submodular (same argument as Step 2(i)). With
  `G' = G - psi(0)`, `g_psi = psi(0) + L_{G'}` on `[0,1]^n`. This uses
  `sum_k p_k = 1`, which holds with the convention `x_pi(0) = 1`.
- The worry about "only on the nonnegative orthant" does not apply. The
  identity `L_{G'}(w) = max{s^T w : s in B(G')}` over the **base** polytope
  holds for all `w in R^n` (Edmonds; see Bach, *Learning with Submodular
  Functions*, 2013, Sec. 3; I did not recheck the proposition number). The restriction to
  `w >= 0` concerns the submodular polyhedron `P(G')`. In either case
  `[0,1]^n` lies in the orthant. Monotonicity of `G` is not needed. Each
  greedy vector `s^pi` with `s^pi_{pi(j)} = psi(t_j^pi) - psi(t_{j-1}^pi)` is in
  `B(G')`, so `h_{psi,pi}(y) = psi(0) + (s^pi)^T y <= g_psi(y)` for all
  `y in [0,1]^n` (indeed for all `y in R^n`, reading `g_psi` as
  `psi(0) + L_{G'}`).
- The Abel-summation identity `h_{psi,pi}(y) = sum_k p_k^pi(y) psi(t_k^pi)`, with
  `p_k^pi(y) = y_pi(k) - y_pi(k+1)`, `y_pi(0) = 1` and `y_pi(n+1) = 0`, is
  correct.
- `g_psi <= f` follows from Jensen's inequality on a finite law. Concave `psi`
  need not be continuous at the endpoints of `I`, and nothing uses continuity.
- Probe P1: 200 random non-monotone concave `psi` with `psi(0) != 0`, `n = 3`,
  all 6 permutations, 4000 random points plus the vertices. Results:
  `max(h - g) = 7e-15` and `max(g - f) = 0`.
- **Terminology fix:** say "the staircase (Kuhn) interpolation of
  `S -> psi(a(S))`, equal on `[0,1]^n` to `psi(0)` plus the Lovász extension of
  `G - psi(0)`". The standard Lovász extension assumes `G(emptyset) = 0` and is
  positively homogeneous; `g_psi` is not.
- **Wording fix:** `p^pi` and `h_{psi,pi}` are *affine*, not linear.
- **Implementation caveat (important for cut generation):** the cut must be
  built from node values of a concave `psi`. If `y` is only feasible for the
  Step 3 program, then `h_y(z) = sum_k p_k^pi(z) y_k` is still `<= f` on
  `Delta_pi`, where `p^pi >= 0`. Outside `Delta_pi` some `p_k^pi(z) < 0`, and a
  low `y_k` makes `h_y` too large. Probe P2 uses `sigma(s) = s`, `a = (1,1)`,
  and `y = (0, -10, 2)`. This `y` is `Lambda`-feasible, but `h_y(0,1) = 12 > f(0,1) = 1`.
  Hence:
  - In "Computing (D)", the concavity inequalities must hold exactly for the
    returned `y`. A cheap exact repair of a numerically returned `y` is
    `psi = min_k l_k`, where `l_k` is the line through `(t_k, y_k)` and
    `(t_{k+1}, y_{k+1})`. It is concave, and it is `<= sigma` whenever every
    segment chord is. The cut then uses `psi(t_k) <= y_k`.
  - The sentence "validity requires only feasibility of `psi`, which can be
    certified segment by segment with univariate interval arithmetic" should
    add: "and the (linear, exact) concavity inequalities on `y`".
  - The numerical code imposes concavity only up to Gurobi's feasibility
    tolerance of 1e-9. This is harmless at the reported accuracy, but it is
    not a certificate.
- `vex_B f = sup_psi g_psi` is correct pointwise. Each `g_psi` is a convex
  minorant, and at each `x` the supremum equals (D), which equals `vex_B f(x)`.
  The supremum is not always attained (boundary example).
- "Optimality in (D) gives the deepest cut at x": correct, provided `pi` is
  consistent with the order of `x`. For such `pi`, `h(x) = g_psi(x) = vex_B f(x)`,
  and no valid affine underestimator can exceed `vex_B f(x)`. State the proviso.

### Remark on ties — correct; can be sharpened

For every `pi` consistent with `x`, `x in Delta_pi`, and the positive
barycentric weights sit on the same node values. So every such
`h_{psi,pi}` is valid **and tight at `x`** (`h(x) = g_psi(x)`). The node
values at zero-weight nodes differ between permutations. Take them from the
same concave `psi`, for example the piecewise-linear interpolant of the solved
nodes.

### Concave-envelope sentence — wrong word

"the minimum of `sum_k p_k phi(t_k)` over convex majorants": replace with
"infimum". It is attained when `p_0, p_n > 0`. It is not attained for
`sigma = sqrt(s)` at `x = 0`.

### Computing (D) — correct

- Equivalence: (⇐) the piecewise-linear interpolant is itself a feasible
  `psi`. (⇒) The node values of a concave `psi` have nonincreasing slopes, and
  each chord lies below `psi`, hence below `sigma`. Correct, for strictly
  increasing `t`, which holds.
- The program is a semi-infinite LP with `n+1` variables. "Convex program" is
  correct. The adjacent-segment chord constraints suffice only together with
  concavity; without concavity the `Lambda` constraints would involve all
  pairs of nodes. This is fine as written.
- Convex `sigma`: correct, including the "(when one exists)" caveat.
- Concave `sigma`: correct, since `sigma` is feasible and dominates every
  feasible `psi`.
- S-shaped and multi-inflection bullets: no mathematical claim, so nothing to
  check. The earlier unproven "one tangent line" claim flagged in novelty.md
  is no longer in the text.

### Corollary 2 (order polytopes) — correct for `a > 0`; sign sentence needs a precise statement

- Tie-breaking by a linear extension of `Q` gives a `pi` that is a linear
  extension of `Q`. If `i <_Q j`, then either `z_i > z_j`, and `i` precedes
  `j` by value, or `z_i = z_j`, and the tie-break places `i` first. So each
  `v_k` is the indicator of a down-set, and `v_k in O(Q)`.
  `Delta_pi ⊂ O(Q) ⊂ B` gives the sandwich, and Step 2(ii) closes it. Correct.
- Probe P4 uses a non-chain poset (zigzag `z1 >= z3`, `z2 >= z3`, `z2 >= z4`),
  12 instances with `sin` and `s^3 - 3s`, and a grid LP over `O(Q)` (11 points
  per axis). The grid value is always `>=` the Theorem 1 value, with gaps from
  0 to 3.4e-5 R, consistent with grid resolution. This is the first test of a
  general poset; numerical-verification.md tested only chains.
- **Sign sentence:** "the sign condition is on the coordinates in which `Q` is
  an order" is unclear. Replace with:
  - "Corollary 2 holds for `a >= 0`. With zero coefficients it still holds:
    use the randomized `K` in Step 2(ii). Coordinates cannot simply be dropped,
    because `O(Q)` is not a product. Probe P5 checks the chain `z1 >= z2 >= z3`
    with `a = (1, 0, 2)`; the grid-LP gaps are between 0 and 9e-5.
  - It holds for `a <= 0` by the global reflection `z -> 1 - z`, which maps
    `O(Q)` onto `O(Q^op)`.
  - It fails in general for mixed signs." Counterexample (probe P3): the chain
    `z1 >= z2`, `a = (1,-1)`, `sigma(s) = -s^2`, and `z = (1/2, 1/2)`. The point
    lies on the edge `z1 = z2` of the triangle `O(Q)`, and `f = 0` on that edge,
    so `vex_{O(Q)} f(z) = 0`, while `vex_box f(z) = -1`.

### Corollary 3 (products of simplices) — correct

- The tail-sum map is linear. Its inverse is `x_1 = 1 - z_1`,
  `x_i = z_{i-1} - z_i`, `x_r = z_{r-1}`, and `x >= 0` is equivalent to the
  chain inequalities, so the map is a bijection of the simplex onto the chain
  polytope.
- `sum_i (c_{i+1} - c_i) z_i = sum_m x_m (c_m - c_1)`, so
  `c^T x = c_1 + sum_i (c_{i+1} - c_i) z_i`. The increments are positive by
  strict ordering. The product of chains is `O(disjoint union of chains)`.
  Correct.
- Merging equal values is correct but unproven in the text. One-line proof:
  split each merged weight in the fixed proportions of `x`. This is a linear
  lift `L` with `L(P x) = x` that maps the merged simplex into the original, so
  decompositions lift. Alternatively, keep equal values and use `a >= 0` with
  the randomized `K`.
- Comonotone description: in chain coordinates, block `j` takes the value
  `c_{j,m}` with `m = 1 + #{i : U <= z_{j,i}}`. This is a nonincreasing
  function of `U` with law `sum_i x_{j,i} delta_{c_{j,i}}`, so it equals
  `Q_j(1-U)`. All blocks use the same `U`, so the sum is a comonotone sum.
  Correct.
- "Mixed domains are covered in the same way": correct for box coordinates
  (singleton chains; any sign, by reflection) and one-hot blocks (any values).
  For extra order constraints among box variables, the sign restriction of
  Corollary 2 applies. Say so.

### Regularity of `sigma`

- **Lower semicontinuous `sigma` suffices; the proof is unchanged.** For `f`
  lsc and bounded below on compact `B`, `conv(epi f)` is closed. In the
  limiting argument, atoms whose weight tends to 0 contribute at least
  `lambda * min f -> 0`. This gives Step 1 with minima. `mu -> int sigma dmu` is
  weakly lsc (portmanteau), so (P) is attained. `vex_Lambda F` is closed, so
  Step 3 holds. Steps 2 and 4 do not use continuity.
- **Without lower semicontinuity, (P) = (D) fails.** Take `n = 1`, `a = 1`,
  `I = [0,1]`, `sigma(0) = 1` and `sigma = 0` on `(0,1]`. Then `vex_B f` is 1
  at 0 and 0 elsewhere (this function is convex), so (P) = 1 at `x = 0`. But a
  concave `psi <= sigma` has `psi(0) <= liminf_{s->0+} psi(s) <= 0`, so
  (D) = 0. The identity `vex_B f = sup_psi g_psi` also fails there.
- `sigma` defined only on `I` is all that is used. `psi` is required to be
  concave and real-valued on `I`, and may jump down at the endpoints of `I`,
  which is harmless.

## Probes run (targeted)

```
cd code && ~/miniconda3/envs/exact-quadratic-hull/bin/python review_probes.py   # 12 s
```

Output summary: P1 `max(h-g) = 7.1e-15`, `max(g-f) = 0`. P2 `h(0,1) = 12 > f = 1`
for a `Lambda`-feasible, nonconcave `y`. P3 `vex_{O(Q)} = 0` versus
`vex_box = -1`. P4 the grid LP over the zigzag `O(Q)` minus Theorem 1 lies in
`[0, 3.4e-5] R`. P5 the zero-coefficient chain gives grid minus box envelope in
`[0, 9.2e-5]`. No CI checks were run or consulted.
