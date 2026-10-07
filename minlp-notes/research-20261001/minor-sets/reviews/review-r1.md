# Review r1 of the minor-sets note

Reviewer: independent research agent (second reviewer of round 1; the first was interrupted by a
usage limit). Date: 2026-10-02. Object: [`../note.md`](../note.md) (dated 2026-10-01), the code in
[`../code/`](../code/), the logs in [`../logs/`](../logs/) and the author summary in
`../../.coordination/minor-sets-author.json`. "Reviewed" means checked by another research agent,
not journal peer review.

**Verdict: minor fixes.** I found no major issue. I checked every proof and found them correct
under their stated hypotheses. Every certificate I re-ran reproduces, and my own independent code
confirms the main numbers. The SCIP source claims match the source. Five minor issues remain:
- the process-hygiene statement that the task requires is missing from the note;
- the headline "with larger gaps" and the comparison with the bilinear search in Section 7.3 are
  not supported as stated;
- the summary drops a hypothesis of Proposition 5;
- the LP re-solve comparisons are reported without uncertainty;
- Proposition 1, labelled proved, also covers `nlhdlr_quadratic`, which rests on untested source
  reading.

Each needs only a small text change. There are also some optional items.

My code is in [`r1-code/`](r1-code/) and its outputs in [`r1-logs/`](r1-logs/). The first reviewer
left `r1-code/indep_exact.py` and `r1-code/indep_families.py`. I read both, confirmed that they do
not import the stream's code, and re-ran them before using their results. The scripts
`rev_random.py`, `rev_orbit.py`, `rev_symbolic.py` and `rev_lpstats.py` are mine.

## 1. Proofs, line by line

- **Section 2 (SCIP source).** I checked every statement against `sepa_interminor.c`,
  `nlhdlr_quadratic.c` and `sepa_minor.c` of SCIP 10.0.3. The sha256 checksums match the manifest.
  - `SEPA_FREQ -1`, `maxrounds 10`, `maxroundsroot -1`, `mincutviol 1e-4`, `MAXNMINORS 100000`.
  - The `SCIPisIpoptAvailableIpopt()` early return comes with hard-coded eigenvectors and
    eigenvalues `±1/2`, and the vars order is `(xik, xjl, xil, xjk)`.
  - The column swap for `det < 0` is the call `separateDeterminant(xil, xik, xjl, xjk)`.
  - `usebounds` acts only when a diagonal entry has a negative LP value.
  - The `TODO` comment about storing minors twice is there, and principal and one-diagonal minors
    are included.
  - In `nlhdlr_quadratic`, a constraint root has `auxvar = NULL`, so `x1x4 − x2x3 = 0` is Case 1.
- **Proposition 1.** The coordinates `x̂, ŷ`, `det = |x̂|² − |ŷ|²`, the PSD criterion, the formula
  for `x_1(R_φ^T M)`, and the rotation acting isometrically on `ŷ` are all correct. Polar
  uniqueness gives `R_φ = U`. BCM (14a) and (17a) match the downloaded text (arXiv v7, Lemma 22 and
  Lemma 24). The `det < 0` case is correct: `(WΠ)(Π^T P Π)` is the polar decomposition of `M̄Π`.
  The identities are also confirmed symbolically (`rev_symbolic.py`, part 1). SCIP's eigenvector
  coordinates equal `√2 (x_1, x_2, y_1, y_2)`.
- **Lemma 2.**
  - (1) is correct.
  - (2): the step from an interior point of `cone(C)` to an interior point of `C` is the usual
    argument via `M̄ ∈ int C`, which is BCM Lemma 14.
  - (3) is correct.
  - The MPS description matches arXiv:2211.05185: `D_d` is the unit sphere, so for `m = n = 2`,
    `Γ : S^1 → S^1`. The non-expansive and convex-hull conditions are Theorem 1.2.
- **Proposition 3.**
  - (2) is checked symbolically. `F'^T(AMB^T) = B(F^T M)B^T` is a congruence; transposition gives
    `F^{-1}`.
  - (1): `C_F = (F·PSD)^*`, and `G·PSD = PSD` forces `G = cI`, `c > 0`.
  - Maximality of `C_I` follows from BCM Theorem 23(iv) because the four entries are distinct. A
    maximal cylinder in `S^{n×n}` gives a maximal S-free set in `R^4`.
  - (3) holds, including the transposition case: `F^T M̄^T = P'` implies
    `F^{-T} M̄ = F^{-T} P' F^{-1}`.
  - (4): `ρR^T` with `ρ < 0` also gives `C_U`, because `F^T = |ρ|(−R)^T` and `−R = U`.
  - (5) is a restatement.
