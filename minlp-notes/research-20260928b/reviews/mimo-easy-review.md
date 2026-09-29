# Review of the easy side of `bb-complexity/binary-least-squares/certification-thresholds.md`

Scope: results (1), (2), (3) and (5) of the note's Summary, that is,
Sections 0 (as used), 1, 2.1–2.2, 3 and 6, and the parts of Sections 7–9 that
report on them. Result (4) (Sections 2.3, 4, 5, the hard side) is reviewed
separately. Reviewer: independent; I did not write the note or its code.
Date: 2026-09-29. My scripts and raw outputs are in
[`mimo-easy/`](mimo-easy/). They were written from scratch. They use only
NumPy, SciPy (`nnls`, `lsq_linear`/BVLS, `eigh`) and CVXPY/Clarabel, not the
author's `core.py`. I did not edit the note and did not commit. I ran only
the targeted checks listed in Section 8, with at most 6 processes. I ran no
project-wide checks and did not inspect CI.

## Verdict

I found no counterexample to any theorem in scope, and every proof I checked
is correct. The simulations agree with every exact law and bound. The main
problems are attribution and novelty, not mathematics:

- The "exact law for Gaussian cones" (Theorem 1.3) is known in substance.
  The expected conic intrinsic volumes of a cone spanned by `n <= d`
  Gaussian vectors are `C(n,k) 2^{-n}`. This follows from Hug–Schneider 2016
  as quoted in formula (3.5) of Godland–Kabluchko–Thäle 2022; for `n = d` it
  is their Lemma 5.1. Parts (b)
  and (c) are the master Steiner formula of McCoy–Tropp 2014, that is, the
  classical chi-bar-squared distribution. The note says it did not find the
  statement. It should cite these sources and present its proof as a
  self-contained derivation with a mild extension (R1).
- First-order ML achievability at `2 log N` (Theorem 2.2(a), `beta = 1`) is
  due to Hansen–Hassibi–Dimakis–Xu 2009 and Hassibi et al. 2014, as
  Papailiopoulos himself states. The note credits only Papailiopoulos (R2).
- Proposition 6.1 is the Jaldén–Martin–Ottersten (2003) tightness condition,
  with the same "iff" (R3).

One improvement is available at no extra cost. For `beta = 1`, failure of
C1 below `(1 - eps) N/4` follows from the same Hu–Lu input that
Corollary 1.6 already uses. One fixed single-wrong-fixing node is, in law, a
root problem at SNR `theta (N-1)/(1 + 4 theta)`. So the `beta = 1` C1
threshold is sharp at `N/4` under that input. Conjecture 3.3 is needed only
for the stronger statement that every such node fails (R4). The other
corrections are small (R5–R12).

| Claim | Verdict |
|---|---|
| Lemma 0.1, Lemma 0.2 | Correct (re-derived; the constants in Lemma 0.2 check out). |
| Prop. 1.1 (KKT; `P = 2^{-N}` exactly, every SNR, every `M >= 1`) | Correct. Confirmed numerically, including `M < N`: all 38 cells within 2 standard errors of `2^{-N}` (Section 8, check 2). |
| Thm 1.2 (both bounds; `rho > 3/4` for `beta = 1`) | Correct. The MGF step (`lambda = 2` is optimal) and the concavity step re-derived. No cell exceeds the bound beyond sampling error (check 2). |
| "Hu–Lu's `4 log N` concerns rounding, not exactness" | Correct. Checked in the source: their decoder is `sign(argmin_{[-1,1]^p} ||y - Ax||^2)`, and their threshold `(delta - 1/2)/(2 sigma^2 log p) -> alpha* > 1` converts to `rho > 4 log N/(2beta - 1)`. |
| Thm 1.3(a) uniform face law | Correct; proof checked; confirmed by simulation. True more generally (any column law invariant under single-column sign flips). Not new in substance (R1). |
| Thm 1.3(b),(c) Beta mixture, `chi^2_{Bin(n,1/2)}`, variance `5n/4` | Correct; confirmed by simulation. (b) needs rotation invariance: it fails for Laplace or correlated designs, while (a) survives. Known as chi-bar-squared / master Steiner formula (R1). |
| Cor. 1.4, Lemma 1.5, Cor. 1.6 | Correct. |
| Thm 1.7(a),(b) root gain `>= (beta/(1+2beta) - o(1)) N`, `= N/2 + O(sqrt(N log N))` | Correct. |
| Thm 1.7(c) | Correct, but it cites (a) outside (a)'s stated hypothesis when `beta > 8` (R6). |
| Lemma 2.1, Thm 2.2(a)–(c) | Correct. (a) is known for `beta = 1` (R2). The Summary overstates (b) as an equality (R8). |
| Thm 2.2(d) converse | Correct. The other direction comes from conditional independence of the `N` one-bit events given `w`, not from a first moment. |
| Thm 3.1(a) | Correct. The `2N+1` claim needs the incumbent/best-bound qualifier, which is stated here but dropped elsewhere (R5). |
| Thm 3.1(b) (`beta > 1`, sharp) | Correct. |
| Thm 3.1(c) (`beta >= 1`, `theta <= (1-eps)/(8beta)`) | Correct; one union-bound constant is off (R7, harmless). |
| Conjecture 3.3 | Plausible; my numerics agree. Its consequence for the C1 threshold follows from Hu–Lu (R4). |
| Prop. 6.1 (iff, dual certificate) | Correct, including uniqueness under strict PSD. Known (R3). |
| Thm 6.2 | Correct (loose constant, as the note says). |
| SDP numerics (thresholds; `rho* ~ N^3` for `beta = 1`) | Reproduced with an exact closed-form threshold. The note's per-coordinate heuristic does not explain the exponent 3; a bottom-eigenvector bound does. At `N <= 3200` the data cannot separate `N^3` from `N^2 polylog N` (R9). |

