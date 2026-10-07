# Recheck of the revised note "Exponential lower bounds for single-tree spatial branch-and-bound with termwise McCormick relaxations on a path"

Date: 2026-09-30. Note: `research-20260929/theory-face-exact/face-exact-exponential.md`
(revised version, 1441 lines; changes listed in its Section 13). First review:
`reviews/face-exact-review.md`. I did not write the note or the first review.
Scripts and logs are in `reviews/face-exact-recheck-checks/`. I ran only targeted
checks, with no project-wide verification and no CI (AGENTS.md). I did not
commit anything or edit the note.

## Verdict in brief

| Item | Verdict |
|---|---|
| 1. New pruning logic in `bb_path.py` | **correct**, with small fixes to wording and logging |
| 2. Revised grid optima at `n = 2` | **correct**; one wording fix on the tie |
| 3. New Section 9 (significance) | **correct with fixes**: attribution to Griewank–Toint, the "convex exactly on the cube" wording, and what the alphaBB proxy shows |
| 4. Theorem statements, Summary, title, status table | **correct**. Theorems 1 and 2 are unchanged word for word. There are three small Summary wording fixes. |

Main evidence:
- An independent branch-and-bound in exact rational arithmetic reproduces
  every count I tried and flips no pruning decision:
  - `kappa = 0`, `c = 0`: 38, 162, 522, 1562 at `eps = 1e-6` and 24, 100, 320,
    962 at `eps = 1e-4` (`n = 2..5`);
  - PROGRAM seed 0 with the secant relaxation: 20, 80, 249, 738 at
    `eps = 1e-4`.
- Across about 10,000 nodes, the note's certified bound never exceeds the
  exact bound by more than `1.3e-16`.
- No exact node bound falls in the tie band `[f* - eps - 1e-12, f* - eps)`.
  So the tie tolerance changes nothing in these runs.

## 1. Pruning logic in `bb_path.py`

### 1.1 Validity, from the code (`certified`, `_dual`, `_phi_min`, `_F`, `relax_split`)

I checked every path by which a node can be pruned. A node is pruned only if
`lb >= thr`, where `thr = fstar - eps - 1e-12` and `lb` is one of the bounds
below.

- **`mc` and `mcx`: the separable dual function.**
  - I rederived the McCormick pieces. For `b > 0`,
    `P = l_j x_i + l_i x_j - l_i l_j` and `Q = u_j x_i + u_i x_j - u_i u_j`.
    For `b < 0` they are the negated upper envelopes (unused here, since
    `b = 0.8`). `_edge_affine` matches.
  - For every `lambda in [0,1]^(n-1)`, `lambda P + (1 - lambda) Q <= max(P, Q)`
    pointwise. So `d(lambda) <= min_C F_C`. This needs no duality theory.
  - The separable minimization is exact. For `mc` it is the closed form
    `clip(-lin/2)` for `x^2 + lin x`. For `mcx` it uses 80 bisections of a
    monotone derivative. Evaluating at an approximate minimizer overestimates
    the minimum by `O(dx^2)`, about `1e-48`, which is negligible.
  - Dual ascent (L-BFGS-B) and the Clarabel fallback only choose `lambda`.
    The Clarabel multipliers are clipped to `[0,1]`. So every `lb` is a valid
    bound up to rounding.
- **Upper bound `ub`.** `ub = _F(xh)` is used only to trigger refinement and
  to decide "not prunable". It can never cause a prune.
  - The v2 bug evaluated `_F` with the true quartic instead of its secant.
    Since `-kappa x^4` lies above its secant, that value was still an upper
    bound on the relaxation, only a looser one.
  - Stalled dual ascent leaves the node unpruned.
  - So the note's statement "neither could make pruning invalid" is correct.
