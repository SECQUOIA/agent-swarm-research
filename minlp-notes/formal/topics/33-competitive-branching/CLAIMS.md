# Topic 33 claims

Source: Theorem 1 and its lemmas in
[competitive-branching.md](../../../research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md),
Sections 1 and 4. All declarations are in namespace `CompetitiveBranching`.
The [package README](README.md) states the model and the exclusions.

Common hypotheses of the `m`-formulation: `0 < α`, `0 < m` on `[L, U]`,
`IsCertificate m α L U N s`, and `MinRule m α L U t`.

| ID | Claim in the note | Lean declaration | Notes |
|---|---|---|---|
| C01 | Model (Sections 1.1–1.3): exact gap `q_B`, `phi_B = m - α q_B`, pruning iff `phi_B ≥ 0` on `B`, `R_min` splits at a relaxation minimizer, certificates | `q`, `phi`, `Valid`, `Tree`, `MinRule`, `IsCertificate` (`Model.lean`) | Leaves of a `MinRule` tree are unconstrained; any minimizer may be chosen |
| C02 | Pruning `LB(B) ≥ f* - eps` is `phi_B ≥ 0` with `m = f - f* + eps`, and minimizers of `f_B` and `phi_B` agree | `phi_shifted`, `valid_shifted_iff`, `isMinOn_shifted_iff`, `rminTree_iff`, `shifted_pos` (`Pruning.lean`) | Pruning is stated pointwise; `f*` need only be a lower bound of `f` on `[L, U]` |
| C03 | Validity passes to sub-intervals (Section 1.3) | `Valid.mono` (`Lemmas.lean`) | Needs `0 ≤ α` |
| C04 | `T = 2 (#internal nodes) + 1` | `Tree.size_eq` (`Model.lean`) | |
| C05 | Lemma 1(i): split points are interior | `node_facts` (`Lemmas.lean`) | Also gives `phi_B(y_B) < 0` |
| C06 | Lemma 1(ii): distinct internal nodes have distinct split points | `count_eq_le_one` (`Counting.lean`), `count_breakpoint_le_one` (`Theorem1.lean`) | Stated as: each point is a split point at most once |
| C07 | Lemma 1(iii): a split in `int J` forces a breakpoint of `J` into the node's interior | `count_zero_of_out` (`Counting.lean`) | Stated for whole subtrees |
| C08 | Lemma 1(iv): nodes whose interiors meet are nested | Built into the tree induction | Not a separate statement |
| C09 | Lemma 2 and its mirror | `key_left`, `key_right` (`Lemmas.lean`) | Proved under weaker hypotheses: `B₂` need not contain `s` |
| C10 | Proof steps 4–5: `|Y^LR|, |Y^L|, |Y^R| ≤ 1` | `count_left_zero`, `count_right_zero`, `count_le_one_of_right_out`, `count_le_one_of_left_out`, `count_le_three` (`Counting.lean`) | By induction instead of global classes |
| C11 | Theorem 1: at most 3 split points in the interior of each certificate interval, at most 1 in each end interval | `count_interval_le_three`, `count_first_interval_le_one`, `count_last_interval_le_one` (`Theorem1.lean`) | |
| C12 | Theorem 1: at most `4N - 5` internal nodes (`N ≥ 2`) | `internal_le` (`Theorem1.lean`); `theorem1` (`Pruning.lean`) for `f` | |
| C13 | Theorem 1: `T ≤ 8N - 9` (`N ≥ 2`) | `size_le` (`Theorem1.lean`); `theorem1` (`Pruning.lean`) for `f` | |
| C14 | If `N_opt = 1`, the root is pruned and `T = 1` | `eq_leaf_of_certificate_one` (`Theorem1.lean`) | |
| C15 | Leaves of every finished tree form a certificate; `T ≤ 8 N_opt - 9 < 4 T_opt` | `Partition.certificate`, `size_add_three_le`, `size_lt_four_mul` (`Competitive.lean`) | Compared with every finished tree, not only optimal ones |

Excluded, as listed in the README: existence of minimizers and run
semantics, Section 4.1 (node orders, incumbents, Corollary 1), the converse
direction of `T_opt = 2 N_opt - 1`, Section 4.2 sharpness, Propositions 0, 1
and 4, Theorems 2 and 3, and all `n`-dimensional statements.
