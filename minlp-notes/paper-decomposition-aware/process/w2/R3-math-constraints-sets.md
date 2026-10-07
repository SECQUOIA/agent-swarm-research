# R3: mathematical correctness of `constraints.tex`, `optsets.tex`, `appendix-proximal.tex`

Reviewer key: `R3-math-constraints-sets`. Sources were read at their state of
2026-10-03 01:07; PDF build of 01:19. Section 8 is `sec:constraints`,
Section 9 is `sec:optsets`, Appendix B is `app:proximal`.

## Verdict

No critical issue. I re-derived every proof in the three files. All main
theorems are correct:

- TU rounding, the rounding allowance, soundness, state counts, complexity;
- exact output, height and snapping recovery;
- the uniform-cell algorithm and the endpoint identity with its CSP corollary;
- the diagonal certificate, the proximal stage, the discovery theorem and
  `prop:sshard`.

There are three major problems:

1. **Proposition 9.1 (`prop:twocenters`).** Its quantitative consequences are
   false for the algorithm CT that it names. CT gives the coordinate `z`
   (with `L_z = 0`) the two-node grid `{0, M}`. The bag table therefore grows
   linearly in `M/sqrt(eps)`, not quadratically. The conclusion `2^{Omega(I)}`
   survives. "FG" is never defined.
2. **"Uniform meshes are forced."** The intro and Section 8 claim this. What is
   proved is narrower: misaligned grids (Proposition 8.20) and one common
   graded pattern (Example 8.21) give invalid bounds with curvature-only
   corrections.
3. **Polynomial-complexity claims for TU coupling.** The abstract and intro
   omit the hypotheses these claims need: set growth, finitely many optimal
   coordinate values, and polynomially bounded `kappa_c`, `W/eta` and `r`.
   Without growth the cost is `(W sqrt(n_c Lbar/eps))^p`, which is
   pseudopolynomial in `1/eps`.

The remaining findings are minor:

- a tie-dependent claim in Remark B.2;
- wrong part references;
- an open question stated as open although Proposition `lim:prop:setgrowth`
  partly answers it;
- a stale cross-reference range in `exact.tex`;
- loose constants;
- notation clashes.

## What was re-derived (all correct unless listed under Findings)

### Section 8 (constraints.tex)

**Feasible corner rounding (`lem:tu-round`).**

- Alignment `(b-Bz)/eta in Z^m` and `t/h in Z^{n_c}` make
  `rho = (b-Bz-At)/h` integral.
- `[A; I; -I; e_i rows]` is TU, so by Hoffman–Kruskal the polytope `Q` has
  0/1 vertices that vanish on `N_0`.
- The Caratheodory decomposition of `theta` gives a rounding that is feasible
  and preserves the mean.
- Equality pairs force `A_r(Y-x) = 0`, so `Y - x` lies in `ker C`.
- Each coordinate has variance `(x_i-t_i)(t_i+h-x_i) <= h^2/4`.
- Cells of non-node coordinates lie inside the component.

**Rounding allowance (`lem:tu-allow`).** The Taylor step is valid along the
segment inside the box, with `w in K`. This gives `E_j = n_c Lbar h_j^2/8`.

**Example 8.7.** `F(s,s) = 2s^2 - 2hs` has minimum `-h^2/2`, every grid point
has value `2h^2 k(k-1) >= 0`, the Hessian eigenvalues are `±2`, and the
allowance `h^2/2` is attained. Exact check passed.

**Soundness (`prop:tu-sound`), all cases of (c).**

- Label removal.
- A node coordinate in a single-point component.
- A node coordinate as a shared endpoint: all adjacent cells removed implies
  `m_i(x_i) > U_j`.
- A non-node coordinate.
- The hull variant, a fortiori.
- (d) and (e), and the checker statement, which needs only (b), (c) and the
  recomputed `U_j >= U_J`.
- Nestedness holds in both variants. (Single-point components never arise in
  TU-GRID, which is harmless.)

**State counts (`thm:tu-states`).**

- A qualifying endpoint `t` has a witness with `F(w) <= F* + 2E_j`, so
  `dist(w,S)^2 <= a_j^2 = n_c Lbar h_j^2/(4g)`.