- **`abb`, `abbU`, `abbS`: the Frank–Wolfe bound.**
  `F(x) >= F(xh) + min_box grad F(xh)'(x - xh)` is valid when `F` is convex
  on the box.
  - `abb` (`kappa = 0`): `alpha = (sqrt(1 + b^2) - 1)/2` is exact for the
    constant factor Hessian `[[2, b], [b, 0]]`.
  - `abbU`, `abbS`: `lambda_min([[p, b], [b, q]])` is nondecreasing in `p` and
    `q`. Each diagonal entry depends on one variable, and `g''` is smallest at
    the end of the interval farthest from 0. So using `gmin` gives the exact
    box-dependent `alpha`, and the relaxation is convex.
  - The split weights add to 1 for every variable, including the ends and
    `n = 2`.
  - Numerically (`section9_checks.py`, 300 random boxes at `n = 5`, 20 points
    each), the smallest Hessian eigenvalue of the relaxation is 1.121 (`abb`),
    0.533 (`abbU`) and 0.056 (`abbS`). The FW bound minus the relaxation
    minimum is at most `2.2e-16`.
- **Incumbent.** For `c = 0`, `Inst.fstar` is exactly `0.0`. The start `x0 = 0`
  gives `f = 0`, and a replacement needs a value `1e-12` lower. For the seeds,
  `fstar` is `f` at a feasible point, so it is `>= f*` up to rounding. That is
  a valid `UBD`.

**What "valid" means with the tie tolerance.** The rule is
`LB_cert >= f* - eps - 1e-12`. So each pruned box is certified at tolerance
`eps + 1e-12` (plus rounding of about `1e-16`), not at `eps`. This is
harmless for the theorems. For the counts it means "exact at `eps`, provided
no exact bound lies in `[f* - eps - 1e-12, f* - eps)`". In all my exact
checks none did (Sections 1.2 and 2).
- *Fix (Section 7, first bullet; Section 11).* State this in one sentence:
  "pruned boxes are valid at `eps + 1e-12` up to rounding; in exact-arithmetic
  rechecks no node bound fell in that band".

**"In the final runs no node remained undecided" (Section 7).** The logged
counter `undecided` (`STATS["ambiguous"]`) counts only nodes where the solver
value was at least `thr` but the certified bound was not. It does not count a
node that stays undecided after refinement (`lb < thr <= ub`) while the solver
value is also below `thr`. Such a node is branched, which inflates the count
but never invalidates a prune. My exact comparison found no such node on the
instances checked (0 flipped decisions).
- *Fix.* Count every node with `lb < thr <= ub` after refinement, or reword to
  "no node where the solver value was above the threshold remained
  undecided".

**Stale docstring.** `bb_path.py` lines 6 and 15–16 still say "node bound =
exact optimum of a convex QP, HiGHS" and "pruned iff LB >= f* - eps". Update
them to the certified bound and the `1e-12` tie tolerance.

### 1.2 Independent exact branch-and-bound (`exact_bb.py`)

**Method.** Nothing in this method comes from `bb_path.py`.
- The node relaxation is `sum_i (x_i^2 + lin_i x_i + const_i) + b sum_e max(P_e, Q_e)`,
  with all data exact rationals: `b = 4/5`, dyadic boxes,
  `kappa = 1/10` for seed 0, and the float `c_i` taken as exact rationals.
- OSQP, a solver the note does not use, supplies an approximate minimizer.
  Each variable is then classified as lower, upper or free, and each edge as
  `P`, `Q` or kink.
- The face's KKT system is solved in `Fraction` arithmetic. For each kink,
  `lambda_e = 1 + nu_e/b`.
- **Certificate.** `x` is feasible and `d(lambda) == F(x)` exactly (weak
  duality).
- **Fallback.** Enumerate all `3^n * 3^(n-1)` faces. The minimum over the
  feasible faces is the exact minimum without any duals, because the
  objective is strictly convex on every face.
- Pruning uses `LB >= f* - eps` with `eps = 10^-k` exact. Bisection splits the
  widest side at the midpoint, with ties to the lowest index.
- At every node the script also calls the note's `bb_path.relax` and
  `bb_path.certified`, and records flipped decisions and
  `max(certified LB - exact LB)`.

**Validation** (`validate_exact.py`). On 145 random dyadic boxes (`n = 2, 3, 4`;
half of them orthant boxes with a vertex at `x* = 0`):
- the guided exact value equals the full enumeration on all 145;
- it agrees with Clarabel at tolerance `1e-12` to `6.6e-13`.

**Results** (`logs/exact_bb_*.log`):

