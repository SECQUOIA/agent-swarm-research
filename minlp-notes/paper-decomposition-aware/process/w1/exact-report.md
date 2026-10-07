# Cluster `exact`: exact rational output, recovery without uniqueness, polynomial factors

Scope: report Section 5 (`main.tex`, lines 456-695): rational height lemma,
uniqueness implies growth, exact theorem, candidate-denominator acceptance,
finite exact recovery without uniqueness, and the polynomial corollary. I also
read the companion notes listed in the task and `solver/exact_output.py`.

Outputs:

- `process/w1/exact-proofs.tex`: a self-contained replacement for the paper's
  exact-output section, with complete proofs.
- `process/w1/checks/exact_*.py`: exact-arithmetic checks using
  `fractions.Fraction`.

## Verdict

**Sound, with fixes.** Every claim in the cluster is correct as stated in the
report. I found no critical or major mathematical error. The fixes concern:

- a loose and awkwardly normalized height constant;
- two separate determinant arguments that can be merged into one;
- a "finite recovery" theorem phrased in terms of implementation resource caps;
- an understated description of what fails without uniqueness.

Development work produced four new results, all with complete proofs in the
fragment:

1. **A unified height lemma via stationary polytopes.** Positive
   semidefiniteness forces every vertex system to be *principal*. This gives
   the clean bound `R = D * prod_{i in I_C, H_ii>0} (D H_ii)` for both the
   height lemma and the recovery lemma. It needs only the Hessian diagonal,
   and `R <= D (D L)^{|I_C|}`.
2. **A transfer theorem.** Under set growth `F - F* >= g_S dist(x,S)^2`, one
   snap plus one linear-programming solve turns any feasible point with
   certified gap at most `min{g_S/(64 n^2 R^2), 1/(2V^2)}` into an accepted
   exact minimizer. So exactness costs only `poly(I) + log(1/g_S)` bits of
   accuracy, with or without uniqueness.
3. **A negative result for the paper's algorithm.** On
   `F_M(x,z) = x^2 - 2xz + Mz` over `[0,M]^2`:
   - there are two minimizers;
   - set-growth condition number is at most 40;
   - `p = 2`.

   Every stage of FG/CT has certified gap at least
   `max{theta^2 M^2/379, h^2/20}`. Exact output therefore needs
   `2^{Omega(I)}` work. The single-center graded grid, not conditioning,
   blocks a rate without uniqueness.
4. **A positive rate without uniqueness: uniform cells, with unions instead of
   hulls.** For finite `S` with `r = max_i |pi_i(S)|`, every stage has at most
   `12 r (2 sqrt(n kappa_S) + 1)` nodes per coordinate. Exact output then costs
   `O(p (N+|A|) K_S^p) poly(I + log kappa_S)`. This is polynomial for fixed
   `p`, but not fixed-parameter tractable because of the `n^{p/2}` factor. No
   parameter is supplied.

## Issues and fixes

