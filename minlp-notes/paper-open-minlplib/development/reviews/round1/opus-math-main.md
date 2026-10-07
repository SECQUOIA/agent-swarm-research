# Round 1 review: mathematics of the main paper (opus-math-main)

Scope: Sections 2, 4, 5, 6, 7, 8 and Appendices A and B (`G-proofs-split.tex`) of
`build/main.pdf`, read against the supplement proofs that they cite (B1–B9, C, E,
F, H). I checked every definition, lemma, proposition, theorem and proof sketch in
this scope, the extended-value arithmetic of Section 4 and Appendix B, the
minimization/maximization conventions, and whether each main-text statement matches
the proof in the supplement.

## Verdict

**Minor revision.** I found no mathematical error that invalidates a theorem, bound,
gap or refutation. Every proof in Appendix B is correct, including the edge cases
of the extended-value conventions. The issues below are:

- scope statements that the paper itself contradicts, with unproved reading (c) claims (issue 1);
- an over-attribution to Proposition 4.3(c) and an imprecise citation of Lemma 4.1(d) (issues 3 and 13);
- a counting error and an overstated "needed" (issues 5 and 6);
- a definition stated twice in two different forms, and conventions that are left unstated or misattributed (issues 2, 4, 7 and 8);
- internal inconsistencies between the main text and the supplement (issues 9–12).

Blockers: 0. Major: 0. Minor: 13.

## Targeted checks I ran (copies in /tmp; no repository script was run)

All of these agree with the paper.

- **`lnts` optimum, recomputed at 50 digits.** I solved `g(ν)=0` and evaluated `N·9/(20C(ν*))`. The values are
  0.55466876493867889…, 0.554595401166911161…, 0.55457701610308367…
  and 0.554572413700687108…. Each lies inside the corresponding bracket of Theorem 4.7 (`thm:lnts-opt`).
  - The root properties used in App. B.6 also hold: `g(0) = −20N²/81`, the limit of `g` is positive, and `g' > 0`.
- **`dtoc5` point (`dtoc5_point.txt.gz`, SHA-256 prefix `6e963788`).**
  - All 49,999 rows hold exactly in `Fraction` arithmetic.
  - `min_{t≤T−2} û_t = 1.46e-5 > 0`, so `λ̂_t < 0`.
  - At 120 digits: `f(x̂) = 5.3896721191811404674239664991362718688313134098…` and
    `q(λ̂) = 5.3896721191811404674239664991362718688313126893…`, so `f − q = 7.2051e-43`.
    This matches Theorem 4.9 (`thm:dtoc5-bracket`) and its displays.
- **`camshape100` and `camshape200` in exact rationals.**
  - Checks (K1)–(K4) pass.
  - The floor and ceiling of `v_n` at 14 decimals equal the values in the paper.
  - The point `(E, d^E)` satisfies every row and bound exactly.
  - `max U_m = 605.9087` for n = 800, and `nφ/π ≈ 0.3995`.
- **Lemma 8.4 (`lem:scip-cube`).** `fl(0.343)−2^-53 < fl(0.7)^3 < fl(0.343)−2^-54`; the residual is `−1.664·2^-54`. For the other station values, the tightest binary64 interval contains `fl(ℓ^k)`.
- **`fm336`/`tiny2` case analysis** (supplement S6): checked by hand. The value is `187/270`, and `0.2−1.6√0.8 > −1.337`.
- **`hvycrash` (Proposition 5.13).**
  - `κ = 0.0065106 < 6.52e-3` and `−cos 2.6 = 0.85689`.
  - The backward recursion gives `θ_0 = 2.65651 > 2.6`.
  - `50·fl(4.37e-3) − 0.2185 = −1.24e-17`.
- **Exact fractions.**
  - `39157472136693483/2^47 = 278.2305737745608…`.
  - `7447080719734483·2^-41 = 3386.540229…`.
