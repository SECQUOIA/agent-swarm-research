# Recheck of the revised binary-least-squares certification note

Reviewed file:
[`../bb-complexity/binary-least-squares/certification-thresholds.md`](../bb-complexity/binary-least-squares/certification-thresholds.md)
(revision of 2026-09-29, after
[`mimo-easy-review.md`](mimo-easy-review.md) and
[`mimo-hard-review.md`](mimo-hard-review.md); changes listed in its
Section 10). Reviewer: fresh independent reviewer (probability, convex
relaxations). I had not seen this material before. Date: 2026-09-29. Scope:
the five substantive revisions named in the brief. I did not edit the note
and did not commit.

My scripts and logs are in [`mimo-recheck/`](mimo-recheck/). They import
nothing from the note's `code/` or from the earlier reviewers' scripts. The
instance generator in `rc_common.py` mirrors the note's documented generator
(`core.instance`, which I read). The match is confirmed by exact agreement of
all 36 per-seed node counts in item (5).

## Verdict

| Revision | Verdict |
|---|---|
| (1) Theorem 4.1, top-`K` sum of the `zeta_i` | **Correct.** Every event, union bound and error term checks. The loss factor `kappa_rho -> 1` for every `rho -> inf`, and the proof never uses that `x*` is the ML point: it compares node bounds with `W >= UB`. The theorem itself carries the factor `N+1` (`+ log(N+1)` in the exponent). The Summary's restatement drops it, which makes that sentence false at `rho = Theta(N)` (F1). At practical sizes, `kappa_rho` is only 0.2–0.7 (F9). |
| (2) Theorem 3.1(d), `beta = 1`, via Hu–Lu | **Correct.** The reduction is exact, both as an identity (relative difference `<= 3e-16`) and in law (KS p = 0.76 for the node value, 0.28 for the largest NNLS coefficient). The Hu–Lu hypotheses hold, with `alpha* = 1 + eps` exactly. Two precision points: `theta` must be fixed (F5), and the reformulation of Conjecture 3.3 is a sufficient condition, not an equivalent one (F4). |
| (3) Proposition 6.3, eigenvalue shift | **Correct.** `f_d` agrees with `f` on `{-1,1}^N` and is convex iff `d <= lambda_min(A'A)`. The KKT condition `zeta_i >= -d` is exact (160/160 instances agree with a QP solve), and the threshold follows as in Theorem 6.2. Two issues with the surrounding text: the "0.000 at `rho = 300`" gap is `3.9e-4`, and the relaxation is not exact in any of the four instances there (F2). The shift threshold is also sharp, and at `beta = 2` it is 16–25 times the SDP's at `N = 100–1600` (F3). |
| (4) Theorem 5.1(a), upper half | **Correct.** The Hamming-ball reduction, the small-regime display, the tail sum and the large regime all check. The display and the tail bound also hold numerically on a grid. One check cell in the note is capped, which does not matter (F7). |
| (5) Fincke–Pohst versus box static order | **Reproduced exactly.** With my own implementations, I get the same per-seed counts at `N = 32` (FP 839, box 90 geometric means). I also reproduced all six seeds at `N = 48` and `N = 64`. The comparison is in node counts. In wall-clock time, FP is faster at these sizes (F6). |

## 1. Theorem 4.1 (top-`K` refinement)

I checked the proof line by line.

- **Node bound.** For a data-independent order, `v = w + 2 B_Wr 1` is
  independent of the free columns. By Theorem 1.3(b), the node bound is at
  least `||v||^2 (1 - Y)` with `Y` a Beta mixture. The node is pruned if
  `D_Wr >= W Y/(1-Y)`, because then its bound is at least `W >= UB >= UB - eps'`.
  This is the only place `OPT` could enter, and it does not. So the ML
  hypothesis is indeed unnecessary.