| # | Severity | Location (`main.tex`) | Issue | Fix (verified) |
|---|---|---|---|---|
| 1 | minor | eq. (height), Lemma `lem:height` | `Delta=(2nC_H)^n` is valid: the Leibniz bound covers every minor. It is loose by at least `n^n`, and uses all entries. | Hadamard's inequality for positive definite matrices gives `det P_SS <= prod_{i in S} P_ii`. Use `R = D prod_{i in I_C^+} P_ii` with `P = D*Hessian`. Always smaller than the report's and the code's bound; in 225 random instances it was strictly smaller than the report's in 213 and than the code's in 151 (`exact_check_height.py`). |
| 2 | minor | "Include factors of two from off-diagonal normalization" | Harmless but unnecessary. If `D` clears only the *monomial* coefficients, the stationarity matrix `2H = D*Hessian` and the value numerator `z^T H z` (off-diagonals enter as `2H_ij`) are already integral. The code's choice (`D` clears `A/2`) may double `D` for no gain. | State `D` as a common denominator of the monomial coefficients `H_ii/2`, `H_ij (i<j)`, `b`, `c` and the endpoints, and put `P = D*Hessian`. Then `P` is integral automatically (fragment, eq. `eq:exact-constants`). |
| 3 | minor | Thm `thm:generalfinite`, "nonprincipal minor" | Correct. The vertex system (stationarity rows plus unit bound rows) expands to a possibly nonprincipal minor, bounded by both `(2nC)^n` and the row-norm product. But a separate argument is unnecessary: `H_{J0J0}` is PSD at an optimizer. If `v` is a vertex with free set `T`, then `H_{J0,T}` has trivial kernel, so `H_TT` is positive definite. The principal system `P_TT` therefore determines `v`. | Lemma `lem:statpoly`(c). The same lemma also proves the height corollary: take a vertex of `P(s)` for any minimizer `s`. This replaces the minimum-face argument and makes the height and recovery denominators one statement. Check: 112 stationary-polytope vertices, including singular flat faces; every one had `P_TT` positive definite and common denominator dividing `D det P_TT <= R`. |
| 4 | minor | Thm `thm:exact` | The case `L <= 0` (so `kappa` is undefined) is not mentioned in the theorem, although endpoint DP covers it. Also, coordinatewise reconstruction needs uniqueness, while snapping recovery handles both cases. | Algorithm EX in the fragment uses snapping recovery plus the candidate-denominator test. With `L = 0` the CT stage-0 bound is exact and the test passes. Coordinatewise reconstruction becomes Remark `rem:cf`. Under growth, the selected system is nonsingular whenever recovery is needed, so no LP is needed (Thm `thm:exact`). |
| 5 | minor (presentation) | Thm `thm:generalfinite` | It is stated about "the implementation" with "sufficiently large finite round, stage, table, LP-pivot and time limits" and "the default geometric conditioning schedule". A journal theorem should not depend on implementation caps. | Split it into Theorem `thm:transfer` (quantitative under set growth; existential `epsilon_0` otherwise) and the termination clause of Theorem `thm:exact`. The mathematics is unchanged and verified: snapping is unambiguous (`1/D >= 4 n tau > 2 tau`), active coordinates snap correctly, `phi(s) <= 3/(8R) < 1/R`, and the vertex minimum is `0`. Every solution of the selected system is optimal without nonsingularity. 699 recoveries, 84 with extra snaps and 186 with singular selected systems, all returned exact minimizers that the candidate rule accepted (`exact_check_recovery.py`, using the *smaller* Hadamard `R`, which is the harder test). |
| 6 | minor | Abstract and Section 5.1, "finite exact output ... without a favorable general complexity bound" | Understated and vague. | State the transfer theorem: exactness costs `poly(I) + log(1/g_S)` bits. Add Proposition `prop:twocenters`: the paper's own algorithm needs `2^{Omega(I)}` time on a two-minimizer family with `kappa_S <= 40`. |
| 7 | minor | Corollary (polynomial), "If every coordinate is a native integer" | If fixed *continuous* coordinates are substituted first, `Q_0` must be the denominator of the reduced objective. The report's text implies the original coefficients. | Proposition `prop:lattice`: `Q_0` of the objective after substitution. Its bit length is still `O(dI)`. |
| 8 | minor | Lemma "uniqueness supplies growth" | The pure-integer case (a contradiction once integer labels agree) is implicit. | The fragment states it ("they differ in some continuous coordinate"). |

Verified without change:

- Proposition `prop:candidateheight` (gap `1/(VW)`; the strict inequality is
  needed).
- Value-denominator bound `V = D R^2`.
- Uniqueness implies growth: the polyhedral tangent cone is closed, so
  `x* + t u` is feasible.
- Theorem `thm:exact` thresholds (`1/(4V^2)`, `g/(32R^4)`, window
  `1/(4R^2) < 1/(2R^2)` length).
- Interval curvature certificate: the range of a single monomial on a box is
  exact as the product of coordinate power ranges; summing upper endpoints is
  valid.
- Native-integer lattice rule (`q = 1 + ceil(log2 Q_0)`).
- `x^3 - 6x` on `[1,2]`: `F'' = 6x <= 12`, `F - F* = (x - sqrt2)^2 (x + 2 sqrt2)`,
  so `g = 1 + 2sqrt2 >= 3`, optimizer `sqrt2`, value `-4 sqrt2`. Checked in
  exact `Q(sqrt2)` arithmetic.
- `x^4`: no positive growth constant.
- Binary-exponent example `x^2 - x^{2^k}/2 + y^2`: `F(1/2, 0)` has reduced
  denominator `2^{2^k+1}`.
- `exact_output.py`:
  - computes heights from original data with a valid row-norm bound;
  - uses the correct strict acceptance inequality;
  - computes `tau` with `n` = all coordinates, which is conservative;
  - matches the snapping/LP recovery of the proof.

## Classical versus new

- **Rational height of QP optima: classical.** Vavasis (IPL 36 (1990) 73-77)
  showed that QP is in NP via a polynomial-size global minimizer obtained from
  a linear system. The original was not available locally. The statement is
  confirmed by two secondary sources:
  - Del Pia-Dey-Molinaro, *Math. Program.* 162 (2017) 225-240, Theorem 3
    (verified in the local full text, p.3);
  - Ahmadi-Zhang, arXiv:2008.05558 §2.2: "there will always be a local
    minimizer that has rational entries with polynomial bitsize [Vavasis]".

  What is new here is the explicit diagonal constant, obtained by
  Hadamard–PSD (standard tools). It matters because the stopping threshold
  must be computable. DDM's extension to unbounded integers is not needed on
  bounded boxes.
