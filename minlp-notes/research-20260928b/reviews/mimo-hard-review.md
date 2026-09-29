# Review: hard side (result (4)) of the binary-least-squares certification note

Reviewed file:
[`../bb-complexity/binary-least-squares/certification-thresholds.md`](../bb-complexity/binary-least-squares/certification-thresholds.md)
(untracked; mtime 2026-09-29 04:39, md5 `1397c681…`). Scope: summary item (4),
Sections 4 and 5, Theorem 2.3, the parts of Theorem 2.2 that Section 4 uses, the
tree predictor and its extrapolation (Section 7.3), and the hard-side
statements in Section 8. Background: Sections 1 and 5 of the integer-core note.
Reviewer: independent agent (probability, combinatorics, IP proof complexity).
I did not write the note, and I did not edit it. Date: 2026-09-29. My scripts
and logs are in [`mimo-hard/`](mimo-hard/). All checks are targeted and local
(Section 10). No project-wide checks were run and CI was not inspected.

## Verdict

The two main theorems are correct. I checked every step of Theorem 4.3 (class
number) and Theorem 4.1 (static-order upper bound), including the
probabilistic events, the constants, the range of `rho`, and the handling of
`OPT`. I found no counterexample and no gap. Lemma 4.2 (entropy lemma) is
correct. Theorem 2.3 and Theorem 5.1(a,b) are correct. The search/certification
statement lines up with Papailiopoulos' theorem for `beta = 1`, which I read in
the PDF.

The side statements need corrections:

- One comparison in Section 8 is wrong for square systems (C3).
- Several summary sentences are broader than the theorems (C1, C4, C7, C8).
- One two-sided claim is proved only on one side (C5).
- The predictor's extrapolation is labeled heuristic in Section 7.3 but not in
  the summary. Its agreement with Conjecture 4.5 is partly circular (C6).

The proof of Theorem 4.1 also gives more than stated. The loss factor
`kappa_N` is an artifact, and the upper bound extends below the ML threshold
(S1).

| Claim | Verdict | Notes |
|---|---|---|
| Lemma 4.2 (entropy lemma) | **correct** | All steps checked by hand: the KL identity, `phi(p) >= L p(p - lambda/2)` by concavity at both endpoints, and `L >= 1`. Elementary; the extremal loss of a factor 2 is as stated. |
| Theorem 4.3, `log kappa >= c_beta (N/rho) log rho - log 8N` | **correct (asymptotic)** | Barycenter identity, `X/W < 0.04`, `-1.96X`, slack 1.71 over `lambda_1`, counting via integer-core Lemma 1.5(b), and absorption into `log 8N` all check. The events do not depend on the class, so no union bound over classes is needed. |
| Constants `c_beta = beta p/(64 e^2 (sqrt beta + 1)^4)`, `1.8e-5`, `rho_0(1) = 71` | **correct** | Recomputed: `c_1 = 1.796e-5`, `c_2 = 1.692e-5`; `rho_0(1) = 70.7` as written (69.1 would suffice). The implicit `c'_1 ≈ 1.4e-4` is not stated. |
| Range `rho_0 <= rho <= c'_beta N`; `OPT` handling | **correct** | The proof does not need `x*` to be ML. It needs `Delta + eps' <= 0.5 a k` with `Delta = W - OPT`, which Theorem 2.2(a)/(c) supplies. |
| Finite-`N` content of Theorem 4.3 | **not stated; vacuous at practical sizes** | For `beta = 1` the bound is positive only from `N ≈ 1.7e7` (`rho = 4 log N` or `rho = 71`). It exceeds `10 log N` only from `N ≈ 2e8`. The range `[71, c'N]` is nonempty only for `N ≳ 5e5` (C9). |
| Coverage: splits, multiway, semantic, cuts in `x`, `kappa/(N+1)` with incumbent-based tightening | **correct for the box relaxation `phi = f` on `[-1,1]^N`** | Follows from integer-core Theorems 1.6, 1.8(a), 1.8(c). Not covered: relaxation changes that use `x_i^2 = 1` (diagonal shift/QCR, RLT/McCormick linearization, SDP), and tolerances `eps' > 0.25 a k` (C7, C8). |
| Theorem 4.1 (static order, `exp((1+o(1)) (N/(4(2beta-1) kappa_N rho)) log rho)`) | **correct; weaker than the proof allows** | Every event and union bound checks. `kappa_N` can be replaced by `1 - sqrt(2 log(Cρ)/(rho beta)) -> 1` for every `rho -> inf`, and the bound extends below `2 log N/beta` (S1). |
| "`log(tree) = Theta((N/rho) log rho)` for all kinds of certificates" | **correct on the stated range, but the constants differ by a factor ~4e4–9e4** | The table row "`rho_0 <= rho = o(N)`" is broader than Theorem 4.1 as stated. The gap `rho -> inf`, `rho beta <= 2 log N` is closed by S1 (C1). |
| Search/certification gap at `rho = c log N` with Papailiopoulos | **correct for `beta = 1`, `c > 2`** | His Theorem 2.1(a) gives exact block recovery in `O(N^3)` operations, uniformly over `x*` and all `rho >= 2 log N`, in the same normalization. The gap is specific to box-relaxation certificates (for `beta > 1` the SDP closes it). The parenthetical in summary (4) applies only to `beta = 1` (C10). |
| Theorem 2.3 (no midpoint conflicts above `8 log N`) | **correct** | First-moment sums checked. |
| Theorem 5.1(a) (`exp(N^{1-c/8-delta})` cliques) | **correct** | Code construction, cross terms and union bound check. The two-sided "`exp(N^{1-c/8+o(1)})`" after the theorem needs an upper bound that the note does not prove; a first-moment proof is given below (C5). |
| Theorem 5.1(b) (fixed `rho >= rho_1`) | **correct; `rho_1` unstated and large** | The proof as written needs `rho ≳ 600` (`beta = 1`), `≳ 300` (`beta = 2`). |
| "pairwise conflicts are blind on `8 log N < rho = o(N)`" | **overstated** | Proved for the midpoint graph only. The segment graph is nonempty; its chromatic number is not analysed (C4). |
| "Gaussian bases … cause no difficulty here" | **true for the binary problem; says nothing about integer-core Conjecture 3.8** | The binary box and the unbounded lattice are different problems (Section 4.3 below). |
| Predictor `f(x^Wr)(1 - n/(2M))` and extrapolation to `N = 1e5` | **labeled heuristic in Section 7.3 and the appendix; not labeled in summary (6)** | Node-level error is small, but the predictor underpredicts the capped `N = 256`, `4 log N` runs that Table 7.3b excludes. Agreement with Conjecture 4.5 is partly circular (C6). |
| Section 8: "The box relaxation therefore does not change the order of the exponent of enumeration" | **wrong for `beta = 1`; unsupported in general** | JO is a lower bound only. Natural-order Fincke–Pohst has a typical exponent of order `N/sqrt(rho)` for square systems. Measured: `1.7e5` FP nodes versus 246 box static nodes at `N = 64`, `rho = 4 log N` (C3). |
| Corollary 4.4 bullet: "the same order as the Jaldén–Ottersten lower bound" | **imprecise** | Section 8 correctly says "up to the factor `log rho`" (C2). |

