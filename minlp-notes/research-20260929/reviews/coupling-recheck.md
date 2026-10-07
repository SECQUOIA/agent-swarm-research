# Recheck: coupling note, second-round revision

Date: 2026-09-30. Note:
[`../theory-coupling/coupling.md`](../theory-coupling/coupling.md), Section 11
("Revision after review") and the passages it changed. First review:
[`coupling-review.md`](coupling-review.md). My checks are in
[`coupling-recheck-checks/`](coupling-recheck-checks/) (scripts `r0`–`r4`,
logs in `logs/`). I am an independent referee: I did not write or review the
note before. I did not edit the note and did not commit anything.

Scope: the eight items I was asked to recheck. I read the whole note, but I
did not re-verify results that the revision did not touch (Theorems 2.1,
2.2, 3.1 and the proof of Theorem 4.5 beyond its constants). For
Definition 1.2, Corollary 2.1 and Lemma 3.1 I used the decomposition note
[D] as the source.

## Verdict

| # | Item | Verdict |
|---|---|---|
| 1 | Prop. 1.1: factor `det(I + H^{-1/2} A^T ∇²g A H^{-1/2})^{-1/2}` | **correct**; two wording points (M1, M2) |
| 2 | `Gamma_sigma = 16(1+Delta)(d+1) max(1, 64 sqrt(k) nu_A (1+M_F/c_g)^2)` | **correct**; follows exactly from (T4) |
| 3 | Thm. 5.1(d): lifted box certificate, `3n^2 - 3n + 2` boxes | **correct**; proof checked against [D, Def. 1.2]; exact check for all odd `n <= 29`; wrong part label in one table (M4) |
| 4 | Prop. 2.6(c): the dual optimum is attained, so the attainment hypothesis can be dropped | **correct**; `x*` should be called a global minimizer (M3) |
| 5 | Prop. 5.2 extended to envelope (Lagrangian) node bounds; bases 1.85–1.92 at `m = 8` | **correct**; two rounding slips (M5) |
| 6 | Corrected ETH statements | **correct**; they match the KPW abstract; the model-of-computation sentence needs care (M7) |
| 7 | Census shares 14.8%; 17.2–17.4%; 16.3–17.0% | **reproduced exactly** by independent code; sample rerun of the heuristics identical (34/34 records) |
| 8 | Every summary-log line comes from a saved script | **confirmed**: `census_k_analyze.py` reprints `census_k_summary.log` byte for byte; two open counts in the text are not printed by any script (M8) |

No claim in the revision is false. Items M1–M8 below are small wording,
labeling and provenance fixes. None changes a theorem or a headline number.

## 1. Proposition 1.1: the determinant factor

**Correct.** Derivation:

- The bound of [D, Corollary 2.1] is
  `2 (2n/pi)^{n/2} (prod_j alpha_j / det H)^{1/2} Gamma(n/2)^{-1} J_n(R/sqrt(eps))`,
  with `R^2 = lambda_min(H) r_in^2/2`. It needs
  `m(x) <= (1/2)(x - x*)^T H (x - x*)` on `X0`.
- Add a convex `C^2` cost `g(y)` with `∇²g ⪯ Gbar`, and keep `x* = 0` (for
  example `A^T ∇g(0) = 0`). The Hessian of `F_n` is at most `H` on the whole
  box, because `2 - 12 kappa x_i^2 <= 2`. So the hypothesis holds with
  `H' = H + A^T Gbar A`.
- `det H' = det H · det(I + H^{-1/2} A^T Gbar A H^{-1/2})`. This gives the
  stated factor. `J_n` can only grow, because `lambda_min(H') >= lambda_min(H)`.
- The matrix `H^{-1/2} A^T Gbar A H^{-1/2}` has rank at most `k`, and its
  eigenvalues are at most `||A||^2 ||Gbar|| / lambda_min(H)`. This gives the
  lower estimate `(1 + ||A||^2 sup||∇²g|| / lambda_min(H))^{-k/2}`.

`r4_constants.py`, part (1), with `n = 8, 16, 24` and `k = 1..4`:
- the new quadratic upper bound holds on samples;
- the determinant identity holds to `1e-15`;
- the factor is above the lower estimate;
- the full Corollary 2.1 bound with `H'`, divided by the bound with `H`, is
  at least the factor.