| instance | `eps` | n = 2 | 3 | 4 | 5 | note's counts | flipped decisions | max(certified LB - exact LB) |
|---|---|---|---|---|---|---|---|---|
| `kappa = 0`, `c = 0`, `mc` | `1e-6` | 38 | 162 | 522 | 1562 | 38, 162, 522, 1562 | 0 | `1.7e-17` |
| `kappa = 0`, `c = 0`, `mc` | `1e-4` | 24 | 100 | 320 | 962 | 24, 100, 320, 962 | 0 | `1.7e-17` |
| seed 0, `kappa = 0.1`, secant `mc` | `1e-4` | 20 | 80 | 249 | 738 | 20, 80, 249, 738 | 0 | `1.3e-16` |
| seed 0, `kappa = 0.1`, secant `mc` | `1e-6` | 26 | 112 | 365 | — | not reported | 0 | `7.6e-17` |

- In every run, no node has an exact bound equal to `f* - eps` or in the tie
  band.
- Full enumeration was needed for 0–6 nodes per run on the degenerate
  instance, and for none on seed 0.
- The positive differences, at most `1.3e-16`, are rounding. On seed 0 part of
  the difference comes from the note's float `kappa = 0.1` against my exact
  `1/10`.
- *Provenance fix.* The note cites 1562 (`n = 5`, `eps = 1e-6`) in Section 13,
  but no log in `theory-face-exact/` contains it. I ran
  `python3 bb_path.py mc bisect 0.0 zero 1e-6 5` and got 1562 leaves,
  `undecided=0` (`logs/bb_path_mc_bisect_k0_1e-6_n5.log`). Add this run to
  the note's logs or table.

**Verdict, item 1: correct.** Every pruning decision is valid by weak duality
or convexity, up to rounding and the stated `1e-12` tolerance. The exact
recheck confirms both the counts and every individual decision on the
instances tried.

## 2. Grid optima at `n = 2` (`grid_dp_exact.py`)

I wrote an independent DP over all grid boxes. Each node bound is the exact
rational minimum from the 27-face enumeration. The DP reports the optimum
under the note's non-strict rule (`LB >= -eps`) and under the strict rule.

| `eps` | K | optimum, `LB >= -eps` | optimum, `LB > -eps` | grid boxes with `LB = -eps` exactly | in `[-eps - 1e-12, -eps)` | note |
|---|---|---|---|---|---|---|
| `1e-2` | 4 | **4** | 5 | 56 | 0 | 4 with tie tolerance, 5 without |
| `1e-4` | 7 | **8** | 8 | 0 | 0 | 8 |
| `1e-6` | 10 | **12** | 12 | 0 | 0 | 12 |

- The optimal leaves at `1e-4` and `1e-6` are the same boxes as in the note's
  `grid_dp_n2_*.log`, with exact bounds. For example, `[-1/64, 1/64] x [0, 1]`
  has `LB = -1/25600`.
- The tie at `1e-2` is exact. For example, `[-1/4, 1/4] x [-1, 0]` has
  `LB = -1/100` exactly.
- The note's own code with `TIE = 0` returns 5, because its float bound at
  these boxes is `-0.01 - 1.7e-18` (`logs/grid_dp_note_code_TIE0_K4.log`).

**Verdict, item 2: correct.** *Wording fix (Sections 7.6 and 13).* Replace
"4 with the tie tolerance and 5 without it" with: "4 is the exact optimum
under the definition `LB >= f* - eps`. Some grid boxes, such as
`[-1/4, 1/4] x [-1, 0]`, have bound exactly `-eps`. Without the tie tolerance,
floating-point rounding puts them `1.7e-18` below `-eps` and gives 5, which is
also the optimum under a strict inequality."

## 3. Section 9 (significance)

### 3.1 Lemma 9.1: correct

- By hand, the diagonal at `i` is `b_{i-1}^2/p_{i-1} + p_i = d_i`, and each
  block has determinant 0 and trace `> 0`. The pivots are the `LDL'` pivots,
  which are positive iff `H` is positive definite.
- Numerically, on 279 random positive definite tridiagonal matrices
  (`n = 2..12`, mixed signs), the blocks sum to `H` to `4.4e-16` and are PSD
  to rounding (`logs/section9_checks.log`).