- An interval of length `2a_j + 2h_j` holds at most `floor(4a_j/h_j) + 5`
  points of `h_{j+1}Z`, and `4a_j/h_j = 2 sqrt(n_c Lbar/g)`.
- (c) for the hull variant is correct.

**Example 8.10.**

- `g = 1/6`: verified by hand in both halves, and on a rational sample (the
  minimum ratio is exactly 1/6, at `z = 1/2`).
- Hessian rows: `Lbar = 12` is valid.
- `n_c Lbar/g = 216 n_b`.
- The hull variant has `2^j + 1` points.

**Complexity (`thm:tu-approx`).**

- `J <= ceil((1/2) log2(n_c Lbar eta^2/(8 eps)))`.
- `K_0 <= max{d, W/eta + 1}`; `K_j <= K` for `j >= 1`.
- Bit lengths: denominators divide `D_0 2^j`.
- The table size without growth at the last level,
  `(W sqrt(n_c Lbar/(2eps)) + 1)^p`, follows from minimality of `J`.

**Height (`lem:tu-statpoly`, `cor:tu-height`).**

- (a) stationarity and positive semidefiniteness on `ker M_{J0}`.
- (b) `P(s) x {z}` is contained in `S`.
- (c) `P_xx` is positive definite on `ker E`, through the polarization step
  `P_xx w ⊥ ker M_{J0}`.
- The saddle matrix `K` is nonsingular.
- Cramer's rule with the right side in `D_0^{-1}Z`.
- Hadamard row bound `(sqrt(2 n_c) C_P)^{n_c} n_c^{r/2} <= (sqrt2 n_c C_P)^{n_c} <= R`.
- `W <= Delta (D_0 R)^2 = Omega`.

**Acceptance and snapping (`prop:tu-accept`, `lem:tu-snap`).**

- `J_0` is contained in `J`.
- The slack at `s_x` is at most `3tau/2`.
- `psi(s_x) <= 3/(8 D_0 R)`, and `psi(v)` lies in `(D_0 delta)^{-1}Z`, so
  `psi(v) = 0`.
- Every point of `Pi` is optimal (exact expansion, unrestricted multipliers).
- The premature-recovery example `x - x^2` returns `(1/2,1/2)` with value
  `1/4`.

**Exact output (`thm:tu-exact`).**

- (b) uses compactness.
- (c) sufficient conditions:
  - `h_j <= tau/(n_c sqrt(kappa_c))` gives `E_j <= g tau^2/(4 n_c)`, using
    `g >= Lbar/kappa_c`;
  - `h_j <= 2/(Omega sqrt(n_c Lbar))` gives `E_j <= 1/(2 Omega^2)`.
- `J_ex` is correct, with a little slack in the second term.

**Uniform-mesh lower bound (`prop:tu-tight`).**

- The induction from `D^{(1)} = [0,1]^{n_c}`.
- `m_i(t) <= 0` if and only if `|t - 1/2| <= sqrt(n_c) h_j/2`.
- The retained interval is `[1/2 ± (k+1)h_j]`, with `4k + 5` nodes.
- Exact simulation: `n_c in {4, 9, 16, 25, 50, 100}`, levels 0–13. Passed.

**Misaligned grids (`prop:tu-misaligned`) and its two examples.**

- The `{0,1/2,1} x {0,1/3,1}` example:
  - `gamma = 1/3`;
  - threshold `75L/288`;
  - corrected minimum `743/9000 > 0` just above the threshold.
- The graded grids around `3/10` and `7/10` (`h = 1/16`, `theta = 1/4`):
  - eleven nodes each;
  - common nodes exactly `{0,1}`;
  - the gap condition holds at `m = 1/2`;
  - `gamma = 27/1280`;
  - a violating `lambda` exists.

**Example 8.21.**

- `G = {0, 1, 9/4, 3}`.
- Corrections `L/8`, `25L/128`, `25L/128`, `9L/128`.
- Seven feasible points; minimum corrected value `31L/64`.
- The triangle fiber has the non-corner vertex `(1,1,2)`.