## 1. Theorem 4.3 (class number): step-by-step

### 1.1 Setup and events

Conditioning on `w` and using Lemma 0.1:

- `zeta_i = a g_i` with `a = sqrt(rho/N)||w|| = sqrt(rho beta)(1 + O(sqrt(log N/N)))`.
- `T = {g_i in [-2,-1]}` depends only on `g`.
- `H^perp_T` is, after rotation, an `(M-1) x n'` Gaussian matrix independent
  of `g`.

So `sigma_T <= sqrt(M-1) + sqrt(n') + sqrt(2 log N)`, which is at most
`sqrt N (sqrt beta + 1)(1 + o(1))` with probability `1 - 1/N`. Also `n' >= pN/2`
w.h.p. by Hoeffding. None of these events refers to a class. This is the key
design point: the operator norm bounds `||H^perp c||^2` for every `c` supported
on `T` at once. Monte Carlo (`barycenter_mc.log`, 20 instances with
`N = 1000, 3000`, `beta = 1, 2`, `rho = 10..160`) gives:

| quantity | measured |
|---|---|
| `n'/(pN)` | 0.81–1.08 |
| `a/sqrt(rho beta)` | 0.97–1.05 |
| `s_max/(sqrt(M-1)+sqrt(n'))` | 0.98–1.005 |
| `s_max/(sqrt N sigbar)` | 0.67–0.75 (the `sigbar` bound is loose, as expected) |

### 1.2 The barycenter inequality

For a class `I` with `F_I` a family of `k`-subsets of `T`:

- The barycenter `u = c = 2p` lies in `conv I ∩ box`.
- `f(xbar) - W = -2X + X^2/W + (rho/N)||H^perp c||^2` (identity checked by
  hand; the note's L4 checks it numerically).
- `sum c_i = 2k` gives `2ak <= X <= 4ak`.
- `X/W <= 4ak/W <= 1/(e^2 sigbar^2) = 0.0338` for `beta = 1`, so
  `-2X + X^2/W <= -1.96 X <= -3.92 ak`.
- `(rho/N)||H^perp c||^2 <= 4 rho sigbar^2 (1+o(1)) sum p_i^2`.

Admissibility then gives `sum p_i^2 >= (3.42 ak)/(4 rho sigbar^2)(1-o(1))`. This
equals `1.71 lambda_1 k (1 - o(1))`, so the claimed `>= lambda_1 k` holds with
room to spare.

On 1,232 families (disjoint, random, and star-shaped `k`-set families with
`k = 8`), the deterministic inequality
`f(xbar) - W <= -2X + X^2/W + 4(rho/N) s_max^2 sum p_i^2` was never violated.

The *actual* overlap threshold at which barycenters cross `W` is
`sum p_i^2/k ≈ 1.4/sqrt(rho beta)`. It matches the heuristic `2X/(4 rho beta k)`
in every run and is about 10–11 times the proof's `lambda_1 = 1/(8 sqrt rho)`
(`beta = 1`). A class can contain only about `0.7 sqrt(rho beta)` pairwise
disjoint `T`-vertices of weight `k`: the first undercutting `m` was 3–14 against
the heuristic 2.3–13.2. The mechanism works as described.

### 1.3 Counting

- The hypothesis of Lemma 4.2 is exactly `k <= lambda_1 n'/(2e^2)`.
- `log(n'/(ek)) >= log(2e/lambda_1) >= (1/2) log rho`, because
  `2e/lambda_1 = 4e sigbar^2 sqrt(rho)/sqrt(beta) >= 16 e sqrt(rho)`.
- `lambda_1 k >= beta p N/(16 e^2 sigbar^4 rho) - lambda_1`.
- The discarded terms `(lambda_1/4) log rho <= 0.023` and `(1/2) log(8k)` fit
  inside `log(8N)`.
- Integer-core Lemma 1.5(b) then gives `kappa >= C(n',k)/max_I |F_I|`.

All correct. Lemma 4.2 itself:

- `H(S) <= sum h(p_i)`.
- `h(q) - h(p) = d(p||q) + (p-q) log(q/(1-q))`.
- `d(p||q) >= p log(p/q) + q - p`.
- `L = log(1/(eq)) >= log(2e) >= 1`, because `sum p_i^2 <= k` forces
  `lambda <= 1`.
- The concave comparison is nonnegative at `p = lambda/2` (value `>= 1`) and at
  `p = 1` (value `L lambda/2`).
- `log C(n,k) >= n h(k/n) - (1/2) log(8k)` is the standard bound.

### 1.4 Constants and range (`constants.log`, Part A–B)

- `p = 0.135905`. `c_beta = 1.796e-5, 1.760e-5, 1.692e-5, 1.419e-5` for
  `beta = 1, 1.5, 2, 4`.
- `ak/N ≈ beta p/(8 e^2 sigbar^2) = 5.75e-4` (`beta = 1`). The proof needs
  `eps' <= rho <= 0.25 ak`, so implicitly `c'_1 ≈ 1.4e-4`. The condition
  `k >= 1` is much weaker.
- `rho_0`: the note's condition gives 70.7. The condition actually needed
  (`4N e^{-0.148 rho} <= 0.25 ak` to leading order) gives 69.1. The constant
  `0.148` is `log(8)/14 = 0.1485`; correct.
- Finite `N`: see C9.
- The ratio between the upper exponent (Theorem 4.1) and the lower exponent
  (Theorem 4.3) is `3.7e4–9.0e4` for `rho = 3..8 log N` (Part C). "Theta" is
  correct but hides this factor.

### 1.5 Is `OPT` correctly identified?

Yes. The class number is taken at `tau = OPT - eps'` with the true binary
optimum. The proof uses only `Delta = W - OPT >= 0` and needs
`Delta + eps' <= 0.5 ak`:

- For `rho beta >= (2+eps) log N`, `Delta = 0` w.h.p. (Theorem 2.2(a); I
  re-checked the small/large split and `(1+eps/2)(1-eps/8) >= 1+eps/4` for
  `eps <= 2`).
- Below that, Theorem 2.2(c) gives `Delta <= 4N log(1+e^{-0.148 beta rho}) + 4 log N`.
  I re-derived this: the `log(1+x) >= x log 8/7` step for `x <= 7`, and
  `1 - (1/2) log 8 < -0.039` for `x > 7`.

`x*` need not be ML. The conclusion for `rho_0 <= rho < 2 log N/beta` is
therefore sound.

### 1.6 What exactly is covered

Covered, with `P = {-1,1}^N` and `phi = f` on the box:

- every `P`-covering convex-piece certificate: variable, split, multiway or
  semantic branching, any rule and node order, weaker computed bounds (integer-core
  Lemma 1.3 and Theorems 1.6–1.7);
- cuts in `x` valid for the node's vertices (Theorem 1.8(a));
- incumbent-based tightening on binaries (OBBT, probing, reduced-cost fixing),
  giving at least `kappa/(N+1)` nodes (Theorem 1.8(c)).

Also covered, although the note does not say so:

- *Weaker* relaxations (integer-core Remark 1.11), in particular the
  unconstrained partial-distance bound of Fincke–Pohst/Schnorr–Euchner sphere
  decoders. So Theorem 4.3 also lower-bounds sphere-decoder trees per instance
  w.h.p. The asymptotic order is `log rho` times larger than Jaldén–Ottersten's.
  But `c_1 log rho` exceeds JO's constant `(log 2)/4 ≈ 0.17` only when
  `log rho > 9.6e3`, so the JO bound is numerically stronger in every realistic
  regime.

Not covered (the note is right to say "for the box relaxation", but the
summary's "every convex-piece certificate" can be misread):

- Relaxation changes that use `x_i^2 = 1`. Examples: the diagonal-shift/QCR
  reformulation `f + sum d_i (1 - x_i^2)` with `A'A - D ⪰ 0`, RLT/McCormick
  linearization of products, and the SDP.
  - For `beta > 1`, the smallest-eigenvalue shift `d = lambda_min(A'A) ≈ rho(sqrt beta - 1)^2`
    adds `4d(k - sum p_i^2)` at the barycenter.
  - For `beta = 2` this exceeds the barycenter gain `≈ 5.5 sqrt(rho beta) k`
    once `rho ≳ 130` (my estimate from the same first-order formulas).
  - So the barycenter argument fails for that reformulation.
  - Standard MIQP solvers may apply such reformulations to binary quadratics.
- Certificates with tolerance `eps' > ~0.25 ak ≈ 1.4e-4 N` (`beta = 1`). See C8.

### 1.7 Tiny instances, exact class numbers (`tiny_kappa.py`, `summarize_tiny.log`)

I computed exact class numbers by brute force on 590 instances: `N = 5, 6`
(20 seeds per cell) and `N = 8` (5 seeds), `beta = 1, 2`,
`rho = 1..64`, `eps' = 1e-7`. The method is an exact minimum partition search
with Wolfe's min-norm-point oracle, validated against SLSQP to `1e-15`. Along
with `kappa` I computed:

- the midpoint and segment graphs, `omega(G^mid)`, `omega(G^seg)` and
  `chi(G^seg)`;
- the exact minimum number of leaves of an adaptive variable-branching
  certificate (DP over all `3^N` subcubes);
- the leaves of the static-order certificate.

Results:

- 587 of 590 instances were solved exactly. In the other 3 the search budget
  was hit and `kappa` is bracketed.
- The chain
  `omega_mid <= omega_seg <= chi_seg <= kappa <= L_var <= L_static` holds in all
  590 instances.
- No admissibility decision lay within `1e-10 (1+OPT)` of `tau`.
- In 372 instances the midpoint graph has no edges. Of these, 351 have
  `kappa >= 2` and 29 have `kappa = 3`.
- In 36 instances, `kappa > chi(G^seg)`: the class number lies strictly above
  every pairwise bound.
- `kappa < L_var` in 449 instances and `L_var < L_static` in 498.

At these sizes the asymptotic regimes cannot be tested (at high SNR,
`kappa = 2` in almost all cells). But the framework inequalities and the
non-pairwise character of `kappa` are confirmed exactly.

## 2. Theorem 4.1 (upper bound)

All steps check:

- The free set `{d+1..N}` is independent of `v = w + 2 B_Wr 1` for a
  data-independent order.
- `||v||^2(1-Y)` lower-bounds the node value (Moreau decomposition; upper bounds
  dropped).
- Lemma 0.2, including the mixture step and both tails, is correct as written.
- The four events hold with the stated union bounds: `(N+1)C(N,K)` nodes and
  `C(N,K)` subsets for `s_min`.
- `WY/(1-Y) <= beta N (1+o(1))/(2beta-1)`.
- Induction: nodes with `|Wr| = K` are all pruned, so no processed node has
  `|Wr| > K`.
- The count `(N+1) sum_{j<=K} C(N,j)` follows.

The static order and the given incumbent are genuinely needed, as the Remarks
say.

**S1 (strengthening; not an error).** The factor `kappa_N = 1 - sqrt(2 log N/(rho beta))`
comes from bounding `sum_{i in Wr} zeta_i >= -K a max_i(-g_i)`.

- One can instead use the sum of the `K` most negative `g_i`. With `q = K/N`,
  its mean is `N phi(t_q) <= K(t_q + 1/t_q)`, where `t_q <= sqrt(2 log(N/K))`.
  It is `sqrt K`-Lipschitz, so it concentrates when `K >> log N`. For
  `K = O(log N)`, `rho >= N/log N`, and the crude bound already gives
  `kappa_N -> 1`.
- With `N/K ≈ 4(2beta-1) rho` this gives
  `D_Wr >= 4 rho beta K (1 - sqrt(2 log(4(2beta-1)rho)/(rho beta)) - o(1))`.
  The factor tends to 1 for every `rho -> inf`, not only when
  `rho/log N -> inf`.
- Numerically (`constants.log` Part D, `N = 1e6`, `rho = 4 log N`): the top-`K`
  mean of `-g` is 2.91, against `max(-g) = 4.57`. The loss factor is 0.56
  (refined) instead of 0.29 (`kappa_N`).
- Below the ML threshold only `OPT - eps' >= W - Delta - eps'` is needed.
  With `Delta = o(N)` (Theorem 2.2(b,c)), the same proof then gives
  `log #nodes <= (1+o(1)) (N/(4(2beta-1)rho)) log rho` for every
  `rho -> inf`, `rho beta <= N`, given the incumbent value.

This closes the range gap in the summary table (C1) and gives the sharp upper
constant of Conjecture 4.5 at `rho = c log N` for every `c`.

## 3. Corollary 4.4 and the search/certification gap

Papailiopoulos (arXiv 2609.19405, v. 16 Sep 2026; PDF read, Section 1 and
Theorem 2.1):

- The model is `y = sqrt(rho/N) H x* + w` with square `H`, so the
  normalization matches the note with `beta = 1`.
- Theorem 2.1(a): `lim_N sup_{x*, rho >= 2 log N} P(xhat != x*) = 0`, with
  `O(N^3)` unit-cost real operations. This is exact block recovery, uniform
  over *all* `rho >= 2 log N`, so it covers `2 log N <= rho = o(N)`.
- Remark A.2 gives ML success at `rho >= 2 log N`.

The note's lower bound (Theorem 4.3) holds throughout `rho_0 <= rho <= c'N`. Its
upper bound (Theorem 4.1) needs `c > 2`, or any `c` with S1. So at every
`rho = c log N` with `c > 2` (`beta = 1`):

- the ML point is `x*`;
- it is found in polynomial time;
- every box-relaxation certificate has `exp(Theta(N log log N/log N))` leaves.

The regimes line up.

Two qualifications:

- The gap is for one proof system, box-relaxation branch-and-bound. For
  `beta > 1` the Shor SDP certifies `x*` at `rho = O(log N)` (Theorem 6.2), and
  for `beta = 1` it is open whether any polynomial-size certificate exists. The
  note says this in Section 6. The summary's phrase
  "polynomial-search / superpolynomial-certification gap" should keep
  "for this relaxation" (Section 8 does).
- Papailiopoulos covers `beta = 1` only. For `beta > 1`, polynomial-time search
  between the ML threshold `2 log N/beta` and the box-decoder threshold
  `4 log N/(2beta - 1)` is not covered by the cited results (C10).

## 4. Midpoint cliques, pairwise blindness, Gaussian bases

### 4.1 Theorems 2.3 and 5.1

Theorem 2.3:

- The small-`x` terms are bounded by `N^{-(eps/16)n_1 - 3n_2}/(n_1! n_2!)`,
  which sum to `o(1)`.
- The large-`x` part uses `C(N,n)2^n` and `||c||^2 >= n`. Its bracket
  `t log(2e/t) - (beta/2) log(1+rho t/4)` is uniformly negative because
  `rho -> inf`.

Correct.

Theorem 5.1(a):

- `P(i in T) = N^{-(1+2eta)^2 c/8 + o(1)}`.
- The greedy code has at least `e^{eta m}` members. The bound
  `(em/(eta n_T))^{eta m} <= e^{-eta m}` uses `m <= eta n_T/e^2`.
- `||c||^2 = 2m + 2|S∩S'| <= 2m(1+eta)`.
- The `(rho/N)(g'c)^2` term is `O(rho m/N) mu m = o(mu m)`.
- The chi-square union bound over `e^{2 eta m + 2}` pairs is fine because
  `m = N^{1-Omega(1)}`.
- `Delta = N^{1-c/2+o(1)} = o(mu m)` because `(1+2eta)^2 < 4`.

Correct.

Theorem 5.1(b) is correct. The union-bound error is `O(sqrt(eta m/M))`, not
`O(eta)`, so `eps_1` must be taken small depending on `eta`, as the proof
says. `rho_1` is not given. Following the proof as written, it is about 600,
300 and 150 for `beta = 1, 2, 4` (`rho1_estimate.log`). Theorem 4.3 already
gives exponential class numbers from `rho = 71`.

**C5 (missing upper bound).** After Theorem 5.1 the note says the midpoint
clique "is `exp(N^{1 - c/8 + o(1)})`", which is two-sided. Only the lower
bound is proved. A first-moment proof of the upper half:

- If every ternary `c` with `F(c) < W` has at most `D` entries equal to 1,
  then all members of a clique lie within Hamming distance `D` of one member.
  So `omega <= sum_{j<=D} C(N,j) = exp(D log(eN/D))`.
- By Lemma 2.1, in the small regime the expected number of such `c` with
  `n_1 = n` is at most `(e N^{1-c'/8}/n)^n exp(N^{1-c'/2})`, with
  `c' = c(1 - x0/2)`.
- Take `D = e^2 N^{1-c'/8}`. Then this is at most
  `exp(-D + N^{1-c'/2}) -> 0`, since `1 - c'/2 < 1 - c'/8`. The large regime
  is as in Theorem 2.3.

So `omega(G^mid) = exp(N^{1-c/8+o(1)})` holds. The numbers
(`constants.log` Part E, `N = 1e4, 1e5`) put the last `n_1` with a
non-negligible expected count at 3.0–10 times `N^{1-c/8}`, consistent with an
`N^{o(1)}` factor. For `c = 2.5`, `N = 1e5` it is at least 7.3 times; the
scan was capped.

### 4.2 "Pairwise conflicts are blind" (C4)

Theorem 2.3 shows `G^mid` has no edges, so its clique and chromatic numbers
are 1. The segment graph is not empty:

- `x*` conflicts with every `x^{i}` with `zeta_i < 0`, as the note itself says.
- `chi(G^seg)`, also a pairwise bound `<= kappa`, is not analysed.

The phrase "pairwise conflicts are blind" in summary (4) and the Section 2.3
wording should say "midpoint conflicts". In my tiny instances `chi(G^seg)`
was usually 2 at high SNR. First-order computations suggest that segments
between two `T`-vertices behave like midpoints. So `chi(G^seg) = O(1)` above
`8 log N` is plausible, but it is not proved.

### 4.3 Gaussian bases

The statement is true in the following sense:

- For the binary problem the obstruction is the box's tangent cone at `x*`.
  The class-number proof uses only Gaussian column statistics, not lattice
  geometry (Siegel moments, `lambda_1`).
- Short lattice vectors play no role, because only `{0, ±2}^N` differences
  occur.

But the integer-core concern (its Section 3.6(iv), Conjecture 3.8) is about
unbounded integer variables with the unconstrained relaxation, where the root
bound is 0 and there is no box. The binary result neither uses nor resolves
that conjecture. "This answers the scout's concern … for the binary problem"
should read "sidesteps", with an explicit note that Conjecture 3.8 remains open.

## 5. Predictor and extrapolation

Labeling:

- The knapsack extrapolation is labeled "(heuristic)" in Section 7.3.
- The appendix says "a heuristic model, not a certificate".
- The code docstring says "heuristic, not a certified computation".
- Summary item (6) is not labeled. It reads "extrapolates to `e^{~80}` …
  `e^{~1900}`" without qualification. Add "(heuristic model; not a bound)".

My checks (`predictor_check.log`):

- **Node level.** On 360 random static-order nodes of real instances
  (`N = 200, 400`, `beta = 1, 2`, `rho = 4 log N`, `d = N/8..N/2`,
  `|Wr| <= 5`), `(true bound - predictor)/(4 rho beta)` has mean in
  `[-0.12, 0.25]` and sd 0.08–0.26, with extremes −0.60 and +1.26.
  All nodes were box-inactive. So the node approximation is good to a fraction
  of one wrong fixing, as the first-order law says.
- **Capped runs.** Table 7.3b excludes capped runs. At `N = 256`,
  `rho = 4 log N` (the regime the extrapolation targets), all four real
  static trees exceeded `1e5` nodes. The predictor gives 76,885, 50,259,
  141,113 and 56,993. So it underpredicts by at least 1.3–2 in three of four
  instances, consistent with the upward trend of real/pred ratios in
  Table 7.3b. "Within a factor of about 2" is not tested where it matters most.
- **Circularity.** The knapsack predictor uses the same first-order model
  (mean `Y`, no box activity, no cross terms) that motivates Conjecture 4.5.
  Its agreement with `(N/(4(2beta-1)rho)) log rho` (Table 7.3c) checks the
  asymptotic evaluation of that model. It is not independent evidence that
  real trees, or other rules, follow the constant. The note's appendix sentence
  "None of the computations is evidence for the asymptotic constants beyond
  the trends described" is appropriate. The sentence "Its log tree size
  approaches … (Conjecture 4.5)" should say this explicitly.
- **Rule.** The predictor is for the static order. Most-fractional trees were
  up to 12 times smaller at `N = 256`.

## 6. Sphere decoding comparison (C2, C3)

Section 8 says the note's result is "the same order, up to the factor
`log rho`", as JO, and concludes that "the box relaxation therefore does not
change the order of the exponent of enumeration". The conclusion does not
follow: JO give a lower bound on sphere-decoder complexity, not an upper bound.
For square systems it is also false, heuristically and in small-`N`
measurements (`sd_vs_box.log`).

- **Heuristic.** Fincke–Pohst with natural order and radius `W`: fixing `k`
  coordinates with `j` wrong gives partial distance `~ (1 + 4 rho j/N) chi^2_{M-N+k}`.
  - For `beta = 1` every partial vector survives up to level `k ≈ N/(2 sqrt rho)`.
  - A cruder uniform argument gives all `2^k` vectors surviving up to
    `k ≈ N/(4 sqrt rho)`.
  - So the exponent is of order `N/sqrt(rho)`. The typical-count maximum is
    `≈ 0.5 N/sqrt(rho)`, against the box model's `≈ (N/(4rho)) log rho`.
  - At `rho = 4 log N` the ratio of exponents is 3.7 (`N = 1e3`) to 4.4
    (`N = 1e6`). It grows like `sqrt(rho)/log rho`.
  - For `beta = 2` both exponents are `Theta((N/rho) log rho)`, with constants
    of about `1/(4(beta-1))` and `1/(4(2beta-1))`.
- **Measured** (`beta = 1`, `rho = 4 log N`, 4 seeds): the note's box static
  trees (Table 7.3, other seeds, same law) are 90, 246, 2000.

  | `N` | FP nodes, geometric mean |
  |---:|---:|
  | 32 | 1,070 |
  | 64 | 1.66e5 |
  | 96 | 2.6e6 |
  | 128 | `>= 2e7` (3 runs capped) |

So for square systems the box relaxation changes the order of the exponent,
from about `N/sqrt(rho)` to `(N/rho) log rho`, relative to natural-order
enumeration with the unconstrained bound. Data-dependent orderings (SQRD,
V-BLAST) were not examined.

Also, the JO bound as restated by Papailiopoulos, `2^{N/(4rho+2)} - 1`, is far
below both. The Corollary 4.4 bullet "the same order as the Jaldén–Ottersten
lower bound" should carry the `log rho` qualification, as Section 8 does.

## 7. Novelty

I could not run new web searches (the session's search budget was exhausted).
I fetched Papailiopoulos (PDF) and the DDM lower-bound abstract. Items marked
"memory" were not re-read.

- **Sphere-decoding complexity.**
  - Jaldén–Ottersten 2005 (via Papailiopoulos' restatement): the expected
    complexity of one algorithm, a lower bound `exp(Theta(N/rho))`.
  - Hassibi–Vikalo 2005: expected-complexity expressions.
  - Seethaler–Jaldén–Studer–Bölcskei 2011 (memory, and the note's abstract
    check): Pareto tails for infinite lattices.

  None gives per-instance lower bounds for all branching schemes with a
  relaxation-based bound. Theorem 4.3 is, to my knowledge, new in this
  respect, and it also applies to sphere decoders via the weaker-relaxation
  remark. Its constant makes it numerically weaker than JO everywhere
  practical.
- **Proof-complexity lower bounds for B&B.**
  - Dey–Dubey–Molinaro (arXiv 2103.09807; abstract read): exponential lower
    bounds for general-disjunction trees on packing, set-cover and TSP
    instances, and a *smoothed* bound for a Gaussian-perturbed cross-polytope.
  - Related: Basu–Conforti–Di Summa–Jiang; stabbing planes (Beame et al.);
    Dadush–Tiwari (memory).

  The note's contribution is a lower bound for a natural *planted* random
  model with a convex quadratic objective and a nonlinear relaxation, via the
  integer-core class number. The test-set counting is standard: integer-core
  Lemma 1.5(b), the analog of DDM/Kaibel–Weltge hiding sets. Lemma 4.2 is
  elementary (subadditivity plus KL). I do not know an identical published
  statement, but I would not claim it as a contribution. A missing classical
  precedent for random-instance B&B lower bounds is Chvátal, "Hard knapsack
  problems" (Oper. Res. 1980; memory): random knapsacks need `2^{Omega(n)}`
  nodes for a broad class of recursive algorithms. So do the positive results
  of Dey–Dubey–Molinaro ("B&B solves random binary IPs in polytime", arXiv
  2007.15192) and Borst–Dadush–Huiberts–Tiwari (memory), which make the
  contrast.
- **Search versus certification.**
  - The known gaps are for null models: Montanari's SK algorithm versus
    Bandeira–Kunisky–Wein's low-degree hardness of certifying bounds (cited by
    Papailiopoulos; memory for details).
  - In planted models, SDP dual certificates often certify exact recovery at
    the IT threshold (Abbe–Bandeira–Hall, Hajek–Wu–Xu; memory). The note's
    Theorem 6.2 is of this type.

  The note's gap is unconditional, but it holds for a single proof system (box
  B&B), and for `beta > 1` a stronger relaxation removes it. It is best
  described as a relaxation-specific certification lower bound in a planted
  model where search is easy. That is a clean and, as far as I know, new
  observation, not a computational search/certification gap.

## 8. Corrections requested

1. **C1 (range of "Theta").** The summary table's row "`exp(Theta((N/rho) log rho))`
   for `rho_0 <= rho = o(N)`" and summary (4) need a qualification:
   - the upper bound is proved only for `rho beta >= (2+eps) log N`;
   - it is trivial (`2^{N+1}`) at fixed `rho`.

   Either restrict the claim, or add S1, which closes the gap for all
   `rho -> inf`.
2. **C2.** Corollary 4.4 bullet: "the same order as the Jaldén–Ottersten lower
   bound" should read "the same order up to a `log rho` factor in the
   exponent". Add that JO's constant is larger unless `log rho > ~1e4`.
3. **C3.** Section 8: delete or restrict "The box relaxation therefore does not
   change the order of the exponent of enumeration". It does not follow from a
   lower bound. For `beta = 1` it is contradicted by the natural-order
   Fincke–Pohst exponent `Theta(N/sqrt rho)` (heuristic) and by the
   measurements in Section 6. For `beta > 1` it is plausible.
4. **C4.** "Pairwise conflicts are blind" should be "midpoint conflicts are
   blind". The segment-graph chromatic number is not analysed.
5. **C5.** Either prove the upper half of "midpoint clique is
   `exp(N^{1-c/8+o(1)})`" (argument in Section 4.1) or state it one-sided.
6. **C6.** Summary (6): mark the extrapolation as a heuristic model. In
   Section 7.3:
   - note that the capped `N = 256` runs are excluded and that the predictor
     underpredicts them;
   - note that agreement with Conjecture 4.5 checks the model, not real trees.
7. **C7.** Summary (4) and Theorem 4.3's consequence paragraph: say "for the
   box relaxation of `f`". List reformulations that use `x_i^2 = 1`
   (diagonal shift/QCR, RLT/McCormick linearization, SDP) as not covered;
   solvers may apply them by default.
8. **C8.** State that the tolerance hypothesis `eps' <= rho` excludes typical
   relative gap tolerances at large `N`: `1e-4 OPT ≈ 1e-4 beta N >> rho`. The
   proof tolerates `eps' <= 0.25 ak - Delta ≈ 1.4e-4 N` (`beta = 1`) and says
   nothing about larger relative gaps.
9. **C9.** State the finite-`N` content of Theorem 4.3 and the implicit
   constant `c'_1 ≈ 1.4e-4`:
   - the bound is vacuous below `N ≈ 1.7e7` (`beta = 1`, `rho = 4 log N` or
     71);
   - it exceeds `N^{10}` only from `N ≈ 2e8`;
   - for `rho = sqrt N` it is positive only from `N ≈ 1.5e10`.

   The practical evidence for large trees is Section 7, not Theorem 4.3.
10. **C10.** The parenthetical "(where the ML point is found in polynomial time
    by Papailiopoulos' algorithm)" applies to `beta = 1` (and `c >= 2`). For
    `beta > 1` cite Hu–Lu above `4 log N/(2beta-1)`, and say that the gap
    between the ML and box-decoder thresholds is not covered. Add Chvátal
    1980 to Section 8.
11. Minor. Theorem 5.1(b) should give a value or estimate for `rho_1`.
    Section 8's JO relation paragraph should add that Theorem 4.3 applies to
    sphere decoders themselves via the weaker-relaxation remark.

## 9. Not checked

- Conjecture 4.5 (lower half) and the adaptive-rule claims beyond what the
  class number gives.
- The full SDP section (Theorem 6.2 was read only as context).
- Theorem 1.3, Corollary 1.6 and Section 3, except where Section 4 uses the
  Theorem 1.3 law. These are used as inputs to Theorem 4.1, and I checked
  Lemma 0.2 fully.
- Hu–Lu's theorem (used as input for the remark on best-bound search without
  an incumbent).
- Jaldén–Ottersten's paper itself. The form `2^{N/(4rho+2)} - 1` is taken from
  Papailiopoulos' restatement, which I read.
- Whether data-dependent sphere-decoder orderings change the `beta = 1` order.
- Whether `chi(G^seg)` stays bounded above `8 log N`.
- The exact large-deviation constant of the midpoint-clique upper bound. I
  gave only the first-order argument.
- The literature beyond the fetched items. Items marked "memory" should be
  verified before they are cited.

## 10. Checks run (targeted, local; at most 6 processes)

All from `reviews/mimo-hard/` with `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`
(4 threads for `barycenter_mc.py`):

- `python3 constants.py > constants.log`: constants, range, finite-`N` onset,
  exponent ratio, the top-`K` versus max loss (S1), and the midpoint-clique
  first moment.
- `python3 barycenter_mc.py > barycenter_mc.log`: 20 real instances, 1,232
  families; events, deterministic inequality, overlap threshold.
- `python3 tiny_kappa.py N seeds rhos betas` for `N = 5` (β = 1, 2), `N = 6`
  (β = 1 and β = 2 separately), and `N = 8` (`rho = 2, 8, 32`, 5 seeds), all
  with `rho = 1..64` where listed. Then `python3 summarize_tiny.py > summarize_tiny.log`.
  590 instances; exact `kappa`, pairwise bounds, and variable-branching and
  static certificates. The min-norm-point oracle was validated against SLSQP
  on 300 random sets (max relative difference `1.1e-15`; ad hoc test, not
  saved).
- `python3 sd_vs_box.py > sd_vs_box.log`: typical-count exponents and exact
  Fincke–Pohst counts.
- `python3 predictor_check.py > predictor_check.log`: node-level predictor
  error and predictions for the capped `N = 256` runs. It imports the note's
  `core.py` and `predict_trees.py` read-only.
- `python3 rho1_estimate.py > rho1_estimate.log`: rough `rho_1` of
  Theorem 5.1(b).
- Papailiopoulos' PDF was fetched and converted with `pdftotext`: Section 1,
  Theorem 2.1, Remark A.2.

These are my own targeted checks. They are not CI results, and no CI was run
or inspected.
