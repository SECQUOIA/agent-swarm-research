# Review r1 of stream `ratio-bound`

Reviewer: an independent research agent that did not write this material.
Date: 2026-10-02. Object of review: `../note.md` (1195 lines, last modified
20:04), the code in `../code/` and the logs in `../logs/`. My own scripts are
in `r1-code/` and their outputs in `r1-logs/`. I did not edit the note, the
code or the logs.

## Verdict

**Minor fixes needed.** I found no wrong theorem and no gap in a proof. The
main results hold as stated:

- Theorem A and Corollary A' (proved);
- Theorem B (proved);
- Theorems B2 and B3 (computer-assisted). I re-derived the reduction by hand
  and re-verified all 16 box certificates with an independent exact verifier.
- Lemma S, Theorem S, Propositions S2 and S3 (proved);
- Theorem C and Propositions C2 and C3 (proved).

Three minor issues remain, listed below:

1. The note gives the wrong reason why three box searches failed.
2. In three places, numerical values are presented as exact or proved.
3. The scope of the SCIP part (task step 2) is not stated.

There are also seven optional points. There is no major issue.

## What I checked by hand

- **Lemma N, normalized frame, Lemma R, membership remark, cylinder formula
  (1).** I re-derived each: the matrix form `M → AMB^T`, the invariance of
  `D` and of the relative discriminant (also under rescaling a ray), the
  translation `a = −αx̄`, `b = −βȳ`, the identity
  `det sym(A) = det A − ((A12 − A21)/2)^2`, the closedness of `C_X + R_+ e_w`,
  and the root formula (1). All correct.
- **Theorem A.** All steps are correct:
  - (i) `|b_j(t*)| ≤ 2D`;
  - (ii) `a_j ≥ −(1 + D²)`, and `a_j ≥ −max(2, 2D)` in all three cases (meets
    `S` with `c_j > 0`, meets `S` with `c_j ≤ 0`, misses `S`);
  - (iii) both denominator bounds; I checked the squaring step and its
    difference `8D⁴`.

  The cylinder has `s̄` in its interior and lies in both families.
- **Corollary A'.** Correct. The relative discriminant of `q̄ g_j` is
  `(a² − 4c)/(a² + 4c)` because `c ≥ 0` for a ray that misses `S`. Rays with
  `a_j ≥ 0` give `α ≥ 1/D`, which is at least the stated constant. (Optional
  point O6 concerns where "`D ≥ 1`" is stated.)
- **Theorem B.**
  - (1)–(3): the expansion of `q(s̄ + Pλ)`, `z_0`, the relative
    discriminants, `D = z_0 sqrt(2/ε)`, and SCIP's step `2√ε` together with
    the condition `ε ≤ 4/9`. `cond(P) = 12.0136`, recomputed.
  - (5): I checked the compactness argument line by line:
    - the `{w ≥ 0}` argument;
    - the exposed face of dimension 2;
    - the face structure of an affine preimage of the 2×2 PSD cone in the
      rank-3 and rank-2 cases, including why the rank-2 image plane misses
      the apex;
    - the rank-one limit with the plane `w = αx + βy`.

    All correct.
- **Reduction for Theorems B2(1) and B3.** Correct:
  - The seven conditions are necessary for a (B) set that contains `T_r` with
    `s̄` in its interior. Midpoints follow from convexity; the line condition
    follows from the membership remark.
  - The point test is valid: the form is affine in `τ` and negative at both
    ends of `[0, q(s)]`, and every test point has `q > 0`. I checked
    `m_12` for both families.
  - The `(2,2)` entry `ρ x21 + x22` is correct.
  - I re-derived `max_h det sym(X M(ρ, ρ, h)) = (det X/x21²) Ψ(X)` by
    completing the square. The case `x21 = 0` gives `Ψ = det X`.
  - Scaling to the 8 facets of `max |x_ij| = 1` is legitimate.
  - The bound `z_B/z_K ≤ r` follows because containment is monotone in `r`.
  - The test points of the near-tangent family do not depend on `L`, and
    `D = √k z_K`.
- **Theorem B2(2).** Correct. The logic of `h_0`, upward closure and
  `ε ≤ (ρ/(h_0 − 1))²` holds. I re-checked the rational `X` exactly; see the
  computations below.
- **Theorem B3(1).** Correct: the Cauchy–Schwarz step, `L < z_K < L + 1/L`,
  and the relative discriminants.
