# Review: powerflow0039p / 0039r leaf-bus extension (`open-instances-wave3/powerflow/extension-report.md`)

Date: 2026-09-30. This is an independent, adversarial review; I did not write the
extension. Scope: recompute the new certified bounds from the stored certificate data
with my own code, check the new cuts and the branching, and re-evaluate the primal
point p1. My scripts and logs are in
[`powerflow0039-review-checks/`](powerflow0039-review-checks/). Following `AGENTS.md`, I
ran only targeted checks: no project-wide verification, and no CI status or logs. All runs
were single-threaded and under `timeout`.

## Verdict

**Verified.** Both new bounds hold, and so do the rounded rational bounds that the report
cites:

- powerflow0039p ≥ 41869051484850140/10¹² = 41869.05148485014
- powerflow0039r ≥ 41869051483272433/10¹² = 41869.05148327244

I rebuilt every row of the relaxation from the OSIL files with my own reader. I
enumerated and checked the cut planes myself, and checked the leaf-box partition by a
different method from the author's. I re-evaluated every leaf Lagrangian in exact
rationals and proved the PSD part by a third method (high-precision Cholesky, then an
exact residual with a Gershgorin bound). No leaf bound fell short of its stored value.

This review also covers the report's dependency on the wave-3 relaxation (`pf_model`) for
every row these certificates use. That includes the 92 angle rows of 0039p, which the
wave-3 verifier (`wave3-verification/powerflow/pfv.py`) dropped.

I found three minor problems, none of which affects a bound (Section 7):

1. As logged, the fixed-leaf diagnostic value does not support the report's conclusion.
   A tight re-solve does.
2. One B&B log prints a wrong rational bound.
3. One "within 3e-3" statement is slightly off.

## 1. Relaxation R rebuilt from the OSIL (`own_osil.py`, `own_relax.py`, `cmp_rows.py`)

- I wrote my own OSIL reader, `own_osil.py`. It uses ElementTree, keeps exact
  Fractions of the decimal strings, and expands OSiL `mult`/`incr` arrays itself. It
  shares no code with `osilx` or `pf_model`.
- From this parse I built R independently. Its content matches the author's
  `pf_model.decode` output exactly:
  - 0039p: all 393 non-angle rows (184 flow, 92 limit, 78 linear, 39 voltage), the 20 y
    boxes, the y list, `vmax2` (Σ = 43.8204) and the objective.
  - 0039r: all 432 rows and the same boxes and objective.
  - The dropped rows are e580 (0039p, reference angle) and e396 (0039r, f_ref = 0).
    Dropping a row is always a valid relaxation.
- **Polar flow rows (0039p).** I converted each OSIL term c·v_a·v_b·cos/sin(θ_p − θ_q) and
  c·v_a² term by term with exact identities. My own v↔θ pairing came from the v² terms.
  I also evaluated the native OSIL expression against the converted quadratic at 3 random
  points in 60-digit arithmetic. The largest difference was 1.6e-58.
- **Polar angle rows (0039p, 46 bus pairs, 92 rows).** I read the intervals [A0, B0] for
  θ_p − θ_q from the OSIL myself. For each pair I checked the author's row structure
  (tb·w_R − w_I ≥ 0 and w_I − ta·w_R ≥ 0). With 300-bit interval arithmetic and exact
  rational comparisons I also checked that |A0|, |B0| < π/2, tb ≥ tan(B0) and
  ta ≤ tan(A0). The smallest margin was 1.0e-35. These rows are valid: w_R = v_p v_q cos δ
  > 0 and w_I = w_R tan δ.

## 2. Leaf identity and cuts (`leaf_struct.py`, `verify_leaves.py`)

- **Structure, read directly from the OSIL rows.** Bus 29 is (x30, x253) in 0039p and
  (x214, x253) in 0039r; bus 1 is (x2, x225) and (x186, x225). The rows that touch bus
  29 are:
  - the four flow rows of line 1–29 (e64, e65, e156, e157), each a pure susceptance
    b = 69060773480663/1250000000000 = 55.2486187845304, with no conductance, shunt or
    tap;
  - its voltage bounds [0.94, 1.06];
  - in 0039p only, the angle rows |θ₁ − θ₂₉| ≤ 0.26.

  The bus-29 balance rows are `x103 − x263 = 0` and `x195 − x273 = 0` (0039r: e397, e407).
  So bus 29 has no load or shunt, and Pg = x263 = P_{29→1} and Qg = x273 = Q_{29→1}. Pg
  carries 30·Pg + 100·Pg². The boxes are Pg ∈ [0, 52/5] and Qg ∈ [7/5, 4]. Hence
  Pg = s·b·w_I (s = +1 polar, −1 rectangular) and Qg = b(W_LL − w_R), as the report says.