- **Continued-fraction reconstruction and polynomial-time LP: classical**
  (GLS Theorem 5.1.9 and Theorem 6.4.12, verified in the local full text).
  Rounding near-optimal LP solutions to exact optima is likewise classical
  (GLS Ch. 6).
- **Candidate-denominator acceptance: elementary.** It is the standard
  rational-separation argument, applied with the candidate's own
  denominator.
- **Snapping recovery near a nonunique optimal set: closest prior work is
  active-constraint identification.**
  - Facchinei-Fischer-Kanzow, "On the accurate identification of active
    constraints" (title and abstract verified; I recall the venue as SIAM J.
    Optim. 1998 but did not check it).
  - Burke's work on active-constraint identification (not checked).

  Those results identify the active set near an *isolated* stationary point.
  The lemma here works near arbitrary optimal sets (continua, ties), snaps a
  possibly larger set, and proves through rational heights that some
  minimizer satisfies every snap. I found no prior statement of this exact
  lemma for nonconvex box QP; it comes from the repository's
  proximal-recovery note. Treat it as likely new but elementary.
- **Transfer theorem, negative two-minimizer proposition, uniform-cell rate:
  new as stated** (repository work; not found in prior art). The uniform-cell
  theorem is the box analogue of the report's TU "unions of retained cells".
  It avoids the TU section's pseudopolynomial initial mesh because boxes need
  no alignment.
- **Set growth always holds** for QP on polytopes: Luo-Sturm 2000, Theorem
  3.3 (verified in the local package), extended to mixed boxes by finitely
  many slices.
- **Interval curvature certificate: standard.** Interval Hessian bounds are
  used in alphaBB (Adjiman-Dallwig-Floudas-Neumaier 1998).
- **Relation to NP results (question e).** Vavasis and DDM certify `F* <= t`
  (short optimal points). Box-QP decision is NP-complete: in NP by Vavasis,
  and strongly NP-hard at treewidth 2 by Del Pia-Khajavirad 2026. So short,
  efficiently checkable certificates of `F* >= t` for all instances would put
  an NP-complete problem in coNP. Theorem `thm:exact` supplies such
  lower-bound certificates of size `f(p,kappa) poly(I)` for bounded
  `(p,kappa)`, and their validity does not use the promise. This is the
  precise sense in which exact output adds something beyond NP membership.

## Placement recommendations

| Result | Recommendation | Reason |
|---|---|---|
| Lemma `lem:statpoly` + Cor `cor:height` (Hadamard height) | main | One short lemma serves both height and recovery; explicit computable constant |
| Prop `prop:accept` (candidate denominator) | main | One line; makes all certificates uniqueness-free |
| Lemma `lem:snap` + Thm `thm:transfer` | main | Clean statement of what exactness costs, with and without uniqueness; replaces the implementation-flavoured finite theorem |
| Lemma `lem:unique-growth` | main (short) | Needed to say every unique instance has finite `kappa` |
| Thm `thm:exact` (FPT exact output) | main | Headline corollary of the approximation theorem |
| Prop `prop:twocenters` | main, in the structural-limits section | Shows uniqueness is needed for the paper's algorithm; strong, short, fits "structural limits" |
| Thm `thm:cells` + Lemma `lem:cells` | appendix (state as a remark in the main text) | Rate without uniqueness, but only polynomial for fixed `p`; parallels the TU unions section |
| Remark `rem:grading` | remark | Explains that grading turns `sqrt n` into `log n` (FPT) at the cost of uniqueness |
| Remark `rem:np` | remark / related work | Precise relation to Vavasis and DDM |
| Remark `rem:cf` (continued fractions) | drop or footnote | Superseded by snapping |
| Remark `rem:heights` | remark (short) | Records that the report's and code's constants are also valid |
| Lemma `lem:intcurv`, Prop `prop:lattice`, Cor `cor:poly`, Ex `ex:polylimits` | main (short subsection) | Needed for the polynomial claim and its limits |
| Report's Thm `thm:generalfinite` (implementation caps) | drop as stated | Content is preserved by `thm:transfer` and the termination clause of `thm:exact` |

## Open questions: what succeeded and what failed