- **Lemma S.**
  - I re-derived the Sylvester coordinates and showed that multiplying by
    `R_θ = cos θ I − sin θ J` rotates both coordinate pairs, so the
    Muñoz–Serrano set is `C_{R_θ}`.
  - I checked `ℓ = −V(s − s̄)/N` and the trace term.
  - SCIP's `xextra = wzlp + kappa + norm` is at lines 1665–1666 of
    `nlhdlr_quadratic.c` (the note says 1662–1666, which includes the
    declarations; acceptable).
  - With `κ = 0` this gives `x̂ = ((x − y)/2, (w + 1)/2)`.
  - The piecewise `φ_λ` (pieces 4a and 4b, described in the
    `scip-rule-fidelity` note, Section 1.3) agrees with the upward closure;
    see S2 below.
- **Theorem S.** Correct: the bound `g_j ≥ 1/4` on `[0, s_0]` in all three
  cases, `|V(p)| ≤ N‖(p_x − p_y, p_w)‖`, positive definiteness up to the
  first zero of the determinant, `σ_min ≤ √3 D √q̄`, and
  `1/(√6 κ D) ≤ 1/(2D)`.
- **Propositions S2 and S3.** I recomputed every identity:
  - S2: `cond(P~) = L²` for `L ≥ √2` and `√2 L` otherwise.
  - S3:
    - the expansion with `u² − 1 = v²`;
    - the centred map;
    - the orbit-set slacks; `βv < 1` because `u > v`;
    - SCIP's set `{4q ≥ (w + 1)², x ≥ y}`;
    - the step `2/(u + 1)`, for both the uncompleted set and its upward
      closure. On ray 3 the point has `ŷ_e ≤ 0`, so the 4a piece applies.
- **Theorem C.**
  - (1): from sfree Lemma 10(3).
  - (2): the roots, and the trace condition implied by the `(1,1)` entry.
  - (3): both directions and the compactness part. The appeal to sfree
    Proposition 12 for `det F ≥ 0` is unnecessary; continuity suffices.
  - (4): the cylinder criterion and the cruder `h_v ≥ XY` condition.
  - (5): with `α = −d_y/d_x`.

  All correct.
- **Proposition C2.** Correct: invariance under `φ_k`. I recomputed the
  cosines `0.99984, 0.96946, 0.99855` for `k = 100`.
- **Proposition C3.** I re-derived all inequalities. In the case `t ≤ 1` the
  bound can be stated as `(1 − t)(77 − 17t)/62 + (9/4)dt`; the note's
  `+ 2dt` is weaker and still valid. The compactness argument at `d = 0`
  (vertices on the cylinder, distinct rulings `x + y = 0, 1, 2, 4`, no
  vertex other than `t*` on the contact curve) is correct.

## Independent computations

All of my scripts are new; only the decoding of a bisection path into a box
follows the same convention as the author's code.

1. **Box certificates of Theorems B2 and B3**
   (`r1-code/indep_verify_boxes.py`, run by `r1-code/run_indep_boxes.sh`).
   - Test points are built from the note's formulas.
   - Each `pt`, `det` and `a22` certificate is checked exactly at all 8
     vertices of the box.
   - Each `psi` certificate is checked against the exact maximum of `Ψ` over
     the box. `Ψ` is bilinear in `(x11, x22)` and concave in `x21`, so this
     is stronger than the author's interval bound.
   - Coverage is checked geometrically: the box volumes of each facet sum
     exactly to 8, and no two boxes overlap in their interiors (pairwise
     test on exact dyadic endpoints).

   Result: 16 of 16 files pass, with the same certificate counts as
   `logs/zB_cert/verify_all.log` (`r1-logs/boxes/*.log`). Negative controls
   (`r1-code/neg_controls.py`) confirm that the verifier rejects a wrong `ρ`
   (261 leaf failures), a dropped leaf (volume 255/32) and a duplicated leaf
   (volume 257/32, one overlap).
