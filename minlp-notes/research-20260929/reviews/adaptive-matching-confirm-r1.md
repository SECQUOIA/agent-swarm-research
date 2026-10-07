# Confirmation review, round 1: `theory-decomposition/adaptive-matching.md`

Date: 2026-09-30. Independent referee; I did not write the note or the
round-1 review. I checked whether the revision fixes the nine points of
[`adaptive-matching-review.md`](adaptive-matching-review.md), redid every
changed number, and looked for claims that the revision made stronger. My
scripts and logs are in
[`adaptive-matching-confirm-r1-checks/`](adaptive-matching-confirm-r1-checks/).
Only targeted checks were run. No project-wide verification was run and no
CI results were consulted.

Labels. **By hand**: I redid the argument. **Float**: double-precision
computation, not certified. **Reproduced**: I reran the authors' script and
got output identical to the logged output. Nothing was checked in exact
arithmetic or in Lean.

## 1. Verdict

All nine review points are fixed. Every changed number that I recomputed
is correct. Lemma 1, Theorem 2 for paths and Proposition 6 are unchanged, as
the note says. I found no claim that the revision made stronger. The
reviser's two corrections of the review are right: the review's arXiv
number for Shin–Anitescu–Zavala is wrong, and its `k^4` order for
`1/theta*` fails when `w kappa < 1`.

Three small problems remain:

1. **Wrong page numbers for Shin–Anitescu–Zavala.** The note gives SIAM
   J. Optim. 32(2) (2022) **1110–1136** in Section 9 (line 1375) and in
   Revision item 4 (line 1597), and says the bibliographic data were
   checked. Crossref, for DOI `10.1137/21M1391079`, gives **1156–1183**
   (`crossref.log`). The title, authors, volume, issue, year and arXiv
   number 2101.03067 are correct. Fix the pages and add the DOI.
2. **Proposition 6 is stated more broadly than it is proved.** Summary
   item 4 (line 143) says the discount "costs `sqrt(n)` per separator
   dimension per halving" and attributes this to "the proof". Section 5
   item 2 (line 800) says "costs `sqrt(n)` per separator dimension (proved
   for rule `bd`)". Proposition 6 is proved only for a quadratic path with
   one-dimensional separators. Higher separator dimensions are an
   extrapolation, plausible but not proved. Suggested wording: "costs
   `sqrt(n)` per edge per halving (proved for rule `bd` on a quadratic path
   with one-dimensional separators; per separator dimension in general is a
   conjecture)". The new *Scope* paragraph should also say that the
   separators are one-dimensional.