- The pivots of `2I + 0.8A` decrease from 2 to 1.6, the fixed point of
  `p = 2 - 0.64/p`. The balanced blocks work, with end blocks
  `[[2, .8], [.8, 1]]`.

### 3.2 Consequence A (clique-wise PSD cuts are exact for `kappa = 0`): correct

- *Proof.* The block PSD condition gives `X_c - x_c x_c' ⪰ 0`. Then
  `<H_c, X_c - x_c x_c'> >= 0` for PSD `H_c`, and the `p_n` term uses
  `X_nn >= x_n^2`. So the bound is at least `min_C f`. The point
  `(x, xx')` is feasible, so the bound is at most `min_C f`. The relaxation
  is therefore exact on every box, for any `c` and any signs of `b_i`.
- *Numerically.* On 24 random sub-boxes (`n = 4`; `c = 0` or random;
  uniform or mixed signs), the SDP bound equals the QP minimum to `4e-8`,
  which is the SDP solver's accuracy.
- *SCIP.* I read `scip/src/scip/sepa_minor.h` and `sepa_minor.c` of SCIP
  10.0.3. The separator detects the minors of `xx'` whose auxiliaries
  `X_ii`, `X_jj`, `X_ij` all exist. It cuts off points where
  `A = [[1, x_i, x_j], [x_i, X_ii, X_ij], [x_j, X_ij, X_jj]]` is not PSD, with
  eigenvector cuts `v'A v >= 0`. Its settings are frequency 10, at most 10
  rounds per node (unlimited at the root), and minimum violation `1e-4`. So
  "outer-approximation cuts at some nodes, not the full constraint" is
  accurate. "(As documented)" can cite this header.

### 3.3 Consequence B (split factorization): correct in substance, with fixes

- The argument is correct. With positive definite blocks at `x*` and `g_i` of
  class `C^2`, every factor is convex on a neighbourhood. The per-factor
  envelopes are then exact there, and the neighbourhood is certified by one
  box.
- `kappa = 0`, balanced split: the blocks `[[1, .8], [.8, 1]]` and
  `[[2, .8], [.8, 1]]` are positive definite everywhere, so `N_cert = 1`.
  Correct.
- `kappa = 0.1`: I solved for the largest centred cube on which each factor
  is convex (`brentq`). It is `0.577350 = 1/sqrt(3)` for interior factors and
  `0.8508` for end factors. The interior factor at `(1, 1)` has
  `lambda_min = -0.400`. Correct.

Fixes:
- **(a) "Convex exactly on `|x|_inf <= 1/sqrt(3)`" (Section 9.2).** The set on
  which a factor is convex is not a cube. For example, the interior factor is
  convex at `(u, v) = (0.77, 0)`, since `(2 - 1.2 u^2)/2 >= 0.8` needs only
  `u^2 <= 0.6` when `v = 0`. Say "the largest centred cube on which every
  factor is convex is `|x|_inf <= 1/sqrt(3)`". It coincides with the convexity
  cube of `f` in Lemma 1.1(c).
- **(b) Summary item 2 says "PSD `2x2` blocks".** PSD blocks, such as the
  determinant-0 blocks of Lemma 9.1, make the factors convex at `x*` only.
  Convexity "near `x*`" needs positive definite blocks, as Section 9.2
  correctly says. Also state the hypotheses once: Hessian of `f` positive
  definite at `x*`, and `g_i` of class `C^2` near `x*_i`.
- **(c) Notation.** `U = x* + [-rho, rho]^n` reuses `rho`, which is already
  `D/(2b)`.
- **(d) Priority.** This is Griewank and Toint's construction; see 3.5.

### 3.4 The alphaBB proxy for the split: argument correct; the evidence is weaker than stated

- **Tree containment.** Per-factor alphaBB with the exact box-dependent
  `alpha` is a convex underestimator of each factor, hence below that
  factor's envelope. So its gap dominates the split-envelope gap. With
  bisection and `UBD = f*`, every box that alphaBB prunes, the envelope also
  prunes. The envelope tree is therefore a subtree of the alphaBB tree, and
  `leaves = internal nodes + 1` gives leaves(envelope) `<=` leaves(alphaBB).
  Correct.