2. **`r1-code/indep_checks.py 1`** (`r1-logs/indep_checks_seed1.log`, ALL
   PASS):
   - S1, Theorem A and Corollary A':
     - 120 random corners with `N = 3, 5` and random costs;
     - my own `z_K` by face enumeration and bisection;
     - formula (1) agrees with bisection on the definition (0 mismatches);
     - no violation of `ρ_par ≥ f(D)`;
     - Corollary A' applied in 18 cases with no violation.

     `r1-code/indep_thmA_deep.py 7 150` repeats this on deep corners with
     `D` up to `1.3·10^4`: no violation (`r1-logs/indep_thmA_deep_seed7.log`).
   - S2, Lemma S and Theorem S: on 150 random corners (450 rays):
     - SCIP's Case-4 set, implemented from the piecewise `φ_λ`, gives the
       same steps as the upward closure of `{4N² q ≥ V², trace ≥ 0}`
       (0 mismatches);
     - the plain Muñoz–Serrano set gives the same steps as the closed form
       (0 mismatches);
     - no violation of Theorem S; the smallest ratio to the first bound is
       1.41.
   - S3, Theorem B2(2): exact check of the rational `X` and of
     `ε_0 = 24336/1330717441`.
   - S4, Proposition S3, at `u = 5/3, 25/7, 401/40` and `D = 1/2, 1, v`:
     - the boundary point on ray 3 is exact;
     - the `z_K` identity holds;
     - the orbit-set slacks are nonnegative;
     - the `φ_λ` steps are `∞, ∞, 2/(u + 1)`.
   - S5: `cond(P) = 12.0136`, and `L < z_K < L + 1/L` in 12 near-tangent
     cases.
   - S6, Proposition C3, for `d = 10^-2, 10^-3, 10^-4`:
     - `H_cyl(t = 1) = 1 − 4d`;
     - the smallest gap between disjoint intervals over a grid of `40,001`
       values of `t` is positive (`3.6·10^-2, 3.6·10^-3, 6.0·10^-4`);
     - `min_{T*} q = 0` at `t*`, and `q > 0.016` on 200,000 sampled points
       away from `t*`.
3. **Best (B) sets reported in Section 3.2**
   (`r1-code/indep_check_found_B.py`, `r1-logs/indep_check_found_B.log`).
   All 16 sets are valid at their reported `ρ`. Note that `s̄` lies within
   `6·10^-10` to `2·10^-8` (minimum eigenvalue) of the boundary of `B_X`.
4. **`r1-code/exact_feasible_below.py`** (`r1-logs/exact_feasible_below.log`).
   This is the basis of issue 1. Rational `X` with `sym(X) ≻ 0` contain
   `s̄`, `P_1` and `P_2` without lowering, and a lowered point of `P_3`, at:
   - `ρ = 6/5` for `tan:1/100:4`;
   - `ρ = 1` and `ρ = 19/20` for `tan:1/1000:9/4`;
   - in both cases for `L = 10, 30, 100, 300, 1000`.

   All PSD and PD tests are exact.
5. **Reruns of the author's code**
   (`r1-logs/rerun_stream/`):
   - `certify_zB.py 137 … 2300 90`: 28,699 boxes, all 8 facets done in 83 s,
     and `verify_zB.py` passes.
   - `certify_zB.py 197/200 … 2300 100 tan:1/1000:4`: 11,132 boxes, verified.
   - `certify_zB_lower.py` and `certify_support_one.py`: output
     byte-identical to `logs/certify_zB_lower.log` and
     `logs/certify_support_one.log`.
6. **Numbers against logs.** I compared every number in the tables of
   Sections 2, 3.1–3.3, 4 and 8 with the logs. They match, except for the
   optional points O1–O3.