- **Top-`K` step.** `sum_{i in Wr} zeta_i >= -a T_K` for `|Wr| = K`.
  - `T_K <= Kt + sum_i (-g_i - t)_+` holds.
  - `E(Z - t)_+ = phi(t) - t Phibar(t) <= phi(t)/(1 + t^2)` follows from
    `Phibar(t) >= t phi(t)/(1+t^2)`; I also checked it on a grid in
    `[0, 12]` (`topk_check.log` (a)).
  - At `t = sqrt(2 log(N/K))`, `N phi(t) = K/sqrt(2 pi)`, so
    `E T_K <= K(t + 1)` with room to spare.
  - `T_K` is a maximum of linear forms with gradient norm `sqrt K`. Gaussian
    concentration therefore gives the `sqrt(2K log N)` term with probability
    `>= 1 - 1/N`.
- **Error terms.** These all check.
  - `log(N/K) <= L_rho` because `K >= N/(4(2beta-1) rho)`.
  - `2 log N/(K rho beta) <= 8(2beta-1) log N/(beta N) -> 0`.
  - `s_min(H~_Wr)^2 >= M(1 - o(1))` uniformly over `C(N,K)` sets, because
    `K/N -> 0` and `log C(N,K)/N -> 0`.
  - `t' -> 0` in the `Y` event, and the union bound over `(N+1) C(N,K)`
    nodes leaves `O(1/(N C(N,K)))`.
  - Together these give `D_Wr >= 4 rho beta K (kappa_rho - o(1))`, and
    `kappa_rho -> 1` for every `rho -> inf`.
  - The small-`K` end (`rho` of order `N`, `K = 1`) is also covered, because
    `sqrt(2 log N/(K rho beta)) -> 0` there.
- **Counting.** Nodes with `|Wr| > K` have a pruned ancestor with
  `|Wr| = K`, because each branching adds at most one wrong fixing. So
  `#nodes <= (N+1) sum_{j<=K} C(N,j)`, as stated.

**Numerics** (`topk_check.log` (b)). I computed `T_K` for `N = 10^4, 10^5, 10^6`,
`beta = 1, 2`, and `rho` from `2.5 log N` to `N/beta`, including `K = 1..3`.

- The mean of `T_K` is 0.66–0.79 of `K(t+1)`.
- In 5,100 draws, the w.h.p. bound was never exceeded.

**Finite-size factor** (`topk_check.log` (c), `N = 10^6`).

| `rho beta/log N` | `kappa_rho` | `kappa_N` | realised `1 - T_K/(K sqrt(rho beta))` |
|---:|---:|---:|---:|
| 2 | 0.23 | 0 | 0.49 |
| 4 | 0.42 | 0.29 | 0.61 |
| 8 | 0.57 | 0.50 | 0.70 |
| 16 | 0.69 | 0.65 | 0.78 |

## 2. Theorem 3.1(d)

- **Reduction.** For `rho = theta N`, `b_i = sqrt(theta) h~_i`. The vector
  `v_i = w + 2 b_i` is exactly `N(0, (1+4theta) I_M)` and independent of
  `B_{-i} = sqrt(theta) H~_{-i}`. Dividing by `c = sqrt(1 + 4theta)` gives
  noise `xi` and matrix `sqrt(theta/(1+4theta)) H~_{-i}`, which is
  `sqrt(rho'/N') H'` with `rho' = theta(N-1)/(1+4theta)` and `N' = N-1`. So
  `r_i = c^2 R'`, where `R'` is the root value of the model with
  `(N', M = N' + 1, rho', x*' = 1)`. The two problems have the same
  minimizer.
- **Checks** (`c1d_reduction.log`).
  - (a) The identity holds to `3e-16`.
  - (b) Over 400 + 400 samples at `N = 100`, `theta = 0.2`: `r_0/c^2`
    against fresh root values gives KS p = 0.76. The largest NNLS coefficient
    `U` of the node, against that of a fresh root problem, gives medians 3.43
    and 3.48, KS p = 0.28. These medians match the easy review's 3.5 at
    `N = 100`.
- **Box inactivity.** By Corollary 1.4(b,c), the node is box-inactive iff
  `U <= 2 sqrt(rho')`.