**Remark 8.22.** The composite rounding (coupled block by TU vertices, free
coordinates independently) needs exactly `Lbar` on the coupled block and
coordinate curvature on the free coordinates. The outline is correct as
stated.

**Remark 8.23 (Bienstock–Muñoz).** Checked against the knowledge base:

- Theorems 4 and 15: size `O((2pi/eps)^{omega+1} n log(pi/eps))`;
- feasibility tolerance `𝔉 eps`, optimality tolerance `||c||_1 eps`;
- Appendix A lower bounds: treewidth `<= 2`, subset-sum reductions.

The halving `p/2` against `omega + 1 = p` is correct. The proximity radius
`n Delta s` of Hochbaum–Shanthikumar is confirmed.

### Section 9 (optsets.tex)

**`prop:twocenters`.**

- `S`, `F*` and the symmetry hold.
- Growth `1/20` holds in both cases; the sample minimum is `1/2`.
- The bound: the case `K = 1`, the case split `c'^2 >= a^2/5`, the recursion
  `D_{K-2} >= (D_K - (2+theta)h)/(1+theta)^2`, `23M/100`, and
  `0.23^2/20 = 0.002645 > 1/379`.
- Exact check over 168 parameter combinations: `beta <= bound` everywhere.
- **The consequences paragraph is wrong for CT** (Finding 1).

**UC and `lem:cells`, `thm:cells`.**

- Nested `Lambda`, including the integer ceiling identity.
- Cell lengths `<= h_j`, and `< 2h_j` for integer cells.
- Sequential Jensen with independent rounding.
- Gap `D <= (1/2) n L h_j^2`.
- The count:
  - qualifying endpoint gives `F(z) - F* <= n L h_j^2`, hence
    `|v - sigma| <= sqrt(n kappa_S) h_j`;
  - at most `2 rho/delta + 2` endpoints per optimal value, two cells per
    endpoint;
  - `3 x 2r(4 sqrt(n kappa_S) + 2) = K_S`.
- Exact UC run on `F_M`, `M = 4`, 12 stages: brackets hold, at most 6 nodes
  against `K_S = 453`.

**`lem:endpointid`, `thm:endpointset`, `cor:facecsp`.**

- Telescoping; expectation under independent endpoint rounding,
  `E F(Y) = F(x) + (1/2) sum H_ii Var`.
- Traceback via running intersection.
- The `x + y - 2xy` example.
- Face patterns: (i)–(iii); the formulas for uniqueness, dimension, `|S|`
  and `dist(y,S)^2`; linear minimization over `{L, U}` labels.
- `rem:endpointext`:
  - the two-label chord identity holds at `l` and `l + 1`;
  - the multilinear and concave extension holds;
  - "affine if and only if it vanishes at an interior point" holds for
    concave `psi`.

**`lem:diagcert` (i)–(iii).**

- Value, gradient and Hessian match at `xbar`.
- Dual argument: complementarity and stationarity force
  `lambda = lambda(xbar)`, which gives uniqueness and invariance.
- `rem:shor` example: diagonal `(2, 2, 1/4)`, `Lambda = diag(0,0,1/4)`,
  `H + Lambda = 2aa^T`. Exact check passed.

**`lem:proximal` (Appendix B).**

- (i):
  - integer step `>= (H + theta t)/3`;
  - `theta rho <= sqrt(n/2) + 1/2`;
  - `|G_i| <= 10 theta^{-1} ceil(log2(n+2))`.
- (ii):
  - `s*` lies in `B`;
  - variance `<= (1/2)(h^2 + theta^2 |s*_i - c_i|^2)`;
  - `d_i <= L h^2/4 + eta |v - c_i|^2`;
  - `1 + (1/2)(33/32) + 1/32 = 99/64`.
- (iii) induction.
- (iv) the denominator formula
  `h_j[(2^mu + 1)^k - 2^{mu k}]/2^{mu(k-1)}`.

**`thm:diagdiscovery`: the thresholds match REC.**