## 1. Result (1): the root relaxation

**Proposition 1.1.** `f` is convex, and the box is a product of intervals.
So `x*` is optimal iff `x*_i d_i f(x*) <= 0` for every `i`, with
`d_i f(x*) = -2 a_i'w`, that is, iff `zeta_i >= 0`. Given `w != 0`, the
`a_i'w` are independent centred Gaussians, so `P = 2^{-N}` exactly for every
`rho` and every `M >= 1`. The argument is complete. Numerically, the KKT
sign test and a BVLS solve agree in all but at most 3 of 20,000 trials per
cell, which I attribute to the solver tolerance. The claim that there is
"no margin to gain from the SNR" is right: `rho` scales all `zeta_i` by the
same factor.

**Theorem 1.2.** I re-derived each step:

- `v = x^S` is a box minimizer iff `v_i a_i'(y - Av) >= 0` for all `i`,
  where `y - Av = w + 2 B_S 1`.
- The `N - k` conditions off `S` have conditional probability exactly
  `2^{-(N-k)}` given `(w, B_S)`.
- The summed condition on `S` has the MGF
  `(1 + 4 lambda a^2 - lambda^2 a^2)^{-M/2}`, which is minimized at
  `lambda = 2`.
- Concavity gives `log(1 + 4 rho t) >= t log(1 + 4 rho)`.

"`R = OPT` iff the box minimizer is a vertex" uses uniqueness (`M >= N`),
as stated. Numerically, the frequency of `R = OPT` (with `OPT` by full
enumeration) agrees with the frequency of a vertex minimizer to within
0.0002 in every cell (solver tolerance). It
never exceeds the sum-form bound by more than 3 standard errors
(`root_checks_A.out`). The bound is vacuous (above 1) at `rho = 0.5`,
`beta = 1`, consistent with the stated condition `rho > 3/4`. At large
`rho` the bound tends to `2^{-N}`, the `k = 0` term. So at high SNR root
exactness is essentially the event "`x*` is the box minimizer".

**Hu–Lu.** I read the source (arXiv 2006.08416, Section I-B). Model
(A.1)–(A.5): `A_ij ~ N(0, 1/p)`, noise `N(0, sigma^2 I)`, `delta = n/p`
with `liminf delta > 1/2`, and `sigma^2 log^2 p` bounded below. Decoder:
`beta_hat = sign(x^*)` with `x^* = argmin_{[-1,1]^p} ||y - Ax||^2/2`.
Proposition 1: `P(N_e = 0) -> 1` if `alpha* > 1` and `-> 0` if
`alpha* < 1`, where `alpha_p = (delta_p - 1/2)/(2 sigma_p^2 log p)`. With
`sigma^2 = 1/rho` and `delta = beta`, this is `rho > 4 log N/(2beta - 1)`.
The note's conversion and its reading (rounding, not exactness) are correct.
Papailiopoulos (arXiv 2609.19405, p. 3–4) describes it the same way.

**Theorem 1.3 (uniform face law).** The proof is correct.

- The KKT characterization of `Pi_K(v) in relint F_S` by (i) and (ii) is
  right.
- (ii) has conditional probability `2^{-(n-|S|)}` given `G_S`.
- The `2^{|S|}` sign-flipped cones tile `L_S`, so (i) has probability
  `2^{-|S|}`.
- For (b) and (c), the event `{face = S}` depends only on the directions of
  `P_{L_S} xi` and `P_{L_S}^perp xi`. Their norms are therefore
  conditionally independent `chi^2_s` and `chi^2_{M-s}`.
- The variance `n + n/4 = 5n/4` is right.

A shorter proof shows exactly what (a) needs. For fixed linearly
independent `g_j` and generic `v`, each face `S` is the projection face of
exactly one of the `2^n` cones `cone{eps_j g_j}`:

- (i) fixes `eps` on `S`;
- (ii) fixes `eps` off `S`.

Hence `sum_eps 1{face(cone{eps_j g_j}) = S} = 1` deterministically. So (a)
holds whenever the joint law of the columns is invariant under flipping any
single column's sign (plus general position). This does not require
independence, identical laws, Gaussianity or rotation invariance. Part (b)
does need rotation invariance.

Simulation (`face_law.out`; 64,000 NNLS projections per case, fixed `v`):

- **Gaussian columns** with `(n, M)` in `{(3,3), (3,5), (4,4), (4,9), (5,6),
  (6,12)}`. Chi-square test of uniformity over the `2^n` faces:
  `p = 0.27`–`0.96`. Mean and variance of `|S|` equal `n/2` and `n/4` to
  within 0.01. KS tests of `Beta(s/2, (M-s)/2)` given `|S| = s`:
  `p >= 0.06` in all 23 cells.
- **Sign-symmetric but not rotation-invariant designs** (iid Laplace
  entries; `N(0, Sigma)` columns with a fixed non-identity `Sigma`). The face
  law holds (`p = 0.16`–`0.99`). The Beta law fails (KS `p <= 4e-6`), as
  predicted.
