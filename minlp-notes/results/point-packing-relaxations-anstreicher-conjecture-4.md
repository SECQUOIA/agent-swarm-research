# Exact values of RLT and SDP relaxations of point packing: proof of Anstreicher's Conjecture 4

Status (independent agent audit, 2026-09-04): the four main formulas and their
constructions are correct after the corrections recorded below. **These are known results,
not new results of this project.** Khajavirad (2024), Proposition 1(i–ii) and Proposition 3,
proves the same values, including redundancy of RLT for the SDP relaxations. The proofs
below remain useful as a short self-contained derivation. This was an independent
mathematical audit by another agent, not journal peer review or formal verification.

Sources: Anstreicher, “Semidefinite programming versus the reformulation-linearization
technique for nonconvex quadratically constrained quadratic programming,” J. Global Optim.
43:471–484 (2009), Section 4; local original checked at
[[anstreicher2009-semidefinite-programming-versus-the-reformulation]] p.12.
Khajavirad, “The circle packing problem: A theoretical comparison of various
convexification techniques,” Operations Research Letters 57, 107197 (2024),
[DOI](https://doi.org/10.1016/j.orl.2024.107197),
[open preprint, Propositions 1 and 3](https://arxiv.org/html/2404.03091v1).
The open preprint was checked on 2026-09-04; its reflection to the lower-left quarter
is equivalent to the upper-right convention used here.

Audit corrections: removed the false statement that Anstreicher leaves rounding implicit;
corrected the opening two-dimensional averaging bound (which previously missed a factor
of two); required `k ≥ 2`; replaced an undefined symbol in Lemma 1; and qualified the
application discussion. The numerical table was subsequently reproduced with the corrected
solver script on 2026-09-04. Solver checks and the earlier exact rational checks are recorded below.

## Setting

Point packing (equivalent to packing `n` equal circles in the unit square):

```
PP:  max θ  s.t.  (x_i − x_j)² + (y_i − y_j)² ≥ θ  (1 ≤ i < j ≤ n),   x, y ∈ [0,1]^n .
```

Relaxations replace `x_i x_j` by `X_ij` and `y_i y_j` by `Y_ij` (no `x_i y_j` terms occur), and the
pair constraints become `D_ij := (X_ii − 2X_ij + X_jj) + (Y_ii − 2Y_ij + Y_jj) ≥ θ`.

- RLT (Anstreicher's Section 2): for bounds `l ≤ x ≤ u` the four products of bound constraints,
  `X_ij ≥ l_i x_j + l_j x_i − l_i l_j`, `X_ij ≥ u_i x_j + u_j x_i − u_i u_j`,
  `X_ij ≤ l_i x_j + u_j x_i − l_i u_j`, `X_ij ≤ u_i x_j + l_j x_i − u_i l_j` (also for `i = j`); same for `Y`.
- SDP: `X ⪰ xxᵀ`, `Y ⪰ yyᵀ`, plus the diagonal bounds `X_ii ≤ (l_i+u_i)x_i − l_i u_i` (which is
  `X_ii ≤ x_i` on `[0,1]`).
- SYM: the bounds `x_i ∈ [1/2, 1]` for `i ≤ n_x = ⌈n/2⌉` and `y_i ∈ [1/2, 1]` for `i ≤ n_y = ⌈n_x/2⌉ = ⌈n/4⌉`
  (these ceilings are explicit in the original paper, p.12). SYM also updates the RLT
  products and SDP diagonal secants to use the tightened bounds. Merely adding the
  bounds on `x,y` while retaining the old secants does not give these values.

Conjecture 4 (Anstreicher 2009, verified numerically there for `n ≤ 50`): (1) RLT value `= 2`;
(2) SDP value `= 1 + 1/(n−1)`, unchanged by adding RLT; (3) RLT+SYM value `= 1/2` for `n ≥ 5`;
(4) SDP+SYM value `= (1/4)(1 + 1/⌊(n−1)/4⌋)` for `n ≥ 5`.

## Lemma 1 (single-pair RLT bound)

For one coordinate with `x_i ∈ [l_i,u_i]`, `x_j ∈ [l_j,u_j]`, the largest value of `X_ii − 2X_ij + X_jj`
allowed by RLT is `D_ij(x) = (l_i+u_i)x_i − l_iu_i + (l_j+u_j)x_j − l_ju_j − 2 max(l_ix_j + l_jx_i − l_il_j,
u_ix_j + u_jx_i − u_iu_j)`, attained by taking `X_ii, X_jj` at their RLT upper bounds and `X_ij` at its
RLT lower bound. Since RLT couples different pairs only through the diagonal entries, which can be
at their upper bounds simultaneously, the RLT value equals `max_{x,y} min_{i<j} [D_ij(x) + D_ij(y)]`.
For a common interval `[l,u]` of length `L`, `D_ij(x) ≤ L²` with equality iff `x_i + x_j = l + u`
(for `L > 0`, the function is `L min(s − 2l, 2u − s)` in `s = x_i + x_j`; direct computation: on
`[0,1]`, `D_ij = min(s, 2 − s) ≤ 1`; on `[1/2,1]`, `D_ij = min(s/2 − 1/2, 1 − s/2) ≤ 1/4`).

## Theorem 1 (parts (1) and (3))

(1) The RLT value of PP is `2` for every `n ≥ 2`.
(3) The RLT+SYM value of PP is `1/2` for every `n` with `n_y ≥ 2`, i.e. `n ≥ 5`.

Proof. (1) Upper bound: by Lemma 1 every pair has `D_ij(x) + D_ij(y) ≤ 1 + 1 = 2`. Lower bound:
`x = y = (1/2)e` gives `D_ij(x) = D_ij(y) = 1` for all pairs, and the corresponding `X, Y`
(`X_ii = 1/2`, `X_ij = 0`) are RLT-feasible.

(3) Upper bound: the two points `i, j ≤ n_y` lie in the quarter square `[1/2,1]²`, so by Lemma 1
`D_ij(x) + D_ij(y) ≤ 1/4 + 1/4 = 1/2`. Lower bound: place the `n_y` quarter points at `(3/4, 3/4)`,
the `n_x − n_y` half points (`x ∈ [1/2,1]`, `y ∈ [0,1]`) at `(3/4, 1/2)`, and the free points at
`(1/2, 1/2)`. Lemma 1 gives, coordinate-wise: quarter–quarter `1/4 + 1/4 = 1/2`; quarter–half
`1/4 + 5/8 = 7/8`; quarter–free `5/8 + 5/8 = 5/4`; half–half `1/4 + 1 = 5/4`; half–free `5/8 + 1 = 13/8`;
free–free `1 + 1 = 2`. All are `≥ 1/2`, so the RLT+SYM value is at least `1/2`. ∎

(For `n ≤ 4`, `n_y ≤ 1` and the value is larger: numerically 2, 1.2, 1.2 for `n = 2, 3, 4`.)

## Theorem 2 (parts (2) and (4), and the general averaging bound)

Let `k ≥ 2` points be confined to a box `[l, l + L]^2`, where `L ≥ 0`, in the SDP
relaxation, with diagonal bounds `X_ii ≤ (2l + L)x_i − l(l+L)` and the corresponding
bounds for `Y`. Then

```
avg_{i<j} D_ij ≤ L² k/(k−1).
```

To prove this, restrict `x,X` to these `k` indices and let `e` be the `k`-vector of ones.
Positive semidefiniteness of `X − xxᵀ` implies

```
Σ_{i<j} (X_ii − 2X_ij + X_jj)
  = k Σ_i X_ii − eᵀXe
  ≤ k[(2l+L)Σ_i x_i − kl(l+L)] − (Σ_i x_i)²
  = kLs − s²
  ≤ k²L²/4,                       s = Σ_i(x_i−l).
```

Dividing by `k(k−1)/2` gives the per-coordinate average bound `L²k/[2(k−1)]`.
Adding the two coordinate bounds proves the displayed bound. The minimum distance
is at most this average, so the SDP value is at most `L²k/(k−1)` whenever a subset
of `k` points shares this box.

(2) With `L = 1`, `k = n`: SDP value `≤ 1 + 1/(n−1)`. Attainment: `x = y = (1/2)e`,
`X = Y = (1/4)eeᵀ + Z`, `Z = (1/4)·(n/(n−1))·(I − eeᵀ/n) ⪰ 0`. Then `X_ii = 1/2 = x_i` (diagonal bound
tight), `X_ij = 1/4 − 1/(4(n−1))`, and every pair has `D_ij = 2(Z_ii − Z_ij) = (1/2)(1 + 1/(n−1))` per
coordinate, `1 + 1/(n−1)` in total. This point also satisfies all RLT inequalities (`X_ij ∈ [0, 1/2]`
and `X_ij ≥ x_i + x_j − 1 = 0`), so SDP+RLT has the same value.

(4) With SYM and `n_y ≥ 2`: the `k = n_y` quarter points share `[1/2,1]²` (`L = 1/2`), so the
SDP+SYM value is `≤ (1/4)(1 + 1/(n_y − 1))`, and `n_y − 1 = ⌈n/4⌉ − 1 = ⌊(n−1)/4⌋`, which is
Anstreicher's expression. Attainment: put the quarter points at `(3/4,3/4)` with the scaled
construction `Z_Q = (1/16)(k/(k−1))(I − eeᵀ/k)` in both coordinates (diagonal bound
`X_ii ≤ (3/2)x_i − 1/2 = 5/8` is tight: `9/16 + 1/16`), the half points at `(3/4, 1/2)` with
`Z = (1/16) I` in `x` and `(1/4) I` in `y`, and the free points at `(1/2,1/2)` with `Z = (1/4) I` in both
coordinates; take `Z` block-diagonal across the three groups. All diagonal bounds hold, `X ⪰ xxᵀ`,
and the pair values are: quarter–quarter `(1/4)(1 + 1/(k−1))`; quarter–half `1/8 + 3/8 = 1/2`;
quarter–free `3/8 + 3/8 = 3/4`; half–half `1/8 + 1/2 = 5/8`; half–free `3/8 + 1/2 = 7/8`; free–free `1`.
All are `≥ (1/4)(1 + 1/(k−1))` because `k ≥ 2`. The point satisfies the RLT inequalities as well
(cross-group `X_ij = x_i x_j`; within the quarter group `X_ij = 9/16 − 1/(16(k−1)) ∈ [1/2, 5/8]`), so
SDP+SYM+RLT has the same value, as observed numerically. ∎

## Numerical confirmation (`code/point_packing/pp_relaxations.py`)

| n | RLT | SDP | SDP+RLT | 1+1/(n−1) | RLT+SYM (ceil) | SDP+SYM (ceil) | (1/4)(1+1/⌊(n−1)/4⌋) |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | – |
| 3 | 2 | 1.5 | 1.5 | 1.5 | 1.2 | 1.235 | – |
| 4 | 2 | 1.3333 | 1.3333 | 1.3333 | 1.2 | 1.219 | – |
| 5 | 2 | 1.25 | 1.25 | 1.25 | 0.5 | 0.5 | 0.5 |
| 6–8 | 2 | 1.2, 1.1667, 1.1429 | same | same | 0.5 | 0.5 | 0.5 |
| 9–12 | 2 | 1.125 … 1.0909 | same | same | 0.5 | 0.375 | 0.375 |
| 13, 14 | 2 | 1.0833, 1.0769 | same | same | 0.5 | 0.3333 | 0.3333 |

The corrected script defaults to the published `conv="ceil"` convention and checks
`n=2,…,14`. Its output compares computed values with all four actual Conjecture 4
formulas; the two SYM formulas display `n/a` for `n<5`. The table above summarizes
the rerun output. The run used Gurobi for LPs and Clarabel through CVXPY for SDPs in
the `minlp-notes` conda environment. All applicable formula comparisons passed with
absolute and relative tolerances `10⁻⁶`, including SDP+RLT for `n≥2` and
SDP+SYM+RLT for `n≥5`. These are floating-point solver checks, not exact certificates.
The script rejects nonoptimal solver status, including `optimal_inaccurate`, and
nonfinite objectives before reporting a value. The optional explicit `floor` and
`round` conventions are exploratory variants and are not used by the default run.

Independent finite audit (2026-09-04): using Python `fractions.Fraction`, every entry of
the explicit SDP construction was checked against all four RLT inequalities, including
diagonal entries, and every pair distance was checked against the claimed optimum for
`n=2,…,100` without SYM and `n=5,…,100` with SYM. All checks passed. Positive
semidefiniteness was checked analytically from the projection and diagonal block formulas;
the finite checks are supplementary evidence, not the proof for arbitrary `n`.

## Remarks

1. **General dimension.** The same argument gives, for `n` points in `[0,1]^d`: RLT value `= d`
   (vacuous) and SDP value `= (d/2)(1 + 1/(n−1))`, both attained at the centre with the
   construction above; more generally, `k` points confined to a common box of side `L` force the
   SDP value to at most `(dL²/2)(1 + 1/(k−1))`.
2. **Why the SDP bound is weak.** The upper certificate uses only a sum of pair
   inequalities, the diagonal secants, and the semidefinite inequality in the direction
   `e`. The feasible construction proves this certificate is sharp for the stated models.
   This is a variance/simplex averaging argument; no novelty is claimed for it.
3. **Ordering constraints are known territory.** This note does not prove the ORD
   formulas. Khajavirad (2024), Proposition 1(iii–iv), already gives the corresponding
   LP values for the ordered convexifications. The script's former unused `ord_` option
   was removed because it added only variable ordering, whereas Anstreicher's ORD also
   includes lifted products. The script does not implement ORD. Any comparison must
   match the exact product constraints before identifying formulations.
4. **PSE relevance and limits.** Unanchored max-min-distance QCQPs arise as simplified
   equipment-layout and sensor-placement models. The exact values here show that these
   particular relaxations retain a positive upper bound as `n` grows, although achievable
   minimum separation tends to zero in a bounded box. Additional valid inequalities,
   model-specific constraints, or branching are needed to close that gap. The formulas
   do not establish that any one strengthening strategy is indispensable, and they do
   not directly apply after adding equipment sizes, anchors, or process constraints.
