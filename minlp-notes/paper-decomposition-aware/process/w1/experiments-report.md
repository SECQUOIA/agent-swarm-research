# Experiments cluster: implementation audit, new computational study, and three new results

## Verdict

- **Implementation.** The implementation matches the paper's algorithm in
  every point that affects validity. I found no soundness problem in the
  solver, the stored certificate, or the independent checker. The
  differences from the paper's text are presentation gaps (minor), plus one
  real description gap: per-coordinate curvature and two-point grids for
  coordinates with nonpositive diagonal are used but not described.
- **Reported numbers.** Every number I checked in `computation.tex` and
  `completion.tex` matches the saved result files. That covers the
  core-solver figures and spot checks of the extension figures.
- **New study.** A small, clean, reproducible study (E1–E5 plus a
  supplementary S1) now exists under `paper-decomposition-aware/experiments/`.
  It covers 290 runs in 4.1 min wall time (about 16 CPU-minutes), with one
  command to reproduce, CSV output and one figure per experiment. It
  illustrates the main theorem well: filtering removes the accuracy
  dependence, and the plateau grows like `sqrt(kappa)`. It also exposes
  limits honestly: flat optimal sets, very large height bounds, and
  `theta` above the theorem's threshold.
- **Development.** The experiments led to three results with complete
  proofs, in `experiments-proofs.tex`:
  1. A growth certificate and necessary condition for box QPs: nonconvexity
     with growth can live only on active or integer coordinates, and
     `kappa >= 2` whenever a coordinate is free.
  2. **Filtering versus grading.** Filtered *uniform* grids use
     `Theta(sqrt(n kappa))` labels per coordinate at every accuracy.
     - The upper bound `(2+sqrt2) sqrt(n kappa) + 7` holds always, with no
       slope condition and no trials.
     - The lower bound `sqrt((n-2) kappa) + 1` holds on a pair instance with
       exact curvature, for every `kappa >= 2`. The same instance shows that
       the `5 sqrt(n kappa) h` localization radius is sharp up to a constant.
     - Geometric grading is therefore what yields `log n`, and with it the
       `f(p,kappa) poly(n)` form.
  3. **Localized exact acceptance.** A sound rule that certifies exact
     optimality from the filtering history plus a local first/second-order
     test, with no height bound. Under growth and strict complementarity it
     provably succeeds after `O(log(s sqrt(n kappa)/margin))` stages. On 30
     random instances it accepted 29 within at most 4 stages, versus 1–542
     stages for the height rule, with zero disagreements.

## Part A: implementation audit

Files read: `solver/certified_grid.py`, `verify_certificate.py`,
`exact_output.py`, `finite_dp.py`, `decomposition.py`, the solver README, and
the benchmark README, PROTOCOL, RESULTS, FINDINGS and VERIFICATION files.

### Algorithm versus paper