1. **(c) Rate without uniqueness — resolved in part.**
   - Refuted for the paper's algorithm (Prop `prop:twocenters`).
   - Proved with a modified algorithm (Thm `thm:cells`, polynomial for fixed
     `p`).
   - Clean transfer statement proved (Thm `thm:transfer`).
   - Still open: `f(p, kappa_S, r) poly(I)` for finite `S`, that is, removing
     `n^{p/2}`. I tried graded grids around several centers, using retained
     endpoints as centers. The contraction recursion does not close: the
     correction energy involves `sum_i dist(s_i, C_i)^2` for the optimizer `s`
     nearest the new minimizer. With centers chosen per coordinate, this is
     only bounded by `n * (per-coordinate radius)^2`, which feeds back as
     `n^2`, then `n^3`, and so on, instead of one Euclidean distance as in the
     single-center proof.
   - Linear tie-breaking (`F + eta w^T x`) also fails. It makes the minimizer
     unique only generically, and the new growth constant is `O(eta)`, so
     `kappa` becomes exponential in the bits of `eta`.
   - For a continuum `S`, no accuracy-independent bound is possible for cell
     unions: the cell count grows like `|pi_i(S)|/h`.
2. **(a)/(b) Height and nonprincipal minors — resolved.** Verified, and
   simplified to principal minors with the diagonal Hadamard bound.
3. **(d) Polynomial items — verified.** Remaining open obligations, as in the
   report:
   - exact algebraic output for continuous polynomial coordinates;
   - rational lattices whose metric differs from the native one;
   - binary-encoded exponents or circuits.

   None was attempted beyond the counterexamples.
4. **Integer analogue of Prop `prop:twocenters` — not proved.** A variant with
   `x, z` integer appears to behave the same way. The floor steps add case
   analysis (unit intervals carry no correction), so I make no claim.

## Checks run (targeted; not CI)

All commands were run from `paper-decomposition-aware/process/w1/checks/`, and
all passed:

- `python3 exact_check_height.py`
  - 225 instances (random mixed `n <= 3` plus five hand-built singular or flat
    cases);
  - 253 enumerated optimizers;
  - 39 flat optimal pieces with 112 stationary-polytope vertices;
  - checked: `beta <= F*` sandwich, denominators dividing `D det P_SS <= R`,
    `den(F*) <= V`, `P_{J0J0}` PSD, vertex `P_TT` positive definite, and
    `R_had <= R_code`, `R_had <= R_report`.
- `python3 exact_check_recovery.py`
  - 699 snapping recoveries (84 with extra snaps, 186 with singular selected
    systems);
  - all returned exact minimizers, accepted by `F(x) - beta < 1/(VW)`.
- `python3 exact_check_single_center.py`
  - 288 grid configurations (`M` in {16, 40, 100}; `theta` in
    {1/4, 1/8, 1/16}; four values of `h`; random centers; `L_z` in {0, 2}),
    all satisfying `beta <= -max{theta^2 M^2/379, h^2/20}`;
  - full FG runs with filtering for 10 stages keep the box `[0,M]^2`, and the
    gap never falls below the bound (it stays above 1);
  - sampled growth ratio is at least 0.50, so `g = 1/20` is conservative.
- `python3 exact_check_union_cells.py`
  - uniform-cell UC on `F_64`: counts stay at 6 nodes per coordinate, and the
    gap reaches `2.4e-4` at stage 11;
  - on the four-optimum "wells" instance: at most 11 nodes per coordinate;
  - both are below `K_S`;
  - end to end, UC plus REC plus acceptance gave the exact minimizer at stage
    7 (`F_64`, `R=2`, `V=4`) and stage 6 (wells, `R=32`, `V=4096`).
- `python3 exact_check_polynomial.py`
  - 40,230 samples confirming that the interval curvature bound dominates the
    second derivative, with exact single-monomial ranges;
  - 1,500 lattice-rule acceptances;
  - the `x^3 - 6x` identity in `Q(sqrt2)` arithmetic.
- `pdflatex` of `exact-proofs.tex` wrapped with `paper-decomposition-aware/macros.tex`
  compiled with no errors and no overfull boxes. The only warnings were
  undefined references to labels in other sections and citations. The
  temporary build directory was removed.

Bibliography note: `DelPiaDeyMolinaro2017` is not in the report's
`references.bib`. Its metadata are in the local package
`literature/papers/pia2016-mixed-integer-quadratic-programming-is`: *Math.
Program.* 162(1-2):225-240, DOI 10.1007/s10107-016-1036-0, arXiv 1407.4798.
GLS theorem numbers 5.1.9 and 6.4.12 and Luo-Sturm Theorem 3.3 were checked in
the local full texts. The Vavasis 1990 original was not checked.
