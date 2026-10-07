# W4 review C-computation: Section 11 and `experiments/`

Scope: `sections/computation.tex` (Section 11), the computational claims that
other sections make (abstract, `intro.tex` 154–158, `conclusion.tex` 25–35,
`exact-localized.tex` 1–5 and 131–139, `grids.tex` 287–290), and the artifacts
in `experiments/` (README, `run_all.py`, `instances.py`, `analysis.py`,
`oracle.py`, `localized.py`, `summarize.py`, `figures.py`, `results/*.csv`,
`results/summary.json`, `chain/`, `recourse/`, `qplib/`). I also read the
solver code that the experiments import (`certified_grid.py`,
`exact_output.py`, `verify_certificate.py`, read-only).

## Verdict

Section 11 is in good shape. I recomputed every number, table entry and
figure statement from the result files, and they match. Exceptions are listed
below. The experimental design in the text matches `run_all.py`. The list of
implementation-versus-analysis differences is essentially complete, and
re-running E6 and the E2 CT runs with the current code reproduces the saved
results exactly. The section's claims are worded cautiously and follow from
the data.

One statement is wrong. The SCIP paragraph says that SCIP's primal bounds lie
below the optimum "because the epigraph constraint is satisfied only within a
feasibility tolerance". In fact, 51% to 94% of that shortfall comes from SCIP's
incumbents lying 10⁻⁸ outside the box at every active coordinate. The
"incumbents optimal to within 1.3·10⁻¹⁴" are the incumbents after projection
onto the box. The other findings are minor:
- a "smallest eigenvalue at most −1.75" claim fails for one E4 instance;
- one replay statement is slightly too broad;
- three run parameters are missing;
- two reproduction commands write their output to the wrong directory, and the
  artifact is not self-contained;
- the experiment labels appear out of order.

## Findings

### C-computation-1 (major): the SCIP primal-bound shortfall is misattributed, and SCIP's "incumbents" are projected points

**Location:** `computation.tex:369–375`; Table 5 caption at `computation.tex:394–398`. The same wording appears in `experiments/README.md` (E5 paragraph) and in the comment on `epigraph_shortfall` in `run_all.py:task_scip`.

**Problem.** The text says: "Its incumbents were optimal to within
1.3·10⁻¹⁴ … Every reported primal bound lay below the optimum, by 1.8·10⁻⁶ to
1.6·10⁻⁵, because the epigraph constraint is satisfied only within a
feasibility tolerance." `task_scip` clips SCIP's point to the box before it
evaluates the point exactly (`v = min(max(v, lo), hi)`). So both the
1.3·10⁻¹⁴ figure and the "exact gap" in Table 5 refer to the projected point.

I rebuilt the E5 model exactly as `task_scip` does and split the shortfall
F(clip x) − t into a bound-violation part F(clip x) − F(x) and an epigraph
part F(x) − t (`process/w4/checks/scip_shortfall_cause.py`,
`scip_shortfall_large.py`). Results:

| run | max bound violation (#coords) | shortfall | bound part | epigraph part |
|---|---|---|---|---|
| path16 s202, default | 1.0e-8 (4 = all active) | 1.82e-6 | 0.92e-6 | 0.90e-6 |
| band12 s101, default | 1.0e-8 (3) | 3.05e-6 | 2.15e-6 | 0.90e-6 |
| path128 s101, default | 1.0e-8 (32) | 1.61e-5 | 1.52e-5 | 0.90e-6 |
| path32 s101, feastol 1e-9 | 9.0e-10 (8) | 2.42e-7 | 2.41e-7 | 8.9e-10 |

All 21 E5 runs fit the formula shortfall = n_A·μ·10⁻⁸ + 9.0·10⁻⁷ exactly to
three digits, where n_A is the number of active coordinates and μ is the
inward slope. The bound violations therefore account for 51% (path16) to 94%
(path128) of the shortfall. The epigraph violation is a constant 9·10⁻⁷. So
the stated cause explains only the smaller part for n ≥ 12. SCIP's actual
incumbents are slightly infeasible, and their objective lies below OPT. The
conclusion that SCIP's reported interval never contains OPT still holds.

**Fix.** Replace `computation.tex:369–375` from "Its incumbents were optimal"
to "in any run." with:

> Its incumbents lie slightly outside the box: every coordinate that is at a
> bound in $x^*$ violates that bound by $10^{-8}$, within SCIP's tolerances.
> Projected onto the box, the incumbents were optimal to within
> $1.3\cdot10^{-14}$, and the dual bounds were valid. With the projected
> incumbent evaluated exactly, the gap to the dual bound was
> $2.8\cdot10^{-6}$ to $6.8\cdot10^{-6}$ on the instances with $n\le16$, so
> the requested $10^{-6}$ was not reached. Every reported primal bound lay
> below the optimum, by $1.8\cdot10^{-6}$ to $1.6\cdot10^{-5}$: the bound
> violations, at which $F$ decreases with slope $\mu$, account for $51\%$ to
> $94\%$ of this, and a violation of the epigraph constraint by
> $9\cdot10^{-7}$ accounts for the rest. Hence SCIP's reported interval did
> not contain the optimum in any run.

In the Table 5 caption, write "exact value of SCIP's incumbent projected onto
the box minus its dual bound" and "SCIP's projected incumbents are optimal to
within 1.3·10⁻¹⁴". Optionally add "SCIP received the coefficients rounded to
double precision." Update the README the same way. In `task_scip`, record the
maximum bound violation and F at the unclipped point, so that `summarize.py`
can report the split.

### C-computation-2 (minor): "smallest eigenvalue at most −1.75 in every instance" is false for one planted instance

**Location:** `computation.tex:104–105`; README, "Planted nonconvex family".

**Problem.** E4 uses three planted instances (`planted(kind, 6, 4, 4100)`). For
the tree instance, λ_min(H) = −1.161, which is above −1.75. The path and band
instances give −3.32 and −3.59. The value −1.75 is the minimum over E1–E3 and
E5 only (check: `c_numbers.py`, plus a direct call of `planted`).

**Fix.** Change the text to "$H$ is indefinite in every instance (its smallest
eigenvalue is at most $-1.16$, and at most $-1.75$ in E1--E3 and E5)", or
simply "at most $-1.16$".

### C-computation-3 (minor): the replay statement omits S1's EX runs, on which a stated result rests

**Location:** `computation.tex:90–93`, compared with `computation.tex:346–347`; README, "Experiments and results".

**Problem.** The text says "Every certificate on which a result … rests was
replayed …; the runs of S1 that only count stages … were not replayed." But
`task_localized` never passes the S1 `solve_exact` certificate to
`verify_certificate`. These EX runs supply the reference values for "The
accepted values agreed with those of EX on all 29 instances" (on the 17
instances with n ≥ 8 there is no enumeration). The README's "except the EX
runs and the single-run threshold runs of S1" is ambiguous, because the E4 EX
runs *are* replayed.

**Fix.** Either replay the 30 S1 EX certificates and record
`height_rule_replay_valid`, or change the sentence to:

> …; in S1, the runs of EX, which supply reference values and stage counts,
> and the single-run threshold runs were not replayed.

### C-computation-4 (minor): two small omissions in the list of implementation differences

**Location:** `computation.tex:29–41`, items (d) and (e).

**Problem.**
- Item (e) presents the maximum over all stages and trials only as the
  *reported* bound. In `certified_grid.solve`, however, the success test
  `upper - lower <= epsilon` also uses this cumulative bound, so a later trial
  could succeed because of an earlier trial's bound.
- Item (d) lists ℓ as a polishing start. In EX rounds after the first,
  `warm_start` replaces ℓ.

Neither omission matters for the reported data. I checked that in all 45 CT
runs of E2 and E5, the last stage's own gap U − β_j is already at most ε.

**Fix.**
- Item (e): "The lower bound used in the success test and reported at the
  end is the largest bound of all stages and trials, …".
- Item (g): add "(the incumbent also replaces $\ell$ as a start of the
  descent)".

### C-computation-5 (minor): run parameters that Section 11 does not state

**Location:** `computation.tex:173–187` (E2), 189–199 (E3), 136–141 (E1).

**Problem.** The accuracy of the CT runs in E2 (ε = 2⁻²⁰) appears only in the
README. The paper also omits the stage counts of the single trials: E2 runs
12 stages and E3 runs 11. E1's 16 stages can only be read off Figure 1. For
E3, the paper does not say that the quoted node counts use the plateau
statistic of Figure 2. Without these values the E2 and E3 statements cannot
be reproduced from the paper alone.

**Fix.**
- E2: "With the theorem's grading (12 stages) …" and "CT ($\varepsilon=2^{-20}$)
  handled this automatically …".
- E3: "(11 stages; nodes are the plateau of Figure 2, the median of the
  maximum over free coordinates in the last four stages, median over three
  seeds)".

### C-computation-6 (minor): the reproduction commands for the chain and recourse write to the wrong directory, and the artifact is not self-contained

