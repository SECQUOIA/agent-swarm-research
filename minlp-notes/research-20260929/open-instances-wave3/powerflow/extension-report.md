# powerflow0039p / 0039r: closing the leaf-bus gap (extension of wave 3, Section 3)

Date: 2026-09-30. Status: computational result with the validity argument below and
two separate re-checks of every leaf certificate. Independently verified
([`../../reviews/powerflow0039-review.md`](../../reviews/powerflow0039-review.md)); the
review's three minor items were applied by the root on 2026-09-30 (Section 8). The
wave-3 verification (`reviews/wave3-verification/`) was still running when this was
first written. This result reuses two wave-3 components that the verification covers: the
relaxation R (`pf_model.py`) and the certificate evaluator (`pf_cert.py`). All runs
were single-threaded (`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=RAYON_NUM_THREADS=1`) and
time-limited. In total they used about 30 minutes of CPU time.

## Summary

- **Both gaps are closed to below 1e-9 relative.** The branch and bound needs only 11
  nodes (309 s) on 0039p and 17 nodes (423 s) on 0039r.

  | instance | listed primal | best listed dual | wave-3 rigorous dual | **new rigorous dual** | gap to p1 (abs / rel) |
  |---|---|---|---|---|---|
  | powerflow0039p | 41869.05151 | 41818.27916 (GUROBI) | 41868.26524 | **41869.05148485** | 2.6e-5 / 6.3e-10 |
  | powerflow0039r | 41869.05151 | 41804.88153 | 41867.77921 | **41869.05148327** | 2.8e-5 / 6.7e-10 |

  The upper bound is obj(p1) for the MINLPLib point p1, evaluated at 50 digits:
  41869.0515113202 for 0039p and 41869.0515113208 for 0039r. p1 is feasible only up to
  row violations of 1.2e-12 and 7.9e-12, so the gaps are stated relative to that
  evaluated value.
- **The mechanism is an exact identity for the leaf bus.** Bus 29 (0-based) is a leaf
  with a generator, joined to bus 1 by a single lossless line. Its line rows and
  Lagrange's identity give, at every feasible point,

  W₁₁ = F(Pg, Qg, W₂₉) = W₂₉ − 2Qg/b + (Qg² + Pg²)/(b²W₂₉),

  where Pg and Qg are the bus-29 generator outputs and b = 55.2486187845304. F is
  convex. The Shor SDP enforces only W₁₁ ≥ F, through the 2×2 minor on line 1–29. At
  the root it has W₁₁ = 1.09176 against F = 1.08662. The new cuts are the concave
  envelope of F over a box in (Pg, Qg, W₂₉): exact rational planes through box vertices.
  Branching on the three box coordinates then closes the gap.
- **The rest of the network is exact** (numerically). With the leaf state fixed to its
  value at p1 and the angle rows dropped, the Shor SDP at default Clarabel tolerances
  gives 41869.05037, 1.1e-3 below obj(p1) = 41869.05151; that difference is solver
  error. The review's re-solve at tolerances 1e-10 gives 41869.05150, 9.3e-6 below
  obj(p1), with a matrix that is rank one to about 1e-9 (diagnostic only; not a
  bound).

## 1. What the defect is

Structure, found by `ext/leafcut.py:leaf_info` and asserted there for both models:

- Bus L = 29 has one line, to N = 1. The line has only a series susceptance b > 0 (no
  conductance, no shunt, no tap). Its four flow rows are

  P_{L→N} = s·b·w_I,  P_{N→L} = −s·b·w_I,  Q_{L→N} = b(W_LL − w_R),  Q_{N→L} = b(W_NN − w_R),

  with W_NN = e_N² + f_N², W_LL = e_L² + f_L², w_R = e_N e_L + f_N f_L,
  w_I = e_N f_L − f_N e_L, and s = +1 (polar) or −1 (rectangular). `leaf_info`
  asserts the forms of the two P rows and of Q_{L→N}. Q_{N→L} was read from the model
  dump; the cuts do not use it.
- The generator variables are defined by linear rows P_{L→N} − Pg = 0 and
  Q_{L→N} − Qg = 0. Pg carries the cost 30 Pg + 100 Pg². The boxes are Pg ∈ [0, 10.4]
  and Qg ∈ [1.4, 4]. `leaf_info` asserts that Pg and Qg occur only in two-variable
  linear rows.