7. **Sources.** The sha256 of
   `sources/bienstock-chen-munoz-1610.04604v6.pdf` matches the manifest. The
   text of Lemma 4.14 and of the remark quoted after it ("'best' in a
   violation sense, and may not translate to finding the deepest cut") is
   verified. I fetched v7 of the paper to confirm that the lemma is Lemma 24
   there; the file was not saved in the repository. "Math. Program. 2020"
   agrees with what I know of the published version.

## Issues

### Major

None.

### Minor

**1. The note gives the wrong reason why three box searches stopped at
maximum depth** (Section 8.2, rows `tan:1/100:4` with `ρ = 6/5` and
`tan:1/1000:9/4` with `ρ = 1, 19/20`; Section 9, fourth bullet; and the
`negative-result` item of the results list).

- **What the note says.** These searches failed because the closed
  relaxation (`s̄ ∈ B_X` instead of `s̄ ∈ int B_X`) is feasible on the
  boundary. It concludes that "the certified constants can be slightly above
  the true ones".
- **Why this is wrong.** At those values of `ρ` the original strict
  problem is feasible:
  - The note's own best (B) sets (Section 3.2) reach `ρ = 1.2234` for
    `η = 1/100`, `k = 4`, and `ρ = 1.0414` for `k = 9/4`.
  - My exact check (computation 4) gives rational sets with `s̄` in the
    interior at `ρ = 6/5`, `1` and `19/20`.

  So `z_B/z_K ≤ ρ/z_K` is false at these values, and no method could certify
  it. The failures say nothing about a gap caused by the closed relaxation.
- **Fix.**
  - State that these `ρ` values lie below the values attained by the best
    sets found.
  - Remove them as examples of a possible closed-relaxation gap. The general
    caveat may stay, but no example of it was observed.
  - Optionally, certify the found sets exactly, as in Theorem B2(2). Exact
    lower bounds for the listed `L` follow already: `D z_B/z_K ≥ 2.4`
    (`η = 1/100`, `k = 4`) and `≥ 1.5` (`k = 9/4`). This would turn "within
    0.06–2.2% of the best sets found" into certified brackets.

**2. Numerical values are presented as exact or proved in three places.**

- (a) Section 6.1, first bullet, and the results item labelled
  `computed-exactly`: "`z_A/z_K ∈ [0.0305, 0.0306]`". Only the lower end is
  exact (`r = 763/25000`). The upper end 0.0306 comes from Clarabel's
  bisection; SCS gives 0.0337 as its upper value (`logs/recheck_adv3.log`).
  The exact part already refutes the sfree note's "infeasible from 0.029",
  so the correction stands. Fix: label the upper end as numerical.
- (b) Section 6.1, second bullet: "true constant in `[136.707, 137]`",
  "within 0.22%". The value 136.707 is a floating-point evaluation of the
  heuristic set. The certified bracket is `[136.5, 137]` (Theorem B2(2),
  for `ε ≤ 1.83·10^-5`). Fix: label it as numerical, or certify the same
  `X` at 136.7.
- (c) Section 3.1, "So the (B) value is the (A) value at the best height:
  `max_H ρ_max(H)`." Only "`≥`" follows from the construction. Equality is
  supported numerically (box bound 137; `ρ_max` about 136.5 on a coarse
  grid; 136.707 found). Fix: label it as numerical or heuristic.

**3. The scope of the SCIP part (task step 2) is not stated** (Summary
item 3, Section 4, Section 9).

- The task's step 2 refers to sfree Proposition 6, which concerns SCIP's
  Case 2 for a two-variable set with `κ = 1`. The note analyses only Case 4
  for a constraint that SCIP sees exactly as `w − xy`: `κ = 0`, no linear
  terms in `x` and `y`, and unit scaling. Proposition 6's setting gets only a
  remark: it violates both the margin and the conditioning, and I confirmed
  the margin part (relative discriminant `−4/(8x_0² + 4) → 0`).
- SCIP's rule also changes if the constraint is rescaled or shifted (for
  example `2w = 2xy`, or `w = xy + c`, which gives `κ ≠ 0`). So Theorem S and
  Proposition S3 hold for that exact form, in the given coordinates.
- Fix: say this in the Summary and in Limits. This is a scoping statement;
  no new analysis is required.

### Optional

- **O1.** Section 3.3 table: the "best (B) found" value at `ε = 10^-5`
  (0.4323) comes from `logs/zB_extended.log`; `logs/sharp_family_k2.log`
  has 0.4310. Cite both logs.
- **O2.** Section 3.3: "for `H ≤ 3·10^3` it equals `√H`". The logged values
  are `√(1 + H)` (31.6386 = √1001).
- **O3.** Section 4: "with `D ≤ 2`, `κ ≤ 10` never below 0.24". The minimum
  in the logs is 0.2397. Also, Section 4 says "15,700 corners" while Section
  8.1 says 15,731 (the logs contain 15,731).
- **O4.** The symbol `κ` denotes both SCIP's constant (Section 4, first
  paragraph) and `cond(P~)` (Theorem S). Rename one of them.
- **O5.** The results list says that "an interval test decides family-(A)
  exactness". Theorem C(3) decides whether `z_K` is *attained*. One boundary
  case is left open: the closed intervals meet only at an endpoint of
  `I_s̄`, so the supremum is undecided there. The note's own Theorem C(3)
  and Summary item 4 are worded correctly.