- **Identity.** With sympy I checked Lagrange's identity
  W_NN·W_LL = w_R² + w_I², and that ((W_LL − Qg/b)² + Pg²/b²)/W_LL equals F. The Hessian
  of (p² + q²)/s has diagonal 2/s, 2/s, 2(p²+q²)/s³, its 2×2 principal minors are
  4/s², 4q²/s⁴ and 4p²/s⁴ (all ≥ 0), and its determinant is 0. So it is PSD, and F is convex on
  s > 0. At p1 the identity residual is 3.3e-15 (0039p) and −4.7e-15 (0039r), consistent
  with p1's rounding.
- **Cuts.** For every leaf box of all four runs I enumerated the vertex planes myself,
  using Cramer's rule with exact determinants. My list equals the author's
  `leafcut.planes3` list, which is needed only to align the stored multipliers; each box
  has 4 planes. I checked H ≥ F exactly at all 8 vertices of every plane. Since
  s1 ≥ 0.8836 > 0 and F is convex, H ≥ F on the whole box, so W_NN ≤ H is valid on R
  within the box. `leafcut.py` was last modified (08:28:58) after the last B&B run
  finished (08:27:44). But the current planes reproduce the stored bounds exactly (next
  section), so they are the rows the runs used.

## 3. Coverage of the root box (`verify_leaves.py: cover`)

This check does not use the author's volume-and-disjointness argument. All leaf-box
breakpoints, together with the root box ends, define a grid, and I checked that every
elementary cell lies in exactly one leaf box. I read the root box from my own rows:
Pg ∈ [0, 52/5], Qg ∈ [7/5, 4], W_LL ∈ [2209/2500, 2809/2500]. Every feasible point lies
in this box.

| run | leaves | grid cells, each in exactly one leaf |
|---|---|---|
| 0039p bb3 | 5 | 12 |
| 0039p bb3t | 6 | 16 |
| 0039r bb3 | 6 | 16 |
| 0039r bb3t | 9 | 45 |

Every leaf stores its own multipliers; none inherits a parent bound.

## 4. Leaf certificates recomputed (`verify_leaves.py`)

**Method.** For each leaf, the node rows are my rows in the author's row order, plus
VBL (s1 ≤ W_LL ≤ s2) and my cut rows, with Pg and Qg boxed to the leaf. I used
`pf_model` only for the row order. The Lagrangian is

obj + Σ_eq w(h − rhs) + Σ_ineq [m⁺(h − ub) + m⁻(lb − h)] = const + Σ_y (σy² + κy) + xᵀAx.

It is formed in exact rationals from the stored float multipliers. Negative inequality
duals would be clipped to 0; none occurred. The y part is minimized exactly over the boxes.
Every unboxed y had σ > 0 or κ = 0, so no multiplier adjustment was needed.

**PSD proof.** This is a different method from both `pf_cert`'s interval Cholesky and the
author's exact LDLᵀ.

1. Compute λ = λ_min(A) at 50 digits and set ε = max(0, −λ) + 1e-30.
2. Compute the Cholesky factor R of A + εI at 60 digits and round it to exact binary
   rationals.
3. Compute E = A + εI − RRᵀ exactly and take the Gershgorin bound g ≤ λ_min(E).
4. Then xᵀAx ≥ min(0, g − ε)·Σ vmax_k² on R.

Across all leaves, λ_min(A) ranged from −1.3e-7 to +1.4e-7.

| run | own minimum over leaves | stored LB | own − stored | cited rational bound |
|---|---|---|---|---|
| 0039p bb3 | 41869.0510497334 | 41869.05104582637 | +3.9e-6 | — |
| 0039p bb3t | **41869.051485240394** | 41869.05148485014 | +3.9e-7 | 41869051484850140/10¹² ≤ both: holds |
| 0039r bb3 | 41869.05119609605 | 41869.05119609605 | −4.4e-29 | — |
| 0039r bb3t | **41869.05148328967** | 41869.05148327244 | +1.7e-8 | 41869051483272433/10¹² ≤ both: holds |

- For every leaf of every run, my bound ≥ the stored bound − 4.4e-29. The 4.4e-29 is my
  own ε margin (1e-30 × 43.82), and it appears only on leaves where the author used ε = 0.
- The positive differences, up to 3.8e-5 on one 0039p bb3 leaf, come from the author's
  coarser ε list (10⁻⁹…10⁻⁶).
- My floors are 41869051485240391/10¹² (0039p) and 41869051483289675/10¹² (0039r). The
  report cites slightly smaller rationals, so its citations are valid.
- The gaps to obj(p1) are 2.647e-5 (6.3e-10 relative) for 0039p and 2.805e-5 (6.7e-10
  relative) for 0039r, as reported.

**Author's own checks.** I also re-ran them; the logs are `logs/author_verify_*.log`.
Both `verify_bb3.py` and `verify_exact.py` reproduce the report's statements on all four
runs. That covers the partition, the recomputed minima, L(p1) − bound, the exact-ε
choices, and the "exceeds by at most 4.4e-8" claim.

## 5. The primal point p1 (`p1_check.py`)