- Hence, exactly: w_R = W_LL − Qg/b and w_I² = Pg²/b².
- Lagrange's identity (e_N² + f_N²)(e_L² + f_L²) = w_R² + w_I² holds for all real
  numbers. Dividing by W_LL ≥ 0.94² > 0 gives W_NN = F(Pg, Qg, W_LL).

At p1, v₂₉ = 1.06 (at its upper bound) and Qg = 1.4 (at its lower bound). A generator
that must produce at least 1.4 p.u. of reactive power through a line of susceptance
55.25 forces v₁ cos δ ≤ v₂₉ − 1.4/(b v₂₉), which caps v₁. The SDP loosens exactly this
cap. It keeps W₂₉ = 1.06² and Qg = 1.4 while raising W₁₁ from 1.08664 to 1.09176, that
is, v₁ from 1.0424 to 1.0449 (`ext/diag_leaf.py`, `ext/logs/diag_leaf.log`).

## 2. Method (`ext/leafcut.py`, `ext/pf_bb3.py`)

- **Node.** A box B = [p1,p2] × [q1,q2] × [s1,s2] for (Pg, Qg, W_LL). The root box is
  [0, 10.4] × [1.4, 4] × [0.94², 1.06²].
- **Node relaxation.** R (wave-3 `pf_model.py`; the polar model keeps its angle rows)
  plus:
  - the Pg and Qg boxes, written as y boxes;
  - the row s1 ≤ e_L² + f_L² ≤ s2;
  - for every affine H(p, q, s) that passes through four vertices of B and satisfies
    H ≥ F at all eight vertices, the row W_NN − α·Pg − β·Qg − γ·W_LL ≤ δ. All plane
    coefficients are exact rationals.
- **Node bound.** The primal Shor SDP (`ext/pf_primal.py`, Clarabel, chordal
  decomposition off) supplies multipliers. The wave-3 `pf_cert.certify` then evaluates
  the Lagrangian bound in exact rationals and proves A(w) + εI ⪰ 0 by interval Cholesky.
  A child's bound is max(parent bound, own certificate).
- **Branching.** The coordinate with the largest estimated envelope error at the SDP
  point is split. The split point is the SDP value, clamped to the middle 80% of the
  interval and rounded to a rational. Children share the split value, so they cover the
  parent.
- **Search.** Best-first; a node is closed when its bound is ≥ UB − tol. The final bound
  is the minimum over all leaves, both open and closed. UB therefore controls only when
  branching stops; it does not affect validity.

## 3. Results

| run | Clarabel tolerances | nodes | time | certified bound | leaf containing p1 |
|---|---|---|---|---|---|
| 0039p, tol 1e-3 | default | 9 | 247 s | 41869.05104582637 | [6.7094, 7.0784] × [1.4, 1.66] × [1.0996, 1.1236] |
| 0039p, tol 1e-4 | 1e-10 | 11 | 309 s | **41869.05148485014** | [6.7094, 6.7463] × [1.4, 1.66] × [1.0996, 1.1236] |
| 0039r, tol 1e-3 | default | 11 | 283 s | 41869.05119609605 | [6.7094, 6.7463] × [1.4, 1.66] × [1.0996, 1.1236] |
| 0039r, tol 1e-4 | 1e-10 | 17 | 423 s | **41869.05148327244** | [6.7094, 6.7144] × [1.4, 1.426] × [1.1212, 1.1236] |

- **Root.** The cuts change almost nothing: 41867.7795 on 0039p. Over Pg ∈ [0, 10.4]
  the envelope error in the Pg direction is (Pg − 0)(10.4 − Pg)/(b²W₂₉) ≈ 7e-3 in W₁₁,
  larger than the defect.
- **First split.** A single split at Pg = 6.7094 lifts both children close to obj(p1)
  (0039p: 41869.05448, above it, and 41869.04818, 3.3e-3 below it).
