# Independent statement review of topic 33

Date: 2026-09-29. Scope: the six modules in
[`Formal/CompetitiveBranching`](../../../Formal/CompetitiveBranching), the
package [README](../README.md), [CLAIMS](../CLAIMS.md) and
[VERIFICATION](../VERIFICATION.md), and the
[axiom audit](../verification/AuditCompetitiveBranching.lean). Source:
Sections 1 and 4 of
[competitive-branching.md](../../../../research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md)
("the note") and the independent
[review of the note](../../../../research-20260928b/reviews/competitive-review.md).
The reviewer did not write the package and did not edit the Lean sources.
This review checks that the statements are faithful and sound. The proofs
themselves are checked by Lean.

## Verdict

The formal statements encode Theorem 1 of the note faithfully. Several are
slightly stronger than the note: they allow any minimizer at each node,
partial trees, any lower bound `f*`, and comparison with every finished tree.
No vacuity, loophole or soundness problem was found. All targeted checks
pass. Four documentation points and one optional addition are listed at the
end. None of them affects a Lean statement.

## Model definitions

- **`q`, `phi`, `Valid`.** These match the note exactly: `q_B(y) = (y - l)(u - y)`,
  `phi_B = m - α q_B`, and "valid" means `phi_B ≥ 0` on `B`.
- **`relax`, `Pruned`, `shifted` (`Pruning.lean`).**
  - `Pruned` is the pointwise test `f* - ε ≤ f_B(y)` for all `y ∈ B`. This is
    equivalent to `LB(B) = min_B f_B ≥ f* - ε`, since an infimum is at least
    `c` iff every value is.
  - `valid_shifted_iff` and `isMinOn_shifted_iff` are exact identities, and
    `rminTree_iff` is an equivalence. So `RminTree f α f* ε` and
    `MinRule (f - f* + ε) α` are the same predicate.
- **`Tree` and interval bookkeeping.** The root interval is a parameter. A
  node on `[l, u]` with split `y` has children on `[l, y]` and `[y, u]`. This
  is exactly a one-dimensional split, so every node's interval is determined.
- **`MinRule`.** Every internal node must be not `Valid`, and its split `y`
  must lie in `[l, u]` and minimize `phi` over `[l, u]`. The same holds
  recursively in both children. This is `R_min`, with the minimizer chosen
  independently at each node, so every tie-breaking rule is covered,
  including history-dependent ones.
  - *Unconstrained leaves are harmless.* The finished tree of any `R_min`
    run satisfies `MinRule`, so the bounds apply to it. They also apply to
    every partial tree. A single leaf is always a `MinRule` tree, but for an
    upper bound this is just the trivial case.
  - *`MinRule` is not vacuous.* The sanity file below builds a `MinRule`
    tree with three internal nodes.
  - *Degenerate intervals cannot be split.* If `u < l`, the condition
    `y ∈ Icc l u` fails. If `l = u` and `m l > 0`, the node is valid. Both
    facts are checked in the sanity file.
  - *Strict interiority follows; it is not assumed.* `MinRule` asks only
    `y ∈ Icc l u`. `node_facts` derives `l < y < u` from `m > 0` at the
    endpoints, as in Lemma 1(i). The positivity hypothesis is needed. With
    `m y = 5y - 1`, `α = 1` and root `[0, 1]`, the endpoint `0` minimizes
    `phi` on an invalid node, and `MinRule` accepts a split there (sanity
    file). The note has `m ≥ ε > 0`, so this case cannot arise there.
- **`IsCertificate`.** It requires `s 0 = L`, `s N = U`,
  `s j < s (j + 1)` and a valid piece `[s j, s (j + 1)]` for each `j < N`.
  This is a partition of `[L, U]` into `N` valid intervals of positive length.
  - Requiring strict increase loses nothing. Dropping zero-length pieces
    lowers `N`, which only strengthens the bound.
  - Only `s 0, ..., s N` are constrained, and every use stays in that range.
    `IsCertificate.cover` takes the least `k` with `y < s k`, which is at
    most `N`. The per-interval statements use `j < N` or `j + 1 = N`. So
    values of `s` beyond `N` are ignored consistently.
- **`internal`, `size`, `size_eq`.** `size` counts all nodes, the note's `T`,
  and `size_eq` gives `T = 2 · internal + 1`. In a partial tree, `size` also
  counts leaves whose relaxations have not yet been solved. This only
  over-counts, so the bound stays an upper bound.
- **`Partition` (the formal "finished tree").** Every split is strictly
  interior and every leaf is valid. Internal nodes may be valid.
  - A finished branch-and-bound tree under any split rule has these
    properties: splits are interior, and in a finished run every leaf is
    pruned, that is, valid.
  - Allowing splits of valid nodes only enlarges the class. So the comparison
    covers every finished tree, in particular an optimal one.
  - `Partition.certificate` turns a `Partition` tree into a certificate with
    `internal + 1` intervals. This is the note's direction from finished tree
    to certificate.