- **Hu–Lu input.** In their normalization the reduced instance has
  `A = H'/sqrt(N')`, `sigma^2 = 1/rho_0` and `delta_p = N/(N-1) -> 1 > 1/2`.
  Then `alpha_p = (delta_p - 1/2) rho_0/(2 log N') = 1 + eps` exactly, and
  `sigma^2 log^2 p = log^2 N/rho_0 -> inf`. By sign symmetry, the choice
  `x*' = 1` is harmless.
- **Conclusion.** Corollary 1.4(d) then gives `U < sqrt(rho_0) = O(sqrt(log N))`
  against the threshold `2 sqrt(rho') = Theta(sqrt N)`. The rest (Lemma 0.2
  for one node, `chi^2` concentration, `OPT = W`) is routine and correct.
- **Finite `N`** (`theta = 0.2`, node 0; `c1d_reduction.log` (c)). Every node
  was box-inactive (largest NNLS coefficient at most 1.9). The mean of
  `(r_0 - W)/N` is close to the first-order value `-0.10`.

  | `N` | instances | `r_0 < W` | mean `(r_0 - W)/N` |
  |---:|---:|---:|---:|
  | 100 | 200 | 133 | -0.085 |
  | 200 | 200 | 160 | -0.105 |
  | 400 | 100 | 88 | -0.115 |

## 3. Proposition 6.3

- **Proof.** `x_i^2 = 1` on vertices, so `f_d = f` there. The Hessian is
  `2(A'A - dI)`, which is PSD iff `d <= lambda_min(A'A)`. The gradient gives
  `x*_i d_i f_d(x*) = -2 zeta_i - 2d`. The first-order condition is necessary
  and, by convexity, sufficient. So `x*` minimizes `f_d` over the box iff
  `min_i zeta_i >= -d`. In that case the relaxation value is
  `f_d(x*) = W >= OPT >= ` relaxation value, so the root is exact (and `x*` is
  ML) with no separate ML argument. Taking `d = lambda_min(A'A)`, the
  condition `lambda_min(A'A) >= max_i(-zeta_i)` is the same sufficient
  condition as in Theorem 6.2, so the stated threshold follows. The
  `4d(k - sum p_i^2)` barycenter term of Section 4.3 is also correct.
- **Checks** (`shift_check.log`).
  - (a) `f_d = f` on 400 random vertices; the Hessian's minimum eigenvalue is
    `>= -5e-16` relative; the gradient identity holds to `2e-8` (finite
    differences).
  - (b) On 160 instances (`beta = 2`, `N = 40`, `d = lambda_min` exactly,
    CVXPY/Clarabel), the rule "the QP minimizer is `x*` iff
    `min zeta >= -d`" held in 160/160.

## 4. Theorem 5.1(a), upper half

- **Hamming-ball reduction.** A conflicting pair `x^S, x^{S'}` has midpoint
  `c = 1_S + 1_{S'}` with `n_1 = |S Δ S'|` and `F(c) < OPT - eps' <= W`. So
  `omega <= sum_{j <= D} C(N,j)`, for every `eps' >= 0`, and without needing
  `OPT = W`.
- **Small regime.** `x = rho(n_1 + 4n_2)/(4N) <= rho(n_1+n_2)/N <= x0`, and
  `sum_m C(N,m) N^{-c'm/2} <= exp(N^{1-c'/2})`.
- **Tail sum.** With `D = e^2 N^{1-c'/8}`, each term is at most `e^{-n}`. The
  sum is at most `(1-1/e)^{-1} e^{-D} exp(N^{1-c'/2}) <= 2 exp(-D + N^{1-c'/2})`,
  and `1 - c'/2 < 1 - c'/8`.
