# Review: exponential lower bound for spatial branch-and-bound with separable relaxations

Reviewed file: `results/spatial-bb-exponential-lower-bound.md` (version dated 2026-09-04).
Review date: 2026-09-05. Numerical checks used for this review are described at the end.

## Verdict: PASS WITH CORRECTIONS

The core argument (Lemma 1, Steps 1-3, Proposition 2, the cover formulation) is
correct. Two statements in the file are wrong as written and must be fixed:

1. Theorem 1 states the bound with `max`; the proof gives `min`. The `max`
   form is false (explicit counterexamples below). The headline case
   `k = z = m = t` is unaffected because both terms coincide.
2. The Summary and Remark 6 claim exponential size for the family without
   restricting `k`. For fixed `k` (or fixed `n-k`) there is an explicit
   `O(n^{k+1})`-node certificate with `ε = 0`, so the exponential behaviour
   requires `k` and `n-k` both linear in `n`. The theorem itself is consistent
   with this once `max` is replaced by `min`.

A third, minor error is in Remark 3 (the RLT+SDP root certificate): the
justification `1/n <= d` is false for most `(n,k)`, and the claim itself fails
for `(n,k) = (2,1)`.

Everything else checks out. Issues are listed by severity, then the
point-by-point answers to the referee questions, then recommended text.

## Issues

### Issue 1 (major, statement error): `max` must be `min` in Theorem 1

Step 2 defines `ρ = max{((n-z)/n)^{h/2}, ((n-k)/n)^{h/2}}` and Step 3 gives
`#leaves >= 1/ρ = min{(n/(n-z))^{h/2}, (n/(n-k))^{h/2}}`. The theorem box
states `max{(n/(n-k))^{h/2}, (n/(n-z))^{h/2}}`, which is `1/min ρ`, not
`1/ρ`. The stronger `max` form is false:

- Cover version. Take `k = n-1`, `m = 1`, `z = 0`. The single box
  `[1/2,1]^n` has chord `ℓ_i(x) = (1-x)/2`, so `LB = (n - (n-1/2))/2 = 1/4`
  on `F`; it is ε-pruned for every `ε >= 0` and covers `F` (all of `F` has
  `x_i >= 1/2`). So one box suffices, but the `max` form asks for
  `n^{(1/4-ε)/1}` boxes, which exceeds 1 for `n >= 2`. (This box is exactly
  what feasibility-based tightening produces at the root, so Remark 2's cover
  claim is what makes this a genuine counterexample.)
- Tree version (no tightening). For `k = 1` the tree of Issue 2 below is an
  ε-certificate with `ε = 0` and `n(n+1)/2` leaves. With `m = z = (n-1)/2`
  and `ε = 0.01`, the `max` form requires `(n/(n-z))^{h/2} ≈ 2^{0.24 n}`
  leaves: at `n = 400` it requires `2.4·10^{14}` leaves, while the tree has
  `80200`. LP verification of all leaves was done for `n <= 50`; for larger
  `n` the pruning follows from the closed-form bound in Issue 2.

The `min` form is consistent with all of these (it evaluates to `1` when
`z = 0`, and to at most `e^{k/4}` when `k` is fixed).

### Issue 2 (major, overclaim): exponential size needs `k = Θ(n)` and `n-k = Θ(n)`

The Summary ("every spatial branch-and-bound tree ... has `2^{Ω(n)}` leaves")
and Remark 6 ("every off-the-shelf ... scheme ... needs exponentially many
nodes on this family") are stated for the whole family `P_n` with
`1 <= k <= n-1`. That is false for fixed `k`. Explicit certificate with
`ε = 0`: branch every coordinate at `1/2` in order `1, …, n`; a node with `c`
coordinates fixed to `[1/2,1]` and `d` fixed to `[0,1/2]` (the rest free) has

```
LB >= (c - k - 1/2)/2 >= 1/4   if c >= k+1   (since sum of high coordinates <= k+1/2),
LB >= (k + 1/2 - (n - d))/2 >= 1/4   if d >= n-k   (since sum of low coordinates >= k+1/2-(n-d)),
```

so prune as soon as `c = k+1` or `d = n-k`. Every remaining leaf at depth `n`
is also pruned (it has `c <= k` and `d <= n-k-1`, hence `c + d <= n-1 < n`, a
contradiction, so no such leaf exists). The number of nodes is
`O(n^{min(k, n-k)+1})`: for `k = 1` it is `n^2 + n - 1` nodes and
`n(n+1)/2` leaves (`2549` nodes, `1275` leaves at `n = 50`; all leaves
verified pruned by LP). The same construction with the roles of `0` and `1`
exchanged handles fixed `n-k`.

So the correct scope is: for `k`, `n-k` both `Θ(n)` (in particular
`k = n/3`) the size is `2^{Θ(n)}`; for `k = O(1)` or `n-k = O(1)` it is
polynomial. The theorem's `min` bound already reflects this (the second base
`(n/(n-k))^{h/2}` is bounded by `e^{k/4}` for fixed `k`), so only the prose
needs to change. This also sharpens the relevance remark: the hard instances
are those where the number of "full" units `k` is a constant fraction of `n`.