- **M1 (precision).** The factor is exact when the minimizer stays at 0.
  The note also allows the minimizer to move ("if `g` has linear terms"). In
  that case `r_in`, and hence the `J_n` term, also change. Corollary 2.1 then
  needs the new minimizer to be interior with zero gradient. One clause
  would cover this.
- **M2 (Summary item 1 and status table: "changes the constant").** For
  dense rows with entries of order one, the factor is not a constant. For
  one row of ones and `g(y) = y^2/2`, it is about `1.9/sqrt(n)`
  (`r4`: 0.502, 0.186, 0.060 at `n = 10, 100, 1000`). So it is about
  `n^{-k/2}` for `k` such rows. The claim that matters, that the
  exponential base in `n` survives for fixed `k`, is right. Suggested
  wording: "changes the prefactor by a factor at least
  `(1 + ||A||^2 sup||∇²g||/lambda_min(H))^{-k/2}`, which is polynomial in
  `n` for rows with bounded entries".

## 2. `Gamma_sigma` from the conditions of Theorem 4.5

**Correct.** (T4) has two conditions:

1. `theta ((1+Delta) d + Delta) <= 1/2`;
2. `128 rho ||A|| sqrt(k) (1+Delta)(d+1) alpha_A theta <= c_g`.

With `rho = K` and `m = M_F/c_g`:
- `K/c_g = kappa^2 (m^2 + m + 1)/2 <= kappa^2 (1+m)^2`. The ratio is at most
  1/2, so there is a factor 2 of slack.
- So `rho ||A|| alpha_A / c_g <= nu_A (1+m)^2 =: V`.

Put `X = 2 (1+Delta)(d+1) max(1, 64 sqrt(k) V)`.
- If `theta <= 1/X`, condition 1 holds because
  `(1+Delta) d + Delta < (1+Delta)(d+1)`. Condition 2 holds because
  `128 sqrt(k) V (1+Delta)(d+1) <= X`.
- The largest power of 1/2 with `theta <= 1/X` satisfies
  `theta > 1/(2X)`. So `4/theta < 8X = Gamma_sigma`.
- On paths (`Delta = 1`, `d + 1 = |T|`), `Gamma_sigma = 32 |T| max(...)`,
  as the note says.

`r4`, part (2): on 200,000 random `(Delta, d, k, V)`, both conditions held,
and `(4/theta)/Gamma_sigma <= 1` in every case (maximum 1.0000). The size
bound `Gamma_sigma^{k Delta_1}` is used consistently in the Summary, in
Sections 4.3, 5.3 and 8, and in Section 11.

## 3. Theorem 5.1(d): the lifted certificate for `J_n`

**Correct.** I checked the proof against [D, Definition 1.2], applied to the
lifted model of Section 4.2:

- *Minorants.* `(c/2) dist(·, Z)` is affine on every interval
  `[j/2, (j+1)/2]`, so it is an admissible cell minorant. The chord of
  `c y(1-y)` is `(c/2) y` on `[0, 1/2]` and `(c/2)(1 - y)` on `[1/2, 1]`,
  which is `(c/2) dist(y, Z)` in both cases.
- *(CM).* Each bag leaf projects onto exactly one child cell. Take the child
  bound to be that cell's minorant. It meets the neighbouring cells only at
  their shared endpoints, where all minorants take the same value
  `(c/2) dist`.
- *(LC).* The condition reads
  `dist(y) + dist(zeta_{t-1}) >= dist(zeta_{t-1} + y)`. This is
  subadditivity: if `p` and `q` are the integers nearest to `a` and `b`,
  then `|(a + b) - (p + q)| <= dist(a) + dist(b)`.
- *Root.* Section 4.2 now lets the root impose `zeta_n = n/2`. Every
  admissible point then has relaxed value at least
  `(c/2) dist(n/2) = c/4 = OPT`.
- *Count.* Bag 1 has 2 leaves. Bag `t >= 2` has `4(t-1)` leaves. Separator
  `t < n` has `2t` cells. The total is
  `2 + 2n(n-1) + n(n-1) = 3n^2 - 3n + 2`.
- *Side-1 cells.* Validity forces each affine minorant to lie below `c phi`
  on `[j, j+1]`. `c phi` vanishes at both ends, so the minorant is at most 0
  there. At the root point `y_n = 0`, `zeta_{n-1} = n/2`, every leaf
  relaxation is then at most 0. So `l_r <= 0` for **any** leaves.