- **Dependent columns with independent random signs.** The face law holds
  (`p = 0.34`, `0.95`).
- **Negative controls.** Mean-shifted columns, and `n > M`: uniformity is
  rejected (`p = 0`), and `|S|` is not `Bin(n, 1/2)`.
- **Part (c)** at `n = 50`–`200`, `M = n, 2n`: mean `||Pi_K v||^2/n` is
  0.499–0.504, variance/`n` is 1.22–1.33 (law 1.25), and KS against the
  chi-bar-squared mixture gives `p = 0.11`–`0.64`.

**Corollary 1.4, Lemma 1.5, Corollary 1.6, Theorem 1.7.**

- 1.4(a)–(d): correct. The scaling `u°(rho) = u°(1)/sqrt(rho)` holds
  because `w` does not scale with `rho`.
- Lemma 1.5: correct. The only inequality is the nonnegativity of the terms
  `k != j`, which holds by restricted KKT and `u° >= 0`.
- Corollary 1.6: correct. The arithmetic gives `u°_j <=
  2 sqrt(6 beta log N/rho)(1 + o(1))/(sqrt(beta) - 1)^2`.
- Theorem 1.7(a): the witness algebra (1.1) is right.
  `F(tau* s) = W X/(Q^2 + X)` and `X ~ Q chi^2_{M-1}` given `s`. Feasibility
  needs `rho >= 2 beta log N (1+o(1))/(1+2beta)^2`, which `rho >= (log N)/4`
  implies.
- Theorem 1.7(c): see R6.

Numerically (`root_checks_B.out`; 300 instances at `N = 100` and 100 at
`N = 400`, `beta = 1, 2`; box solved in `x`-coordinates by BVLS):

- `G <= G_inf` in all 3200 instance/SNR pairs (800 instances, 4 SNRs).
- `G = G_inf` in every instance at `rho = 2 log N/beta`, `4 log N` and
  `N/4`. At `rho = (log N)/4` this holds in 0.0–0.3% of instances
  (`beta = 1`) and 59–63% (`beta = 2`).
- Mean `G_inf/N` is 0.498–0.509. Variance/`N` is 1.14–1.39, against 1.25;
  with 100–300 samples the relative error of a variance estimate is 8–14%.
- The active-set variance/`N` is 0.21–0.25.
- The witness gives mean `G_wit/N` of 0.331–0.338 (`beta = 1`, law `1/3`)
  and 0.399–0.405 (`beta = 2`, law `0.4`). `G >= G_wit` always.
- At `rho = (log N)/4` and `beta = 1` the unclipped witness step is
  infeasible in 7–8% of instances. The finite-`N` margin is thin
  (`tau* max_j s_j ~ 1.9` against 2). This does not affect the asymptotic
  statement.

## 2. Result (2): condition C1

**Theorem 3.1(a).** Correct. Dropping the upper bounds gives
`r_i >= ||v_i||^2 (1 - Y_i)`. Theorem 1.3 applies with `n = N - 1` because
`v_i = w + 2 b_i` is independent of `B_{-i}`. Lemma 0.2 with
`t = sqrt(128 log N/M)` gives failure probability `6 N^{-2}` per node, and
the arithmetic `r_i - W >= (N/2)(theta/theta_c - 1) - o(N)` is right.
Uniqueness of `x*` follows because every other vertex lies in some
single-wrong-fixing node.

**Theorem 3.1(b) (`beta > 1`).** Correct. `r~_{ij}` depends on `w`, `b_i`
and the columns other than `i` and `j`, so it is independent of `b_j`. With
`sigma_min(B_{-i}) >= sigma_min(B)`, Lemma 1.5 gives
`u°_j = O(sqrt(log N/(theta N))) -> 0` uniformly. The node problems are
therefore box-inactive, and the lower tail of Lemma 0.2 finishes the proof.
So for `beta > 1` the C1 threshold `rho = N/(4(2beta - 1))` is proved sharp.

**Theorem 3.1(c).** Correct, apart from R7.
`r_i <= ||v_i||^2 (2beta/(1+2beta))(1 + o(1))` is below `W - cN` iff
`8 beta theta < 1`.

**The `2N+1` tree bound.** It is correct as stated in Theorem 3.1(a):
"incumbent `OPT` available, or best-bound search". Without that qualifier
it is false in general. Depth-first search that dives into an off-path
child has nothing to prune against. See R5.

**`beta = 1`: the sharp threshold follows from Hu–Lu (R4).** C1 fails as
soon as one single-wrong-fixing node has bound `< OPT`. So Theorem 3.1(b)'s
"every node" form is more than the threshold needs. Fix a node `i`. Then
`v_i = w + 2 b_i ~ N(0, (1 + 4 theta) I_M)` exactly, and it is independent
of `B_{-i} = sqrt(theta) H_{-i}`. Dividing by `c = sqrt(1 + 4 theta)` shows
two things:

- `r_i = c^2 R'`, where `R'` is the root value of an instance with
  `N' = N - 1` unknowns, `M` observations, unit noise and SNR
  `rho' = theta (N-1)/(1 + 4 theta)`.
- The minimizers coincide.