### Issue 3 (minor, side remark): Remark 3's RLT+SDP feasibility argument

The proposed point has `d = (k-1/2)(k+1/2)/(n(n-1))` and the constraint
`X_ij >= x_i + x_j - 1 = (2k+1-n)/n` must hold. The text argues "for
`n >= 2k` the right-hand side is at most `1/n <= d`". But `1/n <= d` is
equivalent to `n <= k^2 + 3/4`, which fails for most pairs (e.g. `(n,k) =
(5,2)`: `d = 3/16 < 1/5`). The constraint itself holds whenever
`n >= 2k+1` (right-hand side `<= 0 <= d`) and when `n = 2k` with `k >= 2`
(then the right-hand side is `1/(2k)` and `d = (2k+1)/(8k) >= 1/(2k)`), but
it fails for `(n,k) = (2,1)`: `d = 3/8 < 1/2`. For `(2,1)` the RLT+McCormick
relaxation alone is exact (objective `= 2X_12 - 3/4 >= 1/4`), so the claim
"RLT+SDP has value 0" is false there. The PSD computation and the RLT
equality `sum_j X_ij = (k+1/2)x_i` are correct; `0 <= d <= c` holds for all
`1 <= k <= n-1`.

The check script `check_rlt_sdp_root` only tests pairs where the claim holds
and would fail on `(2,1)`; it does not test the stated justification.

### Issue 4 (minor, scope clarification): fathoming rules and tolerances

The definition of ε-certificate is correctly implied by any run that fathoms
only by infeasibility or by `LB_g >= UB - ε` with `UB >= 1/4`. The
parenthetical about exact relaxation solutions is right and covers the
usual "relaxation solution is feasible and its objective matches the bound"
rule (then `LB_g = f(x*) >= 1/4`). A strict rule `LB_g > UB - ε` only
strengthens the leaf condition. Three things are not mentioned and are worth
one sentence each so a reader does not look for loopholes:

- Relative tolerances: with `UB = 1/4`, a relative gap `ε_rel` is an absolute
  `ε = ε_rel/4`, so the theorem applies for `ε_rel < 1`.
- Feasibility tolerance `δ` on the equality lowers the best incumbent to at
  least `1/4 - δ^2` (`x = 1_H + (1/2-δ)e_j`), so replace `ε` by `ε + δ^2`.
- Not covered: symmetry exploitation (orbital branching, `x_1 >= … >= x_n`
  constraints), branching on the auxiliary product variable `w_i = x_i y_i`
  (that region is not a box; note that `w_i <= θ` gives bound `0` and
  `w_i >= θ` is equivalent to a middle interval for `x_i`, so it does not
  help, but the theorem as stated does not cover it), and non-convex
  separable underestimators solved by MIP (piecewise-concave models), which
  are not bounded by the chord.

### Issue 5 (minor): Remark 2 and the root box

Feasibility-based tightening changes the leaf boxes and hence tightens their
chords; the statement "does not affect the count" is true only because the
theorem is applied in its cover form (every witness lies in `F`, and
tightening never removes points of `F`). The tree definition fixes the root
box as `[0,1]^n`, which a tightened run violates. Say explicitly that the
cover form is what is used. Note also that at the root no tightening is
possible when `1 <= k <= n-2`, and that for `k = n-1` tightening alone
certifies (see Issue 1), consistent with the `min` bound being `1` there.

### Issue 6 (trivial): Proposition 2 node count