- `exact.tex` defines `tau = 1/(4nR)` with `R = Delta prod_{I_C^+} P_ii`.
- `lem:snap` needs `dist(y,S) <= tau/2`.
- `J_K`, the least `j` with `4^j tau^2 >= 4Kns^2`, gives
  `dist^2 <= (99/256) K n s^2 4^{-J_K} <= (99/256) tau^2/4 < tau^2/4`.
- The REC endpoint separation `1/Delta >= 4n tau > 2 tau` holds because
  `R >= Delta`.
- (a) and (b) follow.
- (c): at most `1 + log2(2 kappa)` guesses, `J_K = poly(I) + O(log K)`, and
  `K_theta <= 600 sqrt(K) ceil(log2(n+2))`. Correct.

**`rem:falseguess`.**

- Exact rerun of the proximal iteration.
- Budgets `J_K = 28, 28, 29` for `K = 1, 2, 4`, against the stated 33.
- The origin is returned at every stage up to 33.
- `H + Lambda` has eigenvalue `-1/64` at the origin and is positive definite
  at `(1,1)`.
- **Caveat:** for `K = 4`, stages 0 and 1 have tied minimizers (Finding 4).

**`prop:sshard`.**

- The path decomposition is valid.
- `F = 0` exactly at Subset Sum solutions.
- `H + Lambda = M`, with `M` positive semidefinite, and `lambda = 2` on `x`.
- The reduction is sound, including on instances outside `C`.
- Zero-subset-sum uniqueness hardness holds.

## Findings

Severity: **critical**, a false main claim; **major**, a wrong statement,
misleading claim or real gap; **minor**, a local error, notation or wording
problem.

### Major

**1. `optsets.tex:39-51` (statement) and `:91-100` (proof), Proposition 9.1
(`prop:twocenters`).**

*Issue.*

- **The `z`-grid in CT.** The consequences are stated "in FG and CT". In
  Algorithm 1 (and so in CT), every `i ∉ P` gets `G_i = {l_i, u_i}`
  (`growth.tex:47-49`). Here `L_z = 0`, so `G_z = {0, M}` at every stage.
- **False counts.** These three claims are false for CT:
  - "uses grids with at least `M/(48 sqrt eps)` nodes in each coordinate";
  - "the table of the bag `{x,z}` has at least `M^2/(2304 eps)` entries";
  - "builds a table with at least `M^2/2304` entries".
- **Concrete failure.** Take a trial with `2^{-mu}` in
  `(sqrt(eps)/(2M), sqrt(eps)/M]` and the stage with `h_x` in
  `(sqrt(eps)/2, sqrt(eps)]`, which lies within the budget `J`.
  - The gap is at most `D <= (2/8)(h + theta M)^2 <= eps`.
  - The `x`-grid stays below the cap `K_mu = 20 * 2^mu`, so the trial
    succeeds there or earlier.
  - The table then has at most `40 * 2^mu < 80 M/sqrt(eps)` entries. This is
    below `M^2/(2304 eps)` once `M/sqrt(eps) > 184320`.
  - Illustration: `M = 2^20`, `eps = 1/16` gives a table of about `5.8e6`
    against the claimed `7.6e9` (`checks/r3_optsets.py`).
- **Still true.** `2^{Omega(I)}` survives, since the `x`-grid alone has at
  least `M/(48 sqrt eps)` nodes.
- **Undefined name.** "FG" is used twice and never defined.
- **Stage 0.** The hypothesis `h <= M` excludes CT's stage 0, where `h_{x0}`
  lies in `[M, 2M)`.

*Fix.* Replace the statement from "Let `theta`" to the end with:

> Let `theta ∈ (0,1/4]`, `h ∈ (0,M]` and `c ∈ X`. Let `G_x` be the graded
> grid (5.1) of `[0,M]` with center `c_x`, mesh `h` and grading `theta`. Let
> `G_z ⊆ [0,M]` be any grid containing `0` and `M`. Use corrections
> `d_x = L_x w_x^2/8` with `L_x >= 2` and any `d_z >= 0`. Then
> `beta = min_G Q <= -max{theta^2 M^2/379, h^2/20}`.
>
> Consequently, every stage of Algorithm 1 and of CT has certified gap
> `U - beta >= max{theta^2 M^2/379, h^2/20}`. At stage 0, `h < 2M` and the
> `x`-grid is `{0, M}`, so `beta <= -M^2/4 <= -h^2/20`.
>
> A stage certifying a gap `eps` has an `x`-grid with at least
> `M/(48 sqrt eps)` nodes, so its bag table has at least `M/(24 sqrt eps)`
> entries. Any exact-output procedure based on these certificates that
> accepts only when `U - beta < 1`, such as EX, builds a table with at least
> `M/24` entries. For integer `M`, `I = O(log M)`, so this work is
> `2^{Omega(I)}`.