| Item | Paper (`main.tex`) | Implementation | Verdict |
| --- | --- | --- | --- |
| Correction | `d_i(v) = L w_i(v)^2/8`, common `L` | `max(0,A_ii) w^2/8`, per coordinate (A is the Hessian) | Valid and sharper. The paper should state the per-coordinate rule (the new draft `sections/grids.tex` already uses `L_i`). |
| Coordinates with `A_ii <= 0` | Only the all-nonpositive case is mentioned (endpoint DP exact) | Every such coordinate gets the two-point grid `{lo, hi}` with zero correction, mixed with graded coordinates | Valid: the interpolation lemma holds with `L_i = 0` by Jensen. **Not described in the paper (minor; needs a sentence)**. The growth lemmas hold verbatim (zero correction, 2 labels). |
| Unit integer intervals | Correction ignores length-1 intervals | `d > 1` filter in `coordinate_grid` and in the checker | Match. |
| Grid rule | Steps `h_j + theta t` (continuous) and `max{1, floor(h_j + theta t)}` (integer), clipped | Identical; `t = |point - center|` | Match. Stage 0 has at most 3 nodes per coordinate. |
| Min-marginals and DP | Two passes, all coordinate marginals | `finite_dp.solve_tree`; marginals read from the first bag containing the coordinate | Match. |
| Filter | Keep `[a,b]` iff `min{m(a),m(b)} <= U`; take the hull; singletons stay | `filtered_bounds`, identical | Match. `removed_intervals` counts failed intervals, including some that the hull later reintroduces (reporting nuance only). |
| Incumbent | `U <- min{U, F(y)}` | Also polishes `y` by exact coordinate descent | Allowed: U only decreases and stays feasible. |
| Next center | `y` (corrected minimizer) | `point = result["point"]` | Match. |
| Stage budget J | Smallest J with `7 L n s^2 4^-J / 8 <= eps` | Same, by rational comparison; `n` and `s` include fixed coordinates | Minor: the paper substitutes fixed coordinates first; the larger `n` only increases J. |
| Trials | `theta = 2^-mu`, mu = 2, 3, ...; restart from the original box **with the lower endpoint vector as center** | Restart from the original box **with the best feasible point as center** | Minor text mismatch. The proof allows any feasible center (Lemma contraction), so both are valid; update the text. |
| Cap | `K = 100 theta^-1 ceil(log2(n+2))`, abort before allocating tables | `100 * 2**mu * (n+1).bit_length()` (`(n+1).bit_length() = ceil(log2(n+2))` exactly), checked per coordinate during generation | Match, up to the fixed-coordinate count. Resource caps (`max_table_states`) are outside the theorem. |
| Stop rule | Stop when the verified global gap `U - b <= eps` | `upper - lower <= epsilon`; `lower` = max of all stage bounds and an initial interval bound | Valid: every stage bound is at most `F*`, because `x*` is never filtered. |
| Certificate | Factors, curvature evidence, grids, corrections, messages, filtering decisions, incumbents | Grids, all directed messages, marginals, grid lower bound and witness, incumbents, next bounds; corrections and curvature recomputed from `A` by the checker | Match. |
| Checker | Independent replay | Recomputes tables, every Bellman equality (sufficient on a tree: the directed dependencies are acyclic), beliefs, marginals, witness, filtering, bounds; restarts only reset to the original box (always safe); PSD/KKT presolve checked by `A = L D L^T`, `D >= 0`, and KKT signs | Sound. It shares only parsing, validation and evaluation with the solver, as documented. |
| Exact output | Theorem exact: doubling `q = 1, 2, 4, ...`; reconstruction window `1/(4R^2)`; value isolation by continued fractions plus an equality check | Doubling from `q = 4`; candidates are the incumbent, `limit_denominator(R)` within `1/(4R^2)`, and face stationarity (LP when singular, `tau = 1/(4nR)`); acceptance by **Proposition candidateheight**, `F - lower < 1/(V W)` | Valid. The theorem's proof can be **simplified** to use the implemented rule: the reconstructed candidate `x*` has `W <= V`, so a gap below `1/V^2` suffices and no continued-fraction value reconstruction is needed. |
| Height bound | `R = D (2 n C_H)^n` | Hadamard product of `max(1, row 1-norms)` of `D*A` over free continuous columns; the checker recomputes it independently | Valid (I re-derived the denominators: `D` clears `A/2`, `u = Dx` satisfies an integral system, and the value denominator divides `D R^2`). Note that `H` in Sec. 5 of `main.tex` is not the Hessian (notation clash with Sec. 2). |

### Reported numbers versus saved files

Rechecked by `process/w1/checks/audit_first_release.py` and
`audit_completion.py` against `solver/extra-benchmarks/results*/results.json`
and `completion/benchmarks/results/*.json`:

- `computation.tex`:
  - Method table: 13/13, 13/13, 11/13, 13/13; public instances 0/2 each;
    incomplete runs 2/2/4 table limits and 2 SCIP time limits.
  - SCIP: 6 optimal and 7 gap-limit statuses.
  - 45 certificates valid; 39 enclosures; states 6,167 versus 27,386, and
    771 versus 13,527.
  - Medians: solve 0.0059/0.0082 s, replay 0.0084/0.0078 s, subprocess
    0.174/0.193 s; memory about 25 MB.
  - Summed subprocess wall time 20.23 and 22.23 s; 56 certificates.
  - Path table (gaps, times, MiB); n = 256 unpruned replay 1.790 s; SCIP
    0.000612 in 1.797 s; width-two case 5/256, 0.0318 s and 0.0546 s.
  - Affine table: 1,694/64,564/76,986/394 states and the stated gaps.
  - Diagnostic counts 9 / 70 / 26,589 / 526 / 21,034 (from
    `research-20261002/new-direction/check_pruned_grid-results.json`).
  - **All match.**
- `completion.tex`:
  - Lane table: 16/12/16, 16/12/16, 9/9/9, 11/10/11, 16/13/15, 5/5/5, total
    73/61/72.
  - 54 enclosures; 29 exact values; 15.18 and 15.34 s.
  - Affine star: 16 removed, value -1, 0.065 s and 0.047 s. Minimum cut:
    1/1024, 0.089 s and 0.099 s. Piecewise examples: 27/65536 (state and
    query counts not rechecked in detail).
  - Constrained runs: 15 stages and 33,502 states; 43 stages and 2,538
    states; 252,192; 1,938.
  - Extensions: 545 states in 36 stages; 469 states in 8 stages; 17 states
    in 2 stages; -509/105 with 9 queries, 5 cuts and 88 pivots; 1.584 s;
    10 replays.
  - 158 tests in 4.114 s (`completion/targeted-tests.txt`).
  - **All match.**

## Issues (severity, fix)

1. **Major (paper story, not correctness).** `computation.tex` and
   `completion.tex` report repository-history benchmarks. They use
   unplanted instances, heterogeneous lanes, and 84+74 configurations
   that mostly test engineering contracts. They do not test the theorem's
   prediction (accuracy-independent plateau, dependence on `kappa` and
   `n`). *Fix:* replace them with the new study (draft in
   `experiments-proofs.tex`, Sec. "Computational illustration": two tables
   and the E1/E2/S1 figures). Mention the old suites at most in
   supplementary material, with the honest public-instance result: the
   width barrier on QPLIB 3852/5881.
2. **Minor (description gap).** Per-coordinate `L_i` and two-point grids
   for `L_i = 0` are used by the implementation and the experiments but
   not stated in the paper's algorithm. *Fix:* one paragraph. The
   interpolation lemma with `L_i` (as in `sections/grids.tex`) already
   covers validity, and the growth lemmas hold verbatim (the conventions
   paragraph of the fragment).
3. **Minor.** The restart center is "lower endpoint vector" in the text but
   the incumbent in the implementation. *Fix:* say "any feasible point
   (the implementation uses the incumbent)".
4. **Minor.** `n` in J and in the cap counts fixed coordinates. Harmless;
   one sentence.
5. **Minor (simplification).** The proof of Theorem exact can use
   Proposition candidateheight directly (gap `< 1/V^2`, `W <= V`) instead of
   value isolation by continued fractions. This matches the implementation.
6. **Minor (constants).** On compliant runs (E1, filtered graded,
   `theta = 1/8`) the measured quantities stay far inside the bounds:
   - `|y_j - x*|^2 <= 0.047 kappa n h_j^2`;
   - `D(y_j) <= 0.155 L n h_j^2`, against 7/8 in the old main text and 9/16
     in the core cluster's trial lemma;
   - radius `<= 0.135 * 4.2 sqrt(n kappa) h_j`;
   - labels `<= 0.0034 * (100/theta) ceil(log2(n+2))`. This is the
     implementation's cap; it equals 0.034 times the core cluster's cap
     `10/theta ...`.

   The implementation's cap is 10 times the core cluster's new cap. A larger
   cap is still valid (it only weakens the worst-case bound), but the paper
   and the code should state the same constant. The cap never triggered a
   restart in practice; restarts in E2 came from the stage budget J. Worth
   one sentence: the cap matters only for the worst-case bound.