- **Leaves.** The other leaves of the first 0039p run have bounds 41869.05448
  (Pg ≤ 6.7094, which excludes p1's Pg = 6.71424), 41872.597 (Qg ≥ 1.66), 41875.404
  (W₂₉ ≤ 1.0996) and 41885.799 (Pg ≥ 7.0784).
- **Rounded bounds.** Rational numbers at or below the exact minima, for citation:
  0039p ≥ 41869051484850140/10¹²; 0039r ≥ 41869051483272433/10¹².

## 4. Validity argument

A dual bound here is a number L with L ≤ f(x) for every exactly feasible x of the OSIL
model.

1. **Relaxation R.** Every feasible point of the OSIL model gives a point of R with the
   same objective (wave 3, Section 3.1; checked by the wave-3 verification and, for
   every row these certificates use, by the review of this extension). Polar points
   map through e = v cos θ, f = v sin θ.
2. **Leaf identity.** The identity W_NN = F(Pg, Qg, W_LL) holds at every point of R. It
   uses only the flow rows P_{L→N} and Q_{L→N}, the two linear rows that define Pg and
   Qg, the lower voltage row W_LL ≥ 0.8836 > 0, and Lagrange's identity. `leaf_info` checks
   the exact rational coefficients of these rows by assertion. At p1 the two sides agree
   to 3e-15 in 50-digit arithmetic; the residual comes from p1's rounding.
3. **Cuts.** On W_LL > 0, F is convex: (p² + q²)/s is the perspective of a convex
   function, and the rest is linear. Every point of a box is a convex combination of the
   box's vertices. So an affine H with H ≥ F at the eight vertices, checked exactly in
   rationals, satisfies H ≥ F on the whole box. Hence W_NN = F ≤ H at every point of R
   whose (Pg, Qg, W_LL) lies in the box.
4. **Partition.** The node rows restrict (Pg, Qg, W_LL) to the box, and the root box
   contains every feasible point. For each finished run, `ext/verify_bb3.py` checks that
   the leaf boxes lie in the root box, that their volumes sum exactly to the root volume,
   and that their interiors are pairwise disjoint. A finite union of closed boxes of full
   measure is the whole box. So every feasible point lies in some leaf.
5. **Node bounds.** For any multipliers (free on equalities, nonnegative on inequality
   sides), the Lagrangian is ≤ the objective at every point of the node relaxation. The
   bound is const + min_y(separable y part) + min_x xᵀA x. It is evaluated exactly, and
   min_x xᵀA x ≥ −ε Σ_k vmax_k² once A + εI ⪰ 0 is proven (Σ vmax² = 43.82). Inaccurate
   multipliers can only weaken the bound; they cannot make it invalid.
6. **Result.** The certified value is the minimum over the leaves, so it is ≤ the
   objective of every feasible point.

**Checks run on the stored leaf certificates** (`ext/logs/<name>.<tag>.json` stores each
leaf's box and multipliers):

- **`verify_bb3.py`** checks the partition (item 4) and recomputes each leaf bound with
  `pf_cert.certify`. At p1 (50 digits) it also checks the identity, the cut rows of the
  leaf containing p1, and bound ≤ L(p1) ≤ obj(p1). Results:
  - 0039p tight run: L(p1) − bound = 5.2e-7, obj(p1) − L(p1) = 2.6e-5, largest node-row
    violation at p1 1.2e-12.
  - 0039r tight run: L(p1) − bound = 6.2e-7, obj(p1) − L(p1) = 2.7e-5.
  - 0039r first run: L(p1) − bound = 5.2e-6.
- **`verify_exact.py`** is written separately from `pf_cert`: it forms the Lagrangian
  in exact rationals and proves A + εI ⪰ 0 by exact LDLᵀ with no floating point. For
  every leaf of all four runs it reproduces the stored bound, or exceeds it by at most
  4.4e-8 where it needs a smaller ε than `pf_cert`. The
  exact ε chosen is 0 or 10⁻⁹ to 10⁻⁶; ε > 0 is needed because the rotation direction
  of A has float eigenvalue about −1e-8. The largest ε costs 4.4e-5. The leaf that sets
  the final 0039p bound needs ε = 10⁻⁸, which costs 4.4e-7.
- **Limits of these checks.** Both checks use the rows produced by `pf_model.decode`, so
  they do not re-check item 1 against the OSIL. That is the scope of the parallel wave-3
  verification, which reported 184 flow rows verified symbolically for 0039p in its
  root log.

## 5. Diagnostics and honest failures

- **First cut attempt failed.** The first cut used only Qg ≥ 1.4 and w_R ≥ 0 to bound
  w_R ≤ W_LL − 1.4/b, giving W_NN ≤ G(Pg, W_LL). On the box Pg ∈ [6.5, 7] it raised
  0039p only to 41868.415 (`/tmp` diagnostic, not kept). The SDP moved Qg off its bound
  to 1.747 and reopened the defect through w_R. Writing the identity in (Pg, Qg, W_LL),
  with no inequality used, fixed this. The G variant was removed from `leafcut.py`.
- **The pf_bb2 stall is not explained.** The wave-3 `pf_bb2.py` stalled at 41868.26524
  on 0039p. At the stalled node the SDP looked rank-one on lines, yet the extracted
  point violated balance rows by about 1e-4. The fixed-leaf diagnostic shows that the
  relaxation of the rest of the network is exact at p1's leaf state, so the stall was
  not caused by a second relaxation defect. Likely causes, unconfirmed:
  - the envelope cuts in pf_bb2 lower-bound |W₁,₂₉| through √(W₁₁W₂₉) and need narrow
    boxes in v₁, v₂₉ and angle at once;
  - pf_bb2 recovers W from the dual formulation and keeps the parent bound when a child
    certificate is lower, which hides child progress.

  This was not investigated further.
- **The gap is not zero.** The remaining 2.6e-5 on 0039p is mostly the envelope slack
  at p1 times the cut multipliers: obj(p1) − L(p1) = 2.6e-5. Further Pg splits around
  6.714 would shrink it quadratically. Below about 1e-5, Clarabel's accuracy (tolerances
  1e-10 here) and the ε shifts start to matter.
- **Scope.**
  - The cut is specific to a leaf bus whose only rows are one lossless line and a
    generator with boxed P and Q, and `leaf_info` asserts this structure.
  - A line with conductance or shunt terms would change F. The same derivation would
    then need the corresponding exact expressions for w_R and w_I.
  - No other bus of these instances needed treatment: at the root, only line 1–29 had a
    2×2 defect above 1e-6.

## 6. Commands run (targeted only; no project-wide checks, no CI)

All commands were run from `research-20260929/open-instances-wave3/powerflow/ext/`,
with single-threaded BLAS and `timeout`.

- `python3 pf_bb3.py powerflow0039p 2400 41869.0515113202` (log
  `logs/powerflow0039p.bb3.log`, leaves `logs/powerflow0039p.bb3.json`)
- `python3 pf_bb3.py powerflow0039r 2400 41869.0515113208` (`...0039r.bb3.*`)
- `python3 pf_bb3.py powerflow0039p 2400 41869.0515113202 1/10000 1e-10 bb3t` (`...0039p.bb3t.*`)
- `python3 pf_bb3.py powerflow0039r 2400 41869.0515113208 1/10000 1e-10 bb3t` (`...0039r.bb3t.*`)
- `python3 verify_bb3.py <name> [bb3t]` and `python3 verify_exact.py <name> [bb3t]` for
  all four runs
- `python3 diag_leaf.py` (`logs/diag_leaf.log`)
- Note on `logs/powerflow0039p.bb3t.log`: its FINAL line prints "rational bound
  2093452574242507/10^12", exactly 1/20 of the cited 41869051484850140/10¹². The log
  was written before the last edit of `pf_bb3.py`, so an earlier version of that line
  printed it. The cited number is correct: `verify_exact.py` and the review recompute
  floor(LB·10¹²) = 41869051484850140.
- Exploratory `/tmp` scripts, not kept: structure dump, and root SDP solves with the
  first cut variant G.

## 7. Files (under `open-instances-wave3/powerflow/ext/`)

- `leafcut.py`: leaf structure check, F, exact vertex planes, cut rows.
- `pf_primal.py`: primal Shor SDP with explicit W and y; duals in pf_cert format.
- `pf_bb3.py`: the leaf branch and bound.
- `verify_bb3.py`, `verify_exact.py`: re-checks of stored leaf certificates.
- `diag_leaf.py`: root and fixed-leaf diagnostics.
- `logs/`: B&B logs, leaf JSON files (boxes, bounds, multipliers), `diag_leaf.log`.

## 8. Revision after review (root, 2026-09-30)

The review ([`../../reviews/powerflow0039-review.md`](../../reviews/powerflow0039-review.md),
verdict "verified") recomputed both certified bounds with its own code and raised
three minor items, none affecting a bound. Each was checked against the review's
logs before the text was changed.

1. **Fixed-leaf diagnostic.** The Summary now gives the default-tolerance value with
   its 1.1e-3 solver error, the review's tight-tolerance value (41869.05150, 9.3e-6
   below obj(p1); `reviews/powerflow0039-review-checks/logs/diag_tight.log`), and says
   that the diagnostic drops the angle rows.
2. **Log inconsistency.** Section 6 notes that the FINAL line of
   `logs/powerflow0039p.bb3t.log` came from an earlier version of `pf_bb3.py`; the log
   itself was not edited.
3. **First split.** "Within 3e-3 of obj(p1)" became "41869.04818, 3.3e-3 below it".

The header records the review, and the validity argument's step 1 no longer says
"under independent verification".