In the proof:

- replace "every box of FG" with "every box of Algorithm 1";
- replace the last three sentences with: "Since `L_z = 0`, Algorithm 1 uses
  `G_z = {0, M}`. The side of length at least `M/2` of the `x`-grid needs at
  least `M/(48 sqrt eps)` nodes, and the table of the bag `{x,z}` has at
  least `2M/(48 sqrt eps)` entries. CT stops only after some stage certifies
  its target, and an acceptance with `U - beta < 1` needs a stage with gap
  below one."

**2. Overclaim that uniform meshes are forced.** Locations:
`intro.tex:113-114`, `constraints.tex:12-15`, `:674-679` and `:729-730`.

*Issue.*

- **The claims.** The intro says "we show that the uniform meshes responsible
  for this are forced". Section 8 says "the mesh must be uniform … both
  prices are intrinsic" and "Uniformity, however, is forced by the
  constraints".
- **What Proposition 8.20 shows.** Grids `G_1, G_2` that satisfy the gap
  condition (8.6) give invalid bounds on an order row for some `lambda`. Such
  grids lack a common node close enough to `m`. A common grid `G_1 = G_2`
  with the corrections of Section 4 never satisfies (8.6).
- **What Example 8.21 shows.** One specific common graded pattern fails on a
  sum row.
- **What is missing.** Neither result shows that every non-uniform aligned
  product grid fails, nor that every certificate using non-uniform grids must
  fail.
- **What holds.** The first price (full Hessian) is shown to be necessary by
  Example 8.7.

*Fix.*

- In `intro.tex:113-114`, replace with: "and we show that two natural
  non-uniform alternatives, misaligned coordinate grids and a common graded
  pattern, give invalid bounds with curvature-only corrections
  (Proposition 8.20, Example 8.21)".
- In `constraints.tex:12-15`, replace with: "and the analysis uses a uniform
  aligned mesh, so the per-coordinate state count is of order
  `sqrt(n_c kappa_c)` instead of logarithmic in `n`. The last subsection
  shows that the first price is necessary, that the second is incurred by
  the algorithm, and that natural non-uniform grids give invalid bounds with
  curvature-only corrections."
- In `:729-730`, replace with: "Natural non-uniform alternatives fail, as
  follows."

**3. Polynomial-complexity claims for TU coupling.** Locations:
`abstract.tex:30-32` and `intro.tex:111-113`.

*Issue.*

- **The claims.** The abstract says TU coupling admits rounding "with
  polynomial complexity for fixed width". The intro says "the algorithm is
  polynomial for fixed width and conditioning".
- **What Theorem 8.11 gives.** Polynomiality only under all of:
  - set growth;
  - finitely many optimal coordinate values (`r`);
  - polynomially bounded `kappa_c`, `W/eta` and `r`.
- **Without growth.** The last table has `(W sqrt(n_c Lbar/eps) + 1)^p`
  entries, which is pseudopolynomial in `1/eps`.
- **Even with growth.** `K_0` can be pseudopolynomial in the data, and
  `limits.tex:594` shows that this cannot be removed in general.

*Fix.*

- Abstract: "Totally unimodular coupling constraints with aligned data admit
  exactly feasible correlated rounding; under set growth with finitely many
  optimal values per coordinate the grids have accuracy-independent size,
  polynomial for fixed width when the condition number and the initial mesh
  are polynomially bounded".
- Intro: "under set growth with finitely many optimal coordinate values the
  algorithm is polynomial for fixed width when `kappa_c`, `W/eta` and `r` are
  polynomially bounded, but it is not fixed-parameter tractable".

### Minor