Computations:
- `r3_jn_certificate.py` checks the stated certificate in exact rational
  arithmetic for every odd `n` from 1 to 29. It confirms:
  - every minorant is affine on its cell;
  - (CM) holds, and (LC) holds for every (leaf, cell) pair;
  - every minorant lies below the value function `c phi`;
  - `l_r = 1/4`;
  - the size equals `3n^2 - 3n + 2`.
- An LP over **all** affine minorants with the same leaves gives `max l_r = 0`
  for side 1 and `0.25` for side 1/2 (`n = 3..9`).
- The lattice-path identity `2 sum_{j<=m} C(m+j, j) = C(n+1, (n+1)/2)`
  holds for `m <= 39`.
- The first odd `n` with fewer boxes than `C(n+1, (n+1)/2)` is 9.

The author's `jn_lifted_cert.py` computes maximal intercepts and does not
check (CM). `r3` shows that its intercepts equal the `(c/2) dist` ones (for
`n <= 15`). So its minorants are continuous and its certificate is valid
too. Its log reproduces exactly (`r0`).

- **M4 (label).** The table in Section 6.2 cites "Theorem 5.1(c)" for the
  `3n^2 - 3n + 2` certificate; it is part (d). The docstring of
  `jn_lifted_cert.py` also says "(c)".
- **M6 (cosmetic).** The itemized sum `2 + 2 + ... + 4(n-1)` assumes
  `n >= 2`: it gives 4 at `n = 1`, where the closed form 2 is right. Also,
  "exceeds `C(n+1,(n+1)/2)` for `n <= 7`" holds for `3 <= n <= 7`; at
  `n = 1` the two are equal.

## 4. Proposition 2.6(c): attainment

**Correct.** `A` has full row rank and `B(x*, r0) ⊂ X0`. For `mu != 0` put
`x = x* - r A^+ mu/|mu|` with `r = r0 sigma_min(A)`. Then `x` lies in the
ball, and `mu^T (A x - b) = -r |mu|`. So `L(mu) <= max_{X0} F - r |mu|`.

`L` is finite and concave, hence continuous. Its superlevel sets are
compact, so `D` is attained. If `D = OPT`, then `x*` minimizes the
Lagrangian at an interior point. The second-order necessary condition then
gives `∇²F(x*) ⪰ 0`, a contradiction. (`F` must be `C^2` near `x*`; this is
implicit.)

- **M3.** Part (c) does not say what `x*` is. The proof uses `F(x*) = OPT`,
  so `x*` must be a global minimizer of (P). A local minimizer, as in
  Proposition 2.5, is not enough. Any global minimizer works; uniqueness is
  not needed. The separate attainment remark in Proposition 5.2(a) is now
  redundant, but harmless.

## 5. Proposition 5.2 extended to envelope node bounds

**Correct.**
- *Concavity.* `h'' = -beta + 12 s^2 <= -(beta - 12)` on `[-1, 1]`, and
  `beta = 3.2 m > 12` for `m >= 4`. So the envelope of `h` on any
  sub-interval is the chord.
- *Gap.* The difference `h - chord` has second derivative at most
  `-(beta - 12)` and vanishes at both ends. So it is at least
  `((beta-12)/2)(s-l)(u-s)`.
- *Transfer.* The covering proof of (b) uses only this per-leaf gap
  inequality, so `alpha' = 1.6m - 6` can replace `alpha`.
- *Lagrangian bounds.* For single-variable blocks, the termwise envelope
  bound with the rows equals the box Lagrangian dual (Theorem 2.1 with
  blocks of one variable).

Numbers from `r4`, part (3). Sampled chord gaps were at or above `alpha'` in
all cases.

| `m` | envelope base, over `1 <= k <= m` |
|---|---|
| 4 | 0.6117–0.6546 |
| 8 | 1.8469–1.9165 |
| 16 | 2.2584–2.3019 |
| 32 | 2.4482–2.4720 |
| 1024 (`k = 1`) | 2.6254; the limit is `sqrt(8e/pi) = 2.6310` |

`alpha'/lambda'` increases with `m`. So the base is at least 1.85 for every
`m >= 8`, and "`exp(Omega(k))` once `m >= 8`" is right, with
`m >= max(8, k)`.