- **Proposition 4.** Correct. A set with `sym(F^T M̄) ≻ 0` automatically has `det F > 0`, so the
  LMI family is exactly the orbit family.
- **Proposition 5.**
  - The use of sfree Theorem 4 with `q = det`, `S_≤ = {det ≤ 0}` and `ρ = 2 + 0 + 1 = 3` is
    legitimate. By Lemma 2(3) the minimizers for `S` and `S_≤` coincide.
  - The signature argument holds: `H = span{t*, u}` is of type (1,1),
    `T = span{t*} ⊕ H^⊥`, and the radical is `span{t*}`.
  - The conclusion `s̄ ∈ span P_J` is also right.
  - (2) is correct, including the case without LICQ.
  - The proposition is stated with the hypothesis "`P_J` injective"; see minor issue 3 for the
    summary.
- **Lemma 6.** All identities are checked symbolically for general `a_0, b_0, D`:
  `adj(ab^T) = (Jb)(Ja)^T`, `adj(D) = J^T D^T J`, `G_1 a_0 = 0`,
  `(Jb_0)^T G_0 a_0 = tr(adj(M_0)D)`, `det(G_0 + κG_1) = det D + κ tr(adj(M_0)D)`, and
  `J adj(D + κM_0) = G_0 + κG_1`. The rest of the argument also checks out: PSD with a zero
  diagonal value gives `Yu = 0`, and the sign is fixed by `c > 0`.
- **Corollary 7.** Correct. The sfree family (A) is `{C_F ∩ H : det F > 0}` (sfree Lemma 10 and
  §8.1). The apex of sfree Theorem 14 has `q(s̄) = 3/2 > 0`, so the embedded apex has `det > 0`.
  Re-run: `embed_check.log` gives 0.97539, 0.83477, 0.98385.
- **Theorem 8.**
  - (1)–(3) are certified in exact arithmetic. The face enumeration in
    `exact_tools.min_det_over_simplex` skips singular faces. This is sound for the minimum value,
    because the face minimum is then attained on a lower face. It is also sound for uniqueness: a
    continuum of minimizers would show up as at least two boundary points. In the independent run
    no face of A, B or S1 is singular.
  - The small `z = 1` certificate printed in the note is exact. I checked `Σ_V V Y_V = 0` and that
    each `Y_V` is positive definite (`rev_symbolic.py`, part 5).
  - (4), robustness: the dual certificate has full row rank 4, and lower semicontinuity of `z_K`
    is all that is needed. Correct.
  - The appeal to sfree Theorem 1(4) is valid: `∇det(t*)·(s̄ − t*) = ∇det(t*)·s̄ = 6 > 0`.
- **Theorem 9.** Exact checks reproduce. The independent run gives `ν = (0, 1/36, 2/9, 1/9)`,
  edge products `9/2, 1/8, 1, 1/2` and cosines `0.088, 0.011, 0.037, 0.017`. The largest
  denominator in the `z = 1` certificate is `216000`.
- **Proposition 10.** Correct. Rank-one `ab^T ∈ C_F` iff `F^T a ∈ R_+ b`. In the SCIP case,
  `U^T s̄` symmetric forces `U^T p_j` symmetric, a single linear condition. The paragraph after it
  is labelled heuristic, which is appropriate.
- **Proposition 11.** All four steps are checked symbolically in `δ`:
  - `C_I` gives `(2√δ, 1, 1, 2/√δ)`;
  - `C_diag(1,1/δ)` gives `(2, 1, 1, 2)`;
  - the formula for `det(s̄ + Pλ)` is correct;
  - the BCM bound `((16 + 2√73)/3)√δ ≈ 11.03√δ` is valid.

  A dense BCM scan (200001 angles) for `δ = 2.5·10^-1 … 2.5·10^-8` gives at most `3.99√δ`, so the
  bound holds and "numerically ≈ 4√δ" is accurate.
- **Section 8.** Correct for `S = {det = 0}`:
  - principal minors with `det M̄ > 0`: the PSD (or NSD) cone is the unique maximal set;
  - `det M̄ < 0`: signature (2,1), sfree Theorem 8(1);
  - one diagonal entry: the closure of the projection is `{det = 0, a ≥ 0}`, verified by hand;
  - BCM Theorem 23 and Theorem 27 match the text.