**Location:** `experiments/README.md`, "Reproduce"; `chain/run_chain.py` and `recourse/run_recourse.py` (`open('results.csv', 'w')`, …); `computation.tex:84–85`.

**Problems.**
- The README code block starts with `cd paper-decomposition-aware/experiments`
  and then runs `python3 chain/run_chain.py` and
  `python3 recourse/run_recourse.py`. Both scripts write `results.json` and
  `results.csv` (and, for the chain, `per_stage.csv`) to the *current
  directory*. Run as documented, they write into `experiments/`, and
  `summarize.py` silently keeps reading the stale `chain/results.csv` and
  `recourse/results.csv`. `run_chain_warmstart.py` and `qplib/run_qplib.py`
  already write next to themselves.
- The experiments import the solver from
  `../research-20261002-decomposition/solver/`. The recourse runs also import
  `completion/benchmarks/corpus.py` and `completion/theory/piecewise-recourse`
  from that tree, and QPLIB reads `solver/extra-benchmarks/data`. All of these
  lie outside the paper directory, yet the paper says "Code, inputs, … accompany
  the paper". Also, `environment.json` hashes only six solver files, not the
  recourse modules or the corpus.

**Fix.**
- In both scripts, write to `Path(__file__).parent`, or change the README
  commands to `(cd chain && python3 run_chain.py)`.
- Bundle the solver and the corpus with the artifact, or pin them by a commit
  hash, and hash every imported module.

### C-computation-7 (minor): experiment labels appear out of order

**Location:** `computation.tex`, §11.3–11.7.

**Problem.** The subsections present E1–E3, then E6 (§11.3), the chain, E4
(§11.5), S1 and E5 (§11.7). A reader meets "E6" before E4 and E5.

**Fix.** Renumber in order of appearance (for example E4 := random
unplanted, E5 := exact output, E6 := localized, E7 := SCIP), together with the
README, CSV names and `summarize.py` keys. Alternatively, move §11.3 after
§11.7. If renaming files is too costly, renumbering only in the paper, with a
mapping table in the README, also works.

## Checked and found correct

Every check below is against `results/*.csv`, `summary.json`, `chain/*.csv`,
`recourse/results.csv` and `qplib/results.json`, and, where stated, against
the code.

- **Design versus code.** I checked the following against `run_all.design()`
  and are as described:
  - E1: 4 families × 3 seeds × {graded, uniform} × {filtered, unfiltered},
    θ = 1/8 (theorem grading for κ_ub ≤ 4.45), 16 stages, cap 10⁵.
  - E2: κ_target 2…256, three single-trial methods (12 stages) plus CT.
  - E3: κ_target ∈ {2, 4}, n = 4…128, 11 stages.
  - E4: 12 random (n = 3…6, 1 integer coordinate if n ≤ 4, else 2), 3 tied,
    2 flat, 3 planted; 3,000 stages, 30 s and 5 s.
  - E5: SCIP absgap 10⁻⁶, 20 s, single thread (params recorded, not
    skipped); CT ε = 10⁻⁶, 60 s.
  - E5V: 60 s, feastol and dualfeastol 10⁻⁹, offset; 39 runs.
  - E6: path and band2, n = 8…24, 5 seeds, q = 10…50.
  - S1: 30 instances, ε = 2⁻⁶⁰.
- **Section 11.1 against the solver.**
  - Common mesh h = s/2^j.
  - Trial cap `100·2^μ·(n+1).bit_length()` = 12.5 × the Lemma cap.
  - Stage limit from (7/8)Lns²4^{-J}, at most one stage more than with 9/16.
  - First center = incumbent; later centers = y_j (`center, bounds = point,
    next_bounds`).
  - Polishing from ℓ, u and the midpoint, then from y_j within the current
    box.
  - Convex presolve.
  - Cumulative lower bound (see C-computation-4).
  - θ = 0 for "uniform".
  - Exact wrapper: denominator clearing all A_ij/2; row-sum product over
    continuous rows; q = 4, doubled each round; full-box restart with warm
    start; three candidates. The wrapper's constant is never smaller than Ω
    in (eq:exact-constants), and it is sound by Remark rem:heights.
- **The checker.** `verify_certificate.py` imports only `BoxQP` and
  `rational`. It recomputes tables, Bellman equalities, min-marginals,
  filtering, incumbents and final status, and recomputes the exact-wrapper
  heights. The description in 11.1 is accurate. Its per-entry bag search,
  which is the reason given for not replaying QPLIB_3852, is as described.
  Floats are rejected (`rational()`).