Apply Hu–Lu to that instance at `rho_0 = (1 + eps) 4 log N'/(2beta' - 1)`,
with `beta' = M/(N-1)`. The conditions hold: `delta -> beta >= 1 > 1/2`,
and `sigma^2 = 1/rho_0` has `sigma^2 log^2 N -> inf`. Corollary 1.4(d) then
gives `rho'_box < rho_0/4 = O(log N)` w.h.p. Since `rho' = Theta(N)`, node
`i` is box-inactive w.h.p. and `r_i = ||v_i||^2 (1 - Y_i)`. The last display
of the proof of Theorem 3.1(b) then applies verbatim to this one node:
`r_i - W <= (N/2)(theta/theta_c - 1) + o(N)`. Hence for `beta = 1` and
`theta <= (1 - eps)/4`, C1 fails w.h.p. with `OPT = W`. This is exactly the
standard of Corollary 1.6, which also takes Hu–Lu as input.

The "every node" version still needs a union bound, that is,
`P(node i box-active) = o(1/N)`. Hu–Lu's rate (`polylog/p^{1/5}`) does not
give this. So Conjecture 3.3 remains open as stated, but only the
"every node" form and Conjecture 4.5 depend on it. The same reduction
turns Conjecture 3.3 into a tail bound for one pure-noise NNLS problem.
With `U` the largest NNLS coefficient of `xi ~ N(0, I_N)` on
`H'/sqrt(N)` (`H'` Gaussian, `N x (N-1)`), node `i` is box-inactive iff
`U <= 2 sqrt(theta N/(1 + 4theta))` up to a factor `1 + O(N^{-1/2})`. At
`theta = 1/4` the bound is `U <= sqrt(N/2)`. Conjecture 3.3 then amounts to
`P(U > c sqrt(N)) = o(1/N)` for every fixed `c > 0`. Tail data:
in `nnls_tail.out`, the median of `U` is 3.5, 3.9, 4.1, 4.5
and 4.8 at `N = 100, 200, 400, 800, 1600`, roughly `sqrt(log N)` growth.
The largest of 2000, 1000, 400, 100 and 30 samples gives
`max U/sqrt(N) = 0.79, 0.53, 0.30, 0.20, 0.16`, against the `theta = 1/4`
threshold 0.707. One sample in 2000 exceeds it at `N = 100`, and none does
from `N = 200` on. The tail looks light, which supports Conjecture 3.3.

**Numerics.** I solved all `N` single-fixing nodes of 184 instances (NNLS,
with BVLS if needed; `c1_checks.out`, aggregate in `c1_aggregate.out`):

- **Design.** `beta` in `{1, 1.5, 2, 3}` at `N = 200` and `400` (4 seeds
  each), and `beta` in `{1, 2}` at `N = 800` (2 seeds). `theta/theta_c` in
  `{0.8, 1, 1.2, 1.5, 2}`, plus 0.5 for `beta = 1`.
- **Box inactivity.** Every node problem in every instance was
  box-inactive. This includes all `beta = 1` instances, with `theta` from
  1/8 to 1/2. The largest NNLS coefficient over all nodes decreases with
  `N`: 1.62, 1.12, 0.78 at `N = 200, 400, 800` for `beta = 1`, and 1.09,
  0.83, 0.58 for `beta = 2`.
- **A fixed node follows the first-order law.** The mean of `(r_0 - W)/N`
  over all instances is −0.241, −0.089, −0.008, +0.127, +0.242 and +0.519
  at `theta/theta_c = 0.5, 0.8, 1, 1.2, 1.5, 2`. The law
  `(theta/theta_c - 1)/2` gives −0.25, −0.1, 0, +0.1, +0.25 and +0.5. This
  is the finite-`N` picture behind R4.
- **The minimum over nodes is lower**, by the `sqrt(log N)` terms. C1 held
  in 0 of 76 instances with `theta <= theta_c`, 1 of 36 at
  `1.2 theta_c`, 12 of 36 at `1.5 theta_c` and 32 of 36 at `2 theta_c`.
  This matches the note's Table 7.2: at practical `N` the transition sits
  at 1.5–2 times `theta_c`.
- **Node values.** Per instance, the mean of `r_i/||v_i||^2` lies within
  [−0.12, +0.07] of `1 - (N-1)/(2M)`. Cell means lie within 0.03.

## 3. Result (3): the ML threshold

**Lemma 2.1.** Correct. `lambda = 1/4` is optimal. A Monte Carlo check of
four cases stays below the bound (`ml_checks.out`).

**Theorem 2.2(a) (first moment).** Correct. I checked the following:

- the small-`k` bound
  `C(N,k)(1 + x_k)^{-M/2} <= (N e^{-(beta rho/2)(1 - x0/2)})^k/k!`;
- the inequality `(1 + eps/2)(1 - eps/8) >= 1 + eps/4` for `eps <= 2`;
- the large-`k` split at `t1`, which needs `rho -> inf`. This holds because
  `beta` is fixed.

Evaluated exactly, the sum `Sigma` in (2.1) decays slowly. At
`rho beta = 2.2 log N` it is 0.73, 0.37 and 0.22 at `N = 10^3, 10^5, 10^7`.
The `k = 1` term `~ N^{1 - c/2}` dominates. So the theorem is asymptotic in
the usual sense.