- **Large regime.** It is as in Theorem 2.3 and uses `rho -> inf`, which holds.
- **Result.** Letting `x0 -> 0` gives `exp(N^{1-c/8+delta})`.
- **Numerical check.** On a grid (`N = 10^3..10^6`, `c' = 0.5..7.5`), the
  display and the tail bound both hold: `log(lhs/rhs)` is at most `-1.0`
  and `-0.59` respectively (`clique_moment.log` (b)).

## 5. Sphere-decoding comparison

My implementations (`sd_vs_box.py`):

- **Fincke–Pohst.** Depth-first and recursive (the note's code is
  level-synchronous), with QR, natural order `x_N, ..., x_1`, and radius
  `f(x*)`.
- **Box static-order B&B.** Order `1..N`, depth-first, fixed incumbent
  `f(x*)`, pruning on a certified Lagrangian bound, and node problems solved by
  scipy's BVLS rather than NNLS.

Both count the root plus both children of each expanded node. FP found no
vertex other than `x*` within the radius, so `x*` is ML and the tree does not
depend on the node order.

| `N` | FP per seed 0–5 | geo. mean | box per seed | geo. mean |
|---:|---|---:|---|---:|
| 32 | 945, 1631, 487, 1169, 933, 427 | 839 | 103, 137, 63, 65, 127, 73 | 90 |
| 48 | 5961, 6389, 11387, 7851, 7417, 9899 | 7937 | 91, 167, 105, 215, 261, 251 | 168 |
| 64 | 48835, 37333, 10661, 424835, 204591, 31373 | 61289 | 153, 379, 129, 417, 351, 201 | 246 |

All 36 numbers equal `data/check_revision_D.log` and Table 7.3 (`c4` rows).
Branched box nodes had at most 3 wrong fixings.

## Other findings and suggested fixes

- **F1 (Summary (4)).** "Static-order variable branching ... needs at most
  `exp((1 + o(1)) (N/(4(2beta - 1) rho)) log rho)` nodes for every
  `rho -> inf`, `rho beta <= N`" drops the factor `N+1` of Theorem 4.1.
  - At `rho = N/beta` this would give at most `N^{1/4 + o(1)}` nodes.
  - But the root gap is about `N/2`, so the path to `x*` alone has about `N`
    nodes.
  - Fix: write `(N+1) exp(...)`, or `+ O(log N)` in the exponent as
    Corollary 4.4 does, or restrict the sentence to `rho = o(N)`.
- **F2 (Section 6 and Section 10, C7).** "0.066, 0.034, 0.010 and 0.000 at
  `rho = 30, 60, 130, 300`": the last value is `3.9e-4` (max `4.2e-4`) with
  `d = lambda_min`.
  - At `rho = 300`, `x*` is not the shifted box minimizer in any of the four
    instances, and the KKT condition fails in all four.
  - At `rho = 600` the relaxation is exact in 4/4 (`shift_check.log` (d)).
  - Fix: report `4e-4 (not exact; exact at rho = 600)`.
- **F3 (Proposition 6.3; suggestion).** Because the proposition's condition is
  an "iff", its threshold is sharp.
  - `lambda_min(A'A)/rho -> (sqrt(beta)-1)^2` and
    `max_i(-zeta_i)/sqrt(2 rho beta log N) -> 1`. So the shifted relaxation
    is not exact below `(1-eps) 2 beta log N/(sqrt(beta)-1)^4`, which is
    `136 log N` at `beta = 2`.
  - Per-instance thresholds, `rho/log N`, medians (`shift_check.log` (c)):

    | `beta` | `N` | shift | SDP |
    |---:|---:|---:|---:|
    | 2 | 100 | 73 | 4.6 |
    | 2 | 400 | 93 | 4.4 |
    | 2 | 1600 | 110 | 4.4 |
    | 4 | 100 | 4.5 | 0.71 |
    | 4 | 400 | 5.7 | 0.74 |
    | 4 | 1600 | 5.9 | 0.70 |

    My SDP medians agree with Table 7.5a.
  - "At the same SNR even the eigenvalue-shift relaxation is exact" is correct
    for the proved sufficient condition. However, the shift becomes exact only
    there: at `beta = 2` its per-instance threshold is 16–25 times the SDP's
    at `N = 100–1600`, and the ratio of the constants (`136/4`) is 34. One sentence
    would prevent a reader from equating the two relaxations. The qualitative
    conclusion (`Theta(log N)`, a superpolynomial separation from the box
    relaxation) stands.