- **`LeavesValid`** is defined but not used by any theorem (see finding 3).

## The hypothesis on `f*`

`theorem1` assumes `fstar ≤ f` on `[L, U]` instead of `f* = min f`.

- The note's `f* = min f`, which exists for continuous `f`, satisfies this
  hypothesis. So `theorem1` specializes to the note's statement. The formal
  hypothesis is weaker, which is the correct direction.
- A smaller `fstar` lowers the threshold `fstar - ε`. That makes pruning
  easier, not harder. It does not matter here, because the run and the
  certificate use the same threshold.
- `Pruned` depends on `fstar` and `ε` only through `fstar - ε`. The two
  hypotheses `fstar ≤ f` and `0 < ε` enter the proof only through
  `0 < f - fstar + ε` on `[L, U]` (`shifted_pos`). That is the note's
  `m ≥ ε > 0`.

**Observation.** Because leaves are unconstrained, the model already covers
the incumbent remark of Section 4.1 (review of the note, Section 2.5).

- Suppose every incumbent satisfies `U_t ≤ f* + g` with `0 ≤ g < ε`.
- Each internal node was not pruned when it was processed. So
  `LB(B) < U_t - ε ≤ f* - (ε - g)`.
- Hence the node is invalid for `m' = f - f* + (ε - g) > 0`, and it splits at
  a minimizer of `phi'_B`.
- So the run's tree is a `MinRule` tree for `m'`. `internal_le`, applied with
  a certificate at tolerance `ε - g`, gives the Section 4.1 bound.

This is an instantiation argument, not a Lean statement. The README's
"not formalized" entry is therefore accurate.

## Main statements against the README and CLAIMS

The `#check` output of the audit file matches the statements printed in the
README. Each statement was compared with the note.

| Declaration | Formal statement | Assessment |
|---|---|---|
| `theorem1` | For `α, ε > 0`, `fstar ≤ f` on `[L, U]`, breakpoints `s` with every piece `Pruned`, and `2 ≤ N`: every `RminTree` has `internal ≤ 4N - 5` and `size ≤ 8N - 9` | Theorem 1 in the note's variables. Natural subtraction cannot truncate because `N ≥ 2` |
| `internal_le`, `size_le` | The same bounds for the `m` formulation, under `0 < m` on `[L, U]` and `IsCertificate` | Theorem 1, bullets 2 and 3 |
| `count_interval_le_three` | For each `j < N`, at most 3 internal nodes split in `Ioo (s j) (s (j + 1))` | Theorem 1, bullet 1 |
| `count_first_interval_le_one`, `count_last_interval_le_one` | At most 1 split in the first interval (`1 ≤ N`) and in the last interval (`j + 1 = N`) | Theorem 1, bullet 1, for the end intervals |
| `count_eq_le_one`, `count_breakpoint_le_one` | Every point is the split point of at most one internal node | Equivalent to Lemma 1(ii) |
| `count_zero_of_out` | If neither `a` nor `b` is interior to the subtree's root interval, no split lies in `(a, b)` | Lemma 1(iii) applied to the whole subtree. At a single node it is the contrapositive of the note's statement |
| `key_left`, `key_right` | Lemma 2 and its mirror | The README says these need weaker hypotheses, and that is correct. `key_left` assumes neither `l₁ < a` nor `l₂ < a`. It uses only `phi_{B₂}(y₂) < 0` at a point `y₂ ∈ B₂` with `a < y₂`. The identity `(y₁-l₁)(u₁-y₁) - (y₂-l₁)(u₁-y₂) + (y₂-l₁)(y₁-y₂) = (y₁-y₂)(u₁-y₁)` was checked by hand |
| `eq_leaf_of_certificate_one` | With `N = 1`, every `MinRule` tree is a leaf | The note's `N_opt = 1` case. It correctly needs neither `α > 0` nor `m > 0` |
| `size_add_three_le` | `t.size + 3 ≤ 4 * t'.size` for every `MinRule` tree `t` and every `Partition` tree `t'` | The note's `T ≤ 8 N_opt - 9 < 4 T_opt`, taking `t'` optimal. The unproved direction (certificate to tree) is not needed, because every finished tree is covered |
| `size_lt_four_mul` | `t.size < 4 * t'.size` | Ratio below 4 |

A detail about `size_add_three_le`: when `t'` is a node, the proof gives the
stronger bound `t.size + 5 ≤ 4 * t'.size`. The constant 3 is needed only when
both trees are single leaves, where `1 + 3 = 4`.

All rows C01–C15 of CLAIMS match their declarations.

## Findings