**Theorem 2.2(b),(c).** Correct. For (c): `log(1+x) >= (log 8/7) x` on
`[0,7]`, the binomial theorem bounds the small part, and
`1 - (1/2) log 8 < -0.039` bounds the large part. Only an upper bound on
`W - OPT` is proved. The Summary's "`W - OPT = N^{1 - c/2 + o(1)}`"
overstates this (R8).

**Both directions.** A first-moment bound alone gives only (a). The other
direction, (d), comes from exact conditional independence. Given `w`, the
pairs `(zeta_i, ||b_i||^2)` are independent across `i` (Lemma 0.1), so
`P(no improving one-bit flip | w) = (1 - p(w))^N <= exp(-N p(w))`. A Gaussian
tail estimate then gives `N p -> inf` for `rho beta <= (2 - eps) log N`. The
proof is correct. The hypothesis `rho beta -> inf` is unnecessary: for
bounded `rho beta`, `p` is a positive constant. Together, (a) and (d) make
`rho beta = 2 log N` the sharp first-order ML threshold for every fixed
`beta >= 1`.

Computed exactly (`ml_checks.out`), the converse also converges very
slowly. At `rho beta = 1.8 log N`, `P(no improving flip)` is still 0.79,
0.74 and 0.65 at `N = 10^4, 10^6, 10^8`. This matches Papailiopoulos'
`- log log N` correction: `rho = 2 log N - log log N` is `1.72`–`1.84`
times `log N` for `N = 10^3`–`10^8`.

**Comparison with Papailiopoulos (arXiv 2609.19405; PDF read, Section 1,
Theorem 2.1, Appendix A).** The model and normalization are identical
(`beta = 1`). The note's summary of his results is accurate:

- Theorem 2.1(a): polynomial time at `rho >= 2 log N`, uniformly over `x*`.
- Theorem 2.1(b): ML fails for `rho <= 2 log N - log log N - s_N`.
- Remark A.2: ML succeeds by MAP optimality.

His Appendix A states that "first-order ML achievability was already
identified in Hansen et al. [2009] and stated with a diverging additive
slack in Hassibi et al. [2014, Lemma IV.2]" (`rho > 2 log N + f(N)`,
`f -> inf`). The note omits both references (R2). What the note adds is the
general-`beta` statement, the value bounds (b)–(c), and a short converse for
general `beta`. His converse is sharper (the `log log N` term, uniform in
`rho`) and correspondingly longer. The note's relation paragraph (search in
polynomial time versus superpolynomial certification) is fair. Its
superpolynomial half rests on Theorem 4.3, which is reviewed separately.

## 4. Result (5): the SDP relaxation

**Proposition 6.1.** Correct. Both the primal (`X = I`) and the dual are
strictly feasible, so strong duality holds and both optima are attained.
Complementary slackness with `xt` (all entries nonzero) forces
`lambda_i = -zeta_i` and `lambda_{N+1} = y'w`. I re-derived the identity
`(v,t)'(Q - Diag lambda)(v,t) = ||A d||^2 + sum_i zeta_i d_i^2` with
`d = v - t x*`; the `t^2` coefficients agree because
`y'y - y'w = ||Ax*||^2 + w'Ax*`.

The "iff" is right in the sense stated: "`xt xt'` is SDP-optimal". It is
not the same as "the SDP value equals `OPT`". When `x*` is not the ML point
the SDP could be tight at another vertex. The note uses it correctly.

Uniqueness also holds. If `A'A + Diag(zeta)` is positive definite, then
`Q - Diag(lambda)` has kernel `span(xt)`. Every optimal `X` has range in
that kernel, so `X = xt xt'`, and the ML point is unique. The diagonal of
the condition is the one-bit condition, as the note says.

I checked the "iff" against actual SDP solves (`sdp_checks_a.out`,
Clarabel, `N = 10`, 16 instances, `beta = 1, 2`). At `rho = 2 rho*` the SDP
value equals `f(x*)` to `1.2e-7` relative and `X` has rank one
(second eigenvalue below `1e-9` of the first). At
`rho = 0.5 rho*` the value is strictly below `f(x*)`, by `1.6e-3` to
`8e-2` relative. There were 0 mismatches. Five square instances with
`rho* > 10^4` were skipped: at that scale Clarabel returned values above
`f(x*)`, which is impossible (`sdp_checks_a_first_attempt.out`).

**Theorem 6.2.** Correct. `lambda_min(A'A) >= rho (sqrt beta - 1 - o(1))^2`
and `max_i(-zeta_i) <= sqrt(2 rho beta log N)(1 + o(1))` give the stated
constant. As the note says, the constant is far from sharp.

**Exact per-instance threshold.**
`A'A + Diag(zeta) = sqrt(rho)(sqrt(rho) K + D)` with `K = H'H/N` and
`D = Diag(x* o H'w)/sqrt(N)`. So the SDP is exact at `x*` iff
`rho >= rho* = (lambda_max(-D; K))_+^2`, a generalized eigenvalue. No
bisection is needed, and the note's bisection is consistent with this
monotone structure. Results (`sdp_checks_b.out`): 

- **Coverage.** 40, 40 and 10 instances at `N = 100, 400, 1600` for each
  `beta`, plus `beta = 1` at `N = 200, 800, 3200`. In every instance a
  direct `lambda_min` evaluation at `0.999 rho*` and `1.001 rho*` agrees
  with the closed form.