The count sentence omits the intermediate upper children (`x_i in [α,1]`).
Exact count: root plus, for each `i = 1..n`, `2^{i-1}` nodes of each of the
four kinds (low, upper, middle, high), i.e. `1 + sum_{i=1}^n 2^{i+1} =
2^{n+2} - 3` nodes and `2^{n+1} - 1` leaves. The stated bound `2^{n+2}` is
correct. Verified for `n <= 7`.

### Issue 7 (trivial): Proposition 2 and strict fathoming

The middle child has `LB` exactly `1/4 - ε` (numerically `0.125` for
`ε = 1/8`), so it is ε-pruned under the `>=` definition but would not be
fathomed by a solver using a strict rule. Choosing `α(1-α) = 1/4 - ε + δ`
for small `δ > 0` fixes this; a footnote suffices.

## Point-by-point answers to the referee questions

1. **Lemma 1.** Correct. `F` is a nonempty compact polytope (`k+1/2 <= n-1/2`),
   a concave function attains its minimum at a vertex, a vertex has `n`
   linearly independent tight constraints of which at most one is the
   equality, and the two bounds of a coordinate cannot both be tight; so
   `n-1` coordinates are in `{0,1}` and the last is `k+1/2 - integer in
   [0,1]`, i.e. `1/2`. Every vertex has value exactly `1/4`. Verified by
   enumeration for `n <= 7`.
2. **Definitions.** The implication "complete run with separable relaxation
   and standard fathoming gives an ε-certificate" is correct, including for
   exactness-based fathoming and strict inequalities (see Issue 4). The
   incumbent is always `>= 1/4`, so any rule of the form `LB >= u - ε` (or
   `>`) with a feasible value `u` yields `LB >= 1/4 - ε`. No standard rule
   fathoms a node with `LB_g < 1/4 - ε`.
3. **Step 1.** `LB(B) <= sum_i ℓ_i(w_i)` holds because `w in B ∩ F`.
   `ℓ_i(1) = a_i·1 + (1-a_i-1) = 0` when `b_i = 1`; `ℓ_i(0) = a_i b_i = 0`
   when `a_i = 0`; on `[0,1]` the chord is `0 + 0·x`. `ℓ_i(1/(2m)) <=
   f(1/(2m)) = (1/(2m))(1-1/(2m)) < 1/(2m)`; sign of the terms is irrelevant
   because each is bounded above. `|M ∩ R| > 2m(1/4-ε) = h` follows, and
   `|A| + |D| >= |A ∪ D| >= |M ∩ R|`. Correct.
4. **Step 2.** `A`, `D` depend only on `B`. Under a uniform ordered partition,
   `Z` is a uniform `z`-subset and `H` a uniform `k`-subset. `C(n-s,z)/C(n,z)
   = prod_{j<s} (n-z-j)/(n-j) <= ((n-z)/n)^s` (with the product `0` when
   `s > n-z`). Every witness in `B` satisfies both events, so the fraction is
   at most the minimum of the two probabilities. Since `|A| > h/2` or
   `|D| > h/2` and the bases are in `(0,1]`, `min <= base^{h/2} <= max`.
   Boxes without witnesses contribute nothing to the count and are handled.
   The only defect is the `1/ρ` conversion in the statement (Issue 1).
5. **Step 3.** With `N` witnesses, `#leaves · ρN >= N`. Correct. Witnesses
   are distinct for distinct partitions because `0 < 1/(2m) < 1`.
6. **Proposition 2.** Middle child: `a_i + b_i = 1` gives the constant chord
   `α(1-α) = 1/4 - ε`; earlier coordinates have chords `(1-α)x` or
   `(1-α)(1-x) >= 0`, later ones `0`. Final leaves: chord sum equals `(1-α)`
   times the `ℓ_1` distance to the corner `c` with `c_i = 1` on the high set,
   and `‖x - c‖_1 >= |sum(x - c)| = |k+1/2-b| >= 1/2`. `(1-α)/2 > 1/4`.
   Node count `2^{n+2}-3 <= 2^{n+2}`. Correct (Issues 6, 7 are cosmetic).
7. **Remarks 2 and 3.** Remark 2 is correct in substance (Issue 5). Remark 3:
   PSD and RLT equalities are correct; the McCormick bound `X_ij >= x_i + x_j
   - 1` holds for `n >= 2k+1` and for `n = 2k`, `k >= 2`, but not for
   `(2,1)`, and the given justification is wrong (Issue 3).