- **F4 (Section 3 after the proof of (d); Conjecture 3.3; Section 10, R4).**
  "'Every node fails' needs `P(U > c sqrt N) = o(1/N)`" and "Equivalently ...
  `P(U > c sqrt N) = o(1/N)`" overstate the reduction.
  - The union bound makes the tail bound sufficient for all `N` nodes to be
    box-inactive w.h.p.
  - It is not necessary: the `N` node events share `w` and all but one column,
    so they can be strongly positively correlated (for example, through a
    small `s_min(H)`).
  - Fix: use "follows from" or "is implied by".
- **F5 (Theorem 3.1 hypotheses).** The statement fixes `beta` and `eps` but
  not `theta`.
  - The proofs of (b)–(d) need `theta N >> log N`. Part (b) needs
    `u°_j -> 0`. Part (c) needs `tau_i max s_j -> 0`. Part (d) needs
    `rho' >= (1+eps) log N` for the Hu–Lu comparison. Parts (b)–(d) need
    `OPT = W`.
  - Fix: "`theta > 0` fixed" (or `theta N/log N -> inf`).
- **F6 (Summary (6) and Section 7.3).** "The box relaxation still beats
  natural-order sphere decoding by a wide margin" holds in node counts.
  - An FP node costs `O(N)`; a box node costs a bound-constrained
    least-squares solve.
  - In my single-thread Python implementations, FP took 0.8 s and the box B&B
    3.4 s for the six `N = 64` instances (`sd_timing.log`; indicative only).
  - Fix: add "in node count". The growth statement is unaffected.
- **F7 (Section 10, C5; check part E).** The `N = 10^5`, `c = 3` cell of
  `check_revision_E` stops at the scan's loop limit (`n_1 = 19999`).
  - Uncapped, the last `n_1` is 20199, ratio 15.1 (`clique_moment.log` (a)).
    The other five cells agree exactly.
  - The stated range "3–15 times" stands. Fix: mark that cell as capped.
- **F8 (Status line, lines 6–7).** "not independently reviewed" contradicts
  Section 10 and the Summary, which describe two independent reviews.
- **F9 (Section 4.1 Remarks; not an error).** The remark compares the realised
  factor only with the old `kappa_N`.
  - The proved factor `kappa_rho` is 0.20–0.69 at `N = 10^6`,
    `rho beta = 2–16 log N`, `beta = 1, 2`.
  - So at practical sizes the proved exponent is 1.5–5 times the
    asymptotic constant.
  - Suggestion: quote `kappa_rho` alongside `kappa_N`.
- **F10 (notation, minor).** In the proof of Theorem 5.1(a), `c` denotes both
  `rho beta/log N` and the ternary vector (for example, "If `c > 2`, `OPT = W`"
  follows a paragraph about `c = 1_S + 1_{S'}`).

## Commands run (targeted, local)

All were run from `reviews/mimo-recheck/`, single-threaded
(`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`), one process at a time:

```
python3 sd_vs_box.py 32      > sd_vs_box_32.log       # item (5), about 1 s
python3 sd_vs_box.py 48 64   > sd_vs_box_48_64.log    # item (5), about 5 s
python3 sd_timing.py         > sd_timing.log          # F6
python3 c1d_reduction.py     > c1d_reduction.log      # item (2), about 2.5 min
python3 shift_check.py       > shift_check.log        # item (3), F2, F3, about 1 min
python3 topk_check.py        > topk_check.log         # item (1), F9
python3 clique_moment.py     > clique_moment.log      # item (4), F7
```

All outputs are as quoted above. These are my own targeted checks. I did not
rerun the note's `code/`, run project-wide checks, or inspect CI.