- **Tall systems.** The median `c* = rho*/log N` at `N = 100, 400, 1600`
  is 17.6, 17.1, 16.8 (`beta = 1.5`); 4.63, 4.68, 4.01 (`beta = 2`); 1.33,
  1.32, 1.38 (`beta = 3`); and 0.70, 0.72, 0.86 (`beta = 4`). This
  reproduces Table 7.5a with independent seeds. The author has 20.3, 17.8,
  17.3; 4.62, 4.42, 4.38; 1.42, 1.33, 1.38; and 0.71, 0.74, 0.70. The
  proved constant `2beta/(sqrt(beta) - 1)^4` is 10–70 times too large, as
  the note says.
- **Coordinate heuristic.** Evaluated per instance,
  `rho_coord = (max_i -D_ii (K^{-1})_ii)^2` is within a median factor
  1.1–2.1 of `rho*` for `beta > 1`, and the ratio falls towards 1 as `beta`
  and `N` grow.
- **Square systems.** The median `log(rho*)/log N` is 2.80, 3.37, 2.84,
  2.84, 2.96 and 2.69 at `N = 100, 200, 400, 800, 1600, 3200` (40, 40, 40,
  20, 10 and 5 instances). The note reports 2.75–3.11. The median
  `log(rho*/N^3)` shows no trend with `N` (−0.9, +2.0, −1.0, −1.1, −0.3,
  −2.5). The upper tail is extremely heavy: one `N = 3200` instance has
  `rho* = 9e19 log N`. The one-bit threshold medians (1.4–1.7 `log N` for
  `beta = 1`) also match the note.

## 5. Novelty and literature

- **Proposition 1.1 and Theorem 1.2.** Both are elementary. I know no
  source for the exact `2^{-N}` law or the vertex bound. The qualitative
  fact that the box solution has a constant fraction of interior
  coordinates at fixed SNR is implicit in the CGMT analyses
  (Thrampoulidis–Abbasi–Xu–Hassibi 2016; Thrampoulidis–Xu–Hassibi 2018).
- **Theorem 1.3.** Known in substance.
  - Godland–Kabluchko–Thäle (Discrete Analysis 2022:5, arXiv 2012.06189)
    define the Donoho–Tanner cone `D_{n,d}` as the positive hull of `n`
    iid Gaussian vectors in `R^d`. Their Lemma 5.1 gives
    `E v_k(D_{n,d}) = C(n,k) 2^{-n}` for `k <= d - 1` when `d <= n`. At
    `n = d` (the square root problem) this is the full law, since
    `E v_n = 2^{-n}`.
  - For `n < d`, the same values follow from the Cover–Efron formula they
    quote as (3.5), `E v_k(C_{n,d}) = C(n,k)/C(n,d)`, from Hug–Schneider
    (DCG 2016, Cor. 4.2–4.3). When `n <= d`, `C(n,d) = 2^n` and the
    Cover–Efron cone is the Gaussian positive hull. I did not verify that
    Hug–Schneider state this range explicitly; the sign-flip argument above
    proves it in two lines.
  - Part (a) follows from these values by exchangeability and rotation
    invariance. Parts (b)–(c) are the master Steiner formula of McCoy–Tropp
    (DCG 2014). Given the face dimension, `||Pi_C g||^2` and
    `||Pi_{C°} g||^2` are independent `chi^2_k` and `chi^2_{d-k}`. This is
    the chi-bar-squared law of order-restricted inference (Kudô 1963;
    Shapiro 1985).
  - The `Bin(n, 1/2)` support law for pure-noise NNLS is therefore a
    corollary of known results.
  - What the note adds is the fixed-`v`, per-face form (immediate from the
    above by exchangeability and rotation invariance) and a direct proof.
    This review adds that (a) holds for sign-symmetric designs. The note
    should not say it did not find the statement (R1).
- **Theorem 2.2.** Part (a) is known for `beta = 1` (Hansen et al. 2009;
  Hassibi et al. 2014, Lemma IV.2, per Papailiopoulos). The general-`beta`
  version and the converse (d) are routine. I did not check whether
  Hassibi et al. treat `M > N`.
- **C1 thresholds (Theorem 3.1).** I know no prior node-level analysis of
  box-relaxation branch-and-bound for this model. The mechanism is novel in
  presentation: Theorem 1.3 applied at a node whose residual `v_i` is
  independent of the free columns. It is the natural consequence of
  known conic geometry.
- **Proposition 6.1.** This is the Jaldén–Martin–Ottersten (ICASSP 2003)
  condition, also in Jaldén's thesis. Jiang–Liu–Bao–Jiang (arXiv
  2102.04586, eq. (2.4)) cite it as "(2.3) is tight if and only if
  `H'H + Diag(x*)^{-1} Diag(H'v) ⪰ 0`", which is exactly Proposition 6.1.
  The note calls it "the standard dual certificate" but cites Jaldén et al.
  only "from memory" for "optimality conditions" (R3).
- **Theorem 6.2.** Its sufficient condition,
  `lambda_min(A'A) > max_i(-zeta_i)`, is implied by the
  `lambda_min(H'H) > ||H'v||_inf` form. That form is the `M = 2` instance of
  the Lu–Liu–Zhang–Zhang condition (1.4),
  `lambda_min(H^dagger H) sin(pi/M) > ||H^dagger v||_inf`, which is stated
  for their enhanced SDRs and `M`-PSK. Per Jiang et al., Lu et al.'s
  Theorem 4.5 shows tightness probability tending to one for small noise
  and `m` large relative to `n`. I did not read Lu et al.'s Theorem 4.5, so
  I cannot say whether it contains the `Theta(log N)` statement for fixed
  `beta > 1`. The `N^3` law for square systems appears to be new (numerical
  only). It is consistent with Papailiopoulos' remark (p. 3–4) that no SDP
  result gives exact block recovery at logarithmic SNR in the square model.