**4. `appendix-proximal.tex:114-116`, Remark B.2.** "The iteration with
`K in {1,2,4}` returns the origin at every stage `j <= 33`." For `K = 4`
(`mu = 3`, `eta = 1/128`), the stage-0 and stage-1 objectives tie between
`(0,0)` and `(1,1)`, both with value `-1/2` at stage 0 (exact rerun,
`checks/r3_falseguess_ties.py`). A minimizer choice of `(1,1)` would lead to
acceptance. *Fix:* "returns the origin at every stage `j <= 33` for
`K in {1,2}`, and for `K = 4` when ties are broken towards the current
center (at stages 0 and 1 the points `(0,0)` and `(1,1)` tie)". Or state a
tie-breaking rule in the proximal stage.

**5. `constraints.tex:659-660`, Remark 8.18.** It cites
Theorem 8.9(a) for the hull variant. Part (a) is stated for TU-GRID (union),
and the hull bound is part (c), which assumes (8.4). *Fix:* "by
Theorem 8.9(c), under (8.4), which holds for some `g > 0` when `S = {v*}`".

**6. `optsets.tex:24`, `:551-553`, `:606` and `:626`, the notation
`kappa`.**

- Section 9 defines `kappa_S`, but these lines use `kappa`. In Setting,
  `kappa` is defined only for point growth.
- Theorem 9.12(c) is unconditional. Outside `C` the procedure may not stop.

*Fix:*

- Replace `kappa` by `kappa_S`, computed with the given `g`.
- Begin (c) with "Under the hypotheses of (b),".
- In Proposition 9.13, write "unless P=NP, no polynomial in the input length
  bounds `kappa_S` on these instances".

**7. `optsets.tex:229-231`, Remark 9.4.** It says it is open whether "any
accuracy-independent grid bound when `S` is a continuum" exists. For
corrected product-grid certificates, Proposition `lim:prop:setgrowth`
already proves it is impossible. *Fix:* "…is open when `S` is finite. When
`S` is a continuum, Proposition `lim:prop:setgrowth` shows that corrected
product grids need accuracy-dependent size; other representations are
open."

**8. `appendix-proximal.tex:66-68`, Lemma B.1(ii).** It cites
Proposition 4.2 (cellwise) for `E[F(Y) - D(Y)] <= F(s*)` under independent
rounding. Proposition 4.2 states the cell bound, not this expectation. The
expectation inequality is proved in Lemma 9.2. *Fix:* "The interpolation
argument in the proof of Lemma 9.2, applied on the box `B`, gives …".

**9. `appendix-proximal.tex:13` and `:59-61`; `optsets.tex:588`.**

- `K_theta = 100 theta^{-1} ceil(log2(n+2))`, but (i) proves
  `|G_i| <= 10 theta^{-1} ceil(log2(n+2))`.
- The unexplained factor 10 inflates the stated table size to
  `(600 sqrt K)^p`.

*Fix:* set `K_theta = 10 theta^{-1} ceil(log2(n+2))`, and replace
`(600 sqrt K)^p` with `(60 sqrt K)^p`.

**10. `exact.tex:19` and `:12-14`.**

- "Throughout Sections 6.1–9.1" now spans Sections 7 (recourse) and 8
  (constraints), because `sec:exact-nonunique` moved to Section 9.
- The Section 6 introduction announces the unions-of-cells result, which
  now lives in Section 9.

*Fix:* end the range at the last subsection of Section 6, and move the
sentence "Without uniqueness … polynomial for fixed bag size" to the
Section 9 introduction, or point to Section 9 explicitly.

**11. `intro.tex:121-123` and `optsets.tex:9-10`.** "An unknown optimal set
is found exactly" suggests explicit knowledge of `S`. The output is one
optimizer plus the implicit description (9.12), and deciding uniqueness from
it is NP-hard (`optsets.tex:633-637`). *Fix:* "an exact optimizer and an
exact description (9.12) of the optimal set are found in `f(p,kappa_S)
poly(I)` time".