8. **Constants.** `h = m(1/2-2ε)`, exponent `h/2 = m(1/4-ε)`, bases
   `(n-k)/n` and `(n-z)/n`, and the specialization `(3/2)^{t(1/4-ε)}`,
   `(3/2)^{n/24}` at `ε = 1/8` are all consistent with the proof. Only the
   `max`/`min` is inconsistent.
9. **Cover claim.** Correct: Step 3 uses only that every witness (a point of
   `F`) lies in some ε-pruned box. Disjointness, tree structure, and the
   root box are not used. This is exactly what makes Remark 2 work.

## Recommended text changes

1. Theorem 1 statement, replace

   ```
   max{ (n/(n-k))^{h/2}, (n/(n-z))^{h/2} }   leaves,   where  h = m(1/2 - 2ε).
   ```

   by

   ```
   min{ (n/(n-k))^{h/2}, (n/(n-z))^{h/2} }   leaves,   where  h = m(1/2 - 2ε).
   ```

   Optionally add after "In particular": "The bound is trivial when `z = 0`
   and bounded by `e^{k/4}` for fixed `k`; see Remark 7."

2. Summary, first paragraph: replace "every spatial branch-and-bound tree ...
   has `2^{Ω(n)}` leaves" by "every spatial branch-and-bound tree ... has
   `2^{Ω(n)}` leaves when `k` and `n-k` are both linear in `n` (for instance
   `k = n/3`)". Add at the end of the Summary: "The restriction on `k` is
   necessary: for fixed `k` (or fixed `n-k`) an `O(n^{k+1})`-node
   certificate exists (Remark 7)."

3. Add a Remark 7 with the polynomial certificate of Issue 2 (branch every
   coordinate at `1/2`; prune once `k+1` coordinates are in `[1/2,1]` or
   `n-k` are in `[0,1/2]`; the two displayed bounds on `LB`; node count
   `O(n^{min(k,n-k)+1})`; `ε = 0`).

4. Remark 6, replace "needs exponentially many nodes on this family" by
   "needs exponentially many nodes on this family when `k = Θ(n)` and
   `n-k = Θ(n)`", and replace "only relaxations coupling the variables
   through the constraint could avoid this" by "only relaxations coupling the
   variables through the constraint, or techniques outside the model such as
   symmetry exploitation, could avoid this".

5. Remark 3, replace

   ```
   `X_ij >= x_i + x_j - 1` (for `n >= 2k` the right-hand side is at most
   `1/n <= d`)
   ```

   by

   ```
   `X_ij >= x_i + x_j - 1 = (2k+1-n)/n` (for `n >= 2k+1` the right-hand side
   is nonpositive; for `n = 2k` it equals `1/(2k)` and `d = (2k+1)/(8k) >=
   1/(2k)` when `k >= 2`; for `(n,k) = (2,1)` the point is infeasible and the
   RLT relaxation is in fact exact)
   ```

   and change the lead-in "at the root box with `n >= 2k`" to "at the root
   box with `n >= 2k+1` (or `n = 2k`, `k >= 2`)". Update
   `check_rlt_sdp_root` in the script to assert the constraint directly for
   all `1 <= k <= n-1`, `n <= 12`, and to record the failing pair `(2,1)`.

6. Remark 2, append: "Both kinds of tightening change the leaf boxes; the
   theorem still applies because Step 3 uses only that the leaf boxes cover
   `F`, and tightening never removes a point of `F`. (At the root, no
   feasibility-based tightening is possible for `1 <= k <= n-2`; for
   `k = n-1` it shrinks the root to `[1/2,1]^n`, which is already pruned,
   consistent with the bound `1` of Theorem 1 for `z = 0`.)"

7. Setting, after the sentence on fathoming, append: "Relative gap
   tolerances `ε_rel` are absolute tolerances `ε_rel/4` here; a feasibility
   tolerance `δ` on the equality replaces `ε` by `ε + δ^2`. Symmetry
   exploitation, branching on auxiliary product variables, and non-convex
   (piecewise) separable underestimators are outside the definition."