- **Gaps for all 43 instances**, recomputed from the exact ends in `numbers.json`: every Δ and δ display is a correct upward rounding. The borderline case is `eg_int_s`, with `δ = 9.9969e-10 ≤ 1.00e-9`.
- **Margins in Sections 7–8.** The BARON margins and relative errors, the CAMINO margins and percentages, the QPLIB margins and the smallest class (i) margin (`1.1158 u(s)`) are all correct.
- **Lemma S1.22 (`lem:chain-calibration`).** At 40 digits on 20,000 random `(a,b,h,H)`, `min(rhs−lhs) ≥ 7.6e-13`. The algebra of its proof also checks out by hand.
- **Proofs re-derived by hand:**
  - Lemmas 4.1 and 4.2;
  - Propositions 4.3, 4.4 and 4.5, including the finite-potential construction for "SP is the largest B" and the extended-value conventions (F1), (F2);
  - Lemma B.2 (`lem:lnts-elim`), Proposition B.3 (`prop:lnts-support`) and the proof of `thm:lnts-opt`;
  - Proposition 4.8 (`prop:dtoc5-identity`);
  - Lemmas 5.1 and 5.2 (camshape);
  - the Krawczyk theorem (Theorem 6.1) and its supplement proof, including nonsingularity "from the widths";
  - Propositions 6.2 and 6.3 (Lindemann–Weierstrass in Baker's form);
  - Lemma S4.1 (`lem:audit-display`) (a) and (b);
  - Proposition 7.1 (`prop:audit-refute`);
  - Proposition 5.7 (`prop:pf-duality`) and the bus-30 identity `W_22 = F(P_g,Q_g,W_30)`;
  - the Hessian recursion for `pindyck`, its strong-concavity bound and the uniqueness corollary (supplement S1, `pindyck` subsection, which handles existence and interiority correctly);
  - the `etamac` majorant;
  - the scaling identity and Lagrangian bound for ex6_2 (`ex62`);
  - the `catmix` nonnegativity, chord-minorant and transport lemmas;
  - the `ann` affine-form and weak-duality lemmas;
  - the KAN projection and perturbation lemmas.

## Issues

### 1. [minor] The scope of "all claims concern reading (b)" is false as stated, and the reading (c) infeasibility claims are not proved

- **Where:** `sections/02-semantics.tex:44`, `:53–54`; `sections/A-semantics.tex:81`, `:84`; `sections/B6-powerflow.tex:316`.
- **Problem.** Line 44 says, in italics: "All claims in this paper concern reading (b)." The paper makes several claims about other readings:
  - Theorem 4.12 (`thm:catmix-bound`, `04-split.tex:293`) and Proposition S1.34 (`prop:catmix-transport`) claim results for reading (a).
  - Proposition 8.3 (`prop:scip-reproducers`)(b) and Lemma 8.4 (`lem:scip-cube`) (`08-solvers.tex:62–74`) claim results for binary64 data.
  - Corollary S4.9 (`cor:audit-tolerance`)(b) claims results for the GAMS form.
- **The same contradiction within Remark 2.3.** Remark 2.3(2) says "We claim nothing for reading (c) except …". The next sentence claims something for reading (c): "Our points of dtoc5, chain, powerflow and waterno2 are not feasible under reading (c)".
- **The reading (c) claim is not proved.** App. A.4 justifies it only by "because they satisfy equality rows whose coefficients change". That is not a proof: changed coefficients need not change the row value. The `waterno2` case is proved (B8, via the speed identities). The `dtoc5`, `chain` and `powerflow` cases are not.
- **Fix, line 44.** Replace with: "*Unless a statement names another reading, every claim in this paper concerns reading (b).* The exceptions are the transfer of the `catmix` bounds to reading (a) (Proposition S1.34), the statements about reading (c) in Remark 2.3(2) and App. A.4, and the statements about binary64 data of small derived models in Section 8.2."
- **Fix, line 53.** Replace with: "For reading (c) we claim only the following: `lukvle10` (integer data) is the same model; our `lnts` points stay exactly feasible (only inactive angle bounds change); and our points of `dtoc5`, `chain`, `powerflow` and `waterno2` are not feasible (App. A.4)."
- **Fix, App. A line 84.** Give the one-line proofs.
  - *`dtoc5`.* `fl(8e-5) = 4 fl(2e-5)` because scaling by a power of two commutes with rounding. So under reading (c), row 0 has residual `(fl(h)−h)(4y_0²−u_0) ≠ 0`, since `fl(2e-5) ≠ 2e-5` and `u_0 ≈ 8.06 ≠ 4`.
  - *`chain`.* η = 1/(2N) is not dyadic. The rows under reading (c) leave the residuals `(η−fl(η))(u_i+u_{i+1})`. These cannot all vanish, because `Σ_i η(u_i+u_{i+1}) = x_N − x_0 = 2`.
  - *`powerflow`.* For example, the branch 2–30 flow row has the residual `(b−fl(b)) w^I_{30,2} ≠ 0`, because `P_g ≈ 6.714 ≠ 0`.

  If these proofs are not added, label the claim "(computed)".

### 2. [minor] The unit `u(σ)` is defined twice, and the two definitions differ

- **Where:** `sections/02-semantics.tex:148`; `sections/07-audit.tex:115`.
- **Problem.**
  - Section 2.4 defines `u(σ)` as "the unit of the last displayed digit".
  - Section 7.2 redefines it as "the largest power of ten of which `d(s)` is an integer multiple".
  - The two differ for strings with trailing integer zeros (e.g. "1200": 1 versus 100).
- **Why it matters.** Lemma S4.1 (`lem:audit-display`)(a), and with it the 10/9 claim at `07-audit.tex:122`, is correct only for the Section 7 definition. With the "last displayed digit" definition, a value that was truncated to a multiple of 100 and printed as "1200" violates `|b−d(s)| < (10/9)u(s)`.
- **Fix.** Define `u` once in Section 2.4: "We write `u(σ)` for the largest power of ten of which `d(σ)` is an integer multiple (`d(σ) ≠ 0`); for a string whose last digit is nonzero, this is the unit of its last displayed digit, for example `u(0.84624567) = 10^-8`." Then shorten `07-audit.tex:115` to a back-reference.

### 3. [minor] "By part (c)" covers more than Proposition 4.3(c) proves

- **Where:** `sections/04-split.tex:85`; compare `sections/G-proofs-split.tex:197–202`.
- **Problem.**
  - Proposition 4.3(c) (`prop:split-affine`) assumes that each `z*_t` is an interior point of `K_t`.
  - When the dynamics rows stay in the bags, `K_t` contains equality rows and has empty interior. Appendix B says so: "(c) does not apply as stated".
  - The main text nevertheless writes "By part (c), exact affine slopes are the copy-row multipliers of a minimizer, or its discrete costates when the dynamics rows stay in the bags".
  - The costate case is only sketched in Appendix B ("Written in coordinates in which these rows are eliminated, the same argument gives …"). That sketch also needs the eliminated bag to have interior points, which fails, for example, on bang arcs where `|u| = 1/5`.
- **No certificate depends on this.** Each certificate checks its own slopes.
- **Fix.** Replace with: "By part (c), exact affine slopes are the copy-row multipliers of a minimizer at which every bag is interior; when the dynamics rows stay in the bags, the analogous computation after eliminating them yields the discrete costates (Appendix B.4). So the affine certificates below take their slopes from a local KKT point; validity never depends on this choice."

### 4. [minor] Hypothesis H0 presents implementation properties as consequences of IEEE 754

- **Where:** `sections/02-semantics.tex:163`.
- **Problem.** "In particular, … the conversion of a rational number or decimal string to binary64 are correctly rounded" does not follow from IEEE 754.
  - IEEE 754 has no rational-to-binary64 operation.
  - For decimal strings, IEEE 754 (§5.12.2) requires correct rounding only up to an implementation-defined number of significant digits `H ≥ M+3` (20 for binary64).
- **What the proofs actually rely on.** They rely on properties of CPython: `float(str)` and `Fraction.__float__`.
- **Fix.** Replace "In particular" with: "and, in addition, the conversion of a rational number (Python `Fraction`) or of a decimal string to binary64 is correctly rounded (true of CPython's `float`), `nextafter` returns …".

### 5. [minor] Wrong count of inequalities that define Ω for `ann_cumene_tanh`

- **Where:** `sections/05-other.tex:331`.
- **Problem.** "Ω ⊂ 𝒰 is cut out by 723 inequalities: the bounds of 722 determined variables and the purity row." All 722 determined variables have two-sided bounds, so Ω is defined by 1,445 one-sided inequalities:
  - 250 tanh outputs in [−1,1];
  - 70 normalized inputs in [−1,1];
  - 380 variables in ±10^6;
  - 22 variables in [−10^9, 10^6].

  This is also the form `σ_j(x_{v_j}−b_j) ≥ 0` that Lemma S1.75 (`lem:ann-duality`) uses.
- **Fix.** "… is cut out by the two-sided bounds of 722 determined variables and the purity row (1,445 one-sided inequalities)."

### 6. [minor] The 39-bus sketch states that shifts "are needed", and applies Proposition 5.7 to multipliers it does not cover

- **Where:** `sections/05-other.tex:188–189`; compare `sections/B6-powerflow.tex:276–284` (Remark S1.55, `rem:pf-anglefree`) and `:223`.
- **Problem 1.** "The shifts are needed because the eigenvalues of `A(w)` come in pairs."
  - For `powerflow0039p`, Remark S1.55 shows that setting the angle-row multipliers to 0 gives a positive definite `A(w)` with `ε = 0` on every leaf, and a larger bound. So no shift is needed there.
  - Paired eigenvalues explain why rounding can create a negative pair. They do not make a shift necessary.
- **Problem 2.** The sketch applies Proposition 5.7 (`prop:pf-duality`), stated for `𝒬`, "with that leaf's stored multipliers". The stored `powerflow0039p` multipliers belong to `𝒬_i^∠`, which includes angle rows.
- **Fix.** "Proposition 5.7 applies verbatim to these leaf relaxations. Because the eigenvalues of `A(w)` come in pairs (Proposition S1.51, `prop:pf-double`), rounding near-optimal multipliers can create a negative pair. The stored `powerflow0039r` certificate absorbs one, about `−6.07·10^-10`, with `ε = 10^-9`. The stored `powerflow0039p` certificate uses `ε = 10^-8` and tiny angle-row multipliers; with those set to zero, it needs no shift (Remark S1.55). All shifts cost less than `4.4·10^-7`."

### 7. [minor] The QPLIB margins assume round-to-nearest display without saying so

- **Where:** `sections/08-solvers.tex:28`; `sections/H-solvers.tex:113–121` (Proposition S6.1, `prop:qplib-copies`).
- **Problem.** "Every number that displays as `−4.2774` is at most `−4.27735`" holds for round-to-nearest only. Under the paper's own convention, Hypothesis H, the bound is `< −4.2773` instead.
  - The margins would then be at least `3.112·10^-3` and `1.547·10^-4` (exact optima ≥ `−4.2741871514717434` and `−4.2841462678046117`), not `3.162·10^-3` and `1.552·10^-4`.
  - Part (b) still holds, because the deficit bounds `−4.2771731888` and `−4.2842973949` exceed `−4.2773` and `−4.284301`.
- **Fix.** Either say "rounded to nearest" explicitly, or state the margins under Hypothesis H as "at least `3.11·10^-3` and `1.54·10^-4`" and the thresholds as `−4.2773` and `−4.284301`.

### 8. [minor] The maximization case is missing from "U is the upper end"

- **Where:** `sections/02-semantics.tex:78`.
- **Problem.** "In practice `U` is the upper end of a rigorous enclosure of `f(x*)`." For `pricing050` (maximization), `U` is the lower end. Definition 2.4(b) (`def:sem-certificate`) says `sU ≥ s f(x*)`, and Section 6 (`06-points.tex:7`) states the reversal.
- **Fix.** Add "(the lower end for maximization)".

### 9. [minor] The `lnts` row of Table 5 (`tab:points`) gives the width of the wrong point, and it conflicts with Remark S1.2

- **Where:** `tables/tab-points.tex:16`; `sections/06-points.tex:73`; `sections/B1-lnts-lukvle10.tex:124`; `sections/C-points.tex:156–162`.
- **Problem.** Section 6.2 says that `U` for `lnts` comes from the attaining point. That point is enclosed in arithmetic [E], with width `< 1.11·10^-91`. The table row instead shows the following, which belongs to the Krawczyk points:
  - arithmetic "[I], 110 digits";
  - width "`< 3·10^-109`".
- **Inconsistency with Remark S1.2 (`rem:lnts-stored`).** That remark says the Krawczyk points' objective enclosures come "from 60-digit enclosures of h" and "contain the rational enclosure of v*". An enclosure narrower than `3·10^-109` cannot contain an enclosure of width about `10^-91`.
- **Fix.** Split the row. Attaining point: [E], width `< 1.11·10^-91`. Krawczyk points: [I] at 110 digits, with their actual width. Then make Remark S1.2 state the same width and precision.

### 10. [minor] Appendix A and supplement B9 describe the data reading of the second `ann` code differently

- **Where:** `sections/A-semantics.tex:46`; `sections/B9-ann-kan.tex:137`; `tables/tab-trust.tex:36`.
- **Problem.** Appendix A says that the second `ann_cumene_tanh` bounding code "uses a rounded reading". B9 says that its decimal constants "are enclosed outward", which is an outward reading. The trust table says "outward / rounded".
- **Fix.** Use one description in all three places.

### 11. [minor] Appendix A and supplement B4 disagree on how the `chain` GAMS and OSIL forms were compared

- **Where:** `sections/A-semantics.tex:68` (Table 9, `tab:sem-gams`, "evaluation … no difference"); `sections/B4-chain-catmix.tex:23` ("The `.gms` files define the same model exactly").
- **Problem.**
  - Remark 2.3(1) counts 21 exact comparisons, and `chain` is not one of them.
  - B4 nevertheless asserts exact identity, apparently from reading the files.
- **Fix.** Either move `chain50`–`chain400` to the "exact: identical" row (and update "21" to "25") if an exact comparison was run, or weaken B4 to "agree in the step, length and end values, and agree at sample points (Table 9)".

### 12. [minor] The replay tiers are defined by cost, but the assignments do not follow that definition

- **Where:** `sections/02-semantics.tex:203`; compare `sections/10-reproducibility.tex` (Table 8, `tab:repro-tiers`) and the certificate boxes.
- **Problem.**
  - The definition is "Tier 1 takes seconds to minutes, Tier 2 up to one hour, and Tier 3 hours or more".
  - Yet `ex6_2_5` (258 s) and `lukvle10` (about 5 min) are in Tier 2, while `pindyck` (322 s) is in Tier 1.
  - `catmix` (20–46 min per instance) is in Tier 3, and its certificate box says "Tier 3; 20.2 to 46.1 min per instance".
- **Fix.** Define the tiers by what Table 8 actually uses. For example: "Tier 1, bound computations without search; Tier 2, searches that finish in under an hour per instance or part; Tier 3, searches that need hours in total". Alternatively, reassign `ex6_2_5`, `lukvle10`, the 39-bus `powerflow` leaves and `catmix`.

### 13. [minor] The `lnts` support bound is not literally Lemma 4.1(d) in its infeasibility form

- **Where:** `sections/04-split.tex:162`; `sections/G-proofs-split.tex:339`.
- **Problem.** The infeasibility form of Lemma 4.1(d) (`lem:split-bound`) requires every `F_t` to vanish. At a fixed `h`, the cost of `lnts` is the constant `Nh`, not 0. Appendix B says "the cost is zero", which is true only after the constant is dropped.
- **Fix.** "At a fixed step `h` the objective is the constant `Nh`; dropping it, …, this is Lemma 4.1(d) in its infeasibility form."

## Optional notation remark (not counted)

Several symbols carry three or more unrelated meanings within the scope reviewed. Each use is defined locally, so nothing is wrong, but a referee will notice:

- `h`: the step length; the functions `h_k` of Lemma 4.1(d); the `waterno2` inflow `h_t`; the equality rows `h(x)` in Section 2.
- `φ`: the split functions; the audit's upper end `φ`; the KAN edge functions `φ_e`.
- `B`: `B(φ;K')`; the camshape `B_j`; the `optcdeg2` bound `B`; the chain `B_N`.
- `β`: `β(h)` (`lnts`); `β_c`; `β_[a,b]`; `β(w,ε)`.
- `C`: `C(ν)`; the Krawczyk matrix `C`.

Renaming the functions in Lemma 4.1(d) (for example `ψ_k`) and the audit's `φ` (for example `ϕ̄` or `U_s`) would remove the two clashes nearest to each other.