**12. `intro.tex:116-118`, `optsets.tex:7-8` and `exact.tex:13-14`.** These
say "unions of uniform cells restore a bound polynomial for fixed width".
But `K_S^p` contains `r^p (n kappa_S)^{p/2}`, and `kappa_S` can be
exponential in `I`. *Fix:* "a bound polynomial in `n`, `r` and `kappa_S` for
fixed width".

**13. `constraints.tex:423-426`.** "It is not fixed-parameter tractable …
this factor is really incurred" can be read as a hardness claim about the
problem. *Fix:* "The running time of TU-GRID is not bounded by
`f(p, kappa_c) poly(I)`: `K^p` contains `n_c^{p/2}`, and Proposition 8.19
shows that this factor is incurred."

**14. Notation clashes in the three files.**

- `W`: maximum width (8.1) and reduced denominator (`cor:tu-height`,
  `prop:tu-accept`, TU-EXACT).
- `J`: last level and the TU-REC row set.
- `K`: grid bound, saddle matrix, the `x`-node count in `prop:twocenters`,
  and the guess.
- `E`: the allowance `E_j`, the row basis `E`, `E_i = {l_i, u_i}`, and
  `E = ||s* - c||^2`.
- `eta`: mesh unit (Section 8) and proximal weight (Appendix B).
- `tau`: Taylor parameter, recovery threshold, and face pattern.
- `rho`: right-side vector and denominator.
- `N`: number of bags and a kernel basis.
- `d`: label bound, `d_z`, and `d_i`.
- `l_i` against `ell_i` in Sections 9.2–9.3.
- `S = \mathcal S`, with `S_i` versus scope `S_a`.
- `psi` and `sigma`, each used three ways.

*Fix:* rename the local objects:

- `W -> W_F` for the denominator;
- the TU-REC row set `-> \mathcal J`;
- the saddle matrix `-> K_E`;
- the guess `-> \hat K`;
- the row basis `-> E_r`;
- the proximal weight `-> \omega`;
- write `ell_i` throughout.

**15. Smaller local items.**

- `optsets.tex:166`: `U_j` is undefined in UC. Write "the threshold `U` used
  at stage `j`".
- `optsets.tex:523-524`: add the range `0 <= v <= 1` to `{(v,v,0)}`.
- `conclusion.tex:45`: change "Propositions~\ref{prop:tu-misaligned}" to
  "Proposition".
- `optsets.tex:465-466`: equation (9.6) has a 5 pt overfull box.
- `appendix-proximal.tex:18`: "outward geometric grid" should be "graded
  grid" (Definition 5.1).
- Appendix B treats integer coordinates although Section 9.3 is
  continuous-only. Drop the integer cases to shorten the proofs
  (`:17-20`, `:51-55`, `:64-66`, `:72`, `:102`).

## Checks run (targeted; exact arithmetic unless noted)

All runs used `python3 -B` from `process/w2/checks/`:

**`r3_examples.py`.** All PASS.

- `ex:tu-fullcurv` for `h in {1/2, 1/3, 1/8}`.
- `ex:tu-union`: growth ratio on a 41x41 rational sample has minimum `1/6`.
- `prop:tu-tight` for `n_c in {4, 9, 16, 25, 50, 100}`, levels 0–13.
- `prop:tu-misaligned`: both examples, including the eleven-node graded grids
  and violating `lambda`.
- `ex:tu-sum`.
- `prop:twocenters` bound on 168 combinations of `(theta, h, c_x)`, with
  `G_z = {0, M}`.

**`r3_optsets.py`.**

- `prop:twocenters` growth sample.
- UC on `F_M` (`M = 4`, 12 stages): brackets hold and node counts stay within
  `K_S`.
- `rem:shor` matrices.
- A floating-point count illustrating Finding 1 (counting only).

**`r3_falseguess.py`.**

- Budgets `J_K = 28, 28, 29`.
- The proximal iteration returns the origin at all stages `<= 33` for
  `K = 1, 2, 4`, with unique argmin for `K = 1, 2` only.
- `H + Lambda` eigenvalues.

**`r3_falseguess_ties.py`.** Lists the `K = 4` ties at stages 0 and 1.

These are finite checks that support the hand derivations. No project-wide
verification was run, and no CI status was inspected.