## 2. Reproduction and independent computations

All targeted; no project-wide checks, no CI. Commands are listed in Section 5.

- **Exact certificates re-run.** The logs are identical to `certify_cex_A.log`,
  `certify_cex_B.log` and `certify_supp1_full.log`, apart from cvxpy warnings, which the note says
  were filtered. All end with ALL PASS.
- **Independent exact check of A, B, S1** (`indep_exact.py`, re-run):
  - its own face enumeration finds `min det = 0`, attained only at `t*`;
  - its own KKT multipliers and `κ`-intervals equal the note's;
  - the authors' dual certificates at `9/20`, `461/500` and `779/1000` are re-verified;
  - its own SDP without preconditioning gives orbit bounds 0.4495356, 0.9219494 and 0.7781084,
    each inside the note's exact bracket;
  - its own rational primal and dual certificates bracket each value to `±3·10^-6`;
  - SCIP's value, computed both from `C_U` and from the literal C formula in 60 digits, gives
    0.1358003, 0.3250185 and 0.3121418.
- **Independent point rule and BCM** (`indep_families.py`, re-run):
  - point rule: 0.1975642, 0.3634910 and 0.4542878, each inside the note's bracket;
  - BCM grid scan: 0.3172918, 0.6528296 and 0.4855194, at or slightly below the brackets, as a
    grid must be;
  - Proposition 11: SCIP gives `2√δ`, `C_diag` gives 1, BCM gives about `4√δ`.
- **Random corners, all 900** (`rev_random.py`, my code). For each corner I regenerated it from
  `(seed, idx)` and computed `z_K` by my own method: direction search over supports 1 and 2 plus
  20000 random directions of the full simplex.
  - The largest relative difference from the logged `z_K` is `9.7·10^-14`, and no random
    direction beats it.
  - Supports agree in all 900 corners, and the 5 records with infinite `z_K` are confirmed
    infinite.
  - SCIP's ratio from the literal `sepa_interminor.c` formula agrees with the log to
    `4·10^-13`.
  - Every count, mean, median, 10% quantile, minimum and miss ratio in the table of Section 7.1
    reproduces from the jsonl files.
- **Family ratios on random corners** (`rev_orbit.py`, my code). I took 25 random "attained"
  corners per log plus all 12 orbit misses, and solved my own LMI bisection without
  preconditioning, my own point-rule parametrization `F^T = P M̄^{-1}`, and a BCM scan with 20000
  angles.
  - On all 87 corners my values agree with the logged ratios to `3.4·10^-7` (orbit and point
    rule) and `2.5·10^-13` (BCM).
  - I re-certified each of the 12 misses with my own exact code, after rounding the rays (divided
    by `w_j`) to denominator `10^6` as the note does. For `z_K ≥ z_lo` I used my own face
    enumeration over all affinely independent vertex subsets, and for `z_orbit ≤ z_up` my own
    rational dual certificate.
  - Every exact ratio bound is below 1: 0.774654 for the worst miss, and at most 0.999953 for
    all 12.
- **LP corners** (`exp_lp.py 31 25 3 3 3`, the first 25 trials of the logged 3×3 run, same seed).
  The 10 corners produced are bit-for-bit identical to the logged records in `z_K`, the gap, all
  ratios and all LP re-solve fractions.
- **SCIP fidelity smoke test** (`scip_fidelity.py 1 5`): 19 of 19 applied cuts matched, largest
  coefficient difference `1.7·10^-16`. This agrees with the note.
- **Adversarial corners** (`rev_symbolic.py`, part 6). I recomputed the margins of the logged
  float corners and of the corners rounded to denominator `10^4`, which are the ones actually
  certified.
  - Rounded corners: every margin is at least 0.01001 for the 1% runs and 0.05008 for the 5% runs.
  - The active margins are the ones the note names: ray grazing in the two best runs, apex margin
    in the two 5% runs.
  - The ten 1% runs end with minimum margins between 0.01001 and 0.01087.
- **Search logs (Section 7.4).**
  - `search_cex`: 1487 valid corners (355 + 357 + 393 + 382) and 354 with disjoint intervals.
    Orbit ratios have minimum 0.4495 and 10/50/90% quantiles 0.890, 0.988 and 0.9998; 13 are at
    least 0.99999.
  - `search_supp1`: 717 valid, 89 misses, worst 0.7781.

  All as stated.