- **Other SDP work** (Kisialiou–Luo SIOPT 2010; So 2010). These give
  constant-factor approximation of the ML objective in probability (from
  the SIOPT abstract via Crossref; So not re-read). They do not bear on
  exactness at `x*`.
- **Sphere decoding.** Jaldén–Ottersten's bound, as restated by
  Papailiopoulos (p. 2), is `C(N) >= 2^{N/(4rho+2)} - 1`, matching the note.
  It bears on result (4), not on the results reviewed here.

## 6. Required corrections

- **R1 (Theorem 1.3, Summary (1), Sections 1.2 and 8).** Cite
  Hug–Schneider 2016 and Godland–Kabluchko–Thäle 2022 for
  `E v_k = C(n,k) 2^{-n}`, and McCoy–Tropp 2014 or the chi-bar-squared
  literature for (b)–(c). Replace "we did not find the uniform face law
  stated" and "We did not find this statement" accordingly. Optionally
  state (a) for column laws invariant under single-column sign flips.
- **R2 (Theorem 2.2(a), Summary table row 1, Section 8).** Credit
  first-order ML achievability for `beta = 1` to Hansen et al. 2009 and
  Hassibi et al. 2014 (Lemma IV.2), as Papailiopoulos does.
- **R3 (Proposition 6.1, Section 8).** Attribute the iff condition to
  Jaldén–Martin–Ottersten 2003 / Jaldén's thesis (cited as such in Jiang et
  al. 2021, eq. (2.4)). Mention that Theorem 6.2's sufficient condition is
  the BPSK case of Lu et al.'s condition (1.4).
- **R4 (Theorem 3.1, Conjecture 3.3, Summary table row "C1", Summary (2),
  Section 9 item 1).** Add the `beta = 1` failure below `(1 - eps) N/4`,
  conditional on Hu–Lu, via the single-node reduction in Section 2 above.
  Restrict Conjecture 3.3 to the "every node" statement and to
  Conjecture 4.5.
- **R5 (`2N+1` qualifier).** The qualifier "incumbent `OPT` available when
  off-path nodes are examined, or strict C1 with best-bound search" is
  dropped in Summary table row 5 (line 25), Summary (2) (line 49),
  Corollary 3.2 (line 713) and Corollary 4.4 (line 958).
- **R6 (Theorem 1.7(c)).** For `beta > 8`, `rho beta >= (2 + eps) log N`
  does not imply `rho >= (log N)/4`. Either state (a) under its actual
  feasibility condition, `rho >= (1 + eps) 2 beta log N/(1 + 2beta)^2`
  (which `rho beta >= 2 log N` implies), or restrict (c).
- **R7 (proof of Theorem 3.1(c)).** `max_{i,j} s^{(i)}_j <= sqrt(4 log N)`
  over `N(N-1)` pairs has failure probability up to about 1 under (T1). Use
  `sqrt(6 log N)`. Nothing else changes.
- **R8 (Summary (3); Section 2.2 prose after the proof).** "`W - OPT =
  N^{1 - c/2 + o(1)}`" should read "at most `N^{1 - c/2 + o(1)}`". A
  matching lower bound is plausible (about `N^{1-c/2}` nearly
  non-interacting improving one-bit flips) but not proved.
- **R9 (Section 6, "Square systems").** The coordinate (rank-one)
  heuristic predicts `rho >~ N^2` for a typical coordinate. The exponent 3
  comes from the bottom eigenvector `v` of `A'A` instead.
  `lambda_min(A'A) = (rho/N) s_min(H)^2 ~ rho/N^2`, and
  `v' Diag(zeta) v = sqrt(rho/N) sum_i v_i^2 x*_i h_i'w` has size about
  `sqrt(rho/N)`, because `sum_i v_i^4 ~ 3/N` for a delocalized `v`. When
  this is negative, the Rayleigh quotient at `v` gives `rho* >~ N^3`, with a
  heavy upper tail inherited from `s_min(H)^{-4}`.
  - The mechanism is visible in the data. In `sdp_square_inspect.out` the
    top eigenvector of the pencil puts 67–99% of its `K`-energy on the
    bottom five eigenvectors of `K`.
  - In `sdp_checks_b.out`, the Rayleigh lower bound
    `s* >= -v_k'D v_k/lambda_k` over the bottom five modes recovers a
    median of 17–73% of `rho*`. The bottom mode alone has the unfavourable
    sign in 35–70% of instances. Heuristically, `rho* >= c N^3` as soon as
    one of the bottom `k` modes has `v_k'Dv_k < 0`, which happens with
    probability about `1 - 2^{-k}`.
  - The data alone cannot separate `N^3` from `N^2 polylog(N)`. Evaluated
    per instance, the coordinate heuristic is also within a median factor
    0.5–2.9 of `rho*`, because `log^4 N ≈ N` for `N <= 3200`.
  - The phrase "and more for the worst one" is not right either. The
    `(K^{-1})_ii` share the common factor `1/lambda_min(K)`, so the worst
    coordinate adds only logarithmic factors.

  Suggested text: explain `N^3` by the bottom-eigenvector bound, and say
  that the exponent is not determined numerically at these sizes.