- **Numbers, from `logs/bb_runs_v2.log`.**
  - `abbS`: 1, 24, 64, 162, 404, 1000, 2476. Growth over the last four steps
    is `(2476/64)^(1/4) = 2.49`.
  - `abbU`: 34 … 13,352. Growth is 2.55.
  - The ratio `abbU/abbS` is 5.0–5.4 for `n = 4..8`.
  - All match the note.
  - The claim "1 leaf for `kappa = 0` at every `n` tried (up to 8)" is logged
    only at `n = 8`. It holds for every `n` because the relaxation equals `f`.
- **"None of its leaves lies inside the convex cube" is automatic.**
  `logs/leaves_abbS.log` shows that every leaf (404 at `n = 6`, 2476 at
  `n = 8`) has a side of length at least 1. Widest-side bisection of
  `[-1, 1]^n` makes such a side `[-1, 0]`, `[0, 1]` or `[-1, 1]`, which reaches
  `|x_i| = 1`. Also, only boxes that reach outside the cube can be invalid.
  So "entirely from boxes that reach outside the cube" (Sections 9.3, 13) is
  true by construction, not a finding.
  - *Fix.* Report it as such. Or, if a diagnostic is wanted, count the split
    (invalid) nodes by how far they extend outside the cube.
- **Direction of the evidence.** The proxy count is an *upper* bound on the
  split-envelope count. It shows that split envelopes need at most about
  2476 leaves at `n = 8` with bisection. It is no evidence that they need
  exponentially many. Section 9.3 says this ("open"), but Section 13 item 4
  and the status-table row ("the alphaBB proxy grows by about 2.5 per
  variable") can be read as evidence.
  - *Fix.* Add "(an upper bound on the envelope count)" in both places.

### 3.5 Literature: citations correct; attribution needs a fix

I verified these by web search and by reading the survey's text.
- **Agler, Helton, McCullough, Rodman.** "Positive semidefinite matrices with
  a given sparsity pattern", *Linear Algebra Appl.* 107 (1988) 101–149. The
  decomposition result is their Theorem 2.3.
- **Griewank, Toint.** "On the existence of convex decompositions of
  partially separable functions", *Math. Programming* 28 (1984) 25–49.
- **Vandenberghe, Andersen.** "Chordal graphs and semidefinite optimization",
  *Foundations and Trends in Optimization* 1(4) (2015) 241–433. Theorem 9.2
  states the clique decomposition of PSD matrices with chordal pattern and
  cites "[106, theorem 4] [1, theorem 2.3] [122, theorem 1]": Griewank–Toint
  1984, Agler et al. 1988, and Kakimura 2010. Section 12.1 says the
  decomposition of `∇²f` into PSD element Hessians "was the motivation that
  led to the theorem in [106]".
- **Waki, Kim, Kojima, Muramatsu.** *SIAM J. Optim.* 17(1) (2006) 218–242.
  Correct.

Fixes:
- The note says that Griewank and Toint "studied the corresponding question".
  That understates their result: their Theorem 4 already proves the matrix
  decomposition, four years before Agler et al. Their paper also constructs
  exactly the local convexification that Consequence B uses. The abstract
  describes shifting quadratic terms among element functions so that the
  modified element functions are locally convex. For sparse structure this is
  possible iff the pattern allows an `LDL'` factorization without fill-in.
  - Credit Consequence B to them.
  - Cite Vandenberghe–Andersen Theorem 9.2 and Section 12.
- Delete "cited from memory, not rechecked" in Sections 9.4 and 11.

**Verdict, item 3: correct with fixes (a)–(d) and the two wording fixes in 3.4.**

## 4. Theorem statements, Summary, title, status table

**Method.** The pre-revision note is not in git; `research-20260929/` is
untracked. I rebuilt the version the first referee reviewed (988 lines) from
that referee's file reads in the session transcript
(`face-exact-recheck-checks/orig_note_as_reviewed.md`) and diffed it against
the revision.

**Unchanged word for word:**
- Theorem 1, statement and proof;
- Theorem 2, statement and proof;
- Lemmas 2.1, 3.1 and 4.1.

**Changed, all justified by the review:**
- Hypotheses. The inherited-cut wording is fixed, and the new (M^+) is
  introduced for Proposition 5.3. This is a genuine strengthening of the
  hypothesis, which the review showed is needed.
- Proposition 5.2 adds `W_i <= r`.
- Corollary 1.3 corrects the Lagrangian percentages.
- The "Other graphs" remark now uses `2 eps''/Delta`.
- Theorem 2's reported base is 1.205 instead of 1.2021. The statement is
  unchanged.
- Proposition 5.5 now has the monotonicity argument. I checked steps 1–5. The
  sandwich `Q' ⊆ L ⊆ Q` holds because widest-first bisection with ties to the
  lowest index halves a prefix of the coordinates. Both dyadic nodes exist
  because all their dyadic ancestors are binary ancestors of `L` that were
  split.

**Title and Summary.** The title and the answer ("yes for termwise McCormick
relaxations …; a statement about the relaxation class") match Theorem 1 and
Section 9. Three wording fixes remain:
1. Summary item 7: "Theorem 1's bound is below every toy and grid count". The
   `abbS` toy run has 1 leaf at `n = 2`, below 1.59. That relaxation is outside
   Theorem 1's class, so write "every termwise toy count".
2. Open problems: "the grid optima suggest at least about 2". Grid optima are
   upper bounds on `N_cert`, as the note itself says under Conjecture 5.4. So
   they cannot suggest a lower base. Write, for example, "the grid optima
   (upper bounds) grow by 2.5–3.2 per variable at `eps = 1e-2`".
3. Summary item 2: "PSD" should be "positive definite" (see 3.3(b)).

**Status table and header.**
- The table is consistent with the body.
- The Consequence A row says "explains SCIP's minor-separator effect", while
  the body says the SCIP data "fit". Use one wording.
- After this recheck, the header's "the revision has not been rechecked"
  should be updated.

**Verdict, item 4: correct.** The theorem statements did not change in
substance. The Summary, title and status table are consistent, apart from the
three wording fixes above.

## 5. What I verified myself, and commands run

Targeted local checks only, not CI. All commands were run from
`reviews/face-exact-recheck-checks/` unless stated, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`.

**By hand:**
- validity of every pruning path in `bb_path.py` (Section 1.1);
- the McCormick pieces and the secant formula;
- Lemma 9.1;
- Consequences A and B;
- the proxy containment argument;
- the binary-bisection argument of Proposition 5.5;
- the secant-gap coefficient `6 kappa x^2` in Section 9.3.

**Commands:**
- `python3 validate_exact.py` → `logs/validate_exact.log`
- `python3 exact_bb.py 6 2 3 4 5 cmp` and `python3 exact_bb.py 4 2 3 4 5 cmp`
  → `logs/exact_bb_eps1e-6.log`, `logs/exact_bb_eps1e-4.log`
- `python3 exact_bb.py 4 2 3 4 5 cmp seed0` and
  `python3 exact_bb.py 6 2 3 4 cmp seed0` → `logs/exact_bb_seed0_eps1e-*.log`
- `python3 grid_dp_exact.py 4 2`, `… 7 4`, `… 10 6` →
  `logs/grid_dp_exact_K*_eps*.log`
- The note's `grid_dp.py 2 4 1e-2` with `bb_path.TIE = 0`, plus certified
  bounds at three tie boxes (inline, from `theory-face-exact/`) →
  `logs/grid_dp_note_code_TIE0_K4.log`
- From `theory-face-exact/`:
  `python3 bb_path.py mc bisect 0.0 zero 1e-6 5` →
  `logs/bb_path_mc_bisect_k0_1e-6_n5.log`
- `python3 section9_checks.py` → `logs/section9_checks.log`

**Also:**
- Read the SCIP 10.0.3 source header `sepa_minor.h` and the defaults in
  `sepa_minor.c`.
- Web search for the four chordal and sparse-SDP references.
- Text of the Vandenberghe–Andersen survey (Theorem 9.2, Section 12.1,
  reference list).
- Checked the Section 7.3, 7.5 and 7.6 numbers I cite against
  `logs/bb_runs_v2.log`, `logs/bb_runs_v3_mc.log`,
  `logs/grid_dp_n2_*.log` and `logs/leaves_abbS.log`.