7. **Observation (supports the theorem's hypothesis).** With `theta = 1/4`
   and `kappa >= 64` (`theta^2 kappa >= 4`), contraction fails:
   `gap/(L n h^2)` reaches 61. In the default schedule's first trial even the
   localization bound is exceeded, by a factor up to 1.45. The slope
   condition is therefore not an artifact. Empirically a trial succeeded
   whenever `theta^2 kappa <= 2.2`, while the theorem asks for 1/8.
8. **Minor (sharpening).** The integer "+1" in the localization lemma is an
   artifact of interval filtering. Node-level exclusion of integer labels
   (Lemma node exclusion) is valid and removes it (Remark in the fragment).
9. **Observation for the exact-output discussion.** The height rule needs
   gaps of `2^-49` to `2^-342` even for `n <= 6`. The number of stages
   tracks `log2(VW)`: 534 stages for 342 bits. Exact output without growth
   (flat segment) did not finish in 5 s (gap about `2^-11`, needed about
   `2^-53`), as Theorem generalfinite allows.

## Part B: new experiments

Location: `paper-decomposition-aware/experiments/`. Run
`python3 run_all.py` (4 workers), then `python3 summarize.py`. The solver
is imported unchanged; file hashes are in `results/environment.json`, and
the hash of `certified_grid.py` equals the frozen phase-two benchmark hash.
The machine was shared, with load average 10.9–15.5; timings are
indicative. Details and numbers are in `experiments/README.md`.

- **E1 (accuracy).** Path/tree n = 16, band n = 12 (p = 3), band n = 8
  (p = 4); `kappa` in [4, 4.45]; `theta = 1/8`; 16 stages. Both filtered
  variants plateau (path: about 1,000–1,100 states per stage from stage 4
  on). Unfiltered graded grids grow polynomially in j to the 1e5 cap;
  unfiltered uniform grids grow exponentially. All 48 replays are valid,
  `F*` is always enclosed, and `x*` is never filtered.
- **E2 (`kappa` = 2..256, path n = 16).** Plateau labels: uniform 13 -> 55,
  graded with the theorem's `theta` 9 -> 49, `theta = 1/4` 9 -> 33.5. The
  radius grows like `sqrt(kappa)`. The default schedule restarts exactly
  when needed (`kappa` = 64, 128, 256).
- **E3 (n = 4..128, `kappa` about 2).** Uniform filtered labels equal
  `4(floor(sqrt(n/4))+1)+1` exactly: 9, 9, 13, 13, 21, 25. Graded: 9 -> 19
  (1/8) and 9 -> 15 (1/4). The n range is too small to separate `log n`
  from `sqrt n` empirically; the proposition supplies the theory.
- **E4 (exact output, 20 instances, n <= 6).** 18 are exact and match the
  independent face enumeration (`oracle.py`, no solver code), including
  isolated ties. The 2 flat-segment instances hit the time limit.
- **E5 (SCIP 10.0, single thread, absgap 1e-6, 20 s).** SCIP closes the gap
  for n <= 16 (0.11–5.4 s) but not for paths with n >= 32. The certified
  solver reaches replayed gaps of at most 1e-6 on all 21 instances
  (0.25–6.9 s solve). **All 21 SCIP primal bounds lie below the true
  optimum** (epigraph tolerance); its dual bounds are valid. This is a
  benign family, one formulation and default settings: no ranking claimed.
- **S1 (localized acceptance, proposed).** 29/30 accepted within 4 stages
  (0.03 s or less), versus 1–542 stages for the height rule; 0
  disagreements; the 12 instances with n <= 6 match the oracle. The one
  failure has two optimal vertices.

**Caveats recorded.**
- The planted family is benign: the minorant certificate proves `x*` once
  known (Lemma growth (a)).
- Python exact arithmetic dominates time.
- E3 cannot show `log n` against `sqrt n` asymptotically.
- The SCIP comparison is formulation-dependent.

## Classical versus new (closest prior work)

- **Finite-state tree DP, min-marginals, two passes.** Classical (variable
  elimination, junction trees; Dechter 1999; Wainwright–Jaakkola–Willsky
  2005, both cited in the report).
- **Interpolation correction `L h^2/8`.** The classical linear-interpolation
  error constant. Using it as a randomized-rounding lower bound on a
  product grid is the paper's (not my cluster's).