- **R10 (Section 6 "What this means", Summary (5)).** At `rho = Theta(log
  N)` the separation is 1 node against `exp(Theta(N log log N/log N))`
  leaves: superpolynomial, not "exponential". It also depends on
  Theorem 4.3, which is reviewed separately.
- **R11 (Section 6 heuristic).** "near the rank-one heuristic" is loose for
  `beta = 1.5`: the note's medians are 17–20 and mine 16.8–17.6, against 12.
  For `beta >= 2` the heuristic is within about 25% (4.0–4.7 against 4;
  1.32–1.38 against 1.5; 0.70–0.86 against 0.89).
- **R12 (Table 7.5b and Sections 6 and 9, "14–37%").** The median relative
  SDP root gaps depend on the seeds. With independent seeds
  (`sdp_checks_c.out`, `OPT` by full enumeration, 6 seeds per cell) I get
  0.17–0.23 at `N = 16` and 0.36–0.44 at `N = 20`. Box gaps are 0.36–0.52
  and 0.61–0.65. Describe the range as indicative. The qualitative claims
  hold: the SDP is never exact at `x*`, and its gap is 0.4–0.7 times the
  box gap.

## 7. Minor remarks (no change required)

- Theorem 2.2(d): the hypothesis `rho beta -> inf` can be dropped.
- Section 3, "Finite-`N` behaviour": the second-order prediction keeps the term
  `-4 sqrt(2 rho beta log N)` from `min_i zeta_i`. It ignores the
  node-to-node fluctuation of `||v_i||^2 Y_i`, which is also of order
  `sqrt(N)` per node. The reason is that `b_i` is independent of the free
  columns, and `||2 b_i||^2 ≈ 4 theta beta N` is comparable to `W`. So its
  minimum over nodes contributes another `sqrt(N log N)`-order term. In my
  data (`c1_aggregate.out`) the prediction is unbiased on average for
  `beta = 1.5`, `2` and `3` (mean error −0.002, −0.001, +0.035 in units of
  `N`), with single-instance errors up to 0.25. For `beta = 1` it is
  optimistic by 0.07 on average and by up to 0.47 in one instance. "These
  match the observed transitions" is fair for `beta >= 1.5` and slightly
  optimistic for `beta = 1`.
- Lemma 0.2 is stated for `t in [0,1]`. The union-bound choices in
  Theorems 3.1 and 4.1 keep `t -> 0`, so this is fine.

## 8. Checks run (targeted; all in `mimo-easy/`, `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`)

1. `python3 face_law.py > face_law.out`: Theorem 1.3(a)–(c), the
   generalization and the negative controls (Section 1).
2. `python3 root_checks.py A > root_checks_A.out`: Proposition 1.1 and
   Theorem 1.2 at `N = 2..8`, `M in {N/2, N, 2N}`, `rho in {0.5, 1, 4, 16}`,
   20,000 trials per cell. `OPT` by enumeration; box by BVLS in
   `x`-coordinates.
3. `python3 root_checks.py B > root_checks_B.out`: Corollary 1.4 and
   Theorem 1.7 (Section 1).
4. `python3 c1_checks.py main > c1_checks.out` (raw `c1_checks.jsonl`) and
   `python3 c1_checks.py tail > nnls_tail.out`: Theorem 3.1 and
   Conjecture 3.3 (Section 2).
5. `python3 ml_checks.py > ml_checks.out`: Lemma 2.1, the first-moment sum
   and the one-bit converse law (Section 3).
6. `python3 sdp_checks.py a > sdp_checks_a.out`, `... b > sdp_checks_b.out`,
   `... c > sdp_checks_c.out`: Proposition 6.1 against SDP solves, exact
   thresholds, and square-system gaps (Section 4).
   `sdp_checks_a_first_attempt.out` is the output of the first version of
   part `a`, which lacked the `rho* <= 10^4` filter and shows the three
   solver failures.
7. `python3 c1_aggregate.py > c1_aggregate.out` and
   `python3 sdp_square_inspect.py > sdp_square_inspect.out`: aggregation of
   check 4 and the square-system diagnostics behind R9.

These are local targeted checks only. No project-wide verification was run,
and CI was not consulted.

## 9. Not checked

- Result (4): Sections 2.3, 4 and 5, and every statement that uses them
  (the separation in R10, Corollary 4.4 and Table 7.3).
- The author's Tables 7.3–7.4 and the predictors in Section 7.3b–c. I did
  not rerun the author's code; all my numbers come from independent code
  and seeds.
- Whether Hug–Schneider 2016 state the Cover–Efron formula for `n < d`.
- Whether Lu et al. 2019 (Theorem 4.5) or Kisialiou–Luo contain Theorem 6.2
  or an equivalent `Theta(log N)` statement for `beta > 1`.
- Whether Hassibi et al. 2014 cover `M > N`.
- Jaldén–Martin–Ottersten 2003, So 2010 and Hansen et al. 2009, which I did
  not read directly (attributions via Jiang et al. 2021, Papailiopoulos
  2026, and the Crossref abstract of Kisialiou–Luo).
- A rigorous proof of Conjecture 3.3's "every node" form. My reduction
  shows only what it amounts to.