- **Planted family.**
  - μ is the same at all active coordinates.
  - x*_i = k/21 with |k| ≤ 10.
  - c is rounded down to a multiple of 2⁻¹².
  - Entries touching A are 2 to 4.
  - 2M = μI_A, so the Lemma growthcert(a) test is the generator's exact LDLᵀ
    test.
  - κ brackets: κ_ub/κ_lb ≤ 1.1123, κ ∈ [3.9985, 4.4487] for κ_target = 4,
    κ_lb/κ_target ≥ 0.978, κ_ub/κ_target ≤ 1.112.
- **Off-grid paragraph.** The dyadic-node argument is valid: nodes are
  {lo, hi, center} plus dyadic steps, filtered endpoints are nodes, and later
  centers are y_j. The count 347/3,177 = 10.9% is correct. I re-ran
  `process/w3/checks/computation-verify-offgrid.py`: 78 runs, 146 descent +
  3 zero + 4 dyadic offset = 153, with no mismatch against the saved results.
- **E1.** Medians: graded filtered 989–1,049 at stages 4–15; uniform
  filtered 1,068–1,122; unfiltered graded 83,161 at stage 11; unfiltered
  uniform 64,879 at stage 6. Figure 1 plots only stages that all three seeds
  completed (`figures.py`). The figure copies in `figures/` are identical to
  `experiments/figures/` apart from the creation date.
- **Lemma ratios over 876 = 192 + 288 + 396 stages.** D/(Lnh²) ≤ 0.155; radius
  ≤ 0.179 of 4.2√(nκ)h; nodes ≤ 4.69% of the analyzed cap and ≤ 0.375% of the
  implementation's cap. The 16.8√(nκ)+3 count follows from (G4) with mesh
  h_j/2.
- **E2.**
  - Plateaus 9 → 49 (theorem grading).
  - θ = 1/4 last-stage gap ratios 4.66, 15.3 and 60.5.
  - Radius 2.12h → 15.2h, slower than √κ.
  - CT: final trial μ = 2 for κ ≤ 32, μ = 3 for 64 and 128, μ = 4 for 256;
    12 restarts, no abort. Lemma commonmesh guarantees success only from
    μ = 5 or 6.
  - The κ = 2 instances are the same as the E3 n = 16 κ = 2 ones.
- **E3.** 7 → 26, 9 → 19, 9 → 17. The separable formula 4(⌊√(n/4)⌋+1)+1 holds
  in *every* run and in each of the last four stages (`c_numbers.py`).
- **E6 / Table 3.**
  - Every cell matches.
  - The time column is attained at q = 50.
  - 11 certified brackets, as listed.
  - 28 localized proofs and 1 unproved instance; 10/10 agree with the oracle.
  - 27/40 instances keep the same largest grid; the change is ≤ 5 nodes;
    stages grow from 7–9 to 27–29.
  - Certified instances have 9–11 nodes at q = 50; the others have 8–18.
  - 42/213 free coordinates are on the last grid.
  - All runs are first-trial runs.
  - After q = 30, only one instance's largest grid still changes, so the
    conclusion's "accuracy-independent grid sizes … on unplanted random
    instances" is supported.
  - `growth_certificate` implements Lemma growthcert(a), with upper bounds
    from part (b) and from flipping one active coordinate.
- **Chain / Table 4.**
  - All 48 entries match.
  - 2^{m−1} message pieces (3.3·10⁴, 2.1·10⁹, 9.2·10¹⁸).
  - Ψ_m in `run_chain.py` equals Prop. lim:prop:messages.
  - κ ≥ 10 (Ψ = 1 at z₁ = 1, L = 10).
  - Stage counts are consistent with J ≈ log₂(2^m−1) + ½log₂(7Lnm/8ε).
  - Warm start: same stages; m = 2 has 6 nodes; table entries change by
    −1.9% to +7.5%.
- **E4.**
  - 18/20 runs exact; values and points correct; all replays valid.
  - Stage groups 67–77/132–144/275/534 match q = 64/128/256/512 and 49–65,
    80–120, 208 and 342 bits.
  - Lemma constant: 21.3–315.0 bits.
  - Flat instances: certified gap 2^−11.8 and 2^−10.8, required 2^−52.5 and
    2^−54.9.
  - The n = 3 instances have no continuous coordinate with H_ii > 0, and the
    integer coordinate of the path instance has width 1.
  - The oracle's minimum-dimension-face argument is correct.