I evaluated p1 at 50 digits with my own reader. The one variable missing from the `.sol`
file (x254, the reference angle in 0039p and f_ref in 0039r) was set to 0.

| | 0039p | 0039r |
|---|---|---|
| obj(p1) | 41869.051511320199159 | 41869.051511320800473 |
| largest native OSIL row violation | 1.18e-12 (e178) | 7.91e-12 (e110) |
| Pg, Qg, v₂₉ at p1 | 6.71424469579, 1.4, 1.06 | 6.71424469578, 1.40000000000021, 1.06000000000001 |
| leaf with p1 (tight run): largest cut value − rhs | −4.5e-8 | −2.7e-10 |
| L(p1) − bound (tight run) | 5.23e-7 | 6.24e-7 |
| obj(p1) − L(p1) (tight run) | 2.59e-5 | 2.74e-5 |
| L(p1) − bound (first run) | 1.17e-5 | 5.22e-6 |

This matches the report and the wave-3 verifier's obj(p1). As the report says, p1 is
feasible only to about 1e-12. So obj(p1) is the objective of an approximately feasible
point, not a certified upper bound, and the "gap" is measured against it.

## 6. The fixed-leaf diagnostic (`diag_tight.py`)

The report says that with the leaf state fixed at p1 the Shor SDP gives 41869.05037 at
rank one, "so the rest of the network is exact". That value is 1.14e-3 below obj(p1),
about 40 times the final certified gap. Taken as logged, it does not show exactness.

I re-solved the same SDP (the author's `solve_primal`, angle rows dropped, leaf state
fixed) with Clarabel tolerances 1e-10:

| Clarabel tolerances | value | obj(p1) − value | top eigenvalues of complex W | largest row residual |
|---|---|---|---|---|
| default (author) | 41869.05037 | 1.1e-3 | 9.6e-8, 1.2e-7, 41.85 | 9.7e-11 |
| 1e-10 (this review) | 41869.05150 | 9.3e-6 | 8.3e-10, 1.1e-9, 41.85 | 5.6e-10 |

So the 1.1e-3 was solver error, and the conclusion holds numerically to about 1e-5. This
remains a diagnostic, not a bound. The certified B&B result is the rigorous evidence that
the leaf was essentially the whole gap.

## 7. Issues found

None of these affects a bound.

1. **Diagnostic number (Section 6).** The report should replace 41869.05037 with the
   tight-tolerance value, or state that the default tolerance leaves a 1.1e-3 error. It
   should also say that this diagnostic drops the angle rows.
2. **Log inconsistency.** The FINAL line of `ext/logs/powerflow0039p.bb3t.log` prints
   "rational bound 2093452574242507/10^12". That is exactly 1/20 of the report's
   41869051484850140/10¹². The log was written at 08:20:23, before the last edit of
   `pf_bb3.py` at 08:20:41, so an earlier version of that line printed it. The printed
   number is a true but useless bound (about 2093.45). The report's number is correct:
   both I and the author's `verify_exact.py` recompute floor(LB·10¹²) = 41869051484850140.
   A one-line note in the log or the report would prevent confusion.
3. **Nit (Section 3, "First split").** The lower child 41869.04818 is 3.3e-3 below
   obj(p1), not "within 3e-3".

## 8. What this review did not check

- These claims were not checked:
  - the statements about `/tmp` scripts that were not kept (the failed G cut reaching
    41868.415, and Qg moving to 1.747);
  - "only line 1–29 had a 2×2 defect above 1e-6";
  - "the rotation direction of A has float eigenvalue about −1e-8";
  - the reasons for the pf_bb2 stall, which the report itself labels unconfirmed.
- I did not re-run the B&B. I checked the stored leaves, which suffices for validity: any
  multipliers give a valid bound.
- The polar flow conversion was checked by a term-by-term derivation and by random-point
  evaluation, not by a symbolic proof. The wave-3 verifier's sympy check covers the same
  rows symbolically.
- Running the author's scripts refreshed the existing `ext/__pycache__`. It is ignored by
  git. No other files outside `reviews/powerflow0039-review-checks/` and this review were
  changed.

## 9. Commands run (targeted only)

All from `reviews/powerflow0039-review-checks/` with `OMP_NUM_THREADS=1` (and
`OPENBLAS_NUM_THREADS=1` where BLAS is used) and `timeout`:

- `python3 cmp_rows.py powerflow0039p powerflow0039r`
- `python3 leaf_struct.py powerflow0039p powerflow0039r`
- `python3 verify_leaves.py <name> <tag>` for all four runs (`logs/verify_leaves.*.log`,
  8–15 s each)
- `python3 p1_check.py <name> bb3 bb3t` for both instances (`logs/p1_check.*.log`)
- `python3 diag_tight.py` (`logs/diag_tight.log`; one SDP solve)
- The author's `ext/verify_bb3.py` and `ext/verify_exact.py`, run from `ext/`, for all four
  runs (`logs/author_verify_*.log`)