1. **Scope wording (README line 12, CLAIMS line 3).** Both say the package
   covers "Sections 1, 3 and 4" of the note. But Section 3 contains only
   Proposition 1, which the note says Theorem 1 does not depend on. The
   README also lists Proposition 1 as not formalized. Fix: "Sections 1 and 4".
2. **Index-shift sentence (README, Model, Certificate bullet).** "Indices are
   shifted by one from the note: the note's `J_j = [s_{j-1}, s_j]` is
   `[s (j - 1), s j]` here." In fact the breakpoint indices are the same in
   both. Only the interval indices shift. Suggested wording: "Breakpoint
   indices agree with the note. Interval indices are shifted by one: the
   note's `J_{j+1} = [s_j, s_{j+1}]` is interval `j` here, for `j < N`."
3. **Unused `LeavesValid` (Model.lean).** No theorem uses it; the README says
   it is defined "for completeness". It is harmless. Deleting it would remove
   an unused definition. If it is deleted, also remove its mentions in the
   README (the Model bullet and the Files list). Then rerun the targeted
   build and audit, and update the declaration count of 171 in
   VERIFICATION.md.
4. **Review status.** README lines 5–6 ("The Lean package itself has not been
   independently reviewed") and the topic-33 row of
   [`topics/README.md`](../../README.md) ("Lean package not independently
   reviewed") should cite this review once it is accepted.
5. **Optional.** The README's "Not formalized" entry for the Section 4.1
   incumbents could mention the instantiation argument in the observation
   above.

## Targeted checks run by the reviewer

All commands were run from `formal/` on the pinned Lean 4.33.1 and Mathlib.

1. Build of the six modules:

   ```sh
   LEAN_NUM_THREADS=4 lake build --wfail \
     Formal.CompetitiveBranching.Model Formal.CompetitiveBranching.Lemmas \
     Formal.CompetitiveBranching.Counting Formal.CompetitiveBranching.Theorem1 \
     Formal.CompetitiveBranching.Competitive Formal.CompetitiveBranching.Pruning
   ```

   Exit 0, `Build completed successfully (8711 jobs).` The build was cached,
   so each source was also elaborated directly (check 2).

2. Direct elaboration:

   ```sh
   for mod in Model Lemmas Counting Theorem1 Competitive Pruning; do
     LEAN_NUM_THREADS=4 lake env lean Formal/CompetitiveBranching/$mod.lean
   done
   ```

   Each run exited 0 and printed nothing, so there were no warnings.

3. Axiom audit:

   ```sh
   LEAN_NUM_THREADS=4 lake env lean \
     topics/33-competitive-branching/verification/AuditCompetitiveBranching.lean
   ```

   Exit 0, `PASS: audited 171 topic-33 declarations across 6 modules.` All
   12 printed axiom lists are `[propext, Classical.choice, Quot.sound]`. The
   four `#check` outputs match the README.

4. Source grep:

   ```sh
   grep -nE "\bsorry\b|^\s*axiom\b|admit|native_decide|implemented_by|@\[extern|unsafe|opaque" \
     Formal/CompetitiveBranching/*.lean
   ```

   No match (exit 1).

5. Kernel replay:

   ```sh
   for mod in Model Lemmas Counting Theorem1 Competitive Pruning; do
     LEAN_NUM_THREADS=4 lake env leanchecker Formal.CompetitiveBranching.$mod
   done
   ```

   Each run exited 0 and printed nothing.

6. Scratch sanity file `/tmp/cb_sanity/Sanity.lean`, kept outside the
   repository and not committed:

   ```sh
   LEAN_NUM_THREADS=4 lake env lean /tmp/cb_sanity/Sanity.lean
   ```

   Exit 0, with no output. The file uses constant `m = 1/30`, `α = 1`, root
   `[0, 1]`, and the tree that splits at `1/2`, then `1/4` and `3/4`. It
   proves the following.
   - The hypotheses can all hold at once, for a non-trivial tree:
     - `MinRule` holds for this tree, `Partition` holds for it, and
       `IsCertificate` holds with `N = 3` and `s j = j/3`.
     - `RminTree` holds for `f = 0`, `f* = 0`, `ε = 1/30`.
     - `internal_le`, `size_le`, `size_add_three_le` and `theorem1` all apply.
   - The per-interval counts are not trivially zero. The root split `1/2`
     lies inside the middle certificate interval, so that count is 1. The
     first interval also has count 1.
   - The degenerate cases hold: an empty or single-point node interval
     admits no `MinRule` split.
   - `node_facts` forces splits into the open interval.
   - Without `m > 0`, an endpoint split is possible (`m y = 5y - 1`).

The diff of `Formal.lean` was also inspected: it adds imports of the six
modules.

Not run: `scripts/verify.sh`, `scripts/check_imports.py`, the build of the
root `Formal` library, and `Verify.lean`. CI status and logs were not
inspected. CI performs the project-wide checks.