- **M5 (rounding).** At `m = 4`, the upper end is 0.6546, so it should read
  "0.61–0.65", not "0.66". "`alpha/lambda' >= 1.73` for `m >= 4`" is
  slightly off: at `m = 4`, `k = 1`, the ratio is `6.4/3.7 = 1.7297`. Write
  `>= 1.729`. The base `≈ 2.45` (2.4468) is fine.

## 6. The corrected ETH statements

**Correct.** I fetched the abstract of arXiv 1811.01296. For
`{0,1}`-matrices it states that "an algorithm with running time
`2^{o(k log k)}·(ℓ+‖b‖∞)^{o(k)}` would contradict ETH". This matches
Proposition 5.3(b).

The transfer checks:
- The optimum is either 0 or at least `4c/(l+1)^2`. So accuracy
  `eps = 2c/(l+1)^2` decides feasibility.
- `polylog(1/eps) = polylog(l)`, which is absorbed by raising the `o(k)`
  exponent by 1.
- `poly(n, s0) 2^{O(k)}` lies inside the excluded class.
- The integer solutions satisfy `z_i <= ||b||_inf`, because the columns are
  nonnegative and nonzero.

The corrected conclusion is stated consistently in Summary item 7,
Section 5.3 and Section 10 item 5: something beyond `poly(n, s0) 2^{O(k)}`
must enter, namely `2^{Omega(k log k)}`, `(n + s0)^{Omega(k)}`, or
conditioning. The Summary also carries the caveat that these statements
bound running time, not certificate size.

- **M7 (model of computation).** The new sentence says values come from "an
  oracle (real-RAM)". ETH is a statement about Turing machines. So the
  transfer covers algorithms that a Turing machine can simulate when
  objective values are supplied to polynomially many bits. `sin^2(pi y)` at
  rational `y` can be computed to `p` bits in time polynomial in `p`. It
  does not cover exact real-RAM algorithms as such. Suggested wording: "a
  Turing machine that queries objective values at rational points to a
  requested number of bits". Also, the status-table cell "excludes
  `poly(n, s0) 2^{O(k)}`, not conditioning-free bounds in general" reads
  ambiguously; "does not exclude conditioning-free bounds in general" is
  clearer.

## 7. Census shares

**Reproduced exactly.** `r1_census_recount.py` reads only the raw JSONL
records and the census metadata. Its counting code is my own. It gives:

- **Baseline.** `min(w_full, w_free) <= 12` for 86 of 582 instances
  (14.8%). Only casctanks moves to `k = 0` (`w_full = 11`, `w_free = 15`).
- **Tables.** The all-rows, linear-rows and linear-equality rows of the
  Section 7.3 tables match exactly. At `k <= 8`: 103 (17.7%), 101 (17.4%)
  and 99 (17.0%).
- **Classification values.**
  - Of the 17 instances gained at `k <= 8`, 14 have linear-only selections
    and 9 have linear-equality-only selections.
  - That gives 100 (17.2%) and 95 (16.3%).
  - With the old baseline of 85: 99 (17.0%) and 94 (16.2%), as stated.
  - The range "1.5–2.6 percentage points" matches.
- **Candidates.**
  - Any rows: 24 candidates, 19 open.
  - Linear rows, nonlinear width at most 12: 22 candidates, 17 open.
  - Linear equality rows: 18 candidates, 14 open.
  - The 17 open names match the note's list. powerflow0057r enters with
    `k = 14`.
  - With only linear rows eligible: kall_ellipsoids_tc03c needs 24 rows and
    tln12 needs 36; wastepaper6 does not reach width 12; powerflow0030r
    needs 3.
- **Gap class.** 294 instances. Bag-rule stop reasons: 82 reached width
  12, 121 hit the 64-row cap, 77 stopped early, 10 hit the time cap, and 4
  had no starting width. `census_k3.jsonl` covers all 98 instances with
  `1 <= k <= 64` under the fixed baseline; its 99th record is casctanks.

**Sample rerun.** `r2_census_sample.py` reruns the author's per-instance
functions (`census_k.work`, `census_k2.work`, `census_k3.work`) in one
process on 12 instances:
- the instances: casctanks, powerflow0030r, powerflow0057r, wastepaper6,
  tln12, kall_ellipsoids_tc03c, waterno1_03, sfacloc1_4_95,
  ann_cumene_tanh, waternd_pescara, waterno2_03 and kriging_peaks-full100;