3. **Two restatements of Theorem 2 still omit (S).** Summary item 5
   (line 152) says "Theorem 2 makes it algorithmic on paths", and the
   status-table row for Theorem 2 (line 220) says "proved (paths)". The
   other restatements now name (S), and Section 7 does too ("for path
   decompositions with (S)"). Add "with (S)" or "under `∇F(x*) = 0`" in
   both places.

None of the three affects a proof or a computation. Verdict:
**fixes_needed** (minor; text-only fixes).

## 2. The review points, one by one

| # | Review point | What the note does now | My check | Status |
|---|---|---|---|---|
| 1a | Tree slope bound "at most `k-1` bags" is false | Remark 3.3 gives the counterexample and the coordinatewise bound `nu_t <= (k-1) M_a sqrt(w(w+1)) \|x-x*\|_inf`, so `gamma_T(K) = 2(k-1) sqrt(w(w+1)) K` | By hand against Lemma 3.2 of [D]: `lambda_{t,i}` sums over `sub(t) ∩ T_i`, which has at most `k-1` bags because `p(t)` is in `T_i` but not in `sub(t)`. The 2-norm over at most `w` coordinates gives `sqrt(w)`. A script check of the counterexample (`my_constants.log`): every `T_i` is connected, `k = 3`, `w = 2`, all three bags of `sub(t)` meet `S_t`, and each coordinate of `S_t` gets only 2 = `k-1` bags. Stage 0 needs `K_T >= 1/2`, which is right. | fixed |
| 1b | Theorem 2's induction needs a fixed point | (Loc_T) is stated. Sufficient growth condition `K_1 <= A_0 + A_1 sqrt(gamma) + A_2 theta gamma` with `theta_T = min(theta_0, 1/(2 A_2 c_T))`, `K_T = max(1/2, 4A_0, 16 A_1^2 c_T)`. The counterexample `K_1 = 1 + gamma`. "Exactly" softened to "sufficient, not shown necessary" | By hand: the three terms are at most `K_T/4`, `K_T/4` and `K_T/2`. Float: no violation in 10^5 random parameter sets. `K_1 = 1 + gamma` has no fixed point because `c_T >= 2 sqrt(2) > 1`. On paths `K_1(gamma(K*), theta*)/K* = 0.7906`, and at most 0.7907 on a grid of `(k, w, kappa, a)`. The parts of `K_1^2/K*^2` are within their bounds 3/8, 3/8 and 1/4 everywhere on the grid. | fixed |
| 1c | (found by the reviser) Section 6 sketch for `L` leaves | The old `(C sqrt L)^{w+1}` and its "interpolation" reading are withdrawn. With the fixed point the sketch now gives `K_T = O(L)`, `theta_T` of order `1/sqrt L`, and a base of order `L` | By hand: if `eta^2` shrinks by a factor `L+1`, then `K^2 >= (L+1) C (Q_0 + c K)` gives `K = Theta(L)`. The `theta^2 gamma^2` term forces `theta` of order `1/sqrt L`. The correction is right, and the result is still labelled a sketch. | correct and weaker than before |
| 2 | Conditioning comparisons used infinite-size bounds | Size-dependent `c_g` brackets are given. "Similar conditioning", "too-large `theta` rather than branching", "chain length alone" and the branching reading of 3.4 → 4.9 are withdrawn. Four new runs hold the conditioning fixed | Float, own code (`my_cg.py`): every lower bound and every coupling `b` agrees to 4 decimals. My upper bounds come from my own projected-gradient search over feasible points. They are within 0.004 of the note's, and every conclusion in the note survives with either set. Reproduced: the fixed-conditioning tree runs (`m = 7, 15`) and the path runs (`n = 8` at 0.035; `n = 16` at 0.073) give identical logs apart from timing. I read every quoted entry against the logs: zloc sequences, stop stages, sizes, gap constants (6.1, 5.9, 26–29, 20–27) and local constants (0.44 → 0.27; paths 0.22–0.24 and 0.16–0.19). All match. | fixed |
| 3 | Heuristics unlabelled; heading; scope of Proposition 6 | Labels added in Summary item 4, Section 5 item 1 and "Bag errors"; heading changed; *Scope* paragraph added | The labels are there. The *Scope* paragraph agrees with Theorem 1 of [Cov]: `theta_e = (2E_e+1)/(2n)`, `psi = U - theta w`, and the `w_e/(2n)` sliver. The "per separator dimension" wording remains (problem 2 above). | fixed except problem 2 |
| 4 | Missing precursors; novelty claim | Shin–Anitescu–Zavala, DDDP, Luus and Munos–Moore added with access levels. The novelty claim is limited to the localization lemma, the certified count and Proposition 6, with a caveat that the search was short | arXiv:2101.03067 is the right paper. arXiv:2101.06350 is the Shin–Zavala paper, as the note says. Crossref confirms DDDP (WRR 7(2):273–282, 1971) and Munos–Moore (Mach. Learn. 49:291–323, 2002). Crossref's record for Luus is the 2019 Chapman & Hall/CRC digital release, which is consistent with a 2000 first edition. The SIAM pages are wrong (problem 1 above). | fixed except problem 1 |
| 5 | Scope: (S), path, quadratic base, numbers | Summary item 1, Significance and Section 3.2 state (S), the path restriction, and `K* = Theta(k^5 w^2 kappa^2)`; they quote `theta* ≈ 8.2e-8`, `K* ≈ 7.3e8` and base `≈ 8.8e9`. "Closes the gap" is removed. Boundary runs are reported as suggestive only | Float, own code (`my_constants.py`): `theta* = 8.188e-8 = 2^-23.54`, `K* = 7.266e8`, base `8.768e9`. Exponents in `K*`: `k` 4.98, `kappa` 2.00, `w` 1.98. By hand, the third term of `K*` is `Theta(k^5 w^2 kappa^2)` and dominates the others because `k kappa >= 2`. `probe_boundary.log` agrees with the review's `boundary_test`/`face_test` logs (zloc at most 0.645 and 3.183; stop stages 7, 8, 11, 12). Two restatements still omit (S) (problem 3 above). | fixed except problem 3 |
| 6 | Corollary 3: enforce the budget during refinement | Checked before each split, with an abort; the proof explains the overshoot; stage cap tightened to `j* <= lambda_eps + ceil((1/2) log2(C_term N))` | By hand: the bound follows from `ceil(x+y) <= ceil(x) + ceil(y)` and `lambda_eps >= 0`, so `j* <= lambda_eps + r* - 1`. Float: no violation in 2·10^5 random cases. `sum_{r<=R} r 2^r <= 2R 2^R` holds (checked to `R = 60`). The run with `mu*` is never aborted because `B* <= 2^{r*}`. The fallback bound of `2^r/N + 1` stages is right, because the leaf that contains each copy has width at least `W_j` and is split. | fixed |
| 7 | Corollary 4: "explains" | Now "is consistent with ... but does not explain their size"; gives `K_1(0,0) ≈ 1.8e6` and `K_LS ≈ 1.4e8` | Float, own code using the closed form of the quadratic fixed point instead of the authors' bisection: `K_1(0,0) = 1.763e6`, `K_LS = 1.363e8`. | fixed |
| 8 | `check_tree_dp.py` check (2) is weak | Check (2) is now described as weak. Check (3) recomputes the relaxed `Phi` of the configuration and tests its constraints. `dp_min` also returns the leaf and cell indices | Reproduced: rerunning `check_tree_dp.py` gives a log identical to `logs/check_tree_dp.log` (`\|Phi - l_r\| <= 8.9e-16`, 0 violations). I read the code: the only change to `dp_min` is that it records `leaf`/`cell`. Running the current `tree_gr.py` reproduces the fixed-conditioning tree runs that used the version before the change, so the computation did not change. | fixed |
| 9 | Minor points | 3.1–5.7; "stop stage"; LS ratios 8/6/3; order of `1/theta*` | From the log: zloc from stage 3 on ranges from 3.118 (`n=8`, seed 0, stage 7) to 5.728 (`n=16`, seed 1, stage 8). LS at `n = 64`, last pass: 8 at sublevel 4, 6 at sublevels 5–10, 3 at sublevels 11–13. Float: `1/theta*` divided by `k^4 w kappa (1 + sqrt(w kappa))` stays between 1.0e3 and 1.2e3 for `kappa = 2/k`, `k = 8, 32, 128`. The same quantity divided by the review's `k^4 w^{1.5} kappa^{1.5}` grows like `sqrt(k)` (3.6e3, 5.2e3, 1.0e4). So the note's order is right and the review's is too small when `w kappa < 1`. | fixed |

## 3. Checked for statements made stronger

I found none. All the new statements are either weaker than in the first
version or labelled:

- the tree sketch (now base `O(L)`);
- the conditioning reading ("does not separate size, conditioning, `k` and
  branching"; "neither support nor refute Conjecture 7");
- Corollary 4 ("consistent with");
- novelty (precursors named, search described as short).

Two new comparisons go beyond the data only mildly, and both carry
caveats:

- "The tree family needs a smaller `theta` than the path family at
  comparable conditioning". The `b = 0.8` path at `n = 256` has the smaller
  `c_g` and keeps ratio 3. The `c_g >= 0.141` trees jump to 10–18 at
  `theta = 1/8` but still stop. The sentence is qualified by "at these
  sizes", and the note says that `k` differs (3 against 2).
- "Both conditioning and chain length matter". Chain length rests on one
  pair of runs (lower bound 0.035, `n = 8` against `n = 16`). The note
  qualifies it with "in the tested range".

I accept both as worded.

## 4. Commands run

From `research-20260929/reviews/adaptive-matching-confirm-r1-checks/` with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PYTHONDONTWRITEBYTECODE=1` and Python 3.13. The machine is shared (load
about 21).

| Command | Log | Result |
|---|---|---|
| `python3 my_constants.py` | `my_constants.log` | Independent constants: `theta*`, `K*`, base, fixed-point ratio 0.79, `K_1(0,0)`, `K_LS`, orders. Random checks of the growth condition and the Corollary 3 stage cap (0 violations). The tree counterexample. |
| `python3 my_cg.py` (under `timeout 1200`) | `my_cg.log` | Own `c_g` brackets and couplings; they agree with `logs/cg_by_size.log` as described above |
| `python3 ../../theory-decomposition/adaptive2/check_tree_dp.py` (34 s) | `rerun_check_tree_dp.log` | identical to `logs/check_tree_dp.log` |
| `python3 .../run_fixed_cg.py tree 8 1e-3 14 7:0.759342 15:0.663689` | `rerun_fixedcg_tree_c141_theta8.log` | identical to `logs/fixedcg_tree_c141_theta8.log` apart from timing |
| `python3 .../run_fixed_cg.py path 16 1e-3 16 8:0.920531` | `rerun_fixedcg_path_c035_theta16.log` | identical apart from timing |
| `python3 .../run_fixed_cg.py path 16 1e-3 16 16:0.841253` | `rerun_fixedcg_path_c073_n16.log` | identical to the `n = 16` part of `logs/fixedcg_path_c073_theta16.log` |
| `curl` Crossref API for the four cited DOIs | `crossref.log` | SIAM pages 1156–1183; the other records as stated |
| arXiv abstract pages 2101.03067 and 2101.06350 (web fetch) | – | 2101.03067 is Shin–Anitescu–Zavala (SIAM J. Optim. 2022, DOI 10.1137/21M1391079); 2101.06350 is Shin–Zavala, "Controllability and observability imply exponential decay of sensitivity in dynamic optimization" |

I also read these logs against the note: `gr_random_eps1e-4.log`,
`ls_scaling_n64_eps1e-4.log`, `probe_boundary.log`, all four
`fixedcg_*.log`, `cg_by_size.log`, `constants_gr.log`, and the review's
`boundary_test_C3.5.log` and `face_test_C3.5_0.5.log`.

Not rerun: the `m = 63` fixed-conditioning tree run (591 s; I compared it
with its log only) and the `n = 32, 64` fixed-conditioning path runs (I
compared them with their log only).

The reruns created no `__pycache__`.