- **O6.** Corollary A': state "`D ≥ 1`" in the hypothesis. At present it
  appears only in the definition of `γ_D`.
- **O7.** The stored box files for `ρ = 137, …, 200` were written by an
  earlier version of `certify_zB.py`: their header has `"rho": 137.0` and no
  family key. Rerunning the listed command with the current code reproduces
  the same 28,699 boxes and verifies (computation 5). A sentence saying so
  would help.

## Novelty, solver relevance, citations

- **Novelty.** The claims are suitably hedged: short searches, "an
  unsuccessful search does not establish novelty", and Averkov–Basu–Paat
  marked as "abstract only". My one extra web search found no result that
  gives a single-cut ratio for quadratic intersection cuts. This does not
  establish novelty either.
- **Solver relevance.** "Modest" is appropriate. The note says that:
  - intersection cuts are off by default in SCIP 10;
  - the bad corners of Proposition S3 have `w̄ = −1` exactly;
  - nothing was tested on real instances.
- **Citations.** The BCM Lemma 4.14 / Lemma 24 locators and the quoted
  remark are correct.

## Process and hygiene

- The note discloses that the cap of four processes was exceeded: six ran
  for about a minute, two were killed, and nothing from them is reported.
  This needs no change to the note.
- When I started, no process from this stream was running (checked through
  `/proc/*/cwd`).
- My own runs used at most three parallel processes, each with a `timeout`.
  All of them have finished, and none is left running. Temporary files in
  `/tmp` were deleted.

## Checks actually run (reviewer)

All commands were run from `reviews/r1-code/` unless noted otherwise. These
are targeted local checks: no project-wide verification was run, and CI was
not consulted.

| command | outcome |
|---|---|
| `timeout 3000 ./run_indep_boxes.sh` (16 files, 3 in parallel, `timeout 1500` each) | 16/16 `INDEPENDENT CHECK PASS`; counts as in `verify_all.log` (`r1-logs/boxes/`, `r1-logs/run_indep_boxes.out`) |
| `timeout 300 python3 neg_controls.py` | the verifier rejects all three corrupted inputs (`r1-logs/neg_controls.log`) |
| `OMP_NUM_THREADS=1 timeout 1500 python3 indep_checks.py 1` | S1–S6 ALL PASS (`r1-logs/indep_checks_seed1.log`) |
| `OMP_NUM_THREADS=1 timeout 900 python3 indep_thmA_deep.py 7 150` | PASS, `D` up to `1.29·10^4`, 0 violations (`r1-logs/indep_thmA_deep_seed7.log`) |
| `timeout 600 python3 indep_check_found_B.py` | ALL OK: 16 reported (B) sets valid; `s̄` margins `5.9·10^-10` to `1.9·10^-8` (`r1-logs/indep_check_found_B.log`) |
| `timeout 600 python3 exact_feasible_below.py` | ALL VALID: exact sets at `ρ = 6/5, 1, 19/20` (`r1-logs/exact_feasible_below.log`) |
| from `code/`: `timeout 2400 python3 certify_zB.py 137 /tmp/… 2300 90`, then `verify_zB.py` | 28,699 boxes; ALL LEAVES VERIFIED (`r1-logs/rerun_stream/search137.out`, `verify137.out`) |
| from `code/`: `timeout 2400 python3 certify_zB.py 197/200 /tmp/… 2300 100 tan:1/1000:4`, then `verify_zB.py` | 11,132 boxes; ALL LEAVES VERIFIED (`rerun_stream/searchtan.out`, `verifytan.out`) |
| from `code/`: `timeout 900 python3 certify_zB_lower.py`; `timeout 900 python3 certify_support_one.py` | byte-identical to the stream's logs (`rerun_stream/lower.out`, `supp1.out`) |
| read-only: `sed -n 1560,1790p` of SCIP 10.0.3 `nlhdlr_quadratic.c` | Case-4 `xextra = wzlp + kappa + norm` (lines 1665–1666) confirmed |
| `sha256sum` and `pdftotext` of the BCM v6 source; WebFetch of arXiv abs page and v7 PDF | hash matches; Lemma 4.14 and remark verified; Lemma 24 in v7 |
| one WebSearch (single-cut strength of quadratic intersection cuts) | no directly overlapping result found |
| short Python one-liners against `logs/*.log` (tables, SCIP random minima) | numbers match, except O1–O3 |