8. Proposition 2, replace "The tree has `2^i` surviving nodes at depth `i`
   plus their pruned middle siblings, at most `2^{n+2}` nodes in total." by
   "Processing coordinate `i` creates `2^{i-1}` nodes of each of four kinds
   (low, upper, middle, high), so the tree has `1 + sum_{i=1}^n 2^{i+1} =
   2^{n+2} - 3` nodes and `2^{n+1} - 1` leaves." Optionally add: "If the
   solver fathoms only on a strict inequality, take `α(1-α) = 1/4 - ε + δ`."

9. Verification section: add a check that the `min` bound of Theorem 1 does
   not exceed the leaf count of the Remark 7 tree for several `(n,k)`, and a
   check that the Remark 7 leaves are pruned (LP) for `n <= 50`.

## Numerical checks performed for this review

Scripts in `/tmp/review/check.py` and `/tmp/review/check2.py` (conda env
`minlp-notes`, HiGHS via scipy):

- Lemma 1 by vertex enumeration, `n <= 7`, all `k`.
- Remark 3: exact rational check of `d >= 2c - 1` and of `1/n <= d` for all
  `1 <= k <= n-1`, `n <= 12`: the constraint fails only at `(2,1)`; the
  justification `1/n <= d` fails for every listed pair with `n >= 2k`.
- `LB([1/2,1]^n) = 1/4` for `k = n-1`, `n = 2,3,4` (cover counterexample to
  the `max` form).
- The `k = 1` and `k = n-1` trees of Issue 2: all leaves LP-verified pruned
  at `ε = 0` for `n <= 8` (both `k = 1, 2`), `n = 50` (`k = 1`), `n = 40`
  (`k = 39`); leaf counts versus the `max` and `min` forms at `n = 50, 100,
  200, 400`.
- Consistency of the `min` form with the counting tree at `k = n/3`,
  `n = 30, 60, 90`.
- Proposition 2 node and leaf counts, `n <= 7`; middle-child `LB` equals
  `1/4 - ε` to floating precision.

Provenance note (added after the 2026-09-24 repository audit): these `/tmp`
scripts and their output were not archived in the repository. The reviewer's
own runs above remain reviewer-reported and unarchived; they are distinct from
the committed author checkers in `code/spatial_bb_lower_bound/`.

Independent reproduction (2026-09-25): a new checker written from this list,
[`review_lower_bound_repro.py`](../code/spatial_bb_lower_bound/review_lower_bound_repro.py),
with saved output
[`review_lower_bound_repro-2026-09-25.log`](../code/spatial_bb_lower_bound/review_lower_bound_repro-2026-09-25.log),
reruns every item. It computes chord-LP bounds both exactly (rational greedy
solver) and with HiGHS, and does not reuse the author checker's code. Results:
all 741 vertices of `F` for `n <= 7` have value exactly `1/4`;
`LB([1/2,1]^n) = 1/4` for `k = n-1`, `n = 2,3,4`; all leaves of the Remark 7
trees are pruned at `ε = 0` for `n = 2..8` with `k = 1, 2`, for `(50,1)`
(`2549` nodes, `1275` leaves) and for `(40,39)`; at `ε = 0.01` with
`m, z ≈ (n-1)/2`, the `max` form requires about `2.2-2.4·10^14` leaves at
`n = 400` against `80200` tree leaves, while the `min` form stays below `1.3`;
at `k = n/3`, `n = 30, 60, 90`, the `min` form stays far below both the
Remark 7 and Proposition 2 leaf counts; Proposition 2 has `2^{n+2}-3` nodes
and `2^{n+1}-1` leaves for `n <= 7`, all leaves are pruned for every `k` at
`ε = 1/8`, and the smallest middle-child bound is `1/4 - ε` to floating
precision. The Remark 3 checks reproduce with two qualifications. The
constraint `d >= 2c-1` fails at `(2,1)` only among pairs with `n >= 2k`; over
all `1 <= k < n <= 12` it fails exactly at the 11 pairs with `k = n-1`, as the
result note states. The statement above that `1/n <= d` "fails for every
listed pair with `n >= 2k`" is not reproduced: among the 36 pairs with
`n >= 2k`, `n <= 12`, it fails at 22 and holds at 14 (for example `(4,2)`),
matching Issue 3's criterion `n <= k^2 + 3/4`. Issue 3's conclusion that the
justification is invalid is unaffected.