- **Min-marginal domain filtering.** Same spirit as optimality-based and
  marginal-based range reduction in spatial branch-and-bound (Puranik and
  Sahinidis 2017 survey domain reduction; I did not check its exact
  statements).
- **Lemma growth (fragment).** Elementary first/second-order arguments;
  part (a) is a standard quadratic-minorant certificate. The consequence for
  the theorem's scope is new as an explicit remark: nonconvex continuous
  instances with growth need active bounds, and `kappa >= 2`.
- **Sharpness of localization (fragment).** New for this method. It is the
  grid analogue of the **cluster problem**: Du and Kearfott, J. Glob. Optim.
  5 (1994); Wechsung, Schaber and Barton, J. Glob. Optim. 58 (2014), Table 1,
  where the number of boxes grows polynomially in n once the second-order
  prefactor exceeds `lambda_1/8`; Kannan and Barton, J. Glob. Optim. 69
  (2017), where first-order growth along feasible directions mitigates
  clustering. All three are in the local knowledge base (read). The novelty
  here is the exact statement for corrected-grid filtering and the
  consequence that grading, not filtering, yields `log n`.
- **Localized exact acceptance (fragment).** New in this setting, as far as
  I know. It is close in spirit to **exclusion boxes and backboxing** around
  local minimizers in interval branch-and-bound (Neumaier, Acta Numerica 13,
  2004, Sec. on exclusion boxes; Van Iwaarden's backboxing and Schichl and
  Neumaier's exclusion regions are cited there, but I did not check them
  directly), and to Kannan–Barton's first-order observation. The rational,
  checker-replayable form, the node-exclusion step, and the margin-based
  stage bound are new.
- **Bibliography entries to add** (DOIs from the knowledge base):
  - DuKearfott1994 (10.1007/BF01096455);
  - WechsungSchaberBarton2014 (10.1007/s10898-013-0059-9);
  - KannanBarton2017 (10.1007/s10898-017-0531-z);
  - Neumaier2004 (10.1017/S0962492904000194).

## Placement recommendations

- **Lemma growth for box QPs.** Appendix, plus a short main-text remark in
  the model section: growth at an interior continuous optimizer forces
  convexity; `kappa >= 2`. It clarifies what "nonconvex" means in the
  theorem.
- **Propositions uniform and sharpness, Corollary uniform.** Main text,
  right after the uniform state bound, as one short proposition: filtered
  uniform grids use `Theta(sqrt(n kappa))` labels, unconditionally, and the
  localization radius is sharp. Proofs go in the appendix. It explains the separate roles of
  filtering and grading, a natural part of the paper's story.
- **Proposition localized acceptance and Corollary eventual.** Main text in
  the exact-output section, as a practical acceptance rule that is sound
  without growth. Put the corollary with its explicit `h*` in the appendix.
  State clearly that it is prototyped in post-processing, not in the
  released solver.
- **Remark on node-level integer filtering.** Remark next to the
  localization lemma.
- **Computational section.** Replace `computation.tex` and `completion.tex`
  with the new illustration: Table E1, Table E5, figures E1, E2 and S1
  (E3 and E4 optional, or merged).

## DEVELOP: open questions and outcomes

1. *Is grading necessary, or does filtering suffice?* **Resolved
   (sharpened).** Filtering alone already gives accuracy independence: Prop.
   uniform proves at most `(2+sqrt2) sqrt(n kappa) + 7` labels for filtered
   uniform grids, unconditionally, in a single run, with no `theta` and no
   trials. The cost is order `sqrt(n kappa)` labels per coordinate (Prop.
   sharpness and Cor. uniform, exact curvature, every `kappa >= 2`), hence
   tables of order `(n kappa)^{p/2}`.
   `checks/experiments_uniform_bound_vs_data.py` confirms the upper bound on
   all 678 uniform stages, with ratio at most 0.56. Grading turns this into
   `theta^-1 log(1 + theta sqrt(n kappa))`. A complete proof is in the
   fragment, and exact checks (`checks/experiments_localization_tightness.py`,
   Fraction arithmetic, plus the unchanged solver) match the predicted
   radius exactly.