- all 34 records are identical to the saved JSONL (timing ignored);
- for the rows removed by the bag rule, a separate raw-XML parse of the
  OSIL files gives the same linear-equality / linear-inequality / nonlinear
  labels as `census_k_rows.log`, on all 9 sampled instances listed there.

*Observation (not an error).* powerflow0057r shows that restricting the
eligible rows can **help** the greedy rule (17 rows unrestricted, 14 with
linear rows only). The docstring of `census_k3.py` says the opposite is
expected. The reruns cover only the 99 instances where the unrestricted
rules succeeded, so the linear-row shares may be slightly underestimated,
not overestimated. The note's caveat already limits the claim to those 99.

## 8. Provenance of the summary-log lines

**Confirmed.** `r0_reproduce.sh` reruns the scripts into a scratch
directory and diffs the output with the saved logs:

| Script rerun | Compared with | Result |
|---|---|---|
| `census_k_analyze.py` | `logs/census_k_summary.log` (130 lines) | identical |
| `census_k_rows.py` | `census_k_rows.log` | identical |
| `jeroslow_bb.py` | its log | identical |
| `jn_lifted_cert.py` | its log | identical |
| review's `c1_jeroslow.py`, `c2_min_tree.py` | the review's logs | identical |

The last row confirms Section 11's statement about the rerun of `c1` and
`c2`. So the F13 problem, three log lines printed by an unsaved script, is
fixed.

- **M8 (text numbers without a printing script).** Section 7.3 and Summary
  item 8 contain numbers that no saved script prints:
  - the open counts "17 open" (linear rows) and "14 open" (linear equality
    rows);
  - the list of 17 open candidates.

  The totals 22 and 18 can be read off the summary log (`100 - 78` and
  `96 - 78` in the `nlprimal<=12` rows). `r1` reproduces all of these
  numbers. For full provenance, `census_k_analyze.py` could print them.

## Suggested edits (all minor)

1. M2, M1: in Summary item 1 and the status table, replace "changes the
   constant" with "changes the prefactor (polynomially in `n` for rows with
   bounded entries)". Note that the factor is exact when the minimizer
   stays at 0.
2. M7: restate the computational model for Proposition 5.3(b) as a Turing
   machine with a bit-precision evaluation oracle. Reword the status-table
   cell.
3. M3: in Proposition 2.6(c), say "a global minimizer `x*` of (P)".
4. M4: Section 6.2 table, "Theorem 5.1(c)" → "(d)"; same in the docstring
   of `jn_lifted_cert.py`.
5. M5, M6: "0.61–0.65"; "`>= 1.729`"; "`3 <= n <= 7`"; the itemized count
   needs `n >= 2`.
6. M8: print the candidate open counts and names from
   `census_k_analyze.py`.
7. The header of the note still says the revision "has not been
   rechecked". That can now point to this report.

## Commands run

All from `research-20260929/reviews/coupling-recheck-checks/`, with
Python 3.13.11, NumPy 2.5.1 and SciPy 1.18.0. Everything ran
single-threaded (`OMP_NUM_THREADS=1`), and each run took under 10 seconds.

These are targeted checks of this note only. I ran no project-wide
verification and did not consult CI status or logs. My first reruns of the
author's scripts left a `__pycache__` directory in `theory-coupling/`; I
removed it. The saved scripts now avoid writing bytecode.

| Command | Log | Result |
|---|---|---|
| `bash r0_reproduce.sh` | `logs/r0_reproduce.log` | 6/6 reruns identical to saved logs (census summary, row classes, Jeroslow B&B, `J_n` certificate, review `c1`, `c2`) |
| `python3 r1_census_recount.py` | `logs/r1_census_recount.log` | all census shares, candidate counts (24/19, 22/17, 18/14) and stop reasons reproduced by independent code |
| `python3 r2_census_sample.py` | `logs/r2_census_sample.log` | 34/34 rerun records identical; raw-XML row classes agree on 9/9 |
| `python3 r3_jn_certificate.py` | `logs/r3_jn_certificate.log` | (CM), (LC), root `l_r = 1/4`, size `3n^2 - 3n + 2` exact for odd `n <= 29`; LP: side 1 gives 0, side 1/2 gives 1/4 |
| `python3 r4_constants.py` | `logs/r4_constants.log` | determinant factor and lower estimate; `Gamma_sigma` (0 failures in 200,000 draws); Prop. 5.2 bases |
| WebFetch arXiv 1811.01296 | — | KPW statement confirmed |