- **S1.**
  - 29/30 accepted, with 0-based indices ≤ 4 (incumbent rule) and ≤ 8 (face
    candidate).
  - Same instances accepted by both rules; 12 accepted on the full box;
    29/29 agree with EX; 12 checked against the oracle.
  - EX used 1–542 stages; the single run needed 40–72 stages (lemma constant)
    and 139–157 (code constant) on the top five instances.
  - `localized.py` implements Prop. prop:local (narrowed box, cases (i)–(iv),
    exact LDLᵀ) and Def. def:facecand.
  - `exact-localized.tex` 1–5 and 131–139 are consistent with these numbers.
- **E5 / Table 5.**
  - Every CT and SCIP cell matches.
  - Status "gaplimit" for all n ≤ 16, time limit for all n ≥ 32.
  - Exact gaps 2.76–6.79·10⁻⁶.
  - Dual bounds strictly below 0.
  - Constants 94–1,577, so 10⁻⁶ is 6.3·10⁻¹⁰ to 1.07·10⁻⁸ of the constant.
  - E5V: 27 path runs all hit the time limit; with 60 s the dual bounds are
    −5.1·10⁻⁵ to −7.5·10⁻⁴; 0/39 intervals contain OPT.
  - The comparison is described fairly: one formulation, default settings,
    a family favoring small width, "not a performance ranking".
- **Recourse / Table 6.**
  - All entries match `recourse/results.csv`.
  - The instance descriptions match `completion/benchmarks/corpus.py`:
    64(y_i − x₀/2)², −x₀², shuffled; φ_M − z² with Example ex:cv-fm; dense:
    convex core, concave diagonal, nonpositive complete residual couplings.
- **QPLIB.** Bag sizes 20 and 94; 5,723,918 entries; 156 s; 4.4 GB; −234 =
  −234, matching the library's .sol value (asserted in `read_qbn`); 7.96·10²⁸
  entries for 5881.
- **Replay ratio and load.**
  - Replay/solve ratio is 0.81–2.54 over E1–E6, chain and plain-grid
    recourse, for runs with solve time ≥ 0.1 s.
  - Environment: 3 workers, load 13–18.
  - "Exact rational arithmetic dominates" is plausible: in a cProfile of the
    band n = 8 CT run, about 60% of the time is in `fractions` and `gcd`
    (`profile_ct.py`).
- **Additional checks supporting Section 11.1.**
  - In all CT trials of E2 and E5, the largest grid is at most 27.5% of the
    *analyzed* cap 8·2^μ⌈log₂(n+2)⌉, so the 12.5× larger implementation cap
    changed nothing.
  - All 45 CT runs succeed on their own last-stage β_j.
- **Reproducibility.**
  - The solver files match the SHA-256 hashes in `environment.json`.
  - The current experiment scripts match `environment_S1.json`.
  - Re-running all 40 E6 tasks and the 9 E2 CT tasks with κ_target ≥ 64 in
    memory with the current code reproduces status, stages, trials, nodes,
    table entries, growth certificates, candidates and replay validity
    exactly (`rerun_e6_e2.py`, 0 differences).

## Commands run (targeted, local; CI not consulted)

| Command | Result |
|---|---|
| `python3 process/w4/checks/c_numbers.py` | min λ_min(H) = −1.75 over E1–E3 and E5; κ brackets; E6 per-instance ranges; time column at q = 50; E3 formula holds in all runs; E1 medians |
| `python3 process/w4/checks/scip_shortfall_cause.py` | shortfall split for path16 (default and feastol 1e-9), band12 and path16 (offset): see C-computation-1 |
| `python3 process/w4/checks/scip_shortfall_large.py a` / `b` (2 processes, about 20 s) | path128 s101: 1.52e-5 bound + 9.0e-7 epigraph; path32 feastol: 2.41e-7 bound + 8.9e-10 epigraph |
| `python3 process/w4/checks/rerun_e6_e2.py` (4 processes, about 1 min) | 49 tasks, 0 differences from `results/raw` |
| `python3 process/w3/checks/computation-verify-offgrid.py` (about 2 min) | 146 descent + 3 zero + 4 dyadic offset = 153; 0 mismatches |
| `python3 process/w4/checks/profile_ct.py` | about 60% of the time is in Fraction arithmetic and gcd |
| inline Python | E4 planted λ_min(H): path −3.32, tree −1.16, band −3.59; n = 3 E4 curvatures; CT cap ratios ≤ 0.275; final-trial own gaps ≤ ε; SHA-256 checks |
| `pdftoppm -f 73 -l 74` on `/tmp/dpaper/out/main.pdf` | Figures 1 and 2 inspected visually; legends, cap line, bound lines and captions match the code |