2. *Is the localization constant 5 tight?* **Partially.** The lower bound is
   `sqrt((n-2) kappa)/4`, so the upper bound is sharp up to a factor of at
   most `20 sqrt 2`. Experiments sit at about 0.06–0.15 of the bound. For
   uniform grids a direct argument gives an upper radius of about
   `(1/2 + 1/sqrt 8) sqrt(n kappa) h + h`. I did not write out the graded
   version.
3. *Can `theta` be larger than `1/sqrt(8 kappa)`?* **Partially.** The
   contraction step works whenever `c = L theta^2/(2g) < 1/5`, that is
   `theta^2 < 2/(5 kappa)`, with `B = L/(4g(1 - 5c))`: in the recursion
   `E_j <= L/(4g(1-c)) n h^2 + c/(1-c) E_{j-1}` with
   `E_{j-1} <= 4 B n h_j^2`, closure needs `4c/(1-c) < 1`. This is a factor
   3.2 over the paper's 1/8. I did not redo the localization and state
   lemmas under this weaker condition, so I make no claim beyond the
   contraction step. Empirically success persists up to
   `theta^2 kappa` of about 2.2; the remaining gap probably comes from the
   worst-case factor 4 in `E_{j-1} <= 4 B n h_j^2` and the loose penalty
   energy bound.
4. *Exact output without the height bound.* **Resolved under strict
   complementarity** (Prop. localized acceptance, sound always; Cor.
   eventual, succeeds once `h_j <= h*`). For rational data
   `log(1/h*) = poly(I) + O(log kappa)`, so it is never worse
   asymptotically and is much better in practice (S1). **Not resolved:**
   ties among optimal vertices, degenerate active sets, and flat optimal
   sets, where the test can fail. A natural next step is to split the
   retained box at tied concave coordinates. Not attempted.
5. *Restart trigger.* The theorem's cap never binds in practice. A
   gap-contraction-based restart rule (restart when the gap fails to shrink
   by about 4 per stage) looks attractive. Not proved; recorded as an idea.
6. *Genuine treewidth lower bound.* The `(n kappa)^{p/2}` lower bound for
   uniform filtered grids uses supplied bags of size p. A version with
   genuine treewidth `p - 1` (all bag members interacting) remains open.

## Files

- `paper-decomposition-aware/experiments/`: `README.md`, `run_all.py`,
  `instances.py`, `oracle.py`, `localized.py`, `figures.py`,
  `summarize.py`, `results/` (raw JSON, CSV, `environment.json`,
  `summary.json`, E4 certificates), and `figures/` (6 PDFs).
- `paper-decomposition-aware/process/w1/experiments-proofs.tex`: fragment;
  compiles with `macros.tex`.
- `paper-decomposition-aware/process/w1/checks/`:
  - `audit_first_release.py` and `audit_completion.py` (number audit);
  - `experiments_localization_tightness.py` (exact checks of the sharpness
    proposition, separable and pair forms, plus a solver cross-check);
  - `experiments_localized_acceptance.py` (development record of the
    acceptance rule);
  - `experiments_uniform_bound_vs_data.py` (uniform upper bound versus all
    uniform stages: PASS).

## Commands actually run (targeted; no project-wide verification, no CI inspection)

- `python3 run_all.py --jobs 4` (final run: 290 tasks, 0 failures,
  248 s wall); earlier partial runs (`--only E4`, `--only S1`) were
  superseded by the final full run.
- `python3 summarize.py`.
- `python3 checks/audit_first_release.py` and
  `python3 checks/audit_completion.py`.
- `python3 checks/experiments_localization_tightness.py`: PASS, both exact
  checks.
- `python3 checks/experiments_localized_acceptance.py random`: 29/30, 0
  disagreements.
- pdflatex compile of the fragment in a throwaway wrapper under `/tmp`:
  only expected undefined cross-references and citations.