- **Literature locators.**
  - BCM (downloaded text): (14a), (14b), (17a), Lemma 14, Theorem 15, Corollary 16, Lemma 22,
    Theorem 23(i)–(viii), Lemma 24 and its remark ("best in a violation sense, and may not
    translate to finding the deepest cut"), and Theorem 27 all match.
  - Chmiela–Muñoz–Serrano, ZIB 20-29: §3.1 says "exactly one of the maximal outer-product-free
    sets constructed by Bienstock et al.", 587 instances, 8% (12% on affected instances), and
    "non-negligible". All match.
  - MPS Theorems 1.1–1.2 match.
  - MPS cites Muñoz–Serrano Theorem 2.1 for the maximality of a homogeneous set.
- **Background processes.** No process of the stream was running at review time. I checked the
  working directories of all python processes. All of my own jobs have finished.

## 3. Issues

### Major

None.

### Minor

1. **Process-hygiene statement missing.** The task rules require every long computation to have
   an explicit wall-clock limit and checkpoints. They also require the note to say that every
   background process has finished or been killed. The note says nothing about processes, limits
   or checkpoints, and the commands in Section 10 carry no `timeout`. In fact:
   - the jsonl outputs are flushed per record;
   - `single_minor_bound` and `test_core.py` use a 60 s SCIP limit;
   - the searches have fixed trial counts and Nelder–Mead has `maxiter`;
   - I found no stray stream process.

   Fix: add this statement to Section 10 or 11.
2. **"With larger gaps" and the comparison with the bilinear search are not supported as
   stated.**
   - The Summary ("Answer: yes, and with larger gaps") and the author summary ("the gaps are
     larger than in the bilinear case") present this as a general finding.
   - Section 7.3 says that the minor corners "reach lower ratios under comparable margins" than
     the sfree search, which "reached 0.45 with rays 1% from grazing".
   - But the sfree note (§8.6) also reports a family-(A) ratio of 0.028 with rays 1% from grazing,
     when the vertex is nearly on `∂S`. Its 0.4526 instance had a vertex violation
     `q(s̄)/max|P|² ≈ 9·10^-4`.
   - The minor search used different margin definitions, including an apex margin that the sfree
     search did not impose. So the margins are not comparable.
   - By Corollary 7 every bilinear corner is a lower-dimensional minor corner, so the minor worst
     case is automatically at least as bad as the bilinear one.
   - What is established is narrower. The certified full-dimensional minor instances (0.45, 0.78)
     have larger gaps than the certified bilinear instances (0.975, 0.984). Section 9 says exactly
     this.

   Fix: qualify the headline as "larger certified gaps". In Section 7.3, mention both sfree
   numbers and the different margin definitions, or drop the comparative sentence.
3. **Summary item 4 drops the hypothesis of Proposition 5.**
   - The summary says: "If the LP value of the minor lies in the span of no three projected rays,
     every corner minimizer has support at most two, and support two means a tangent edge."
   - Proposition 5 only covers minimizers whose support `J` has `P_J` injective.
   - Without that hypothesis the summary statement is false in degenerate cases. Take a corner
     whose minimizer `λ*` has support `{1, 2}` on a tangent edge, and add a duplicate ray
     `p_3 = p_1` with `w_3 = w_1`.
     - Then `λ' = (λ*_1/2) e_1 + λ*_2 e_2 + (λ*_1/2) e_3` is also a minimizer, with the same point
       and cost, and its support has three rays.
     - For generic data `s̄` still lies in the span of no three rays: `span{p_1, p_2, p_3}` has
       dimension 2, and the other spans of three rays have dimension 3.
   - Parallel projected rays are common at LP corners, although equal cost ratios are not.

   Fix: say "every minimizer whose projected rays are linearly independent (and one always
   exists)".
4. **LP re-solve comparisons without uncertainty** (Section 7.2, Summary item 6, author
   solver-relevance text). The note reports mean differences and better/worse counts, with no
   interval or test. I computed paired statistics from the logged jsonl files (`rev_lpstats.py`;
   10000 bootstrap resamples; exact sign test on `|difference| > 0.01`):

   | Comparison | Program size | Mean difference | 95% bootstrap CI | Better/worse | Sign test p |
   | --- | --- | --- | --- | --- | --- |
   | orbit nearest to SCIP minus SCIP | 3×3 | +0.0225 | [+0.002, +0.045] | 30/16 | 0.054 |
   | orbit nearest to SCIP minus SCIP | 4×4 | +0.0057 | [−0.020, +0.029] | 30/10 | 0.002 |
   | max-margin orbit minus SCIP | 3×3 | −0.076 | [−0.117, −0.037] | 22/42 | 0.017 |
   | max-margin orbit minus SCIP | 4×4 | −0.065 | [−0.107, −0.026] | 29/33 | 0.70 |

   So the claim that the nearest-to-SCIP set "closes slightly more (by 0.006–0.022 on average)" is
   not established in mean for 4×4. The claim that the max-margin set closes "clearly less" holds
   in mean but not in the sign count for 4×4.

   The note's conclusions are already hedged ("looks worth testing", "not evidence of a
   solver-level benefit"). Fix: add the intervals or tests and adjust the wording.
5. **Proposition 1 bundles a source-reading claim into a "proved" statement.** The proof covers
   SCIP's formula. That `nlhdlr_quadratic` applies the same set to an explicit constraint
   `x_1x_4 − x_2x_3 = 0` rests on reading the source, and was not tested. The author summary says
   "not tested", but the note does not. I confirmed the source reading: for a constraint root
   `auxvar = NULL`, and the constraint is Case 1. Fix: in Section 2 and Proposition 1, label the
   `nlhdlr_quadratic` part "source reading, not tested".

### Optional

1. Several code docstrings use stale theorem numbers:
   - `minor_core.py`: "Lemma 1", "Prop. 3", "Lemma 5";
   - `certify_cex.py`: "Theorem 7", "Lemma 5";
   - `certify_supp1_full.py`: "Theorem 8";
   - `scaling_example.py`: "Proposition 9";
   - `embed_check.py`: "Corollary 6";
   - `test_core.py`: "Prop. 2";
   - `cert_lib.py`: "Thm 7(c)".
2. The `certify_ratio.py` docstring promises to report "the minimum non-degeneracy margin of the
   rounded corner", but the script does not. The note could state that the rounded, certified
   corners keep all margins at or above 1% (respectively 5%). I verified this (Section 2).
3. Scope wording. The Summary says "a minor with four distinct entries", and §1 says "four distinct
   variables". A minor with one diagonal entry also has four distinct entries, but its implied set
   is `{det = 0, a ≥ 0}` (§8). Use "four distinct indices (no diagonal entry)" where `S = {det = 0}`
   is meant.
4. Section 8, last part of the first bullet. For an NSD `A` of rank 2, `⟨A, X⟩ ≤ 0` is a
   nonnegative combination of two inequalities `g^T X g ≥ 0`, not one. Also, `sepa_minor` builds
   its cuts from eigenvectors of the 3×3 augmented matrix, so it does not necessarily separate
   this particular inequality. Suggested wording: "implied by inequalities of the type …".
5. In the re-run of instance A, `FamilySolver` prints a "bisection upper" value of 0.4495353,
   below the certified lower value 0.4495357. The note correctly relies only on exact
   certificates. It could say once that the bisection upper value is not a bound.
6. Section 9 says "Theorem 2.1 of their homogeneous paper". The reference is Muñoz–Serrano, "Maximal
   quadratic-free sets" (Math. Program. 192), Theorem 2.1, which proves a homogeneous set
   maximal. "Their homogeneous paper" reads as if it were a separate paper.

## 4. Assessment of the main claims

| Claim (note) | Label in note | Review finding |
| --- | --- | --- |
| SCIP's minor set is `C_U` (Prop 1); only `sepa_interminor`, off by default, needs Ipopt | proved / source + run | Correct; source and probe verified; fidelity smoke test reproduced (19/19). `nlhdlr_quadratic` part is source reading (minor 5) |
| Orbit, point-rule and BCM families (Lemma 2, Prop 3) | proved | Correct |
| Bisection and certificates (Prop 4) | proved | Correct |
| Support at most 3, and 3 only if `s̄ ∈ span P_J`; support 2 means a tangent edge (Prop 5) | proved | Correct with the `P_J`-injective hypothesis; summary omits it (minor 3) |
| Homogeneous pencil (Lemma 6) | proved | Correct (symbolic check) |
| Bilinear counterexamples embed (Cor 7) | proved, computed | Correct, reproduced |
| Instance A: `z_K = 1`, orbit in [0.4495347, 0.4495363], tangent edge (Thm 8) | computed exactly | Reproduced and independently confirmed |
| Instance S1: support one, orbit at most 0.779 (Thm 9) | computed exactly | Reproduced and independently confirmed |
| Contact cone (Prop 10) | proved | Correct |
| Scale dependence of SCIP's set (Prop 11) | proved | Correct (symbolic and numerical) |
| Random corners (Section 7.1) | numerical (12 misses certified) | Reproduced independently; misses re-certified with my own code |
| LP corners (Section 7.2) | numerical | Partial rerun identical; comparisons need uncertainty (minor 4) |
| Adversarial 0.200 at 1% margins (Section 7.3) | numerical, certified after rounding | Certificates and margins confirmed; comparison with sfree not supported (minor 2) |
| Principal minors: SCIP attains `z_K` (Section 8) | proved | Correct for `S = {det = 0}` |
| Novelty | qualified | Appropriately hedged (small search, stated) |
| Solver relevance | low, negative | Fair; conclusions do not overstate |

## 5. Checks actually run (by this reviewer)

All commands were run from `research-20261001/minor-sets/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`, under `timeout`, at most 4 processes at a time. They
are targeted checks only; CI was not consulted.

| Command | Outcome (log in `reviews/r1-logs/`) |
| --- | --- |
| `cd code; timeout 1200 python3 certify_cex.py` | `rerun_certify_cex_A.log`: ALL PASS; identical to `logs/certify_cex_A.log` apart from cvxpy warnings |
| `cd code; timeout 1200 python3 certify_cex.py "<instance B JSON from logs/certify_cex_B.log>"` | `rerun_certify_cex_B.log`: ALL PASS; identical apart from warnings |
| `cd code; timeout 1200 python3 certify_supp1_full.py` | `rerun_certify_supp1_full.log`: ALL PASS; identical apart from warnings |
| `cd reviews/r1-code; timeout 1500 python3 indep_exact.py ../../logs` | `indep_exact.log`: as in Section 2 (first reviewer's script, read and re-run) |
| `cd reviews/r1-code; timeout 1500 python3 indep_families.py` | `indep_families.log`: as in Section 2 (first reviewer's script, read and re-run) |
| `cd reviews/r1-code; timeout 1800 python3 rev_random.py ../../logs` | `rev_random.log`: all 900 corners agree (`z_K` to `1e-13`, supports, SCIP ratios to `4e-13`); all Section 7.1 statistics reproduce |
| `cd reviews/r1-code; timeout 3000 python3 rev_orbit.py ../../logs 25` | `rev_orbit.log`: 87 corners (75 sampled plus 12 misses); orbit, point rule and BCM agree with the logs (largest difference `3.4e-7`); all 12 misses re-certified exactly (largest ratio bound 0.999953, worst miss 0.774654) |
| `cd reviews/r1-code; timeout 1500 python3 rev_symbolic.py ../../logs` | `rev_symbolic.log`: ALL PASS (Props 1, 3(2), Lemma 6, Prop 11, Thm 8 small certificate); adversarial margins as in Section 2 |
| `python3 reviews/r1-code/rev_lpstats.py logs` | `rev_lpstats.log`: the paired statistics in minor issue 4 |
| `cd code; timeout 900 python3 scip_fidelity.py 1 5` | `rerun_scip_fidelity_smoke.log`: 19 of 19 applied cuts matched |
| `cd code; timeout 2400 python3 exp_lp.py 31 25 3 3 3 ../reviews/r1-logs/rerun_exp_lp_3x3_first25.jsonl` | 10 corners, bit-for-bit identical to the first 10 records of `logs/exp_lp_3x3.jsonl` |
| Inline Python over `logs/search_cex_*.log` and `logs/search_supp1_7.log` | 354 records, minimum 0.4495, quantiles 0.890 / 0.988 / 0.9998, 13 at least 0.99999; 717 valid, 89 misses, worst 0.7781 |
| `sha256sum` of the three SCIP source files and the two BCM source files | match the manifest |
| `grep`/`sed` over SCIP sources, BCM text, Chmiela text, MPS text | as in Sections 1–2 |
| Process check (`/proc/*/cwd` of python processes) | no stream process left; my own jobs finished |

Not run: the full `exp_random.py`, `exp_lp.py` (all trials), `adversarial.py`, `search_*.py`,
`verify_misses.py` and `certify_ratio.py`. Their outputs were checked through the independent
recomputations and log analyses above. `scip_probe.py` was not re-run; I checked its log against
the source instead.
